// SafeTransferLib model: its helpers routed onto the shared ERC20 token model.

import "erc20.spec";

methods {
    function SafeTransferLib.safeTransfer(address token, address to, uint256 value) internal
        => safeTransferLibCVL(token, calledContract, to, value);
    function SafeTransferLib.safeTransferFrom(address token, address from, address to, uint256 value) internal
        => safeTransferFromLibCVL(token, calledContract, from, to, value);
    function SafeTransferLib.safeApprove(address token, address to, uint256 value) internal
        => safeApproveLibCVL(token, calledContract, to, value);
}

function safeTransferLibCVL(address token, address src, address to, uint256 amount) {
    require(transferERC20CVL(token, src, to, amount), "ASSERT: the token transfer must succeed");
}

function safeTransferFromLibCVL(address token, address spender, address from, address to, uint256 amount) {
    require(transferFromERC20CVL(token, spender, from, to, amount), "ASSERT: the transfer from the payer must succeed");
}

function safeApproveLibCVL(address token, address owner, address spender, uint256 amount) {
    require(approveERC20CVL(token, owner, spender, amount), "ASSERT: the token approval must succeed");
}
