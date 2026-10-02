import "../setup/Accounting_single_pool.spec";

function setupAccountingValidState(env e) {
    setupAccounting(e);
    requireInvariant absentAccountIsEmpty(e);
    requireInvariant nullAccountNeverCreated(e);
    requireInvariant lastUpdatedBetweenEnvFloorAndBlock(e);
    requireInvariant postedHistoryImpliesAnIssuedJournalId(e);
}

// AC-VS-01: a never-created account has no recorded debits or credits.
invariant absentAccountIsEmpty(env e)
    forall mathint a. ghostAcLastUpdated64[a] == 0
        => (ghostAcTotalDebit128[a] == 0 && ghostAcTotalCredit128[a] == 0 && !ghostAcIsDebitNormal[a])
filtered { f -> !EXCLUDED_FUNCTION_AC(f) } { preserved with (env eFunc) { SETUP_AC(e, eFunc); } }

// AC-VS-02: the empty account id never exists, so no entry can be posted to it.
invariant nullAccountNeverCreated(env e)
    ghostAcLastUpdated64[0] == 0
filtered { f -> !EXCLUDED_FUNCTION_AC(f) } { preserved with (env eFunc) { SETUP_AC(e, eFunc); } }

// AC-VS-03: an account's last update time is never in the future.
invariant lastUpdatedBetweenEnvFloorAndBlock(env e)
    forall mathint a. ghostAcLastUpdated64[a] != 0
        => (ghostAcLastUpdated64[a] >= MIN_BLOCK_TIMESTAMP()
            && ghostAcLastUpdated64[a] <= e.block.timestamp)
filtered { f -> !EXCLUDED_FUNCTION_AC(f) } { preserved with (env eFunc) { SETUP_AC(e, eFunc); } }

// AC-VS-04: an account has postings only after at least one journal id was issued.
invariant postedHistoryImpliesAnIssuedJournalId(env e)
    forall mathint a. (ghostAcTotalDebit128[a] != 0 || ghostAcTotalCredit128[a] != 0)
        => ghostAcJournalIdCounter64 >= 1
filtered { f -> !EXCLUDED_FUNCTION_AC(f) } { preserved with (env eFunc) { SETUP_AC(e, eFunc); } }

// AC-VS-05: no journal id a pool has issued is above the latest id the pool has minted.
invariant issuedJournalIdsLieAtOrBelowTheHighWaterMark(env e)
    forall mathint id. ghostAcIssuedJournalId[id]
        => id <= ghostPoolA64 * 2^128 + ghostAcJournalIdCounter64
filtered { f -> !EXCLUDED_FUNCTION_AC(f) } { preserved with (env eFunc) { SETUP_AC(e, eFunc); } }
