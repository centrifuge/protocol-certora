import "Holdings_single_pool_valid_state.spec";

// HO-AC-01: only an admin can grant or revoke admin rights on Holdings.
rule acHoWardRightsMoveOnlyForAWard(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    mathint userWardBefore = _Holdings.wards[user];

    f(e, args);

    mathint userWardAfter = _Holdings.wards[user];

    assert(userWardAfter != userWardBefore => senderWardBefore == 1, "a stranger never changes who holds ward rights");
}

// HO-AC-02: only an admin can change a holding's recorded deposits.
rule acHoDepositHistoryMovesOnlyForAWard(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    mathint increasedBefore = ghostHoIncreasedAmount256[a];

    f(e, args);

    mathint increasedAfter = ghostHoIncreasedAmount256[a];

    assert(increasedAfter != increasedBefore => senderWardBefore == 1,
        "a stranger never moves a holding's deposit total");
}

// HO-AC-03: only an admin can change a holding's recorded withdrawals.
rule acHoWithdrawalHistoryMovesOnlyForAWard(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    mathint decreasedBefore = ghostHoDecreasedAmount256[a];

    f(e, args);

    mathint decreasedAfter = ghostHoDecreasedAmount256[a];

    assert(decreasedAfter != decreasedBefore => senderWardBefore == 1,
        "a stranger never moves a holding's withdrawal total");
}

// HO-AC-04: only an admin can change a holding's carrying value.
rule acHoCarryingValueMovesOnlyForAWard(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    mathint valueBefore = ghostHoAssetAmountValue128[a];

    f(e, args);

    mathint valueAfter = ghostHoAssetAmountValue128[a];

    assert(valueAfter != valueBefore => senderWardBefore == 1, "a stranger never moves a holding's value");
}

// HO-AC-05: only an admin can set or change the price source a holding is valued with.
rule acHoPriceSourceMovesOnlyForAWard(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    address valuationBefore = ghostHoValuation[a];

    f(e, args);

    address valuationAfter = ghostHoValuation[a];

    assert(valuationAfter != valuationBefore => senderWardBefore == 1,
        "only a ward can change a holding's price source");
}

// HO-AC-06: only an admin can set or change a holding's journal accounts.
rule acHoJournalWiringMovesOnlyForAWard(env e, method f, calldataarg args, uint128 a, uint8 k)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    mathint accountBefore = ghostHoAccountId256[a][k];

    f(e, args);

    mathint accountAfter = ghostHoAccountId256[a][k];

    assert(accountAfter != accountBefore => senderWardBefore == 1,
        "a stranger never rewires a holding's ledger account");
}

// HO-AC-07: only an admin can set or change a pool's NAV hook.
rule acHoSnapshotHookMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    address hookBefore = ghostHoSnapshotHook;

    f(e, args);

    address hookAfter = ghostHoSnapshotHook;

    assert(hookAfter != hookBefore => senderWardBefore == 1, "only a ward can change the pool's snapshot hook");
}

// HO-AC-08: only an admin can mark a network's assets and shares as in sync or not.
rule acHoSyncMarkerMovesOnlyForAWard(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    bool markerBefore = ghostHoIsSnapshot[cid];

    f(e, args);

    bool markerAfter = ghostHoIsSnapshot[cid];

    assert(markerAfter != markerBefore => senderWardBefore == 1, "only a ward can flip a network's sync flag");
}

// HO-AC-09: only an admin can advance a network's snapshot nonce.
rule acHoSnapshotNonceMovesOnlyForAWard(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    f(e, args);

    mathint nonceAfter = ghostHoSnapshotNonce64[cid];

    assert(nonceAfter != nonceBefore => senderWardBefore == 1, "a stranger never moves a network's snapshot nonce");
}

// HO-AC-10: only an admin can change a pool's deficit counts.
rule acHoDeficitCountMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldings(e);

    mathint senderWardBefore = _Holdings.wards[e.msg.sender];
    mathint deficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    f(e, args);

    mathint deficitAfter = ghostHoNetworkDeficitCount32;
    mathint classDeficitAfter = ghostHoDeficitCount32;

    assert((deficitAfter != deficitBefore || classDeficitAfter != classDeficitBefore) => senderWardBefore == 1,
        "only a ward can move either deficit count");
}
