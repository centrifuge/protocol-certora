// Spoke. Model: records balance sheet calls, for scenes not compiling it.

import "../../../../shared/call_order.spec";

methods {
    // UNSAFE: records the call only, no escrow, token or queue leg runs.
    function _.deposit(uint64 poolId, bytes16 scId, address asset, uint256 tokenId, uint128 amount) external with (env e)
        => spAssetMoveCVL(e, calledContract, poolId, scId, asset, tokenId, amount, 0) expect void UNRESOLVED;
    function _.noteDeposit(uint64 poolId, bytes16 scId, address asset, uint256 tokenId, uint128 amount) external with (env e)
        => spAssetMoveCVL(e, calledContract, poolId, scId, asset, tokenId, amount, 1) expect void UNRESOLVED;
    function _.withdraw(uint64 poolId, bytes16 scId, address asset, uint256 tokenId, address receiver, uint128 amount) external with (env e)
        => spWithdrawCVL(e, calledContract, poolId, scId, asset, tokenId, receiver, amount) expect void UNRESOLVED;
    function _.withdrawReserved(uint64 poolId, bytes16 scId, address asset, uint256 tokenId, address receiver, uint128 amount,
        address reserver, bytes32 reason) external with (env e)
        => spWithdrawReservedCVL(e, calledContract, poolId, scId, asset, tokenId, receiver, amount, reserver, reason) expect void UNRESOLVED;
    function _.reserve(uint64 poolId, bytes16 scId, address asset, uint256 tokenId, uint128 amount, address reserver, bytes32 reason) external with (env e)
        => spReserveCVL(e, calledContract, poolId, scId, asset, tokenId, amount, reserver, reason, true) expect void UNRESOLVED;
    function _.unreserve(uint64 poolId, bytes16 scId, address asset, uint256 tokenId, uint128 amount, address reserver, bytes32 reason) external with (env e)
        => spReserveCVL(e, calledContract, poolId, scId, asset, tokenId, amount, reserver, reason, false) expect void UNRESOLVED;
    function _.submitQueuedAssets(uint64 poolId, bytes16 scId, uint128 assetId, uint128 extraGasLimit, address refund) external with (env e)
        => spSubmitCVL(e, calledContract, poolId, scId, assetId, extraGasLimit, refund, true) expect void UNRESOLVED;
    function _.submitQueuedShares(uint64 poolId, bytes16 scId, uint128 extraGasLimit, address refund) external with (env e)
        => spSubmitCVL(e, calledContract, poolId, scId, 0, extraGasLimit, refund, false) expect void UNRESOLVED;
    function _.issue(uint64 poolId, bytes16 scId, address to, uint128 shares) external with (env e)
        => spSharesCVL(e, calledContract, poolId, scId, 0, 0, to, shares, 0) expect void UNRESOLVED;
    function _.withdrawShares(uint64 poolId, bytes16 scId, address receiver, uint128 amount) external with (env e)
        => spSharesCVL(e, calledContract, poolId, scId, 0, 0, receiver, amount, 1) expect void UNRESOLVED;
    function _.revoke(uint64 poolId, bytes16 scId, uint128 shares) external with (env e)
        => spSharesCVL(e, calledContract, poolId, scId, 0, 0, 0, shares, 2) expect void UNRESOLVED;
    function _.transferSharesFrom(uint64 poolId, bytes16 scId, address sender, address from, address to, uint256 amount) external with (env e)
        => spSharesCVL(e, calledContract, poolId, scId, sender, from, to, amount, 3) expect void UNRESOLVED;
    function _.crosschainTransferShares(uint16 centrifugeId, uint64 poolId, bytes16 scId, bytes32 receiver, address sender, address owner,
        uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) external with (env e)
        => spCrosschainCVL(e, calledContract, centrifugeId, poolId, scId, receiver, sender, owner, amount, extraGasLimit,
            remoteExtraGasLimit, refund) expect void UNRESOLVED;
    function _.request(uint64 poolId, bytes16 scId, uint128 assetId, bytes payload, uint128 extraGasLimit, bool unpaid, address refund) external with (env e)
        => spRequestCVL(e, calledContract, poolId, scId, assetId, payload, extraGasLimit, unpaid, refund) expect void UNRESOLVED;

    function _.availableBalanceOf(uint64 poolId, bytes16 scId, address asset, uint256 tokenId) external
        => spAvailableBalanceOfCVL(tokenId) expect uint128 UNRESOLVED;
    function _.spokeRegistry() external => ghostSpSpokeRegistry expect address UNRESOLVED;
    function _.gateway() external => ghostSpGateway expect address UNRESOLVED;
    function _.snapshotQueue() external => ghostSpSnapshotQueue expect address UNRESOLVED;
}

persistent ghost address ghostSpSpokeRegistry;
persistent ghost address ghostSpGateway;
persistent ghost address ghostSpSnapshotQueue;

persistent ghost bool ghostSpFaceReverts;

persistent ghost mathint ghostSpFaceDepositCount {
    init_state axiom ghostSpFaceDepositCount == 0;
    axiom ghostSpFaceDepositCount >= 0;
}
persistent ghost mathint ghostSpFaceNoteDepositCount {
    init_state axiom ghostSpFaceNoteDepositCount == 0;
    axiom ghostSpFaceNoteDepositCount >= 0;
}
persistent ghost mathint ghostSpFaceWithdrawCount {
    init_state axiom ghostSpFaceWithdrawCount == 0;
    axiom ghostSpFaceWithdrawCount >= 0;
}
persistent ghost mathint ghostSpFaceWithdrawReservedCount {
    init_state axiom ghostSpFaceWithdrawReservedCount == 0;
    axiom ghostSpFaceWithdrawReservedCount >= 0;
}
persistent ghost mathint ghostSpFaceReserveCount {
    init_state axiom ghostSpFaceReserveCount == 0;
    axiom ghostSpFaceReserveCount >= 0;
}
persistent ghost mathint ghostSpFaceUnreserveCount {
    init_state axiom ghostSpFaceUnreserveCount == 0;
    axiom ghostSpFaceUnreserveCount >= 0;
}
persistent ghost mathint ghostSpFaceSubmitAssetsCount {
    init_state axiom ghostSpFaceSubmitAssetsCount == 0;
    axiom ghostSpFaceSubmitAssetsCount >= 0;
}
persistent ghost mathint ghostSpFaceSubmitSharesCount {
    init_state axiom ghostSpFaceSubmitSharesCount == 0;
    axiom ghostSpFaceSubmitSharesCount >= 0;
}
persistent ghost mathint ghostSpFaceIssueCount {
    init_state axiom ghostSpFaceIssueCount == 0;
    axiom ghostSpFaceIssueCount >= 0;
}
persistent ghost mathint ghostSpFaceWithdrawSharesCount {
    init_state axiom ghostSpFaceWithdrawSharesCount == 0;
    axiom ghostSpFaceWithdrawSharesCount >= 0;
}
persistent ghost mathint ghostSpFaceRevokeCount {
    init_state axiom ghostSpFaceRevokeCount == 0;
    axiom ghostSpFaceRevokeCount >= 0;
}
persistent ghost mathint ghostSpFaceTransferSharesFromCount {
    init_state axiom ghostSpFaceTransferSharesFromCount == 0;
    axiom ghostSpFaceTransferSharesFromCount >= 0;
}
persistent ghost mathint ghostSpFaceCrosschainTransferCount {
    init_state axiom ghostSpFaceCrosschainTransferCount == 0;
    axiom ghostSpFaceCrosschainTransferCount >= 0;
}
persistent ghost mathint ghostSpFaceRequestCount {
    init_state axiom ghostSpFaceRequestCount == 0;
    axiom ghostSpFaceRequestCount >= 0;
}

persistent ghost address ghostSpFaceLastCallee;
persistent ghost address ghostSpFaceLastCaller;
persistent ghost uint256 ghostSpFaceLastValue256;
persistent ghost uint64 ghostSpFaceLastPoolId64;
persistent ghost bytes16 ghostSpFaceLastScId;
persistent ghost address ghostSpFaceLastAsset;
persistent ghost uint256 ghostSpFaceLastTokenId256;
persistent ghost uint128 ghostSpFaceLastAssetId128;
persistent ghost uint256 ghostSpFaceLastAmount256;
persistent ghost address ghostSpFaceLastSender;
persistent ghost address ghostSpFaceLastFrom;
persistent ghost address ghostSpFaceLastReceiver;
persistent ghost address ghostSpFaceLastReserver;
persistent ghost bytes32 ghostSpFaceLastReason;
persistent ghost uint16 ghostSpFaceLastCentrifugeId16;
persistent ghost bytes32 ghostSpFaceLastRemoteReceiver;
persistent ghost uint128 ghostSpFaceLastExtraGasLimit128;
persistent ghost uint128 ghostSpFaceLastRemoteExtraGasLimit128;
persistent ghost address ghostSpFaceLastRefund;
persistent ghost bytes32 ghostSpFaceLastPayloadHash;
persistent ghost bool ghostSpFaceLastUnpaid;
persistent ghost uint128 ghostSpFaceLastAvailableBalance128;
persistent ghost bool ghostSpFaceSawNonZeroTokenId;
persistent ghost mathint ghostSpFaceLastReserveAt;
persistent ghost mathint ghostSpFaceLastTransferSharesFromAt;
persistent ghost mathint ghostSpFaceLastRevokeAt;

function spRecordCVL(env e, address callee, uint64 poolId, bytes16 scId) {
    havoc ghostSpFaceReverts;
    if (ghostSpFaceReverts) {
        revert("spoke refused the call");
    }
    ghostSpFaceLastCallee = callee;
    ghostSpFaceLastCaller = e.msg.sender;
    ghostSpFaceLastValue256 = e.msg.value;
    ghostSpFaceLastPoolId64 = poolId;
    ghostSpFaceLastScId = scId;
}

function spRecordAssetCVL(address asset, uint256 tokenId, uint128 amount) {
    ghostSpFaceLastAsset = asset;
    ghostSpFaceLastTokenId256 = tokenId;
    ghostSpFaceLastAmount256 = amount;
    if (tokenId != 0) {
        ghostSpFaceSawNonZeroTokenId = true;
    }
}

function spAssetMoveCVL(env e, address callee, uint64 poolId, bytes16 scId, address asset, uint256 tokenId, uint128 amount, uint8 kind) {
    spRecordCVL(e, callee, poolId, scId);
    spRecordAssetCVL(asset, tokenId, amount);
    if (kind == 0) {
        ghostSpFaceDepositCount = ghostSpFaceDepositCount + 1;
    } else {
        ghostSpFaceNoteDepositCount = ghostSpFaceNoteDepositCount + 1;
    }
}

function spWithdrawCVL(env e, address callee, uint64 poolId, bytes16 scId, address asset, uint256 tokenId, address receiver,
    uint128 amount) {
    spRecordCVL(e, callee, poolId, scId);
    spRecordAssetCVL(asset, tokenId, amount);
    ghostSpFaceLastReceiver = receiver;
    ghostSpFaceWithdrawCount = ghostSpFaceWithdrawCount + 1;
}

function spWithdrawReservedCVL(env e, address callee, uint64 poolId, bytes16 scId, address asset, uint256 tokenId, address receiver,
    uint128 amount, address reserver, bytes32 reason) {
    spRecordCVL(e, callee, poolId, scId);
    spRecordAssetCVL(asset, tokenId, amount);
    ghostSpFaceLastReceiver = receiver;
    ghostSpFaceLastReserver = reserver;
    ghostSpFaceLastReason = reason;
    ghostSpFaceWithdrawReservedCount = ghostSpFaceWithdrawReservedCount + 1;
}

function spReserveCVL(env e, address callee, uint64 poolId, bytes16 scId, address asset, uint256 tokenId, uint128 amount,
    address reserver, bytes32 reason, bool isReserve) {
    spRecordCVL(e, callee, poolId, scId);
    spRecordAssetCVL(asset, tokenId, amount);
    ghostSpFaceLastReserver = reserver;
    ghostSpFaceLastReason = reason;
    if (isReserve) {
        ghostSpFaceReserveCount = ghostSpFaceReserveCount + 1;
        ghostSpFaceLastReserveAt = callOrderTickCVL();
    } else {
        ghostSpFaceUnreserveCount = ghostSpFaceUnreserveCount + 1;
    }
}

function spSubmitCVL(env e, address callee, uint64 poolId, bytes16 scId, uint128 assetId, uint128 extraGasLimit, address refund,
    bool isAssets) {
    spRecordCVL(e, callee, poolId, scId);
    ghostSpFaceLastAssetId128 = assetId;
    ghostSpFaceLastExtraGasLimit128 = extraGasLimit;
    ghostSpFaceLastRefund = refund;
    if (isAssets) {
        ghostSpFaceSubmitAssetsCount = ghostSpFaceSubmitAssetsCount + 1;
    } else {
        ghostSpFaceSubmitSharesCount = ghostSpFaceSubmitSharesCount + 1;
    }
}

function spSharesCVL(env e, address callee, uint64 poolId, bytes16 scId, address sender, address from, address to, uint256 amount,
    uint8 kind) {
    spRecordCVL(e, callee, poolId, scId);
    ghostSpFaceLastSender = sender;
    ghostSpFaceLastFrom = from;
    ghostSpFaceLastReceiver = to;
    ghostSpFaceLastAmount256 = amount;
    if (kind == 0) {
        ghostSpFaceIssueCount = ghostSpFaceIssueCount + 1;
    } else if (kind == 1) {
        ghostSpFaceWithdrawSharesCount = ghostSpFaceWithdrawSharesCount + 1;
    } else if (kind == 2) {
        ghostSpFaceRevokeCount = ghostSpFaceRevokeCount + 1;
        ghostSpFaceLastRevokeAt = callOrderTickCVL();
    } else {
        ghostSpFaceTransferSharesFromCount = ghostSpFaceTransferSharesFromCount + 1;
        ghostSpFaceLastTransferSharesFromAt = callOrderTickCVL();
    }
}

function spCrosschainCVL(env e, address callee, uint16 centrifugeId, uint64 poolId, bytes16 scId, bytes32 receiver, address sender,
    address owner, uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {
    spRecordCVL(e, callee, poolId, scId);
    ghostSpFaceLastCentrifugeId16 = centrifugeId;
    ghostSpFaceLastRemoteReceiver = receiver;
    ghostSpFaceLastSender = sender;
    ghostSpFaceLastFrom = owner;
    ghostSpFaceLastAmount256 = amount;
    ghostSpFaceLastExtraGasLimit128 = extraGasLimit;
    ghostSpFaceLastRemoteExtraGasLimit128 = remoteExtraGasLimit;
    ghostSpFaceLastRefund = refund;
    ghostSpFaceCrosschainTransferCount = ghostSpFaceCrosschainTransferCount + 1;
}

function spRequestCVL(env e, address callee, uint64 poolId, bytes16 scId, uint128 assetId, bytes payload, uint128 extraGasLimit,
    bool unpaid, address refund) {
    spRecordCVL(e, callee, poolId, scId);
    ghostSpFaceLastAssetId128 = assetId;
    ghostSpFaceLastPayloadHash = keccak256(payload);
    ghostSpFaceLastExtraGasLimit128 = extraGasLimit;
    ghostSpFaceLastUnpaid = unpaid;
    ghostSpFaceLastRefund = refund;
    ghostSpFaceRequestCount = ghostSpFaceRequestCount + 1;
}

function spAvailableBalanceOfCVL(uint256 tokenId) returns uint128 {
    havoc ghostSpFaceReverts;
    if (ghostSpFaceReverts) {
        revert("spoke refused the balance query");
    }
    if (tokenId != 0) {
        ghostSpFaceSawNonZeroTokenId = true;
    }
    uint128 balance;
    ghostSpFaceLastAvailableBalance128 = balance;
    return balance;
}
