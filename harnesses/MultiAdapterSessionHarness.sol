// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

/// @dev _resolve's session read, re-run on the blob the contract slices. Standalone so the harnesses the delivered
///      MultiAdapter confs compile stay as they are.
contract MultiAdapterSessionHarness {
    function sessionOf(bytes calldata payload) external pure returns (uint16) {
        return uint16(bytes2(payload[0:2]));
    }
}
