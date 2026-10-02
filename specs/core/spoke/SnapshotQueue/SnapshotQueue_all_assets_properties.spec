import "setup/SnapshotQueue_all_assets.spec";

// --- valid_state ---

function setupSnapshotQueueAllAssetsValidState(env e) {
    setupSnapshotQueue(e);
    requireInvariant queuedAssetCounterCountsEveryNonEmptyRow(e);
}

// SQ-VS-03: a share class's pending-asset count is its number of assets with queued flows, however many exist.
invariant queuedAssetCounterCountsEveryNonEmptyRow(env e)
    ghostSqQueuedAssetCounter32 == ghostSqNonEmptyRows
filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } { preserved with (env eFunc) { SETUP_SQ(e, eFunc); } }

// --- high_level ---

// SQ-HL-12: a share flush claims a snapshot exactly when it leaves the share class with nothing queued.
rule hlSqShareFlushSnapshotMeansTheClassIsDrained(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueAllAssetsValidState(e);

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    bool snapshotReported = data.isSnapshot;

    uint128 deltaAfter; bool signAfter; uint32 counterAfter; uint64 nonceAfter;
    deltaAfter, signAfter, counterAfter, nonceAfter = _SnapshotQueue.queuedShares(e, poolId, scId);

    assert(snapshotReported <=> (deltaAfter == 0 && ghostSqNonEmptyRows == 0),
        "the snapshot mark is set exactly when the class is left drained");
}

// SQ-HL-13: an asset flush claims a snapshot exactly when it leaves the share class with nothing queued.
rule hlSqAssetFlushSnapshotMeansTheClassIsDrained(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueAllAssetsValidState(e);

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    bool snapshotReported = data.isSnapshot;

    uint128 deltaAfter; bool signAfter; uint32 counterAfter; uint64 nonceAfter;
    deltaAfter, signAfter, counterAfter, nonceAfter = _SnapshotQueue.queuedShares(e, poolId, scId);

    assert(snapshotReported <=> (deltaAfter == 0 && ghostSqNonEmptyRows == 0),
        "the snapshot mark is set exactly when the class is left drained");
}
