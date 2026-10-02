// Escrow. Model: pinned-row total and reserved, for scenes not compiling it.

import "../../../../shared/tokens/erc20.spec";
import "../../../../shared/tokens/erc6909.spec";

methods {
    function _.deposit(bytes16 scId, address asset, uint256 tokenId, uint128 value) external
        => peDepositCVL(scId, asset, tokenId, value) expect void UNRESOLVED;
    function _.withdraw(bytes16 scId, address asset, uint256 tokenId, address receiver, uint128 value) external
        => peWithdrawCVL(scId, asset, tokenId, value) expect void UNRESOLVED;
    function _.reserve(bytes16 scId, address asset, uint256 tokenId, uint128 value, address caller, bytes32 reason) external
        => peReserveCVL(scId, asset, tokenId, value) expect void UNRESOLVED;
    function _.unreserve(bytes16 scId, address asset, uint256 tokenId, uint128 value, address caller, bytes32 reason) external
        => peUnreserveCVL(scId, asset, tokenId, value) expect void UNRESOLVED;
    function _.availableBalanceOf(bytes16 scId, address asset, uint256 tokenId) external
        => peAvailableBalanceOfCVL(scId, asset, tokenId) expect uint128 UNRESOLVED;
    function _.authTransferTo(address asset, uint256 tokenId, address receiver, uint256 value) external
        => peAuthTransferToCVL(calledContract, asset, tokenId, receiver, value) expect void UNRESOLVED;
    function _.reservedBy(bytes16 scId, address reserver, bytes32 reason, address asset, uint256 tokenId) external
        => peReservedByCVL() expect uint128 UNRESOLVED;
}

persistent ghost address ghostPeAsset;
persistent ghost uint256 ghostPeTokenId256;
persistent ghost mathint ghostPeTotal128 {
    axiom ghostPeTotal128 >= 0 && ghostPeTotal128 <= max_uint128;
}
persistent ghost mathint ghostPeReserved128 {
    axiom ghostPeReserved128 >= 0 && ghostPeReserved128 <= max_uint128;
}

persistent ghost mathint ghostPeFaceMoveCount {
    axiom ghostPeFaceMoveCount >= 0;
}
persistent ghost uint128 ghostPeFaceLastMove128;
persistent ghost bool ghostPeFaceLastMoveIsIncrease;

// SCOPE: other rows are untracked and never revert here.
definition PE_PINNED_ROW(bytes16 scId, address asset, uint256 tokenId) returns bool =
    scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256;

// Records every escrow move Spoke makes, on the pinned row or off it.
function peRecordMoveCVL(uint128 value, bool isIncrease) {
    ghostPeFaceMoveCount = ghostPeFaceMoveCount + 1;
    ghostPeFaceLastMove128 = value;
    ghostPeFaceLastMoveIsIncrease = isIncrease;
}

function peDepositCVL(bytes16 scId, address asset, uint256 tokenId, uint128 value) {
    if (PE_PINNED_ROW(scId, asset, tokenId)) {
        ghostPeTotal128 = require_uint128(ghostPeTotal128 + value);
    }
    peRecordMoveCVL(value, true);
}

function peWithdrawCVL(bytes16 scId, address asset, uint256 tokenId, uint128 value) {
    if (PE_PINNED_ROW(scId, asset, tokenId)) {
        require(ghostPeTotal128 >= ghostPeReserved128 && ghostPeTotal128 - ghostPeReserved128 >= value,
            "ASSERT: the unreserved balance must cover the amount");
        ghostPeTotal128 = require_uint128(ghostPeTotal128 - value);
    }
    peRecordMoveCVL(value, false);
}

function peReserveCVL(bytes16 scId, address asset, uint256 tokenId, uint128 value) {
    if (PE_PINNED_ROW(scId, asset, tokenId)) {
        ghostPeReserved128 = require_uint128(ghostPeReserved128 + value);
    }
    peRecordMoveCVL(value, false);
}

// UNSAFE: checks the total reserved, not the caller's own bucket.
function peUnreserveCVL(bytes16 scId, address asset, uint256 tokenId, uint128 value) {
    if (PE_PINNED_ROW(scId, asset, tokenId)) {
        require(ghostPeReserved128 >= value, "ASSERT: the total reserved, not the reservation, covers it");
        ghostPeReserved128 = require_uint128(ghostPeReserved128 - value);
    }
    peRecordMoveCVL(value, true);
}

function peAvailableBalanceOfCVL(bytes16 scId, address asset, uint256 tokenId) returns uint128 {
    if (PE_PINNED_ROW(scId, asset, tokenId)) {
        if (ghostPeTotal128 >= ghostPeReserved128) {
            return require_uint128(ghostPeTotal128 - ghostPeReserved128);
        }
        return 0;
    }
    uint128 free;
    return free;
}

function peReservedByCVL() returns uint128 {
    uint128 bucket;
    return bucket;
}

function peAuthTransferToCVL(address escrow, address asset, uint256 tokenId, address receiver, uint256 value) {
    if (tokenId == 0) {
        require(transferERC20CVL(asset, escrow, receiver, value), "ASSERT: the escrow's payout must succeed");
    } else {
        require(transferERC6909CVL(asset, escrow, receiver, tokenId, value), "ASSERT: the escrow's payout must succeed");
    }
}
