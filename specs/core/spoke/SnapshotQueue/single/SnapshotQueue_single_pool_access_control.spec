import "../setup/SnapshotQueue_single_pool.spec";

// SQ-AC-01: only an admin can change the net share amount queued for the hub.
rule acSqOnlyAWardMovesTheShareNet(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueue(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    mathint deltaBefore = ghostSqDelta128;
    bool signBefore = ghostSqIsPositive;

    f(e, args);

    mathint deltaAfter = ghostSqDelta128;
    bool signAfter = ghostSqIsPositive;

    assert(deltaAfter != deltaBefore || signAfter != signBefore => senderWardBefore == 1,
        "only a ward can change the queued share net");
}

// SQ-AC-02: only an admin can change an asset's queued deposits and withdrawals.
rule acSqOnlyAWardMovesAnAssetRow(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueue(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    mathint depositsBefore = ghostSqDeposits128[a];
    mathint withdrawalsBefore = ghostSqWithdrawals128[a];

    f(e, args);

    mathint depositsAfter = ghostSqDeposits128[a];
    mathint withdrawalsAfter = ghostSqWithdrawals128[a];

    assert(depositsAfter != depositsBefore || withdrawalsAfter != withdrawalsBefore
        => senderWardBefore == 1,
        "only a ward can change an asset's queued flows");
}

// SQ-AC-03: only an admin can change the count of assets with queued flows.
rule acSqOnlyAWardMovesTheOutstandingAssetCount(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueue(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    mathint counterBefore = ghostSqQueuedAssetCounter32;

    f(e, args);

    mathint counterAfter = ghostSqQueuedAssetCounter32;

    assert(counterAfter != counterBefore => senderWardBefore == 1,
        "a non-ward never changes how many assets wait in the queue");
}

// SQ-AC-04: only an admin can advance the nonce that orders queued updates for the hub.
rule acSqOnlyAWardSpendsAFlushOrdinal(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueue(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    mathint nonceBefore = ghostSqNonce64;

    f(e, args);

    mathint nonceAfter = ghostSqNonce64;

    assert(nonceAfter != nonceBefore => senderWardBefore == 1, "only a ward can spend a flush nonce");
}

// SQ-AC-05: only an admin can grant or revoke admin rights on the queue.
rule acSqOnlyAWardMovesTheWardBit(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueue(e);

    mathint senderWardBefore = _SnapshotQueue.wards[e.msg.sender];
    mathint userWardBefore = _SnapshotQueue.wards[user];

    f(e, args);

    mathint userWardAfter = _SnapshotQueue.wards[user];

    assert(userWardAfter != userWardBefore => senderWardBefore == 1,
        "a non-ward cannot change anyone's ward status on the queue");
}
