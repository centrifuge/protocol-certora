// Spoke, linked core, rows lane. Setup: the escrow unhooked, so every holding reads free.

// Own setup: the linked core without Escrow_base, whose hooks pin one escrow holding; rules here read any holding.

import "../../Spoke/setup/Spoke_base.spec";
import "../../SpokeRegistry/setup/SpokeRegistry_base.spec";
import "../../SnapshotQueue/setup/SnapshotQueue_single_pool.spec";

using Escrow as _PoolEscrow;

methods {
    function _.deposit(Escrow.ShareClassId scId, address asset, uint256 tokenId, uint128 value) external
        => DISPATCHER(true);
    function _.withdraw(Escrow.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 value) external
        => DISPATCHER(true);
    function _.reserve(Escrow.ShareClassId scId, address asset, uint256 tokenId, uint128 value, address caller, bytes32 reason) external
        => DISPATCHER(true);
    function _.unreserve(Escrow.ShareClassId scId, address asset, uint256 tokenId, uint128 value, address caller, bytes32 reason) external
        => DISPATCHER(true);
    function _.availableBalanceOf(Escrow.ShareClassId scId, address asset, uint256 tokenId) external
        => DISPATCHER(true);
    function _.authTransferTo(address asset, uint256 tokenId, address receiver, uint256 value) external
        => DISPATCHER(true);

    function _PoolEscrow.holding(Escrow.ShareClassId, address, uint256) external returns (uint128, uint128) envfree;
    function _PoolEscrow.reservedBy(Escrow.ShareClassId, address, bytes32, address, uint256) external returns (uint128) envfree;
}

function setupSpokeLinkedSpokeCoreRows(env e) {
    setupSpoke(e);
    setupSpokeRegistry(e);
    setupSnapshotQueue(e);
    require(e.msg.sender != _PoolEscrow, "SAFE: the escrow never calls the spoke");
    require(ghostEfEscrow(ghostPoolA64) == _PoolEscrow, "SCOPE: the modelled pool's escrow is the linked one");
    require(forall address a. forall mathint t.
        ghostSrAssetToId128[a][t] == 0 || VALID_ASSET_SQ(ghostSrAssetToId128[a][t]),
        "SCOPE: every registered asset is a modelled queue asset");
}
