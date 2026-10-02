import "Spoke_LinkedSpokeCore_valid_state.spec";

// SP-HL-29: a deposit then an equal withdrawal leaves the escrowed amount unchanged.
rule hlSpDepositThenWithdrawRestoresCustody(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");

    mathint totalBefore = ghostPeTotal128;

    _Spoke.deposit(e, poolId, scId, asset, tokenId, amount);
    _Spoke.withdraw(e, poolId, scId, asset, tokenId, receiver, amount);

    mathint totalAfter = ghostPeTotal128;

    assert(totalAfter == totalBefore, "a deposit and an equal withdrawal restore custody");
}

// SP-HL-30: a deposit then an equal withdrawal nets to zero in the hub's pending report.
rule hlSpDepositThenWithdrawRestoresTheQueuedNet(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");
    uint128 aid = ghostSrAssetToId128[ghostPeAsset][ghostPeTokenId256];

    mathint netBefore = ghostSqDeposits128[aid] - ghostSqWithdrawals128[aid];

    _Spoke.deposit(e, poolId, scId, asset, tokenId, amount);
    _Spoke.withdraw(e, poolId, scId, asset, tokenId, receiver, amount);

    mathint netAfter = ghostSqDeposits128[aid] - ghostSqWithdrawals128[aid];

    assert(netAfter == netBefore, "a deposit and an equal withdrawal restore the asset's queued net");
}

// SP-HL-31: reserving then unreserving an amount leaves the escrowed amount unchanged.
rule hlSpReserveThenUnreserveLeavesCustodyUntouched(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");

    mathint totalBefore = ghostPeTotal128;

    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);
    _Spoke.unreserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint totalAfter = ghostPeTotal128;

    assert(totalAfter == totalBefore, "a hold and its release leave custody untouched");
}

// SP-HL-32: reserving then unreserving an amount restores the total reserved in escrow.
rule hlSpReserveThenUnreserveRestoresTheAggregateHold(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");

    mathint reservedBefore = ghostPeReserved128;

    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);
    _Spoke.unreserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint reservedAfter = ghostPeReserved128;

    assert(reservedAfter == reservedBefore, "a hold and its release leave the total held unchanged");
}

// SP-HL-33: reserving then unreserving restores the reserver's reservation under that reason.
rule hlSpReserveThenUnreserveRestoresTheReserversBucket(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");

    mathint bucketBefore = ghostPeReservedBy128[reserver][reason];

    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);
    _Spoke.unreserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint bucketAfter = ghostPeReservedBy128[reserver][reason];

    assert(bucketAfter == bucketBefore, "a hold and its release leave the reserver's reservation unchanged");
}

// SP-HL-34: reserving then unreserving an amount nets to zero in the hub's pending report.
rule hlSpReserveThenUnreserveRestoresTheQueuedNet(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");
    uint128 aid = ghostSrAssetToId128[ghostPeAsset][ghostPeTokenId256];

    mathint netBefore = ghostSqDeposits128[aid] - ghostSqWithdrawals128[aid];

    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);
    _Spoke.unreserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint netAfter = ghostSqDeposits128[aid] - ghostSqWithdrawals128[aid];

    assert(netAfter == netBefore, "a hold and its release leave the asset's queued net unchanged");
}

// SP-HL-35: a reserved withdrawal takes exactly the requested amount out of escrow.
rule hlSpWithdrawReservedPaysOutTheRequestedAmount(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount,
    address reserver, bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");

    mathint totalBefore = ghostPeTotal128;

    _Spoke.withdrawReserved(e, poolId, scId, asset, tokenId, receiver, amount, reserver, reason);

    mathint totalAfter = ghostPeTotal128;

    assert(totalAfter == totalBefore - amount, "a reserved withdrawal lowers custody by exactly the amount");
}

// SP-HL-36: a reserved withdrawal uses up an equal amount of the escrow's reservations.
rule hlSpWithdrawReservedConsumesTheHold(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount,
    address reserver, bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");

    mathint reservedBefore = ghostPeReserved128;

    _Spoke.withdrawReserved(e, poolId, scId, asset, tokenId, receiver, amount, reserver, reason);

    mathint reservedAfter = ghostPeReserved128;

    assert(reservedAfter == reservedBefore - amount,
        "a reserved withdrawal lowers the total held by exactly the amount");
}

// SP-HL-37: a reserved withdrawal queues nothing for the hub.
rule hlSpWithdrawReservedLeavesTheQueueUntouched(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount,
    address reserver, bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");
    uint128 aid = ghostSrAssetToId128[ghostPeAsset][ghostPeTokenId256];

    mathint depositsBefore = ghostSqDeposits128[aid];
    mathint withdrawalsBefore = ghostSqWithdrawals128[aid];
    mathint deltaBefore = ghostSqDelta128;
    mathint nonceBefore = ghostSqNonce64;
    mathint counterBefore = ghostSqQueuedAssetCounter32;

    _Spoke.withdrawReserved(e, poolId, scId, asset, tokenId, receiver, amount, reserver, reason);

    mathint depositsAfter = ghostSqDeposits128[aid];
    mathint withdrawalsAfter = ghostSqWithdrawals128[aid];
    mathint deltaAfter = ghostSqDelta128;
    mathint nonceAfter = ghostSqNonce64;
    mathint counterAfter = ghostSqQueuedAssetCounter32;

    assert(depositsAfter == depositsBefore && withdrawalsAfter == withdrawalsBefore
        && deltaAfter == deltaBefore && nonceAfter == nonceBefore && counterAfter == counterBefore,
        "a reserved withdrawal leaves the queue for the hub untouched");
}

// SP-HL-38: a revoke debits the revoked shares from the caller's balance.
rule hlSpRevokePullsSharesFromTheCaller(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 shares) {

    setupSpokeLinkedSpokeCoreValidState(e);

    address token = ghostSrShareToken;
    mathint callerBefore = ghostERC20Balances128[token][e.msg.sender];

    _Spoke.revoke(e, poolId, scId, shares);

    mathint callerAfter = ghostERC20Balances128[token][e.msg.sender];

    assert(callerAfter == callerBefore - shares, "the caller pays for a revoke with exactly those shares");
}

// SP-HL-39: a revoke lowers the share token supply by the revoked amount.
rule hlSpRevokeBurnsThePulledShares(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 shares) {

    setupSpokeLinkedSpokeCoreValidState(e);

    address token = ghostSrShareToken;
    mathint supplyBefore = ghostERC20TotalSupply256[token];

    _Spoke.revoke(e, poolId, scId, shares);

    mathint supplyAfter = ghostERC20TotalSupply256[token];

    assert(supplyAfter == supplyBefore - shares, "a revoke burns exactly the revoked shares");
}

// SP-HL-40: a revoke leaves no shares behind on the spoke.
rule hlSpRevokeParksNoSharesOnTheSpoke(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 shares) {

    setupSpokeLinkedSpokeCoreValidState(e);

    address token = ghostSrShareToken;
    mathint spokeBefore = ghostERC20Balances128[token][_Spoke];

    _Spoke.revoke(e, poolId, scId, shares);

    mathint spokeAfter = ghostERC20Balances128[token][_Spoke];

    assert(spokeAfter == spokeBefore, "a revoke leaves the spoke's share balance unchanged");
}

// SP-HL-41: a revoke queues a share decrease of exactly the revoked amount for the hub.
rule hlSpRevokeQueuesTheBurnAsADecrease(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 shares) {

    setupSpokeLinkedSpokeCoreValidState(e);

    mathint signedBefore = ghostSqIsPositive ? ghostSqDelta128 : -ghostSqDelta128;

    _Spoke.revoke(e, poolId, scId, shares);

    mathint signedAfter = ghostSqIsPositive ? ghostSqDelta128 : -ghostSqDelta128;

    assert(signedAfter == signedBefore - shares, "a revoke queues its own size as a share decrease");
}

// SP-HL-42: each asset registration sends exactly one RegisterAsset message.
rule hlSpRegisterAssetSendsOneRegistrationAnnouncement(env e, uint16 centrifugeId, address asset,
    uint256 tokenId, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);

    mathint announcedBefore = ghostMsRegisterAssetCount;

    _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);

    mathint announcedAfter = ghostMsRegisterAssetCount;
    mathint kindAfter = ghostMsLastKind;

    assert(announcedAfter == announcedBefore + 1 && kindAfter == MS_REGISTER_ASSET(),
        "the hub gets one asset notice per registration");
}

// SP-HL-43: an asset registration announces the id the registry stores for that asset.
rule hlSpRegisterAssetAnnouncesTheStoredId(env e, uint16 centrifugeId, address asset,
    uint256 tokenId, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);

    _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);

    mathint announcedId = ghostMsLastAssetId128;
    mathint storedId = ghostSrAssetToId128[asset][tokenId];

    assert(announcedId == storedId, "the hub hears the same asset id the registry keeps");
}

// SP-HL-44: submitting queued assets sends an asset update for the requested asset.
rule hlSpAssetFlushAnnouncesAnUpdateForTheFlushedRow(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);
    mathint aid = assetId;

    _Spoke.submitQueuedAssets(e, poolId, scId, assetId, extraGasLimit, refund);

    mathint kindAfter = ghostMsLastKind;
    mathint reportedAsset = ghostMsLastAssetId128;

    assert(kindAfter == MS_UPDATE_ASSETS() && reportedAsset == aid,
        "the update sent on a flush names the flushed asset");
}

// SP-HL-45: an asset update reports the size of the net flow queued for that asset.
rule hlSpAssetFlushReportsTheRowsNetSize(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);
    uint128 aid = assetId;

    mathint depositsBefore = ghostSqDeposits128[aid];
    mathint withdrawalsBefore = ghostSqWithdrawals128[aid];

    _Spoke.submitQueuedAssets(e, poolId, scId, assetId, extraGasLimit, refund);

    mathint reportedNet = ghostMsUpdateNetAmount128;

    assert(reportedNet == (depositsBefore >= withdrawalsBefore
            ? depositsBefore - withdrawalsBefore : withdrawalsBefore - depositsBefore),
        "an asset flush reports the size of the asset's queued net");
}

// SP-HL-46: an asset update reports the direction of the net flow queued for that asset.
rule hlSpAssetFlushReportsTheRowsNetDirection(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);
    uint128 aid = assetId;

    mathint depositsBefore = ghostSqDeposits128[aid];
    mathint withdrawalsBefore = ghostSqWithdrawals128[aid];

    _Spoke.submitQueuedAssets(e, poolId, scId, assetId, extraGasLimit, refund);

    bool reportedIsIncrease = ghostMsUpdateIsIncrease;

    assert(reportedIsIncrease == (depositsBefore > withdrawalsBefore),
        "an asset flush reports an increase iff deposits exceeded withdrawals");
}

// SP-HL-47: an asset update is sent with the queue's current sequence number.
rule hlSpAssetFlushReportsTheStoredSequenceNumber(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);

    mathint nonceBefore = ghostSqNonce64;

    _Spoke.submitQueuedAssets(e, poolId, scId, assetId, extraGasLimit, refund);

    mathint reportedNonce = ghostMsUpdateNonce64;

    assert(reportedNonce == nonceBefore, "an asset flush reports under the stored nonce");
}

// SP-HL-48: submitting an asset's queued flow clears it, so it is not reported twice.
rule hlSpAssetFlushEmptiesTheRow(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);
    uint128 aid = assetId;

    _Spoke.submitQueuedAssets(e, poolId, scId, assetId, extraGasLimit, refund);

    mathint depositsAfter = ghostSqDeposits128[aid];
    mathint withdrawalsAfter = ghostSqWithdrawals128[aid];

    assert(depositsAfter == 0 && withdrawalsAfter == 0, "an asset flush empties the asset queue it reported");
}

// SP-HL-49: submitting queued shares always sends a share update to the hub.
rule hlSpShareFlushAnnouncesAShareUpdate(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);

    _Spoke.submitQueuedShares(e, poolId, scId, extraGasLimit, refund);

    mathint kindAfter = ghostMsLastKind;

    assert(kindAfter == MS_UPDATE_SHARES(), "a share flush sends a share update to the hub");
}

// SP-HL-50: submitting queued share changes reports their net size to the hub.
rule hlSpShareFlushReportsTheQueuedNetSize(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);

    mathint deltaBefore = ghostSqDelta128;

    _Spoke.submitQueuedShares(e, poolId, scId, extraGasLimit, refund);

    mathint reportedNet = ghostMsUpdateNetAmount128;

    assert(reportedNet == deltaBefore, "a share flush reports the size of the queued share net");
}

// SP-HL-51: a share update reports the direction of the queued net share change.
rule hlSpShareFlushReportsTheQueuedNetDirection(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);

    bool isPositiveBefore = ghostSqIsPositive;

    _Spoke.submitQueuedShares(e, poolId, scId, extraGasLimit, refund);

    bool reportedIsIncrease = ghostMsUpdateIsIncrease;

    assert(reportedIsIncrease == isPositiveBefore, "the hub is told whether the queued shares rose or fell");
}

// SP-HL-52: a share update is sent with the queue's current sequence number.
rule hlSpShareFlushReportsTheStoredSequenceNumber(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);

    mathint nonceBefore = ghostSqNonce64;

    _Spoke.submitQueuedShares(e, poolId, scId, extraGasLimit, refund);

    mathint reportedNonce = ghostMsUpdateNonce64;

    assert(reportedNonce == nonceBefore, "a share flush reports under the stored nonce");
}

// SP-HL-53: submitting queued shares clears them, so no share change is reported twice.
rule hlSpShareFlushClearsTheQueuedNet(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);

    _Spoke.submitQueuedShares(e, poolId, scId, extraGasLimit, refund);

    mathint deltaAfter = ghostSqDelta128;

    assert(deltaAfter == 0, "a share flush clears the queued share net");
}

// SP-HL-56: a hold raises the reserver's and the total reservation by the amount, leaving custody alone.
rule hlSpReserveRaisesBucketAndHoldByExactlyTheAmount(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");

    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;
    mathint bucketBefore = ghostPeReservedBy128[reserver][reason];

    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint totalAfter = ghostPeTotal128;
    mathint reservedAfter = ghostPeReserved128;
    mathint bucketAfter = ghostPeReservedBy128[reserver][reason];

    assert(reservedAfter == reservedBefore + amount && bucketAfter == bucketBefore + amount
            && totalAfter == totalBefore,
        "both holds grow by exactly the amount and custody stays put");
}

// SP-HL-57: a release lowers the reserver's and the total reservation by the amount, leaving custody alone.
rule hlSpUnreserveLowersBucketAndHoldByExactlyTheAmount(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");

    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;
    mathint bucketBefore = ghostPeReservedBy128[reserver][reason];

    _Spoke.unreserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint totalAfter = ghostPeTotal128;
    mathint reservedAfter = ghostPeReserved128;
    mathint bucketAfter = ghostPeReservedBy128[reserver][reason];

    assert(reservedAfter == reservedBefore - amount && bucketAfter == bucketBefore - amount
            && totalAfter == totalBefore,
        "both holds shrink by exactly the amount and custody stays put");
}

// SP-HL-58: a zero deposit, withdrawal, hold, release, issue or revoke leaves the hub's pending report alone.
rule hlSpZeroAmountEntryLeavesTheQueueUntouched(env e, uint8 op, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, address to,
    address reserver, bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");
    uint128 aid = ghostSrAssetToId128[ghostPeAsset][ghostPeTokenId256];

    mathint depositsBefore = ghostSqDeposits128[aid];
    mathint withdrawalsBefore = ghostSqWithdrawals128[aid];
    mathint counterBefore = ghostSqQueuedAssetCounter32;
    mathint deltaBefore = ghostSqDelta128;
    bool isPositiveBefore = ghostSqIsPositive;
    mathint nonceBefore = ghostSqNonce64;

    if (op == 0) {
        _Spoke.deposit(e, poolId, scId, asset, tokenId, 0);
    } else if (op == 1) {
        _Spoke.noteDeposit(e, poolId, scId, asset, tokenId, 0);
    } else if (op == 2) {
        _Spoke.withdraw(e, poolId, scId, asset, tokenId, receiver, 0);
    } else if (op == 3) {
        _Spoke.reserve(e, poolId, scId, asset, tokenId, 0, reserver, reason);
    } else if (op == 4) {
        _Spoke.unreserve(e, poolId, scId, asset, tokenId, 0, reserver, reason);
    } else if (op == 5) {
        _Spoke.issue(e, poolId, scId, to, 0);
    } else {
        _Spoke.revoke(e, poolId, scId, 0);
    }

    mathint depositsAfter = ghostSqDeposits128[aid];
    mathint withdrawalsAfter = ghostSqWithdrawals128[aid];
    mathint counterAfter = ghostSqQueuedAssetCounter32;
    mathint deltaAfter = ghostSqDelta128;
    bool isPositiveAfter = ghostSqIsPositive;
    mathint nonceAfter = ghostSqNonce64;

    assert(depositsAfter == depositsBefore && withdrawalsAfter == withdrawalsBefore
            && counterAfter == counterBefore && deltaAfter == deltaBefore
            && isPositiveAfter == isPositiveBefore && nonceAfter == nonceBefore,
        "an entry of zero skips the pending report entirely");
}

// SP-HL-59: every update sent to the hub, an empty one included, uses up exactly one sequence number.
rule hlSpFlushSpendsExactlyOneNonce(env e, bool shares, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, uint128 extraGasLimit, address refund) {

    setupSpokeLinkedSpokeCoreValidState(e);

    mathint nonceBefore = ghostSqNonce64;

    if (shares) {
        _Spoke.submitQueuedShares(e, poolId, scId, extraGasLimit, refund);
    } else {
        _Spoke.submitQueuedAssets(e, poolId, scId, assetId, extraGasLimit, refund);
    }

    mathint nonceAfter = ghostSqNonce64;

    assert(nonceAfter == nonceBefore + 1, "a flush spends exactly one nonce");
}

// SP-HL-60: registering an asset changes no admin right, manager, bridger, request manager or policy.
rule hlSpRegisterAssetGrantsNoSeat(env e, uint16 centrifugeId, address asset, uint256 tokenId,
    address refund, address who) {

    setupSpokeLinkedSpokeCoreValidState(e);

    mathint spokeWardBefore = _Spoke.wards[who];
    mathint registryWardBefore = _SpokeRegistry.wards(who);
    mathint queueWardBefore = _SnapshotQueue.wards[who];
    mathint escrowWardBefore = _PoolEscrow.wards[who];
    bool managerBefore = ghostSrManager[who];
    bool bridgerBefore = ghostSrBridger[who];
    address requestManagerBefore = ghostSrRequestManager;
    address policyBefore = ghostSrPolicy;

    _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);

    mathint spokeWardAfter = _Spoke.wards[who];
    mathint registryWardAfter = _SpokeRegistry.wards(who);
    mathint queueWardAfter = _SnapshotQueue.wards[who];
    mathint escrowWardAfter = _PoolEscrow.wards[who];
    bool managerAfter = ghostSrManager[who];
    bool bridgerAfter = ghostSrBridger[who];
    address requestManagerAfter = ghostSrRequestManager;
    address policyAfter = ghostSrPolicy;

    assert(spokeWardAfter == spokeWardBefore && registryWardAfter == registryWardBefore
            && queueWardAfter == queueWardBefore && escrowWardAfter == escrowWardBefore
            && managerAfter == managerBefore && bridgerAfter == bridgerBefore
            && requestManagerAfter == requestManagerBefore && policyAfter == policyBefore,
        "no ward or pool role changes when an asset is registered");
}

// SP-HL-62: a noted deposit, counted or not, books the given amount in escrow without moving any tokens.
rule hlSpNoteDepositBooksExactlyItsAmount(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint128 amount, bool counted) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");

    address escrowAddress = ghostEfEscrow(poolId);
    mathint tokensBefore = ghostERC20Balances128[asset][escrowAddress];
    mathint totalBefore = ghostPeTotal128;

    if (counted) {
        _Spoke.noteDepositCounted(e, poolId, scId, asset, 0, amount);
    } else {
        _Spoke.noteDeposit(e, poolId, scId, asset, 0, amount);
    }

    assert(ghostPeTotal128 == totalBefore + amount
            && ghostERC20Balances128[asset][escrowAddress] == tokensBefore,
        "a deposit note books exactly the amount and leaves escrow tokens as is");
}

// SP-HL-63: a withdrawal to another address changes escrow tokens and books equally.
rule hlSpWithdrawMovesTokensAndBookTogether(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");
    require(asset != ghostSrShareToken, "SCOPE: the asset is not the pool's own share token");

    address escrowAddress = ghostEfEscrow(poolId);
    require(receiver != escrowAddress, "SCOPE: the receiver is not the escrow itself");

    mathint tokensBefore = ghostERC20Balances128[asset][escrowAddress];
    mathint totalBefore = ghostPeTotal128;

    _Spoke.withdraw(e, poolId, scId, asset, 0, receiver, amount);

    assert(ghostERC20Balances128[asset][escrowAddress] - tokensBefore
            == ghostPeTotal128 - totalBefore,
        "a withdrawal to anyone but the escrow moves its tokens and book alike");
}

// SP-HL-64: a reserved withdrawal to another address changes escrow tokens and books equally.
rule hlSpWithdrawReservedMovesTokensAndBookTogether(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, address receiver, uint128 amount,
    address reserver, bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(scId == ghostShareClassA && asset == ghostPeAsset && ghostPeTokenId256 == 0,
        "SCOPE: the modelled share class and ERC20 asset");
    require(asset != ghostSrShareToken, "SCOPE: the asset is not the pool's own share token");

    address escrowAddress = ghostEfEscrow(poolId);
    require(receiver != escrowAddress, "SCOPE: the receiver is not the escrow itself");

    mathint tokensBefore = ghostERC20Balances128[asset][escrowAddress];
    mathint totalBefore = ghostPeTotal128;

    _Spoke.withdrawReserved(e, poolId, scId, asset, 0, receiver, amount, reserver, reason);

    assert(ghostERC20Balances128[asset][escrowAddress] - tokensBefore
            == ghostPeTotal128 - totalBefore,
        "a reserved payout to anyone but the escrow moves tokens and book alike");
}

// SP-HL-65: a deposit noted then reserved leaves free funds and the hub's pending report unchanged.
rule hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeLinkedSpokeCoreValidState(e);
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SAFE: binds the asset to the measured escrow row");
    uint128 aid = ghostSrAssetToId128[ghostPeAsset][ghostPeTokenId256];

    mathint freeBefore = ghostPeTotal128 - ghostPeReserved128;
    mathint reservedBefore = ghostPeReserved128;
    mathint netBefore = ghostSqDeposits128[aid] - ghostSqWithdrawals128[aid];

    _Spoke.noteDeposit(e, poolId, scId, asset, tokenId, amount);
    _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);

    mathint freeAfter = ghostPeTotal128 - ghostPeReserved128;
    mathint reservedAfter = ghostPeReserved128;
    mathint netAfter = ghostSqDeposits128[aid] - ghostSqWithdrawals128[aid];

    assert(freeAfter == freeBefore && reservedAfter == reservedBefore + amount && netAfter == netBefore,
        "free funds and queued net stay; reservations grow by the reserved amount");
}
