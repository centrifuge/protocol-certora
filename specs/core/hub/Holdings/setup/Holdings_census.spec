// Holdings, census lane. Setup: per-network count of pool A's holdings in shortfall.

// Own setup: counts pool A's shortfall rows over any class and network; the other lanes hook those amounts pinned.

import "Holdings_base.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/single_share_class.spec";

// SCOPE: only pool A counted, over any class, asset and network.
definition HO_CENSUS_POOL(uint64 p) returns bool =
    p == ghostPoolA64;

// SAFE: twin of AssetId.centrifugeId, the asset id's top two bytes.
definition HO_ASSET_NETWORK(uint128 a) returns mathint =
    a / 2^112;

persistent ghost mapping(uint16 => mathint) ghostHoCensusShortRows {
    init_state axiom forall uint16 c. ghostHoCensusShortRows[c] == 0;
}

persistent ghost mapping(bytes16 => mapping(uint16 => mathint)) ghostHoCensusShortRowsSc {
    init_state axiom forall bytes16 sc. forall uint16 c. ghostHoCensusShortRowsSc[sc][c] == 0;
}

persistent ghost mathint ghostHoCensusRowNetwork;

function hoCensusMove(bytes16 sc, uint128 a, bool wasShort, bool isShort) {
    uint16 c = require_uint16(HO_ASSET_NETWORK(a));
    ghostHoCensusRowNetwork = c;
    mathint delta = (isShort ? 1 : 0) - (wasShort ? 1 : 0);
    ghostHoCensusShortRows[c] = ghostHoCensusShortRows[c] + delta;
    ghostHoCensusShortRowsSc[sc][c] = ghostHoCensusShortRowsSc[sc][c] + delta;
}

persistent ghost mapping(bytes16 => mapping(uint128 => mathint)) ghostHoCensusIncreasedAmount256 {
    init_state axiom forall bytes16 sc. forall uint128 a. ghostHoCensusIncreasedAmount256[sc][a] == 0;
    axiom forall bytes16 sc. forall uint128 a.
        ghostHoCensusIncreasedAmount256[sc][a] >= 0 && ghostHoCensusIncreasedAmount256[sc][a] <= max_uint256;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount {
    require(HO_CENSUS_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHoCensusIncreasedAmount256[sc][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount uint256 val (uint256 held) {
    require(HO_CENSUS_POOL(p), "SCOPE: modelled pools stand for any");
    hoCensusMove(sc, aid, ghostHoCensusDecreasedAmount256[sc][aid] > held,
        ghostHoCensusDecreasedAmount256[sc][aid] > val);
    ghostHoCensusIncreasedAmount256[sc][aid] = val;
}

persistent ghost mapping(bytes16 => mapping(uint128 => mathint)) ghostHoCensusDecreasedAmount256 {
    init_state axiom forall bytes16 sc. forall uint128 a. ghostHoCensusDecreasedAmount256[sc][a] == 0;
    axiom forall bytes16 sc. forall uint128 a.
        ghostHoCensusDecreasedAmount256[sc][a] >= 0 && ghostHoCensusDecreasedAmount256[sc][a] <= max_uint256;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount {
    require(HO_CENSUS_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHoCensusDecreasedAmount256[sc][aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount uint256 val (uint256 held) {
    require(HO_CENSUS_POOL(p), "SCOPE: modelled pools stand for any");
    hoCensusMove(sc, aid, held > ghostHoCensusIncreasedAmount256[sc][aid],
        val > ghostHoCensusIncreasedAmount256[sc][aid]);
    ghostHoCensusDecreasedAmount256[sc][aid] = val;
}

function SETUP_HO_CN(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupHoldings(e);
}

// A crossing books the class counter first; the pool counter's key stays unpinned, so the pool census still checks it.
hook Sstore _Holdings.deficitCount[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 c] uint32 val {
    require(HO_CENSUS_POOL(p), "SCOPE: modelled pools stand for any");
    require(c == ghostHoCensusRowNetwork, "TRUSTED: the hub reports an asset on its own network");
}
