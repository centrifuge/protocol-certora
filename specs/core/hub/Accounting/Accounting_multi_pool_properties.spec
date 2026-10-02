import "setup/Accounting_multi_pool.spec";

// --- state_transitions ---

// AC-ST-02: a call changing an account in one pool leaves another pool's accounts untouched.
rule stAcAccountRowsArePerPool(env e, method f, calldataarg args, uint64 p, uint64 q, mathint a, mathint b)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    SETUP_MULTI_AC(e);
    require(AC_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint debitPBefore = ghostAcPoolTotalDebit128[p][a];
    mathint creditPBefore = ghostAcPoolTotalCredit128[p][a];
    bool normalPBefore = ghostAcPoolIsDebitNormal[p][a];
    mathint stampPBefore = ghostAcPoolLastUpdated64[p][a];
    mathint debitQBefore = ghostAcPoolTotalDebit128[q][b];
    mathint creditQBefore = ghostAcPoolTotalCredit128[q][b];
    bool normalQBefore = ghostAcPoolIsDebitNormal[q][b];
    mathint stampQBefore = ghostAcPoolLastUpdated64[q][b];

    f(e, args);

    assert(ghostAcPoolTotalDebit128[p][a] != debitPBefore
        || ghostAcPoolTotalCredit128[p][a] != creditPBefore
        || ghostAcPoolIsDebitNormal[p][a] != normalPBefore
        || ghostAcPoolLastUpdated64[p][a] != stampPBefore
        => ghostAcPoolTotalDebit128[q][b] == debitQBefore
            && ghostAcPoolTotalCredit128[q][b] == creditQBefore
            && ghostAcPoolIsDebitNormal[q][b] == normalQBefore
            && ghostAcPoolLastUpdated64[q][b] == stampQBefore,
        "a call moves the accounts of at most one pool");
}

// AC-ST-03: a call advancing one pool's journal ids leaves another pool's ids unchanged.
rule stAcJournalNumberingIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q)
    filtered { f -> !EXCLUDED_FUNCTION_AC(f) } {

    SETUP_MULTI_AC(e);
    require(AC_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint counterPBefore = ghostAcPoolJournalIdCounter64[p];
    mathint counterQBefore = ghostAcPoolJournalIdCounter64[q];

    f(e, args);

    assert(ghostAcPoolJournalIdCounter64[p] != counterPBefore
        => ghostAcPoolJournalIdCounter64[q] == counterQBefore,
        "a call moves the journal counter of at most one pool");
}

// AC-ST-04: once a pool has a journal id in a transaction, no call for any pool changes it.
rule stAcAPoolsJournalIdIsFixedForTheTransaction(env e, method f, calldataarg args, bytes32 slot)
    filtered { f -> !f.isView && !f.isPure && !f.isFallback } {

    setupAccountingMidTransaction(e);

    mathint journalIdBefore = ghostAcTransientSlot256[slot];

    f(e, args);

    mathint journalIdAfter = ghostAcTransientSlot256[slot];

    assert(journalIdBefore != 0 => journalIdAfter == journalIdBefore, "a journal id already set is never overwritten");
}

// --- high_level ---

// AC-HL-11: a second pool opening a journal in one transaction gets an id in its own range.
rule hlAcSecondPoolOfATransactionOpensUnderItsOwnId(env e, AccountingHarness.PoolId firstPool,
    AccountingHarness.PoolId secondPool, AccountingHarness.AccountId debitAccount, uint128 debitValue,
    AccountingHarness.AccountId creditAccount, uint128 creditValue) {

    SETUP_MULTI_AC(e);
    require(AC_POOL_PAIR(firstPool, secondPool), "SCOPE: two distinct pools");

    _AccountingCaller.journalPair(e, firstPool, debitAccount, debitValue, creditAccount, creditValue);
    _Accounting.unlock(e, secondPool);

    mathint filedId = ghostAcFiledJournalId256;

    assert(filedId >= secondPool * 2^128 && filedId < (secondPool + 1) * 2^128,
        "a second pool in the transaction opens under an id of its own range");
}
