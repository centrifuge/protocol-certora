// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {IGateway} from "../../src/core/messaging/interfaces/IGateway.sol";

// Adapter quoting a stored fee that, once armed, repays one underpaid batch with the fee its send was paid.
contract ReentrantAdapter {
    IGateway public gateway;
    uint256 public quote;
    bool public armed;
    bool public entered;
    uint16 public repayCentrifugeId;
    bytes public repayBatch;
    address public repayRefund;

    function arm(uint16 centrifugeId, bytes calldata batch, address refund) external {
        armed = true;
        entered = false;
        repayCentrifugeId = centrifugeId;
        repayBatch = batch;
        repayRefund = refund;
    }

    function estimate(uint16, bytes calldata, uint256) external view returns (uint256) {
        return quote;
    }

    function send(uint16, bytes calldata, uint256, address) external payable returns (bytes32) {
        if (armed && !entered) {
            entered = true;
            gateway.repay{value: msg.value}(repayCentrifugeId, repayBatch, repayRefund);
        }
        return bytes32(0);
    }
}
