import "../setup/MessageProcessor_base.spec";

// MP-RC-01: an adapter set update can complete on the adapter router.
rule rcMpPoolAdaptersUpdateReachesTheAdapterRouter(env e, uint16 cid, bytes message) {

    setupMessageProcessor(e);
    require(_BytesSlice.toUint8Pure(message, 0) == MT_SET_POOL_ADAPTERS(), "SCOPE: an adapter set update");
    require(_MessageProcessor.multiAdapter() == _MultiAdapterStub, "SCOPE: the adapter router is the stand-in");

    mathint adapterBefore = ghostMaSetAdaptersCount;

    _MessageProcessor.handle(e, cid, message);

    satisfy(ghostMaSetAdaptersCount == adapterBefore + 1 && ghostMaLastSetAdaptersCid16 == cid,
        "the router records the update under its source network");
}
