import "setup/Spoke_LinkedSpokeCore_two_escrows.spec";

// --- high_level ---

// SP-HL-61: an escrow call on one pool never changes another pool's escrow books or lowers its balances.
rule hlSpEscrowResolvedEntryLeavesAnotherPoolsEscrowAlone(env e, uint8 op, SpokeHarness.PoolId poolId,
    uint64 otherPool, SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver,
    uint128 amount, address reserver, bytes32 reason, SpokeHarness.ShareClassId otherScId,
    address otherAsset, uint256 otherTokenId, address otherReserver, bytes32 otherReason,
    address token, uint256 id) {

    setupSpokeLinkedSpokeCoreTwoEscrows(e, otherPool);

    uint128 totalBefore;
    uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrowB.holding(otherScId, otherAsset, otherTokenId);
    mathint bucketBefore = _PoolEscrowB.reservedBy(otherScId, otherReserver, otherReason, otherAsset, otherTokenId);
    mathint erc20Before = ghostERC20Balances128[token][_PoolEscrowB];
    mathint erc6909Before = ghostERC6909Balances128[token][id][_PoolEscrowB];

    if (op == 0) {
        _Spoke.deposit(e, poolId, scId, asset, tokenId, amount);
    } else if (op == 1) {
        _Spoke.noteDeposit(e, poolId, scId, asset, tokenId, amount);
    } else if (op == 2) {
        _Spoke.withdraw(e, poolId, scId, asset, tokenId, receiver, amount);
    } else if (op == 3) {
        _Spoke.withdrawReserved(e, poolId, scId, asset, tokenId, receiver, amount, reserver, reason);
    } else if (op == 4) {
        _Spoke.reserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);
    } else if (op == 5) {
        _Spoke.unreserve(e, poolId, scId, asset, tokenId, amount, reserver, reason);
    } else {
        _Spoke.withdrawShares(e, poolId, scId, receiver, amount);
    }

    uint128 totalAfter;
    uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrowB.holding(otherScId, otherAsset, otherTokenId);
    mathint bucketAfter = _PoolEscrowB.reservedBy(otherScId, otherReserver, otherReason, otherAsset, otherTokenId);

    assert(totalAfter == totalBefore && reservedAfter == reservedBefore && bucketAfter == bucketBefore
            && ghostERC20Balances128[token][_PoolEscrowB] >= erc20Before
            && ghostERC6909Balances128[token][id][_PoolEscrowB] >= erc6909Before,
        "another pool's escrow books stay and its balances do not fall");
}
