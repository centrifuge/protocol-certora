import "setup/Spoke_solo.spec";

// SP-HL-01: a bridge transfer takes the shares from the owner the caller named.
rule hlSpBridgeDebitsTheNamedOwner(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint ownerBefore = ghostERC20Balances128[share][owner];

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint ownerAfter = ghostERC20Balances128[share][owner];

    assert(ownerAfter == ownerBefore - amount, "a bridge transfer debits the owner by exactly the amount");
}

// SP-HL-02: the shares a bridge transfer takes are destroyed on this network.
rule hlSpBridgeBurnsTheBridgedShares(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint supplyBefore = ghostERC20TotalSupply256[share];

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint supplyAfter = ghostERC20TotalSupply256[share];

    assert(supplyAfter == supplyBefore - amount, "a bridge transfer burns exactly the amount from supply");
}

// SP-HL-03: a bridge transfer leaves no shares behind on the spoke.
rule hlSpBridgeParksNoSharesOnTheSpoke(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);
    require(owner != _Spoke, "TRUSTED: the hub never grants the spoke bridger rights");

    address share = ghostSrShareToken;
    mathint spokeBefore = ghostERC20Balances128[share][_Spoke];

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint spokeAfter = ghostERC20Balances128[share][_Spoke];

    assert(spokeAfter == spokeBefore, "a bridge transfer leaves the spoke's share balance unchanged");
}

// SP-HL-04: a bridge transfer sends exactly one outgoing transfer message.
rule hlSpBridgeAnnouncesExactlyOneTransfer(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    mathint bridgedBefore = ghostMsInitiateTransferCount;

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint bridgedAfter = ghostMsInitiateTransferCount;

    assert(bridgedAfter == bridgedBefore + 1, "bridging bumps the outgoing transfer count by one");
}

// SP-HL-05: a bridge transfer message carries the amount of shares burned.
rule hlSpBridgeAnnouncesTheBurnedAmount(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint announcedAmount = ghostMsInitiateTransferAmount128;

    assert(announcedAmount == amount, "the transfer message carries the bridged amount");
}

// SP-HL-06: a bridge transfer message carries the receiver the caller named.
rule hlSpBridgeAnnouncesTheNamedReceiver(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    bytes32 announcedReceiver = ghostMsInitiateTransferReceiver;

    assert(announcedReceiver == receiver, "the transfer message carries the named receiver");
}

// SP-HL-07: a bridge transfer deducts the amount bridged from the owner's finite approval to the spoke.
rule hlSpBridgeSpendsTheOwnersApproval(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);
    require(owner != _Spoke, "TRUSTED: the hub never grants the spoke bridger rights");

    address share = ghostSrShareToken;
    mathint approvedBefore = ghostERC20Allowances256[share][owner][_Spoke];

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint approvedAfter = ghostERC20Allowances256[share][owner][_Spoke];

    assert(approvedBefore != max_uint256 => approvedAfter == approvedBefore - amount,
        "a bridge cuts the owner's finite spoke approval by the amount");
}

// SP-HL-08: a bridge transfer queues no share change for the hub.
rule hlSpBridgeReportsNoShareMovementToTheHub(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    mathint reportedBefore = ghostSqFaceQueueSharesCount;

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint reportedAfter = ghostSqFaceQueueSharesCount;

    assert(reportedAfter == reportedBefore, "bridging leaves the hub's share queue alone");
}

// SP-HL-09: recording a deposit that already reached the escrow transfers no tokens.
rule hlSpNoteDepositMovesNoTokens(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address asset, uint256 tokenId, uint128 amount, address token, address holder, uint256 unitId) {

    setupSpokeValidState(e);

    mathint balanceBefore = ghostERC20Balances128[token][holder];
    mathint unitsBefore = ghostERC6909Balances128[token][unitId][holder];

    _Spoke.noteDeposit(e, poolId, scId, asset, tokenId, amount);

    mathint balanceAfter = ghostERC20Balances128[token][holder];
    mathint unitsAfter = ghostERC6909Balances128[token][unitId][holder];

    assert(balanceAfter == balanceBefore && unitsAfter == unitsBefore,
        "noting a deposit moves no token balance on either ledger");
}

// SP-HL-10: a revocation spends the caller's approval to the spoke.
rule hlSpRevokeSpendsTheCallersApproval(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    uint128 shares) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint approvedBefore = ghostERC20Allowances256[share][e.msg.sender][_Spoke];

    _Spoke.revoke(e, poolId, scId, shares);

    mathint approvedAfter = ghostERC20Allowances256[share][e.msg.sender][_Spoke];

    assert(approvedBefore != max_uint256 => approvedAfter == approvedBefore - shares,
        "a revoke cuts the caller's finite spoke approval by the amount");
}

// SP-HL-11: a forced share transfer spends the holder's approval to the named sender.
rule hlSpTransferSharesFromSpendsTheNamedSendersApproval(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address sender_, address from, address to, uint256 amount) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint approvedBefore = ghostERC20Allowances256[share][from][sender_];

    _Spoke.transferSharesFrom(e, poolId, scId, sender_, from, to, amount);

    mathint approvedAfter = ghostERC20Allowances256[share][from][sender_];

    assert(sender_ != from && approvedBefore != max_uint256 => approvedAfter == approvedBefore - amount,
        "forced transfers cut a finite approval to another sender by the amount");
}

// SP-HL-12: a deposit is paid from the caller's own balance.
rule hlSpDepositDebitsTheCaller(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address asset, uint256 tokenId, uint128 amount) {

    setupSpokeValidState(e);
    require(e.msg.sender != ghostEfEscrow(poolId), "SCOPE: the depositor is not the pool escrow itself");

    mathint paidBefore = tokenId == 0 ? ghostERC20Balances128[asset][e.msg.sender]
        : ghostERC6909Balances128[asset][tokenId][e.msg.sender];

    _Spoke.deposit(e, poolId, scId, asset, tokenId, amount);

    mathint paidAfter = tokenId == 0 ? ghostERC20Balances128[asset][e.msg.sender]
        : ghostERC6909Balances128[asset][tokenId][e.msg.sender];

    assert(paidAfter == paidBefore - amount, "a deposit debits the caller by exactly the amount");
}

// SP-HL-13: registering an asset announces it to the network the caller named.
rule hlSpRegisterAssetAnnouncesToTheNamedNetwork(env e, uint16 centrifugeId, address asset, uint256 tokenId,
    address refund) {

    setupSpokeValidState(e);

    _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);

    mathint announcedTo = ghostMsLastCid16;

    assert(announcedTo == centrifugeId, "an asset registration is announced to the named network");
}

// SP-HL-14: changing the spoke's gateway or message sender leaves the other unchanged.
rule hlSpFileRepointsOnlyTheNamedRoute(env e, bytes32 what, address data) {

    setupSpokeValidState(e);

    address gatewayBefore = _Spoke.gateway;
    address senderBefore = _Spoke.sender;

    _Spoke.file(e, what, data);

    assert((_Spoke.gateway != gatewayBefore => what == FILE_GATEWAY_SP_CVL())
        && (_Spoke.sender != senderBefore => what == FILE_SENDER_SP_CVL()),
        "a rewiring moves only the route it names");
}

// SP-HL-15: issued shares are minted to the recipient the caller named.
rule hlSpIssueMintsToTheRecipientNamed(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address to, uint128 shares) {

    setupSpokeValidState(e);

    address share = ghostSrShareToken;
    mathint recipientBefore = ghostERC20Balances128[share][to];

    _Spoke.issue(e, poolId, scId, to, shares);

    mathint recipientAfter = ghostERC20Balances128[share][to];

    assert(recipientAfter == recipientBefore + shares, "an issue credits the named recipient by exactly the shares");
}

// SP-HL-16: a withdrawal pays the receiver the caller named.
rule hlSpWithdrawalPaysTheReceiverNamed(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address asset, uint256 tokenId, address receiver, uint128 amount) {

    setupSpokeValidState(e);
    require(receiver != ghostEfEscrow(poolId), "SCOPE: the receiver is not the escrow itself");

    mathint paidBefore = tokenId == 0 ? ghostERC20Balances128[asset][receiver]
        : ghostERC6909Balances128[asset][tokenId][receiver];

    _Spoke.withdraw(e, poolId, scId, asset, tokenId, receiver, amount);

    mathint paidAfter = tokenId == 0 ? ghostERC20Balances128[asset][receiver]
        : ghostERC6909Balances128[asset][tokenId][receiver];

    assert(paidAfter == paidBefore + amount, "a withdrawal credits the named receiver by exactly the amount");
}

// SP-HL-17: a withdrawal of reserved funds pays the receiver the caller named.
rule hlSpReservedWithdrawalPaysTheReceiverNamed(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount,
    address reserver, bytes32 reason) {

    setupSpokeValidState(e);
    require(receiver != ghostEfEscrow(poolId), "SCOPE: the receiver is not the escrow itself");

    mathint paidBefore = tokenId == 0 ? ghostERC20Balances128[asset][receiver]
        : ghostERC6909Balances128[asset][tokenId][receiver];

    _Spoke.withdrawReserved(e, poolId, scId, asset, tokenId, receiver, amount, reserver, reason);

    mathint paidAfter = tokenId == 0 ? ghostERC20Balances128[asset][receiver]
        : ghostERC6909Balances128[asset][tokenId][receiver];

    assert(paidAfter == paidBefore + amount, "a reserved withdrawal credits the named receiver by exactly the amount");
}

// SP-HL-18: a share payout from the escrow reaches the receiver the caller named.
rule hlSpSharePayoutReachesTheReceiverNamed(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    address receiver, uint128 amount) {

    setupSpokeValidState(e);
    require(receiver != ghostEfEscrow(poolId), "SCOPE: the receiver is not the escrow itself");

    address share = ghostSrShareToken;
    mathint receiverBefore = ghostERC20Balances128[share][receiver];

    _Spoke.withdrawShares(e, poolId, scId, receiver, amount);

    mathint receiverAfter = ghostERC20Balances128[share][receiver];

    assert(receiverAfter == receiverBefore + amount, "a share payout credits the named receiver by exactly the amount");
}

// SP-HL-19: a manager call tells the hub who made it and forwards the caller's ETH, none inside a batch.
rule hlSpManagerCallNamesItsCallerOnTheWire(env e, SpokeHarness.PoolId poolId, bytes32 target, bytes payload,
    uint128 extraGasLimit, address refund) {

    setupSpokeSoloAnyTransient(e);

    bool inBatch = spInBatchCVL(e);
    address caller = spResolvedSenderCVL(e);

    _Spoke.managerCall(e, poolId, target, payload, extraGasLimit, refund);

    bytes32 namedCaller = ghostMsLastSenderWord;
    mathint forwardedValue = ghostMsLastValue256;

    assert(namedCaller == to_bytes32(caller) << 96 && forwardedValue == (inBatch ? 0 : e.msg.value),
        "the hub learns the caller and gets exactly its ETH, none if batched");
}

// SP-HL-20: a bridge transfer message carries the sender the caller named.
rule hlSpBridgeAnnouncesTheNamedSender(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    bytes32 announcedSender = ghostMsLastSenderWord;

    assert(announcedSender == to_bytes32(sender_) << 96, "the announced sender is the one passed in by the caller");
}

// SP-HL-21: the short-form bridge transfer reports its caller as the sender.
rule hlSpShortBridgeAnnouncesTheCallerAsSender(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, uint128 amount, uint128 remoteExtraGasLimit) {

    setupSpokeValidState(e);

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, amount, remoteExtraGasLimit);

    bytes32 announcedSender = ghostMsLastSenderWord;

    assert(announcedSender == to_bytes32(e.msg.sender) << 96, "the short bridge call names whoever calls it as sender");
}

// SP-HL-22: a request reaches the hub paid or unpaid, as the request manager asked.
rule hlSpRequestRelaysThePaymentModeItWasHanded(env e, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, SpokeHarness.AssetId assetId, bytes payload, uint128 extraGasLimit,
    bool unpaid, address refund) {

    setupSpokeValidState(e);

    _Spoke.request(e, poolId, scId, assetId, payload, extraGasLimit, unpaid, refund);

    bool relayedUnpaid = ghostMsRequestUnpaid;

    assert(relayedUnpaid == unpaid, "a request is relayed in the payment mode it was given");
}

// SP-HL-23: a revocation leaves the spoke with no open approval to the share registrar.
rule hlSpRevokeLeavesNoApprovalToTheRegistrar(env e, SpokeHarness.PoolId poolId, SpokeHarness.ShareClassId scId,
    uint128 shares) {

    setupSpokeValidState(e);
    require(ghostSrRegistrar != _Spoke, "TRUSTED: the hub never names the spoke as registrar");

    _Spoke.revoke(e, poolId, scId, shares);

    mathint leftApproved = ghostERC20Allowances256[ghostSrShareToken][_Spoke][ghostSrRegistrar];

    assert(leftApproved == 0, "a revoke leaves the registrar no approval over spoke shares");
}

// SP-HL-24: a bridge transfer leaves the spoke with no open approval to the share registrar.
rule hlSpBridgeLeavesNoApprovalToTheRegistrar(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);
    require(ghostSrRegistrar != _Spoke, "TRUSTED: the hub never names the spoke as registrar");

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint leftApproved = ghostERC20Allowances256[ghostSrShareToken][_Spoke][ghostSrRegistrar];

    assert(leftApproved == 0, "a bridge transfer leaves the registrar no approval over spoke shares");
}

// SP-HL-25: setting the spoke's gateway or message sender stores exactly the address given.
rule hlSpFileWritesTheValueIntoTheNamedRoute(env e, bytes32 what, address data) {

    setupSpokeValidState(e);

    _Spoke.file(e, what, data);

    address gatewayAfter = _Spoke.gateway;
    address messageSenderAfter = _Spoke.sender;

    assert((what == FILE_GATEWAY_SP_CVL() => gatewayAfter == data)
        && (what == FILE_SENDER_SP_CVL() => messageSenderAfter == data),
        "the named setting now holds the new address");
}

// SP-HL-26: a deposit or payout for one pool leaves another pool's escrow untouched unless paying out to it.
rule hlSpEscrowResolvedEntryNeverMovesAnotherPoolsEscrowTokens(env e, uint8 op, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 amount,
    address reserver, bytes32 reason, uint64 poolB, address token, uint256 id) {

    setupSpokeValidState(e);
    require(poolB != poolId, "SCOPE: the escrow watched belongs to another pool");

    address otherEscrow = ghostEfEscrow(poolB);
    require(e.msg.sender != otherEscrow, "SAFE: an escrow never calls the spoke");

    mathint erc20Before = ghostERC20Balances128[token][otherEscrow];
    mathint erc6909Before = ghostERC6909Balances128[token][id][otherEscrow];

    if (op == 0) {
        _Spoke.deposit(e, poolId, scId, asset, tokenId, amount);
    } else if (op == 1) {
        _Spoke.withdraw(e, poolId, scId, asset, tokenId, receiver, amount);
    } else if (op == 2) {
        _Spoke.withdrawReserved(e, poolId, scId, asset, tokenId, receiver, amount, reserver, reason);
    } else {
        _Spoke.withdrawShares(e, poolId, scId, receiver, amount);
    }

    mathint erc20After = ghostERC20Balances128[token][otherEscrow];
    mathint erc6909After = ghostERC6909Balances128[token][id][otherEscrow];
    bool paysTheWatchedEscrow = op != 0 && receiver == otherEscrow;

    assert((erc20After == erc20Before && erc6909After == erc6909Before)
        || (paysTheWatchedEscrow && erc20After >= erc20Before && erc6909After >= erc6909Before),
        "another pool's escrow is untouched unless paid, and then only gains");
}

// SP-HL-27: a bridge transfer burns the shares before it announces the transfer to the destination.
rule hlSpBridgeBurnsBeforeItAnnounces(env e, uint16 centrifugeId, SpokeHarness.PoolId poolId,
    SpokeHarness.ShareClassId scId, bytes32 receiver, address sender_, address owner, uint128 amount,
    uint128 extraGasLimit, uint128 remoteExtraGasLimit, address refund) {

    setupSpokeValidState(e);

    mathint clockBefore = ghostCallClock;

    _Spoke.crosschainTransferShares(e, centrifugeId, poolId, scId, receiver, sender_, owner, amount,
        extraGasLimit, remoteExtraGasLimit, refund);

    mathint burnedAt = ghostRegistrarLastBurnAt;
    mathint announcedAt = ghostMsInitiateTransferAt;

    assert(burnedAt >= clockBefore && burnedAt < announcedAt,
        "the burn happens in this call, ahead of the announcement");
}

// SP-HL-28: a token rescue moves only the spoke's and the receiver's balances, no spoke field under any key.
// UNSAFE: a rescued token or receiver is taken not to re-enter; recoverTokens holds no lock (Recoverable.sol:15,24).
rule hlSpRecoverTokensMovesOnlyTheRescuedBalances(env e, bool withId, address token, uint256 tokenId,
    address receiver, uint256 amount, address who, address t, uint256 id, address acct, address spender) {

    setupSpokeSolo(e);

    uint256 wardBefore = _Spoke.wards[who];
    address gatewayBefore = _Spoke.gateway;
    address senderBefore = _Spoke.sender;
    uint128 notedBefore = _Spoke.notedWithoutTransfer;
    address batchSenderBefore = ghostSpSenderT;
    address initiatorBefore = ghostSpInitiatorT;
    mathint balance20Before = ghostERC20Balances128[t][acct];
    mathint allowance20Before = ghostERC20Allowances256[t][acct][spender];
    mathint supplyBefore = ghostERC20TotalSupply256[t];
    mathint balance6909Before = ghostERC6909Balances128[t][id][acct];
    mathint allowance6909Before = ghostERC6909Allowances256[t][acct][spender][id];

    if (withId) {
        _Spoke.recoverTokens(e, token, tokenId, receiver, amount);
    } else {
        _Spoke.recoverTokens(e, token, receiver, amount);
    }

    assert(_Spoke.wards[who] == wardBefore && _Spoke.gateway == gatewayBefore && _Spoke.sender == senderBefore
            && _Spoke.notedWithoutTransfer == notedBefore
            && ghostSpSenderT == batchSenderBefore && ghostSpInitiatorT == initiatorBefore,
        "no spoke field, persistent or transient, moves");
    assert(ghostERC20Allowances256[t][acct][spender] == allowance20Before && ghostERC20TotalSupply256[t] == supplyBefore
            && ghostERC6909Allowances256[t][acct][spender][id] == allowance6909Before,
        "no allowance or supply moves");
    assert((acct != _Spoke && acct != receiver) => (ghostERC20Balances128[t][acct] == balance20Before
            && ghostERC6909Balances128[t][id][acct] == balance6909Before),
        "only the spoke's and the receiver's balances move");
}
