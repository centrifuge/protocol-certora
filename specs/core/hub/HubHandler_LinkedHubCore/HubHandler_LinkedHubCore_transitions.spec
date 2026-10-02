import "HubHandler_LinkedHubCore_valid_state.spec";

// --- variable_transitions ---

// HH-VT-01: a network's report nonce advances by at most one per call.
rule vtHhSnapshotSequenceStepsByAtMostOne(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    f(e, args);

    mathint nonceAfter = ghostHoSnapshotNonce64[cid];

    assert(nonceAfter == nonceBefore || nonceAfter == nonceBefore + 1,
        "a network's snapshot nonce stays or steps up by one per call");
}

// HH-VT-02: a pool's journal entry number advances by at most one per call.
rule vtHhJournalSequenceStepsByAtMostOne(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint counterBefore = ghostAcJournalIdCounter64;

    f(e, args);

    mathint counterAfter = ghostAcJournalIdCounter64;

    assert(counterAfter == counterBefore || counterAfter == counterBefore + 1,
        "no call spends more than one journal id");
}

// HH-VT-03: an account's last-updated time, when it changes, is the current block time.
rule vtHhAccountStampRecordsTheCurrentBlock(env e, method f, calldataarg args, mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint blockTime = e.block.timestamp;
    mathint stampBefore = ghostAcLastUpdated64[a];

    f(e, args);

    mathint stampAfter = ghostAcLastUpdated64[a];

    assert(stampAfter != stampBefore => stampAfter == blockTime,
        "a ledger account's update stamp, if it moves, is the current time");
}

// HH-VT-04: a holding's cumulative inflow and outflow totals never decrease.
rule vtHhHoldingFlowHistoryNeverShrinks(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[a];
    mathint decreasedBefore = ghostHoDecreasedAmount256[a];

    f(e, args);

    mathint increasedAfter = ghostHoIncreasedAmount256[a];
    mathint decreasedAfter = ghostHoDecreasedAmount256[a];

    assert(increasedAfter >= increasedBefore, "a holding's deposit total never shrinks");
    assert(decreasedAfter >= decreasedBefore, "a holding's withdrawal total never shrinks");
}

// HH-VT-05: a network's cumulative issued and revoked share totals never decrease.
rule vtHhNetworkShareHistoryNeverShrinks(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint issuedBefore = ghostScIssuances256[cid];
    mathint revokedBefore = ghostScRevocations256[cid];

    f(e, args);

    mathint issuedAfter = ghostScIssuances256[cid];
    mathint revokedAfter = ghostScRevocations256[cid];

    assert(issuedAfter >= issuedBefore, "a network's issued share total never shrinks");
    assert(revokedAfter >= revokedBefore, "a network's revoked share total never shrinks");
}

// HH-VT-06: an account's cumulative debit and credit totals never decrease.
rule vtHhLedgerRowTotalsNeverShrink(env e, method f, calldataarg args, mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint debitBefore = ghostAcTotalDebit128[a];
    mathint creditBefore = ghostAcTotalCredit128[a];

    f(e, args);

    mathint debitAfter = ghostAcTotalDebit128[a];
    mathint creditAfter = ghostAcTotalCredit128[a];

    assert(debitAfter >= debitBefore, "a ledger account's debit total never shrinks");
    assert(creditAfter >= creditBefore, "a ledger account's credit total never shrinks");
}

// HH-VT-07: only share and asset reports send the snapshot hook a sync notice, at most once.
rule vtHhSnapshotHookHearsOnlyAReport(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint syncsBefore = ghostHookOnSyncCount;

    f(e, args);

    assert(ghostHookOnSyncCount - syncsBefore <= 1
        && (ghostHookOnSyncCount != syncsBefore
            => (f.selector == sig:_HubHandler.updateShares(uint16,HubHandler.PoolId,HubHandler.ShareClassId,uint128,bool,bool,uint64).selector
                || f.selector == sig:_HubHandler.updateAssets(uint16,HubHandler.PoolId,HubHandler.ShareClassId,HubHandler.AssetId,uint128,bool,bool,uint64).selector)),
        "the snapshot hook fires at most once, only on share or asset reports");
}

// --- state_transitions ---

// HH-ST-01: an initialized holding's value change is booked in full as a debit and a credit.
rule stHhReportedAssetMoveIsBookedExactly(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCoreValidState(e);

    address valuationBefore = ghostHoValuation[a];
    mathint valueBefore = ghostHoAssetAmountValue128[a];
    mathint debitBefore = AC_TOTAL_DEBIT_SUM();
    mathint creditBefore = AC_TOTAL_CREDIT_SUM();

    f(e, args);

    mathint valueDelta = ghostHoAssetAmountValue128[a] - valueBefore;
    mathint booked = valueDelta > 0 ? valueDelta : -valueDelta;

    assert(valuationBefore != 0 && valueDelta != 0
        => (AC_TOTAL_DEBIT_SUM() - debitBefore == booked && AC_TOTAL_CREDIT_SUM() - creditBefore == booked),
        "both ledger sides take the full value change of an opened holding");
}

// HH-ST-02: a share class's total supply changes by exactly the net change across networks.
rule stHhShareLedgerMovesWithItsNetworkLegs(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint totalBefore = SC_TOTAL_ISSUANCE();
    mathint netBefore = SC_NET_ISSUANCE_SUM();

    f(e, args);

    assert(SC_TOTAL_ISSUANCE() - totalBefore == SC_NET_ISSUANCE_SUM() - netBefore,
        "the class supply moves by exactly the net of its network legs");
}

// HH-ST-03: a network's snapshot mark changes only when its report nonce advances by one.
rule stHhSnapshotFlagCostsANonce(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool flagBefore = ghostHoIsSnapshot[cid];
    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    f(e, args);

    assert(ghostHoIsSnapshot[cid] != flagBefore => ghostHoSnapshotNonce64[cid] == nonceBefore + 1,
        "a network's sync flag flips only with a one-step nonce advance");
}

// HH-ST-04: the network's shortfall count follows the number of holdings in shortfall.
rule stHhNetworkDeficitCountFollowsTheShortRows(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint countBefore = ghostHoNetworkDeficitCount32;
    mathint shortBefore = HO_DEFICIT_CARDINALITY();

    f(e, args);

    assert(ghostHoNetworkDeficitCount32 - countBefore == HO_DEFICIT_CARDINALITY() - shortBefore,
        "the network deficit count moves exactly as the short holdings do");
}

// HH-ST-05: a share class's shortfall count follows the number of its holdings in shortfall.
rule stHhClassDeficitCountFollowsTheShortRows(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint countBefore = ghostHoDeficitCount32;
    mathint shortBefore = HO_DEFICIT_CARDINALITY();

    f(e, args);

    assert(ghostHoDeficitCount32 - countBefore == HO_DEFICIT_CARDINALITY() - shortBefore,
        "the class deficit count moves exactly as the short holdings do");
}

// HH-ST-06: the count of networks with a negative share balance follows their actual number.
rule stHhNegativeNetworkCountFollowsTheShortNetworks(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint countBefore = ghostScNegativeNetworkCount32;
    mathint shortBefore = SC_NEGATIVE_NETWORK_CARDINALITY();

    f(e, args);

    assert(ghostScNegativeNetworkCount32 - countBefore == SC_NEGATIVE_NETWORK_CARDINALITY() - shortBefore,
        "the negative network count moves exactly with the overdrawn networks");
}
