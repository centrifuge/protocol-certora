// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

/// @dev A hub handler refusing every request with a real revert, so a caller's try/catch sees it.
contract HubHandlerRefusingStub {
    error Refused();

    function request(uint64, bytes16, uint128, bytes calldata) external pure {
        revert Refused();
    }
}
