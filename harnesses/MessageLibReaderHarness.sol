// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {MessageLib} from "../../src/core/messaging/libraries/MessageLib.sol";

/// @dev Forwarders to MessageLib's length and extra gas readers, the ones the Gateway and MultiAdapter run.
contract MessageLibReaderHarness {
    function messageLengthOf(bytes calldata message) external pure returns (uint16) {
        return MessageLib.messageLength(message);
    }

    function messageExtraGasLimitOf(bytes calldata message) external pure returns (uint128) {
        return MessageLib.messageExtraGasLimit(message);
    }
}
