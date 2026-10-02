import "../setup/SnapshotQueue_single_pool.spec";

function setupSnapshotQueueValidState(env e) {
    setupSnapshotQueue(e);
    requireInvariant zeroDeltaIsNonPositive(e);
    requireInvariant queuedAssetCounterMatchesOutstandingRows(e);
}

// SQ-VS-01: a fully netted share queue is never flagged as an issuance.
invariant zeroDeltaIsNonPositive(env e)
    ghostSqDelta128 == 0 => !ghostSqIsPositive
filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } { preserved with (env eFunc) { SETUP_SQ(e, eFunc); } }

// SQ-VS-02: the pending-asset count always equals the number of assets with queued flows.
invariant queuedAssetCounterMatchesOutstandingRows(env e)
    ghostSqQueuedAssetCounter32 == SQ_QUEUED_ASSET_CARDINALITY()
filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } { preserved with (env eFunc) { SETUP_SQ(e, eFunc); } }
