import "setup/SpokeHandler_LinkedRegistryFactory_base.spec";

// --- state_transitions ---

// SH-ST-07: a pool is registered on the spoke only if its escrow can also be deployed.
rule stShPoolRowNeedsTheEscrowDeployBehindIt(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedRegistryFactoryValidState(e);

    mathint createdBefore = ghostSrCreatedAt64;
    mathint factoryWardBefore = _PoolEscrowFactory.wards[_SpokeHandler];

    f(e, args);

    assert(createdBefore == 0 && ghostSrCreatedAt64 != 0 => factoryWardBefore == 1,
        "a pool opens only if the handler is a ward of the escrow factory");
}

// SH-ST-08: an escrow is linked to a pool only in the call that registers that same pool.
rule stShEscrowBrandComesWithThePoolRow(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedRegistryFactoryValidState(e);

    mathint brandBefore = ghostPefEscrowPool64[who];
    mathint createdBefore = ghostSrCreatedAt64;

    f(e, args);

    assert(ghostPefEscrowPool64[who] != brandBefore
        => (createdBefore == 0 && ghostSrCreatedAt64 != 0
            && ghostPefEscrowPool64[who] == ghostPoolA64),
        "an address gets a pool record only as that pool is opened");
}

// SH-ST-09: a pool is registered on the spoke only after its escrow was linked to it in the same call.
rule stShPoolRowOpensOnlyAfterItsEscrowIsBranded(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedRegistryFactoryValidState(e);
    require(!ghostShBrandedBeforeRow, "SAFE: no escrow link recorded before the call");

    mathint createdBefore = ghostSrCreatedAt64;

    f(e, args);

    assert(createdBefore == 0 && ghostSrCreatedAt64 != 0 => ghostShBrandedBeforeRow,
        "a new pool's escrow was linked to it earlier in the same call");
}

// --- reachability ---

// SH-RC-21: adding a pool can create its escrow and register the pool in one message.
rule rcShAddPoolBrandsItsEscrowAndOpensTheRowIsReachable(env e, SpokeHandler.PoolId p, address who) {

    setupSpokeHandlerLinkedRegistryFactoryValidState(e);

    mathint brandBefore = ghostPefEscrowPool64[who];
    mathint createdBefore = ghostSrCreatedAt64;

    _SpokeHandler.addPool(e, p);

    satisfy(brandBefore != ghostPefEscrowPool64[who] && createdBefore == 0 && ghostSrCreatedAt64 != 0
        && ghostPefEscrowPool64[who] == ghostPoolA64,
        "adding a pool can open it and record an escrow under it");
}
