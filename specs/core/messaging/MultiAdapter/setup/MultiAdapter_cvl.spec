// MultiAdapter. Model: session and block recorders, for scenes not compiling it.

import "../../../../shared/call_order.spec";

methods {
    function _.nextActiveSessionId(uint16 centrifugeId, uint64 poolId) external
        => maNextActiveSessionIdCVL() expect uint16 UNRESOLVED;
    // UNSAFE: NoDuplicatesAllowed is unmodelled, a duplicated set passes.
    function _.setAdapters(uint16 centrifugeId, uint64 poolId, address[] adapters, uint8 threshold, uint16 targetSessionId) external
        => maSetAdaptersStampedCVL(adapters, threshold, targetSessionId) expect void UNRESOLVED;
    function _.blockSession(uint16 centrifugeId, uint64 poolId, uint16 sessionId) external
        => maBlockSessionCVL(centrifugeId, sessionId) expect void UNRESOLVED;
}

persistent ghost uint16 ghostMaActiveSessionId16;

persistent ghost mathint ghostMaFaceBlockCount {
    axiom ghostMaFaceBlockCount >= 0;
}
persistent ghost uint16 ghostMaFaceLastBlockCentrifugeId;
persistent ghost uint16 ghostMaFaceLastBlockSessionId;

function maNextActiveSessionIdCVL() returns uint16 {
    return require_uint16(ghostMaActiveSessionId16 + 1);
}

function maSetAdaptersCVL(address[] adapters, uint8 threshold, uint16 targetSessionId) {
    require(targetSessionId == ghostMaActiveSessionId16 + 1 && adapters.length <= 8
        && (threshold > 0 || adapters.length == 0) && threshold <= adapters.length,
        "ASSERT: next session id, capped roster, valid threshold");
    ghostMaActiveSessionId16 = targetSessionId;
}

function maBlockSessionCVL(uint16 centrifugeId, uint16 sessionId) {
    bool authorized;
    bool configured;
    if (!authorized) {
        revert("NotAuthorized");
    }
    if (!configured) {
        revert("SessionNotConfigured");
    }
    ghostMaFaceBlockCount = ghostMaFaceBlockCount + 1;
    ghostMaFaceLastBlockCentrifugeId = centrifugeId;
    ghostMaFaceLastBlockSessionId = sessionId;
}

// Call-order tick of the last adapter install.
persistent ghost mathint ghostMaSetAdaptersAt;

function maSetAdaptersStampedCVL(address[] adapters, uint8 threshold, uint16 targetSessionId) {
    maSetAdaptersCVL(adapters, threshold, targetSessionId);
    ghostMaSetAdaptersAt = callOrderTickCVL();
}
