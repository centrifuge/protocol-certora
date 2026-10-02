import "Holdings_single_pool_valid_state.spec";

// --- variable_transitions ---

// HO-VT-01: a holding's lifetime deposit total never decreases.
rule vtHoDepositHistoryNeverShrinks(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[a];

    f(e, args);

    mathint increasedAfter = ghostHoIncreasedAmount256[a];

    assert(increasedAfter >= increasedBefore, "no call lowers a holding's inflow total");
}

// HO-VT-02: a holding's lifetime withdrawal total never decreases.
rule vtHoWithdrawalHistoryNeverShrinks(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint decreasedBefore = ghostHoDecreasedAmount256[a];

    f(e, args);

    mathint decreasedAfter = ghostHoDecreasedAmount256[a];

    assert(decreasedAfter >= decreasedBefore, "no call lowers a holding's outflow total");
}

// HO-VT-03: a holding the pool has opened can never be closed again.
rule vtHoOpenedHoldingIsNeverClosed(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    address valuationBefore = ghostHoValuation[a];

    f(e, args);

    address valuationAfter = ghostHoValuation[a];

    assert(valuationBefore != 0 => valuationAfter != 0, "an opened holding is never closed");
}

// HO-VT-04: a network's sync sequence number advances by at most one per call.
rule vtHoSnapshotNonceStepsByAtMostOne(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    f(e, args);

    mathint nonceAfter = ghostHoSnapshotNonce64[cid];

    assert(nonceAfter == nonceBefore || nonceAfter == nonceBefore + 1,
        "a network's snapshot nonce stays or steps up by one per call");
}

// HO-VT-05: a holding's journal accounts change only through initialize and setAccountId.
rule vtHoAccountWiringMovesOnlyThroughItsTwoWriters(env e, method f, calldataarg args, uint128 a, uint8 k)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    mathint accountBefore = ghostHoAccountId256[a][k];

    f(e, args);

    mathint accountAfter = ghostHoAccountId256[a][k];

    assert(accountAfter != accountBefore
        => f.selector == sig:_Holdings.initialize(Holdings.PoolId,Holdings.ShareClassId,Holdings.AssetId,address,Holdings.AccountId[4]).selector
            || f.selector == sig:_Holdings.setAccountId(Holdings.PoolId,Holdings.ShareClassId,Holdings.AssetId,uint8,Holdings.AccountId).selector,
        "only opening a holding or setting an account changes a ledger account");
}

// HO-VT-06: a pool's NAV hook changes only through setSnapshotHook.
rule vtHoSnapshotHookMovesOnlyThroughItsSetter(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    address hookBefore = ghostHoSnapshotHook;

    f(e, args);

    address hookAfter = ghostHoSnapshotHook;

    assert(hookAfter != hookBefore
        => f.selector == sig:_Holdings.setSnapshotHook(Holdings.PoolId,address).selector,
        "the pool's snapshot hook changes only through its own setter");
}

// HO-VT-07: a network's snapshot nonce changes only through setSnapshot.
rule vtHoSnapshotSequenceMovesOnlyThroughItsPublisher(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    f(e, args);

    mathint nonceAfter = ghostHoSnapshotNonce64[cid];

    assert(nonceAfter != nonceBefore
        => f.selector == sig:_Holdings.setSnapshot(Holdings.PoolId,Holdings.ShareClassId,uint16,bool,uint64).selector,
        "any change to a network's nonce comes from a snapshot update");
}

// --- state_transitions ---

// HO-ST-01: no single call changes both a holding's deposit and withdrawal totals.
rule stHoInflowAndOutflowNeverMoveTogether(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[a];
    mathint decreasedBefore = ghostHoDecreasedAmount256[a];

    f(e, args);

    assert(ghostHoIncreasedAmount256[a] == increasedBefore || ghostHoDecreasedAmount256[a] == decreasedBefore,
        "a call moves a holding's inflow or outflow total, never both");
}

// HO-ST-02: a call changing one holding leaves the share class's other holdings unchanged.
rule stHoOneCallTouchesOneHolding(env e, method f, calldataarg args, uint128 a, uint128 b, uint8 k)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);
    require(VALID_ASSET_HO(a) && VALID_ASSET_HO(b) && a != b, "SCOPE: two distinct assets");

    mathint increasedA = ghostHoIncreasedAmount256[a];
    mathint decreasedA = ghostHoDecreasedAmount256[a];
    mathint valueA = ghostHoAssetAmountValue128[a];
    address valuationA = ghostHoValuation[a];
    mathint accountA = ghostHoAccountId256[a][k];

    mathint increasedB = ghostHoIncreasedAmount256[b];
    mathint decreasedB = ghostHoDecreasedAmount256[b];
    mathint valueB = ghostHoAssetAmountValue128[b];
    address valuationB = ghostHoValuation[b];
    mathint accountB = ghostHoAccountId256[b][k];

    f(e, args);

    bool movedA = ghostHoIncreasedAmount256[a] != increasedA || ghostHoDecreasedAmount256[a] != decreasedA
        || ghostHoAssetAmountValue128[a] != valueA || ghostHoValuation[a] != valuationA
        || ghostHoAccountId256[a][k] != accountA;

    assert(movedA => ghostHoIncreasedAmount256[b] == increasedB && ghostHoDecreasedAmount256[b] == decreasedB
        && ghostHoAssetAmountValue128[b] == valueB && ghostHoValuation[b] == valuationB
        && ghostHoAccountId256[b][k] == accountB,
        "a call that moves one holding leaves any other untouched");
}

// HO-ST-03: an inflow never lowers a holding's value.
rule stHoInflowNeverLowersValue(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[a];
    mathint valueBefore = ghostHoAssetAmountValue128[a];

    f(e, args);

    assert(ghostHoIncreasedAmount256[a] > increasedBefore => ghostHoAssetAmountValue128[a] >= valueBefore,
        "a holding's value holds or rises whenever units come in");
}

// HO-ST-04: an outflow never raises a holding's value.
rule stHoOutflowNeverRaisesValue(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    mathint decreasedBefore = ghostHoDecreasedAmount256[a];
    mathint valueBefore = ghostHoAssetAmountValue128[a];

    f(e, args);

    assert(ghostHoDecreasedAmount256[a] > decreasedBefore => ghostHoAssetAmountValue128[a] <= valueBefore,
        "a holding's value holds or falls whenever units go out");
}

// HO-ST-05: opening a holding books no assets and no value.
rule stHoOpeningAHoldingFundsNothing(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    address valuationBefore = ghostHoValuation[a];
    mathint increasedBefore = ghostHoIncreasedAmount256[a];
    mathint decreasedBefore = ghostHoDecreasedAmount256[a];
    mathint valueBefore = ghostHoAssetAmountValue128[a];

    f(e, args);

    assert(valuationBefore == 0 && ghostHoValuation[a] != 0
        => ghostHoIncreasedAmount256[a] == increasedBefore
            && ghostHoDecreasedAmount256[a] == decreasedBefore
            && ghostHoAssetAmountValue128[a] == valueBefore,
        "the call that opens a holding leaves its totals and value alone");
}

// HO-ST-06: a network's sync flag changes only as its sequence number advances by one.
rule stHoSnapshotFlagMovesWithItsNonce(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    bool markerBefore = ghostHoIsSnapshot[cid];
    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    f(e, args);

    assert(ghostHoIsSnapshot[cid] != markerBefore => ghostHoSnapshotNonce64[cid] == nonceBefore + 1,
        "a network's sync flag flips only with a one-step nonce advance");
}

// HO-ST-11: a sync update to one network leaves every other network's sync state unchanged.
rule stHoSnapshotRowIsPerNetwork(env e, method f, calldataarg args, uint16 cid, uint16 other)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);
    require(cid != other, "SCOPE: two distinct networks");

    bool markerBefore = ghostHoIsSnapshot[cid];
    mathint nonceBefore = ghostHoSnapshotNonce64[cid];
    bool otherMarkerBefore = ghostHoIsSnapshot[other];
    mathint otherNonceBefore = ghostHoSnapshotNonce64[other];

    f(e, args);

    assert(ghostHoIsSnapshot[cid] != markerBefore || ghostHoSnapshotNonce64[cid] != nonceBefore
        => ghostHoIsSnapshot[other] == otherMarkerBefore && ghostHoSnapshotNonce64[other] == otherNonceBefore,
        "a call moves the sync record of at most one network");
}

// HO-ST-16: a pool's deficit counts change only through deposits and withdrawals.
rule stHoDeficitCountersMoveOnlyThroughTheFlowEntries(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    mathint networkBefore = ghostHoNetworkDeficitCount32;
    mathint classBefore = ghostHoDeficitCount32;

    f(e, args);

    assert(ghostHoNetworkDeficitCount32 != networkBefore || ghostHoDeficitCount32 != classBefore
        => f.selector == sig:_Holdings.increase(Holdings.PoolId,Holdings.ShareClassId,Holdings.AssetId,uint16,uint128).selector
            || f.selector == sig:_Holdings.decrease(Holdings.PoolId,Holdings.ShareClassId,Holdings.AssetId,uint16,uint128).selector,
        "a shortfall count moves only on an inflow or an outflow");
}

// HO-ST-17: any call notifies the NAV hook at most once, and only for a network marked in sync.
rule stHoSyncNotificationOnlyUnderAnInSyncMarker(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsValidState(e);

    mathint notificationsBefore = ghostHookOnSyncCount;

    f(e, args);

    assert(ghostHookOnSyncCount - notificationsBefore <= 1
        && (ghostHookOnSyncCount != notificationsBefore => ghostHoIsSnapshot[ghostHookOnSyncCid16]),
        "one notice at most, naming a network whose marker reads in sync");
}
