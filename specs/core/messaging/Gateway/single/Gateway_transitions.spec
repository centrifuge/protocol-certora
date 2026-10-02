import "../setup/Gateway_base.spec";
import "../setup/Gateway_batching.spec";

// --- variable_transitions ---

// GW-VT-01: the adapter, processor and gas model change only through a file call.
rule vtGwDependenciesMoveOnlyUnderFile(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    address adapterBefore = _Gateway.adapter();
    address processorBefore = _Gateway.processor();
    address gasModelBefore = _Gateway.messageGas();

    f(e, args);

    assert(_Gateway.adapter() != adapterBefore || _Gateway.processor() != processorBefore
        || _Gateway.messageGas() != gasModelBefore
        => f.selector == sig:_Gateway.file(bytes32,address).selector,
        "only a file repoints a dependency");
}

// GW-VT-02: only handle, retry, send and repay check the pause, so it never blocks any other entry.
rule vtGwOnlyTheTrafficEntriesConsultThePause(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    mathint readsBefore = ghostGwPauseReads;

    f(e, args);

    assert(ghostGwPauseReads != readsBefore => TRAFFIC_ENTRY_GW(f),
        "the pause is read by handle, retry, send and repay alone");
}

// --- state_transitions ---

// GW-ST-01: only handle and retry reach the processor, and only send and repay an adapter.
rule stGwTheProcessorAndAdapterAreReachedOnlyThroughTheirEntries(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    mathint retriedBefore = ghostGwHandleCount;
    mathint processedBefore = ghostGwEscCount;
    mathint sentBefore = ghostAdSendCount;

    f(e, args);

    assert(ghostGwHandleCount != retriedBefore => f.selector == sig:_Gateway.retry(uint16,bytes).selector,
        "only a retry hands a message to the processor directly");
    assert(ghostGwEscCount != processedBefore => f.selector == sig:_Gateway.handle(uint16,bytes).selector,
        "only a handle runs the capped processor call");
    assert(ghostAdSendCount != sentBefore
        => f.selector == sig:_Gateway.send(uint16,bytes,bool,address).selector
            || f.selector == sig:_Gateway.repay(uint16,bytes,address).selector,
        "only a send or a repay dispatches to an adapter");
}

// GW-ST-02: inside an open batch no call but a repay quotes or dispatches, leaving delivery to the flush.
rule stGwAnOpenBatchReachesTheAdapterOnlyThroughRepay(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);
    require(GA_IS_BATCHING() && !GA_IS_SENDING_BATCH(), "SCOPE: a call inside an open batch, not yet flushing");

    mathint sentBefore = ghostAdSendCount;
    bytes32 quotedBefore = ghostAdLastEstimateHash;

    f(e, args);

    assert(ghostAdSendCount != sentBefore || ghostAdLastEstimateHash != quotedBefore
        => f.selector == sig:_Gateway.repay(uint16,bytes,address).selector,
        "inside an open batch only a repay asks the adapter for anything");
}

// GW-ST-05: in an open batch only a send moves a batch, its gas total or the locator list.
rule stGwBatchRegionsMoveOnlyUnderSend(env e, method f, calldataarg args, bytes32 k)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);
    require(GA_IS_BATCHING() && !GA_IS_SENDING_BATCH(), "SCOPE: a call inside an open batch, not yet flushing");

    mathint lengthBefore = ghostGwBufLen256[k];
    bytes32 tokenBefore = ghostGwBufTok[k];
    mathint gasBefore = ghostGwGasSlot256[k];
    mathint locatorsBefore = ghostGwLocCount;

    f(e, args);

    assert(ghostGwBufLen256[k] != lengthBefore || ghostGwBufTok[k] != tokenBefore || ghostGwGasSlot256[k] != gasBefore
        || ghostGwLocCount != locatorsBefore
        => f.selector == sig:_Gateway.send(uint16,bytes,bool,address).selector,
        "only a send moves an open batch, its gas total or the locator list");
    assert(ghostGwLocCount <= locatorsBefore + 1, "a call registers at most one batch");
}

// GW-ST-06: inside an open batch no call books a debt.
rule stGwAnOpenBatchBooksNoDebt(env e, method f, calldataarg args, uint16 c, bytes32 h)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);
    require(GA_IS_BATCHING() && !GA_IS_SENDING_BATCH(), "SCOPE: a call inside an open batch, not yet flushing");

    mathint debtBefore = _Gateway.underpaid[c][h].counter;

    f(e, args);

    assert(_Gateway.underpaid[c][h].counter <= debtBefore, "no debt copy is booked while a batch is open");
}

// GW-ST-07: a debt copy is booked only by a send and retired only by a repay, and only they move its gas.
rule stGwUnderpaidMovesOnlyThroughSendAndRepay(env e, method f, calldataarg args, uint16 c, bytes32 h)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    mathint counterBefore = _Gateway.underpaid[c][h].counter;
    mathint gasBefore = _Gateway.underpaid[c][h].gasLimit;

    f(e, args);

    assert(_Gateway.underpaid[c][h].counter > counterBefore
        => f.selector == sig:_Gateway.send(uint16,bytes,bool,address).selector,
        "only a send books a debt copy");
    assert(_Gateway.underpaid[c][h].counter < counterBefore
        => f.selector == sig:_Gateway.repay(uint16,bytes,address).selector,
        "only a repay retires a debt copy");
    assert(_Gateway.underpaid[c][h].gasLimit != gasBefore
        => f.selector == sig:_Gateway.send(uint16,bytes,bool,address).selector
            || f.selector == sig:_Gateway.repay(uint16,bytes,address).selector,
        "only a send or a repay moves a debt's gas terms");
}
