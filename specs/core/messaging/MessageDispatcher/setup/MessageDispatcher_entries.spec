// MessageDispatcher. Setup: the 25 send entries called with named arguments.

import "MessageDispatcher_base.spec";

definition POOL_MESSAGE_MD(method f) returns bool =
    f.selector != sig:sendScheduleUpgrade(uint16,bytes32,address).selector
        && f.selector != sig:sendCancelUpgrade(uint16,bytes32,address).selector
        && f.selector != sig:sendRegisterAsset(uint16,MessageDispatcher.AssetId,uint8,address).selector;

definition GAS_MESSAGE_MD(method f) returns bool =
    f.selector == sig:sendNotifyShareClass(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.ShareClassMetadata,bytes32,bytes32,bytes,uint128,address).selector
        || f.selector == sig:sendNotifyShareMetadata(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            string,string,uint128,address).selector
        || f.selector == sig:sendUpdateRestriction(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            bytes,uint128,address).selector
        || f.selector == sig:sendManagerCallFromHub(uint16,MessageDispatcher.PoolId,address,bytes,uint128,uint256,
            address).selector
        || f.selector == sig:sendUpdateVault(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,bytes32,MessageDispatcher.VaultUpdateKind,bytes,uint128,address).selector
        || f.selector == sig:sendInitiateTransferShares(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            bytes32,bytes32,uint128,uint128,uint128,address).selector
        || f.selector == sig:sendExecuteTransferShares(uint16,uint16,MessageDispatcher.PoolId,
            MessageDispatcher.ShareClassId,bytes32,uint128,uint128,address).selector
        || f.selector == sig:sendUpdateAssets(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,ISpokeMessageSender.UpdateData,uint128,address).selector
        || f.selector == sig:sendUpdateHoldingAmount(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,ISpokeMessageSender.UpdateData,MessageDispatcher.D18,uint128,address).selector
        || f.selector == sig:sendUpdateShares(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            ISpokeMessageSender.UpdateData,uint128,address).selector
        || f.selector == sig:sendRequest(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,bytes,uint128,bool,address).selector
        || f.selector == sig:sendManagerCallFromSpoke(MessageDispatcher.PoolId,bytes32,bytes,bytes32,uint128,
            address).selector
        || f.selector == sig:sendRequestCallback(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,bytes,uint128,bool,address).selector;

// Arguments shared by role: cid destination or origin, cid2 transfer target.
function callSendEntryMD(env e, method f, uint16 cid, uint16 cid2, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId,
    MessageDispatcher.ShareClassMetadata metadata, string name, string symbol, bytes32 word1, bytes32 word2,
    bytes payload, uint128 gas, uint128 gas2, uint128 amount, MessageDispatcher.D18 price, uint64 computedAt,
    address target, uint256 value, MessageDispatcher.VaultUpdateKind vaultKind,
    MessageDispatcher.ManagerKind managerKind, bool flag, ISpokeMessageSender.UpdateData data, uint8 small,
    bytes32[] adapters, uint16 sessionId, address refund) {

    if (f.selector == sig:sendNotifyPool(uint16,MessageDispatcher.PoolId,address).selector) {
        _MessageDispatcher.sendNotifyPool(e, cid, poolId, refund);
    } else if (f.selector == sig:sendNotifyShareClass(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.ShareClassMetadata,bytes32,bytes32,bytes,uint128,address).selector) {
        _MessageDispatcher.sendNotifyShareClass(e, cid, poolId, scId, metadata, word1, word2, payload, gas, refund);
    } else if (f.selector == sig:sendNotifyShareMetadata(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            string,string,uint128,address).selector) {
        _MessageDispatcher.sendNotifyShareMetadata(e, cid, poolId, scId, name, symbol, gas, refund);
    } else if (f.selector == sig:sendNotifyPricePoolPerShare(uint16,MessageDispatcher.PoolId,
            MessageDispatcher.ShareClassId,MessageDispatcher.D18,uint64,address).selector) {
        _MessageDispatcher.sendNotifyPricePoolPerShare(e, cid, poolId, scId, price, computedAt, refund);
    } else if (f.selector == sig:sendNotifyPricePoolPerAsset(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,MessageDispatcher.D18,address).selector) {
        _MessageDispatcher.sendNotifyPricePoolPerAsset(e, poolId, scId, assetId, price, refund);
    } else if (f.selector == sig:sendUpdateRestriction(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            bytes,uint128,address).selector) {
        _MessageDispatcher.sendUpdateRestriction(e, cid, poolId, scId, payload, gas, refund);
    } else if (f.selector == sig:sendManagerCallFromHub(uint16,MessageDispatcher.PoolId,address,bytes,uint128,uint256,
            address).selector) {
        _MessageDispatcher.sendManagerCallFromHub(e, cid, poolId, target, payload, gas, value, refund);
    } else if (f.selector == sig:sendUpdateVault(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,bytes32,MessageDispatcher.VaultUpdateKind,bytes,uint128,address).selector) {
        _MessageDispatcher.sendUpdateVault(e, poolId, scId, assetId, word1, vaultKind, payload, gas, refund);
    } else if (f.selector == sig:sendSetRequestManager(uint16,MessageDispatcher.PoolId,bytes32,address).selector) {
        _MessageDispatcher.sendSetRequestManager(e, cid, poolId, word1, refund);
    } else if (f.selector == sig:sendAuthorizeSpokeCall(uint16,MessageDispatcher.PoolId,bytes,address).selector) {
        _MessageDispatcher.sendAuthorizeSpokeCall(e, cid, poolId, payload, refund);
    } else if (f.selector == sig:sendUnauthorizeSpokeCall(uint16,MessageDispatcher.PoolId,bytes,address).selector) {
        _MessageDispatcher.sendUnauthorizeSpokeCall(e, cid, poolId, payload, refund);
    } else if (f.selector == sig:sendSetPolicy(uint16,MessageDispatcher.PoolId,bytes32,address).selector) {
        _MessageDispatcher.sendSetPolicy(e, cid, poolId, word1, refund);
    } else if (f.selector == sig:sendUpdateManager(uint16,MessageDispatcher.PoolId,MessageDispatcher.ManagerKind,
            bytes32,bool,address).selector) {
        _MessageDispatcher.sendUpdateManager(e, cid, poolId, managerKind, word1, flag, refund);
    } else if (f.selector == sig:sendScheduleUpgrade(uint16,bytes32,address).selector) {
        _MessageDispatcher.sendScheduleUpgrade(e, cid, word1, refund);
    } else if (f.selector == sig:sendCancelUpgrade(uint16,bytes32,address).selector) {
        _MessageDispatcher.sendCancelUpgrade(e, cid, word1, refund);
    } else if (f.selector == sig:sendInitiateTransferShares(uint16,MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            bytes32,bytes32,uint128,uint128,uint128,address).selector) {
        _MessageDispatcher.sendInitiateTransferShares(e, cid2, poolId, scId, word1, word2, amount, gas, gas2, refund);
    } else if (f.selector == sig:sendExecuteTransferShares(uint16,uint16,MessageDispatcher.PoolId,
            MessageDispatcher.ShareClassId,bytes32,uint128,uint128,address).selector) {
        _MessageDispatcher.sendExecuteTransferShares(e, cid, cid2, poolId, scId, word2, amount, gas, refund);
    } else if (f.selector == sig:sendUpdateAssets(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,ISpokeMessageSender.UpdateData,uint128,address).selector) {
        _MessageDispatcher.sendUpdateAssets(e, poolId, scId, assetId, data, gas, refund);
    } else if (f.selector == sig:sendUpdateHoldingAmount(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,ISpokeMessageSender.UpdateData,MessageDispatcher.D18,uint128,address).selector) {
        _MessageDispatcher.sendUpdateHoldingAmount(e, poolId, scId, assetId, data, price, gas, refund);
    } else if (f.selector == sig:sendUpdateShares(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            ISpokeMessageSender.UpdateData,uint128,address).selector) {
        _MessageDispatcher.sendUpdateShares(e, poolId, scId, data, gas, refund);
    } else if (f.selector == sig:sendRegisterAsset(uint16,MessageDispatcher.AssetId,uint8,address).selector) {
        _MessageDispatcher.sendRegisterAsset(e, cid, assetId, small, refund);
    } else if (f.selector == sig:sendRequest(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,bytes,uint128,bool,address).selector) {
        _MessageDispatcher.sendRequest(e, poolId, scId, assetId, payload, gas, flag, refund);
    } else if (f.selector == sig:sendManagerCallFromSpoke(MessageDispatcher.PoolId,bytes32,bytes,bytes32,uint128,
            address).selector) {
        _MessageDispatcher.sendManagerCallFromSpoke(e, poolId, word1, payload, word2, gas, refund);
    } else if (f.selector == sig:sendRequestCallback(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,bytes,uint128,bool,address).selector) {
        _MessageDispatcher.sendRequestCallback(e, poolId, scId, assetId, payload, gas, flag, refund);
    } else if (f.selector == sig:sendSetPoolAdapters(uint16,MessageDispatcher.PoolId,bytes32[],uint8,uint16,
            address).selector) {
        _MessageDispatcher.sendSetPoolAdapters(e, cid, poolId, adapters, small, sessionId, refund);
    } else {
        require(false, "SAFE: only the 25 send entries reach here");
    }
}
