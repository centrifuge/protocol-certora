import "MultiAdapter_valid_state.spec";

using MultiAdapterPayloadHarness as _MaPayload;

// MA-RV-01: a configuration update fails for a non-admin caller or an unknown setting.
rule rvMaFileRefusesANonWardOrAnUnknownName(env e, bytes32 what, address instance) {

    setupMultiAdapterValidState(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool unknownParam = what != FILE_GATEWAY_MA_CVL() && what != FILE_PARSER_MA_CVL()
        && what != FILE_MESSAGE_GAS_MA_CVL();

    _MultiAdapter.file@withrevert(e, what, instance);
    bool reverted = lastReverted;

    assert((senderWardBefore != 1 || unknownParam) => reverted, "rewiring fails for a non-ward or an unknown name");
}

// MA-RV-02: only an admin can grant or revoke adapter manager rights for a pool.
rule rvMaUpdateManagerRefusesANonWard(env e, MultiAdapterHarness.PoolId p, address who, bool canManage) {

    setupMultiAdapterValidState(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];

    _MultiAdapter.updateManager@withrevert(e, p, who, canManage);
    bool reverted = lastReverted;

    assert(senderWardBefore != 1 => reverted, "granting or revoking a pool manager fails for a non-ward");
}

// MA-RV-03: only an admin or the pool's adapter manager can replace the pool's adapter set.
rule rvMaSetAdaptersRefusesWithoutTransportAuthority(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    address[] addresses, uint8 newThreshold, uint16 targetSessionId) {

    setupMultiAdapterValidState(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool senderManagerBefore = _MultiAdapter.manager[p][e.msg.sender];

    _MultiAdapter.setAdapters@withrevert(e, cid, p, addresses, newThreshold, targetSessionId);
    bool reverted = lastReverted;

    assert((senderWardBefore != 1 && !senderManagerBefore) => reverted,
        "installing adapters fails for a caller neither ward nor pool manager");
}

// MA-RV-04: an adapter set whose threshold exceeds its adapter count is rejected.
rule rvMaSetAdaptersRefusesAnUnreachableThreshold(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    address[] addresses, uint8 newThreshold, uint16 targetSessionId) {

    setupMultiAdapterValidState(e);

    mathint rosterSize = addresses.length;
    mathint requestedThreshold = newThreshold;

    _MultiAdapter.setAdapters@withrevert(e, cid, p, addresses, newThreshold, targetSessionId);
    bool reverted = lastReverted;

    assert(requestedThreshold > rosterSize => reverted, "an adapter set with a threshold above its size is refused");
}

// MA-RV-05: a non-empty adapter set with a zero threshold is rejected.
rule rvMaSetAdaptersRefusesAZeroThresholdOverALiveRoster(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    address[] addresses, uint8 newThreshold, uint16 targetSessionId) {

    setupMultiAdapterValidState(e);

    mathint rosterSize = addresses.length;
    mathint requestedThreshold = newThreshold;

    _MultiAdapter.setAdapters@withrevert(e, cid, p, addresses, newThreshold, targetSessionId);
    bool reverted = lastReverted;

    assert((requestedThreshold == 0 && rosterSize > 0) => reverted,
        "a zero threshold reverts whenever the set has an adapter");
}

// MA-RV-06: an adapter set listing the same adapter twice is rejected.
rule rvMaSetAdaptersRefusesARepeatedAdapter(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    address[] addresses, uint8 newThreshold, uint16 targetSessionId, uint256 i, uint256 j) {

    setupMultiAdapterValidState(e);
    require(i < addresses.length && j < addresses.length && i != j,
        "SCOPE: two distinct positions in the proposed roster");

    bool repeated = addresses[i] == addresses[j];

    _MultiAdapter.setAdapters@withrevert(e, cid, p, addresses, newThreshold, targetSessionId);
    bool reverted = lastReverted;

    assert(repeated => reverted, "a duplicate in the adapter list makes the install revert");
}

// MA-RV-07: installing an adapter set fails unless it names the next session id.
rule rvMaSetAdaptersRefusesAnUnexpectedSessionId(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    address[] addresses, uint8 newThreshold, uint16 targetSessionId) {

    setupMultiAdapterValidState(e);

    mathint sessionBefore = _MultiAdapter.activeSessionId[cid][p];
    bool mismatched = targetSessionId != sessionBefore + 1;

    _MultiAdapter.setAdapters@withrevert(e, cid, p, addresses, newThreshold, targetSessionId);
    bool reverted = lastReverted;

    assert(mismatched => reverted, "an install not naming the next session id is refused");
}

// MA-RV-08: an admin can always move a pool onto one new adapter at the next session id.
rule rvMaSetAdaptersOnAFreshRosterAlwaysGoesThroughForAWard(env e, uint16 cid,
    MultiAdapterHarness.PoolId p, address[] addresses, address rosterEntry, uint8 newThreshold,
    uint16 targetSessionId) {

    setupMultiAdapterValidState(e);
    require(_MultiAdapter.wards[e.msg.sender] == 1, "SCOPE: the caller is a ward");
    require(addresses.length == 1, "SCOPE: a one-adapter roster, so no repeats");
    require(addresses[0] == rosterEntry, "ASSERT: the decoder refuses a dirty address word");
    require(newThreshold == 1, "SCOPE: threshold one, full consensus");
    require(targetSessionId == _MultiAdapter.activeSessionId[cid][p] + 1,
        "SCOPE: the install names the next session id");
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    _MultiAdapter.setAdapters@withrevert(e, cid, p, addresses, newThreshold, targetSessionId);
    bool reverted = lastReverted;

    assert(!reverted, "a ward's one-adapter install at threshold one never fails");
}

// MA-RV-09: blocking a session fails for an unauthorized caller or a session with no adapters.
rule rvMaBlockSessionRefusesAnOutsiderOrASessionWithNoRoster(env e, uint16 cid,
    MultiAdapterHarness.PoolId p, uint16 sid) {

    setupMultiAdapterValidState(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool senderManagerBefore = _MultiAdapter.manager[p][e.msg.sender];
    mathint rosterSizeBefore = _MultiAdapter.adapters[cid][p][sid].length;

    _MultiAdapter.blockSession@withrevert(e, cid, p, sid);
    bool reverted = lastReverted;

    assert(((senderWardBefore != 1 && !senderManagerBefore) || rosterSizeBefore == 0) => reverted,
        "blocking fails for a caller neither ward nor pool manager, or an empty session");
}

// MA-RV-10: only an admin or a pool's adapter manager can unblock the pool's sessions.
rule rvMaUnblockSessionRefusesWithoutTransportAuthority(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    uint16 sid) {

    setupMultiAdapterValidState(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool senderManagerBefore = _MultiAdapter.manager[p][e.msg.sender];

    _MultiAdapter.unblockSession@withrevert(e, cid, p, sid);
    bool reverted = lastReverted;

    assert((senderWardBefore != 1 && !senderManagerBefore) => reverted,
        "unblocking fails for a caller neither ward nor pool manager");
}

// MA-RV-11: unblocking fails for a session that is not blocked.
rule rvMaUnblockSessionRefusesWithoutAStashedSession(env e, uint16 cid, MultiAdapterHarness.PoolId p,
    uint16 sid) {

    setupMultiAdapterValidState(e);

    mathint stashSizeBefore = _MultiAdapter._blockedSessions[cid][p][sid].list.length;

    _MultiAdapter.unblockSession@withrevert(e, cid, p, sid);
    bool reverted = lastReverted;

    assert(stashSizeBefore == 0 => reverted, "an unblock reverts unless the session is currently blocked");
}

// MA-RV-12: an admin can always unblock a blocked single-adapter session.
rule rvMaUnblockSessionOfASingleStashAlwaysGoesThroughForAWard(env e, uint16 cid,
    MultiAdapterHarness.PoolId p, uint16 sid) {

    setupMultiAdapterValidState(e);
    require(_MultiAdapter.wards[e.msg.sender] == 1, "SCOPE: the caller is a ward");
    require(_MultiAdapter._blockedSessions[cid][p][sid].list.length == 1, "SCOPE: a one-adapter stash, so no repeats");
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    _MultiAdapter.unblockSession@withrevert(e, cid, p, sid);
    bool reverted = lastReverted;

    assert(!reverted, "a ward's unblock of a one-adapter stash never fails");
}

// MA-RV-13: a delivery fails unless sent by the adapter or the adapter manager of the message's pool.
rule rvMaHandleRefusesAStrangerSubmission(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);

    bool senderManagerBefore = ghostMaManager[e.msg.sender];
    bool strangerSubmission = e.msg.sender != adapter;

    _MultiAdapter.handle@withrevert(e, cid, payload, adapter);
    bool reverted = lastReverted;

    assert((strangerSubmission && !senderManagerBefore) => reverted,
        "a delivery fails unless the caller is the adapter or a pool manager");
}

// MA-RV-14: a vote fails unless cast by the adapter or the adapter manager of the message's pool.
rule rvMaVoteRefusesAStrangerSubmission(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);

    bool senderManagerBefore = ghostMaManager[e.msg.sender];
    bool strangerSubmission = e.msg.sender != adapter;

    _MultiAdapter.vote@withrevert(e, cid, payload, adapter);
    bool reverted = lastReverted;

    assert((strangerSubmission && !senderManagerBefore) => reverted,
        "a vote fails unless the caller is the adapter or a pool manager");
}

// MA-RV-15: an execution fails unless made by the adapter or the adapter manager of the message's pool.
rule rvMaExecuteRefusesAStrangerSubmission(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);

    bool senderManagerBefore = ghostMaManager[e.msg.sender];
    bool strangerSubmission = e.msg.sender != adapter;

    _MultiAdapter.execute@withrevert(e, cid, payload, adapter);
    bool reverted = lastReverted;

    assert((strangerSubmission && !senderManagerBefore) => reverted,
        "an execution fails unless the caller is the adapter or a pool manager");
}

// MA-RV-16: executing a message fails for an adapter not registered in any session.
rule rvMaExecuteRefusesAnUnregisteredAdapter(env e, uint16 cid, bytes payload, address adapter) {

    setupMultiAdapterValidState(e);

    bool adapterUnregisteredBefore = forall uint16 s. ghostMaAdapterId8[s][adapter] == 0;

    _MultiAdapter.execute@withrevert(e, cid, payload, adapter);
    bool reverted = lastReverted;

    assert(adapterUnregisteredBefore => reverted, "executing on behalf of an adapter no session lists reverts");
}

// MA-RV-17: an address registered in no session cannot deliver a message in its own name.
rule rvMaHandleRefusesAnUnregisteredSender(env e, uint16 cid, bytes payload) {

    setupMultiAdapterValidState(e);

    bool senderUnregisteredBefore = forall uint16 s. ghostMaAdapterId8[s][e.msg.sender] == 0;

    _MultiAdapter.handle@withrevert(e, cid, payload);
    bool reverted = lastReverted;

    assert(senderUnregisteredBefore => reverted, "a direct delivery from an unregistered address fails");
}

// MA-RV-18: an address registered in no session cannot cast a vote in its own name.
rule rvMaVoteRefusesAnUnregisteredSender(env e, uint16 cid, bytes payload) {

    setupMultiAdapterValidState(e);

    bool senderUnregisteredBefore = forall uint16 s. ghostMaAdapterId8[s][e.msg.sender] == 0;

    _MultiAdapter.vote@withrevert(e, cid, payload);
    bool reverted = lastReverted;

    assert(senderUnregisteredBefore => reverted, "a direct vote from an unregistered address fails");
}

// MA-RV-19: an address registered in no session cannot execute a message in its own name.
rule rvMaExecuteRefusesAnUnregisteredSender(env e, uint16 cid, bytes payload) {

    setupMultiAdapterValidState(e);

    bool senderUnregisteredBefore = forall uint16 s. ghostMaAdapterId8[s][e.msg.sender] == 0;

    _MultiAdapter.execute@withrevert(e, cid, payload);
    bool reverted = lastReverted;

    assert(senderUnregisteredBefore => reverted, "a direct execution from an unregistered address fails");
}

// MA-RV-20: only an admin can send an outbound message.
rule rvMaSendRefusesANonWard(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund) {

    setupMultiAdapterValidState(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];

    _MultiAdapter.send@withrevert(e, cid, payload, gasLimit, refund);
    bool reverted = lastReverted;

    assert(senderWardBefore != 1 => reverted, "sending a message fails for a non-ward");
}

// MA-RV-21: a send with no active adapters fails instead of dropping the message.
rule rvMaSendRefusesWithoutALiveRoster(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund) {

    setupMultiAdapterValidState(e);

    mathint rosterSizeBefore = ghostMaActiveListLength8;

    _MultiAdapter.send@withrevert(e, cid, payload, gasLimit, refund);
    bool reverted = lastReverted;

    assert(rosterSizeBefore == 0 => reverted, "sending fails while the live roster is empty");
}

// MA-RV-22: a cost estimate with no active adapters fails instead of quoting zero.
rule rvMaEstimateRefusesWithoutALiveRoster(env e, uint16 cid, bytes payload, uint256 gasLimit) {

    setupMultiAdapterValidState(e);

    mathint rosterSizeBefore = ghostMaActiveListLength8;

    _MultiAdapter.estimate@withrevert(e, cid, payload, gasLimit);
    bool reverted = lastReverted;

    assert(rosterSizeBefore == 0 => reverted, "quoting a send fails while the live roster is empty");
}

// MA-RV-23: reading a pool's adapter quorum never fails, even with no active adapters.
rule rvMaQuorumAlwaysAnswers(env e, uint16 cid, MultiAdapterHarness.PoolId p) {

    setupMultiAdapterValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    _MultiAdapter.quorum@withrevert(e, cid, p);
    bool reverted = lastReverted;

    assert(!reverted, "a pool's quorum stays readable in every valid state");
}

// MA-RV-24: reading a pool's adapter threshold never fails, even with no active adapters.
rule rvMaThresholdAlwaysAnswers(env e, uint16 cid, MultiAdapterHarness.PoolId p) {

    setupMultiAdapterValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    _MultiAdapter.threshold@withrevert(e, cid, p);
    bool reverted = lastReverted;

    assert(!reverted, "a pool's threshold stays readable in every valid state");
}

// MA-RV-25: looking up the next session id fails once the session counter is exhausted.
rule rvMaNextActiveSessionIdRefusesARouteWhoseCounterIsSpent(env e, uint16 cid,
    MultiAdapterHarness.PoolId p) {

    setupMultiAdapterValidState(e);

    mathint sessionBefore = _MultiAdapter.activeSessionId[cid][p];

    _MultiAdapter.nextActiveSessionId@withrevert(e, cid, p);
    bool reverted = lastReverted;

    assert(sessionBefore == max_uint16 => reverted, "reading the next session id fails once session ids run out");
}

// MA-RV-26: a delivery fails if the adapter is not part of the message's session.
rule rvMaHandleRefusesASessionTheAdapterIsNotIn(env e, uint16 cid, bytes inner, address adapter, uint16 sid) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);

    bool adapterOutsideTheStampedSession = ghostMaAdapterId8[sid][adapter] == 0;

    _MultiAdapter.handle@withrevert(e, cid, payload, adapter);
    bool reverted = lastReverted;

    assert(adapterOutsideTheStampedSession => reverted,
        "a delivery stamped with a session the adapter is not in fails");
}

// MA-RV-27: a vote fails if the adapter it names is not part of the message's session.
rule rvMaVoteRefusesASessionTheAdapterIsNotIn(env e, uint16 cid, bytes inner, address adapter, uint16 sid) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);

    bool adapterOutsideTheStampedSession = ghostMaAdapterId8[sid][adapter] == 0;

    _MultiAdapter.vote@withrevert(e, cid, payload, adapter);
    bool reverted = lastReverted;

    assert(adapterOutsideTheStampedSession => reverted, "a vote naming an adapter outside the stamped session fails");
}

// MA-RV-28: an execution fails if the adapter it names is not part of the message's session.
rule rvMaExecuteRefusesASessionTheAdapterIsNotIn(env e, uint16 cid, bytes inner, address adapter, uint16 sid) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);

    bool adapterOutsideTheStampedSession = ghostMaAdapterId8[sid][adapter] == 0;

    _MultiAdapter.execute@withrevert(e, cid, payload, adapter);
    bool reverted = lastReverted;

    assert(adapterOutsideTheStampedSession => reverted,
        "an execution naming an adapter outside the stamped session fails");
}

// MA-RV-29: an adapter's own delivery fails if it is not part of the message's session.
rule rvMaSelfDeliveryHandleRefusesASessionTheSenderIsNotIn(env e, uint16 cid, bytes inner, uint16 sid) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);

    bool senderOutsideTheStampedSession = ghostMaAdapterId8[sid][e.msg.sender] == 0;

    _MultiAdapter.handle@withrevert(e, cid, payload);
    bool reverted = lastReverted;

    assert(senderOutsideTheStampedSession => reverted, "a delivery sent from outside the stamped session fails");
}

// MA-RV-30: an adapter's own vote fails if it is not part of the message's session.
rule rvMaSelfDeliveryVoteRefusesASessionTheSenderIsNotIn(env e, uint16 cid, bytes inner, uint16 sid) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);

    bool senderOutsideTheStampedSession = ghostMaAdapterId8[sid][e.msg.sender] == 0;

    _MultiAdapter.vote@withrevert(e, cid, payload);
    bool reverted = lastReverted;

    assert(senderOutsideTheStampedSession => reverted, "a vote cast from outside the stamped session fails");
}

// MA-RV-31: an adapter's own execution fails if it is not part of the message's session.
rule rvMaSelfDeliveryExecuteRefusesASessionTheSenderIsNotIn(env e, uint16 cid, bytes inner, uint16 sid) {

    setupMultiAdapterValidState(e);
    bytes payload = _MaPayload.stamp(e, sid, inner);

    bool senderOutsideTheStampedSession = ghostMaAdapterId8[sid][e.msg.sender] == 0;

    _MultiAdapter.execute@withrevert(e, cid, payload);
    bool reverted = lastReverted;

    assert(senderOutsideTheStampedSession => reverted, "an execution sent from outside the stamped session fails");
}

// MA-RV-32: setting the gateway, parser or gas model never fails for an admin.
rule rvMaFileAcceptsAWardUnderAKnownName(env e, bytes32 what, address instance) {

    setupMultiAdapterValidState(e);

    bool known = what == FILE_GATEWAY_MA_CVL() || what == FILE_PARSER_MA_CVL() || what == FILE_MESSAGE_GAS_MA_CVL();
    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];

    _MultiAdapter.file@withrevert(e, what, instance);
    bool reverted = lastReverted;

    assert(senderWardBefore == 1 && known && e.msg.value == 0 => !reverted,
        "a ward can always rewire a known dependency");
}

// MA-RV-33: a send and its quote both fail when one active adapter rejects them.
rule rvMaSendFailsWhenARosterAdapterRefuses(env e, uint16 cid, bytes payload, uint256 gasLimit, address refund,
    uint8 k) {

    setupMultiAdapterValidState(e);
    require(to_mathint(k) < ghostMaActiveListLength8, "SCOPE: one adapter of the active set");

    bool memberRefuses = ghostMaFaceRefuses[ghostMaActiveList[k]];

    storage init = lastStorage;

    _MultiAdapter.estimate@withrevert(e, cid, payload, gasLimit) at init;
    bool quoteReverted = lastReverted;

    _MultiAdapter.send@withrevert(e, cid, payload, gasLimit, refund) at init;
    bool sendReverted = lastReverted;

    assert(memberRefuses => quoteReverted && sendReverted, "one rejecting active adapter stops both the quote and the send");
}
