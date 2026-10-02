import "ShareClassManager_single_pool_valid_state.spec";

// SC-AC-01: only an admin can grant or revoke admin rights on the share class manager.
rule acScOnlyAWardMovesTheWardSet(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    mathint userWardBefore = _ShareClassManager.wards[user];

    f(e, args);

    mathint userWardAfter = _ShareClassManager.wards[user];

    assert(userWardAfter != userWardBefore => senderWardBefore == 1, "only a ward can grant or revoke ward rights");
}

// SC-AC-02: only an admin can change a pool's share class count.
rule acScOnlyAWardMovesTheClassCounter(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    mathint countBefore = ghostScShareClassCount32;

    f(e, args);

    mathint countAfter = ghostScShareClassCount32;

    assert(countAfter != countBefore => senderWardBefore == 1, "a non-ward never changes how many classes a pool has");
}

// SC-AC-03: only an admin can register or remove a share class.
rule acScOnlyAWardMovesTheClassRoster(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    bool rosterBefore = ghostScShareClassIds;

    f(e, args);

    bool rosterAfter = ghostScShareClassIds;

    assert(rosterAfter != rosterBefore => senderWardBefore == 1,
        "only a ward can change whether the share class exists");
}

// SC-AC-04: only an admin can change whether a salt is marked used.
rule acScOnlyAWardMovesTheSaltRegistry(env e, method f, calldataarg args, bytes32 s)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    bool saltClaimedBefore = ghostScSalts[s];

    f(e, args);

    bool saltClaimedAfter = ghostScSalts[s];

    assert(saltClaimedAfter != saltClaimedBefore => senderWardBefore == 1, "a non-ward never claims or frees a salt");
}

// SC-AC-05: only an admin can change a share class's salt.
rule acScOnlyAWardMovesTheClassSalt(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    bytes32 classSaltBefore = ghostScMetadataSalt;

    f(e, args);

    bytes32 classSaltAfter = ghostScMetadataSalt;

    assert(classSaltAfter != classSaltBefore => senderWardBefore == 1, "a non-ward never rewrites a class's salt");
}

// SC-AC-06: only an admin can change a share class's total issued or revoked shares.
rule acScOnlyAWardMovesTheClassSupply(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    mathint issuedBefore = ghostScTotalIssuances256;
    mathint revokedBefore = ghostScTotalRevocations256;

    f(e, args);

    mathint issuedAfter = ghostScTotalIssuances256;
    mathint revokedAfter = ghostScTotalRevocations256;

    assert((issuedAfter != issuedBefore || revokedAfter != revokedBefore) => senderWardBefore == 1,
        "a non-ward never moves a class's supply counters");
}

// SC-AC-07: only an admin can change the shares recorded as issued on a network.
rule acScOnlyAWardMovesANetworkIssuedTotal(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    mathint issuedBefore = ghostScIssuances256[cid];

    f(e, args);

    mathint issuedAfter = ghostScIssuances256[cid];

    assert(issuedAfter != issuedBefore => senderWardBefore == 1, "only a ward can change a network's issued total");
}

// SC-AC-08: only an admin can change the shares recorded as revoked on a network.
rule acScOnlyAWardMovesANetworkRevokedTotal(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    mathint revokedBefore = ghostScRevocations256[cid];

    f(e, args);

    mathint revokedAfter = ghostScRevocations256[cid];

    assert(revokedAfter != revokedBefore => senderWardBefore == 1, "only a ward can change a network's revoked total");
}

// SC-AC-09: only an admin can change a share class's price.
rule acScOnlyAWardMovesTheSharePrice(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    mathint priceBefore = ghostScPricePoolPerShare128;

    f(e, args);

    mathint priceAfter = ghostScPricePoolPerShare128;

    assert(priceAfter != priceBefore => senderWardBefore == 1, "a non-ward never reprices a share class");
}

// SC-AC-10: only an admin can change the timestamp of a share class's price.
rule acScOnlyAWardMovesThePriceTimestamp(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    mathint priceStampBefore = ghostScPriceComputedAt64;

    f(e, args);

    mathint priceStampAfter = ghostScPriceComputedAt64;

    assert(priceStampAfter != priceStampBefore => senderWardBefore == 1, "a non-ward never restamps a class's price");
}

// SC-AC-11: only an admin can change how many networks have revoked more shares than issued.
rule acScOnlyAWardMovesTheNegativeNetworkCount(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint senderWardBefore = _ShareClassManager.wards[e.msg.sender];
    mathint countBefore = ghostScNegativeNetworkCount32;

    f(e, args);

    mathint countAfter = ghostScNegativeNetworkCount32;

    assert(countAfter != countBefore => senderWardBefore == 1,
        "only a ward can change the count of networks in deficit");
}
