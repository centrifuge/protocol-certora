// Escrow, two-class lane. Setup: the pinned row's total and reserved per class.

// Own setup: total and reserved keyed per class over two classes; base hooks the same fields with one pinned class.

import "../../../../shared/env.spec";
import "../../../../shared/domains/multi_share_class.spec";

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

persistent ghost mapping(bytes16 => mathint) ghostPeClassTotal128 {
    init_state axiom forall bytes16 sc. ghostPeClassTotal128[sc] == 0;
    axiom forall bytes16 sc. ghostPeClassTotal128[sc] >= 0 && ghostPeClassTotal128[sc] <= max_uint128;
}

persistent ghost mapping(bytes16 => mathint) ghostPeClassReserved128 {
    init_state axiom forall bytes16 sc. ghostPeClassReserved128[sc] == 0;
    axiom forall bytes16 sc. ghostPeClassReserved128[sc] >= 0 && ghostPeClassReserved128[sc] <= max_uint128;
}

hook Sload uint128 val _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].total {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    require(ghostPeClassTotal128[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].total uint128 val {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    ghostPeClassTotal128[sc] = val;
}

hook Sload uint128 val _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].reserved {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    require(ghostPeClassReserved128[sc] == val, "SAFE: mirror tracks storage");
}

hook Sstore _PoolEscrow.holding[KEY Escrow.ShareClassId sc][KEY address asset][KEY uint256 tokenId].reserved uint128 val {
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(asset == ghostPeAsset && tokenId == ghostPeTokenId256, "SCOPE: modelled asset stands for any");
    ghostPeClassReserved128[sc] = val;
}

function setupPoolEscrowMultiShareClass(env e) {
    setupEnv(e);
    setupShareClassMode();
    require(ghostShareClassA != ghostShareClassB, "SCOPE: two distinct share classes");
}
