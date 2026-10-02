// HubRegistry. Setup: the registry link, the authorization id ghost.

import "../../../../shared/env.spec";
import "../../../../shared/domains/pool.spec";

using HubRegistry as _HubRegistry;

methods {
    function HubRegistry._authId(HubRegistry.PoolId poolId_, address policy_, uint64 nonce_, bytes calldata data) internal returns (bytes32)
        => hubRegistryAuthIdCVL(poolId_, policy_, nonce_, data);

    // SCOPE: no rule reads free form bytes, so setMetadata is cut.
    function _HubRegistry.setMetadata(HubRegistry.PoolId, bytes) external
        => NONDET DELETE;
}

persistent ghost mapping(uint64 => mapping(address => mapping(uint64 => mapping(bytes32 => bytes32)))) ghostHrAuthId {
    // UNSAFE: the image is never zero, so an empty slot means no grant.
    axiom forall uint64 p. forall address pol. forall uint64 n. forall bytes32 h.
        ghostHrAuthId[p][pol][n][h] != to_bytes32(0);

    // SAFE: injective as keccak is, so no key's grant aliases another's.
    axiom forall uint64 p1. forall uint64 p2. forall address pol1. forall address pol2.
        forall uint64 n1. forall uint64 n2. forall bytes32 h1. forall bytes32 h2.
            (p1 != p2 || pol1 != pol2 || n1 != n2 || h1 != h2)
                => ghostHrAuthId[p1][pol1][n1][h1] != ghostHrAuthId[p2][pol2][n2][h2];
}

function hubRegistryAuthIdCVL(HubRegistry.PoolId poolId_, address policy_, uint64 nonce_, bytes data) returns bytes32 {
    require(VALID_POOL(poolId_), "SCOPE: modelled pools stand for any");
    return ghostHrAuthId[poolId_][policy_][nonce_][keccak256(data)];
}

definition EXCLUDED_FUNCTION_HR(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

// SAFE: HubRegistry's internal MAX_DECIMALS, which has no getter.
definition MAX_DECIMALS_CVL() returns mathint = 18;

persistent ghost mapping(mathint => bool) ghostHrAssetRegistered {
    init_state axiom forall mathint a. !ghostHrAssetRegistered[a];
}

persistent ghost mapping(mathint => mathint) ghostHrAssetDecimals8 {
    init_state axiom forall mathint a. ghostHrAssetDecimals8[a] == 0;
    axiom forall mathint a. ghostHrAssetDecimals8[a] >= 0 && ghostHrAssetDecimals8[a] <= max_uint8;
}

hook Sload bool val _HubRegistry.asset[KEY HubRegistry.AssetId a].registered {
    require(ghostHrAssetRegistered[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.asset[KEY HubRegistry.AssetId a].registered bool val {
    ghostHrAssetRegistered[a] = val;
}

hook Sload uint8 val _HubRegistry.asset[KEY HubRegistry.AssetId a].decimals {
    require(ghostHrAssetDecimals8[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.asset[KEY HubRegistry.AssetId a].decimals uint8 val {
    ghostHrAssetDecimals8[a] = val;
}

persistent ghost mapping(bytes32 => mathint) ghostHrAuthorizedAfter48 {
    init_state axiom forall bytes32 id. ghostHrAuthorizedAfter48[id] == 0;
    axiom forall bytes32 id. ghostHrAuthorizedAfter48[id] >= 0 && ghostHrAuthorizedAfter48[id] <= max_uint48;
}

hook Sload uint48 val _HubRegistry.authorizedAfter[KEY bytes32 id] {
    require(ghostHrAuthorizedAfter48[id] == val, "SAFE: mirror tracks storage");
}

hook Sstore _HubRegistry.authorizedAfter[KEY bytes32 id] uint48 val {
    ghostHrAuthorizedAfter48[id] = val;
}

function setupHubRegistry(env e) {
    setupEnv(e);
    setupPoolMode();
    require(e.msg.sender != _HubRegistry, "SAFE: the registry never calls itself");
}

definition AUTH_LEDGER_FUNCTION_HR(method f) returns bool =
    f.selector == sig:_HubRegistry.initiateAuthorization(HubRegistry.PoolId,address,bytes).selector
    || f.selector == sig:_HubRegistry.cancelAuthorization(HubRegistry.PoolId,address,bytes).selector
    || f.selector == sig:_HubRegistry.consumeAuthorization(HubRegistry.PoolId,address,bytes,uint48).selector;

definition MANAGER_WRITER_FUNCTION_HR(method f) returns bool =
    f.selector == sig:_HubRegistry.registerPool(HubRegistry.PoolId,address,HubRegistry.AssetId).selector
    || f.selector == sig:_HubRegistry.updateManager(HubRegistry.PoolId,address,bool).selector;

definition PENDING_HR(address pol, uint64 nonce, bytes32 dataHash) returns mathint =
    ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][pol][nonce][dataHash]];
