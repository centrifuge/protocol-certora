// Gateway_LinkedMessageProcessor, framing lane. Setup: the real framing, free pool, source and budget reads.

// Own setup: only messageLength real, the other readers free; with every reader real handle ran out of memory.

methods {
    function _MessageProcessor.messageLength(bytes) external returns (uint16) envfree;

    // SAFE: free reads over-approximate the real ones, so a refusal proved with them holds.
    function MessageProcessor.messagePoolId(bytes) external returns (MessageProcessor.PoolId) => NONDET;
    function MessageProcessor.messageSourceCentrifugeId(bytes) external returns (uint16) => NONDET;
    function GasService.messageProcessingGasLimit(uint16, bytes) external returns (uint128) => NONDET;

    function Gateway._safeProcess(uint16 centrifugeId, bytes memory message, bytes32 messageHash, uint128 gasLimit,
        uint128 failureGasReserve_) internal => gwForwardCVL(centrifugeId, gasLimit, failureGasReserve_);
}
