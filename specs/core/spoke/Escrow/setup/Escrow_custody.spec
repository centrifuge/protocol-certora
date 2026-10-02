// Escrow, custody lane. Setup: token movers on a permissive token, nothing pinned.

// Own setup: the token movers base excludes, on a modelled token; base's hooks pin one (asset, tokenId) row.

import "../../../../shared/env.spec";

using Escrow as _PoolEscrow;

methods {
    function _PoolEscrow.holding(Escrow.ShareClassId, address, uint256) external returns (uint128, uint128) envfree;

    // TRUSTED: a permissive token, short transfers succeed as no-ops.
    function _.balanceOf(address account) external
        => peCustodyBalanceOf20CVL(calledContract, account) expect uint256;
    function _.balanceOf(address account, uint256 tokenId) external
        => peCustodyBalanceOf6909CVL(calledContract, tokenId, account) expect uint256;
    function _.transfer(address to, uint256 tokenId, uint256 amount) external with (env e)
        => peCustodyTransfer6909CVL(calledContract, e.msg.sender, to, tokenId, amount) expect bool;

    // TRUSTED: SafeTransferLib calls the named token's transfer correctly.
    function SafeTransferLib.safeTransfer(address token, address to, uint256 value) internal
        => peCustodyTransfer20CVL(token, calledContract, to, value);
}

definition PE_ETH_ADDRESS() returns address = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

persistent ghost mapping(address => mapping(address => mathint)) ghostPeTok20Bal {
    axiom forall address token. forall address account. ghostPeTok20Bal[token][account] >= 0;
}

persistent ghost mapping(address => mapping(uint256 => mapping(address => mathint))) ghostPeTok6909Bal {
    axiom forall address token. forall uint256 id. forall address account. ghostPeTok6909Bal[token][id][account] >= 0;
}

persistent ghost mathint ghostPeCustodyMoveCount;
persistent ghost address ghostPeCustodyLastToken;
persistent ghost address ghostPeCustodyLastTo;
persistent ghost uint256 ghostPeCustodyLastTokenId;
persistent ghost uint256 ghostPeCustodyLastAmount;

definition PE_CUSTODY_BAL(address token, uint256 tokenId, address account) returns mathint =
    tokenId == 0 ? ghostPeTok20Bal[token][account] : ghostPeTok6909Bal[token][tokenId][account];

function peCustodyRecordCVL(address token, address to, uint256 tokenId, uint256 amount) {
    ghostPeCustodyMoveCount = ghostPeCustodyMoveCount + 1;
    ghostPeCustodyLastToken = token;
    ghostPeCustodyLastTo = to;
    ghostPeCustodyLastTokenId = tokenId;
    ghostPeCustodyLastAmount = amount;
}

function peCustodyBalanceOf20CVL(address token, address account) returns uint256 {
    require(ghostPeTok20Bal[token][account] <= max_uint256, "SAFE: a balance fits the word it is returned in");
    return assert_uint256(ghostPeTok20Bal[token][account]);
}

function peCustodyBalanceOf6909CVL(address token, uint256 tokenId, address account) returns uint256 {
    require(ghostPeTok6909Bal[token][tokenId][account] <= max_uint256,
        "SAFE: a balance fits the word it is returned in");
    return assert_uint256(ghostPeTok6909Bal[token][tokenId][account]);
}

function peCustodyTransfer20CVL(address token, address from, address to, uint256 amount) {
    if (ghostPeTok20Bal[token][from] >= amount) {
        ghostPeTok20Bal[token][from] = ghostPeTok20Bal[token][from] - amount;
        ghostPeTok20Bal[token][to] = ghostPeTok20Bal[token][to] + amount;
    }
    peCustodyRecordCVL(token, to, 0, amount);
}

function peCustodyTransfer6909CVL(address token, address from, address to, uint256 tokenId, uint256 amount)
    returns bool {
    if (ghostPeTok6909Bal[token][tokenId][from] >= amount) {
        ghostPeTok6909Bal[token][tokenId][from] = ghostPeTok6909Bal[token][tokenId][from] - amount;
        ghostPeTok6909Bal[token][tokenId][to] = ghostPeTok6909Bal[token][tokenId][to] + amount;
    }
    peCustodyRecordCVL(token, to, tokenId, amount);
    return true;
}

function setupPoolEscrowCustody(env e) {
    setupEnv(e);
}
