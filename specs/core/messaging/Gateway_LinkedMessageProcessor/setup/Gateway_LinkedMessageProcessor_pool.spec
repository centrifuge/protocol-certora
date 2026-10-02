// Gateway_LinkedMessageProcessor, pool lane. Setup: the real pool reads, free framing, source and budget reads.

// Own setup: only messagePoolId real, a free length of at least 9; beside the real framing reader it ran out of memory.

methods {
    function _MessageProcessor.messagePoolId(bytes) external returns (MessageProcessor.PoolId) envfree;

    // SAFE: free reads over-approximate the real ones, so a pool check proved with them holds.
    function MessageProcessor.messageLength(bytes) external returns (uint16) => gwPoolFramedLengthCVL();
    function MessageProcessor.messageSourceCentrifugeId(bytes) external returns (uint16) => NONDET;
    function GasService.messageProcessingGasLimit(uint16, bytes) external returns (uint128) => NONDET;

    function Gateway._safeProcess(uint16 centrifugeId, bytes memory message, bytes32 messageHash, uint128 gasLimit,
        uint128 failureGasReserve_) internal => gwForwardPoolCVL(centrifugeId, message, gasLimit, failureGasReserve_);
}

function gwPoolFramedLengthCVL() returns uint16 {
    uint16 length;
    require(length >= 9, "SAFE: every known message type is at least 9 bytes long (MessageLib.sol:80-104,116)");
    return length;
}

persistent ghost uint64 ghostGwBatchPool64;
persistent ghost bool ghostGwForeignPoolForwarded;

function gwForwardPoolCVL(uint16 centrifugeId, bytes message, uint128 gasLimit, uint128 failureGasReserve) {
    gwForwardCVL(centrifugeId, gasLimit, failureGasReserve);
    uint64 pool = _MessageProcessor.messagePoolId@withrevert(message);
    if (lastReverted || pool != ghostGwBatchPool64) {
        ghostGwForeignPoolForwarded = true;
    }
}
