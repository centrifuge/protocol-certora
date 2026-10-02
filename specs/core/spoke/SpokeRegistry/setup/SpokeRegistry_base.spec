// SpokeRegistry. Setup: mirrors of pools, classes, assets, roles and prices.

import "../../../../shared/domains/pool.spec";
import "../../../../shared/env.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/single_share_class.spec";

using SpokeRegistry as _SpokeRegistry;

methods {
    function SpokeRegistry._authId(SpokeRegistry.PoolId poolId, address policy_, uint64 nonce_, bytes calldata data) internal returns (bytes32)
        => spokeRegistryAuthIdCVL(poolId, policy_, nonce_, data);

    function _SpokeRegistry.wards(address) external returns (uint256) envfree;
}

// The keccak of _authId, replaced by a ghost over (pool, policy, nonce, data).
persistent ghost mapping(uint64 => mapping(address => mapping(uint64 => mapping(bytes32 => bytes32)))) ghostSrAuthId {
    // UNSAFE: the image is never zero, so an empty slot means no grant.
    axiom forall uint64 p. forall address pol. forall uint64 n. forall bytes32 h.
        ghostSrAuthId[p][pol][n][h] != to_bytes32(0);

    // SAFE: injective as keccak is, so no key's grant aliases another's.
    axiom forall uint64 p1. forall uint64 p2. forall address pol1. forall address pol2.
        forall uint64 n1. forall uint64 n2. forall bytes32 h1. forall bytes32 h2.
            (p1 != p2 || pol1 != pol2 || n1 != n2 || h1 != h2)
                => ghostSrAuthId[p1][pol1][n1][h1] != ghostSrAuthId[p2][pol2][n2][h2];
}

function spokeRegistryAuthIdCVL(SpokeRegistry.PoolId poolId, address policy_, uint64 nonce_, bytes data) returns bytes32 {
    require(VALID_POOL(poolId), "SCOPE: modelled pools stand for any");
    return ghostSrAuthId[poolId][policy_][nonce_][keccak256(data)];
}

definition EXCLUDED_FUNCTION_SR(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

persistent ghost mathint ghostSrCreatedAt64 {
    init_state axiom ghostSrCreatedAt64 == 0;
    axiom ghostSrCreatedAt64 >= 0 && ghostSrCreatedAt64 <= max_uint64;
}

hook Sload uint64 val _SpokeRegistry.pool[KEY SpokeRegistry.PoolId p].createdAt {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostSrCreatedAt64 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.pool[KEY SpokeRegistry.PoolId p].createdAt uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostSrCreatedAt64 = val;
}

persistent ghost mapping(address => mathint) ghostSrTokenPoolId64 {
    init_state axiom forall address t. ghostSrTokenPoolId64[t] == 0;
    axiom forall address t. ghostSrTokenPoolId64[t] >= 0 && ghostSrTokenPoolId64[t] <= max_uint64;
}

persistent ghost mapping(address => bytes16) ghostSrTokenScId {
    init_state axiom forall address t. ghostSrTokenScId[t] == to_bytes16(0);
}

persistent ghost address ghostSrRequestManager {
    init_state axiom ghostSrRequestManager == 0;
}

hook Sload address val _SpokeRegistry.requestManager[KEY SpokeRegistry.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostSrRequestManager == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.requestManager[KEY SpokeRegistry.PoolId p] address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostSrRequestManager = val;
}

persistent ghost address ghostSrShareToken {
    init_state axiom ghostSrShareToken == 0;
}

persistent ghost address ghostSrRegistrar {
    init_state axiom ghostSrRegistrar == 0;
}

persistent ghost mathint ghostSrPricePoolPerShare128 {
    init_state axiom ghostSrPricePoolPerShare128 == 0;
    axiom ghostSrPricePoolPerShare128 >= 0 && ghostSrPricePoolPerShare128 <= max_uint128;
}

persistent ghost mathint ghostSrPricePoolPerShareComputedAt64 {
    init_state axiom ghostSrPricePoolPerShareComputedAt64 == 0;
    axiom ghostSrPricePoolPerShareComputedAt64 >= 0 && ghostSrPricePoolPerShareComputedAt64 <= max_uint64;
}

hook Sload address val _SpokeRegistry.shareClass[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc].shareToken {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSrShareToken == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.shareClass[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc].shareToken address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSrShareToken = val;
}

hook Sload address val _SpokeRegistry.shareClass[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc].registrar {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSrRegistrar == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.shareClass[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc].registrar address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSrRegistrar = val;
}

persistent ghost mapping(address => bool) ghostSrManager {
    init_state axiom forall address who. !ghostSrManager[who];
}

hook Sload bool val _SpokeRegistry.manager[KEY SpokeRegistry.PoolId p][KEY address who] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostSrManager[who] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.manager[KEY SpokeRegistry.PoolId p][KEY address who] bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostSrManager[who] = val;
}

persistent ghost mapping(address => bool) ghostSrBridger {
    init_state axiom forall address who. !ghostSrBridger[who];
}

hook Sload bool val _SpokeRegistry.bridger[KEY SpokeRegistry.PoolId p][KEY address who] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostSrBridger[who] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.bridger[KEY SpokeRegistry.PoolId p][KEY address who] bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostSrBridger[who] = val;
}

persistent ghost address ghostSrPolicy {
    init_state axiom ghostSrPolicy == 0;
}

persistent ghost uint64 ghostSrPolicyNonce64 {
    init_state axiom ghostSrPolicyNonce64 == 0;
}

persistent ghost mapping(bytes32 => mathint) ghostSrAuthorizations256 {
    init_state axiom forall bytes32 id. ghostSrAuthorizations256[id] == 0;
    axiom forall bytes32 id. ghostSrAuthorizations256[id] >= 0 && ghostSrAuthorizations256[id] <= max_uint256;
}

hook Sload uint256 val _SpokeRegistry.authorizations[KEY bytes32 id] {
    require(ghostSrAuthorizations256[id] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.authorizations[KEY bytes32 id] uint256 val {
    ghostSrAuthorizations256[id] = val;
}

persistent ghost mathint ghostSrAssetCounter64 {
    init_state axiom ghostSrAssetCounter64 == 0;
    axiom ghostSrAssetCounter64 >= 0 && ghostSrAssetCounter64 <= max_uint64;
}

hook Sload uint64 val _SpokeRegistry._assetCounter {
    require(ghostSrAssetCounter64 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._assetCounter uint64 val {
    ghostSrAssetCounter64 = val;
}

persistent ghost mapping(uint128 => address) ghostSrIdToAssetAsset {
    init_state axiom forall uint128 aid. ghostSrIdToAssetAsset[aid] == 0;
}

persistent ghost mapping(uint128 => mathint) ghostSrIdToAssetTokenId256 {
    init_state axiom forall uint128 aid. ghostSrIdToAssetTokenId256[aid] == 0;
    axiom forall uint128 aid. ghostSrIdToAssetTokenId256[aid] >= 0 && ghostSrIdToAssetTokenId256[aid] <= max_uint256;
}

hook Sload address val _SpokeRegistry._idToAsset[KEY SpokeRegistry.AssetId aid].asset {
    require(ghostSrIdToAssetAsset[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._idToAsset[KEY SpokeRegistry.AssetId aid].asset address val {
    ghostSrIdToAssetAsset[aid] = val;
}

hook Sload uint256 val _SpokeRegistry._idToAsset[KEY SpokeRegistry.AssetId aid].tokenId {
    require(ghostSrIdToAssetTokenId256[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._idToAsset[KEY SpokeRegistry.AssetId aid].tokenId uint256 val {
    ghostSrIdToAssetTokenId256[aid] = val;
}

persistent ghost mapping(address => mapping(mathint => uint128)) ghostSrAssetToId128 {
    init_state axiom forall address a. forall mathint t. ghostSrAssetToId128[a][t] == 0;
}

hook Sload SpokeRegistry.AssetId val _SpokeRegistry._assetToId[KEY address a][KEY uint256 t] {
    require(ghostSrAssetToId128[a][t] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._assetToId[KEY address a][KEY uint256 t] SpokeRegistry.AssetId val {
    ghostSrAssetToId128[a][t] = val;
}

persistent ghost mapping(uint128 => mathint) ghostSrPricePoolPerAsset128 {
    init_state axiom forall uint128 aid. ghostSrPricePoolPerAsset128[aid] == 0;
    axiom forall uint128 aid. ghostSrPricePoolPerAsset128[aid] >= 0 && ghostSrPricePoolPerAsset128[aid] <= max_uint128;
}

persistent ghost mapping(uint128 => mathint) ghostSrPricePoolPerAssetComputedAt64 {
    init_state axiom forall uint128 aid. ghostSrPricePoolPerAssetComputedAt64[aid] == 0;
    axiom forall uint128 aid. ghostSrPricePoolPerAssetComputedAt64[aid] >= 0
        && ghostSrPricePoolPerAssetComputedAt64[aid] <= max_uint64;
}

persistent ghost mapping(address => uint64) ghostSrVaultPoolId64 {
    init_state axiom forall address v. ghostSrVaultPoolId64[v] == 0;
}

persistent ghost mapping(address => bytes16) ghostSrVaultScId {
    init_state axiom forall address v. ghostSrVaultScId[v] == to_bytes16(0);
}

persistent ghost mapping(address => uint128) ghostSrVaultAssetId128 {
    init_state axiom forall address v. ghostSrVaultAssetId128[v] == 0;
}

persistent ghost mapping(address => address) ghostSrVaultAsset {
    init_state axiom forall address v. ghostSrVaultAsset[v] == 0;
}

persistent ghost mapping(address => mathint) ghostSrVaultTokenId256 {
    init_state axiom forall address v. ghostSrVaultTokenId256[v] == 0;
    axiom forall address v. ghostSrVaultTokenId256[v] >= 0 && ghostSrVaultTokenId256[v] <= max_uint256;
}

persistent ghost mapping(address => bool) ghostSrVaultIsLinked {
    init_state axiom forall address v. !ghostSrVaultIsLinked[v];
}

hook Sload SpokeRegistry.AssetId val _SpokeRegistry._vaultDetails[KEY address v].assetId {
    require(ghostSrVaultAssetId128[v] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._vaultDetails[KEY address v].assetId SpokeRegistry.AssetId val {
    ghostSrVaultAssetId128[v] = val;
}

hook Sload address val _SpokeRegistry._vaultDetails[KEY address v].asset {
    require(ghostSrVaultAsset[v] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._vaultDetails[KEY address v].asset address val {
    ghostSrVaultAsset[v] = val;
}

hook Sload uint256 val _SpokeRegistry._vaultDetails[KEY address v].tokenId {
    require(ghostSrVaultTokenId256[v] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._vaultDetails[KEY address v].tokenId uint256 val {
    ghostSrVaultTokenId256[v] = val;
}

hook Sload bool val _SpokeRegistry._vaultDetails[KEY address v].isLinked {
    require(ghostSrVaultIsLinked[v] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._vaultDetails[KEY address v].isLinked bool val {
    ghostSrVaultIsLinked[v] = val;
}

function setupSpokeRegistry(env e) {
    setupEnv(e);
    setupPoolMode();
    setupShareClassMode();
    require(e.msg.sender != _SpokeRegistry, "SAFE: the spoke registry never calls itself");
}

hook Sload SpokeRegistry.PoolId val _SpokeRegistry.tokenDetails[KEY address t].poolId {
    require(ghostSrTokenPoolId64[t] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.tokenDetails[KEY address t].poolId SpokeRegistry.PoolId val {
    ghostSrTokenPoolId64[t] = val;
}

// ShareClassId by byte range, a left-aligned bytes16 never moves its mirror.
hook Sload uint128 val _SpokeRegistry.tokenDetails[KEY address t].(offset 8) {
    require(ghostSrTokenScId[t] == to_bytes16(val), "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.tokenDetails[KEY address t].(offset 8) uint128 val {
    ghostSrTokenScId[t] = to_bytes16(val);
}

hook Sload SpokeRegistry.D18 val _SpokeRegistry.shareClass[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc].pricePoolPerShare.price {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSrPricePoolPerShare128 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.shareClass[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc].pricePoolPerShare.price SpokeRegistry.D18 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSrPricePoolPerShare128 = assert_uint128(val);
}

hook Sload uint64 val _SpokeRegistry.shareClass[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc].pricePoolPerShare.computedAt {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSrPricePoolPerShareComputedAt64 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry.shareClass[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc].pricePoolPerShare.computedAt uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSrPricePoolPerShareComputedAt64 = val;
}

hook Sload address val _SpokeRegistry._policy[KEY SpokeRegistry.PoolId p].policy {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostSrPolicy == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._policy[KEY SpokeRegistry.PoolId p].policy address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostSrPolicy = val;
}

hook Sload uint64 val _SpokeRegistry._policy[KEY SpokeRegistry.PoolId p].nonce {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostSrPolicyNonce64 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._policy[KEY SpokeRegistry.PoolId p].nonce uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostSrPolicyNonce64 = val;
}

hook Sload SpokeRegistry.D18 val _SpokeRegistry._pricePoolPerAsset[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc][KEY SpokeRegistry.AssetId aid].price {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSrPricePoolPerAsset128[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._pricePoolPerAsset[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc][KEY SpokeRegistry.AssetId aid].price SpokeRegistry.D18 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSrPricePoolPerAsset128[aid] = val;
}

hook Sload uint64 val _SpokeRegistry._pricePoolPerAsset[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc][KEY SpokeRegistry.AssetId aid].computedAt {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSrPricePoolPerAssetComputedAt64[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._pricePoolPerAsset[KEY SpokeRegistry.PoolId p][KEY SpokeRegistry.ShareClassId sc][KEY SpokeRegistry.AssetId aid].computedAt uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSrPricePoolPerAssetComputedAt64[aid] = val;
}

hook Sload SpokeRegistry.PoolId val _SpokeRegistry._vaultDetails[KEY address v].poolId {
    require(ghostSrVaultPoolId64[v] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._vaultDetails[KEY address v].poolId SpokeRegistry.PoolId val {
    ghostSrVaultPoolId64[v] = val;
}

hook Sload uint128 val _SpokeRegistry._vaultDetails[KEY address v].(offset 8) {
    require(ghostSrVaultScId[v] == to_bytes16(val), "SAFE: mirror tracks storage");
}

hook Sstore _SpokeRegistry._vaultDetails[KEY address v].(offset 8) uint128 val {
    ghostSrVaultScId[v] = to_bytes16(val);
}

function assumeManagerImpliesActivePool() {
    require(forall address who. ghostSrManager[who] => ghostSrCreatedAt64 != 0,
        "PROVED: managerImpliesActivePool (SpokeRegistry)");
}

function assumeAssetReverseResolvesBack() {
    require(forall address a. forall mathint t. ghostSrAssetToId128[a][t] != 0 => (
            ghostSrIdToAssetAsset[ghostSrAssetToId128[a][t]] == a
            && ghostSrIdToAssetTokenId256[ghostSrAssetToId128[a][t]] == t
        ),
        "PROVED: assetReverseResolvesBack (SpokeRegistry)");
}

function assumeNullAssetNeverRegistered() {
    require(forall mathint t. ghostSrAssetToId128[0][t] == 0, "PROVED: nullAssetNeverRegistered (SpokeRegistry)");
}

function assumeLinkedVaultIsRegistered() {
    require(forall address v. ghostSrVaultIsLinked[v] => ghostSrVaultAsset[v] != 0,
        "PROVED: linkedVaultIsRegistered (SpokeRegistry)");
}

function SETUP_SR(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupSpokeRegistry(e);
}
