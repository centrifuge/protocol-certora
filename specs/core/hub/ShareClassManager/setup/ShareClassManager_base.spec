// ShareClassManager. Setup: the link, the metadata cut.

import "../../../../shared/env.spec";

using ShareClassManager as _ShareClassManager;

methods {
    // SCOPE: updateMetadata is cut here, its footprint proved in the unpinned lane.
    function ShareClassManager.updateMetadata(ShareClassManager.PoolId, ShareClassManager.ShareClassId, string, string) external
        => NONDET DELETE;
}

definition EXCLUDED_FUNCTION_SC(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

// UNSAFE: three networks modelled, an update on a fourth is pruned.
persistent ghost uint16 ghostScCidE1;

persistent ghost uint16 ghostScCidE2 {
    axiom ghostScCidE2 != ghostScCidE1;
}

persistent ghost uint16 ghostScCidE3 {
    axiom ghostScCidE3 != ghostScCidE1 && ghostScCidE3 != ghostScCidE2;
}

definition VALID_CID(uint16 cid) returns bool =
    cid == ghostScCidE1 || cid == ghostScCidE2 || cid == ghostScCidE3;

persistent ghost mapping(bytes32 => bool) ghostScSalts {
    init_state axiom forall bytes32 s. !ghostScSalts[s];
}

hook Sload bool val _ShareClassManager.salts[KEY bytes32 s] {
    require(ghostScSalts[s] == val, "SAFE: mirror tracks storage");
}

hook Sstore _ShareClassManager.salts[KEY bytes32 s] bool val {
    ghostScSalts[s] = val;
}

// SAFE: twin of newShareClassId, the pool id above the 64-bit index.
definition NEW_SHARE_CLASS_ID_SC_CVL(uint64 pool, mathint index) returns bytes16 =
    to_bytes16(require_uint128(pool * 2^64 + index));

function setupShareClassManager(env e) {
    setupEnv(e);
    setupPoolMode();
    setupShareClassMode();
    require(e.msg.sender != _ShareClassManager, "SAFE: the share class manager never calls itself");
    require(ghostShareClassA == NEW_SHARE_CLASS_ID_SC_CVL(ghostPoolA64, 1),
        "SCOPE: class A is its pool's first share class");
    require(ghostPoolA64 != ghostPoolB64
        ? ghostShareClassB == NEW_SHARE_CLASS_ID_SC_CVL(ghostPoolB64, 1)
        : (ghostShareClassA == ghostShareClassB || ghostShareClassB == NEW_SHARE_CLASS_ID_SC_CVL(ghostPoolA64, 2)),
        "SCOPE: class B is its pool's first, or second if pools match");
}

definition SC_CLASS_INDEX(bytes16 c) returns mathint =
    c == NEW_SHARE_CLASS_ID_SC_CVL(ghostPoolA64, 2) ? 2 : 1;
