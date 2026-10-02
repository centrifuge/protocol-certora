import "Escrow_valid_state.spec";

// PE-HL-01: the available balance is the unreserved part of the holding, never below zero.
rule hlPeAvailableBalanceIsTheUnreservedCustody(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId) {

    setupPoolEscrowValidState(e);

    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;
    mathint availableExpected = totalBefore >= reservedBefore ? totalBefore - reservedBefore : 0;

    mathint availableReported = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    assert(availableReported == availableExpected, "the available balance is total minus reserved, floored at zero");
}

// PE-HL-02: withdrawing all the available balance leaves only the reserved amount held.
rule hlPeSweepingTheFreeBalanceLeavesTheEarmarks(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, address receiver) {

    setupPoolEscrowValidState(e);

    mathint reservedBefore = ghostPeReserved128;

    uint128 advertisedFree = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);
    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, advertisedFree);

    mathint totalAfter = ghostPeTotal128;

    assert(totalAfter == reservedBefore, "a payout of all free funds brings the total to what is reserved");
}

// PE-HL-03: reserving then releasing the same amount restores the reservation.
rule hlPeReserveThenReleaseRestoresTheBucket(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value, address reserver, bytes32 reason) {

    setupPoolEscrowValidState(e);

    mathint bucketBefore = ghostPeReservedBy128[reserver][reason];

    _PoolEscrow.reserve(e, scId, asset, tokenId, value, reserver, reason);
    _PoolEscrow.unreserve(e, scId, asset, tokenId, value, reserver, reason);

    mathint bucketAfter = ghostPeReservedBy128[reserver][reason];

    assert(bucketAfter == bucketBefore, "an unreserve undoes a reserve of the same amount");
}

// PE-HL-04: a deposit and withdrawal of the same amount leave the holding total unchanged.
rule hlPeTakeInThenPayOutRestoresTheCustody(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value, address receiver) {

    setupPoolEscrowValidState(e);

    mathint totalBefore = ghostPeTotal128;

    _PoolEscrow.deposit(e, scId, asset, tokenId, value);
    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, value);

    mathint totalAfter = ghostPeTotal128;

    assert(totalAfter == totalBefore, "a deposit then a withdrawal of one amount restores the total");
}

// PE-HL-05: a deposit and withdrawal of the same amount leave the reserved amount unchanged.
rule hlPeCustodyRoundTripTouchesNoHold(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value, address receiver) {

    setupPoolEscrowValidState(e);

    mathint reservedBefore = ghostPeReserved128;

    _PoolEscrow.deposit(e, scId, asset, tokenId, value);
    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, value);

    mathint reservedAfter = ghostPeReserved128;

    assert(reservedAfter == reservedBefore, "a deposit then a withdrawal of one amount keeps the reserved total");
}

// PE-HL-06: a new reservation by any reserver immediately caps what can be withdrawn.
rule hlPeAnyHoldCapsEveryPayout(env e, Escrow.ShareClassId scId, address asset, uint256 tokenId,
    uint128 hold, address reserver, bytes32 reason, address receiver, uint128 payout) {

    setupPoolEscrowValidState(e);

    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;
    mathint freeAfterHold = totalBefore >= reservedBefore + hold ? totalBefore - reservedBefore - hold : 0;
    mathint payoutRequested = payout;

    _PoolEscrow.reserve(e, scId, asset, tokenId, hold, reserver, reason);
    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, payout);

    assert(payoutRequested <= freeAfterHold, "a withdrawal after a new reservation stays within what is available");
}
