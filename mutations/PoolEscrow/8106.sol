/* ── MUTATION PoolEscrow #8106 ────────────────────────────────
 * @desc:   recoverTokens pays a plain token back to the escrow itself instead of the named receiver, so an ERC20 recovery moves nothing out of custody.
 * @rules:  rcPeRecoverTokensMovesCustodyWithoutTheLedger
 * @conf:   certora/confs/core/spoke/Escrow/custody_properties.conf
 * @target: src/misc/Recoverable.sol
 * Was:     SafeTransferLib.safeTransfer(token, receiver, amount);
 * Now:     SafeTransferLib.safeTransfer(token, address(this), amount);
 * ────────────────────────────────────────────────────────────────*/
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
            SafeTransferLib.safeTransfer(token, address(this), amount); // MUTATION: the plain token leg pays the escrow itself
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
