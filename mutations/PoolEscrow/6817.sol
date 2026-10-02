/* ── MUTATION PoolEscrow #6817 ────────────────────────
 * @desc:   rely refuses any account not already a ward, so no new account can ever be granted a seat.
 * @rules:  rcPeFreshlyReliedAccountBooksADeposit
 * @conf:   certora/confs/core/spoke/Escrow/reachability.conf
 * @target: src/misc/Auth.sol
 * Was:     function rely(address user) public auth {
 * Now:     the same, plus require(wards[user] == 1, NotAuthorized());
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
        require(wards[user] == 1, NotAuthorized()); // MUTATION: the roll only reaffirms a seat an account already holds
        wards[user] = 1;
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public auth {
        wards[user] = 0;
        emit Deny(user);
    }
}
