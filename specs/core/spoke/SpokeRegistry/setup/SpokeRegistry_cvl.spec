// SpokeRegistry. Model: ghost-backed registry for scenes not compiling it.

persistent ghost mapping(address => bool) ghostSrManager;
persistent ghost mapping(address => bool) ghostSrBridger;
persistent ghost address ghostSrPolicy;
persistent ghost address ghostSrRequestManager;
persistent ghost address ghostSrShareToken;
persistent ghost address ghostSrRegistrar;
persistent ghost mapping(address => mapping(mathint => uint128)) ghostSrAssetToId128;
persistent ghost mapping(uint128 => address) ghostSrIdToAssetAsset;
persistent ghost mapping(uint128 => mathint) ghostSrIdToAssetTokenId256 {
    axiom forall uint128 id. ghostSrIdToAssetTokenId256[id] >= 0 && ghostSrIdToAssetTokenId256[id] <= max_uint256;
}
persistent ghost uint64 ghostSrCreatedAt64;
persistent ghost mapping(address => mathint) ghostSrTokenPoolId64 {
    axiom forall address t. ghostSrTokenPoolId64[t] >= 0 && ghostSrTokenPoolId64[t] <= max_uint64;
}
persistent ghost mapping(address => bytes16) ghostSrTokenScId;
persistent ghost uint64 ghostSrPolicyNonce64;
persistent ghost uint128 ghostSrPricePoolPerShare128;
persistent ghost uint64 ghostSrPricePoolPerShareComputedAt64;
persistent ghost mapping(uint128 => mathint) ghostSrPricePoolPerAsset128 {
    axiom forall uint128 a. ghostSrPricePoolPerAsset128[a] >= 0 && ghostSrPricePoolPerAsset128[a] <= max_uint128;
}
persistent ghost mapping(uint128 => mathint) ghostSrPricePoolPerAssetComputedAt64 {
    axiom forall uint128 a. ghostSrPricePoolPerAssetComputedAt64[a] >= 0 && ghostSrPricePoolPerAssetComputedAt64[a] <= max_uint64;
}
persistent ghost mapping(address => uint64) ghostSrVaultPoolId64;
persistent ghost mapping(address => bytes16) ghostSrVaultScId;
persistent ghost mapping(address => uint128) ghostSrVaultAssetId128;
persistent ghost mapping(address => address) ghostSrVaultAsset;
persistent ghost mapping(address => mathint) ghostSrVaultTokenId256 {
    axiom forall address v. ghostSrVaultTokenId256[v] >= 0 && ghostSrVaultTokenId256[v] <= max_uint256;
}
persistent ghost mapping(address => bool) ghostSrVaultIsLinked;
persistent ghost mathint ghostSrFaceAuthCount {
    axiom ghostSrFaceAuthCount >= 0;
}
persistent ghost bytes32 ghostSrFaceLastAuthDataHash;
persistent ghost bool ghostSrFaceLastAuthGranted;
persistent ghost mathint ghostSrFaceLastCreateCid16;

methods {
    // SCOPE: the pinned class's rows answer any pool and class argument.
    function _.shareToken(uint64 poolId, bytes16 scId) external
        => ghostSrShareToken expect address UNRESOLVED;
    function _.shareTokenAndRegistrar(uint64 poolId, bytes16 scId) external
        => srShareTokenAndRegistrarCVL() expect (address, address) UNRESOLVED;
    function _.requestManager(uint64 poolId) external
        => ghostSrRequestManager expect address UNRESOLVED;

    function _.assetToId(address asset, uint256 tokenId, bool revertOnNull) external
        => srAssetToIdRevertCVL(asset, tokenId, revertOnNull) expect uint128 UNRESOLVED;
    // SCOPE: registerAsset's non-reverting overload, 0 when unknown.
    function _.assetToId(address asset, uint256 tokenId) external
        => srAssetToIdCVL(asset, tokenId) expect uint128 UNRESOLVED;
    function _.createAssetId(uint16 centrifugeId, address asset, uint256 tokenId) external
        => srCreateAssetIdCVL(centrifugeId, asset, tokenId) expect uint128 UNRESOLVED;
    function _.idToAsset(uint128 assetId, bool revertOnNull) external
        => srIdToAssetCVL(assetId, revertOnNull) expect (address, uint256) UNRESOLVED;

    // SCOPE: the pinned pool's rows answer, the pool id is not compared.
    function _.manager(uint64 poolId, address who) external
        => ghostSrManager[who] expect bool UNRESOLVED;
    function _.bridger(uint64 poolId, address who) external
        => ghostSrBridger[who] expect bool UNRESOLVED;
    function _.policy(uint64 poolId) external
        => ghostSrPolicy expect address UNRESOLVED;

    function _.addPool(uint64 poolId) external with (env e)
        => srAddPoolCVL(e, poolId) expect void UNRESOLVED;
    function _.addShareClass(uint64 poolId, bytes16 scId, address shareToken, address registrar) external
        => srAddShareClassCVL(poolId, scId, shareToken, registrar) expect void UNRESOLVED;
    function _.setRequestManager(uint64 poolId, address manager) external
        => srSetRequestManagerCVL(manager) expect void UNRESOLVED;
    function _.updateManager(uint64 poolId, address who, bool canManage) external
        => srUpdateManagerCVL(who, canManage) expect void UNRESOLVED;
    function _.updateBridger(uint64 poolId, address who, bool canBridge) external
        => srUpdateBridgerCVL(who, canBridge) expect void UNRESOLVED;
    function _.setPolicy(uint64 poolId, address policy) external
        => srSetPolicyCVL(policy) expect void UNRESOLVED;
    // SCOPE: a recorder of what was filed, the id ledger is not modelled.
    function _.authorize(uint64 poolId, bytes data) external
        => srAuthorizeCVL(data, true) expect void UNRESOLVED;
    function _.unauthorize(uint64 poolId, bytes data) external
        => srAuthorizeCVL(data, false) expect void UNRESOLVED;

    function _.updatePricePoolPerShare(uint64 poolId, bytes16 scId, uint128 price, uint64 computedAt) external with (env e)
        => srUpdatePricePoolPerShareCVL(e, scId, price, computedAt) expect void UNRESOLVED;
    function _.updatePricePoolPerAsset(uint64 poolId, bytes16 scId, uint128 assetId, uint128 price, uint64 computedAt) external with (env e)
        => srUpdatePricePoolPerAssetCVL(e, scId, assetId, price, computedAt) expect void UNRESOLVED;

    function _.registerVault(uint64 poolId, bytes16 scId, uint128 assetId, address asset, uint256 tokenId, address factory, address vault, bytes payload) external
        => srRegisterVaultCVL(poolId, scId, assetId, asset, tokenId, vault) expect void UNRESOLVED;
    function _.linkVault(uint64 poolId, bytes16 scId, uint128 assetId, address vault) external
        => srLinkVaultCVL(poolId, scId, assetId, vault, true) expect void UNRESOLVED;
    function _.unlinkVault(uint64 poolId, bytes16 scId, uint128 assetId, address vault) external
        => srLinkVaultCVL(poolId, scId, assetId, vault, false) expect void UNRESOLVED;

    // SCOPE: one pool per conf, the pool argument is not compared.
    function _.isPoolActive(uint64 poolId) external
        => srIsPoolActiveCVL(poolId) expect bool UNRESOLVED;
    function _.hasShareClass(uint64 poolId, bytes16 scId) external
        => srHasShareClassCVL(scId) expect bool UNRESOLVED;
    function _.tokenDetails(address token) external
        => srTokenDetailsCVL(token) expect (uint64, bytes16) UNRESOLVED;
    function _.vaultDetails(address vault) external
        => srVaultDetailsCVL(vault) expect (uint64, bytes16, uint128, address, uint256, bool) UNRESOLVED;
    function _.isLinked(address vault) external
        => ghostSrVaultIsLinked[vault] expect bool UNRESOLVED;
    function _.pricePoolPerShare(uint64 poolId, bytes16 scId, bool checkValidity) external
        => srPricePoolPerShareCVL(scId, checkValidity) expect uint128 UNRESOLVED;
    function _.pricePoolPerAsset(uint64 poolId, bytes16 scId, uint128 assetId, bool checkValidity) external
        => srPricePoolPerAssetCVL(scId, assetId, checkValidity) expect uint128 UNRESOLVED;
    function _.pricePoolPerShareComputedAt(uint64 poolId, bytes16 scId) external
        => srPricePoolPerShareComputedAtCVL(scId) expect uint64 UNRESOLVED;
    function _.pricePoolPerAssetComputedAt(uint64 poolId, bytes16 scId, uint128 assetId) external
        => srPricePoolPerAssetComputedAtCVL(scId, assetId) expect uint64 UNRESOLVED;
}

function srShareTokenAndRegistrarCVL() returns (address, address) {
    return (ghostSrShareToken, ghostSrRegistrar);
}

function srAssetToIdCVL(address asset, uint256 tokenId) returns uint128 {
    return ghostSrAssetToId128[asset][tokenId];
}

function srAssetToIdRevertCVL(address asset, uint256 tokenId, bool revertOnNull) returns uint128 {
    mathint id = ghostSrAssetToId128[asset][tokenId];
    require(!revertOnNull || id != 0, "ASSERT: a strict lookup needs a registered asset");
    return require_uint128(id);
}

function srCreateAssetIdCVL(uint16 centrifugeId, address asset, uint256 tokenId) returns uint128 {
    require(asset != 0, "ASSERT: the asset address must be set");
    require(centrifugeId != 0, "ASSERT: the network id must be nonzero");
    require(ghostSrAssetToId128[asset][tokenId] == 0, "ASSERT: the asset must not be registered yet");
    uint128 id;
    require(id != 0, "PROVED: registeredAssetIdWellFormed (SpokeRegistry)");
    ghostSrFaceLastCreateCid16 = centrifugeId;
    ghostSrAssetToId128[asset][tokenId] = id;
    ghostSrIdToAssetAsset[id] = asset;
    ghostSrIdToAssetTokenId256[id] = tokenId;
    return id;
}

function srIdToAssetCVL(uint128 assetId, bool revertOnNull) returns (address, uint256) {
    address asset = ghostSrIdToAssetAsset[assetId];
    require(!revertOnNull || asset != 0, "ASSERT: a strict lookup needs a registered asset");
    return (asset, require_uint256(ghostSrIdToAssetTokenId256[assetId]));
}

function srAddPoolCVL(env e, uint64 poolId) {
    require(poolId != 0 && ghostSrCreatedAt64 == 0, "ASSERT: a nonzero pool id, not yet added");
    ghostSrCreatedAt64 = assert_uint64(e.block.timestamp);
}

// SCOPE: NotAContract on the share token has no CVL counterpart.
function srAddShareClassCVL(uint64 poolId, bytes16 scId, address shareToken, address registrar) {
    require(ghostSrCreatedAt64 != 0, "ASSERT: the pool must exist");
    require(registrar != 0, "ASSERT: the registrar must be set");
    if (scId == ghostShareClassA) {
        require(ghostSrShareToken == 0, "ASSERT: the share class must not be registered yet");
        require(ghostSrTokenPoolId64[shareToken] == 0, "ASSERT: the share token must not be registered yet");
        ghostSrShareToken = shareToken;
        ghostSrRegistrar = registrar;
        ghostSrTokenPoolId64[shareToken] = poolId;
        ghostSrTokenScId[shareToken] = scId;
    }
}

function srSetRequestManagerCVL(address manager) {
    require(ghostSrCreatedAt64 != 0, "ASSERT: the pool must exist");
    ghostSrRequestManager = manager;
}

function srUpdateManagerCVL(address who, bool canManage) {
    require(ghostSrCreatedAt64 != 0, "ASSERT: the pool must exist");
    ghostSrManager[who] = canManage;
}

function srUpdateBridgerCVL(address who, bool canBridge) {
    require(ghostSrCreatedAt64 != 0, "ASSERT: the pool must exist");
    ghostSrBridger[who] = canBridge;
}

function srSetPolicyCVL(address policy) {
    require(ghostSrCreatedAt64 != 0, "ASSERT: the pool must exist");
    ghostSrPolicy = policy;
    ghostSrPolicyNonce64 = require_uint64(ghostSrPolicyNonce64 + 1);
}

function srAuthorizeCVL(bytes data, bool granted) {
    if (granted) {
        require(ghostSrPolicy != 0, "ASSERT: a pool policy must be installed");
    }
    ghostSrFaceAuthCount = ghostSrFaceAuthCount + 1;
    ghostSrFaceLastAuthDataHash = keccak256(data);
    ghostSrFaceLastAuthGranted = granted;
}

function srUpdatePricePoolPerShareCVL(env e, bytes16 scId, uint128 price, uint64 computedAt) {
    require(scId == ghostShareClassA && ghostSrShareToken != 0, "ASSERT: the share class must exist");
    require(computedAt <= e.block.timestamp, "ASSERT: no price stamped in the future");
    require(computedAt >= ghostSrPricePoolPerShareComputedAt64, "ASSERT: no price older than the stored one");
    ghostSrPricePoolPerShare128 = price;
    ghostSrPricePoolPerShareComputedAt64 = computedAt;
}

function srUpdatePricePoolPerAssetCVL(env e, bytes16 scId, uint128 assetId, uint128 price, uint64 computedAt) {
    require(scId == ghostShareClassA && ghostSrShareToken != 0, "ASSERT: the share class must exist");
    require(ghostSrIdToAssetAsset[assetId] != 0, "ASSERT: the asset must be registered");
    require(computedAt <= e.block.timestamp, "ASSERT: no price stamped in the future");
    require(computedAt >= ghostSrPricePoolPerAssetComputedAt64[assetId], "ASSERT: no price older than the stored one");
    ghostSrPricePoolPerAsset128[assetId] = price;
    ghostSrPricePoolPerAssetComputedAt64[assetId] = computedAt;
}

// SCOPE: NotAContract on the vault has no CVL counterpart.
function srRegisterVaultCVL(uint64 poolId, bytes16 scId, uint128 assetId, address asset, uint256 tokenId, address vault) {
    require(scId == ghostShareClassA && ghostSrShareToken != 0, "ASSERT: the share class must exist");
    require(ghostSrIdToAssetAsset[assetId] != 0
        && ghostSrIdToAssetAsset[assetId] == asset
        && ghostSrIdToAssetTokenId256[assetId] == tokenId, "ASSERT: the asset must be registered as named");
    require(ghostSrVaultAsset[vault] == 0, "ASSERT: the vault must not be registered yet");
    ghostSrVaultPoolId64[vault] = poolId;
    ghostSrVaultScId[vault] = scId;
    ghostSrVaultAssetId128[vault] = assetId;
    ghostSrVaultAsset[vault] = asset;
    ghostSrVaultTokenId256[vault] = tokenId;
    ghostSrVaultIsLinked[vault] = false;
}

function srLinkVaultCVL(uint64 poolId, bytes16 scId, uint128 assetId, address vault, bool link) {
    require(ghostSrIdToAssetAsset[assetId] != 0, "ASSERT: the asset must be registered");
    require(ghostSrVaultIsLinked[vault] != link, "ASSERT: link only an unlinked vault, unlink a linked one");
    require(ghostSrVaultAsset[vault] != 0, "ASSERT: the vault must be registered");
    require(ghostSrVaultAssetId128[vault] == assetId, "ASSERT: the vault must serve that asset");
    require(ghostSrVaultPoolId64[vault] == poolId && ghostSrVaultScId[vault] == scId, "ASSERT: the vault must belong to the pool and share class");
    ghostSrVaultIsLinked[vault] = link;
}

function srIsPoolActiveCVL(uint64 poolId) returns bool {
    return poolId != 0 && ghostSrCreatedAt64 != 0;
}

function srHasShareClassCVL(bytes16 scId) returns bool {
    return scId == ghostShareClassA && ghostSrShareToken != 0;
}

function srTokenDetailsCVL(address token) returns (uint64, bytes16) {
    return (require_uint64(ghostSrTokenPoolId64[token]), ghostSrTokenScId[token]);
}

function srVaultDetailsCVL(address vault) returns (uint64, bytes16, uint128, address, uint256, bool) {
    return (ghostSrVaultPoolId64[vault], ghostSrVaultScId[vault], ghostSrVaultAssetId128[vault],
        ghostSrVaultAsset[vault], require_uint256(ghostSrVaultTokenId256[vault]), ghostSrVaultIsLinked[vault]);
}

function srPricePoolPerShareComputedAtCVL(bytes16 scId) returns uint64 {
    return scId == ghostShareClassA ? ghostSrPricePoolPerShareComputedAt64 : 0;
}

function srPricePoolPerAssetComputedAtCVL(bytes16 scId, uint128 assetId) returns uint64 {
    return scId == ghostShareClassA ? require_uint64(ghostSrPricePoolPerAssetComputedAt64[assetId]) : 0;
}

function srPricePoolPerShareCVL(bytes16 scId, bool checkValidity) returns uint128 {
    if (checkValidity && srPricePoolPerShareComputedAtCVL(scId) == 0) {
        revert("InvalidPrice");
    }
    return scId == ghostShareClassA ? ghostSrPricePoolPerShare128 : 0;
}

function srPricePoolPerAssetCVL(bytes16 scId, uint128 assetId, bool checkValidity) returns uint128 {
    if (checkValidity && srPricePoolPerAssetComputedAtCVL(scId, assetId) == 0) {
        revert("InvalidPrice");
    }
    return scId == ghostShareClassA ? require_uint128(ghostSrPricePoolPerAsset128[assetId]) : 0;
}

function assumeShareTokenIffRegistrar() {
    require((ghostSrRegistrar == 0) <=> (ghostSrShareToken == 0), "PROVED: shareTokenIffRegistrar (SpokeRegistry)");
}
