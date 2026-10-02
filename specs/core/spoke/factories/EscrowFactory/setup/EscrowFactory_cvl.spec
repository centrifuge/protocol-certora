// EscrowFactory. Model: ghost escrow addresses, for scenes not compiling it.

methods {
    function _.escrow(uint64 poolId) external
        => escrowFactoryEscrowCVL(poolId) expect address UNRESOLVED;

    // UNSAFE: no deploy, newEscrow(p) returns escrow(p) mapped back to p.
    function _.newEscrow(uint64 poolId) external
        => escrowFactoryNewEscrowCVL(poolId) expect address UNRESOLVED;
    function _.poolId(address escrow) external
        => escrowFactoryPoolIdCVL(escrow) expect uint64 UNRESOLVED;
}

// Uninterpreted image of the CREATE2 address escrow(p) computes.
persistent ghost ghostEfEscrow(uint64) returns address {
    // SAFE: injective, as a 160-bit CREATE2 collision is infeasible.
    axiom forall uint64 p1. forall uint64 p2.
        p1 != p2 => ghostEfEscrow(p1) != ghostEfEscrow(p2);

    // UNSAFE: never zero, so the null address gates stay meaningful.
    axiom forall uint64 p. ghostEfEscrow(p) != 0;
}

function escrowFactoryEscrowCVL(uint64 poolId) returns address {
    return ghostEfEscrow(poolId);
}

persistent ghost mathint ghostEfNewEscrowCount {
    init_state axiom ghostEfNewEscrowCount == 0;
    axiom ghostEfNewEscrowCount >= 0;
}
persistent ghost mathint ghostEfLastNewEscrowPool64;

persistent ghost mapping(address => mathint) ghostEfPoolId64 {
    axiom forall address a. ghostEfPoolId64[a] >= 0 && ghostEfPoolId64[a] <= max_uint64;
}

function escrowFactoryNewEscrowCVL(uint64 poolId) returns address {
    ghostEfNewEscrowCount = ghostEfNewEscrowCount + 1;
    ghostEfLastNewEscrowPool64 = poolId;
    ghostEfPoolId64[ghostEfEscrow(poolId)] = poolId;
    return ghostEfEscrow(poolId);
}

function escrowFactoryPoolIdCVL(address escrow) returns uint64 {
    return require_uint64(ghostEfPoolId64[escrow]);
}
