// Gateway_LinkedMessageProcessor, source lane. Setup: the real source read, free framing, pool and budget reads.

// Own setup: the source read real, a free length no shorter than the type's; every reader real ran out of memory.

methods {
    // SAFE: free reads over-approximate the real ones, so a refusal proved with them holds.
    function MessageProcessor.messageLength(bytes message) external returns (uint16) => gwFramedLengthCVL(message);
    function MessageProcessor.messagePoolId(bytes) external returns (MessageProcessor.PoolId) => NONDET;
    function GasService.messageProcessingGasLimit(uint16, bytes) external returns (uint128) => NONDET;

    function Gateway._safeProcess(uint16 centrifugeId, bytes memory message, bytes32 messageHash, uint128 gasLimit,
        uint128 failureGasReserve_) internal => gwForwardCVL(centrifugeId, gasLimit, failureGasReserve_);
}

function gwFramedLengthCVL(bytes message) returns uint16 {
    uint8 kind = _BytesSlice.toUint8Pure(message, 0);
    uint16 length;
    require(to_mathint(length) >= (kind == 3 ? 18 : (kind == 14 ? 91 : (kind == 16 ? 57 : 9))),
        "SAFE: every known message type is at least its fixed length long (MessageLib.sol:80-104,116)");
    return length;
}
