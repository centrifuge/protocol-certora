// Gateway_LinkedMessageProcessor, witness lane. Setup: every message reader real.

// Own setup: every reader real for the witnesses; the assert lanes free all but one, which would widen a satisfy.

methods {
    function _MessageProcessor.messageLength(bytes) external returns (uint16) envfree;

    function Gateway._safeProcess(uint16 centrifugeId, bytes memory message, bytes32 messageHash, uint128 gasLimit,
        uint128 failureGasReserve_) internal => gwForwardCVL(centrifugeId, gasLimit, failureGasReserve_);
}
