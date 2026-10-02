// Holdings, two-class lane. Setup: holding and snapshot fields mirrored per class.

// Own setup: two classes of the pinned pool; single_pool hooks the same rows pinned to one class.

import "Holdings_base.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/multi_share_class.spec";

persistent ghost mathint ghostHoClassNetworkDeficitCount32 {
    init_state axiom ghostHoClassNetworkDeficitCount32 == 0;
    axiom ghostHoClassNetworkDeficitCount32 >= 0 && ghostHoClassNetworkDeficitCount32 <= max_uint32;
}

hook Sload uint32 val _Holdings.networkDeficitCount[KEY Holdings.PoolId p][KEY uint16 cid] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    require(ghostHoClassNetworkDeficitCount32 == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.networkDeficitCount[KEY Holdings.PoolId p][KEY uint16 cid] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    ghostHoClassNetworkDeficitCount32 = val;
}

persistent ghost mapping(bytes16 => mathint) ghostHoClassDeficitCount32 {
    init_state axiom forall bytes16 sc. ghostHoClassDeficitCount32[sc] == 0;
    axiom forall bytes16 sc. ghostHoClassDeficitCount32[sc] >= 0 && ghostHoClassDeficitCount32[sc] <= max_uint32;
    axiom forall bytes16 sc. !VALID_SC(sc) => ghostHoClassDeficitCount32[sc] == 0;
}

hook Sload uint32 val _Holdings.deficitCount[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    require(ghostHoClassDeficitCount32[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.deficitCount[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    ghostHoClassDeficitCount32[sc] = val;
}

persistent ghost mapping(bytes16 => mapping(uint128 => mathint)) ghostHoClassIncreasedAmount256 {
    init_state axiom forall bytes16 sc. forall uint128 a. ghostHoClassIncreasedAmount256[sc][a] == 0;
    axiom forall bytes16 sc. forall uint128 a.
        ghostHoClassIncreasedAmount256[sc][a] >= 0 && ghostHoClassIncreasedAmount256[sc][a] <= max_uint256;
}

persistent ghost mapping(bytes16 => mapping(uint128 => mathint)) ghostHoClassDecreasedAmount256 {
    init_state axiom forall bytes16 sc. forall uint128 a. ghostHoClassDecreasedAmount256[sc][a] == 0;
    axiom forall bytes16 sc. forall uint128 a.
        ghostHoClassDecreasedAmount256[sc][a] >= 0 && ghostHoClassDecreasedAmount256[sc][a] <= max_uint256;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoClassIncreasedAmount256[sc][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoClassIncreasedAmount256[sc][aid] = val;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoClassDecreasedAmount256[sc][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoClassDecreasedAmount256[sc][aid] = val;
}

definition HO_CLASS_DEFICIT_CARDINALITY() returns mathint =
    (ghostHoClassDecreasedAmount256[ghostShareClassA][ghostHoAssetE1]
        > ghostHoClassIncreasedAmount256[ghostShareClassA][ghostHoAssetE1] ? 1 : 0)
    + (ghostHoClassDecreasedAmount256[ghostShareClassA][ghostHoAssetE2]
        > ghostHoClassIncreasedAmount256[ghostShareClassA][ghostHoAssetE2] ? 1 : 0)
    + (ghostHoClassDecreasedAmount256[ghostShareClassB][ghostHoAssetE1]
        > ghostHoClassIncreasedAmount256[ghostShareClassB][ghostHoAssetE1] ? 1 : 0)
    + (ghostHoClassDecreasedAmount256[ghostShareClassB][ghostHoAssetE2]
        > ghostHoClassIncreasedAmount256[ghostShareClassB][ghostHoAssetE2] ? 1 : 0);

definition HO_SHARE_CLASS_DEFICIT_CARDINALITY(bytes16 c) returns mathint =
    (ghostHoClassDecreasedAmount256[c][ghostHoAssetE1] > ghostHoClassIncreasedAmount256[c][ghostHoAssetE1] ? 1 : 0)
    + (ghostHoClassDecreasedAmount256[c][ghostHoAssetE2] > ghostHoClassIncreasedAmount256[c][ghostHoAssetE2] ? 1 : 0);

function setupHoldingsMultiShareClass(env e) {
    setupHoldings(e);
    require(ghostShareClassA != ghostShareClassB, "SCOPE: two distinct share classes");
}

function SETUP_HO_MC(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupHoldingsMultiShareClass(e);
}

persistent ghost mapping(bytes16 => mapping(uint128 => mathint)) ghostHoClassAssetAmountValue128 {
    init_state axiom forall bytes16 sc. forall uint128 a. ghostHoClassAssetAmountValue128[sc][a] == 0;
    axiom forall bytes16 sc. forall uint128 a.
        ghostHoClassAssetAmountValue128[sc][a] >= 0 && ghostHoClassAssetAmountValue128[sc][a] <= max_uint128;
}

hook Sload uint128 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].assetAmountValue {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoClassAssetAmountValue128[sc][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].assetAmountValue uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoClassAssetAmountValue128[sc][aid] = val;
}

persistent ghost mapping(bytes16 => mapping(uint128 => address)) ghostHoClassValuation {
    init_state axiom forall bytes16 sc. forall uint128 a. ghostHoClassValuation[sc][a] == 0;
}

hook Sload address val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].valuation {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoClassValuation[sc][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].valuation address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoClassValuation[sc][aid] = val;
}

persistent ghost mapping(bytes16 => mapping(uint128 => mapping(uint8 => mathint))) ghostHoClassAccountId256 {
    init_state axiom forall bytes16 sc. forall uint128 a. forall uint8 k. ghostHoClassAccountId256[sc][a][k] == 0;
    axiom forall bytes16 sc. forall uint128 a. forall uint8 k.
        ghostHoClassAccountId256[sc][a][k] >= 0 && ghostHoClassAccountId256[sc][a][k] <= max_uint256;
}

hook Sload Holdings.AccountId val _Holdings.accountId[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid][KEY uint8 kind] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoClassAccountId256[sc][aid][kind] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.accountId[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid][KEY uint8 kind] Holdings.AccountId val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoClassAccountId256[sc][aid][kind] = val;
}

persistent ghost mapping(bytes16 => mapping(uint16 => bool)) ghostHoClassIsSnapshot {
    init_state axiom forall bytes16 sc. forall uint16 cid. !ghostHoClassIsSnapshot[sc][cid];
}

hook Sload bool val _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].isSnapshot {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostHoClassIsSnapshot[sc][cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].isSnapshot bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostHoClassIsSnapshot[sc][cid] = val;
}

persistent ghost mapping(bytes16 => mapping(uint16 => mathint)) ghostHoClassSnapshotNonce64 {
    init_state axiom forall bytes16 sc. forall uint16 cid. ghostHoClassSnapshotNonce64[sc][cid] == 0;
    axiom forall bytes16 sc. forall uint16 cid.
        ghostHoClassSnapshotNonce64[sc][cid] >= 0 && ghostHoClassSnapshotNonce64[sc][cid] <= max_uint64;
}

hook Sload uint64 val _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].nonce {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostHoClassSnapshotNonce64[sc][cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].nonce uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostHoClassSnapshotNonce64[sc][cid] = val;
}
