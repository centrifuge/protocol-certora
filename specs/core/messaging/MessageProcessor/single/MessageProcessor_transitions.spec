import "../setup/MessageProcessor_base.spec";

// --- state_transitions ---

// MP-ST-01: the processor's admins move only under rely or deny, its routing only under file.
rule stMpOwnStateMovesOnlyUnderItsAdminEntries(env e, method f, calldataarg args, address u)
    filtered { f -> !EXCLUDED_FUNCTION_MP(f) } {

    setupMessageProcessor(e);

    mathint wardBefore = _MessageProcessor.wards(u);
    address gatewayBefore = _MessageProcessor.gateway();
    address adapterBefore = _MessageProcessor.multiAdapter();
    address spokeBefore = _MessageProcessor.spokeHandler();
    address hubBefore = _MessageProcessor.hubHandler();
    address envoyBefore = _MessageProcessor.envoy();

    f(e, args);

    assert(_MessageProcessor.wards(u) != wardBefore
        => f.selector == sig:_MessageProcessor.rely(address).selector
            || f.selector == sig:_MessageProcessor.deny(address).selector,
        "a ward bit moves only under rely or deny");
    assert(_MessageProcessor.gateway() != gatewayBefore || _MessageProcessor.multiAdapter() != adapterBefore
        || _MessageProcessor.spokeHandler() != spokeBefore || _MessageProcessor.hubHandler() != hubBefore
        || _MessageProcessor.envoy() != envoyBefore
        => f.selector == sig:_MessageProcessor.file(bytes32,address).selector,
        "a routing pointer moves only under file");
}
