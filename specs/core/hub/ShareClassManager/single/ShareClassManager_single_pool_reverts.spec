import "ShareClassManager_single_pool_valid_state.spec";

// SC-RV-01: adding a share class fails for a non-admin, unknown pool, bad or used salt, or bad metadata.
rule rvScAddShareClassRefusesACreationThatDoesNotCheckOut(env e, ShareClassManager.PoolId p, string name, string symbol,
    bytes32 salt) {

    setupShareClassManagerValidState(e);

    mathint wardOfCaller = _ShareClassManager.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;
    bool poolUnregistered = ghostHrCurrency128 == 0;
    bool saltNotBrandedWithPool = (salt >> 192) != to_bytes32(require_uint256(p));
    bool saltAlreadySpent = ghostScSalts[salt];
    mathint nameLength = name.length;
    mathint symbolLength = symbol.length;

    _ShareClassManager.addShareClass@withrevert(e, p, name, symbol, salt);
    bool reverted = lastReverted;

    assert((callerHoldsNoWard || poolUnregistered || saltNotBrandedWithPool
            || saltAlreadySpent || nameLength == 0 || nameLength > 128 || symbolLength == 0 || symbolLength > 32)
            => reverted,
        "creation fails for a non-ward, unknown pool, bad salt or bad metadata");
}

// SC-RV-02: setting a share price fails for a non-admin, an unknown class, or a future timestamp.
rule rvScUpdateSharePriceRefusesANonWardAnUnknownClassOrAFutureStamp(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, ShareClassManager.D18 price, uint64 computedAt) {

    setupShareClassManagerValidState(e);

    mathint wardOfCaller = _ShareClassManager.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;
    bool classOnRecord = ghostScShareClassIds;
    bool stampAheadOfTheChain = computedAt > e.block.timestamp;

    _ShareClassManager.updateSharePrice@withrevert(e, p, sc, price, computedAt);
    bool reverted = lastReverted;

    assert((callerHoldsNoWard || !classOnRecord || stampAheadOfTheChain) => reverted,
        "a non-ward, an unknown class or a future stamp blocks a price update");
}

// SC-RV-03: a share supply update fails for a non-admin or an unknown share class.
rule rvScUpdateSharesRefusesANonWardOrAnUnknownClass(env e, uint16 centrifugeId, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint128 amount, bool isIssuance) {

    setupShareClassManagerValidState(e);

    mathint wardOfCaller = _ShareClassManager.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;
    bool classOnRecord = ghostScShareClassIds;

    _ShareClassManager.updateShares@withrevert(e, centrifugeId, p, sc, amount, isIssuance);
    bool reverted = lastReverted;

    assert((callerHoldsNoWard || !classOnRecord) => reverted, "a non-ward or an unknown class blocks a supply change");
}

// SC-RV-04: a network's issuance query fails when its revocations exceed its issuances.
rule rvScIssuanceRefusesANetworkInRevocationDeficit(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint16 centrifugeId) {

    setupShareClassManagerValidState(e);

    mathint issuancesBefore = ghostScIssuances256[centrifugeId];
    mathint revocationsBefore = ghostScRevocations256[centrifugeId];

    _ShareClassManager.issuance@withrevert(e, p, sc, centrifugeId);
    bool reverted = lastReverted;

    assert(revocationsBefore > issuancesBefore => reverted,
        "the issuance read fails for a network that revoked more than it issued");
}

// SC-RV-05: previewing the next share class id fails once a pool has used up all ids.
rule rvScPreviewNextShareClassIdRefusesAPoolWhoseClassCounterIsFull(env e, ShareClassManager.PoolId p) {

    setupShareClassManagerValidState(e);

    mathint classCountBefore = ghostScShareClassCount32;

    _ShareClassManager.previewNextShareClassId@withrevert(e, p);
    bool reverted = lastReverted;

    assert(classCountBefore == max_uint32 => reverted, "the id preview fails for a pool whose class counter is full");
}

// SC-RV-06: granting admin rights fails for a caller that is not an admin.
rule rvScRelyRefusesANonWard(env e, address user) {

    setupShareClassManagerValidState(e);

    mathint wardOfCaller = _ShareClassManager.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;

    _ShareClassManager.rely@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerHoldsNoWard => reverted, "a non-ward cannot grant ward rights");
}

// SC-RV-07: revoking admin rights fails for a caller that is not an admin.
rule rvScDenyRefusesANonWard(env e, address user) {

    setupShareClassManagerValidState(e);

    mathint wardOfCaller = _ShareClassManager.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;

    _ShareClassManager.deny@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerHoldsNoWard => reverted, "a non-ward cannot revoke ward rights");
}

// SC-RV-08: an admin's share update on a known class succeeds unless a counter overflows.
rule rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom(env e, uint16 centrifugeId, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint128 amount, bool isIssuance) {

    setupShareClassManagerValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    scShortNetworkIsCounted(centrifugeId);

    bool callerIsWard = _ShareClassManager.wards[e.msg.sender] == 1;
    bool classOnRecord = ghostScShareClassIds;
    mathint legBefore = isIssuance
        ? ghostScIssuances256[centrifugeId]
        : ghostScRevocations256[centrifugeId];
    mathint totalLegBefore = isIssuance ? ghostScTotalIssuances256 : ghostScTotalRevocations256;
    bool counterOversteps = legBefore + amount > max_uint256 || totalLegBefore + amount > max_uint256;

    _ShareClassManager.updateShares@withrevert(e, centrifugeId, p, sc, amount, isIssuance);
    bool reverted = lastReverted;

    assert((callerIsWard && classOnRecord && !counterOversteps) => !reverted,
        "a ward's supply change on a known class goes through if counters fit");
}

// SC-RV-09: a class's total supply query fails when its revocations exceed its issuances.
rule rvScTotalIssuanceRefusesAClassInRevocationDeficit(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc) {

    setupShareClassManagerValidState(e);

    mathint issuancesBefore = ghostScTotalIssuances256;
    mathint revocationsBefore = ghostScTotalRevocations256;

    _ShareClassManager.totalIssuance@withrevert(e, p, sc);
    bool reverted = lastReverted;

    assert(revocationsBefore > issuancesBefore => reverted,
        "the supply read fails for a class that revoked more than it issued");
}

// SC-RV-10: the issued and revoked totals of a class and of each network can always be read.
rule rvScRawCountersAlwaysAnswerWithTheLedger(env e, ShareClassManager.PoolId p, ShareClassManager.ShareClassId sc,
    uint16 centrifugeId) {

    setupShareClassManagerValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    uint256 classIssued;
    uint256 classRevoked;
    classIssued, classRevoked = _ShareClassManager.issuanceAcrossNetworks@withrevert(e, p, sc);
    bool classRefused = lastReverted;

    uint256 networkIssued;
    uint256 networkRevoked;
    networkIssued, networkRevoked = _ShareClassManager.issuancePerNetwork@withrevert(e, p, sc, centrifugeId);
    bool networkRefused = lastReverted;

    assert(!classRefused && !networkRefused
            && classIssued == ghostScTotalIssuances256 && classRevoked == ghostScTotalRevocations256
            && networkIssued == ghostScIssuances256[centrifugeId]
            && networkRevoked == ghostScRevocations256[centrifugeId],
        "the raw issued and revoked counters always read back as booked");
}

// SC-RV-12: a share transfer fails for a non-admin or an unknown share class.
rule rvScTransferSharesRefusesANonWardOrAnUnknownClass(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint16 fromCid, uint16 toCid, uint128 amount) {

    setupShareClassManagerValidState(e);

    bool callerHoldsNoWard = _ShareClassManager.wards[e.msg.sender] != 1;
    bool classOnRecord = ghostScShareClassIds;

    _ShareClassManager.transferShares@withrevert(e, p, sc, fromCid, toCid, amount);
    bool reverted = lastReverted;

    assert((callerHoldsNoWard || !classOnRecord) => reverted, "a transfer fails for a non-admin or an unknown share class");
}

// SC-RV-13: an admin's share transfer on a known class succeeds unless a counter overflows.
rule rvScTransferSharesNeverRefusesAWardWhileTheLegsHaveRoom(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint16 fromCid, uint16 toCid, uint128 amount) {

    setupShareClassManagerValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    scShortNetworkIsCounted(fromCid);
    scShortNetworkIsCounted(toCid);

    bool callerIsWard = _ShareClassManager.wards[e.msg.sender] == 1;
    bool classOnRecord = ghostScShareClassIds;
    bool legOversteps = ghostScRevocations256[fromCid] + amount > max_uint256
        || ghostScIssuances256[toCid] + amount > max_uint256;

    _ShareClassManager.transferShares@withrevert(e, p, sc, fromCid, toCid, amount);
    bool reverted = lastReverted;

    assert((callerIsWard && classOnRecord && !legOversteps) => !reverted,
        "an admin's transfer on a known class succeeds unless a counter overflows");
}

// SC-RV-14: a network's issuance query fails when its net issuance does not fit a uint128.
rule rvScIssuanceRefusesANetworkNetPastUint128(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint16 centrifugeId) {

    setupShareClassManagerValidState(e);

    mathint netBefore = ghostScIssuances256[centrifugeId] - ghostScRevocations256[centrifugeId];

    _ShareClassManager.issuance@withrevert(e, p, sc, centrifugeId);
    bool reverted = lastReverted;

    assert(netBefore > max_uint128 => reverted, "the issuance read fails for a net past uint128");
}

// SC-RV-15: a class's total supply query fails when its net does not fit a uint128.
rule rvScTotalIssuanceRefusesAClassNetPastUint128(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc) {

    setupShareClassManagerValidState(e);

    mathint netBefore = SC_TOTAL_ISSUANCE();

    _ShareClassManager.totalIssuance@withrevert(e, p, sc);
    bool reverted = lastReverted;

    assert(netBefore > max_uint128 => reverted, "the supply read fails for a net past uint128");
}

// SC-RV-16: a network's issuance query never fails unless it is in deficit or its net exceeds uint128.
rule rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint16 centrifugeId) {

    setupShareClassManagerValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint issuancesBefore = ghostScIssuances256[centrifugeId];
    mathint revocationsBefore = ghostScRevocations256[centrifugeId];

    _ShareClassManager.issuance@withrevert(e, p, sc, centrifugeId);
    bool reverted = lastReverted;

    assert(revocationsBefore <= issuancesBefore && issuancesBefore - revocationsBefore <= max_uint128 => !reverted,
        "a network's issuance read fails only on a deficit or a net past uint128");
}

// SC-RV-17: a class's total supply query never fails unless it is in deficit or its net exceeds uint128.
rule rvScTotalIssuanceAnswersAClassNeitherInDeficitNorPastUint128(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc) {

    setupShareClassManagerValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint issuancesBefore = ghostScTotalIssuances256;
    mathint revocationsBefore = ghostScTotalRevocations256;

    _ShareClassManager.totalIssuance@withrevert(e, p, sc);
    bool reverted = lastReverted;

    assert(revocationsBefore <= issuancesBefore && issuancesBefore - revocationsBefore <= max_uint128 => !reverted,
        "a class's supply read fails only on a deficit or a net past uint128");
}
