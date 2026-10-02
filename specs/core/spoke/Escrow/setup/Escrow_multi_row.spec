// Escrow, two-row lane. Setup: reserved mirrors keyed by (asset, tokenId).

// Own setup: reserved mirrors keyed by two (asset, tokenId) rows; base hooks the same fields for one pinned row.

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

// SCOPE: two (asset, tokenId) rows, a third row is unchecked.
persistent ghost address ghostPeRowAssetE1;

persistent ghost address ghostPeRowAssetE2;

persistent ghost uint256 ghostPeRowTokenE1;

persistent ghost uint256 ghostPeRowTokenE2 {
    axiom !(ghostPeRowAssetE2 == ghostPeRowAssetE1 && ghostPeRowTokenE2 == ghostPeRowTokenE1);
}

definition VALID_ROW_PE(address a, mathint t) returns bool =
    (a == ghostPeRowAssetE1 && t == ghostPeRowTokenE1)
    || (a == ghostPeRowAssetE2 && t == ghostPeRowTokenE2);

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

persistent ghost mapping(address => mapping(mathint => mathint)) ghostPeRowReserved128 {
    init_state axiom forall address a. forall mathint t. ghostPeRowReserved128[a][t] == 0;
    axiom forall address a. forall mathint t.
        ghostPeRowReserved128[a][t] >= 0 && ghostPeRowReserved128[a][t] <= max_uint128;
}

hook Sload uint128 val _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].reserved {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ROW_PE(asset, tokenId), "SCOPE: two modelled escrow assets");
    require(ghostPeRowReserved128[asset][tokenId] == val, "SAFE: mirror tracks storage");
}

hook Sstore _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].reserved uint128 val {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_ROW_PE(asset, tokenId), "SCOPE: two modelled escrow assets");
    ghostPeRowReserved128[asset][tokenId] = val;
}

persistent ghost mapping(address => mapping(mathint => mapping(address => mapping(bytes32 => mathint)))) ghostPeRowReservedBy128 {
    init_state axiom forall address a. forall mathint t. forall address r. forall bytes32 n.
        ghostPeRowReservedBy128[a][t][r][n] == 0;
    axiom forall address a. forall mathint t. forall address r. forall bytes32 n.
        ghostPeRowReservedBy128[a][t][r][n] >= 0 && ghostPeRowReservedBy128[a][t][r][n] <= max_uint128;
}

hook Sload uint128 val _PoolEscrow.reservedBy[KEY Escrow.ShareClassId sc][KEY address reserver][KEY bytes32 reason][KEY address asset][KEY uint256 tokenId] {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_RESERVER(reserver), "SCOPE: two modelled reservers");
    require(VALID_REASON(reason), "SCOPE: two modelled hold reasons");
    require(VALID_ROW_PE(asset, tokenId), "SCOPE: two modelled escrow assets");
    require(ghostPeRowReservedBy128[asset][tokenId][reserver][reason] == val, "SAFE: mirror tracks storage");
}

hook Sstore _PoolEscrow.reservedBy[KEY Escrow.ShareClassId sc][KEY address reserver][KEY bytes32 reason][KEY address asset][KEY uint256 tokenId] uint128 val {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(VALID_RESERVER(reserver), "SCOPE: two modelled reservers");
    require(VALID_REASON(reason), "SCOPE: two modelled hold reasons");
    require(VALID_ROW_PE(asset, tokenId), "SCOPE: two modelled escrow assets");
    ghostPeRowReservedBy128[asset][tokenId][reserver][reason] = val;
}

definition PE_ROW_BUCKET_SUM(address a, mathint t) returns mathint =
    ghostPeRowReservedBy128[a][t][ghostPeReserverE1][ghostPeReasonE1]
    + ghostPeRowReservedBy128[a][t][ghostPeReserverE1][ghostPeReasonE2]
    + ghostPeRowReservedBy128[a][t][ghostPeReserverE2][ghostPeReasonE1]
    + ghostPeRowReservedBy128[a][t][ghostPeReserverE2][ghostPeReasonE2];

function setupPoolEscrowMultiRow(env e) {
    setupEnv(e);
    setupShareClassMode();
}

function SETUP_PE_MR(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupPoolEscrowMultiRow(e);
}
