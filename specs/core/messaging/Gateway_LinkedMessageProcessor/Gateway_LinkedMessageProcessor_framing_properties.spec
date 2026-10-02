import "setup/Gateway_LinkedMessageProcessor_base.spec";
import "setup/Gateway_LinkedMessageProcessor_framing.spec";

// The message at start has an unknown type; false past the batch end.
function gwUnknownTypeAtCVL(bytes batch, uint256 start) returns bool {
    if (start >= batch.length) {
        return false;
    }
    return UNKNOWN_TYPE_GW(_BytesSlice.toUint8Pure(batch, start));
}

// --- reverts ---

// GW-RV-23: a batch fails when one of its first three messages has an unknown message type.
rule rvGwHandleRevertsOnAnUnknownTypeByte(env e, uint16 c, bytes batch) {

    setupEnv(e);

    _Gateway.handle@withrevert(e, c, batch);
    bool reverted = lastReverted;

    assert(gwUnknownTypeAtCVL(batch, 0) => reverted, "an unknown first message makes the whole batch revert");
    uint16 firstLength = _MessageProcessor.messageLength@withrevert(batch);
    bool firstFramed = !lastReverted;
    assert(firstFramed && gwUnknownTypeAtCVL(batch, firstLength) => reverted,
        "an unknown second message makes the whole batch revert");
    bool secondFramed = false;
    uint256 thirdStart = 0;
    if (firstFramed && firstLength < batch.length) {
        bytes tail = _BytesSlice.slicePure(batch, firstLength, assert_uint256(batch.length - firstLength));
        uint16 secondLength = _MessageProcessor.messageLength@withrevert(tail);
        secondFramed = !lastReverted;
        if (secondFramed) {
            thirdStart = assert_uint256(firstLength + secondLength);
        }
    }
    assert(secondFramed && gwUnknownTypeAtCVL(batch, thirdStart) => reverted,
        "an unknown third message makes the whole batch revert");
}
