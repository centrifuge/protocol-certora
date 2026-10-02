// Spoke, linked core, multi-pool lane. Setup: a second linked escrow for another pool.

// Own setup: EscrowTwin as a second pool's escrow, which only this setup links; rows_base links one pool.

import "Spoke_LinkedSpokeCore_rows_base.spec";

using EscrowTwin as _PoolEscrowB;

methods {
    function _PoolEscrowB.holding(Escrow.ShareClassId, address, uint256) external returns (uint128, uint128) envfree;
    function _PoolEscrowB.reservedBy(Escrow.ShareClassId, address, bytes32, address, uint256) external returns (uint128) envfree;
}

function setupSpokeLinkedSpokeCoreTwoEscrows(env e, uint64 otherPool) {
    setupSpokeLinkedSpokeCoreRows(e);
    require(e.msg.sender != _PoolEscrowB, "SAFE: an escrow never calls the spoke");
    require(otherPool != ghostPoolA64 && ghostEfEscrow(otherPool) == _PoolEscrowB,
        "SCOPE: another pool, its escrow the second linked one");
}
