// ShareTokenRegistrar. Model: the token calls it relays, for scenes not compiling it.

import "../tokens/erc20.spec";
import "../call_order.spec";

methods {
    // SCOPE: no transfer hook, so a mint it would block succeeds.
    function _.mint(address token, address to, uint256 amount) external
        => registrarMintAtCVL(calledContract, token, to, amount) expect void;

    // SCOPE: no transfer hook, so a burn it would block succeeds.
    function _.burn(address token, address from, uint256 amount) external with (env e)
        => registrarBurnCVL(calledContract, e.msg.sender, token, from, amount) expect void;

    // SCOPE: no transfer hook, so a transfer it would block succeeds.
    function _.authTransferFrom(address token, address sender, address from, address to, uint256 amount) external
        => registrarAuthTransferFromCVL(token, sender, from, to, amount) expect void;

    // UNSAFE: deploys never revert and all return one address.
    function _.newToken(string name, string symbol, uint8 decimals, bytes32 salt, bytes payload) external
        => registrarNewTokenCVL(salt) expect address;

    // SCOPE: a free verdict per argument tuple, fixed for the whole rule.
    function _.canBridge(address token, address from, uint16 centrifugeId, uint256 amount) external
        => ghostRegistrarCanBridge[token][from][centrifugeId][amount] expect bool;

    // SCOPE: a pure address preview no in-scene logic consumes.
    function _.previewTokenAddress(string name, string symbol, uint8 decimals, bytes32 salt, bytes payload) external
        => NONDET;

    // SCOPE: effects land in the token or its hook, unobserved in scene.
    function _.updateMetadata(address token, string name, string symbol) external
        => NONDET;

    // UNSAFE: the InvalidHook refusal and the hook's effects are dropped.
    function _.updateRestriction(address token, bytes update) external
        => registrarUpdateRestrictionCVL(token, update) expect void;
}

// TRUSTED: a token the registrar deploys is never the zero address.
persistent ghost address ghostRegistrarNewToken {
    axiom ghostRegistrarNewToken != 0;
}
persistent ghost bytes32 ghostRegistrarLastNewTokenSalt;
persistent ghost mapping(address => mapping(address => mapping(uint16 => mapping(uint256 => bool)))) ghostRegistrarCanBridge;
persistent ghost mathint ghostRegistrarSupplyCalls;
persistent ghost address ghostRegistrarLastSupplyCallee;
persistent ghost mathint ghostRegistrarLastBurnAt;
persistent ghost mathint ghostRegistrarRestrictionCount {
    init_state axiom ghostRegistrarRestrictionCount == 0;
    axiom ghostRegistrarRestrictionCount >= 0;
}
persistent ghost address ghostRegistrarLastRestrictionToken;
persistent ghost bytes32 ghostRegistrarLastRestrictionHash;

function registrarMintCVL(address token, address to, uint256 amount) {
    require(mintERC20CVL(token, to, amount), "ASSERT: registrar mint must succeed");
}

function registrarMintAtCVL(address registrar, address token, address to, uint256 amount) {
    registrarMintCVL(token, to, amount);
    ghostRegistrarSupplyCalls = ghostRegistrarSupplyCalls + 1;
    ghostRegistrarLastSupplyCallee = registrar;
}

function registrarBurnCVL(address registrar, address caller, address token, address from, uint256 amount) {
    if (caller != registrar && ghostERC20Allowances256[token][caller][registrar] != max_uint256) {
        if (ghostERC20Allowances256[token][caller][registrar] < amount) {
            revert("InsufficientAllowance");
        }
        ghostERC20Allowances256[token][caller][registrar] =
            require_uint256(ghostERC20Allowances256[token][caller][registrar] - amount);
    }
    require(burnERC20CVL(token, from, amount), "ASSERT: registrar burn must succeed");
    ghostRegistrarSupplyCalls = ghostRegistrarSupplyCalls + 1;
    ghostRegistrarLastSupplyCallee = registrar;
    ghostRegistrarLastBurnAt = callOrderTickCVL();
}

function registrarAuthTransferFromCVL(address token, address sender, address from, address to, uint256 amount) {
    require(token != 0, "SAFE: no token has code at address zero");
    require(ERC20_ACCOUNT_BOUNDS(token, from) && ERC20_ACCOUNT_BOUNDS(token, to),
        "UNSAFE: at most three accounts per token");
    require(ghostERC20Balances128[token][from] >= amount, "ASSERT: the balance must cover the amount");
    if (sender != from) {
        require(ghostERC20Allowances256[token][from][sender] == max_uint256
            || ghostERC20Allowances256[token][from][sender] >= amount, "ASSERT: the allowance must cover the amount");
        if (ghostERC20Allowances256[token][from][sender] != max_uint256) {
            ghostERC20Allowances256[token][from][sender] =
                require_uint256(ghostERC20Allowances256[token][from][sender] - amount);
        }
    }
    ghostERC20Balances128[token][from] = require_uint256(ghostERC20Balances128[token][from] - amount);
    ghostERC20Balances128[token][to] = require_uint256(ghostERC20Balances128[token][to] + amount);
}

function registrarNewTokenCVL(bytes32 salt) returns address {
    ghostRegistrarLastNewTokenSalt = salt;
    return ghostRegistrarNewToken;
}

function registrarUpdateRestrictionCVL(address token, bytes update) {
    ghostRegistrarRestrictionCount = ghostRegistrarRestrictionCount + 1;
    ghostRegistrarLastRestrictionToken = token;
    ghostRegistrarLastRestrictionHash = keccak256(update);
}
