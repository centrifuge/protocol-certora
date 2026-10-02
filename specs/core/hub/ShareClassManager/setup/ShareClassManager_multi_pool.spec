// ShareClassManager, multi-pool lane. Setup: rows keyed by pool, for pool isolation.

// Own setup: two pools with one class each; single_pool hooks the same class rows pinned to one pool.

import "ShareClassManager_base.spec";
import "../../../../shared/domains/multi_pool.spec";
import "../../../../shared/domains/multi_share_class.spec";

// SCOPE: one class per pinned pool, a pool-keyed mirror is one row.
definition SC_POOL_SLOT(uint64 p, bytes16 sc) returns bool =
    (p == ghostPoolA64 && sc == ghostShareClassA) || (p == ghostPoolB64 && sc == ghostShareClassB);

persistent ghost mapping(uint64 => mathint) ghostScPoolShareClassCount32 {
    init_state axiom forall uint64 p. ghostScPoolShareClassCount32[p] == 0;
    axiom forall uint64 p. ghostScPoolShareClassCount32[p] >= 0 && ghostScPoolShareClassCount32[p] <= max_uint32;
    axiom forall uint64 p. !VALID_POOL(p) => ghostScPoolShareClassCount32[p] == 0;
}

hook Sload uint32 val _ShareClassManager.shareClassCount[KEY ShareClassManager.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostScPoolShareClassCount32[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.shareClassCount[KEY ShareClassManager.PoolId p] uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostScPoolShareClassCount32[p] = val;
}

persistent ghost mapping(uint64 => bool) ghostScPoolShareClassIds {
    init_state axiom forall uint64 p. !ghostScPoolShareClassIds[p];
    axiom forall uint64 p. !VALID_POOL(p) => !ghostScPoolShareClassIds[p];
}

hook Sload bool val _ShareClassManager.shareClassIds[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostScPoolShareClassIds[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.shareClassIds[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] bool val {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostScPoolShareClassIds[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostScPoolTotalIssuances256 {
    init_state axiom forall uint64 p. ghostScPoolTotalIssuances256[p] == 0;
    axiom forall uint64 p. ghostScPoolTotalIssuances256[p] >= 0 && ghostScPoolTotalIssuances256[p] <= max_uint256;
    axiom forall uint64 p. !VALID_POOL(p) => ghostScPoolTotalIssuances256[p] == 0;
}

hook Sload uint256 val _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].issuances {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostScPoolTotalIssuances256[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].issuances uint256 val {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostScPoolTotalIssuances256[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostScPoolTotalRevocations256 {
    init_state axiom forall uint64 p. ghostScPoolTotalRevocations256[p] == 0;
    axiom forall uint64 p. ghostScPoolTotalRevocations256[p] >= 0 && ghostScPoolTotalRevocations256[p] <= max_uint256;
    axiom forall uint64 p. !VALID_POOL(p) => ghostScPoolTotalRevocations256[p] == 0;
}

hook Sload uint256 val _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].revocations {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostScPoolTotalRevocations256[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuanceAcrossNetworks[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].revocations uint256 val {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostScPoolTotalRevocations256[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostScPoolNegativeNetworkCount32 {
    init_state axiom forall uint64 p. ghostScPoolNegativeNetworkCount32[p] == 0;
    axiom forall uint64 p. ghostScPoolNegativeNetworkCount32[p] >= 0 && ghostScPoolNegativeNetworkCount32[p] <= max_uint32;
    axiom forall uint64 p. !VALID_POOL(p) => ghostScPoolNegativeNetworkCount32[p] == 0;
}

hook Sload uint32 val _ShareClassManager.negativeNetworkCount[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostScPoolNegativeNetworkCount32[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.negativeNetworkCount[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc] uint32 val {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostScPoolNegativeNetworkCount32[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostScPoolPricePoolPerShare128 {
    init_state axiom forall uint64 p. ghostScPoolPricePoolPerShare128[p] == 0;
    axiom forall uint64 p.
        ghostScPoolPricePoolPerShare128[p] >= 0 && ghostScPoolPricePoolPerShare128[p] <= max_uint128;
    axiom forall uint64 p. !VALID_POOL(p) => ghostScPoolPricePoolPerShare128[p] == 0;
}

hook Sload ShareClassManager.D18 val _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].price {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostScPoolPricePoolPerShare128[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].price ShareClassManager.D18 val {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostScPoolPricePoolPerShare128[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostScPoolPriceComputedAt64 {
    init_state axiom forall uint64 p. ghostScPoolPriceComputedAt64[p] == 0;
    axiom forall uint64 p. ghostScPoolPriceComputedAt64[p] >= 0 && ghostScPoolPriceComputedAt64[p] <= max_uint64;
    axiom forall uint64 p. !VALID_POOL(p) => ghostScPoolPriceComputedAt64[p] == 0;
}

hook Sload uint64 val _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].computedAt {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostScPoolPriceComputedAt64[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.pricePoolPerShare[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].computedAt uint64 val {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostScPoolPriceComputedAt64[p] = val;
}

persistent ghost mapping(uint64 => bytes32) ghostScPoolMetadataSalt {
    init_state axiom forall uint64 p. ghostScPoolMetadataSalt[p] == to_bytes32(0);
    axiom forall uint64 p. !VALID_POOL(p) => ghostScPoolMetadataSalt[p] == to_bytes32(0);
}

hook Sload bytes32 val _ShareClassManager.metadata[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].salt {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostScPoolMetadataSalt[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.metadata[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc].salt bytes32 val {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostScPoolMetadataSalt[p] = val;
}

persistent ghost mapping(uint64 => mapping(uint16 => mathint)) ghostScPoolIssuances256 {
    init_state axiom forall uint64 p. forall uint16 cid. ghostScPoolIssuances256[p][cid] == 0;
    axiom forall uint64 p. forall uint16 cid.
        ghostScPoolIssuances256[p][cid] >= 0 && ghostScPoolIssuances256[p][cid] <= max_uint256;
    axiom forall uint64 p. forall uint16 cid. !VALID_POOL(p) => ghostScPoolIssuances256[p][cid] == 0;
}

hook Sload uint256 val _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].issuances {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostScPoolIssuances256[p][cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].issuances uint256 val {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostScPoolIssuances256[p][cid] = val;
}

persistent ghost mapping(uint64 => mapping(uint16 => mathint)) ghostScPoolRevocations256 {
    init_state axiom forall uint64 p. forall uint16 cid. ghostScPoolRevocations256[p][cid] == 0;
    axiom forall uint64 p. forall uint16 cid.
        ghostScPoolRevocations256[p][cid] >= 0 && ghostScPoolRevocations256[p][cid] <= max_uint256;
    axiom forall uint64 p. forall uint16 cid. !VALID_POOL(p) => ghostScPoolRevocations256[p][cid] == 0;
}

hook Sload uint256 val _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].revocations {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    require(ghostScPoolRevocations256[p][cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.issuancePerNetwork[KEY ShareClassManager.PoolId p][KEY ShareClassManager.ShareClassId sc][KEY uint16 cid].revocations uint256 val {
    require(SC_POOL_SLOT(p, sc), "SCOPE: one share class per pool");
    ghostScPoolRevocations256[p][cid] = val;
}

definition SC_POOL_PAIR(uint64 p, uint64 q) returns bool =
    (p == ghostPoolA64 && q == ghostPoolB64) || (p == ghostPoolB64 && q == ghostPoolA64);
