import "HubHandler_LinkedHubCore_valid_state.spec";

// HH-RV-01: rewiring the hub handler fails for a non-admin caller or an unknown parameter.
rule rvHhFileRefusesANonWardOrAnUnknownName(env e, bytes32 what, address data) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool callerIsNotWard = _HubHandler.wards[e.msg.sender] != 1;
    bool unknownParam = what != FILE_HUB_HH_CVL() && what != FILE_HOLDINGS_HH_CVL()
        && what != FILE_SENDER_HH_CVL() && what != FILE_SHARE_CLASS_MANAGER_HH_CVL();

    _HubHandler.file@withrevert(e, what, data);
    bool reverted = lastReverted;

    assert((callerIsNotWard || unknownParam) => reverted,
        "rewiring the handler fails for a non-ward or a name it does not wire");
}

// HH-RV-02: a request fails for a non-admin or when the asset's network has no request manager.
rule rvHhRequestRefusesANonWardOrANetworkWithNoManager(env e, HubHandler.PoolId poolId, HubHandler.ShareClassId scId,
    HubHandler.AssetId assetId, bytes payload) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool callerIsNotWard = _HubHandler.wards[e.msg.sender] != 1;
    address registeredManager = ghostHrHubRequestManager[assert_uint16(ASSET_CENTRIFUGE_ID_HH_CVL(assetId))];
    bool noManager = registeredManager == 0;

    _HubHandler.request@withrevert(e, poolId, scId, assetId, payload);
    bool reverted = lastReverted;

    assert((callerIsNotWard || noManager) => reverted,
        "a non-ward caller or a manager-less network makes a request revert");
}

// HH-RV-03: a share report fails for a non-admin, an unknown share class, or a wrong nonce.
rule rvHhUpdateSharesRefusesANonWardAnUnknownClassOrAMissedNonce(env e, uint16 centrifugeId, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, uint128 amount, bool isIssuance, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool callerIsNotWard = _HubHandler.wards[e.msg.sender] != 1;
    bool classAbsent = !ghostScShareClassIds;
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];
    bool nonceMissed = nonceBefore != nonce;

    _HubHandler.updateShares@withrevert(e, centrifugeId, poolId, scId, amount, isIssuance, isSnapshot, nonce);
    bool reverted = lastReverted;

    assert((callerIsNotWard || classAbsent || nonceMissed) => reverted,
        "a non-ward, an unknown class or a wrong nonce makes a share report revert");
}

// HH-RV-04: an asset report fails for a non-admin or on a bad nonce.
rule rvHhUpdateAssetsRefusesANonWardOrAMissedNonce(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount,
    bool isIncrease, bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool callerIsNotWard = _HubHandler.wards[e.msg.sender] != 1;
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];
    bool nonceMissed = nonceBefore != nonce;

    _HubHandler.updateAssets@withrevert(e, centrifugeId, poolId, scId, assetId, amount, isIncrease,
        isSnapshot, nonce);
    bool reverted = lastReverted;

    assert((callerIsNotWard || nonceMissed) => reverted, "a non-ward or out-of-order asset report fails");
}

// HH-RV-05: the hub never blocks an admin's in-order report on an uninitialized holding, barring overflow.
rule rvHhUninitializedAssetReportIsNeverStrandedByTheShortfallTally(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isIncrease,
    bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(centrifugeId == ghostHoCid16, "SCOPE: binds the reporting network to the tallied one");
    require(ghostHoValuation[assetId] == 0, "SCOPE: an unopened holding, which books nothing");
    require(e.msg.value == 0, "SCOPE: no ether sent");
    require(!ghostSnapshotHookRefuses, "SCOPE: a rejecting snapshot hook is the pool manager's choice");

    bool callerIsWard = _HubHandler.wards[e.msg.sender] == 1;
    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    mathint decreasedBefore = ghostHoDecreasedAmount256[assetId];
    mathint networkDeficitCountBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitCountBefore = ghostHoDeficitCount32;
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];

    bool nonceMissed = nonceBefore != nonce;
    bool nonceExhausted = nonceBefore == max_uint64;
    bool counterOversteps = isIncrease
        ? increasedBefore + amount > max_uint256
        : decreasedBefore + amount > max_uint256;
    bool leavesShortfall = decreasedBefore > increasedBefore
        && decreasedBefore <= increasedBefore + amount;
    bool entersShortfall = decreasedBefore <= increasedBefore
        && decreasedBefore + amount > increasedBefore;
    bool tallyOversteps = isIncrease
        ? (leavesShortfall && (networkDeficitCountBefore == 0 || classDeficitCountBefore == 0))
        : (entersShortfall && (networkDeficitCountBefore == max_uint32 || classDeficitCountBefore == max_uint32));

    _HubHandler.updateAssets@withrevert(e, centrifugeId, poolId, scId, assetId, amount, isIncrease,
        isSnapshot, nonce);
    bool reverted = lastReverted;

    assert((callerIsWard && !nonceMissed && !nonceExhausted && !counterOversteps && !tallyOversteps)
        => !reverted,
        "a ward's in-order report on an unopened holding never fails while counters have room");
}

// HH-RV-06: a share transfer fails for a non-admin or a share class the hub does not know.
rule rvHhTransferRefusesANonWardOrAnUnknownShareClass(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool callerIsNotWard = _HubHandler.wards[e.msg.sender] != 1;
    bool classAbsent = !ghostScShareClassIds;

    _HubHandler.initiateTransferShares@withrevert(e, originCid, targetCid, poolId, scId, sender_,
        receiver, amount, extraGasLimit, refund);
    bool reverted = lastReverted;

    assert((callerIsNotWard || classAbsent) => reverted, "a transfer fails for a non-ward or an unknown share class");
}

// HH-RV-07: barring overflow, the hub never blocks an admin's known-class transfer with no bridging hook or ETH.
rule rvHhHooklessTransferIsNeverStrandedWhileTheCountersHaveRoom(env e, uint16 originCid, uint16 targetCid,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, bytes32 sender_, bytes32 receiver,
    uint128 amount, uint128 extraGasLimit, address refund) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(ghostHrBridgingHook == 0, "SCOPE: no bridging hook, it may alter transfers");
    require(e.msg.value == 0, "UNSAFE: transfers carrying ether are not checked");

    bool callerIsWard = _HubHandler.wards[e.msg.sender] == 1;
    bool classOnRecord = ghostScShareClassIds;
    require(ghostScNegativeNetworkCount32 == SC_NEGATIVE_NETWORK_CARDINALITY(),
        "PROVED: negativeNetworkCountMatchesTheShortNetworks (ShareClassManager)");
    scShortNetworkIsCounted(originCid);
    scShortNetworkIsCounted(targetCid);
    mathint issuedTargetBefore = ghostScIssuances256[targetCid];
    mathint revokedOriginBefore = ghostScRevocations256[originCid];

    bool targetLegOversteps = issuedTargetBefore + amount > max_uint256;
    bool originLegOversteps = revokedOriginBefore + amount > max_uint256;

    _HubHandler.initiateTransferShares@withrevert(e, originCid, targetCid, poolId, scId, sender_,
        receiver, amount, extraGasLimit, refund);
    bool reverted = lastReverted;

    assert((callerIsWard && classOnRecord && !targetLegOversteps && !originLegOversteps) => !reverted,
        "a ward's hookless transfer of a known class never fails while counters have room");
}

// HH-RV-08: granting admin rights on the hub handler fails for a non-admin caller.
rule rvHhRelyRefusesANonWard(env e, address user) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool callerIsNotWard = _HubHandler.wards[e.msg.sender] != 1;

    _HubHandler.rely@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerIsNotWard => reverted, "a non-ward cannot grant ward rights");
}

// HH-RV-09: revoking admin rights on the hub handler fails for a non-admin caller.
rule rvHhDenyRefusesANonWard(env e, address user) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool callerIsNotWard = _HubHandler.wards[e.msg.sender] != 1;

    _HubHandler.deny@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerIsNotWard => reverted, "a non-ward cannot revoke ward rights");
}

// HH-RV-10: the hub handler never blocks an admin's request when the asset's network has a request manager.
rule rvHhRequestIsNeverRefusedOnANetworkThatHasAManager(env e, HubHandler.PoolId poolId,
    HubHandler.ShareClassId scId, HubHandler.AssetId assetId, bytes payload) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    bool callerIsWard = _HubHandler.wards[e.msg.sender] == 1;
    address registeredManager = ghostHrHubRequestManager[assert_uint16(ASSET_CENTRIFUGE_ID_HH_CVL(assetId))];

    _HubHandler.request@withrevert(e, poolId, scId, assetId, payload);
    bool reverted = lastReverted;

    assert((callerIsWard && registeredManager != 0) => !reverted,
        "a ward's request never fails on a network with a manager");
}

// HH-RV-11: the hub never blocks an admin's in-order share report on a known class, barring overflow.
rule rvHhShareReportIsNeverStrandedWhileTheCountersHaveRoom(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, uint128 amount, bool isIssuance,
    bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    require(!ghostSnapshotHookRefuses, "SCOPE: a rejecting snapshot hook is the pool manager's choice");
    require(ghostScNegativeNetworkCount32 == SC_NEGATIVE_NETWORK_CARDINALITY(),
        "PROVED: negativeNetworkCountMatchesTheShortNetworks (ShareClassManager)");
    scShortNetworkIsCounted(centrifugeId);

    bool callerIsWard = _HubHandler.wards[e.msg.sender] == 1;
    bool classOnRecord = ghostScShareClassIds;
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];
    mathint legBefore = isIssuance
        ? ghostScIssuances256[centrifugeId]
        : ghostScRevocations256[centrifugeId];
    mathint totalLegBefore = isIssuance ? ghostScTotalIssuances256 : ghostScTotalRevocations256;

    bool nonceMissed = nonceBefore != nonce;
    bool nonceExhausted = nonceBefore == max_uint64;
    bool legOversteps = legBefore + amount > max_uint256 || totalLegBefore + amount > max_uint256;

    _HubHandler.updateShares@withrevert(e, centrifugeId, poolId, scId, amount, isIssuance, isSnapshot,
        nonce);
    bool reverted = lastReverted;

    assert((callerIsWard && classOnRecord && !nonceMissed && !nonceExhausted && !legOversteps)
        => (!reverted && ghostHoSnapshotNonce64[centrifugeId] == nonceBefore + 1),
        "absent overflow, a ward's in-order known-class report succeeds and spends its nonce");
}

// HH-RV-12: an admin's in-order report on an opened holding fails only on overflow or a missing account.
rule rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount(env e, uint16 centrifugeId,
    HubHandler.PoolId poolId, HubHandler.ShareClassId scId, HubHandler.AssetId assetId, uint128 amount, bool isIncrease,
    bool isSnapshot, uint64 nonce) {

    setupHubHandlerLinkedHubCoreValidState(e);
    require(centrifugeId == ghostHoCid16, "SCOPE: deficit counts are tracked for one network");
    require(ghostHoValuation[assetId] != 0, "SCOPE: an opened holding, HH-RV-05 covers the rest");
    require(e.msg.value == 0, "SCOPE: no ether sent");
    require(!ghostSnapshotHookRefuses, "SCOPE: a rejecting snapshot hook is the pool manager's choice");

    bool callerIsWard = _HubHandler.wards[e.msg.sender] == 1;
    mathint nonceBefore = ghostHoSnapshotNonce64[centrifugeId];
    mathint increasedBefore = ghostHoIncreasedAmount256[assetId];
    mathint decreasedBefore = ghostHoDecreasedAmount256[assetId];
    mathint valueBefore = ghostHoAssetAmountValue128[assetId];
    mathint networkDeficitCountBefore = ghostHoNetworkDeficitCount32;
    mathint classDeficitCountBefore = ghostHoDeficitCount32;
    mathint debitRow = isIncrease ? ghostHoAccountId256[assetId][0] : ghostHoAccountId256[assetId][1];
    mathint creditRow = isIncrease ? ghostHoAccountId256[assetId][1] : ghostHoAccountId256[assetId][0];
    bool accountAbsent = ghostAcLastUpdated64[debitRow] == 0 || ghostAcLastUpdated64[creditRow] == 0;
    mathint debitTotalBefore = ghostAcTotalDebit128[debitRow];
    mathint creditTotalBefore = ghostAcTotalCredit128[creditRow];
    bool journalExhausted = ghostAcJournalIdCounter64 == max_uint64;
    mathint quotesBefore = ghostValQuoteCount;

    mathint amountBefore = increasedBefore >= decreasedBefore ? increasedBefore - decreasedBefore : 0;
    mathint amountAfterOutflow = increasedBefore >= decreasedBefore + amount
        ? increasedBefore - decreasedBefore - amount : 0;
    mathint outflowValue = amountBefore == 0 ? 0 : valueBefore * (amountBefore - amountAfterOutflow) / amountBefore;

    bool counterOversteps = isIncrease
        ? increasedBefore + amount > max_uint256
        : decreasedBefore + amount > max_uint256;
    bool leavesShortfall = decreasedBefore > increasedBefore
        && decreasedBefore <= increasedBefore + amount;
    bool entersShortfall = decreasedBefore <= increasedBefore
        && decreasedBefore + amount > increasedBefore;
    bool tallyOversteps = isIncrease
        ? (leavesShortfall && (networkDeficitCountBefore == 0 || classDeficitCountBefore == 0))
        : (entersShortfall && (networkDeficitCountBefore == max_uint32 || classDeficitCountBefore == max_uint32));

    _HubHandler.updateAssets@withrevert(e, centrifugeId, poolId, scId, assetId, amount, isIncrease,
        isSnapshot, nonce);
    bool reverted = lastReverted;

    bool quoted = ghostValQuoteCount != quotesBefore;
    mathint booked = isIncrease ? (quoted ? to_mathint(ghostValLastQuote128) : 0) : outflowValue;
    bool valueOversteps = isIncrease && quoted && valueBefore + ghostValLastQuote128 > max_uint128;
    bool postingFails = booked != 0 && (accountAbsent || journalExhausted
        || debitTotalBefore + booked > max_uint128 || creditTotalBefore + booked > max_uint128);

    assert((callerIsWard && nonceBefore == nonce && nonceBefore != max_uint64 && !tallyOversteps)
        => (reverted => (counterOversteps || valueOversteps || postingFails)),
        "an admin's in-order report on an opened holding fails only on overflow or no account");
}

// HH-RV-13: asset registration fails exactly on ether, a non-admin, a zero id, over 18 or changed set decimals.
rule rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling(env e, HubHandler.AssetId assetId,
    uint8 assetDecimals) {

    setupHubHandlerLinkedHubCoreValidState(e);

    bool callerIsNotWard = _HubHandler.wards[e.msg.sender] != 1;
    mathint declared = assetDecimals;
    bool registeredBefore = ghostHrAssetRegistered[assetId];
    mathint storedBefore = ghostHrAssetDecimals8[assetId];

    _HubHandler.registerAsset@withrevert(e, assetId, assetDecimals);
    bool reverted = lastReverted;

    assert(reverted <=> (e.msg.value != 0 || callerIsNotWard || assetId == 0 || declared > MAX_DECIMALS_CVL()
            || (registeredBefore && storedBefore != 0 && storedBefore != declared)),
        "only ether, a non-admin, a zero id, over 18 or changed set decimals fail a registration");
}
