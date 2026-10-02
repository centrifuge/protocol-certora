// Spoke, linked core. Setup: the spoke with its registry, queue and escrow.

import "../../Spoke/setup/Spoke_base.spec";
import "../../SpokeRegistry/setup/SpokeRegistry_base.spec";
import "../../SnapshotQueue/setup/SnapshotQueue_single_pool.spec";
import "../../Escrow/setup/Escrow_base.spec";

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
}

function setupSpokeLinkedSpokeCore(env e) {
    setupSpoke(e);
    setupSpokeRegistry(e);
    setupSnapshotQueue(e);
    setupPoolEscrow(e);
    require(ghostEfEscrow(ghostPoolA64) == _PoolEscrow, "SCOPE: the modelled pool's escrow is the linked one");
    require(forall address a. forall mathint t.
        ghostSrAssetToId128[a][t] == 0 || VALID_ASSET_SQ(ghostSrAssetToId128[a][t]),
        "SCOPE: every registered asset is a modelled queue asset");
}

definition RECOVER_TOKENS_SP(method f) returns bool =
    f.selector == sig:_Spoke.recoverTokens(address,address,uint256).selector
    || f.selector == sig:_Spoke.recoverTokens(address,uint256,address,uint256).selector;

// SCOPE: a deposit note books with no token move; a withdrawal's law binds its receiver argument.
definition NOTE_OR_WITHDRAWAL_SP(method f) returns bool =
    f.selector == sig:_Spoke.noteDeposit(SpokeHarness.PoolId, SpokeHarness.ShareClassId, address, uint256,
        uint128).selector
    || f.selector == sig:_Spoke.noteDepositCounted(SpokeHarness.PoolId, SpokeHarness.ShareClassId, address, uint256,
        uint128).selector
    || f.selector == sig:_Spoke.withdraw(SpokeHarness.PoolId, SpokeHarness.ShareClassId, address, uint256, address,
        uint128).selector
    || f.selector == sig:_Spoke.withdrawReserved(SpokeHarness.PoolId, SpokeHarness.ShareClassId, address, uint256,
        address, uint128, address, bytes32).selector;
