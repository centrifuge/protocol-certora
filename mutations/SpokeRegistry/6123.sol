/* ── MUTATION SpokeRegistry #6123 ─────────────────────────────────────
 * @desc:   Revoking authority clears the caller's own seat instead of the named account's, so the target keeps its rights.
 * @rules:  rcSrDenyLeavingTheCallersOwnSeatIsReachable
 * @conf:   certora/confs/core/spoke/SpokeRegistry/reachability.conf
 * @target: src/misc/Auth.sol
 * Was:     wards[user] = 0;
 * Now:     wards[msg.sender] = 0;
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
    function deny(address user) public auth {
        // MUTATION: the withdrawal lands on the caller instead of the named account
        wards[msg.sender] = 0;
        emit Deny(user);
    }
}
