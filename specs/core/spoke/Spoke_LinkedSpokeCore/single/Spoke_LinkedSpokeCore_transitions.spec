import "Spoke_LinkedSpokeCore_valid_state.spec";

// --- variable_transitions ---

// SP-VT-07: no spoke call moves the share price, an asset price or the time either was last set.
rule vtSpNoSpokeEntryMovesAPrice(env e, method f, calldataarg args, uint128 aid)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeLinkedSpokeCoreValidState(e);

    mathint sharePriceBefore = ghostSrPricePoolPerShare128;
    mathint sharePriceAtBefore = ghostSrPricePoolPerShareComputedAt64;
    mathint assetPriceBefore = ghostSrPricePoolPerAsset128[aid];
    mathint assetPriceAtBefore = ghostSrPricePoolPerAssetComputedAt64[aid];

    f(e, args);

    mathint sharePriceAfter = ghostSrPricePoolPerShare128;
    mathint sharePriceAtAfter = ghostSrPricePoolPerShareComputedAt64;
    mathint assetPriceAfter = ghostSrPricePoolPerAsset128[aid];
    mathint assetPriceAtAfter = ghostSrPricePoolPerAssetComputedAt64[aid];

    assert(sharePriceAfter == sharePriceBefore && sharePriceAtAfter == sharePriceAtBefore
            && assetPriceAfter == assetPriceBefore && assetPriceAtAfter == assetPriceAtBefore,
        "prices and their timestamps stay as they were");
}

// --- state_transitions ---

// SP-ST-02: each change in unreserved escrow assets is queued for the hub as an equal change.
rule stSpSpendableBalanceMoveIsQueuedForTheHub(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeLinkedSpokeCoreValidState(e);

    uint128 aid = ghostSrAssetToId128[ghostPeAsset][ghostPeTokenId256];
    require(VALID_ASSET_SQ(aid), "SCOPE: the escrowed asset is a modelled queue asset");

    mathint availableBefore = ghostPeTotal128 - ghostPeReserved128;
    mathint depositsBefore = ghostSqDeposits128[aid];
    mathint withdrawalsBefore = ghostSqWithdrawals128[aid];

    f(e, args);

    mathint availableDelta = (ghostPeTotal128 - ghostPeReserved128) - availableBefore;
    mathint queuedDelta = (ghostSqDeposits128[aid] - depositsBefore)
        - (ghostSqWithdrawals128[aid] - withdrawalsBefore);

    assert(availableDelta != 0 => queuedDelta == availableDelta,
        "a change in the unreserved escrow balance is queued at its signed size");
}

// SP-ST-03: emptying an asset's queued flow uses one sequence number and dequeues the asset.
rule stSpDrainingAQueueRowSpendsANonceAndItsSlot(env e, method f, calldataarg args, uint128 aid)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeLinkedSpokeCoreValidState(e);

    mathint depositsBefore = ghostSqDeposits128[aid];
    mathint withdrawalsBefore = ghostSqWithdrawals128[aid];
    mathint nonceBefore = ghostSqNonce64;
    mathint counterBefore = ghostSqQueuedAssetCounter32;

    f(e, args);

    assert((depositsBefore != 0 || withdrawalsBefore != 0)
            && ghostSqDeposits128[aid] == 0 && ghostSqWithdrawals128[aid] == 0
        => (ghostSqNonce64 == nonceBefore + 1 && ghostSqQueuedAssetCounter32 == counterBefore - 1),
        "draining an asset queue spends one nonce, waiting count down by one");
}

// SP-ST-04: outside hub submissions and share bridging, every share supply change is queued.
rule stSpShareSupplyMovesOnlyAsReported(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeLinkedSpokeCoreValidState(e);

    address token = ghostSrShareToken;
    mathint supplyBefore = ghostERC20TotalSupply256[token];
    mathint signedBefore = ghostSqIsPositive ? ghostSqDelta128 : -ghostSqDelta128;
    mathint nonceBefore = ghostSqNonce64;
    mathint bridgedBefore = ghostMsInitiateTransferCount;

    f(e, args);

    mathint signedAfter = ghostSqIsPositive ? ghostSqDelta128 : -ghostSqDelta128;

    // SCOPE: the class must hold a share token.
    assert(token != 0 && ghostSqNonce64 == nonceBefore && ghostMsInitiateTransferCount == bridgedBefore
        => ghostERC20TotalSupply256[token] - supplyBefore == signedAfter - signedBefore,
        "a class token's supply tracks the queued net, bar flushes and bridges");
}

// SP-ST-05: except withdrawals and noted deposits, escrow tokens and booked assets change equally.
// SCOPE: fee-on-transfer and rebasing tokens are not modelled.
// SCOPE: a ward's rescue to the escrow adds tokens nobody books, as a plain transfer does (hl_layer_handoff.md).
rule stSpEscrowCustodyMovesWithItsTokens(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(ghostPeTokenId256 == 0, "SCOPE: the escrowed asset is an ERC20 token");
    require(ghostPeAsset != ghostSrShareToken, "SCOPE: the asset is not the pool's own share token");

    address escrowAddress = ghostEfEscrow(ghostPoolA64);
    mathint tokensBefore = ghostERC20Balances128[ghostPeAsset][escrowAddress];
    mathint totalBefore = ghostPeTotal128;

    f(e, args);

    mathint tokenMove = ghostERC20Balances128[ghostPeAsset][escrowAddress] - tokensBefore;
    mathint bookMove = ghostPeTotal128 - totalBefore;

    assert(tokenMove != bookMove => NOTE_OR_WITHDRAWAL_SP(f) || RECOVER_TOKENS_SP(f),
        "bar deposit notes, withdrawals and a rescue, escrow tokens and book move alike");
    assert(RECOVER_TOKENS_SP(f) => bookMove == 0 && tokenMove >= 0, "a rescue only adds unbooked tokens");
}
