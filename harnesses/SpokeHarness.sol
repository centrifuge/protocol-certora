// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {Spoke} from "../../src/core/spoke/Spoke.sol";
import {PoolId} from "../../src/core/types/PoolId.sol";
import {ShareClassId} from "../../src/core/types/ShareClassId.sol";
import {IGateway} from "../../src/core/messaging/interfaces/IGateway.sol";
import {ISnapshotQueue} from "../../src/core/spoke/interfaces/ISnapshotQueue.sol";
import {ISpokeRegistry} from "../../src/core/spoke/interfaces/ISpokeRegistry.sol";
import {IEscrowProvider} from "../../src/core/spoke/factories/interfaces/IEscrowFactory.sol";

// Spoke plus the one counter SP-VS-06 needs: custody booked without a transfer behind it.
contract SpokeHarness is Spoke {
    // No storage hook can see this: noteDeposit and deposit write the same holding.total.
    uint128 public notedWithoutTransfer;

    constructor(
        IGateway gateway_,
        ISnapshotQueue queues_,
        ISpokeRegistry spokeRegistry_,
        IEscrowProvider escrowProvider_,
        address deployer
    ) Spoke(gateway_, queues_, spokeRegistry_, escrowProvider_, deployer) {}

    // noteDeposit twin: the original is external and not virtual, so it cannot be overridden.
    function noteDepositCounted(PoolId poolId, ShareClassId scId, address asset, uint256 tokenId, uint128 amount)
        external
        payable
        enforced(poolId)
    {
        notedWithoutTransfer += amount;

        escrow(poolId).deposit(scId, asset, tokenId, amount);
        _queueAssets(poolId, scId, asset, tokenId, amount, true);
    }
}
