import "MultiAdapter_valid_state.spec";

// MA-HL-01: executing a message consumes its votes only if enough adapters confirmed it.
rule hlMaExecuteSpendsATallyOnlyAtTheThreshold(env e, uint16 cid, bytes payload, address adapter,
    uint16 sid, bytes32 voteKey) {

    setupMultiAdapterValidState(e);
    uint16 s = sid;
    require(forall uint16 s2. s2 != s => ghostMaAdapterId8[s2][adapter] == 0,
        "SCOPE: the adapter is registered in this session only");

    mathint quorumBefore = ghostMaAdapterQuorum8[s][adapter];
    mathint thresholdBefore = ghostMaAdapterThreshold8[s][adapter];
    mathint lane0Before = _MultiAdapter.voteAt(e, cid, voteKey, 0);
    mathint lane1Before = _MultiAdapter.voteAt(e, cid, voteKey, 1);
    mathint lane2Before = _MultiAdapter.voteAt(e, cid, voteKey, 2);
    mathint lane3Before = _MultiAdapter.voteAt(e, cid, voteKey, 3);
    mathint lane4Before = _MultiAdapter.voteAt(e, cid, voteKey, 4);
    mathint lane5Before = _MultiAdapter.voteAt(e, cid, voteKey, 5);
    mathint lane6Before = _MultiAdapter.voteAt(e, cid, voteKey, 6);
    mathint lane7Before = _MultiAdapter.voteAt(e, cid, voteKey, 7);
    mathint positivesBefore = POSITIVE_LANES_MA(lane0Before, lane1Before, lane2Before, lane3Before,
        lane4Before, lane5Before, lane6Before, lane7Before, quorumBefore);

    _MultiAdapter.execute(e, cid, payload, adapter);

    mathint lane0After = _MultiAdapter.voteAt(e, cid, voteKey, 0);

    assert(lane0After < lane0Before => positivesBefore >= thresholdBefore,
        "an execution lowers adapter one's votes only if the threshold was met");
}

// MA-HL-02: with a single adapter, execution leaves the second adapter's votes untouched.
rule hlMaExecuteSparesTheSecondLaneOutsideTheQuorum(env e, uint16 cid, bytes payload, address adapter,
    uint16 sid, bytes32 voteKey) {

    setupMultiAdapterValidState(e);
    uint16 s = sid;
    require(forall uint16 s2. s2 != s => ghostMaAdapterId8[s2][adapter] == 0,
        "SCOPE: the adapter is registered in this session only");

    mathint quorumBefore = ghostMaAdapterQuorum8[s][adapter];
    mathint lane1Before = _MultiAdapter.voteAt(e, cid, voteKey, 1);

    _MultiAdapter.execute(e, cid, payload, adapter);

    mathint lane1After = _MultiAdapter.voteAt(e, cid, voteKey, 1);

    assert(quorumBefore <= 1 => lane1After == lane1Before,
        "with a quorum below two, an execution keeps adapter two's votes");
}

// MA-HL-03: with at most two adapters, execution leaves the third adapter's votes untouched.
rule hlMaExecuteSparesTheThirdLaneOutsideTheQuorum(env e, uint16 cid, bytes payload, address adapter,
    uint16 sid, bytes32 voteKey) {

    setupMultiAdapterValidState(e);
    uint16 s = sid;
    require(forall uint16 s2. s2 != s => ghostMaAdapterId8[s2][adapter] == 0,
        "SCOPE: the adapter is registered in this session only");

    mathint quorumBefore = ghostMaAdapterQuorum8[s][adapter];
    mathint lane2Before = _MultiAdapter.voteAt(e, cid, voteKey, 2);

    _MultiAdapter.execute(e, cid, payload, adapter);

    mathint lane2After = _MultiAdapter.voteAt(e, cid, voteKey, 2);

    assert(quorumBefore <= 2 => lane2After == lane2Before,
        "with a quorum below three, an execution keeps adapter three's votes");
}

// MA-HL-04: a successful execution passes exactly one message to the gateway.
rule hlMaExecuteForwardsExactlyOneMessage(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.execute(e, cid, payload, adapter);

    mathint forwardCountAfter = ghostGwHandleCount;

    assert(forwardCountAfter == forwardCountBefore + 1, "an execution hands the gateway exactly one message");
}

// MA-HL-05: an executed message reaches the gateway tagged with the network it came from.
rule hlMaExecuteForwardsOnTheArrivalChain(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);

    _MultiAdapter.execute(e, cid, payload, adapter);

    mathint forwardCidAfter = ghostGwLastHandleCid16;

    assert(forwardCidAfter == cid, "an execution forwards on the network the message came from");
}

// MA-HL-06: one adapter delivery passes at most one message to the gateway.
rule hlMaHandleForwardsAtMostOnce(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload, adapter);

    mathint forwardCountAfter = ghostGwHandleCount;

    assert(forwardCountAfter <= forwardCountBefore + 1, "the gateway receives no more than one message per delivery");
}

// MA-HL-07: a vote alone never passes a message to the gateway.
rule hlMaVoteNeverReachesTheGateway(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.vote(e, cid, payload, adapter);

    mathint forwardCountAfter = ghostGwHandleCount;

    assert(forwardCountAfter == forwardCountBefore, "a vote forwards nothing to the gateway");
}

// MA-HL-08: a new adapter set leaves existing sessions' adapter ids unchanged.
rule hlMaRotationKeepsEarlierSessionAdapterIds(env e, calldataarg args, uint16 sid, address adapter) {

    setupMultiAdapterValidState(e);

    uint16 s = sid;
    mathint sessionBefore = ghostMaActiveSessionId16;
    mathint idBefore = ghostMaAdapterId8[s][adapter];

    _MultiAdapter.setAdapters(e, args);

    mathint idAfter = ghostMaAdapterId8[s][adapter];

    assert(s <= sessionBefore => idAfter == idBefore, "a rotation keeps the adapter id of a session already minted");
}

// MA-HL-09: a new adapter set leaves existing sessions' quorums unchanged.
rule hlMaRotationKeepsEarlierSessionQuorums(env e, calldataarg args, uint16 sid, address adapter) {

    setupMultiAdapterValidState(e);

    uint16 s = sid;
    mathint sessionBefore = ghostMaActiveSessionId16;
    mathint quorumBefore = ghostMaAdapterQuorum8[s][adapter];

    _MultiAdapter.setAdapters(e, args);

    mathint quorumAfter = ghostMaAdapterQuorum8[s][adapter];

    assert(s <= sessionBefore => quorumAfter == quorumBefore,
        "a rotation keeps the quorum of a session already minted");
}

// MA-HL-10: a new adapter set leaves existing sessions' thresholds unchanged.
rule hlMaRotationKeepsEarlierSessionThresholds(env e, calldataarg args, uint16 sid, address adapter) {

    setupMultiAdapterValidState(e);

    uint16 s = sid;
    mathint sessionBefore = ghostMaActiveSessionId16;
    mathint thresholdBefore = ghostMaAdapterThreshold8[s][adapter];

    _MultiAdapter.setAdapters(e, args);

    mathint thresholdAfter = ghostMaAdapterThreshold8[s][adapter];

    assert(s <= sessionBefore => thresholdAfter == thresholdBefore,
        "a rotation keeps the threshold of a session already minted");
}

// MA-HL-11: blocking then unblocking a session keeps its confirmation threshold unchanged.
rule hlMaBlockThenUnblockKeepsTheThreshold(env e, uint16 cid, MultiAdapterHarness.PoolId p, uint16 sid) {

    // No extra requires: blockSession stashes the threshold, unblock restores it.
    setupMultiAdapter(e);

    uint16 s = sid;
    address headAdapterBefore = ghostMaSessionList[s][0];
    mathint thresholdBefore = ghostMaAdapterThreshold8[s][headAdapterBefore];

    _MultiAdapter.blockSession(e, cid, p, sid);
    _MultiAdapter.unblockSession(e, cid, p, sid);

    mathint thresholdAfter = ghostMaAdapterThreshold8[s][headAdapterBefore];

    assert(thresholdAfter == thresholdBefore, "a block-unblock round trip leaves the threshold as it was");
}

// MA-HL-12: one outbound send makes as many dispatches as the active set has adapters.
rule hlMaSendFansOutOncePerRosterMember(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund) {

    setupMultiAdapterValidState(e);

    mathint rosterLengthBefore = ghostMaActiveListLength8;
    mathint dispatchCountBefore = ghostMaFaceSendCount;

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    mathint dispatchCountAfter = ghostMaFaceSendCount;

    assert(dispatchCountAfter == dispatchCountBefore + rosterLengthBefore,
        "a send raises the dispatch count by the live roster size");
}

// MA-HL-13: an outbound message is sent to the destination network the caller named.
rule hlMaSendCarriesTheRequestedChain(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund) {

    setupMultiAdapterValidState(e);

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    mathint dispatchCidAfter = ghostMaFaceLastSendCid16;

    assert(dispatchCidAfter == cid, "the last dispatch goes to the network the send names");
}

// MA-HL-14: an outbound message passes on the refund address the caller gave.
rule hlMaSendCarriesTheRefundAddressItWasGiven(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund) {

    setupMultiAdapterValidState(e);

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    address dispatchRefundAfter = ghostMaFaceLastSendRefund;

    assert(dispatchRefundAfter == refund, "the last dispatch refunds the address the send was given");
}

// MA-HL-15: an outbound message is stamped with the active session id.
rule hlMaSendWrapsThePayloadWithTheLiveSessionId(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund) {

    setupMultiAdapterValidState(e);
    require(ghostMaActiveListLength8 == 1, "SCOPE: one live adapter, every adapter gets the same payload");

    mathint routeSessionBefore = ghostMaActiveSetSessionId16;

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    bytes1 stampHighAfter = ghostMaFaceLastSendByte0;
    bytes1 stampLowAfter = ghostMaFaceLastSendByte1;

    assert(stampHighAfter == to_bytes1(require_uint8(routeSessionBefore / 256))
        && stampLowAfter == to_bytes1(require_uint8(routeSessionBefore % 256)),
        "the dispatched payload carries the live route's session id");
}

// MA-HL-16: sending a message leaves the active adapter set unchanged.
rule hlMaSendLeavesTheLiveRouteWhereItStands(env e, uint16 cid, bytes payload, uint256 gasLimit,
    address refund, uint256 slot) {

    setupMultiAdapterValidState(e);

    mathint routeSessionBefore = ghostMaActiveSetSessionId16;
    mathint routeLengthBefore = ghostMaActiveListLength8;
    address routeSlotBefore = ghostMaActiveList[slot];

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    mathint routeSessionAfter = ghostMaActiveSetSessionId16;
    mathint routeLengthAfter = ghostMaActiveListLength8;
    address routeSlotAfter = ghostMaActiveList[slot];

    assert(routeSessionAfter == routeSessionBefore && routeLengthAfter == routeLengthBefore
        && routeSlotAfter == routeSlotBefore,
        "a send leaves the live roster and its session stamp unchanged");
}

// MA-HL-17: every adapter dispatch uses the gas limit the caller gave.
rule hlMaSendCarriesTheGasLimitItWasGiven(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund) {

    setupMultiAdapterValidState(e);
    require(ghostMaFaceLastSendGasLimit256 == gasLimit && !ghostMaFaceSendGasLimitVaried,
        "SAFE: binds the recorded gas limit to this send's limit");

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    bool gasLimitVariedAfter = ghostMaFaceSendGasLimitVaried;

    assert(!gasLimitVariedAfter, "every dispatch carries the gas limit the send was given");
}

// MA-HL-18: one outbound send reaches each adapter of the active set exactly once.
rule hlMaSendReachesEachRosterMemberOnce(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund,
    uint256 slot) {

    setupMultiAdapterValidState(e);
    require(slot < ghostMaActiveListLength8, "SCOPE: a member of the live roster");

    address member = ghostMaActiveList[slot];
    mathint memberDispatchesBefore = ghostMaFaceSendCountOf[member];

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    mathint memberDispatchesAfter = ghostMaFaceSendCountOf[member];

    assert(memberDispatchesAfter == memberDispatchesBefore + 1,
        "a send dispatches to each live roster member exactly once");
}

// MA-HL-19: each adapter dispatch is paid exactly the fee that adapter quoted.
rule hlMaSendFundsEachDispatchWithItsOwnQuote(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund) {

    setupMultiAdapterValidState(e);

    bool misfundedBefore = ghostMaFaceDispatchMisfunded;

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    bool misfundedAfter = ghostMaFaceDispatchMisfunded;

    assert(!misfundedBefore => !misfundedAfter, "every dispatch is funded with exactly its adapter's quote");
}

// MA-HL-20: an outbound message is two bytes longer than its payload, so nothing is cut.
rule hlMaSendDispatchesTheStampedPayloadAtFullLength(env e, uint16 cid, bytes payload, uint256 gasLimit,
    address refund) {

    setupMultiAdapterValidState(e);
    require(ghostMaActiveListLength8 == 1, "SCOPE: one live adapter, every adapter gets the same payload");

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    mathint dispatchLengthAfter = ghostMaFaceLastSendLength;

    assert(dispatchLengthAfter == payload.length + 2, "a dispatch is the payload plus exactly two session-stamp bytes");
}

// MA-HL-26: each adapter dispatch is paid the quote that same adapter gave just before it.
rule hlMaSendPaysEachAdapterTheQuoteItGaveItself(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund) {

    setupMultiAdapterValidState(e);
    require(!ghostMaFaceDispatchMisfunded && !ghostMaFaceDispatchQuotedByAnother,
        "SAFE: the dispatch recorders start clean");

    _MultiAdapter.send(e, cid, payload, gasLimit, refund);

    assert(!ghostMaFaceDispatchMisfunded && !ghostMaFaceDispatchQuotedByAnother,
        "every dispatch pays the latest quote, made by its own adapter");
}

// MA-HL-37: a new adapter set moves the session id up by one, to the named id, which the route then uses.
rule hlMaRotationBumpsTheSessionToTheNamedTarget(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    address[] addresses, uint8 newThreshold, uint16 targetSessionId) {

    setupMultiAdapter(e);

    mathint sessionBefore = ghostMaActiveSessionId16;

    _MultiAdapter.setAdapters(e, cid, p, addresses, newThreshold, targetSessionId);

    assert(ghostMaActiveSessionId16 == sessionBefore + 1
        && ghostMaActiveSessionId16 == targetSessionId
        && ghostMaActiveSetSessionId16 == ghostMaActiveSessionId16,
        "the session steps once onto the target and the route follows");
}

// MA-HL-38: a successful unblock empties the session's stash and puts the stashed roster back in that session.
rule hlMaUnblockEmptiesTheStashIntoItsOwnSession(env e, uint16 cid, MultiAdapterHarness.PoolId p, uint16 sid,
    uint256 i) {

    setupMultiAdapter(e);
    require(cid == ghostMaCid16, "SCOPE: the modelled remote network");
    require(VALID_POOL(p), "SCOPE: the modelled pool");
    require(i < MAX_ADAPTERS_CVL(), "SAFE: no roster has a position past the eighth");

    uint16 s = sid;
    mathint stashLengthBefore = ghostMaBlockedListLength8[s];
    address stashSlotBefore = _MultiAdapter.blockedListAt(e, cid, p, sid, i);

    _MultiAdapter.unblockSession(e, cid, p, sid);

    assert(ghostMaBlockedListLength8[s] == 0, "a successful unblock leaves no stash behind");
    assert(ghostMaSessionListLength8[s] == stashLengthBefore
        && (i < stashLengthBefore => ghostMaSessionList[s][i] == stashSlotBefore),
        "the stashed roster is back in the session the unblock names");
}

// MA-HL-41: setting, blocking or unblocking adapters asks no adapter for a quote or a send.
rule hlMaRotationCallsNoAdapter(env e, method f, calldataarg args)
    filtered { f -> ROTATION_FUNCTION_MA(f)
        || f.selector == sig:_MultiAdapter.blockSession(uint16,MultiAdapterHarness.PoolId,uint16).selector
        || f.selector == sig:_MultiAdapter.unblockSession(uint16,MultiAdapterHarness.PoolId,uint16).selector } {

    setupMultiAdapterValidState(e);

    mathint dispatchCountBefore = ghostMaFaceSendCount;
    mathint quoteCountBefore = ghostMaFaceQuoteCount;

    f(e, args);

    assert(ghostMaFaceSendCount == dispatchCountBefore && ghostMaFaceQuoteCount == quoteCountBefore,
        "an adapter change asks no adapter for a quote or a send");
}
