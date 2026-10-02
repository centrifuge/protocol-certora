// MessageDispatcher. High level: where each send goes, and what a rewiring writes.

import "../setup/MessageDispatcher_single.spec";

// MD-HL-01: a pool notification for this network is handled locally, otherwise sent cross-chain.
rule hlMdNotifyPoolRoutesByDestination(env e, uint16 cid, MessageDispatcher.PoolId poolId, address refund) {

    setupMessageDispatcher(e);

    bool local = cid == _MessageDispatcher.localCentrifugeId();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyPool(e, cid, poolId, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "a pool notice for this network is handled here once, never sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore,
        "a pool notice for another network is sent once, never handled here");
}

// MD-HL-02: the local hub gets asset updates for its own pools; others are sent cross-chain.
rule hlMdUpdateAssetsRoutesByThePoolsHubChain(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, ISpokeMessageSender.UpdateData data,
    uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = poolId / 2^48 == _MessageDispatcher.localCentrifugeId();
    mathint localCallsBefore = ghostHhCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateAssets(e, poolId, scId, assetId, data, extraGasLimit, refund);

    mathint localCallsAfter = ghostHhCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "an asset report to a local hub is handled here once, never sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore,
        "an asset report to a remote hub is sent once, never handled here");
}

// MD-HL-03: a share transfer to this network is executed locally, otherwise sent cross-chain.
rule hlMdExecuteTransferSharesRoutesByTheTargetChain(env e, uint16 originCid, uint16 targetCid,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, bytes32 receiver, uint128 amount,
    uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = targetCid == _MessageDispatcher.localCentrifugeId();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendExecuteTransferShares(e, originCid, targetCid, poolId, scId, receiver, amount,
        extraGasLimit, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "a share transfer to this network runs here once, never sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore,
        "a share transfer to another network is sent once, never run here");
}

// MD-HL-04: a local manager update reaches the spoke, adapter or gateway contract it is for.
rule hlMdLocalManagerUpdateReachesTheContractOfItsKind(env e, uint16 cid, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ManagerKind kind, bytes32 who, bool canManage, address refund) {

    setupMessageDispatcher(e);

    bool local = cid == _MessageDispatcher.localCentrifugeId();
    address spokeBefore = _MessageDispatcher.spokeHandler();
    address adapterBefore = _MessageDispatcher.multiAdapter();
    address gatewayBefore = _MessageDispatcher.gateway();

    _MessageDispatcher.sendUpdateManager(e, cid, poolId, kind, who, canManage, refund);

    address calleeAfter = ghostShLastCallee;

    assert(local && kind == MessageDispatcher.ManagerKind.Spoke => calleeAfter == spokeBefore,
        "a local spoke manager update reaches the spoke handler");
    assert(local && kind == MessageDispatcher.ManagerKind.Adapter => calleeAfter == adapterBefore,
        "a local adapter manager update reaches the multi-adapter");
    assert(local && kind == MessageDispatcher.ManagerKind.Gateway => calleeAfter == gatewayBefore,
        "a local gateway manager update reaches the gateway");
}

// MD-HL-05: a configuration update sets only the routing address it names.
rule hlMdFileRepointsOnlyTheNamedSlot(env e, bytes32 what, address data) {

    setupMessageDispatcher(e);

    address envoyBefore = _MessageDispatcher.envoy();
    address gatewayBefore = _MessageDispatcher.gateway();
    address adapterBefore = _MessageDispatcher.multiAdapter();
    address spokeBefore = _MessageDispatcher.spokeHandler();
    address hubBefore = _MessageDispatcher.hubHandler();

    _MessageDispatcher.file(e, what, data);

    assert(_MessageDispatcher.envoy() == (what == FILE_ENVOY_MD_CVL() ? data : envoyBefore)
        && _MessageDispatcher.gateway() == (what == FILE_GATEWAY_MD_CVL() ? data : gatewayBefore)
        && _MessageDispatcher.multiAdapter() == (what == FILE_MULTI_ADAPTER_MD_CVL() ? data : adapterBefore)
        && _MessageDispatcher.spokeHandler() == (what == FILE_SPOKE_HANDLER_MD_CVL() ? data : spokeBefore)
        && _MessageDispatcher.hubHandler() == (what == FILE_HUB_HANDLER_MD_CVL() ? data : hubBefore),
        "a rewiring sets exactly the pointer it names and no other");
}

// MD-HL-06: every completed send reaches exactly one destination, a local handler or the gateway.
rule hlMdEachSendReachesExactlyOneNeighbour(env e, method f, calldataarg args)
    filtered { f -> SEND_ENTRY_MD(f) } {

    setupMessageDispatcher(e);

    mathint callsBefore = DOWNSTREAM_CALLS();

    f(e, args);

    assert(DOWNSTREAM_CALLS() == callsBefore + 1, "a send makes exactly one downstream call");
}

// MD-HL-07: a share class announcement for this network is handled here, otherwise sent once to that network.
rule hlMdNotifyShareClassRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.ShareClassMetadata metadata, bytes32 salt,
    bytes32 registrar, bytes payload, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyShareClass(e, centrifugeId, poolId, scId, metadata, salt, registrar, payload,
        extraGasLimit, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-08: a share metadata update for this network is handled here, otherwise sent once to that network.
rule hlMdNotifyShareMetadataRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, string name, string symbol, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyShareMetadata(e, centrifugeId, poolId, scId, name, symbol, extraGasLimit, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-09: a share price update for this network is handled here, otherwise sent once to that network.
rule hlMdNotifyPricePoolPerShareRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.D18 pricePoolPerShare, uint64 computedAt,
    address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyPricePoolPerShare(e, centrifugeId, poolId, scId, pricePoolPerShare, computedAt,
        refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-10: an asset price update for a local asset is handled here, otherwise sent once to the asset's network.
rule hlMdNotifyPricePoolPerAssetRoutesByTheAssetsChain(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, MessageDispatcher.D18 pricePoolPerAsset,
    address refund) {

    setupMessageDispatcher(e);

    bool local = assetId / 2^112 == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyPricePoolPerAsset(e, poolId, scId, assetId, pricePoolPerAsset, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == assetId / 2^112 && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the asset's network, no local call");
}

// MD-HL-11: a transfer restriction update for this network is handled here, otherwise sent once to that network.
rule hlMdUpdateRestrictionRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, bytes payload, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateRestriction(e, centrifugeId, poolId, scId, payload, extraGasLimit, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-12: a hub manager call for this network is handled here, otherwise sent once to that network.
rule hlMdManagerCallFromHubRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    address target, bytes payload, uint128 extraGasLimit, uint256 value, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostEnCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendManagerCallFromHub(e, centrifugeId, poolId, target, payload, extraGasLimit, value,
        refund);

    mathint localCallsAfter = ghostEnCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the envoy is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-13: a vault update for a local asset is handled here, otherwise sent once to the asset's network.
rule hlMdUpdateVaultRoutesByTheAssetsChain(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, bytes32 vaultOrFactory,
    MessageDispatcher.VaultUpdateKind kind, bytes payload, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = assetId / 2^112 == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateVault(e, poolId, scId, assetId, vaultOrFactory, kind, payload, extraGasLimit,
        refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == assetId / 2^112 && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the asset's network, no local call");
}

// MD-HL-14: a request manager change for this network is handled here, otherwise sent once to that network.
rule hlMdSetRequestManagerRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes32 manager, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendSetRequestManager(e, centrifugeId, poolId, manager, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-15: a spoke call authorization for this network is handled here, otherwise sent once to that network.
rule hlMdAuthorizeSpokeCallRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes data, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendAuthorizeSpokeCall(e, centrifugeId, poolId, data, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-16: a spoke call revocation for this network is handled here, otherwise sent once to that network.
rule hlMdUnauthorizeSpokeCallRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes data, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUnauthorizeSpokeCall(e, centrifugeId, poolId, data, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-17: a policy change for this network is handled here, otherwise sent once to that network.
rule hlMdSetPolicyRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId, bytes32 policy,
    address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendSetPolicy(e, centrifugeId, poolId, policy, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-18: a manager update for this network is handled here, otherwise sent once to that network.
rule hlMdUpdateManagerRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ManagerKind kind, bytes32 who, bool canManage, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateManager(e, centrifugeId, poolId, kind, who, canManage, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, a manager registry is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-19: an upgrade schedule for this network is handled here, otherwise sent once to that network.
rule hlMdScheduleUpgradeRoutesByDestination(env e, uint16 centrifugeId, bytes32 target, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostSaCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendScheduleUpgrade(e, centrifugeId, target, refund);

    mathint localCallsAfter = ghostSaCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the root is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-20: an upgrade cancellation for this network is handled here, otherwise sent once to that network.
rule hlMdCancelUpgradeRoutesByDestination(env e, uint16 centrifugeId, bytes32 target, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostSaCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendCancelUpgrade(e, centrifugeId, target, refund);

    mathint localCallsAfter = ghostSaCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the root is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-21: a share transfer start for a locally hubbed pool is handled here, else sent once to the pool's hub.
rule hlMdInitiateTransferSharesRoutesByThePoolsHubChain(env e, uint16 targetCentrifugeId,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, bytes32 sender, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = poolId / 2^48 == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostHhCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendInitiateTransferShares(e, targetCentrifugeId, poolId, scId, sender, receiver, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint localCallsAfter = ghostHhCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the hub handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == poolId / 2^48 && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the pool's hub network, no local call");
}

// MD-HL-22: a holding amount report for a locally hubbed pool is handled here, else sent once to the pool's hub.
rule hlMdUpdateHoldingAmountRoutesByThePoolsHubChain(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, ISpokeMessageSender.UpdateData data,
    MessageDispatcher.D18 price, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = poolId / 2^48 == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostHhCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateHoldingAmount(e, poolId, scId, assetId, data, price, extraGasLimit, refund);

    mathint localCallsAfter = ghostHhCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the hub handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == poolId / 2^48 && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the pool's hub network, no local call");
}

// MD-HL-23: a share supply report for a locally hubbed pool is handled here, else sent once to the pool's hub.
rule hlMdUpdateSharesRoutesByThePoolsHubChain(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, ISpokeMessageSender.UpdateData data, uint128 extraGasLimit,
    address refund) {

    setupMessageDispatcher(e);

    bool local = poolId / 2^48 == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostHhCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateShares(e, poolId, scId, data, extraGasLimit, refund);

    mathint localCallsAfter = ghostHhCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the hub handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == poolId / 2^48 && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the pool's hub network, no local call");
}

// MD-HL-24: an asset registration for this network is handled here, otherwise sent once to that network.
rule hlMdRegisterAssetRoutesByDestination(env e, uint16 centrifugeId, MessageDispatcher.AssetId assetId,
    uint8 decimals, address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostHhCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendRegisterAsset(e, centrifugeId, assetId, decimals, refund);

    mathint localCallsAfter = ghostHhCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the hub handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the named network, no local call");
}

// MD-HL-25: a request for a locally hubbed pool is handled here, else sent once to the pool's hub.
rule hlMdRequestRoutesByThePoolsHubChain(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, bytes payload, uint128 extraGasLimit,
    bool unpaidMode, address refund) {

    setupMessageDispatcher(e);

    bool local = poolId / 2^48 == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostHhCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendRequest(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);

    mathint localCallsAfter = ghostHhCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the hub handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == poolId / 2^48 && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the pool's hub network, no local call");
}

// MD-HL-26: a spoke manager call for a locally hubbed pool is handled here, else sent once to the pool's hub.
rule hlMdManagerCallFromSpokeRoutesByThePoolsHubChain(env e, MessageDispatcher.PoolId poolId, bytes32 target,
    bytes payload, bytes32 sender, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = poolId / 2^48 == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostEnCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendManagerCallFromSpoke(e, poolId, target, payload, sender, extraGasLimit, refund);

    mathint localCallsAfter = ghostEnCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the envoy is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == poolId / 2^48 && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the pool's hub network, no local call");
}

// MD-HL-27: a request callback for a local asset is handled here, otherwise sent once to the asset's network.
rule hlMdRequestCallbackRoutesByTheAssetsChain(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, bytes payload, uint128 extraGasLimit,
    bool unpaidMode, address refund) {

    setupMessageDispatcher(e);

    bool local = assetId / 2^112 == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendRequestCallback(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);

    mathint localCallsAfter = ghostShCallCount;
    mathint wireSendsAfter = ghostGwSendCount;

    assert(local => localCallsAfter == localCallsBefore + 1 && wireSendsAfter == wireSendsBefore,
        "if local, the spoke handler is called once and nothing is sent");
    assert(!local => wireSendsAfter == wireSendsBefore + 1 && localCallsAfter == localCallsBefore
            && ghostGwLastSendCid16 == assetId / 2^112 && ghostGwLastSendCallee == gatewayBefore,
        "if remote, one gateway send to the asset's network, no local call");
}

// MD-HL-28: an adapter set announcement is sent once, paid, via the gateway to its network, never handled here.
rule hlMdSetPoolAdaptersShipsPaidOverTheGatewayOnce(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes32[] adapters, uint8 threshold, uint16 targetSessionId, address refund) {

    setupMessageDispatcher(e);

    address gatewayBefore = _MessageDispatcher.gateway();
    mathint localCallsBefore = ghostShCallCount + ghostHhCallCount + ghostEnCallCount + ghostSaCallCount;
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendSetPoolAdapters(e, centrifugeId, poolId, adapters, threshold, targetSessionId, refund);

    assert(ghostGwSendCount == wireSendsBefore + 1 && !ghostGwLastSendUnpaid
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore
            && ghostShCallCount + ghostHhCallCount + ghostEnCallCount + ghostSaCallCount == localCallsBefore,
        "one paid gateway send to the named network and no local call");
}

// MD-HL-31: every message other than a request, a request callback or a share transfer travels paid.
rule hlMdOnlyRequestsCallbacksAndForwardedTransfersTravelUnpaid(env e, method f, calldataarg args)
    filtered { f -> SEND_ENTRY_MD(f)
        && f.selector != sig:sendRequest(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,bytes,uint128,bool,address).selector
        && f.selector != sig:sendRequestCallback(MessageDispatcher.PoolId,MessageDispatcher.ShareClassId,
            MessageDispatcher.AssetId,bytes,uint128,bool,address).selector
        && f.selector != sig:sendExecuteTransferShares(uint16,uint16,MessageDispatcher.PoolId,
            MessageDispatcher.ShareClassId,bytes32,uint128,uint128,address).selector } {

    setupMessageDispatcher(e);

    mathint wireSendsBefore = ghostGwSendCount;

    f(e, args);

    assert(ghostGwSendCount != wireSendsBefore => !ghostGwLastSendUnpaid, "every other send goes on the wire paid");
}

// MD-HL-32: a request or request callback sent cross-chain travels paid or unpaid as its caller chose.
rule hlMdRequestAndCallbackCarryTheCallersPaymentMode(env e, bool callback, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, bytes payload, uint128 extraGasLimit,
    bool unpaidMode, address refund) {

    setupMessageDispatcher(e);

    bool remote = callback ? assetId / 2^112 != _MessageDispatcher.localCentrifugeId()
        : poolId / 2^48 != _MessageDispatcher.localCentrifugeId();
    mathint wireSendsBefore = ghostGwSendCount;

    if (callback) {
        _MessageDispatcher.sendRequestCallback(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);
    } else {
        _MessageDispatcher.sendRequest(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);
    }

    assert(remote => ghostGwSendCount == wireSendsBefore + 1 && ghostGwLastSendUnpaid == unpaidMode,
        "the wire carries the payment mode the caller picked");
}

// MD-HL-33: a share transfer to another network travels unpaid exactly when it started elsewhere.
rule hlMdForwardedTransferRunsUnpaidExactlyWhenItArrivedFromElsewhere(env e, uint16 originCentrifugeId,
    uint16 targetCentrifugeId, MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId,
    bytes32 receiver, uint128 amount, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool remote = targetCentrifugeId != _MessageDispatcher.localCentrifugeId();
    bool forwarded = originCentrifugeId != _MessageDispatcher.localCentrifugeId();
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendExecuteTransferShares(e, originCentrifugeId, targetCentrifugeId, poolId, scId, receiver,
        amount, extraGasLimit, refund);

    assert(remote => ghostGwSendCount == wireSendsBefore + 1 && ghostGwLastSendUnpaid == forwarded,
        "unpaid exactly when the origin is not this network");
}

// MD-HL-34: a pool announcement for another network is sent through the gateway to that network.
rule hlMdNotifyPoolSendsToTheNamedChain(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    address refund) {

    setupMessageDispatcher(e);

    bool local = centrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendNotifyPool(e, centrifugeId, poolId, refund);

    assert(!local => ghostGwSendCount == wireSendsBefore + 1
            && ghostGwLastSendCid16 == centrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "a remote pool notice goes out once, addressed to its network");
}

// MD-HL-35: an asset report for a pool hubbed elsewhere is sent through the gateway to that hub.
rule hlMdUpdateAssetsSendsToThePoolsHubChain(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, ISpokeMessageSender.UpdateData data,
    uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = poolId / 2^48 == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendUpdateAssets(e, poolId, scId, assetId, data, extraGasLimit, refund);

    assert(!local => ghostGwSendCount == wireSendsBefore + 1
            && ghostGwLastSendCid16 == poolId / 2^48 && ghostGwLastSendCallee == gatewayBefore,
        "a remote asset report goes out once, to the pool's hub network");
}

// MD-HL-36: a share transfer to another network is sent through the gateway to that network.
rule hlMdExecuteTransferSharesSendsToTheTargetChain(env e, uint16 originCentrifugeId, uint16 targetCentrifugeId,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, bytes32 receiver, uint128 amount,
    uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = targetCentrifugeId == _MessageDispatcher.localCentrifugeId();
    address gatewayBefore = _MessageDispatcher.gateway();
    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendExecuteTransferShares(e, originCentrifugeId, targetCentrifugeId, poolId, scId, receiver,
        amount, extraGasLimit, refund);

    assert(!local => ghostGwSendCount == wireSendsBefore + 1
            && ghostGwLastSendCid16 == targetCentrifugeId && ghostGwLastSendCallee == gatewayBefore,
        "a remote transfer goes out once, addressed to its target");
}

// MD-HL-37: a local asset report reaches the hub handler with every field of the report intact.
rule hlMdLocalAssetReportCarriesTheFlushedNet(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, ISpokeMessageSender.UpdateData data,
    uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = poolId / 2^48 == _MessageDispatcher.localCentrifugeId();
    address hubBefore = _MessageDispatcher.hubHandler();
    mathint hubCallsBefore = ghostHhCallCount;

    _MessageDispatcher.sendUpdateAssets(e, poolId, scId, assetId, data, extraGasLimit, refund);

    assert(local => ghostHhCallCount == hubCallsBefore + 1 && ghostHhLastCallee == hubBefore
            && ghostHhLastSourceCid16 == _MessageDispatcher.localCentrifugeId()
            && ghostHhLastPoolId64 == poolId && ghostHhLastScId == scId && ghostHhLastAssetId128 == assetId
            && ghostHhLastAmount128 == data.netAmount && ghostHhLastIsIncrease == data.isIncrease
            && ghostHhLastIsSnapshot == data.isSnapshot && ghostHhLastNonce64 == data.nonce,
        "the hub gets this network, pool, class, asset, amount, flags and nonce");
}
