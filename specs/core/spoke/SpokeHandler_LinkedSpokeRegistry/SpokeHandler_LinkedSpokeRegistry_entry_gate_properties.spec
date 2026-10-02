import "setup/SpokeHandler_LinkedSpokeRegistry_entry_gate.spec";

// --- high_level ---

// SH-HL-22: a metadata update writes no field of the handler or the registry, under any key.
rule hlShUpdateShareMetadataWritesNoHandlerOrRegistryField(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, string name, string symbol, SpokeRegistry.PoolId p,
    SpokeRegistry.ShareClassId s, SpokeRegistry.AssetId a, address who, address t, uint256 id, bytes32 authId) {

    setupSpokeHandlerEntryGate(e);

    uint256 wardBefore = _SpokeHandler.wards[who];
    address registryBefore = _SpokeHandler.spokeRegistry;
    address factoryBefore = _SpokeHandler.escrowFactory;
    uint256 srWardBefore = _SpokeRegistry.wards[who];
    uint64 createdAtBefore = _SpokeRegistry.pool[p].createdAt;
    SpokeRegistry.PoolId tokenPoolBefore = _SpokeRegistry.tokenDetails[t].poolId;
    address requestManagerBefore = _SpokeRegistry.requestManager[p];
    address shareTokenBefore = _SpokeRegistry.shareClass[p][s].shareToken;
    address registrarBefore = _SpokeRegistry.shareClass[p][s].registrar;
    SpokeRegistry.D18 sharePriceBefore = _SpokeRegistry.shareClass[p][s].pricePoolPerShare.price;
    bool managerBefore = _SpokeRegistry.manager[p][who];
    bool bridgerBefore = _SpokeRegistry.bridger[p][who];
    address policyBefore = _SpokeRegistry._policy[p].policy;
    uint64 nonceBefore = _SpokeRegistry._policy[p].nonce;
    uint256 authorizationsBefore = _SpokeRegistry.authorizations[authId];
    uint64 assetCounterBefore = _SpokeRegistry._assetCounter;
    address idAssetBefore = _SpokeRegistry._idToAsset[a].asset;
    SpokeRegistry.AssetId assetIdBefore = _SpokeRegistry._assetToId[t][id];
    SpokeRegistry.D18 assetPriceBefore = _SpokeRegistry._pricePoolPerAsset[p][s][a].price;
    bool linkedBefore = _SpokeRegistry._vaultDetails[t].isLinked;
    mathint supplyCallsBefore = ghostRegistrarSupplyCalls;
    mathint restrictionsBefore = ghostRegistrarRestrictionCount;

    _SpokeHandler.updateShareMetadata(e, poolId, scId, name, symbol);

    assert(_SpokeHandler.wards[who] == wardBefore && _SpokeHandler.spokeRegistry == registryBefore
            && _SpokeHandler.escrowFactory == factoryBefore,
        "the handler's wards and wiring stay as they were");
    assert(_SpokeRegistry.wards[who] == srWardBefore && _SpokeRegistry.pool[p].createdAt == createdAtBefore
            && _SpokeRegistry.tokenDetails[t].poolId == tokenPoolBefore
            && _SpokeRegistry.requestManager[p] == requestManagerBefore
            && _SpokeRegistry.shareClass[p][s].shareToken == shareTokenBefore
            && _SpokeRegistry.shareClass[p][s].registrar == registrarBefore
            && _SpokeRegistry.shareClass[p][s].pricePoolPerShare.price == sharePriceBefore
            && _SpokeRegistry.manager[p][who] == managerBefore && _SpokeRegistry.bridger[p][who] == bridgerBefore
            && _SpokeRegistry._policy[p].policy == policyBefore && _SpokeRegistry._policy[p].nonce == nonceBefore
            && _SpokeRegistry.authorizations[authId] == authorizationsBefore
            && _SpokeRegistry._assetCounter == assetCounterBefore && _SpokeRegistry._idToAsset[a].asset == idAssetBefore
            && _SpokeRegistry._assetToId[t][id] == assetIdBefore
            && _SpokeRegistry._pricePoolPerAsset[p][s][a].price == assetPriceBefore
            && _SpokeRegistry._vaultDetails[t].isLinked == linkedBefore,
        "no registry row moves");
    assert(ghostRegistrarSupplyCalls == supplyCallsBefore && ghostRegistrarRestrictionCount == restrictionsBefore,
        "no supply or restriction call reaches the registrar");
}

// --- access_control ---

// SH-AC-18: changing a share token's name or symbol through the handler fails for a non-admin.
rule acShUpdateShareMetadataRefusesANonWard(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, string name, string symbol) {

    setupSpokeHandlerEntryGate(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];

    _SpokeHandler.updateShareMetadata@withrevert(e, poolId, scId, name, symbol);
    bool reverted = lastReverted;

    assert(callerWardBefore != 1 => reverted, "a non-ward call to the metadata writer reverts");
}
