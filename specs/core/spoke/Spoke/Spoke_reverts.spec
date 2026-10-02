import "setup/Spoke_solo.spec";

// SP-RV-01: configuring the spoke fails for a non-admin caller or an unknown setting.
rule rvSpFileRefusesANonWardOrAnUnknownName(env e, bytes32 what, address data) {

    setupSpokeValidState(e);

    mathint callerWard = _Spoke.wards[e.msg.sender];
    bool unknownParam = what != FILE_GATEWAY_SP_CVL() && what != FILE_SENDER_SP_CVL();

    _Spoke.file@withrevert(e, what, data);
    bool reverted = lastReverted;

    assert((callerWard != 1 || unknownParam) => reverted, "rewiring fails for a non-ward or an unknown route name");
}

// SP-RV-02: a deposit into the pool escrow fails unless the caller is a pool manager, even in a batch.
rule rvSpDepositRefusesANonManager(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address asset, uint256 tokenId, uint128 amount) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.deposit@withrevert(e, poolId, scId, asset, tokenId, amount);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "a deposit by a non-manager fails");
}

// SP-RV-03: counting assets already in the escrow fails unless the caller is a pool manager, even in a batch.
rule rvSpNoteDepositRefusesANonManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.noteDeposit@withrevert(e, poolId, scId, asset, tokenId, amount);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "noting a deposit fails for a non-manager");
}

// SP-RV-04: a withdrawal from the pool escrow fails unless the caller is a pool manager, even in a batch.
rule rvSpWithdrawRefusesANonManager(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address asset, uint256 tokenId, address receiver, uint128 amount) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.withdraw@withrevert(e, poolId, scId, asset, tokenId, receiver, amount);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "a withdrawal by a non-manager fails");
}

// SP-RV-05: paying out reserved assets fails unless the caller is a pool manager, even in a batch.
rule rvSpWithdrawReservedRefusesANonManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount,
    address reserver, bytes32 reason) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.withdrawReserved@withrevert(e, poolId, scId, asset, tokenId, receiver, amount, reserver, reason);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "a reserved withdrawal by a non-manager fails");
}

// SP-RV-06: reserving pool assets fails unless the caller is a pool manager, even in a batch.
rule rvSpReserveRefusesANonManager(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address asset, uint256 tokenId, uint128 amount, address reserver, bytes32 reason) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.reserve@withrevert(e, poolId, scId, asset, tokenId, amount, reserver, reason);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "a reservation by a non-manager fails");
}

// SP-RV-07: releasing reserved assets fails unless the caller is a pool manager, even in a batch.
rule rvSpUnreserveRefusesANonManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, uint128 amount, address reserver,
    bytes32 reason) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.unreserve@withrevert(e, poolId, scId, asset, tokenId, amount, reserver, reason);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "releasing a reservation fails for a non-manager");
}

// SP-RV-08: reporting asset changes to the hub fails unless the caller is a pool manager, even in a batch.
rule rvSpSubmitQueuedAssetsRefusesANonManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, uint128 extraGasLimit, address refund) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.submitQueuedAssets@withrevert(e, poolId, scId, assetId, extraGasLimit, refund);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "submitting queued assets fails for a non-manager");
}

// SP-RV-09: issuing share tokens fails unless the caller is a pool manager, even in a batch.
rule rvSpIssueRefusesANonManager(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address to, uint128 shares) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.issue@withrevert(e, poolId, scId, to, shares);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "an issue by a non-manager fails");
}

// SP-RV-10: revoking share tokens fails unless the caller is a pool manager, even in a batch.
rule rvSpRevokeRefusesANonManager(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    uint128 shares) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.revoke@withrevert(e, poolId, scId, shares);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "a revoke by a non-manager fails");
}

// SP-RV-11: moving shares out of the pool escrow fails unless the caller is a pool manager, even in a batch.
rule rvSpWithdrawSharesRefusesANonManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address receiver, uint128 amount) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.withdrawShares@withrevert(e, poolId, scId, receiver, amount);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "a share payout by a non-manager fails");
}

// SP-RV-12: reporting share changes to the hub fails unless the caller is a pool manager, even in a batch.
rule rvSpSubmitQueuedSharesRefusesANonManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 extraGasLimit, address refund) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.submitQueuedShares@withrevert(e, poolId, scId, extraGasLimit, refund);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "submitting queued shares fails for a non-manager");
}

// SP-RV-13: a forced share transfer fails unless the caller is a pool manager, even in a batch.
rule rvSpTransferSharesFromRefusesANonManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address sender_, address from, address to, uint256 amount) {

    setupSpokeSoloAnyTransient(e);

    bool callerIsManager = ghostSrManager[spResolvedSenderCVL(e)];

    _Spoke.transferSharesFrom@withrevert(e, poolId, scId, sender_, from, to, amount);
    bool reverted = lastReverted;

    assert(!callerIsManager => reverted, "a forced transfer by a non-manager fails");
}

// SP-RV-14: a cross-chain share transfer fails unless the caller is the owner or an admin, even in a batch.
rule rvSpBridgeRefusesAStrangerToTheOwner(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeSoloAnyTransient(e);

    address caller = spResolvedSenderCVL(e);
    bool callerMayActForOwner = caller == owner || _Spoke.wards[caller] == 1;

    _Spoke.crosschainTransferShares@withrevert(e, centrifugeId, poolId, scId, receiver, sender_, owner,
        amount, extraGasLimit, remoteExtraGasLimit, refund);
    bool reverted = lastReverted;

    assert(!callerMayActForOwner => reverted, "a caller who is neither owner nor ward cannot bridge");
}

// SP-RV-15: a cross-chain share transfer fails unless the pool lets the owner bridge shares.
rule rvSpBridgeRefusesANonBridgerOwner(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    bool ownerIsBridger = ghostSrBridger[owner];

    _Spoke.crosschainTransferShares@withrevert(e, centrifugeId, poolId, scId, receiver, sender_, owner,
        amount, extraGasLimit, remoteExtraGasLimit, refund);
    bool reverted = lastReverted;

    assert(!ownerIsBridger => reverted, "a bridge fails for an owner that is not a bridger");
}

// SP-RV-16: a cross-chain share transfer of zero shares fails.
rule rvSpBridgeRefusesAZeroAmount(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    bool emptyAmount = amount == 0;

    _Spoke.crosschainTransferShares@withrevert(e, centrifugeId, poolId, scId, receiver, sender_, owner,
        amount, extraGasLimit, remoteExtraGasLimit, refund);
    bool reverted = lastReverted;

    assert(emptyAmount => reverted, "bridging nothing reverts");
}

// SP-RV-17: a cross-chain share transfer to this same network fails.
rule rvSpBridgeRefusesALocalDestination(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    bool localDestination = centrifugeId == ghostMsLocalCentrifugeId16;

    _Spoke.crosschainTransferShares@withrevert(e, centrifugeId, poolId, scId, receiver, sender_, owner,
        amount, extraGasLimit, remoteExtraGasLimit, refund);
    bool reverted = lastReverted;

    assert(localDestination => reverted, "bridging to the local network reverts");
}

// SP-RV-18: a request to the hub fails unless the direct caller is the pool's request manager, even in a batch.
rule rvSpRequestRefusesAnyCallerButTheRegisteredManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, bytes payload, uint128 extraGasLimit,
    bool unpaid, address refund) {

    setupSpokeSoloAnyTransient(e);

    address requestManager = ghostSrRequestManager;

    _Spoke.request@withrevert(e, poolId, scId, assetId, payload, extraGasLimit, unpaid, refund);
    bool reverted = lastReverted;

    assert((requestManager == 0 || e.msg.sender != requestManager) => reverted,
        "a request fails with no request manager set, or from any other caller");
}

// SP-RV-19: granting spoke admin rights fails unless the caller is an admin.
rule rvSpRelyRefusesANonWard(env e, address user) {

    setupSpokeValidState(e);

    mathint callerWard = _Spoke.wards[e.msg.sender];

    _Spoke.rely@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerWard != 1 => reverted, "granting ward rights fails for a non-ward");
}

// SP-RV-20: revoking spoke admin rights fails unless the caller is an admin.
rule rvSpDenyRefusesANonWard(env e, address user) {

    setupSpokeValidState(e);

    mathint callerWard = _Spoke.wards[e.msg.sender];

    _Spoke.deny@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerWard != 1 => reverted, "revoking ward rights fails for a non-ward");
}

// SP-RV-21: with no policy and no ETH sent, a non-admin pool manager can always report asset changes.
rule rvSpSubmitQueuedAssetsIsNeverRefusedToASeatedManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, uint128 extraGasLimit, address refund) {

    setupSpokeValidState(e);
    address messageSender = _Spoke.sender;
    address installedPolicy = ghostSrPolicy;
    require(nativeCodesize[messageSender] > 0
        && (installedPolicy == 0 || nativeCodesize[installedPolicy] > 0),
        "TRUSTED: governance and hub wire only deployed code");
    require(e.msg.value == 0, "UNSAFE: a paid submission's refusals are unchecked");
    require(installedPolicy == 0, "SCOPE: no pool policy installed, which may refuse");

    bool callerIsManager = ghostSrManager[e.msg.sender];
    bool callerHoldsNoWard = _Spoke.wards[e.msg.sender] != 1;

    _Spoke.submitQueuedAssets@withrevert(e, poolId, scId, assetId, extraGasLimit, refund);
    bool reverted = lastReverted;

    assert((callerIsManager && callerHoldsNoWard) => !reverted, "a non-ward manager can always submit queued assets");
}

// SP-RV-22: with no policy and no ETH sent, a non-admin pool manager can always report share changes.
rule rvSpSubmitQueuedSharesIsNeverRefusedToASeatedManager(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, uint128 extraGasLimit, address refund) {

    setupSpokeValidState(e);
    address messageSender = _Spoke.sender;
    address installedPolicy = ghostSrPolicy;
    require(nativeCodesize[messageSender] > 0
        && (installedPolicy == 0 || nativeCodesize[installedPolicy] > 0),
        "TRUSTED: governance and hub wire only deployed code");
    require(e.msg.value == 0, "UNSAFE: a paid submission's refusals are unchecked");
    require(installedPolicy == 0, "SCOPE: no pool policy installed, which may refuse");

    bool callerIsManager = ghostSrManager[e.msg.sender];
    bool callerHoldsNoWard = _Spoke.wards[e.msg.sender] != 1;

    _Spoke.submitQueuedShares@withrevert(e, poolId, scId, extraGasLimit, refund);
    bool reverted = lastReverted;

    assert((callerIsManager && callerHoldsNoWard) => !reverted, "a non-ward manager can always submit queued shares");
}

// SP-RV-23: a manager call with no ETH attached never fails, whoever the caller is.
rule rvSpManagerCallIsNeverRefusedToAnyCaller(env e, SpokeHarness.PoolId poolId, bytes32 target,
    bytes payload, uint128 extraGasLimit, address refund) {

    setupSpokeValidState(e);
    address messageSender = _Spoke.sender;
    require(nativeCodesize[messageSender] > 0, "TRUSTED: governance wires a deployed message sender");
    require(e.msg.value == 0, "UNSAFE: a paid manager call's refusals are unchecked");

    _Spoke.managerCall@withrevert(e, poolId, target, payload, extraGasLimit, refund);
    bool reverted = lastReverted;

    assert(!reverted, "a manager call is never refused, whoever the caller");
}


// SP-RV-24: a cross-chain share transfer fails when the share token's restriction rejects that owner and amount.
rule rvSpBridgeRefusesAnOwnerTheRegistrarVetoes(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    bool ownerVetoed = !ghostRegistrarCanBridge[ghostSrShareToken][owner][centrifugeId][amount];

    _Spoke.crosschainTransferShares@withrevert(e, centrifugeId, poolId, scId, receiver, sender_, owner,
        amount, extraGasLimit, remoteExtraGasLimit, refund);
    bool reverted = lastReverted;

    assert(ownerVetoed => reverted, "a bridge fails for an owner the share's restrictions veto");
}

// SP-RV-25: while a call is in progress, registering an asset or bridging shares fails for any other caller.
rule rvSpProtectedEntriesRefuseAForeignReentrantCaller(env e, bool op, uint16 centrifugeId, address asset,
    uint256 tokenId, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_,
    address owner, uint128 amount, uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeSoloAnyTransient(e);

    address initiator = ghostSpInitiatorT;

    if (op) {
        _Spoke.registerAsset@withrevert(e, centrifugeId, asset, tokenId, refund);
    } else {
        _Spoke.crosschainTransferShares@withrevert(e, centrifugeId, poolId, scId, receiver, sender_, owner,
            amount, extraGasLimit, remoteExtraGasLimit, refund);
    }
    bool reverted = lastReverted;

    assert((initiator != 0 && e.msg.sender != initiator) => reverted,
        "a re-entrant call from a different account is refused");
}

// SP-RV-26: a cross-chain share transfer fails when the share class has no share token.
rule rvSpBridgeRefusesAnUnregisteredShareClass(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    bool noShareToken = ghostSrShareToken == 0;

    _Spoke.crosschainTransferShares@withrevert(e, centrifugeId, poolId, scId, receiver, sender_, owner,
        amount, extraGasLimit, remoteExtraGasLimit, refund);
    bool reverted = lastReverted;

    assert(noShareToken => reverted, "a bridge fails for a class with no share token");
}
