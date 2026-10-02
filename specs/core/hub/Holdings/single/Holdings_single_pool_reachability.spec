import "Holdings_single_pool_valid_state.spec";

// HO-RC-01: a pool can open the first holding of a share class.
rule rcHoOpeningThePoolsFirstHoldingIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, address valuationSource, Holdings.AccountId[4] accounts) {

    setupHoldingsValidState(e);
    require(aid == ghostHoAssetE1, "SCOPE: opens the first modelled asset beside the second");

    address valuationBefore = ghostHoValuation[aid];
    address siblingBefore = ghostHoValuation[ghostHoAssetE2];

    _Holdings.initialize(e, p, sc, aid, valuationSource, accounts);

    address valuationAfter = ghostHoValuation[aid];
    address siblingAfter = ghostHoValuation[ghostHoAssetE2];
    bool initializedAfter = _Holdings.isInitialized(e, p, sc, aid);

    satisfy(valuationBefore == 0 && siblingBefore == 0 && valuationAfter != 0 && initializedAfter
        && siblingAfter == 0,
        "the first holding of a share class can be opened");
}

// HO-RC-02: opening a holding can set all four of its journal accounts in one call.
rule rcHoOpeningWiringAllFourLedgerAccountsIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, address valuationSource, Holdings.AccountId[4] accounts) {

    setupHoldingsValidState(e);

    _Holdings.initialize(e, p, sc, aid, valuationSource, accounts);

    mathint firstKindAfter = ghostHoAccountId256[aid][0];
    mathint secondKindAfter = ghostHoAccountId256[aid][1];
    mathint thirdKindAfter = ghostHoAccountId256[aid][2];
    mathint fourthKindAfter = ghostHoAccountId256[aid][3];

    satisfy(firstKindAfter != 0 && secondKindAfter != 0 && thirdKindAfter != 0 && fourthKindAfter != 0,
        "one opening can wire all four ledger accounts");
}

// HO-RC-03: a second holding can be opened beside an existing one, leaving it unchanged.
rule rcHoOpeningASecondHoldingIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, address valuationSource, Holdings.AccountId[4] accounts) {

    setupHoldingsValidState(e);
    require(aid == ghostHoAssetE1, "SCOPE: opens the first modelled asset beside the second");

    address siblingBefore = ghostHoValuation[ghostHoAssetE2];

    _Holdings.initialize(e, p, sc, aid, valuationSource, accounts);

    address openedAfter = ghostHoValuation[aid];
    address siblingAfter = ghostHoValuation[ghostHoAssetE2];

    satisfy(siblingBefore != 0 && openedAfter != 0 && siblingAfter == siblingBefore,
        "a second holding can be opened, leaving the first untouched");
}

// HO-RC-04: a deposit can be booked on an open holding and add value to it.
rule rcHoBookingADepositIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc, Holdings.AssetId aid,
    uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    uint128 valueBooked = _Holdings.increase(e, p, sc, aid, cid, flow);

    mathint increasedAfter = ghostHoIncreasedAmount256[aid];
    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    satisfy(valueBooked > 0 && increasedAfter > increasedBefore && valueAfter > valueBefore,
        "a deposit can raise a holding and book a positive value");
}

// HO-RC-05: an empty deposit on an open holding can go through without changing it.
rule rcHoZeroDepositIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc, Holdings.AssetId aid,
    uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    address valuationBefore = ghostHoValuation[aid];
    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    uint128 valueBooked = _Holdings.increase(e, p, sc, aid, cid, flow);

    mathint increasedAfter = ghostHoIncreasedAmount256[aid];
    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    satisfy(valuationBefore != 0 && valueBooked == 0 && increasedAfter == increasedBefore
        && valueAfter == valueBefore,
        "a zero deposit on an opened holding is accepted and books nothing");
}

// HO-RC-06: a deposit the price source values at zero can still grow the holding's amount.
rule rcHoDepositPricedAtNothingIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    address valuationBefore = ghostHoValuation[aid];
    mathint valueBefore = ghostHoAssetAmountValue128[aid];
    uint128 amountViewBefore = _Holdings.amount(e, p, sc, aid);

    uint128 valueBooked = _Holdings.increase(e, p, sc, aid, cid, flow);

    mathint valueAfter = ghostHoAssetAmountValue128[aid];
    uint128 amountViewAfter = _Holdings.amount(e, p, sc, aid);

    satisfy(valuationBefore != 0 && valueBooked == 0 && amountViewAfter > amountViewBefore
        && valueAfter == valueBefore,
        "an opened holding can gain units at zero value");
}

// HO-RC-07: a deposit can be booked on a holding not yet opened, adding no value.
rule rcHoBookingADepositBeforeTheRowIsOpenedIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    address valuationBefore = ghostHoValuation[aid];
    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    uint128 valueBooked = _Holdings.increase(e, p, sc, aid, cid, flow);

    mathint increasedAfter = ghostHoIncreasedAmount256[aid];
    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    satisfy(valuationBefore == 0 && valueBooked == 0 && increasedAfter > increasedBefore
        && valueAfter == valueBefore,
        "a deposit can grow an unopened holding without booking value");
}

// HO-RC-08: a deposit can exactly offset an earlier over-withdrawal, clearing the shortfall.
rule rcHoClearingADeficitExactlyIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint decreasedBefore = ghostHoDecreasedAmount256[aid];
    mathint deficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    _Holdings.increase(e, p, sc, aid, cid, flow);

    mathint increasedAfter = ghostHoIncreasedAmount256[aid];
    mathint decreasedAfter = ghostHoDecreasedAmount256[aid];
    mathint deficitAfter = ghostHoNetworkDeficitCount32;

    satisfy(decreasedBefore > increasedBefore && increasedAfter == decreasedAfter && deficitBefore == 1
        && deficitAfter == 0 && ghostHoDeficitCount32 == classDeficitBefore - 1,
        "a deposit can exactly clear a shortfall, dropping both deficit counts");
}

// HO-RC-09: a withdrawal can be booked on a funded holding and remove value from it.
rule rcHoBookingAWithdrawalIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc, Holdings.AssetId aid,
    uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    mathint decreasedBefore = ghostHoDecreasedAmount256[aid];
    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    uint128 valueRemoved = _Holdings.decrease(e, p, sc, aid, cid, flow);

    mathint decreasedAfter = ghostHoDecreasedAmount256[aid];
    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    satisfy(valueRemoved > 0 && decreasedAfter > decreasedBefore && valueAfter < valueBefore,
        "a withdrawal can shrink a holding and release a positive value");
}

// HO-RC-10: a withdrawal can exceed the holding, leaving it at zero and in shortfall.
rule rcHoWithdrawingPastThePositionIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    mathint valueBefore = ghostHoAssetAmountValue128[aid];
    mathint deficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    uint128 valueRemoved = _Holdings.decrease(e, p, sc, aid, cid, flow);

    mathint valueAfter = ghostHoAssetAmountValue128[aid];
    mathint deficitAfter = ghostHoNetworkDeficitCount32;
    uint128 amountViewAfter = _Holdings.amount(e, p, sc, aid);
    uint256 increasedGross;
    uint256 decreasedGross;
    increasedGross, decreasedGross = _Holdings.holdingAmounts(e, p, sc, aid);

    satisfy(valueBefore > 0 && valueRemoved == valueBefore && valueAfter == 0
        && amountViewAfter == 0 && increasedGross > 0 && decreasedGross > increasedGross
        && deficitAfter == deficitBefore + 1 && ghostHoDeficitCount32 == classDeficitBefore + 1,
        "an over-withdrawal can zero a holding and raise both deficit counts");
}

// HO-RC-11: a withdrawal can close a holding at exactly zero without a shortfall.
rule rcHoClosingThePositionExactlyIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    mathint valueBefore = ghostHoAssetAmountValue128[aid];
    uint128 amountViewBefore = _Holdings.amount(e, p, sc, aid);

    uint128 valueRemoved = _Holdings.decrease(e, p, sc, aid, cid, flow);

    mathint increasedAfter = ghostHoIncreasedAmount256[aid];
    mathint decreasedAfter = ghostHoDecreasedAmount256[aid];
    mathint valueAfter = ghostHoAssetAmountValue128[aid];
    uint128 amountViewAfter = _Holdings.amount(e, p, sc, aid);

    satisfy(amountViewBefore > 0 && amountViewAfter == 0 && increasedAfter == decreasedAfter
        && valueAfter == 0 && valueRemoved == valueBefore,
        "a holding can be drained to zero with outflow matching inflow");
}

// HO-RC-12: a further withdrawal can deepen a shortfall without counting the holding twice.
rule rcHoDeepeningADeficitIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc, Holdings.AssetId aid,
    uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint decreasedBefore = ghostHoDecreasedAmount256[aid];
    mathint deficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    uint128 valueRemoved = _Holdings.decrease(e, p, sc, aid, cid, flow);

    mathint decreasedAfter = ghostHoDecreasedAmount256[aid];
    mathint deficitAfter = ghostHoNetworkDeficitCount32;

    satisfy(decreasedBefore > increasedBefore && decreasedAfter > decreasedBefore && valueRemoved == 0
        && deficitBefore == 1 && deficitAfter == 1 && ghostHoDeficitCount32 == classDeficitBefore,
        "a short holding can go shorter, deficit counts unchanged");
}

// HO-RC-13: two holdings of one share class can be in shortfall at the same time.
rule rcHoDeficitCountCarryingASecondShortRowIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    mathint deficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    _Holdings.decrease(e, p, sc, aid, cid, flow);

    mathint increasedAfter = ghostHoIncreasedAmount256[aid];
    mathint decreasedAfter = ghostHoDecreasedAmount256[aid];
    mathint deficitAfter = ghostHoNetworkDeficitCount32;

    satisfy(deficitBefore == 1 && deficitAfter == 2 && decreasedAfter > increasedAfter
        && ghostHoDeficitCount32 == classDeficitBefore + 1,
        "a second holding can go short, both deficit counts rising by one");
}

// HO-RC-14: a withdrawal can be booked on a holding not yet opened, removing no value.
rule rcHoBookingAWithdrawalBeforeTheRowIsOpenedIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    address valuationBefore = ghostHoValuation[aid];
    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint decreasedBefore = ghostHoDecreasedAmount256[aid];
    uint128 amountViewBefore = _Holdings.amount(e, p, sc, aid);

    uint128 valueRemoved = _Holdings.decrease(e, p, sc, aid, cid, flow);

    mathint decreasedAfter = ghostHoDecreasedAmount256[aid];
    uint128 amountViewAfter = _Holdings.amount(e, p, sc, aid);

    satisfy(valuationBefore == 0 && increasedBefore > 0 && valueRemoved == 0
        && decreasedAfter > decreasedBefore && amountViewAfter < amountViewBefore,
        "a withdrawal can shrink an unopened holding without booking value");
}

// HO-RC-15: a revaluation can raise a holding's value and report the gain.
rule rcHoRevaluationUpwardIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc, Holdings.AssetId aid) {

    setupHoldingsValidState(e);

    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    bool isPositive;
    uint128 diffValue;
    isPositive, diffValue = _Holdings.update(e, p, sc, aid);

    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    satisfy(isPositive && diffValue > 0 && valueAfter > valueBefore,
        "a mark-up can lift a holding and report a positive difference");
}

// HO-RC-16: a revaluation can lower a holding's value and report the loss.
rule rcHoRevaluationDownwardIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid) {

    setupHoldingsValidState(e);

    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    bool isPositive;
    uint128 diffValue;
    isPositive, diffValue = _Holdings.update(e, p, sc, aid);

    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    satisfy(!isPositive && diffValue > 0 && valueAfter < valueBefore,
        "a mark-down can cut a holding and report a negative difference");
}

// HO-RC-17: a network can be marked in sync, advancing its sequence number by one.
rule rcHoMarkingANetworkInSyncIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc, uint16 cid,
    uint64 nonce) {

    setupHoldingsValidState(e);

    bool markerBefore = ghostHoIsSnapshot[cid];
    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    _Holdings.setSnapshot(e, p, sc, cid, true, nonce);

    bool markerAfter = ghostHoIsSnapshot[cid];
    mathint nonceAfter = ghostHoSnapshotNonce64[cid];

    satisfy(!markerBefore && markerAfter && nonceAfter == nonceBefore + 1,
        "an out-of-sync network can be flagged synced, one nonce later");
}

// HO-RC-18: a network marked in sync can be marked out of sync again.
rule rcHoMarkingANetworkOutOfSyncIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc, uint16 cid,
    uint64 nonce) {

    setupHoldingsValidState(e);

    bool markerBefore = ghostHoIsSnapshot[cid];
    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    _Holdings.setSnapshot(e, p, sc, cid, false, nonce);

    bool markerAfter = ghostHoIsSnapshot[cid];
    mathint nonceAfter = ghostHoSnapshotNonce64[cid];

    satisfy(markerBefore && nonceBefore >= 1 && !markerAfter && nonceAfter == nonceBefore + 1,
        "a synced network can lose its sync flag, one nonce later");
}

// HO-RC-19: a network can be marked in sync and back out of sync in one transaction.
rule rcHoSyncAndDesyncRoundTripIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc, uint16 cid,
    uint64 nonce, uint64 nextNonce) {

    setupHoldingsValidState(e);

    bool markerBefore = ghostHoIsSnapshot[cid];
    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    _Holdings.setSnapshot(e, p, sc, cid, true, nonce);

    bool markerMid = ghostHoIsSnapshot[cid];

    _Holdings.setSnapshot(e, p, sc, cid, false, nextNonce);

    bool markerAfter = ghostHoIsSnapshot[cid];
    mathint nonceAfter = ghostHoSnapshotNonce64[cid];

    satisfy(!markerBefore && markerMid && !markerAfter && nonceAfter == nonceBefore + 2,
        "a network can sync and desync in one transaction, nonce up by two");
}

// HO-RC-20: a pool without a snapshot hook can have one attached.
rule rcHoAttachingNavAutomationIsReachable(env e, Holdings.PoolId p, address automation) {

    setupHoldingsValidState(e);

    address hookBefore = ghostHoSnapshotHook;

    _Holdings.setSnapshotHook(e, p, automation);

    address hookAfter = ghostHoSnapshotHook;

    satisfy(hookBefore == 0 && hookAfter != 0, "a snapshot hook can be attached to a pool that had none");
}

// HO-RC-21: a pool's snapshot hook can be attached and removed again.
rule rcHoAutomationAttachAndDetachRoundTripIsReachable(env e, Holdings.PoolId p, address automation,
    address noAutomation) {

    setupHoldingsValidState(e);

    address hookBefore = ghostHoSnapshotHook;

    _Holdings.setSnapshotHook(e, p, automation);

    address hookMid = ghostHoSnapshotHook;

    _Holdings.setSnapshotHook(e, p, noAutomation);

    address hookAfter = ghostHoSnapshotHook;

    satisfy(hookBefore == 0 && hookMid != 0 && hookAfter == 0, "a pool can go from no snapshot hook to one and back");
}

// HO-RC-22: a holding's journal account can be replaced with a different one.
rule rcHoRewiringALedgerAccountIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint8 kind, Holdings.AccountId account) {

    setupHoldingsValidState(e);

    mathint accountBefore = ghostHoAccountId256[aid][kind];

    _Holdings.setAccountId(e, p, sc, aid, kind, account);

    mathint accountAfter = ghostHoAccountId256[aid][kind];

    satisfy(accountBefore != 0 && accountAfter != 0 && accountAfter != accountBefore,
        "a wired ledger account can be redirected to another account");
}

// HO-RC-23: a holding can switch price source without changing its amount or value.
rule rcHoSwappingThePriceSourceIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, address valuationSource) {

    setupHoldingsValidState(e);

    address valuationBefore = ghostHoValuation[aid];
    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint decreasedBefore = ghostHoDecreasedAmount256[aid];
    mathint valueBefore = ghostHoAssetAmountValue128[aid];

    _Holdings.updateValuation(e, p, sc, aid, valuationSource);

    address valuationViewAfter = _Holdings.valuation(e, p, sc, aid);
    mathint increasedAfter = ghostHoIncreasedAmount256[aid];
    mathint decreasedAfter = ghostHoDecreasedAmount256[aid];
    mathint valueAfter = ghostHoAssetAmountValue128[aid];

    satisfy(valuationBefore != 0 && valuationViewAfter != valuationBefore && increasedAfter == increasedBefore
        && decreasedAfter == decreasedBefore && valueAfter == valueBefore,
        "a price source can be swapped with the position and value untouched");
}

// HO-RC-24: admin rights on Holdings can be granted and revoked in one transaction.
rule rcHoWardGrantAndRevokeRoundTripIsReachable(env e, address user) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[user];

    _Holdings.rely(e, user);

    mathint wardMid = _Holdings.wards[user];

    _Holdings.deny(e, user);

    mathint wardAfter = _Holdings.wards[user];

    satisfy(wardBefore == 0 && wardMid == 1 && wardAfter == 0,
        "an account can become a ward and lose it within one transaction");
}

// HO-RC-25: a holding can be opened, funded and emptied, and still show its lifetime totals.
rule rcHoOpeningAndFullyClosingAPositionIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow, address valuationSource, Holdings.AccountId[4] accounts) {

    setupHoldingsValidState(e);

    _Holdings.initialize(e, p, sc, aid, valuationSource, accounts);
    uint128 valueBooked = _Holdings.increase(e, p, sc, aid, cid, flow);
    uint128 valueRemoved = _Holdings.decrease(e, p, sc, aid, cid, flow);

    uint128 amountViewAfter = _Holdings.amount(e, p, sc, aid);
    uint128 valueViewAfter = _Holdings.value(e, p, sc, aid);
    uint256 increasedGross;
    uint256 decreasedGross;
    increasedGross, decreasedGross = _Holdings.holdingAmounts(e, p, sc, aid);

    satisfy(valueBooked > 0 && valueRemoved == valueBooked && amountViewAfter == 0 && valueViewAfter == 0
        && increasedGross == flow && decreasedGross == flow,
        "a holding can take in and pay out one flow, ending at zero");
}

// HO-RC-26: a holding can enter and leave a deficit, and both deficit counts clear again.
rule rcHoEnteringAndLeavingADeficitIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 outflow, uint128 inflow) {

    setupHoldingsValidState(e);

    mathint deficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    _Holdings.decrease(e, p, sc, aid, cid, outflow);

    mathint deficitMid = ghostHoNetworkDeficitCount32;
    mathint classDeficitMid = ghostHoDeficitCount32;
    mathint increasedMid = ghostHoIncreasedAmount256[aid];
    mathint decreasedMid = ghostHoDecreasedAmount256[aid];

    _Holdings.increase(e, p, sc, aid, cid, inflow);

    mathint deficitAfter = ghostHoNetworkDeficitCount32;

    satisfy(deficitBefore == 0 && decreasedMid > increasedMid && deficitMid == 1 && deficitAfter == 0
        && classDeficitMid == classDeficitBefore + 1 && ghostHoDeficitCount32 == classDeficitBefore,
        "a holding can go short and recover in one transaction, counts restored");
}

// HO-RC-29: an amount just deposited can be withdrawn at a value other than the quote it was booked at.
rule rcHoDecreaseBooksOffTheQuoteJustTaken(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint decreasedBefore = ghostHoDecreasedAmount256[aid];
    address valuationBefore = ghostHoValuation[aid];
    mathint quotesBefore = ghostValQuoteCount;

    _Holdings.increase(e, p, sc, aid, cid, flow);

    mathint quotesMid = ghostValQuoteCount;
    uint128 quoteTaken = ghostValLastQuote128;

    uint128 valueRemoved = _Holdings.decrease(e, p, sc, aid, cid, flow);

    satisfy(increasedBefore >= decreasedBefore && valuationBefore != 0 && flow > 0
        && quotesMid == quotesBefore + 1 && ghostValLastBase128 == flow && ghostValQuoteCount == quotesMid
        && valueRemoved != quoteTaken,
        "a same-size withdrawal can return a value unlike the fresh quote");
}

// HO-RC-30: a deposit into a holding in shortfall can be priced only on the part past the shortfall.
rule rcHoNettingInflowPricesOnlyItsPositivePart(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 flow) {

    setupHoldingsValidState(e);

    mathint shortfall = ghostHoDecreasedAmount256[aid] - ghostHoIncreasedAmount256[aid];
    address valuationBefore = ghostHoValuation[aid];
    mathint quotesBefore = ghostValQuoteCount;

    _Holdings.increase(e, p, sc, aid, cid, flow);

    satisfy(shortfall > 0 && valuationBefore != 0 && flow > shortfall
        && ghostValQuoteCount == quotesBefore + 1 && ghostValLastBase128 == flow - shortfall,
        "the quote can cover only the inflow's excess over the shortfall");
}

// HO-RC-31: a funded holding can switch price source and keep its old value, with no quote taken.
rule rcHoStaleValueSurvivesAPriceSourceSwapOnALivePosition(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, address valuationSource) {

    setupHoldingsValidState(e);

    address valuationBefore = ghostHoValuation[aid];
    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint decreasedBefore = ghostHoDecreasedAmount256[aid];
    mathint valueBefore = ghostHoAssetAmountValue128[aid];
    mathint quotesBefore = ghostValQuoteCount;

    _Holdings.updateValuation(e, p, sc, aid, valuationSource);

    satisfy(valuationBefore != 0 && valuationSource != valuationBefore && increasedBefore > decreasedBefore
        && valueBefore > 0 && ghostHoValuation[aid] == valuationSource
        && ghostHoAssetAmountValue128[aid] == valueBefore && ghostValQuoteCount == quotesBefore,
        "the old value can survive a switch to a new source, unquoted");
}
