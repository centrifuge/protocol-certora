import "Hub_LinkedHubCore_valid_state.spec";

// --- variable_transitions ---

// HU-VT-01: a pool's policy install counter grows by at most one per call, never going back.
rule vtHuAuthorizationTenureStepsByAtMostOne(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);

    mathint nonceBefore = ghostHrPolicyNonce64;

    f(e, args);

    mathint nonceAfter = ghostHrPolicyNonce64;

    assert(nonceAfter == nonceBefore || nonceAfter == nonceBefore + 1,
        "the policy nonce stays or steps up by exactly one");
}

// HU-VT-02: a pool's journal number advances by at most one per call and never goes back.
rule vtHuJournalSequenceStepsByAtMostOne(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);

    mathint counterBefore = ghostAcJournalIdCounter64;

    f(e, args);

    mathint counterAfter = ghostAcJournalIdCounter64;

    assert(counterAfter == counterBefore || counterAfter == counterBefore + 1,
        "the journal counter stays or steps up by exactly one");
}

// HU-VT-03: a pool's share class count grows by at most one per call and never shrinks.
rule vtHuShareClassSequenceStepsByAtMostOne(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);

    mathint countBefore = ghostScShareClassCount32;

    f(e, args);

    mathint countAfter = ghostScShareClassCount32;

    assert(countAfter == countBefore || countAfter == countBefore + 1,
        "the share class count stays or steps up by exactly one");
}

// HU-VT-04: a holding's ledger accounts change only when it is opened or an account is reassigned.
rule vtHuAccountWiringMovesOnlyThroughWiringEntries(env e, method f, calldataarg args, uint128 a, uint8 k)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    mathint accountBefore = ghostHoAccountId256[a][k];

    f(e, args);

    mathint accountAfter = ghostHoAccountId256[a][k];

    assert(accountAfter == accountBefore || WIRING_FUNCTION_HU(f),
        "a holding's ledger accounts change only by opening or rewiring it");
}

// HU-VT-05: a holding's valuation changes only when it is opened or its valuation is updated.
rule vtHuValuationMovesOnlyThroughItsInstallers(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    address valuationBefore = ghostHoValuation[a];

    f(e, args);

    address valuationAfter = ghostHoValuation[a];

    assert(valuationAfter == valuationBefore || VALUATION_FUNCTION_HU(f),
        "a holding's price source changes only by opening it or a source swap");
}

// HU-VT-06: a pool's snapshot hook changes only through its dedicated setter.
rule vtHuSnapshotHookMovesOnlyThroughItsSetter(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    address hookBefore = ghostHoSnapshotHook;

    f(e, args);

    address hookAfter = ghostHoSnapshotHook;

    assert(hookAfter == hookBefore
        || f.selector == sig:_Hub.setSnapshotHook(HubHarness.PoolId,address).selector,
        "any call but the hook setter leaves the snapshot hook alone");
}

// HU-VT-07: only a hub revaluation notifies the snapshot hook, at most once per call.
rule vtHuSnapshotHookHearsOnlyARevaluation(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    mathint syncsBefore = ghostHookOnSyncCount;

    f(e, args);

    assert(ghostHookOnSyncCount - syncsBefore <= 1
        && (ghostHookOnSyncCount != syncsBefore
            => f.selector == sig:_Hub.updateHoldingValue(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId).selector),
        "a call pings the snapshot hook at most once, and only when revaluing");
}

// --- state_transitions ---

// HU-ST-01: changing a pool's policy voids the authorizations scheduled under the old one.
rule stHuPolicySwapAdvancesTheAuthorizationNamespace(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    address policyBefore = ghostHrPolicy;
    mathint nonceBefore = ghostHrPolicyNonce64;

    f(e, args);

    assert(ghostHrPolicy != policyBefore => ghostHrPolicyNonce64 == nonceBefore + 1,
        "a policy change advances the policy nonce by exactly one");
}

// HU-ST-02: any change to a pool's books is filed under one new journal id.
rule stHuLedgerMoveIsFiledUnderAFreshJournal(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    mathint debitBefore = AC_TOTAL_DEBIT_SUM();
    mathint creditBefore = AC_TOTAL_CREDIT_SUM();
    mathint counterBefore = ghostAcJournalIdCounter64;

    f(e, args);

    bool posted = AC_TOTAL_DEBIT_SUM() != debitBefore || AC_TOTAL_CREDIT_SUM() != creditBefore;

    assert(posted => (ghostAcJournalIdCounter64 == counterBefore + 1 && ghostAcJournalId256 != 0),
        "a call that moves the books opens exactly one new journal");
}

// HU-ST-03: a change in a holding's value is booked at its exact size on both sides.
rule stHuValueMoveIsBookedExactly(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    mathint valueBefore = ghostHoAssetAmountValue128[a];
    mathint debitBefore = AC_TOTAL_DEBIT_SUM();
    mathint creditBefore = AC_TOTAL_CREDIT_SUM();

    f(e, args);

    mathint valueDelta = ghostHoAssetAmountValue128[a] - valueBefore;
    mathint booked = valueDelta > 0 ? valueDelta : -valueDelta;

    assert(valueDelta != 0
        => (AC_TOTAL_DEBIT_SUM() - debitBefore == booked && AC_TOTAL_CREDIT_SUM() - creditBefore == booked),
        "a change in a holding's value is booked exactly, debit and credit");
}

// HU-ST-04: no call changes both an opened holding's price source and one of its accounts.
rule stHuPriceSourceSwapNeverRewiresTheAccounts(env e, method f, calldataarg args, uint128 a, uint8 k)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    address valuationBefore = ghostHoValuation[a];
    mathint accountBefore = ghostHoAccountId256[a][k];

    f(e, args);

    assert(valuationBefore != 0
        => (ghostHoValuation[a] == valuationBefore || ghostHoAccountId256[a][k] == accountBefore),
        "an opened holding never swaps its price source and an account at once");
}

// HU-ST-05: no hub call leaves accounting unlocked.
rule stHuEveryHubCallLeavesTheLedgerLocked(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    f(e, args);

    assert(ghostAcCurrentPoolT == 0, "no journal is still open when a hub call returns");
}

// HU-ST-06: a holding's value change moves its own account's net equally when no other slot shares it.
rule stHuProtocolValueMovesLandOnTheHoldingsOwnRow(env e, method f, calldataarg args, uint128 a, mathint own)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);
    assumeUninitializedHoldingHasNoValue(a);

    mathint valueBefore = ghostHoAssetAmountValue128[a];
    mathint netBefore = ghostAcTotalDebit128[own] - ghostAcTotalCredit128[own];

    f(e, args);

    mathint valueDelta = ghostHoAssetAmountValue128[a] - valueBefore;
    mathint netDelta = ghostAcTotalDebit128[own] - ghostAcTotalCredit128[own] - netBefore;
    bool ownRowApart = own == ghostHoAccountId256[a][AMOUNT_DEBIT_KIND_HU_CVL()]
        && own != ghostHoAccountId256[a][AMOUNT_CREDIT_KIND_HU_CVL()]
        && own != ghostHoAccountId256[a][VALUE_INCREASE_KIND_HU_CVL()]
        && own != ghostHoAccountId256[a][VALUE_DECREASE_KIND_HU_CVL()];

    assert((valueDelta != 0 && ownRowApart) => netDelta == valueDelta,
        "the holding's value and its unshared account's net move together");
}

// HU-ST-08: a pool's total debits and credits change only through journal postings.
rule stHuLedgerTotalsMoveOnlyThroughJournalling(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    mathint debitBefore = AC_TOTAL_DEBIT_SUM();
    mathint creditBefore = AC_TOTAL_CREDIT_SUM();

    f(e, args);

    mathint debitAfter = AC_TOTAL_DEBIT_SUM();
    mathint creditAfter = AC_TOTAL_CREDIT_SUM();

    assert((debitAfter == debitBefore && creditAfter == creditBefore) || JOURNALLING_FUNCTION_HU(f),
        "the ledger totals move only through the five journalling entries");
}

// HU-ST-09: no hub call changes a share class's issued or revoked shares on any network.
rule stHuShareLedgerIsNeverMovedByTheHub(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    mathint issuedBefore = ghostScIssuances256[cid];
    mathint revokedBefore = ghostScRevocations256[cid];
    mathint totalIssuedBefore = ghostScTotalIssuances256;
    mathint totalRevokedBefore = ghostScTotalRevocations256;
    mathint shortNetworksBefore = ghostScNegativeNetworkCount32;

    f(e, args);

    assert(ghostScIssuances256[cid] == issuedBefore && ghostScRevocations256[cid] == revokedBefore
        && ghostScTotalIssuances256 == totalIssuedBefore && ghostScTotalRevocations256 == totalRevokedBefore
        && ghostScNegativeNetworkCount32 == shortNetworksBefore,
        "no hub call moves issuance, revocation or short-network counts");
}

// HU-ST-10: no hub call moves a share class or a network into or out of deficit.
rule stHuDeficitGateIsNeverMovedByTheHub(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    mathint classDeficitBefore = ghostHoDeficitCount32;
    mathint networkDeficitBefore = ghostHoNetworkDeficitCount32;

    f(e, args);

    assert(ghostHoDeficitCount32 == classDeficitBefore && ghostHoNetworkDeficitCount32 == networkDeficitBefore,
        "hub calls leave the class and network deficit counts as they were");
}

// HU-VT-08: a hub call that sends a message passes on the attached ETH, or none inside a batch.
rule vtHuEveryOutboundSendCarriesTheAttachedValue(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreAnyTransient(e);

    bool inBatch = huInBatchCVL(e);
    mathint sentBefore = ghostMsSendCount;

    f(e, args);

    assert(ghostMsSendCount != sentBefore => ghostMsLastValue256 == (inBatch ? 0 : e.msg.value),
        "a sent message carries exactly the caller's ETH, or none when batched");
}
