// Gateway. High level: pause, failure counts, value splits, capped calls, paid sends.

import "../setup/Gateway_base.spec";
import "../setup/Gateway_batching.spec";

// GW-HL-01: an unbatched send pays exactly the quote and refunds the rest, or books a debt and refunds all.
rule hlGwUnbatchedSendSplitsTheValueExactly(env e, uint16 c, bytes m, bool unpaidMode) {

    setupGateway(e);
    require(!GA_IS_BATCHING(), "SCOPE: a send outside a batch");
    require(e.msg.sender != _RefundSink && _Gateway.adapter() != _RefundSink,
        "SCOPE: the refund receiver is not the payer or adapter");

    mathint sinkBefore = nativeBalances[_RefundSink];
    mathint sentBefore = ghostAdSendCount;

    _Gateway.send(e, c, m, unpaidMode, _RefundSink);

    mathint refunded = nativeBalances[_RefundSink] - sinkBefore;
    bool dispatched = ghostAdSendCount == sentBefore + 1;
    bool booked = ghostAdSendCount == sentBefore;

    assert(dispatched || booked, "an unbatched send either dispatches once or books the debt");
    assert(dispatched => (ghostAdLastSendValue256 == ghostAdLastQuote256
        && refunded == e.msg.value - ghostAdLastQuote256),
        "a dispatched send forwards the quote and refunds the remainder");
    assert(booked => refunded == e.msg.value, "a booked send refunds all it carried");
}

// GW-HL-02: a send inside an open batch takes no value, refunds nothing and dispatches nothing.
rule hlGwBatchedSendTakesNoValue(env e, uint16 c, bytes m, bool unpaidMode) {

    setupGateway(e);
    require(GA_IS_BATCHING(), "SCOPE: a send inside an open batch");

    mathint sinkBefore = nativeBalances[_RefundSink];
    mathint sentBefore = ghostAdSendCount;

    _Gateway.send(e, c, m, unpaidMode, _RefundSink);

    assert(e.msg.value == 0 && nativeBalances[_RefundSink] == sinkBefore && ghostAdSendCount == sentBefore,
        "a batched send carries no ether and moves none");
}

// GW-HL-03: a repay forwards exactly the adapter's quote and refunds the rest.
rule hlGwRepaySplitsTheValueExactly(env e, uint16 c, bytes b) {

    setupGateway(e);
    require(e.msg.sender != _RefundSink && _Gateway.adapter() != _RefundSink,
        "SCOPE: the refund receiver is not the payer or adapter");

    mathint sinkBefore = nativeBalances[_RefundSink];
    mathint sentBefore = ghostAdSendCount;

    _Gateway.repay(e, c, b, _RefundSink);

    mathint refunded = nativeBalances[_RefundSink] - sinkBefore;

    assert(ghostAdSendCount == sentBefore + 1 && ghostAdLastSendValue256 == ghostAdLastQuote256
        && refunded == e.msg.value - ghostAdLastQuote256,
        "one dispatch at the quoted fee, the change back to the refund address");
}

// GW-HL-04: each inbound processor call gets its budget less the reserve, and the last carries no ether.
rule hlGwProcessorCallIsCappedBelowTheReserve(env e, uint16 c, bytes batch) {

    setupGateway(e);
    require(!ghostGwEscCapBroken, "SAFE: the cap check starts clear");

    mathint callsBefore = ghostGwEscCount;

    _Gateway.handle(e, c, batch);

    assert(!ghostGwEscCapBroken, "each processor call gets the budget minus the reserve");
    assert(ghostGwEscCount > callsBefore => (ghostGwEscTarget == _Gateway.processor() && ghostGwEscValue256 == 0),
        "the last capped call goes to the processor and forwards no ether");
}

// GW-HL-05: up to three deep, each inbound message is source checked before it is priced and processed.
rule hlGwEachProcessedSubMessageWasSourceCheckedFirst(env e, uint16 c, bytes batch) {

    setupGateway(e);
    require(!ghostGwSrcArmed && !ghostGwSrcPairBroken, "SAFE: the source checks start clear");

    _Gateway.handle(e, c, batch);

    assert(!ghostGwSrcPairBroken, "each message is source checked before its gas lookup and its call");
}

// GW-HL-06: a paid unbatched send goes out at once on its own network, payload and gas, booking no debt.
rule hlGwPaidUnbatchedSendReachesTheAdapterInTheSameCall(env e, uint16 cid, bytes m, address refund) {

    setupGateway(e);
    require(!GA_IS_BATCHING(), "SCOPE: a send outside a batch");

    bytes32 h = keccak256(m);
    mathint sentBefore = ghostAdSendCount;
    mathint copiesBefore = _Gateway.underpaid[cid][h].counter;

    _Gateway.send(e, cid, m, false, refund);

    assert(ghostAdSendCount == sentBefore + 1 && ghostAdLastSendAdapter == _Gateway.adapter()
        && ghostAdLastSendCid16 == cid && ghostAdLastSendHash == h,
        "the message goes out once, through the adapter, to its network");
    assert(ghostAdLastSendGasLimit256 == ghostGwOverallGas128[cid][h],
        "the message goes out with the gas limit the gas model quotes");
    assert(_Gateway.underpaid[cid][h].counter == copiesBefore, "a paid send books no debt");
}

// GW-HL-08: a batched send appends only to its own network and pool batch, registering it once when empty.
rule hlGwBatchedSendAppendsToItsOwnRegionOnly(env e, uint16 c, bytes m, bool unpaidMode, address refund, uint16 c2,
    uint64 p2) {

    setupGateway(e);
    require(GA_IS_BATCHING(), "SCOPE: a send inside an open batch");

    bytes32 h = keccak256(m);
    uint64 p = ghostGwPoolId64[h];
    require(c2 != c || p2 != p, "SCOPE: another network and pool pair");

    bytes32 ownBuffer = gwBatchSlotKey(c, p);
    bytes32 ownGas = gwGasSlotKey(c, p);
    bytes32 otherBuffer = gwBatchSlotKey(c2, p2);
    bytes32 otherGas = gwGasSlotKey(c2, p2);
    require(ownBuffer != otherBuffer && ownGas != otherGas, "SAFE: distinct pairs hash to distinct slots");

    mathint ownLength = ghostGwBufLen256[ownBuffer];
    mathint ownRunningGas = ghostGwGasSlot256[ownGas] % 2^128;
    mathint otherLength = ghostGwBufLen256[otherBuffer];
    bytes32 otherToken = ghostGwBufTok[otherBuffer];
    mathint otherRunningGas = ghostGwGasSlot256[otherGas];
    uint256 locators = ghostGwLocCount;

    _Gateway.send(e, c, m, unpaidMode, refund);

    assert(ghostGwBufLen256[ownBuffer] == ownLength + m.length
        && ghostGwGasSlot256[ownGas] == ownRunningGas + ghostGwOverallGas128[c][h],
        "the message and its gas are added to its own batch");
    assert(ghostGwBufLen256[otherBuffer] == otherLength && ghostGwBufTok[otherBuffer] == otherToken
        && ghostGwGasSlot256[otherGas] == otherRunningGas,
        "no other batch's buffer or gas total moves");
    assert(ownLength == 0 => (ghostGwLocCount == locators + 1 && ghostGwLocAt[locators] == GW_LOCATOR(c, p)),
        "an empty batch is registered once, under its own locator");
    assert(ownLength != 0 => ghostGwLocCount == locators, "a batch already registered is not registered again");
}

// GW-HL-09: inside an open batch the unpaid flag changes nothing, and neither setting books a debt.
rule hlGwTheUnpaidFlagIsInertInsideABatch(env e, uint16 c, bytes m, address refund, uint16 c2, bytes32 h2,
    uint16 c3, uint64 p3) {

    setupGateway(e);
    require(GA_IS_BATCHING() && !GA_IS_SENDING_BATCH(), "SCOPE: a send inside an open batch, not yet flushing");
    require(ghostAdLastEstimateHash != keccak256(m), "SAFE: a sentinel quote record, reset by every estimate");

    bytes32 h = keccak256(m);
    uint64 p = ghostGwPoolId64[h];
    require(c3 != c || p3 != p, "SCOPE: another network and pool pair");
    bytes32 buffer = gwBatchSlotKey(c, p);
    bytes32 gasSlot = gwGasSlotKey(c, p);
    bytes32 otherBuffer = gwBatchSlotKey(c3, p3);
    bytes32 otherGas = gwGasSlotKey(c3, p3);
    require(buffer != otherBuffer && gasSlot != otherGas, "SAFE: distinct pairs hash to distinct slots");
    uint256 pushedAt = ghostGwLocCount;
    mathint debtBefore = _Gateway.underpaid[c2][h2].counter;
    mathint debtGasBefore = _Gateway.underpaid[c2][h2].gasLimit;
    mathint sentBefore = ghostAdSendCount;
    bytes32 quotedBefore = ghostAdLastEstimateHash;

    storage init = lastStorage;

    _Gateway.send@withrevert(e, c, m, true, refund) at init;
    bool unpaidReverted = lastReverted;
    storage afterUnpaid = lastStorage;
    mathint unpaidLength = ghostGwBufLen256[buffer];
    bytes32 unpaidToken = ghostGwBufTok[buffer];
    mathint unpaidGas = ghostGwGasSlot256[gasSlot];
    mathint unpaidLocators = ghostGwLocCount;
    bytes32 unpaidPushed = ghostGwLocAt[pushedAt];
    mathint unpaidOtherLength = ghostGwBufLen256[otherBuffer];
    bytes32 unpaidOtherToken = ghostGwBufTok[otherBuffer];
    mathint unpaidOtherGas = ghostGwGasSlot256[otherGas];
    bool unpaidBookedNothing = _Gateway.underpaid[c2][h2].counter == debtBefore
        && _Gateway.underpaid[c2][h2].gasLimit == debtGasBefore;

    _Gateway.send@withrevert(e, c, m, false, refund) at init;
    bool paidReverted = lastReverted;

    assert(unpaidReverted == paidReverted, "the flag decides no refusal");
    assert(!paidReverted => (unpaidLength == ghostGwBufLen256[buffer] && unpaidToken == ghostGwBufTok[buffer]
        && unpaidGas == ghostGwGasSlot256[gasSlot] && unpaidLocators == ghostGwLocCount
        && unpaidPushed == ghostGwLocAt[pushedAt]),
        "both settings write the same batch, gas total and locator entry");
    assert(!paidReverted => (unpaidOtherLength == ghostGwBufLen256[otherBuffer]
        && unpaidOtherToken == ghostGwBufTok[otherBuffer] && unpaidOtherGas == ghostGwGasSlot256[otherGas]),
        "both settings leave another batch and its gas total alike");
    assert(!paidReverted => afterUnpaid[_Gateway] == lastStorage[_Gateway],
        "both settings leave the gateway's storage alike");
    assert(unpaidBookedNothing && _Gateway.underpaid[c2][h2].counter == debtBefore
        && _Gateway.underpaid[c2][h2].gasLimit == debtGasBefore,
        "neither setting books a debt");
    assert(ghostAdSendCount == sentBefore && ghostAdLastEstimateHash == quotedBefore,
        "neither setting asks the adapter for anything");
}

// GW-HL-10: repointing a dependency changes exactly the one it names and leaves the other two alone.
rule hlGwFileWritesExactlyTheNamedDependency(env e, bytes32 what, address instance) {

    setupGateway(e);

    address adapterBefore = _Gateway.adapter();
    address processorBefore = _Gateway.processor();
    address gasModelBefore = _Gateway.messageGas();

    _Gateway.file(e, what, instance);

    address adapterAfter = _Gateway.adapter();
    address processorAfter = _Gateway.processor();
    address gasModelAfter = _Gateway.messageGas();

    assert(adapterAfter == (what == FILE_ADAPTER_GW() ? instance : adapterBefore),
        "the adapter moves exactly when it is the dependency named");
    assert(processorAfter == (what == FILE_PROCESSOR_GW() ? instance : processorBefore),
        "the processor moves exactly when it is the dependency named");
    assert(gasModelAfter == (what == FILE_MESSAGE_GAS_GW() ? instance : gasModelBefore),
        "the gas model moves exactly when it is the dependency named");
}

// GW-HL-11: a retry or a clear lowers its own failure count by one and touches no other.
rule hlGwRetryAndClearRetireExactlyOneOwnCopy(env e, bool viaRetry, uint16 c, bytes m, uint16 c2, bytes32 h2) {

    setupGateway(e);

    bytes32 h = keccak256(m);
    mathint ownBefore = _Gateway.failedMessages(c, h);
    mathint otherBefore = _Gateway.failedMessages(c2, h2);

    if (viaRetry) {
        _Gateway.retry(e, c, m);
    } else {
        _Gateway.clearFailedMessage(e, c, m);
    }

    mathint ownAfter = _Gateway.failedMessages(c, h);
    mathint otherAfter = _Gateway.failedMessages(c2, h2);

    assert(ownAfter == ownBefore - 1, "the message's own failure record drops by exactly one copy");
    assert((c2 != c || h2 != h) => otherAfter == otherBefore, "no other failure record moves");
}

// GW-HL-12: a retry passes the processor exactly the message it names, once, under the network it names.
rule hlGwRetryForwardsItsOwnMessageOnce(env e, uint16 c, bytes m) {

    setupGateway(e);

    mathint retriedBefore = ghostGwHandleCount;

    _Gateway.retry(e, c, m);

    assert(ghostGwHandleCount == retriedBefore + 1 && ghostGwLastHandleCid16 == c
        && ghostGwLastHandleHash == keccak256(m),
        "a retry forwards its own message to the processor exactly once");
}

// GW-HL-13: a one-message batch books one failure under its own key exactly when its processing failed.
rule hlGwAFailedOneMessageBatchBooksOneCopyUnderItsKey(env e, uint16 c, bytes batch, uint16 c2, bytes32 h2) {

    setupGateway(e);

    mathint callsBefore = ghostGwEscCount;
    mathint recordBefore = _Gateway.failedMessages(c2, h2);

    _Gateway.handle(e, c, batch);

    mathint recordAfter = _Gateway.failedMessages(c2, h2);
    bool bookedHere = !ghostGwEscLastSuccess && c2 == c && h2 == ghostGwLastProcessedHash;

    assert(ghostGwEscCount == callsBefore + 1 => recordAfter == recordBefore + (bookedHere ? 1 : 0),
        "in a one-message batch only a failed message's own count rises, by one");
}

// GW-HL-14: repaying the last unpaid copy of a batch deletes its debt record, gas included, and no other.
rule hlGwRepayOfTheLastCopyDeletesItsRow(env e, uint16 c, bytes b, uint16 c2, bytes32 h2) {

    setupGateway(e);

    bytes32 h = keccak256(b);
    require(_Gateway.underpaid[c][h].counter == 1, "SCOPE: the last pending copy of the batch");
    mathint otherCounterBefore = _Gateway.underpaid[c2][h2].counter;
    mathint otherGasBefore = _Gateway.underpaid[c2][h2].gasLimit;

    _Gateway.repay(e, c, b, _RefundSink);

    assert(_Gateway.underpaid[c][h].counter == 0 && _Gateway.underpaid[c][h].gasLimit == 0,
        "the drained record keeps neither a copy nor gas terms");
    assert((c2 != c || h2 != h) => (_Gateway.underpaid[c2][h2].counter == otherCounterBefore
        && _Gateway.underpaid[c2][h2].gasLimit == otherGasBefore),
        "no other underpaid record moves");
}

// GW-HL-15: an unpaid send outside a batch books a short payment as one debt copy and refunds every wei.
rule hlGwAnUnpaidShortfallBooksOneCopyAndRefundsAll(env e, uint16 c, bytes m) {

    setupGateway(e);
    require(!GA_IS_BATCHING(), "SCOPE: a send outside a batch, GW-HL-09 covers batches");
    require(e.msg.sender != _RefundSink && _Gateway.adapter() != _RefundSink,
        "SCOPE: the refund receiver is not the payer or adapter");

    bytes32 h = keccak256(m);
    mathint counterBefore = _Gateway.underpaid[c][h].counter;
    mathint sinkBefore = nativeBalances[_RefundSink];
    mathint sentBefore = ghostAdSendCount;

    _Gateway.send(e, c, m, true, _RefundSink);

    bool booked = ghostAdSendCount == sentBefore;

    assert(booked <=> e.msg.value < ghostAdLastQuote256, "the send is booked exactly when it carried less than the quote");
    assert(booked => (nativeBalances[_RefundSink] == sinkBefore + e.msg.value
        && _Gateway.underpaid[c][h].counter == counterBefore + 1
        && _Gateway.underpaid[c][h].gasLimit == ghostGwOverallGas128[c][h]),
        "a booked send refunds everything and adds one copy at its gas");
}

// GW-HL-16: an inbound batch of up to three messages books exactly its failed calls, under its own network.
rule hlGwHandleBooksItsFailuresUnderItsSourceNetwork(env e, uint16 c, bytes batch, bytes32 h, uint16 c2) {

    setupGateway(e);

    mathint recordBefore = _Gateway.failedMessages(c, h);
    mathint failuresBefore = ghostGwEscFailedOf[h];
    mathint otherBefore = _Gateway.failedMessages(c2, h);

    _Gateway.handle(e, c, batch);

    assert(_Gateway.failedMessages(c, h) - recordBefore == ghostGwEscFailedOf[h] - failuresBefore,
        "each message's failure count rises by its failed calls exactly");
    assert(c2 != c => _Gateway.failedMessages(c2, h) == otherBefore, "no other network's record moves");
}

// GW-HL-17: message details come only from the processor, gas limits only from the gas model.
rule hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);
    require(ghostGwFramer == _Gateway.processor() && ghostGwGasModel == _Gateway.messageGas(),
        "SAFE: the checks track the processor and gas model in use");
    require(!ghostGwFramingStray && !ghostGwGasStray, "SAFE: the reader checks start clear");

    f(e, args);

    assert(!ghostGwFramingStray, "the gateway reads message details only from its processor");
    assert(!ghostGwGasStray, "the gateway reads gas limits only from its gas model");
}

// GW-HL-18: the gateway prices every inbound message for its own network.
rule hlGwHandlePricesEachMessageForItsOwnNetwork(env e, uint16 c, bytes batch) {

    setupGateway(e);
    require(ghostGwPricingCidExpected16 == _Gateway.localCentrifugeId() && !ghostGwPricedForeign,
        "SAFE: the pricing check starts clear");

    _Gateway.handle(e, c, batch);

    assert(!ghostGwPricedForeign, "no message is priced for another network");
}
