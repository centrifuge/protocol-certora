// HubHandler. Model: records that a call arrived, for scenes not compiling it.

methods {
    // UNSAFE: effects dropped, and every refusal except a request's.
    function _.initiateTransferShares(uint16 originCentrifugeId, uint16 targetCentrifugeId, uint64 poolId,
        bytes16 scId, bytes32 sender, bytes32 receiver, uint128 amount, uint128 extraGasLimit,
        address refund) external with (env e)
        => hubHandlerInitiateTransferSharesCVL(e, calledContract, originCentrifugeId, refund) expect void UNRESOLVED;
    function _.updateAssets(uint16 centrifugeId, uint64 poolId, bytes16 scId, uint128 assetId,
        uint128 amount, bool isIncrease, bool isSnapshot, uint64 nonce) external with (env e)
        => hubHandlerUpdateAssetsCVL(e, calledContract, centrifugeId, poolId, scId, assetId, amount, isIncrease,
            isSnapshot, nonce) expect void UNRESOLVED;
    function _.updateShares(uint16 centrifugeId, uint64 poolId, bytes16 scId, uint128 amount,
        bool isIssuance, bool isSnapshot, uint64 nonce) external
        => hubHandlerUpdateSharesCVL(calledContract, centrifugeId) expect void UNRESOLVED;
    function _.registerAsset(uint128 assetId, uint8 decimals) external
        => hubHandlerEntryCVL(calledContract, 201) expect void UNRESOLVED;
    function _.request(uint64 poolId, bytes16 scId, uint128 assetId, bytes payload) external
        => hubHandlerRequestCVL(calledContract) expect void UNRESOLVED;
}

persistent ghost mathint ghostHhCallCount {
    init_state axiom ghostHhCallCount == 0;
    axiom ghostHhCallCount >= 0;
}
persistent ghost address ghostHhLastCallee;
persistent ghost mathint ghostHhLastSourceCid16;
persistent ghost address ghostHhLastRefund;
persistent ghost mathint ghostHhLastValue;
persistent ghost mathint ghostHhLastPoolId64;
persistent ghost bytes16 ghostHhLastScId;
persistent ghost mathint ghostHhLastAssetId128;
persistent ghost mathint ghostHhLastAmount128;
persistent ghost bool ghostHhLastIsIncrease;
persistent ghost bool ghostHhLastIsSnapshot;
persistent ghost mathint ghostHhLastNonce64;
// Tags the entry last reached, 2xx of the handler-face scheme in SpokeHandler.
persistent ghost mathint ghostHhLastEntry;
// Free unless pinned: a request may refuse, as the real handler can.
persistent ghost bool ghostHhRequestRefuses;

function hubHandlerRecordCVL(address callee) {
    ghostHhCallCount = ghostHhCallCount + 1;
    ghostHhLastCallee = callee;
}

function hubHandlerEntryCVL(address callee, mathint tag) {
    hubHandlerRecordCVL(callee);
    ghostHhLastEntry = tag;
}

function hubHandlerInitiateTransferSharesCVL(env e, address callee, uint16 originCentrifugeId, address refund) {
    hubHandlerEntryCVL(callee, 203);
    ghostHhLastSourceCid16 = originCentrifugeId;
    ghostHhLastRefund = refund;
    ghostHhLastValue = e.msg.value;
}

function hubHandlerUpdateAssetsCVL(env e, address callee, uint16 centrifugeId, uint64 poolId, bytes16 scId,
    uint128 assetId, uint128 amount, bool isIncrease, bool isSnapshot, uint64 nonce) {
    hubHandlerEntryCVL(callee, 204);
    ghostHhLastSourceCid16 = centrifugeId;
    ghostHhLastPoolId64 = poolId;
    ghostHhLastScId = scId;
    ghostHhLastAssetId128 = assetId;
    ghostHhLastAmount128 = amount;
    ghostHhLastIsIncrease = isIncrease;
    ghostHhLastIsSnapshot = isSnapshot;
    ghostHhLastNonce64 = nonce;
    ghostHhLastValue = e.msg.value;
}

function hubHandlerUpdateSharesCVL(address callee, uint16 centrifugeId) {
    hubHandlerEntryCVL(callee, 205);
    ghostHhLastSourceCid16 = centrifugeId;
}

function hubHandlerRequestCVL(address callee) {
    if (ghostHhRequestRefuses) {
        revert("handler refused");
    }
    hubHandlerEntryCVL(callee, 202);
}
