import "Accounting_single_pool_valid_state.spec";

// AC-AC-01: only an admin's call can change an account's booked debits.
rule acAcDebitHistoryMovesOnlyForAWard(env e, method f, calldataarg args, mathint account)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);

    mathint senderWardBefore = _Accounting.wards[e.msg.sender];
    mathint callerWardBefore = _Accounting.wards[_AccountingCaller];
    mathint debitBefore = ghostAcTotalDebit128[account];

    f(e, args);

    mathint debitAfter = ghostAcTotalDebit128[account];

    assert(debitAfter != debitBefore => (senderWardBefore == 1 || callerWardBefore == 1),
        "an account's debits move only if the sender or the hub is a ward");
}

// AC-AC-02: only an admin's call can change an account's booked credits.
rule acAcCreditHistoryMovesOnlyForAWard(env e, method f, calldataarg args, mathint account)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);

    mathint senderWardBefore = _Accounting.wards[e.msg.sender];
    mathint callerWardBefore = _Accounting.wards[_AccountingCaller];
    mathint creditBefore = ghostAcTotalCredit128[account];

    f(e, args);

    mathint creditAfter = ghostAcTotalCredit128[account];

    assert(creditAfter != creditBefore => (senderWardBefore == 1 || callerWardBefore == 1),
        "an account's credits move only if the sender or the hub is a ward");
}

// AC-AC-03: only an admin's call can change an account's last-updated time.
rule acAcAccountStampMovesOnlyForAWard(env e, method f, calldataarg args, mathint account)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);

    mathint senderWardBefore = _Accounting.wards[e.msg.sender];
    mathint callerWardBefore = _Accounting.wards[_AccountingCaller];
    mathint stampBefore = ghostAcLastUpdated64[account];

    f(e, args);

    mathint stampAfter = ghostAcLastUpdated64[account];

    assert(stampAfter != stampBefore => (senderWardBefore == 1 || callerWardBefore == 1),
        "an account's update time moves only if the sender or the hub is a ward");
}

// AC-AC-04: only an admin can open a new account in the ledger.
rule acAcAccountOpensOnlyForAWard(env e, method f, calldataarg args, mathint account)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);

    mathint senderWardBefore = _Accounting.wards[e.msg.sender];
    mathint stampBefore = ghostAcLastUpdated64[account];

    f(e, args);

    mathint stampAfter = ghostAcLastUpdated64[account];

    assert(stampBefore == 0 && stampAfter != 0 => senderWardBefore == 1, "only a ward can open an account");
}

// AC-AC-05: only an admin can set whether an account is debit-normal or credit-normal.
rule acAcAccountOrientationIsSetOnlyByAWard(env e, method f, calldataarg args, mathint account)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);

    mathint senderWardBefore = _Accounting.wards[e.msg.sender];
    bool orientationBefore = ghostAcIsDebitNormal[account];

    f(e, args);

    bool orientationAfter = ghostAcIsDebitNormal[account];

    assert(orientationAfter != orientationBefore => senderWardBefore == 1,
        "only a ward can change an account's orientation");
}

// AC-AC-06: only an admin can grant or revoke admin rights on Accounting.
rule acAcPermissionsMoveOnlyForAWard(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);

    mathint senderWardBefore = _Accounting.wards[e.msg.sender];
    mathint userWardBefore = _Accounting.wards[user];

    f(e, args);

    mathint userWardAfter = _Accounting.wards[user];

    assert(userWardAfter != userWardBefore => senderWardBefore == 1, "a stranger never changes who holds ward rights");
}

// AC-AC-07: only an admin's call can advance a pool's journal numbering.
rule acAcJournalNumberingAdvancesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);

    mathint senderWardBefore = _Accounting.wards[e.msg.sender];
    mathint callerWardBefore = _Accounting.wards[_AccountingCaller];
    mathint counterBefore = ghostAcJournalIdCounter64;

    f(e, args);

    mathint counterAfter = ghostAcJournalIdCounter64;

    assert(counterAfter != counterBefore => (senderWardBefore == 1 || callerWardBefore == 1),
        "the journal counter moves only if the sender or the hub is a ward");
}

// AC-AC-08: only an admin can leave accounting unlocked for posting.
rule acAcSessionIsLeftOpenOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);

    mathint senderWardBefore = _Accounting.wards[e.msg.sender];

    f(e, args);

    mathint sessionAfter = ghostAcCurrentPoolT;

    assert(sessionAfter != 0 => senderWardBefore == 1, "only a ward can leave a journal open");
}
