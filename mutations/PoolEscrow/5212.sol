/* ── MUTATION PoolEscrow #5212 ────────────────────────────
 * @desc:   deny refuses to remove the caller itself, so a ward can no longer step down.
 * @rules:  rvPeDenyAlwaysAdmitsAWardStandingItselfDown
 * @conf:   certora/confs/core/spoke/Escrow/reverts.conf
 * @target: src/misc/Auth.sol
 * Was:     function deny(address user) public auth {
 * Now:     the same, plus require(user != msg.sender, NotAuthorized());
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
        require(user != msg.sender, NotAuthorized()); // MUTATION: the ward roll refuses to remove the caller's own seat
        wards[user] = 0;
        emit Deny(user);
    }
}
