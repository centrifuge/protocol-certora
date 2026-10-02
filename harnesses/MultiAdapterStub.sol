// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

/// @dev Stand-in for setAdapters, whose call from MessageProcessor loses its sighash on a symbolic length list.
///      The scene summarizes the entry, so the body is empty and never reverts.
contract MultiAdapterStub {
    function setAdapters(
        uint16 centrifugeId,
        uint64 poolId,
        address[] calldata adapters,
        uint8 threshold,
        uint16 targetSessionId
    ) external {}
}
