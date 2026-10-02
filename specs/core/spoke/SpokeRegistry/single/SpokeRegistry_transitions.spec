import "SpokeRegistry_valid_state.spec";

// --- variable_transitions ---

// SR-VT-01: a share class never loses its share token once it has one.
rule vtSrShareTokenNeverClears(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address shareTokenBefore = ghostSrShareToken;

    f(e, args);

    address shareTokenAfter = ghostSrShareToken;

    assert(shareTokenBefore != 0 => shareTokenAfter != 0, "a share class with a token always keeps one");
}

// SR-VT-02: a call leaves the pool's policy nonce unchanged or raises it by one.
rule vtSrPolicyTenureCounterStepsForwardByOne(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    mathint nonceBefore = ghostSrPolicyNonce64;

    f(e, args);

    mathint nonceAfter = ghostSrPolicyNonce64;

    assert(nonceAfter == nonceBefore || nonceAfter == nonceBefore + 1,
        "a pool's policy nonce stays or advances by exactly one");
}

// SR-VT-03: a call leaves the asset id counter unchanged or raises it by one.
rule vtSrAssetCounterStepsForwardByOne(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    mathint counterBefore = ghostSrAssetCounter64;

    f(e, args);

    mathint counterAfter = ghostSrAssetCounter64;

    assert(counterAfter == counterBefore || counterAfter == counterBefore + 1,
        "the asset counter stays or advances by exactly one");
}

// SR-VT-04: an issued asset id always refers to the same token and token id.
rule vtSrIssuedAssetNumberKeepsItsBinding(env e, method f, calldataarg args, SpokeRegistry.AssetId aid)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);
    requireInvariant registeredAssetIdWellFormed(e);

    address assetBefore = ghostSrIdToAssetAsset[aid];
    mathint tokenIdBefore = ghostSrIdToAssetTokenId256[aid];

    f(e, args);

    address assetAfter = ghostSrIdToAssetAsset[aid];
    mathint tokenIdAfter = ghostSrIdToAssetTokenId256[aid];

    assert(assetBefore != 0 => (assetAfter == assetBefore && tokenIdAfter == tokenIdBefore),
        "an issued asset id keeps its asset and token id");
}

// SR-VT-05: a token's asset id never changes once assigned.
rule vtSrRegisteredAssetKeepsItsNumber(env e, method f, calldataarg args, address a, uint256 t)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    mathint pairNumberBefore = ghostSrAssetToId128[a][t];

    f(e, args);

    mathint pairNumberAfter = ghostSrAssetToId128[a][t];

    assert(pairNumberBefore != 0 => pairNumberAfter == pairNumberBefore, "an asset pair that has an id keeps it");
}

// SR-VT-06: one call changes the manager or bridger rights of at most one account.
rule vtSrPoolRolesMoveOneAccountAtATime(env e, method f, calldataarg args, address moved, address other)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);
    require(moved != other, "SCOPE: two distinct addresses");

    bool movedManagerBefore = ghostSrManager[moved];
    bool movedBridgerBefore = ghostSrBridger[moved];
    bool otherManagerBefore = ghostSrManager[other];
    bool otherBridgerBefore = ghostSrBridger[other];

    f(e, args);

    bool movedManagerAfter = ghostSrManager[moved];
    bool movedBridgerAfter = ghostSrBridger[moved];
    bool otherManagerAfter = ghostSrManager[other];
    bool otherBridgerAfter = ghostSrBridger[other];

    assert(movedManagerAfter != movedManagerBefore || movedBridgerAfter != movedBridgerBefore
        => otherManagerAfter == otherManagerBefore && otherBridgerAfter == otherBridgerBefore,
        "moving one account's roles leaves any other's untouched");
}

// SR-VT-07: authorizations change only through the grant, revoke and consume calls.
rule vtSrAuthorizationLedgerMovesOnlyThroughItsThreeWriters(env e, method f, calldataarg args, bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistryValidState(e);

    mathint countBefore = ghostSrAuthorizations256[id];

    f(e, args);

    mathint countAfter = ghostSrAuthorizations256[id];

    assert(countAfter != countBefore
        => f.selector == sig:_SpokeRegistry.authorize(SpokeRegistry.PoolId, bytes).selector
            || f.selector == sig:_SpokeRegistry.unauthorize(SpokeRegistry.PoolId, bytes).selector
            || f.selector == sig:_SpokeRegistry.consumeAuthorization(SpokeRegistry.PoolId, address, bytes).selector,
        "only a grant, a revocation or a consumption changes a grant count");
}

// SR-VT-08: a vault's linked status changes only through linkVault or unlinkVault.
rule vtSrVaultLinkMovesOnlyOnLinkOrUnlink(env e, method f, calldataarg args, address v)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistryValidState(e);

    bool linkedBefore = ghostSrVaultIsLinked[v];

    f(e, args);

    assert(ghostSrVaultIsLinked[v] != linkedBefore
        => f.selector == sig:_SpokeRegistry.linkVault(SpokeRegistry.PoolId, SpokeRegistry.ShareClassId,
                SpokeRegistry.AssetId, address).selector
            || f.selector == sig:_SpokeRegistry.unlinkVault(SpokeRegistry.PoolId, SpokeRegistry.ShareClassId,
                SpokeRegistry.AssetId, address).selector,
        "no other call links or unlinks a vault");
}

// --- state_transitions ---

// SR-ST-01: a newly registered vault starts unlinked, so it does not serve investors yet.
rule stSrRegisteredVaultStartsUnlinked(env e, method f, calldataarg args, address v)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistryValidState(e);

    address assetBefore = ghostSrVaultAsset[v];

    f(e, args);

    assert(assetBefore == 0 && ghostSrVaultAsset[v] != 0 => !ghostSrVaultIsLinked[v],
        "a newly registered vault starts unlinked");
}

// SR-ST-02: a policy change bumps the pool's version, retiring outstanding authorizations.
rule stSrPolicySwapAdvancesTheInstallCounter(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistryValidState(e);

    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;

    f(e, args);

    assert(ghostSrPolicy != policyBefore => ghostSrPolicyNonce64 == nonceBefore + 1,
        "changing a pool's policy steps its policy nonce by exactly one");
}

// SR-ST-03: authorizations are granted only under the pool's current policy and version.
rule stSrGrantsLandOnlyOnTheInstalledPolicy(env e, method f, calldataarg args,
    address pol, uint64 n, bytes32 h)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistryValidState(e);

    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;
    bytes32 id = ghostSrAuthId[ghostPoolA64][pol][n][h];
    mathint countBefore = ghostSrAuthorizations256[id];

    f(e, args);

    assert(ghostSrAuthorizations256[id] > countBefore
        => pol == policyBefore && pol != 0 && n == nonceBefore,
        "a grant is filed only under the installed policy and its nonce");
}

// SR-ST-04: price timestamps never decrease, so an older price cannot replace a newer one.
rule stSrPriceStampsNeverRewind(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {
    setupSpokeRegistryValidState(e);
    mathint shareBefore = ghostSrPricePoolPerShareComputedAt64;
    mathint assetBefore = ghostSrPricePoolPerAssetComputedAt64[a];

    f(e, args);

    assert(ghostSrPricePoolPerShareComputedAt64 >= shareBefore && ghostSrPricePoolPerAssetComputedAt64[a] >= assetBefore,
        "share and asset price stamps never move backwards");
}

// SR-ST-05: authorization counts change by one, only under the current policy and version.
rule stSrAuthorizationLedgerStepsByOneInTheStandingNamespace(env e, method f, calldataarg args, address pol, uint64 n, bytes32 h)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {
    setupSpokeRegistryValidState(e);
    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;
    bytes32 id = ghostSrAuthId[ghostPoolA64][pol][n][h];
    mathint countBefore = ghostSrAuthorizations256[id];

    f(e, args);

    assert(ghostSrAuthorizations256[id] != countBefore
        => pol == policyBefore && n == nonceBefore
            && (ghostSrAuthorizations256[id] == countBefore + 1 || ghostSrAuthorizations256[id] == countBefore - 1),
        "a grant count moves by one, only under the current policy and nonce");
}

// SR-ST-06: a registered vault's pool, share class and asset never change.
rule stSrRegisteredVaultKeepsItsIdentity(env e, method f, calldataarg args, address v)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {
    setupSpokeRegistryValidState(e);
    address assetBefore = ghostSrVaultAsset[v];
    mathint poolBefore = ghostSrVaultPoolId64[v]; bytes16 scBefore = ghostSrVaultScId[v];
    mathint aidBefore = ghostSrVaultAssetId128[v]; mathint tokenIdBefore = ghostSrVaultTokenId256[v];

    f(e, args);

    assert(assetBefore != 0
        => ghostSrVaultAsset[v] == assetBefore && ghostSrVaultPoolId64[v] == poolBefore && ghostSrVaultScId[v] == scBefore
            && ghostSrVaultAssetId128[v] == aidBefore && ghostSrVaultTokenId256[v] == tokenIdBefore,
        "a registered vault's identity never changes");
}

// SR-ST-07: a pool's creation time, once set, never changes.
rule stSrPoolEntryStampIsWrittenOnce(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {
    setupSpokeRegistryValidState(e);
    mathint before = ghostSrCreatedAt64;

    f(e, args);

    assert(before != 0 => ghostSrCreatedAt64 == before, "an opened pool keeps its opening stamp");
}

// SR-ST-09: a call changes the linked status of at most one vault.
rule stSrAtMostOneVaultLinkMovesPerCall(env e, method f, calldataarg args, address v1, address v2)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistryValidState(e);
    require(v1 != v2, "SCOPE: two distinct vaults");

    bool linked1Before = ghostSrVaultIsLinked[v1];
    bool linked2Before = ghostSrVaultIsLinked[v2];

    f(e, args);

    assert(ghostSrVaultIsLinked[v1] != linked1Before => ghostSrVaultIsLinked[v2] == linked2Before,
        "a call links or unlinks at most one vault");
}

// SR-ST-10: manager rights change only through updateManager and bridger rights only through updateBridger.
rule stSrRoleSeatsMoveOnlyOnTheirOwnWriter(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistryValidState(e);

    bool managerBefore = ghostSrManager[who];
    bool bridgerBefore = ghostSrBridger[who];

    f(e, args);

    assert((ghostSrManager[who] != managerBefore
            => f.selector == sig:_SpokeRegistry.updateManager(SpokeRegistry.PoolId, address, bool).selector)
        && (ghostSrBridger[who] != bridgerBefore
            => f.selector == sig:_SpokeRegistry.updateBridger(SpokeRegistry.PoolId, address, bool).selector),
        "each role moves only through its own update call");
}
