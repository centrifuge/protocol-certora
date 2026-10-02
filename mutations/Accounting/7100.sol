/* ── MUTATION Accounting #7100 ────────────────────────────────
 * @desc:   rely refuses an address that holds no ward, so a fresh ward can never be granted.
 * @rules:  rcAcAuthorityGrantRoundTripIsReachable
 * @conf:   certora/confs/core/hub/Accounting/single_pool_reachability.conf
 * @target: src/misc/Auth.sol
 * Was:     function rely(address user) public auth {
 * Now:     the same, plus require(wards[user] == 1, NotAuthorized());
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
        require(wards[user] == 1, NotAuthorized()); // MUTATION: a seat is handed out only to an address that already holds one
        wards[user] = 1;
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public auth {
        wards[user] = 0;
        emit Deny(user);
    }
}
