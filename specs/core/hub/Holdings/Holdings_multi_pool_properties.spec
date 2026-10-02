import "setup/Holdings_multi_pool.spec";
import "../HubRegistry/setup/HubRegistry_cvl.spec";

// --- state_transitions ---

// HO-ST-07: a call that changes one pool's holding leaves other pools' holdings unchanged.
rule stHoHoldingRowIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q, uint128 a, uint128 b)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);
    require(HO_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint increasedPBefore = ghostHoPoolIncreasedAmount256[p][a];
    mathint decreasedPBefore = ghostHoPoolDecreasedAmount256[p][a];
    mathint valuePBefore = ghostHoPoolAssetAmountValue128[p][a];
    address valuationPBefore = ghostHoPoolValuation[p][a];
    mathint increasedQBefore = ghostHoPoolIncreasedAmount256[q][b];
    mathint decreasedQBefore = ghostHoPoolDecreasedAmount256[q][b];
    mathint valueQBefore = ghostHoPoolAssetAmountValue128[q][b];
    address valuationQBefore = ghostHoPoolValuation[q][b];

    f(e, args);

    assert(ghostHoPoolIncreasedAmount256[p][a] != increasedPBefore
        || ghostHoPoolDecreasedAmount256[p][a] != decreasedPBefore
        || ghostHoPoolAssetAmountValue128[p][a] != valuePBefore
        || ghostHoPoolValuation[p][a] != valuationPBefore
        => ghostHoPoolIncreasedAmount256[q][b] == increasedQBefore
            && ghostHoPoolDecreasedAmount256[q][b] == decreasedQBefore
            && ghostHoPoolAssetAmountValue128[q][b] == valueQBefore
            && ghostHoPoolValuation[q][b] == valuationQBefore,
        "a call changes holdings in at most one pool");
}

// HO-ST-08: setting one pool's journal accounts leaves other pools' accounts unchanged.
rule stHoAccountWiringIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q, uint128 a,
    uint128 b, uint8 k) filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);
    require(HO_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint wiredPBefore = ghostHoPoolAccountId256[p][a][k];
    mathint wiredQBefore = ghostHoPoolAccountId256[q][b][k];

    f(e, args);

    assert(ghostHoPoolAccountId256[p][a][k] != wiredPBefore
        => ghostHoPoolAccountId256[q][b][k] == wiredQBefore,
        "a call rewires ledger accounts in at most one pool");
}

// HO-ST-09: a pool's snapshot change never touches another pool's snapshot on that network.
rule stHoSnapshotRowIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);
    require(HO_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    bool markerPBefore = ghostHoPoolIsSnapshot[p][cid];
    mathint noncePBefore = ghostHoPoolSnapshotNonce64[p][cid];
    bool markerQBefore = ghostHoPoolIsSnapshot[q][cid];
    mathint nonceQBefore = ghostHoPoolSnapshotNonce64[q][cid];

    f(e, args);

    assert(ghostHoPoolIsSnapshot[p][cid] != markerPBefore
        || ghostHoPoolSnapshotNonce64[p][cid] != noncePBefore
        => ghostHoPoolIsSnapshot[q][cid] == markerQBefore
            && ghostHoPoolSnapshotNonce64[q][cid] == nonceQBefore,
        "a call changes one network's snapshot in at most one pool");
}

// HO-ST-10: a deposit or withdrawal never changes another pool's deficit counts or NAV hook.
rule stHoDeficitCountAndHookIgnoreASiblingsFlow(env e, method f, calldataarg args, uint64 p, uint64 q,
    uint128 a) filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);
    require(HO_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint increasedPBefore = ghostHoPoolIncreasedAmount256[p][a];
    mathint decreasedPBefore = ghostHoPoolDecreasedAmount256[p][a];
    mathint deficitQBefore = ghostHoPoolNetworkDeficitCount32[q];
    mathint classDeficitQBefore = ghostHoPoolDeficitCount32[q];
    address hookQBefore = ghostHoPoolSnapshotHook[q];

    f(e, args);

    assert(ghostHoPoolIncreasedAmount256[p][a] != increasedPBefore
        || ghostHoPoolDecreasedAmount256[p][a] != decreasedPBefore
        => ghostHoPoolNetworkDeficitCount32[q] == deficitQBefore
            && ghostHoPoolDeficitCount32[q] == classDeficitQBefore
            && ghostHoPoolSnapshotHook[q] == hookQBefore,
        "a flow in one pool leaves the other's deficit counts and hook alone");
}

// --- high_level ---

// HO-HL-16: setting a snapshot bumps its pool's nonce and moves no other pool's snapshot on that network.
rule hlHoSetSnapshotBumpsTheNamedPoolsNonce(env e, Holdings.PoolId p, Holdings.PoolId q, Holdings.ShareClassId sc,
    uint16 cid, bool isSnapshot, uint64 nonce) {

    setupHoldings(e);
    require(HO_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint nonceBefore = ghostHoPoolSnapshotNonce64[p][cid];
    mathint otherNonceBefore = ghostHoPoolSnapshotNonce64[q][cid];
    bool otherMarkerBefore = ghostHoPoolIsSnapshot[q][cid];

    _Holdings.setSnapshot(e, p, sc, cid, isSnapshot, nonce);

    assert(ghostHoPoolSnapshotNonce64[p][cid] == nonceBefore + 1
        && ghostHoPoolSnapshotNonce64[q][cid] == otherNonceBefore
        && ghostHoPoolIsSnapshot[q][cid] == otherMarkerBefore,
        "the named pool's nonce rises by one, the other pool's snapshot stays");
}
