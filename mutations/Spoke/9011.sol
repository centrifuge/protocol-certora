/* ── MUTATION Spoke #9011 ──────────────────────────────
 * @desc:   An ERC20 token rescue transfers a zero amount, so rescued tokens never leave the contract.
 * @rules:  rcSpARescueToTheEscrowLeavesUnbookedTokens
 * @conf:   certora/confs/core/spoke/Spoke_LinkedSpokeCore/reachability.conf
 * @target: src/misc/Recoverable.sol
 * Was:     SafeTransferLib.safeTransfer(token, receiver, amount);
 * Now:     SafeTransferLib.safeTransfer(token, receiver, 0); // MUTATION: the rescue forwards nothing
 * ────────────────────────────────────────────────────────────────────*/
// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity 0.8.28;

import {Auth} from "./Auth.sol";
import {SafeTransferLib} from "./libraries/SafeTransferLib.sol";
import {IERC6909, TransferFailed} from "./interfaces/IERC6909.sol";
import {IRecoverable, ETH_ADDRESS} from "./interfaces/IRecoverable.sol";

/// @title  Recoverable
/// @notice Abstract contract that provides emergency token recovery functionality, allowing authorized parties
///         to retrieve accidentally sent ETH, ERC20, or ERC6909 tokens from the contract to a specified
///         receiver address.
abstract contract Recoverable is Auth, IRecoverable {
    /// @inheritdoc IRecoverable
    function recoverTokens(address token, address receiver, uint256 amount) public auth {
        if (token == ETH_ADDRESS) {
            SafeTransferLib.safeTransferETH(receiver, amount);
        } else {
            SafeTransferLib.safeTransfer(token, receiver, 0); // MUTATION: the rescue forwards nothing
        }
    }

    /// @inheritdoc IRecoverable
    function recoverTokens(address token, uint256 tokenId, address receiver, uint256 amount) external auth {
        if (tokenId == 0) {
            recoverTokens(token, receiver, amount);
        } else {
            require(IERC6909(token).transfer(receiver, tokenId, amount), TransferFailed());
        }
    }
}
