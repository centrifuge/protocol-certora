/* ── MUTATION ShareClassManager #9050 ──────────────────────────────
 * @desc:   The class id shifts the pool id only 16 bits above the index, so two pool and index pairs can share an id.
 * @rules:  hlScShareClassIdIsInjectiveInPoolAndIndex
 * @conf:   certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf
 * @target: src/core/types/ShareClassId.sol
 * Was:     return ShareClassId.wrap(bytes16((uint128(PoolId.unwrap(poolId)) << 64) + index_));
 * Now:     return ShareClassId.wrap(bytes16((uint128(PoolId.unwrap(poolId)) << 16) + index_)); // MUTATION: the pool id is shifted by 16 bits instead of 64
 * ────────────────────────────────────────────────────────────────────*/
// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {PoolId} from "./PoolId.sol";

type ShareClassId is bytes16;

function isNull(ShareClassId scId) pure returns (bool) {
    return ShareClassId.unwrap(scId) == 0;
}

function index(ShareClassId scId) pure returns (uint32) {
    return uint32(uint128(ShareClassId.unwrap(scId)));
}

function equals(ShareClassId left, ShareClassId right) pure returns (bool) {
    return ShareClassId.unwrap(left) == ShareClassId.unwrap(right);
}

function raw(ShareClassId scId) pure returns (bytes16) {
    return ShareClassId.unwrap(scId);
}

function newShareClassId(PoolId poolId, uint32 index_) pure returns (ShareClassId scId) {
    return ShareClassId.wrap(bytes16((uint128(PoolId.unwrap(poolId)) << 16) + index_)); // MUTATION: the pool id is shifted by 16 bits instead of 64
}

using {isNull, index, raw, equals as ==} for ShareClassId global;
