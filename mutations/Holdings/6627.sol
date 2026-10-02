/* ── MUTATION Holdings #6627 ─────────────────────
 * @desc:   revoking authority emits the event but never clears the ward, so granted authority can never be taken back.
 * @rules:  rcHoWardGrantAndRevokeRoundTripIsReachable
 * @conf:   certora/confs/core/hub/Holdings/single_pool_reachability.conf
 * @target: src/misc/Auth.sol
 * Was:     wards[user] = 0;
 * Now:     // MUTATION: the revocation never takes the ward off the roll
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
        // MUTATION: the revocation records the event but never takes the ward off the roll
        emit Deny(user);
    }
}
