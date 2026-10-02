import "../setup/SpokeRegistry_base.spec";

function setupSpokeRegistryValidState(env e) {
    setupSpokeRegistry(e);
    requireInvariant poolCreatedAtNotFuture(e);
    requireInvariant poolCreatedAboveEnvFloor(e);
    requireInvariant shareTokenIffRegistrar(e);
    requireInvariant shareClassImpliesActivePool(e);
    requireInvariant tokenRowScIdImpliesPoolId(e);
    requireInvariant shareTokenHasCanonicalReverseRow(e);
    requireInvariant onlyCurrentShareTokenHoldsALookupRow(e);
    requireInvariant nullTokenRowPoolIdZero(e);
    requireInvariant requestManagerImpliesActivePool(e);
    requireInvariant managerImpliesActivePool(e);
    requireInvariant bridgerImpliesActivePool(e);
    requireInvariant policyImpliesNonzeroNonce(e);
    requireInvariant policyNonceImpliesActivePool(e);
    requireInvariant nullAuthIdRowEmpty(e);
    requireInvariant noPolicyEverMeansNoAuthorizations(e);
    requireInvariant noAuthorizationsUnderZeroNonce(e);
    requireInvariant noAuthorizationsAheadOfTenure(e);
    requireInvariant currentTenureAuthorizationsCarryTheInstalledPolicy(e);
    requireInvariant assetForwardResolvesBack(e);
    requireInvariant assetReverseResolvesBack(e);
    requireInvariant registeredAssetIdWellFormed(e);
    requireInvariant unregisteredAssetRowEmpty(e);
    requireInvariant nullAssetNeverRegistered(e);
    requireInvariant sharePriceStampImpliesShareClass(e);
    requireInvariant sharePriceValueImpliesShareClass(e);
    requireInvariant assetPriceStampImpliesShareClass(e);
    requireInvariant assetPriceValueImpliesShareClass(e);
    requireInvariant assetPriceStampImpliesRegisteredAsset(e);
    requireInvariant assetPriceValueImpliesRegisteredAsset(e);
    requireInvariant linkedVaultIsRegistered(e);
    requireInvariant unregisteredVaultPoolIdZero(e);
    requireInvariant unregisteredVaultScIdZero(e);
    requireInvariant unregisteredVaultAssetIdZero(e);
    requireInvariant unregisteredVaultTokenIdZero(e);
    requireInvariant registeredVaultMatchesAssetRegistry(e);
    requireInvariant registeredVaultSitsOnALiveShareClass(e);
    requireInvariant nullVaultNeverRegistered(e);
    requireInvariant sharePriceStampNotFuture(e);
    requireInvariant assetPriceStampNotFuture(e);
}

// SR-VS-01: a pool's creation time is never in the future.
invariant poolCreatedAtNotFuture(env e)
    ghostSrCreatedAt64 <= e.block.timestamp
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-02: a created pool's creation time is never before the earliest assumed block time.
invariant poolCreatedAboveEnvFloor(env e)
    ghostSrCreatedAt64 != 0 => ghostSrCreatedAt64 >= MIN_BLOCK_TIMESTAMP()
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-03: a share class has a share token exactly when it has a token registrar.
invariant shareTokenIffRegistrar(env e)
    ghostSrShareToken != 0 <=> ghostSrRegistrar != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-04: a share class exists only on a created pool.
invariant shareClassImpliesActivePool(env e)
    ghostSrShareToken != 0 => ghostSrCreatedAt64 != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-05: a share token never resolves to a share class without also resolving to a pool.
invariant tokenRowScIdImpliesPoolId(env e)
    forall address t. ghostSrTokenScId[t] != to_bytes16(0) => ghostSrTokenPoolId64[t] != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-06: the registered share token resolves back to its own pool and share class.
invariant shareTokenHasCanonicalReverseRow(env e)
    ghostSrShareToken != 0 => (
        ghostSrTokenPoolId64[ghostSrShareToken] == ghostPoolA64
        && ghostSrTokenScId[ghostSrShareToken] == ghostShareClassA
    )
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-07: only a share class's current token resolves to it, so a replaced token does not.
// SCOPE: one pool in scene, another pool's token has its own row.
invariant onlyCurrentShareTokenHoldsALookupRow(env e)
    forall address t. ghostSrTokenPoolId64[t] != 0 => t == ghostSrShareToken
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireInvariant nullTokenRowPoolIdZero(e);
    SETUP_SR(e, eFunc);
} }

// SR-VS-08: the zero address never resolves to a pool as a share token.
invariant nullTokenRowPoolIdZero(env e)
    ghostSrTokenPoolId64[0] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-09: a request manager can only be installed on a created pool.
invariant requestManagerImpliesActivePool(env e)
    ghostSrRequestManager != 0 => ghostSrCreatedAt64 != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-10: manager rights exist only on a created pool.
invariant managerImpliesActivePool(env e)
    forall address who. ghostSrManager[who] => ghostSrCreatedAt64 != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-11: bridger rights exist only on a created pool.
invariant bridgerImpliesActivePool(env e)
    forall address who. ghostSrBridger[who] => ghostSrCreatedAt64 != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-12: a pool with an installed policy always has a non-zero policy nonce.
invariant policyImpliesNonzeroNonce(env e)
    ghostSrPolicy != 0 => ghostSrPolicyNonce64 != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-13: a pool's policy nonce is non-zero only once the pool is created.
invariant policyNonceImpliesActivePool(env e)
    ghostSrPolicyNonce64 != 0 => ghostSrCreatedAt64 != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-14: no authorization is ever recorded under the zero authorization id.
invariant nullAuthIdRowEmpty(env e)
    ghostSrAuthorizations256[to_bytes32(0)] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-15: a pool that never had a policy set holds no authorizations.
// SCOPE: one pool, a second pool's grants share the same flat ledger.
invariant noPolicyEverMeansNoAuthorizations(env e)
    forall bytes32 id. ghostSrPolicyNonce64 == 0 => ghostSrAuthorizations256[id] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireInvariant policyImpliesNonzeroNonce(e);
    SETUP_SR(e, eFunc);
} }

// SR-VS-16: a registered asset id's token and token id map back to that same asset id.
invariant assetForwardResolvesBack(env e)
    forall uint128 aid. ghostSrIdToAssetAsset[aid] != 0
        => ghostSrAssetToId128[ghostSrIdToAssetAsset[aid]][ghostSrIdToAssetTokenId256[aid]] == aid
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireInvariant registeredAssetIdWellFormed(e);
    SETUP_SR(e, eFunc);
} }

// SR-VS-17: an asset id assigned to a token resolves back to that token and token id.
invariant assetReverseResolvesBack(env e)
    forall address a. forall mathint t. ghostSrAssetToId128[a][t] != 0 => (
        ghostSrIdToAssetAsset[ghostSrAssetToId128[a][t]] == a
        && ghostSrIdToAssetTokenId256[ghostSrAssetToId128[a][t]] == t
    )
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireInvariant registeredAssetIdWellFormed(e);
    requireInvariant nullAssetNeverRegistered(e);
    SETUP_SR(e, eFunc);
} }

// SR-VS-18: a registered asset id has a non-zero network id and an already issued number.
invariant registeredAssetIdWellFormed(env e)
    forall uint128 aid. ghostSrIdToAssetAsset[aid] != 0 => (
        aid / 2^112 != 0
        && aid % 2^112 >= 1
        && aid % 2^112 <= ghostSrAssetCounter64
    )
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-19: an unregistered asset id holds no leftover token id.
invariant unregisteredAssetRowEmpty(env e)
    forall uint128 aid. ghostSrIdToAssetAsset[aid] == 0 => ghostSrIdToAssetTokenId256[aid] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-20: the zero asset address is never registered under any token id.
invariant nullAssetNeverRegistered(env e)
    forall mathint t. ghostSrAssetToId128[0][t] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-21: a share price timestamp can only exist once the share class does.
invariant sharePriceStampImpliesShareClass(env e)
    ghostSrPricePoolPerShareComputedAt64 != 0 => ghostSrShareToken != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-22: a share price value can only exist once the share class does.
invariant sharePriceValueImpliesShareClass(env e)
    ghostSrPricePoolPerShare128 != 0 => ghostSrShareToken != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-23: an asset price timestamp can only exist once the share class does.
invariant assetPriceStampImpliesShareClass(env e)
    forall uint128 aid. ghostSrPricePoolPerAssetComputedAt64[aid] != 0 => ghostSrShareToken != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-24: an asset price value can only exist once the share class does.
invariant assetPriceValueImpliesShareClass(env e)
    forall uint128 aid. ghostSrPricePoolPerAsset128[aid] != 0 => ghostSrShareToken != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-25: an asset price timestamp can only exist for a registered asset.
invariant assetPriceStampImpliesRegisteredAsset(env e)
    forall uint128 aid. ghostSrPricePoolPerAssetComputedAt64[aid] != 0 => ghostSrIdToAssetAsset[aid] != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-26: an asset price value can only exist for a registered asset.
invariant assetPriceValueImpliesRegisteredAsset(env e)
    forall uint128 aid. ghostSrPricePoolPerAsset128[aid] != 0 => ghostSrIdToAssetAsset[aid] != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-27: a vault can only be linked after it was registered.
invariant linkedVaultIsRegistered(env e)
    forall address v. ghostSrVaultIsLinked[v] => ghostSrVaultAsset[v] != 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-28: an unregistered vault has no pool recorded.
invariant unregisteredVaultPoolIdZero(env e)
    forall address v. ghostSrVaultAsset[v] == 0 => ghostSrVaultPoolId64[v] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-29: an unregistered vault has no share class recorded.
invariant unregisteredVaultScIdZero(env e)
    forall address v. ghostSrVaultAsset[v] == 0 => ghostSrVaultScId[v] == to_bytes16(0)
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-30: an unregistered vault has no asset id recorded.
invariant unregisteredVaultAssetIdZero(env e)
    forall address v. ghostSrVaultAsset[v] == 0 => ghostSrVaultAssetId128[v] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-31: an unregistered vault has no token id recorded.
invariant unregisteredVaultTokenIdZero(env e)
    forall address v. ghostSrVaultAsset[v] == 0 => ghostSrVaultTokenId256[v] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-32: a registered vault's asset id always resolves to the vault's asset and token id.
invariant registeredVaultMatchesAssetRegistry(env e)
    forall address v. ghostSrVaultAsset[v] != 0 => (
        ghostSrIdToAssetAsset[ghostSrVaultAssetId128[v]] == ghostSrVaultAsset[v]
        && ghostSrIdToAssetTokenId256[ghostSrVaultAssetId128[v]] == ghostSrVaultTokenId256[v]
    )
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireInvariant registeredAssetIdWellFormed(e);
    SETUP_SR(e, eFunc);
} }

// SR-VS-33: every registered vault belongs to a share class that has a share token.
// SCOPE: one pool, a vault of a second pool would name that pool.
invariant registeredVaultSitsOnALiveShareClass(env e)
    forall address v. ghostSrVaultAsset[v] != 0 => (
        ghostSrVaultPoolId64[v] == ghostPoolA64
        && ghostSrVaultScId[v] == ghostShareClassA
        && ghostSrShareToken != 0
    )
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-34: the zero address is never a registered vault.
invariant nullVaultNeverRegistered(env e)
    ghostSrVaultAsset[0] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-35: no authorization is ever recorded under a zero policy nonce.
invariant noAuthorizationsUnderZeroNonce(env e)
    forall uint64 p. forall address pol. forall bytes32 h.
        ghostSrAuthorizations256[ghostSrAuthId[p][pol][0][h]] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireInvariant policyImpliesNonzeroNonce(e);
    SETUP_SR(e, eFunc);
} }

// SR-VS-36: no authorization is recorded for a policy nonce the pool has not reached yet.
invariant noAuthorizationsAheadOfTenure(env e)
    forall address pol. forall uint64 n. forall bytes32 h. n > ghostSrPolicyNonce64
        => ghostSrAuthorizations256[ghostSrAuthId[ghostPoolA64][pol][n][h]] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-37: under the current policy nonce, only the installed policy has authorizations.
invariant currentTenureAuthorizationsCarryTheInstalledPolicy(env e)
    forall address pol. forall bytes32 h. pol != ghostSrPolicy
        => ghostSrAuthorizations256[ghostSrAuthId[ghostPoolA64][pol][ghostSrPolicyNonce64][h]] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireInvariant noAuthorizationsAheadOfTenure(e);
    SETUP_SR(e, eFunc);
} }

// SR-VS-38: only an address with deployed code can resolve to a pool as a share token.
invariant onlyADeployedContractOwnsATokenRow(env e)
    forall address t. ghostSrTokenPoolId64[t] != 0 => nativeCodesize[t] > 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-43: a share price timestamp never runs ahead of the chain clock.
invariant sharePriceStampNotFuture(env e)
    ghostSrPricePoolPerShareComputedAt64 <= e.block.timestamp
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-44: an asset price timestamp never runs ahead of the chain clock.
invariant assetPriceStampNotFuture(env e)
    forall uint128 aid. ghostSrPricePoolPerAssetComputedAt64[aid] <= e.block.timestamp
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }

// SR-VS-45: only an address with deployed code is ever a registered vault.
invariant onlyADeployedContractHoldsAVaultRow(env e)
    forall address v. ghostSrVaultAsset[v] != 0 => nativeCodesize[v] > 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR(e, eFunc); } }
