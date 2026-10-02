import "../setup/MessageDispatcher_single.spec";

// MD-AC-01: only an admin can grant or revoke admin rights on the message dispatcher.
rule acMdWardSetMovesOnlyForAWard(env e, method f, calldataarg args, address u)
    filtered { f -> !EXCLUDED_FUNCTION_MD(f) } {

    setupMessageDispatcher(e);

    mathint senderWardBefore = _MessageDispatcher.wards(e.msg.sender);
    mathint wardBefore = _MessageDispatcher.wards(u);

    f(e, args);

    assert(_MessageDispatcher.wards(u) != wardBefore => senderWardBefore == 1,
        "only a ward can grant or revoke ward rights");
}

// MD-AC-02: only an admin can change the contracts the dispatcher routes messages through.
rule acMdWiringMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MD(f) } {

    setupMessageDispatcher(e);

    mathint senderWardBefore = _MessageDispatcher.wards(e.msg.sender);
    address envoyBefore = _MessageDispatcher.envoy();
    address gatewayBefore = _MessageDispatcher.gateway();
    address adapterBefore = _MessageDispatcher.multiAdapter();
    address spokeBefore = _MessageDispatcher.spokeHandler();
    address hubBefore = _MessageDispatcher.hubHandler();

    f(e, args);

    assert((_MessageDispatcher.envoy() != envoyBefore
            || _MessageDispatcher.gateway() != gatewayBefore
            || _MessageDispatcher.multiAdapter() != adapterBefore
            || _MessageDispatcher.spokeHandler() != spokeBefore
            || _MessageDispatcher.hubHandler() != hubBefore) => senderWardBefore == 1,
        "only a ward can repoint a contract the dispatcher routes to");
}

// MD-AC-03: only an admin can make the dispatcher deliver or send a message.
rule acMdNoUnwardedCallerReachesANeighbour(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MD(f) } {

    setupMessageDispatcher(e);

    mathint senderWardBefore = _MessageDispatcher.wards(e.msg.sender);
    mathint callsBefore = DOWNSTREAM_CALLS();

    f(e, args);

    assert(DOWNSTREAM_CALLS() != callsBefore => senderWardBefore == 1,
        "only a ward's call reaches a downstream contract");
}
