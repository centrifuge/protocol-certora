import "Accounting_single_pool_valid_state.spec";

// --- variable_transitions ---

// AC-VT-01: an account's total debits never decrease, so posted history cannot be erased.
rule vtAcAccountDebitNeverDecreases(env e, method f, calldataarg args, mathint account)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);
    requireInvariant absentAccountIsEmpty(e);

    mathint debitBefore = ghostAcTotalDebit128[account];

    f(e, args);

    mathint debitAfter = ghostAcTotalDebit128[account];

    assert(debitAfter >= debitBefore, "an account's debit total never decreases");
}

// AC-VT-02: an account's total credits never decrease, so posted history cannot be erased.
rule vtAcAccountCreditNeverDecreases(env e, method f, calldataarg args, mathint account)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);
    requireInvariant absentAccountIsEmpty(e);

    mathint creditBefore = ghostAcTotalCredit128[account];

    f(e, args);

    mathint creditAfter = ghostAcTotalCredit128[account];

    assert(creditAfter >= creditBefore, "an account's credit total never decreases");
}

// AC-VT-03: an account's last update time never goes backwards.
rule vtAcAccountStampNeverRegresses(env e, method f, calldataarg args, mathint account)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);
    requireInvariant lastUpdatedBetweenEnvFloorAndBlock(e);

    mathint stampBefore = ghostAcLastUpdated64[account];

    f(e, args);

    mathint stampAfter = ghostAcLastUpdated64[account];

    assert(stampAfter >= stampBefore, "no call rewinds an account's timestamp");
}

// AC-VT-04: a pool's journal numbering never goes backwards.
rule vtAcJournalCounterNeverRewinds(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccounting(e);

    mathint counterBefore = ghostAcJournalIdCounter64;

    f(e, args);

    mathint counterAfter = ghostAcJournalIdCounter64;

    assert(counterAfter >= counterBefore, "a pool's journal counter never decreases");
}

// --- state_transitions ---

// AC-ST-01: an account's debit-normal or credit-normal side never changes once created.
rule stAcAccountOrientationIsPermanent(env e, method f, calldataarg args, mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccountingValidState(e);

    mathint stampBefore = ghostAcLastUpdated64[a];
    bool normalBefore = ghostAcIsDebitNormal[a];

    f(e, args);

    assert(stampBefore != 0 => ghostAcIsDebitNormal[a] == normalBefore,
        "an opened account's orientation never changes");
}

// AC-ST-05: ledger totals change only when a journal is posted.
rule stAcLedgerMovesOnlyThroughAJournal(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccountingValidState(e);

    mathint debitSumBefore = AC_TOTAL_DEBIT_SUM();
    mathint creditSumBefore = AC_TOTAL_CREDIT_SUM();

    f(e, args);

    mathint debitSumAfter = AC_TOTAL_DEBIT_SUM();
    mathint creditSumAfter = AC_TOTAL_CREDIT_SUM();

    assert(debitSumAfter != debitSumBefore || creditSumAfter != creditSumBefore
        => AC_JOURNAL_FUNCTIONS(f),
        "ledger totals move only through a journal call");
}

// AC-ST-06: a journal a call opens gets an id its pool never issued before.
rule stAcMintedJournalIdWasNeverIssuedBefore(env e, method f, calldataarg args, mathint id)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    setupAccountingValidState(e);
    requireInvariant issuedJournalIdsLieAtOrBelowTheHighWaterMark(e);

    bool issuedBefore = ghostAcIssuedJournalId[id];

    f(e, args);

    mathint journalIdAfter = ghostAcJournalId256;

    assert(journalIdAfter == id && id != 0 => !issuedBefore, "the call's journal id is fresh for the pool");
}
