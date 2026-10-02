import "../setup/Escrow_base.spec";

// PE-AC-01: only an admin can change an escrow holding's total.
rule acPeOnlyWardMovesTheCustodyTotal(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_PE(f) } {

    setupPoolEscrow(e);

    mathint senderWardBefore = _PoolEscrow.wards[e.msg.sender];
    mathint totalBefore = ghostPeTotal128;

    f(e, args);

    mathint totalAfter = ghostPeTotal128;

    assert(totalAfter != totalBefore => senderWardBefore == 1, "a non-ward caller leaves the escrowed total unchanged");
}

// PE-AC-02: only an admin can change an escrow holding's reserved amount.
rule acPeOnlyWardMovesTheAggregateHold(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_PE(f) } {

    setupPoolEscrow(e);

    mathint senderWardBefore = _PoolEscrow.wards[e.msg.sender];
    mathint reservedBefore = ghostPeReserved128;

    f(e, args);

    mathint reservedAfter = ghostPeReserved128;

    assert(reservedAfter != reservedBefore => senderWardBefore == 1, "only a ward can change the reserved total");
}

// PE-AC-03: only an admin can change a reserver's reservation.
rule acPeOnlyWardMovesAReservationBucket(env e, method f, calldataarg args, address reserver,
    bytes32 reason) filtered { f -> !EXCLUDED_FUNCTION_PE(f) } {

    setupPoolEscrow(e);

    mathint senderWardBefore = _PoolEscrow.wards[e.msg.sender];
    mathint bucketBefore = ghostPeReservedBy128[reserver][reason];

    f(e, args);

    mathint bucketAfter = ghostPeReservedBy128[reserver][reason];

    assert(bucketAfter != bucketBefore => senderWardBefore == 1,
        "a non-ward caller leaves every reservation as it was");
}

// PE-AC-04: only an admin can grant or revoke admin rights on the escrow.
rule acPeOnlyWardMovesAWardSeat(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_PE(f) } {

    setupPoolEscrow(e);

    mathint senderWardBefore = _PoolEscrow.wards[e.msg.sender];
    mathint seatBefore = _PoolEscrow.wards[user];

    f(e, args);

    mathint seatAfter = _PoolEscrow.wards[user];

    assert(seatAfter != seatBefore => senderWardBefore == 1, "a non-ward cannot change anyone's ward status in escrow");
}
