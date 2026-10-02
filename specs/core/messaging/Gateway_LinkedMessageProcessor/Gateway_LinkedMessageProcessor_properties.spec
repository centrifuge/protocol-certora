import "setup/Gateway_LinkedMessageProcessor_base.spec";
import "setup/Gateway_LinkedMessageProcessor_witness.spec";

// --- reachability ---

// GW-RC-11: a pool manager that is not an admin can deliver a hub message for its pool to processing.
rule rcGwPoolManagerInjectsAHubOriginatedMessage(env e, uint16 c, bytes m) {

    setupEnv(e);
    require(POOL_HOMED_TYPE_GW(_BytesSlice.toUint8Pure(m, 0)), "SCOPE: a hub-to-spoke message type");
    require(_Gateway.wards(e.msg.sender) != 1, "SCOPE: the caller is not a ward");

    mathint forwardedBefore = ghostGwForwardCount;

    _Gateway.handle(e, c, m);

    satisfy(ghostGwForwardCount == forwardedBefore + 1 && ghostGwLastForwardCid16 == c,
        "a non-ward pool manager gets one hub message forwarded");
}

// GW-RC-12: a batch can fail on an unknown second message after its first went to processing.
rule rcGwUnknownTailRevertsTheBatchAfterItsFirstMessageWasForwarded(env e, uint16 c, bytes batch) {

    setupEnv(e);
    require(_BytesSlice.toUint8Pure(batch, 0) == 1, "SCOPE: a schedule-upgrade message opens the batch");
    require(c == MAINNET_CENTRIFUGE_ID_GW(), "SCOPE: sent from mainnet");
    uint16 firstLength = _MessageProcessor.messageLength(batch);
    require(batch.length == firstLength + 1, "SCOPE: the second message is one byte long");
    require(UNKNOWN_TYPE_GW(_BytesSlice.toUint8Pure(batch, firstLength)),
        "SCOPE: the second message has an unknown type");

    mathint forwardedBefore = ghostGwForwardCount;

    _Gateway.handle@withrevert(e, c, batch);
    bool reverted = lastReverted;

    satisfy(reverted && ghostGwForwardCount == forwardedBefore + 1,
        "the batch reverts after its first message was forwarded");
}
