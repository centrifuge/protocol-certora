import "MultiAdapter_valid_state.spec";

// MA-RC-01: a pool's first adapter set can be a single adapter at threshold one.
rule rcMaFirstRosterInstallIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p, address[] addresses) {

    setupMultiAdapterValidState(e);

    uint16 target = _MultiAdapter.nextActiveSessionId(e, cid, p);

    _MultiAdapter.setAdapters(e, cid, p, addresses, 1, target);

    uint16 sessionAfter = ghostMaActiveSessionId16;
    mathint rosterLengthAfter = ghostMaSessionListLength8[sessionAfter];
    mathint routeSessionAfter = ghostMaActiveSetSessionId16;
    mathint quorumAfter = _MultiAdapter.quorum(e, cid, p);
    mathint thresholdAfter = _MultiAdapter.threshold(e, cid, p);

    satisfy(sessionAfter == 1 && rosterLengthAfter == 1 && routeSessionAfter == 1
        && quorumAfter == 1 && thresholdAfter == 1,
        "a route's first session can carry one adapter at threshold one");
}

// MA-RC-02: an eight-adapter set, the maximum, can be installed requiring unanimity.
rule rcMaRosterCapInstallIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p, address[] addresses) {

    setupMultiAdapterValidState(e);

    uint16 target = _MultiAdapter.nextActiveSessionId(e, cid, p);

    _MultiAdapter.setAdapters(e, cid, p, addresses, 8, target);

    uint16 sessionAfter = ghostMaActiveSessionId16;
    mathint rosterLengthAfter = ghostMaSessionListLength8[sessionAfter];
    mathint quorumAfter = _MultiAdapter.quorum(e, cid, p);
    mathint thresholdAfter = _MultiAdapter.threshold(e, cid, p);

    satisfy(sessionAfter == 1 && rosterLengthAfter == 8 && quorumAfter == 8 && thresholdAfter == 8,
        "a first session can fill the eight-adapter cap, all eight required");
}

// MA-RC-03: an adapter set can require two of its three adapters to agree.
rule rcMaIntermediateThresholdInstallIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    address[] addresses) {

    setupMultiAdapterValidState(e);

    uint16 target = _MultiAdapter.nextActiveSessionId(e, cid, p);

    _MultiAdapter.setAdapters(e, cid, p, addresses, 2, target);

    uint16 sessionAfter = ghostMaActiveSessionId16;
    mathint rosterLengthAfter = ghostMaSessionListLength8[sessionAfter];
    mathint quorumAfter = _MultiAdapter.quorum(e, cid, p);
    mathint thresholdAfter = _MultiAdapter.threshold(e, cid, p);

    satisfy(sessionAfter == 1 && rosterLengthAfter == 3 && quorumAfter == 3 && thresholdAfter == 2,
        "a first session can install a two-of-three threshold");
}

// MA-RC-04: a pool's adapter manager can halt its outbound route with an empty adapter set.
rule rcMaManagerHaltsARouteWithTheEmptySetIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    address[] addresses) {

    setupMultiAdapterValidState(e);
    require(ghostMaManager[e.msg.sender], "SCOPE: the caller holds the pool's manager rights");
    require(_MultiAdapter.wards[e.msg.sender] != 1, "SCOPE: not a ward, so manager rights alone admit it");

    mathint sessionBefore = ghostMaActiveSessionId16;
    uint16 target = _MultiAdapter.nextActiveSessionId(e, cid, p);

    _MultiAdapter.setAdapters(e, cid, p, addresses, 0, target);

    mathint sessionAfter = ghostMaActiveSessionId16;
    mathint routeLengthAfter = ghostMaActiveListLength8;
    mathint quorumAfter = _MultiAdapter.quorum(e, cid, p);

    satisfy(sessionAfter == sessionBefore + 1 && routeLengthAfter == 0 && quorumAfter == 0,
        "manager rights alone suffice to empty a pool's route");
}

// MA-RC-05: the active session can be blocked, stopping the pool's outbound messages.
rule rcMaBlockingTheSessionInServiceIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p, uint16 sid) {

    setupMultiAdapterValidState(e);
    require(ghostMaSessionListLength8[1] == 1 && ghostMaActiveSetSessionId16 == 1,
        "SCOPE: the route runs on session one with one adapter");

    _MultiAdapter.blockSession(e, cid, p, sid);

    bool stashedAfter = _MultiAdapter.blockedSession(e, cid, p, sid);
    mathint rosterLengthAfter = ghostMaSessionListLength8[1];
    mathint routeLengthAfter = ghostMaActiveListLength8;
    mathint routeSessionAfter = ghostMaActiveSetSessionId16;

    satisfy(stashedAfter && rosterLengthAfter == 0 && routeLengthAfter == 0 && routeSessionAfter == 0,
        "a live session can be blocked, its roster stashed, its route cleared");
}

// MA-RC-06: a session can be blocked and unblocked, restoring its adapters and threshold.
rule rcMaBlockThenUnblockRestoresTheRouteIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    uint16 sid) {

    setupMultiAdapterValidState(e);
    require(ghostMaSessionListLength8[1] == 1 && ghostMaActiveSetSessionId16 == 1,
        "SCOPE: the route runs on session one with one adapter");

    _MultiAdapter.blockSession(e, cid, p, sid);

    mathint rosterLengthMid = ghostMaSessionListLength8[1];
    mathint routeSessionMid = ghostMaActiveSetSessionId16;

    _MultiAdapter.unblockSession(e, cid, p, sid);

    mathint rosterLengthAfter = ghostMaSessionListLength8[1];
    mathint routeSessionAfter = ghostMaActiveSetSessionId16;
    mathint routeLengthAfter = ghostMaActiveListLength8;
    mathint thresholdAfter = _MultiAdapter.threshold(e, cid, p);

    satisfy(rosterLengthMid == 0 && routeSessionMid == 0
        && rosterLengthAfter == 1 && routeSessionAfter == 1 && routeLengthAfter == 1 && thresholdAfter == 1,
        "blocking then unblocking can restore the roster, route and threshold");
}

// MA-RC-07: an old session can be blocked while the active one keeps carrying messages.
rule rcMaBlockingASupersededSessionKeepsTheRouteIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    uint16 sid) {

    setupMultiAdapterValidState(e);
    require(ghostMaSessionListLength8[1] == 1, "SCOPE: session one holds one adapter");

    _MultiAdapter.blockSession(e, cid, p, sid);

    bool stashedAfter = _MultiAdapter.blockedSession(e, cid, p, sid);
    mathint retiredLengthAfter = ghostMaSessionListLength8[1];
    mathint routeSessionAfter = ghostMaActiveSetSessionId16;
    mathint routeLengthAfter = ghostMaActiveListLength8;

    satisfy(stashedAfter && retiredLengthAfter == 0 && routeSessionAfter == 2 && routeLengthAfter == 1,
        "a superseded session can be blocked, the live route left in place");
}

// MA-RC-08: an old session can be unblocked without replacing the active adapter set.
rule rcMaUnblockingASupersededSessionKeepsTheRouteIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    uint16 sid) {

    setupMultiAdapterValidState(e);
    require(ghostMaBlockedListLength8[1] == 1 && ghostMaBlockedWasActive[1],
        "SCOPE: session one was blocked while live, with one adapter");

    _MultiAdapter.unblockSession(e, cid, p, sid);

    mathint restoredLengthAfter = ghostMaSessionListLength8[1];
    bool stashedAfter = _MultiAdapter.blockedSession(e, cid, p, sid);
    mathint routeSessionAfter = ghostMaActiveSetSessionId16;
    mathint routeLengthAfter = ghostMaActiveListLength8;

    satisfy(restoredLengthAfter == 1 && !stashedAfter && routeSessionAfter == 2 && routeLengthAfter == 1,
        "a superseded session can be unblocked, the live route left in place");
}

// MA-RC-09: a blocked and unblocked session can send outbound messages again.
rule rcMaSendResumesAfterABlockAndUnblockIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    uint16 sid, bytes payload, uint256 gasLimit, address refund) {

    // Requires below pin each row to what setAdapters([member], 1) at sid leaves.
    setupMultiAdapter(e);
    require(ghostMaActiveSessionId16 == sid && sid != 0, "SCOPE: the live session, any nonzero id, is the one blocked");
    require(ghostMaSessionListLength8[sid] == 1 && ghostMaActiveSetSessionId16 == sid,
        "SCOPE: the route runs on that session with one adapter");
    address member = ghostMaSessionList[sid][0];
    require(ghostMaAdapterId8[sid][member] == 1 && ghostMaAdapterQuorum8[sid][member] == 1
        && ghostMaAdapterThreshold8[sid][member] == 1,
        "SAFE: the lone adapter's id, quorum and threshold are one");
    require(ghostMaActiveListLength8 == 1 && ghostMaActiveList[0] == member,
        "PROVED: activeSetMirrorsSessionList (MultiAdapter)");
    require(ghostMaBlockedListLength8[sid] == 0, "PROVED: blockedExcludesLive (MultiAdapter)");
    require(payload.length == 32, "SCOPE: a one-word message");

    mathint dispatchCountBefore = ghostMaFaceSendCount;

    _MultiAdapter.blockSession(e, cid, p, sid);

    mathint routeLengthMid = ghostMaActiveListLength8;

    _MultiAdapter.unblockSession(e, cid, p, sid);
    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    mathint dispatchCountAfter = ghostMaFaceSendCount;

    satisfy(routeLengthMid == 0 && dispatchCountAfter == dispatchCountBefore + 1,
        "a route can be blocked, unblocked and then carry a send again");
}

// MA-RC-10: with two required adapters, the second delivery can release the message.
rule rcMaSecondDeliveryCompletesTheQuorumIsReachable(env e, uint16 cid, bytes payload, address adapterA,
    address adapterB) {

    setupMultiAdapterValidState(e);
    require(ghostMaActiveSessionId16 == 1, "SCOPE: only session one is configured");
    require(ghostMaSessionListLength8[1] == 2 && ghostMaAdapterThreshold8[1][adapterA] == 2,
        "SCOPE: a two-of-two session");
    require(ghostMaAdapterId8[1][adapterA] == 1 && ghostMaAdapterId8[1][adapterB] == 2,
        "SCOPE: the two adapters hold ids one and two");
    require(ghostMaAdapterQuorum8[1][adapterA] == 2 && ghostMaAdapterQuorum8[1][adapterB] == 2
        && ghostMaAdapterThreshold8[1][adapterB] == 2,
        "SAFE: both adapters have quorum and threshold two");
    require(payload.length == 34, "SCOPE: a session stamp plus a one-word message");
    require(ghostGwHandleCount == 0 && ghostMaVoteForwardMark == 0,
        "SCOPE: nothing forwarded yet, the vote mark at zero");

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload, adapterA);

    mathint forwardCountMid = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload, adapterB);

    mathint forwardCountAfter = ghostGwHandleCount;
    mathint forwardCidAfter = ghostGwLastHandleCid16;

    satisfy(forwardCountMid == forwardCountBefore && forwardCountAfter == forwardCountBefore + 1
        && forwardCidAfter == cid,
        "a first delivery can record without releasing, a second release it");
}

// MA-RC-11: a message can be released by an execution after two adapters voted.
rule rcMaExecuteReleasesThePayloadAfterTwoProofsIsReachable(env e, uint16 cid, bytes payload, address adapterA,
    address adapterB) {

    setupMultiAdapterValidState(e);
    require(ghostMaActiveSessionId16 == 1, "SCOPE: only session one is configured");
    require(ghostMaSessionListLength8[1] == 2 && ghostMaAdapterThreshold8[1][adapterA] == 2,
        "SCOPE: a two-of-two session");
    require(ghostMaAdapterId8[1][adapterA] == 1 && ghostMaAdapterId8[1][adapterB] == 2,
        "SCOPE: the two adapters hold ids one and two");
    require(ghostMaAdapterQuorum8[1][adapterA] == 2 && ghostMaAdapterQuorum8[1][adapterB] == 2
        && ghostMaAdapterThreshold8[1][adapterB] == 2,
        "SAFE: both adapters have quorum and threshold two");
    require(payload.length == 34, "SCOPE: a session stamp plus a one-word message");
    require(ghostGwHandleCount == 0 && ghostMaVoteForwardMark == 0,
        "SCOPE: nothing forwarded yet, the vote mark at zero");

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.vote(e, cid, payload, adapterA);
    _MultiAdapter.vote(e, cid, payload, adapterB);

    mathint forwardCountMid = ghostGwHandleCount;

    _MultiAdapter.execute(e, cid, payload, adapterA);

    mathint forwardCountAfter = ghostGwHandleCount;

    satisfy(forwardCountMid == forwardCountBefore && forwardCountAfter == forwardCountBefore + 1,
        "two votes can stay unreleased until a later execution releases them");
}

// MA-RC-12: with a threshold of one, a single adapter can release a message alone.
rule rcMaThresholdOneLetsOneAdapterForwardAloneIsReachable(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);
    require(ghostMaActiveSessionId16 == 1, "SCOPE: only session one is configured");
    require(ghostMaSessionListLength8[1] == 2 && ghostMaAdapterThreshold8[1][adapter] == 1,
        "SCOPE: a one-of-two session");
    require(e.msg.sender == adapter, "SCOPE: the adapter delivers for itself");

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload, adapter);

    mathint forwardCountAfter = ghostGwHandleCount;
    mathint forwardCidAfter = ghostGwLastHandleCid16;

    satisfy(forwardCountAfter == forwardCountBefore + 1 && forwardCidAfter == cid,
        "one adapter's lone delivery can release a payload at threshold one");
}

// MA-RC-13: an execution can leave a vote count negative for an adapter that never voted.
rule rcMaExecuteDrivesASilentLaneNegativeIsReachable(env e, uint16 cid, bytes payload, address adapter,
    bytes32 voteKey) {

    setupMultiAdapterValidState(e);
    require(ghostMaActiveSessionId16 == 1, "SCOPE: only session one is configured");
    require(ghostMaSessionListLength8[1] == 2 && ghostMaAdapterThreshold8[1][adapter] == 1,
        "SCOPE: a one-of-two session");
    require(e.msg.sender == adapter, "SCOPE: the adapter submits for itself");

    mathint forwardCountBefore = ghostGwHandleCount;
    mathint lane0Before = _MultiAdapter.voteAt(e, cid, voteKey, 0);
    mathint lane1Before = _MultiAdapter.voteAt(e, cid, voteKey, 1);
    require(lane0Before == 1 && lane1Before == 0, "SCOPE: adapter one has one vote, adapter two none");

    _MultiAdapter.execute(e, cid, payload, adapter);

    mathint lane1After = _MultiAdapter.voteAt(e, cid, voteKey, 1);
    mathint forwardCountAfter = ghostGwHandleCount;

    satisfy(lane1After < 0 && forwardCountAfter == forwardCountBefore + 1,
        "an execution's release can leave a silent adapter's votes negative");
}

// MA-RC-14: an in-flight message of a replaced adapter set can still be delivered.
rule rcMaSupersededSessionStillDeliversIsReachable(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    address[] addresses, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);
    require(ghostMaSessionListLength8[1] == 1 && ghostMaAdapterId8[1][adapter] != 0,
        "SCOPE: the adapter alone makes up session one");
    require(ghostMaManager[e.msg.sender], "SCOPE: a pool manager rotates and delivers");
    require(addresses.length == 1 && addresses[0] != adapter,
        "SCOPE: a one-adapter replacement without the old adapter");

    mathint forwardCountBefore = ghostGwHandleCount;
    uint16 target = _MultiAdapter.nextActiveSessionId(e, cid, p);

    _MultiAdapter.setAdapters(e, cid, p, addresses, 1, target);

    mathint sessionMid = ghostMaActiveSessionId16;

    _MultiAdapter.handle(e, cid, payload, adapter);

    mathint forwardCountAfter = ghostGwHandleCount;

    satisfy(sessionMid == 2 && forwardCountAfter == forwardCountBefore + 1,
        "an adapter of a superseded session can still get its payload released");
}

// MA-RC-15: a pool's adapter manager can be appointed and removed again.
rule rcMaManagerSeatGrantAndRevokeIsReachable(env e, MultiAdapterHarness.PoolId p, address who) {

    setupMultiAdapterValidState(e);
    require(!ghostMaManager[who], "SCOPE: an account without manager rights");

    _MultiAdapter.updateManager(e, p, who, true);

    bool seatMid = ghostMaManager[who];

    _MultiAdapter.updateManager(e, p, who, false);

    bool seatAfter = ghostMaManager[who];

    satisfy(seatMid && !seatAfter, "an account can gain and then lose pool manager rights");
}

// MA-RC-16: both the gateway and the message reader can be replaced.
rule rcMaFileRepointsBothWiringTargetsIsReachable(env e, bytes32 whatGateway, address newGateway,
    bytes32 whatParser, address newParser) {

    setupMultiAdapterValidState(e);

    address gatewayBefore = _MultiAdapter.gateway;
    address parserBefore = _MultiAdapter.parser;

    _MultiAdapter.file(e, whatGateway, newGateway);
    _MultiAdapter.file(e, whatParser, newParser);

    address gatewayAfter = _MultiAdapter.gateway;
    address parserAfter = _MultiAdapter.parser;

    satisfy(gatewayAfter == newGateway && gatewayAfter != gatewayBefore
        && parserAfter == newParser && parserAfter != parserBefore,
        "the gateway and the pool-lookup reader can both take new addresses");
}

// MA-RC-17: admin rights can be granted to a new account and revoked again.
rule rcMaWardSeatGrantAndRevokeIsReachable(env e, address user) {

    setupMultiAdapterValidState(e);
    require(_MultiAdapter.wards[user] == 0, "SCOPE: an account that is not a ward");

    _MultiAdapter.rely(e, user);

    mathint wardMid = _MultiAdapter.wards[user];

    _MultiAdapter.deny(e, user);

    mathint wardAfter = _MultiAdapter.wards[user];

    satisfy(wardMid == 1 && wardAfter == 0, "a non-ward can become a ward and lose it again");
}
