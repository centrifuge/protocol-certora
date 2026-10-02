// Gateway. Setup: withBatch callbacks dispatched to BatchInitiator, and its pause.

// Own setup: withBatch dispatched to BatchInitiator; only the withbatch and reentrant confs compile that harness.

using BatchInitiator as _BatchInitiator;

methods {
    function _BatchInitiator.gateway() external returns (address) envfree;

    // SCOPE: BatchInitiator callbacks only, others run nothing and fail.
    unresolved external in Gateway.withBatch(bytes,uint256,address) => DISPATCH [
        BatchInitiator.lockingCallback(bytes),
        BatchInitiator.notLockingCallback(bytes),
        BatchInitiator.sendingCallback(uint16,uint16,bytes),
        BatchInitiator.sendThenPauseCallback(uint16,bytes)
    ] default NONDET;

    unresolved external in Gateway.withBatch(bytes,address) => DISPATCH [
        BatchInitiator.lockingCallback(bytes),
        BatchInitiator.notLockingCallback(bytes),
        BatchInitiator.sendingCallback(uint16,uint16,bytes),
        BatchInitiator.sendThenPauseCallback(uint16,bytes)
    ] default NONDET;

    // SCOPE: a guardian pausing mid transaction, from the callback.
    function BatchInitiator._pause() internal => gwPauseCVL();
}

function gwPauseCVL() {
    ghostGwPaused = true;
}
