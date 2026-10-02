/* ── MUTATION HubRegistry #6420 ──────────────────────────
 * @desc:   rely clears the ward slot instead of setting it, so authority can never be handed to an account that holds none.
 * @rules:  rcHrAuthorityRoundTripIsReachable
 * @conf:   certora/confs/core/hub/HubRegistry/single_pool_reachability.conf
 * @target: src/misc/Auth.sol
 * Was:     wards[user] = 1;
 * Now:     wards[user] = 0; // MUTATION: the grant clears the ward instead of setting it
 * ──────────────────────────────────────────────────*/
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
        wards[user] = 0; // MUTATION: the grant clears the ward instead of setting it
        emit Rely(user);
    }

    /// @inheritdoc IAuth
    function deny(address user) public auth {
        wards[user] = 0;
        emit Deny(user);
    }
}
