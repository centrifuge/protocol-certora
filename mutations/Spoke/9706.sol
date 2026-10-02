/* ── MUTATION Spoke #9706 ────────────────────────────────────────────────
 * @desc:   The re-entrancy lock no longer checks who re-enters, so another contract can register assets or bridge shares mid-call.
 * @rules:  rvSpProtectedEntriesRefuseAForeignReentrantCaller
 * @conf:   certora/confs/core/spoke/Spoke/reverts.conf
 * @target: src/misc/ReentrancyProtection.sol
 * Was:     require(msg.sender == _initiator, UnauthorizedSender());
 * Now:     // MUTATION: a caller other than the lock holder re-enters unchecked
 * ────────────────────────────────────────────────────────────────*/
// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.28;

// NOTE: This file has warning disabled due https://github.com/ethereum/solidity/issues/14359
// If perform any change on it, please ensure no other warnings appears

/// @title  ReentrancyProtection
/// @notice Abstract contract that implements reentrancy protection using transient storage.
abstract contract ReentrancyProtection {
    /// @notice Dispatched when there is a re-entrancy issue
    error UnauthorizedSender();

    address private transient _initiator;

    /// @dev The method is protected for reentrancy issues.
    modifier protected() {
        if (_initiator == address(0)) {
            // Single call re-entrancy lock
            _initiator = msg.sender;
            _;
            _initiator = address(0);
        } else {
            // Multicall re-entrancy lock
            // MUTATION: a caller other than the lock holder re-enters unchecked
            _;
        }
    }
}
