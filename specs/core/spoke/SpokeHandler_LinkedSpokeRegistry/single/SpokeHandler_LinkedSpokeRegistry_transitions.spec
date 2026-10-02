import "../setup/SpokeHandler_LinkedSpokeRegistry_base.spec";
import "../setup/SpokeHandler_LinkedSpokeRegistry_pointer_writes.spec";

// --- variable_transitions ---

// SH-VT-01: a share class with a token never changes its token or registrar.
rule vtShLiveShareClassKeepsItsTokenAndRegistrar(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    address tokenBefore = ghostSrShareToken;
    address registrarBefore = ghostSrRegistrar;

    f(e, args);

    address tokenAfter = ghostSrShareToken;
    address registrarAfter = ghostSrRegistrar;

    assert(tokenBefore != 0 => tokenAfter == tokenBefore, "a share class with a token keeps that token");
    assert(tokenBefore != 0 => registrarAfter == registrarBefore, "once tokened, a class never swaps its registrar");
}

// SH-VT-02: a share token assigned to a pool stays assigned to that pool.
rule vtShShareTokenKeepsThePoolItBacks(env e, method f, calldataarg args, address t)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint tokenPoolBefore = ghostSrTokenPoolId64[t];

    f(e, args);

    mathint tokenPoolAfter = ghostSrTokenPoolId64[t];

    assert(tokenPoolBefore != 0 => tokenPoolAfter == tokenPoolBefore,
        "a token filed under a pool stays filed under that pool");
}

// SH-VT-03: only an incoming share transfer can change token supply through the handler.
rule vtShShareSupplyMovesOnlyOnTheTransferExecutor(env e, method f, calldataarg args, address t)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint supplyBefore = ghostERC20TotalSupply256[t];

    f(e, args);

    mathint supplyAfter = ghostERC20TotalSupply256[t];

    assert(supplyAfter != supplyBefore
        => f.selector == sig:_SpokeHandler.executeTransferShares(
            SpokeHandler.PoolId, SpokeHandler.ShareClassId, bytes32, uint128).selector,
        "only a bridge arrival can change a token's supply");
}

// SH-VT-04: through the handler, a pool manager role changes only on a manager update message.
rule vtShManagerSeatMovesOnlyOnItsRoleMessage(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bool seatBefore = ghostSrManager[who];

    f(e, args);

    bool seatAfter = ghostSrManager[who];

    assert(seatAfter != seatBefore
        => f.selector == sig:_SpokeHandler.updateManager(SpokeHandler.PoolId, address, bool).selector,
        "only a manager update message changes manager rights");
}

// SH-VT-05: through the handler, a share bridging role changes only on a bridger update message.
rule vtShBridgerSeatMovesOnlyOnItsRoleMessage(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bool seatBefore = ghostSrBridger[who];

    f(e, args);

    bool seatAfter = ghostSrBridger[who];

    assert(seatAfter != seatBefore
        => f.selector == sig:_SpokeHandler.updateBridger(SpokeHandler.PoolId, address, bool).selector,
        "only a bridger update message changes bridger rights");
}

// --- state_transitions ---

// SH-ST-01: only a registered vault is linked or unlinked, keeping its pool, class and asset.
rule stShVaultLinkNeverMovesItsIdentity(env e, method f, calldataarg args, address v)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bool linkedBefore = ghostSrVaultIsLinked[v];
    address assetBefore = ghostSrVaultAsset[v];
    mathint poolBefore = ghostSrVaultPoolId64[v];
    bytes16 scBefore = ghostSrVaultScId[v];
    mathint assetIdBefore = ghostSrVaultAssetId128[v];

    f(e, args);

    assert(ghostSrVaultIsLinked[v] != linkedBefore => ghostSrVaultAsset[v] != 0,
        "only a registered vault can have its link flag changed");
    assert(ghostSrVaultIsLinked[v] != linkedBefore && assetBefore != 0
        => (ghostSrVaultPoolId64[v] == poolBefore && ghostSrVaultScId[v] == scBefore
            && ghostSrVaultAssetId128[v] == assetIdBefore),
        "a link change keeps a registered vault's pool, class and asset");
}

// SH-ST-02: a new share token is the one the registrar deployed, and maps back to its pool and class.
rule stShShareClassBindsTheRegistrarsTokenAndItsLookupBack(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address tokenBefore = ghostSrShareToken;

    f(e, args);

    address tokenAfter = ghostSrShareToken;

    assert(tokenAfter != tokenBefore && tokenAfter != 0
        => (ghostSrRegistrar != 0 && ghostSrTokenPoolId64[tokenAfter] == ghostPoolA64
            && ghostSrTokenScId[tokenAfter] == ghostShareClassA
            && tokenAfter == ghostRegistrarNewToken),
        "a new class token is the deployed one, has a registrar and maps back");
}

// SH-ST-03: changing a pool's policy invalidates its outstanding authorizations.
rule stShPolicySwapAdvancesTheAuthorizationNamespace(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;

    f(e, args);

    assert(ghostSrPolicy != policyBefore => ghostSrPolicyNonce64 == nonceBefore + 1,
        "changing a pool's policy steps its policy nonce by exactly one");
}

// SH-ST-04: authorizations can be granted or revoked only while the pool's policy stays unchanged.
rule stShAuthorizationsMoveOnlyWithinAStandingNamespace(env e, method f, calldataarg args, bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint countBefore = ghostSrAuthorizations256[id];
    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;

    f(e, args);

    assert(ghostSrAuthorizations256[id] != countBefore
        => (ghostSrPolicy == policyBefore && ghostSrPolicyNonce64 == nonceBefore),
        "an authorization moves only while the policy and nonce stay put");
}

// SH-ST-05: prices are recorded only for existing share classes and registered assets.
rule stShPricesNeedTheRowsTheyPriceTo(env e, method f, calldataarg args, uint128 aid)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address tokenBefore = ghostSrShareToken;
    mathint sharePriceBefore = ghostSrPricePoolPerShare128;
    mathint shareStampBefore = ghostSrPricePoolPerShareComputedAt64;
    mathint assetPriceBefore = ghostSrPricePoolPerAsset128[aid];
    mathint assetStampBefore = ghostSrPricePoolPerAssetComputedAt64[aid];
    address assetBefore = ghostSrIdToAssetAsset[aid];

    f(e, args);

    assert(ghostSrPricePoolPerShare128 != sharePriceBefore
            || ghostSrPricePoolPerShareComputedAt64 != shareStampBefore
        => tokenBefore != 0,
        "a share price moves only for an existing share class");
    assert(ghostSrPricePoolPerAsset128[aid] != assetPriceBefore
            || ghostSrPricePoolPerAssetComputedAt64[aid] != assetStampBefore
        => (tokenBefore != 0 && assetBefore != 0),
        "an asset price moves only for an existing class and registered asset");
}

// SH-ST-06: a price update never records a timestamp later than the spoke's current time.
rule stShPriceStampsNeverRunAheadOfTheClock(env e, method f, calldataarg args, uint128 aid)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint shareStampBefore = ghostSrPricePoolPerShareComputedAt64;
    mathint assetStampBefore = ghostSrPricePoolPerAssetComputedAt64[aid];

    f(e, args);

    assert(ghostSrPricePoolPerShareComputedAt64 != shareStampBefore
        => ghostSrPricePoolPerShareComputedAt64 <= e.block.timestamp,
        "a share price stamp is never written ahead of the clock");
    assert(ghostSrPricePoolPerAssetComputedAt64[aid] != assetStampBefore
        => ghostSrPricePoolPerAssetComputedAt64[aid] <= e.block.timestamp,
        "an asset price stamp is never written ahead of the clock");
}
