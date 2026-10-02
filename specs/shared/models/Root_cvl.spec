// Root. Model: scheduleRely and cancelRely, for scenes not compiling it.

methods {
    // UNSAFE: drops the schedule and every refusal of both Root calls.
    function _.scheduleRely(address target) external
        => scheduleAuthEntryCVL(401) expect void UNRESOLVED;
    function _.cancelRely(address target) external
        => scheduleAuthEntryCVL(402) expect void UNRESOLVED;
}

persistent ghost mathint ghostSaCallCount {
    init_state axiom ghostSaCallCount == 0;
    axiom ghostSaCallCount >= 0;
}
// Tags the entry last reached, 4xx of the handler-face scheme in SpokeHandler.
persistent ghost mathint ghostSaLastEntry;

function scheduleAuthRecordCVL() {
    ghostSaCallCount = ghostSaCallCount + 1;
}

function scheduleAuthEntryCVL(mathint tag) {
    scheduleAuthRecordCVL();
    ghostSaLastEntry = tag;
}
