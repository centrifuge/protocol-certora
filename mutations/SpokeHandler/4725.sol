/* ── MUTATION SpokeHandler #4725 ──────────────────────────────────
 * @desc:   rely loses its ward gate in the shared Auth mixin, so authority over the handler is handed on by an account that never held it.
 * @rules:  rvShRelyRefusesANonWard
 * @conf:   certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf
 * @target: src/misc/Auth.sol
 * Was:     function rely(address user) public auth {
 * Now:     function rely(address user) public { // MUTATION: the ward gate is gone
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
    function rely(address user) public { // MUTATION: the ward gate is gone
        wards[user] = 1;
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public auth {
        wards[user] = 0;
        emit Deny(user);
    }
}
