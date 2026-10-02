import "SnapshotQueue_single_pool_valid_state.spec";

// SQ-RV-01: queueing an asset flow fails for a non-admin caller.
rule rvSqQueueAssetsRefusesANonWard(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, uint128 amount, bool isIncrease) {

    setupSnapshotQueueValidState(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    bool callerIsWard = senderWardBefore == 1;

    _SnapshotQueue.queueAssets@withrevert(e, poolId, scId, assetId, amount, isIncrease);
    bool reverted = lastReverted;

    assert(!callerIsWard => reverted, "a non-ward's asset queueing call reverts");
}

// SQ-RV-02: queueing a share change fails for a non-admin caller.
rule rvSqQueueSharesRefusesANonWard(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    uint128 shares, bool isIssuance) {

    setupSnapshotQueueValidState(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    bool callerIsWard = senderWardBefore == 1;

    _SnapshotQueue.queueShares@withrevert(e, poolId, scId, shares, isIssuance);
    bool reverted = lastReverted;

    assert(!callerIsWard => reverted, "a non-ward's share queueing call reverts");
}

// SQ-RV-03: flushing an asset queue to the hub fails for a non-admin caller.
rule rvSqFlushAssetsRefusesANonWard(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    bool callerIsWard = senderWardBefore == 1;

    _SnapshotQueue.flushAssets@withrevert(e, poolId, scId, assetId);
    bool reverted = lastReverted;

    assert(!callerIsWard => reverted, "a non-ward cannot flush an asset's queue");
}

// SQ-RV-04: flushing the share queue to the hub fails for a non-admin caller.
rule rvSqFlushSharesRefusesANonWard(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueValidState(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    bool callerIsWard = senderWardBefore == 1;

    _SnapshotQueue.flushShares@withrevert(e, poolId, scId);
    bool reverted = lastReverted;

    assert(!callerIsWard => reverted, "a non-ward cannot flush the share queue");
}

// SQ-RV-05: granting queue admin rights fails for a non-admin caller.
rule rvSqRelyRefusesANonWard(env e, address user) {

    setupSnapshotQueueValidState(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    bool callerIsWard = senderWardBefore == 1;

    _SnapshotQueue.rely@withrevert(e, user);
    bool reverted = lastReverted;

    assert(!callerIsWard => reverted, "a non-ward's attempt to add a queue ward reverts");
}

// SQ-RV-06: revoking queue admin rights fails for a non-admin caller.
rule rvSqDenyRefusesANonWard(env e, address user) {

    setupSnapshotQueueValidState(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    bool callerIsWard = senderWardBefore == 1;

    _SnapshotQueue.deny@withrevert(e, user);
    bool reverted = lastReverted;

    assert(!callerIsWard => reverted, "a non-ward's attempt to remove a queue ward reverts");
}

// SQ-RV-07: an asset flush by an admin never fails while update nonces remain.
rule rvSqFlushAssetsAlwaysAdmitsAWardWhileOrdinalsRemain(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) {

    setupSnapshotQueueValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    bool callerIsWard = senderWardBefore == 1;
    bool nonceExhausted = ghostSqNonce64 == max_uint64;

    _SnapshotQueue.flushAssets@withrevert(e, poolId, scId, assetId);
    bool reverted = lastReverted;

    assert((callerIsWard && !nonceExhausted) => !reverted,
        "a ward can always flush any asset queue while nonces remain");
}

// SQ-RV-08: a share flush by an admin never fails while update nonces remain.
rule rvSqFlushSharesAlwaysAdmitsAWardWhileOrdinalsRemain(env e, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId) {

    setupSnapshotQueueValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    bool callerIsWard = senderWardBefore == 1;
    bool nonceExhausted = ghostSqNonce64 == max_uint64;

    _SnapshotQueue.flushShares@withrevert(e, poolId, scId);
    bool reverted = lastReverted;

    assert((callerIsWard && !nonceExhausted) => !reverted,
        "a ward can always flush the share queue while nonces remain");
}
