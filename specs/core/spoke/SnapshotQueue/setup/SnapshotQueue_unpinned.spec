// SnapshotQueue, unpinned lane. Setup: any pool, class and asset, read through getters.

// Own setup: no hooks or pins, rows read through getters; every other lane's hooks pin the pool and class.

import "../../../../shared/env.spec";

using SnapshotQueue as _SnapshotQueue;

methods {
    function _SnapshotQueue.queuedAssets(SnapshotQueue.PoolId, SnapshotQueue.ShareClassId, SnapshotQueue.AssetId)
        external returns (uint128, uint128) envfree;
    function _SnapshotQueue.queuedShares(SnapshotQueue.PoolId, SnapshotQueue.ShareClassId)
        external returns (uint128, bool, uint32, uint64) envfree;
}

definition EXCLUDED_FUNCTION_SQ(method f) returns bool =
    f.isView || f.isPure || f.isFallback;

function setupSnapshotQueueUnpinned(env e) {
    setupEnv(e);
}
