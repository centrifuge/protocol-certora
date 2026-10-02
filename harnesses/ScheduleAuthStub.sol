// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

/// @dev Stand-in for the upgrade authority, whose calls from MessageProcessor lose their sighash.
///      The scene summarizes both entries, so the bodies are empty and never revert.
contract ScheduleAuthStub {
    function scheduleRely(address target) external {}

    function cancelRely(address target) external {}
}
