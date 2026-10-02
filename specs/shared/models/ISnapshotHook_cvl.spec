// Snapshot hook model: sync and transfer notifications recorded, a sync refused on one free bit.

methods {
    // UNSAFE: one refusal bit shared by every hook, whatever the notified network.
    function _.onSync(uint64 poolId, bytes16 scId, uint16 centrifugeId) external
        => snapshotHookOnSyncCVL(poolId, scId, centrifugeId) expect void;

    // UNSAFE: drops the hook's refusals on the transfer notification.
    function _.onTransfer(uint64 poolId, bytes16 scId, uint16 fromCentrifugeId, uint16 toCentrifugeId, uint128 sharesTransferred) external
        => snapshotHookOnTransferCVL(poolId, scId, fromCentrifugeId, toCentrifugeId, sharesTransferred) expect void;
}

persistent ghost bool ghostSnapshotHookRefuses;

persistent ghost mathint ghostHookOnSyncCount {
    init_state axiom ghostHookOnSyncCount == 0;
    axiom ghostHookOnSyncCount >= 0;
}
persistent ghost uint64 ghostHookOnSyncPool64;
persistent ghost bytes16 ghostHookOnSyncScId;
persistent ghost uint16 ghostHookOnSyncCid16;

function snapshotHookOnSyncCVL(uint64 poolId, bytes16 scId, uint16 centrifugeId) {
    if (ghostSnapshotHookRefuses) {
        revert("SnapshotHookRefuses");
    }
    ghostHookOnSyncCount = ghostHookOnSyncCount + 1;
    ghostHookOnSyncPool64 = poolId;
    ghostHookOnSyncScId = scId;
    ghostHookOnSyncCid16 = centrifugeId;
}

persistent ghost mathint ghostHookOnTransferCount {
    init_state axiom ghostHookOnTransferCount == 0;
    axiom ghostHookOnTransferCount >= 0;
}
persistent ghost uint64 ghostHookOnTransferPool64;
persistent ghost bytes16 ghostHookOnTransferScId;
persistent ghost uint16 ghostHookOnTransferFromCid16;
persistent ghost uint16 ghostHookOnTransferToCid16;
persistent ghost uint128 ghostHookOnTransferShares128;

function snapshotHookOnTransferCVL(uint64 poolId, bytes16 scId, uint16 fromCentrifugeId, uint16 toCentrifugeId, uint128 sharesTransferred) {
    ghostHookOnTransferCount = ghostHookOnTransferCount + 1;
    ghostHookOnTransferPool64 = poolId;
    ghostHookOnTransferScId = scId;
    ghostHookOnTransferFromCid16 = fromCentrifugeId;
    ghostHookOnTransferToCid16 = toCentrifugeId;
    ghostHookOnTransferShares128 = sharesTransferred;
}
