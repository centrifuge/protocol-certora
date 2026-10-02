import "setup/Gateway_reentrant.spec";

// --- reachability ---

// GW-RC-09: a repay can retire a debt from inside a batch send, re-entered by the adapter being paid.
rule rcGwRepayRunsInsideTheFlush(env eW, env eA, env eB, uint16 c, bytes m, uint16 c2, bytes b2) {

    setupEnv(eW);
    setupEnv(eA);
    setupEnv(eB);
    require(!GA_IS_BATCHING() && !GA_IS_SENDING_BATCH() && GA_BATCHER() == 0 && ghostGwLocCount == 0,
        "SCOPE: a fresh transaction, no batch open");

    bytes32 h2 = keccak256(b2);
    require(_Gateway.underpaid[c2][h2].counter == 0, "SCOPE: the batch has no debt on record yet");

    _Gateway.send(eW, c2, b2, true, _RefundSink);

    bool booked = _Gateway.underpaid[c2][h2].counter == 1;

    _ReentrantAdapter.arm(eA, c2, b2, _RefundSink);
    _BatchInitiator.runSending(eB, c, c, m, 0, _RefundSink);

    satisfy(booked && _Gateway.underpaid[c2][h2].counter == 0 && ghostGwLastPauseReadMidFlush,
        "the booked debt is repaid and cleared during the flush");
}
