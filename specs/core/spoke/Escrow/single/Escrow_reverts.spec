import "Escrow_valid_state.spec";

// PE-RV-01: a deposit fails for a caller without admin rights.
rule rvPeDepositRefusesANonWard(env e, Escrow.ShareClassId scId, address asset, uint256 tokenId,
    uint128 value) {

    setupPoolEscrowValidState(e);

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;

    _PoolEscrow.deposit@withrevert(e, scId, asset, tokenId, value);
    bool reverted = lastReverted;

    assert(callerHoldsNoWard => reverted, "a non-ward can never book a deposit");
}

// PE-RV-02: a withdrawal fails for a non-admin, an over-reserved holding, or more than is available.
rule rvPeWithdrawRefusesANonWardOrAPayoutBeyondTheFreeBalance(env e, Escrow.ShareClassId scId,
    address asset, uint256 tokenId, address receiver, uint128 value) {

    setupPoolEscrowValidState(e);

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;
    bool callerHoldsNoWard = wardOfCaller != 1;
    bool holdsOutrunCustody = totalBefore < reservedBefore;
    bool requestOutrunsTheFreeBalance = totalBefore - reservedBefore < value;

    _PoolEscrow.withdraw@withrevert(e, scId, asset, tokenId, receiver, value);
    bool reverted = lastReverted;

    assert((callerHoldsNoWard || holdsOutrunCustody || requestOutrunsTheFreeBalance) => reverted,
        "withdraw reverts for a non-ward, reserved above held, or an amount above free funds");
}

// PE-RV-03: a reservation fails for a caller without admin rights.
rule rvPeReserveRefusesANonWard(env e, Escrow.ShareClassId scId, address asset, uint256 tokenId,
    uint128 value, address reserver, bytes32 reason) {

    setupPoolEscrowValidState(e);

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;

    _PoolEscrow.reserve@withrevert(e, scId, asset, tokenId, value, reserver, reason);
    bool reverted = lastReverted;

    assert(callerHoldsNoWard => reverted, "a non-ward can never place a reservation");
}

// PE-RV-04: releasing a reservation fails for a non-admin or for more than it holds.
rule rvPeUnreserveRefusesANonWardOrAShortBucket(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, uint128 value, address reserver, bytes32 reason) {

    setupPoolEscrowValidState(e);

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    mathint bucketBefore = ghostPeReservedBy128[reserver][reason];
    bool callerHoldsNoWard = wardOfCaller != 1;
    bool bucketIsShort = bucketBefore < value;

    _PoolEscrow.unreserve@withrevert(e, scId, asset, tokenId, value, reserver, reason);
    bool reverted = lastReverted;

    assert((callerHoldsNoWard || bucketIsShort) => reverted,
        "an unreserve fails for a non-ward or above the named reservation");
}

// PE-RV-05: granting escrow admin rights fails for a non-admin caller.
rule rvPeRelyRefusesANonWard(env e, address user) {

    setupPoolEscrowValidState(e);

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;

    _PoolEscrow.rely@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerHoldsNoWard => reverted, "a non-ward's attempt to add an escrow ward reverts");
}

// PE-RV-06: revoking escrow admin rights fails for a non-admin caller.
rule rvPeDenyRefusesANonWard(env e, address user) {

    setupPoolEscrowValidState(e);

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;

    _PoolEscrow.deny@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerHoldsNoWard => reverted, "a non-ward's attempt to remove an escrow ward reverts");
}

// PE-RV-07: the available balance query never fails, even when a holding is over-reserved.
rule rvPeAvailableBalanceOfAlwaysAnswers(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId) {

    setupPoolEscrowValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    _PoolEscrow.availableBalanceOf@withrevert(e, scId, asset, tokenId);
    bool reverted = lastReverted;

    assert(!reverted, "the available balance is always readable, even when over-reserved");
}

// PE-RV-08: transferring assets out of the escrow fails for a non-admin caller.
rule rvPeAuthTransferToRefusesANonWard(env e, address asset, uint256 tokenId, address receiver,
    uint256 amount) {

    setupPoolEscrowValidState(e);

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;

    _PoolEscrow.authTransferTo@withrevert(e, asset, tokenId, receiver, amount);
    bool reverted = lastReverted;

    assert(callerHoldsNoWard => reverted, "a non-ward's direct transfer of tokens out of the escrow fails");
}

// PE-RV-09: recovering ETH or an ERC20 token fails for a non-admin caller.
rule rvPeRecoverTokensRefusesANonWard(env e, address token, address receiver, uint256 amount) {

    setupPoolEscrowValidState(e);

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;

    _PoolEscrow.recoverTokens@withrevert(e, token, receiver, amount);
    bool reverted = lastReverted;

    assert(callerHoldsNoWard => reverted, "a non-ward can never recover ether or ERC20 tokens");
}

// PE-RV-10: recovering a token by token id fails for a non-admin caller.
rule rvPeRecoverTokensByTokenIdRefusesANonWard(env e, address token, uint256 tokenId, address receiver,
    uint256 amount) {

    setupPoolEscrowValidState(e);

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    bool callerHoldsNoWard = wardOfCaller != 1;

    _PoolEscrow.recoverTokens@withrevert(e, token, tokenId, receiver, amount);
    bool reverted = lastReverted;

    assert(callerHoldsNoWard => reverted, "a non-ward can never recover tokens by token id");
}

// PE-RV-11: an admin can always release a reservation, up to its full amount.
rule rvPeUnreserveAlwaysAdmitsAKeyReleasingItsWholeBucket(env e, Escrow.ShareClassId scId,
    address asset, uint256 tokenId, uint128 value, address reserver, bytes32 reason) {

    setupPoolEscrowValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    mathint bucketBefore = ghostPeReservedBy128[reserver][reason];

    _PoolEscrow.unreserve@withrevert(e, scId, asset, tokenId, value, reserver, reason);
    bool reverted = lastReverted;

    assert((wardOfCaller == 1 && bucketBefore >= value) => !reverted,
        "a ward's unreserve within the named reservation never fails");
}

// PE-RV-12: an admin can always revoke its own admin rights.
rule rvPeDenyAlwaysAdmitsAWardStandingItselfDown(env e) {

    setupPoolEscrowValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];

    _PoolEscrow.deny@withrevert(e, e.msg.sender);
    bool reverted = lastReverted;

    assert(wardOfCaller == 1 => !reverted, "a ward stepping itself down never reverts");
}

// PE-RV-14: an admin's withdrawal of at most the free balance never fails.
rule rvPeWithdrawAlwaysAdmitsAWardWithinTheFreeBalance(env e, Escrow.ShareClassId scId, address asset,
    uint256 tokenId, address receiver, uint128 value) {

    setupPoolEscrowValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint wardOfCaller = _PoolEscrow.wards[e.msg.sender];
    mathint totalBefore = ghostPeTotal128;
    mathint reservedBefore = ghostPeReserved128;

    _PoolEscrow.withdraw@withrevert(e, scId, asset, tokenId, receiver, value);
    bool reverted = lastReverted;

    assert((wardOfCaller == 1 && reservedBefore + value <= totalBefore) => !reverted,
        "a ward's withdrawal within the free balance never fails");
}
