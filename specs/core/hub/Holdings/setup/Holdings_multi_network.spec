// Holdings, two-network lane. Setup: deficit counters per network, one pool and class.

// Own setup: a second network keys the deficit counters; single_pool hooks the same counters for one network.

import "Holdings_base.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/single_share_class.spec";

// UNSAFE: two networks only, a third reaches no mirrored bucket.
persistent ghost uint16 ghostHoCid16Other;

definition HO_NET_SLOT(uint16 c) returns bool =
    c == ghostHoCid16 || c == ghostHoCid16Other;

definition HO_NET_PAIR(uint16 c, uint16 d) returns bool =
    (c == ghostHoCid16 && d == ghostHoCid16Other) || (c == ghostHoCid16Other && d == ghostHoCid16);

persistent ghost mapping(uint16 => mathint) ghostHoNetNetworkDeficitCount32 {
    init_state axiom forall uint16 c. ghostHoNetNetworkDeficitCount32[c] == 0;
    axiom forall uint16 c.
        ghostHoNetNetworkDeficitCount32[c] >= 0 && ghostHoNetNetworkDeficitCount32[c] <= max_uint32;
    axiom forall uint16 c. !HO_NET_SLOT(c) => ghostHoNetNetworkDeficitCount32[c] == 0;
}

hook Sload uint32 val _Holdings.networkDeficitCount[KEY Holdings.PoolId p][KEY uint16 cid] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(HO_NET_SLOT(cid), "UNSAFE: deficits tracked on two networks only");
    require(ghostHoNetNetworkDeficitCount32[cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.networkDeficitCount[KEY Holdings.PoolId p][KEY uint16 cid] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(HO_NET_SLOT(cid), "UNSAFE: deficits tracked on two networks only");
    ghostHoNetNetworkDeficitCount32[cid] = val;
}

persistent ghost mapping(uint16 => mathint) ghostHoNetDeficitCount32 {
    init_state axiom forall uint16 c. ghostHoNetDeficitCount32[c] == 0;
    axiom forall uint16 c. ghostHoNetDeficitCount32[c] >= 0 && ghostHoNetDeficitCount32[c] <= max_uint32;
    axiom forall uint16 c. !HO_NET_SLOT(c) => ghostHoNetDeficitCount32[c] == 0;
}

hook Sload uint32 val _Holdings.deficitCount[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(HO_NET_SLOT(cid), "UNSAFE: deficits tracked on two networks only");
    require(ghostHoNetDeficitCount32[cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings.deficitCount[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY uint16 cid] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(HO_NET_SLOT(cid), "UNSAFE: deficits tracked on two networks only");
    ghostHoNetDeficitCount32[cid] = val;
}

persistent ghost mapping(uint128 => mathint) ghostHoNetIncreasedAmount256 {
    init_state axiom forall uint128 a. ghostHoNetIncreasedAmount256[a] == 0;
    axiom forall uint128 a. ghostHoNetIncreasedAmount256[a] >= 0 && ghostHoNetIncreasedAmount256[a] <= max_uint256;
    axiom forall uint128 a. !VALID_ASSET_HO(a) => ghostHoNetIncreasedAmount256[a] == 0;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoNetIncreasedAmount256[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].increasedAmount uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoNetIncreasedAmount256[aid] = val;
}

persistent ghost mapping(uint128 => mathint) ghostHoNetDecreasedAmount256 {
    init_state axiom forall uint128 a. ghostHoNetDecreasedAmount256[a] == 0;
    axiom forall uint128 a. ghostHoNetDecreasedAmount256[a] >= 0 && ghostHoNetDecreasedAmount256[a] <= max_uint256;
    axiom forall uint128 a. !VALID_ASSET_HO(a) => ghostHoNetDecreasedAmount256[a] == 0;
}

hook Sload uint256 val _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    require(ghostHoNetDecreasedAmount256[aid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _Holdings._holding[KEY Holdings.PoolId p][KEY Holdings.ShareClassId sc][KEY Holdings.AssetId aid].decreasedAmount uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ASSET_HO(aid), "UNSAFE: at most two assets per share class");
    ghostHoNetDecreasedAmount256[aid] = val;
}

definition HO_NET_DEFICIT_CARDINALITY() returns mathint =
    (ghostHoNetDecreasedAmount256[ghostHoAssetE1] > ghostHoNetIncreasedAmount256[ghostHoAssetE1] ? 1 : 0)
    + (ghostHoNetDecreasedAmount256[ghostHoAssetE2] > ghostHoNetIncreasedAmount256[ghostHoAssetE2] ? 1 : 0);

function setupHoldingsMultiNetwork(env e) {
    setupHoldings(e);
    require(ghostHoCid16 != ghostHoCid16Other, "SCOPE: the two distinct modelled networks");
}

function SETUP_HO_MN(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupHoldingsMultiNetwork(e);
}
