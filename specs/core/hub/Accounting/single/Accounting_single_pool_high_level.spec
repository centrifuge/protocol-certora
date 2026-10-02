import "Accounting_single_pool_valid_state.spec";

// AC-HL-01: a journal can be closed only when its debits and credits balance.
rule hlAcSessionClosesOnlyOnEqualPostedValues(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId firstDebitAccount, uint128 firstDebitValue,
    AccountingHarness.AccountId secondDebitAccount, uint128 secondDebitValue,
    AccountingHarness.AccountId creditAccount, uint128 creditValue) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, firstDebitAccount, firstDebitValue);
    _Accounting.addDebit(e, secondDebitAccount, secondDebitValue);
    _Accounting.addCredit(e, creditAccount, creditValue);
    _Accounting.lock(e);

    assert(firstDebitValue + secondDebitValue == creditValue,
        "a journal closes only if its two debits sum to its credit");
}

// AC-HL-02: posting a journal pair debits only the named account, by the stated amount.
rule hlAcJournalPairDebitsExactlyItsNamedRow(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, uint128 debitValue,
    AccountingHarness.AccountId creditAccount, uint128 creditValue, mathint row) {

    setupAccountingValidState(e);

    mathint rowDebitBefore = ghostAcTotalDebit128[row];

    _AccountingCaller.journalPair(e, poolId, debitAccount, debitValue, creditAccount, creditValue);

    mathint rowDebitAfter = ghostAcTotalDebit128[row];

    assert(rowDebitAfter == rowDebitBefore + (row == debitAccount ? debitValue : 0),
        "a journal pair debits only the named account, by exactly its value");
}

// AC-HL-03: posting a journal pair credits only the named account, by the stated amount.
rule hlAcJournalPairCreditsExactlyItsNamedRow(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, uint128 debitValue,
    AccountingHarness.AccountId creditAccount, uint128 creditValue, mathint row) {

    setupAccountingValidState(e);

    mathint rowCreditBefore = ghostAcTotalCredit128[row];

    _AccountingCaller.journalPair(e, poolId, debitAccount, debitValue, creditAccount, creditValue);

    mathint rowCreditAfter = ghostAcTotalCredit128[row];

    assert(rowCreditAfter == rowCreditBefore + (row == creditAccount ? creditValue : 0),
        "a journal pair credits only the named account, by exactly its value");
}

// AC-HL-04: a pool's second journal in one transaction reuses the first journal's id.
rule hlAcSecondJournalOfAPoolReusesItsJournalId(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId firstDebitAccount, uint128 firstDebitValue,
    AccountingHarness.AccountId firstCreditAccount, uint128 firstCreditValue,
    AccountingHarness.AccountId secondDebitAccount, uint128 secondDebitValue,
    AccountingHarness.AccountId secondCreditAccount, uint128 secondCreditValue) {

    setupAccountingValidState(e);

    _AccountingCaller.journalPair(e, poolId, firstDebitAccount, firstDebitValue,
        firstCreditAccount, firstCreditValue);

    mathint journalIdBefore = ghostAcJournalId256;

    _AccountingCaller.journalPair(e, poolId, secondDebitAccount, secondDebitValue,
        secondCreditAccount, secondCreditValue);

    mathint journalIdAfter = ghostAcJournalId256;

    assert(journalIdAfter == journalIdBefore, "back-to-back journals of a pool share one id");
}

// AC-HL-05: an account's reported balance is the difference between its debits and credits.
rule hlAcAccountValueReportsTheRowsNetMagnitude(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account) {

    setupAccountingValidState(e);

    mathint rowDebit = ghostAcTotalDebit128[account];
    mathint rowCredit = ghostAcTotalCredit128[account];

    bool isPositive;
    uint128 reported;
    isPositive, reported = _Accounting.accountValue(e, poolId, account);

    assert(reported == (rowDebit >= rowCredit ? rowDebit - rowCredit : rowCredit - rowDebit),
        "an account reports the absolute net of its debits and credits");
}

// AC-HL-06: an account reads positive exactly when its normal side is at least the other.
rule hlAcAccountValueSignsByTheRowsOrientation(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account) {

    setupAccountingValidState(e);

    bool rowOrientation = ghostAcIsDebitNormal[account];
    mathint rowDebit = ghostAcTotalDebit128[account];
    mathint rowCredit = ghostAcTotalCredit128[account];

    bool isPositive;
    uint128 reported;
    isPositive, reported = _Accounting.accountValue(e, poolId, account);

    assert(isPositive <=> (rowOrientation ? rowDebit >= rowCredit : rowCredit >= rowDebit),
        "an account is negative exactly when its contra side is larger");
}

// AC-HL-07: a reopened journal starts with zero running debit and credit sums.
rule hlAcReopenedJournalStartsFromEmptyPostedSides(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, AccountingHarness.AccountId creditAccount, uint128 value) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, debitAccount, value);
    _Accounting.addCredit(e, creditAccount, value);
    _Accounting.lock(e);
    _Accounting.unlock(e, poolId);

    mathint debitedAfter = ghostAcDebitedT;
    mathint creditedAfter = ghostAcCreditedT;

    assert(debitedAfter == 0 && creditedAfter == 0, "reopening a journal carries no debit or credit over");
}

// AC-HL-08: a new journal id falls in its pool's own range, so pools' ids never collide.
rule hlAcMintedJournalIdCarriesItsPool(env e, AccountingHarness.PoolId poolId) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);

    mathint journalIdAfter = ghostAcJournalId256;

    assert(journalIdAfter >= poolId * 2^128 && journalIdAfter < (poolId + 1) * 2^128,
        "a newly minted journal id lies in its own pool's id range");
}

// AC-HL-09: opening a journal unlocks accounting for exactly the requested pool.
rule hlAcUnlockOpensTheSessionOnTheNamedPool(env e, AccountingHarness.PoolId poolId) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);

    mathint currentPoolAfter = ghostAcCurrentPoolT;

    assert(currentPoolAfter == poolId, "a journal opens on exactly the pool the call names");
}
