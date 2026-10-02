// MessageProcessor. High level: each message reaches exactly one handler; its length, source and route follow its encoding.

import "../setup/MessageProcessor_base.spec";

// MP-HL-01: a hub message makes exactly one call: to the envoy for a spoke manager call, else the hub handler.
rule hlMpEachHubKindReachesExactlyItsHandler(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);

    mathint k = _BytesSlice.toUint8Pure(message, 0);
    require(HUB_KIND_MP(k), "SCOPE: a message bound for the hub");

    mathint downstreamBefore = DOWNSTREAM_MP();
    mathint hubBefore = ghostHhCallCount;
    mathint envoyBefore = ghostEnCallCount;

    _MessageProcessor.handle(e, cid, message);

    assert(DOWNSTREAM_MP() == downstreamBefore + 1, "a hub message makes exactly one outbound call");
    assert(k != MT_MANAGER_CALL_FROM_SPOKE() => ghostHhCallCount == hubBefore + 1,
        "any other hub message calls the hub handler");
    assert(k == MT_MANAGER_CALL_FROM_SPOKE() => ghostEnCallCount == envoyBefore + 1,
        "a manager call from a spoke goes to the envoy");
}

// MP-HL-02: transfer requests, holding and share reports and spoke manager calls pass on their source network.
rule hlMpSourceNetworkReachesTheSourceKeyedHandlersUnchanged(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);

    mathint k = _BytesSlice.toUint8Pure(message, 0);
    mathint hubBefore = ghostHhCallCount;
    mathint envoyBefore = ghostEnCallCount;

    _MessageProcessor.handle(e, cid, message);

    assert((k == MT_INITIATE_TRANSFER_SHARES() || k == MT_UPDATE_ASSETS() || k == MT_UPDATE_SHARES())
        => (ghostHhCallCount == hubBefore + 1 && ghostHhLastSourceCid16 == cid),
        "a transfer or report reaches the hub handler once, with its source");
    assert(k == MT_MANAGER_CALL_FROM_SPOKE()
        => (ghostEnCallCount == envoyBefore + 1 && ghostEnLastSourceCid16 == cid),
        "a spoke manager call reaches the envoy once, with its source");
}

// MP-HL-03: a manager update reaches exactly the one contract its manager kind selects.
rule hlMpManagerUpdateReachesOnlyTheContractOfItsKind(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(_BytesSlice.toUint8Pure(message, 0) == MT_UPDATE_MANAGER(), "SCOPE: a manager update");

    mathint managerKind = _BytesSlice.toUint8Pure(message, 9);
    mathint downstreamBefore = DOWNSTREAM_MP();
    mathint spokeCallsBefore = ghostShCallCount;
    address adapterBefore = _MessageProcessor.multiAdapter();
    address gatewayBefore = _MessageProcessor.gateway();
    address spokeBefore = _MessageProcessor.spokeHandler();

    _MessageProcessor.handle(e, cid, message);

    assert(DOWNSTREAM_MP() == downstreamBefore + 1 && ghostShCallCount == spokeCallsBefore + 1,
        "a manager update makes exactly one manager call");
    assert(managerKind == 0 => (ghostShLastCallee == adapterBefore && !ghostShLastWasBridger),
        "an adapter manager update reaches the adapter router");
    assert(managerKind == 1 => (ghostShLastCallee == gatewayBefore && !ghostShLastWasBridger),
        "a gateway manager update reaches the gateway");
    assert(managerKind == 2 => (ghostShLastCallee == spokeBefore && !ghostShLastWasBridger),
        "a spoke manager update reaches the spoke handler as a manager");
    assert(managerKind == 3 => (ghostShLastCallee == spokeBefore && ghostShLastWasBridger),
        "a bridger update reaches the spoke handler as a bridger");
}

// MP-HL-04: an inbound share transfer reaches the hub handler unpaid, refund-free, with its source network.
rule hlMpInboundTransferRunsWithNoRefundAndNoValue(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(_BytesSlice.toUint8Pure(message, 0) == MT_INITIATE_TRANSFER_SHARES(), "SCOPE: a transfer initiation");

    mathint hubBefore = ghostHhCallCount;

    _MessageProcessor.handle(e, cid, message);

    assert(ghostHhCallCount == hubBefore + 1 && ghostHhLastRefund == 0 && ghostHhLastValue == 0
        && ghostHhLastSourceCid16 == cid,
        "an inbound transfer goes on once, unpaid, refund-free, with its source");
}

// MP-HL-05: a spoke message other than an adapter set makes one call, to the envoy only for a hub manager call.
rule hlMpEachSpokeKindReachesExactlyItsHandler(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);

    mathint k = _BytesSlice.toUint8Pure(message, 0);
    require(SPOKE_KIND_MP(k) && k != MT_SET_POOL_ADAPTERS(), "SCOPE: a spoke message, MP-HL-07 covers adapter sets");

    mathint downstreamBefore = DOWNSTREAM_MP();
    mathint spokeBefore = ghostShCallCount;
    mathint envoyBefore = ghostEnCallCount;

    _MessageProcessor.handle(e, cid, message);

    assert(DOWNSTREAM_MP() == downstreamBefore + 1, "a spoke message makes exactly one outbound call");
    assert(k != MT_MANAGER_CALL_FROM_HUB() => ghostShCallCount == spokeBefore + 1,
        "any other spoke message makes its one call on a spoke-side contract");
    assert(k == MT_MANAGER_CALL_FROM_HUB() => ghostEnCallCount == envoyBefore + 1,
        "a manager call from the hub goes to the envoy");
}

// MP-HL-06: an upgrade schedule or cancellation makes exactly one call, to the upgrade authority.
rule hlMpEachRootKindReachesExactlyTheScheduleAuthority(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(ROOT_KIND_MP(_BytesSlice.toUint8Pure(message, 0)), "SCOPE: an upgrade schedule or cancellation");
    require(_MessageProcessor.scheduleAuth() == _ScheduleAuthStub, "SCOPE: the upgrade authority is the stand-in");

    mathint downstreamBefore = DOWNSTREAM_MP();
    mathint rootBefore = ghostSaCallCount;

    _MessageProcessor.handle(e, cid, message);

    assert(DOWNSTREAM_MP() == downstreamBefore + 1 && ghostSaCallCount == rootBefore + 1,
        "an upgrade message calls the schedule authority and nothing else");
}

// MP-HL-07: an adapter set update makes exactly one call, to the adapter router, with its source network.
rule hlMpPoolAdaptersUpdateReachesExactlyTheAdapterRouter(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(_BytesSlice.toUint8Pure(message, 0) == MT_SET_POOL_ADAPTERS(), "SCOPE: an adapter set update");
    require(_MessageProcessor.multiAdapter() == _MultiAdapterStub, "SCOPE: the adapter router is the stand-in");

    mathint downstreamBefore = DOWNSTREAM_MP();
    mathint adapterBefore = ghostMaSetAdaptersCount;

    _MessageProcessor.handle(e, cid, message);

    assert(DOWNSTREAM_MP() == downstreamBefore + 1 && ghostMaSetAdaptersCount == adapterBefore + 1
        && ghostMaLastSetAdaptersCallee == _MultiAdapterStub && ghostMaLastSetAdaptersCid16 == cid,
        "the adapter router alone is called, once, with the source network");
}

// MP-HL-08: a well-formed message's length is exactly the bytes its decoder reads.
rule hlMpFramedLengthIsTheDecodedLength(bytes message) {
    require(wellFormedMp(message), "SCOPE: a message its decoder accepts");
    require(decodedLengthMp(message) <= max_uint16, "SCOPE: a message length fits in 16 bits");

    uint16 framed = _MessageProcessor.messageLength@withrevert(message);
    bool reverted = lastReverted;

    assert(!reverted && framed == decodedLengthMp(message), "the length is exactly the bytes the decoder reads");
}

// MP-HL-09: each message type is accepted only from its home network, three spoke reports from any.
rule hlMpSourceNetworkOfEachKindIsItsHome(bytes message) {
    mathint k = _BytesSlice.toUint8Pure(message, 0);

    uint16 src = _MessageProcessor.messageSourceCentrifugeId@withrevert(message);
    bool reverted = lastReverted;

    uint64 poolWord = _BytesSlice.toUint64Pure@withrevert(message, 1);
    bool poolWordReverted = lastReverted;
    uint128 assetAt1 = _BytesSlice.toUint128Pure@withrevert(message, 1);
    bool assetAt1Reverted = lastReverted;
    uint128 assetAt25 = _BytesSlice.toUint128Pure@withrevert(message, 25);
    bool assetAt25Reverted = lastReverted;

    assert(!reverted && ROOT_KIND_MP(k) => src == MAINNET_CID_MP(), "an upgrade is accepted only from mainnet");
    assert(!reverted && (k == MT_INITIATE_TRANSFER_SHARES() || k == MT_UPDATE_SHARES()
            || k == MT_MANAGER_CALL_FROM_SPOKE()) => src == 0, "a spoke report is accepted from any network");
    assert(!reverted && SPOKE_KIND_MP(k) => src != 0 && !poolWordReverted && src == poolWord / 2^48,
        "a hub-to-spoke message is accepted only from its pool's home");
    assert(!reverted && k == MT_REGISTER_ASSET() => src != 0 && !assetAt1Reverted && src == assetAt1 / 2^112,
        "an asset registration is accepted only from the asset's home");
    assert(!reverted && (k == MT_REQUEST() || k == MT_UPDATE_ASSETS())
            => src != 0 && !assetAt25Reverted && src == assetAt25 / 2^112,
        "a request or holding report is accepted only from the asset's home");
}

// MP-HL-10: messages route by their pool, a pool's first adapter set over the global adapters.
rule hlMpRouteFallsBackToTheGlobalSetOnlyForAFirstAdapterSet(bytes message, bool poolConfigured) {
    mathint k = _BytesSlice.toUint8Pure(message, 0);
    require(k >= 1 && k <= MT_UNAUTHORIZE_SPOKE_CALL(), "SCOPE: a known message type");

    MessageProcessor.PoolId route = _MessageProcessor.routePoolId@withrevert(message, poolConfigured);
    bool routeReverted = lastReverted;
    MessageProcessor.PoolId pool = _MessageProcessor.messagePoolId@withrevert(message);
    bool poolReverted = lastReverted;

    uint64 poolWord = _BytesSlice.toUint64Pure@withrevert(message, 1);
    bool poolWordReverted = lastReverted;
    bool firstAdapterSet = k == MT_SET_POOL_ADAPTERS() && !poolConfigured;

    assert(firstAdapterSet => !routeReverted && route == 0, "a pool's first adapter set routes over the global set");
    assert(!firstAdapterSet => routeReverted == poolReverted && (!routeReverted => route == pool),
        "every other message routes over its own pool");
    assert(!poolReverted && k >= MT_SET_POOL_ADAPTERS() => !poolWordReverted && pool == poolWord,
        "a pool-carrying message names the pool at offset 1");
    assert(!poolReverted && k < MT_SET_POOL_ADAPTERS() => pool == 0, "an upgrade or asset registration names no pool");
}

// MP-HL-11: an adapter set update passes its pool and target session to the adapter router.
rule hlMpPoolAdaptersUpdateForwardsTheAnnouncedSession(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(_BytesSlice.toUint8Pure(message, 0) == MT_SET_POOL_ADAPTERS(), "SCOPE: an adapter set update");
    require(_MessageProcessor.multiAdapter() == _MultiAdapterStub, "SCOPE: the adapter router is the stand-in");

    mathint adapterBefore = ghostMaSetAdaptersCount;
    mathint wirePool = _BytesSlice.toUint64Pure(message, 1);
    mathint wireSession = _BytesSlice.toUint16Pure(message, 10);

    _MessageProcessor.handle(e, cid, message);

    assert(ghostMaSetAdaptersCount == adapterBefore + 1 && ghostMaLastSetAdaptersPool64 == wirePool
        && ghostMaLastSetAdaptersSession16 == wireSession,
        "the router gets the pool and the target session the message carries");
}

// MP-HL-12: the processor never reports a zero message length.
rule hlMpEveryFramedLengthIsPositive(bytes message) {
    uint16 framed = _MessageProcessor.messageLength@withrevert(message);
    bool reverted = lastReverted;

    assert(!reverted => framed > 0, "no computed message length is zero");
}

// MP-HL-13: each message type but a manager update calls only the handler function it names.
rule hlMpEachWireCodeReachesItsNamedEntry(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);

    mathint k = _BytesSlice.toUint8Pure(message, 0);
    require(k >= MT_SCHEDULE_UPGRADE() && k <= MT_UNAUTHORIZE_SPOKE_CALL() && k != MT_UPDATE_MANAGER(),
        "SCOPE: a known message type, MP-HL-03 covers manager updates");
    require(ROOT_KIND_MP(k) => _MessageProcessor.scheduleAuth() == _ScheduleAuthStub,
        "SCOPE: the upgrade authority is the stand-in");
    require(k == MT_SET_POOL_ADAPTERS() => _MessageProcessor.multiAdapter() == _MultiAdapterStub,
        "SCOPE: the adapter router is the stand-in");

    mathint downstreamBefore = DOWNSTREAM_MP();
    clearEntriesMp();

    _MessageProcessor.handle(e, cid, message);

    assert(DOWNSTREAM_MP() == downstreamBefore + 1 && LAST_ENTRY_MP() == ENTRY_OF_MP(k),
        "one call, on the handler function the message type names");
}

// MP-HL-14: a share transfer execution passes the spoke handler the receiver it carries.
rule hlMpInboundTransferExecutionHandsOnTheWireReceiver(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(_BytesSlice.toUint8Pure(message, 0) == MT_EXECUTE_TRANSFER_SHARES(), "SCOPE: a transfer execution");

    bytes32 wireReceiver = _BytesSlice.toBytes32Pure(message, 25);
    mathint spokeBefore = ghostShCallCount;

    _MessageProcessor.handle(e, cid, message);

    assert(ghostShCallCount == spokeBefore + 1 && ghostShLastTransferReceiver == wireReceiver,
        "the spoke handler gets the receiver the message carries");
}
