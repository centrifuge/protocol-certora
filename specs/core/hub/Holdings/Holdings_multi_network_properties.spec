import "setup/Holdings_multi_network.spec";
import "../HubRegistry/setup/HubRegistry_cvl.spec";

// --- valid_state ---

// HO-VS-10: summed over networks, the deficit counts match the holdings in shortfall.
invariant deficitCountsSumToTheShortRowsAcrossTheNetworks(env e)
    ghostHoNetNetworkDeficitCount32[ghostHoCid16]
        + ghostHoNetNetworkDeficitCount32[ghostHoCid16Other] == HO_NET_DEFICIT_CARDINALITY()
    && ghostHoNetDeficitCount32[ghostHoCid16]
        + ghostHoNetDeficitCount32[ghostHoCid16Other] == HO_NET_DEFICIT_CARDINALITY()
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO_MN(e, eFunc); } }

// --- state_transitions ---

// HO-ST-14: a call moves the deficit counts of at most one network.
rule stHoDeficitCountsOfAtMostOneNetworkMovePerCall(env e, method f, calldataarg args, uint16 cid, uint16 other)
    filtered { f -> !EXCLUDED_FUNCTION_HO(f) } {

    setupHoldingsMultiNetwork(e);
    require(HO_NET_PAIR(cid, other), "SCOPE: the two modelled networks");

    mathint rollupBefore = ghostHoNetNetworkDeficitCount32[cid];
    mathint classBefore = ghostHoNetDeficitCount32[cid];
    mathint otherRollupBefore = ghostHoNetNetworkDeficitCount32[other];
    mathint otherClassBefore = ghostHoNetDeficitCount32[other];

    f(e, args);

    assert(ghostHoNetNetworkDeficitCount32[cid] != rollupBefore || ghostHoNetDeficitCount32[cid] != classBefore
        => ghostHoNetNetworkDeficitCount32[other] == otherRollupBefore
            && ghostHoNetDeficitCount32[other] == otherClassBefore,
        "a call moves the deficit counts of at most one network");
}

// --- high_level ---

// HO-HL-14: a new shortfall raises the deficit counts of the withdrawal's network only.
rule hlHoEnteringADeficitBooksTheNamedNetworkOnly(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount, uint16 other) {

    setupHoldingsMultiNetwork(e);
    require(HO_NET_PAIR(cid, other), "SCOPE: the named network and the other modelled one");

    mathint namedRollupBefore = ghostHoNetNetworkDeficitCount32[cid];
    mathint namedClassBefore = ghostHoNetDeficitCount32[cid];
    mathint otherRollupBefore = ghostHoNetNetworkDeficitCount32[other];
    mathint otherClassBefore = ghostHoNetDeficitCount32[other];
    bool wasShort = ghostHoNetDecreasedAmount256[aid] > ghostHoNetIncreasedAmount256[aid];

    _Holdings.decrease(e, p, sc, aid, cid, amount);

    bool isShort = ghostHoNetDecreasedAmount256[aid] > ghostHoNetIncreasedAmount256[aid];
    mathint step = (!wasShort && isShort) ? 1 : 0;

    assert(ghostHoNetNetworkDeficitCount32[cid] == namedRollupBefore + step
        && ghostHoNetDeficitCount32[cid] == namedClassBefore + step,
        "a new shortfall adds one to the named network's counts, else none");
    assert(ghostHoNetNetworkDeficitCount32[other] == otherRollupBefore
        && ghostHoNetDeficitCount32[other] == otherClassBefore,
        "a withdrawal leaves the other network's deficit counts alone");
}

// HO-HL-15: an ended shortfall lowers the deficit counts of the deposit's network only.
rule hlHoLeavingADeficitReleasesTheNamedNetworkOnly(env e, Holdings.PoolId p, Holdings.ShareClassId sc,
    Holdings.AssetId aid, uint16 cid, uint128 amount, uint16 other) {

    setupHoldingsMultiNetwork(e);
    require(HO_NET_PAIR(cid, other), "SCOPE: the named network and the other modelled one");

    mathint namedRollupBefore = ghostHoNetNetworkDeficitCount32[cid];
    mathint namedClassBefore = ghostHoNetDeficitCount32[cid];
    mathint otherRollupBefore = ghostHoNetNetworkDeficitCount32[other];
    mathint otherClassBefore = ghostHoNetDeficitCount32[other];
    bool wasShort = ghostHoNetDecreasedAmount256[aid] > ghostHoNetIncreasedAmount256[aid];

    _Holdings.increase(e, p, sc, aid, cid, amount);

    bool isShort = ghostHoNetDecreasedAmount256[aid] > ghostHoNetIncreasedAmount256[aid];
    mathint step = (wasShort && !isShort) ? -1 : 0;

    assert(ghostHoNetNetworkDeficitCount32[cid] == namedRollupBefore + step
        && ghostHoNetDeficitCount32[cid] == namedClassBefore + step,
        "a cleared shortfall drops the named network's counts by one, else none");
    assert(ghostHoNetNetworkDeficitCount32[other] == otherRollupBefore
        && ghostHoNetDeficitCount32[other] == otherClassBefore,
        "a deposit leaves the other network's deficit counts alone");
}

// --- reverts ---

// HO-RV-14: a deposit ending a shortfall fails if its network has no shortfall counted.
rule rvHoLeavingADeficitIsRefusedWhenTheNamedNetworkCountsNone(env e, Holdings.PoolId p,
    Holdings.ShareClassId sc, Holdings.AssetId aid, uint128 outflow, uint128 inflow) {

    setupHoldingsMultiNetwork(e);
    require(ghostHoNetDecreasedAmount256[aid] <= ghostHoNetIncreasedAmount256[aid],
        "SCOPE: the holding is not yet short");

    _Holdings.decrease(e, p, sc, aid, ghostHoCid16, outflow);

    require(ghostHoNetDecreasedAmount256[aid] > ghostHoNetIncreasedAmount256[aid],
        "SCOPE: the first withdrawal leaves the holding short");

    mathint classCountBefore = ghostHoNetDeficitCount32[ghostHoCid16Other];
    mathint rollupCountBefore = ghostHoNetNetworkDeficitCount32[ghostHoCid16Other];
    bool leavesShortfall = ghostHoNetDecreasedAmount256[aid]
        <= ghostHoNetIncreasedAmount256[aid] + inflow;

    _Holdings.increase@withrevert(e, p, sc, aid, ghostHoCid16Other, inflow);
    bool reverted = lastReverted;

    assert((leavesShortfall && (classCountBefore == 0 || rollupCountBefore == 0)) => reverted,
        "clearing a shortfall under a network with a zero deficit count fails");
}

// --- reachability ---

// HO-RC-28: a shortfall can stay counted on a network after a deposit elsewhere clears it.
rule rcHoShortfallAttributionCanOutliveItsNetworkIsReachable(env e, Holdings.PoolId p,
    Holdings.ShareClassId sc, Holdings.AssetId aid1, Holdings.AssetId aid2, uint128 outflow1,
    uint128 outflow2, uint128 inflow) {

    setupHoldingsMultiNetwork(e);
    require(ghostHoNetNetworkDeficitCount32[ghostHoCid16] == 0
        && ghostHoNetNetworkDeficitCount32[ghostHoCid16Other] == 0
        && ghostHoNetDeficitCount32[ghostHoCid16] == 0
        && ghostHoNetDeficitCount32[ghostHoCid16Other] == 0
        && ghostHoNetDecreasedAmount256[aid1] <= ghostHoNetIncreasedAmount256[aid1]
        && ghostHoNetDecreasedAmount256[aid2] <= ghostHoNetIncreasedAmount256[aid2],
        "SCOPE: no holding short, no deficit counted yet");

    _Holdings.decrease(e, p, sc, aid2, ghostHoCid16Other, outflow1);

    mathint otherClassMid = ghostHoNetDeficitCount32[ghostHoCid16Other];
    mathint otherRollupMid = ghostHoNetNetworkDeficitCount32[ghostHoCid16Other];

    _Holdings.decrease(e, p, sc, aid1, ghostHoCid16, outflow2);

    mathint namedClassMid = ghostHoNetDeficitCount32[ghostHoCid16];
    mathint namedRollupMid = ghostHoNetNetworkDeficitCount32[ghostHoCid16];

    _Holdings.increase(e, p, sc, aid1, ghostHoCid16Other, inflow);

    satisfy(otherClassMid == 1 && otherRollupMid == 1 && namedClassMid == 1 && namedRollupMid == 1
        && ghostHoNetDeficitCount32[ghostHoCid16] == 1
        && ghostHoNetNetworkDeficitCount32[ghostHoCid16] == 1
        && ghostHoNetDeficitCount32[ghostHoCid16Other] == 0
        && ghostHoNetNetworkDeficitCount32[ghostHoCid16Other] == 0
        && ghostHoNetDecreasedAmount256[aid2] > ghostHoNetIncreasedAmount256[aid2]
        && ghostHoNetDecreasedAmount256[aid1] <= ghostHoNetIncreasedAmount256[aid1],
        "a shortfall cleared via another network can stay counted where booked");
}
