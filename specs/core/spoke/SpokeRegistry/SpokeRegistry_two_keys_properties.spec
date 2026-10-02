import "setup/SpokeRegistry_two_keys.spec";

// --- valid_state ---

function requireClassTokensResolveBackAtEveryPinnedKey(env e) {
    SpokeRegistry.PoolId pA;
    SpokeRegistry.PoolId pB;
    SpokeRegistry.ShareClassId cA;
    SpokeRegistry.ShareClassId cB;
    require(pA == ghostPoolA64 && pB == ghostPoolB64 && cA == ghostShareClassA && cB == ghostShareClassB,
        "SAFE: binds the keys to the modelled pools and classes");
    requireInvariant classTokenResolvesBack(e, pA, cA);
    requireInvariant classTokenResolvesBack(e, pA, cB);
    requireInvariant classTokenResolvesBack(e, pB, cA);
    requireInvariant classTokenResolvesBack(e, pB, cB);
}

function requireLookupRowsPointBackAtEveryPinnedKey(env e, address t) {
    SpokeRegistry.PoolId pA;
    SpokeRegistry.PoolId pB;
    SpokeRegistry.ShareClassId cA;
    SpokeRegistry.ShareClassId cB;
    require(pA == ghostPoolA64 && pB == ghostPoolB64 && cA == ghostShareClassA && cB == ghostShareClassB,
        "SAFE: binds the keys to the modelled pools and classes");
    requireInvariant lookupRowPointsBack(e, pA, cA, t);
    requireInvariant lookupRowPointsBack(e, pA, cB, t);
    requireInvariant lookupRowPointsBack(e, pB, cA, t);
    requireInvariant lookupRowPointsBack(e, pB, cB, t);
    requireInvariant nullAddressOwnsNoLookupRowOnAnyKey(e);
}

function setupSrTwoClassKeysValidState(env e, address t) {
    setupTwoClassKeys(e);
    requireClassTokensResolveBackAtEveryPinnedKey(e);
    requireLookupRowsPointBackAtEveryPinnedKey(e, t);
}

// SR-VS-39: a share class's live token looks back up to exactly that pool and share class.
invariant classTokenResolvesBack(env e, SpokeRegistry.PoolId p, SpokeRegistry.ShareClassId sc)
    VALID_POOL(p) && VALID_SC(sc) && _SpokeRegistry.shareClass[p][sc].shareToken != 0 => (
        ghostSrTokenPoolId64[_SpokeRegistry.shareClass[p][sc].shareToken] == p
        && ghostSrTokenScId[_SpokeRegistry.shareClass[p][sc].shareToken] == sc
    )
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireClassTokensResolveBackAtEveryPinnedKey(e);
    SETUP_SR_TWO_KEYS(e, eFunc);
} }

// SR-VS-40: a token that looks up to a pool and share class is the token that share class holds.
invariant lookupRowPointsBack(env e, SpokeRegistry.PoolId p, SpokeRegistry.ShareClassId sc, address t)
    VALID_POOL(p) && VALID_SC(sc) && p != 0
        && ghostSrTokenPoolId64[t] == p && ghostSrTokenScId[t] == sc
        => _SpokeRegistry.shareClass[p][sc].shareToken == t
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireLookupRowsPointBackAtEveryPinnedKey(e, t);
    SETUP_SR_TWO_KEYS(e, eFunc);
} }

// SR-VS-41: no two share classes, in one pool or two, ever hold the same share token.
invariant twoClassKeysNeverShareAToken(env e, SpokeRegistry.PoolId p1, SpokeRegistry.ShareClassId s1,
    SpokeRegistry.PoolId p2, SpokeRegistry.ShareClassId s2)
    VALID_POOL(p1) && VALID_SC(s1) && VALID_POOL(p2) && VALID_SC(s2)
        && (p1 != p2 || s1 != s2)
        && _SpokeRegistry.shareClass[p1][s1].shareToken != 0
        => _SpokeRegistry.shareClass[p1][s1].shareToken != _SpokeRegistry.shareClass[p2][s2].shareToken
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) {
    requireClassTokensResolveBackAtEveryPinnedKey(e);
    SETUP_SR_TWO_KEYS(e, eFunc);
} }

// SR-VS-42: the zero address never looks up to a pool as a share token.
invariant nullAddressOwnsNoLookupRowOnAnyKey(env e)
    ghostSrTokenPoolId64[0] == 0
filtered { f -> !EXCLUDED_FUNCTION_SR(f) } { preserved with (env eFunc) { SETUP_SR_TWO_KEYS(e, eFunc); } }

// --- state_transitions ---

// SR-ST-08: a call changing a manager or bridger right on one pool changes no such right on another.
rule stSrRoleSeatsArePerPool(env e, method f, calldataarg args, SpokeRegistry.PoolId p, SpokeRegistry.PoolId q,
    address who1, address who2) filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupTwoPools(e);
    require(p == ghostPoolA64 && q == ghostPoolB64, "SCOPE: two distinct pools");

    bool managerPBefore = _SpokeRegistry.manager[p][who1];
    bool bridgerPBefore = _SpokeRegistry.bridger[p][who1];
    bool managerQBefore = _SpokeRegistry.manager[q][who2];
    bool bridgerQBefore = _SpokeRegistry.bridger[q][who2];

    f(e, args);

    assert(_SpokeRegistry.manager[p][who1] != managerPBefore || _SpokeRegistry.bridger[p][who1] != bridgerPBefore
        => _SpokeRegistry.manager[q][who2] == managerQBefore && _SpokeRegistry.bridger[q][who2] == bridgerQBefore,
        "no call moves manager or bridger rights on two pools at once");
}

// SR-ST-11: no call, even one for another pool, reassigns a registered vault.
rule stSrRegisteredVaultIsNeverTakenByAnotherPool(env e, method f, calldataarg args, address v)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupTwoPools(e);

    address assetBefore = ghostSrVaultAsset[v];
    mathint poolBefore = ghostSrVaultPoolId64[v]; bytes16 scBefore = ghostSrVaultScId[v];
    mathint aidBefore = ghostSrVaultAssetId128[v]; mathint tokenIdBefore = ghostSrVaultTokenId256[v];
    require(poolBefore == ghostPoolA64, "SCOPE: pool A's vault, pool B stands for any other");

    f(e, args);

    assert(assetBefore != 0
        => ghostSrVaultAsset[v] == assetBefore && ghostSrVaultPoolId64[v] == poolBefore && ghostSrVaultScId[v] == scBefore
            && ghostSrVaultAssetId128[v] == aidBefore && ghostSrVaultTokenId256[v] == tokenIdBefore,
        "no call, even another pool's, reassigns a registered vault");
}

// --- high_level ---

// SR-HL-12: a manager or bridger update sets that right as asked and leaves the other right and pool alone.
rule hlSrRoleGrantLandsOnTheNamedPoolOnly(env e, bool bridgerRole, SpokeRegistry.PoolId p, SpokeRegistry.PoolId q,
    address who, address other, bool can) {

    setupTwoPools(e);
    require(p == ghostPoolA64 && q == ghostPoolB64, "SCOPE: two distinct pools");

    bool otherRoleBefore = bridgerRole ? _SpokeRegistry.manager[p][who] : _SpokeRegistry.bridger[p][who];
    bool neighbourManagerBefore = _SpokeRegistry.manager[q][other];
    bool neighbourBridgerBefore = _SpokeRegistry.bridger[q][other];

    if (bridgerRole) {
        _SpokeRegistry.updateBridger(e, p, who, can);
    } else {
        _SpokeRegistry.updateManager(e, p, who, can);
    }

    bool namedRoleAfter = bridgerRole ? _SpokeRegistry.bridger[p][who] : _SpokeRegistry.manager[p][who];
    bool otherRoleAfter = bridgerRole ? _SpokeRegistry.manager[p][who] : _SpokeRegistry.bridger[p][who];

    assert(namedRoleAfter == can && otherRoleAfter == otherRoleBefore
        && _SpokeRegistry.manager[q][other] == neighbourManagerBefore
        && _SpokeRegistry.bridger[q][other] == neighbourBridgerBefore,
        "the right is set as given, the other right and other pool stay put");
}

// --- reachability ---

// SR-RC-44: an admin can add a second share class to a pool beside a live first, each with its own token.
rule rcSrSecondClassGoesLiveBesideALiveFirstClassIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId sc1, SpokeRegistry.ShareClassId sc2, address token2, address registrar2) {

    setupSrTwoClassKeysValidState(e, token2);
    require(VALID_SC(sc1) && sc1 != sc2, "SCOPE: two distinct share classes");

    address class1TokenBefore = _SpokeRegistry.shareClass[poolId][sc1].shareToken;

    _SpokeRegistry.addShareClass(e, poolId, sc2, token2, registrar2);

    address class1TokenAfter = _SpokeRegistry.shareClass[poolId][sc1].shareToken;
    address class2TokenAfter = _SpokeRegistry.shareClass[poolId][sc2].shareToken;

    satisfy(class1TokenBefore != 0 && class1TokenAfter == class1TokenBefore && class2TokenAfter == token2
        && token2 != 0 && token2 != class1TokenAfter
        && ghostSrTokenPoolId64[class1TokenAfter] == poolId && ghostSrTokenScId[class1TokenAfter] == sc1
        && ghostSrTokenPoolId64[token2] == poolId && ghostSrTokenScId[token2] == sc2,
        "a pool can open a second class, each token resolving to its own class");
}

// SR-RC-45: an admin can swap a share class to a new token, retiring the old, while another keeps its own.
rule rcSrTokenSwapBesideALiveSecondClassIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId sc1, SpokeRegistry.ShareClassId sc2, address newTok, address registrar2) {

    address oldTok = _SpokeRegistry.shareClass[poolId][sc2].shareToken;
    setupSrTwoClassKeysValidState(e, oldTok);
    require(VALID_SC(sc1) && sc1 != sc2, "SCOPE: two distinct share classes");

    address class1TokenBefore = _SpokeRegistry.shareClass[poolId][sc1].shareToken;

    _SpokeRegistry.linkToken(e, poolId, sc2, newTok, registrar2);

    satisfy(oldTok != 0 && newTok != oldTok && ghostSrTokenPoolId64[oldTok] == 0
        && _SpokeRegistry.shareClass[poolId][sc2].shareToken == newTok
        && class1TokenBefore != 0 && _SpokeRegistry.shareClass[poolId][sc1].shareToken == class1TokenBefore,
        "a class can swap tokens, retiring the old, beside a live second class");
}
