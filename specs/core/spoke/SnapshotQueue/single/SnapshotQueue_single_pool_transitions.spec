import "SnapshotQueue_single_pool_valid_state.spec";

// --- variable_transitions ---

// SQ-VT-01: a call changes the queued amounts of at most one asset.
rule vtSqAssetRowsMoveOneAtATime(env e, method f, calldataarg args, uint128 a, uint128 b)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueue(e);
    require(a != b, "SCOPE: two distinct assets");

    mathint depositsABefore = ghostSqDeposits128[a];
    mathint withdrawalsABefore = ghostSqWithdrawals128[a];
    mathint depositsBBefore = ghostSqDeposits128[b];
    mathint withdrawalsBBefore = ghostSqWithdrawals128[b];

    f(e, args);

    mathint depositsAAfter = ghostSqDeposits128[a];
    mathint withdrawalsAAfter = ghostSqWithdrawals128[a];
    mathint depositsBAfter = ghostSqDeposits128[b];
    mathint withdrawalsBAfter = ghostSqWithdrawals128[b];

    assert(depositsAAfter != depositsABefore || withdrawalsAAfter != withdrawalsABefore
        => depositsBAfter == depositsBBefore && withdrawalsBAfter == withdrawalsBBefore,
        "when one asset's queue moves, every other asset's stays put");
}

// SQ-VT-02: only flushing shares or assets advances the update nonce.
rule vtSqOnlyAFlushSpendsAnOrdinal(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueueValidState(e);

    mathint nonceBefore = ghostSqNonce64;

    f(e, args);

    mathint nonceAfter = ghostSqNonce64;

    assert(nonceAfter != nonceBefore => FLUSH_FUNCTION_SQ(f), "only a flush spends a flush nonce");
}

// --- state_transitions ---

// SQ-ST-01: a flushed asset queue is emptied, no longer counted as pending, and uses one nonce.
rule stSqAssetFlushEmptiesTheRowAndSpendsOneOrdinal(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueueValidState(e);

    mathint depositsBefore = ghostSqDeposits128[a];
    mathint withdrawalsBefore = ghostSqWithdrawals128[a];
    mathint counterBefore = ghostSqQueuedAssetCounter32;
    mathint nonceBefore = ghostSqNonce64;

    f(e, args);

    bool drained = ghostSqDeposits128[a] < depositsBefore || ghostSqWithdrawals128[a] < withdrawalsBefore;

    assert(drained => ghostSqDeposits128[a] == 0 && ghostSqWithdrawals128[a] == 0,
        "an asset queue that shrinks is emptied on both sides");
    assert(drained => ghostSqQueuedAssetCounter32 == counterBefore - 1,
        "an asset queue that shrinks drops the waiting count by one");
    assert(drained => ghostSqNonce64 == nonceBefore + 1, "an asset queue that shrinks spends exactly one nonce");
}

// SQ-ST-02: a share flush empties the share queue, never leaving part of it behind.
rule stSqShareFlushHandsOverTheWholeNet(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueueValidState(e);

    mathint deltaBefore = ghostSqDelta128;
    bool signBefore = ghostSqIsPositive;
    mathint nonceBefore = ghostSqNonce64;

    f(e, args);

    assert(ghostSqNonce64 != nonceBefore
        && (ghostSqDelta128 != deltaBefore || ghostSqIsPositive != signBefore)
        => ghostSqDelta128 == 0 && !ghostSqIsPositive,
        "a nonce-spending call that moves the share net drains it fully");
}

// SQ-ST-03: opening an asset queue uses no nonce and keeps the queued share amount.
rule stSqOpeningAnAssetRowSpendsNoOrdinalAndMovesNoShareNet(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueueValidState(e);

    mathint deltaBefore = ghostSqDelta128;
    mathint counterBefore = ghostSqQueuedAssetCounter32;
    mathint nonceBefore = ghostSqNonce64;

    f(e, args);

    assert(ghostSqQueuedAssetCounter32 > counterBefore
        => ghostSqNonce64 == nonceBefore && ghostSqDelta128 == deltaBefore,
        "a newly waiting asset leaves the nonce and share net as they were");
}

// SQ-ST-04: queueing an asset flow updates its deposit or withdrawal side, never both.
rule stSqAssetFlowTakesOneSideOnly(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueueValidState(e);

    mathint depositsBefore = ghostSqDeposits128[a];
    mathint withdrawalsBefore = ghostSqWithdrawals128[a];

    f(e, args);

    assert(ghostSqDeposits128[a] > depositsBefore => ghostSqWithdrawals128[a] == withdrawalsBefore,
        "raising an asset's queued deposits leaves its withdrawals alone");
    assert(ghostSqWithdrawals128[a] > withdrawalsBefore => ghostSqDeposits128[a] == depositsBefore,
        "raising an asset's queued withdrawals leaves its deposits alone");
}

// SQ-ST-05: the update nonce advances by at most one per call, so no number is skipped.
rule stSqNonceAdvancesByAtMostOne(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueueValidState(e);

    mathint nonceBefore = ghostSqNonce64;

    f(e, args);

    assert(ghostSqNonce64 == nonceBefore || ghostSqNonce64 == nonceBefore + 1,
        "the flush nonce advances by at most one per call");
}
