/* ── MUTATION Spoke #5302 ────────────────────────────────
 * @desc:   deny drops its authorisation, so any caller strips a ward of its permissions.
 * @rules:  acSpWardListMovesOnlyForAWard
 * @conf:   certora/confs/core/spoke/Spoke/access_control.conf
 * @target: src/misc/Auth.sol
 * Was:     function deny(address user) public auth {
 * Now:     function deny(address user) public {  (auth dropped)
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
    function rely(address user) public auth {
        wards[user] = 1;
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public { // MUTATION: authorisation dropped
        wards[user] = 0;
        emit Deny(user);
    }
}
