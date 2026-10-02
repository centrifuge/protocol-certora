import "Escrow_valid_state.spec";

// PE-RC-01: a deposit can increase the holding of an ERC6909 token.
rule rcPeDepositBooksAnErc6909Row(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value) {

    setupPoolEscrowValidState(e);

    mathint rowTokenId = tokenId;
    mathint totalBefore = ghostPeTotal128;

    _PoolEscrow.deposit(e, scId, asset, tokenId, value);

    mathint totalAfter = ghostPeTotal128;

    satisfy(rowTokenId != 0 && totalAfter > totalBefore,
        "a deposit under a nonzero token id can grow the escrowed total");
}

// PE-RC-02: a deposit into a fully reserved holding can make funds available again.
rule rcPeDepositReopensAFullyEncumberedRow(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value) {

    setupPoolEscrowValidState(e);

    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;
    mathint freeBefore = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    _PoolEscrow.deposit(e, scId, asset, tokenId, value);

    mathint freeAfter = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    satisfy(reservedBefore > 0 && reservedBefore == totalBefore && freeBefore == 0 && freeAfter > 0,
        "new funds can unlock a holding that was all reserved");
}

// PE-RC-03: a withdrawal can empty a holding that has no reservations.
rule rcPeWithdrawEmptiesAnUnencumberedRow(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, address receiver, uint128 value) {

    setupPoolEscrowValidState(e);

    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;

    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, value);

    mathint totalAfter = ghostPeTotal128;

    satisfy(reservedBefore == 0 && totalBefore > 0 && totalAfter == 0, "a withdrawal can empty an unreserved holding");
}

// PE-RC-04: the whole available balance can be withdrawn at once while reservations remain.
rule rcPeWithdrawSweepsTheAdvertisedFreeBalance(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, address receiver) {

    setupPoolEscrowValidState(e);

    mathint reservedBefore = ghostPeReserved128;
    uint128 advertisedFree = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);
    mathint sweptAmount = advertisedFree;

    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, advertisedFree);

    mathint totalAfter = ghostPeTotal128;

    satisfy(reservedBefore > 0 && sweptAmount > 0 && totalAfter == reservedBefore,
        "a withdrawal can take all that is available, leaving only the reserved");
}

// PE-RC-05: a partial withdrawal from a reserved holding can leave funds still available.
rule rcPeWithdrawLeavesTheRowStillPaying(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, address receiver, uint128 value) {

    setupPoolEscrowValidState(e);

    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;

    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, value);

    mathint totalAfter = ghostPeTotal128;
    mathint freeAfter = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    satisfy(reservedBefore > 0 && totalAfter < totalBefore && freeAfter > 0,
        "a reserved holding can keep free funds after paying out");
}

// PE-RC-06: a withdrawal can be recorded with the zero address as receiver.
rule rcPeWithdrawBooksAPayoutToANullReceiver(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, address receiver, uint128 value) {

    setupPoolEscrowValidState(e);

    mathint totalBefore = ghostPeTotal128;

    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, value);

    mathint totalAfter = ghostPeTotal128;

    satisfy(receiver == 0 && totalAfter < totalBefore,
        "a withdrawal naming the zero address as receiver can be booked");
}

// PE-RC-07: a new reservation can be opened, raising the holding's reserved amount.
rule rcPeReserveOpensABucket(env e, Escrow.ShareClassId scId, address asset, uint256 tokenId,
    uint128 value, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    mathint bucketBefore = ghostPeReservedBy128[keyHolder][reason];
    mathint reservedBefore = ghostPeReserved128;

    _PoolEscrow.reserve(e, scId, asset, tokenId, value, keyHolder, reason);

    mathint bucketAfter = ghostPeReservedBy128[keyHolder][reason];
    mathint reservedAfter = ghostPeReserved128;

    satisfy(bucketBefore == 0 && bucketAfter > 0 && reservedAfter > reservedBefore,
        "a reservation can start from zero and raise the reserved total");
}

// PE-RC-08: an admin can reserve funds for another account that has no admin rights.
rule rcPeReserveBooksABucketForAnUnauthorizedKey(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    mathint keyHolderWard = _PoolEscrow.wards(e, keyHolder);
    mathint bucketBefore = ghostPeReservedBy128[keyHolder][reason];

    _PoolEscrow.reserve(e, scId, asset, tokenId, value, keyHolder, reason);

    mathint bucketAfter = ghostPeReservedBy128[keyHolder][reason];

    satisfy(keyHolder != e.msg.sender && keyHolderWard == 0 && bucketAfter > bucketBefore,
        "a ward can reserve on behalf of an account that is not a ward");
}

// PE-RC-09: an admin can fully release another account's reservation.
rule rcPeUnreserveEmptiesAForeignBucket(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    mathint keyHolderWard = _PoolEscrow.wards(e, keyHolder);
    mathint bucketBefore = ghostPeReservedBy128[keyHolder][reason];
    mathint reservedBefore = ghostPeReserved128;

    _PoolEscrow.unreserve(e, scId, asset, tokenId, require_uint128(bucketBefore), keyHolder, reason);

    mathint bucketAfter = ghostPeReservedBy128[keyHolder][reason];
    mathint reservedAfter = ghostPeReserved128;

    satisfy(keyHolder != e.msg.sender && keyHolderWard == 0 && bucketBefore > 0 && bucketAfter == 0
        && reservedAfter < reservedBefore,
        "a ward can release all of a non-ward's reservation");
}

// PE-RC-10: two reservers can hold reservations on the same holding at once.
rule rcPeTwoReserversHoldOneRowAtOnce(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 firstHold, uint128 secondHold, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolderA = ghostPeReserverE1;
    address keyHolderB = ghostPeReserverE2;
    mathint bucketABefore = ghostPeReservedBy128[keyHolderA][reason];
    mathint bucketBBefore = ghostPeReservedBy128[keyHolderB][reason];

    _PoolEscrow.reserve(e, scId, asset, tokenId, firstHold, keyHolderA, reason);
    _PoolEscrow.reserve(e, scId, asset, tokenId, secondHold, keyHolderB, reason);

    mathint bucketAAfter = ghostPeReservedBy128[keyHolderA][reason];
    mathint bucketBAfter = ghostPeReservedBy128[keyHolderB][reason];
    mathint reservedAfter = ghostPeReserved128;

    satisfy(bucketABefore == 0 && bucketBBefore == 0 && bucketAAfter > 0 && bucketBAfter > 0
        && reservedAfter == bucketAAfter + bucketBAfter,
        "two reservers can reserve at once, the reserved total their sum");
}

// PE-RC-11: one reserver can hold two reservations on a holding under different reasons.
rule rcPeOneReserverHoldsTwoReasons(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 firstHold, uint128 secondHold) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    bytes32 reasonA = ghostPeReasonE1;
    bytes32 reasonB = ghostPeReasonE2;
    mathint bucketABefore = ghostPeReservedBy128[keyHolder][reasonA];
    mathint bucketBBefore = ghostPeReservedBy128[keyHolder][reasonB];

    _PoolEscrow.reserve(e, scId, asset, tokenId, firstHold, keyHolder, reasonA);
    _PoolEscrow.reserve(e, scId, asset, tokenId, secondHold, keyHolder, reasonB);

    mathint bucketAAfter = ghostPeReservedBy128[keyHolder][reasonA];
    mathint bucketBAfter = ghostPeReservedBy128[keyHolder][reasonB];
    mathint reservedAfter = ghostPeReserved128;

    satisfy(bucketABefore == 0 && bucketBBefore == 0 && bucketAAfter > 0 && bucketBAfter > 0
        && reservedAfter == bucketAAfter + bucketBAfter,
        "one reserver's two reasons can split the reserved total");
}

// PE-RC-12: one reservation can over-reserve a holding, leaving nothing available.
rule rcPeReserveBeyondCustodyFreezesTheRow(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    mathint freeBefore = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    _PoolEscrow.reserve(e, scId, asset, tokenId, value, keyHolder, reason);

    mathint totalAfter = ghostPeTotal128;
    mathint reservedAfter = ghostPeReserved128;
    mathint freeAfter = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    satisfy(freeBefore > 0 && reservedAfter > totalAfter && freeAfter == 0,
        "reserving past the held amount can freeze funds that were free");
}

// PE-RC-13: one reservation can take the whole available balance, leaving nothing free.
rule rcPeReserveEncumbersTheWholeFreeBalance(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    uint128 advertisedFree = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);
    mathint heldAmount = advertisedFree;

    _PoolEscrow.reserve(e, scId, asset, tokenId, advertisedFree, keyHolder, reason);

    mathint totalAfter = ghostPeTotal128;
    mathint reservedAfter = ghostPeReserved128;
    mathint freeAfter = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    satisfy(heldAmount > 0 && reservedAfter == totalAfter && freeAfter == 0,
        "reserving all free funds can make the reserved sum equal the total");
}

// PE-RC-14: releasing one full reservation can leave the holding with nothing reserved.
rule rcPeUnreserveClearsTheRowsEarmark(env e, Escrow.ShareClassId scId, address asset, uint256 tokenId,
    bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    mathint bucketBefore = ghostPeReservedBy128[keyHolder][reason];

    _PoolEscrow.unreserve(e, scId, asset, tokenId, require_uint128(bucketBefore), keyHolder, reason);

    mathint bucketAfter = ghostPeReservedBy128[keyHolder][reason];
    mathint reservedAfter = ghostPeReserved128;

    satisfy(bucketBefore > 0 && bucketAfter == 0 && reservedAfter == 0,
        "unreserving in full can bring the reserved total to zero");
}

// PE-RC-15: a reservation can be partly released, keeping the rest reserved.
rule rcPeUnreserveLeavesTheBucketStillHolding(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    mathint bucketBefore = ghostPeReservedBy128[keyHolder][reason];
    mathint reservedBefore = ghostPeReserved128;

    _PoolEscrow.unreserve(e, scId, asset, tokenId, value, keyHolder, reason);

    mathint bucketAfter = ghostPeReservedBy128[keyHolder][reason];
    mathint reservedAfter = ghostPeReserved128;

    satisfy(bucketAfter > 0 && bucketAfter < bucketBefore && reservedAfter < reservedBefore,
        "a partial release can leave the reservation still standing");
}

// PE-RC-16: one reserver's reservation can be released in full while another's stays intact.
rule rcPeReleasingOneBucketLeavesTheOtherHeld(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 firstHold, uint128 secondHold, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolderA = ghostPeReserverE1;
    address keyHolderB = ghostPeReserverE2;
    mathint bucketABefore = ghostPeReservedBy128[keyHolderA][reason];
    mathint bucketBBefore = ghostPeReservedBy128[keyHolderB][reason];

    _PoolEscrow.reserve(e, scId, asset, tokenId, firstHold, keyHolderA, reason);
    _PoolEscrow.reserve(e, scId, asset, tokenId, secondHold, keyHolderB, reason);

    mathint bucketBHeld = ghostPeReservedBy128[keyHolderB][reason];

    _PoolEscrow.unreserve(e, scId, asset, tokenId, firstHold, keyHolderA, reason);

    mathint bucketAAfter = ghostPeReservedBy128[keyHolderA][reason];
    mathint bucketBAfter = ghostPeReservedBy128[keyHolderB][reason];
    mathint reservedAfter = ghostPeReserved128;

    satisfy(bucketABefore == 0 && bucketBBefore == 0 && bucketAAfter == 0 && bucketBAfter == bucketBHeld
        && bucketBAfter > 0 && reservedAfter == bucketBAfter,
        "one reservation can be fully released while another stands untouched");
}

// PE-RC-17: after a release, an over-reserved holding can allow withdrawals again.
rule rcPeReleaseLetsAnOverEncumberedRowPayOutAgain(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 hold, uint128 release, address receiver, uint128 payout, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    mathint totalBefore = ghostPeTotal128;

    _PoolEscrow.reserve(e, scId, asset, tokenId, hold, keyHolder, reason);

    mathint reservedUnderHold = ghostPeReserved128;
    mathint freeUnderHold = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    _PoolEscrow.unreserve(e, scId, asset, tokenId, release, keyHolder, reason);
    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, payout);

    mathint totalAfter = ghostPeTotal128;

    satisfy(reservedUnderHold > totalBefore && freeUnderHold == 0 && totalAfter < totalBefore,
        "an over-reserved holding can be released and withdrawn from again");
}

// PE-RC-18: a reservation can hold funds back from a withdrawal, then free them on release.
rule rcPeHoldPayoutReleaseWidensTheFreeBalance(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 hold, address receiver, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    mathint heldAmount = hold;

    _PoolEscrow.reserve(e, scId, asset, tokenId, hold, keyHolder, reason);

    uint128 freeUnderHold = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);
    mathint payableUnderHold = freeUnderHold;

    _PoolEscrow.withdraw(e, scId, asset, tokenId, receiver, freeUnderHold);

    mathint freeAfterPayout = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    _PoolEscrow.unreserve(e, scId, asset, tokenId, hold, keyHolder, reason);

    mathint freeAfterRelease = _PoolEscrow.availableBalanceOf(e, scId, asset, tokenId);

    satisfy(heldAmount > 0 && payableUnderHold > 0 && freeAfterPayout == 0 && freeAfterRelease == heldAmount,
        "a release after a full withdrawal frees exactly the reserved amount");
}

// PE-RC-19: an admin can revoke another admin while keeping its own rights.
rule rcPeDenyRevokesAnotherWard(env e, address user) {

    setupPoolEscrowValidState(e);

    mathint subjectBefore = _PoolEscrow.wards(e, user);

    _PoolEscrow.deny(e, user);

    mathint subjectAfter = _PoolEscrow.wards(e, user);
    mathint callerAfter = _PoolEscrow.wards(e, e.msg.sender);

    satisfy(user != e.msg.sender && subjectBefore == 1 && subjectAfter == 0 && callerAfter == 1,
        "a ward can remove a fellow ward yet stay seated");
}

// PE-RC-20: a newly added admin can record a deposit in the same block.
rule rcPeFreshlyReliedAccountBooksADeposit(env e, env eNewWard, Escrow.ShareClassId scId,
    address asset, uint256 tokenId, uint128 value) {

    setupPoolEscrowValidState(e);
    setupPoolEscrowValidState(eNewWard);
    require(eNewWard.block.number == e.block.number && eNewWard.block.timestamp == e.block.timestamp,
        "SCOPE: the grant and the first deposit in one block");

    address newWard = eNewWard.msg.sender;
    mathint wardBefore = _PoolEscrow.wards(e, newWard);
    mathint totalBefore = ghostPeTotal128;

    _PoolEscrow.rely(e, newWard);
    _PoolEscrow.deposit(eNewWard, scId, asset, tokenId, value);

    mathint totalAfter = ghostPeTotal128;

    satisfy(newWard != e.msg.sender && wardBefore == 0 && totalAfter > totalBefore,
        "a newly granted ward can deposit in the very next call");
}

// PE-RC-21: the reservation lookup can report exactly the amount just reserved.
rule rcPeBucketReadsBackTheHold(env e, Escrow.ShareClassId scId, address asset, uint256 tokenId,
    uint128 value, bytes32 reason) {

    setupPoolEscrowValidState(e);

    address keyHolder = ghostPeReserverE1;
    mathint heldAmount = value;
    mathint reportedBefore = _PoolEscrow.reservedBy(e, scId, keyHolder, reason, asset, tokenId);

    _PoolEscrow.reserve(e, scId, asset, tokenId, value, keyHolder, reason);

    mathint reportedAfter = _PoolEscrow.reservedBy(e, scId, keyHolder, reason, asset, tokenId);

    satisfy(heldAmount > 0 && reportedBefore == 0 && reportedAfter == heldAmount,
        "a new reservation reads back exactly through the public getter");
}
