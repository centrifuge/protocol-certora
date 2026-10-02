import "Accounting_single_pool_valid_state.spec";

// AC-RV-01: opening a journal fails for a caller that is not an admin.
rule rvAcUnlockRefusesANonWard(env e, AccountingHarness.PoolId poolId) {

    setupAccountingValidState(e);

    mathint callerWard = _Accounting.wards[e.msg.sender];
    bool notWard = callerWard != 1;

    _Accounting.unlock@withrevert(e, poolId);
    bool reverted = lastReverted;

    assert(notWard => reverted, "a non-ward cannot open a journal");
}

// AC-RV-02: opening a journal fails while another journal is still open.
rule rvAcUnlockRefusesASecondOpenWhileAJournalStands(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.PoolId secondPoolId) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);

    _Accounting.unlock@withrevert(e, secondPoolId);
    bool reverted = lastReverted;

    assert(reverted, "a journal cannot be opened while another is open");
}

// AC-RV-03: creating an account fails for a non-admin, an empty id, or an existing account.
rule rvAcCreateAccountRefusesANonWardTheNullIdOrARowThatStands(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, bool isDebitNormal) {

    setupAccountingValidState(e);

    mathint callerWard = _Accounting.wards[e.msg.sender];
    bool notWard = callerWard != 1;
    bool nullAccount = account == 0;
    mathint stampBefore = ghostAcLastUpdated64[account];
    bool rowAlreadyStands = stampBefore != 0;

    _Accounting.createAccount@withrevert(e, poolId, account, isDebitNormal);
    bool reverted = lastReverted;

    assert((notWard || nullAccount || rowAlreadyStands) => reverted,
        "opening fails for a non-ward, the null id or an existing account");
}

// AC-RV-04: a debit fails on an account that was never created.
rule rvAcAddDebitRefusesARowTheLedgerNeverOpened(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);

    mathint stampBefore = ghostAcLastUpdated64[account];
    bool rowNeverOpened = stampBefore == 0;

    _Accounting.addDebit@withrevert(e, account, value);
    bool reverted = lastReverted;

    assert(rowNeverOpened => reverted, "a debit to an unopened account is refused");
}

// AC-RV-05: a credit fails on an account that was never created.
rule rvAcAddCreditRefusesARowTheLedgerNeverOpened(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);

    mathint stampBefore = ghostAcLastUpdated64[account];
    bool rowNeverOpened = stampBefore == 0;

    _Accounting.addCredit@withrevert(e, account, value);
    bool reverted = lastReverted;

    assert(rowNeverOpened => reverted, "a credit to an unopened account is refused");
}

// AC-RV-06: closing a journal as admin fails exactly when its debits and credits differ.
rule rvAcLockRevertsIffThePostedSidesDiffer(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId debitAccount, uint128 debitValue,
    AccountingHarness.AccountId creditAccount, uint128 creditValue) {

    setupAccountingValidState(e);

    _Accounting.unlock(e, poolId);
    _Accounting.addDebit(e, debitAccount, debitValue);
    _Accounting.addCredit(e, creditAccount, creditValue);

    mathint debitedBefore = ghostAcDebitedT;
    mathint creditedBefore = ghostAcCreditedT;
    bool sidesDiffer = debitedBefore != creditedBefore;

    _Accounting.lock@withrevert(e);
    bool reverted = lastReverted;

    assert(reverted <=> sidesDiffer, "a journal closes if and only if its debits and credits match");
}

// AC-RV-07: outside an open journal, a non-admin post fails and so does any post with entries.
rule rvAcAddJournalOffSessionRefusesANonWardOrAnyEntry(env e,
    AccountingHarness.JournalEntry[] debits, AccountingHarness.JournalEntry[] credits) {

    setupAccountingValidState(e);

    mathint callerWard = _Accounting.wards[e.msg.sender];
    bool notWard = callerWard != 1;
    bool carriesEntries = debits.length > 0 || credits.length > 0;

    _Accounting.addJournal@withrevert(e, debits, credits);
    bool reverted = lastReverted;

    assert((notWard || carriesEntries) => reverted, "with no journal open, a batch fails for a non-ward or any entry");
}

// AC-RV-08: reading the value of a never-created account fails rather than returning zero.
rule rvAcAccountValueRefusesARowTheLedgerNeverOpened(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account) {

    setupAccountingValidState(e);

    mathint stampBefore = ghostAcLastUpdated64[account];
    bool rowNeverOpened = stampBefore == 0;

    _Accounting.accountValue@withrevert(e, poolId, account);
    bool reverted = lastReverted;

    assert(rowNeverOpened => reverted, "the value of an unopened account is refused, not read as zero");
}

// AC-RV-09: a debit by a non-admin fails even while an admin has a journal open.
rule rvAcAddDebitRefusesAnOutsiderInsideAnOpenJournal(env e, env eOutsider,
    AccountingHarness.PoolId poolId, AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);
    setupEnv(eOutsider);
    require(eOutsider.block.number == e.block.number && eOutsider.block.timestamp == e.block.timestamp,
        "SAFE: both calls in the same block");

    mathint outsiderWard = _Accounting.wards[eOutsider.msg.sender];
    require(outsiderWard != 1, "SCOPE: the second caller is not a ward");

    _Accounting.unlock(e, poolId);

    _Accounting.addDebit@withrevert(eOutsider, account, value);
    bool reverted = lastReverted;

    assert(reverted, "a non-ward cannot debit inside a journal a ward opened");
}

// AC-RV-10: a credit by a non-admin fails even while an admin has a journal open.
rule rvAcAddCreditRefusesAnOutsiderInsideAnOpenJournal(env e, env eOutsider,
    AccountingHarness.PoolId poolId, AccountingHarness.AccountId account, uint128 value) {

    setupAccountingValidState(e);
    setupEnv(eOutsider);
    require(eOutsider.block.number == e.block.number && eOutsider.block.timestamp == e.block.timestamp,
        "SAFE: both calls in the same block");

    mathint outsiderWard = _Accounting.wards[eOutsider.msg.sender];
    require(outsiderWard != 1, "SCOPE: the second caller is not a ward");

    _Accounting.unlock(e, poolId);

    _Accounting.addCredit@withrevert(eOutsider, account, value);
    bool reverted = lastReverted;

    assert(reverted, "a non-ward cannot credit inside a journal a ward opened");
}

// AC-RV-11: closing a journal fails for a non-admin even while one is open.
rule rvAcLockRefusesAnOutsiderOnAnOpenJournal(env e, env eOutsider, AccountingHarness.PoolId poolId) {

    setupAccountingValidState(e);
    setupEnv(eOutsider);
    require(eOutsider.block.number == e.block.number && eOutsider.block.timestamp == e.block.timestamp,
        "SAFE: both calls in the same block");

    mathint outsiderWard = _Accounting.wards[eOutsider.msg.sender];
    require(outsiderWard != 1, "SCOPE: the second caller is not a ward");

    _Accounting.unlock(e, poolId);

    _Accounting.lock@withrevert(eOutsider);
    bool reverted = lastReverted;

    assert(reverted, "a non-ward cannot close a journal a ward opened");
}

// AC-RV-12: reading an existing account's value always succeeds, positive or negative.
rule rvAcAccountValueAlwaysAnswersForARowThatStands(env e, AccountingHarness.PoolId poolId,
    AccountingHarness.AccountId account) {

    setupAccountingValidState(e);
    require(e.msg.value == 0, "UNSAFE: a read carrying ether is not claimed");

    mathint stampBefore = ghostAcLastUpdated64[account];

    _Accounting.accountValue@withrevert(e, poolId, account);
    bool reverted = lastReverted;

    assert(stampBefore != 0 => !reverted, "an opened account's value can always be read");
}

// AC-RV-13: a debit always fails while no journal is open.
rule rvAcAddDebitIsRefusedOffSession(env e, AccountingHarness.AccountId account, uint128 value) {

    setupNullPoolTracked(e);

    _Accounting.addDebit@withrevert(e, account, value);
    bool reverted = lastReverted;

    assert(reverted, "debiting outside a session always reverts");
}

// AC-RV-14: a credit always fails while no journal is open.
rule rvAcAddCreditIsRefusedOffSession(env e, AccountingHarness.AccountId account, uint128 value) {

    setupNullPoolTracked(e);

    _Accounting.addCredit@withrevert(e, account, value);
    bool reverted = lastReverted;

    assert(reverted, "crediting outside a session always reverts");
}

// AC-RV-15: closing a journal always fails when none is open.
rule rvAcLockIsRefusedOffSession(env e) {

    setupNullPoolTracked(e);

    _Accounting.lock@withrevert(e);
    bool reverted = lastReverted;

    assert(reverted, "closing fails while no journal is open, whoever calls");
}

// AC-RV-16: opening a journal fails for the empty pool id.
rule rvAcUnlockRefusesTheNullPool(env e, AccountingHarness.PoolId poolId) {

    setupNullPoolTracked(e);

    bool nullPool = poolId == 0;

    _Accounting.unlock@withrevert(e, poolId);
    bool reverted = lastReverted;

    assert(nullPool => reverted, "no journal opens on the null pool, whoever calls");
}

// AC-RV-17: closing fails when no journal is open, whatever an earlier journal left behind.
rule rvAcLockIsRefusedAfterAClosedJournal(env e) {

    setupEnv(e);

    bool offSession = ghostAcCurrentPoolT == 0;

    _Accounting.lock@withrevert(e);
    bool reverted = lastReverted;

    assert(offSession => reverted, "a close with no open journal is refused");
}
