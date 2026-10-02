import "setup/HubRegistry_metadata.spec";

// --- state_transitions ---

// HR-ST-12: no registry method but setMetadata moves any pool's metadata.
rule stHrOnlySetMetadataMovesMetadata(env e, method f, calldataarg args, HubRegistry.PoolId q)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupEnv(e);

    bytes32 metadataBefore = keccak256(_HubRegistry.metadata(e, q));

    f(e, args);

    assert(keccak256(_HubRegistry.metadata(e, q)) != metadataBefore
        => f.selector == sig:_HubRegistry.setMetadata(HubRegistry.PoolId,bytes).selector,
        "only setMetadata moves pool metadata");
}

// --- high_level ---

// HR-HL-13: metadata written as one or more whole 32-byte words reads back exactly as written.
rule hlHrSetMetadataStoresTheBytesVerbatim(env e, HubRegistry.PoolId p, bytes data) {

    setupEnv(e);

    // SCOPE: the model over-approximates short-form packing and ragged-tail masking; whole words avoid both.
    require(data.length > 0 && data.length % 32 == 0, "SCOPE: metadata of one or more whole words");

    _HubRegistry.setMetadata(e, p, data);

    bytes stored = _HubRegistry.metadata(e, p);

    assert(stored.length == data.length && keccak256(stored) == keccak256(data),
        "the stored metadata matches the written bytes in length and content");
}

// HR-HL-15: setMetadata writes only the named pool's metadata; every other field reads the same under any key.
rule hlHrSetMetadataWritesOnlyItsPoolsMetadata(env e, HubRegistry.PoolId p, bytes data, HubRegistry.PoolId q,
    HubRegistry.AssetId a, address who, bytes32 authId, uint16 cid) {

    setupEnv(e);

    bool registeredBefore = _HubRegistry.asset[a].registered;
    uint8 decimalsBefore = _HubRegistry.asset[a].decimals;
    HubRegistry.AssetId currencyBefore = _HubRegistry.currency[q];
    bool managerBefore = _HubRegistry.manager[q][who];
    address policyBefore = _HubRegistry._policy[q].policy;
    uint64 nonceBefore = _HubRegistry._policy[q].nonce;
    uint48 authorizedAfterBefore = _HubRegistry.authorizedAfter[authId];
    address hookBefore = _HubRegistry.bridgingHook[q];
    address requestManagerBefore = _HubRegistry.hubRequestManager[q][cid];
    uint256 wardBefore = _HubRegistry.wards[who];
    bytes32 metadataQBefore = keccak256(_HubRegistry.metadata(e, q));

    _HubRegistry.setMetadata(e, p, data);

    assert(_HubRegistry.asset[a].registered == registeredBefore && _HubRegistry.asset[a].decimals == decimalsBefore
            && _HubRegistry.currency[q] == currencyBefore && _HubRegistry.manager[q][who] == managerBefore
            && _HubRegistry._policy[q].policy == policyBefore && _HubRegistry._policy[q].nonce == nonceBefore
            && _HubRegistry.authorizedAfter[authId] == authorizedAfterBefore
            && _HubRegistry.bridgingHook[q] == hookBefore && _HubRegistry.hubRequestManager[q][cid] == requestManagerBefore
            && _HubRegistry.wards[who] == wardBefore
            && (q != p => keccak256(_HubRegistry.metadata(e, q)) == metadataQBefore),
        "a metadata write moves nothing but the named pool's metadata");
}
