// ShareClassManager, multi-class lane. Setup: rows keyed by class, for class isolation.

// Own setup: two classes of the pinned pool; single_pool hooks the same class rows pinned to one class.

import "ShareClassManager_base.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/multi_share_class.spec";

persistent ghost mathint ghostScClassShareClassCount32 {
    init_state axiom ghostScClassShareClassCount32 == 0;
    axiom ghostScClassShareClassCount32 >= 0 && ghostScClassShareClassCount32 <= max_uint32;
}

hook Sload uint32 val _ShareClassManager.shareClassCount[KEY ShareClassManager.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostScClassShareClassCount32 == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.shareClassCount[KEY ShareClassManager.PoolId p] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostScClassShareClassCount32 = val;
}

persistent ghost mapping(bytes16 => bool) ghostScClassShareClassIds {
    init_state axiom forall bytes16 sc. !ghostScClassShareClassIds[sc];
    axiom forall bytes16 sc. !VALID_SC(sc) => !ghostScClassShareClassIds[sc];
}

hook Sload bool val _ShareClassManager.shareClassIds[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScClassShareClassIds[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.shareClassIds[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScClassShareClassIds[sc] = val;
}

persistent ghost mapping(bytes16 => mathint) ghostScClassTotalIssuances256 {
    init_state axiom forall bytes16 sc. ghostScClassTotalIssuances256[sc] == 0;
    axiom forall bytes16 sc.
        ghostScClassTotalIssuances256[sc] >= 0 && ghostScClassTotalIssuances256[sc] <= max_uint256;
    axiom forall bytes16 sc. !VALID_SC(sc) => ghostScClassTotalIssuances256[sc] == 0;
}

hook Sload uint256 val _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].issuances {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScClassTotalIssuances256[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].issuances uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScClassTotalIssuances256[sc] = val;
}

persistent ghost mapping(bytes16 => mathint) ghostScClassTotalRevocations256 {
    init_state axiom forall bytes16 sc. ghostScClassTotalRevocations256[sc] == 0;
    axiom forall bytes16 sc.
        ghostScClassTotalRevocations256[sc] >= 0 && ghostScClassTotalRevocations256[sc] <= max_uint256;
    axiom forall bytes16 sc. !VALID_SC(sc) => ghostScClassTotalRevocations256[sc] == 0;
}

hook Sload uint256 val _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].revocations {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScClassTotalRevocations256[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].revocations uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScClassTotalRevocations256[sc] = val;
}

definition SC_CLASS_TOTAL_ISSUANCE(bytes16 c) returns mathint =
    ghostScClassTotalIssuances256[c] - ghostScClassTotalRevocations256[c];

persistent ghost mapping(bytes16 => mathint) ghostScClassNegativeNetworkCount32 {
    init_state axiom forall bytes16 sc. ghostScClassNegativeNetworkCount32[sc] == 0;
    axiom forall bytes16 sc.
        ghostScClassNegativeNetworkCount32[sc] >= 0 && ghostScClassNegativeNetworkCount32[sc] <= max_uint32;
    axiom forall bytes16 sc. !VALID_SC(sc) => ghostScClassNegativeNetworkCount32[sc] == 0;
}

hook Sload uint32 val _ShareClassManager.negativeNetworkCount[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScClassNegativeNetworkCount32[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.negativeNetworkCount[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScClassNegativeNetworkCount32[sc] = val;
}

persistent ghost mapping(bytes16 => mathint) ghostScClassPricePoolPerShare128 {
    init_state axiom forall bytes16 sc. ghostScClassPricePoolPerShare128[sc] == 0;
    axiom forall bytes16 sc.
        ghostScClassPricePoolPerShare128[sc] >= 0 && ghostScClassPricePoolPerShare128[sc] <= max_uint128;
    axiom forall bytes16 sc. !VALID_SC(sc) => ghostScClassPricePoolPerShare128[sc] == 0;
}

hook Sload ShareClassManager.D18 val _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].price {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScClassPricePoolPerShare128[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].price ShareClassManager.D18 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScClassPricePoolPerShare128[sc] = val;
}

persistent ghost mapping(bytes16 => mathint) ghostScClassPriceComputedAt64 {
    init_state axiom forall bytes16 sc. ghostScClassPriceComputedAt64[sc] == 0;
    axiom forall bytes16 sc.
        ghostScClassPriceComputedAt64[sc] >= 0 && ghostScClassPriceComputedAt64[sc] <= max_uint64;
    axiom forall bytes16 sc. !VALID_SC(sc) => ghostScClassPriceComputedAt64[sc] == 0;
}

hook Sload uint64 val _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].computedAt {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScClassPriceComputedAt64[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].computedAt uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScClassPriceComputedAt64[sc] = val;
}

persistent ghost mapping(bytes16 => bytes32) ghostScClassMetadataSalt {
    init_state axiom forall bytes16 sc. ghostScClassMetadataSalt[sc] == to_bytes32(0);
    axiom forall bytes16 sc. !VALID_SC(sc) => ghostScClassMetadataSalt[sc] == to_bytes32(0);
}

hook Sload bytes32 val _ShareClassManager.metadata[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].salt {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostScClassMetadataSalt[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.metadata[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].salt bytes32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostScClassMetadataSalt[sc] = val;
}

persistent ghost mapping(bytes16 => mapping(uint16 => mathint)) ghostScClassIssuances256 {
    init_state axiom forall bytes16 sc. forall uint16 cid. ghostScClassIssuances256[sc][cid] == 0;
    axiom forall bytes16 sc. forall uint16 cid.
        ghostScClassIssuances256[sc][cid] >= 0 && ghostScClassIssuances256[sc][cid] <= max_uint256;
    axiom forall bytes16 sc. forall uint16 cid.
        (!VALID_SC(sc) || !VALID_CID(cid)) => ghostScClassIssuances256[sc][cid] == 0;
}

hook Sload uint256 val _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].issuances {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_CID(cid), "UNSAFE: at most three networks per share class");
    require(ghostScClassIssuances256[sc][cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].issuances uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_CID(cid), "UNSAFE: at most three networks per share class");
    ghostScClassIssuances256[sc][cid] = val;
}

persistent ghost mapping(bytes16 => mapping(uint16 => mathint)) ghostScClassRevocations256 {
    init_state axiom forall bytes16 sc. forall uint16 cid. ghostScClassRevocations256[sc][cid] == 0;
    axiom forall bytes16 sc. forall uint16 cid.
        ghostScClassRevocations256[sc][cid] >= 0 && ghostScClassRevocations256[sc][cid] <= max_uint256;
    axiom forall bytes16 sc. forall uint16 cid.
        (!VALID_SC(sc) || !VALID_CID(cid)) => ghostScClassRevocations256[sc][cid] == 0;
}

hook Sload uint256 val _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].revocations {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_CID(cid), "UNSAFE: at most three networks per share class");
    require(ghostScClassRevocations256[sc][cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].revocations uint256 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_CID(cid), "UNSAFE: at most three networks per share class");
    ghostScClassRevocations256[sc][cid] = val;
}

definition SC_CLASS_PAIR(bytes16 c1, bytes16 c2) returns bool =
    ghostShareClassA != ghostShareClassB
    && ((c1 == ghostShareClassA && c2 == ghostShareClassB)
        || (c1 == ghostShareClassB && c2 == ghostShareClassA));

definition SC_CLASS_NET_ISSUANCE_SUM(bytes16 c) returns mathint =
    (ghostScClassIssuances256[c][ghostScCidE1] - ghostScClassRevocations256[c][ghostScCidE1])
    + (ghostScClassIssuances256[c][ghostScCidE2] - ghostScClassRevocations256[c][ghostScCidE2])
    + (ghostScClassIssuances256[c][ghostScCidE3] - ghostScClassRevocations256[c][ghostScCidE3]);

definition SC_CLASS_NEGATIVE_NETWORK_CARDINALITY(bytes16 c) returns mathint =
    (ghostScClassRevocations256[c][ghostScCidE1] > ghostScClassIssuances256[c][ghostScCidE1] ? 1 : 0)
    + (ghostScClassRevocations256[c][ghostScCidE2] > ghostScClassIssuances256[c][ghostScCidE2] ? 1 : 0)
    + (ghostScClassRevocations256[c][ghostScCidE3] > ghostScClassIssuances256[c][ghostScCidE3] ? 1 : 0);
