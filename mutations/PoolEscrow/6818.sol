/* ── MUTATION PoolEscrow #6818 ────────────────────────
 * @desc:   deny refuses to strip any seat but the caller's own, so a ward can no longer remove another account from the roll.
 * @rules:  rcPeDenyRevokesAnotherWard
 * @conf:   certora/confs/core/spoke/Escrow/reachability.conf
 * @target: src/misc/Auth.sol
 * Was:     function deny(address user) public auth {
 * Now:     the same, plus require(user == msg.sender, NotAuthorized());
 * ──────────────────────────────────────────────────────*/
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
        require(user == msg.sender, NotAuthorized()); // MUTATION: only a ward's own seat can be stripped
        wards[user] = 0;
        emit Deny(user);
    }
}
