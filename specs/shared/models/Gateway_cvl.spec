// Gateway model: records handle() and send() calls, for scenes not compiling it.

methods {
    function _.isBatching() external
        => ghostGwIsBatching expect bool UNRESOLVED;
    // UNSAFE: the callback is dropped, so a batch's calls go unanalysed.
    function _.withBatch(bytes callbackData, address refund) external with (env e)
        => gatewayWithBatchCVL(e, callbackData, refund) expect void UNRESOLVED;
    function _.lockCallback() external
        => gatewayLockCallbackCVL() expect void UNRESOLVED;

    // UNSAFE: what the gateway does with a message is unanalysed.
    function _.handle(uint16 centrifugeId, bytes message) external
        => gatewayHandleCVL(centrifugeId, message) expect void UNRESOLVED;

    // UNSAFE: only the fact of a send, no delivery, payment or ETH.
    function _.send(uint16 centrifugeId, bytes message, bool unpaidMode, address refund) external
        => gatewaySendCVL() expect void UNRESOLVED;
}

persistent ghost mathint ghostGwSendCount {
    init_state axiom ghostGwSendCount == 0;
    axiom ghostGwSendCount >= 0;
}

function gatewaySendCVL() {
    ghostGwSendCount = ghostGwSendCount + 1;
}

persistent ghost bool ghostGwIsBatching;

function gatewayWithBatchCVL(env e, bytes callbackData, address refund) {
}

function gatewayLockCallbackCVL() {
    require(ghostGwIsBatching, "ASSERT: a lock needs an open batch, any caller admitted");
}

persistent ghost mathint ghostGwHandleCount {
    init_state axiom ghostGwHandleCount == 0;
    axiom ghostGwHandleCount >= 0;
}
persistent ghost mathint ghostGwLastHandleCid16;
persistent ghost bytes32 ghostGwLastHandleHash;

function gatewayHandleCVL(uint16 centrifugeId, bytes message) {
    ghostGwHandleCount = ghostGwHandleCount + 1;
    ghostGwLastHandleCid16 = centrifugeId;
    ghostGwLastHandleHash = keccak256(message);
}
