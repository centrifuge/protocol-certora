// HubRegistry, multi-pool lane. Setup: registry rows keyed by pool, for isolation.

// Own setup: rows keyed by pool over two pools; single_pool hooks the same registry fields for one pinned pool.

import "HubRegistry_base.spec";
import "../../../../shared/domains/multi_pool.spec";

persistent ghost mapping(uint64 => mathint) ghostHrPoolCurrency128 {
    init_state axiom forall uint64 p. ghostHrPoolCurrency128[p] == 0;
    axiom forall uint64 p. ghostHrPoolCurrency128[p] >= 0 && ghostHrPoolCurrency128[p] <= max_uint128;
    axiom forall uint64 p. !VALID_POOL(p) => ghostHrPoolCurrency128[p] == 0;
}

hook Sload HubRegistry.AssetId val _HubRegistry.currency[KEY HubRegistry.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrPoolCurrency128[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.currency[KEY HubRegistry.PoolId p] HubRegistry.AssetId val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrPoolCurrency128[p] = val;
}

persistent ghost mapping(uint64 => mapping(address => bool)) ghostHrPoolManager {
    init_state axiom forall uint64 p. forall address who. !ghostHrPoolManager[p][who];
    axiom forall uint64 p. forall address who. !VALID_POOL(p) => !ghostHrPoolManager[p][who];
}

hook Sload bool val _HubRegistry.manager[KEY HubRegistry.PoolId p][KEY address who] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrPoolManager[p][who] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.manager[KEY HubRegistry.PoolId p][KEY address who] bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrPoolManager[p][who] = val;
}

persistent ghost mapping(uint64 => address) ghostHrPoolPolicy {
    init_state axiom forall uint64 p. ghostHrPoolPolicy[p] == 0;
    axiom forall uint64 p. !VALID_POOL(p) => ghostHrPoolPolicy[p] == 0;
}

hook Sload address val _HubRegistry._policy[KEY HubRegistry.PoolId p].policy {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrPoolPolicy[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry._policy[KEY HubRegistry.PoolId p].policy address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrPoolPolicy[p] = val;
}

persistent ghost mapping(uint64 => mathint) ghostHrPoolPolicyNonce64 {
    init_state axiom forall uint64 p. ghostHrPoolPolicyNonce64[p] == 0;
    axiom forall uint64 p. ghostHrPoolPolicyNonce64[p] >= 0 && ghostHrPoolPolicyNonce64[p] <= max_uint64;
    axiom forall uint64 p. !VALID_POOL(p) => ghostHrPoolPolicyNonce64[p] == 0;
}

hook Sload uint64 val _HubRegistry._policy[KEY HubRegistry.PoolId p].nonce {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrPoolPolicyNonce64[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry._policy[KEY HubRegistry.PoolId p].nonce uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrPoolPolicyNonce64[p] = val;
}

persistent ghost mapping(uint64 => address) ghostHrPoolBridgingHook {
    init_state axiom forall uint64 p. ghostHrPoolBridgingHook[p] == 0;
    axiom forall uint64 p. !VALID_POOL(p) => ghostHrPoolBridgingHook[p] == 0;
}

hook Sload address val _HubRegistry.bridgingHook[KEY HubRegistry.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrPoolBridgingHook[p] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.bridgingHook[KEY HubRegistry.PoolId p] address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrPoolBridgingHook[p] = val;
}

persistent ghost mapping(uint64 => mapping(uint16 => address)) ghostHrPoolHubRequestManager {
    init_state axiom forall uint64 p. forall uint16 cid. ghostHrPoolHubRequestManager[p][cid] == 0;
    axiom forall uint64 p. forall uint16 cid. !VALID_POOL(p) => ghostHrPoolHubRequestManager[p][cid] == 0;
}

hook Sload address val _HubRegistry.hubRequestManager[KEY HubRegistry.PoolId p][KEY uint16 cid] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrPoolHubRequestManager[p][cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.hubRequestManager[KEY HubRegistry.PoolId p][KEY uint16 cid] address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrPoolHubRequestManager[p][cid] = val;
}

definition HR_POOL_PAIR(uint64 p, uint64 q) returns bool =
    (p == ghostPoolA64 && q == ghostPoolB64) || (p == ghostPoolB64 && q == ghostPoolA64);
