import "setup/Escrow_unpinned.spec";

// --- valid_state ---

// PE-VS-03: every holding's reserved amount equals the sum of all its reservations.
invariant reservedIsTheSumOfEveryBucket()
    ghostPeReservedRow == ghostPeBucketSumRow
filtered { f -> !EXCLUDED_FUNCTION_PE_UP(f) }

// --- variable_transitions ---

// PE-VT-01: only deposit or withdraw moves a holding's total, only reserve or unreserve its reserved amount.
rule vtPeTotalMovesOnlyOnFlowsAndReservedOnlyOnReservations(env e, method f, calldataarg args,
    Escrow.ShareClassId scId, address asset, uint256 tokenId)
    filtered { f -> !EXCLUDED_FUNCTION_PE_UP(f) } {

    setupPoolEscrowUnpinned(e);

    uint128 totalBefore; uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(scId, asset, tokenId);

    f(e, args);

    uint128 totalAfter; uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(scId, asset, tokenId);

    assert(totalAfter != totalBefore
        => f.selector == sig:_PoolEscrow.deposit(Escrow.ShareClassId, address, uint256, uint128).selector
            || f.selector == sig:_PoolEscrow.withdraw(Escrow.ShareClassId, address, uint256, address,
                uint128).selector,
        "only a deposit or a withdrawal moves a holding's total");
    assert(reservedAfter != reservedBefore
        => f.selector == sig:_PoolEscrow.reserve(Escrow.ShareClassId, address, uint256, uint128, address,
                bytes32).selector
            || f.selector == sig:_PoolEscrow.unreserve(Escrow.ShareClassId, address, uint256, uint128, address,
                bytes32).selector,
        "only a reservation or its release moves a holding's reserved amount");
}

// --- state_transitions ---

// PE-ST-05: a call moves the total or reserved amount of at most one holding.
rule stPeACallMovesAtMostOneHoldingRow(env e, method f, calldataarg args, Escrow.ShareClassId scId,
    address asset, uint256 tokenId, Escrow.ShareClassId scId2, address asset2, uint256 tokenId2)
    filtered { f -> !EXCLUDED_FUNCTION_PE_UP(f) } {

    setupPoolEscrowUnpinned(e);
    require(scId2 != scId || asset2 != asset || tokenId2 != tokenId, "SCOPE: two distinct holdings");

    uint128 totalBefore; uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2Before; uint128 reserved2Before;
    total2Before, reserved2Before = _PoolEscrow.holding(scId2, asset2, tokenId2);

    f(e, args);

    uint128 totalAfter; uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2After; uint128 reserved2After;
    total2After, reserved2After = _PoolEscrow.holding(scId2, asset2, tokenId2);

    assert(totalAfter != totalBefore || reservedAfter != reservedBefore
        => total2After == total2Before && reserved2After == reserved2Before,
        "a call moves at most one holding");
}

// --- high_level ---

// PE-HL-09: a deposit changes only its holding's total, adding exactly the amount.
rule hlPeDepositMovesExactlyItsOwnRow(env e, Escrow.ShareClassId scId, address asset, uint256 tokenId,
    uint128 value, Escrow.ShareClassId scId2, address asset2, uint256 tokenId2) {

    setupPoolEscrowUnpinned(e);

    bool otherRow = scId2 != scId || asset2 != asset || tokenId2 != tokenId;
    uint128 totalBefore; uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2Before; uint128 reserved2Before;
    total2Before, reserved2Before = _PoolEscrow.holding(scId2, asset2, tokenId2);

    _PoolEscrow.deposit(e, scId, asset, tokenId, value);

    uint128 totalAfter; uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2After; uint128 reserved2After;
    total2After, reserved2After = _PoolEscrow.holding(scId2, asset2, tokenId2);

    assert(totalAfter == totalBefore + value && reservedAfter == reservedBefore,
        "the holding's total grows by the amount, its reserved amount unchanged");
    assert(otherRow => total2After == total2Before && reserved2After == reserved2Before,
        "no other holding's total or reserved amount changes");
}

// PE-HL-10: a withdrawal changes only its holding's total, taking off exactly the amount.
rule hlPeWithdrawMovesExactlyItsOwnRow(env e, Escrow.ShareClassId scId, address asset, uint256 tokenId,
    address receiver, uint128 value, Escrow.ShareClassId scId2, address asset2, uint256 tokenId2) {

    setupPoolEscrowUnpinned(e);

    bool otherRow = scId2 != scId || asset2 != asset || tokenId2 != tokenId;
    uint128 totalBefore; uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2Before; uint128 reserved2Before;
    total2Before, reserved2Before = _PoolEscrow.holding(scId2, asset2, tokenId2);

    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, value);

    uint128 totalAfter; uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2After; uint128 reserved2After;
    total2After, reserved2After = _PoolEscrow.holding(scId2, asset2, tokenId2);

    assert(totalAfter == totalBefore - value && reservedAfter == reservedBefore,
        "the holding's total drops by the amount, its reserved amount unchanged");
    assert(otherRow => total2After == total2Before && reserved2After == reserved2Before,
        "no other holding's total or reserved amount changes");
}

// PE-HL-11: reserving adds the amount to the reservation and to its holding's reserved amount alone.
rule hlPeReserveMirrorsBucketAndAggregateExactly(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value, address caller, bytes32 reason, Escrow.ShareClassId scId2,
    address asset2, uint256 tokenId2) {

    setupPoolEscrowUnpinned(e);

    mathint bucketBefore = _PoolEscrow.reservedBy(scId, caller, reason, asset, tokenId);
    uint128 totalBefore; uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2Before; uint128 reserved2Before;
    total2Before, reserved2Before = _PoolEscrow.holding(scId2, asset2, tokenId2);

    _PoolEscrow.reserve(e, scId, asset, tokenId, value, caller, reason);

    mathint bucketAfter = _PoolEscrow.reservedBy(scId, caller, reason, asset, tokenId);
    uint128 totalAfter; uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2After; uint128 reserved2After;
    total2After, reserved2After = _PoolEscrow.holding(scId2, asset2, tokenId2);

    assert(bucketAfter == bucketBefore + value && reservedAfter == reservedBefore + value,
        "both the reservation and the reserved amount grow by exactly this much");
    assert(total2After == total2Before, "no holding's total changes, its own included");
    assert((scId2 != scId || asset2 != asset || tokenId2 != tokenId) => reserved2After == reserved2Before,
        "no other holding's reserved amount changes");
}

// PE-HL-12: releasing takes the amount off the reservation and off its holding's reserved amount alone.
rule hlPeUnreserveMirrorsBucketAndAggregateExactly(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value, address caller, bytes32 reason, Escrow.ShareClassId scId2,
    address asset2, uint256 tokenId2) {

    setupPoolEscrowUnpinned(e);

    mathint bucketBefore = _PoolEscrow.reservedBy(scId, caller, reason, asset, tokenId);
    uint128 totalBefore; uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2Before; uint128 reserved2Before;
    total2Before, reserved2Before = _PoolEscrow.holding(scId2, asset2, tokenId2);

    _PoolEscrow.unreserve(e, scId, asset, tokenId, value, caller, reason);

    mathint bucketAfter = _PoolEscrow.reservedBy(scId, caller, reason, asset, tokenId);
    uint128 totalAfter; uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(scId, asset, tokenId);
    uint128 total2After; uint128 reserved2After;
    total2After, reserved2After = _PoolEscrow.holding(scId2, asset2, tokenId2);

    assert(bucketAfter == bucketBefore - value && reservedAfter == reservedBefore - value,
        "both the reservation and the reserved amount drop by exactly this much");
    assert(total2After == total2Before, "no holding's total changes, its own included");
    assert((scId2 != scId || asset2 != asset || tokenId2 != tokenId) => reserved2After == reserved2Before,
        "no other holding's reserved amount changes");
}

// --- access_control ---

// PE-AC-05: admin rights change only through rely, which grants them, or deny, which revokes them.
rule acPeWardSeatMovesOnlyThroughRelyOrDeny(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_PE_UP(f) } {

    setupPoolEscrowUnpinned(e);

    mathint seatBefore = _PoolEscrow.wards(user);

    f(e, args);

    mathint seatAfter = _PoolEscrow.wards(user);

    assert(seatAfter != seatBefore
        => (f.selector == sig:_PoolEscrow.rely(address).selector && seatAfter == 1)
            || (f.selector == sig:_PoolEscrow.deny(address).selector && seatAfter == 0),
        "ward rights change only by rely setting 1 or deny setting 0");
}
