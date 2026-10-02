import "setup/SnapshotQueue_multi_pool.spec";

// --- state_transitions ---

// SQ-ST-06: changing one pool's share queue never touches another pool's share queue.
rule stSqShareRowIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueue(e);
    require(SQ_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint deltaPBefore = ghostSqPoolDelta128[p];
    bool signPBefore = ghostSqPoolIsPositive[p];
    mathint counterPBefore = ghostSqPoolQueuedAssetCounter32[p];
    mathint noncePBefore = ghostSqPoolNonce64[p];
    mathint deltaQBefore = ghostSqPoolDelta128[q];
    bool signQBefore = ghostSqPoolIsPositive[q];
    mathint counterQBefore = ghostSqPoolQueuedAssetCounter32[q];
    mathint nonceQBefore = ghostSqPoolNonce64[q];

    f(e, args);

    assert(ghostSqPoolDelta128[p] != deltaPBefore || ghostSqPoolIsPositive[p] != signPBefore
        || ghostSqPoolQueuedAssetCounter32[p] != counterPBefore || ghostSqPoolNonce64[p] != noncePBefore
        => ghostSqPoolDelta128[q] == deltaQBefore && ghostSqPoolIsPositive[q] == signQBefore
            && ghostSqPoolQueuedAssetCounter32[q] == counterQBefore
            && ghostSqPoolNonce64[q] == nonceQBefore,
        "a call changes the share queue of at most one pool");
}

// SQ-ST-07: changing one pool's asset queue never touches another pool's asset queues.
rule stSqAssetRowIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q, uint128 a, uint128 b)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueue(e);
    require(SQ_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint depositsPBefore = ghostSqPoolDeposits128[p][a];
    mathint withdrawalsPBefore = ghostSqPoolWithdrawals128[p][a];
    mathint depositsQBefore = ghostSqPoolDeposits128[q][b];
    mathint withdrawalsQBefore = ghostSqPoolWithdrawals128[q][b];

    f(e, args);

    assert(ghostSqPoolDeposits128[p][a] != depositsPBefore
        || ghostSqPoolWithdrawals128[p][a] != withdrawalsPBefore
        => ghostSqPoolDeposits128[q][b] == depositsQBefore
            && ghostSqPoolWithdrawals128[q][b] == withdrawalsQBefore,
        "a call changes the asset queues of at most one pool");
}

// SQ-ST-08: changing one pool's share queue never touches another pool's asset queues.
rule stSqQueueSidesDoNotCrossPools(env e, method f, calldataarg args, uint64 p, uint64 q, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueue(e);
    require(SQ_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint deltaPBefore = ghostSqPoolDelta128[p];
    bool signPBefore = ghostSqPoolIsPositive[p];
    mathint counterPBefore = ghostSqPoolQueuedAssetCounter32[p];
    mathint noncePBefore = ghostSqPoolNonce64[p];
    mathint depositsQBefore = ghostSqPoolDeposits128[q][a];
    mathint withdrawalsQBefore = ghostSqPoolWithdrawals128[q][a];

    f(e, args);

    assert(ghostSqPoolDelta128[p] != deltaPBefore || ghostSqPoolIsPositive[p] != signPBefore
        || ghostSqPoolQueuedAssetCounter32[p] != counterPBefore || ghostSqPoolNonce64[p] != noncePBefore
        => ghostSqPoolDeposits128[q][a] == depositsQBefore
            && ghostSqPoolWithdrawals128[q][a] == withdrawalsQBefore,
        "a share queue move leaves other pools' asset flows unchanged");
}
