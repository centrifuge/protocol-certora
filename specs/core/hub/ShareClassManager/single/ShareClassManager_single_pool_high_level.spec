import "ShareClassManager_single_pool_valid_state.spec";

// SC-HL-01: equal revocation and issuance on two networks leave the class supply unchanged.
rule hlScCrossChainTransferConservesClassSupply(env e, uint16 origin, uint16 target,
    ShareClassManager.PoolId p, ShareClassManager.ShareClassId sc, uint128 amount) {

    setupShareClassManagerValidState(e);
    require(origin != target, "SCOPE: two distinct networks");

    mathint totalBefore = SC_TOTAL_ISSUANCE();

    _ShareClassManager.updateShares(e, origin, p, sc, amount, false);
    _ShareClassManager.updateShares(e, target, p, sc, amount, true);

    mathint totalAfter = SC_TOTAL_ISSUANCE();

    assert(totalAfter == totalBefore, "a cross-network transfer leaves the class supply unchanged");
}

// SC-HL-02: adding a share class gives it the id previewed just before.
rule hlScCreationHandsOutThePreviewedId(env e, ShareClassManager.PoolId p, calldataarg args) {

    setupShareClassManagerValidState(e);

    ShareClassManager.ShareClassId previewedIdBefore = _ShareClassManager.previewNextShareClassId(e, p);

    ShareClassManager.ShareClassId createdId = _ShareClassManager.addShareClass(e, args);

    assert(createdId == previewedIdBefore, "a new share class gets exactly the id the preview announced");
}

// SC-HL-03: a price update stores exactly the given price and timestamp.
rule hlScRepricingStoresTheGivenPriceAndStamp(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, ShareClassManager.D18 price, uint64 computedAt) {

    setupShareClassManagerValidState(e);

    _ShareClassManager.updateSharePrice(e, p, sc, price, computedAt);

    mathint priceAfter = ghostScPricePoolPerShare128;
    mathint priceStampAfter = ghostScPriceComputedAt64;

    assert(priceAfter == price && priceStampAfter == computedAt,
        "the stored price and stamp are exactly the ones passed in");
}

// SC-HL-04: a new share class's id matches the preview for its position in the pool.
rule hlScCreationMatchesTheIndexedPreview(env e, ShareClassManager.PoolId p, string name, string symbol,
    bytes32 salt) {

    setupShareClassManagerValidState(e);

    ShareClassManager.ShareClassId createdId = _ShareClassManager.addShareClass(e, p, name, symbol, salt);

    mathint countAfter = ghostScShareClassCount32;
    ShareClassManager.ShareClassId previewedAtIndex =
        _ShareClassManager.previewShareClassId(e, p, require_uint32(countAfter));

    assert(createdId == previewedAtIndex, "a new class's id is the one the preview gives for its index");
}

// SC-HL-05: a share update adds its amount only to the matching network and class totals.
rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass(env e, uint16 cid, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint128 amount, bool isIssuance, uint16 other) {

    setupShareClassManagerValidState(e);
    require(other != cid, "SCOPE: a network other than the updated one");

    mathint networkIssuedBefore = ghostScIssuances256[cid];
    mathint networkRevokedBefore = ghostScRevocations256[cid];
    mathint classIssuedBefore = ghostScTotalIssuances256;
    mathint classRevokedBefore = ghostScTotalRevocations256;
    mathint otherIssuedBefore = ghostScIssuances256[other];
    mathint otherRevokedBefore = ghostScRevocations256[other];

    _ShareClassManager.updateShares(e, cid, p, sc, amount, isIssuance);

    mathint networkIssuedAfter = ghostScIssuances256[cid];
    mathint networkRevokedAfter = ghostScRevocations256[cid];
    mathint classIssuedAfter = ghostScTotalIssuances256;
    mathint classRevokedAfter = ghostScTotalRevocations256;

    assert(isIssuance
            ? (networkIssuedAfter == networkIssuedBefore + amount
                && classIssuedAfter == classIssuedBefore + amount
                && networkRevokedAfter == networkRevokedBefore && classRevokedAfter == classRevokedBefore)
            : (networkRevokedAfter == networkRevokedBefore + amount
                && classRevokedAfter == classRevokedBefore + amount
                && networkIssuedAfter == networkIssuedBefore && classIssuedAfter == classIssuedBefore),
        "an update raises only its own leg of network and class, by the amount");
    assert(ghostScIssuances256[other] == otherIssuedBefore
        && ghostScRevocations256[other] == otherRevokedBefore,
        "a supply update leaves any other network's ledger untouched");
}

// SC-HL-06: reported supply, in total and per network, is shares issued minus revoked.
rule hlScSupplyViewsReportIssuedMinusRevoked(env e, uint16 cid, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc) {

    setupShareClassManagerValidState(e);

    mathint reportedClassSupply = _ShareClassManager.totalIssuance(e, p, sc);
    mathint reportedNetworkNet = _ShareClassManager.issuance(e, p, sc, cid);

    assert(reportedClassSupply == SC_TOTAL_ISSUANCE()
        && reportedNetworkNet == ghostScIssuances256[cid] - ghostScRevocations256[cid],
        "the supply views of class and network report issued minus revoked");
}

// SC-HL-07: two different pool and index pairs never get the same share class id.
rule hlScShareClassIdIsInjectiveInPoolAndIndex(env e, ShareClassManager.PoolId p1, uint32 i1,
    ShareClassManager.PoolId p2, uint32 i2) {

    ShareClassManager.ShareClassId id1 = _ShareClassManager.previewShareClassId(e, p1, i1);
    ShareClassManager.ShareClassId id2 = _ShareClassManager.previewShareClassId(e, p2, i2);

    assert((p1 != p2 || i1 != i2) => id1 != id2, "each pool and index yields its own class id");
}

// SC-HL-11: a supply update moves only its class's issued or revoked sum over every network, by its amount.
rule hlScAnUpdateMovesItsLegByItsAmount(env e, uint16 cid, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint128 amount, bool isIssuance) {

    setupShareClassManager(e);

    mathint issuedBefore = SC_ISSUANCES_SUM();
    mathint revokedBefore = SC_REVOCATIONS_SUM();

    _ShareClassManager.updateShares(e, cid, p, sc, amount, isIssuance);

    mathint issuedMove = SC_ISSUANCES_SUM() - issuedBefore;
    mathint revokedMove = SC_REVOCATIONS_SUM() - revokedBefore;

    assert(isIssuance ? issuedMove == amount && revokedMove == 0 : revokedMove == amount && issuedMove == 0,
        "only the named side of the class moves, by exactly the amount");
}

// SC-HL-12: a share transfer only revokes on the origin network and issues on the target.
rule hlScTransferSharesMovesOnlyTheTwoNetworkLegs(env e, ShareClassManager.PoolId p, ShareClassManager.ShareClassId sc,
    uint16 fromCid, uint16 toCid, uint128 amount, uint16 other) {

    setupShareClassManagerValidState(e);
    require(other != fromCid && other != toCid, "SCOPE: a network outside the transfer");

    mathint fromRevokedBefore = ghostScRevocations256[fromCid];
    mathint fromIssuedBefore = ghostScIssuances256[fromCid];
    mathint toIssuedBefore = ghostScIssuances256[toCid];
    mathint toRevokedBefore = ghostScRevocations256[toCid];
    mathint classIssuedBefore = ghostScTotalIssuances256;
    mathint classRevokedBefore = ghostScTotalRevocations256;
    mathint otherIssuedBefore = ghostScIssuances256[other];
    mathint otherRevokedBefore = ghostScRevocations256[other];

    _ShareClassManager.transferShares(e, p, sc, fromCid, toCid, amount);

    assert(ghostScRevocations256[fromCid] == fromRevokedBefore + amount
        && ghostScIssuances256[toCid] == toIssuedBefore + amount
        && (fromCid != toCid => ghostScIssuances256[fromCid] == fromIssuedBefore
            && ghostScRevocations256[toCid] == toRevokedBefore),
        "a transfer revokes on the origin and issues on the target, by the amount");
    assert(ghostScTotalIssuances256 == classIssuedBefore && ghostScTotalRevocations256 == classRevokedBefore,
        "a transfer leaves the class totals unchanged");
    assert(ghostScIssuances256[other] == otherIssuedBefore && ghostScRevocations256[other] == otherRevokedBefore,
        "a transfer leaves any other network's ledger untouched");
}
