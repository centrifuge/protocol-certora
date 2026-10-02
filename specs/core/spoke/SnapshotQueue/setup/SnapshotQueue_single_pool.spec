// SnapshotQueue, single-pool lane. Setup: deltas and flush state of the pinned pair.

// Own setup: the pinned pair's mirrors; not in base, which multi_pool imports and hooks the same fields in.

import "SnapshotQueue_base.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/single_share_class.spec";

persistent ghost mathint ghostSqDelta128 {
    init_state axiom ghostSqDelta128 == 0;
    axiom ghostSqDelta128 >= 0 && ghostSqDelta128 <= max_uint128;
}

persistent ghost bool ghostSqIsPositive {
    init_state axiom !ghostSqIsPositive;
}

persistent ghost mathint ghostSqQueuedAssetCounter32 {
    init_state axiom ghostSqQueuedAssetCounter32 == 0;
    axiom ghostSqQueuedAssetCounter32 >= 0 && ghostSqQueuedAssetCounter32 <= max_uint32;
}

persistent ghost mathint ghostSqNonce64 {
    init_state axiom ghostSqNonce64 == 0;
    axiom ghostSqNonce64 >= 0 && ghostSqNonce64 <= max_uint64;
}

persistent ghost mapping(uint128 => mathint) ghostSqDeposits128 {
    init_state axiom forall uint128 a. ghostSqDeposits128[a] == 0;
    axiom forall uint128 a. ghostSqDeposits128[a] >= 0 && ghostSqDeposits128[a] <= max_uint128;
    axiom forall uint128 a. !VALID_ASSET_SQ(a) => ghostSqDeposits128[a] == 0;
}

persistent ghost mapping(uint128 => mathint) ghostSqWithdrawals128 {
    init_state axiom forall uint128 a. ghostSqWithdrawals128[a] == 0;
    axiom forall uint128 a. ghostSqWithdrawals128[a] >= 0 && ghostSqWithdrawals128[a] <= max_uint128;
    axiom forall uint128 a. !VALID_ASSET_SQ(a) => ghostSqWithdrawals128[a] == 0;
}

definition SQ_NONEMPTY_ASSET_ROW(uint128 a) returns mathint =
    (ghostSqDeposits128[a] != 0 || ghostSqWithdrawals128[a] != 0) ? 1 : 0;

definition SQ_QUEUED_ASSET_CARDINALITY() returns mathint =
    SQ_NONEMPTY_ASSET_ROW(ghostSqAssetE1) + SQ_NONEMPTY_ASSET_ROW(ghostSqAssetE2)
    + SQ_NONEMPTY_ASSET_ROW(ghostSqAssetE3);

hook Sload uint128 val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].delta {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqDelta128 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].delta uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSqDelta128 = val;
}

hook Sload bool val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].isPositive {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqIsPositive == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].isPositive bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSqIsPositive = val;
}

hook Sload uint32 val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].queuedAssetCounter {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqQueuedAssetCounter32 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].queuedAssetCounter uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSqQueuedAssetCounter32 = val;
}

hook Sload uint64 val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].nonce {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqNonce64 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].nonce uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSqNonce64 = val;
}

hook Sload uint128 val _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].deposits {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_SQ(a), "UNSAFE: at most three assets per queue");
    require(ghostSqDeposits128[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].deposits uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_SQ(a), "UNSAFE: at most three assets per queue");
    ghostSqDeposits128[a] = val;
}

hook Sload uint128 val _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].withdrawals {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_SQ(a), "UNSAFE: at most three assets per queue");
    require(ghostSqWithdrawals128[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].withdrawals uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_SQ(a), "UNSAFE: at most three assets per queue");
    ghostSqWithdrawals128[a] = val;
}

function assumeQueuedAssetCounterMatchesCardinality() {
    require(ghostSqQueuedAssetCounter32 == SQ_QUEUED_ASSET_CARDINALITY(),
        "PROVED: queuedAssetCounterMatchesOutstandingRows (SnapshotQueue)");
}

function SETUP_SQ(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupSnapshotQueue(e);
}
