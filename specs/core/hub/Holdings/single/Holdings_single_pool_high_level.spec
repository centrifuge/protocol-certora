import "Holdings_single_pool_valid_state.spec";

// HO-HL-01: a deposit is recorded in full and stays so after an equal withdrawal.
rule hlHoDepositHistoryRecordsTheInflowAndSurvivesTheOutflow(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[aid];

    _Holdings.increase(e, p, sc, aid, cid, amount);
    _Holdings.decrease(e, p, sc, aid, cid, amount);

    mathint increasedAfter = ghostHoIncreasedAmount256[aid];

    assert(increasedAfter == increasedBefore + amount,
        "a deposit and equal withdrawal add the amount to the deposit total");
}

// HO-HL-02: a withdrawal following an equal deposit is recorded at its full amount.
rule hlHoWithdrawalHistoryRecordsTheWholeOutflow(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);

    mathint decreasedBefore = ghostHoDecreasedAmount256[aid];

    _Holdings.increase(e, p, sc, aid, cid, amount);
    _Holdings.decrease(e, p, sc, aid, cid, amount);

    mathint decreasedAfter = ghostHoDecreasedAmount256[aid];

    assert(decreasedAfter == decreasedBefore + amount,
        "a deposit and equal withdrawal add the amount to the withdrawal total");
}

// HO-HL-03: a deposit reports exactly the value it adds to the holding.
rule hlHoIncreaseReturnsTheValueItBooked(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);

    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    uint128 valueReturned = _Holdings.increase(e, p, sc, aid, cid, amount);

    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    assert(valueAfter == valueBefore + valueReturned,
        "a deposit raises the holding's value by exactly what it returns");
}

// HO-HL-04: a withdrawal reports exactly the value it removes from the holding.
rule hlHoDecreaseReturnsTheValueItRemoved(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);

    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    uint128 valueReturned = _Holdings.decrease(e, p, sc, aid, cid, amount);

    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    assert(valueAfter == valueBefore - valueReturned,
        "a withdrawal lowers the holding's value by exactly what it returns");
}

// HO-HL-05: a revaluation reports exactly the gain or loss it applies to the holding.
rule hlHoUpdateReportsTheRevaluationItWrote(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid) {

    setupHoldingsValidState(e);

    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    bool isPositive; uint128 diffValue;
    isPositive, diffValue = _Holdings.update(e, p, sc, aid);

    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    assert(valueAfter == (isPositive ? valueBefore + diffValue : valueBefore - diffValue),
        "a revaluation reports exactly the signed change it books");
}

// HO-HL-06: each accepted snapshot update advances the network's snapshot nonce by one.
rule hlHoPublishingASyncMarkerAlwaysAdvancesTheSequence(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    uint16 cid, bool isSnapshot, uint64 nonce) {

    setupHoldingsValidState(e);

    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    _Holdings.setSnapshot(e, p, sc, cid, isSnapshot, nonce);

    mathint nonceAfter = ghostHoSnapshotNonce64[cid];

    assert(nonceAfter == nonceBefore + 1, "an accepted sync update steps the network's nonce by exactly one");
}

// HO-HL-07: a snapshot update notifies the NAV hook, with its class and network, exactly when in sync.
rule hlHoSyncNotificationCarriesTheMarkersOwnKeys(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    uint16 cid, bool isSnapshot, uint64 nonce) {

    setupHoldingsValidState(e);
    require(ghostHoSnapshotHook != 0, "SCOPE: a pool with a snapshot hook to notify");

    mathint notificationsBefore = ghostHookOnSyncCount;

    _Holdings.setSnapshot(e, p, sc, cid, isSnapshot, nonce);

    assert(isSnapshot
        ? (ghostHookOnSyncCount == notificationsBefore + 1
            && ghostHookOnSyncPool64 == p && ghostHookOnSyncScId == sc
            && ghostHookOnSyncCid16 == cid)
        : ghostHookOnSyncCount == notificationsBefore,
        "a sync update notifies the hook exactly when in sync, with its own ids");
}

// HO-HL-08: a snapshot replay notifies the NAV hook, with its class and network, exactly when in sync.
rule hlHoReplayNotifiesUnderTheMarkersOwnKeys(env e, Holdings.PoolId p, Holdings.ShareClassId sc, uint16 cid) {

    setupHoldingsValidState(e);
    require(ghostHoSnapshotHook != 0, "SCOPE: a pool with a snapshot hook to notify");

    bool inSync;
    uint64 storedNonce;
    inSync, storedNonce = _Holdings.snapshot(e, p, sc, cid);
    mathint notificationsBefore = ghostHookOnSyncCount;

    _Holdings.callOnSyncSnapshot(e, p, sc, cid);

    assert(inSync
        ? (ghostHookOnSyncCount == notificationsBefore + 1
            && ghostHookOnSyncPool64 == p && ghostHookOnSyncScId == sc
            && ghostHookOnSyncCid16 == cid)
        : ghostHookOnSyncCount == notificationsBefore,
        "a replay notifies the hook exactly when in sync, with its own ids");
}

// HO-HL-09: a withdrawal removes value in proportion to the amount it takes out, rounded down.
rule hlHoDecreaseRemovesValueProRataToTheRealizedAmount(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);

    mathint increased = ghostHoIncreasedAmount256[aid];
    mathint decreased = ghostHoDecreasedAmount256[aid];
    mathint valueBefore = ghostHoAssetAmountValue128[aid];
    mathint oldAmount = increased >= decreased ? increased - decreased : 0;
    mathint newAmount = increased >= decreased + amount ? increased - decreased - amount : 0;
    mathint removed = oldAmount - newAmount;

    uint128 valueReturned = _Holdings.decrease(e, p, sc, aid, cid, amount);

    assert(oldAmount == 0 => valueReturned == 0, "an empty holding gives up no value");
    assert(oldAmount != 0 => (valueReturned * oldAmount <= valueBefore * removed
            && valueBefore * removed < (valueReturned + 1) * oldAmount),
        "the value removed is the old value's pro rata share, rounded down");
}

// HO-HL-10: a deposit books one quote from the holding's source on the part past any shortfall, else zero.
rule hlHoIncreaseQuotesOnlyTheRealizedAmount(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);

    mathint increased = ghostHoIncreasedAmount256[aid];
    mathint decreased = ghostHoDecreasedAmount256[aid];
    address source = ghostHoValuation[aid];
    mathint oldAmount = increased >= decreased ? increased - decreased : 0;
    mathint newAmount = increased + amount >= decreased ? increased + amount - decreased : 0;
    mathint realized = newAmount - oldAmount;
    mathint quotesBefore = ghostValQuoteCount;

    uint128 valueBooked = _Holdings.increase(e, p, sc, aid, cid, amount);

    assert((realized != 0 && source != 0)
        ? (ghostValQuoteCount == quotesBefore + 1 && ghostValLastCallee == source
            && ghostValLastAsset128 == aid && ghostValLastBase128 == realized
            && valueBooked == ghostValLastQuote128)
        : (ghostValQuoteCount == quotesBefore && valueBooked == 0),
        "one quote of the net inflow is booked, else no quote and zero");
}

// HO-HL-11: a revaluation carries one quote of the unchanged amount from the holding's own source.
rule hlHoUpdateMarksTheBookToTheQuoteOfItsAmount(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid) {

    setupHoldingsValidState(e);

    mathint increased = ghostHoIncreasedAmount256[aid];
    mathint decreased = ghostHoDecreasedAmount256[aid];
    mathint heldAmount = increased >= decreased ? increased - decreased : 0;
    address source = ghostHoValuation[aid];
    mathint quotesBefore = ghostValQuoteCount;

    _Holdings.update(e, p, sc, aid);

    uint128 amountViewAfter = _Holdings.amount(e, p, sc, aid);

    assert(ghostValQuoteCount == quotesBefore + 1 && ghostValLastCallee == source
        && ghostValLastBase128 == heldAmount
        && ghostHoAssetAmountValue128[aid] == ghostValLastQuote128
        && amountViewAfter == heldAmount,
        "the value is one quote of the held amount by its source, amount kept");
}

// HO-HL-12: a withdrawal never asks a price source for a quote.
rule hlHoDecreaseNeverConsultsTheOracle(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);

    mathint quotesBefore = ghostValQuoteCount;

    _Holdings.decrease(e, p, sc, aid, cid, amount);

    assert(ghostValQuoteCount == quotesBefore, "no quote is taken while withdrawing");
}

// HO-HL-13: switching a holding's price source takes no quote and leaves its value unchanged.
rule hlHoPriceSourceSwapLeavesTheCarryingValueStanding(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, address valuationSource) {

    setupHoldingsValidState(e);

    mathint valueBefore = ghostHoAssetAmountValue128[aid];
    mathint quotesBefore = ghostValQuoteCount;

    _Holdings.updateValuation(e, p, sc, aid, valuationSource);

    assert(ghostHoAssetAmountValue128[aid] == valueBefore && ghostValQuoteCount == quotesBefore,
        "the value stands and no quote is taken on a source swap");
}

// HO-HL-18: a holding reports its amount as inflow minus outflow, or zero when overdrawn.
rule hlHoHoldingViewReportsTheFlooredNetOfWideTotals(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid) {

    setupHoldingsValidState(e);

    mathint increased = ghostHoIncreasedAmount256[aid];
    mathint decreased = ghostHoDecreasedAmount256[aid];
    mathint net = increased >= decreased ? increased - decreased : 0;

    uint128 heldAmount; uint128 heldValue; address source;
    heldAmount, heldValue, source = _Holdings.holding(e, p, sc, aid);
    uint128 amountView = _Holdings.amount(e, p, sc, aid);

    assert(heldAmount == net && amountView == net && heldValue == ghostHoAssetAmountValue128[aid]
        && source == ghostHoValuation[aid],
        "the views report the floored net of the totals, the stored value and source");
}
