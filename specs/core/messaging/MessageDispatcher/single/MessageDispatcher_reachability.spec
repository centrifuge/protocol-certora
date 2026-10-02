// MessageDispatcher. Reachability: every route a send may take can complete.

import "../setup/MessageDispatcher_single.spec";

// MD-RC-01: a pool announcement for this network can be handled by the local spoke handler.
rule rcMdNotifyPoolLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendNotifyPool(e, centrifugeId, poolId, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the pool announcement");
}

// MD-RC-02: a pool announcement for another network can be sent cross-chain.
rule rcMdNotifyPoolRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyPool(e, centrifugeId, poolId, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the pool announcement can go out through the gateway");
}

// MD-RC-03: a share class announcement for this network can be handled by the local spoke handler.
rule rcMdNotifyShareClassLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.ShareClassMetadata metadata, bytes32 salt,
    bytes32 registrar, bytes payload, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendNotifyShareClass(e, centrifugeId, poolId, scId, metadata, salt, registrar, payload,
        extraGasLimit, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the share class announcement");
}

// MD-RC-04: a share class announcement for another network can be sent cross-chain.
rule rcMdNotifyShareClassRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.ShareClassMetadata metadata, bytes32 salt,
    bytes32 registrar, bytes payload, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyShareClass(e, centrifugeId, poolId, scId, metadata, salt, registrar, payload,
        extraGasLimit, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the share class announcement can go out through the gateway");
}

// MD-RC-05: a share metadata update for this network can be handled by the local spoke handler.
rule rcMdNotifyShareMetadataLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, string name, string symbol, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendNotifyShareMetadata(e, centrifugeId, poolId, scId, name, symbol, extraGasLimit, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the share metadata update");
}

// MD-RC-06: a share metadata update for another network can be sent cross-chain.
rule rcMdNotifyShareMetadataRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, string name, string symbol, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyShareMetadata(e, centrifugeId, poolId, scId, name, symbol, extraGasLimit, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the share metadata update can go out through the gateway");
}

// MD-RC-07: a share price update for this network can be handled by the local spoke handler.
rule rcMdNotifyPricePoolPerShareLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.D18 pricePoolPerShare, uint64 computedAt,
    address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendNotifyPricePoolPerShare(e, centrifugeId, poolId, scId, pricePoolPerShare, computedAt,
        refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the share price update");
}

// MD-RC-08: a share price update for another network can be sent cross-chain.
rule rcMdNotifyPricePoolPerShareRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.D18 pricePoolPerShare, uint64 computedAt,
    address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyPricePoolPerShare(e, centrifugeId, poolId, scId, pricePoolPerShare, computedAt,
        refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the share price update can go out through the gateway");
}

// MD-RC-09: an asset price update for a local asset can be handled by the local spoke handler.
rule rcMdNotifyPricePoolPerAssetLocalLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, MessageDispatcher.D18 pricePoolPerAsset,
    address refund) {

    setupMessageDispatcher(e);
    require(assetId / 2^112 == _MessageDispatcher.localCentrifugeId(), "SCOPE: the asset is on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendNotifyPricePoolPerAsset(e, poolId, scId, assetId, pricePoolPerAsset, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the asset price update");
}

// MD-RC-10: an asset price update for an asset of another network can be sent cross-chain.
rule rcMdNotifyPricePoolPerAssetRemoteLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, MessageDispatcher.D18 pricePoolPerAsset,
    address refund) {

    setupMessageDispatcher(e);
    require(assetId / 2^112 != _MessageDispatcher.localCentrifugeId(), "SCOPE: the asset is on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyPricePoolPerAsset(e, poolId, scId, assetId, pricePoolPerAsset, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the asset price update can go out through the gateway");
}

// MD-RC-11: a transfer restriction update for this network can be handled by the local spoke handler.
rule rcMdUpdateRestrictionLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, bytes payload, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendUpdateRestriction(e, centrifugeId, poolId, scId, payload, extraGasLimit, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1,
        "the spoke handler here can take the transfer restriction update");
}

// MD-RC-12: a transfer restriction update for another network can be sent cross-chain.
rule rcMdUpdateRestrictionRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, bytes payload, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateRestriction(e, centrifugeId, poolId, scId, payload, extraGasLimit, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the transfer restriction update can go out through the gateway");
}

// MD-RC-13: a hub manager call for this network can be handled by the local envoy.
rule rcMdManagerCallFromHubLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    address target, bytes payload, uint128 extraGasLimit, uint256 value, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostEnCallCount;

    _MessageDispatcher.sendManagerCallFromHub(e, centrifugeId, poolId, target, payload, extraGasLimit, value,
        refund);

    satisfy(ghostEnCallCount == localCallsBefore + 1, "the envoy here can take the hub manager call");
}

// MD-RC-14: a hub manager call for another network can be sent cross-chain.
rule rcMdManagerCallFromHubRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    address target, bytes payload, uint128 extraGasLimit, uint256 value, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendManagerCallFromHub(e, centrifugeId, poolId, target, payload, extraGasLimit, value,
        refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the hub manager call can go out through the gateway");
}

// MD-RC-15: a vault update for a local asset can be handled by the local spoke handler.
rule rcMdUpdateVaultLocalLegIsReachable(env e, MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId,
    MessageDispatcher.AssetId assetId, bytes32 vaultOrFactory, MessageDispatcher.VaultUpdateKind kind,
    bytes payload, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(assetId / 2^112 == _MessageDispatcher.localCentrifugeId(), "SCOPE: the asset is on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendUpdateVault(e, poolId, scId, assetId, vaultOrFactory, kind, payload, extraGasLimit,
        refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the vault update");
}

// MD-RC-16: a vault update for an asset of another network can be sent cross-chain.
rule rcMdUpdateVaultRemoteLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, bytes32 vaultOrFactory,
    MessageDispatcher.VaultUpdateKind kind, bytes payload, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(assetId / 2^112 != _MessageDispatcher.localCentrifugeId(), "SCOPE: the asset is on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateVault(e, poolId, scId, assetId, vaultOrFactory, kind, payload, extraGasLimit,
        refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the vault update can go out through the gateway");
}

// MD-RC-17: a request manager change for this network can be handled by the local spoke handler.
rule rcMdSetRequestManagerLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes32 manager, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendSetRequestManager(e, centrifugeId, poolId, manager, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the request manager change");
}

// MD-RC-18: a request manager change for another network can be sent cross-chain.
rule rcMdSetRequestManagerRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes32 manager, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendSetRequestManager(e, centrifugeId, poolId, manager, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the request manager change can go out through the gateway");
}

// MD-RC-19: a spoke call authorization for this network can be handled by the local spoke handler.
rule rcMdAuthorizeSpokeCallLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes data, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendAuthorizeSpokeCall(e, centrifugeId, poolId, data, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the spoke call authorization");
}

// MD-RC-20: a spoke call authorization for another network can be sent cross-chain.
rule rcMdAuthorizeSpokeCallRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes data, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendAuthorizeSpokeCall(e, centrifugeId, poolId, data, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the spoke call authorization can go out through the gateway");
}

// MD-RC-21: a spoke call revocation for this network can be handled by the local spoke handler.
rule rcMdUnauthorizeSpokeCallLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes data, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendUnauthorizeSpokeCall(e, centrifugeId, poolId, data, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the spoke call revocation");
}

// MD-RC-22: a spoke call revocation for another network can be sent cross-chain.
rule rcMdUnauthorizeSpokeCallRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes data, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUnauthorizeSpokeCall(e, centrifugeId, poolId, data, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the spoke call revocation can go out through the gateway");
}

// MD-RC-23: a policy change for this network can be handled by the local spoke handler.
rule rcMdSetPolicyLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId, bytes32 policy,
    address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendSetPolicy(e, centrifugeId, poolId, policy, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the policy change");
}

// MD-RC-24: a policy change for another network can be sent cross-chain.
rule rcMdSetPolicyRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId, bytes32 policy,
    address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendSetPolicy(e, centrifugeId, poolId, policy, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the policy change can go out through the gateway");
}

// MD-RC-25: a manager update for this network can be handled by the local manager registry.
rule rcMdUpdateManagerLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ManagerKind kind, bytes32 who, bool canManage, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendUpdateManager(e, centrifugeId, poolId, kind, who, canManage, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the manager registry here can take the manager update");
}

// MD-RC-26: a manager update for another network can be sent cross-chain.
rule rcMdUpdateManagerRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ManagerKind kind, bytes32 who, bool canManage, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateManager(e, centrifugeId, poolId, kind, who, canManage, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the manager update can go out through the gateway");
}

// MD-RC-27: an upgrade schedule for this network can be handled by the local root.
rule rcMdScheduleUpgradeLocalLegIsReachable(env e, uint16 centrifugeId, bytes32 target, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostSaCallCount;

    _MessageDispatcher.sendScheduleUpgrade(e, centrifugeId, target, refund);

    satisfy(ghostSaCallCount == localCallsBefore + 1, "the root here can take the upgrade schedule");
}

// MD-RC-28: an upgrade schedule for another network can be sent cross-chain.
rule rcMdScheduleUpgradeRemoteLegIsReachable(env e, uint16 centrifugeId, bytes32 target, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendScheduleUpgrade(e, centrifugeId, target, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the upgrade schedule can go out through the gateway");
}

// MD-RC-29: an upgrade cancellation for this network can be handled by the local root.
rule rcMdCancelUpgradeLocalLegIsReachable(env e, uint16 centrifugeId, bytes32 target, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostSaCallCount;

    _MessageDispatcher.sendCancelUpgrade(e, centrifugeId, target, refund);

    satisfy(ghostSaCallCount == localCallsBefore + 1, "the root here can take the upgrade cancellation");
}

// MD-RC-30: an upgrade cancellation for another network can be sent cross-chain.
rule rcMdCancelUpgradeRemoteLegIsReachable(env e, uint16 centrifugeId, bytes32 target, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendCancelUpgrade(e, centrifugeId, target, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the upgrade cancellation can go out through the gateway");
}

// MD-RC-31: a share transfer start for a locally hubbed pool can be handled by the local hub handler.
rule rcMdInitiateTransferSharesLocalLegIsReachable(env e, uint16 targetCentrifugeId,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, bytes32 sender, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 == _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on this network");

    mathint localCallsBefore = ghostHhCallCount;

    _MessageDispatcher.sendInitiateTransferShares(e, targetCentrifugeId, poolId, scId, sender, receiver, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    satisfy(ghostHhCallCount == localCallsBefore + 1, "the hub handler here can take the share transfer start");
}

// MD-RC-32: a share transfer start for a pool hubbed elsewhere can be sent cross-chain.
rule rcMdInitiateTransferSharesRemoteLegIsReachable(env e, uint16 targetCentrifugeId,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, bytes32 sender, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 != _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendInitiateTransferShares(e, targetCentrifugeId, poolId, scId, sender, receiver, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the share transfer start can go out through the gateway");
}

// MD-RC-33: a share transfer to this network can be handled by the local spoke handler.
rule rcMdExecuteTransferSharesLocalLegIsReachable(env e, uint16 originCentrifugeId, uint16 targetCentrifugeId,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, bytes32 receiver, uint128 amount,
    uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(targetCentrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendExecuteTransferShares(e, originCentrifugeId, targetCentrifugeId, poolId, scId, receiver,
        amount, extraGasLimit, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the share transfer");
}

// MD-RC-34: a share transfer to another network can be sent cross-chain.
rule rcMdExecuteTransferSharesRemoteLegIsReachable(env e, uint16 originCentrifugeId, uint16 targetCentrifugeId,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, bytes32 receiver, uint128 amount,
    uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(targetCentrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendExecuteTransferShares(e, originCentrifugeId, targetCentrifugeId, poolId, scId, receiver,
        amount, extraGasLimit, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the share transfer can go out through the gateway");
}

// MD-RC-35: an asset report for a locally hubbed pool can be handled by the local hub handler.
rule rcMdUpdateAssetsLocalLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, ISpokeMessageSender.UpdateData data,
    uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 == _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on this network");

    mathint localCallsBefore = ghostHhCallCount;

    _MessageDispatcher.sendUpdateAssets(e, poolId, scId, assetId, data, extraGasLimit, refund);

    satisfy(ghostHhCallCount == localCallsBefore + 1, "the hub handler here can take the asset report");
}

// MD-RC-36: an asset report for a pool hubbed elsewhere can be sent cross-chain.
rule rcMdUpdateAssetsRemoteLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, ISpokeMessageSender.UpdateData data,
    uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 != _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateAssets(e, poolId, scId, assetId, data, extraGasLimit, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the asset report can go out through the gateway");
}

// MD-RC-37: a holding amount report for a locally hubbed pool can be handled by the local hub handler.
rule rcMdUpdateHoldingAmountLocalLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, ISpokeMessageSender.UpdateData data,
    MessageDispatcher.D18 price, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 == _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on this network");

    mathint localCallsBefore = ghostHhCallCount;

    _MessageDispatcher.sendUpdateHoldingAmount(e, poolId, scId, assetId, data, price, extraGasLimit, refund);

    satisfy(ghostHhCallCount == localCallsBefore + 1, "the hub handler here can take the holding amount report");
}

// MD-RC-38: a holding amount report for a pool hubbed elsewhere can be sent cross-chain.
rule rcMdUpdateHoldingAmountRemoteLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, ISpokeMessageSender.UpdateData data,
    MessageDispatcher.D18 price, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 != _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateHoldingAmount(e, poolId, scId, assetId, data, price, extraGasLimit, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the holding amount report can go out through the gateway");
}

// MD-RC-39: a share supply report for a locally hubbed pool can be handled by the local hub handler.
rule rcMdUpdateSharesLocalLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, ISpokeMessageSender.UpdateData data, uint128 extraGasLimit,
    address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 == _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on this network");

    mathint localCallsBefore = ghostHhCallCount;

    _MessageDispatcher.sendUpdateShares(e, poolId, scId, data, extraGasLimit, refund);

    satisfy(ghostHhCallCount == localCallsBefore + 1, "the hub handler here can take the share supply report");
}

// MD-RC-40: a share supply report for a pool hubbed elsewhere can be sent cross-chain.
rule rcMdUpdateSharesRemoteLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, ISpokeMessageSender.UpdateData data, uint128 extraGasLimit,
    address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 != _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateShares(e, poolId, scId, data, extraGasLimit, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the share supply report can go out through the gateway");
}

// MD-RC-41: an asset registration for this network can be handled by the local hub handler.
rule rcMdRegisterAssetLocalLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.AssetId assetId,
    uint8 decimals, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId == _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on this network");

    mathint localCallsBefore = ghostHhCallCount;

    _MessageDispatcher.sendRegisterAsset(e, centrifugeId, assetId, decimals, refund);

    satisfy(ghostHhCallCount == localCallsBefore + 1, "the hub handler here can take the asset registration");
}

// MD-RC-42: an asset registration for another network can be sent cross-chain.
rule rcMdRegisterAssetRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.AssetId assetId,
    uint8 decimals, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendRegisterAsset(e, centrifugeId, assetId, decimals, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the asset registration can go out through the gateway");
}

// MD-RC-43: a request for a locally hubbed pool can be handled by the local hub handler.
rule rcMdRequestLocalLegIsReachable(env e, MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId,
    MessageDispatcher.AssetId assetId, bytes payload, uint128 extraGasLimit, bool unpaidMode, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 == _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on this network");

    mathint localCallsBefore = ghostHhCallCount;

    _MessageDispatcher.sendRequest(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);

    satisfy(ghostHhCallCount == localCallsBefore + 1, "the hub handler here can take the request");
}

// MD-RC-44: a request for a pool hubbed elsewhere can be sent cross-chain.
rule rcMdRequestRemoteLegIsReachable(env e, MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId,
    MessageDispatcher.AssetId assetId, bytes payload, uint128 extraGasLimit, bool unpaidMode, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 != _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendRequest(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the request can go out through the gateway");
}

// MD-RC-45: a spoke manager call for a locally hubbed pool can be handled by the local envoy.
rule rcMdManagerCallFromSpokeLocalLegIsReachable(env e, MessageDispatcher.PoolId poolId, bytes32 target,
    bytes payload, bytes32 sender, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 == _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on this network");

    mathint localCallsBefore = ghostEnCallCount;

    _MessageDispatcher.sendManagerCallFromSpoke(e, poolId, target, payload, sender, extraGasLimit, refund);

    satisfy(ghostEnCallCount == localCallsBefore + 1, "the envoy here can take the spoke manager call");
}

// MD-RC-46: a spoke manager call for a pool hubbed elsewhere can be sent cross-chain.
rule rcMdManagerCallFromSpokeRemoteLegIsReachable(env e, MessageDispatcher.PoolId poolId, bytes32 target,
    bytes payload, bytes32 sender, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);
    require(poolId / 2^48 != _MessageDispatcher.localCentrifugeId(), "SCOPE: the pool's hub is on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendManagerCallFromSpoke(e, poolId, target, payload, sender, extraGasLimit, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the spoke manager call can go out through the gateway");
}

// MD-RC-47: a request callback for a local asset can be handled by the local spoke handler.
rule rcMdRequestCallbackLocalLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, bytes payload, uint128 extraGasLimit,
    bool unpaidMode, address refund) {

    setupMessageDispatcher(e);
    require(assetId / 2^112 == _MessageDispatcher.localCentrifugeId(), "SCOPE: the asset is on this network");

    mathint localCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendRequestCallback(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);

    satisfy(ghostShCallCount == localCallsBefore + 1, "the spoke handler here can take the request callback");
}

// MD-RC-48: a request callback for an asset of another network can be sent cross-chain.
rule rcMdRequestCallbackRemoteLegIsReachable(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, bytes payload, uint128 extraGasLimit,
    bool unpaidMode, address refund) {

    setupMessageDispatcher(e);
    require(assetId / 2^112 != _MessageDispatcher.localCentrifugeId(), "SCOPE: the asset is on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendRequestCallback(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the request callback can go out through the gateway");
}

// MD-RC-49: an adapter set announcement for another network can be sent cross-chain.
rule rcMdSetPoolAdaptersRemoteLegIsReachable(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes32[] adapters, uint8 threshold, uint16 targetSessionId, address refund) {

    setupMessageDispatcher(e);
    require(centrifugeId != _MessageDispatcher.localCentrifugeId(), "SCOPE: a destination on another network");

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendSetPoolAdapters(e, centrifugeId, poolId, adapters, threshold, targetSessionId, refund);

    satisfy(ghostGwSendCount == wireSendsBefore + 1, "the adapter set announcement can go out through the gateway");
}
