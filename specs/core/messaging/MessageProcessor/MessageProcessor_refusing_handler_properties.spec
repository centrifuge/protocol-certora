import "setup/MessageProcessor_base.spec";

// --- reverts ---

// MP-RV-09: a request the hub handler refuses makes the whole message fail.
// SCOPE: the hub handler is a compiled stub refusing every request.
rule rvMpRefusedRequestPropagatesToTheGateway(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(_BytesSlice.toUint8Pure(message, 0) == MT_REQUEST(), "SCOPE: a request");
    require(_MessageProcessor.wards(e.msg.sender) == 1, "SCOPE: the caller is a ward");

    _MessageProcessor.handle@withrevert(e, cid, message);
    bool reverted = lastReverted;

    assert(reverted, "the processor never swallows a request refusal");
}
