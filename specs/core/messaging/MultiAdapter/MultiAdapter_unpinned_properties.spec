import "setup/MultiAdapter_unpinned.spec";

// --- high_level ---

// MA-HL-28: a vote moves no tally but the one keyed by its routed pool and whole stamped message.
rule hlMaVoteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage(env e, uint16 cid, bytes payload, address adapter,
    bytes32 otherKey) {

    setupMultiAdapterUnpinned(e);

    int16 lane0Before = _MultiAdapter.voteAt(e, cid, otherKey, 0);
    int16 lane1Before = _MultiAdapter.voteAt(e, cid, otherKey, 1);
    int16 lane2Before = _MultiAdapter.voteAt(e, cid, otherKey, 2);
    int16 lane3Before = _MultiAdapter.voteAt(e, cid, otherKey, 3);
    int16 lane4Before = _MultiAdapter.voteAt(e, cid, otherKey, 4);
    int16 lane5Before = _MultiAdapter.voteAt(e, cid, otherKey, 5);
    int16 lane6Before = _MultiAdapter.voteAt(e, cid, otherKey, 6);
    int16 lane7Before = _MultiAdapter.voteAt(e, cid, otherKey, 7);

    _MultiAdapter.vote(e, cid, payload, adapter);

    bytes32 ownKey = _MaPayload.voteKeyOf(e, ghostMaRtRoutedPool64, payload);

    assert(otherKey != ownKey => _MultiAdapter.voteAt(e, cid, otherKey, 0) == lane0Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 1) == lane1Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 2) == lane2Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 3) == lane3Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 4) == lane4Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 5) == lane5Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 6) == lane6Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 7) == lane7Before,
        "every other message's vote counts are unchanged by the vote");
}

// MA-HL-29: a delivery moves no tally but the one keyed by its routed pool and whole stamped message.
rule hlMaHandleMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage(env e, uint16 cid, bytes payload, address adapter,
    bytes32 otherKey) {

    setupMultiAdapterUnpinned(e);

    int16 lane0Before = _MultiAdapter.voteAt(e, cid, otherKey, 0);
    int16 lane1Before = _MultiAdapter.voteAt(e, cid, otherKey, 1);
    int16 lane2Before = _MultiAdapter.voteAt(e, cid, otherKey, 2);
    int16 lane3Before = _MultiAdapter.voteAt(e, cid, otherKey, 3);
    int16 lane4Before = _MultiAdapter.voteAt(e, cid, otherKey, 4);
    int16 lane5Before = _MultiAdapter.voteAt(e, cid, otherKey, 5);
    int16 lane6Before = _MultiAdapter.voteAt(e, cid, otherKey, 6);
    int16 lane7Before = _MultiAdapter.voteAt(e, cid, otherKey, 7);

    _MultiAdapter.handle(e, cid, payload, adapter);

    bytes32 ownKey = _MaPayload.voteKeyOf(e, ghostMaRtRoutedPool64, payload);

    assert(otherKey != ownKey => _MultiAdapter.voteAt(e, cid, otherKey, 0) == lane0Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 1) == lane1Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 2) == lane2Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 3) == lane3Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 4) == lane4Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 5) == lane5Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 6) == lane6Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 7) == lane7Before,
        "every other message's vote counts are unchanged by the delivery");
}

// MA-HL-30: an execution spends no tally but the one keyed by its routed pool and whole stamped message.
rule hlMaExecuteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage(env e, uint16 cid, bytes payload, address adapter,
    bytes32 otherKey) {

    setupMultiAdapterUnpinned(e);

    int16 lane0Before = _MultiAdapter.voteAt(e, cid, otherKey, 0);
    int16 lane1Before = _MultiAdapter.voteAt(e, cid, otherKey, 1);
    int16 lane2Before = _MultiAdapter.voteAt(e, cid, otherKey, 2);
    int16 lane3Before = _MultiAdapter.voteAt(e, cid, otherKey, 3);
    int16 lane4Before = _MultiAdapter.voteAt(e, cid, otherKey, 4);
    int16 lane5Before = _MultiAdapter.voteAt(e, cid, otherKey, 5);
    int16 lane6Before = _MultiAdapter.voteAt(e, cid, otherKey, 6);
    int16 lane7Before = _MultiAdapter.voteAt(e, cid, otherKey, 7);

    _MultiAdapter.execute(e, cid, payload, adapter);

    bytes32 ownKey = _MaPayload.voteKeyOf(e, ghostMaRtRoutedPool64, payload);

    assert(otherKey != ownKey => _MultiAdapter.voteAt(e, cid, otherKey, 0) == lane0Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 1) == lane1Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 2) == lane2Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 3) == lane3Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 4) == lane4Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 5) == lane5Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 6) == lane6Before
            && _MultiAdapter.voteAt(e, cid, otherKey, 7) == lane7Before,
        "every other message's vote counts are unchanged by the execution");
}

// MA-HL-31: a delivery succeeds only for an adapter of the routed pool, sent by it or that pool's manager.
rule hlMaHandleIsJudgedByTheRoutedPoolsRosterAndManagers(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterUnpinned(e);

    _MultiAdapter.handle(e, cid, payload, adapter);

    assert(!ghostMaRtOffRouted && ghostMaRtLoadedId8 != 0
        && (e.msg.sender == adapter || (ghostMaRtManagerBit && ghostMaRtManagerAccount == e.msg.sender)),
        "a delivery passes on the routed pool's own adapters and managers only");
}

// MA-HL-32: a vote succeeds only for an adapter of the routed pool, cast by it or that pool's manager.
rule hlMaVoteIsJudgedByTheRoutedPoolsRosterAndManagers(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterUnpinned(e);

    _MultiAdapter.vote(e, cid, payload, adapter);

    assert(!ghostMaRtOffRouted && ghostMaRtLoadedId8 != 0
        && (e.msg.sender == adapter || (ghostMaRtManagerBit && ghostMaRtManagerAccount == e.msg.sender)),
        "a vote passes on the routed pool's own adapters and managers only");
}

// MA-HL-33: an execution succeeds only for an adapter of the routed pool, made by it or that pool's manager.
rule hlMaExecuteIsJudgedByTheRoutedPoolsRosterAndManagers(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterUnpinned(e);

    _MultiAdapter.execute(e, cid, payload, adapter);

    assert(!ghostMaRtOffRouted && ghostMaRtLoadedId8 != 0
        && (e.msg.sender == adapter || (ghostMaRtManagerBit && ghostMaRtManagerAccount == e.msg.sender)),
        "an execution passes on the routed pool's adapters and managers only");
}

// MA-HL-34: on a vote, the router is told whether the message's pool is configured on the arrival network.
rule hlMaVoteAsksTheRouterAboutTheMessagesOwnPoolsConfiguration(env e, uint16 cid, bytes payload, address adapter,
    MultiAdapterHarness.PoolId messagePool) {

    setupMultiAdapterUnpinned(e);

    _MultiAdapter.vote(e, cid, payload, adapter);

    require(messagePool == ghostMaRtMessagePool64, "SAFE: binds the pool to the one the message names");

    assert(ghostMaRtConfiguredArg == (_MultiAdapter.activeSessionId[cid][messagePool] != 0),
        "the router hears whether the message's pool has a session there");
}

// MA-HL-35: on a vote, both router questions are asked about the message without its session stamp.
rule hlMaVoteHandsTheRouterTheUnstampedMessage(env e, env eh, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterUnpinned(e);
    bytes message = _MaPayload.unwrap(eh, payload);

    _MultiAdapter.vote(e, cid, payload, adapter);

    assert(ghostMaRtMessagePoolArgHash == keccak256(message) && ghostMaRtRouteArgHash == keccak256(message),
        "the router sees the unstamped message both times");
}

// MA-HL-39: a vote takes the message's pool and routing from the configured parser.
rule hlMaVoteAsksTheFiledParserNotTheGasModel(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterUnpinned(e);

    _MultiAdapter.vote(e, cid, payload, adapter);

    assert(ghostMaRtMessagePoolCallee == _MultiAdapter.parser && ghostMaRtRouteCallee == _MultiAdapter.parser,
        "the vote asks the configured parser for the pool and the routing");
}

// MA-HL-40: an execution succeeds only if the routed pool's positive votes met its threshold.
rule hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally(env e, uint16 cid, bytes payload, address adapter,
    uint64 pool) {

    setupMultiAdapterUnpinned(e);
    bytes32 voteKey = _MaPayload.voteKeyOf(e, pool, payload);

    mathint lane0Before = _MultiAdapter.voteAt(e, cid, voteKey, 0);
    mathint lane1Before = _MultiAdapter.voteAt(e, cid, voteKey, 1);
    mathint lane2Before = _MultiAdapter.voteAt(e, cid, voteKey, 2);
    mathint lane3Before = _MultiAdapter.voteAt(e, cid, voteKey, 3);
    mathint lane4Before = _MultiAdapter.voteAt(e, cid, voteKey, 4);
    mathint lane5Before = _MultiAdapter.voteAt(e, cid, voteKey, 5);
    mathint lane6Before = _MultiAdapter.voteAt(e, cid, voteKey, 6);
    mathint lane7Before = _MultiAdapter.voteAt(e, cid, voteKey, 7);

    _MultiAdapter.execute(e, cid, payload, adapter);

    require(pool == ghostMaRtRoutedPool64, "SAFE: the claim is about the pool the router picked");

    assert(POSITIVE_LANES_RT_MA(lane0Before, lane1Before, lane2Before, lane3Before, lane4Before, lane5Before,
            lane6Before, lane7Before, ghostMaRtLoadedQuorum8) >= ghostMaRtLoadedThreshold8,
        "an executed message met the vote threshold of its routed pool");
}
