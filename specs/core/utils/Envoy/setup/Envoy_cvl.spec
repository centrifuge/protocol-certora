// Envoy. Model: counts forwarded manager calls, for scenes not compiling it.

methods {
    // UNSAFE: forwarded call dropped, Envoy is a stateless sender anchor.
    function _.callFromHub(uint64 poolId, address target, bytes payload) external
        => envoyEntryCVL(301) expect void UNRESOLVED;
    function _.callFromSpoke(uint64 poolId, address target, bytes payload, uint16 centrifugeId,
        bytes32 sender) external
        => envoyCallFromSpokeCVL(centrifugeId) expect void UNRESOLVED;
}

persistent ghost mathint ghostEnCallCount {
    init_state axiom ghostEnCallCount == 0;
    axiom ghostEnCallCount >= 0;
}
persistent ghost mathint ghostEnLastSourceCid16;
// Tags the entry last reached, 3xx of the handler-face scheme in SpokeHandler.
persistent ghost mathint ghostEnLastEntry;

function envoyRecordCVL() {
    ghostEnCallCount = ghostEnCallCount + 1;
}

function envoyEntryCVL(mathint tag) {
    envoyRecordCVL();
    ghostEnLastEntry = tag;
}

function envoyCallFromSpokeCVL(uint16 centrifugeId) {
    envoyEntryCVL(302);
    ghostEnLastSourceCid16 = centrifugeId;
}
