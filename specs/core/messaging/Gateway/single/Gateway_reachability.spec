// Gateway. Reachability: manager delivery, retry races, mid-flush repays, debts, clears.

import "../setup/Gateway_base.spec";
import "../setup/Gateway_batching.spec";

// GW-RC-01: a pool manager who is not an admin can execute an inbound message with no adapter quorum.
rule rcGwAPoolManagerInjectsAMessageNoQuorumApproved(env e, uint16 c, bytes batch) {

    setupGateway(e);
    require(_Gateway.wards(e.msg.sender) != 1, "SCOPE: the caller is not a ward");

    mathint callsBefore = ghostGwEscCount;
    mathint recordBefore = _Gateway.failedMessages(c, keccak256(batch));

    _Gateway.handle(e, c, batch);

    satisfy(ghostGwEscCount == callsBefore + 1 && ghostGwEscLastSuccess
        && _Gateway.failedMessages(c, keccak256(batch)) == recordBefore
        && _Gateway.manager(ghostGwPoolAsked64, e.msg.sender),
        "a non-ward pool manager gets one message processed");
}

// GW-RC-02: an outsider can retry a freshly failed message before an admin clears it, so the clear fails.
rule rcGwPermissionlessRetryPreemptsAClear(env e0, env e1, env e2, uint16 c, bytes m) {

    setupGateway(e0);
    setupEnv(e1);
    setupEnv(e2);
    require(_Gateway.failedMessages(c, keccak256(m)) == 0, "SCOPE: no failure of the message on record yet");
    require(_Gateway.wards(e0.msg.sender) == 1, "SCOPE: a ward delivers the message");
    require(_Gateway.wards(e1.msg.sender) != 1, "SCOPE: the retrier is not a ward");
    require(_Gateway.wards(e2.msg.sender) == 1 && e2.msg.sender != e1.msg.sender, "SCOPE: another account, a ward, clears");
    require(e2.msg.value == 0, "SCOPE: the clear carries no ether");

    mathint callsBefore = ghostGwEscCount;

    _Gateway.handle(e0, c, m);

    bool processingFailed = ghostGwEscCount == callsBefore + 1 && !ghostGwEscLastSuccess;
    bool retrierManages = _Gateway.manager(ghostGwPoolAsked64, e1.msg.sender);
    mathint retriedBefore = ghostGwHandleCount;

    _Gateway.retry(e1, c, m);

    _Gateway.clearFailedMessage@withrevert(e2, c, m);
    bool clearRefused = lastReverted;

    satisfy(processingFailed && !retrierManages && clearRefused && ghostGwHandleCount == retriedBefore + 1
        && _Gateway.failedMessages(c, keccak256(m)) == 0,
        "a non-ward retry succeeds first and the ward's clear is refused");
}

// GW-RC-03: a repay can succeed and dispatch while a batch is being sent out.
rule rcGwRepayIsUnguardedMidDispatch(env e, uint16 c, bytes b, address refund) {

    setupGateway(e);
    require(GA_IS_SENDING_BATCH() && GA_IS_BATCHING(), "SCOPE: a repay during a batch flush");

    bytes32 h = keccak256(b);
    mathint copiesBefore = _Gateway.underpaid[c][h].counter;
    mathint sentBefore = ghostAdSendCount;

    _Gateway.repay(e, c, b, refund);

    satisfy(GA_IS_SENDING_BATCH() && _Gateway.underpaid[c][h].counter == copiesBefore - 1
        && ghostAdSendCount == sentBefore + 1,
        "one unpaid copy is retired and dispatched mid flush");
}

// GW-RC-04: an unpaid send outside a batch can book its shortfall and refund every wei it carried.
rule rcGwUnpaidShortfallIsBookedAndRefunded(env e, uint16 c, bytes m) {

    setupGateway(e);
    require(!GA_IS_BATCHING(), "SCOPE: a send outside a batch");
    require(e.msg.sender != _RefundSink && _Gateway.adapter() != _RefundSink,
        "SCOPE: the refund receiver is not the payer or adapter");

    bytes32 h = keccak256(m);
    mathint copiesBefore = _Gateway.underpaid[c][h].counter;
    mathint sinkBefore = nativeBalances[_RefundSink];
    mathint sentBefore = ghostAdSendCount;

    _Gateway.send(e, c, m, true, _RefundSink);

    satisfy(ghostAdSendCount == sentBefore && e.msg.value > 0
        && nativeBalances[_RefundSink] == sinkBefore + e.msg.value
        && _Gateway.underpaid[c][h].counter == copiesBefore + 1,
        "a send with ether is booked as debt and fully refunded");
}

// GW-RC-05: an inbound batch of two different messages can be processed whole, each with its own call.
rule rcGwMultiMessageBatchIsDeliveredWhole(env e, uint16 c, bytes batch) {

    setupGateway(e);

    mathint callsBefore = ghostGwEscCount;

    _Gateway.handle(e, c, batch);

    satisfy(ghostGwEscCount == callsBefore + 2
        && ghostGwEscHashAt[callsBefore + 1] != ghostGwEscHashAt[callsBefore + 2],
        "two distinct messages of one batch both reach the processor");
}

// GW-RC-06: a second unpaid copy of a batch can replace the gas terms the first copy booked.
rule rcGwUnderpaidGasLimitIsOverwrittenByTheLatestSend(env e1, env e2, env eF, uint16 c, bytes m, address model) {

    setupGateway(e1);
    setupEnv(e2);
    setupEnv(eF);
    require(!GA_IS_BATCHING(), "SCOPE: sends outside a batch");

    bytes32 h = keccak256(m);
    require(_Gateway.underpaid[c][h].counter == 0 && _Gateway.underpaid[c][h].gasLimit == 0,
        "SCOPE: the batch has no debt on record yet");

    _Gateway.send(e1, c, m, true, _RefundSink);

    mathint firstGas = _Gateway.underpaid[c][h].gasLimit;

    _Gateway.file(eF, FILE_MESSAGE_GAS_GW(), model);
    _Gateway.send(e2, c, m, true, _RefundSink);

    satisfy(_Gateway.underpaid[c][h].counter == 2 && _Gateway.underpaid[c][h].gasLimit != firstGas,
        "after a gas model change, a second unpaid send overwrites the booked gas limit");
}

// GW-RC-07: a send inside an open batch can be queued with no payment and no adapter call.
rule rcGwBatchedSendDefersPaymentIsReachable(env e, uint16 c, bytes m, address refund) {

    setupGateway(e);
    require(GA_IS_BATCHING(), "SCOPE: a send inside an open batch");

    bytes32 buffer = gwBatchSlotKey(c, ghostGwPoolId64[keccak256(m)]);
    mathint lengthBefore = ghostGwBufLen256[buffer];
    mathint sentBefore = ghostAdSendCount;

    _Gateway.send(e, c, m, false, refund);

    satisfy(e.msg.value == 0 && ghostAdSendCount == sentBefore && ghostGwBufLen256[buffer] == lengthBefore + m.length,
        "the message is queued unpaid, nothing sent to the adapter");
}

// GW-RC-10: an inbound batch can reach the processor, priced for this network.
rule rcGwHandlePricesAndForwardsAMessage(env e, uint16 c, bytes batch) {

    setupGateway(e);
    require(ghostGwPricingCidExpected16 == _Gateway.localCentrifugeId() && !ghostGwPricedForeign,
        "SAFE: the pricing check starts clear");

    mathint callsBefore = ghostGwEscCount;

    _Gateway.handle(e, c, batch);

    satisfy(ghostGwEscCount > callsBefore && !ghostGwPricedForeign,
        "a message is priced for the local network and forwarded");
}
