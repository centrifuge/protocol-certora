import "setup/ShareClassManager_unpinned.spec";

// --- valid_state ---

// SC-VS-24: a registered share class id carries its own pool and an index from one to the pool's class count.
invariant recordedClassIdSitsUnderItsPoolWithinCount(ShareClassManager.PoolId p, ShareClassManager.ShareClassId sc,
    ShareClassManager.PoolId q, uint64 i)
    (_ShareClassManager.shareClassIds[p][sc] && sc == NEW_SHARE_CLASS_ID_SC_CVL(q, i))
        => (p == q && i >= 1 && i <= _ShareClassManager.shareClassCount[p])
filtered { f -> !EXCLUDED_FUNCTION_SC(f) }

// SC-VS-25: a share class id is registered under at most one pool.
invariant classIdIsOnRecordUnderOnePoolOnly(ShareClassManager.PoolId p, ShareClassManager.PoolId p2,
    ShareClassManager.ShareClassId sc, ShareClassManager.PoolId q, uint64 i)
    (_ShareClassManager.shareClassIds[p][sc] && _ShareClassManager.shareClassIds[p2][sc]
        && sc == NEW_SHARE_CLASS_ID_SC_CVL(q, i)) => p == p2
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {
    preserved {
        requireInvariant recordedClassIdSitsUnderItsPoolWithinCount(p, sc, q, i);
        requireInvariant recordedClassIdSitsUnderItsPoolWithinCount(p2, sc, q, i);
    }
}

// --- state_transitions ---

// SC-ST-08: a registered share class stays registered under its pool through every call.
rule stScRecordedClassStaysRecorded(env e, method f, calldataarg args, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc) filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManagerUnpinned(e);

    bool recordedBefore = _ShareClassManager.shareClassIds[p][sc];

    f(e, args);

    assert(recordedBefore => _ShareClassManager.shareClassIds[p][sc], "no call ever unregisters a share class");
}

// --- high_level ---

// SC-HL-08: adding a share class bumps the pool's count and registers the next index's id, unregistered before.
rule hlScCreationMintsTheNextFreshIndex(env e, ShareClassManager.PoolId p, string name, string symbol, bytes32 salt) {

    setupShareClassManagerUnpinned(e);

    mathint countBefore = _ShareClassManager.shareClassCount[p];
    require(countBefore < max_uint32, "SAFE: a full class counter makes creation revert");
    ShareClassManager.ShareClassId next = _ShareClassManager.previewShareClassId(e, p, assert_uint32(countBefore + 1));
    requireInvariant recordedClassIdSitsUnderItsPoolWithinCount(p, next, p, assert_uint64(countBefore + 1));
    bool nextOnRecordBefore = _ShareClassManager.shareClassIds[p][next];

    ShareClassManager.ShareClassId createdId = _ShareClassManager.addShareClass(e, p, name, symbol, salt);

    assert(!nextOnRecordBefore && _ShareClassManager.shareClassCount[p] == countBefore + 1
            && createdId == next && _ShareClassManager.shareClassIds[p][createdId],
        "registers the next index's id, new to the pool, and counts it");
}

// SC-HL-09: a share class id is its pool in the high eight bytes over its index, zero only when both are zero.
rule hlScClassIdIsThePoolOverTheIndex(env e, ShareClassManager.PoolId p, uint32 i) {

    setupShareClassManagerUnpinned(e);

    ShareClassManager.ShareClassId id = _ShareClassManager.previewShareClassId(e, p, i);

    assert(id == NEW_SHARE_CLASS_ID_SC_CVL(p, i) && ((p != 0 || i != 0) => id != to_bytes16(0)),
        "pool in the top eight bytes, index below, zero only if both are");
}

// SC-HL-10: updateMetadata rewrites only the named class's name and symbol; every other field reads the same.
rule hlScUpdateMetadataWritesOnlyItsClassesStrings(env e, ShareClassManager.PoolId p, ShareClassManager.ShareClassId sc,
    string name, string symbol, ShareClassManager.PoolId q, ShareClassManager.ShareClassId sc2, bytes32 s, uint16 cid,
    address who) {

    setupShareClassManagerUnpinned(e);

    bool saltUsedBefore = _ShareClassManager.salts[s];
    uint32 countBefore = _ShareClassManager.shareClassCount[q];
    bool recordedBefore = _ShareClassManager.shareClassIds[q][sc2];
    ShareClassManager.D18 priceBefore = _ShareClassManager.pricePoolPerShare[q][sc2].price;
    uint64 computedAtBefore = _ShareClassManager.pricePoolPerShare[q][sc2].computedAt;
    uint32 negativeBefore = _ShareClassManager.negativeNetworkCount[q][sc2];
    uint256 totalIssuedBefore = _ShareClassManager.issuanceAcrossNetworks[q][sc2].issuances;
    uint256 totalRevokedBefore = _ShareClassManager.issuanceAcrossNetworks[q][sc2].revocations;
    uint256 networkIssuedBefore = _ShareClassManager.issuancePerNetwork[q][sc2][cid].issuances;
    uint256 networkRevokedBefore = _ShareClassManager.issuancePerNetwork[q][sc2][cid].revocations;
    uint256 wardBefore = _ShareClassManager.wards[who];
    string nameBefore;
    string symbolBefore;
    bytes32 classSaltBefore;
    nameBefore, symbolBefore, classSaltBefore = _ShareClassManager.metadata(e, q, sc2);
    require(nameBefore.length <= 128 && symbolBefore.length <= 32, "SAFE: every metadata write caps the name and symbol lengths");

    _ShareClassManager.updateMetadata(e, p, sc, name, symbol);

    string nameAfter;
    string symbolAfter;
    bytes32 classSaltAfter;
    nameAfter, symbolAfter, classSaltAfter = _ShareClassManager.metadata(e, q, sc2);

    assert(_ShareClassManager.salts[s] == saltUsedBefore && _ShareClassManager.shareClassCount[q] == countBefore
            && _ShareClassManager.shareClassIds[q][sc2] == recordedBefore
            && _ShareClassManager.pricePoolPerShare[q][sc2].price == priceBefore
            && _ShareClassManager.pricePoolPerShare[q][sc2].computedAt == computedAtBefore
            && _ShareClassManager.negativeNetworkCount[q][sc2] == negativeBefore
            && _ShareClassManager.issuanceAcrossNetworks[q][sc2].issuances == totalIssuedBefore
            && _ShareClassManager.issuanceAcrossNetworks[q][sc2].revocations == totalRevokedBefore
            && _ShareClassManager.issuancePerNetwork[q][sc2][cid].issuances == networkIssuedBefore
            && _ShareClassManager.issuancePerNetwork[q][sc2][cid].revocations == networkRevokedBefore
            && _ShareClassManager.wards[who] == wardBefore && classSaltAfter == classSaltBefore
            && ((q != p || sc2 != sc) => (keccak256(nameAfter) == keccak256(nameBefore)
                && keccak256(symbolAfter) == keccak256(symbolBefore))),
        "a rename moves nothing but the named class's name and symbol");
}

// --- reverts ---

// SC-RV-11: a metadata update fails for a non-admin, an unknown class, or an empty or too-long name or symbol.
rule rvScUpdateMetadataRefusesANonWardAnUnknownClassOrBadLengths(env e, ShareClassManager.PoolId p,
    ShareClassManager.ShareClassId sc, string name, string symbol) {

    bool callerHoldsNoWard = _ShareClassManager.wards[e.msg.sender] != 1;
    bool classOnRecord = _ShareClassManager.shareClassIds[p][sc];
    mathint nameLength = name.length;
    mathint symbolLength = symbol.length;

    _ShareClassManager.updateMetadata@withrevert(e, p, sc, name, symbol);
    bool reverted = lastReverted;

    assert((callerHoldsNoWard || !classOnRecord || nameLength == 0 || nameLength > 128
            || symbolLength == 0 || symbolLength > 32) => reverted,
        "a non-ward, an unknown class, or a blank or oversize name or symbol blocks renaming");
}
