import "setup/Holdings_multi_share_class.spec";
import "../HubRegistry/setup/HubRegistry_cvl.spec";

// --- valid_state ---

function setupHoldingsMultiShareClassValidState(env e) {
    setupHoldingsMultiShareClass(e);
    requireInvariant networkDeficitCountSpansEveryShareClass(e);
    requireInvariant deficitCountIsKeptPerShareClass(e);
}

// HO-VS-07: a pool's deficit count on a network includes shortfalls from every share class.
invariant networkDeficitCountSpansEveryShareClass(env e)
    ghostHoClassNetworkDeficitCount32 == HO_CLASS_DEFICIT_CARDINALITY()
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO_MC(e, eFunc); } }

// HO-VS-09: each share class's deficit count covers only its own holdings in shortfall.
invariant deficitCountIsKeptPerShareClass(env e)
    ghostHoClassDeficitCount32[ghostShareClassA] == HO_SHARE_CLASS_DEFICIT_CARDINALITY(ghostShareClassA)
    && ghostHoClassDeficitCount32[ghostShareClassB] == HO_SHARE_CLASS_DEFICIT_CARDINALITY(ghostShareClassB)
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO_MC(e, eFunc); } }

// --- state_transitions ---

// HO-ST-12: a deposit or withdrawal on one share class leaves another's amounts unchanged.
rule stHoFlowRowIsPerShareClass(env e, method f, calldataarg args, bytes16 sc, bytes16 other, uint128 a, uint128 b)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsMultiShareClass(e);
    require(VALID_SC(sc) && VALID_SC(other) && sc != other, "SCOPE: two distinct share classes");

    mathint increasedBefore = ghostHoClassIncreasedAmount256[sc][a];
    mathint decreasedBefore = ghostHoClassDecreasedAmount256[sc][a];
    mathint otherIncreasedBefore = ghostHoClassIncreasedAmount256[other][b];
    mathint otherDecreasedBefore = ghostHoClassDecreasedAmount256[other][b];

    f(e, args);

    assert(ghostHoClassIncreasedAmount256[sc][a] != increasedBefore
        || ghostHoClassDecreasedAmount256[sc][a] != decreasedBefore
        => ghostHoClassIncreasedAmount256[other][b] == otherIncreasedBefore
            && ghostHoClassDecreasedAmount256[other][b] == otherDecreasedBefore,
        "a flow on one share class leaves the other class's flows alone");
}

// HO-ST-13: a call changing any part of one class's holding leaves the other class's holdings unchanged.
rule stHoHoldingRowIsPerShareClass(env e, method f, calldataarg args, bytes16 sc, bytes16 other, uint128 a,
    uint128 b, uint8 k, uint8 j) filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsMultiShareClass(e);
    require(VALID_SC(sc) && VALID_SC(other) && sc != other, "SCOPE: two distinct share classes");

    mathint increasedBefore = ghostHoClassIncreasedAmount256[sc][a];
    mathint decreasedBefore = ghostHoClassDecreasedAmount256[sc][a];
    mathint valueBefore = ghostHoClassAssetAmountValue128[sc][a];
    address valuationBefore = ghostHoClassValuation[sc][a];
    mathint accountBefore = ghostHoClassAccountId256[sc][a][k];

    mathint otherIncreasedBefore = ghostHoClassIncreasedAmount256[other][b];
    mathint otherDecreasedBefore = ghostHoClassDecreasedAmount256[other][b];
    mathint otherValueBefore = ghostHoClassAssetAmountValue128[other][b];
    address otherValuationBefore = ghostHoClassValuation[other][b];
    mathint otherAccountBefore = ghostHoClassAccountId256[other][b][j];

    f(e, args);

    bool moved = ghostHoClassIncreasedAmount256[sc][a] != increasedBefore
        || ghostHoClassDecreasedAmount256[sc][a] != decreasedBefore
        || ghostHoClassAssetAmountValue128[sc][a] != valueBefore
        || ghostHoClassValuation[sc][a] != valuationBefore
        || ghostHoClassAccountId256[sc][a][k] != accountBefore;

    assert(moved => ghostHoClassIncreasedAmount256[other][b] == otherIncreasedBefore
        && ghostHoClassDecreasedAmount256[other][b] == otherDecreasedBefore
        && ghostHoClassAssetAmountValue128[other][b] == otherValueBefore
        && ghostHoClassValuation[other][b] == otherValuationBefore
        && ghostHoClassAccountId256[other][b][j] == otherAccountBefore,
        "a call changes the holdings of at most one share class");
}

// HO-ST-15: a call changing one class's snapshot on a network leaves another class's snapshot there unchanged.
rule stHoSnapshotRowIsPerShareClass(env e, method f, calldataarg args, bytes16 sc, bytes16 other, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsMultiShareClass(e);
    require(VALID_SC(sc) && VALID_SC(other) && sc != other, "SCOPE: two distinct share classes");

    bool markerBefore = ghostHoClassIsSnapshot[sc][cid];
    mathint nonceBefore = ghostHoClassSnapshotNonce64[sc][cid];
    bool otherMarkerBefore = ghostHoClassIsSnapshot[other][cid];
    mathint otherNonceBefore = ghostHoClassSnapshotNonce64[other][cid];

    f(e, args);

    assert(ghostHoClassIsSnapshot[sc][cid] != markerBefore || ghostHoClassSnapshotNonce64[sc][cid] != nonceBefore
        => ghostHoClassIsSnapshot[other][cid] == otherMarkerBefore
            && ghostHoClassSnapshotNonce64[other][cid] == otherNonceBefore,
        "a call changes one network's snapshot in at most one share class");
}

// --- high_level ---

// HO-HL-17: setting a snapshot bumps its class's nonce and moves no other class's snapshot on that network.
rule hlHoSetSnapshotBumpsTheNamedClassesNonce(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.ShareClassId other, uint16 cid, bool isSnapshot, uint64 nonce) {

    setupHoldingsMultiShareClass(e);
    require(VALID_SC(sc) && VALID_SC(other) && sc != other, "SCOPE: two distinct share classes");

    mathint nonceBefore = ghostHoClassSnapshotNonce64[sc][cid];
    mathint otherNonceBefore = ghostHoClassSnapshotNonce64[other][cid];
    bool otherMarkerBefore = ghostHoClassIsSnapshot[other][cid];

    _Holdings.setSnapshot(e, p, sc, cid, isSnapshot, nonce);

    assert(ghostHoClassSnapshotNonce64[sc][cid] == nonceBefore + 1
        && ghostHoClassSnapshotNonce64[other][cid] == otherNonceBefore
        && ghostHoClassIsSnapshot[other][cid] == otherMarkerBefore,
        "the named class's nonce rises by one, the other class's snapshot stays");
}

// --- reverts ---

// HO-RV-15: an admin's inflow to an unopened holding fails only on overflow, even if another class is short.
rule rvHoIncreaseBeforeOpeningIsNeverRefusedOverASiblingClassShortfall(env e, Holdings.PoolId p,
    Holdings.ShareClassId sc, Holdings.AssetId aid, uint16 cid, uint128 amount) {

    setupHoldingsMultiShareClassValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    require(_Holdings.wards[e.msg.sender] == 1, "SCOPE: the caller is a ward");
    require(!_Holdings.isInitialized(e, p, sc, aid), "SCOPE: a holding not yet opened, no price read");
    require(ghostHoClassIncreasedAmount256[sc][aid] + amount <= max_uint256, "SCOPE: no deposit-total overflow");

    _Holdings.increase@withrevert(e, p, sc, aid, cid, amount);

    assert(!lastReverted, "a ward's deposit before opening never fails, sibling short or not");
}

// --- reachability ---

// HO-RC-27: two share classes of a pool can both be in shortfall on one network at once.
rule rcHoTwoShareClassesShortOnOneNetworkIsReachable(env e, Holdings.PoolId p, Holdings.ShareClassId sc1,
    Holdings.ShareClassId sc2, Holdings.AssetId aid, uint16 cid, uint128 outflow1, uint128 outflow2) {

    setupHoldingsMultiShareClassValidState(e);
    require(VALID_SC(sc1) && VALID_SC(sc2) && sc1 != sc2, "SCOPE: two distinct share classes");

    mathint rollupBefore = ghostHoClassNetworkDeficitCount32;

    _Holdings.decrease(e, p, sc1, aid, cid, outflow1);
    _Holdings.decrease(e, p, sc2, aid, cid, outflow2);

    satisfy(rollupBefore == 0 && ghostHoClassNetworkDeficitCount32 == 2
        && ghostHoClassDeficitCount32[sc1] == 1 && ghostHoClassDeficitCount32[sc2] == 1,
        "both share classes can be short on one network, the pool count at two");
}
