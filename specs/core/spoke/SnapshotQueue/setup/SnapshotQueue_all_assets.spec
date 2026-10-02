// SnapshotQueue, all-assets lane. Setup: the pinned class, non-empty asset rows counted.

// Own setup: every asset id counted, no three asset cap; single_pool hooks the same fields and caps them at three ids.

import "../../../../shared/env.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/single_share_class.spec";

using SnapshotQueue as _SnapshotQueue;

definition EXCLUDED_FUNCTION_SQ(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

function setupSnapshotQueue(env e) {
    setupEnv(e);
    setupPoolMode();
    setupShareClassMode();
    require(e.msg.sender != _SnapshotQueue, "SAFE: the queue never calls itself");
}

function SETUP_SQ(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupSnapshotQueue(e);
}

persistent ghost mathint ghostSqDelta128 {
    init_state axiom ghostSqDelta128 == 0;
    axiom ghostSqDelta128 >= 0 && ghostSqDelta128 <= max_uint128;
}

persistent ghost bool ghostSqIsPositive {
    init_state axiom !ghostSqIsPositive;
}

persistent ghost mathint ghostSqQueuedAssetCounter32 {
    init_state axiom ghostSqQueuedAssetCounter32 == 0;
    axiom ghostSqQueuedAssetCounter32 >= 0 && ghostSqQueuedAssetCounter32 <= max_uint32;
}

persistent ghost mathint ghostSqNonce64 {
    init_state axiom ghostSqNonce64 == 0;
    axiom ghostSqNonce64 >= 0 && ghostSqNonce64 <= max_uint64;
}

persistent ghost mapping(uint128 => mathint) ghostSqAllDeposits128 {
    init_state axiom forall uint128 a. ghostSqAllDeposits128[a] == 0;
    axiom forall uint128 a. ghostSqAllDeposits128[a] >= 0 && ghostSqAllDeposits128[a] <= max_uint128;
}

persistent ghost mapping(uint128 => mathint) ghostSqAllWithdrawals128 {
    init_state axiom forall uint128 a. ghostSqAllWithdrawals128[a] == 0;
    axiom forall uint128 a. ghostSqAllWithdrawals128[a] >= 0 && ghostSqAllWithdrawals128[a] <= max_uint128;
}

persistent ghost mathint ghostSqNonEmptyRows {
    init_state axiom ghostSqNonEmptyRows == 0;
}

hook Sload uint128 val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].delta {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqDelta128 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].delta uint128 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSqDelta128 = val;
}

hook Sload bool val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].isPositive {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqIsPositive == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].isPositive bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSqIsPositive = val;
}

hook Sload uint32 val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].queuedAssetCounter {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqQueuedAssetCounter32 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].queuedAssetCounter uint32 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSqQueuedAssetCounter32 = val;
}

hook Sload uint64 val _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].nonce {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqNonce64 == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedShares[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc].nonce uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    ghostSqNonce64 = val;
}

hook Sload uint128 val _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].deposits {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqAllDeposits128[a] == val, "SAFE: mirror tracks storage");
}

// SAFE: the other amount is read before a row is emptied or filled.
hook Sstore _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].deposits uint128 val (uint128 held) {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    mathint w = ghostSqAllWithdrawals128[a];
    ghostSqNonEmptyRows = ghostSqNonEmptyRows + ((val != 0 || w != 0) ? 1 : 0) - ((held != 0 || w != 0) ? 1 : 0);
    ghostSqAllDeposits128[a] = val;
}

hook Sload uint128 val _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].withdrawals {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    require(ghostSqAllWithdrawals128[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _SnapshotQueue.queuedAssets[KEY SnapshotQueue.PoolId p][KEY SnapshotQueue.ShareClassId sc][KEY SnapshotQueue.AssetId a].withdrawals uint128 val (uint128 held) {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(VALID_SC(sc), "SCOPE: modelled classes stand for any");
    mathint d = ghostSqAllDeposits128[a];
    ghostSqNonEmptyRows = ghostSqNonEmptyRows + ((val != 0 || d != 0) ? 1 : 0) - ((held != 0 || d != 0) ? 1 : 0);
    ghostSqAllWithdrawals128[a] = val;
}
