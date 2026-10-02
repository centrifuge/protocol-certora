import "Accounting_single_pool_valid_state.spec";

// AC-RC-01: an admin can open a journal on a pool, getting a fresh journal id.
rule rcAcUnlockOpensAJournalIsReachable(env e, AccountingHarness.PoolId poolId) {

    setupAccountingValidState(e);

    mathint counterBefore = ghostAcJournalIdCounter64;

    _Accounting.unlock(e, poolId);

    mathint counterAfter = ghostAcJournalIdCounter64;
    mathint journalIdAfter = ghostAcJournalId256;
    mathint currentPoolAfter = ghostAcCurrentPoolT;

    satisfy(currentPoolAfter == poolId && journalIdAfter != 0
        && counterAfter == counterBefore + 1,
        "a ward can open a pool's journal, minting a fresh id");
}

// AC-RC-02: an empty journal can open and close, still using up a journal id.
rule rcAcEmptyJournalOverAnUntouchedLedgerIsReachable(env e, AccountingHarness.PoolId poolId) {

    setupAccountingValidState(e);
    require(ghostAcLastUpdated64[ghostAcAccountE1] == 0 && ghostAcLastUpdated64[ghostAcAccountE2] == 0
        && ghostAcLastUpdated64[ghostAcAccountE3] == 0,
        "SCOPE: no account opened yet");

    mathint counterBefore = ghostAcJournalIdCounter64;

    _Accounting.unlock(e, poolId);
    _Accounting.lock(e);

    mathint counterAfter = ghostAcJournalIdCounter64;
    mathint journalIdAfter = ghostAcJournalId256;
    mathint currentPoolAfter = ghostAcCurrentPoolT;

    satisfy(currentPoolAfter == 0 && journalIdAfter != 0 && counterAfter == counterBefore + 1,
        "a journal with no entries can close and consume one id");
}

// AC-RC-03: a journal can open, post a matching debit and credit to two accounts, and close.
rule rcAcBalancedPairPostsAndClosesIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, AccountingHarness.AccountId creditAccount, uint128 value) {

    setupAccountingValidState(e);
    require(debitAccount != creditAccount, "SCOPE: the two legs post to distinct accounts");

    mathint debitRowBefore = ghostAcTotalDebit128[debitAccount];
    mathint creditRowBefore = ghostAcTotalCredit128[creditAccount];

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, debitAccount, value);
    _Accounting.addCredit(e, creditAccount, value);
    _Accounting.lock(e);

    mathint debitRowAfter = ghostAcTotalDebit128[debitAccount];
    mathint creditRowAfter = ghostAcTotalCredit128[creditAccount];
    mathint currentPoolAfter = ghostAcCurrentPoolT;

    satisfy(debitRowAfter > debitRowBefore && creditRowAfter > creditRowBefore
        && currentPoolAfter == 0,
        "a debit and a credit on two accounts can balance and close");
}

// AC-RC-04: a journal with two non-zero debits can close against one credit of their sum.
rule rcAcTwoDebitsCloseAgainstOneCreditIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId firstDebitAccount, uint128 firstDebitValue,
    AccountingHarness.AccountId secondDebitAccount, uint128 secondDebitValue,
    AccountingHarness.AccountId creditAccount, uint128 creditValue) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, firstDebitAccount, firstDebitValue);
    _Accounting.addDebit(e, secondDebitAccount, secondDebitValue);
    _Accounting.addCredit(e, creditAccount, creditValue);
    _Accounting.lock(e);

    mathint currentPoolAfter = ghostAcCurrentPoolT;

    satisfy(firstDebitValue > 0 && secondDebitValue > 0 && currentPoolAfter == 0,
        "one credit can balance two nonzero debits");
}

// AC-RC-05: a zero-value debit can refresh an account's timestamp without changing totals.
rule rcAcZeroValueDebitRestampsTheRowIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account) {

    setupAccountingValidState(e);
    require(ghostAcLastUpdated64[account] < e.block.timestamp, "SCOPE: the account was last updated before now");

    mathint rowDebitBefore = ghostAcTotalDebit128[account];

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, account, 0);

    mathint rowDebitAfter = ghostAcTotalDebit128[account];
    mathint rowStampAfter = ghostAcLastUpdated64[account];

    satisfy(rowDebitAfter == rowDebitBefore && rowStampAfter == e.block.timestamp,
        "a zero debit restamps the account without moving its total");
}

// AC-RC-06: a zero-value credit can refresh an account's timestamp without changing totals.
rule rcAcZeroValueCreditRestampsTheRowIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account) {

    setupAccountingValidState(e);
    require(ghostAcLastUpdated64[account] < e.block.timestamp, "SCOPE: the account was last updated before now");

    mathint rowCreditBefore = ghostAcTotalCredit128[account];

    _Accounting.unlock(e, poolId);
    _Accounting.addCredit(e, account, 0);

    mathint rowCreditAfter = ghostAcTotalCredit128[account];
    mathint rowStampAfter = ghostAcLastUpdated64[account];

    satisfy(rowCreditAfter == rowCreditBefore && rowStampAfter == e.block.timestamp,
        "a zero credit restamps the account without moving its total");
}

// AC-RC-07: a single debit can fill an empty account's debit side to the maximum value.
rule rcAcDebitFillsARowToTheCeilingIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);
    require(ghostAcTotalDebit128[account] == 0, "SCOPE: the account's debit total starts empty");

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, account, value);

    mathint rowDebitAfter = ghostAcTotalDebit128[account];
    mathint debitedAfter = ghostAcDebitedT;

    satisfy(rowDebitAfter == max_uint128 && debitedAfter == max_uint128,
        "an account's debits can reach the 128-bit ceiling in one entry");
}

// AC-RC-08: a single credit can fill an empty account's credit side to the maximum value.
rule rcAcCreditFillsARowToTheCeilingIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);
    require(ghostAcTotalCredit128[account] == 0, "SCOPE: the account's credit total starts empty");

    _Accounting.unlock(e, poolId);
    _Accounting.addCredit(e, account, value);

    mathint rowCreditAfter = ghostAcTotalCredit128[account];
    mathint creditedAfter = ghostAcCreditedT;

    satisfy(rowCreditAfter == max_uint128 && creditedAfter == max_uint128,
        "an account's credits can reach the 128-bit ceiling in one entry");
}

// AC-RC-09: a journal posting the maximum value on both sides can still close.
rule rcAcCeilingPairPostsAndClosesIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, AccountingHarness.AccountId creditAccount, uint128 value) {

    setupAccountingValidState(e);
    require(debitAccount != creditAccount, "SCOPE: the two legs post to distinct accounts");
    require(ghostAcTotalDebit128[debitAccount] == 0
        && ghostAcTotalCredit128[creditAccount] == 0,
        "SCOPE: each leg's side of its account starts empty");

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, debitAccount, value);
    _Accounting.addCredit(e, creditAccount, value);
    _Accounting.lock(e);

    mathint debitRowAfter = ghostAcTotalDebit128[debitAccount];
    mathint creditRowAfter = ghostAcTotalCredit128[creditAccount];
    mathint currentPoolAfter = ghostAcCurrentPoolT;

    satisfy(debitRowAfter == max_uint128 && creditRowAfter == max_uint128 && currentPoolAfter == 0,
        "a journal can post the maximum amount on each leg and close");
}

// AC-RC-10: an account with debits at the maximum value can still take a credit.
rule rcAcSaturatedDebitRowStillTakesACreditIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);
    require(ghostAcTotalDebit128[account] == max_uint128, "SCOPE: the account's debit total is at its maximum");
    require(ghostAcTotalCredit128[account] == 0, "SCOPE: the account's credit total starts empty");

    _Accounting.unlock(e, poolId);
    _Accounting.addCredit(e, account, value);

    mathint rowCreditAfter = ghostAcTotalCredit128[account];

    satisfy(rowCreditAfter > 0, "a credit can still post to an account whose debits are maxed");
}

// AC-RC-11: a debit can turn a credit-heavy account into a debit-heavy one.
rule rcAcDebitOvertakesACreditHeavyRowIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);
    require(ghostAcTotalCredit128[account] > ghostAcTotalDebit128[account], "SCOPE: the account is credit-heavy");

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, account, value);

    mathint rowDebitAfter = ghostAcTotalDebit128[account];
    mathint rowCreditAfter = ghostAcTotalCredit128[account];

    satisfy(rowDebitAfter > rowCreditAfter, "debits can overtake an account's credits");
}

// AC-RC-12: a debit-normal account can be opened where none existed.
rule rcAcCreateDebitNormalAccountIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account) {

    setupAccountingValidState(e);

    bool existedBefore = _Accounting.exists(e, poolId, account);

    _Accounting.createAccount(e, poolId, account, true);

    bool existsAfter = _Accounting.exists(e, poolId, account);
    bool orientationAfter = ghostAcIsDebitNormal[account];
    mathint stampAfter = ghostAcLastUpdated64[account];

    satisfy(!existedBefore && existsAfter && orientationAfter
        && stampAfter == e.block.timestamp,
        "an account can be created debit-normal, dated to this block");
}

// AC-RC-13: a credit-normal account can be opened with empty debit and credit sides.
rule rcAcCreateCreditNormalAccountIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account) {

    setupAccountingValidState(e);

    _Accounting.createAccount(e, poolId, account, false);

    bool existsAfter = _Accounting.exists(e, poolId, account);
    bool orientationAfter = ghostAcIsDebitNormal[account];
    mathint rowDebitAfter = ghostAcTotalDebit128[account];
    mathint rowCreditAfter = ghostAcTotalCredit128[account];
    mathint stampAfter = ghostAcLastUpdated64[account];

    satisfy(existsAfter && !orientationAfter && rowDebitAfter == 0 && rowCreditAfter == 0
        && stampAfter == e.block.timestamp,
        "a credit-normal account can be opened, stamped and empty");
}

// AC-RC-14: a second account can be opened without disturbing an existing one.
rule rcAcSecondRowOpensBesideALiveOneIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, bool isDebitNormal) {

    setupAccountingValidState(e);
    require(ghostAcLastUpdated64[ghostAcAccountE1] != 0, "SCOPE: the first account is already open");
    require(account == ghostAcAccountE2, "SCOPE: the new account is the second modelled one");

    mathint liveStampBefore = ghostAcLastUpdated64[ghostAcAccountE1];
    mathint liveDebitBefore = ghostAcTotalDebit128[ghostAcAccountE1];

    _Accounting.createAccount(e, poolId, account, isDebitNormal);

    mathint newStampAfter = ghostAcLastUpdated64[ghostAcAccountE2];
    mathint liveStampAfter = ghostAcLastUpdated64[ghostAcAccountE1];
    mathint liveDebitAfter = ghostAcTotalDebit128[ghostAcAccountE1];

    satisfy(newStampAfter != 0 && liveStampAfter == liveStampBefore
        && liveDebitAfter == liveDebitBefore,
        "a second account can open, the first keeping its stamp and debits");
}

// AC-RC-15: a pool's very first account can be opened.
rule rcAcFirstRowOfAnEmptyChartIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, bool isDebitNormal) {

    setupAccountingValidState(e);
    require(ghostAcLastUpdated64[ghostAcAccountE1] == 0 && ghostAcLastUpdated64[ghostAcAccountE2] == 0
        && ghostAcLastUpdated64[ghostAcAccountE3] == 0, "SCOPE: no account opened yet");
    require(account == ghostAcAccountE1, "SCOPE: the opened account is the first modelled one");

    _Accounting.createAccount(e, poolId, account, isDebitNormal);

    mathint firstStampAfter = ghostAcLastUpdated64[ghostAcAccountE1];
    mathint secondStampAfter = ghostAcLastUpdated64[ghostAcAccountE2];
    mathint thirdStampAfter = ghostAcLastUpdated64[ghostAcAccountE3];

    satisfy(firstStampAfter != 0 && secondStampAfter == 0 && thirdStampAfter == 0,
        "the pool's first account can be opened on an empty chart");
}

// AC-RC-16: one journal can debit two accounts, credit a third and still close balanced.
rule rcAcJournalBatchReachesTheWholeChartIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.JournalEntry[] debits, AccountingHarness.JournalEntry[] credits) {

    setupAccountingValidState(e);
    require(debits.length == 2 && credits.length == 2, "SCOPE: two entries on each side");
    require(debits[0].accountId == ghostAcAccountE1
        && debits[1].accountId == ghostAcAccountE2,
        "SCOPE: the debits name the first two accounts");
    require(credits[0].accountId == ghostAcAccountE3, "SCOPE: the first credit names the third account");

    mathint firstDebitBefore = ghostAcTotalDebit128[ghostAcAccountE1];
    mathint secondDebitBefore = ghostAcTotalDebit128[ghostAcAccountE2];
    mathint thirdCreditBefore = ghostAcTotalCredit128[ghostAcAccountE3];

    _AccountingCaller.journalBatch(e, poolId, debits, credits);

    mathint firstDebitAfter = ghostAcTotalDebit128[ghostAcAccountE1];
    mathint secondDebitAfter = ghostAcTotalDebit128[ghostAcAccountE2];
    mathint thirdCreditAfter = ghostAcTotalCredit128[ghostAcAccountE3];
    mathint currentPoolAfter = ghostAcCurrentPoolT;

    satisfy(firstDebitAfter > firstDebitBefore && secondDebitAfter > secondDebitBefore
        && thirdCreditAfter > thirdCreditBefore && currentPoolAfter == 0,
        "one batch can post to all three accounts and still close");
}

// AC-RC-17: an empty journal can go through and still use up a journal id.
rule rcAcEmptyJournalBatchIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.JournalEntry[] debits, AccountingHarness.JournalEntry[] credits) {

    setupAccountingValidState(e);
    require(debits.length == 0 && credits.length == 0, "SCOPE: a batch with no entries");

    mathint debitSumBefore = AC_TOTAL_DEBIT_SUM();
    mathint creditSumBefore = AC_TOTAL_CREDIT_SUM();
    mathint counterBefore = ghostAcJournalIdCounter64;

    _AccountingCaller.journalBatch(e, poolId, debits, credits);

    mathint debitSumAfter = AC_TOTAL_DEBIT_SUM();
    mathint creditSumAfter = AC_TOTAL_CREDIT_SUM();
    mathint counterAfter = ghostAcJournalIdCounter64;
    mathint currentPoolAfter = ghostAcCurrentPoolT;

    satisfy(debitSumAfter == debitSumBefore && creditSumAfter == creditSumBefore
        && counterAfter == counterBefore + 1 && currentPoolAfter == 0,
        "an empty batch is admitted and still spends a journal id");
}

// AC-RC-18: a zero-value journal can close and still refresh an account's timestamp.
rule rcAcZeroValueJournalBatchIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.JournalEntry[] debits, AccountingHarness.JournalEntry[] credits) {

    setupAccountingValidState(e);
    require(debits.length == 1 && credits.length == 1, "SCOPE: one entry on each side");
    require(ghostAcLastUpdated64[debits[0].accountId] < e.block.timestamp,
        "SCOPE: the debit account was last updated before now");
    require(credits[0].accountId != debits[0].accountId, "SCOPE: the credit names a different account");

    mathint debitRowBefore = ghostAcTotalDebit128[debits[0].accountId];

    _AccountingCaller.journalBatch(e, poolId, debits, credits);

    mathint debitRowAfter = ghostAcTotalDebit128[debits[0].accountId];
    mathint debitStampAfter = ghostAcLastUpdated64[debits[0].accountId];
    mathint currentPoolAfter = ghostAcCurrentPoolT;

    satisfy(debitRowAfter == debitRowBefore && debitStampAfter == e.block.timestamp
        && currentPoolAfter == 0,
        "a zero-value batch restamps the debit account and closes");
}

// AC-RC-19: accounts can be created and posted to within one transaction.
rule rcAcRowsCreatedAndJournalledInOneTransactionIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, AccountingHarness.AccountId creditAccount, uint128 value) {

    setupAccountingValidState(e);

    bool debitRowExistedBefore = _Accounting.exists(e, poolId, debitAccount);
    bool creditRowExistedBefore = _Accounting.exists(e, poolId, creditAccount);

    _Accounting.createAccount(e, poolId, debitAccount, true);
    _Accounting.createAccount(e, poolId, creditAccount, false);
    _AccountingCaller.journalPair(e, poolId, debitAccount, value, creditAccount, value);

    mathint debitRowAfter = ghostAcTotalDebit128[debitAccount];
    mathint creditRowAfter = ghostAcTotalCredit128[creditAccount];
    mathint currentPoolAfter = ghostAcCurrentPoolT;

    satisfy(!debitRowExistedBefore && !creditRowExistedBefore && debitRowAfter > 0
        && creditRowAfter > 0 && currentPoolAfter == 0,
        "a journal can post to accounts opened in the same transaction");
}

// AC-RC-20: a newly created account can report exactly the value just posted to it.
rule rcAcFreshRowReadsBackThePostedValueIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, AccountingHarness.AccountId creditAccount, uint128 value) {

    setupAccountingValidState(e);

    _Accounting.createAccount(e, poolId, debitAccount, true);
    _AccountingCaller.journalPair(e, poolId, debitAccount, value, creditAccount, value);

    bool isPositive;
    uint128 reported;
    isPositive, reported = _Accounting.accountValue(e, poolId, debitAccount);

    satisfy(isPositive && reported > 0 && reported == value,
        "a fresh account reads back exactly the value posted to it");
}

// AC-RC-21: a debit-normal account credited more than debited can report a negative value.
rule rcAcDebitNormalRowReportsANegativeValueIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, AccountingHarness.AccountId creditAccount, uint128 value) {

    setupAccountingValidState(e);

    _Accounting.createAccount(e, poolId, creditAccount, true);
    _AccountingCaller.journalPair(e, poolId, debitAccount, value, creditAccount, value);

    bool isPositive;
    uint128 reported;
    isPositive, reported = _Accounting.accountValue(e, poolId, creditAccount);

    satisfy(!isPositive && reported > 0 && reported == value,
        "excess credits can drive a debit-normal account below zero");
}

// AC-RC-22: an account debited and credited by the same amount can report a zero value.
rule rcAcRowDebitedAndCreditedAlikeReadsZeroIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);

    _Accounting.createAccount(e, poolId, account, true);
    _AccountingCaller.journalPair(e, poolId, account, value, account, value);

    bool isPositive;
    uint128 reported;
    isPositive, reported = _Accounting.accountValue(e, poolId, account);
    mathint rowDebitAfter = ghostAcTotalDebit128[account];

    satisfy(reported == 0 && rowDebitAfter > 0, "an account debited and credited alike reads zero");
}

// AC-RC-23: an open journal can report its running debit total as posted so far.
rule rcAcOpenSessionReportsItsRunningSidesIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, account, value);

    uint128 debitedNow = _Accounting.debited(e);
    uint128 creditedNow = _Accounting.credited(e);

    satisfy(debitedNow > 0 && creditedNow == 0 && debitedNow == value,
        "an open journal reports the debit posted and no credit");
}

// AC-RC-24: an admin can grant admin rights and revoke them again in one transaction.
rule rcAcAuthorityGrantRoundTripIsReachable(env e, address user) {

    setupAccountingValidState(e);

    uint256 wardBefore = _Accounting.wards(e, user);

    _Accounting.rely(e, user);

    uint256 wardMid = _Accounting.wards(e, user);

    _Accounting.deny(e, user);

    uint256 wardAfter = _Accounting.wards(e, user);

    satisfy(wardBefore == 0 && wardMid == 1 && wardAfter == 0,
        "ward rights can be granted and revoked in one transaction");
}

// AC-RC-25: an admin can revoke its own admin rights on the ledger.
rule rcAcWardRevokesItselfIsReachable(env e) {

    setupAccountingValidState(e);

    uint256 callerWardBefore = _Accounting.wards(e, e.msg.sender);

    _Accounting.deny(e, e.msg.sender);

    uint256 callerWardAfter = _Accounting.wards(e, e.msg.sender);

    satisfy(callerWardBefore == 1 && callerWardAfter == 0, "a ward can revoke its own ward rights");
}

// AC-RC-26: the hub can post a non-zero balanced debit and credit to two existing accounts.
rule rcAcPassingJournalPairOnABalancedPairIsReachable(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, uint128 debitValue,
    AccountingHarness.AccountId creditAccount, uint128 creditValue) {

    setupAccountingValidState(e);

    require(debitValue == creditValue, "SCOPE: a balanced pair, AC-RV-06 covers the rest");
    require(debitValue != 0, "SCOPE: a nonzero pair, not the trivial zero posting");

    _AccountingCaller.journalPair@withrevert(e, poolId, debitAccount, debitValue, creditAccount, creditValue);
    bool reverted = lastReverted;

    satisfy(!reverted, "a nonzero balanced pair on open accounts can be journaled");
}
