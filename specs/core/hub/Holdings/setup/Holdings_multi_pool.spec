// Holdings, multi-pool lane. Setup: rows keyed by pool and class, for pool isolation.

// Own setup: two pools with one class each; single_pool hooks the same rows pinned to one pool and class.

import "Holdings_base.spec";
import "../../../../shared/domains/multi_pool.spec";
import "../../../../shared/domains/multi_share_class.spec";

// SCOPE: one class per pinned pool, a pool-keyed mirror is one row.
definition HO_POOL_SLOT(uint64 p, bytes16 sc) returns bool =
    (p == ghostPoolA64 && sc == ghostShareClassA) || (p == ghostPoolB64 && sc == ghostShareClassB);

persistent ghost mapping(uint64 => address) ghostHoPoolSnapshotHook {
    init_state axiom forall uint64 p. ghostHoPoolSnapshotHook[p] == 0;
    axiom forall uint64 p. !VALID_POOL(p) => ghostHoPoolSnapshotHook[p] == 0;
}

hook Sload address val _Holdings.snapshotHook[KEY Holdings.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHoPoolSnapshotHook[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.snapshotHook[KEY Holdings.PoolId p] address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHoPoolSnapshotHook[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostHoPoolNetworkDeficitCount32 {
    init_state axiom forall uint64 p. ghostHoPoolNetworkDeficitCount32[p] == 0;
    axiom forall uint64 p. ghostHoPoolNetworkDeficitCount32[p] >= 0 && ghostHoPoolNetworkDeficitCount32[p] <= max_uint32;
    axiom forall uint64 p. !VALID_POOL(p) => ghostHoPoolNetworkDeficitCount32[p] == 0;
}

hook Sload uint32 val _Holdings.networkDeficitCount[KEY Holdings.PoolId p][KEY uint16 cid] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    require(ghostHoPoolNetworkDeficitCount32[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.networkDeficitCount[KEY Holdings.PoolId p][KEY uint16 cid] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    ghostHoPoolNetworkDeficitCount32[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostHoPoolDeficitCount32 {
    init_state axiom forall uint64 p. ghostHoPoolDeficitCount32[p] == 0;
    axiom forall uint64 p. ghostHoPoolDeficitCount32[p] >= 0 && ghostHoPoolDeficitCount32[p] <= max_uint32;
    axiom forall uint64 p. !VALID_POOL(p) => ghostHoPoolDeficitCount32[p] == 0;
}

hook Sload uint32 val _Holdings.deficitCount[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid] {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    require(ghostHoPoolDeficitCount32[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.deficitCount[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid] uint32 val {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(cid == ghostHoCid16, "UNSAFE: deficits tracked on a single network");
    ghostHoPoolDeficitCount32[p] = val;
}

persistent ghost mapping(uint64 => mapping(uint128 => mathint)) ghostHoPoolIncreasedAmount256 {
    init_state axiom forall uint64 p. forall uint128 a. ghostHoPoolIncreasedAmount256[p][a] == 0;
    axiom forall uint64 p. forall uint128 a.
        ghostHoPoolIncreasedAmount256[p][a] >= 0 && ghostHoPoolIncreasedAmount256[p][a] <= max_uint256;
    axiom forall uint64 p. forall uint128 a.
        (!VALID_POOL(p) || !VALID_ASSET_HO(a)) => ghostHoPoolIncreasedAmount256[p][a] == 0;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoPoolIncreasedAmount256[p][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount uint256 val {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoPoolIncreasedAmount256[p][aid] = val;
}

persistent ghost mapping(uint64 => mapping(uint128 => mathint)) ghostHoPoolDecreasedAmount256 {
    init_state axiom forall uint64 p. forall uint128 a. ghostHoPoolDecreasedAmount256[p][a] == 0;
    axiom forall uint64 p. forall uint128 a.
        ghostHoPoolDecreasedAmount256[p][a] >= 0 && ghostHoPoolDecreasedAmount256[p][a] <= max_uint256;
    axiom forall uint64 p. forall uint128 a.
        (!VALID_POOL(p) || !VALID_ASSET_HO(a)) => ghostHoPoolDecreasedAmount256[p][a] == 0;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoPoolDecreasedAmount256[p][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount uint256 val {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoPoolDecreasedAmount256[p][aid] = val;
}

persistent ghost mapping(uint64 => mapping(uint128 => mathint)) ghostHoPoolAssetAmountValue128 {
    init_state axiom forall uint64 p. forall uint128 a. ghostHoPoolAssetAmountValue128[p][a] == 0;
    axiom forall uint64 p. forall uint128 a.
        ghostHoPoolAssetAmountValue128[p][a] >= 0 && ghostHoPoolAssetAmountValue128[p][a] <= max_uint128;
    axiom forall uint64 p. forall uint128 a.
        (!VALID_POOL(p) || !VALID_ASSET_HO(a)) => ghostHoPoolAssetAmountValue128[p][a] == 0;
}

hook Sload uint128 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].assetAmountValue {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoPoolAssetAmountValue128[p][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].assetAmountValue uint128 val {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoPoolAssetAmountValue128[p][aid] = val;
}

persistent ghost mapping(uint64 => mapping(uint128 => address)) ghostHoPoolValuation {
    init_state axiom forall uint64 p. forall uint128 a. ghostHoPoolValuation[p][a] == 0;
    axiom forall uint64 p. forall uint128 a.
        (!VALID_POOL(p) || !VALID_ASSET_HO(a)) => ghostHoPoolValuation[p][a] == 0;
}

hook Sload address val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].valuation {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoPoolValuation[p][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].valuation address val {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoPoolValuation[p][aid] = val;
}

persistent ghost mapping(uint64 => mapping(uint16 => bool)) ghostHoPoolIsSnapshot {
    init_state axiom forall uint64 p. forall uint16 cid. !ghostHoPoolIsSnapshot[p][cid];
    axiom forall uint64 p. forall uint16 cid. !VALID_POOL(p) => !ghostHoPoolIsSnapshot[p][cid];
}

hook Sload bool val _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].isSnapshot {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostHoPoolIsSnapshot[p][cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].isSnapshot bool val {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostHoPoolIsSnapshot[p][cid] = val;
}

persistent ghost mapping(uint64 => mapping(uint16 => mathint)) ghostHoPoolSnapshotNonce64 {
    init_state axiom forall uint64 p. forall uint16 cid. ghostHoPoolSnapshotNonce64[p][cid] == 0;
    axiom forall uint64 p. forall uint16 cid.
        ghostHoPoolSnapshotNonce64[p][cid] >= 0 && ghostHoPoolSnapshotNonce64[p][cid] <= max_uint64;
    axiom forall uint64 p. forall uint16 cid. !VALID_POOL(p) => ghostHoPoolSnapshotNonce64[p][cid] == 0;
}

hook Sload uint64 val _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].nonce {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostHoPoolSnapshotNonce64[p][cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.snapshot[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid].nonce uint64 val {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostHoPoolSnapshotNonce64[p][cid] = val;
}

// No bound on kind: initialize writes 0..3 but setAccountId takes any.
persistent ghost mapping(uint64 => mapping(uint128 => mapping(uint8 => mathint))) ghostHoPoolAccountId256 {
    init_state axiom forall uint64 p. forall uint128 a. forall uint8 k. ghostHoPoolAccountId256[p][a][k] == 0;
    axiom forall uint64 p. forall uint128 a. forall uint8 k.
        ghostHoPoolAccountId256[p][a][k] >= 0 && ghostHoPoolAccountId256[p][a][k] <= max_uint256;
    axiom forall uint64 p. forall uint128 a. forall uint8 k.
        (!VALID_POOL(p) || !VALID_ASSET_HO(a)) => ghostHoPoolAccountId256[p][a][k] == 0;
}

hook Sload Holdings.AccountId val _Holdings.accountId[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid][KEY uint8 kind] {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoPoolAccountId256[p][aid][kind] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.accountId[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid][KEY uint8 kind] Holdings.AccountId val {
    require(HO_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoPoolAccountId256[p][aid][kind] = val;
}

definition HO_POOL_PAIR(uint64 p, uint64 q) returns bool =
    (p == ghostPoolA64 && q == ghostPoolB64) || (p == ghostPoolB64 && q == ghostPoolA64);
