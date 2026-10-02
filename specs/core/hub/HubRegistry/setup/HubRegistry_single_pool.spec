// HubRegistry, single-pool lane. Setup: pool rows mirrored for the one pinned pool.

// Own setup: rows of the one pinned pool; multi_pool hooks the same registry fields with a pool key.

import "HubRegistry_base.spec";
import "../../../../shared/domains/single_pool.spec";

persistent ghost mathint ghostHrCurrency128 {
    init_state axiom ghostHrCurrency128 == 0;
    axiom ghostHrCurrency128 >= 0 && ghostHrCurrency128 <= max_uint128;
}

hook Sload HubRegistry.AssetId val _HubRegistry.currency[KEY HubRegistry.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrCurrency128 == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.currency[KEY HubRegistry.PoolId p] HubRegistry.AssetId val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrCurrency128 = assert_uint128(val);
}

persistent ghost mapping(address => bool) ghostHrManager {
    init_state axiom forall address who. !ghostHrManager[who];
}

hook Sload bool val _HubRegistry.manager[KEY HubRegistry.PoolId p][KEY address who] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrManager[who] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.manager[KEY HubRegistry.PoolId p][KEY address who] bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrManager[who] = val;
}

persistent ghost address ghostHrBridgingHook {
    init_state axiom ghostHrBridgingHook == 0;
}

hook Sload address val _HubRegistry.bridgingHook[KEY HubRegistry.PoolId p] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrBridgingHook == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.bridgingHook[KEY HubRegistry.PoolId p] address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrBridgingHook = val;
}

persistent ghost mapping(uint16 => address) ghostHrHubRequestManager {
    init_state axiom forall uint16 cid. ghostHrHubRequestManager[cid] == 0;
}

hook Sload address val _HubRegistry.hubRequestManager[KEY HubRegistry.PoolId p][KEY uint16 cid] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrHubRequestManager[cid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.hubRequestManager[KEY HubRegistry.PoolId p][KEY uint16 cid] address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrHubRequestManager[cid] = val;
}

persistent ghost address ghostHrPolicy {
    init_state axiom ghostHrPolicy == 0;
}

persistent ghost uint64 ghostHrPolicyNonce64 {
    init_state axiom ghostHrPolicyNonce64 == 0;
}

hook Sload address val _HubRegistry._policy[KEY HubRegistry.PoolId p].policy {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrPolicy == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry._policy[KEY HubRegistry.PoolId p].policy address val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrPolicy = val;
}

hook Sload uint64 val _HubRegistry._policy[KEY HubRegistry.PoolId p].nonce {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostHrPolicyNonce64 == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry._policy[KEY HubRegistry.PoolId p].nonce uint64 val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostHrPolicyNonce64 = val;
}

function assumeManagerImpliesPoolExists() {
    require(forall address who. ghostHrManager[who] => ghostHrCurrency128 != 0,
        "PROVED: managerImpliesPoolExists (HubRegistry)");
}

function SETUP_HR(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupHubRegistry(e);
}
