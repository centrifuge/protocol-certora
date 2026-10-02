import "../setup/Spoke_LinkedSpokeCore_base.spec";
import "../../Escrow/single/Escrow_valid_state.spec";

methods {
    function _Spoke.notedWithoutTransfer() external returns (uint128) envfree;
}

function setupSpokeLinkedSpokeCoreValidState(env e) {
    setupSpokeLinkedSpokeCore(e);
    requirePoolEscrowInvariants(e);
    assumeQueuedAssetCounterMatchesCardinality();
    assumeManagerImpliesActivePool();
    assumeAssetReverseResolvesBack();
    assumeNullAssetNeverRegistered();
}

function SETUP_SP_VS(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupSpokeLinkedSpokeCoreValidState(e);
}

// SP-VS-01: every asset with a queued flow is a registered asset.
invariant queuedAssetRowImpliesRegisteredAsset(env e)
    forall uint128 aid. (ghostSqDeposits128[aid] != 0 || ghostSqWithdrawals128[aid] != 0)
        => ghostSrIdToAssetAsset[aid] != 0
filtered { f -> !EXCLUDED_FUNCTION_SP(f) } { preserved with (env eFunc) { SETUP_SP_VS(e, eFunc); } }

// SP-VS-02: the escrow holds or reserves only registered assets.
invariant escrowedRowImpliesRegisteredAsset(env e)
    (ghostPeTotal128 != 0 || ghostPeReserved128 != 0)
        => ghostSrAssetToId128[ghostPeAsset][ghostPeTokenId256] != 0
filtered { f -> !EXCLUDED_FUNCTION_SP(f) } { preserved with (env eFunc) { SETUP_SP_VS(e, eFunc); } }

// SP-VS-03: the escrow holds or reserves funds only for a pool the spoke has created.
invariant escrowedCustodyImpliesCreatedPool(env e)
    (ghostPeTotal128 != 0 || ghostPeReserved128 != 0) => ghostSrCreatedAt64 != 0
filtered { f -> !EXCLUDED_FUNCTION_SP(f) } { preserved with (env eFunc) { SETUP_SP_VS(e, eFunc); } }

// SP-VS-04: updates are queued for the hub only for a pool the spoke has created.
invariant queueActivityImpliesCreatedPool(env e)
    (ghostSqDelta128 != 0 || ghostSqNonce64 != 0 || ghostSqQueuedAssetCounter32 != 0
        || SQ_QUEUED_ASSET_CARDINALITY() != 0) => ghostSrCreatedAt64 != 0
filtered { f -> !EXCLUDED_FUNCTION_SP(f) } { preserved with (env eFunc) { SETUP_SP_VS(e, eFunc); } }

// SP-VS-05: every asset id registered on a spoke encodes that spoke's own network.
invariant registeredAssetIsLocal(env e)
    forall uint128 aid. ghostSrIdToAssetAsset[aid] != 0
        => aid / 2^112 == ghostMsLocalCentrifugeId16
filtered { f -> !EXCLUDED_FUNCTION_SP(f) } { preserved with (env eFunc) { SETUP_SP_VS(e, eFunc); } }

// SP-VS-06: the escrow's tokens plus noted deposits always cover the assets on its books.
// SAFE: noteDeposit runs as its harness copy noteDepositCounted, which only adds a counter.
invariant escrowCustodyIsBackedOrNoted(env e)
    ghostERC20Balances128[ghostPeAsset][_PoolEscrow] + notedWithoutTransfer() >= ghostPeTotal128
filtered { f -> !EXCLUDED_FUNCTION_SP(f) && f.selector != sig:_Spoke.noteDeposit(SpokeHarness.PoolId,SpokeHarness.ShareClassId,address,uint256,uint128).selector }
{ preserved with (env eFunc) {
    SETUP_SP_VS(e, eFunc);
    require(ghostPeTokenId256 == 0, "SCOPE: the escrowed asset is an ERC20 token");
    require(ghostPeAsset != ghostSrShareToken, "SCOPE: the asset is not the pool's own share token");
} }
