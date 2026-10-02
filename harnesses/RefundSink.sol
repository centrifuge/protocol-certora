// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

// ETH refund receiver with accept and reject modes, so ETH neutrality rules see both.
contract RefundSink {
    error RefundRejected();

    bool public rejectMode;

    function setRejectMode(bool rejectMode_) external {
        rejectMode = rejectMode_;
    }

    receive() external payable {
        require(!rejectMode, RefundRejected());
    }
}
