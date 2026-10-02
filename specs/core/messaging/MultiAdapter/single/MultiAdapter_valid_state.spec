import "../setup/MultiAdapter_base.spec";

function setupMultiAdapterValidState(env e) {
    setupMultiAdapter(e);
    requireInvariant activeSetSessionCurrentOrCleared(e);
    requireInvariant clearedActiveSetEmpty(e);
    requireInvariant activeSetMirrorsSessionList(e);
    requireInvariant sessionsAboveCounterEmpty(e);
    requireInvariant blockedAboveCounterEmpty(e);
    requireInvariant sessionZeroNeverConfigured(e);
    requireInvariant registeredAdapterWellFormed(e);
    requireInvariant adapterQuorumEqualsListLength(e);
    requireInvariant sessionThresholdUniform(e);
    requireInvariant listedAdapterHoldsItsIndex(e);
    requireInvariant adapterIdPointsAtItsOwnSlot(e);
    requireInvariant blockedExcludesLive(e);
    requireInvariant blockedThresholdWithinList(e);
    requireInvariant blockedAtCounterWasActive(e);
    requireInvariant blockedCounterClearsActiveSet(e);
}

// MA-VS-01: the active outbound adapter set is always the current session's, or none.
invariant activeSetSessionCurrentOrCleared(env e)
    ghostMaActiveSetSessionId16 == 0 || ghostMaActiveSetSessionId16 == ghostMaActiveSessionId16
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) { SETUP_MA(e, eFunc); } }

// MA-VS-02: an outbound adapter set without a session id is always empty.
invariant clearedActiveSetEmpty(env e)
    ghostMaActiveSetSessionId16 == 0 => ghostMaActiveListLength8 == 0
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant sessionZeroNeverConfigured(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-03: the active outbound adapters always match the active session's adapter list.
invariant activeSetMirrorsSessionList(env e)
    ghostMaActiveSetSessionId16 != 0 => (
        ghostMaActiveListLength8 == ghostMaSessionListLength8[ghostMaActiveSetSessionId16]
        && (forall mathint i. i >= 0 && i < ghostMaActiveListLength8 =>
            ghostMaActiveList[i] == ghostMaSessionList[ghostMaActiveSetSessionId16][i])
    )
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant activeSetSessionCurrentOrCleared(e);
    requireInvariant blockedAtCounterWasActive(e);
    requireInvariant blockedCounterClearsActiveSet(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-04: no adapters are ever configured for a future session id.
invariant sessionsAboveCounterEmpty(env e)
    forall uint16 s. s > ghostMaActiveSessionId16 => ghostMaSessionListLength8[s] == 0
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant blockedAboveCounterEmpty(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-05: a future session id is never blocked.
invariant blockedAboveCounterEmpty(env e)
    forall uint16 s. s > ghostMaActiveSessionId16 => ghostMaBlockedListLength8[s] == 0
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant sessionsAboveCounterEmpty(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-06: session zero never has adapters and is never blocked.
invariant sessionZeroNeverConfigured(env e)
    ghostMaSessionListLength8[0] == 0 && ghostMaBlockedListLength8[0] == 0
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) { SETUP_MA(e, eFunc); } }

// MA-VS-07: an adapter's threshold is between one and its quorum, which is within the adapter cap.
invariant registeredAdapterWellFormed(env e)
    forall uint16 s. forall address a. ghostMaAdapterId8[s][a] != 0 => (
        ghostMaAdapterThreshold8[s][a] >= 1
        && ghostMaAdapterThreshold8[s][a] <= ghostMaAdapterQuorum8[s][a]
        && ghostMaAdapterQuorum8[s][a] <= MAX_ADAPTERS_CVL()
        && ghostMaAdapterId8[s][a] <= ghostMaAdapterQuorum8[s][a]
    )
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant blockedThresholdWithinList(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-08: every registered adapter's quorum equals its session's adapter count.
invariant adapterQuorumEqualsListLength(env e)
    forall uint16 s. forall address a.
        ghostMaAdapterId8[s][a] != 0 => ghostMaAdapterQuorum8[s][a] == ghostMaSessionListLength8[s]
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant sessionsAboveCounterEmpty(e);
    requireInvariant adapterIdPointsAtItsOwnSlot(e);
    requireInvariant blockedExcludesLive(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-09: all adapters of a session share one threshold.
invariant sessionThresholdUniform(env e)
    forall uint16 s. forall address a1. forall address a2.
        (ghostMaAdapterId8[s][a1] != 0 && ghostMaAdapterId8[s][a2] != 0)
            => ghostMaAdapterThreshold8[s][a1] == ghostMaAdapterThreshold8[s][a2]
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant sessionsAboveCounterEmpty(e);
    requireInvariant adapterIdPointsAtItsOwnSlot(e);
    requireInvariant blockedExcludesLive(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-10: each adapter in a session votes in the slot matching its list position.
invariant listedAdapterHoldsItsIndex(env e)
    forall uint16 s. forall mathint i.
        (i >= 0 && i < ghostMaSessionListLength8[s])
            => ghostMaAdapterId8[s][ghostMaSessionList[s][i]] == i + 1
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant sessionsAboveCounterEmpty(e);
    requireInvariant adapterIdPointsAtItsOwnSlot(e);
    requireInvariant blockedExcludesLive(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-11: a registered adapter's id always leads back to that adapter in the session list.
invariant adapterIdPointsAtItsOwnSlot(env e)
    forall uint16 s. forall address a. ghostMaAdapterId8[s][a] != 0 => (
        ghostMaAdapterId8[s][a] <= ghostMaSessionListLength8[s]
        && ghostMaSessionList[s][ghostMaAdapterId8[s][a] - 1] == a
    )
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant sessionsAboveCounterEmpty(e);
    requireInvariant blockedExcludesLive(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-12: a blocked session never also has live adapters.
invariant blockedExcludesLive(env e)
    forall uint16 s. ghostMaBlockedListLength8[s] > 0 => ghostMaSessionListLength8[s] == 0
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant sessionsAboveCounterEmpty(e);
    requireInvariant blockedAboveCounterEmpty(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-13: a blocked session keeps a threshold between one and its adapter count.
invariant blockedThresholdWithinList(env e)
    forall uint16 s. ghostMaBlockedListLength8[s] > 0 => (
        ghostMaBlockedThreshold8[s] >= 1
        && ghostMaBlockedThreshold8[s] <= ghostMaBlockedListLength8[s]
    )
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant registeredAdapterWellFormed(e);
    requireInvariant adapterQuorumEqualsListLength(e);
    requireInvariant listedAdapterHoldsItsIndex(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-14: a blocked current session is always recorded as having been active.
invariant blockedAtCounterWasActive(env e)
    ghostMaBlockedListLength8[ghostMaActiveSessionId16] > 0
        => ghostMaBlockedWasActive[ghostMaActiveSessionId16]
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant blockedAboveCounterEmpty(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-15: while the current session is blocked, the pool has no outbound adapters.
invariant blockedCounterClearsActiveSet(env e)
    ghostMaBlockedListLength8[ghostMaActiveSessionId16] > 0 => (
        ghostMaActiveListLength8 == 0 && ghostMaActiveSetSessionId16 == 0
    )
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant activeSetSessionCurrentOrCleared(e);
    requireInvariant blockedAboveCounterEmpty(e);
    requireInvariant blockedAtCounterWasActive(e);
    SETUP_MA(e, eFunc);
} }

// MA-VS-16: a blocked session never lists the same adapter twice.
invariant blockedListDistinct(env e, uint16 cid, MultiAdapterHarness.PoolId p, uint16 sid, uint256 i, uint256 j)
    (cid == ghostMaCid16 && VALID_POOL(p)
        && i < j && j < ghostMaBlockedListLength8[sid])
        => _MultiAdapter.blockedListAt(e, cid, p, sid, i) != _MultiAdapter.blockedListAt(e, cid, p, sid, j)
filtered { f -> !EXCLUDED_FUNCTION_MA(f) } { preserved with (env eFunc) {
    requireInvariant listedAdapterHoldsItsIndex(e);
    SETUP_MA(e, eFunc);
} }
