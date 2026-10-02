import "MultiAdapter_valid_state.spec";

// MA-AC-01: only an admin can grant or revoke admin rights.
rule acMaOnlyWardMovesTheWardSet(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    mathint userWardBefore = _MultiAdapter.wards[user];

    f(e, args);

    mathint userWardAfter = _MultiAdapter.wards[user];

    assert(userWardAfter != userWardBefore => senderWardBefore == 1, "a non-ward caller never changes who is a ward");
}

// MA-AC-02: only an admin can appoint or remove a pool's adapter manager.
rule acMaOnlyWardModifiesManagerRights(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool managesBefore = ghostMaManager[who];

    f(e, args);

    bool managesAfter = ghostMaManager[who];

    assert(managesAfter != managesBefore => senderWardBefore == 1,
        "only a ward can grant or revoke a pool's manager rights");
}

// MA-AC-03: only an admin can change the gateway that receives confirmed messages.
rule acMaOnlyWardRepointsTheGateway(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    address gatewayBefore = _MultiAdapter.gateway;

    f(e, args);

    address gatewayAfter = _MultiAdapter.gateway;

    assert(gatewayAfter != gatewayBefore => senderWardBefore == 1, "only a ward can repoint the gateway");
}

// MA-AC-04: only an admin can replace the reader that determines a message's pool.
rule acMaOnlyWardRepointsTheParser(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    address parserBefore = _MultiAdapter.parser;

    f(e, args);

    address parserAfter = _MultiAdapter.parser;

    assert(parserAfter != parserBefore => senderWardBefore == 1, "only a ward can repoint the parser");
}

// MA-AC-05: only an admin can send outbound messages through the adapters.
rule acMaOnlyWardFansOutASend(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    mathint dispatchCountBefore = ghostMaFaceSendCount;

    f(e, args);

    mathint dispatchCountAfter = ghostMaFaceSendCount;

    assert(dispatchCountAfter != dispatchCountBefore => senderWardBefore == 1,
        "a non-ward caller never triggers an adapter dispatch");
}

// MA-AC-06: only an admin or the pool's adapter manager can start a new adapter session.
rule acMaOnlyWardOrManagerAdvancesTheSession(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool senderManagesBefore = ghostMaManager[e.msg.sender];
    mathint sessionBefore = ghostMaActiveSessionId16;

    f(e, args);

    mathint sessionAfter = ghostMaActiveSessionId16;

    assert(sessionAfter != sessionBefore => senderWardBefore == 1 || senderManagesBefore,
        "only a ward or the pool's manager can move the session id");
}

// MA-AC-07: only an admin or the pool's adapter manager can change the outbound adapter set.
rule acMaOnlyWardOrManagerMovesTheLiveRoute(env e, method f, calldataarg args, uint256 slot)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool senderManagesBefore = ghostMaManager[e.msg.sender];
    mathint routeSessionBefore = ghostMaActiveSetSessionId16;
    mathint routeLengthBefore = ghostMaActiveListLength8;
    address routeSlotBefore = ghostMaActiveList[slot];

    f(e, args);

    mathint routeSessionAfter = ghostMaActiveSetSessionId16;
    mathint routeLengthAfter = ghostMaActiveListLength8;
    address routeSlotAfter = ghostMaActiveList[slot];

    assert(routeSessionAfter != routeSessionBefore
        || routeLengthAfter != routeLengthBefore
        || routeSlotAfter != routeSlotBefore
        => senderWardBefore == 1 || senderManagesBefore,
        "only a ward or the pool's manager can change the live roster");
}

// MA-AC-08: only an admin or the pool's adapter manager can change a session's adapter list.
rule acMaOnlyWardOrManagerMovesASessionRoster(env e, method f, calldataarg args, uint16 sid, uint256 slot)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    uint16 s = sid;
    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool senderManagesBefore = ghostMaManager[e.msg.sender];
    mathint rosterLengthBefore = ghostMaSessionListLength8[s];
    address rosterSlotBefore = ghostMaSessionList[s][slot];

    f(e, args);

    mathint rosterLengthAfter = ghostMaSessionListLength8[s];
    address rosterSlotAfter = ghostMaSessionList[s][slot];

    assert(rosterLengthAfter != rosterLengthBefore
        || rosterSlotAfter != rosterSlotBefore
        => senderWardBefore == 1 || senderManagesBefore,
        "a session roster change needs a ward or the pool's manager");
}

// MA-AC-09: only an admin or the pool's adapter manager can change an adapter's registration.
rule acMaOnlyWardOrManagerMovesAnAdapterRegistration(env e, method f, calldataarg args, uint16 sid,
    address adapter)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    uint16 s = sid;
    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool senderManagesBefore = ghostMaManager[e.msg.sender];
    mathint idBefore = ghostMaAdapterId8[s][adapter];
    mathint quorumBefore = ghostMaAdapterQuorum8[s][adapter];
    mathint thresholdBefore = ghostMaAdapterThreshold8[s][adapter];

    f(e, args);

    mathint idAfter = ghostMaAdapterId8[s][adapter];
    mathint quorumAfter = ghostMaAdapterQuorum8[s][adapter];
    mathint thresholdAfter = ghostMaAdapterThreshold8[s][adapter];

    assert(idAfter != idBefore
        || quorumAfter != quorumBefore
        || thresholdAfter != thresholdBefore
        => senderWardBefore == 1 || senderManagesBefore,
        "an adapter registration change needs a ward or the pool's manager");
}

// MA-AC-10: only an admin or the pool's adapter manager can block or unblock a session.
rule acMaOnlyWardOrManagerMovesTheBlockedStash(env e, method f, calldataarg args, uint16 sid)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    uint16 s = sid;
    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    bool senderManagesBefore = ghostMaManager[e.msg.sender];
    mathint stashLengthBefore = ghostMaBlockedListLength8[s];
    mathint stashThresholdBefore = ghostMaBlockedThreshold8[s];
    bool stashWasActiveBefore = ghostMaBlockedWasActive[s];

    f(e, args);

    mathint stashLengthAfter = ghostMaBlockedListLength8[s];
    mathint stashThresholdAfter = ghostMaBlockedThreshold8[s];
    bool stashWasActiveAfter = ghostMaBlockedWasActive[s];

    assert(stashLengthAfter != stashLengthBefore
        || stashThresholdAfter != stashThresholdBefore
        || stashWasActiveAfter != stashWasActiveBefore
        => senderWardBefore == 1 || senderManagesBefore,
        "a session's block state moves only for a ward or the pool's manager");
}

// MA-AC-11: only a registered adapter or the pool's adapter manager can change the votes on a message.
rule acMaOnlyAdapterOrManagerMovesAVoteTally(env e, method f, calldataarg args, uint16 cid, bytes32 voteKey)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    bool senderUnregisteredBefore = forall uint16 s. ghostMaAdapterId8[s][e.msg.sender] == 0;
    bool senderManagesBefore = ghostMaManager[e.msg.sender];
    mathint lane0Before = _MultiAdapter.voteAt(e, cid, voteKey, 0);
    mathint lane1Before = _MultiAdapter.voteAt(e, cid, voteKey, 1);
    mathint lane2Before = _MultiAdapter.voteAt(e, cid, voteKey, 2);
    mathint lane3Before = _MultiAdapter.voteAt(e, cid, voteKey, 3);
    mathint lane4Before = _MultiAdapter.voteAt(e, cid, voteKey, 4);
    mathint lane5Before = _MultiAdapter.voteAt(e, cid, voteKey, 5);
    mathint lane6Before = _MultiAdapter.voteAt(e, cid, voteKey, 6);
    mathint lane7Before = _MultiAdapter.voteAt(e, cid, voteKey, 7);

    f(e, args);

    mathint lane0After = _MultiAdapter.voteAt(e, cid, voteKey, 0);
    mathint lane1After = _MultiAdapter.voteAt(e, cid, voteKey, 1);
    mathint lane2After = _MultiAdapter.voteAt(e, cid, voteKey, 2);
    mathint lane3After = _MultiAdapter.voteAt(e, cid, voteKey, 3);
    mathint lane4After = _MultiAdapter.voteAt(e, cid, voteKey, 4);
    mathint lane5After = _MultiAdapter.voteAt(e, cid, voteKey, 5);
    mathint lane6After = _MultiAdapter.voteAt(e, cid, voteKey, 6);
    mathint lane7After = _MultiAdapter.voteAt(e, cid, voteKey, 7);

    assert(senderUnregisteredBefore && !senderManagesBefore => (
        lane0After == lane0Before && lane1After == lane1Before
        && lane2After == lane2Before && lane3After == lane3Before
        && lane4After == lane4Before && lane5After == lane5Before
        && lane6After == lane6Before && lane7After == lane7Before),
        "a caller neither adapter nor pool manager changes no vote count");
}

// MA-AC-12: only a registered adapter or the pool's adapter manager can pass a message to the gateway.
rule acMaOnlyAdapterOrManagerReachesTheGateway(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    bool senderUnregisteredBefore = forall uint16 s. ghostMaAdapterId8[s][e.msg.sender] == 0;
    bool senderManagesBefore = ghostMaManager[e.msg.sender];
    mathint forwardCountBefore = ghostGwHandleCount;

    f(e, args);

    mathint forwardCountAfter = ghostGwHandleCount;

    assert(senderUnregisteredBefore && !senderManagesBefore
        => forwardCountAfter == forwardCountBefore,
        "a caller neither adapter nor pool manager hands the gateway nothing");
}

// MA-AC-13: only an admin can replace the gas model the adapters read.
rule acMaOnlyWardRepointsTheMessageGas(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MA(f) } {

    setupMultiAdapter(e);

    mathint senderWardBefore = _MultiAdapter.wards[e.msg.sender];
    address messageGasBefore = _MultiAdapter.messageGas;

    f(e, args);

    address messageGasAfter = _MultiAdapter.messageGas;

    assert(messageGasAfter != messageGasBefore => senderWardBefore == 1, "only a ward can repoint the gas model");
}
