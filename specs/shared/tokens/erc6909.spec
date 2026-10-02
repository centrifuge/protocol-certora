// ERC6909 token model: per id balances over the ERC20 model's bounded holders.

import "erc20.spec";

methods {
    // TRUSTED: only standard ERC6909 assets, no operators and no fee.
    function _.balanceOf(address owner, uint256 tokenId) external
        => balanceOfERC6909CVL(calledContract, owner, tokenId) expect uint256;

    function _.allowance(address owner, address spender, uint256 tokenId) external
        => require_uint256(ghostERC6909Allowances256[calledContract][owner][spender][tokenId]) expect uint256;

    function _.decimals(uint256 tokenId) external
        => ghostERC6909Decimals8[calledContract][tokenId] expect uint8;

    function _.approve(address spender, uint256 tokenId, uint256 amount) external with (env e)
        => approveERC6909CVL(calledContract, e.msg.sender, spender, tokenId, amount) expect bool;

    function _.transfer(address to, uint256 tokenId, uint256 amount) external with (env e)
        => transferERC6909CVL(calledContract, e.msg.sender, to, tokenId, amount) expect bool;

    function _.transferFrom(address from, address to, uint256 tokenId, uint256 amount) external with (env e)
        => transferFromERC6909CVL(calledContract, e.msg.sender, from, to, tokenId, amount) expect bool;
}

persistent ghost mapping(address => mapping(uint256 => uint8)) ghostERC6909Decimals8;

persistent ghost mapping(address => mapping(uint256 => mapping(address => mathint))) ghostERC6909Balances128 {
    init_state axiom forall address token. forall uint256 tokenId. forall address account.
        ghostERC6909Balances128[token][tokenId][account] == 0;
    // UNSAFE: balances above max uint128 are not analysed.
    axiom forall address token. forall uint256 tokenId. forall address account.
        ghostERC6909Balances128[token][tokenId][account] >= 0
        && ghostERC6909Balances128[token][tokenId][account] <= max_uint128;
}

persistent ghost mapping(address => mapping(address => mapping(address => mapping(uint256 => mathint)))) ghostERC6909Allowances256 {
    init_state axiom forall address token. forall address owner. forall address spender.
        forall uint256 tokenId.
            ghostERC6909Allowances256[token][owner][spender][tokenId] == 0;
    axiom forall address token. forall address owner. forall address spender.
        forall uint256 tokenId.
            ghostERC6909Allowances256[token][owner][spender][tokenId] >= 0
            && ghostERC6909Allowances256[token][owner][spender][tokenId] <= max_uint256;
}

function setupERC6909() {
    require(forall address token. forall uint256 tokenId.
        ghostERC6909Decimals8[token][tokenId] >= 6
        && ghostERC6909Decimals8[token][tokenId] <= 18,
        "UNSAFE: only tokens of 6 to 18 decimals"
    );
}

function balanceOfERC6909CVL(address token, address account, uint256 tokenId) returns uint256 {
    require(token != 0, "SAFE: no token has code at address zero");
    require(ERC20_ACCOUNT_BOUNDS(token, account), "UNSAFE: at most three accounts per token");
    return require_uint256(ghostERC6909Balances128[token][tokenId][account]);
}

function approveERC6909CVL(
    address token,
    address owner,
    address spender,
    uint256 tokenId,
    uint256 amount
) returns bool {

    require(token != 0, "SAFE: no token has code at address zero");
    require(
        ERC20_ACCOUNT_BOUNDS(token, owner)
        && ERC20_ACCOUNT_BOUNDS(token, spender),
        "UNSAFE: at most three accounts per token"
    );

    ghostERC6909Allowances256[token][owner][spender][tokenId] = amount;

    return true;
}

function transferERC6909CVL(
    address token,
    address from,
    address to,
    uint256 tokenId,
    uint256 amount
) returns bool {

    require(token != 0, "SAFE: no token has code at address zero");
    require(
        ERC20_ACCOUNT_BOUNDS(token, from)
        && ERC20_ACCOUNT_BOUNDS(token, to),
        "UNSAFE: at most three accounts per token"
    );

    require(ghostERC6909Balances128[token][tokenId][from] >= amount, "ASSERT: the balance must cover the amount");

    ghostERC6909Balances128[token][tokenId][from] =
        require_uint256(ghostERC6909Balances128[token][tokenId][from] - amount);
    ghostERC6909Balances128[token][tokenId][to] =
        require_uint256(ghostERC6909Balances128[token][tokenId][to] + amount);

    return true;
}

function transferFromERC6909CVL(
    address token,
    address spender,
    address from,
    address to,
    uint256 tokenId,
    uint256 amount
) returns bool {

    require(token != 0, "SAFE: no token has code at address zero");
    require(
        ERC20_ACCOUNT_BOUNDS(token, from)
        && ERC20_ACCOUNT_BOUNDS(token, to),
        "UNSAFE: at most three accounts per token"
    );

    if (spender != from) {
        require(
            ghostERC6909Allowances256[token][from][spender][tokenId] == max_uint256
            || ghostERC6909Allowances256[token][from][spender][tokenId] >= amount,
            "ASSERT: the allowance must cover the amount"
        );
        if (ghostERC6909Allowances256[token][from][spender][tokenId] != max_uint256) {
            ghostERC6909Allowances256[token][from][spender][tokenId] =
                require_uint256(
                    ghostERC6909Allowances256[token][from][spender][tokenId]
                    - amount
                );
        }
    }

    require(ghostERC6909Balances128[token][tokenId][from] >= amount, "ASSERT: the balance must cover the amount");
    ghostERC6909Balances128[token][tokenId][from] =
        require_uint256(ghostERC6909Balances128[token][tokenId][from] - amount);
    ghostERC6909Balances128[token][tokenId][to] =
        require_uint256(ghostERC6909Balances128[token][tokenId][to] + amount);

    return true;
}
