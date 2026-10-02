// Spoke request manager model: records callee and fields of each callback.

methods {
    // SCOPE: the manager's effects lie outside the scene.
    function _.callback(uint64 poolId, bytes16 scId, uint128 assetId, bytes payload) external
        => hmSpokeCallbackCVL(calledContract, poolId, scId, assetId, payload) expect void;
}

persistent ghost mathint ghostHmCallbackCount {
    init_state axiom ghostHmCallbackCount == 0;
    axiom ghostHmCallbackCount >= 0;
}
persistent ghost address ghostHmCallbackManager;
persistent ghost mathint ghostHmCallbackPool64;
persistent ghost bytes16 ghostHmCallbackScId;
persistent ghost mathint ghostHmCallbackAssetId128;
persistent ghost bytes32 ghostHmCallbackPayloadHash;

function hmSpokeCallbackCVL(address manager, uint64 poolId, bytes16 scId, uint128 assetId, bytes payload) {
    ghostHmCallbackCount = ghostHmCallbackCount + 1;
    ghostHmCallbackManager = manager;
    ghostHmCallbackPool64 = poolId;
    ghostHmCallbackScId = scId;
    ghostHmCallbackAssetId128 = assetId;
    ghostHmCallbackPayloadHash = keccak256(payload);
}
