/* ── MUTATION SnapshotQueue #5102 ──────────────────────────────────
 * @desc:   rely runs without the ward gate in the shared Auth mixin, so any caller seats itself among the wards that move the whole queue.
 * @rules:  acSqOnlyAWardMovesTheWardBit
 * @conf:   certora/confs/core/spoke/SnapshotQueue/single_pool_access_control.conf
 * @target: src/misc/Auth.sol
 * Was:     function rely(address user) public auth {
 * Now:     function rely(address user) public { // MUTATION: granting authority over the queue no longer requires a ward
 * ────────────────────────────────────────────────────────────────*/
// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity 0.8.28;

import {IAuth} from "./interfaces/IAuth.sol";

/// @title  Auth
/// @notice Simple authentication pattern
/// @author Based on code from https://github.com/makerdao/dss
abstract contract Auth is IAuth {
    /// @inheritdoc IAuth
    mapping(address => uint256) public wards;

    constructor(address initialWard) {
        wards[initialWard] = 1;
        emit Rely(initialWard);
    }

    /// @dev Check if the msg.sender has permissions
    modifier auth() {
        require(wards[msg.sender] == 1, NotAuthorized());
        _;
    }

    /// @inheritdoc IAuth
    function rely(address user) public { // MUTATION: granting authority over the queue no longer requires a ward
        wards[user] = 1;
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public auth {
        wards[user] = 0;
        emit Deny(user);
    }
}
