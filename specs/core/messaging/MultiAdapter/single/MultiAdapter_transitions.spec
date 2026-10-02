import "MultiAdapter_valid_state.spec";

// --- variable_transitions ---

// MA-VT-01: a pool's session counter never decreases.
rule vtMaSessionIdNeverRegresses(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint sessionIdBefore = ghostMaActiveSessionId16;

    f(e, args);

    mathint sessionIdAfter = ghostMaActiveSessionId16;

    assert(sessionIdAfter >= sessionIdBefore, "the session id never decreases");
}

// MA-VT-02: a single call advances a pool's session counter by at most one.
rule vtMaSessionIdAdvancesByOneAtMost(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint sessionIdBefore = ghostMaActiveSessionId16;

    f(e, args);

    mathint sessionIdAfter = ghostMaActiveSessionId16;

    assert(sessionIdAfter <= sessionIdBefore + 1, "one call raises the session id by at most one");
}

// MA-VT-03: changing one session's adapter list leaves other sessions' lists unchanged.
rule vtMaRosterMoveSparesOtherSessions(env e, method f, calldataarg args, uint16 movedSid, uint16 otherSid,
    uint256 slot)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint movedLengthBefore = ghostMaSessionListLength8[movedSid];
    mathint otherLengthBefore = ghostMaSessionListLength8[otherSid];
    address otherSlotBefore = ghostMaSessionList[otherSid][slot];

    f(e, args);

    mathint movedLengthAfter = ghostMaSessionListLength8[movedSid];
    mathint otherLengthAfter = ghostMaSessionListLength8[otherSid];
    address otherSlotAfter = ghostMaSessionList[otherSid][slot];

    assert(movedSid != otherSid && movedLengthAfter != movedLengthBefore
        => otherLengthAfter == otherLengthBefore && otherSlotAfter == otherSlotBefore,
        "resizing one session's roster leaves every other session's untouched");
}

// MA-VT-04: a pool's session id changes only when a new adapter set is installed.
rule vtMaSessionIdMovesOnlyByRotation(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapterValidState(e);

    mathint sessionBefore = ghostMaActiveSessionId16;

    f(e, args);

    mathint sessionAfter = ghostMaActiveSessionId16;

    assert(sessionAfter != sessionBefore => ROTATION_FUNCTION_MA(f), "only a rotation moves the session id");
}

// --- state_transitions ---

// MA-ST-01: a session id change immediately makes outbound messages use that session.
rule stMaSessionAdvanceRestampsTheRoute(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapterValidState(e);

    mathint sessionBefore = ghostMaActiveSessionId16;

    f(e, args);

    assert(ghostMaActiveSessionId16 != sessionBefore
        => ghostMaActiveSetSessionId16 == ghostMaActiveSessionId16,
        "a session change stamps the live roster with the new session");
}

// MA-ST-02: blocking a session saves its adapters, threshold and whether it was active.
rule stMaBlockStashesTheLiveRosterWhole(env e, method f, calldataarg args, uint16 cid,
    MultiAdapterHarness.PoolId p, uint16 sid, uint256 i)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapterValidState(e);
    require(cid == ghostMaCid16, "SCOPE: the modelled remote network");
    require(VALID_POOL(p), "SCOPE: the modelled pool");

    uint16 s = sid;
    mathint sessionBefore = ghostMaActiveSessionId16;
    mathint liveLengthBefore = ghostMaSessionListLength8[s];
    require(i < liveLengthBefore, "SCOPE: a position within the session's roster");
    address liveSlotBefore = ghostMaSessionList[s][i];
    mathint liveThresholdBefore = ghostMaAdapterThreshold8[s][ghostMaSessionList[s][0]];
    mathint stashLengthBefore = ghostMaBlockedListLength8[s];

    f(e, args);

    assert(ghostMaBlockedListLength8[s] > stashLengthBefore
        => ghostMaBlockedListLength8[s] == liveLengthBefore
            && _MultiAdapter.blockedListAt(e, cid, p, sid, i) == liveSlotBefore
            && ghostMaBlockedThreshold8[s] == liveThresholdBefore,
        "blocking stashes the session's roster and threshold unchanged");
    assert(ghostMaBlockedListLength8[s] > stashLengthBefore
        => (ghostMaBlockedWasActive[s] <=> s == sessionBefore),
        "blocking records whether the session was the current one");
}

// MA-ST-03: blocking an old session leaves the active outbound adapters unchanged.
rule stMaBlockingASupersededSessionKeepsTheRoute(env e, method f, calldataarg args, uint16 s)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapterValidState(e);

    mathint sessionBefore = ghostMaActiveSessionId16;
    mathint stashLengthBefore = ghostMaBlockedListLength8[s];
    mathint routeSessionBefore = ghostMaActiveSetSessionId16;
    mathint routeLengthBefore = ghostMaActiveListLength8;

    f(e, args);

    assert(ghostMaBlockedListLength8[s] > stashLengthBefore && s != sessionBefore
        => ghostMaActiveSetSessionId16 == routeSessionBefore
            && ghostMaActiveListLength8 == routeLengthBefore,
        "blocking a non-current session keeps the live session and roster size");
}

// MA-ST-04: unblocking a session restores exactly the adapters and threshold it had.
rule stMaUnblockRestoresExactlyWhatWasStashed(env e, method f, calldataarg args, uint16 cid,
    MultiAdapterHarness.PoolId p, uint16 sid, uint256 i)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapterValidState(e);
    require(cid == ghostMaCid16, "SCOPE: the modelled remote network");
    require(VALID_POOL(p), "SCOPE: the modelled pool");
    require(i < MAX_ADAPTERS_CVL(), "SAFE: no roster has a position past the eighth");

    uint16 s = sid;
    mathint stashLengthBefore = ghostMaBlockedListLength8[s];
    address stashSlotBefore = _MultiAdapter.blockedListAt(e, cid, p, sid, i);
    mathint stashThresholdBefore = ghostMaBlockedThreshold8[s];

    f(e, args);

    bool restored = stashLengthBefore > 0 && ghostMaBlockedListLength8[s] == 0;

    assert(restored
        => ghostMaSessionListLength8[s] == stashLengthBefore
            && ghostMaSessionList[s][i] == stashSlotBefore,
        "unblocking restores exactly the stashed roster");
    assert(restored && i < stashLengthBefore
        => ghostMaAdapterThreshold8[s][stashSlotBefore] == stashThresholdBefore,
        "every restored adapter gets back the stashed threshold");
}

// MA-ST-05: an unblocked session resumes sending with its stashed adapters only if still active.
rule stMaUnblockReopensTheRouteOnlyForTheSessionInService(env e, method f, calldataarg args, uint16 cid,
    MultiAdapterHarness.PoolId p, uint16 s, uint256 i)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapterValidState(e);
    require(cid == ghostMaCid16, "SCOPE: the modelled remote network");
    require(VALID_POOL(p), "SCOPE: the modelled pool");
    require(i < MAX_ADAPTERS_CVL(), "SAFE: no roster has a position past the eighth");

    mathint sessionBefore = ghostMaActiveSessionId16;
    mathint stashLengthBefore = ghostMaBlockedListLength8[s];
    address stashSlotBefore = _MultiAdapter.blockedListAt(e, cid, p, s, i);
    bool stashWasActiveBefore = ghostMaBlockedWasActive[s];
    mathint routeSessionBefore = ghostMaActiveSetSessionId16;
    mathint routeLengthBefore = ghostMaActiveListLength8;

    f(e, args);

    bool restored = stashLengthBefore > 0 && ghostMaBlockedListLength8[s] == 0;

    assert(restored && stashWasActiveBefore && s == sessionBefore
        => ghostMaActiveSetSessionId16 == s && ghostMaActiveListLength8 == stashLengthBefore,
        "unblocking a once-live, still-current session makes it live again");
    assert(restored && stashWasActiveBefore && s == sessionBefore && i < stashLengthBefore
        => ghostMaActiveList[i] == stashSlotBefore,
        "every stashed adapter is back on the route");
    assert(restored && !(stashWasActiveBefore && s == sessionBefore)
        => ghostMaActiveSetSessionId16 == routeSessionBefore
            && ghostMaActiveListLength8 == routeLengthBefore,
        "unblocking any other session keeps the live session and roster size");
}

// MA-ST-06: a configuration update sets only the named dependency, to the given address.
rule stMaFileWritesExactlyTheDependencyItsKeyNames(env e, bytes32 what, address instance) {

    setupMultiAdapterValidState(e);

    address gatewayBefore = _MultiAdapter.gateway;
    address parserBefore = _MultiAdapter.parser;
    address messageGasBefore = _MultiAdapter.messageGas;

    _MultiAdapter.file(e, what, instance);

    address gatewayAfter = _MultiAdapter.gateway;
    address parserAfter = _MultiAdapter.parser;
    address messageGasAfter = _MultiAdapter.messageGas;

    assert(gatewayAfter == (what == FILE_GATEWAY_MA_CVL() ? instance : gatewayBefore)
        && parserAfter == (what == FILE_PARSER_MA_CVL() ? instance : parserBefore)
        && messageGasAfter == (what == FILE_MESSAGE_GAS_MA_CVL() ? instance : messageGasBefore),
        "an update changes only the named dependency, to the given address");
}
