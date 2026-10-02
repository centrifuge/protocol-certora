// Gateway. Setup: processor framing and gas model limits, free per message hash.

methods {
    function _.messagePoolId(bytes message) external
        => gwMessagePoolIdCVL(calledContract, message) expect uint64 UNRESOLVED;
    function _.messageLength(bytes message) external
        => gwMessageLengthCVL(calledContract, message) expect uint16 UNRESOLVED;
    function _.messageSourceCentrifugeId(bytes message) external
        => gwSourceCidCVL(calledContract, message) expect uint16 UNRESOLVED;
    function _.messageProcessingGasLimit(uint16 centrifugeId, bytes message) external
        => gwProcessingGasCVL(calledContract, centrifugeId, message) expect uint128 UNRESOLVED;
    function _.messageOverallGasLimit(uint16 centrifugeId, bytes message) external
        => gwOverallGasCVL(calledContract, centrifugeId, message) expect uint128 UNRESOLVED;
    function _.maxBatchGasLimit(uint16 centrifugeId) external
        => gwMaxBatchGasCVL(calledContract, centrifugeId) expect uint128 UNRESOLVED;
    function _.messageFailureGasReserve() external
        => gwFailureReserveCVL(calledContract) expect uint128 UNRESOLVED;
}

persistent ghost mapping(bytes32 => uint64) ghostGwPoolId64;
persistent ghost mapping(bytes32 => uint16) ghostGwLength16;
persistent ghost mapping(bytes32 => uint16) ghostGwSourceCid16;
persistent ghost mapping(uint16 => mapping(bytes32 => uint128)) ghostGwProcessingGas128;
persistent ghost mapping(uint16 => mapping(bytes32 => uint128)) ghostGwOverallGas128;
persistent ghost mapping(address => mapping(uint16 => mapping(bytes32 => uint128))) ghostGwOverallGasOf128;
persistent ghost mapping(uint16 => uint128) ghostGwMaxBatchGas128;
persistent ghost uint128 ghostGwFailureReserve128;

persistent ghost uint64 ghostGwPoolAsked64;
persistent ghost bool ghostGwLengthOverran;
persistent ghost uint16 ghostGwInboundCid16;
persistent ghost bool ghostGwForeignSourceSeen;
persistent ghost uint128 ghostGwLastProcessingGas128;
persistent ghost bytes32 ghostGwLastProcessedHash;
persistent ghost bool ghostGwBudgetBelowReserve;
persistent ghost bool ghostGwSrcArmed;
persistent ghost bytes32 ghostGwSrcLastHash;
persistent ghost bool ghostGwSrcPairBroken;
persistent ghost address ghostGwFramer;
persistent ghost address ghostGwGasModel;
persistent ghost bool ghostGwFramingStray;
persistent ghost bool ghostGwGasStray;
persistent ghost uint16 ghostGwPricingCidExpected16;
persistent ghost bool ghostGwPricedForeign;

function gwNoteFramer(address reader) {
    if (reader != ghostGwFramer) {
        ghostGwFramingStray = true;
    }
}

function gwNoteGasModel(address reader) {
    if (reader != ghostGwGasModel) {
        ghostGwGasStray = true;
    }
}

// TRUSTED: no pool read refuses, handle already read every message.
function gwMessagePoolIdCVL(address reader, bytes message) returns uint64 {
    gwNoteFramer(reader);
    uint64 poolId = ghostGwPoolId64[keccak256(message)];
    ghostGwPoolAsked64 = poolId;
    return poolId;
}

function gwMessageLengthCVL(address reader, bytes message) returns uint16 {
    gwNoteFramer(reader);
    uint16 len = ghostGwLength16[keccak256(message)];
    // SAFE: no known message has zero length, so zero stands for the processor's rejection.
    if (len == 0) {
        revert("UnknownMessageType");
    }
    if (len > message.length) {
        ghostGwLengthOverran = true;
    }
    return len;
}

function gwSourceCidCVL(address reader, bytes message) returns uint16 {
    gwNoteFramer(reader);
    bytes32 h = keccak256(message);
    uint16 source = ghostGwSourceCid16[h];
    if (source != 0 && source != ghostGwInboundCid16) {
        ghostGwForeignSourceSeen = true;
    }
    ghostGwSrcArmed = true;
    ghostGwSrcLastHash = h;
    return source;
}

function gwProcessingGasCVL(address reader, uint16 centrifugeId, bytes message) returns uint128 {
    gwNoteGasModel(reader);
    if (centrifugeId != ghostGwPricingCidExpected16) {
        ghostGwPricedForeign = true;
    }
    bytes32 h = keccak256(message);
    if (!ghostGwSrcArmed || h != ghostGwSrcLastHash) {
        ghostGwSrcPairBroken = true;
    }
    uint128 gasLimit = ghostGwProcessingGas128[centrifugeId][h];
    ghostGwLastProcessingGas128 = gasLimit;
    ghostGwLastProcessedHash = h;
    if (gasLimit < ghostGwFailureReserve128) {
        ghostGwBudgetBelowReserve = true;
    }
    return gasLimit;
}

function gwOverallGasCVL(address model, uint16 centrifugeId, bytes message) returns uint128 {
    gwNoteGasModel(model);
    bytes32 h = keccak256(message);
    uint128 gasLimit = ghostGwOverallGasOf128[model][centrifugeId][h];
    ghostGwOverallGas128[centrifugeId][h] = gasLimit;
    return gasLimit;
}

function gwMaxBatchGasCVL(address reader, uint16 centrifugeId) returns uint128 {
    gwNoteGasModel(reader);
    return ghostGwMaxBatchGas128[centrifugeId];
}

function gwFailureReserveCVL(address reader) returns uint128 {
    gwNoteGasModel(reader);
    return ghostGwFailureReserve128;
}
