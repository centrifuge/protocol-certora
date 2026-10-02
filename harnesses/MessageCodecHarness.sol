// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {MessageLib} from "../../src/core/messaging/libraries/MessageLib.sol";

/// @dev MessageLib's encoders on structs built as MessageDispatcher builds them, so MessageProcessor gets its bytes.
contract MessageCodecHarness {
    function serializeInitiateTransferShares(
        uint16 centrifugeId,
        uint64 poolId,
        bytes16 scId,
        bytes32 receiver,
        uint128 amount,
        uint128 remoteExtraGasLimit,
        uint128 extraGasLimit,
        bytes32 sender
    ) external pure returns (bytes memory) {
        return MessageLib.serialize(
            MessageLib.InitiateTransferShares({
                centrifugeId: centrifugeId,
                poolId: poolId,
                scId: scId,
                receiver: receiver,
                amount: amount,
                remoteExtraGasLimit: remoteExtraGasLimit,
                extraGasLimit: extraGasLimit,
                sender: sender
            })
        );
    }

    function serializeSetPoolAdapters(
        uint64 poolId,
        uint8 threshold,
        uint16 targetSessionId,
        bytes32[] calldata adapters
    ) external pure returns (bytes memory) {
        return MessageLib.serialize(
            MessageLib.SetPoolAdapters({
                poolId: poolId, threshold: threshold, targetSessionId: targetSessionId, adapterList: adapters
            })
        );
    }
}
