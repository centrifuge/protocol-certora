import "../setup/Gateway_base.spec";

// GW-AC-01: only an admin, a manager of the message's pool, or a retry can pass a message to the processor.
rule acGwOnlyAWardOrThePoolsManagerFeedsTheProcessor(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    bool wardBefore = _Gateway.wards(e.msg.sender) == 1;
    mathint fedBefore = ghostGwEscCount + ghostGwHandleCount;

    f(e, args);

    bool fed = ghostGwEscCount + ghostGwHandleCount > fedBefore;

    assert(fed => (wardBefore || _Gateway.manager(ghostGwPoolAsked64, e.msg.sender)
        || f.selector == sig:_Gateway.retry(uint16,bytes).selector),
        "no one but a ward, a pool manager or a retrier feeds the processor");
}

// GW-AC-02: only an admin can grant or revoke admin rights on the gateway.
rule acGwOnlyAWardMovesTheWardBit(env e, method f, calldataarg args, address u)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    bool wardBefore = _Gateway.wards(e.msg.sender) == 1;
    mathint bitBefore = _Gateway.wards(u);

    f(e, args);

    assert(_Gateway.wards(u) != bitBefore => wardBefore, "a non-ward never changes anyone's ward status");
}

// GW-AC-03: only an admin can appoint or remove a pool manager.
rule acGwOnlyAWardMovesAManagerSeat(env e, method f, calldataarg args, Gateway.PoolId p, address u)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    bool wardBefore = _Gateway.wards(e.msg.sender) == 1;
    bool seatBefore = _Gateway.manager(p, u);

    f(e, args);

    assert(_Gateway.manager(p, u) != seatBefore => wardBefore, "a non-ward never changes who manages a pool");
}

// GW-AC-04: only an admin can repoint the adapter, the processor or the gas model.
rule acGwOnlyAWardRepointsADependency(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    bool wardBefore = _Gateway.wards(e.msg.sender) == 1;
    address adapterBefore = _Gateway.adapter();
    address processorBefore = _Gateway.processor();
    address gasModelBefore = _Gateway.messageGas();

    f(e, args);

    bool repointed = _Gateway.adapter() != adapterBefore || _Gateway.processor() != processorBefore
        || _Gateway.messageGas() != gasModelBefore;

    assert(repointed => wardBefore, "a non-ward leaves adapter, processor and gas model in place");
}

// GW-AC-05: outside a batch envelope, only an admin books a debt, and only an admin or a repay dispatches.
rule acGwOnlyAWardSends(env e, method f, calldataarg args, uint16 c, bytes32 h)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    bool wardBefore = _Gateway.wards(e.msg.sender) == 1;
    mathint copiesBefore = _Gateway.underpaid[c][h].counter;
    mathint sentBefore = ghostAdSendCount;

    f(e, args);

    assert(_Gateway.underpaid[c][h].counter > copiesBefore => wardBefore, "a non-ward never adds an unpaid batch copy");
    assert(ghostAdSendCount > sentBefore => (wardBefore || f.selector == sig:_Gateway.repay(uint16,bytes,address).selector),
        "only a ward or a repay makes the adapter send");
}

// GW-AC-06: a failed message is cleared only by an admin, a manager of its pool, or a retry.
rule acGwOnlyAWardOrThePoolsManagerClearsAFailedMessage(env e, method f, calldataarg args, uint16 c, bytes32 h)
    filtered { f -> !EXCLUDED_FUNCTION_GW(f) } {

    setupGateway(e);

    bool wardBefore = _Gateway.wards(e.msg.sender) == 1;
    mathint recordBefore = _Gateway.failedMessages(c, h);

    f(e, args);

    assert(_Gateway.failedMessages(c, h) < recordBefore => (wardBefore
        || _Gateway.manager(ghostGwPoolId64[h], e.msg.sender)
        || f.selector == sig:_Gateway.retry(uint16,bytes).selector),
        "no one but a ward, a pool manager or a retrier lowers a failure count");
}
