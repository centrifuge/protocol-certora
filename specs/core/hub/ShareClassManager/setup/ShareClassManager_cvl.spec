// ShareClassManager. Model: share price and issuance, for scenes not compiling it.

methods {
    function _.pricePoolPerShare(uint64 poolId, bytes16 scId) external
        => scPricePoolPerShareCVL(poolId, scId) expect (uint128, uint64) UNRESOLVED;
    function _.issuance(uint64 poolId, bytes16 scId, uint16 centrifugeId) external
        => scIssuanceCVL(poolId, scId, centrifugeId) expect uint128 UNRESOLVED;
}

persistent ghost mathint ghostScPricePoolPerShare128 {
    axiom ghostScPricePoolPerShare128 >= 0 && ghostScPricePoolPerShare128 <= max_uint128;
}
persistent ghost mathint ghostScPriceComputedAt64 {
    axiom ghostScPriceComputedAt64 >= 0 && ghostScPriceComputedAt64 <= max_uint64;
}
persistent ghost mapping(uint16 => mathint) ghostScIssuances256 {
    axiom forall uint16 cid. ghostScIssuances256[cid] >= 0 && ghostScIssuances256[cid] <= max_uint256;
}
persistent ghost mapping(uint16 => mathint) ghostScRevocations256 {
    axiom forall uint16 cid. ghostScRevocations256[cid] >= 0 && ghostScRevocations256[cid] <= max_uint256;
}

// SCOPE: other pool and class rows are untracked, never revert here.
definition SC_PINNED_ROW(uint64 poolId, bytes16 scId) returns bool =
    poolId == ghostPoolA64 && scId == ghostShareClassA;

function scPricePoolPerShareCVL(uint64 poolId, bytes16 scId) returns (uint128, uint64) {
    uint128 price;
    uint64 computedAt;
    if (SC_PINNED_ROW(poolId, scId)) {
        return (require_uint128(ghostScPricePoolPerShare128), require_uint64(ghostScPriceComputedAt64));
    }
    return (price, computedAt);
}

function scIssuanceCVL(uint64 poolId, bytes16 scId, uint16 centrifugeId) returns uint128 {
    if (SC_PINNED_ROW(poolId, scId)) {
        uint16 cid = centrifugeId;
        if (ghostScIssuances256[cid] < ghostScRevocations256[cid]) {
            revert("NegativeIssuance");
        }
        if (ghostScIssuances256[cid] - ghostScRevocations256[cid] > max_uint128) {
            revert("Uint128_Overflow");
        }
        return assert_uint128(ghostScIssuances256[cid] - ghostScRevocations256[cid]);
    }
    uint128 free;
    return free;
}
