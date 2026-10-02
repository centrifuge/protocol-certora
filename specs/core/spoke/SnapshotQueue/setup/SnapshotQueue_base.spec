// SnapshotQueue. Setup: the queue link, asset ids and setup both lanes share.

import "../../../../shared/env.spec";

using SnapshotQueue as _SnapshotQueue;

definition EXCLUDED_FUNCTION_SQ(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

// UNSAFE: three asset ids reach empty, one and many, no wider set.
persistent ghost uint128 ghostSqAssetE1;

persistent ghost uint128 ghostSqAssetE2 {
    axiom ghostSqAssetE2 != ghostSqAssetE1;
}

persistent ghost uint128 ghostSqAssetE3 {
    axiom ghostSqAssetE3 != ghostSqAssetE1 && ghostSqAssetE3 != ghostSqAssetE2;
}

definition VALID_ASSET_SQ(uint128 a) returns bool =
    a == ghostSqAssetE1 || a == ghostSqAssetE2 || a == ghostSqAssetE3;

function setupSnapshotQueue(env e) {
    setupEnv(e);
    setupPoolMode();
    setupShareClassMode();
    require(e.msg.sender != _SnapshotQueue, "SAFE: the queue never calls itself");
}

definition FLUSH_FUNCTION_SQ(method f) returns bool =
    f.selector ==
        sig:_SnapshotQueue.flushAssets(SnapshotQueue.PoolId,SnapshotQueue.ShareClassId,SnapshotQueue.AssetId).selector
    || f.selector == sig:_SnapshotQueue.flushShares(SnapshotQueue.PoolId,SnapshotQueue.ShareClassId).selector;
