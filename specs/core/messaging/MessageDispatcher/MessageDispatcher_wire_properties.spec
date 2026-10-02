import "setup/MessageDispatcher_wire.spec";

// --- high_level ---

// MD-HL-38: every message within the gateway's size limit decodes to exactly its own length.
rule hlMdEveryWireMessageMeasuresItsOwnLength(env e, method f, calldataarg args)
    filtered { f -> SEND_ENTRY_MD(f) } {

    setupMessageDispatcher(e);

    mathint wireSendsBefore = ghostGwSendCount;

    f(e, args);

    assert(ghostGwSendCount == wireSendsBefore + 1 && ghostGwLastSendLength <= GATEWAY_MAX_LENGTH_MD()
            => ghostGwLastSendLengthRead && ghostGwLastSendLengthOf == ghostGwLastSendLength,
        "the length read back from a sent message equals its size");
}

// MD-HL-39: every message about a pool carries that pool's id right after its type byte.
rule hlMdEveryPoolMessageCarriesItsPoolAtOffsetOne(env e, method f, uint16 cid, uint16 cid2,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId,
    MessageDispatcher.ShareClassMetadata metadata, string name, string symbol, bytes32 word1, bytes32 word2,
    bytes payload, uint128 gas, uint128 gas2, uint128 amount, MessageDispatcher.D18 price, uint64 computedAt,
    address target, uint256 value, MessageDispatcher.VaultUpdateKind vaultKind,
    MessageDispatcher.ManagerKind managerKind, bool flag, ISpokeMessageSender.UpdateData data, uint8 small,
    bytes32[] adapters, uint16 sessionId, address refund)
    filtered { f -> SEND_ENTRY_MD(f) && POOL_MESSAGE_MD(f) } {

    setupMessageDispatcher(e);

    mathint wireSendsBefore = ghostGwSendCount;

    callSendEntryMD(e, f, cid, cid2, poolId, scId, assetId, metadata, name, symbol, word1, word2, payload, gas, gas2,
        amount, price, computedAt, target, value, vaultKind, managerKind, flag, data, small, adapters, sessionId,
        refund);

    assert(ghostGwSendCount == wireSendsBefore + 1 => ghostGwLastSendPoolAt1 == poolId,
        "the pool id sits at byte 1 of the message");
}

// MD-HL-40: every message yields the extra gas limit its send was given, or zero for a type without one.
rule hlMdEveryWireMessageYieldsItsExtraGasLimit(env e, method f, uint16 cid, uint16 cid2,
    MessageDispatcher.PoolId poolId, MessageDispatcher.ShareClassId scId, MessageDispatcher.AssetId assetId,
    MessageDispatcher.ShareClassMetadata metadata, string name, string symbol, bytes32 word1, bytes32 word2,
    bytes payload, uint128 gas, uint128 gas2, uint128 amount, MessageDispatcher.D18 price, uint64 computedAt,
    address target, uint256 value, MessageDispatcher.VaultUpdateKind vaultKind,
    MessageDispatcher.ManagerKind managerKind, bool flag, ISpokeMessageSender.UpdateData data, uint8 small,
    bytes32[] adapters, uint16 sessionId, address refund)
    filtered { f -> SEND_ENTRY_MD(f) } {

    setupMessageDispatcher(e);

    mathint wireSendsBefore = ghostGwSendCount;

    callSendEntryMD(e, f, cid, cid2, poolId, scId, assetId, metadata, name, symbol, word1, word2, payload, gas, gas2,
        amount, price, computedAt, target, value, vaultKind, managerKind, flag, data, small, adapters, sessionId,
        refund);

    assert(ghostGwSendCount == wireSendsBefore + 1
            => ghostGwLastSendGasRead && ghostGwLastSendGasOf == (GAS_MESSAGE_MD(f) ? gas : 0),
        "the gas read back is the caller's limit, or zero if the type has none");
}

// MD-HL-41: setting a pool's adapters sends one message with its threshold and target session.
rule hlMdSetPoolAdaptersWiresItsTargetSession(env e, uint16 centrifugeId, MessageDispatcher.PoolId poolId,
    bytes32[] adapters, uint8 threshold, uint16 targetSessionId, address refund) {

    setupMessageDispatcher(e);

    mathint wireSendsBefore = ghostGwSendCount;

    _MessageDispatcher.sendSetPoolAdapters(e, centrifugeId, poolId, adapters, threshold, targetSessionId, refund);

    assert(ghostGwSendCount == wireSendsBefore + 1 && ghostGwLastSendThresholdAt9 == threshold
            && ghostGwLastSendSessionAt10 == targetSessionId,
        "one send carrying the threshold and the target session");
}

// MD-HL-42: every sent message starts with the type code of the function that sent it.
rule hlMdEverySendCarriesItsFrozenTypeCode(env e, method f, calldataarg args)
    filtered { f -> SEND_ENTRY_MD(f) } {

    setupMessageDispatcher(e);

    mathint wireSendsBefore = ghostGwSendCount;

    f(e, args);

    assert(ghostGwSendCount == wireSendsBefore + 1 => ghostGwLastSendTypeAt0 == TYPE_CODE_OF_MD(f),
        "the first byte is the type code of the sending function");
}

// MD-HL-43: a share transfer passes its receiver to the spoke handler if local, else in one message.
rule hlMdTransferCarriesTheNamedReceiver(env e, uint16 originCid, uint16 targetCid, MessageDispatcher.PoolId poolId,
    MessageDispatcher.ShareClassId scId, bytes32 receiver, uint128 amount, uint128 extraGasLimit, address refund) {

    setupMessageDispatcher(e);

    bool local = targetCid == _MessageDispatcher.localCentrifugeId();
    mathint wireSendsBefore = ghostGwSendCount;
    mathint spokeCallsBefore = ghostShCallCount;

    _MessageDispatcher.sendExecuteTransferShares(e, originCid, targetCid, poolId, scId, receiver, amount,
        extraGasLimit, refund);

    assert(local => ghostShCallCount == spokeCallsBefore + 1 && ghostShLastTransferReceiver == receiver,
        "a local transfer passes its receiver to the spoke handler");
    assert(!local => ghostGwSendCount == wireSendsBefore + 1 && ghostGwLastSendTypeAt0 == 11
            && ghostGwLastSendWordAt25 == receiver,
        "a remote transfer sends one transfer message with the receiver at byte 25");
}
