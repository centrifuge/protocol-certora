import "HubHandler_LinkedHubCore_valid_state.spec";

// HH-RC-01: a spoke can register a new asset on the hub with its declared decimals.
rule rcHhRegisterAssetIsReachable(env e, HubHandler.AssetId assetId, uint8 decimals) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];

    _HubHandler.registerAsset(e, assetId, decimals);

    bool registeredAfter = ghostHrAssetRegistered[assetId];
    mathint decimalsAfter = ghostHrAssetDecimals8[assetId];

    satisfy(!registeredBefore && registeredAfter && decimalsAfter == decimals,
        "a new asset can be registered with its declared decimals");
}

// HH-RC-02: an asset with 18 decimals, the maximum accepted, can be registered.
rule rcHhRegisterAssetAtTheDecimalsCeilingIsReachable(env e, HubHandler.AssetId assetId, uint8 decimals) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];

    _HubHandler.registerAsset(e, assetId, decimals);

    bool registeredAfter = ghostHrAssetRegistered[assetId];
    mathint decimalsAfter = ghostHrAssetDecimals8[assetId];

    satisfy(!registeredBefore && registeredAfter && decimalsAfter == MAX_DECIMALS_CVL(),
        "a new asset can be registered at the 18-decimal cap");
}

// HH-RC-03: an asset with zero decimals can be registered.
rule rcHhRegisterAssetAtZeroDecimalsIsReachable(env e, HubHandler.AssetId assetId, uint8 decimals) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];

    _HubHandler.registerAsset(e, assetId, decimals);

    bool registeredAfter = ghostHrAssetRegistered[assetId];
    mathint decimalsAfter = ghostHrAssetDecimals8[assetId];

    satisfy(!registeredBefore && registeredAfter && decimalsAfter == 0,
        "a new asset can be registered with zero decimals");
}

// HH-RC-04: a deposit report can raise a holding's value with a balanced journal entry.
rule rcHhAssetDepositOnALiveHoldingIsReachable(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isSnapshot,
    uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHoValuation[assetId] != 0, "SCOPE: an opened holding, which reaches the books");

    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    mathint valueBefore = ghostHoAssetAmountValue128[assetId];
    mathint debitBefore = AC_TOTAL_DEBIT_SUM();
    mathint creditBefore = AC_TOTAL_CREDIT_SUM();

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, true, isSnapshot, nonce);

    mathint increasedAfter = ghostHoIncreasedAmount256[assetId];
    mathint valueAfter = ghostHoAssetAmountValue128[assetId];
    mathint debitAfter = AC_TOTAL_DEBIT_SUM();
    mathint creditAfter = AC_TOTAL_CREDIT_SUM();

    satisfy(amount > 0 && increasedAfter == increasedBefore + amount
        && valueAfter > valueBefore
        && debitAfter - debitBefore == valueAfter - valueBefore
        && creditAfter - creditBefore == valueAfter - valueBefore,
        "a deposit report can grow an opened holding and journal the value rise");
}

// HH-RC-05: a withdrawal report can lower a holding's value with a balanced journal entry.
rule rcHhAssetWithdrawalOnALiveHoldingIsReachable(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isSnapshot,
    uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHoValuation[assetId] != 0, "SCOPE: an opened holding, which reaches the books");

    mathint decreasedBefore = ghostHoDecreasedAmount256[assetId];
    mathint valueBefore = ghostHoAssetAmountValue128[assetId];
    mathint debitBefore = AC_TOTAL_DEBIT_SUM();
    mathint creditBefore = AC_TOTAL_CREDIT_SUM();

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, false, isSnapshot, nonce);

    mathint decreasedAfter = ghostHoDecreasedAmount256[assetId];
    mathint valueAfter = ghostHoAssetAmountValue128[assetId];
    mathint debitAfter = AC_TOTAL_DEBIT_SUM();
    mathint creditAfter = AC_TOTAL_CREDIT_SUM();

    satisfy(amount > 0 && decreasedAfter == decreasedBefore + amount
        && valueAfter < valueBefore
        && debitAfter - debitBefore == valueBefore - valueAfter
        && creditAfter - creditBefore == valueBefore - valueAfter,
        "a withdrawal report can shrink an opened holding, journaling the drop");
}

// HH-RC-06: a report on a holding never set up can be counted with no journal entry.
rule rcHhAssetReportOnAnUnopenedHoldingIsReachable(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, HubHandler.AssetId assetId,
    uint128 amount, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHoValuation[assetId] == 0, "SCOPE: an unopened holding, which books nothing");

    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    mathint debitBefore = AC_TOTAL_DEBIT_SUM();
    mathint creditBefore = AC_TOTAL_CREDIT_SUM();

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, true, isSnapshot, nonce);

    mathint increasedAfter = ghostHoIncreasedAmount256[assetId];
    mathint debitAfter = AC_TOTAL_DEBIT_SUM();
    mathint creditAfter = AC_TOTAL_CREDIT_SUM();

    satisfy(amount > 0 && increasedAfter == increasedBefore + amount
        && debitAfter == debitBefore && creditAfter == creditBefore,
        "a deposit report can grow an unopened holding without journaling");
}

// HH-RC-07: an asset report can close its network's batch, marking the network in sync.
rule rcHhAssetReportClosingTheBatchIsReachable(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    bool markerBefore = ghostHoIsSnapshot[centrifugeId];
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, true, true, nonce);

    mathint increasedAfter = ghostHoIncreasedAmount256[assetId];
    bool markerAfter = ghostHoIsSnapshot[centrifugeId];
    mathint nonceAfter = ghostHoSnapshotNonce64[centrifugeId];

    satisfy(amount > 0 && increasedAfter == increasedBefore + amount
        && !markerBefore && markerAfter && nonceAfter == nonceBefore + 1,
        "a deposit report can mark its network in sync, nonce up by one");
}

// HH-RC-08: an asset report moving nothing can still close its network's batch.
rule rcHhEmptyAssetBatchClosingIsReachable(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    bool markerBefore = ghostHoIsSnapshot[centrifugeId];
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, 0, true, true, nonce);

    mathint increasedAfter = ghostHoIncreasedAmount256[assetId];
    bool markerAfter = ghostHoIsSnapshot[centrifugeId];
    mathint nonceAfter = ghostHoSnapshotNonce64[centrifugeId];

    satisfy(increasedAfter == increasedBefore && !markerBefore && markerAfter
        && nonceAfter == nonceBefore + 1,
        "an empty asset report can still mark its network in sync");
}

// HH-RC-09: a network's first report, at nonce zero, can close its first batch.
rule rcHhFirstAssetReportOfANetworkIsReachable(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, true, true, 0);

    bool markerAfter = ghostHoIsSnapshot[centrifugeId];
    mathint nonceAfter = ghostHoSnapshotNonce64[centrifugeId];

    satisfy(nonceBefore == 0 && nonceAfter == 1 && markerAfter,
        "a network at nonce zero can become synced on its first report");
}

// HH-RC-10: a withdrawal report can put a holding in deficit, raising its deficit counts.
rule rcHhAssetWithdrawalEnteringDeficitIsReachable(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, HubHandler.AssetId assetId,
    uint128 amount, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    mathint decreasedBefore = ghostHoDecreasedAmount256[assetId];
    mathint networkDeficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, false, isSnapshot, nonce);

    mathint increasedAfter = ghostHoIncreasedAmount256[assetId];
    mathint decreasedAfter = ghostHoDecreasedAmount256[assetId];
    mathint networkDeficitAfter = ghostHoNetworkDeficitCount32;

    satisfy(decreasedBefore <= increasedBefore && decreasedAfter > increasedAfter
        && networkDeficitAfter == networkDeficitBefore + 1 && ghostHoDeficitCount32 == classDeficitBefore + 1,
        "a withdrawal report can take a holding short, both counts up by one");
}

// HH-RC-11: a deposit report can clear a holding's deficit, lowering the class and network deficit counts.
rule rcHhAssetDepositLeavingDeficitIsReachable(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isSnapshot,
    uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    mathint decreasedBefore = ghostHoDecreasedAmount256[assetId];
    mathint networkDeficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, true, isSnapshot, nonce);

    mathint increasedAfter = ghostHoIncreasedAmount256[assetId];
    mathint decreasedAfter = ghostHoDecreasedAmount256[assetId];
    mathint networkDeficitAfter = ghostHoNetworkDeficitCount32;

    satisfy(decreasedBefore > increasedBefore && decreasedAfter <= increasedAfter
        && networkDeficitAfter == networkDeficitBefore - 1 && ghostHoDeficitCount32 == classDeficitBefore - 1,
        "a deposit report can clear a shortfall, both counts down by one");
}

// HH-RC-12: a share report can close its network's batch, marking the network in sync.
rule rcHhShareReportClosingTheBatchIsReachable(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, uint128 amount, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint issuedBefore = ghostScIssuances256[centrifugeId];
    bool markerBefore = ghostHoIsSnapshot[centrifugeId];
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];

    _HubHandler.updateShares(e, centrifugeId, poolId, scId, amount, true, true, nonce);

    mathint issuedAfter = ghostScIssuances256[centrifugeId];
    bool markerAfter = ghostHoIsSnapshot[centrifugeId];
    mathint nonceAfter = ghostHoSnapshotNonce64[centrifugeId];

    satisfy(amount > 0 && issuedAfter == issuedBefore + amount
        && !markerBefore && markerAfter && nonceAfter == nonceBefore + 1,
        "an issuance report can mark its network in sync, nonce up by one");
}

// HH-RC-13: a share report with no movement can still close its network's batch.
rule rcHhMarkerOnlyShareReportIsReachable(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint issuedBefore = ghostScIssuances256[centrifugeId];
    mathint totalBefore = SC_TOTAL_ISSUANCE();
    bool markerBefore = ghostHoIsSnapshot[centrifugeId];
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];

    _HubHandler.updateShares(e, centrifugeId, poolId, scId, 0, true, true, nonce);

    mathint issuedAfter = ghostScIssuances256[centrifugeId];
    mathint totalAfter = SC_TOTAL_ISSUANCE();
    bool markerAfter = ghostHoIsSnapshot[centrifugeId];
    mathint nonceAfter = ghostHoSnapshotNonce64[centrifugeId];

    satisfy(issuedAfter == issuedBefore && totalAfter == totalBefore
        && !markerBefore && markerAfter && nonceAfter == nonceBefore + 1,
        "an empty share report can still mark its network in sync");
}

// HH-RC-14: a bridging hook can resize a share transfer, the burn matching the new amount.
rule rcHhBridgeReachableWithAHookRewritingTheAmount(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook != 0, "SCOPE: a pool with its own bridging hook");
    require(originCid != targetCid, "SCOPE: a transfer between two distinct networks");

    mathint revokedOriginBefore = ghostScRevocations256[originCid];
    mathint sendsBefore = ghostMsSendCount;

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint revokedOriginAfter = ghostScRevocations256[originCid];
    mathint sendsAfter = ghostMsSendCount;
    mathint sentAmount = ghostMsExecuteTransferAmount128;

    satisfy(sendsAfter == sendsBefore + 1 && sentAmount != amount
        && revokedOriginAfter - revokedOriginBefore == sentAmount,
        "a bridging hook can resize a transfer and the burn follows it");
}

// HH-RC-15: a transfer between two networks can leave a third network's shares unchanged.
rule rcHhBridgeLeavesAThirdNetworkAloneIsReachable(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund, uint16 otherCid) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");
    require(originCid != targetCid, "SCOPE: a transfer between two distinct networks");
    require(ghostScIssuances256[otherCid] > 0, "SCOPE: a bystander network already holding shares");

    mathint revokedOriginBefore = ghostScRevocations256[originCid];
    mathint issuedTargetBefore = ghostScIssuances256[targetCid];
    mathint issuedOtherBefore = ghostScIssuances256[otherCid];
    mathint revokedOtherBefore = ghostScRevocations256[otherCid];

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint revokedOriginAfter = ghostScRevocations256[originCid];
    mathint issuedTargetAfter = ghostScIssuances256[targetCid];
    mathint issuedOtherAfter = ghostScIssuances256[otherCid];
    mathint revokedOtherAfter = ghostScRevocations256[otherCid];

    satisfy(amount > 0 && revokedOriginAfter == revokedOriginBefore + amount
        && issuedTargetAfter == issuedTargetBefore + amount
        && issuedOtherAfter == issuedOtherBefore && revokedOtherAfter == revokedOtherBefore,
        "a bridge can burn and mint while a third network stays untouched");
}

// HH-RC-16: a network's whole share position can leave in one transfer.
rule rcHhBridgeEmptyingTheOriginNetworkIsReachable(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");
    require(originCid != targetCid, "SCOPE: a transfer between two distinct networks");

    mathint netOriginBefore = ghostScIssuances256[originCid]
        - ghostScRevocations256[originCid];

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint netOriginAfter = ghostScIssuances256[originCid]
        - ghostScRevocations256[originCid];

    satisfy(netOriginBefore > 0 && amount == netOriginBefore && netOriginAfter == 0,
        "one bridge can move a network's whole net position out");
}

// HH-RC-17: a transfer can move more shares off a network than it has, marking it negative.
rule rcHhBridgeDrivesTheOriginNetworkNegativeIsReachable(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");
    require(originCid != targetCid, "SCOPE: a transfer between two distinct networks");

    mathint issuedOriginBefore = ghostScIssuances256[originCid];
    mathint revokedOriginBefore = ghostScRevocations256[originCid];
    mathint sendsBefore = ghostMsSendCount;
    mathint shortNetworksBefore = ghostScNegativeNetworkCount32;

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    mathint issuedOriginAfter = ghostScIssuances256[originCid];
    mathint revokedOriginAfter = ghostScRevocations256[originCid];
    mathint sendsAfter = ghostMsSendCount;

    satisfy(revokedOriginBefore <= issuedOriginBefore && revokedOriginAfter > issuedOriginAfter
        && sendsAfter == sendsBefore + 1
        && ghostScNegativeNetworkCount32 == shortNetworksBefore + 1,
        "a bridge can drive its origin network short, the short count rising");
}

// HH-RC-18: an admin can switch the handler to a different hub.
rule rcHhFileRepointsTheHubIsReachable(env e, address data) {

    setupHubHandlerLinkedHubCoreValidState(e);

    address hubBefore = _HubHandler.hub(e);

    _HubHandler.file(e, FILE_HUB_HH_CVL(), data);

    address hubAfter = _HubHandler.hub(e);

    satisfy(data != 0 && hubBefore != data && hubAfter == data,
        "the handler's hub can be repointed to a new nonzero address");
}

// HH-RC-19: an admin can switch the handler to a different holdings contract.
rule rcHhFileRepointsTheHoldingsLedgerIsReachable(env e, address data) {

    setupHubHandlerLinkedHubCoreValidState(e);

    address holdingsBefore = _HubHandler.holdings(e);

    _HubHandler.file(e, FILE_HOLDINGS_HH_CVL(), data);

    address holdingsAfter = _HubHandler.holdings(e);

    satisfy(data != 0 && holdingsBefore != data && holdingsAfter == data,
        "the handler's holdings can be repointed to a new nonzero address");
}

// HH-RC-20: an admin can switch the handler to a different outbound message sender.
rule rcHhFileRepointsTheSenderIsReachable(env e, address data) {

    setupHubHandlerLinkedHubCoreValidState(e);

    address senderBefore = _HubHandler.sender(e);

    _HubHandler.file(e, FILE_SENDER_HH_CVL(), data);

    address senderAfter = _HubHandler.sender(e);

    satisfy(data != 0 && senderBefore != data && senderAfter == data,
        "the handler's message sender can be repointed to a new nonzero address");
}

// HH-RC-21: an admin can point the hub handler at a different share class manager.
rule rcHhFileRepointsTheShareClassBookIsReachable(env e, address data) {

    setupHubHandlerLinkedHubCoreValidState(e);

    address bookBefore = _HubHandler.shareClassManager(e);

    _HubHandler.file(e, FILE_SHARE_CLASS_MANAGER_HH_CVL(), data);

    address bookAfter = _HubHandler.shareClassManager(e);

    satisfy(data != 0 && bookBefore != data && bookAfter == data,
        "the handler's class manager can be repointed to a new nonzero address");
}

// HH-RC-22: admin rights on the hub handler can be granted and then revoked again.
rule rcHhRelyThenDenyRoundTripIsReachable(env e, address user) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint wardBefore = _HubHandler.wards(e, user);

    _HubHandler.rely(e, user);

    mathint wardMid = _HubHandler.wards(e, user);

    _HubHandler.deny(e, user);

    mathint wardAfter = _HubHandler.wards(e, user);

    satisfy(wardBefore == 0 && wardMid == 1 && wardAfter == 0,
        "ward rights can be granted and revoked in one transaction");
}

// HH-RC-23: an asset can be registered and receive a reported inflow in one transaction.
rule rcHhRegisterThenReportOnTheAssetIsReachable(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, HubHandler.AssetId assetId,
    uint8 decimals, uint128 amount, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];
    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];

    _HubHandler.registerAsset(e, assetId, decimals);
    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, true, isSnapshot, nonce);

    bool registeredAfter = ghostHrAssetRegistered[assetId];
    mathint increasedAfter = ghostHoIncreasedAmount256[assetId];

    satisfy(!registeredBefore && registeredAfter && amount > 0
        && increasedAfter == increasedBefore + amount,
        "registration and a first inflow can land in one transaction");
}

// HH-RC-24: shares a network issues can be revoked again, leaving total supply unchanged.
rule rcHhIssueThenRevokeRestoresTheClassTotalIsReachable(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, uint128 amount, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint issuedBefore = ghostScIssuances256[centrifugeId];
    mathint revokedBefore = ghostScRevocations256[centrifugeId];
    mathint totalBefore = SC_TOTAL_ISSUANCE();

    _HubHandler.updateShares(e, centrifugeId, poolId, scId, amount, true, false, nonce);
    _HubHandler.updateShares(e, centrifugeId, poolId, scId, amount, false, false,
        require_uint64(nonce + 1));

    mathint issuedAfter = ghostScIssuances256[centrifugeId];
    mathint revokedAfter = ghostScRevocations256[centrifugeId];
    mathint totalAfter = SC_TOTAL_ISSUANCE();

    satisfy(amount > 0 && issuedAfter == issuedBefore + amount
        && revokedAfter == revokedBefore + amount && totalAfter == totalBefore,
        "a network can issue and revoke the same shares, the total unchanged");
}

// HH-RC-25: a report can mark a network's state as a snapshot and the next can clear it.
rule rcHhSnapshotSetThenClearedIsReachable(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool markerBefore = ghostHoIsSnapshot[centrifugeId];
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, true, true, nonce);

    bool markerMid = ghostHoIsSnapshot[centrifugeId];

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, true, false,
        require_uint64(nonce + 1));

    bool markerAfter = ghostHoIsSnapshot[centrifugeId];
    mathint nonceAfter = ghostHoSnapshotNonce64[centrifugeId];

    satisfy(!markerBefore && markerMid && !markerAfter && nonceAfter == nonceBefore + 2,
        "a network can sync and desync in one transaction, nonce up by two");
}

// HH-RC-26: shares can be bridged to another network and back with no net change on either.
rule rcHhBridgeAndReturnLegIsReachable(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");
    require(originCid != targetCid, "SCOPE: a transfer between two distinct networks");

    mathint netOriginBefore = ghostScIssuances256[originCid]
        - ghostScRevocations256[originCid];
    mathint netTargetBefore = ghostScIssuances256[targetCid]
        - ghostScRevocations256[targetCid];
    mathint sendsBefore = ghostMsSendCount;

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);
    _HubHandler.initiateTransferShares(e, targetCid, originCid, poolId, scId, receiver, sender_,
        amount, extraGasLimit, refund);

    mathint netOriginAfter = ghostScIssuances256[originCid]
        - ghostScRevocations256[originCid];
    mathint netTargetAfter = ghostScIssuances256[targetCid]
        - ghostScRevocations256[targetCid];
    mathint sendsAfter = ghostMsSendCount;

    satisfy(amount > 0 && netOriginAfter == netOriginBefore && netTargetAfter == netTargetBefore
        && sendsAfter == sendsBefore + 2,
        "a bridge and its return leg can leave both positions unchanged");
}

// HH-RC-27: a reported revocation can exceed all issued shares, making total supply negative.
rule rcHhShareReportPastTheClassSupplyIsReachable(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, uint128 amount, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    mathint totalBefore = SC_TOTAL_ISSUANCE();
    mathint shortNetworksBefore = ghostScNegativeNetworkCount32;
    bool markerBefore = ghostHoIsSnapshot[centrifugeId];
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];

    _HubHandler.updateShares(e, centrifugeId, poolId, scId, amount, false, true, nonce);

    satisfy(totalBefore >= 0 && SC_TOTAL_ISSUANCE() < 0
        && ghostScNegativeNetworkCount32 == shortNetworksBefore + 1
        && !markerBefore && ghostHoIsSnapshot[centrifugeId]
        && ghostHoSnapshotNonce64[centrifugeId] == nonceBefore + 1,
        "a report can revoke past the class supply, count short and still sync");
}

// HH-RC-28: a shortfall can count against the reporting network, not the asset's home network.
rule rcHhShortfallLandsOnTheReportingNetworkIsReachable(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, HubHandler.AssetId assetId,
    uint128 amount, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(centrifugeId == ghostHoCid16, "SCOPE: binds the reporting network to the tallied one");
    require(ASSET_CENTRIFUGE_ID_HH_CVL(assetId) != centrifugeId, "SCOPE: the asset id names another network");

    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    mathint decreasedBefore = ghostHoDecreasedAmount256[assetId];
    mathint networkDeficitBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitBefore = ghostHoDeficitCount32;

    _HubHandler.updateAssets(e, centrifugeId, poolId, scId, assetId, amount, false, isSnapshot, nonce);

    satisfy(decreasedBefore <= increasedBefore
        && ghostHoDecreasedAmount256[assetId] > ghostHoIncreasedAmount256[assetId]
        && ghostHoNetworkDeficitCount32 == networkDeficitBefore + 1
        && ghostHoDeficitCount32 == classDeficitBefore + 1,
        "going short can raise the class and reporting-network deficit counts");
}

// HH-RC-29: a bridge can clear a network's negative share balance, total supply unchanged.
rule rcHhBridgeClearsAShortTargetNetworkIsReachable(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");
    require(originCid != targetCid, "SCOPE: a transfer between two distinct networks");

    mathint issuedTargetBefore = ghostScIssuances256[targetCid];
    mathint revokedTargetBefore = ghostScRevocations256[targetCid];
    mathint countBefore = ghostScNegativeNetworkCount32;
    mathint totalBefore = SC_TOTAL_ISSUANCE();

    _HubHandler.initiateTransferShares(e, originCid, targetCid, poolId, scId, sender_, receiver,
        amount, extraGasLimit, refund);

    satisfy(revokedTargetBefore > issuedTargetBefore
        && ghostScRevocations256[targetCid] <= ghostScIssuances256[targetCid]
        && ghostScNegativeNetworkCount32 == countBefore - 1
        && SC_TOTAL_ISSUANCE() == totalBefore,
        "a bridge can clear a short target network, the class total unchanged");
}

// HH-RC-30: an asset recorded with zero decimals can later take its real decimals.
rule rcHhZeroDecimalAssetTakesItsDecimalsLaterIsReachable(env e, HubHandler.AssetId assetId, uint8 decimals) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];
    mathint decimalsBefore = ghostHrAssetDecimals8[assetId];

    _HubHandler.registerAsset(e, assetId, decimals);

    satisfy(registeredBefore && decimalsBefore == 0 && decimals > 0
        && ghostHrAssetRegistered[assetId] && ghostHrAssetDecimals8[assetId] == decimals,
        "a zero-decimal asset can be re-announced with its decimals");
}

// HH-RC-31: a new asset registered with zero decimals can be corrected by registering it again.
rule rcHhZeroPrecisionAssetCanBeCorrectedByARepeatRegistration(env e, HubHandler.AssetId assetId, uint8 decimals) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];

    _HubHandler.registerAsset(e, assetId, 0);

    bool registeredAtZero = ghostHrAssetRegistered[assetId];
    mathint decimalsAtZero = ghostHrAssetDecimals8[assetId];

    _HubHandler.registerAsset(e, assetId, decimals);

    satisfy(!registeredBefore && registeredAtZero && decimalsAtZero == 0
        && ghostHrAssetDecimals8[assetId] == to_mathint(decimals) && decimals > 0,
        "a zero-decimal first registration can be corrected by a repeat one");
}
