import "single/MultiAdapter_valid_state.spec";

using MultiAdapterPayloadHarness as _MaPayload;
using MultiAdapterSessionHarness as _MaSession;

function futureSessionSetupMA(env e, env eFunc) {
    requireInvariant sessionsAboveCounterEmpty(e);
    requireInvariant adapterIdPointsAtItsOwnSlot(e);
    SETUP_MA(e, eFunc);
}

// The prover's key image leaves the session at byte 8 unseparated, so collision freedom is stated.
function futureKeyCarriesItsSessionMA(env e, uint16 sid, bytes inner, bytes32 voteKey, bytes payload) {
    require(voteKey == _MaPayload.voteKeyOf(e, ghostPoolA64, _MaPayload.stamp(e, sid, inner))
        && _MaPayload.voteKeyOf(e, ghostPoolA64, payload) == voteKey => _MaSession.sessionOf(e, payload) == sid,
        "SAFE: keccak is collision free, so a message on a stamp's key carries that stamp's session");
}

// --- valid_state ---

// MA-VS-17: no message stamped with a session id not yet issued has any votes recorded.
invariant futureSessionTallyEmpty(env e, uint16 sid, bytes inner, bytes32 voteKey)
    (sid > ghostMaActiveSessionId16
        && voteKey == _MaPayload.voteKeyOf(e, ghostPoolA64, _MaPayload.stamp(e, sid, inner)))
    => (_MultiAdapter.voteAt(e, ghostMaCid16, voteKey, 0) == 0 && _MultiAdapter.voteAt(e, ghostMaCid16, voteKey, 1) == 0
        && _MultiAdapter.voteAt(e, ghostMaCid16, voteKey, 2) == 0 && _MultiAdapter.voteAt(e, ghostMaCid16, voteKey, 3) == 0
        && _MultiAdapter.voteAt(e, ghostMaCid16, voteKey, 4) == 0 && _MultiAdapter.voteAt(e, ghostMaCid16, voteKey, 5) == 0
        && _MultiAdapter.voteAt(e, ghostMaCid16, voteKey, 6) == 0 && _MultiAdapter.voteAt(e, ghostMaCid16, voteKey, 7) == 0)
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {
    preserved with (env eFunc) { futureSessionSetupMA(e, eFunc); }
    preserved vote(uint16 c, bytes payload) with (env eFunc) {
        futureSessionSetupMA(e, eFunc);
        futureKeyCarriesItsSessionMA(e, sid, inner, voteKey, payload);
    }
    preserved vote(uint16 c, bytes payload, address a) with (env eFunc) {
        futureSessionSetupMA(e, eFunc);
        futureKeyCarriesItsSessionMA(e, sid, inner, voteKey, payload);
    }
    preserved handle(uint16 c, bytes payload) with (env eFunc) {
        futureSessionSetupMA(e, eFunc);
        futureKeyCarriesItsSessionMA(e, sid, inner, voteKey, payload);
    }
    preserved handle(uint16 c, bytes payload, address a) with (env eFunc) {
        futureSessionSetupMA(e, eFunc);
        futureKeyCarriesItsSessionMA(e, sid, inner, voteKey, payload);
    }
    preserved execute(uint16 c, bytes payload) with (env eFunc) {
        futureSessionSetupMA(e, eFunc);
        futureKeyCarriesItsSessionMA(e, sid, inner, voteKey, payload);
    }
    preserved execute(uint16 c, bytes payload, address a) with (env eFunc) {
        futureSessionSetupMA(e, eFunc);
        futureKeyCarriesItsSessionMA(e, sid, inner, voteKey, payload);
    }
}

// --- high_level ---

// MA-HL-21: an execution succeeds only if the message already had enough confirmations for the threshold.
rule hlMaExecuteForwardsOnlyOverAThresholdOfPositiveLanes(env e, uint16 cid, uint16 sid, bytes inner, address adapter) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);
    bytes32 voteKey = _MaPayload.voteKeyOf(e, ghostPoolA64, payload);

    mathint quorumBefore = ghostMaAdapterQuorum8[sid][adapter];
    mathint thresholdBefore = ghostMaAdapterThreshold8[sid][adapter];
    mathint lane0Before = _MultiAdapter.voteAt(e, cid, voteKey, 0);
    mathint lane1Before = _MultiAdapter.voteAt(e, cid, voteKey, 1);
    mathint lane2Before = _MultiAdapter.voteAt(e, cid, voteKey, 2);
    mathint lane3Before = _MultiAdapter.voteAt(e, cid, voteKey, 3);
    mathint lane4Before = _MultiAdapter.voteAt(e, cid, voteKey, 4);
    mathint lane5Before = _MultiAdapter.voteAt(e, cid, voteKey, 5);
    mathint lane6Before = _MultiAdapter.voteAt(e, cid, voteKey, 6);
    mathint lane7Before = _MultiAdapter.voteAt(e, cid, voteKey, 7);

    _MultiAdapter.execute(e, cid, payload, adapter);

    assert(POSITIVE_LANES_MA(lane0Before, lane1Before, lane2Before, lane3Before, lane4Before, lane5Before,
            lane6Before, lane7Before, quorumBefore) >= thresholdBefore,
        "a released message already had a threshold of positive votes");
}

// MA-HL-22: an execution updates the message's votes before the gateway call, never after it.
rule hlMaExecuteSpendsTheTallyBeforeForwarding(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);
    require(ghostMaVoteForwardMark == ghostGwHandleCount
        && !ghostMaVoteWrittenBeforeForward && !ghostMaVoteWrittenAfterForward,
        "SAFE: the vote recorder starts clean at this call");

    _MultiAdapter.execute(e, cid, payload, adapter);

    assert(ghostMaVoteWrittenBeforeForward && !ghostMaVoteWrittenAfterForward,
        "votes are written before the forward and not once after it");
}

// MA-HL-23: an execution lowers the first adapter's vote count on the message it releases.
rule hlMaExecuteLowersTheTallyItSpends(env e, uint16 cid, uint16 sid, bytes inner, address adapter) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);
    bytes32 voteKey = _MaPayload.voteKeyOf(e, ghostPoolA64, payload);

    mathint lane0Before = _MultiAdapter.voteAt(e, cid, voteKey, 0);

    _MultiAdapter.execute(e, cid, payload, adapter);

    assert(_MultiAdapter.voteAt(e, cid, voteKey, 0) < lane0Before, "adapter one's recorded votes on the message drop");
}

// MA-HL-24: an execution passes the gateway one message, the original without its session stamp.
rule hlMaExecuteHandsTheGatewayTheUnstampedMessage(env e, uint16 cid, uint16 sid, bytes inner, address adapter) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.execute(e, cid, payload, adapter);

    assert(ghostGwHandleCount == forwardCountBefore + 1 && ghostGwLastHandleHash == keccak256(inner),
        "the gateway gets a single forward of the unstamped message");
}

// MA-HL-27: a delivery that releases a message passes the gateway the original without its session stamp.
rule hlMaHandleHandsTheGatewayTheUnstampedMessage(env e, uint16 cid, uint16 sid, bytes inner, address adapter) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload, adapter);

    assert(ghostGwHandleCount == forwardCountBefore + 1 => ghostGwLastHandleHash == keccak256(inner),
        "a release forwards the unstamped message");
}

// MA-HL-36: a delivery that releases a message updates its votes before the gateway call, never after.
rule hlMaHandleSpendsTheTallyBeforeForwarding(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);
    require(ghostMaVoteForwardMark == ghostGwHandleCount
        && !ghostMaVoteWrittenBeforeForward && !ghostMaVoteWrittenAfterForward,
        "SAFE: the vote recorder starts clean at this call");

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload, adapter);

    assert(ghostGwHandleCount == forwardCountBefore + 1
        => ghostMaVoteWrittenBeforeForward && !ghostMaVoteWrittenAfterForward,
        "on a release, votes are written before the forward and never after");
}

// --- reachability ---

// MA-RC-18: a message can be released twice when its only adapter delivers it again.
rule rcMaSamePayloadIsReleasedTwiceIsReachable(env e, uint16 cid, uint16 sid, bytes inner, address adapter) {

    // Requires below pin each row to what setAdapters([adapter], 1) at sid leaves.
    setupMultiAdapter(e);
    require(ghostMaActiveSessionId16 == sid && sid != 0, "SCOPE: the live session, any nonzero id, stamps the message");
    require(ghostMaAdapterId8[sid][adapter] == 1 && ghostMaAdapterQuorum8[sid][adapter] == 1
        && ghostMaAdapterThreshold8[sid][adapter] == 1,
        "SAFE: the lone adapter's id, quorum and threshold are one");
    require(e.msg.sender == adapter, "SCOPE: the adapter delivers for itself");
    require(inner.length == 32, "SCOPE: a one-word message");
    bytes payload = _MaPayload.stamp(e, sid, inner);

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload);

    bytes32 firstForwardHash = ghostGwLastHandleHash;

    _MultiAdapter.handle(e, cid, payload);

    satisfy(ghostGwHandleCount == forwardCountBefore + 2 && ghostGwLastHandleHash == firstForwardHash,
        "two deliveries of one stamped message can each forward it");
}

// MA-RC-20: a pool manager can release a message in an adapter's name without any adapter delivering it.
rule rcMaAManagerReleasesAPayloadNoAdapterDeliveredIsReachable(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);
    require(ghostMaActiveSessionId16 == 1, "SCOPE: only session one is configured");
    require(ghostMaSessionListLength8[1] == 2 && ghostMaAdapterThreshold8[1][adapter] == 1,
        "SCOPE: a one-of-two session");
    require(ghostMaAdapterId8[1][adapter] != 0, "SCOPE: the adapter sits in session one");
    require(e.msg.sender != adapter && ghostMaManager[e.msg.sender],
        "SCOPE: a pool manager submits in the adapter's name");
    require(forall uint16 s. ghostMaAdapterId8[s][e.msg.sender] == 0,
        "SCOPE: the manager is no adapter of any session");

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload, adapter);

    satisfy(ghostGwHandleCount == forwardCountBefore + 1 && ghostGwLastHandleCid16 == cid,
        "a manager's submission alone can forward a message");
}

// MA-RC-21: the pool's adapter manager can release a two-of-two message no adapter confirmed.
rule rcMaManagerAloneReleasesATwoOfTwoMessageIsReachable(env e, uint16 cid, bytes inner, address adapterA,
    address adapterB) {

    setupMultiAdapterValidState(e);
    require(ghostMaActiveSessionId16 == 1, "SCOPE: only session one is configured");
    require(ghostMaSessionListLength8[1] == 2 && ghostMaAdapterThreshold8[1][adapterA] == 2,
        "SCOPE: a two-of-two session");
    require(ghostMaAdapterId8[1][adapterA] == 1 && ghostMaAdapterId8[1][adapterB] == 2,
        "SCOPE: the two adapters hold ids one and two");
    require(ghostMaAdapterQuorum8[1][adapterA] == 2 && ghostMaAdapterQuorum8[1][adapterB] == 2
        && ghostMaAdapterThreshold8[1][adapterB] == 2,
        "SAFE: every adapter of a session shares its quorum and threshold");
    require(ghostMaManager[e.msg.sender] && (forall uint16 s. ghostMaAdapterId8[s][e.msg.sender] == 0),
        "SCOPE: the manager is no adapter of any session");
    require(inner.length == 32, "SCOPE: a one-word message");
    bytes payload = _MaPayload.stamp(e, 1, inner);
    bytes32 voteKey = _MaPayload.voteKeyOf(e, ghostPoolA64, payload);
    require(_MultiAdapter.voteAt(e, cid, voteKey, 0) == 0 && _MultiAdapter.voteAt(e, cid, voteKey, 1) == 0,
        "SCOPE: no adapter has confirmed the message");

    mathint forwardCountBefore = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload, adapterA);

    mathint forwardCountMid = ghostGwHandleCount;

    _MultiAdapter.handle(e, cid, payload, adapterB);

    satisfy(forwardCountMid == forwardCountBefore && ghostGwHandleCount == forwardCountBefore + 1,
        "the first submission forwards nothing, the second forwards the message");
}
