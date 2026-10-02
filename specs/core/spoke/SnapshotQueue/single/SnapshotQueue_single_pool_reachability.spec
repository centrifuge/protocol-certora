import "SnapshotQueue_single_pool_valid_state.spec";

// SQ-RC-01: a deposit can open a new asset queue for the share class.
rule rcSqQueueAssetsCanOpenADepositRow(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, uint128 amount) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset is queued yet");

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, amount, true);

    mathint depositsAfter = ghostSqDeposits128[assetId];
    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(depositsAfter > 0 && counterAfter == 1, "queueing a deposit can open the class's first asset queue");
}

// SQ-RC-02: a withdrawal can open a new asset queue for the share class.
rule rcSqQueueAssetsCanOpenAWithdrawalRow(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, uint128 amount) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset is queued yet");

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, amount, false);

    mathint withdrawalsAfter = ghostSqWithdrawals128[assetId];
    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(withdrawalsAfter > 0 && counterAfter == 1, "queueing a withdrawal can open the class's first asset queue");
}

// SQ-RC-03: a second deposit can add to an asset queue without counting the asset twice.
rule rcSqQueueAssetsCanAccumulateASecondDeposit(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, uint128 amount) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDeposits128[assetId] > 0 && SQ_QUEUED_ASSET_CARDINALITY() == 1,
        "SCOPE: the asset alone is queued, with a deposit");

    mathint depositsBefore = ghostSqDeposits128[assetId];

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, amount, true);

    mathint depositsAfter = ghostSqDeposits128[assetId];
    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(depositsAfter > depositsBefore && counterAfter == 1,
        "a further deposit can grow a queued asset, still counted once");
}

// SQ-RC-04: one asset queue can hold a deposit and a withdrawal at the same time.
rule rcSqQueueAssetsCanHoldBothSidesOfOneRow(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, uint128 amount) {

    setupSnapshotQueueValidState(e);

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, amount, false);

    mathint depositsAfter = ghostSqDeposits128[assetId];
    mathint withdrawalsAfter = ghostSqWithdrawals128[assetId];
    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(depositsAfter > 0 && withdrawalsAfter > 0 && counterAfter == 1,
        "an asset can queue a deposit and a withdrawal, counted once");
}

// SQ-RC-05: three assets of one share class can have queued flows at the same time.
rule rcSqQueueAssetsCanLeaveThreeAssetsOutstandingAtOnce(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, uint128 amount) {

    setupSnapshotQueueValidState(e);
    require(assetId == ghostSqAssetE3, "SCOPE: the queued asset is the third modelled one");
    require(SQ_QUEUED_ASSET_CARDINALITY() == 2 && SQ_NONEMPTY_ASSET_ROW(ghostSqAssetE3) == 0,
        "SCOPE: the other two assets are queued, this one is not");

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, amount, true);

    mathint depositsAfter = ghostSqDeposits128[assetId];
    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(depositsAfter > 0 && counterAfter == 3, "one share class's queue can count three waiting assets");
}

// SQ-RC-06: a single deposit of the maximum amount can be queued for an asset.
rule rcSqQueueAssetsCanAbsorbTheFullAccumulatorWidth(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId, uint128 amount) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset is queued yet");

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, amount, true);

    mathint depositsAfter = ghostSqDeposits128[assetId];
    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(depositsAfter == max_uint128 && counterAfter == 1,
        "one deposit can fill an empty asset queue to its maximum");
}

// SQ-RC-07: a single unit of an asset can open a queue for the share class.
rule rcSqQueueAssetsCanMakeAClassOutstandingWithOneUnit(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset is queued yet");

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, 1, true);

    mathint depositsAfter = ghostSqDeposits128[assetId];
    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(depositsAfter == 1 && counterAfter == 1, "a one-unit deposit can open the class's first asset queue");
}

// SQ-RC-08: after a zero-amount asset call, the share class can still report a snapshot.
rule rcSqZeroAmountQueueLeavesTheSnapshotAvailable(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId, bool isIncrease) {

    setupSnapshotQueueValidState(e);

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, 0, isIncrease);

    mathint counterAfterQueue = ghostSqQueuedAssetCounter32;

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    bool snapshotReported = data.isSnapshot;

    satisfy(counterAfterQueue == 0 && snapshotReported,
        "a zero asset call leaves no asset waiting and a snapshot possible");
}

// SQ-RC-09: an issuance can open a net issuance on an empty share queue.
rule rcSqQueueSharesCanOpenAnIssuanceNet(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    uint128 shares) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 == 0, "SCOPE: no share change is queued yet");

    _SnapshotQueue.queueShares(e, poolId, scId, shares, true);

    mathint deltaAfter = ghostSqDelta128;
    bool signAfter = ghostSqIsPositive;

    satisfy(deltaAfter > 0 && signAfter, "issuing shares on a clean queue can leave a positive share net");
}

// SQ-RC-10: a revocation can open a net revocation on an empty share queue.
rule rcSqQueueSharesCanOpenARevocationNet(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    uint128 shares) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 == 0, "SCOPE: no share change is queued yet");

    _SnapshotQueue.queueShares(e, poolId, scId, shares, false);

    mathint deltaAfter = ghostSqDelta128;
    bool signAfter = ghostSqIsPositive;

    satisfy(deltaAfter > 0 && !signAfter, "revoking shares on a clean queue can leave a negative share net");
}

// SQ-RC-11: a further issuance can grow a queued net issuance.
rule rcSqQueueSharesCanGrowAnIssuanceNet(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    uint128 shares) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 > 0 && ghostSqIsPositive, "SCOPE: a net issuance is already queued");

    mathint deltaBefore = ghostSqDelta128;

    _SnapshotQueue.queueShares(e, poolId, scId, shares, true);

    mathint deltaAfter = ghostSqDelta128;
    bool signAfter = ghostSqIsPositive;

    satisfy(deltaAfter > deltaBefore && signAfter, "more issuance can enlarge a positive share net");
}

// SQ-RC-12: a smaller revocation can reduce a queued net issuance without reversing it.
rule rcSqQueueSharesCanShrinkAnIssuanceNet(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    uint128 shares) {

    setupSnapshotQueueValidState(e);

    mathint deltaBefore = ghostSqDelta128;

    _SnapshotQueue.queueShares(e, poolId, scId, shares, false);

    mathint deltaAfter = ghostSqDelta128;
    bool signAfter = ghostSqIsPositive;

    satisfy(deltaAfter > 0 && deltaAfter < deltaBefore && signAfter,
        "a revocation can shrink a net issuance, leaving it an issuance");
}

// SQ-RC-13: an equal revocation can cancel a queued net issuance back to zero.
rule rcSqQueueSharesCanCancelAnIssuanceNetExactly(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, uint128 shares) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 > 0 && ghostSqIsPositive, "SCOPE: a net issuance is already queued");

    _SnapshotQueue.queueShares(e, poolId, scId, shares, false);

    mathint deltaAfter = ghostSqDelta128;
    bool signAfter = ghostSqIsPositive;

    satisfy(deltaAfter == 0 && !signAfter, "revoking exactly the queued issuance can reset the share net to zero");
}

// SQ-RC-14: a single share issuance of the maximum amount can be queued.
rule rcSqQueueSharesCanAbsorbTheFullNetWidth(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    uint128 shares) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 == 0, "SCOPE: no share change is queued yet");

    _SnapshotQueue.queueShares(e, poolId, scId, shares, true);

    mathint deltaAfter = ghostSqDelta128;
    bool signAfter = ghostSqIsPositive;

    satisfy(deltaAfter == max_uint128 && signAfter, "one issuance can fill an empty share queue to its maximum");
}

// SQ-RC-15: after a zero-share call, a queued issuance can still be reported unchanged.
rule rcSqZeroShareQueueLeavesTheNetPayloadIntact(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, bool isIssuance) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 > 0 && ghostSqIsPositive, "SCOPE: a net issuance is already queued");

    mathint deltaBefore = ghostSqDelta128;

    _SnapshotQueue.queueShares(e, poolId, scId, 0, isIssuance);

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    mathint netReported = data.netAmount;
    bool increaseReported = data.isIncrease;

    satisfy(netReported == deltaBefore && netReported > 0 && increaseReported,
        "the flush after an empty share call can report the old issuance as is");
}

// SQ-RC-16: a larger revocation can turn a queued net issuance into a net revocation.
rule rcSqALargerRevocationCanFlipTheQueuedNet(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, uint128 issueAmount, uint128 revokeAmount) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 == 0, "SCOPE: no share change is queued yet");

    _SnapshotQueue.queueShares(e, poolId, scId, issueAmount, true);

    mathint deltaAfterIssue = ghostSqDelta128;
    bool signAfterIssue = ghostSqIsPositive;

    _SnapshotQueue.queueShares(e, poolId, scId, revokeAmount, false);

    mathint deltaAfterRevoke = ghostSqDelta128;
    bool signAfterRevoke = ghostSqIsPositive;

    satisfy(deltaAfterIssue > 0 && signAfterIssue && deltaAfterRevoke > 0 && !signAfterRevoke,
        "revoking more than was issued can make the share net negative");
}

// SQ-RC-17: flushing the last queued asset can report its amount as a snapshot.
rule rcSqAssetFlushCanHandOverAndReportASnapshot(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);

    mathint nonceBefore = ghostSqNonce64;

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint netReported = data.netAmount;
    bool snapshotReported = data.isSnapshot;

    mathint depositsAfter = ghostSqDeposits128[assetId];
    mathint withdrawalsAfter = ghostSqWithdrawals128[assetId];
    mathint counterAfter = ghostSqQueuedAssetCounter32;
    mathint nonceAfter = ghostSqNonce64;

    satisfy(netReported > 0 && snapshotReported && depositsAfter == 0 && withdrawalsAfter == 0
        && counterAfter == 0 && nonceAfter == nonceBefore + 1,
        "the last queued asset can flush as a snapshot, spending one nonce");
}

// SQ-RC-18: an asset update can report an amount but no snapshot if another asset is queued.
rule rcSqAssetFlushWithASiblingRowOutstandingCanReportNoSnapshot(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint netReported = data.netAmount;
    bool snapshotReported = data.isSnapshot;

    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(netReported > 0 && !snapshotReported && counterAfter == 1,
        "an asset flush can carry a real amount and not be a snapshot");
}

// SQ-RC-19: an asset update can report no snapshot while a share change is still queued.
rule rcSqAssetFlushWithSharesOutstandingCanReportNoSnapshot(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint netReported = data.netAmount;
    bool snapshotReported = data.isSnapshot;

    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(netReported > 0 && !snapshotReported && counterAfter == 0,
        "an asset flush can empty the last queue and not be a snapshot");
}

// SQ-RC-20: an asset queued both ways can be reported to the hub as a net deposit.
rule rcSqAssetFlushCanNetTowardTheDepositSide(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId, uint128 depositAmount, uint128 withdrawAmount) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset is queued yet");

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, depositAmount, true);
    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, withdrawAmount, false);

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint netReported = data.netAmount;
    bool increaseReported = data.isIncrease;

    satisfy(netReported > 0 && increaseReported && withdrawAmount > 0,
        "deposits can outweigh withdrawals of one asset in a flush");
}

// SQ-RC-21: an asset queued both ways can be reported to the hub as a net withdrawal.
rule rcSqAssetFlushCanNetTowardTheWithdrawalSide(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId, uint128 depositAmount, uint128 withdrawAmount) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset is queued yet");

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, depositAmount, true);
    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, withdrawAmount, false);

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint netReported = data.netAmount;
    bool increaseReported = data.isIncrease;

    satisfy(netReported > 0 && !increaseReported && depositAmount > 0,
        "withdrawals can outweigh deposits of one asset in a flush");
}

// SQ-RC-22: a flush of an empty asset queue can still use up an update nonce.
rule rcSqEmptyAssetFlushStillSpendsAnOrdinal(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset is queued, so the flush carries nothing");

    mathint nonceBefore = ghostSqNonce64;
    mathint counterBefore = ghostSqQueuedAssetCounter32;

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint netReported = data.netAmount;
    mathint nonceReported = data.nonce;

    mathint nonceAfter = ghostSqNonce64;
    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(netReported == 0 && nonceReported == nonceBefore && nonceAfter == nonceBefore + 1
        && counterAfter == counterBefore,
        "an empty asset flush reports nothing yet spends one nonce");
}

// SQ-RC-23: an asset whose flows cancel out can be flushed as a zero snapshot update.
rule rcSqOffsettingRowCanFlushZeroYetClearTheCount(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDeposits128[assetId] == ghostSqWithdrawals128[assetId]
        && ghostSqDeposits128[assetId] > 0,
        "SCOPE: equal, nonzero deposits and withdrawals queued");

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint netReported = data.netAmount;
    bool increaseReported = data.isIncrease;
    bool snapshotReported = data.isSnapshot;

    mathint counterAfter = ghostSqQueuedAssetCounter32;

    satisfy(netReported == 0 && !increaseReported && snapshotReported && counterAfter == 0,
        "an offset asset can flush as a zero snapshot, leaving none queued");
}

// SQ-RC-24: with no asset change queued, a share issuance can reach the hub as a snapshot.
rule rcSqShareFlushCanHandOverAnIssuanceAndReportASnapshot(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 > 0 && ghostSqIsPositive, "SCOPE: a net issuance is already queued");

    mathint nonceBefore = ghostSqNonce64;

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    mathint netReported = data.netAmount;
    bool increaseReported = data.isIncrease;
    bool snapshotReported = data.isSnapshot;

    mathint deltaAfter = ghostSqDelta128;
    bool signAfter = ghostSqIsPositive;
    mathint nonceAfter = ghostSqNonce64;

    satisfy(netReported > 0 && increaseReported && snapshotReported && deltaAfter == 0 && !signAfter
        && nonceAfter == nonceBefore + 1,
        "a net issuance can flush as a snapshot, emptying the share queue");
}

// SQ-RC-25: with no asset change queued, a share revocation can reach the hub as a snapshot.
rule rcSqShareFlushCanHandOverARevocationAndReportASnapshot(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset queued, so the share flush is a snapshot");

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    mathint netReported = data.netAmount;
    bool increaseReported = data.isIncrease;
    bool snapshotReported = data.isSnapshot;

    mathint deltaAfter = ghostSqDelta128;

    satisfy(netReported > 0 && !increaseReported && snapshotReported && deltaAfter == 0,
        "a net revocation can flush as a snapshot, emptying the share queue");
}

// SQ-RC-26: a share update can report no snapshot while an asset change is still queued.
rule rcSqShareFlushWithAnAssetRowOutstandingCanReportNoSnapshot(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 1, "SCOPE: exactly one asset is queued");

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    mathint netReported = data.netAmount;
    bool snapshotReported = data.isSnapshot;

    mathint deltaAfter = ghostSqDelta128;

    satisfy(netReported > 0 && !snapshotReported && deltaAfter == 0,
        "a share flush can carry a real net and not be a snapshot");
}

// SQ-RC-27: with nothing queued, a share flush can still use a nonce and report a snapshot.
rule rcSqEmptyShareFlushStillSpendsAnOrdinal(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 == 0 && SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: nothing is queued for the share class");

    mathint nonceBefore = ghostSqNonce64;

    ISpokeMessageSender.UpdateData data = _SnapshotQueue.flushShares(e, poolId, scId);
    mathint netReported = data.netAmount;
    bool snapshotReported = data.isSnapshot;
    mathint nonceReported = data.nonce;

    mathint nonceAfter = ghostSqNonce64;

    satisfy(netReported == 0 && snapshotReported && nonceReported == nonceBefore
        && nonceAfter == nonceBefore + 1,
        "an empty share flush can be a snapshot and spend one nonce");
}

// SQ-RC-28: a share class with queued shares and assets can be flushed back into sync.
rule rcSqAnOutOfSyncClassCanBeBroughtBackIntoSync(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId, uint128 shares, uint128 amount) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 == 0 && SQ_QUEUED_ASSET_CARDINALITY() == 0,
        "SCOPE: nothing is queued for the share class yet");

    _SnapshotQueue.queueShares(e, poolId, scId, shares, true);
    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, amount, true);

    ISpokeMessageSender.UpdateData assetData = _SnapshotQueue.flushAssets(e, poolId, scId, assetId);
    mathint assetNetReported = assetData.netAmount;
    bool assetSnapshotReported = assetData.isSnapshot;

    ISpokeMessageSender.UpdateData shareData = _SnapshotQueue.flushShares(e, poolId, scId);
    mathint shareNetReported = shareData.netAmount;
    bool shareSnapshotReported = shareData.isSnapshot;

    mathint deltaAfter = ghostSqDelta128;
    mathint outstandingAfter = SQ_QUEUED_ASSET_CARDINALITY();

    satisfy(assetNetReported > 0 && !assetSnapshotReported && shareNetReported > 0 && shareSnapshotReported
        && deltaAfter == 0 && outstandingAfter == 0,
        "shares and an asset can flush in full, only the last as a snapshot");
}

// SQ-RC-29: an asset queue can be flushed and reused with nothing left over.
rule rcSqAnAssetRowCanBeReusedAfterAFlush(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, uint128 firstAmount, uint128 secondAmount) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset is queued yet");

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, firstAmount, true);

    mathint counterAfterFirstQueue = ghostSqQueuedAssetCounter32;

    _SnapshotQueue.flushAssets(e, poolId, scId, assetId);

    mathint counterAfterFlush = ghostSqQueuedAssetCounter32;
    mathint depositsAfterFlush = ghostSqDeposits128[assetId];

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, secondAmount, true);

    mathint counterAfterSecondQueue = ghostSqQueuedAssetCounter32;
    mathint depositsAfterSecondQueue = ghostSqDeposits128[assetId];

    satisfy(counterAfterFirstQueue == 1 && counterAfterFlush == 0 && depositsAfterFlush == 0
        && counterAfterSecondQueue == 1 && depositsAfterSecondQueue > 0,
        "an asset queue can be filled, flushed clean and filled again");
}

// SQ-RC-30: an admin can revoke another account's admin rights on the queue.
rule rcSqDenyCanRemoveAnotherAccountsQueueSeat(env e, address user) {

    setupSnapshotQueueValidState(e);
    require(user != e.msg.sender, "SCOPE: another account, SQ-RC-32 covers the caller itself");

    mathint userWardBefore = _SnapshotQueue.wards[user];

    _SnapshotQueue.deny(e, user);

    mathint userWardAfter = _SnapshotQueue.wards[user];

    satisfy(userWardBefore == 1 && userWardAfter == 0, "one queue ward can unseat another");
}

// SQ-RC-31: a newly added admin can queue share changes right away.
rule rcSqAFreshlyReliedAccountCanMoveTheQueue(env e, env eUser, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, address user, uint128 shares) {

    setupSnapshotQueueValidState(e);
    setupSnapshotQueueValidState(eUser);
    require(eUser.msg.sender == user, "SCOPE: the newly granted ward makes the call");
    require(ghostSqDelta128 == 0, "SCOPE: no share change is queued yet");

    mathint userWardBefore = _SnapshotQueue.wards[user];

    _SnapshotQueue.rely(e, user);
    _SnapshotQueue.queueShares(eUser, poolId, scId, shares, true);

    mathint deltaAfter = ghostSqDelta128;
    bool signAfter = ghostSqIsPositive;

    satisfy(userWardBefore == 0 && deltaAfter > 0 && signAfter,
        "a newly granted ward can queue an issuance in the next call");
}

// SQ-RC-32: an admin can revoke its own admin rights on the queue.
rule rcSqAWardCanDenyItself(env e, address user) {

    setupSnapshotQueueValidState(e);
    require(user == e.msg.sender, "SCOPE: the ward revokes itself");

    mathint callerWardBefore = _SnapshotQueue.wards[e.msg.sender];

    _SnapshotQueue.deny(e, user);

    mathint callerWardAfter = _SnapshotQueue.wards[e.msg.sender];

    satisfy(callerWardBefore == 1 && callerWardAfter == 0, "a ward can revoke its own ward rights");
}

// SQ-RC-33: the share queue view can show an issuance just queued.
rule rcSqQueuedSharesViewCanReadBackAFreshNet(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, uint128 shares) {

    setupSnapshotQueueValidState(e);
    require(ghostSqDelta128 == 0, "SCOPE: no share change is queued yet");

    _SnapshotQueue.queueShares(e, poolId, scId, shares, true);

    uint128 delta;
    bool isPositive;
    uint32 queuedAssetCounter;
    uint64 nonce;
    delta, isPositive, queuedAssetCounter, nonce = _SnapshotQueue.queuedShares(e, poolId, scId);
    mathint reportedDelta = delta;

    satisfy(reportedDelta == shares && reportedDelta > 0 && isPositive,
        "the share queue view can read back a just-queued issuance");
}

// SQ-RC-34: the asset queue view can show a deposit just queued.
rule rcSqQueuedAssetsViewCanReadBackAFreshFlow(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId, uint128 amount) {

    setupSnapshotQueueValidState(e);
    require(SQ_QUEUED_ASSET_CARDINALITY() == 0, "SCOPE: no asset is queued yet");

    _SnapshotQueue.queueAssets(e, poolId, scId, assetId, amount, true);

    uint128 deposits;
    uint128 withdrawals;
    deposits, withdrawals = _SnapshotQueue.queuedAssets(e, poolId, scId, assetId);
    mathint reportedDeposits = deposits;
    mathint reportedWithdrawals = withdrawals;

    satisfy(reportedDeposits == amount && reportedDeposits > 0 && reportedWithdrawals == 0,
        "the asset queue view can read back a just-queued deposit");
}
