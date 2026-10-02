import "Spoke_LinkedSpokeCore_valid_state.spec";

// SP-RC-50: a withdrawal can pay another address and lower the escrowed amount by as much.
rule rcSpWithdrawToAnotherAddressIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");
    require(asset != ghostSrShareToken, "SCOPE: the asset is not the pool's own share token");

    require(amount != 0, "SCOPE: a nonzero withdrawal, not the trivial zero one");

    mathint receiverBefore = ghostERC20Balances128[asset][receiver];
    mathint totalBefore = ghostPeTotal128;

    _Spoke.withdraw(e, poolId, scId, asset, 0, receiver, amount);

    satisfy(ghostERC20Balances128[asset][receiver] == receiverBefore + amount
        && ghostPeTotal128 == totalBefore - amount,
        "a receiver can gain what the escrow loses in one withdrawal");
}

// SP-RC-51: a known asset can be registered again with new decimals under the same asset id.
rule rcSpReRegistrationCanAnnounceNewDecimalsUnderTheSameId(env e, uint16 centrifugeId, address asset,
    uint256 tokenId, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(ghostSrAssetToId128[asset][tokenId] != 0, "SCOPE: the asset is already registered");

    SpokeHarness.AssetId firstId = _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);
    mathint firstDecimals = ghostMsRegisterAssetDecimals8;

    SpokeHarness.AssetId secondId = _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);
    mathint secondDecimals = ghostMsRegisterAssetDecimals8;

    satisfy(firstId == secondId && firstDecimals != secondDecimals,
        "a re-registration can announce new decimals under the same id");
}

// SP-RC-52: a share payout can move share tokens out of escrow while the escrow's books still count them.
rule rcSpSharePayoutDrainsABookedShareTokenRow(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address receiver, uint128 amount) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(ghostPeTokenId256 == 0 && ghostPeAsset == ghostSrShareToken,
        "SCOPE: the escrowed ERC20 is the pool's own share token");
    require(ghostSrAssetToId128[ghostPeAsset][0] != 0, "SCOPE: the share token is also a registered asset");

    address escrowAddress = ghostEfEscrow(ghostPoolA64);
    require(ghostERC20Balances128[ghostPeAsset][escrowAddress] == ghostPeTotal128,
        "SCOPE: the escrow holds exactly the custody it books");

    mathint totalBefore = ghostPeTotal128;

    _Spoke.withdrawShares(e, poolId, scId, receiver, amount);

    satisfy(ghostERC20Balances128[ghostPeAsset][escrowAddress] < ghostPeTotal128
            && ghostPeTotal128 == totalBefore,
        "escrowed share tokens can leave while the books still count them");
}

// SP-RC-53: a ward's rescue to the escrow leaves it holding tokens no holding books.
rule rcSpARescueToTheEscrowLeavesUnbookedTokens(env e, uint256 amount) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(ghostPeTokenId256 == 0, "SCOPE: the escrowed asset is an ERC20 token");

    address escrowAddress = ghostEfEscrow(ghostPoolA64);
    mathint tokensBefore = ghostERC20Balances128[ghostPeAsset][escrowAddress];
    mathint totalBefore = ghostPeTotal128;

    _Spoke.recoverTokens(e, ghostPeAsset, escrowAddress, amount);

    satisfy(ghostERC20Balances128[ghostPeAsset][escrowAddress] > tokensBefore && ghostPeTotal128 == totalBefore,
        "a rescue to the escrow adds tokens its books do not count");
}
