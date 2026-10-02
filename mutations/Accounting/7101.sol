/* ── MUTATION Accounting #7101 ────────────────────────────────
 * @desc:   deny refuses a caller naming its own address, so a ward can never revoke its own rights.
 * @rules:  rcAcWardRevokesItselfIsReachable
 * @conf:   certora/confs/core/hub/Accounting/single_pool_reachability.conf
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
        require(user != msg.sender, NotAuthorized()); // MUTATION: the caller's own seat is out of reach of a revocation
        wards[user] = 0;
        emit Deny(user);
    }
}
