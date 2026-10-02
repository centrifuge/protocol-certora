// Adapter entrypoint model: records each refusable handle() call.

methods {
    // UNSAFE: drops what handle() does, adapter re-entry included.
    function _.handle(uint16 centrifugeId, bytes message) external
        => messageHandlerHandleCVL(centrifugeId, message) expect void UNRESOLVED;
}

persistent ghost bool ghostMhHandleReverts;

persistent ghost mathint ghostGwHandleCount {
    init_state axiom ghostGwHandleCount == 0;
    axiom ghostGwHandleCount >= 0;
}
persistent ghost mathint ghostGwLastHandleCid16;
persistent ghost bytes32 ghostGwLastHandleHash;

function messageHandlerHandleCVL(uint16 centrifugeId, bytes message) {
    havoc ghostMhHandleReverts;
    if (ghostMhHandleReverts) {
        revert("entrypoint refused the message");
    }
    ghostGwHandleCount = ghostGwHandleCount + 1;
    ghostGwLastHandleCid16 = centrifugeId;
    ghostGwLastHandleHash = keccak256(message);
}
