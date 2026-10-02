import "setup/Gateway_base.spec";
import "setup/Gateway_batching.spec";
import "setup/Gateway_callback.spec";

// --- state_transitions ---

// GW-ST-03: withBatch included, a failure count rises only by handle, falls only by retry or clear.
rule stGwFailureLedgerMovesOnlyThroughItsOwnEntriesAcrossBatches(env e, method f, calldataarg args, uint16 c,
    bytes32 h) filtered { f -> !f.isView && !f.isPure && !f.isFallback } {

    setupGateway(e);

    mathint recordBefore = _Gateway.failedMessages(c, h);

    f(e, args);

    assert(_Gateway.failedMessages(c, h) > recordBefore => f.selector == sig:_Gateway.handle(uint16,bytes).selector,
        "only a handle raises a failure count");
    assert(_Gateway.failedMessages(c, h) < recordBefore
        => f.selector == sig:_Gateway.retry(uint16,bytes).selector
            || f.selector == sig:_Gateway.clearFailedMessage(uint16,bytes).selector,
        "only a retry or a clear lowers a failure count");
}

// GW-ST-04: withBatch included, no call made with no batch open leaves a batch flag set.
rule stGwNoCallLeavesABatchOpen(env e, method f, calldataarg args)
    filtered { f -> !f.isView && !f.isPure && !f.isFallback } {

    setupGateway(e);
    require(!GA_IS_BATCHING() && !GA_IS_SENDING_BATCH() && GA_BATCHER() == 0, "SAFE: transient storage starts empty");

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(!reverted => !GA_IS_BATCHING() && !GA_IS_SENDING_BATCH() && GA_BATCHER() == 0,
        "all batching flags are clear once a call returns");
    assert(reverted => !GA_IS_BATCHING() && !GA_IS_SENDING_BATCH() && GA_BATCHER() == 0,
        "a refused call leaves no batching flag set");
}

// --- high_level ---

// GW-HL-07: a batch envelope writes no persistent gateway field, under any key.
rule hlGwWithBatchWritesNoPersistentField(env e, bytes data, uint256 callbackValue, bool shortForm, address who,
    Gateway.PoolId p, uint16 c, bytes32 h) {

    setupGateway(e);

    uint256 wardBefore = _Gateway.wards[who];
    bool managerBefore = _Gateway.manager[p][who];
    uint256 failedBefore = _Gateway.failedMessages[c][h];
    uint64 underpaidCounterBefore = _Gateway.underpaid[c][h].counter;
    uint128 underpaidGasBefore = _Gateway.underpaid[c][h].gasLimit;
    address adapterBefore = _Gateway.adapter;
    address processorBefore = _Gateway.processor;
    address gasModelBefore = _Gateway.messageGas;

    if (shortForm) {
        _Gateway.withBatch(e, data, _RefundSink);
    } else {
        _Gateway.withBatch(e, data, callbackValue, _RefundSink);
    }

    assert(_Gateway.wards[who] == wardBefore && _Gateway.manager[p][who] == managerBefore
            && _Gateway.failedMessages[c][h] == failedBefore
            && _Gateway.underpaid[c][h].counter == underpaidCounterBefore
            && _Gateway.underpaid[c][h].gasLimit == underpaidGasBefore && _Gateway.adapter == adapterBefore
            && _Gateway.processor == processorBefore && _Gateway.messageGas == gasModelBefore,
        "no ward, manager, failure, debt or wiring moves across a batch envelope");
}

// --- reachability ---

// GW-RC-08: a batch can still be sent out after the protocol is paused mid batch, in one transaction.
rule rcGwFlushDispatchesAfterAMidBatchPause(env e, uint16 c, bytes m, address refund) {

    setupGateway(e);
    require(!ghostGwPaused, "SCOPE: the protocol is live when the batch opens");
    require(!GA_IS_BATCHING() && !GA_IS_SENDING_BATCH() && GA_BATCHER() == 0 && ghostGwLocCount == 0,
        "SCOPE: a fresh transaction, no batch open");

    uint64 p = ghostGwPoolId64[keccak256(m)];
    require(ghostGwBufLen256[gwBatchSlotKey(c, p)] == 0 && ghostGwGasSlot256[gwGasSlotKey(c, p)] == 0,
        "SCOPE: the message's batch starts empty");

    mathint sentBefore = ghostAdSendCount;

    _BatchInitiator.runSendThenPause(e, c, m, refund);

    satisfy(ghostGwPaused && ghostAdSendCount == sentBefore + 1 && ghostAdLastSendCid16 == c,
        "the flush dispatches despite a pause thrown by the callback");
}
