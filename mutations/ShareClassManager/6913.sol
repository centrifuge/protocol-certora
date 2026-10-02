/* ── MUTATION ShareClassManager #6913 ──────────────────
 * @desc:   Granting authority emits the grant without writing the seat, so the party named is never actually admitted.
 * @rules:  rcScRelyThenDenyRoundTripIsReachable
 * @conf:   certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf
 * @target: src/misc/Auth.sol
 * Was:     wards[user] = 1;
 * Now:     // wards[user] = 1; // MUTATION: the grant never writes the seat
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
        // wards[user] = 1; // MUTATION: the grant never writes the seat
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public auth {
        wards[user] = 0;
        emit Deny(user);
    }
}
