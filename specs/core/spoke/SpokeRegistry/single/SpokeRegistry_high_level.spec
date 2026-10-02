import "SpokeRegistry_valid_state.spec";

// SR-HL-01: an authorization covers exactly one use by the pool's policy.
rule hlSrConsumptionSpendsExactlyOneGrant(env e, env ePolicy, SpokeRegistry.PoolId poolId, address caller, bytes data) {

    setupSpokeRegistryValidState(e);
    setupSpokeRegistryValidState(ePolicy);

    bytes32 id = _SpokeRegistry.authId(e, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.consumeAuthorization(ePolicy, poolId, caller, data);

    mathint countAfter = ghostSrAuthorizations256[id];

    assert(countAfter == countBefore, "one grant then one consumption leaves the grant count unchanged");
}

// SR-HL-02: after a policy change, earlier authorizations can no longer be spent.
rule hlSrPolicySwapOrphansOutstandingGrants(env e, env ePolicy, SpokeRegistry.PoolId poolId,
    address newPolicy, address caller, bytes data) {

    setupSpokeRegistryValidState(e);
    setupSpokeRegistryValidState(ePolicy);

    bytes32 idOld = _SpokeRegistry.authId(e, poolId, data);
    mathint orphanedBefore = ghostSrAuthorizations256[idOld];

    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.setPolicy(e, poolId, newPolicy);
    _SpokeRegistry.consumeAuthorization@withrevert(ePolicy, poolId, caller, data);
    bool reverted = lastReverted;

    mathint orphanedAfter = ghostSrAuthorizations256[idOld];

    assert(reverted && orphanedAfter == orphanedBefore + 1,
        "a consumption after a policy swap is refused, and the grant made before it survives");
}

// SR-HL-03: repeated authorizations add up, and a revocation removes only one of them.
rule hlSrAuthorizationLedgerCountsGrants(env e, SpokeRegistry.PoolId poolId, bytes data) {

    setupSpokeRegistryValidState(e);

    bytes32 id = _SpokeRegistry.authId(e, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.unauthorize(e, poolId, data);

    mathint countAfter = ghostSrAuthorizations256[id];

    assert(countAfter == countBefore + 1, "two grants and one revocation leave one grant more than before");
}

// SR-HL-04: a newly registered asset maps to the id its registration returned.
rule hlSrCreatedAssetPairResolvesToIssuedId(env e, uint16 centrifugeId, address asset, uint256 tokenId) {

    setupSpokeRegistryValidState(e);

    mathint pairTokenId = tokenId;

    SpokeRegistry.AssetId newId = _SpokeRegistry.createAssetId(e, centrifugeId, asset, tokenId);

    mathint issuedId = newId;
    mathint reverseIdAfter = ghostSrAssetToId128[asset][pairTokenId];

    assert(reverseIdAfter == issuedId, "a new asset pair is filed under the id registration returns");
}

// SR-HL-05: a new asset id resolves back to the registered asset address.
rule hlSrCreatedAssetIdResolvesToItsAsset(env e, uint16 centrifugeId, address asset, uint256 tokenId) {

    setupSpokeRegistryValidState(e);

    SpokeRegistry.AssetId newId = _SpokeRegistry.createAssetId(e, centrifugeId, asset, tokenId);

    uint128 issuedId = newId;
    address forwardAssetAfter = ghostSrIdToAssetAsset[issuedId];

    assert(forwardAssetAfter == asset, "a new asset id resolves to the asset it was issued for");
}

// SR-HL-06: a new asset id resolves back to the registered token id.
rule hlSrCreatedAssetIdResolvesToItsTokenId(env e, uint16 centrifugeId, address asset, uint256 tokenId) {

    setupSpokeRegistryValidState(e);

    mathint pairTokenId = tokenId;

    SpokeRegistry.AssetId newId = _SpokeRegistry.createAssetId(e, centrifugeId, asset, tokenId);

    uint128 issuedId = newId;
    mathint forwardTokenIdAfter = ghostSrIdToAssetTokenId256[issuedId];

    assert(forwardTokenIdAfter == pairTokenId, "a new asset id resolves to the token id it was issued for");
}

// SR-HL-07: an asset price update stores exactly the price and timestamp the hub sent.
rule hlSrAssetQuoteIsStoredExactlyAsSent(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.AssetId assetId, SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    uint128 pricedAssetId = assetId;

    _SpokeRegistry.updatePricePoolPerAsset(e, poolId, scId, assetId, price, computedAt);

    mathint priceAfter = ghostSrPricePoolPerAsset128[pricedAssetId];
    mathint stampAfter = ghostSrPricePoolPerAssetComputedAt64[pricedAssetId];

    assert(priceAfter == price && stampAfter == computedAt, "an asset quote is kept verbatim, price and stamp");
}

// SR-HL-08: a share price update stores exactly the price and timestamp the hub sent.
rule hlSrShareQuoteIsStoredExactlyAsSent(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    _SpokeRegistry.updatePricePoolPerShare(e, poolId, scId, price, computedAt);

    mathint priceAfter = ghostSrPricePoolPerShare128;
    mathint stampAfter = ghostSrPricePoolPerShareComputedAt64;

    assert(priceAfter == price && stampAfter == computedAt, "a share quote is kept verbatim, price and stamp");
}

// SR-HL-09: a share class gets the given token and registrar, and the token maps back to it.
rule hlSrShareClassBindsExactlyTheTokenAndRegistrarNamed(env e, bool relink, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, address shareToken_, address registrar_) {

    setupSpokeRegistryValidState(e);

    if (relink) {
        _SpokeRegistry.linkToken(e, poolId, scId, shareToken_, registrar_);
    } else {
        _SpokeRegistry.addShareClass(e, poolId, scId, shareToken_, registrar_);
    }

    address tokenAfter = ghostSrShareToken;
    address registrarAfter = ghostSrRegistrar;
    mathint lookupPoolAfter = ghostSrTokenPoolId64[shareToken_];
    bytes16 lookupClassAfter = ghostSrTokenScId[shareToken_];

    assert(tokenAfter == shareToken_ && registrarAfter == registrar_
        && lookupPoolAfter == poolId && lookupClassAfter == scId,
        "a class add or relink binds the named token, registrar and lookup");
}

// SR-HL-10: adding a pool records the current block time, never zero, and the pool then reads as active.
rule hlSrAddedPoolIsStampedWithTheBlockTime(env e, SpokeRegistry.PoolId poolId) {

    setupSpokeRegistryValidState(e);

    _SpokeRegistry.addPool(e, poolId);

    mathint stampAfter = ghostSrCreatedAt64;
    bool activeAfter = _SpokeRegistry.isPoolActive(e, poolId);

    assert(stampAfter == e.block.timestamp && stampAfter != 0 && activeAfter,
        "the new pool carries the block time, nonzero, and reads as active");
}

// SR-HL-11: moving a share class to a new token leaves the old token resolving to no pool or class.
rule hlSrTokenSwapDeletesTheOutgoingTokensRow(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, address shareToken_, address registrar_) {

    setupSpokeRegistry(e);

    address outgoing = ghostSrShareToken;

    _SpokeRegistry.linkToken(e, poolId, scId, shareToken_, registrar_);

    mathint outgoingPoolAfter = ghostSrTokenPoolId64[outgoing];
    bytes16 outgoingClassAfter = ghostSrTokenScId[outgoing];

    assert((outgoing != 0 && outgoing != shareToken_)
        => outgoingPoolAfter == 0 && outgoingClassAfter == to_bytes16(0),
        "the replaced token maps to no pool and no class afterwards");
}

// SR-HL-13: a new asset id joins its nonzero network id with the next count, and the count advances by one.
rule hlSrIssuedAssetIdIsTheChainOverTheCounter(env e, uint16 centrifugeId, address asset, uint256 tokenId) {

    setupSpokeRegistryValidState(e);

    mathint counterBefore = ghostSrAssetCounter64;

    SpokeRegistry.AssetId newId = _SpokeRegistry.createAssetId(e, centrifugeId, asset, tokenId);

    assert(newId == centrifugeId * 2^112 + counterBefore + 1 && centrifugeId != 0
        && ghostSrAssetCounter64 == counterBefore + 1,
        "the id is the nonzero network over the new count, which rose by one");
}

// SR-HL-14: linking or unlinking one vault never changes another vault's linked status.
rule hlSrLinkCallMovesOnlyItsOwnVaultsFlag(env e, bool link, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, address vault_, address v) {

    setupSpokeRegistryValidState(e);

    bool linkedBefore = ghostSrVaultIsLinked[v];

    if (link) {
        _SpokeRegistry.linkVault(e, poolId, scId, assetId, vault_);
    } else {
        _SpokeRegistry.unlinkVault(e, poolId, scId, assetId, vault_);
    }

    assert(v != vault_ => ghostSrVaultIsLinked[v] == linkedBefore,
        "every other vault stays linked or unlinked as before");
}
