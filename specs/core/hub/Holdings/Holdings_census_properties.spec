import "setup/Holdings_census.spec";
import "../HubRegistry/setup/HubRegistry_cvl.spec";

// --- valid_state ---

// HO-VS-11: a pool's deficit count on a network is the number of its holdings there in shortfall.
invariant networkDeficitCountIsItsNetworksShortRowCensus(env e, Holdings.PoolId p, uint16 c)
    HO_CENSUS_POOL(p) => _Holdings.networkDeficitCount[p][c] == ghostHoCensusShortRows[c]
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO_CN(e, eFunc); } }

// HO-VS-12: a share class's deficit count on a network is the number of its holdings there in shortfall.
invariant deficitCountIsItsClassNetworksShortRowCensus(env e, Holdings.PoolId p, Holdings.ShareClassId sc, uint16 c)
    HO_CENSUS_POOL(p) => _Holdings.deficitCount[p][sc][c] == ghostHoCensusShortRowsSc[sc][c]
filtered { f -> !EXCLUDED_FUNCTION_HO(f) } { preserved with (env eFunc) { SETUP_HO_CN(e, eFunc); } }

// --- reachability ---

// HO-RC-32: a pool can count three holdings of two share classes in shortfall on one network.
rule rcHoCensusReachesThreeShortRowsOnOneNetwork(env e, Holdings.PoolId p, uint16 c, Holdings.ShareClassId sc1,
    Holdings.ShareClassId sc2, Holdings.AssetId aid1, Holdings.AssetId aid2, Holdings.AssetId aid3, uint128 outflow1,
    uint128 outflow2, uint128 outflow3) {

    setupHoldings(e);
    require(HO_CENSUS_POOL(p), "SCOPE: the modelled pool");
    require(HO_ASSET_NETWORK(aid1) == c && HO_ASSET_NETWORK(aid2) == c && HO_ASSET_NETWORK(aid3) == c
        && aid1 != aid2 && sc1 != sc2, "SCOPE: three holdings of two classes on one network");
    require(ghostHoCensusShortRows[c] == 0 && _Holdings.networkDeficitCount[p][c] == 0
        && ghostHoCensusShortRowsSc[sc1][c] == 0 && _Holdings.deficitCount[p][sc1][c] == 0,
        "SCOPE: no holding short on that network before");

    _Holdings.decrease(e, p, sc1, aid1, c, outflow1);
    _Holdings.decrease(e, p, sc1, aid2, c, outflow2);
    _Holdings.decrease(e, p, sc2, aid3, c, outflow3);

    satisfy(ghostHoCensusShortRows[c] == 3 && _Holdings.networkDeficitCount[p][c] == 3
        && ghostHoCensusShortRowsSc[sc1][c] == 2 && _Holdings.deficitCount[p][sc1][c] == 2,
        "the pool's count can reach three and the first class's two");
}
