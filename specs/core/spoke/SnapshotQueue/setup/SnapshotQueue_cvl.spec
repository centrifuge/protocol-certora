// SnapshotQueue. Model: records queue and flush calls, for scenes not compiling it.

methods {
    function _.queueAssets(uint64 poolId, bytes16 scId, uint128 assetId, uint128 amount, bool isIncrease) external
        => sqQueueAssetsCVL(assetId, amount, isIncrease) expect void UNRESOLVED;
    function _.queueShares(uint64 poolId, bytes16 scId, uint128 shares, bool isIssuance) external
        => sqQueueSharesCVL(shares, isIssuance) expect void UNRESOLVED;
    function _.flushAssets(uint64 poolId, bytes16 scId, uint128 assetId) external
        => sqFlushCVL() expect ISpokeMessageSender.UpdateData UNRESOLVED;
    function _.flushShares(uint64 poolId, bytes16 scId) external
        => sqFlushCVL() expect ISpokeMessageSender.UpdateData UNRESOLVED;
    function _.queuedAssets(uint64 poolId, bytes16 scId, uint128 assetId) external
        => sqQueuedAssetsCVL() expect (uint128, uint128) UNRESOLVED;
    function _.queuedShares(uint64 poolId, bytes16 scId) external
        => sqQueuedSharesCVL() expect (uint128, bool, uint32, uint64) UNRESOLVED;
}

persistent ghost mathint ghostSqFaceQueueAssetsCount {
    axiom ghostSqFaceQueueAssetsCount >= 0;
}
persistent ghost uint128 ghostSqFaceLastAssetId128;
persistent ghost uint128 ghostSqFaceLastAmount128;
persistent ghost bool ghostSqFaceLastIsIncrease;

persistent ghost mathint ghostSqFaceQueueSharesCount {
    axiom ghostSqFaceQueueSharesCount >= 0;
}
persistent ghost uint128 ghostSqFaceLastShares128;
persistent ghost bool ghostSqFaceLastIsIssuance;

persistent ghost uint128 ghostSqFaceFlushedNetAmount128;
persistent ghost bool ghostSqFaceFlushedIsIncrease;
persistent ghost bool ghostSqFaceFlushedIsSnapshot;
persistent ghost uint64 ghostSqFaceFlushedNonce64;

function sqQueueAssetsCVL(uint128 assetId, uint128 amount, bool isIncrease) {
    ghostSqFaceQueueAssetsCount = ghostSqFaceQueueAssetsCount + 1;
    ghostSqFaceLastAssetId128 = assetId;
    ghostSqFaceLastAmount128 = amount;
    ghostSqFaceLastIsIncrease = isIncrease;
}

function sqQueueSharesCVL(uint128 shares, bool isIssuance) {
    ghostSqFaceQueueSharesCount = ghostSqFaceQueueSharesCount + 1;
    ghostSqFaceLastShares128 = shares;
    ghostSqFaceLastIsIssuance = isIssuance;
}

// SCOPE: a flush returns an arbitrary update, not the queued deltas.
function sqFlushCVL() returns ISpokeMessageSender.UpdateData {
    ISpokeMessageSender.UpdateData data;
    ghostSqFaceFlushedNetAmount128 = assert_uint128(data.netAmount);
    ghostSqFaceFlushedIsIncrease = data.isIncrease;
    ghostSqFaceFlushedIsSnapshot = data.isSnapshot;
    ghostSqFaceFlushedNonce64 = assert_uint64(data.nonce);
    return data;
}

function sqQueuedAssetsCVL() returns (uint128, uint128) {
    uint128 deposits;
    uint128 withdrawals;
    return (deposits, withdrawals);
}

function sqQueuedSharesCVL() returns (uint128, bool, uint32, uint64) {
    uint128 delta;
    bool isPositive;
    uint32 queuedAssetCounter;
    uint64 nonce;
    return (delta, isPositive, queuedAssetCounter, nonce);
}
