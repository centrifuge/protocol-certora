import "setup/Spoke_solo.spec";

// --- variable_transitions ---

// SP-VT-01: the spoke never announces a cross-chain share transfer of nothing.
rule vtSpBridgeNeverAnnouncesAnEmptyTransfer(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    mathint announcedBefore = ghostMsInitiateTransferCount;

    f(e, args);

    mathint announcedAfter = ghostMsInitiateTransferCount;
    mathint announcedAmount = ghostMsInitiateTransferAmount128;

    assert(announcedAfter != announcedBefore => announcedAmount != 0,
        "no bridge transfer is ever announced for zero shares");
}

// SP-VT-02: a cross-chain share transfer is never announced back to this same network.
rule vtSpBridgeNeverAnnouncesBackToThisNetwork(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    mathint sentBefore = ghostMsSendCount;

    f(e, args);

    mathint sentAfter = ghostMsSendCount;
    mathint announcedKind = ghostMsLastKind;
    mathint announcedChain = ghostMsLastCid16;
    mathint localChain = ghostMsLocalCentrifugeId16;

    assert(sentAfter != sentBefore && announcedKind == MS_INITIATE_TRANSFER_SHARES()
        => announcedChain != localChain,
        "an announced share transfer always names another network");
}

// SP-VT-03: an asset registration message never has an empty asset id.
rule vtSpAssetRegistrationNeverAnnouncesTheNullId(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    mathint sentBefore = ghostMsSendCount;

    f(e, args);

    mathint sentAfter = ghostMsSendCount;
    mathint announcedKind = ghostMsLastKind;
    mathint announcedAssetId = ghostMsLastAssetId128;

    assert(sentAfter != sentBefore && announcedKind == MS_REGISTER_ASSET()
        => announcedAssetId != 0,
        "no asset registration announces the null asset id");
}

// SP-VT-04: an asset registration message never states more than the maximum decimals.
rule vtSpAssetRegistrationRespectsTheDecimalsCeiling(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    mathint registeredBefore = ghostMsRegisterAssetCount;

    f(e, args);

    mathint registeredAfter = ghostMsRegisterAssetCount;
    mathint announcedDecimals = ghostMsRegisterAssetDecimals8;

    assert(registeredAfter != registeredBefore => announcedDecimals <= MAX_DECIMALS_CVL(),
        "no asset registration announces more than 18 decimals");
}

// SP-VT-05: one call on the spoke sends at most one outbound message.
rule vtSpOneCallHandsOverAtMostOneMessage(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    mathint sentBefore = ghostMsSendCount;

    f(e, args);

    mathint sentAfter = ghostMsSendCount;

    assert(sentAfter <= sentBefore + 1, "a single call never sends two messages");
}

// SP-VT-06: every outbound message forwards the ETH its caller attached, and none from inside a batch.
rule vtSpEveryOutboundSendCarriesTheAttachedValue(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSoloAnyTransient(e);

    bool inBatch = spInBatchCVL(e);
    mathint sentBefore = ghostMsSendCount;

    f(e, args);

    mathint sentAfter = ghostMsSendCount;
    mathint forwardedValue = ghostMsLastValue256;

    assert(sentAfter != sentBefore => forwardedValue == (inBatch ? 0 : e.msg.value),
        "a sent message carries exactly the caller's ETH, or none when batched");
}

// --- state_transitions ---

// SP-ST-01: each queued asset change is matched by the same change in the escrow's spendable balance.
rule stSpQueuedMoveIsBackedByTheEscrow(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {
    setupSpokeValidState(e);
    mathint movesBefore = ghostPeFaceMoveCount;
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    f(e, args);

    assert(ghostSqFaceQueueAssetsCount == queuedBefore + 1
        => ghostPeFaceMoveCount == movesBefore + 1
            && ghostPeFaceLastMove128 == ghostSqFaceLastAmount128
            && ghostPeFaceLastMoveIsIncrease == ghostSqFaceLastIsIncrease,
        "one queued asset change brings one escrow move of equal size and sign");
}
