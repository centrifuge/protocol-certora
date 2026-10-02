// Accounting, multi-pool lane. Setup: rows mirrored per pool for cross-pool checks.

// Own setup: rows keyed by pool over two pools; single_pool hooks the same account fields pinned to one pool.

import "Accounting_base.spec";
import "../../../../shared/domains/multi_pool.spec";

definition AC_POOL_PAIR(uint64 p, uint64 q) returns bool =
    (p == ghostPoolA64 && q == ghostPoolB64) || (p == ghostPoolB64 && q == ghostPoolA64);

persistent ghost mapping(uint64 => mapping(mathint => mathint)) ghostAcPoolTotalDebit128 {
    init_state axiom forall uint64 p. forall mathint a. ghostAcPoolTotalDebit128[p][a] == 0;
    axiom forall uint64 p. forall mathint a.
        ghostAcPoolTotalDebit128[p][a] >= 0 && ghostAcPoolTotalDebit128[p][a] <= max_uint128;
    axiom forall uint64 p. forall mathint a.
        (!VALID_POOL(p) || !VALID_ACCOUNT(a)) => ghostAcPoolTotalDebit128[p][a] == 0;
}

hook Sload uint128 val _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].totalDebit {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    require(ghostAcPoolTotalDebit128[p][a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].totalDebit uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    ghostAcPoolTotalDebit128[p][a] = val;
}

persistent ghost mapping(uint64 => mapping(mathint => mathint)) ghostAcPoolTotalCredit128 {
    init_state axiom forall uint64 p. forall mathint a. ghostAcPoolTotalCredit128[p][a] == 0;
    axiom forall uint64 p. forall mathint a.
        ghostAcPoolTotalCredit128[p][a] >= 0 && ghostAcPoolTotalCredit128[p][a] <= max_uint128;
    axiom forall uint64 p. forall mathint a.
        (!VALID_POOL(p) || !VALID_ACCOUNT(a)) => ghostAcPoolTotalCredit128[p][a] == 0;
}

hook Sload uint128 val _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].totalCredit {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    require(ghostAcPoolTotalCredit128[p][a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].totalCredit uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    ghostAcPoolTotalCredit128[p][a] = val;
}

persistent ghost mapping(uint64 => mapping(mathint => bool)) ghostAcPoolIsDebitNormal {
    init_state axiom forall uint64 p. forall mathint a. !ghostAcPoolIsDebitNormal[p][a];
    axiom forall uint64 p. forall mathint a.
        (!VALID_POOL(p) || !VALID_ACCOUNT(a)) => !ghostAcPoolIsDebitNormal[p][a];
}

hook Sload bool val _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].isDebitNormal {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    require(ghostAcPoolIsDebitNormal[p][a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].isDebitNormal bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    ghostAcPoolIsDebitNormal[p][a] = val;
}

persistent ghost mapping(uint64 => mapping(mathint => mathint)) ghostAcPoolLastUpdated64 {
    init_state axiom forall uint64 p. forall mathint a. ghostAcPoolLastUpdated64[p][a] == 0;
    axiom forall uint64 p. forall mathint a.
        ghostAcPoolLastUpdated64[p][a] >= 0 && ghostAcPoolLastUpdated64[p][a] <= max_uint64;
    axiom forall uint64 p. forall mathint a.
        (!VALID_POOL(p) || !VALID_ACCOUNT(a)) => ghostAcPoolLastUpdated64[p][a] == 0;
}

hook Sload uint64 val _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].lastUpdated {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    require(ghostAcPoolLastUpdated64[p][a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting.accounts[KEY AccountingHarness.PoolId p][KEY AccountingHarness.AccountId a].lastUpdated uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_ACCOUNT(a), "UNSAFE: at most three accounts per pool");
    ghostAcPoolLastUpdated64[p][a] = val;
}

methods {
    function TransientStorageLib.tloadUint256(bytes32 slot) internal returns (uint256) => accountingTloadCVL(slot);
    function TransientStorageLib.tstore(bytes32 slot, uint256 value) internal => accountingTstoreCVL(slot, value);
}

// SAFE: journal kept per slot, so the pool key derivation is tested.
persistent ghost mapping(bytes32 => mathint) ghostAcTransientSlot256 {
    init_state axiom forall bytes32 s. ghostAcTransientSlot256[s] == 0;
    axiom forall bytes32 s. ghostAcTransientSlot256[s] >= 0 && ghostAcTransientSlot256[s] <= max_uint256;
}

persistent ghost mathint ghostAcFiledJournalId256;

function accountingTloadCVL(bytes32 slot) returns uint256 {
    ghostAcFiledJournalId256 = ghostAcTransientSlot256[slot];
    return require_uint256(ghostAcTransientSlot256[slot]);
}

function accountingTstoreCVL(bytes32 slot, uint256 value) {
    ghostAcTransientSlot256[slot] = value;
}

// Any state inside a transaction: no transient pins.
function setupAccountingMidTransaction(env e) {
    setupEnv(e);
    setupPoolMode();
    setupAccountDomain();
}

function setupJournalRegion() {
    require(forall bytes32 s. ghostAcTransientSlot256[s] == 0, "SAFE: transient storage starts empty");
}

persistent ghost mapping(uint64 => mathint) ghostAcPoolJournalIdCounter64 {
    init_state axiom forall uint64 p. ghostAcPoolJournalIdCounter64[p] == 0;
    axiom forall uint64 p.
        ghostAcPoolJournalIdCounter64[p] >= 0 && ghostAcPoolJournalIdCounter64[p] <= max_uint64;
    axiom forall uint64 p. !VALID_POOL(p) => ghostAcPoolJournalIdCounter64[p] == 0;
}

hook Sload uint64 val _Accounting._poolJournalIdCounter[KEY AccountingHarness.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostAcPoolJournalIdCounter64[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Accounting._poolJournalIdCounter[KEY AccountingHarness.PoolId p] uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostAcPoolJournalIdCounter64[p] = val;
}

function SETUP_MULTI_AC(env e) {
    setupAccounting(e);
}
