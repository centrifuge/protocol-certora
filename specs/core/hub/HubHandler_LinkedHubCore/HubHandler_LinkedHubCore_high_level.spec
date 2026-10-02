// HubHandler, linked hub core lane. High level: conservation, forwarding and isolation.

import "HubHandler_LinkedHubCore_valid_state.spec";

// HH-HL-01: moving shares between networks leaves the share class's total supply unchanged.
rule hlHhTransferConservesTheClassTotal(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint totalBefore = SC_TOTAL_ISSUANCE();

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint totalAfter = SC_TOTAL_ISSUANCE();

    assert(totalAfter == totalBefore, "a cross-network transfer leaves the class supply unchanged");
}

// HH-HL-02: a transfer revokes on the origin network exactly the amount its message sends.
rule hlHhTransferDebitsOriginByTheSentAmount(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint revokedBefore = ghostScRevocations256[originCid];

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint revokedDelta = ghostScRevocations256[originCid] - revokedBefore;
    mathint sentAmount = ghostMsExecuteTransferAmount128;

    assert(revokedDelta == sentAmount, "the origin network's revocations rise by exactly the amount sent");
}

// HH-HL-03: a transfer issues on the target network exactly the amount its message sends.
rule hlHhTransferSendsTheAmountItMints(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint issuedBefore = ghostScIssuances256[targetCid];

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint issuedDelta = ghostScIssuances256[targetCid] - issuedBefore;
    mathint sentAmount = ghostMsExecuteTransferAmount128;

    assert(issuedDelta == sentAmount, "the target network's issuance rises by exactly the amount sent");
}

// HH-HL-04: a transfer's message states the network the shares left.
rule hlHhTransferKeepsTheOriginNetwork(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint sentOrigin = ghostMsExecuteTransferOriginCid16;

    assert(sentOrigin == originCid, "the transfer message names the origin network");
}

// HH-HL-05: a transfer's message is addressed to the requested target network.
rule hlHhTransferKeepsTheTargetNetwork(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint sentTarget = ghostMsExecuteTransferTargetCid16;

    assert(sentTarget == targetCid, "the outbound transfer goes to the network the caller picked");
}

// HH-HL-06: with no bridging hook, a transfer keeps the receiver the caller requested.
rule hlHhHooklessTransferKeepsTheReceiver(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    bytes32 sentReceiver = ghostMsExecuteTransferReceiver;

    assert(sentReceiver == receiver, "a hookless transfer sends the receiver unchanged");
}

// HH-HL-07: with no bridging hook, a transfer sends the amount the caller requested.
rule hlHhHooklessTransferKeepsTheAmount(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint sentAmount = ghostMsExecuteTransferAmount128;

    assert(sentAmount == amount, "a hookless transfer sends the amount unchanged");
}

// HH-HL-08: with no bridging hook, the transfer keeps the caller's refund address.
rule hlHhHooklessTransferKeepsTheRefund(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    address sentRefund = ghostMsLastRefund;

    assert(sentRefund == refund, "without a hook, refunds still go where the caller asked");
}

// HH-HL-09: one transfer emits exactly one outbound message.
rule hlHhTransferSendsExactlyOneMessage(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint sendsBefore = ghostMsSendCount;

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint sendsAfter = ghostMsSendCount;

    assert(sendsAfter == sendsBefore + 1, "the outbound message count grows by one per transfer");
}

// HH-HL-10: the message a share transfer sends is an ExecuteTransferShares message.
rule hlHhTransferSendsAnExecuteTransfer(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint sentKind = ghostMsLastKind;

    assert(sentKind == MS_EXECUTE_TRANSFER_SHARES(), "transfers go out with the execute-transfer-shares kind");
}

// HH-HL-11: a spoke's asset report adds its full amount to its incoming or outgoing total.
rule hlHhAssetReportLandsGrossOnItsSide(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isIncrease,
    bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    mathint decreasedBefore = ghostHoDecreasedAmount256[assetId];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, isIncrease, isSnapshot, nonce);

    mathint reportedDelta = isIncrease
        ? ghostHoIncreasedAmount256[assetId] - increasedBefore
        : ghostHoDecreasedAmount256[assetId] - decreasedBefore;

    assert(reportedDelta == amount, "an asset report raises its side's gross total by exactly the amount");
}

// HH-HL-12: an asset inflow report never changes the outflow total, and vice versa.
rule hlHhAssetReportLeavesTheOppositeSideAlone(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isIncrease,
    bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    mathint decreasedBefore = ghostHoDecreasedAmount256[assetId];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, isIncrease, isSnapshot, nonce);

    mathint oppositeDelta = isIncrease
        ? ghostHoDecreasedAmount256[assetId] - decreasedBefore
        : ghostHoIncreasedAmount256[assetId] - increasedBefore;

    assert(oppositeDelta == 0, "an asset report leaves the opposite side's total unchanged");
}

// HH-HL-13: one asset's report cannot change another asset's incoming total.
rule hlHhAssetReportLeavesOtherIncreasesAlone(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isIncrease,
    bool isSnapshot, uint64 nonce, uint128 b) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(b != assetId, "SCOPE: a second asset, not the reported one");

    mathint increasedBefore = ghostHoIncreasedAmount256[b];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, isIncrease, isSnapshot, nonce);

    mathint increasedAfter = ghostHoIncreasedAmount256[b];

    assert(increasedAfter == increasedBefore, "an asset report leaves every other asset's deposit total alone");
}

// HH-HL-14: one asset's report cannot change another asset's outgoing total.
rule hlHhAssetReportLeavesOtherDecreasesAlone(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isIncrease,
    bool isSnapshot, uint64 nonce, uint128 b) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(b != assetId, "SCOPE: a second asset, not the reported one");

    mathint decreasedBefore = ghostHoDecreasedAmount256[b];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, isIncrease, isSnapshot, nonce);

    mathint decreasedAfter = ghostHoDecreasedAmount256[b];

    assert(decreasedAfter == decreasedBefore, "an asset report leaves every other asset's withdrawal total alone");
}

// HH-HL-15: one asset's report cannot revalue another asset's holding.
rule hlHhAssetReportLeavesOtherValuesAlone(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isIncrease,
    bool isSnapshot, uint64 nonce, uint128 b) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(b != assetId, "SCOPE: a second asset, not the reported one");

    mathint valueBefore = ghostHoAssetAmountValue128[b];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, isIncrease, isSnapshot, nonce);

    mathint valueAfter = ghostHoAssetAmountValue128[b];

    assert(valueAfter == valueBefore, "an asset report leaves every other holding's value alone");
}

// HH-HL-16: a network's share report adds its full amount to its issued or revoked total.
rule hlHhShareReportLandsOnItsCounter(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, uint128 amount, bool isIssuance, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint issuedBefore = ghostScIssuances256[centrifugeId];
    mathint revokedBefore = ghostScRevocations256[centrifugeId];

    _HubHandler.updateShares(e, centrifugeId, poolId, scId, amount, isIssuance, isSnapshot, nonce);

    mathint reportedDelta = isIssuance
        ? ghostScIssuances256[centrifugeId] - issuedBefore
        : ghostScRevocations256[centrifugeId] - revokedBefore;

    assert(reportedDelta == amount, "a share report raises its side's network total by exactly the amount");
}

// HH-HL-17: a share report changes the class supply by the reported amount and direction.
rule hlHhShareReportMovesTheClassTotalInStep(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, uint128 amount, bool isIssuance, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint totalBefore = SC_TOTAL_ISSUANCE();

    _HubHandler.updateShares(e, centrifugeId, poolId, scId, amount, isIssuance, isSnapshot, nonce);

    mathint totalDelta = SC_TOTAL_ISSUANCE() - totalBefore;

    assert(totalDelta == (isIssuance ? to_mathint(amount) : -to_mathint(amount)),
        "an issued amount adds to class supply, a revoked amount subtracts");
}

// HH-HL-18: an investor request is forwarded once and only once.
rule hlHhRequestForwardsExactlyOnce(env e, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, bytes payload) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint forwardsBefore = ghostHmRequestCount;

    _HubHandler.request(e, poolId, scId, assetId, payload);

    mathint forwardsAfter = ghostHmRequestCount;

    assert(forwardsAfter == forwardsBefore + 1, "a request is forwarded exactly once");
}

// HH-HL-19: an investor request goes to the pool's request manager for its asset's network.
rule hlHhRequestReachesTheRegisteredManager(env e, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, bytes payload) {

    setupHubHandlerLinkedHubCoreValidState(e);

    address registeredBefore = ghostHrHubRequestManager[assert_uint16(ASSET_CENTRIFUGE_ID_HH_CVL(assetId))];

    _HubHandler.request(e, poolId, scId, assetId, payload);

    address calleeAfter = ghostHmRequestManager;

    assert(calleeAfter == registeredBefore, "a request reaches the manager registered for the asset's network");
}

// HH-HL-20: an investor request arrives at the manager under the pool it was sent for.
rule hlHhRequestForwardsThePool(env e, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, bytes payload) {

    setupHubHandlerLinkedHubCoreValidState(e);

    _HubHandler.request(e, poolId, scId, assetId, payload);

    mathint poolAfter = ghostHmRequestPool64;

    assert(poolAfter == poolId, "a request is forwarded under the pool it names");
}

// HH-HL-21: an investor request arrives at the manager under the share class it was sent for.
rule hlHhRequestForwardsTheShareClass(env e, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, bytes payload) {

    setupHubHandlerLinkedHubCoreValidState(e);

    _HubHandler.request(e, poolId, scId, assetId, payload);

    bytes16 scIdAfter = ghostHmRequestScId;

    assert(scIdAfter == scId, "a request is forwarded under the share class it names");
}

// HH-HL-22: an investor request arrives at the manager under the asset it was sent for.
rule hlHhRequestForwardsTheAsset(env e, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, bytes payload) {

    setupHubHandlerLinkedHubCoreValidState(e);

    _HubHandler.request(e, poolId, scId, assetId, payload);

    mathint assetIdAfter = ghostHmRequestAssetId128;

    assert(assetIdAfter == assetId, "a request is forwarded under the asset it names");
}

// HH-HL-23: an investor request reaches its manager with the payload unaltered.
rule hlHhRequestForwardsThePayload(env e, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, bytes payload) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bytes32 payloadHash = keccak256(payload);

    _HubHandler.request(e, poolId, scId, assetId, payload);

    bytes32 payloadHashAfter = ghostHmRequestPayloadHash;

    assert(payloadHashAfter == payloadHash, "a request is forwarded with its payload unchanged");
}

// HH-HL-24: a share report notifies the pool's snapshot hook exactly when it closes a batch.
rule hlHhSyncNotificationOnlyOnAClosedBatch(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, uint128 amount, bool isIssuance, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    address hookBefore = ghostHoSnapshotHook;
    mathint syncsBefore = ghostHookOnSyncCount;

    _HubHandler.updateShares(e, centrifugeId, poolId, scId, amount, isIssuance, isSnapshot, nonce);

    assert(ghostHookOnSyncCount == syncsBefore + ((isSnapshot && hookBefore != 0) ? 1 : 0),
        "a share report notifies a set hook once exactly when it marks sync");
    assert(ghostHookOnSyncCount != syncsBefore
        => (ghostHookOnSyncCid16 == centrifugeId && ghostHookOnSyncPool64 == poolId
            && ghostHookOnSyncScId == scId),
        "the notice names the report's network, pool and share class");
}

// HH-HL-25: an admin updating one handler dependency leaves the other three unchanged.
rule hlHhFileWiresOnlyTheNamedSlot(env e, bytes32 what, address data) {

    setupHubHandlerLinkedHubCoreValidState(e);

    address hubBefore = _HubHandler.hub;
    address holdingsBefore = _HubHandler.holdings;
    address senderBefore = _HubHandler.sender;
    address bookBefore = _HubHandler.shareClassManager;

    _HubHandler.file(e, what, data);

    assert(_HubHandler.hub == (what == FILE_HUB_HH_CVL() ? data : hubBefore)
        && _HubHandler.holdings == (what == FILE_HOLDINGS_HH_CVL() ? data : holdingsBefore)
        && _HubHandler.sender == (what == FILE_SENDER_HH_CVL() ? data : senderBefore)
        && _HubHandler.shareClassManager == (what == FILE_SHARE_CLASS_MANAGER_HH_CVL() ? data : bookBefore),
        "rewiring sets only the named dependency, to the address given");
}

// HH-HL-26: an asset report notifies the snapshot hook exactly when it closes a batch.
rule hlHhAssetReportNotifiesTheHookExactlyOnAClosedBatch(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isIncrease, bool isSnapshot,
    uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    address hookBefore = ghostHoSnapshotHook;
    mathint syncsBefore = ghostHookOnSyncCount;

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, isIncrease, isSnapshot, nonce);

    assert(ghostHookOnSyncCount == syncsBefore + ((isSnapshot && hookBefore != 0) ? 1 : 0),
        "an asset report pings a set hook once if it is a snapshot, else never");
    assert(ghostHookOnSyncCount != syncsBefore
        => (ghostHookOnSyncCid16 == centrifugeId && ghostHookOnSyncPool64 == poolId
            && ghostHookOnSyncScId == scId),
        "the notice names the report's network, pool and share class");
}

// HH-HL-27: an asset report books exactly the holding's value change to its own accounts, none if uninitialized.
rule hlHhAssetReportJournalsTheRealizedValueOnlyOnAnInitializedHolding(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount,
    bool isIncrease, bool isSnapshot, uint64 nonce, mathint x) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool live = ghostHoValuation[assetId] != 0;
    mathint valueBefore = ghostHoAssetAmountValue128[assetId];
    mathint amountDebit = ghostHoAccountId256[assetId][0];
    mathint amountCredit = ghostHoAccountId256[assetId][1];
    mathint debitAccount = isIncrease ? amountDebit : amountCredit;
    mathint creditAccount = isIncrease ? amountCredit : amountDebit;
    mathint debitBefore = ghostAcTotalDebit128[x];
    mathint creditBefore = ghostAcTotalCredit128[x];
    mathint updatedBefore = ghostAcLastUpdated64[x];
    mathint journalsBefore = ghostAcJournalIdCounter64;

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, isIncrease, isSnapshot, nonce);

    mathint valueAfter = ghostHoAssetAmountValue128[assetId];
    mathint realized = valueAfter >= valueBefore ? valueAfter - valueBefore : valueBefore - valueAfter;

    assert(!live => (ghostAcTotalDebit128[x] == debitBefore && ghostAcTotalCredit128[x] == creditBefore
            && ghostAcLastUpdated64[x] == updatedBefore && ghostAcJournalIdCounter64 == journalsBefore),
        "a report on an uninitialized holding touches no account or journal");
    assert(live => (ghostAcTotalDebit128[x] - debitBefore == ((realized != 0 && x == debitAccount) ? realized : 0)
            && ghostAcTotalCredit128[x] - creditBefore == ((realized != 0 && x == creditAccount) ? realized : 0)),
        "if initialized, the change posts by direction to its accounts only");
}

// HH-HL-28: an accepted asset report spends exactly its own network's next snapshot nonce, once.
rule hlHhAcceptedAssetReportSpendsItsNetworksNonceOnce(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isIncrease, bool isSnapshot,
    uint64 nonce, uint16 other) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(other != centrifugeId, "SCOPE: two distinct networks");

    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];
    mathint otherNonceBefore = ghostHoSnapshotNonce64[other];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, isIncrease, isSnapshot, nonce);

    assert(nonce == nonceBefore
        && ghostHoSnapshotNonce64[centrifugeId] == nonceBefore + 1
        && ghostHoSnapshotNonce64[other] == otherNonceBefore,
        "the report used the awaited nonce, now one higher on its network only");
}

// HH-HL-29: an accepted share report spends exactly its own network's next snapshot nonce, once.
rule hlHhAcceptedShareReportSpendsItsNetworksNonceOnce(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, uint128 amount, bool isIssuance, bool isSnapshot, uint64 nonce, uint16 other) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(other != centrifugeId, "SCOPE: two distinct networks");

    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];
    mathint otherNonceBefore = ghostHoSnapshotNonce64[other];

    _HubHandler.updateShares(e, centrifugeId, poolId, scId, amount, isIssuance, isSnapshot, nonce);

    assert(nonce == nonceBefore
        && ghostHoSnapshotNonce64[centrifugeId] == nonceBefore + 1
        && ghostHoSnapshotNonce64[other] == otherNonceBefore,
        "the report used the awaited nonce, now one higher on its network only");
}

// HH-HL-30: an asset report from one network never changes another network's shortfall counts.
rule hlHhReportOfAnotherNetworkLeavesTheTrackedCountersAlone(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount,
    bool isIncrease, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(centrifugeId != ghostHoCid16, "SCOPE: a report from a network other than the tallied one");

    mathint networkBefore = ghostHoNetworkDeficitCount32;
    mathint classBefore = ghostHoDeficitCount32;

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, isIncrease, isSnapshot, nonce);

    assert(ghostHoNetworkDeficitCount32 == networkBefore && ghostHoDeficitCount32 == classBefore,
        "a report from another network leaves the tallied deficit counts alone");
}

// HH-HL-31: a share transfer leaves a share class's issued and revoked totals unchanged.
rule hlHhTransferLeavesTheClassCountersAlone(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint issuedBefore = ghostScTotalIssuances256;
    mathint revokedBefore = ghostScTotalRevocations256;

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    assert(ghostScTotalIssuances256 == issuedBefore && ghostScTotalRevocations256 == revokedBefore,
        "a transfer leaves the class's issued and revoked counters untouched");
}

// HH-HL-32: with no bridging hook, a transfer keeps the caller's extra gas limit.
rule hlHhHooklessTransferKeepsTheExtraGasLimit(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    assert(ghostMsLastExtraGasLimit128 == to_mathint(extraGasLimit), "a hookless transfer sends the extra gas limit unchanged");
}

// HH-HL-33: a bridging hook cannot redirect a share transfer to another pool or share class.
rule hlHhTransferKeepsThePoolAndClass(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    assert(ghostMsLastPool64 == to_mathint(poolId) && ghostMsLastScId == scId,
        "the transfer message names the pool and class the caller named");
}
