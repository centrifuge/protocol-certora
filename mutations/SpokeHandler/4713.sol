/* ── MUTATION SpokeHandler #4713 ──────────────────────────────────
 * @desc:   The auth modifier's ward test is inverted, so only non-wards pass and any of them can make itself a ward.
 * @rules:  acShWardRosterMovesOnlyForAWard
 * @conf:   certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf
 * @target: src/misc/Auth.sol
 * Was:     require(wards[msg.sender] == 1, NotAuthorized());
 * Now:     require(wards[msg.sender] != 1, NotAuthorized()); // MUTATION: the ward test is inverted
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
        require(wards[msg.sender] != 1, NotAuthorized()); // MUTATION: the ward test is inverted
        _;
    }

    /// @inheritdoc IAuth
    function rely(address user) public auth {
        wards[user] = 1;
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public auth {
        wards[user] = 0;
        emit Deny(user);
    }
}
