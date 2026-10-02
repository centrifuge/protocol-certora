import "ShareClassManager_single_pool_valid_state.spec";

// --- variable_transitions ---

// SC-VT-01: a network's cumulative issued shares never decrease.
rule vtScNetworkIssuedTotalNeverDecreases(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint issuancesBefore = ghostScIssuances256[cid];

    f(e, args);

    mathint issuancesAfter = ghostScIssuances256[cid];

    assert(issuancesAfter >= issuancesBefore, "a network's issuance tally only grows or holds");
}

// SC-VT-02: a network's cumulative revoked shares never decrease.
rule vtScNetworkRevokedTotalNeverDecreases(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint revocationsBefore = ghostScRevocations256[cid];

    f(e, args);

    mathint revocationsAfter = ghostScRevocations256[cid];

    assert(revocationsAfter >= revocationsBefore, "a network's revocation tally only grows or holds");
}

// SC-VT-03: a class's cumulative issued shares never decrease.
rule vtScClassIssuedTotalNeverDecreases(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint issuancesBefore = ghostScTotalIssuances256;

    f(e, args);

    mathint issuancesAfter = ghostScTotalIssuances256;

    assert(issuancesAfter >= issuancesBefore, "a class's issuance tally only grows or holds");
}

// SC-VT-04: a class's cumulative revoked shares never decrease.
rule vtScClassRevokedTotalNeverDecreases(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint revocationsBefore = ghostScTotalRevocations256;

    f(e, args);

    mathint revocationsAfter = ghostScTotalRevocations256;

    assert(revocationsAfter >= revocationsBefore, "a class's revocation tally only grows or holds");
}

// --- state_transitions ---

// SC-ST-01: a new share class takes an unused salt and marks it used.
rule stScCreationClaimsAFreeIdentity(env e, method f, calldataarg args, bytes32 s)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManagerValidState(e);

    mathint countBefore = ghostScShareClassCount32;
    bool saltBefore = ghostScSalts[s];
    bool idsBefore = ghostScShareClassIds;

    f(e, args);

    assert(ghostScShareClassCount32 == countBefore + 1 && ghostScMetadataSalt == s
        => !saltBefore && ghostScSalts[s] && ghostScShareClassIds && !idsBefore,
        "creating a class spends an unused salt and registers a new class");
}

// SC-ST-09: salts, the class count and class records change only when a share class is added.
rule stScClassIdentityMovesOnlyOnCreation(env e, method f, calldataarg args, bytes32 s)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManagerValidState(e);

    bool saltClaimedBefore = ghostScSalts[s];
    mathint countBefore = ghostScShareClassCount32;
    bool classOnRecordBefore = ghostScShareClassIds;
    bytes32 classSaltBefore = ghostScMetadataSalt;

    f(e, args);

    bool saltClaimedAfter = ghostScSalts[s];
    mathint countAfter = ghostScShareClassCount32;
    bool classOnRecordAfter = ghostScShareClassIds;
    bytes32 classSaltAfter = ghostScMetadataSalt;

    assert(saltClaimedAfter != saltClaimedBefore || countAfter != countBefore
        || classOnRecordAfter != classOnRecordBefore || classSaltAfter != classSaltBefore
        => f.selector == sig:_ShareClassManager.addShareClass(ShareClassManager.PoolId,string,string,bytes32).selector,
        "only adding a class moves used salts, the count, roster or class salt");
}

// SC-ST-10: a share class's price and its timestamp change only through a price update.
rule stScSharePriceMovesOnlyOnRepricing(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManagerValidState(e);

    mathint priceBefore = ghostScPricePoolPerShare128;
    mathint priceStampBefore = ghostScPriceComputedAt64;

    f(e, args);

    mathint priceAfter = ghostScPricePoolPerShare128;
    mathint priceStampAfter = ghostScPriceComputedAt64;

    assert(priceAfter != priceBefore || priceStampAfter != priceStampBefore
        => f.selector == sig:_ShareClassManager.updateSharePrice(ShareClassManager.PoolId,
            ShareClassManager.ShareClassId, ShareClassManager.D18, uint64).selector,
        "only a repricing changes a class's price or its timestamp");
}

// SC-ST-11: class totals change only on a share update, network supply also on a transfer.
rule stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManagerValidState(e);

    mathint classIssuedBefore = ghostScTotalIssuances256;
    mathint classRevokedBefore = ghostScTotalRevocations256;
    mathint networkIssuedBefore = ghostScIssuances256[cid];
    mathint networkRevokedBefore = ghostScRevocations256[cid];
    mathint shortNetworkCountBefore = ghostScNegativeNetworkCount32;

    f(e, args);

    assert(ghostScTotalIssuances256 != classIssuedBefore || ghostScTotalRevocations256 != classRevokedBefore
        => f.selector == sig:_ShareClassManager.updateShares(uint16, ShareClassManager.PoolId,
            ShareClassManager.ShareClassId, uint128, bool).selector,
        "only a supply update changes class totals");
    assert(ghostScIssuances256[cid] != networkIssuedBefore || ghostScRevocations256[cid] != networkRevokedBefore
        || ghostScNegativeNetworkCount32 != shortNetworkCountBefore
        => f.selector == sig:_ShareClassManager.updateShares(uint16, ShareClassManager.PoolId,
            ShareClassManager.ShareClassId, uint128, bool).selector
            || f.selector == sig:_ShareClassManager.transferShares(ShareClassManager.PoolId,
                ShareClassManager.ShareClassId, uint16, uint16, uint128).selector,
        "only a supply update or a transfer changes network supply or the deficit count");
}
