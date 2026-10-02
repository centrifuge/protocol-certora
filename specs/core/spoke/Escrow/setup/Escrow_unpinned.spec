// Escrow, unpinned lane. Setup: any holding's reserve and its reservations summed.

// Own setup: one symbolic row with its bucket sum and no cuts; base hooks the same fields and pins the row.

import "../../../../shared/env.spec";

using Escrow as _PoolEscrow;

methods {
    function _PoolEscrow.wards(address) external returns (uint256) envfree;
    function _PoolEscrow.holding(Escrow.ShareClassId, address, uint256) external returns (uint128, uint128) envfree;
    function _PoolEscrow.reservedBy(Escrow.ShareClassId, address, bytes32, address, uint256) external returns (uint128) envfree;
}

// SAFE: only views cut, unresolved calls cannot write the escrow.
definition EXCLUDED_FUNCTION_PE_UP(method f) returns bool =
    f.isView || f.isPure || f.isFallback;

function setupPoolEscrowUnpinned(env e) {
    setupEnv(e);
}

// The measured holding: symbolic, never pinned.
persistent ghost bytes16 ghostPeRowSc;

persistent ghost address ghostPeRowAsset;

persistent ghost uint256 ghostPeRowTokenId;

definition PE_IS_ROW(bytes16 sc, address a, uint256 t) returns bool =
    sc == ghostPeRowSc && a == ghostPeRowAsset && t == ghostPeRowTokenId;

persistent ghost mathint ghostPeBucketSumRow {
    init_state axiom ghostPeBucketSumRow == 0;
}

persistent ghost mathint ghostPeReservedRow {
    init_state axiom ghostPeReservedRow == 0;
}

hook Sstore _PoolEscrow.reservedBy[KEY Escrow.ShareClassId sc][KEY address r][KEY bytes32 n][KEY address a][KEY uint256 t] uint128 val (uint128 held) {
    ghostPeBucketSumRow = PE_IS_ROW(sc, a, t) ? ghostPeBucketSumRow + val - held : ghostPeBucketSumRow;
}

hook Sload uint128 val _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address a][KEY uint256 t].reserved {
    require(!PE_IS_ROW(sc, a, t) || ghostPeReservedRow == val, "SAFE: mirror tracks storage");
}

hook Sstore _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address a][KEY uint256 t].reserved uint128 val {
    ghostPeReservedRow = PE_IS_ROW(sc, a, t) ? val : ghostPeReservedRow;
}
