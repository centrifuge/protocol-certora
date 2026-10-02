// Fee accrual hook model: both calls silent, for scenes where the hook sits outside.

methods {
    // SCOPE: the hook's effects lie outside the scene.
    function _.accrue(uint64 poolId, bytes16 scId) external
        => feeAccrualAccrueCVL(calledContract, poolId, scId) expect void UNRESOLVED;
    function _.accrued(uint64 poolId, bytes16 scId) external
        => NONDET;
}

persistent ghost mathint ghostFaAccrueCount {
    init_state axiom ghostFaAccrueCount == 0;
    axiom ghostFaAccrueCount >= 0;
}
persistent ghost address ghostFaLastCallee;
persistent ghost uint64 ghostFaLastPool64;
persistent ghost bytes16 ghostFaLastScId;

function feeAccrualAccrueCVL(address accrual, uint64 poolId, bytes16 scId) {
    ghostFaAccrueCount = ghostFaAccrueCount + 1;
    ghostFaLastCallee = accrual;
    ghostFaLastPool64 = poolId;
    ghostFaLastScId = scId;
}
