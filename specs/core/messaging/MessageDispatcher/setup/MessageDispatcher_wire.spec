// MessageDispatcher, wire lane. Setup: MessageLib's own readers on each sent message.

// Own setup: _.send runs MessageLib's readers through a harness only wire_properties.conf compiles; single reads none.

import "MessageDispatcher_entries.spec";

using MessageLibReaderHarness as _MsgReader;

methods {
    function MessageLibReaderHarness.messageLengthOf(bytes message) external returns (uint16) envfree;
    function MessageLibReaderHarness.messageExtraGasLimitOf(bytes message) external returns (uint128) envfree;
    function _.send(uint16 centrifugeId, bytes message, bool unpaidMode, address refund) external with (env e)
        => gatewaySendWireMdCVL(e, calledContract, centrifugeId, message, unpaidMode, refund) expect void UNRESOLVED;
}

persistent ghost mathint ghostGwLastSendLength;
persistent ghost mathint ghostGwLastSendPoolAt1;
persistent ghost bool ghostGwLastSendLengthRead;
persistent ghost mathint ghostGwLastSendLengthOf;
persistent ghost bool ghostGwLastSendGasRead;
persistent ghost mathint ghostGwLastSendGasOf;
persistent ghost mathint ghostGwLastSendTypeAt0;
persistent ghost mathint ghostGwLastSendThresholdAt9;
persistent ghost mathint ghostGwLastSendSessionAt10;
persistent ghost bytes32 ghostGwLastSendWordAt25;

// TRUSTED: MessageLib's logic over the hand-checked BytesLib twins.
function gatewaySendWireMdCVL(env e, address callee, uint16 centrifugeId, bytes message, bool unpaidMode,
    address refund) {
    gatewaySendMdCVL(e, callee, centrifugeId, unpaidMode, refund);
    ghostGwLastSendLength = message.length;
    if (message.length >= 1) {
        ghostGwLastSendTypeAt0 = _BytesSlice.toUint8Pure(message, 0);
    }
    if (message.length >= 9) {
        ghostGwLastSendPoolAt1 = _BytesSlice.toUint64Pure(message, 1);
    }
    if (message.length >= 12) {
        ghostGwLastSendThresholdAt9 = _BytesSlice.toUint8Pure(message, 9);
        ghostGwLastSendSessionAt10 = _BytesSlice.toUint16Pure(message, 10);
    }
    if (message.length >= 57) {
        ghostGwLastSendWordAt25 = _BytesSlice.toBytes32Pure(message, 25);
    }
    uint16 measured = _MsgReader.messageLengthOf@withrevert(message);
    ghostGwLastSendLengthRead = !lastReverted;
    ghostGwLastSendLengthOf = measured;
    uint128 gas = _MsgReader.messageExtraGasLimitOf@withrevert(message);
    ghostGwLastSendGasRead = !lastReverted;
    ghostGwLastSendGasOf = gas;
}

// MessageType code each send function writes; the v3.1 holding amount overload writes UpdateAssets.
definition TYPE_CODE_OF_MD(method f) returns mathint =
    f.selector == sig:sendScheduleUpgrade(uint16,bytes32,address).selector ? 1
    : f.selector == sig:sendCancelUpgrade(uint16,bytes32,address).selector ? 2
    : f.selector == sig:sendRegisterAsset(uint16,MessageDispatcher.AssetId,uint8,address).selector ? 3
    : f.selector == sig:sendSetPoolAdapters(uint16,MessageDispatcher.PoolId,bytes32[],uint8,uint16,address).selector ? 4
    : f.selector == sig:sendNotifyPool(uint16,MessageDispatcher.PoolId,address).selector ? 5
    : f.selector == sig:sendNotifyShareClass(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        MessageDispatcher.ShareClassMetadata,bytes32,bytes32,bytes,uint128,address).selector ? 6
    : f.selector == sig:sendNotifyPricePoolPerShare(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        MessageDispatcher.D18,uint64,address).selector ? 7
    : f.selector == sig:sendNotifyPricePoolPerAsset(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        MessageDispatcher.AssetId,MessageDispatcher.D18,address).selector ? 8
    : f.selector == sig:sendNotifyShareMetadata(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        string,string,uint128,address).selector ? 9
    : f.selector == sig:sendInitiateTransferShares(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        bytes32,bytes32,uint128,uint128,uint128,address).selector ? 10
    : f.selector == sig:sendExecuteTransferShares(uint16,uint16,MessageDispatcher.PoolId,
        MessageDispatcher.ShareClassId,bytes32,uint128,uint128,address).selector ? 11
    : f.selector == sig:sendUpdateRestriction(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        bytes,uint128,address).selector ? 12
    : f.selector == sig:sendUpdateVault(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        MessageDispatcher.AssetId,bytes32,MessageDispatcher.VaultUpdateKind,bytes,uint128,address).selector ? 13
    : f.selector == sig:sendUpdateAssets(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        MessageDispatcher.AssetId,ISpokeMessageSender.UpdateData,uint128,address).selector ? 14
    : f.selector == sig:sendUpdateHoldingAmount(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        MessageDispatcher.AssetId,ISpokeMessageSender.UpdateData,MessageDispatcher.D18,uint128,address).selector ? 14
    : f.selector == sig:sendUpdateShares(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        ISpokeMessageSender.UpdateData,uint128,address).selector ? 15
    : f.selector == sig:sendRequest(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        MessageDispatcher.AssetId,bytes,uint128,bool,address).selector ? 16
    : f.selector == sig:sendRequestCallback(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
        MessageDispatcher.AssetId,bytes,uint128,bool,address).selector ? 17
    : f.selector == sig:sendSetRequestManager(uint16,MessageDispatcher.PoolId,bytes32,address).selector ? 18
    : f.selector == sig:sendManagerCallFromSpoke(MessageDispatcher.PoolId,bytes32,bytes,bytes32,uint128,
        address).selector ? 19
    : f.selector == sig:sendManagerCallFromHub(uint16,MessageDispatcher.PoolId,address,bytes,uint128,uint256,
        address).selector ? 20
    : f.selector == sig:sendUpdateManager(uint16,MessageDispatcher.PoolId,MessageDispatcher.ManagerKind,bytes32,bool,
        address).selector ? 21
    : f.selector == sig:sendSetPolicy(uint16,MessageDispatcher.PoolId,bytes32,address).selector ? 22
    : f.selector == sig:sendAuthorizeSpokeCall(uint16,MessageDispatcher.PoolId,bytes,address).selector ? 23
    : f.selector == sig:sendUnauthorizeSpokeCall(uint16,MessageDispatcher.PoolId,bytes,address).selector ? 24
    : 0;

// SCOPE: only messages within the gateway's length cap are measured.
definition GATEWAY_MAX_LENGTH_MD() returns mathint = 1000;
