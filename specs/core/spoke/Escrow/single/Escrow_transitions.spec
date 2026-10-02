import "Escrow_valid_state.spec";

// --- state_transitions ---

// PE-ST-01: no call can reduce a holding by more than its prior available balance.
rule stPePayoutBoundedByFreeBalance(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_PE(f) } {

    setupPoolEscrowValidState(e);

    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;
    mathint availableBefore = totalBefore >= reservedBefore ? totalBefore - reservedBefore : 0;

    f(e, args);

    assert(totalBefore - ghostPeTotal128 <= availableBefore, "no call lowers the total by more than was available");
}

// PE-ST-02: a single call changes at most one reservation.
rule stPeOneCallTouchesOneBucket(env e, method f, calldataarg args, address r1, bytes32 reason1,
    address r2, bytes32 reason2) filtered { f -> !EXCLUDED_FUNCTION_PE(f) } {

    setupPoolEscrowValidState(e);
    require(r1 != r2 || reason1 != reason2, "SCOPE: two distinct reservations");

    mathint bucket1Before = ghostPeReservedBy128[r1][reason1];
    mathint bucket2Before = ghostPeReservedBy128[r2][reason2];

    f(e, args);

    assert(ghostPeReservedBy128[r1][reason1] != bucket1Before
        => ghostPeReservedBy128[r2][reason2] == bucket2Before,
        "when one reservation moves, every other stays put");
}

// PE-ST-03: only a withdrawal lowers the holding total.
rule stPeOnlyAWithdrawalLowersTheCustodyTotal(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_PE(f) } {

    setupPoolEscrowValidState(e);

    mathint totalBefore = ghostPeTotal128;

    f(e, args);

    assert(ghostPeTotal128 < totalBefore
        => f.selector == sig:_PoolEscrow.withdraw(Escrow.ShareClassId, address, uint256, address,
            uint128).selector,
        "only a withdrawal lowers the escrow's total");
}
