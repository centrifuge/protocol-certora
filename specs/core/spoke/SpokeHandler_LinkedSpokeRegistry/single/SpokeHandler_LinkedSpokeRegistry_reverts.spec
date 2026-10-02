import "../setup/SpokeHandler_LinkedSpokeRegistry_base.spec";

// SH-RV-01: changing the handler's configuration fails for a non-admin or an unknown key.
rule rvShFileRefusesANonWardOrAnUnknownName(env e, bytes32 what, address data) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    bool unknownName = what != FILE_KEY_SPOKE_REGISTRY_SH_CVL()
        && what != FILE_KEY_ESCROW_FACTORY_SH_CVL();

    _SpokeHandler.file@withrevert(e, what, data);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || unknownName) => reverted, "rewiring fails for a non-ward or an unknown name");
}

// SH-RV-02: adding a pool fails for an unauthorized caller or a pool already added.
rule rvShAddPoolRefusesAnUntrustedCallerOrAPoolAlreadyOpen(env e, SpokeHandler.PoolId poolId) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeHandler.addPool@withrevert(e, poolId);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || createdAtBefore != 0) => reverted,
        "adding a pool fails on a missing ward or an existing pool");
}

// SH-RV-03: adding a share class fails if unauthorized, with no registrar or pool, or a taken class or token.
rule rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot(env e, SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId,
    string name, string symbol, uint8 decimals, bytes32 salt, address registrar, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    mathint createdAtBefore = ghostSrCreatedAt64;
    address shareTokenBefore = ghostSrShareToken;
    address deployedToken = ghostRegistrarNewToken;
    mathint tokenPoolIdBefore = ghostSrTokenPoolId64[deployedToken];
    bool anyGateFails = callerWardBefore != 1 || registryWardBefore != 1 || registrar == 0
        || createdAtBefore == 0 || shareTokenBefore != 0 || tokenPoolIdBefore != 0;

    _SpokeHandler.addShareClass@withrevert(e, poolId, scId, name, symbol, decimals, salt, registrar, payload);
    bool reverted = lastReverted;

    assert(anyGateFails => reverted,
        "a new class needs both wards, a registrar, an opened pool, a free slot and token");
}

// SH-RV-04: changing pool manager rights fails for an unauthorized caller or a pool not yet added.
rule rvShUpdateManagerRefusesAnUntrustedCallerOrAPoolNeverOpened(env e, SpokeHandler.PoolId poolId,
    address who, bool canManage) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeHandler.updateManager@withrevert(e, poolId, who, canManage);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || createdAtBefore == 0) => reverted,
        "a manager update fails on a missing ward or an unopened pool");
}

// SH-RV-05: changing share bridging rights fails for an unauthorized caller or a pool not yet added.
rule rvShUpdateBridgerRefusesAnUntrustedCallerOrAPoolNeverOpened(env e, SpokeHandler.PoolId poolId,
    address who, bool canBridge) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeHandler.updateBridger@withrevert(e, poolId, who, canBridge);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || createdAtBefore == 0) => reverted,
        "a bridger update fails on a missing ward or an unopened pool");
}

// SH-RV-06: setting a policy fails for an unauthorized caller or a pool not yet added.
rule rvShSetPolicyRefusesAnUntrustedCallerOrAPoolNeverOpened(env e, SpokeHandler.PoolId poolId,
    address newPolicy) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeHandler.setPolicy@withrevert(e, poolId, newPolicy);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || createdAtBefore == 0) => reverted,
        "setting a policy fails on a missing ward or an unopened pool");
}

// SH-RV-07: authorizing a call fails for an unauthorized caller or a pool with no policy.
rule rvShAuthorizeRefusesAnUntrustedCallerOrAPoolWithNoRuleBook(env e, env eRead,
    SpokeHandler.PoolId poolId, bytes data) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    address policyBefore = ghostSrPolicy;

    _SpokeHandler.authorize@withrevert(e, poolId, data);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || policyBefore == 0) => reverted,
        "an authorization fails on a missing ward or when no policy is set");
}

// SH-RV-08: revoking an authorization fails for an unauthorized caller or when none is outstanding.
rule rvShUnauthorizeRefusesAnUntrustedCallerOrAGrantThatDoesNotStand(env e, env eRead,
    SpokeHandler.PoolId poolId, bytes data) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    bytes32 grantId = _SpokeRegistry.authId(eRead, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[grantId];

    _SpokeHandler.unauthorize@withrevert(e, poolId, data);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || countBefore == 0) => reverted,
        "a revocation fails on a missing ward or when no grant stands");
}

// SH-RV-09: a share price update fails for an unauthorized caller, an unknown class or an older timestamp.
rule rvShUpdatePricePoolPerShareRefusesAnUntrustedCallerAnAbsentClassOrAnOlderStamp(env e,
    SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId, SpokeHandler.D18 price, uint64 computedAt) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    address shareTokenBefore = ghostSrShareToken;
    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeHandler.updatePricePoolPerShare@withrevert(e, poolId, scId, price, computedAt);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || shareTokenBefore == 0
            || computedAt < stampBefore) => reverted,
        "a share price needs both wards, a tokened class and no older stamp");
}

// SH-RV-10: an asset price update fails if unauthorized, for an unknown class or asset, or an older timestamp.
rule rvShUpdatePricePoolPerAssetRefusesAnUntrustedCallerAnUnknownRowOrAnOlderStamp(env e,
    SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId,
    SpokeHandler.D18 price, uint64 computedAt) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    address shareTokenBefore = ghostSrShareToken;
    address assetRowBefore = ghostSrIdToAssetAsset[assetId];
    mathint stampBefore = ghostSrPricePoolPerAssetComputedAt64[assetId];

    _SpokeHandler.updatePricePoolPerAsset@withrevert(e, poolId, scId, assetId, price, computedAt);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || shareTokenBefore == 0
            || assetRowBefore == 0 || computedAt < stampBefore) => reverted,
        "an asset price needs both wards, a class, a known asset and no older stamp");
}

// SH-RV-11: assigning a request manager fails for an unauthorized caller or a pool not yet added.
rule rvShSetRequestManagerRefusesAnUntrustedCallerOrAPoolNeverOpened(env e, SpokeHandler.PoolId poolId,
    address manager) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeHandler.setRequestManager@withrevert(e, poolId, manager);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || createdAtBefore == 0) => reverted,
        "setting a request manager fails on a missing ward or an unopened pool");
}

// SH-RV-12: a request callback fails for an unauthorized caller or a pool without a deployed request manager.
rule rvShRequestCallbackRefusesAnUntrustedCallerOrAPoolWithNoRequestManager(env e,
    SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId,
    bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    address requestManagerBefore = ghostSrRequestManager;
    mathint requestManagerCodesize = nativeCodesize[requestManagerBefore];

    _SpokeHandler.requestCallback@withrevert(e, poolId, scId, assetId, payload);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || requestManagerBefore == 0 || requestManagerCodesize == 0) => reverted,
        "a callback reverts for a non-ward or a missing or codeless manager");
}

// SH-RV-13: a transfer restriction update fails for an unauthorized caller or a class not on this network.
rule rvShUpdateRestrictionRefusesAnUntrustedCallerOrAClassTheSpokeDoesNotCarry(env e,
    SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId, bytes update) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    address shareTokenBefore = ghostSrShareToken;
    address registrarBefore = ghostSrRegistrar;
    mathint registrarCodesize = nativeCodesize[registrarBefore];

    _SpokeHandler.updateRestriction@withrevert(e, poolId, scId, update);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || shareTokenBefore == 0 || registrarCodesize == 0) => reverted,
        "a restriction update fails for a non-ward, an unknown class or a codeless registrar");
}

// SH-RV-14: receiving bridged shares fails for an unauthorized caller, unknown class or malformed receiver.
rule rvShExecuteTransferSharesRefusesAnAbsentClassOrAMalformedReceiver(env e,
    SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId, bytes32 receiver, uint128 amount) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    address shareTokenBefore = ghostSrShareToken;
    address registrarBefore = ghostSrRegistrar;
    mathint registrarCodesize = nativeCodesize[registrarBefore];
    // A cross-chain address fills the top 20 bytes, the low 12 must be zero.
    bool receiverNamesNoAddress = (receiver << 160) != to_bytes32(0);

    _SpokeHandler.executeTransferShares@withrevert(e, poolId, scId, receiver, amount);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || shareTokenBefore == 0 || registrarCodesize == 0
            || receiverNamesNoAddress) => reverted,
        "bridging in fails for a non-ward, unknown class, codeless registrar or bad receiver");
}

// SH-RV-15: linking a vault fails for an unauthorized caller or an unregistered, linked or mismatched vault.
rule rvShUpdateVaultLinkRefusesAnUnknownOrMismatchedVault(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address vault, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    address assetRowBefore = ghostSrIdToAssetAsset[assetId];
    bool linkedBefore = ghostSrVaultIsLinked[vault];
    address vaultAssetBefore = ghostSrVaultAsset[vault];
    mathint vaultAssetIdBefore = ghostSrVaultAssetId128[vault];
    mathint vaultPoolIdBefore = ghostSrVaultPoolId64[vault];
    bytes16 vaultScIdBefore = ghostSrVaultScId[vault];

    _SpokeHandler.updateVault@withrevert(e, poolId, scId, assetId, vault,
        SpokeHandler.VaultUpdateKind.Link, payload);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || assetRowBefore == 0 || linkedBefore
            || vaultAssetBefore == 0 || vaultAssetIdBefore != assetId
            || vaultPoolIdBefore != poolId || vaultScIdBefore != scId) => reverted,
        "linking fails on a missing ward, unknown asset or vault, a linked vault or a mismatch");
}

// SH-RV-16: unlinking a vault fails for an unauthorized caller or an unlinked or mismatched vault.
rule rvShUpdateVaultUnlinkRefusesAnUnroutedOrMismatchedVault(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address vault, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    address assetRowBefore = ghostSrIdToAssetAsset[assetId];
    bool linkedBefore = ghostSrVaultIsLinked[vault];
    mathint vaultAssetIdBefore = ghostSrVaultAssetId128[vault];
    mathint vaultPoolIdBefore = ghostSrVaultPoolId64[vault];
    bytes16 vaultScIdBefore = ghostSrVaultScId[vault];

    _SpokeHandler.updateVault@withrevert(e, poolId, scId, assetId, vault,
        SpokeHandler.VaultUpdateKind.Unlink, payload);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || assetRowBefore == 0 || !linkedBefore
            || vaultAssetIdBefore != assetId || vaultPoolIdBefore != poolId
            || vaultScIdBefore != scId) => reverted,
        "unlinking fails on a missing ward, unknown asset, an unlinked vault or a mismatch");
}

// SH-RV-17: deploying a vault fails for an unauthorized caller, an unknown asset or class, or a taken address.
rule rvShUpdateVaultDeployAndLinkRefusesAnUnknownAssetADeadClassOrATakenAddress(env e,
    SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId,
    address factory, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    address assetRowBefore = ghostSrIdToAssetAsset[assetId];
    address shareTokenBefore = ghostSrShareToken;
    address deployedVault = ghostHmNewVault;
    address vaultAssetBefore = ghostSrVaultAsset[deployedVault];

    _SpokeHandler.updateVault@withrevert(e, poolId, scId, assetId, factory,
        SpokeHandler.VaultUpdateKind.DeployAndLink, payload);
    bool reverted = lastReverted;

    assert((callerWardBefore != 1 || registryWardBefore != 1 || assetRowBefore == 0
            || shareTokenBefore == 0 || vaultAssetBefore != 0) => reverted,
        "deploy and link fails on a missing ward, unknown asset or class, or a taken vault");
}

// SH-RV-18: adding a share class that passes every check always goes through.
rule rvShAddShareClassAcceptsACleanRegistration(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, string name, string symbol, uint8 decimals, bytes32 salt,
    address registrar, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);
    require(nativeCodesize[registrar] > 0, "TRUSTED: the hub names only deployed registrars");

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    mathint createdAtBefore = ghostSrCreatedAt64;
    address shareTokenBefore = ghostSrShareToken;
    address deployedToken = ghostRegistrarNewToken;
    mathint tokenPoolIdBefore = ghostSrTokenPoolId64[deployedToken];
    bool saltBrandedWithPool = (salt >> 192) == to_bytes32(require_uint256(poolId));
    require(callerWardBefore == 1 && e.msg.value == 0 && registryWardBefore == 1 && registrar != 0
            && saltBrandedWithPool && createdAtBefore != 0 && shareTokenBefore == 0 && tokenPoolIdBefore == 0,
        "SCOPE: unpaid, every gate of SH-RV-03 and SH-RV-24 passed");

    _SpokeHandler.addShareClass@withrevert(e, poolId, scId, name, symbol, decimals, salt, registrar, payload);
    bool reverted = lastReverted;

    assert(!reverted, "a registration that clears every gate never reverts");
}

// SH-RV-19: granting admin rights over the handler fails for a non-admin.
rule rvShRelyRefusesANonWard(env e, address user) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];

    _SpokeHandler.rely@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerWardBefore != 1 => reverted, "granting ward rights fails for a non-ward");
}

// SH-RV-20: revoking admin rights over the handler fails for a non-admin.
rule rvShDenyRefusesANonWard(env e, address user) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];

    _SpokeHandler.deny@withrevert(e, user);
    bool reverted = lastReverted;

    assert(callerWardBefore != 1 => reverted, "revoking ward rights fails for a non-ward");
}

// SH-RV-21: changing pool manager rights never fails for an authorized caller on an added pool.
rule rvShUpdateManagerIsNeverRefusedOnAPoolTheHubOpened(env e, SpokeHandler.PoolId poolId, address who,
    bool canManage) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeHandler.updateManager@withrevert(e, poolId, who, canManage);
    bool reverted = lastReverted;

    assert((callerWardBefore == 1 && registryWardBefore == 1 && createdAtBefore != 0) => !reverted,
        "a manager update with both wards on an opened pool never fails");
}

// SH-RV-22: revoking an outstanding authorization always goes through for an authorized caller.
rule rvShUnauthorizeIsNeverRefusedOnAGrantThatStands(env e, env eRead, SpokeHandler.PoolId poolId,
    bytes data) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    bytes32 grantId = _SpokeRegistry.authId(eRead, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[grantId];

    _SpokeHandler.unauthorize@withrevert(e, poolId, data);
    bool reverted = lastReverted;

    assert((callerWardBefore == 1 && registryWardBefore == 1 && countBefore != 0) => !reverted,
        "a revocation with both wards and a standing grant never fails");
}

// SH-RV-23: the handler never rejects an admin's callback to a pool's deployed request manager.
rule rvShRequestCallbackIsNeverRefusedOnAPoolThatHasARequestManager(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    address requestManagerBefore = ghostSrRequestManager;
    mathint requestManagerCodesize = nativeCodesize[requestManagerBefore];

    _SpokeHandler.requestCallback@withrevert(e, poolId, scId, assetId, payload);
    bool reverted = lastReverted;

    assert((callerWardBefore == 1 && requestManagerBefore != 0 && requestManagerCodesize > 0) => !reverted,
        "a ward's request callback to a deployed manager never fails");
}

// SH-RV-24: adding a share class fails unless its salt begins with the pool's id.
rule rvShAddShareClassRefusesASaltOutsideItsPool(env e, SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId,
    string name, string symbol, uint8 decimals, bytes32 salt, address registrar, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bool saltOutsideThePool = (salt >> 192) != to_bytes32(require_uint256(poolId));

    _SpokeHandler.addShareClass@withrevert(e, poolId, scId, name, symbol, decimals, salt, registrar, payload);
    bool reverted = lastReverted;

    assert(saltOutsideThePool => reverted, "adding a class fails if the salt does not start with the pool id");
}

// SH-RV-25: a share price update stamped later than the spoke's current time fails.
rule rvShSharePriceStampedAheadOfTheClockIsRefused(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.D18 price, uint64 computedAt) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    _SpokeHandler.updatePricePoolPerShare@withrevert(e, poolId, scId, price, computedAt);
    bool reverted = lastReverted;

    assert(computedAt > e.block.timestamp => reverted, "a share price from the future never lands");
}

// SH-RV-26: an asset price update stamped later than the spoke's current time fails.
rule rvShAssetPriceStampedAheadOfTheClockIsRefused(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, SpokeHandler.D18 price, uint64 computedAt) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    _SpokeHandler.updatePricePoolPerAsset@withrevert(e, poolId, scId, assetId, price, computedAt);
    bool reverted = lastReverted;

    assert(computedAt > e.block.timestamp => reverted, "an asset price from the future never lands");
}

// SH-RV-27: unlinking a vault from the pool, class and asset it is linked to never fails for an admin.
rule rvShUpdateVaultUnlinkIsNeverRefusedForALinkedVault(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address vault, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint registryWardBefore = _SpokeRegistry.wards[_SpokeHandler];
    address assetRowBefore = ghostSrIdToAssetAsset[assetId];
    bool linkedBefore = ghostSrVaultIsLinked[vault];
    mathint vaultAssetIdBefore = ghostSrVaultAssetId128[vault];
    mathint vaultPoolIdBefore = ghostSrVaultPoolId64[vault];
    bytes16 vaultScIdBefore = ghostSrVaultScId[vault];

    _SpokeHandler.updateVault@withrevert(e, poolId, scId, assetId, vault,
        SpokeHandler.VaultUpdateKind.Unlink, payload);
    bool reverted = lastReverted;

    assert((callerWardBefore == 1 && registryWardBefore == 1 && assetRowBefore != 0 && linkedBefore
            && vaultAssetIdBefore == assetId && vaultPoolIdBefore == poolId && vaultScIdBefore == scId) => !reverted,
        "an unlink of a linked vault under its own ids with both wards never fails");
}
