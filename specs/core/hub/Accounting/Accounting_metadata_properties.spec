import "setup/Accounting_metadata.spec";

// --- high_level ---

// AC-HL-10: setAccountMetadata writes only the named account's metadata; every other field reads the same.
rule hlAcSetAccountMetadataWritesOnlyItsAccountsMetadata(env e, AccountingHarness.PoolId p,
    AccountingHarness.AccountId a, bytes data, AccountingHarness.PoolId q, AccountingHarness.AccountId b, address who) {

    setupEnv(e);

    uint64 journalCounterBefore = _Accounting._poolJournalIdCounter[q];
    uint256 wardBefore = _Accounting.wards[who];
    mathint sessionStoresBefore = ghostAcSessionStores;
    uint128 debitBefore;
    uint128 creditBefore;
    bool debitNormalBefore;
    uint64 stampBefore;
    bytes metadataBefore;
    debitBefore, creditBefore, debitNormalBefore, stampBefore, metadataBefore = _Accounting.accounts(e, q, b);

    _Accounting.setAccountMetadata(e, p, a, data);

    uint128 debitAfter;
    uint128 creditAfter;
    bool debitNormalAfter;
    uint64 stampAfter;
    bytes metadataAfter;
    debitAfter, creditAfter, debitNormalAfter, stampAfter, metadataAfter = _Accounting.accounts(e, q, b);

    assert(debitAfter == debitBefore && creditAfter == creditBefore && debitNormalAfter == debitNormalBefore
            && stampAfter == stampBefore && _Accounting._poolJournalIdCounter[q] == journalCounterBefore
            && _Accounting.wards[who] == wardBefore && ghostAcSessionStores == sessionStoresBefore
            && ((q != p || b != a) => keccak256(metadataAfter) == keccak256(metadataBefore)),
        "a metadata write moves nothing but the named account's metadata");
}
