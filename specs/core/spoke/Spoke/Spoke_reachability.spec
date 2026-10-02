import "setup/Spoke_solo.spec";

// SP-RC-01: an unprivileged caller can register a new ERC20 and create its asset id.
rule rcSpRegisterAssetMintsAFreshIdForAnUnknownErc20(env e, uint16 centrifugeId, address asset,
    address refund) {

    setupSpokeValidState(e);
    require(!ghostSrManager[e.msg.sender] && _Spoke.wards[e.msg.sender] != 1,
        "SCOPE: a stranger, neither pool manager nor spoke ward");
    require(ghostSrAssetToId128[asset][0] == 0, "SCOPE: an unregistered token, SP-RC-02 covers a repeat");

    mathint announcedBefore = ghostMsRegisterAssetCount;

    SpokeHarness.AssetId mintedId = _Spoke.registerAsset(e, centrifugeId, asset, 0, refund);

    mathint mintedRaw = mintedId;
    mathint storedAfter = ghostSrAssetToId128[asset][0];
    mathint announcedAfter = ghostMsRegisterAssetCount;

    satisfy(mintedRaw != 0 && storedAfter == mintedRaw && announcedAfter == announcedBefore + 1,
        "an unknown ERC20 can be registered with a fresh id, announced once");
}

// SP-RC-02: re-registering an asset can announce to the hub the id it was first given.
rule rcSpRegisterAssetReannouncesTheStoredIdIsReachable(env e, uint16 centrifugeId, address asset,
    uint256 tokenId, address refund) {

    setupSpokeValidState(e);

    mathint storedBefore = ghostSrAssetToId128[asset][tokenId];
    mathint announcedBefore = ghostMsRegisterAssetCount;

    SpokeHarness.AssetId reportedId = _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);

    mathint reportedRaw = reportedId;
    mathint messageAssetId = ghostMsLastAssetId128;
    mathint announcedAfter = ghostMsRegisterAssetCount;

    satisfy(storedBefore != 0 && reportedRaw == storedBefore && messageAssetId == storedBefore
        && announcedAfter == announcedBefore + 1,
        "a registered asset can be re-announced under its existing id");
}

// SP-RC-03: an ERC6909 token can be registered as an asset and get a fresh id.
rule rcSpRegisterAssetMintsAFreshIdForAnErc6909Tranche(env e, uint16 centrifugeId, address asset,
    uint256 tokenId, address refund) {

    setupSpokeValidState(e);
    require(tokenId != 0, "SCOPE: an ERC6909 token id, SP-RC-01 covers ERC20");
    require(ghostSrAssetToId128[asset][tokenId] == 0, "SCOPE: an unregistered tranche, SP-RC-02 covers a repeat");

    mathint announcedBefore = ghostMsRegisterAssetCount;

    SpokeHarness.AssetId mintedId = _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);

    mathint mintedRaw = mintedId;
    mathint storedAfter = ghostSrAssetToId128[asset][tokenId];
    mathint announcedAfter = ghostMsRegisterAssetCount;

    satisfy(mintedRaw != 0 && storedAfter == mintedRaw && announcedAfter == announcedBefore + 1,
        "an ERC6909 tranche can be registered with a fresh id, announced once");
}

// SP-RC-04: an asset with the maximum allowed decimals can still be registered with the hub.
rule rcSpRegisterAssetAtTheDecimalsCeilingIsReachable(env e, uint16 centrifugeId, address asset,
    uint256 tokenId, address refund) {

    setupSpokeValidState(e);

    mathint announcedBefore = ghostMsRegisterAssetCount;

    _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);

    mathint announcedDecimals = ghostMsRegisterAssetDecimals8;
    mathint announcedAfter = ghostMsRegisterAssetCount;

    satisfy(announcedDecimals == MAX_DECIMALS_CVL() && announcedAfter == announcedBefore + 1,
        "registration can announce an asset of 18 decimals");
}

// SP-RC-05: a first deposit into empty escrow can be fully spendable and queued for the hub.
rule rcSpFirstDepositIntoAnEmptyRowIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.deposit(e, poolId, scId, asset, 0, amount);

    mathint totalAfter = ghostPeTotal128;
    mathint availableAfter = _Spoke.availableBalanceOf(e, poolId, scId, asset, 0);
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;
    bool queuedIncrease = ghostSqFaceLastIsIncrease;

    satisfy(totalAfter == amount && totalAfter > 0 && availableAfter == totalAfter
        && queuedAfter == queuedBefore + 1 && queuedIncrease,
        "a first deposit leaves all of it available and queues one increase");
}

// SP-RC-06: a deposit can top up an escrow balance and queue its amount for the hub.
rule rcSpDepositIntoAHoldingRowIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256,
        "SCOPE: the modelled share class and asset");
    require(ghostPeTotal128 > 0, "SCOPE: a funded holding, SP-RC-05 covers the first deposit");

    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.deposit(e, poolId, scId, asset, tokenId, amount);

    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;
    mathint queuedAmount = ghostSqFaceLastAmount128;
    bool queuedIncrease = ghostSqFaceLastIsIncrease;

    satisfy(totalAfter == totalBefore + amount && totalAfter > totalBefore
        && queuedAfter == queuedBefore + 1 && queuedAmount == amount && queuedIncrease,
        "a top-up can grow a funded holding, queueing an increase of its size");
}

// SP-RC-07: a payer can deposit their entire balance of an asset in one call.
rule rcSpDepositOfThePayersWholeBalanceIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    mathint payerBefore = ghostERC20Balances128[asset][e.msg.sender];
    mathint totalBefore = ghostPeTotal128;

    _Spoke.deposit(e, poolId, scId, asset, 0, amount);

    mathint payerAfter = ghostERC20Balances128[asset][e.msg.sender];
    mathint totalAfter = ghostPeTotal128;

    satisfy(payerBefore > 0 && payerAfter == 0 && totalAfter == totalBefore + payerBefore,
        "a deposit can empty the payer's balance into escrow");
}

// SP-RC-08: an ERC6909 token can be deposited into the pool escrow.
rule rcSpDepositOfAnErc6909TrancheIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256,
        "SCOPE: the modelled share class and asset");

    address escrowAddress = ghostEfEscrow(poolId);
    mathint escrowUnitsBefore = ghostERC6909Balances128[asset][tokenId][escrowAddress];
    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.deposit(e, poolId, scId, asset, tokenId, amount);

    mathint escrowUnitsAfter = ghostERC6909Balances128[asset][tokenId][escrowAddress];
    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;

    satisfy(escrowUnitsAfter == escrowUnitsBefore + amount && escrowUnitsAfter > escrowUnitsBefore
        && totalAfter == totalBefore + amount && queuedAfter == queuedBefore + 1,
        "an ERC6909 tranche can be deposited into the escrow, booked and queued");
}

// SP-RC-09: a deposit can be recorded in the escrow and queued without any token transfer.
rule rcSpNoteDepositCreditsCustodyWithoutMovingTokens(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    address escrowAddress = ghostEfEscrow(poolId);
    mathint escrowTokensBefore = ghostERC20Balances128[asset][escrowAddress];
    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.noteDeposit(e, poolId, scId, asset, 0, amount);

    mathint escrowTokensAfter = ghostERC20Balances128[asset][escrowAddress];
    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;

    satisfy(totalAfter == totalBefore + amount && totalAfter > totalBefore
        && queuedAfter == queuedBefore + 1 && escrowTokensAfter == escrowTokensBefore,
        "a noted deposit can raise custody and queue it, escrow tokens unmoved");
}

// SP-RC-10: a zero-amount deposit can succeed and still queue an update for the hub.
rule rcSpZeroAmountDepositIsReachable(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address asset, uint256 tokenId) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256,
        "SCOPE: the modelled share class and asset");

    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.deposit(e, poolId, scId, asset, tokenId, 0);

    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;
    mathint queuedAmount = ghostSqFaceLastAmount128;

    satisfy(totalAfter == totalBefore && queuedAfter == queuedBefore + 1 && queuedAmount == 0,
        "a zero deposit can succeed, custody unchanged, a zero entry queued");
}

// SP-RC-11: a withdrawal can pay the receiver from escrow and queue a decrease for the hub.
rule rcSpWithdrawPaysTheReceiverIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    mathint receiverBefore = ghostERC20Balances128[asset][receiver];
    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.withdraw(e, poolId, scId, asset, 0, receiver, amount);

    mathint receiverAfter = ghostERC20Balances128[asset][receiver];
    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;
    bool queuedIncrease = ghostSqFaceLastIsIncrease;

    satisfy(totalAfter == totalBefore - amount && totalAfter < totalBefore
        && receiverAfter == receiverBefore + amount && receiverAfter > receiverBefore
        && queuedAfter == queuedBefore + 1 && !queuedIncrease,
        "funds can leave escrow for the receiver with one decrease queued");
}

// SP-RC-12: a withdrawal can empty an escrow balance that has nothing reserved.
rule rcSpWithdrawEmptiesTheFreeBalanceExactlyIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    mathint totalBefore = ghostPeTotal128;

    _Spoke.withdraw(e, poolId, scId, asset, 0, receiver, amount);

    mathint totalAfter = ghostPeTotal128;
    mathint availableAfter = _Spoke.availableBalanceOf(e, poolId, scId, asset, 0);

    satisfy(totalBefore > 0 && totalAfter == 0 && availableAfter == 0, "a withdrawal can empty an unreserved holding");
}

// SP-RC-13: a withdrawal can pay out all unreserved funds while reservations stay intact.
rule rcSpWithdrawLeavesTheHeldPartBehindIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    mathint reservedBefore = ghostPeReserved128;
    mathint totalBefore = ghostPeTotal128;

    _Spoke.withdraw(e, poolId, scId, asset, 0, receiver, amount);

    mathint reservedAfter = ghostPeReserved128;
    mathint totalAfter = ghostPeTotal128;

    satisfy(totalAfter < totalBefore && totalAfter == reservedBefore && reservedAfter == reservedBefore
        && reservedBefore > 0,
        "a withdrawal can take all that is available, leaving only the reserved");
}

// SP-RC-14: a manager can withdraw assets to their own account.
rule rcSpWithdrawToTheCallerThemselvesIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");
    require(receiver == e.msg.sender, "SCOPE: the manager withdraws to their own account");

    mathint receiverBefore = ghostERC20Balances128[asset][receiver];
    mathint totalBefore = ghostPeTotal128;

    _Spoke.withdraw(e, poolId, scId, asset, 0, receiver, amount);

    mathint receiverAfter = ghostERC20Balances128[asset][receiver];
    mathint totalAfter = ghostPeTotal128;

    satisfy(totalAfter < totalBefore && receiverAfter == receiverBefore + amount
        && receiverAfter > receiverBefore,
        "a withdrawal can pay out to the manager who asked for it");
}

// SP-RC-15: a first reservation can hold funds in escrow and queue a decrease for the hub.
rule rcSpFirstHoldOnARowIsReachable(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address asset, uint256 tokenId, uint128 amount, address reserver, bytes32 reason) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256,
        "SCOPE: the modelled share class and asset");

    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint reservedAfter = ghostPeReserved128;
    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;
    bool queuedIncrease = ghostSqFaceLastIsIncrease;

    satisfy(reservedAfter == amount && reservedAfter > 0 && totalAfter == totalBefore
        && queuedAfter == queuedBefore + 1 && !queuedIncrease,
        "a first hold can reserve funds, keep custody and queue one decrease");
}

// SP-RC-16: a reservation can cover the whole escrow balance, leaving nothing spendable.
rule rcSpHoldOnTheWholeFreeBalanceIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256,
        "SCOPE: the modelled share class and asset");
    require(ghostPeReserved128 == 0 && amount == ghostPeTotal128,
        "SCOPE: nothing reserved yet, the hold equals the total");

    mathint totalBefore = ghostPeTotal128;

    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint reservedAfter = ghostPeReserved128;
    mathint totalAfter = ghostPeTotal128;
    mathint availableAfter = _Spoke.availableBalanceOf(e, poolId, scId, asset, tokenId);

    satisfy(totalBefore > 0 && totalAfter == totalBefore && reservedAfter == totalBefore
        && availableAfter == 0,
        "one hold can reserve a whole funded holding, leaving nothing available");
}

// SP-RC-17: a reservation can be released in full, queuing an increase for the hub.
rule rcSpReleaseOfTheWholeHoldIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256,
        "SCOPE: the modelled share class and asset");

    mathint reservedBefore = ghostPeReserved128;
    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.unreserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint reservedAfter = ghostPeReserved128;
    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;
    bool queuedIncrease = ghostSqFaceLastIsIncrease;

    satisfy(reservedBefore > 0 && reservedAfter == 0 && totalAfter == totalBefore
        && queuedAfter == queuedBefore + 1 && queuedIncrease,
        "unreserving everything can queue one increase and keep the total");
}

// SP-RC-18: reserved funds can be paid out in full with no new update queued for the hub.
rule rcSpWithdrawReservedPaysHeldFundsOutIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    mathint reservedBefore = ghostPeReserved128;
    mathint totalBefore = ghostPeTotal128;
    mathint receiverBefore = ghostERC20Balances128[asset][receiver];
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.withdrawReserved(e, poolId, scId, asset, 0, receiver, amount, reserver, reason);

    mathint reservedAfter = ghostPeReserved128;
    mathint totalAfter = ghostPeTotal128;
    mathint receiverAfter = ghostERC20Balances128[asset][receiver];
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;

    satisfy(reservedBefore > 0 && reservedAfter == 0 && totalAfter == totalBefore - reservedBefore
        && receiverAfter > receiverBefore && queuedAfter == queuedBefore,
        "a whole hold can be paid out to a receiver with nothing queued");
}

// SP-RC-19: shares can be issued to an investor, with the issuance queued for the hub.
rule rcSpIssueMintsSharesIsReachable(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address to, uint128 shares) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint receiverBefore = ghostERC20Balances128[share][to];
    mathint supplyBefore = ghostERC20TotalSupply256[share];
    mathint queuedBefore = ghostSqFaceQueueSharesCount;

    _Spoke.issue(e, poolId, scId, to, shares);

    mathint receiverAfter = ghostERC20Balances128[share][to];
    mathint supplyAfter = ghostERC20TotalSupply256[share];
    mathint queuedAfter = ghostSqFaceQueueSharesCount;
    bool queuedIssuance = ghostSqFaceLastIsIssuance;

    satisfy(receiverAfter == receiverBefore + shares && supplyAfter == supplyBefore + shares
        && supplyAfter > supplyBefore && queuedAfter == queuedBefore + 1 && queuedIssuance,
        "an issuance can mint shares to the receiver and queue one issuance");
}

// SP-RC-20: a zero-share issuance can succeed and still queue an update for the hub.
rule rcSpZeroShareIssuanceIsReachable(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address to) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint supplyBefore = ghostERC20TotalSupply256[share];
    mathint queuedBefore = ghostSqFaceQueueSharesCount;

    _Spoke.issue(e, poolId, scId, to, 0);

    mathint supplyAfter = ghostERC20TotalSupply256[share];
    mathint queuedAfter = ghostSqFaceQueueSharesCount;
    mathint queuedShares = ghostSqFaceLastShares128;
    bool queuedIssuance = ghostSqFaceLastIsIssuance;

    satisfy(supplyAfter == supplyBefore && queuedAfter == queuedBefore + 1 && queuedShares == 0
        && queuedIssuance,
        "a zero issuance can mint nothing and still queue a zero issuance");
}

// SP-RC-21: a caller's shares can be revoked and burned, with the decrease queued for the hub.
rule rcSpRevokeBurnsTheCallersSharesIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 shares) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint callerBefore = ghostERC20Balances128[share][e.msg.sender];
    mathint spokeBefore = ghostERC20Balances128[share][_Spoke];
    mathint supplyBefore = ghostERC20TotalSupply256[share];
    mathint queuedBefore = ghostSqFaceQueueSharesCount;

    _Spoke.revoke(e, poolId, scId, shares);

    mathint callerAfter = ghostERC20Balances128[share][e.msg.sender];
    mathint spokeAfter = ghostERC20Balances128[share][_Spoke];
    mathint supplyAfter = ghostERC20TotalSupply256[share];
    mathint queuedAfter = ghostSqFaceQueueSharesCount;
    bool queuedIssuance = ghostSqFaceLastIsIssuance;

    satisfy(callerAfter == callerBefore - shares && callerAfter < callerBefore
        && supplyAfter == supplyBefore - shares && spokeAfter == spokeBefore
        && queuedAfter == queuedBefore + 1 && !queuedIssuance,
        "a revocation can burn the caller's shares and queue one revocation");
}

// SP-RC-22: a pool manager holding every share can revoke the share class's entire supply.
rule rcSpRevokeDownToAnEmptyClassIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 shares) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;

    mathint callerBefore = ghostERC20Balances128[share][e.msg.sender];
    mathint supplyBefore = ghostERC20TotalSupply256[share];

    _Spoke.revoke(e, poolId, scId, shares);

    mathint callerAfter = ghostERC20Balances128[share][e.msg.sender];
    mathint supplyAfter = ghostERC20TotalSupply256[share];

    satisfy(supplyBefore > 0 && callerBefore > 0 && supplyAfter == 0 && callerAfter == 0,
        "a sole holder can revoke a whole share class down to nothing");
}

// SP-RC-23: escrowed shares can go to an investor without minting or reporting to the hub.
rule rcSpWithdrawSharesHandsCustodyOutIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address receiver, uint128 amount) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    address escrowAddress = ghostEfEscrow(poolId);
    mathint receiverBefore = ghostERC20Balances128[share][receiver];
    mathint escrowBefore = ghostERC20Balances128[share][escrowAddress];
    mathint supplyBefore = ghostERC20TotalSupply256[share];
    mathint queuedBefore = ghostSqFaceQueueSharesCount;

    _Spoke.withdrawShares(e, poolId, scId, receiver, amount);

    mathint receiverAfter = ghostERC20Balances128[share][receiver];
    mathint escrowAfter = ghostERC20Balances128[share][escrowAddress];
    mathint supplyAfter = ghostERC20TotalSupply256[share];
    mathint queuedAfter = ghostSqFaceQueueSharesCount;

    satisfy(receiverAfter == receiverBefore + amount && receiverAfter > receiverBefore
        && escrowAfter == escrowBefore - amount && supplyAfter == supplyBefore
        && queuedAfter == queuedBefore,
        "escrowed shares can go to an investor with no mint and nothing queued");
}

// SP-RC-24: a manager can move shares between two holders without changing supply.
rule rcSpTransferSharesFromMovesAHoldingIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address sender_, address from, address to, uint256 amount) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint fromBefore = ghostERC20Balances128[share][from];
    mathint toBefore = ghostERC20Balances128[share][to];
    mathint supplyBefore = ghostERC20TotalSupply256[share];

    _Spoke.transferSharesFrom(e, poolId, scId, sender_, from, to, amount);

    mathint fromAfter = ghostERC20Balances128[share][from];
    mathint toAfter = ghostERC20Balances128[share][to];
    mathint supplyAfter = ghostERC20TotalSupply256[share];

    satisfy(fromAfter == fromBefore - amount && fromAfter < fromBefore
        && toAfter == toBefore + amount && toAfter > toBefore && supplyAfter == supplyBefore,
        "a forced transfer can move shares while supply stays the same");
}

// SP-RC-25: queued asset updates can be sent to the hub for the asset the caller chose.
rule rcSpSubmitQueuedAssetsReportsToTheHubIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, uint128 extraGasLimit, address refund) {

    setupSpokeValidState(e);

    mathint sentBefore = ghostMsSendCount;

    _Spoke.submitQueuedAssets(e, poolId, scId, assetId, extraGasLimit, refund);

    mathint sentAfter = ghostMsSendCount;
    mathint messageKind = ghostMsLastKind;
    mathint messageAssetId = ghostMsLastAssetId128;

    satisfy(sentAfter == sentBefore + 1 && messageKind == MS_UPDATE_ASSETS()
        && messageAssetId == assetId,
        "an asset report can be sent to the hub for the named asset");
}

// SP-RC-26: queued share updates can reach the hub without asking for extra execution gas.
rule rcSpSubmitQueuedSharesWithNoExtraGasIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address refund) {

    setupSpokeValidState(e);

    mathint sentBefore = ghostMsSendCount;

    _Spoke.submitQueuedShares(e, poolId, scId, 0, refund);

    mathint sentAfter = ghostMsSendCount;
    mathint messageKind = ghostMsLastKind;
    mathint messagePool = ghostMsLastPool64;

    satisfy(sentAfter == sentBefore + 1 && messageKind == MS_UPDATE_SHARES()
        && messagePool == poolId,
        "a share report for the pool can be sent with no extra gas");
}

// SP-RC-27: a share owner can bridge their own shares to another network, burning them here.
rule rcSpBridgeDrivenByTheOwnerIsReachable(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);
    require(owner == e.msg.sender, "SCOPE: the owner bridges, SP-RC-28 covers a ward");

    address share = ghostSrShareToken;
    mathint ownerBefore = ghostERC20Balances128[share][owner];
    mathint supplyBefore = ghostERC20TotalSupply256[share];
    mathint bridgedBefore = ghostMsInitiateTransferCount;

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint ownerAfter = ghostERC20Balances128[share][owner];
    mathint supplyAfter = ghostERC20TotalSupply256[share];
    mathint bridgedAfter = ghostMsInitiateTransferCount;
    mathint announcedAmount = ghostMsInitiateTransferAmount128;

    satisfy(ownerAfter == ownerBefore - amount && ownerAfter < ownerBefore
        && supplyAfter == supplyBefore - amount && bridgedAfter == bridgedBefore + 1
        && announcedAmount == amount,
        "an owner can bridge their own shares, burning the amount announced");
}

// SP-RC-28: an admin can bridge shares on an owner's behalf, paid from the owner's balance.
rule rcSpBridgeDrivenByAWardForTheOwnerIsReachable(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);
    require(owner != e.msg.sender, "SCOPE: someone else calls, SP-RC-27 covers the owner");

    address share = ghostSrShareToken;
    mathint ownerBefore = ghostERC20Balances128[share][owner];
    mathint supplyBefore = ghostERC20TotalSupply256[share];
    mathint bridgedBefore = ghostMsInitiateTransferCount;

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint ownerAfter = ghostERC20Balances128[share][owner];
    mathint supplyAfter = ghostERC20TotalSupply256[share];
    mathint bridgedAfter = ghostMsInitiateTransferCount;

    satisfy(ownerAfter == ownerBefore - amount && ownerAfter < ownerBefore
        && supplyAfter == supplyBefore - amount && bridgedAfter == bridgedBefore + 1,
        "a ward can burn and bridge the shares of an owner other than itself");
}

// SP-RC-29: an owner's entire share balance can be bridged to another network at once.
rule rcSpBridgeOfTheWholeHoldingIsReachable(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;

    mathint ownerBefore = ghostERC20Balances128[share][owner];
    mathint bridgedBefore = ghostMsInitiateTransferCount;

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint ownerAfter = ghostERC20Balances128[share][owner];
    mathint bridgedAfter = ghostMsInitiateTransferCount;
    mathint announcedAmount = ghostMsInitiateTransferAmount128;

    satisfy(ownerBefore > 0 && ownerAfter == 0 && announcedAmount == ownerBefore
        && bridgedAfter == bridgedBefore + 1,
        "an owner can bridge their whole holding out in one transfer");
}

// SP-RC-30: a holder can bridge shares with the simplified call and no extra destination gas.
rule rcSpBridgeThroughTheShortEntryPointIsReachable(env e, uint16 centrifugeId,
    SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId, bytes32 receiver, uint128 amount) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint callerBefore = ghostERC20Balances128[share][e.msg.sender];
    mathint bridgedBefore = ghostMsInitiateTransferCount;

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, amount, 0);

    mathint callerAfter = ghostERC20Balances128[share][e.msg.sender];
    mathint bridgedAfter = ghostMsInitiateTransferCount;
    bytes32 announcedReceiver = ghostMsInitiateTransferReceiver;

    satisfy(callerAfter == callerBefore - amount && callerAfter < callerBefore
        && bridgedAfter == bridgedBefore + 1 && announcedReceiver == receiver,
        "the short bridge entry can send the caller's shares with no remote gas");
}

// SP-RC-31: the request manager can relay a paid investor request to the hub.
rule rcSpPaidRequestIsRelayedIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, bytes payload, uint128 extraGasLimit,
    address refund) {

    setupSpokeValidState(e);

    mathint sentBefore = ghostMsSendCount;

    _Spoke.request(e, poolId, scId, assetId, payload, extraGasLimit, false, refund);

    mathint sentAfter = ghostMsSendCount;
    mathint messageKind = ghostMsLastKind;
    mathint messageAssetId = ghostMsLastAssetId128;

    satisfy(sentAfter == sentBefore + 1 && messageKind == MS_REQUEST()
        && messageAssetId == assetId,
        "a paid request can be relayed to the hub for the named asset");
}

// SP-RC-32: the request manager can relay an unpaid investor request to the hub.
rule rcSpUnpaidRequestIsRelayedIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, bytes payload, uint128 extraGasLimit,
    address refund) {

    setupSpokeValidState(e);

    mathint sentBefore = ghostMsSendCount;

    _Spoke.request(e, poolId, scId, assetId, payload, extraGasLimit, true, refund);

    mathint sentAfter = ghostMsSendCount;
    mathint messageKind = ghostMsLastKind;
    mathint messageAssetId = ghostMsLastAssetId128;

    satisfy(sentAfter == sentBefore + 1 && messageKind == MS_REQUEST()
        && messageAssetId == assetId,
        "an unpaid request can be relayed to the hub for the named asset");
}

// SP-RC-33: a caller with no manager or admin rights can send a manager call to the hub.
rule rcSpManagerCallFromAnUnseatedCallerIsReachable(env e, SpokeHarness.PoolId poolId, bytes32 target,
    bytes payload, uint128 extraGasLimit, address refund) {

    setupSpokeValidState(e);
    require(!ghostSrManager[e.msg.sender] && _Spoke.wards[e.msg.sender] != 1,
        "SCOPE: a stranger, neither pool manager nor spoke ward");

    mathint sentBefore = ghostMsSendCount;

    _Spoke.managerCall(e, poolId, target, payload, extraGasLimit, refund);

    mathint sentAfter = ghostMsSendCount;
    mathint messageKind = ghostMsLastKind;
    mathint messagePool = ghostMsLastPool64;

    satisfy(sentAfter == sentBefore + 1 && messageKind == MS_MANAGER_CALL_SPOKE()
        && messagePool == poolId,
        "a stranger can relay a manager call for the pool to the hub");
}

// SP-RC-34: spoke admin rights can be granted and revoked again in the same transaction.
rule rcSpRelyThenDenyRoundTripIsReachable(env e, address user) {

    setupSpokeValidState(e);

    mathint wardBefore = _Spoke.wards[user];

    _Spoke.rely(e, user);

    mathint wardMid = _Spoke.wards[user];

    _Spoke.deny(e, user);

    mathint wardAfter = _Spoke.wards[user];

    satisfy(wardBefore == 0 && wardMid == 1 && wardAfter == 0,
        "an account can gain and lose spoke ward rights back to back");
}

// SP-RC-35: a deposit then an equal withdrawal can restore the escrow balance, queuing both.
rule rcSpDepositThenWithdrawRoundTripIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.deposit(e, poolId, scId, asset, 0, amount);
    _Spoke.withdraw(e, poolId, scId, asset, 0, receiver, amount);

    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;

    satisfy(amount > 0 && totalAfter == totalBefore && queuedAfter == queuedBefore + 2,
        "a same-size deposit and withdrawal can net out yet queue twice");
}

// SP-RC-36: funds can be reserved then paid out, with a single update queued for the hub.
rule rcSpHoldThenPayOutIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.reserve(e, poolId, scId, asset, 0, amount, reserver, reason);
    _Spoke.withdrawReserved(e, poolId, scId, asset, 0, receiver, amount, reserver, reason);

    mathint totalAfter = ghostPeTotal128;
    mathint reservedAfter = ghostPeReserved128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;

    satisfy(amount > 0 && totalAfter == totalBefore - amount
        && reservedAfter == reservedBefore && queuedAfter == queuedBefore + 1,
        "funds can be held and then paid out, the hub told once");
}

// SP-RC-37: shares can be issued into escrow then sent to an investor, queuing one update.
rule rcSpIssueThenWithdrawSharesIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address receiver, uint128 shares) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    address escrowAddress = ghostEfEscrow(poolId);
    mathint receiverBefore = ghostERC20Balances128[share][receiver];
    mathint escrowBefore = ghostERC20Balances128[share][escrowAddress];
    mathint queuedBefore = ghostSqFaceQueueSharesCount;

    _Spoke.issue(e, poolId, scId, escrowAddress, shares);
    _Spoke.withdrawShares(e, poolId, scId, receiver, shares);

    mathint receiverAfter = ghostERC20Balances128[share][receiver];
    mathint escrowAfter = ghostERC20Balances128[share][escrowAddress];
    mathint queuedAfter = ghostSqFaceQueueSharesCount;

    satisfy(receiverAfter == receiverBefore + shares && receiverAfter > receiverBefore
        && escrowAfter == escrowBefore && queuedAfter == queuedBefore + 1,
        "shares can be minted into escrow and handed on, one issuance queued");
}

// SP-RC-38: a deposit can be made and reported to the hub in one transaction.
rule rcSpDepositThenSubmitQueuedAssetsIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint128 amount, SpokeHarness.AssetId assetId,
    uint128 extraGasLimit, address refund) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");
    require(assetId == ghostSrAssetToId128[asset][0], "SCOPE: reports the asset the deposit just queued");

    mathint totalBefore = ghostPeTotal128;
    mathint sentBefore = ghostMsSendCount;

    _Spoke.deposit(e, poolId, scId, asset, 0, amount);
    _Spoke.submitQueuedAssets(e, poolId, scId, assetId, extraGasLimit, refund);

    mathint totalAfter = ghostPeTotal128;
    mathint sentAfter = ghostMsSendCount;
    mathint messageKind = ghostMsLastKind;

    satisfy(totalAfter > totalBefore && sentAfter == sentBefore + 1
        && messageKind == MS_UPDATE_ASSETS(),
        "a deposit and its asset report can go out in one transaction");
}

// SP-RC-39: assets can be reserved and released again, with both changes queued for the hub.
rule rcSpHoldThenReleaseRoundTripIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256,
        "SCOPE: the modelled share class and asset");

    mathint reservedBefore = ghostPeReserved128;
    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);
    _Spoke.unreserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint reservedAfter = ghostPeReserved128;
    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;

    satisfy(amount > 0 && reservedAfter == reservedBefore && totalAfter == totalBefore
        && queuedAfter == queuedBefore + 2,
        "a hold can be placed and lifted, restoring the holding, both queued");
}

// SP-RC-40: an ERC6909 asset can be paid out of the pool escrow to a receiver.
rule rcSpWithdrawOfAnErc6909TrancheIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256,
        "SCOPE: the modelled share class and asset");

    address escrowAddress = ghostEfEscrow(poolId);
    mathint escrowUnitsBefore = ghostERC6909Balances128[asset][tokenId][escrowAddress];
    mathint receiverUnitsBefore = ghostERC6909Balances128[asset][tokenId][receiver];
    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.withdraw(e, poolId, scId, asset, tokenId, receiver, amount);

    mathint escrowUnitsAfter = ghostERC6909Balances128[asset][tokenId][escrowAddress];
    mathint receiverUnitsAfter = ghostERC6909Balances128[asset][tokenId][receiver];
    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;

    satisfy(escrowUnitsAfter == escrowUnitsBefore - amount
        && receiverUnitsAfter == receiverUnitsBefore + amount
        && receiverUnitsAfter > receiverUnitsBefore
        && totalAfter == totalBefore - amount && queuedAfter == queuedBefore + 1,
        "an ERC6909 tranche can be paid out to a receiver and queued");
}

// SP-RC-41: an admin can point the spoke at a different gateway.
rule rcSpFileRepointsTheGatewayIsReachable(env e, address data) {

    setupSpokeValidState(e);

    address gatewayBefore = _Spoke.gateway;

    _Spoke.file(e, FILE_GATEWAY_SP_CVL(), data);

    address gatewayAfter = _Spoke.gateway;

    satisfy(data != 0 && gatewayBefore != data && gatewayAfter == data,
        "the gateway can be repointed to a different nonzero address");
}

// SP-RC-42: an admin can replace the spoke's outbound message sender.
rule rcSpFileRepointsTheMessageSenderIsReachable(env e, address data) {

    setupSpokeValidState(e);

    address messageSenderBefore = _Spoke.sender;

    _Spoke.file(e, FILE_SENDER_SP_CVL(), data);

    address messageSenderAfter = _Spoke.sender;

    satisfy(data != 0 && messageSenderBefore != data && messageSenderAfter == data,
        "the message sender can be repointed to a different nonzero address");
}

// SP-RC-43: a pool can reserve more assets than its escrow currently holds.
rule rcSpHoldBeyondTheRowsCustodyIsReachable(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && tokenId == ghostPeTokenId256,
        "SCOPE: the modelled share class and asset");
    require(ghostPeReserved128 == 0 && amount > ghostPeTotal128,
        "SCOPE: nothing reserved yet, the hold exceeds the total");

    mathint totalBefore = ghostPeTotal128;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint reservedAfter = ghostPeReserved128;
    mathint totalAfter = ghostPeTotal128;
    mathint queuedAfter = ghostSqFaceQueueAssetsCount;
    bool queuedIncrease = ghostSqFaceLastIsIncrease;

    satisfy(reservedAfter > totalAfter && totalAfter == totalBefore
        && queuedAfter == queuedBefore + 1 && !queuedIncrease,
        "a hold can exceed the escrowed total, queueing one decrease");
}

// SP-RC-44: an admin can make the gateway an admin, which can then reconfigure the spoke.
rule rcSpAWardCanSeatTheGatewayOnTheWardRoll(env e1, env e2, address x) {

    setupSpokeValidState(e1);
    setupEnv(e2);

    address gatewayBefore = _Spoke.gateway;
    require(e2.msg.sender == gatewayBefore && x != _Spoke.sender,
        "SCOPE: the gateway then repoints the message sender");

    _Spoke.rely(e1, gatewayBefore);
    _Spoke.file(e2, FILE_SENDER_SP_CVL(), x);

    mathint gatewayWardAfter = _Spoke.wards[gatewayBefore];
    address messageSenderAfter = _Spoke.sender;

    satisfy(gatewayWardAfter == 1 && messageSenderAfter == x,
        "the gateway, once made a ward, can repoint the message sender");
}

// SP-RC-45: an admin can set the spoke's gateway to the zero address.
rule rcSpFileAcceptsTheNullAddress(env e) {

    setupSpokeValidState(e);

    address nullAddress = 0;

    _Spoke.file(e, FILE_GATEWAY_SP_CVL(), nullAddress);

    address gatewayAfter = _Spoke.gateway;

    satisfy(gatewayAfter == 0, "the gateway can be cleared to zero");
}

// SP-RC-46: an owner can bridge shares to a receiver that is not a valid address, burning them here.
rule rcSpBridgeToAnUndeliverableReceiverBurnsAndAnnounces(env e, uint16 centrifugeId,
    SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner,
    uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);
    require(owner == e.msg.sender, "SCOPE: the owner bridges their own shares");
    require((receiver << 160) != to_bytes32(0), "SCOPE: a receiver the destination refuses");

    address share = ghostSrShareToken;
    mathint supplyBefore = ghostERC20TotalSupply256[share];
    mathint bridgedBefore = ghostMsInitiateTransferCount;

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint supplyAfter = ghostERC20TotalSupply256[share];
    mathint bridgedAfter = ghostMsInitiateTransferCount;
    bytes32 announcedReceiver = ghostMsInitiateTransferReceiver;

    satisfy(amount > 0 && supplyAfter == supplyBefore - amount
        && bridgedAfter == bridgedBefore + 1 && announcedReceiver == receiver,
        "shares burn and a transfer is announced to that receiver");
}

// SP-RC-47: a non-admin share owner can bridge naming a sender who is neither the caller nor the owner.
rule rcSpBridgeAnnouncesASenderNeitherCallerNorOwner(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);
    require(owner == e.msg.sender && _Spoke.wards[e.msg.sender] == 0,
        "SCOPE: a plain bridger drives the transfer for themselves");
    require(sender_ != e.msg.sender, "SCOPE: the named sender is a third party to the call");

    mathint bridgedBefore = ghostMsInitiateTransferCount;

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint bridgedAfter = ghostMsInitiateTransferCount;
    bytes32 announcedSender = ghostMsLastSenderWord;

    satisfy(bridgedAfter == bridgedBefore + 1 && announcedSender == to_bytes32(sender_) << 96,
        "a bridge announces a sender the call never authenticated");
}

// SP-RC-48: an asset with zero decimals can be registered and announced to the hub.
rule rcSpRegisterAssetAtZeroDecimalsIsReachable(env e, uint16 centrifugeId, address asset,
    uint256 tokenId, address refund) {

    setupSpokeValidState(e);

    mathint announcedBefore = ghostMsRegisterAssetCount;

    _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);

    mathint announcedDecimals = ghostMsRegisterAssetDecimals8;
    mathint announcedAfter = ghostMsRegisterAssetCount;

    satisfy(announcedDecimals == 0 && announcedAfter == announcedBefore + 1,
        "registration can announce an asset of 0 decimals");
}

// SP-RC-49: a batching account can relay a request when the gateway is the request manager.
rule rcSpBatchedRequestPassesTheGateWhenTheGatewayIsTheRequestManagerIsReachable(env e,
    SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, bytes payload,
    uint128 extraGasLimit, bool unpaid, address refund) {

    setupSpokeSoloAnyTransient(e);
    require(ghostSrRequestManager == _Spoke.gateway, "SCOPE: the gateway is the pool's request manager");
    require(spInBatchCVL(e), "SCOPE: the call arrives from inside a gateway batch");

    address resolved = spResolvedSenderCVL(e);
    mathint sentBefore = ghostMsSendCount;

    _Spoke.request(e, poolId, scId, assetId, payload, extraGasLimit, unpaid, refund);

    mathint sentAfter = ghostMsSendCount;
    mathint messageKind = ghostMsLastKind;

    satisfy(sentAfter == sentBefore + 1 && messageKind == MS_REQUEST() && resolved != _Spoke.gateway,
        "a batched caller who is not the request manager gets a request relayed");
}
