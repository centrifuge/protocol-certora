import "../setup/MessageProcessor_base.spec";

// MP-RV-01: a message whose type code names no message type is refused.
rule rvMpUnknownKindIsRefused(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);

    mathint k = _BytesSlice.toUint8Pure(message, 0);

    _MessageProcessor.handle@withrevert(e, cid, message);
    bool reverted = lastReverted;

    assert((k == 0 || k > MT_UNAUTHORIZE_SPOKE_CALL()) => reverted,
        "type code 0 and every code past the last type always revert");
}

// MP-RV-02: a manager update naming no manager kind is refused.
rule rvMpOutOfRangeManagerKindIsRefused(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(_BytesSlice.toUint8Pure(message, 0) == MT_UPDATE_MANAGER(), "SCOPE: a manager update");

    mathint managerKind = _BytesSlice.toUint8Pure(message, 9);

    _MessageProcessor.handle@withrevert(e, cid, message);
    bool reverted = lastReverted;

    assert(managerKind > 3 => reverted, "a manager update of a kind past Bridger is refused");
}

// MP-RV-03: a vault update naming no vault update kind is refused.
rule rvMpOutOfRangeVaultKindIsRefused(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(_BytesSlice.toUint8Pure(message, 0) == MT_UPDATE_VAULT(), "SCOPE: a vault update");

    mathint updateKind = _BytesSlice.toUint8Pure(message, 73);

    _MessageProcessor.handle@withrevert(e, cid, message);
    bool reverted = lastReverted;

    assert(updateKind > 2 => reverted, "a vault update of a kind past Unlink is refused");
}

// MP-RV-04: a message from a non-admin is refused.
rule rvMpHandleRefusesANonWard(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);

    bool isWard = _MessageProcessor.wards(e.msg.sender) == 1;

    _MessageProcessor.handle@withrevert(e, cid, message);
    bool reverted = lastReverted;

    assert(!isWard => reverted, "a non-ward caller never gets a message processed");
}

// MP-RV-05: an empty message is refused.
rule rvMpEmptyMessageIsRefused(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);

    bool empty = message.length == 0;

    _MessageProcessor.handle@withrevert(e, cid, message);
    bool reverted = lastReverted;

    assert(empty => reverted, "a zero-length message never goes through");
}

// MP-RV-06: a well formed hub message from an admin goes through whenever the hub handler accepts it.
rule rvMpWellFormedHubKindIsNeverRefused(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    assumeMpNeighboursAnswer();
    require(_MessageProcessor.wards(e.msg.sender) == 1, "SCOPE: the caller is a ward");
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    require(!ghostHhRequestRefuses, "SCOPE: the hub handler accepts a request");
    require(wellFormedMp(message), "SCOPE: a message its decoder accepts");
    require(HUB_KIND_MP(_BytesSlice.toUint8Pure(message, 0)), "SCOPE: a message bound for the hub");

    _MessageProcessor.handle@withrevert(e, cid, message);
    bool reverted = lastReverted;

    assert(!reverted, "a ward's valid hub message never reverts");
}

// MP-RV-07: a well formed spoke message from an admin always goes through.
rule rvMpWellFormedSpokeKindIsNeverRefused(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    assumeMpNeighboursAnswer();
    require(_MessageProcessor.wards(e.msg.sender) == 1, "SCOPE: the caller is a ward");
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    require(wellFormedMp(message), "SCOPE: a message its decoder accepts");
    require(SPOKE_KIND_MP(_BytesSlice.toUint8Pure(message, 0)), "SCOPE: a message bound for the spoke");

    _MessageProcessor.handle@withrevert(e, cid, message);
    bool reverted = lastReverted;

    assert(!reverted, "a ward's valid spoke message never reverts");
}

// MP-RV-08: a well formed upgrade schedule or cancellation from an admin always goes through.
rule rvMpWellFormedRootKindIsNeverRefused(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    assumeMpNeighboursAnswer();
    require(_MessageProcessor.wards(e.msg.sender) == 1, "SCOPE: the caller is a ward");
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    require(wellFormedMp(message), "SCOPE: a message its decoder accepts");
    require(ROOT_KIND_MP(_BytesSlice.toUint8Pure(message, 0)), "SCOPE: an upgrade schedule or cancellation");

    _MessageProcessor.handle@withrevert(e, cid, message);
    bool reverted = lastReverted;

    assert(!reverted, "a ward's valid upgrade message never reverts");
}

// MP-RV-10: computing the length of a message fails when it is empty or its type is unknown.
rule rvMpMessageLengthRefusesAnUnknownKind(bytes message) {
    mathint k = 0;
    if (message.length > 0) {
        k = _BytesSlice.toUint8Pure(message, 0);
    }

    _MessageProcessor.messageLength@withrevert(message);
    bool reverted = lastReverted;

    assert((k == 0 || k > MT_UNAUTHORIZE_SPOKE_CALL()) => reverted, "an empty or unknown message has no length");
}
