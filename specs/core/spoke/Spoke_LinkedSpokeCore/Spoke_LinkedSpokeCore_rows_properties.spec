import "setup/Spoke_LinkedSpokeCore_rows_base.spec";

// --- high_level ---

// SP-HL-54: a deposit adds the amount to its holding, a withdrawal takes it, a reserved one from both holds too.
rule hlSpEscrowEntryMovesItsOwnRowByExactlyTheAmount(env e, uint8 op, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount,
    address reserver, bytes32 reason) {

    setupSpokeLinkedSpokeCoreRows(e);

    uint128 totalBefore;
    uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(scId, asset, tokenId);
    mathint bucketBefore = _PoolEscrow.reservedBy(scId, reserver, reason, asset, tokenId);

    if (op == 0) {
        _Spoke.deposit(e, poolId, scId, asset, tokenId, amount);
    } else if (op == 1) {
        _Spoke.noteDeposit(e, poolId, scId, asset, tokenId, amount);
    } else if (op == 2) {
        _Spoke.withdraw(e, poolId, scId, asset, tokenId, receiver, amount);
    } else {
        _Spoke.withdrawReserved(e, poolId, scId, asset, tokenId, receiver, amount, reserver, reason);
    }

    uint128 totalAfter;
    uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(scId, asset, tokenId);
    mathint bucketAfter = _PoolEscrow.reservedBy(scId, reserver, reason, asset, tokenId);

    assert(op <= 1
        ? (totalAfter == totalBefore + amount && reservedAfter == reservedBefore && bucketAfter == bucketBefore)
        : op == 2
            ? (totalAfter == totalBefore - amount && reservedAfter == reservedBefore
                && bucketAfter == bucketBefore)
            : (totalAfter == totalBefore - amount && reservedAfter == reservedBefore - amount
                && bucketAfter == bucketBefore - amount),
        "deposits add, withdrawals remove; only a reserved one moves both holds");
}

// SP-HL-55: a deposit or withdrawal leaves every other holding and reservation in the escrow unchanged.
rule hlSpEscrowEntryTouchesOnlyItsOwnRow(env e, uint8 op, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount,
    address reserver, bytes32 reason, SpokeHarness.ShareClassId otherScId, address otherAsset,
    uint256 otherTokenId, address otherReserver, bytes32 otherReason) {

    setupSpokeLinkedSpokeCoreRows(e);

    bool otherRow = otherScId != scId || otherAsset != asset || otherTokenId != tokenId;
    bool otherBucket = otherRow || otherReserver != reserver || otherReason != reason;

    uint128 totalBefore;
    uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(otherScId, otherAsset, otherTokenId);
    mathint bucketBefore = _PoolEscrow.reservedBy(otherScId, otherReserver, otherReason, otherAsset, otherTokenId);

    if (op == 0) {
        _Spoke.deposit(e, poolId, scId, asset, tokenId, amount);
    } else if (op == 1) {
        _Spoke.noteDeposit(e, poolId, scId, asset, tokenId, amount);
    } else if (op == 2) {
        _Spoke.withdraw(e, poolId, scId, asset, tokenId, receiver, amount);
    } else {
        _Spoke.withdrawReserved(e, poolId, scId, asset, tokenId, receiver, amount, reserver, reason);
    }

    uint128 totalAfter;
    uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(otherScId, otherAsset, otherTokenId);
    mathint bucketAfter = _PoolEscrow.reservedBy(otherScId, otherReserver, otherReason, otherAsset, otherTokenId);

    assert((otherRow => totalAfter == totalBefore && reservedAfter == reservedBefore)
            && (otherBucket => bucketAfter == bucketBefore),
        "other holdings and reservations stay as they were");
}
