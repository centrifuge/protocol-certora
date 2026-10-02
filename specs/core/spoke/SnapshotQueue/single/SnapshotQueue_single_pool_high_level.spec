// SnapshotQueue, single-pool lane. High level: laws of queue and flush sequences.

import "SnapshotQueue_single_pool_valid_state.spec";

// SQ-HL-01: a share update claims a snapshot exactly when no asset flows are still queued.
rule hlSqShareFlushReportsATruthfulSnapshot(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueValidState(e);

    mathint outstandingBefore = SQ_QUEUED_ASSET_CARDINALITY();

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    bool snapshotReported = data.isSnapshot;

    assert(snapshotReported <=> (outstandingBefore == 0),
        "a share flush is a snapshot exactly when no asset queue waits");
}

// SQ-HL-02: an asset update claims a snapshot exactly when nothing else is still queued.
rule hlSqAssetFlushReportsATruthfulSnapshot(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);

    mathint shareNetBefore = ghostSqDelta128;
    mathint outstandingBefore = SQ_QUEUED_ASSET_CARDINALITY();
    mathint flushedRowBefore = SQ_NONEMPTY_ASSET_ROW(assetId);

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    bool snapshotReported = data.isSnapshot;

    assert(snapshotReported <=> (shareNetBefore == 0 && outstandingBefore == flushedRowBefore),
        "the flush says snapshot exactly when no shares or other assets wait");
}

// SQ-HL-03: an asset update reports the net of queued deposits and withdrawals.
rule hlSqAssetPayloadCarriesTheNetMagnitude(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, uint128 depositAmount, uint128 withdrawAmount) {

    setupSnapshotQueueValidState(e);

    mathint depositsBefore = ghostSqDeposits128[assetId];
    mathint withdrawalsBefore = ghostSqWithdrawals128[assetId];
    mathint depositsTotal = depositsBefore + depositAmount;
    mathint withdrawalsTotal = withdrawalsBefore + withdrawAmount;
    mathint expectedNet = depositsTotal >= withdrawalsTotal
        ? depositsTotal - withdrawalsTotal : withdrawalsTotal - depositsTotal;

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, depositAmount, true);
    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, withdrawAmount, false);
    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint netReported = data.netAmount;

    assert(netReported == expectedNet, "an asset flush reports the absolute net of all queued flows");
}

// SQ-HL-04: an asset update is an increase exactly when queued deposits exceed withdrawals.
rule hlSqAssetPayloadPointsTowardTheLargerSide(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, uint128 depositAmount, uint128 withdrawAmount) {

    setupSnapshotQueueValidState(e);

    mathint depositsBefore = ghostSqDeposits128[assetId];
    mathint withdrawalsBefore = ghostSqWithdrawals128[assetId];
    mathint depositsTotal = depositsBefore + depositAmount;
    mathint withdrawalsTotal = withdrawalsBefore + withdrawAmount;

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, depositAmount, true);
    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, withdrawAmount, false);
    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    bool increaseReported = data.isIncrease;

    assert(increaseReported <=> (depositsTotal > withdrawalsTotal),
        "an asset flush is a decrease exactly when withdrawals reach deposits");
}

// SQ-HL-05: a share update reports the net of queued issuances and revocations.
rule hlSqSharePayloadCarriesTheNetMagnitude(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    uint128 issueAmount, uint128 revokeAmount) {

    setupSnapshotQueueValidState(e);

    mathint deltaBefore = ghostSqDelta128;
    bool signBefore = ghostSqIsPositive;
    mathint signedTotal = (signBefore ? deltaBefore : -deltaBefore) + issueAmount - revokeAmount;
    mathint expectedNet = signedTotal >= 0 ? signedTotal : -signedTotal;

    _SnapshotQueue.queueShares(e, poolId, scId, issueAmount, true);
    _SnapshotQueue.queueShares(e, poolId, scId, revokeAmount, false);
    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    mathint netReported = data.netAmount;

    assert(netReported == expectedNet, "a share flush reports the absolute net of all queued share changes");
}

// SQ-HL-06: a share update is an issuance exactly when queued issuances exceed revocations.
rule hlSqSharePayloadCarriesTheNetSign(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    uint128 issueAmount, uint128 revokeAmount) {

    setupSnapshotQueueValidState(e);

    mathint deltaBefore = ghostSqDelta128;
    bool signBefore = ghostSqIsPositive;
    mathint signedTotal = (signBefore ? deltaBefore : -deltaBefore) + issueAmount - revokeAmount;

    _SnapshotQueue.queueShares(e, poolId, scId, issueAmount, true);
    _SnapshotQueue.queueShares(e, poolId, scId, revokeAmount, false);
    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    bool increaseReported = data.isIncrease;

    assert(increaseReported <=> (signedTotal > 0),
        "a share flush is an issuance exactly when the queued net is positive");
}

// SQ-HL-07: flushing clears an asset's queue, so an immediate second update reports zero.
rule hlSqSecondAssetFlushReportsNothing(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);

    _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    ISpokeMessageSender.UpdateData second = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint secondNetReported = second.netAmount;

    assert(secondNetReported == 0, "a second asset flush reports a zero amount");
}

// SQ-HL-08: flushing clears the share queue, so an immediate second update reports zero.
rule hlSqSecondShareFlushReportsNothing(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueValidState(e);

    _SnapshotQueue.flushShares(e, poolId, scId);
    ISpokeMessageSender.UpdateData second = _SnapshotQueue.flushShares(e, poolId, scId);
    mathint secondNetReported = second.netAmount;

    assert(secondNetReported == 0, "a second share flush reports a zero amount");
}

// SQ-HL-09: back-to-back asset updates carry consecutive nonces.
rule hlSqConsecutiveAssetFlushesSpendConsecutiveOrdinals(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);

    ISpokeMessageSender.UpdateData first = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    ISpokeMessageSender.UpdateData second = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint firstNonce = first.nonce;
    mathint secondNonce = second.nonce;

    assert(secondNonce == firstNonce + 1, "consecutive asset flushes report consecutive nonces");
}

// SQ-HL-10: back-to-back share updates carry consecutive nonces.
rule hlSqConsecutiveShareFlushesSpendConsecutiveOrdinals(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueValidState(e);

    ISpokeMessageSender.UpdateData first = _SnapshotQueue.flushShares(e, poolId, scId);
    ISpokeMessageSender.UpdateData second = _SnapshotQueue.flushShares(e, poolId, scId);
    mathint firstNonce = first.nonce;
    mathint secondNonce = second.nonce;

    assert(secondNonce == firstNonce + 1, "consecutive share flushes report consecutive nonces");
}

// SQ-HL-11: queueing a zero asset amount leaves the snapshot status unchanged.
rule hlSqZeroAmountQueueingCannotStallTheSnapshot(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId, bool isIncrease) {

    setupSnapshotQueueValidState(e);

    mathint outstandingBefore = SQ_QUEUED_ASSET_CARDINALITY();

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, 0, isIncrease);
    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    bool snapshotReported = data.isSnapshot;

    assert(snapshotReported <=> (outstandingBefore == 0),
        "after a zero asset call, a share flush is a snapshot iff none waited");
}
