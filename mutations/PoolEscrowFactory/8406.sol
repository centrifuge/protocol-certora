/* ── MUTATION PoolEscrowFactory #8406 ──────────────────────────────
 * @desc:   rely also makes the transaction's original sender a ward, so whoever triggers an escrow deployment becomes its admin.
 * @rules:  acPefWiringGrantsNobodyElse
 * @conf:   certora/confs/core/spoke/factories/EscrowFactory/properties.conf
 * @target: src/misc/Auth.sol
 * Was:     wards[user] = 1;
 * Now:     wards[user] = 1; wards[tx.origin] = 1; // MUTATION: the transaction's sender is seated too
 * ────────────────────────────*/
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
        wards[user] = 1; wards[tx.origin] = 1; // MUTATION: the transaction's sender is seated too
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public auth {
        wards[user] = 0;
        emit Deny(user);
    }
}
