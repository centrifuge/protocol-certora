// ShareClassManager, single-pool lane. Setup: class rows of the pinned pool and class.

// Own setup: rows of the one pinned pool and class with network sums; the isolation lanes hook the same fields keyed.

import "ShareClassManager_base.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/single_share_class.spec";

persistent ghost mathint ghostScShareClassCount32 {
    init_state axiom ghostScShareClassCount32 == 0;
    axiom ghostScShareClassCount32 >= 0 && ghostScShareClassCount32 <= max_uint32;
}

hook Sload uint32 val _ShareClassManager.shareClassCount[KEY ShareClassManager.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostScShareClassCount32 == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.shareClassCount[KEY ShareClassManager.PoolId p] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostScShareClassCount32 = val;
}

persistent ghost bool ghostScShareClassIds {
    init_state axiom !ghostScShareClassIds;
}

hook Sload bool val _ShareClassManager.shareClassIds[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScShareClassIds == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.shareClassIds[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScShareClassIds = val;
}

persistent ghost mathint ghostScTotalIssuances256 {
    init_state axiom ghostScTotalIssuances256 == 0;
    axiom ghostScTotalIssuances256 >= 0 && ghostScTotalIssuances256 <= max_uint256;
}

hook Sload uint256 val _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].issuances {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScTotalIssuances256 == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].issuances uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScTotalIssuances256 = val;
}

persistent ghost mathint ghostScTotalRevocations256 {
    init_state axiom ghostScTotalRevocations256 == 0;
    axiom ghostScTotalRevocations256 >= 0 && ghostScTotalRevocations256 <= max_uint256;
}

hook Sload uint256 val _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].revocations {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScTotalRevocations256 == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].revocations uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScTotalRevocations256 = val;
}

definition SC_TOTAL_ISSUANCE() returns mathint = ghostScTotalIssuances256 - ghostScTotalRevocations256;

persistent ghost mathint ghostScNegativeNetworkCount32 {
    init_state axiom ghostScNegativeNetworkCount32 == 0;
    axiom ghostScNegativeNetworkCount32 >= 0 && ghostScNegativeNetworkCount32 <= max_uint32;
}

hook Sload uint32 val _ShareClassManager.negativeNetworkCount[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScNegativeNetworkCount32 == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.negativeNetworkCount[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScNegativeNetworkCount32 = val;
}

persistent ghost mathint ghostScPricePoolPerShare128 {
    init_state axiom ghostScPricePoolPerShare128 == 0;
    axiom ghostScPricePoolPerShare128 >= 0 && ghostScPricePoolPerShare128 <= max_uint128;
}

persistent ghost mathint ghostScPriceComputedAt64 {
    init_state axiom ghostScPriceComputedAt64 == 0;
    axiom ghostScPriceComputedAt64 >= 0 && ghostScPriceComputedAt64 <= max_uint64;
}

persistent ghost bytes32 ghostScMetadataSalt {
    init_state axiom ghostScMetadataSalt == to_bytes32(0);
}

hook Sload bytes32 val _ShareClassManager.metadata[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].salt {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScMetadataSalt == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.metadata[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].salt bytes32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScMetadataSalt = val;
}

persistent ghost mapping(uint16 => mathint) ghostScIssuances256 {
    init_state axiom forall uint16 cid. ghostScIssuances256[cid] == 0;
    axiom forall uint16 cid. ghostScIssuances256[cid] >= 0 && ghostScIssuances256[cid] <= max_uint256;
}

persistent ghost mapping(uint16 => mathint) ghostScRevocations256 {
    init_state axiom forall uint16 cid. ghostScRevocations256[cid] == 0;
    axiom forall uint16 cid. ghostScRevocations256[cid] >= 0 && ghostScRevocations256[cid] <= max_uint256;
}

// Every network's sums and short count, each store moving them by its own delta.
persistent ghost mathint ghostScIssuancesSum {
    init_state axiom ghostScIssuancesSum == 0;
}

persistent ghost mathint ghostScRevocationsSum {
    init_state axiom ghostScRevocationsSum == 0;
}

persistent ghost mathint ghostScShortNetworks {
    init_state axiom ghostScShortNetworks == 0;
}

definition SC_NET_ISSUANCE_SUM() returns mathint = ghostScIssuancesSum - ghostScRevocationsSum;

definition SC_ISSUANCES_SUM() returns mathint = ghostScIssuancesSum;

definition SC_REVOCATIONS_SUM() returns mathint = ghostScRevocationsSum;

definition SC_NEGATIVE_NETWORK_CARDINALITY() returns mathint = ghostScShortNetworks;

definition SC_CROSSING(bool wasShort, bool isShort) returns mathint = (isShort ? 1 : 0) - (wasShort ? 1 : 0);

// The census a network's crossing moves: it counts that network while short, and it counts uint16 ids only.
function scShortNetworkIsCounted(uint16 cid) {
    require(ghostScRevocations256[cid] > ghostScIssuances256[cid] => ghostScShortNetworks >= 1,
        "SAFE: the census starts at zero and every crossing moves it, so a short network is in it");
    require(ghostScShortNetworks <= 65536, "SAFE: the census counts networks, and a network id is a uint16");
}

hook Sload ShareClassManager.D18 val _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].price {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScPricePoolPerShare128 == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].price ShareClassManager.D18 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScPricePoolPerShare128 = assert_uint128(val);
}

hook Sload uint64 val _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].computedAt {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScPriceComputedAt64 == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].computedAt uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScPriceComputedAt64 = val;
}

hook Sload uint256 val _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].issuances {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScIssuances256[cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].issuances uint256 val (uint256 held) {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScIssuancesSum = ghostScIssuancesSum + val - held;
    ghostScShortNetworks = ghostScShortNetworks
        + SC_CROSSING(ghostScRevocations256[cid] > held, ghostScRevocations256[cid] > val);
    ghostScIssuances256[cid] = val;
}

hook Sload uint256 val _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].revocations {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScRevocations256[cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].revocations uint256 val (uint256 held) {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScRevocationsSum = ghostScRevocationsSum + val - held;
    ghostScShortNetworks = ghostScShortNetworks
        + SC_CROSSING(held > ghostScIssuances256[cid], val > ghostScIssuances256[cid]);
    ghostScRevocations256[cid] = val;
}

function SETUP_SC(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupShareClassManager(e);
}
