// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {Escrow} from "../../src/core/spoke/Escrow.sol";
import {PoolId} from "../../src/core/types/PoolId.sol";
import {EscrowFactory} from "../../src/core/spoke/factories/EscrowFactory.sol";

// The parametric surface for the EscrowFactory scene, plus a linked escrow the conf binds.
contract EscrowFactoryHarness is EscrowFactory {
    // Scene escrow bound by conf linking, so its calls resolve to real bytecode statically.
    Escrow public escrowLink;

    constructor(address root_, address deployer) EscrowFactory(root_, deployer) {}

    // newEscrow twin against the linked child: a fresh create2 address resolves statically to
    // nothing, so the ward wiring a real newEscrow performs cannot be observed on that entry point.
    // PEF-AC-03 reads the child's ward roll on this entry; every parametric PEF rule takes it as f.
    function newEscrowLinked(PoolId poolId_) external auth {
        poolId[address(escrowLink)] = poolId_;

        escrowLink.rely(root);
        escrowLink.rely(spoke);

        escrowLink.deny(address(this));
    }
}
