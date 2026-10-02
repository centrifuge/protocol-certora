// Cross-chain adapter model: a free quote and a free send, each recorded.

methods {
    function _.estimate(uint16 centrifugeId, bytes payload, uint256 gasLimit) external
        => adapterEstimateCVL(calledContract, centrifugeId, payload, gasLimit) expect uint256 UNRESOLVED;

    // UNSAFE: drops the adapter's effects, callbacks and the ETH moved.
    function _.send(uint16 centrifugeId, bytes payload, uint256 gasLimit, address refund) external with (env e)
        => adapterSendCVL(e, calledContract, centrifugeId, payload, gasLimit, refund) expect bytes32 UNRESOLVED;
}

persistent ghost bool ghostAdEstimateReverts;
persistent ghost address ghostAdLastEstimateAdapter;
persistent ghost uint16 ghostAdLastEstimateCid16;
persistent ghost bytes32 ghostAdLastEstimateHash;
persistent ghost uint256 ghostAdLastEstimateGasLimit256;
persistent ghost uint256 ghostAdLastQuote256;

persistent ghost bool ghostAdSendReverts;

persistent ghost mathint ghostAdSendCount {
    init_state axiom ghostAdSendCount == 0;
    axiom ghostAdSendCount >= 0;
}
persistent ghost address ghostAdLastSendAdapter;
persistent ghost uint16 ghostAdLastSendCid16;
persistent ghost bytes32 ghostAdLastSendHash;
persistent ghost uint256 ghostAdLastSendGasLimit256;
persistent ghost address ghostAdLastSendRefund;
persistent ghost uint256 ghostAdLastSendValue256;

function adapterEstimateCVL(address adapter, uint16 centrifugeId, bytes payload, uint256 gasLimit) returns uint256 {
    havoc ghostAdEstimateReverts;
    if (ghostAdEstimateReverts) {
        revert("adapter refused the quote");
    }
    ghostAdLastEstimateAdapter = adapter;
    ghostAdLastEstimateCid16 = centrifugeId;
    ghostAdLastEstimateHash = keccak256(payload);
    ghostAdLastEstimateGasLimit256 = gasLimit;
    uint256 quote;
    ghostAdLastQuote256 = quote;
    return quote;
}

function adapterSendCVL(env e, address adapter, uint16 centrifugeId, bytes payload, uint256 gasLimit, address refund) returns bytes32 {
    havoc ghostAdSendReverts;
    if (ghostAdSendReverts) {
        revert("adapter refused the send");
    }
    ghostAdSendCount = ghostAdSendCount + 1;
    ghostAdLastSendAdapter = adapter;
    ghostAdLastSendCid16 = centrifugeId;
    ghostAdLastSendHash = keccak256(payload);
    ghostAdLastSendGasLimit256 = gasLimit;
    ghostAdLastSendRefund = refund;
    ghostAdLastSendValue256 = e.msg.value;
    bytes32 adapterData;
    return adapterData;
}
