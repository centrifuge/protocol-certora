// HubRegistry. Model: pool, asset and wiring rows, for scenes not compiling it.

persistent ghost uint128 ghostHrCurrency128;
persistent ghost mapping(mathint => bool) ghostHrAssetRegistered;
persistent ghost mapping(mathint => mathint) ghostHrAssetDecimals8 {
    axiom forall mathint a. ghostHrAssetDecimals8[a] >= 0 && ghostHrAssetDecimals8[a] <= max_uint8;
}
persistent ghost mapping(uint16 => address) ghostHrHubRequestManager;
persistent ghost address ghostHrBridgingHook;
persistent ghost mapping(address => bool) ghostHrManager;
persistent ghost address ghostHrPolicy;
persistent ghost uint64 ghostHrPolicyNonce64;

methods {
    // SCOPE: one currency answers every pool, so pools exist together.
    function _.exists(uint64 poolId) external
        => hrExistsCVL(poolId) expect bool UNRESOLVED;

    function _.registerAsset(uint128 assetId, uint8 decimals) external
        => hrRegisterAssetCVL(assetId, decimals) expect void UNRESOLVED;
    function _.isRegistered(uint128 assetId) external
        => hrIsRegisteredCVL(assetId) expect bool UNRESOLVED;
    // SCOPE: one pool per conf, so decimals ignores the pool argument.
    function _.decimals(uint64 poolId) external
        => hrDecimalsCVL() expect uint8 UNRESOLVED;
    function _.decimals(uint128 assetId) external
        => hrAssetDecimalsCVL(assetId) expect uint8 UNRESOLVED;

    // SCOPE: pool argument ignored, two-pool scenes reach only exists.
    function _.manager(uint64 poolId, address who) external
        => ghostHrManager[who] expect bool UNRESOLVED;
    function _.updateManager(uint64 poolId, address who, bool canManage) external
        => hrUpdateManagerCVL(who, canManage) expect void UNRESOLVED;
    function _.registerPool(uint64 poolId, address admin, uint128 currency) external
        => hrRegisterPoolCVL(poolId, admin, currency) expect void UNRESOLVED;
    function _.policy(uint64 poolId) external
        => ghostHrPolicy expect address UNRESOLVED;
    function _.setPolicy(uint64 poolId, address policy) external
        => hrSetPolicyCVL(policy) expect void UNRESOLVED;
    function _.updateCurrency(uint64 poolId, uint128 currency) external
        => hrUpdateCurrencyCVL(currency) expect void UNRESOLVED;
    function _.hubRequestManager(uint64 poolId, uint16 centrifugeId) external
        => hrHubRequestManagerCVL(centrifugeId) expect address UNRESOLVED;
    function _.setHubRequestManager(uint64 poolId, uint16 centrifugeId, address manager) external
        => hrSetHubRequestManagerCVL(centrifugeId, manager) expect void UNRESOLVED;
    function _.bridgingHook(uint64 poolId) external
        => ghostHrBridgingHook expect address UNRESOLVED;
    function _.setBridgingHook(uint64 poolId, address h) external
        => hrSetBridgingHookCVL(h) expect void UNRESOLVED;

    // SCOPE: no rule reads metadata or authorizations through this model.
    function _.setMetadata(uint64 poolId, bytes metadata) external
        => NONDET UNRESOLVED;
    function _.initiateAuthorization(uint64 poolId, address who, bytes data) external
        => NONDET UNRESOLVED;
    function _.cancelAuthorization(uint64 poolId, address who, bytes data) external
        => NONDET UNRESOLVED;
}

function hrExistsCVL(uint64 poolId) returns bool {
    require(VALID_POOL(poolId), "SCOPE: modelled pools stand for any");
    return ghostHrCurrency128 != 0;
}

function hrRegisterAssetCVL(uint128 assetId, uint8 decimals) {
    require(assetId != 0 && decimals <= 18 && (!ghostHrAssetRegistered[assetId]
        || ghostHrAssetDecimals8[assetId] == 0 || ghostHrAssetDecimals8[assetId] == decimals),
        "ASSERT: a nonzero asset of at most 18 decimals, a set precision unchanged");
    ghostHrAssetRegistered[assetId] = true;
    ghostHrAssetDecimals8[assetId] = decimals;
}

function hrIsRegisteredCVL(uint128 assetId) returns bool {
    return ghostHrAssetRegistered[assetId];
}

function hrDecimalsCVL() returns uint8 {
    require(ghostHrCurrency128 != 0 && ghostHrAssetRegistered[ghostHrCurrency128], "ASSERT: the pool's currency must be registered");
    return require_uint8(ghostHrAssetDecimals8[ghostHrCurrency128]);
}

function hrAssetDecimalsCVL(uint128 assetId) returns uint8 {
    if (!ghostHrAssetRegistered[assetId]) {
        revert("AssetNotFound");
    }
    return require_uint8(ghostHrAssetDecimals8[assetId]);
}

function assumeAssetDecimalsCapped() {
    require(forall mathint a. ghostHrAssetDecimals8[a] <= 18, "PROVED: assetDecimalsCapped (HubRegistry)");
}

function hrUpdateManagerCVL(address who, bool canManage) {
    require(ghostHrCurrency128 != 0 && who != 0, "ASSERT: the pool must exist and the account be set");
    ghostHrManager[who] = canManage;
}

function hrRegisterPoolCVL(uint64 poolId, address admin, uint128 currency) {
    require(poolId != 0 && admin != 0 && currency != 0 && ghostHrAssetRegistered[currency]
        && ghostHrCurrency128 == 0, "ASSERT: a new pool, a manager and a registered currency");
    ghostHrCurrency128 = currency;
    ghostHrManager[admin] = true;
}

function hrSetPolicyCVL(address policy) {
    require(ghostHrCurrency128 != 0, "ASSERT: the pool must exist");
    ghostHrPolicy = policy;
    ghostHrPolicyNonce64 = require_uint64(ghostHrPolicyNonce64 + 1);
}

function hrUpdateCurrencyCVL(uint128 currency) {
    require(ghostHrCurrency128 != 0 && currency != 0 && ghostHrAssetRegistered[currency]
        && ghostHrAssetDecimals8[currency] == ghostHrAssetDecimals8[ghostHrCurrency128],
        "ASSERT: existing pool, registered currency of same decimals");
    ghostHrCurrency128 = currency;
}

function hrHubRequestManagerCVL(uint16 centrifugeId) returns address {
    return ghostHrHubRequestManager[centrifugeId];
}

function hrSetHubRequestManagerCVL(uint16 centrifugeId, address manager) {
    require(ghostHrCurrency128 != 0, "ASSERT: the pool must exist");
    ghostHrHubRequestManager[centrifugeId] = manager;
}

function hrSetBridgingHookCVL(address h) {
    require(ghostHrCurrency128 != 0, "ASSERT: the pool must exist");
    ghostHrBridgingHook = h;
}
