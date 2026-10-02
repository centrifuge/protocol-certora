// Hub request manager model: records callee and fields of each routed request.

methods {
    // SCOPE: the manager's effects lie outside the scene.
    function _.request(uint64 poolId, bytes16 scId, uint128 assetId, bytes payload) external
        => hmHubRequestCVL(calledContract, poolId, scId, assetId, payload) expect void;
}

persistent ghost mathint ghostHmRequestCount {
    init_state axiom ghostHmRequestCount == 0;
    axiom ghostHmRequestCount >= 0;
}
persistent ghost address ghostHmRequestManager;
persistent ghost mathint ghostHmRequestPool64;
persistent ghost bytes16 ghostHmRequestScId;
persistent ghost mathint ghostHmRequestAssetId128;
persistent ghost bytes32 ghostHmRequestPayloadHash;

function hmHubRequestCVL(address manager, uint64 poolId, bytes16 scId, uint128 assetId, bytes payload) {
    ghostHmRequestCount = ghostHmRequestCount + 1;
    ghostHmRequestManager = manager;
    ghostHmRequestPool64 = poolId;
    ghostHmRequestScId = scId;
    ghostHmRequestAssetId128 = assetId;
    ghostHmRequestPayloadHash = keccak256(payload);
}
