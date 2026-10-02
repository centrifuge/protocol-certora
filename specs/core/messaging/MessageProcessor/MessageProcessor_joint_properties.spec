import "setup/MessageProcessor_joint.spec";

// --- reachability ---

// MP-RC-02: a share transfer can reach the hub handler with a different refund address locally than by message.
rule rcMpLocalAndRoundTripTransferInitiationHandDifferentRefunds(env eDispatch, env eProcess, uint16 targetCid,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, bytes32 sender, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupMessageProcessorJoint(eDispatch, eProcess);

    uint16 localCid = _MessageDispatcher.localCentrifugeId();
    require(poolId / 2^48 == localCid, "SCOPE: a pool hubbed on this network");

    _MessageDispatcher.sendInitiateTransferShares(eDispatch, targetCid, poolId, scId, sender, receiver, amount,
        extraGasLimit, remoteExtraGasLimit, refund);
    address localRefund = ghostHhLastRefund;

    bytes message = _Codec.serializeInitiateTransferShares(targetCid, poolId, scId, receiver, amount,
        remoteExtraGasLimit, extraGasLimit, sender);
    _MessageProcessor.handle(eProcess, localCid, message);

    satisfy(localRefund != ghostHhLastRefund, "the local and the relayed transfer pass different refunds");
}

// --- high_level ---

// MP-HL-15: the target session an adapter set update is encoded with reaches the adapter router.
rule hlMpRoundTripAdapterUpdateInstallsTheSenderSession(env e, uint16 cid, uint64 poolId, uint8 threshold,
    uint16 targetSessionId, bytes32[] adapters) {

    setupMessageProcessorJoint(e, e);
    require(_MessageProcessor.multiAdapter() == _MultiAdapterStub, "SCOPE: the adapter router is the stand-in");
    require(adapters.length <= 8, "SCOPE: an adapter set holds at most 8 adapters");

    bytes message = _Codec.serializeSetPoolAdapters(poolId, threshold, targetSessionId, adapters);
    mathint adapterBefore = ghostMaSetAdaptersCount;

    _MessageProcessor.handle(e, cid, message);

    assert(ghostMaSetAdaptersCount == adapterBefore + 1 && ghostMaLastSetAdaptersSession16 == targetSessionId,
        "the adapter router is called once, with the encoded target session");
}
