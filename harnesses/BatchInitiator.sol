// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {IGateway} from "../../src/core/messaging/interfaces/IGateway.sol";

interface IPauseSwitch {
    function pause() external;
}

// withBatch driver: callbacks that lock, skip the lock, send twice, or send then pause the protocol.
contract BatchInitiator {
    IGateway public gateway;
    IPauseSwitch public pauser;

    function runLocking(bytes calldata inner, uint256 callbackValue, address refund) external payable {
        gateway.withBatch{value: msg.value}(abi.encodeCall(this.lockingCallback, (inner)), callbackValue, refund);
    }

    function runNotLocking(bytes calldata inner, uint256 callbackValue, address refund) external payable {
        gateway.withBatch{value: msg.value}(abi.encodeCall(this.notLockingCallback, (inner)), callbackValue, refund);
    }

    function runSending(
        uint16 centrifugeIdA,
        uint16 centrifugeIdB,
        bytes calldata inner,
        uint256 callbackValue,
        address refund
    ) external payable {
        gateway.withBatch{value: msg.value}(
            abi.encodeCall(this.sendingCallback, (centrifugeIdA, centrifugeIdB, inner)), callbackValue, refund
        );
    }

    function runSendThenPause(uint16 centrifugeId, bytes calldata inner, address refund) external payable {
        gateway.withBatch{value: msg.value}(abi.encodeCall(this.sendThenPauseCallback, (centrifugeId, inner)), refund);
    }

    function lockingCallback(bytes calldata) external payable {
        gateway.lockCallback();
    }

    function notLockingCallback(bytes calldata) external payable {}

    // Any callback value stays here, as send refuses value inside a batch.
    function sendingCallback(uint16 centrifugeIdA, uint16 centrifugeIdB, bytes calldata inner) external payable {
        gateway.lockCallback();
        gateway.send(centrifugeIdA, inner, false, address(this));
        gateway.send(centrifugeIdB, inner, false, address(this));
    }

    function sendThenPauseCallback(uint16 centrifugeId, bytes calldata inner) external payable {
        gateway.lockCallback();
        gateway.send(centrifugeId, inner, false, address(this));
        _pause();
    }

    // Internal so the scene can summarize it: a wildcard entry misses this dispatched call.
    function _pause() internal {
        pauser.pause();
    }
}
