// Escrow, single-row lane. Setup: total and reserved mirrors of the pinned row.

import "../../../../shared/env.spec";
import "../../../../shared/domains/single_share_class.spec";

using Escrow as _PoolEscrow;

// SAFE: the cut methods write no holding, reservation or ward, as the custody lane proves.
definition EXCLUDED_FUNCTION_PE(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    || f.selector == sig:_PoolEscrow.authTransferTo(address,uint256,address,uint256).selector
    || f.selector == sig:_PoolEscrow.recoverTokens(address,address,uint256).selector
    || f.selector == sig:_PoolEscrow.recoverTokens(address,uint256,address,uint256).selector
    ;

// SCOPE: one pinned (asset, tokenId) row, other assets unchecked.
persistent ghost address ghostPeAsset;

persistent ghost uint256 ghostPeTokenId256;

// SCOPE: two reservers times two reasons, wider hold sets unchecked.
persistent ghost address ghostPeReserverE1;

persistent ghost address ghostPeReserverE2 {
    axiom ghostPeReserverE2 != ghostPeReserverE1;
}

persistent ghost bytes32 ghostPeReasonE1;

persistent ghost bytes32 ghostPeReasonE2 {
    axiom ghostPeReasonE2 != ghostPeReasonE1;
}

definition VALID_RESERVER(address r) returns bool =
    r == ghostPeReserverE1 || r == ghostPeReserverE2;

definition VALID_REASON(bytes32 reason) returns bool =
    reason == ghostPeReasonE1 || reason == ghostPeReasonE2;

persistent ghost mathint ghostPeTotal128 {
    init_state axiom ghostPeTotal128 == 0;
    axiom ghostPeTotal128 >= 0 && ghostPeTotal128 <= max_uint128;
}

persistent ghost mathint ghostPeReserved128 {
    init_state axiom ghostPeReserved128 == 0;
    axiom ghostPeReserved128 >= 0 && ghostPeReserved128 <= max_uint128;
}

hook Sload uint128 val _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].total {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    require(ghostPeTotal128 == val, "SAFE: mirror tracks storage");
}

hook Sstore _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].total uint128 val {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    ghostPeTotal128 = val;
}

hook Sload uint128 val _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].reserved {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    require(ghostPeReserved128 == val, "SAFE: mirror tracks storage");
}

hook Sstore _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].reserved uint128 val {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    ghostPeReserved128 = val;
}

persistent ghost mapping(address => mapping(bytes32 => mathint)) ghostPeReservedBy128 {
    init_state axiom forall address r. forall bytes32 reason. ghostPeReservedBy128[r][reason] == 0;
    axiom forall address r. forall bytes32 reason.
        ghostPeReservedBy128[r][reason] >= 0 && ghostPeReservedBy128[r][reason] <= max_uint128;
    axiom forall address r. forall bytes32 reason.
        (!VALID_RESERVER(r) || !VALID_REASON(reason)) => ghostPeReservedBy128[r][reason] == 0;
}

definition PE_RESERVED_BUCKET_SUM() returns mathint =
    ghostPeReservedBy128[ghostPeReserverE1][ghostPeReasonE1]
    + ghostPeReservedBy128[ghostPeReserverE1][ghostPeReasonE2]
    + ghostPeReservedBy128[ghostPeReserverE2][ghostPeReasonE1]
    + ghostPeReservedBy128[ghostPeReserverE2][ghostPeReasonE2];

hook Sload uint128 val _PoolEscrow.reservedBy[KEY Escrow.ShareClassId sc][KEY address reserver][KEY bytes32 reason][KEY address asset][KEY uint256 tokenId] {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_RESERVER(reserver), "SCOPE: two modelled reservers");
    require(VALID_REASON(reason), "SCOPE: two modelled hold reasons");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    require(ghostPeReservedBy128[reserver][reason] == val, "SAFE: mirror tracks storage");
}

hook Sstore _PoolEscrow.reservedBy[KEY Escrow.ShareClassId sc][KEY address reserver][KEY bytes32 reason][KEY address asset][KEY uint256 tokenId] uint128 val {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_RESERVER(reserver), "SCOPE: two modelled reservers");
    require(VALID_REASON(reason), "SCOPE: two modelled hold reasons");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    ghostPeReservedBy128[reserver][reason] = val;
}

function setupPoolEscrow(env e) {
    setupEnv(e);
    setupShareClassMode();
    require(e.msg.sender != _PoolEscrow, "SAFE: the escrow never calls itself");
}

function SETUP_PE(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupPoolEscrow(e);
}
