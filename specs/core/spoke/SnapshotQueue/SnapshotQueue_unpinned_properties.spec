import "setup/SnapshotQueue_unpinned.spec";

// --- state_transitions ---

// SQ-ST-09: only queueing or flushing shares moves a class's queued net share amount or its direction.
rule stSqTheShareNetMovesOnlyUnderShareEntries(env e, method f, calldataarg args, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId) filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueueUnpinned(e);

    uint128 deltaBefore; bool signBefore; uint32 counterBefore; uint64 nonceBefore;
    deltaBefore, signBefore, counterBefore, nonceBefore = _SnapshotQueue.queuedShares(poolId, scId);

    f(e, args);

    uint128 deltaAfter; bool signAfter; uint32 counterAfter; uint64 nonceAfter;
    deltaAfter, signAfter, counterAfter, nonceAfter = _SnapshotQueue.queuedShares(poolId, scId);

    assert(deltaAfter != deltaBefore || signAfter != signBefore
        => f.selector == sig:_SnapshotQueue.queueShares(SnapshotQueue.PoolId, SnapshotQueue.ShareClassId, uint128,
                bool).selector
            || f.selector == sig:_SnapshotQueue.flushShares(SnapshotQueue.PoolId, SnapshotQueue.ShareClassId).selector,
        "only a share entry moves the queued share net");
}

// SQ-ST-10: only queueing or flushing assets moves an asset queue or a class's pending-asset count.
rule stSqAssetQueuesMoveOnlyUnderAssetEntries(env e, method f, calldataarg args, SnapshotQueue.PoolId poolId,
    SnapshotQueue.ShareClassId scId, SnapshotQueue.AssetId assetId) filtered { f -> !EXCLUDED_FUNCTION_SQ(f) } {

    setupSnapshotQueueUnpinned(e);

    uint128 depositsBefore; uint128 withdrawalsBefore;
    depositsBefore, withdrawalsBefore = _SnapshotQueue.queuedAssets(poolId, scId, assetId);
    uint128 deltaBefore; bool signBefore; uint32 counterBefore; uint64 nonceBefore;
    deltaBefore, signBefore, counterBefore, nonceBefore = _SnapshotQueue.queuedShares(poolId, scId);

    f(e, args);

    uint128 depositsAfter; uint128 withdrawalsAfter;
    depositsAfter, withdrawalsAfter = _SnapshotQueue.queuedAssets(poolId, scId, assetId);
    uint128 deltaAfter; bool signAfter; uint32 counterAfter; uint64 nonceAfter;
    deltaAfter, signAfter, counterAfter, nonceAfter = _SnapshotQueue.queuedShares(poolId, scId);

    assert(depositsAfter != depositsBefore || withdrawalsAfter != withdrawalsBefore || counterAfter != counterBefore
        => f.selector == sig:_SnapshotQueue.queueAssets(SnapshotQueue.PoolId, SnapshotQueue.ShareClassId,
                SnapshotQueue.AssetId, uint128, bool).selector
            || f.selector == sig:_SnapshotQueue.flushAssets(SnapshotQueue.PoolId, SnapshotQueue.ShareClassId,
                SnapshotQueue.AssetId).selector,
        "only an asset entry moves an asset queue or the pending-asset count");
}

// --- high_level ---

// SQ-HL-14: an asset flush empties that asset's queue, changing no other asset queue and not the queued shares.
rule hlSqAnAssetFlushEmptiesItsOwnRowOnly(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.AssetId assetId, SnapshotQueue.PoolId poolId2, SnapshotQueue.ShareClassId scId2,
    SnapshotQueue.AssetId assetId2) {

    setupSnapshotQueueUnpinned(e);

    bool otherRow = poolId2 != poolId || scId2 != scId || assetId2 != assetId;
    uint128 deposits2Before; uint128 withdrawals2Before;
    deposits2Before, withdrawals2Before = _SnapshotQueue.queuedAssets(poolId2, scId2, assetId2);
    uint128 deltaBefore; bool signBefore; uint32 counterBefore; uint64 nonceBefore;
    deltaBefore, signBefore, counterBefore, nonceBefore = _SnapshotQueue.queuedShares(poolId, scId);

    _SnapshotQueue.flushAssets(e, poolId, scId, assetId);

    uint128 depositsAfter; uint128 withdrawalsAfter;
    depositsAfter, withdrawalsAfter = _SnapshotQueue.queuedAssets(poolId, scId, assetId);
    uint128 deposits2After; uint128 withdrawals2After;
    deposits2After, withdrawals2After = _SnapshotQueue.queuedAssets(poolId2, scId2, assetId2);
    uint128 deltaAfter; bool signAfter; uint32 counterAfter; uint64 nonceAfter;
    deltaAfter, signAfter, counterAfter, nonceAfter = _SnapshotQueue.queuedShares(poolId, scId);

    assert(depositsAfter == 0 && withdrawalsAfter == 0, "the flushed asset has no deposits or withdrawals left");
    assert(otherRow => deposits2After == deposits2Before && withdrawals2After == withdrawals2Before,
        "no other asset queue in any pool or class moves");
    assert(deltaAfter == deltaBefore && signAfter == signBefore,
        "the queued net share amount and its direction stay put");
}

// SQ-HL-15: a share flush zeroes the queued shares and moves neither an asset queue nor the pending-asset count.
rule hlSqAShareFlushClearsOnlyItsNet(env e, SnapshotQueue.PoolId poolId, SnapshotQueue.ShareClassId scId,
    SnapshotQueue.PoolId poolId2, SnapshotQueue.ShareClassId scId2, SnapshotQueue.AssetId assetId2) {

    setupSnapshotQueueUnpinned(e);

    uint128 deposits2Before; uint128 withdrawals2Before;
    deposits2Before, withdrawals2Before = _SnapshotQueue.queuedAssets(poolId2, scId2, assetId2);
    uint128 deltaBefore; bool signBefore; uint32 counterBefore; uint64 nonceBefore;
    deltaBefore, signBefore, counterBefore, nonceBefore = _SnapshotQueue.queuedShares(poolId, scId);

    _SnapshotQueue.flushShares(e, poolId, scId);

    uint128 deposits2After; uint128 withdrawals2After;
    deposits2After, withdrawals2After = _SnapshotQueue.queuedAssets(poolId2, scId2, assetId2);
    uint128 deltaAfter; bool signAfter; uint32 counterAfter; uint64 nonceAfter;
    deltaAfter, signAfter, counterAfter, nonceAfter = _SnapshotQueue.queuedShares(poolId, scId);

    assert(deltaAfter == 0 && !signAfter, "no net issuance or revocation stays queued");
    assert(deposits2After == deposits2Before && withdrawals2After == withdrawals2Before,
        "no asset queue in any pool or class moves");
    assert(counterAfter == counterBefore, "the pending-asset count stays put");
}
