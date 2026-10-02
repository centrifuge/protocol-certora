import "ShareClassManager_single_pool_valid_state.spec";

// SC-RC-01: a pool can create its first share class, using up its salt.
rule rcScFirstClassCreationIsReachable(env e, ShareClassManager.PoolId p, string name, string symbol,
    bytes32 salt) {

    setupShareClassManagerValidState(e);
    require(name.length == 1 && symbol.length == 1, "SCOPE: a one-character name and symbol");

    mathint countBefore = ghostScShareClassCount32;
    bool classOnRecordBefore = ghostScShareClassIds;
    bool saltClaimedBefore = ghostScSalts[salt];

    _ShareClassManager.addShareClass(e, p, name, symbol, salt);

    mathint countAfter = ghostScShareClassCount32;
    bool classOnRecordAfter = ghostScShareClassIds;
    bool saltClaimedAfter = ghostScSalts[salt];
    bytes32 classSaltAfter = ghostScMetadataSalt;

    satisfy(countBefore == 0 && countAfter == 1 && !classOnRecordBefore && classOnRecordAfter
        && !saltClaimedBefore && saltClaimedAfter && classSaltAfter == salt,
        "a pool's first class can be born, claiming and keeping its salt");
}

// SC-RC-02: a price computed in the current block can be published.
rule rcScPricePublishedAtTheCurrentBlockIsReachable(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, ShareClassManager.D18 price, uint64 computedAt) {

    setupShareClassManagerValidState(e);

    _ShareClassManager.updateSharePrice(e, p, sc, price, computedAt);

    mathint priceAfter = ghostScPricePoolPerShare128;
    mathint stampAfter = ghostScPriceComputedAt64;

    satisfy(priceAfter > 0 && priceAfter == price && stampAfter == e.block.timestamp,
        "a positive price can be published stamped with the current block time");
}

// SC-RC-03: a price computed earlier can be published with its original timestamp.
rule rcScBackdatedPriceKeepsItsOwnStamp(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, ShareClassManager.D18 price, uint64 computedAt) {

    setupShareClassManagerValidState(e);

    _ShareClassManager.updateSharePrice(e, p, sc, price, computedAt);

    mathint priceAfter = ghostScPricePoolPerShare128;
    mathint stampAfter = ghostScPriceComputedAt64;

    satisfy(priceAfter > 0 && priceAfter == price && stampAfter == computedAt
        && stampAfter > 0 && stampAfter < e.block.timestamp,
        "a backdated positive price can be stored under its own stamp");
}

// SC-RC-04: an older price can replace a more recent one.
rule rcScOlderPriceReplacesTheStoredOne(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, ShareClassManager.D18 price, uint64 computedAt) {

    setupShareClassManagerValidState(e);

    mathint priceBefore = ghostScPricePoolPerShare128;
    mathint stampBefore = ghostScPriceComputedAt64;

    _ShareClassManager.updateSharePrice(e, p, sc, price, computedAt);

    mathint priceAfter = ghostScPricePoolPerShare128;
    mathint stampAfter = ghostScPriceComputedAt64;

    satisfy(stampBefore > 0 && stampAfter < stampBefore && priceAfter != priceBefore,
        "a price older than the stored one can replace it");
}

// SC-RC-05: a share class with a positive price can be marked down to zero.
rule rcScPriceCanBeWrittenDownToZero(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, ShareClassManager.D18 price, uint64 computedAt) {

    setupShareClassManagerValidState(e);

    mathint priceBefore = ghostScPricePoolPerShare128;

    _ShareClassManager.updateSharePrice(e, p, sc, price, computedAt);

    mathint priceAfter = ghostScPricePoolPerShare128;

    satisfy(priceBefore > 0 && priceAfter == 0, "a class price can fall from positive to zero");
}

// SC-RC-06: one issuance can take an empty share class to the largest readable supply.
rule rcScClassSupplyCanReachItsStoredCeiling(env e, uint16 cid, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint128 amount) {

    setupShareClassManagerValidState(e);

    mathint totalBefore = SC_TOTAL_ISSUANCE();

    _ShareClassManager.updateShares(e, cid, p, sc, amount, true);

    mathint totalAfter = SC_TOTAL_ISSUANCE();

    satisfy(totalBefore == 0 && totalAfter == max_uint128,
        "an empty class can be issued up to the readable maximum in one call");
}

// SC-RC-07: a network can revoke more than it issued while the class supply stays positive.
rule rcScNetworkRevocationsCanExceedItsIssuances(env e, uint16 cid, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint128 amount) {

    setupShareClassManagerValidState(e);
    require(ghostScRevocations256[cid] == 0, "SCOPE: the network has revoked nothing yet");

    _ShareClassManager.updateShares(e, cid, p, sc, amount, false);

    mathint issuancesAfter = ghostScIssuances256[cid];
    mathint revocationsAfter = ghostScRevocations256[cid];
    mathint totalAfter = SC_TOTAL_ISSUANCE();

    satisfy(issuancesAfter == 0 && revocationsAfter > issuancesAfter && totalAfter > 0,
        "a network that issued nothing can still revoke, with supply above zero");
}

// SC-RC-08: admin rights can be granted and revoked again in one transaction.
rule rcScRelyThenDenyRoundTripIsReachable(env e, address user) {

    setupShareClassManagerValidState(e);

    mathint wardBefore = _ShareClassManager.wards[user];

    _ShareClassManager.rely(e, user);

    mathint wardMid = _ShareClassManager.wards[user];

    _ShareClassManager.deny(e, user);

    mathint wardAfter = _ShareClassManager.wards[user];

    satisfy(wardBefore == 0 && wardMid == 1 && wardAfter == 0, "an account can gain and lose ward rights in one go");
}

// SC-RC-09: a network can go negative by revoking first and recover once its issuance arrives.
rule rcScNegativeNetworkCountOpensAndCloses(env e, uint16 cid, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint128 revoked, uint128 issued) {

    setupShareClassManagerValidState(e);

    mathint countBefore = ghostScNegativeNetworkCount32;

    _ShareClassManager.updateShares(e, cid, p, sc, revoked, false);

    mathint countMid = ghostScNegativeNetworkCount32;

    _ShareClassManager.updateShares(e, cid, p, sc, issued, true);

    mathint countAfter = ghostScNegativeNetworkCount32;

    satisfy(countBefore == 0 && countMid == 1 && countAfter == 0,
        "a revocation can open the short-network count and an issuance close it");
}

// SC-RC-10: a class's total supply query can fail when revocations exceed issuances.
rule rcScRefusedClassSupplyIsReachable(env e, uint16 centrifugeId, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint128 amount) {

    setupShareClassManagerValidState(e);

    _ShareClassManager.updateShares(e, centrifugeId, p, sc, amount, false);

    _ShareClassManager.totalIssuance@withrevert(e, p, sc);
    bool reverted = lastReverted;

    satisfy(reverted && ghostScTotalRevocations256 > ghostScTotalIssuances256
        && ghostScNegativeNetworkCount32 > 0,
        "a class can go short, count a short network and be refused its supply");
}

// SC-RC-11: an issuance can push a network past uint128, so its issuance query fails.
rule rcScNetworkNetPastUint128IsReachable(env e, uint16 cid, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, uint128 amount) {

    setupShareClassManagerValidState(e);

    mathint issuedBefore = ghostScIssuances256[cid];

    _ShareClassManager.updateShares(e, cid, p, sc, amount, true);

    _ShareClassManager.issuance@withrevert(e, p, sc, cid);
    bool reverted = lastReverted;

    satisfy(issuedBefore <= max_uint128 && ghostScIssuances256[cid] > max_uint128
        && ghostScRevocations256[cid] == 0 && reverted,
        "an issuance can push a network past uint128, so its issuance query fails");
}
