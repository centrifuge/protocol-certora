// MultiAdapter, unpinned lane. Setup: pool, network and session free, a recording router.

// Own setup: pool, network and session free; the base setup pins all three.

import "../../../../shared/env.spec";
import "../../../../shared/models/Gateway_cvl.spec";

using MultiAdapterHarness as _MultiAdapter;
using MultiAdapterPayloadHarness as _MaPayload;

methods {
    // SAFE: both readers are pure, a free answer stands for any router.
    function _.messagePoolId(bytes message) external
        => maRtMessagePoolIdCVL(calledContract, message) expect uint64;
    function _.routePoolId(bytes message, bool poolConfigured) external
        => maRtRoutePoolIdCVL(calledContract, message, poolConfigured) expect uint64;
}

persistent ghost uint64 ghostMaRtMessagePool64;
persistent ghost bytes32 ghostMaRtMessagePoolArgHash;
persistent ghost address ghostMaRtMessagePoolCallee;
persistent ghost uint64 ghostMaRtRoutedPool64;
persistent ghost bool ghostMaRtConfiguredArg;
persistent ghost bytes32 ghostMaRtRouteArgHash;
persistent ghost address ghostMaRtRouteCallee;

function maRtMessagePoolIdCVL(address callee, bytes message) returns uint64 {
    uint64 pool;
    ghostMaRtMessagePool64 = pool;
    ghostMaRtMessagePoolArgHash = keccak256(message);
    ghostMaRtMessagePoolCallee = callee;
    return pool;
}

function maRtRoutePoolIdCVL(address callee, bytes message, bool poolConfigured) returns uint64 {
    uint64 pool;
    ghostMaRtRoutedPool64 = pool;
    ghostMaRtRouteCallee = callee;
    ghostMaRtConfiguredArg = poolConfigured;
    ghostMaRtRouteArgHash = keccak256(message);
    return pool;
}

// The resolve window: loads before the gateway hears a forward.
persistent ghost mathint ghostMaRtForwardMark;
persistent ghost bool ghostMaRtOffRouted;
persistent ghost mathint ghostMaRtLoadedId8;
persistent ghost mathint ghostMaRtLoadedQuorum8;
persistent ghost mathint ghostMaRtLoadedThreshold8;
persistent ghost bool ghostMaRtManagerBit;
persistent ghost address ghostMaRtManagerAccount;

hook Sload uint8 val _MultiAdapter._adapterDetails[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][KEY address adapter].id {
    bool inWindow = ghostGwHandleCount == ghostMaRtForwardMark;
    ghostMaRtOffRouted = inWindow ? ghostMaRtOffRouted || p != ghostMaRtRoutedPool64 : ghostMaRtOffRouted;
    ghostMaRtLoadedId8 = inWindow ? val : ghostMaRtLoadedId8;
}

hook Sload uint8 val _MultiAdapter._adapterDetails[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][KEY address adapter].quorum {
    ghostMaRtLoadedQuorum8 = ghostGwHandleCount == ghostMaRtForwardMark ? val : ghostMaRtLoadedQuorum8;
}

hook Sload uint8 val _MultiAdapter._adapterDetails[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][KEY address adapter].threshold {
    ghostMaRtLoadedThreshold8 = ghostGwHandleCount == ghostMaRtForwardMark ? val : ghostMaRtLoadedThreshold8;
}

hook Sload bool val _MultiAdapter.manager[KEY MultiAdapter.PoolId p][KEY address a] {
    bool inWindow = ghostGwHandleCount == ghostMaRtForwardMark;
    ghostMaRtOffRouted = inWindow ? ghostMaRtOffRouted || p != ghostMaRtRoutedPool64 : ghostMaRtOffRouted;
    ghostMaRtManagerBit = inWindow ? val : ghostMaRtManagerBit;
    ghostMaRtManagerAccount = inWindow ? a : ghostMaRtManagerAccount;
}

// SAFE: POSITIVE_LANES_MA of the base setup, which this lane does not import.
definition POSITIVE_LANES_RT_MA(mathint l0, mathint l1, mathint l2, mathint l3, mathint l4, mathint l5,
    mathint l6, mathint l7, mathint q) returns mathint =
    (q > 0 && l0 > 0 ? 1 : 0) + (q > 1 && l1 > 0 ? 1 : 0) + (q > 2 && l2 > 0 ? 1 : 0)
    + (q > 3 && l3 > 0 ? 1 : 0) + (q > 4 && l4 > 0 ? 1 : 0) + (q > 5 && l5 > 0 ? 1 : 0)
    + (q > 6 && l6 > 0 ? 1 : 0) + (q > 7 && l7 > 0 ? 1 : 0);

function setupMultiAdapterUnpinned(env e) {
    setupEnv(e);
    require(_MultiAdapter.gateway != 0, "TRUSTED: gateway wired at deploy, never cleared");
    require(_MultiAdapter.parser != 0, "TRUSTED: parser wired at deploy, never cleared");
    require(ghostMaRtForwardMark == ghostGwHandleCount && !ghostMaRtOffRouted && ghostMaRtLoadedId8 == 0
        && !ghostMaRtManagerBit,
        "SAFE: the router recorders start clean at this call");
}
