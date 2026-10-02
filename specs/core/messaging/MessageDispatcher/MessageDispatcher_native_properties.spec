import "setup/MessageDispatcher_native.spec";

// --- high_level ---

// MD-HL-29: a send keeps none of the ETH it is paid, so the dispatcher's balance never grows.
rule hlMdKeepsNoneOfTheValueItIsHanded(env e, method f, uint16 cid, uint16 cid2, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId,
    MessageDispatcher.ShareClassMetadata metadata, string name, string symbol, bytes32 word1, bytes32 word2,
    bytes payload, uint128 gas, uint128 gas2, uint128 amount, MessageDispatcher.D18 price, uint64 computedAt,
    address target, uint256 value, MessageDispatcher.VaultUpdateKind vaultKind,
    MessageDispatcher.ManagerKind managerKind, bool flag, ISpokeMessageSender.UpdateData data, uint8 small,
    bytes32[] adapters, uint16 sessionId, address refund)
    filtered { f -> SEND_ENTRY_MD(f) } {

    setupMessageDispatcherNative(e, refund);

    mathint heldBefore = nativeBalances[_MessageDispatcher];

    callSendEntryMD(e, f, cid, cid2, poolId, scId, assetId, metadata, name, symbol, word1, word2, payload, gas, gas2,
        amount, price, computedAt, target, value, vaultKind, managerKind, flag, data, small, adapters, sessionId,
        refund);

    assert(nativeBalances[_MessageDispatcher] <= heldBefore,
        "the dispatcher holds no more ETH after a send than before it");
}

// MD-HL-30: a holding amount report behaves exactly like an asset report, whatever price it carries.
rule hlMdHoldingAmountShimActsAsUpdateAssetsForAnyPrice(env e, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId, ISpokeMessageSender.UpdateData data,
    MessageDispatcher.D18 price, uint128 extraGasLimit, address refund) {

    setupMessageDispatcherNative(e, refund);

    storage init = lastStorage;
    mathint hubCalls0 = ghostHhCallCount;
    mathint wireSends0 = ghostGwSendCount;

    _MessageDispatcher.sendUpdateHoldingAmount@withrevert(e, poolId, scId, assetId, data, price, extraGasLimit,
        refund);
    bool shimReverted = lastReverted;
    mathint hubCalls1 = ghostHhCallCount;
    mathint wireSends1 = ghostGwSendCount;
    address hubCallee = ghostHhLastCallee;
    mathint hubCid = ghostHhLastSourceCid16;
    mathint hubPool = ghostHhLastPoolId64;
    bytes16 hubScId = ghostHhLastScId;
    mathint hubAsset = ghostHhLastAssetId128;
    mathint hubAmount = ghostHhLastAmount128;
    bool hubIncrease = ghostHhLastIsIncrease;
    bool hubSnapshot = ghostHhLastIsSnapshot;
    mathint hubNonce = ghostHhLastNonce64;
    mathint hubValue = ghostHhLastValue;
    address wireCallee = ghostGwLastSendCallee;
    mathint wireCid = ghostGwLastSendCid16;
    bool wireUnpaid = ghostGwLastSendUnpaid;
    address wireRefund = ghostGwLastSendRefund;
    mathint wireValue = ghostGwLastSendValue;
    bytes32 wireHash = ghostGwLastSendHash;
    mathint shimHeld = nativeBalances[_MessageDispatcher];
    mathint shimRefunded = nativeBalances[refund];
    mathint shimPayer = nativeBalances[e.msg.sender];

    _MessageDispatcher.sendUpdateAssets@withrevert(e, poolId, scId, assetId, data, extraGasLimit, refund) at init;
    bool reportReverted = lastReverted;

    assert(shimReverted == reportReverted
            && ghostHhCallCount - hubCalls1 == hubCalls1 - hubCalls0
            && ghostGwSendCount - wireSends1 == wireSends1 - wireSends0,
        "both calls fail together and make as many hub and gateway calls");
    assert(hubCalls1 == hubCalls0 + 1 => ghostHhLastCallee == hubCallee && ghostHhLastSourceCid16 == hubCid
            && ghostHhLastPoolId64 == hubPool && ghostHhLastScId == hubScId && ghostHhLastAssetId128 == hubAsset
            && ghostHhLastAmount128 == hubAmount && ghostHhLastIsIncrease == hubIncrease
            && ghostHhLastIsSnapshot == hubSnapshot && ghostHhLastNonce64 == hubNonce && ghostHhLastValue == hubValue,
        "locally, the hub handler receives the same report from both");
    assert(wireSends1 == wireSends0 + 1 => ghostGwLastSendCallee == wireCallee && ghostGwLastSendCid16 == wireCid
            && ghostGwLastSendUnpaid == wireUnpaid && ghostGwLastSendRefund == wireRefund
            && ghostGwLastSendValue == wireValue && ghostGwLastSendHash == wireHash,
        "remotely, both put the same message on the wire, paid alike");
    assert(nativeBalances[_MessageDispatcher] == shimHeld && nativeBalances[refund] == shimRefunded
            && nativeBalances[e.msg.sender] == shimPayer,
        "both leave the dispatcher, refund and payer balances equal");
}
