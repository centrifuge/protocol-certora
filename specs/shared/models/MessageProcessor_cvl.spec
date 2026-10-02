// MessageProcessor. Model: the IMessageParser framing readers, for scenes not compiling it.

import "../domains/single_pool.spec";

methods {
    function _.messagePoolId(bytes message) external
        => messageProcessorMessagePoolIdCVL(message) expect uint64;

    function _.routePoolId(bytes message, bool poolConfigured) external
        => messageProcessorRoutePoolIdCVL(message, poolConfigured) expect uint64;

    function _.messageLength(bytes message) external
        => messageProcessorMessageLengthCVL(message) expect uint16;

    function _.messageSourceCentrifugeId(bytes message) external
        => messageProcessorSourceCidCVL(message) expect uint16;
}

// SCOPE: messagePoolId answers the pinned pool or pool zero.
persistent ghost mapping(bytes32 => mathint) ghostMpPoolId64 {
    axiom forall bytes32 h.
        ghostMpPoolId64[h] == ghostPoolA64 || ghostMpPoolId64[h] == 0;
}

persistent ghost mapping(bytes32 => mathint) ghostMpRouteUnconfigured64 {
    axiom forall bytes32 h.
        ghostMpRouteUnconfigured64[h] == ghostMpPoolId64[h] || ghostMpRouteUnconfigured64[h] == 0;
}

persistent ghost mapping(bytes32 => mathint) ghostMpLength16 {
    axiom forall bytes32 h. ghostMpLength16[h] >= 0 && ghostMpLength16[h] <= max_uint16;
}

persistent ghost mapping(bytes32 => mathint) ghostMpSourceCid16 {
    axiom forall bytes32 h. ghostMpSourceCid16[h] >= 0 && ghostMpSourceCid16[h] <= max_uint16;
}

function messageProcessorMessagePoolIdCVL(bytes message) returns uint64 {
    return require_uint64(ghostMpPoolId64[keccak256(message)]);
}

function messageProcessorRoutePoolIdCVL(bytes message, bool poolConfigured) returns uint64 {
    bytes32 h = keccak256(message);
    if (poolConfigured) {
        return require_uint64(ghostMpPoolId64[h]);
    }
    return require_uint64(ghostMpRouteUnconfigured64[h]);
}

function messageProcessorMessageLengthCVL(bytes message) returns uint16 {
    uint16 len = require_uint16(ghostMpLength16[keccak256(message)]);
    require(len > 0, "SAFE: MP-HL-12, no framed length is zero");
    return len;
}

function messageProcessorSourceCidCVL(bytes message) returns uint16 {
    return require_uint16(ghostMpSourceCid16[keccak256(message)]);
}
