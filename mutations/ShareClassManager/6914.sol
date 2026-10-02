/* ── MUTATION ShareClassManager #6914 ──────────────────
 * @desc:   Withdrawing authority installs the seat instead of clearing it, so a party that was denied keeps its powers.
 * @rules:  rcScRelyThenDenyRoundTripIsReachable
 * @conf:   certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf
 * @target: src/misc/Auth.sol
 * Was:     wards[user] = 0;
 * Now:     wards[user] = 1; // MUTATION: the withdrawal installs a seat instead of clearing one
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
        wards[user] = 1; // MUTATION: the withdrawal installs a seat instead of clearing one
        emit Deny(user);
    }
}
