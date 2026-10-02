/* ── MUTATION HubRegistry #9940 ───────────────────────────────────────────
 * @desc:   The pool id packs the chain one bit too low, so the chain overlaps the local id and two different pools can share one id.
 * @rules:  hlHrPoolIdIsTheChainOverTheLocalId
 * @conf:   certora/confs/core/hub/HubRegistry/single_pool_high_level.conf
 * @target: src/core/types/PoolId.sol
 * Was:     return PoolId.wrap((uint64(centrifugeId_) << 48) | uint64(localPoolId));
 * Now:     return PoolId.wrap((uint64(centrifugeId_) << 47) | uint64(localPoolId)); // MUTATION: the chain is shifted by 47 bits instead of 48
 * ────────────────────────────────────────────────────────────────*/
// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

type PoolId is uint64;

function centrifugeId(PoolId poolId) pure returns (uint16) {
    return uint16(PoolId.unwrap(poolId) >> 48);
}

function newPoolId(uint16 centrifugeId_, uint48 localPoolId) pure returns (PoolId) {
    return PoolId.wrap((uint64(centrifugeId_) << 47) | uint64(localPoolId)); // MUTATION: the chain is shifted by 47 bits instead of 48
}

function isNull(PoolId poolId) pure returns (bool) {
    return PoolId.unwrap(poolId) == 0;
}

function isEqual(PoolId a, PoolId b) pure returns (bool) {
    return PoolId.unwrap(a) == PoolId.unwrap(b);
}

function raw(PoolId poolId) pure returns (uint64) {
    return PoolId.unwrap(poolId);
}

using {centrifugeId, isNull, raw, isEqual as ==} for PoolId global;
