import "../setup/Hub_LinkedHubCore_base.spec";

function setupHubLinkedHubCoreValidState(env e) {
    setupHubLinkedHubCore(e);
    requireInvariant journalDebitsEqualCredits(e);
    requireInvariant holdingAccountIdsExist(e);
    requireInvariant initializedHoldingHasAccounts(e);
    requireInvariant initializedHoldingAssetRegistered(e);
    requireInvariant registeredPoolIsLocal(e);
    requireInvariant initializedHoldingImpliesShareClassExists(e);
    requireInvariant ledgerAccountImpliesRegisteredPool(e);
    assumeAbsentAccountIsEmpty();
    assumeNullAccountNeverCreated();
}

// HU-VS-01: a pool's total debits always equal its total credits.
invariant journalDebitsEqualCredits(env e)
    AC_TOTAL_DEBIT_SUM() == AC_TOTAL_CREDIT_SUM()
filtered { f -> !EXCLUDED_FUNCTION_HU(f) } { preserved with (env eFunc) {
    assumeAbsentAccountIsEmpty();
    SETUP_HU(e, eFunc);
} }

// HU-VS-02: every account a holding posts to exists in the pool's books.
invariant holdingAccountIdsExist(env e)
    forall uint128 a. forall uint8 k. ghostHoAccountId256[a][k] != 0
        => ghostAcLastUpdated64[ghostHoAccountId256[a][k]] != 0
filtered { f -> !EXCLUDED_FUNCTION_HU(f) } { preserved with (env eFunc) { SETUP_HU(e, eFunc); } }

// HU-VS-03: an opened holding always has all four of its accounts set.
invariant initializedHoldingHasAccounts(env e)
    forall uint128 a. ghostHoValuation[a] != 0
        => (ghostHoAccountId256[a][0] != 0 && ghostHoAccountId256[a][1] != 0
            && ghostHoAccountId256[a][2] != 0 && ghostHoAccountId256[a][3] != 0)
filtered { f -> !EXCLUDED_FUNCTION_HU(f) } { preserved with (env eFunc) {
    assumeNullAccountNeverCreated();
    SETUP_HU(e, eFunc);
} }

// HU-VS-04: a holding exists only for a registered asset.
invariant initializedHoldingAssetRegistered(env e)
    forall uint128 a. ghostHoValuation[a] != 0 => ghostHrAssetRegistered[a]
filtered { f -> !EXCLUDED_FUNCTION_HU(f) } { preserved with (env eFunc) { SETUP_HU(e, eFunc); } }

// HU-VS-05: an existing pool always belongs to this hub's own network.
invariant registeredPoolIsLocal(env e)
    ghostHrCurrency128 != 0 => ghostPoolA64 / 2^48 == ghostMsLocalCentrifugeId16
filtered { f -> !EXCLUDED_FUNCTION_HU(f) } { preserved with (env eFunc) { SETUP_HU(e, eFunc); } }

// HU-VS-06: a holding exists only on an existing share class.
invariant initializedHoldingImpliesShareClassExists(env e)
    forall uint128 a. ghostHoValuation[a] != 0 => ghostScShareClassIds
filtered { f -> !EXCLUDED_FUNCTION_HU(f) } { preserved with (env eFunc) { SETUP_HU(e, eFunc); } }

// HU-VS-07: an accounting account exists only in a created pool.
invariant ledgerAccountImpliesRegisteredPool(env e)
    forall mathint a. ghostAcLastUpdated64[a] != 0 => ghostHrCurrency128 != 0
filtered { f -> !EXCLUDED_FUNCTION_HU(f) } { preserved with (env eFunc) {
    assumeManagerImpliesPoolExists();
    SETUP_HU(e, eFunc);
} }
