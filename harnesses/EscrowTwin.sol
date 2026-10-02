// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {Escrow} from "../../src/core/spoke/Escrow.sol";
import {PoolId} from "../../src/core/types/PoolId.sol";

// A second Escrow, so a scene can hold another pool's escrow beside its own.
contract EscrowTwin is Escrow {
    constructor(PoolId poolId_, address deployer) Escrow(poolId_, deployer) {}
}
