// ERC20 token model: balances, allowances and supply over a bounded holder set.

methods {
    // TRUSTED: the asset policy admits plain ERC20s, no fee or rebase.
    function _.balanceOf(address account) external
        => balanceOfERC20CVL(calledContract, account) expect uint256;

    function _.decimals() external
        => ghostERC20Decimals8[calledContract] expect uint8;

    function _.totalSupply() external
        => require_uint256(ghostERC20TotalSupply256[calledContract]) expect uint256;

    function _.approve(address spender, uint256 amount) external with (env e)
        => approveERC20CVL(calledContract, e.msg.sender, spender, amount) expect bool;

    // SCOPE: no ShareToken hook veto, so a transfer it blocks succeeds.
    function _.transfer(address to, uint256 amount) external with (env e)
        => transferERC20CVL(calledContract, e.msg.sender, to, amount) expect bool;

    function _.transferFrom(address from, address to, uint256 amount) external with (env e)
        => transferFromERC20CVL(calledContract, e.msg.sender, from, to, amount) expect bool;

    function _.allowance(address owner, address spender) external
        => require_uint256(ghostERC20Allowances256[calledContract][owner][spender]) expect uint256;
}

// UNSAFE: three holders per token, one spare beside a two-party move.
definition MAX_ERC20_USERS() returns mathint = 3;

definition ERC20_ACCOUNT_BOUNDS(address token, address account) returns bool =
    ghostERC20AccountsValues[token][0] == account
    || ghostERC20AccountsValues[token][1] == account
    || ghostERC20AccountsValues[token][2] == account
    ;

persistent ghost ghostERC20Accounts(address, mathint) returns address {
    axiom forall address token. forall mathint i. forall mathint j.
        i >= 0 && i < MAX_ERC20_USERS()
        && j >= 0 && j < MAX_ERC20_USERS()
        && i != j
        => ghostERC20Accounts(token, i) != ghostERC20Accounts(token, j);
}

persistent ghost mapping (address => mapping (mathint => address)) ghostERC20AccountsValues {
    axiom forall address token. forall mathint i.
        ghostERC20AccountsValues[token][i] == ghostERC20Accounts(token, i);
    axiom forall address token. forall mathint i.
        (i >= 0 && i < MAX_ERC20_USERS())
        => ghostERC20AccountsValues[token][i] != 0;
}

definition ERC20_TOTAL_SUPPLY_SOLVENCY() returns bool =
    forall address token.
        ghostERC20TotalSupply256[token]
        == ghostERC20Balances128[token][ghostERC20AccountsValues[token][0]]
        + ghostERC20Balances128[token][ghostERC20AccountsValues[token][1]]
        + ghostERC20Balances128[token][ghostERC20AccountsValues[token][2]];

function setupERC20() {

    require(ERC20_TOTAL_SUPPLY_SOLVENCY(), "UNSAFE: a token's whole supply sits in its three accounts");

    require(forall address token.
        ghostERC20Decimals8[token] >= 6
        && ghostERC20Decimals8[token] <= 18,
        "UNSAFE: only tokens of 6 to 18 decimals"
    );
}

persistent ghost mapping(address => uint8) ghostERC20Decimals8;

persistent ghost mapping(address => mapping(address => mathint)) ghostERC20Balances128 {
    init_state axiom forall address token. forall address account.
        ghostERC20Balances128[token][account] == 0;
    // UNSAFE: balances above max uint128 are not analysed.
    axiom forall address token. forall address account.
        ghostERC20Balances128[token][account] >= 0
        && ghostERC20Balances128[token][account] <= max_uint128;
}

persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostERC20Allowances256 {
    init_state axiom forall address token. forall address owner.
        forall address spender.
            ghostERC20Allowances256[token][owner][spender] == 0;
    axiom forall address token. forall address owner.
        forall address spender.
            ghostERC20Allowances256[token][owner][spender] >= 0
            && ghostERC20Allowances256[token][owner][spender] <= max_uint256;
}

persistent ghost mapping(address => mathint) ghostERC20TotalSupply256 {
    init_state axiom forall address token.
        ghostERC20TotalSupply256[token] == 0;
    axiom forall address token.
        ghostERC20TotalSupply256[token] >= 0
        && ghostERC20TotalSupply256[token] <= max_uint256;
}

function balanceOfERC20CVL(address token, address account) returns uint256 {
    require(token != 0, "SAFE: no token has code at address zero");
    require(ERC20_ACCOUNT_BOUNDS(token, account), "UNSAFE: at most three accounts per token");
    return require_uint256(ghostERC20Balances128[token][account]);
}

function approveERC20CVL(
    address token,
    address owner,
    address spender,
    uint256 amount
) returns bool {

    require(token != 0, "SAFE: no token has code at address zero");
    require(
        ERC20_ACCOUNT_BOUNDS(token, owner)
        && ERC20_ACCOUNT_BOUNDS(token, spender),
        "UNSAFE: at most three accounts per token"
    );

    ghostERC20Allowances256[token][owner][spender] = amount;

    return true;
}

function transferERC20CVL(
    address token,
    address from,
    address to,
    uint256 amount
) returns bool {

    require(token != 0, "SAFE: no token has code at address zero");
    require(
        ERC20_ACCOUNT_BOUNDS(token, from)
        && ERC20_ACCOUNT_BOUNDS(token, to),
        "UNSAFE: at most three accounts per token"
    );

    require(ghostERC20Balances128[token][from] >= amount, "ASSERT: the balance must cover the amount");

    ghostERC20Balances128[token][from] =
        require_uint256(ghostERC20Balances128[token][from] - amount);
    ghostERC20Balances128[token][to] =
        require_uint256(ghostERC20Balances128[token][to] + amount);

    return true;
}

function transferFromERC20CVL(
    address token,
    address spender,
    address from,
    address to,
    uint256 amount
) returns bool {

    require(token != 0, "SAFE: no token has code at address zero");
    require(
        ERC20_ACCOUNT_BOUNDS(token, from)
        && ERC20_ACCOUNT_BOUNDS(token, to),
        "UNSAFE: at most three accounts per token"
    );

    // UNSAFE: self-pulls need a self-allowance here, pruning some paths.
    require(
        ghostERC20Allowances256[token][from][spender] == max_uint256
        || ghostERC20Allowances256[token][from][spender] >= amount,
        "ASSERT: the allowance must cover the amount"
    );

    if (ghostERC20Allowances256[token][from][spender] != max_uint256) {
        ghostERC20Allowances256[token][from][spender] =
            require_uint256(
                ghostERC20Allowances256[token][from][spender]
                - amount
            );
    }

    require(ghostERC20Balances128[token][from] >= amount, "ASSERT: the balance must cover the amount");
    ghostERC20Balances128[token][from] =
        require_uint256(ghostERC20Balances128[token][from] - amount);
    ghostERC20Balances128[token][to] =
        require_uint256(ghostERC20Balances128[token][to] + amount);

    return true;
}

function mintERC20CVL(
    address token,
    address to,
    uint256 amount
) returns bool {

    require(token != 0, "SAFE: no token has code at address zero");
    require(ERC20_ACCOUNT_BOUNDS(token, to), "UNSAFE: at most three accounts per token");

    ghostERC20Balances128[token][to] =
        require_uint256(ghostERC20Balances128[token][to] + amount);
    ghostERC20TotalSupply256[token] =
        require_uint256(ghostERC20TotalSupply256[token] + amount);

    return true;
}

function burnERC20CVL(
    address token,
    address from,
    uint256 amount
) returns bool {

    require(token != 0, "SAFE: no token has code at address zero");
    require(ERC20_ACCOUNT_BOUNDS(token, from), "UNSAFE: at most three accounts per token");

    require(ghostERC20Balances128[token][from] >= amount, "ASSERT: the balance must cover the amount");

    ghostERC20Balances128[token][from] =
        require_uint256(ghostERC20Balances128[token][from] - amount);
    ghostERC20TotalSupply256[token] =
        require_uint256(ghostERC20TotalSupply256[token] - amount);

    return true;
}
