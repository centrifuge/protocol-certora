// Accounting, single-pool lane. Setup: rows keyed by account, journal pinned to the pool.

// Own setup: rows keyed by account for the pinned pool; multi_pool hooks the same fields with a pool key.

import "Accounting_base.spec";
import "../../../../shared/domains/single_pool.spec";

persistent ghost mapping(mathint => mathint) ghostAcTotalDebit128 {
    init_state axiom forall mathint a. ghostAcTotalDebit128[a] == 0;
    axiom forall mathint a. ghostAcTotalDebit128[a] >= 0 && ghostAcTotalDebit128[a] <= max_uint128;
    axiom forall mathint a. !VALID_ACCOUNT(a) => ghostAcTotalDebit128[a] == 0;
}

hook Sload uint128 val _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].totalDebit {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    require(ghostAcTotalDebit128[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].totalDebit uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    ghostAcTotalDebit128[a] = val;
}

persistent ghost mapping(mathint => mathint) ghostAcTotalCredit128 {
    init_state axiom forall mathint a. ghostAcTotalCredit128[a] == 0;
    axiom forall mathint a. ghostAcTotalCredit128[a] >= 0 && ghostAcTotalCredit128[a] <= max_uint128;
    axiom forall mathint a. !VALID_ACCOUNT(a) => ghostAcTotalCredit128[a] == 0;
}

hook Sload uint128 val _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].totalCredit {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    require(ghostAcTotalCredit128[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].totalCredit uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    ghostAcTotalCredit128[a] = val;
}

persistent ghost mapping(mathint => bool) ghostAcIsDebitNormal {
    init_state axiom forall mathint a. !ghostAcIsDebitNormal[a];
    axiom forall mathint a. !VALID_ACCOUNT(a) => !ghostAcIsDebitNormal[a];
}

hook Sload bool val _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].isDebitNormal {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    require(ghostAcIsDebitNormal[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].isDebitNormal bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    ghostAcIsDebitNormal[a] = val;
}

persistent ghost mapping(mathint => mathint) ghostAcLastUpdated64 {
    init_state axiom forall mathint a. ghostAcLastUpdated64[a] == 0;
    axiom forall mathint a. ghostAcLastUpdated64[a] >= 0 && ghostAcLastUpdated64[a] <= max_uint64;
    axiom forall mathint a. !VALID_ACCOUNT(a) => ghostAcLastUpdated64[a] == 0;
}

hook Sload uint64 val _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].lastUpdated {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    require(ghostAcLastUpdated64[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].lastUpdated uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    ghostAcLastUpdated64[a] = val;
}

methods {
    function TransientJournal.journalId(AccountingHarness.PoolId poolId) internal returns (uint256)
        => accountingJournalIdCVL(poolId);
    function TransientJournal.setJournalId(AccountingHarness.PoolId poolId, uint256 value) internal
        => accountingSetJournalIdCVL(poolId, value);
}

persistent ghost mathint ghostAcJournalId256 {
    init_state axiom ghostAcJournalId256 == 0;
    axiom ghostAcJournalId256 >= 0 && ghostAcJournalId256 <= max_uint256;
}

function accountingJournalIdCVL(AccountingHarness.PoolId poolId) returns uint256 {
    require(VALID_POOL(poolId), "SCOPE: modelled pools stand for any");
    return require_uint256(ghostAcJournalId256);
}

persistent ghost mapping(mathint => bool) ghostAcIssuedJournalId {
    init_state axiom forall mathint id. !ghostAcIssuedJournalId[id];
}

function accountingSetJournalIdCVL(AccountingHarness.PoolId poolId, uint256 value) {
    require(VALID_POOL(poolId), "SCOPE: modelled pools stand for any");
    ghostAcJournalId256 = value;
    if (value != 0) {
        ghostAcIssuedJournalId[value] = true;
    }
}

function setupJournalRegion() {
    require(ghostAcJournalId256 == 0, "SAFE: transient storage starts empty");
}

persistent ghost mathint ghostAcJournalIdCounter64 {
    init_state axiom ghostAcJournalIdCounter64 == 0;
    axiom ghostAcJournalIdCounter64 >= 0 && ghostAcJournalIdCounter64 <= max_uint64;
}

hook Sload uint64 val _Accounting._poolJournalIdCounter[KEY AccountingHarness.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostAcJournalIdCounter64 == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting._poolJournalIdCounter[KEY AccountingHarness.PoolId p] uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostAcJournalIdCounter64 = val;
}

definition AC_TOTAL_DEBIT_SUM() returns mathint =
    ghostAcTotalDebit128[ghostAcAccountE1] + ghostAcTotalDebit128[ghostAcAccountE2]
    + ghostAcTotalDebit128[ghostAcAccountE3];

definition AC_TOTAL_CREDIT_SUM() returns mathint =
    ghostAcTotalCredit128[ghostAcAccountE1] + ghostAcTotalCredit128[ghostAcAccountE2]
    + ghostAcTotalCredit128[ghostAcAccountE3];

definition AC_JOURNAL_FUNCTIONS(method f) returns bool =
    f.selector == sig:_AccountingCaller.journalPair(
        AccountingHarness.PoolId, AccountingHarness.AccountId, uint128, AccountingHarness.AccountId, uint128).selector
    || f.selector == sig:_AccountingCaller.journalBatch(
        AccountingHarness.PoolId, AccountingHarness.JournalEntry[], AccountingHarness.JournalEntry[]).selector;

function assumeAbsentAccountIsEmpty() {
    require(forall mathint a. ghostAcLastUpdated64[a] == 0
        => (ghostAcTotalDebit128[a] == 0 && ghostAcTotalCredit128[a] == 0 && !ghostAcIsDebitNormal[a]),
        "PROVED: absentAccountIsEmpty (Accounting)");
}

function assumeNullAccountNeverCreated() {
    require(ghostAcLastUpdated64[0] == 0, "PROVED: nullAccountNeverCreated (Accounting)");
}

function setupNullPoolTracked(env e) {
    setupEnv(e);
    setupAccountDomain();
    setupJournalRegion();
    require(ghostPoolA64 == 0 && ghostPoolB64 == 0, "SCOPE: the null pool is modelled, off-session calls use it");
    require(ghostAcCurrentPoolT == 0 && ghostAcDebitedT == 0 && ghostAcCreditedT == 0,
        "SAFE: transient storage starts empty");
}

function SETUP_AC(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupAccounting(e);
}
