// SnapshotQueue, multi-pool lane. Setup: deltas keyed by pool and class.

// Own setup: mirrors keyed by two pools, one class each; single_pool hooks the same fields for one pinned pair.

import "SnapshotQueue_base.spec";
import "../../../../shared/domains/multi_pool.spec";
import "../../../../shared/domains/multi_share_class.spec";

// SCOPE: one class per pinned pool, a pool-keyed mirror is one row.
definition SQ_POOL_SLOT(uint64 p, bytes16 sc) returns bool =
    (p == ghostPoolA64 && sc == ghostShareClassA) || (p == ghostPoolB64 && sc == ghostShareClassB);

persistent ghost mapping(uint64 => mathint) ghostSqPoolDelta128 {
    init_state axiom forall uint64 p. ghostSqPoolDelta128[p] == 0;
    axiom forall uint64 p. ghostSqPoolDelta128[p] >= 0 && ghostSqPoolDelta128[p] <= max_uint128;
    axiom forall uint64 p. !VALID_POOL(p) => ghostSqPoolDelta128[p] == 0;
}

hook Sload uint128 val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].delta {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostSqPoolDelta128[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].delta uint128 val {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostSqPoolDelta128[p] = val;
}

persistent ghost mapping(uint64 => bool) ghostSqPoolIsPositive {
    init_state axiom forall uint64 p. !ghostSqPoolIsPositive[p];
    axiom forall uint64 p. !VALID_POOL(p) => !ghostSqPoolIsPositive[p];
}

hook Sload bool val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].isPositive {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostSqPoolIsPositive[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].isPositive bool val {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostSqPoolIsPositive[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostSqPoolQueuedAssetCounter32 {
    init_state axiom forall uint64 p. ghostSqPoolQueuedAssetCounter32[p] == 0;
    axiom forall uint64 p. ghostSqPoolQueuedAssetCounter32[p] >= 0 && ghostSqPoolQueuedAssetCounter32[p] <= max_uint32;
    axiom forall uint64 p. !VALID_POOL(p) => ghostSqPoolQueuedAssetCounter32[p] == 0;
}

hook Sload uint32 val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].queuedAssetCounter {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostSqPoolQueuedAssetCounter32[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].queuedAssetCounter uint32 val {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostSqPoolQueuedAssetCounter32[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostSqPoolNonce64 {
    init_state axiom forall uint64 p. ghostSqPoolNonce64[p] == 0;
    axiom forall uint64 p. ghostSqPoolNonce64[p] >= 0 && ghostSqPoolNonce64[p] <= max_uint64;
    axiom forall uint64 p. !VALID_POOL(p) => ghostSqPoolNonce64[p] == 0;
}

hook Sload uint64 val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].nonce {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostSqPoolNonce64[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].nonce uint64 val {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostSqPoolNonce64[p] = val;
}

persistent ghost mapping(uint64 => mapping(uint128 => mathint)) ghostSqPoolDeposits128 {
    init_state axiom forall uint64 p. forall uint128 a. ghostSqPoolDeposits128[p][a] == 0;
    axiom forall uint64 p. forall uint128 a.
        ghostSqPoolDeposits128[p][a] >= 0 && ghostSqPoolDeposits128[p][a] <= max_uint128;
    axiom forall uint64 p. forall uint128 a.
        (!VALID_POOL(p) || !VALID_ASSET_SQ(a)) => ghostSqPoolDeposits128[p][a] == 0;
}

hook Sload uint128 val _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].deposits {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_SQ(a), "UNSAFE: at most three assets per queue");
    require(ghostSqPoolDeposits128[p][a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].deposits uint128 val {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_SQ(a), "UNSAFE: at most three assets per queue");
    ghostSqPoolDeposits128[p][a] = val;
}

persistent ghost mapping(uint64 => mapping(uint128 => mathint)) ghostSqPoolWithdrawals128 {
    init_state axiom forall uint64 p. forall uint128 a. ghostSqPoolWithdrawals128[p][a] == 0;
    axiom forall uint64 p. forall uint128 a.
        ghostSqPoolWithdrawals128[p][a] >= 0 && ghostSqPoolWithdrawals128[p][a] <= max_uint128;
    axiom forall uint64 p. forall uint128 a.
        (!VALID_POOL(p) || !VALID_ASSET_SQ(a)) => ghostSqPoolWithdrawals128[p][a] == 0;
}

hook Sload uint128 val _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].withdrawals {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_SQ(a), "UNSAFE: at most three assets per queue");
    require(ghostSqPoolWithdrawals128[p][a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].withdrawals uint128 val {
    require(SQ_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(VALID_ASSET_SQ(a), "UNSAFE: at most three assets per queue");
    ghostSqPoolWithdrawals128[p][a] = val;
}

definition SQ_POOL_PAIR(uint64 p, uint64 q) returns bool =
    (p == ghostPoolA64 && q == ghostPoolB64) || (p == ghostPoolB64 && q == ghostPoolA64);
