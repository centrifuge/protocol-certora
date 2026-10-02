import "../setup/MessageProcessor_base.spec";

// MP-AC-01: only an admin can grant or revoke admin rights over the processor.
rule acMpWardSetMovesOnlyForAWard(env e, method f, calldataarg args, address u)
    filtered { f -> !EXCLUDED_FUNCTION_MP(f) } {

    setupMessageProcessor(e);

    mathint senderWardBefore = _MessageProcessor.wards(e.msg.sender);
    mathint wardBefore = _MessageProcessor.wards(u);

    f(e, args);

    assert(_MessageProcessor.wards(u) != wardBefore => senderWardBefore == 1,
        "a non-ward caller never changes any ward bit");
}

// MP-AC-02: only an admin can rewire the contracts the processor routes messages to.
rule acMpWiringMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MP(f) } {

    setupMessageProcessor(e);

    mathint senderWardBefore = _MessageProcessor.wards(e.msg.sender);
    address gatewayBefore = _MessageProcessor.gateway();
    address adapterBefore = _MessageProcessor.multiAdapter();
    address spokeBefore = _MessageProcessor.spokeHandler();
    address hubBefore = _MessageProcessor.hubHandler();
    address envoyBefore = _MessageProcessor.envoy();

    f(e, args);

    assert((_MessageProcessor.gateway() != gatewayBefore
            || _MessageProcessor.multiAdapter() != adapterBefore
            || _MessageProcessor.spokeHandler() != spokeBefore
            || _MessageProcessor.hubHandler() != hubBefore
            || _MessageProcessor.envoy() != envoyBefore) => senderWardBefore == 1,
        "a non-ward caller never moves a routing pointer");
}
