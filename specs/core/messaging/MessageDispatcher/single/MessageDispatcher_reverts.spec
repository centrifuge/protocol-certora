// MessageDispatcher. Reverts: what a rewiring and a local adapter set update must refuse.

import "../setup/MessageDispatcher_single.spec";

// MD-RV-01: reconfiguring the dispatcher fails for a non-admin caller or an unknown setting name.
rule rvMdFileRefusesANonWardOrAnUnknownName(env e, bytes32 what, address data) {

    setupMessageDispatcher(e);

    mathint senderWardBefore = _MessageDispatcher.wards(e.msg.sender);
    bool unknownParam = what != FILE_ENVOY_MD_CVL() && what != FILE_GATEWAY_MD_CVL()
        && what != FILE_MULTI_ADAPTER_MD_CVL() && what != FILE_SPOKE_HANDLER_MD_CVL()
        && what != FILE_HUB_HANDLER_MD_CVL();

    _MessageDispatcher.file@withrevert(e, what, data);
    bool reverted = lastReverted;

    assert((senderWardBefore != 1 || unknownParam) => reverted, "rewiring fails for a non-ward or an unknown name");
}

// MD-RV-02: a pool adapter update addressed to this network fails instead of being dropped.
rule rvMdSetPoolAdaptersRefusesTheLocalNetwork(env e, uint16 cid, MessageDispatcher.PoolId poolId,
    bytes32[] adapters, uint8 threshold, uint16 targetSessionId, address refund) {

    setupMessageDispatcher(e);

    bool local = cid == _MessageDispatcher.localCentrifugeId();

    _MessageDispatcher.sendSetPoolAdapters@withrevert(e, cid, poolId, adapters, threshold, targetSessionId, refund);
    bool reverted = lastReverted;

    assert(local => reverted, "announcing an adapter set to this network is refused");
}
