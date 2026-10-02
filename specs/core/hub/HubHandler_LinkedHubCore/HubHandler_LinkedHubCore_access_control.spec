import "HubHandler_LinkedHubCore_valid_state.spec";

// HH-AC-01: only an admin can grant or revoke admin rights on the hub handler.
rule acHhOnlyAWardMovesTheWardSet(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint userWardBefore = _HubHandler.wards[user];

    f(e, args);

    mathint userWardAfter = _HubHandler.wards[user];

    assert(userWardAfter != userWardBefore => senderWardBefore == 1,
        "only a ward can grant or revoke the handler's ward rights");
}

// HH-AC-02: only an admin can change which hub inbound messages are applied to.
rule acHhOnlyAWardMovesTheHubPointer(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    address hubBefore = _HubHandler.hub;

    f(e, args);

    address hubAfter = _HubHandler.hub;

    assert(hubAfter != hubBefore => senderWardBefore == 1, "only a ward can repoint the handler's hub");
}

// HH-AC-03: only an admin can change which holdings contract inbound asset reports update.
rule acHhOnlyAWardMovesTheHoldingsPointer(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    address holdingsBefore = _HubHandler.holdings;

    f(e, args);

    address holdingsAfter = _HubHandler.holdings;

    assert(holdingsAfter != holdingsBefore => senderWardBefore == 1, "only a ward can repoint the handler's holdings");
}

// HH-AC-04: only an admin can change the contract the hub handler sends messages through.
rule acHhOnlyAWardMovesTheSenderPointer(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    address messageSenderBefore = _HubHandler.sender;

    f(e, args);

    address messageSenderAfter = _HubHandler.sender;

    assert(messageSenderAfter != messageSenderBefore => senderWardBefore == 1,
        "only a ward can repoint the handler's message sender");
}

// HH-AC-05: only an admin can change which share class manager inbound share reports update.
rule acHhOnlyAWardMovesTheShareClassManagerPointer(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    address managerBefore = _HubHandler.shareClassManager;

    f(e, args);

    address managerAfter = _HubHandler.shareClassManager;

    assert(managerAfter != managerBefore => senderWardBefore == 1,
        "only a ward can repoint the handler's share class manager");
}

// HH-AC-06: only an admin can register an asset on the hub via the hub handler.
rule acHhOnlyAWardRegistersAnAsset(env e, method f, calldataarg args, mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    bool registeredBefore = ghostHrAssetRegistered[a];

    f(e, args);

    bool registeredAfter = ghostHrAssetRegistered[a];

    assert(registeredAfter != registeredBefore => senderWardBefore == 1,
        "only a handler ward can change whether an asset is registered");
}

// HH-AC-07: only an admin can set an asset's decimals via the hub handler.
rule acHhOnlyAWardMovesAnAssetDecimals(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint decimalsBefore = ghostHrAssetDecimals8[a];

    f(e, args);

    mathint decimalsAfter = ghostHrAssetDecimals8[a];

    assert(decimalsAfter != decimalsBefore => senderWardBefore == 1,
        "only a handler ward can change an asset's decimals");
}

// HH-AC-08: only an admin can record incoming assets on a holding via the hub handler.
rule acHhOnlyAWardMovesADepositHistory(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint increasedBefore = ghostHoIncreasedAmount256[a];

    f(e, args);

    mathint increasedAfter = ghostHoIncreasedAmount256[a];

    assert(increasedAfter != increasedBefore => senderWardBefore == 1,
        "only a handler ward can change a holding's deposit total");
}

// HH-AC-09: only an admin can record outgoing assets on a holding via the hub handler.
rule acHhOnlyAWardMovesAWithdrawalHistory(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint decreasedBefore = ghostHoDecreasedAmount256[a];

    f(e, args);

    mathint decreasedAfter = ghostHoDecreasedAmount256[a];

    assert(decreasedAfter != decreasedBefore => senderWardBefore == 1,
        "only a handler ward can change a holding's withdrawal total");
}

// HH-AC-10: only an admin can change a holding's value via the hub handler.
rule acHhOnlyAWardMovesACarriedValue(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint valueBefore = ghostHoAssetAmountValue128[a];

    f(e, args);

    mathint valueAfter = ghostHoAssetAmountValue128[a];

    assert(valueAfter != valueBefore => senderWardBefore == 1,
        "only a handler ward can change a holding's carrying value");
}

// HH-AC-11: only an admin can change the counts of holdings in deficit via the hub handler.
rule acHhOnlyAWardMovesTheDeficitCount(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint networkDeficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    f(e, args);

    mathint networkDeficitAfter = ghostHoNetworkDeficitCount32;
    mathint classDeficitAfter = ghostHoDeficitCount32;

    assert((networkDeficitAfter != networkDeficitBefore || classDeficitAfter != classDeficitBefore)
        => senderWardBefore == 1,
        "only a handler ward can change the class or network deficit count");
}

// HH-AC-12: only an admin can change whether a network is marked in sync, via the hub handler.
rule acHhOnlyAWardMovesASyncMarker(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    bool markerBefore = ghostHoIsSnapshot[cid];

    f(e, args);

    bool markerAfter = ghostHoIsSnapshot[cid];

    assert(markerAfter != markerBefore => senderWardBefore == 1, "only a handler ward can flip a network's sync flag");
}

// HH-AC-13: only an admin can change a network's snapshot sequence number via the hub handler.
rule acHhOnlyAWardMovesASnapshotNonce(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint nonceBefore = ghostHoSnapshotNonce64[cid];

    f(e, args);

    mathint nonceAfter = ghostHoSnapshotNonce64[cid];

    assert(nonceAfter != nonceBefore => senderWardBefore == 1,
        "only a handler ward can change a network's snapshot nonce");
}

// HH-AC-14: only an admin can change a network's issued share total via the hub handler.
rule acHhOnlyAWardMovesANetworkIssuedTotal(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint issuedBefore = ghostScIssuances256[cid];

    f(e, args);

    mathint issuedAfter = ghostScIssuances256[cid];

    assert(issuedAfter != issuedBefore => senderWardBefore == 1,
        "only a handler ward can change a network's issued shares");
}

// HH-AC-15: only an admin can change a network's revoked share total via the hub handler.
rule acHhOnlyAWardMovesANetworkRevokedTotal(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint revokedBefore = ghostScRevocations256[cid];

    f(e, args);

    mathint revokedAfter = ghostScRevocations256[cid];

    assert(revokedAfter != revokedBefore => senderWardBefore == 1,
        "only a handler ward can change a network's revoked shares");
}

// HH-AC-16: only an admin can change a share class's total supply via the hub handler.
rule acHhOnlyAWardMovesTheClassSupply(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint issuedBefore = ghostScTotalIssuances256;
    mathint revokedBefore = ghostScTotalRevocations256;

    f(e, args);

    mathint issuedAfter = ghostScTotalIssuances256;
    mathint revokedAfter = ghostScTotalRevocations256;

    assert((issuedAfter != issuedBefore || revokedAfter != revokedBefore) => senderWardBefore == 1,
        "only a handler ward can change the class's issued or revoked total");
}

// HH-AC-17: only an admin can debit a pool's accounting account via the hub handler.
rule acHhOnlyAWardMovesALedgerDebit(env e, method f, calldataarg args, mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint debitBefore = ghostAcTotalDebit128[a];

    f(e, args);

    mathint debitAfter = ghostAcTotalDebit128[a];

    assert(debitAfter != debitBefore => senderWardBefore == 1,
        "only a handler ward can change a ledger account's debit total");
}

// HH-AC-18: only an admin can credit a pool's accounting account via the hub handler.
rule acHhOnlyAWardMovesALedgerCredit(env e, method f, calldataarg args, mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint creditBefore = ghostAcTotalCredit128[a];

    f(e, args);

    mathint creditAfter = ghostAcTotalCredit128[a];

    assert(creditAfter != creditBefore => senderWardBefore == 1,
        "only a handler ward can change a ledger account's credit total");
}

// HH-AC-19: only an admin can book accounting journal entries via the hub handler.
rule acHhOnlyAWardMovesTheJournalCounter(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint counterBefore = ghostAcJournalIdCounter64;

    f(e, args);

    mathint counterAfter = ghostAcJournalIdCounter64;

    assert(counterAfter != counterBefore => senderWardBefore == 1,
        "only a handler ward can change the pool's journal counter");
}

// HH-AC-20: only an admin can make the hub handler forward an investor request.
rule acHhOnlyAWardForwardsAnInvestorRequest(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint forwardsBefore = ghostHmRequestCount;

    f(e, args);

    mathint forwardsAfter = ghostHmRequestCount;

    assert(forwardsAfter != forwardsBefore => senderWardBefore == 1,
        "only a handler ward can forward an investor request");
}

// HH-AC-21: only an admin can make the hub handler send a message to another network.
rule acHhOnlyAWardSendsAnOutboundMessage(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HH(f) } {

    setupHubHandlerLinkedHubCore(e);

    mathint senderWardBefore = _HubHandler.wards[e.msg.sender];
    mathint sendsBefore = ghostMsSendCount;

    f(e, args);

    mathint sendsAfter = ghostMsSendCount;

    assert(sendsAfter != sendsBefore => senderWardBefore == 1, "only a handler ward can send an outbound message");
}
