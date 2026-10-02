import "Holdings_single_pool_valid_state.spec";

// HO-RV-01: opening a holding fails for a non-admin, with no price source, or if already open.
rule rvHoInitializeRefusesANonWardANullSourceOrAnOpenRow(env e, Holdings.PoolId p,
    Holdings.ShareClassId sc, Holdings.AssetId aid, address newValuation, Holdings.AccountId[4] accounts) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[e.msg.sender];
    address rowValuationBefore = ghostHoValuation[aid];
    bool nullValuation = newValuation == 0;

    _Holdings.initialize@withrevert(e, p, sc, aid, newValuation, accounts);
    bool reverted = lastReverted;

    assert((wardBefore != 1 || nullValuation || rowValuationBefore != 0) => reverted,
        "opening fails for a non-ward, a null price source or an open holding");
}

// HO-RV-02: setting a journal account fails for a non-admin or on an unopened holding.
rule rvHoSetAccountIdRefusesANonWardOrAnUnopenedHolding(env e, Holdings.PoolId p,
    Holdings.ShareClassId sc, Holdings.AssetId aid, uint8 kind, Holdings.AccountId account) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[e.msg.sender];
    address rowValuationBefore = ghostHoValuation[aid];

    _Holdings.setAccountId@withrevert(e, p, sc, aid, kind, account);
    bool reverted = lastReverted;

    assert((wardBefore != 1 || rowValuationBefore == 0) => reverted,
        "a non-ward or an unopened holding cannot get a ledger account");
}

// HO-RV-03: switching a price source fails for a non-admin, a zero source, or an unopened holding.
rule rvHoUpdateValuationRefusesANonWardANullSourceOrAnUnopenedHolding(env e, Holdings.PoolId p,
    Holdings.ShareClassId sc, Holdings.AssetId aid, address newValuation) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[e.msg.sender];
    address rowValuationBefore = ghostHoValuation[aid];
    bool nullValuation = newValuation == 0;

    _Holdings.updateValuation@withrevert(e, p, sc, aid, newValuation);
    bool reverted = lastReverted;

    assert((wardBefore != 1 || nullValuation || rowValuationBefore == 0) => reverted,
        "a non-ward, a null source or an unopened holding blocks a source swap");
}

// HO-RV-04: attaching a snapshot hook fails for a non-admin or for a pool unknown to the hub.
rule rvHoSetSnapshotHookRefusesANonWardOrAnUnknownPool(env e, Holdings.PoolId p, address newHook) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[e.msg.sender];
    bool poolMissing = ghostHrCurrency128 == 0;

    _Holdings.setSnapshotHook@withrevert(e, p, newHook);
    bool reverted = lastReverted;

    assert((wardBefore != 1 || poolMissing) => reverted,
        "a non-ward or an unregistered pool makes hook attachment revert");
}

// HO-RV-05: a sync update fails for a non-admin or with an out-of-order sequence number.
rule rvHoSetSnapshotRefusesANonWardOrAnOutOfOrderNonce(env e, Holdings.PoolId p, Holdings.ShareClassId sc, uint16 cid,
    bool isSnapshot, uint64 nonce) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[e.msg.sender];
    mathint nonceBefore = ghostHoSnapshotNonce64[cid];
    bool wrongNonce = nonce != nonceBefore;

    _Holdings.setSnapshot@withrevert(e, p, sc, cid, isSnapshot, nonce);
    bool reverted = lastReverted;

    assert((wardBefore != 1 || wrongNonce) => reverted, "marking sync fails for a non-ward or an out-of-order nonce");
}

// HO-RV-06: Holdings itself never rejects an admin resending a network's sync notification.
rule rvHoCallOnSyncSnapshotIsNeverRefusedToAWard(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    uint16 cid) {

    setupHoldingsValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    require(!ghostSnapshotHookRefuses, "SCOPE: the snapshot hook accepts, its refusal stall is listed out of scope");

    mathint wardBefore = _Holdings.wards[e.msg.sender];

    _Holdings.callOnSyncSnapshot@withrevert(e, p, sc, cid);
    bool reverted = lastReverted;

    assert(wardBefore == 1 => !reverted, "a ward's sync replay is never refused, on any network");
}

// HO-RV-07: with no snapshot hook set, an admin can always notify a cross-network transfer.
rule rvHoCallOnTransferSnapshotIsNeverRefusedToAWard(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    uint16 originCid, uint16 targetCid, uint128 shares) {

    setupHoldingsValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    require(ghostHoSnapshotHook == 0, "SCOPE: no snapshot hook set, an installed one may refuse");

    mathint wardBefore = _Holdings.wards[e.msg.sender];

    _Holdings.callOnTransferSnapshot@withrevert(e, p, sc, originCid, targetCid, shares);
    bool reverted = lastReverted;

    assert(wardBefore == 1 => !reverted, "a ward's transfer notice is never refused on a hookless pool");
}

// HO-RV-08: booking an inflow to a holding fails for a non-admin.
rule rvHoIncreaseRefusesANonWard(env e, Holdings.PoolId p, Holdings.ShareClassId sc, Holdings.AssetId aid,
    uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[e.msg.sender];

    _Holdings.increase@withrevert(e, p, sc, aid, cid, amount);
    bool reverted = lastReverted;

    assert(wardBefore != 1 => reverted, "a non-ward can never book a deposit");
}

// HO-RV-09: with one network, an admin's inflow to an unopened holding fails only on overflow.
rule rvHoIncreaseBeforeTheRowIsOpenedIsNeverRefusedToAWard(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);
    require(ghostHoValuation[aid] == 0, "SCOPE: a holding not yet opened, no price read");
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint wardBefore = _Holdings.wards[e.msg.sender];
    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    bool counterOverflows = increasedBefore + amount > max_uint256;

    _Holdings.increase@withrevert(e, p, sc, aid, cid, amount);
    bool reverted = lastReverted;

    assert((wardBefore == 1 && !counterOverflows) => !reverted,
        "a ward's deposit before opening fails only if the total overflows");
}

// HO-RV-10: an outflow larger than the holding never fails for an admin, barring overflow.
rule rvHoDecreaseNeverStallsOnAnOversizedOutflow(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[e.msg.sender];
    mathint decreasedBefore = ghostHoDecreasedAmount256[aid];
    bool counterOverflows = decreasedBefore + amount > max_uint256;
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    _Holdings.decrease@withrevert(e, p, sc, aid, cid, amount);
    bool reverted = lastReverted;

    assert((wardBefore == 1 && !counterOverflows) => !reverted,
        "a ward's withdrawal, even past the position, fails only on overflow");
}

// HO-RV-11: an unopened holding has no readable price source, not even the zero address.
rule rvHoValuationRefusesAnUnopenedHolding(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid) {

    setupHoldingsValidState(e);

    address rowValuationBefore = ghostHoValuation[aid];

    _Holdings.valuation@withrevert(e, p, sc, aid);
    bool reverted = lastReverted;

    assert(rowValuationBefore == 0 => reverted, "reading the price source of an unopened holding fails");
}

// HO-RV-12: resending a network's sync notification fails for a non-admin.
rule rvHoCallOnSyncSnapshotRefusesANonWard(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    uint16 cid) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[e.msg.sender];

    _Holdings.callOnSyncSnapshot@withrevert(e, p, sc, cid);
    bool reverted = lastReverted;

    assert(wardBefore != 1 => reverted, "a non-ward can never replay a sync notification");
}

// HO-RV-13: notifying a cross-network share transfer fails for a non-admin.
rule rvHoCallOnTransferSnapshotRefusesANonWard(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    uint16 originCid, uint16 targetCid, uint128 shares) {

    setupHoldingsValidState(e);

    mathint wardBefore = _Holdings.wards[e.msg.sender];

    _Holdings.callOnTransferSnapshot@withrevert(e, p, sc, originCid, targetCid, shares);
    bool reverted = lastReverted;

    assert(wardBefore != 1 => reverted, "a non-ward can never notify a cross-network transfer");
}

// HO-RV-16: a revaluation fails exactly for a non-admin, an unopened holding, or a net amount past uint128.
rule rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid) {

    setupHoldingsValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint wardBefore = _Holdings.wards[e.msg.sender];
    address rowValuationBefore = ghostHoValuation[aid];
    bool netOversized = ghostHoIncreasedAmount256[aid] - ghostHoDecreasedAmount256[aid] > max_uint128;

    _Holdings.update@withrevert(e, p, sc, aid);
    bool reverted = lastReverted;

    assert(reverted <=> (wardBefore != 1 || rowValuationBefore == 0 || netOversized),
        "a revaluation fails only for a non-ward, an unopened holding or a net past uint128");
}

// HO-RV-17: reading a holding's amount, alone or with its value, fails exactly when its net exceeds uint128.
rule rvHoAmountViewsRefuseOnlyANetPastUint128(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid) {

    setupHoldingsValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    bool netOversized = ghostHoIncreasedAmount256[aid] - ghostHoDecreasedAmount256[aid] > max_uint128;

    _Holdings.amount@withrevert(e, p, sc, aid);
    bool amountReverted = lastReverted;
    _Holdings.holding@withrevert(e, p, sc, aid);
    bool holdingReverted = lastReverted;

    assert(amountReverted <=> netOversized, "the amount view fails exactly when the net exceeds uint128");
    assert(holdingReverted <=> netOversized, "the holding view fails exactly when the net exceeds uint128");
}

// HO-RV-18: with one network, an admin's inflow to an opened holding fails only on a total or value overflow.
rule rvHoIncreaseOnAnOpenHoldingFailsOnlyOnAnOverflowingTotalOrValue(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsValidState(e);
    require(_Holdings.wards[e.msg.sender] == 1, "SCOPE: the caller is a ward");
    require(ghostHoValuation[aid] != 0, "SCOPE: an opened holding, HO-RV-09 covers the rest");
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint increasedBefore = ghostHoIncreasedAmount256[aid];
    mathint valueBefore = ghostHoAssetAmountValue128[aid];
    mathint quotesBefore = ghostValQuoteCount;

    _Holdings.increase@withrevert(e, p, sc, aid, cid, amount);
    bool reverted = lastReverted;

    assert(reverted => (increasedBefore + amount > max_uint256
        || (ghostValQuoteCount != quotesBefore && valueBefore + ghostValLastQuote128 > max_uint128)),
        "a ward's deposit on an opened holding fails only on a total or value overflow");
}
