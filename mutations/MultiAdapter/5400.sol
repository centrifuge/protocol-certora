/* ── MUTATION MultiAdapter #5400 ────────────────────────────────
 * @desc:   The ward gate no longer checks the caller, so any account can rewire routes, appoint managers and send messages.
 * @rules:  acMaOnlyWardMovesTheWardSet, acMaOnlyWardModifiesManagerRights, acMaOnlyWardRepointsTheGateway, acMaOnlyWardRepointsTheParser, acMaOnlyWardFansOutASend, acMaOnlyWardRepointsTheMessageGas
 * @conf:   certora/confs/core/messaging/MultiAdapter/access_control.conf
 * @target: src/misc/Auth.sol
 * Was:     require(wards[msg.sender] == 1, NotAuthorized());
 * Now:     // MUTATION: the ward gate no longer looks at the caller
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
        // MUTATION: the ward gate no longer looks at the caller
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
