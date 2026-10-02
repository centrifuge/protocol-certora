// MessageDispatcher. Model: records each outbound send, for scenes not compiling it.

import "../../../../shared/call_order.spec";

definition MS_NOTIFY_POOL() returns mathint = 1;
definition MS_NOTIFY_SHARE_METADATA() returns mathint = 2;
definition MS_NOTIFY_PRICE_SHARE() returns mathint = 3;
definition MS_NOTIFY_PRICE_ASSET() returns mathint = 4;
definition MS_UPDATE_RESTRICTION() returns mathint = 5;
definition MS_MANAGER_CALL_HUB() returns mathint = 6;
definition MS_UPDATE_VAULT() returns mathint = 7;
definition MS_SET_REQUEST_MANAGER() returns mathint = 8;
definition MS_SET_POLICY() returns mathint = 9;
definition MS_AUTHORIZE_SPOKE() returns mathint = 10;
definition MS_UNAUTHORIZE_SPOKE() returns mathint = 11;
definition MS_UPDATE_MANAGER() returns mathint = 12;
definition MS_EXECUTE_TRANSFER_SHARES() returns mathint = 13;
definition MS_REQUEST_CALLBACK() returns mathint = 14;
definition MS_SET_POOL_ADAPTERS() returns mathint = 15;
definition MS_INITIATE_TRANSFER_SHARES() returns mathint = 16;
definition MS_REGISTER_ASSET() returns mathint = 17;
definition MS_UPDATE_ASSETS() returns mathint = 18;
definition MS_UPDATE_SHARES() returns mathint = 19;
definition MS_REQUEST() returns mathint = 20;
definition MS_MANAGER_CALL_SPOKE() returns mathint = 21;
definition MS_NOTIFY_SHARE_CLASS() returns mathint = 22;

// TRUSTED: deployment sets a nonzero local chain id.
persistent ghost uint16 ghostMsLocalCentrifugeId16 {
    axiom ghostMsLocalCentrifugeId16 != 0;
}
persistent ghost mathint ghostMsSendCount {
    init_state axiom ghostMsSendCount == 0;
    axiom ghostMsSendCount >= 0;
}
persistent ghost mathint ghostMsLastKind;
persistent ghost mathint ghostMsLastCid16;
persistent ghost mathint ghostMsLastPool64;
persistent ghost bytes16 ghostMsLastScId;
persistent ghost mathint ghostMsLastAssetId128;
persistent ghost mathint ghostMsLastAmount;
persistent ghost address ghostMsLastRefund;
persistent ghost bytes32 ghostMsLastPayloadHash;
persistent ghost mathint ghostMsExecuteTransferAmount128;
persistent ghost bytes32 ghostMsExecuteTransferReceiver;
persistent ghost mathint ghostMsExecuteTransferOriginCid16;
persistent ghost mathint ghostMsExecuteTransferTargetCid16;
persistent ghost mathint ghostMsRequestCallbackCount {
    init_state axiom ghostMsRequestCallbackCount == 0;
    axiom ghostMsRequestCallbackCount >= 0;
}
persistent ghost bool ghostMsRequestCallbackUnpaid;
persistent ghost mathint ghostMsInitiateTransferCount {
    init_state axiom ghostMsInitiateTransferCount == 0;
    axiom ghostMsInitiateTransferCount >= 0;
}
persistent ghost mathint ghostMsInitiateTransferAmount128;
persistent ghost bytes32 ghostMsInitiateTransferReceiver;
persistent ghost mathint ghostMsInitiateTransferAt;
persistent ghost mathint ghostMsSetPoolAdaptersAt;
persistent ghost mathint ghostMsRegisterAssetCount {
    init_state axiom ghostMsRegisterAssetCount == 0;
    axiom ghostMsRegisterAssetCount >= 0;
}
persistent ghost mathint ghostMsRegisterAssetDecimals8;
persistent ghost mathint ghostMsUpdateNetAmount128;
persistent ghost bool ghostMsUpdateIsIncrease;
persistent ghost bool ghostMsUpdateIsSnapshot;
persistent ghost mathint ghostMsUpdateNonce64;
// Field recorders: a summary that drops a field hides a mismatch on it.
persistent ghost bool ghostMsRequestUnpaid;
persistent ghost bytes32 ghostMsLastSenderWord;
persistent ghost mathint ghostMsLastValue256;
persistent ghost mathint ghostMsLastExtraGasLimit128;
persistent ghost mathint ghostMsLastRemoteExtraGasLimit128;
persistent ghost mathint ghostMsLastVaultKind8;
persistent ghost mathint ghostMsLastComputedAt64;
persistent ghost mathint ghostMsLastManagerKind8;
persistent ghost bytes32 ghostMsLastWord;
persistent ghost bool ghostMsLastCanManage;
persistent ghost address ghostMsLastTarget;
persistent ghost mathint ghostMsLastThreshold8;
persistent ghost mathint ghostMsLastSessionId16;

function msRecordCoreCVL(env e, mathint kind, uint16 cid, uint64 pool, bytes16 scId, uint128 assetId, mathint amount, address refund) {
    ghostMsSendCount = ghostMsSendCount + 1;
    ghostMsLastKind = kind;
    ghostMsLastCid16 = cid;
    ghostMsLastPool64 = pool;
    ghostMsLastScId = scId;
    ghostMsLastAssetId128 = assetId;
    ghostMsLastAmount = amount;
    ghostMsLastRefund = refund;
    ghostMsLastValue256 = e.msg.value;
}

function msRecordCVL(env e, mathint kind, uint16 cid, uint64 pool, bytes16 scId, uint128 assetId, mathint amount, address refund) {
    msRecordCoreCVL(e, kind, cid, pool, scId, assetId, amount, refund);
}

function msRecordGasCVL(env e, mathint kind, uint16 cid, uint64 pool, bytes16 scId, uint128 extraGasLimit, address refund) {
    msRecordCoreCVL(e, kind, cid, pool, scId, 0, 0, refund);
    ghostMsLastExtraGasLimit128 = extraGasLimit;
}

function msRecordPayloadCVL(env e, mathint kind, uint16 cid, uint64 pool, bytes16 scId, uint128 assetId, mathint amount, address refund, bytes payload) {
    msRecordCoreCVL(e, kind, cid, pool, scId, assetId, amount, refund);
    ghostMsLastPayloadHash = keccak256(payload);
}

function msRecordPayloadGasCVL(env e, mathint kind, uint16 cid, uint64 pool, bytes16 scId, bytes payload, uint128 extraGasLimit, address refund) {
    msRecordPayloadCVL(e, kind, cid, pool, scId, 0, 0, refund, payload);
    ghostMsLastExtraGasLimit128 = extraGasLimit;
}

function msExecuteTransferSharesCVL(env e, uint16 originCid, uint16 targetCid, uint64 pool, bytes16 scId, bytes32 receiver, uint128 amount, uint128 extraGasLimit, address refund) {
    msRecordCoreCVL(e, MS_EXECUTE_TRANSFER_SHARES(), targetCid, pool, scId, 0, amount, refund);
    ghostMsLastExtraGasLimit128 = extraGasLimit;
    ghostMsExecuteTransferAmount128 = amount;
    ghostMsExecuteTransferReceiver = receiver;
    ghostMsExecuteTransferOriginCid16 = originCid;
    ghostMsExecuteTransferTargetCid16 = targetCid;
}

function msRequestCallbackCVL(env e, uint64 pool, bytes16 scId, uint128 assetId, bytes payload, uint128 extraGasLimit, bool unpaidMode, address refund) {
    msRecordCoreCVL(e, MS_REQUEST_CALLBACK(), 0, pool, scId, assetId, 0, refund);
    ghostMsLastPayloadHash = keccak256(payload);
    ghostMsLastExtraGasLimit128 = extraGasLimit;
    ghostMsRequestCallbackCount = ghostMsRequestCallbackCount + 1;
    ghostMsRequestCallbackUnpaid = unpaidMode;
}

function msRequestCVL(env e, uint64 pool, bytes16 scId, uint128 assetId, bytes payload, uint128 extraGasLimit, bool unpaidMode, address refund) {
    msRecordCoreCVL(e, MS_REQUEST(), 0, pool, scId, assetId, 0, refund);
    ghostMsLastPayloadHash = keccak256(payload);
    ghostMsLastExtraGasLimit128 = extraGasLimit;
    ghostMsRequestUnpaid = unpaidMode;
}

function msInitiateTransferSharesCVL(env e, uint16 cid, uint64 pool, bytes16 scId, bytes32 sender, bytes32 receiver, uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {
    msRecordCoreCVL(e, MS_INITIATE_TRANSFER_SHARES(), cid, pool, scId, 0, amount, refund);
    ghostMsInitiateTransferCount = ghostMsInitiateTransferCount + 1;
    ghostMsInitiateTransferAmount128 = amount;
    ghostMsInitiateTransferReceiver = receiver;
    ghostMsLastSenderWord = sender;
    ghostMsLastExtraGasLimit128 = extraGasLimit;
    ghostMsLastRemoteExtraGasLimit128 = remoteExtraGasLimit;
    ghostMsInitiateTransferAt = callOrderTickCVL();
}

function msSetPoolAdaptersStampedCVL(env e, uint16 cid, uint64 pool, uint8 threshold, uint16 targetSessionId, address refund) {
    msSetPoolAdaptersCVL(e, cid, pool, threshold, targetSessionId, refund);
    ghostMsSetPoolAdaptersAt = callOrderTickCVL();
}

function msRegisterAssetCVL(env e, uint16 cid, uint128 assetId, uint8 decimals, address refund) {
    msRecordCoreCVL(e, MS_REGISTER_ASSET(), cid, 0, to_bytes16(0), assetId, 0, refund);
    ghostMsRegisterAssetCount = ghostMsRegisterAssetCount + 1;
    ghostMsRegisterAssetDecimals8 = decimals;
}

function msRecordUpdateDataCVL(ISpokeMessageSender.UpdateData data) {
    ghostMsUpdateNetAmount128 = data.netAmount;
    ghostMsUpdateIsIncrease = data.isIncrease;
    ghostMsUpdateIsSnapshot = data.isSnapshot;
    ghostMsUpdateNonce64 = data.nonce;
}

function msUpdateAssetsCVL(env e, uint64 pool, bytes16 scId, uint128 assetId, ISpokeMessageSender.UpdateData data, uint128 extraGasLimit, address refund) {
    msRecordCoreCVL(e, MS_UPDATE_ASSETS(), 0, pool, scId, assetId, data.netAmount, refund);
    msRecordUpdateDataCVL(data);
    ghostMsLastExtraGasLimit128 = extraGasLimit;
}

function msUpdateSharesCVL(env e, uint64 pool, bytes16 scId, ISpokeMessageSender.UpdateData data, uint128 extraGasLimit, address refund) {
    msRecordCoreCVL(e, MS_UPDATE_SHARES(), 0, pool, scId, 0, data.netAmount, refund);
    msRecordUpdateDataCVL(data);
    ghostMsLastExtraGasLimit128 = extraGasLimit;
}

function msNotifyPricePoolPerShareCVL(env e, uint16 cid, uint64 pool, bytes16 scId, uint128 price, uint64 computedAt, address refund) {
    msRecordCoreCVL(e, MS_NOTIFY_PRICE_SHARE(), cid, pool, scId, 0, price, refund);
    ghostMsLastComputedAt64 = computedAt;
}

function msManagerCallFromHubCVL(env e, uint16 cid, uint64 pool, address target, bytes payload, uint128 extraGasLimit, uint256 value, address refund) {
    msRecordCoreCVL(e, MS_MANAGER_CALL_HUB(), cid, pool, to_bytes16(0), 0, value, refund);
    ghostMsLastPayloadHash = keccak256(payload);
    ghostMsLastTarget = target;
    ghostMsLastExtraGasLimit128 = extraGasLimit;
}

function msManagerCallFromSpokeCVL(env e, uint64 pool, bytes32 target, bytes payload, bytes32 sender, uint128 extraGasLimit, address refund) {
    msRecordPayloadCVL(e, MS_MANAGER_CALL_SPOKE(), 0, pool, to_bytes16(0), 0, 0, refund, payload);
    ghostMsLastWord = target;
    ghostMsLastSenderWord = sender;
    ghostMsLastExtraGasLimit128 = extraGasLimit;
}

function msUpdateVaultCVL(env e, uint64 pool, bytes16 scId, uint128 assetId, bytes32 vaultOrFactory, uint8 kind, bytes payload, uint128 extraGasLimit, address refund) {
    msRecordPayloadCVL(e, MS_UPDATE_VAULT(), 0, pool, scId, assetId, 0, refund, payload);
    ghostMsLastWord = vaultOrFactory;
    ghostMsLastVaultKind8 = kind;
    ghostMsLastExtraGasLimit128 = extraGasLimit;
}

function msRecordWordCVL(env e, mathint kind, uint16 cid, uint64 pool, bytes32 word, address refund) {
    msRecordCoreCVL(e, kind, cid, pool, to_bytes16(0), 0, 0, refund);
    ghostMsLastWord = word;
}

function msUpdateManagerCVL(env e, uint16 cid, uint64 pool, uint8 kind, bytes32 who, bool canManage, address refund) {
    msRecordCoreCVL(e, MS_UPDATE_MANAGER(), cid, pool, to_bytes16(0), 0, 0, refund);
    ghostMsLastManagerKind8 = kind;
    ghostMsLastWord = who;
    ghostMsLastCanManage = canManage;
}

function msSetPoolAdaptersCVL(env e, uint16 cid, uint64 pool, uint8 threshold, uint16 targetSessionId, address refund) {
    msRecordCoreCVL(e, MS_SET_POOL_ADAPTERS(), cid, pool, to_bytes16(0), 0, 0, refund);
    ghostMsLastThreshold8 = threshold;
    ghostMsLastSessionId16 = targetSessionId;
}

function msNotifyShareClassCVL(env e, uint16 cid, uint64 pool, bytes16 scId, bytes32 salt, bytes payload, address refund) {
    msRecordPayloadCVL(e, MS_NOTIFY_SHARE_CLASS(), cid, pool, scId, 0, 0, refund, payload);
    ghostMsLastWord = salt;
}

// UNSAFE: a recorded send has no effect, delivery and ETH unanalysed.
methods {
    function _.localCentrifugeId() external
        => ghostMsLocalCentrifugeId16 expect uint16 UNRESOLVED;

    function _.sendNotifyPool(uint16 centrifugeId, uint64 poolId, address refund) external with (env e)
        => msRecordCVL(e, MS_NOTIFY_POOL(), centrifugeId, poolId, to_bytes16(0), 0, 0, refund) expect void UNRESOLVED;
    function _.sendNotifyShareMetadata(uint16 centrifugeId, uint64 poolId, bytes16 scId, string name, string symbol, uint128 extraGasLimit, address refund) external with (env e)
        => msRecordGasCVL(e, MS_NOTIFY_SHARE_METADATA(), centrifugeId, poolId, scId, extraGasLimit, refund) expect void UNRESOLVED;
    function _.sendNotifyPricePoolPerShare(uint16 centrifugeId, uint64 poolId, bytes16 scId, uint128 pricePoolPerShare, uint64 computedAt, address refund) external with (env e)
        => msNotifyPricePoolPerShareCVL(e, centrifugeId, poolId, scId, pricePoolPerShare, computedAt, refund) expect void UNRESOLVED;
    function _.sendNotifyPricePoolPerAsset(uint64 poolId, bytes16 scId, uint128 assetId, uint128 pricePoolPerAsset, address refund) external with (env e)
        => msRecordCVL(e, MS_NOTIFY_PRICE_ASSET(), 0, poolId, scId, assetId, pricePoolPerAsset, refund) expect void UNRESOLVED;
    function _.sendUpdateRestriction(uint16 centrifugeId, uint64 poolId, bytes16 scId, bytes payload, uint128 extraGasLimit, address refund) external with (env e)
        => msRecordPayloadGasCVL(e, MS_UPDATE_RESTRICTION(), centrifugeId, poolId, scId, payload, extraGasLimit, refund) expect void UNRESOLVED;
    function _.sendManagerCallFromHub(uint16 centrifugeId, uint64 poolId, address target, bytes payload, uint128 extraGasLimit, uint256 value, address refund) external with (env e)
        => msManagerCallFromHubCVL(e, centrifugeId, poolId, target, payload, extraGasLimit, value, refund) expect void UNRESOLVED;
    function _.sendUpdateVault(uint64 poolId, bytes16 scId, uint128 assetId, bytes32 vaultOrFactory, uint8 kind, bytes payload, uint128 extraGasLimit, address refund) external with (env e)
        => msUpdateVaultCVL(e, poolId, scId, assetId, vaultOrFactory, kind, payload, extraGasLimit, refund) expect void UNRESOLVED;
    function _.sendSetRequestManager(uint16 centrifugeId, uint64 poolId, bytes32 manager, address refund) external with (env e)
        => msRecordWordCVL(e, MS_SET_REQUEST_MANAGER(), centrifugeId, poolId, manager, refund) expect void UNRESOLVED;
    function _.sendSetPolicy(uint16 centrifugeId, uint64 poolId, bytes32 policy, address refund) external with (env e)
        => msRecordWordCVL(e, MS_SET_POLICY(), centrifugeId, poolId, policy, refund) expect void UNRESOLVED;
    function _.sendAuthorizeSpokeCall(uint16 centrifugeId, uint64 poolId, bytes data, address refund) external with (env e)
        => msRecordPayloadCVL(e, MS_AUTHORIZE_SPOKE(), centrifugeId, poolId, to_bytes16(0), 0, 0, refund, data) expect void UNRESOLVED;
    function _.sendUnauthorizeSpokeCall(uint16 centrifugeId, uint64 poolId, bytes data, address refund) external with (env e)
        => msRecordPayloadCVL(e, MS_UNAUTHORIZE_SPOKE(), centrifugeId, poolId, to_bytes16(0), 0, 0, refund, data) expect void UNRESOLVED;
    function _.sendUpdateManager(uint16 centrifugeId, uint64 poolId, uint8 kind, bytes32 who, bool canManage, address refund) external with (env e)
        => msUpdateManagerCVL(e, centrifugeId, poolId, kind, who, canManage, refund) expect void UNRESOLVED;
    function _.sendRequestCallback(uint64 poolId, bytes16 scId, uint128 assetId, bytes payload, uint128 extraGasLimit, bool unpaidMode, address refund) external with (env e)
        => msRequestCallbackCVL(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund) expect void UNRESOLVED;
    function _.sendSetPoolAdapters(uint16 centrifugeId, uint64 poolId, bytes32[] adapters, uint8 threshold, uint16 targetSessionId, address refund) external with (env e)
        => msSetPoolAdaptersStampedCVL(e, centrifugeId, poolId, threshold, targetSessionId, refund) expect void UNRESOLVED;

    function _.sendExecuteTransferShares(uint16 originCentrifugeId, uint16 targetCentrifugeId, uint64 poolId, bytes16 scId, bytes32 receiver, uint128 amount, uint128 extraGasLimit, address refund) external with (env e)
        => msExecuteTransferSharesCVL(e, originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund) expect void UNRESOLVED;

    function _.sendInitiateTransferShares(uint16 centrifugeId, uint64 poolId, bytes16 scId, bytes32 sender, bytes32 receiver, uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) external with (env e)
        => msInitiateTransferSharesCVL(e, centrifugeId, poolId, scId, sender, receiver, amount, extraGasLimit, remoteExtraGasLimit, refund) expect void UNRESOLVED;
    function _.sendRegisterAsset(uint16 centrifugeId, uint128 assetId, uint8 decimals, address refund) external with (env e)
        => msRegisterAssetCVL(e, centrifugeId, assetId, decimals, refund) expect void UNRESOLVED;
    function _.sendUpdateAssets(uint64 poolId, bytes16 scId, uint128 assetId, ISpokeMessageSender.UpdateData data, uint128 extraGasLimit, address refund) external with (env e)
        => msUpdateAssetsCVL(e, poolId, scId, assetId, data, extraGasLimit, refund) expect void UNRESOLVED;
    function _.sendUpdateShares(uint64 poolId, bytes16 scId, ISpokeMessageSender.UpdateData data, uint128 extraGasLimit, address refund) external with (env e)
        => msUpdateSharesCVL(e, poolId, scId, data, extraGasLimit, refund) expect void UNRESOLVED;
    function _.sendRequest(uint64 poolId, bytes16 scId, uint128 assetId, bytes payload, uint128 extraGasLimit, bool unpaidMode, address refund) external with (env e)
        => msRequestCVL(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund) expect void UNRESOLVED;
    function _.sendManagerCallFromSpoke(uint64 poolId, bytes32 target, bytes payload, bytes32 sender, uint128 extraGasLimit, address refund) external with (env e)
        => msManagerCallFromSpokeCVL(e, poolId, target, payload, sender, extraGasLimit, refund) expect void UNRESOLVED;
}
