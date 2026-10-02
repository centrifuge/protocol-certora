// Gateway. Reverts: authority gates, the pause and each message's refusals.

import "../setup/Gateway_base.spec";
import "../setup/Gateway_batching.spec";

// GW-RV-01: repointing a dependency fails exactly for a non-admin caller or an unknown name, paused or not.
rule rvGwFileRevertsIffGateFails(env e, bytes32 what, address instance) {

    setupGateway(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    bool notWard = _Gateway.wards(e.msg.sender) != 1;
    bool unknownName = what != FILE_MESSAGE_GAS_GW() && what != FILE_PROCESSOR_GW()
        && what != FILE_ADAPTER_GW();

    _Gateway.file@withrevert(e, what, instance);
    bool reverted = lastReverted;

    assert(reverted <=> (notWard || unknownName), "refused exactly for a non-ward or a name the gateway does not know");
}

// GW-RV-02: setting a pool manager fails exactly when the caller is not an admin, paused or not.
rule rvGwUpdateManagerRevertsIffCallerNotWard(env e, Gateway.PoolId p, address who, bool canManage) {

    setupGateway(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    bool notWard = _Gateway.wards(e.msg.sender) != 1;

    _Gateway.updateManager@withrevert(e, p, who, canManage);
    bool reverted = lastReverted;

    assert(reverted <=> notWard, "a manager update goes through exactly when a ward asks");
}

// GW-RV-03: an outbound send fails for a caller who is not an admin, whatever the batching state.
rule rvGwSendRefusedToANonWard(env e, uint16 c, bytes m, bool unpaidMode, address refund) {

    setupGateway(e);

    bool notWard = _Gateway.wards(e.msg.sender) != 1;

    _Gateway.send@withrevert(e, c, m, unpaidMode, refund);
    bool reverted = lastReverted;

    assert(notWard => reverted, "a non-ward never gets a message out");
}

// GW-RV-04: an inbound batch fails unless the caller is an admin or a manager of the batch's pool.
rule rvGwHandleRequiresAWardOrThePoolManager(env e, uint16 c, bytes batch) {

    setupGateway(e);

    _Gateway.handle@withrevert(e, c, batch);
    bool reverted = lastReverted;

    bool outsider = _Gateway.wards(e.msg.sender) != 1 && !_Gateway.manager(ghostGwPoolAsked64, e.msg.sender);

    assert(outsider => reverted, "a caller neither ward nor pool manager cannot deliver a batch");
}

// GW-RV-05: clearing a failed message fails unless the caller is an admin or a manager of its pool.
rule rvGwClearRequiresAWardOrThePoolManager(env e, uint16 c, bytes m) {

    setupGateway(e);

    bool outsider = _Gateway.wards(e.msg.sender) != 1 && !_Gateway.manager(ghostGwPoolId64[keccak256(m)], e.msg.sender);

    _Gateway.clearFailedMessage@withrevert(e, c, m);
    bool reverted = lastReverted;

    assert(outsider => reverted, "a caller neither ward nor pool manager cannot clear a failure");
}

// GW-RV-06: while the protocol is paused, no message is handled, retried, sent or repaid.
rule rvGwPauseHaltsTheFourTrafficEntries(env e, method f, calldataarg args)
    filtered { f -> TRAFFIC_ENTRY_GW(f) } {

    setupGateway(e);
    require(ghostGwPaused, "SCOPE: a paused protocol");

    f@withrevert(e, args);

    assert(lastReverted, "every traffic entry is refused while the protocol is paused");
}

// GW-RV-07: a pause never stops an admin from changing admins, clearing a failure or recovering funds.
rule rvGwAdminEntriesStayLiveUnderPause(env e, address u, uint16 c, bytes m, address token, uint256 tokenId,
    address receiver, uint256 amount) {

    setupGateway(e);
    require(ghostGwPaused, "SCOPE: a paused protocol");
    require(e.msg.value == 0, "SCOPE: no ether, the entries are not payable");
    require(_Gateway.wards(e.msg.sender) == 1, "SCOPE: the caller is a ward");
    require(_Gateway.failedMessages(c, keccak256(m)) > 0, "SCOPE: a failure on record to clear");
    require(amount <= nativeBalances[_Gateway], "SCOPE: the gateway holds the ether to recover");
    require(!_RefundSink.rejectMode(), "SCOPE: an ether receiver that accepts");
    require(nativeBalances[_RefundSink] + amount <= max_uint256, "SAFE: ether balances cannot overflow");
    require(token != ETH_ADDRESS_GW() && tokenId != 0, "SCOPE: a real token and a nonzero token id");
    require(ghostGwToken6909Ok, "SCOPE: an ERC6909 token that accepts the transfer");

    storage init = lastStorage;

    _Gateway.rely@withrevert(e, u) at init;
    bool relyRefused = lastReverted;
    _Gateway.deny@withrevert(e, u) at init;
    bool denyRefused = lastReverted;
    _Gateway.clearFailedMessage@withrevert(e, c, m) at init;
    bool clearRefused = lastReverted;
    _Gateway.recoverTokens@withrevert(e, ETH_ADDRESS_GW(), _RefundSink, amount) at init;
    bool etherRefused = lastReverted;
    _Gateway.recoverTokens@withrevert(e, token, receiver, amount) at init;
    bool tokenRefused = lastReverted;
    _Gateway.recoverTokens@withrevert(e, token, 0, receiver, amount) at init;
    bool tokenIdZeroRefused = lastReverted;
    _Gateway.recoverTokens@withrevert(e, token, tokenId, receiver, amount) at init;
    bool tokenIdRefused = lastReverted;

    assert(!relyRefused && !denyRefused && !clearRefused && !etherRefused && !tokenRefused
        && !tokenIdZeroRefused && !tokenIdRefused,
        "a paused gateway lets a ward add or remove wards, clear and recover");
}

// GW-RV-08: a batch claiming to come from this very network is refused.
rule rvGwHandleRejectsLocallySourcedBatch(env e, uint16 c, bytes batch) {

    setupGateway(e);

    bool claimsLocalOrigin = c == _Gateway.localCentrifugeId();

    _Gateway.handle@withrevert(e, c, batch);
    bool reverted = lastReverted;

    assert(claimsLocalOrigin => reverted, "a batch from the local network id never gets through");
}

// GW-RV-09: a retry reverts when the processor refuses the message, keeping the failure on record.
rule rvGwRetryPropagatesAProcessorRevert(env e, uint16 c, bytes m) {

    setupGateway(e);

    _Gateway.retry@withrevert(e, c, m);
    bool reverted = lastReverted;

    assert(ghostMhHandleReverts => reverted, "a processor refusal inside retry reverts the retry");
}

// GW-RV-10: a message with no failure on record cannot be retried.
rule rvGwRetryRefusedWithoutRecordedFailure(env e, uint16 c, bytes m) {

    setupGateway(e);

    bool noFailure = _Gateway.failedMessages(c, keccak256(m)) == 0;

    _Gateway.retry@withrevert(e, c, m);
    bool reverted = lastReverted;

    assert(noFailure => reverted, "a retry of a never-failed message is refused");
}

// GW-RV-11: a message with no failure on record cannot be cleared, not even by an admin.
rule rvGwClearRefusedWithoutRecordedFailure(env e, uint16 c, bytes m) {

    setupGateway(e);

    bool noFailure = _Gateway.failedMessages(c, keccak256(m)) == 0;

    _Gateway.clearFailedMessage@withrevert(e, c, m);
    bool reverted = lastReverted;

    assert(noFailure => reverted, "clearing a message that never failed is refused to every caller");
}

// GW-RV-12: an empty message or one past the maximum message size cannot be sent.
rule rvGwSendRejectsEmptyOrOversizedMessage(env e, uint16 c, bytes m, bool unpaidMode, address refund) {

    setupGateway(e);

    bool badSize = m.length == 0 || m.length > MESSAGE_MAX_LENGTH_GW();

    _Gateway.send@withrevert(e, c, m, unpaidMode, refund);
    bool reverted = lastReverted;

    assert(badSize => reverted, "an empty or oversized outbound message is refused");
}

// GW-RV-13: outside a batch and outside unpaid mode, a send never succeeds on less than the adapter's quote.
rule rvGwSendRefusesUnderpaymentOutsideUnpaidMode(env e, uint16 c, bytes m, address refund) {

    setupGateway(e);
    require(!GA_IS_BATCHING(), "SCOPE: a send outside a batch");
    require(e.msg.value < max_uint256, "SAFE: no call carries the largest possible value");
    require(ghostAdLastQuote256 == max_uint256, "SAFE: a sentinel quote, reset by every estimate");

    _Gateway.send@withrevert(e, c, m, false, refund);
    bool reverted = lastReverted;

    assert(!reverted => e.msg.value >= ghostAdLastQuote256, "a successful paid send carried at least the quote");
}

// GW-RV-14: a send inside an open batch fails if it carries ether, since the flush pays for the batch.
rule rvGwBatchedSendRefusesValue(env e, uint16 c, bytes m, bool unpaidMode, address refund) {

    setupGateway(e);
    require(GA_IS_BATCHING() && !GA_IS_SENDING_BATCH(), "SCOPE: a send inside an open batch, not yet flushing");
    require(e.msg.value > 0, "SCOPE: the call carries ether");

    _Gateway.send@withrevert(e, c, m, unpaidMode, refund);

    assert(lastReverted, "a batched send with ether attached is refused");
}

// GW-RV-15: while a batch is being sent out, no message joins it and no new batch opens.
rule rvGwNothingJoinsABatchMidFlush(env e, uint16 c, bytes m, bool unpaidMode, address refund, bytes data,
    uint256 callbackValue) {

    setupGateway(e);
    require(GA_IS_SENDING_BATCH(), "SCOPE: a batch being flushed");

    storage init = lastStorage;

    _Gateway.send@withrevert(e, c, m, unpaidMode, refund) at init;
    bool sendRefused = lastReverted;
    _Gateway.withBatch@withrevert(e, data, callbackValue, refund) at init;
    bool envelopeRefused = lastReverted;
    _Gateway.withBatch@withrevert(e, data, refund) at init;
    bool shortEnvelopeRefused = lastReverted;

    assert(sendRefused && envelopeRefused && shortEnvelopeRefused,
        "mid flush every send and every batch envelope is refused");
}

// GW-RV-16: a batch carrying a message bound to another source network is refused whole.
rule rvGwHandleRejectsAMessageFromTheWrongSource(env e, uint16 c, bytes batch) {

    setupGateway(e);
    require(ghostGwInboundCid16 == c, "SAFE: binds the source check to the arriving network");
    require(!ghostGwForeignSourceSeen, "SAFE: the source check starts clear");

    _Gateway.handle@withrevert(e, c, batch);
    bool reverted = lastReverted;

    assert(ghostGwForeignSourceSeen => reverted, "a foreign-source message sinks its whole batch");
}

// GW-RV-17: a batch whose framed message overruns the remaining bytes is refused whole.
rule rvGwHandleRevertsOnAnOverrunningTail(env e, uint16 c, bytes batch) {

    setupGateway(e);
    require(!ghostGwLengthOverran, "SAFE: the framing check starts clear");

    _Gateway.handle@withrevert(e, c, batch);
    bool reverted = lastReverted;

    assert(ghostGwLengthOverran => reverted, "an overrunning length sinks the whole batch");
}

// GW-RV-18: a message whose processing budget is below the failure reserve makes its batch fail.
rule rvGwHandleRevertsWhenTheBudgetIsBelowTheReserve(env e, uint16 c, bytes batch) {

    setupGateway(e);
    require(!ghostGwBudgetBelowReserve, "SAFE: the budget check starts clear");

    _Gateway.handle@withrevert(e, c, batch);
    bool reverted = lastReverted;

    assert(ghostGwBudgetBelowReserve => reverted, "a budget below the reserve sinks the whole batch");
}

// GW-RV-19: a send outside a batch whose gas exceeds the destination's batch cap is refused.
rule rvGwSendRejectsGasAboveTheDestinationCap(env e, uint16 c, bytes m, bool unpaidMode, address refund) {

    setupGateway(e);
    require(!GA_IS_BATCHING(), "SCOPE: a send outside a batch, GW-RV-20 covers batches");

    bool overCap = ghostGwOverallGasOf128[_Gateway.messageGas()][c][keccak256(m)] > ghostGwMaxBatchGas128[c];

    _Gateway.send@withrevert(e, c, m, unpaidMode, refund);
    bool reverted = lastReverted;

    assert(overCap => reverted, "a message costing more gas than its destination accepts is refused");
}

// GW-RV-20: a batched send fails when its gas would push the batch's running total past the destination cap.
rule rvGwBatchCapIsCheckedOnTheRunningSum(env e, uint16 c, bytes m, bool unpaidMode, address refund) {

    setupGateway(e);
    require(GA_IS_BATCHING() && !GA_IS_SENDING_BATCH(), "SCOPE: a send inside an open batch, not yet flushing");

    bytes32 h = keccak256(m);
    mathint runningGas = ghostGwGasSlot256[gwGasSlotKey(c, ghostGwPoolId64[h])] % 2^128;
    mathint gasOfMessage = ghostGwOverallGasOf128[_Gateway.messageGas()][c][h];

    _Gateway.send@withrevert(e, c, m, unpaidMode, refund);
    bool reverted = lastReverted;

    assert(runningGas + gasOfMessage > ghostGwMaxBatchGas128[c] => reverted,
        "a batch may not grow past its destination's gas cap");
}

// GW-RV-21: a clear fails exactly with no failure on record or a caller neither admin nor manager of its pool.
rule rvGwClearRevertsIffOutsiderOrNoRecordedFailure(env e, uint16 c, bytes m) {

    setupGateway(e);
    require(e.msg.value == 0, "SCOPE: no ether, the function is not payable");

    bool outsider = _Gateway.wards(e.msg.sender) != 1 && !_Gateway.manager(ghostGwPoolId64[keccak256(m)], e.msg.sender);
    bool noFailure = _Gateway.failedMessages(c, keccak256(m)) == 0;

    _Gateway.clearFailedMessage@withrevert(e, c, m);
    bool reverted = lastReverted;

    assert(reverted <=> (outsider || noFailure), "a clear fails exactly for an unauthorized caller or no recorded failure");
}

// GW-RV-22: a retry fails exactly when paused, sent ether, not recorded as failed, or the processor refuses it.
rule rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused(env e, uint16 c, bytes m) {

    setupGateway(e);
    require(nativeCodesize[_Gateway.processor()] > 0, "TRUSTED: governance wires a deployed processor");

    bool noFailure = _Gateway.failedMessages(c, keccak256(m)) == 0;
    bool paused = ghostGwPaused;

    _Gateway.retry@withrevert(e, c, m);
    bool reverted = lastReverted;

    assert(reverted <=> (paused || e.msg.value != 0 || noFailure || ghostMhHandleReverts),
        "a retry fails exactly on pause, ether, no recorded failure or processor refusal");
}
