// Holdings, single-pool lane. Setup: holding rows for the pinned pool and share class.

// Own setup: the primary pins, one pool, class and network; the isolation lanes hook the same rows with two keys.

import "Holdings_base.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/single_share_class.spec";

persistent ghost address ghostHoSnapshotHook {
    init_state axiom ghostHoSnapshotHook == 0;
}

hook Sload address val _Holdings.snapshotHook[KEY Holdings.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHoSnapshotHook == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.snapshotHook[KEY Holdings.PoolId p] address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHoSnapshotHook = val;
}

persistent ghost mathint ghostHoNetworkDeficitCount32 {
    init_state axiom ghostHoNetworkDeficitCount32 == 0;
    axiom ghostHoNetworkDeficitCount32 >= 0 && ghostHoNetworkDeficitCount32 <= max_uint32;
}

hook Sload uint32 val _Holdings.networkDeficitCount[KEY Holdings.PoolId p][KEY uint16 cid] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    require(ghostHoNetworkDeficitCount32 == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.networkDeficitCount[KEY Holdings.PoolId p][KEY uint16 cid] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    ghostHoNetworkDeficitCount32 = val;
}

persistent ghost mathint ghostHoDeficitCount32 {
    init_state axiom ghostHoDeficitCount32 == 0;
    axiom ghostHoDeficitCount32 >= 0 && ghostHoDeficitCount32 <= max_uint32;
}

hook Sload uint32 val _Holdings.deficitCount[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    require(ghostHoDeficitCount32 == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.deficitCount[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    ghostHoDeficitCount32 = val;
}

persistent ghost mapping(uint128 => mathint) ghostHoIncreasedAmount256 {
    init_state axiom forall uint128 a. ghostHoIncreasedAmount256[a] == 0;
    axiom forall uint128 a. ghostHoIncreasedAmount256[a] >= 0 && ghostHoIncreasedAmount256[a] <= max_uint256;
    axiom forall uint128 a. !VALID_ASSET_HO(a) => ghostHoIncreasedAmount256[a] == 0;
}

persistent ghost mapping(uint128 => mathint) ghostHoDecreasedAmount256 {
    init_state axiom forall uint128 a. ghostHoDecreasedAmount256[a] == 0;
    axiom forall uint128 a. ghostHoDecreasedAmount256[a] >= 0 && ghostHoDecreasedAmount256[a] <= max_uint256;
    axiom forall uint128 a. !VALID_ASSET_HO(a) => ghostHoDecreasedAmount256[a] == 0;
}

persistent ghost mapping(uint128 => mathint) ghostHoAssetAmountValue128 {
    init_state axiom forall uint128 a. ghostHoAssetAmountValue128[a] == 0;
    axiom forall uint128 a. ghostHoAssetAmountValue128[a] >= 0 && ghostHoAssetAmountValue128[a] <= max_uint128;
    axiom forall uint128 a. !VALID_ASSET_HO(a) => ghostHoAssetAmountValue128[a] == 0;
}

hook Sload uint128 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].assetAmountValue {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoAssetAmountValue128[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].assetAmountValue uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoAssetAmountValue128[aid] = val;
}

persistent ghost mapping(uint128 => address) ghostHoValuation {
    init_state axiom forall uint128 a. ghostHoValuation[a] == 0;
    axiom forall uint128 a. !VALID_ASSET_HO(a) => ghostHoValuation[a] == 0;
}

hook Sload address val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].valuation {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoValuation[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].valuation address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoValuation[aid] = val;
}

definition HO_DEFICIT_CARDINALITY() returns mathint =
    (ghostHoDecreasedAmount256[ghostHoAssetE1] > ghostHoIncreasedAmount256[ghostHoAssetE1] ? 1 : 0)
    + (ghostHoDecreasedAmount256[ghostHoAssetE2] > ghostHoIncreasedAmount256[ghostHoAssetE2] ? 1 : 0);

persistent ghost mapping(uint16 => bool) ghostHoIsSnapshot {
    init_state axiom forall uint16 cid. !ghostHoIsSnapshot[cid];
}

persistent ghost mapping(uint16 => mathint) ghostHoSnapshotNonce64 {
    init_state axiom forall uint16 cid. ghostHoSnapshotNonce64[cid] == 0;
    axiom forall uint16 cid. ghostHoSnapshotNonce64[cid] >= 0 && ghostHoSnapshotNonce64[cid] <= max_uint64;
}

persistent ghost mapping(uint128 => mapping(uint8 => mathint)) ghostHoAccountId256 {
    init_state axiom forall uint128 a. forall uint8 k. ghostHoAccountId256[a][k] == 0;
    axiom forall uint128 a. forall uint8 k.
        ghostHoAccountId256[a][k] >= 0 && ghostHoAccountId256[a][k] <= max_uint256;
    axiom forall uint128 a. forall uint8 k. !VALID_ASSET_HO(a) => ghostHoAccountId256[a][k] == 0;
}

hook Sload Holdings.AccountId val _Holdings.accountId[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid][KEY uint8 kind] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoAccountId256[aid][kind] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.accountId[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid][KEY uint8 kind] Holdings.AccountId val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoAccountId256[aid][kind] = val;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoIncreasedAmount256[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoIncreasedAmount256[aid] = val;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoDecreasedAmount256[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoDecreasedAmount256[aid] = val;
}

hook Sload bool val _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].isSnapshot {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostHoIsSnapshot[cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].isSnapshot bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostHoIsSnapshot[cid] = val;
}

hook Sload uint64 val _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].nonce {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostHoSnapshotNonce64[cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].nonce uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostHoSnapshotNonce64[cid] = val;
}

function SETUP_HO(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupHoldings(e);
}
