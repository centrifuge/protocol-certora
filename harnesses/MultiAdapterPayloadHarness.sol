// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

/// @dev send()'s session stamp and _resolve's vote key and unwrapped message, re-run on the blob the contract
///      slices, which a CVL byte prefix cannot bind. Standalone so the MultiAdapterHarness bytecode stays as is.
contract MultiAdapterPayloadHarness {
    function stamp(uint16 sessionId, bytes calldata payload) external pure returns (bytes memory) {
        return abi.encodePacked(sessionId, payload);
    }

    function voteKeyOf(uint64 poolId, bytes calldata payload) external pure returns (bytes32) {
        return keccak256(abi.encodePacked(poolId, payload));
    }

    function unwrap(bytes calldata payload) external pure returns (bytes memory) {
        return payload[2:];
    }
}
