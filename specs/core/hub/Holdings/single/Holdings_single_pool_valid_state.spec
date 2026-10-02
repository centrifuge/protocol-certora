import "../setup/Holdings_single_pool.spec";
import "../../HubRegistry/setup/HubRegistry_cvl.spec";

function setupHoldingsValidState(env e) {
    setupHoldings(e);
    requireInvariant snapshotHookImpliesPoolExists(e);
    requireInvariant networkDeficitCountMatchesTheShortRows(e);
    requireInvariant deficitCountMatchesTheClassShortRows(e);
    requireInvariant uninitializedHoldingHasNoValue(e);
    requireInvariant emptyHoldingCarriesNoValue(e);
    requireInvariant snapshotFlagImpliesAStartedNonce(e);
    requireInvariant accountIdImpliesInitialized(e);
}

// HO-VS-01: a snapshot hook is attached only to a pool the hub registry knows.
invariant snapshotHookImpliesPoolExists(env e)
    ghostHoSnapshotHook != 0 => ghostHrCurrency128 != 0
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO(e, eFunc); } }

// HO-VS-02: with one network, a pool's deficit count equals its holdings in deficit.
invariant networkDeficitCountMatchesTheShortRows(env e)
    ghostHoNetworkDeficitCount32 == HO_DEFICIT_CARDINALITY()
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO(e, eFunc); } }

// HO-VS-03: a holding that was never opened has no value.
invariant uninitializedHoldingHasNoValue(env e)
    forall uint128 a. ghostHoValuation[a] == 0 => ghostHoAssetAmountValue128[a] == 0
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO(e, eFunc); } }

// HO-VS-04: a holding with nothing left in it has zero value.
// TRUSTED: the valuation prices a zero amount at zero value.
invariant emptyHoldingCarriesNoValue(env e)
    forall uint128 a. ghostHoIncreasedAmount256[a] <= ghostHoDecreasedAmount256[a]
        => ghostHoAssetAmountValue128[a] == 0
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO(e, eFunc); } }

// HO-VS-05: a network marked in sync has had at least one sync update.
invariant snapshotFlagImpliesAStartedNonce(env e)
    forall uint16 cid. ghostHoIsSnapshot[cid] => ghostHoSnapshotNonce64[cid] >= 1
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO(e, eFunc); } }

// HO-VS-06: journal accounts are set only on holdings that have been opened.
invariant accountIdImpliesInitialized(env e)
    forall uint128 a. forall uint8 k. ghostHoAccountId256[a][k] != 0 => ghostHoValuation[a] != 0
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO(e, eFunc); } }

// HO-VS-08: with one network, a share class's deficit count equals its holdings in deficit.
invariant deficitCountMatchesTheClassShortRows(env e)
    ghostHoDeficitCount32 == HO_DEFICIT_CARDINALITY()
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO(e, eFunc); } }
