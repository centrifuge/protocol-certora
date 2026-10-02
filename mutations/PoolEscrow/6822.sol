/* ── MUTATION PoolEscrow #6822 ────────────────────────────────
 * @desc:   the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.
 * @rules:  rvPeDepositRefusesANonWard, rvPeReserveRefusesANonWard, rvPeRelyRefusesANonWard
 * @conf:   certora/confs/core/spoke/Escrow/reverts.conf
 * @target: src/misc/Auth.sol
 * Was:     require(wards[msg.sender] == 1, NotAuthorized());
 * Now:     (removed)
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
        // MUTATION: the shared ward gate no longer looks at the caller
        _;
    }

    /// @inheritdoc IAuth
    function rely(address user) public auth {
        wards[user] = 1;
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public auth {
        wards[user] = 0;
        emit Deny(user);
    }
}
