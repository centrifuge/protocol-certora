import "SpokeRegistry_valid_state.spec";

// SR-RV-01: adding a pool fails for a non-admin or a pool already added.
rule rvSrAddPoolRefusesANonWardOrAPoolAlreadyOpen(env e, SpokeRegistry.PoolId poolId) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeRegistry.addPool@withrevert(e, poolId);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || createdAtBefore != 0) => reverted,
        "opening a pool fails for a non-ward or an already opened pool");
}

// SR-RV-02: adding a share class fails for a non-admin, inactive pool, repeat, or missing token or registrar.
rule rvSrAddShareClassRefusesARepeatOrAnUnusableRegistration(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, address shareToken_, address registrar_) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    mathint createdAtBefore = ghostSrCreatedAt64;
    address shareTokenBefore = ghostSrShareToken;
    mathint tokenCodesize = nativeCodesize[shareToken_];

    _SpokeRegistry.addShareClass@withrevert(e, poolId, scId, shareToken_, registrar_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || createdAtBefore == 0 || shareTokenBefore != 0 || tokenCodesize == 0
            || registrar_ == 0) => reverted,
        "a class add fails for a non-ward, no pool, a repeat, no token code or no registrar");
}

// SR-RV-03: relinking a share token fails for a non-admin, an inactive pool, or a missing token or registrar.
rule rvSrLinkTokenRefusesANonWardADeadPoolOrAnUnusableToken(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, address shareToken_, address registrar_) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    mathint createdAtBefore = ghostSrCreatedAt64;
    mathint tokenCodesize = nativeCodesize[shareToken_];

    _SpokeRegistry.linkToken@withrevert(e, poolId, scId, shareToken_, registrar_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || createdAtBefore == 0 || tokenCodesize == 0 || registrar_ == 0)
        => reverted,
        "relinking fails for a non-ward, an unopened pool, a codeless token or no registrar");
}

// SR-RV-04: setting a request manager fails for a non-admin or a pool never added.
rule rvSrSetRequestManagerRefusesANonWardOrAPoolNeverOpened(env e, SpokeRegistry.PoolId poolId,
    address manager_) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeRegistry.setRequestManager@withrevert(e, poolId, manager_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || createdAtBefore == 0) => reverted,
        "a request manager change needs a ward and an opened pool");
}

// SR-RV-05: changing a pool manager fails for a non-admin or a pool never added.
rule rvSrUpdateManagerRefusesANonWardOrAPoolNeverOpened(env e, SpokeRegistry.PoolId poolId,
    address who, bool canManage) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeRegistry.updateManager@withrevert(e, poolId, who, canManage);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || createdAtBefore == 0) => reverted,
        "updating a pool manager fails for a non-ward or an unopened pool");
}

// SR-RV-06: changing a bridger fails for a non-admin or a pool never added.
rule rvSrUpdateBridgerRefusesANonWardOrAPoolNeverOpened(env e, SpokeRegistry.PoolId poolId,
    address who, bool canBridge) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeRegistry.updateBridger@withrevert(e, poolId, who, canBridge);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || createdAtBefore == 0) => reverted,
        "updating a bridger fails for a non-ward or an unopened pool");
}

// SR-RV-07: setting a policy fails for a non-admin or a pool never added.
rule rvSrSetPolicyRefusesANonWardOrAPoolNeverOpened(env e, SpokeRegistry.PoolId poolId, address policy_) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeRegistry.setPolicy@withrevert(e, poolId, policy_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || createdAtBefore == 0) => reverted, "a policy change needs a ward and an opened pool");
}

// SR-RV-08: recording an authorization fails for a non-admin or a pool without a policy.
rule rvSrAuthorizeRefusesANonWardOrAPoolWithNoPolicy(env e, SpokeRegistry.PoolId poolId, bytes data) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    address policyBefore = ghostSrPolicy;

    _SpokeRegistry.authorize@withrevert(e, poolId, data);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || policyBefore == 0) => reverted, "authorizing needs a ward and a pool with a policy");
}

// SR-RV-09: revoking an authorization fails for a non-admin or with none outstanding under the current policy.
rule rvSrUnauthorizeRefusesANonWardOrAGrantThatDoesNotStand(env e, env eRead,
    SpokeRegistry.PoolId poolId, bytes data) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    bytes32 id = _SpokeRegistry.authId(eRead, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.unauthorize@withrevert(e, poolId, data);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || countBefore == 0) => reverted,
        "a revocation fails for a non-ward or when no current grant stands");
}

// SR-RV-10: consuming an authorization fails for any caller but the pool's policy, or with none outstanding.
rule rvSrConsumeAuthorizationRefusesAnyCallerButThePolicyOrAnEmptySlot(env e, env eRead,
    SpokeRegistry.PoolId poolId, address caller, bytes data) {

    setupSpokeRegistryValidState(e);

    address policyBefore = ghostSrPolicy;
    address senderBefore = e.msg.sender;
    bytes32 id = _SpokeRegistry.authId(eRead, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.consumeAuthorization@withrevert(e, poolId, caller, data);
    bool reverted = lastReverted;

    assert((senderBefore != policyBefore || countBefore == 0) => reverted,
        "a consumption fails unless the policy calls and a current grant stands");
}

// SR-RV-11: vault registration fails for a non-admin, unknown class, repeat, wrong asset, or undeployed vault.
rule rvSrRegisterVaultRefusesARepeatOrAMismatchedRegistration(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, address asset, uint256 tokenId,
    address factory, address vault_, bytes payload) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    address shareTokenBefore = ghostSrShareToken;
    address registryAssetBefore = ghostSrIdToAssetAsset[assetId];
    mathint registryTokenIdBefore = ghostSrIdToAssetTokenId256[assetId];
    address vaultAssetBefore = ghostSrVaultAsset[vault_];
    mathint vaultCodesize = nativeCodesize[vault_];

    _SpokeRegistry.registerVault@withrevert(e, poolId, scId, assetId, asset, tokenId, factory, vault_, payload);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || shareTokenBefore == 0 || registryAssetBefore == 0
            || registryAssetBefore != asset || registryTokenIdBefore != tokenId
            || vaultAssetBefore != 0 || vaultCodesize == 0) => reverted,
        "registering a vault needs a ward, a class, the id's asset, a new vault with code");
}

// SR-RV-12: vault linking fails for a non-admin, unknown asset or vault, linked vault, or registration mismatch.
rule rvSrLinkVaultRefusesAnUnknownOrAlreadyLinkedVault(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, address vault_) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    address registryAssetBefore = ghostSrIdToAssetAsset[assetId];
    bool linkedBefore = ghostSrVaultIsLinked[vault_];
    address vaultAssetBefore = ghostSrVaultAsset[vault_];
    mathint vaultAssetIdBefore = ghostSrVaultAssetId128[vault_];
    mathint vaultPoolIdBefore = ghostSrVaultPoolId64[vault_];
    bytes16 vaultScIdBefore = ghostSrVaultScId[vault_];

    _SpokeRegistry.linkVault@withrevert(e, poolId, scId, assetId, vault_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || registryAssetBefore == 0 || linkedBefore || vaultAssetBefore == 0
            || vaultAssetIdBefore != assetId || vaultPoolIdBefore != poolId
            || vaultScIdBefore != scId) => reverted,
        "linking needs a ward, a known asset, an unlinked vault filed under these ids");
}

// SR-RV-13: vault unlinking fails for a non-admin, unknown asset, unlinked vault, or registration mismatch.
rule rvSrUnlinkVaultRefusesAnUnroutedOrMismatchedVault(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, address vault_) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    address registryAssetBefore = ghostSrIdToAssetAsset[assetId];
    bool linkedBefore = ghostSrVaultIsLinked[vault_];
    mathint vaultAssetIdBefore = ghostSrVaultAssetId128[vault_];
    mathint vaultPoolIdBefore = ghostSrVaultPoolId64[vault_];
    bytes16 vaultScIdBefore = ghostSrVaultScId[vault_];

    _SpokeRegistry.unlinkVault@withrevert(e, poolId, scId, assetId, vault_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || registryAssetBefore == 0 || !linkedBefore
            || vaultAssetIdBefore != assetId || vaultPoolIdBefore != poolId
            || vaultScIdBefore != scId) => reverted,
        "unlinking needs a ward, a known asset and a linked vault filed under these ids");
}

// SR-RV-14: creating an asset id fails for a non-admin, the zero address, or an asset already registered.
rule rvSrCreateAssetIdRefusesANonWardANullAssetOrAPairAlreadyNumbered(env e, uint16 centrifugeId,
    address asset, uint256 tokenId) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    mathint existingIdBefore = ghostSrAssetToId128[asset][tokenId];

    _SpokeRegistry.createAssetId@withrevert(e, centrifugeId, asset, tokenId);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || asset == 0 || existingIdBefore != 0) => reverted,
        "numbering fails for a non-ward, the null asset or an already numbered pair");
}

// SR-RV-15: a share price update fails for a non-admin, an unknown class, or an older price.
rule rvSrUpdatePricePoolPerShareRefusesANonWardADeadClassOrAnOlderStamp(env e,
    SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId, SpokeRegistry.D18 price,
    uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    address shareTokenBefore = ghostSrShareToken;
    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeRegistry.updatePricePoolPerShare@withrevert(e, poolId, scId, price, computedAt);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || shareTokenBefore == 0 || computedAt < stampBefore)
        => reverted,
        "a share price needs a ward, a tokened class and no older stamp");
}

// SR-RV-16: an asset price update fails for a non-admin, an unknown class or asset, or an older price.
rule rvSrUpdatePricePoolPerAssetRefusesANonWardAnUnknownAssetOrAnOlderStamp(env e,
    SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId,
    SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    address shareTokenBefore = ghostSrShareToken;
    address registryAssetBefore = ghostSrIdToAssetAsset[assetId];
    mathint stampBefore = ghostSrPricePoolPerAssetComputedAt64[assetId];

    _SpokeRegistry.updatePricePoolPerAsset@withrevert(e, poolId, scId, assetId, price, computedAt);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || shareTokenBefore == 0 || registryAssetBefore == 0
            || computedAt < stampBefore) => reverted,
        "an asset price needs a ward, a class, a known asset and no older stamp");
}

// SR-RV-17: a fail-closed asset lookup reverts on an unregistered id.
rule rvSrIdToAssetFailClosedRefusesAnUnregisteredId(env e, SpokeRegistry.AssetId assetId,
    bool revertOnNull) {

    setupSpokeRegistryValidState(e);

    address registryAssetBefore = ghostSrIdToAssetAsset[assetId];

    _SpokeRegistry.idToAsset@withrevert(e, assetId, revertOnNull);
    bool reverted = lastReverted;

    assert((revertOnNull && registryAssetBefore == 0) => reverted,
        "asked strictly, the registry rejects an unregistered asset id");
}

// SR-RV-18: the plain asset lookup never fails, even for an unregistered id.
rule rvSrIdToAssetLookupAlwaysAnswers(env e, SpokeRegistry.AssetId assetId) {

    setupSpokeRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");


    _SpokeRegistry.idToAsset@withrevert(e, assetId);
    bool reverted = lastReverted;

    assert(!reverted, "an id lookup without the strict flag always returns");
}

// SR-RV-19: a fail-closed asset id lookup reverts on an unregistered asset.
rule rvSrAssetToIdFailClosedRefusesAnUnregisteredPair(env e, address asset, uint256 tokenId,
    bool revertOnNull) {

    setupSpokeRegistryValidState(e);

    mathint registryIdBefore = ghostSrAssetToId128[asset][tokenId];

    _SpokeRegistry.assetToId@withrevert(e, asset, tokenId, revertOnNull);
    bool reverted = lastReverted;

    assert((revertOnNull && registryIdBefore == 0) => reverted, "a strict id lookup fails for a pair with no id");
}

// SR-RV-20: the plain asset id lookup never fails, even for an unregistered asset.
rule rvSrAssetToIdLookupAlwaysAnswers(env e, address asset, uint256 tokenId) {

    setupSpokeRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");


    _SpokeRegistry.assetToId@withrevert(e, asset, tokenId);
    bool reverted = lastReverted;

    assert(!reverted, "the plain id lookup never fails, even for a pair with no id");
}

// SR-RV-21: a validity-checked share price read fails when no price was ever set.
rule rvSrPricePoolPerShareCheckedRefusesANeverComputedPrice(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, bool checkValidity) {

    setupSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeRegistry.pricePoolPerShare@withrevert(e, poolId, scId, checkValidity);
    bool reverted = lastReverted;

    assert((checkValidity && stampBefore == 0) => reverted, "a never-priced class has no checked share price");
}

// SR-RV-22: a validity-checked asset price read fails when no price was ever set.
rule rvSrPricePoolPerAssetCheckedRefusesANeverComputedPrice(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, bool checkValidity) {

    setupSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrPricePoolPerAssetComputedAt64[assetId];

    _SpokeRegistry.pricePoolPerAsset@withrevert(e, poolId, scId, assetId, checkValidity);
    bool reverted = lastReverted;

    assert((checkValidity && stampBefore == 0) => reverted, "a never-priced asset has no checked asset price");
}

// SR-RV-23: granting registry admin rights fails for a non-admin.
rule rvSrRelyRefusesANonWard(env e, address user) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);

    _SpokeRegistry.rely@withrevert(e, user);
    bool reverted = lastReverted;

    assert(wardBitBefore != 1 => reverted, "a stranger cannot make anyone a registry ward");
}

// SR-RV-24: revoking registry admin rights fails for a non-admin.
rule rvSrDenyRefusesANonWard(env e, address user) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);

    _SpokeRegistry.deny@withrevert(e, user);
    bool reverted = lastReverted;

    assert(wardBitBefore != 1 => reverted, "a stranger cannot strip a registry ward");
}

// SR-RV-25: adding pool zero always fails, whoever calls and whatever the registry holds.
rule rvSrAddPoolRefusesTheNullPool(env e, SpokeRegistry.PoolId poolId) {

    setupEnv(e);

    _SpokeRegistry.addPool@withrevert(e, poolId);
    bool reverted = lastReverted;

    assert(poolId == 0 => reverted, "pool zero can never be added");
}

// SR-RV-26: an unpaid spend of an outstanding grant by the pool's policy never fails, whatever caller it names.
rule rvSrStandingGrantIsSpendableUnderAnyNamedCaller(env ePolicy, env eRead, SpokeRegistry.PoolId poolId,
    address caller, bytes data) {

    setupSpokeRegistryValidState(ePolicy);

    address policyBefore = ghostSrPolicy;
    bytes32 id = _SpokeRegistry.authId(eRead, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.consumeAuthorization@withrevert(ePolicy, poolId, caller, data);
    bool reverted = lastReverted;

    assert((ePolicy.msg.sender == policyBefore && ePolicy.msg.value == 0 && countBefore != 0) => !reverted,
        "the policy's unpaid spend of a live grant succeeds for any caller");
}

// SR-RV-27: an admin's share price update for a known class never fails unless older or future-dated.
rule rvSrHonestSharePriceUpdateIsAccepted(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    address shareTokenBefore = ghostSrShareToken;
    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeRegistry.updatePricePoolPerShare@withrevert(e, poolId, scId, price, computedAt);
    bool reverted = lastReverted;

    assert((e.msg.value == 0 && wardBitBefore == 1 && shareTokenBefore != 0
            && stampBefore <= computedAt && computedAt <= e.block.timestamp) => !reverted,
        "an admin's share price for a known class, dated from the last one to now, lands");
}

// SR-RV-28: an admin's asset price update for a known class and asset never fails unless older or future-dated.
rule rvSrHonestAssetPriceUpdateIsAccepted(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.AssetId assetId, SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    address shareTokenBefore = ghostSrShareToken;
    address registryAssetBefore = ghostSrIdToAssetAsset[assetId];
    mathint stampBefore = ghostSrPricePoolPerAssetComputedAt64[assetId];

    _SpokeRegistry.updatePricePoolPerAsset@withrevert(e, poolId, scId, assetId, price, computedAt);
    bool reverted = lastReverted;

    assert((e.msg.value == 0 && wardBitBefore == 1 && shareTokenBefore != 0 && registryAssetBefore != 0
            && stampBefore <= computedAt && computedAt <= e.block.timestamp) => !reverted,
        "an admin's asset price for a known class and asset, dated from the last one to now, lands");
}

// SR-RV-29: a future-dated share price update always fails, whoever calls.
rule rvSrSharePriceStampedAheadOfTheClockIsRefused(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    _SpokeRegistry.updatePricePoolPerShare@withrevert(e, poolId, scId, price, computedAt);
    bool reverted = lastReverted;

    assert(computedAt > e.block.timestamp => reverted, "a share price from the future never lands");
}

// SR-RV-30: a future-dated asset price update always fails, whoever calls.
rule rvSrAssetPriceStampedAheadOfTheClockIsRefused(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    _SpokeRegistry.updatePricePoolPerAsset@withrevert(e, poolId, scId, assetId, price, computedAt);
    bool reverted = lastReverted;

    assert(computedAt > e.block.timestamp => reverted, "an asset price from the future never lands");
}

// SR-RV-31: unlinking a linked vault never fails for an admin naming its pool, share class and asset.
rule rvSrUnlinkVaultIsNeverRefusedForALinkedVaultFiledUnderItsIds(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, address vault_) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    address registryAssetBefore = ghostSrIdToAssetAsset[assetId];
    bool linkedBefore = ghostSrVaultIsLinked[vault_];
    mathint vaultAssetIdBefore = ghostSrVaultAssetId128[vault_];
    mathint vaultPoolIdBefore = ghostSrVaultPoolId64[vault_];
    bytes16 vaultScIdBefore = ghostSrVaultScId[vault_];

    _SpokeRegistry.unlinkVault@withrevert(e, poolId, scId, assetId, vault_);
    bool reverted = lastReverted;

    assert((e.msg.value == 0 && wardBitBefore == 1 && registryAssetBefore != 0 && linkedBefore
            && vaultAssetIdBefore == assetId && vaultPoolIdBefore == poolId && vaultScIdBefore == scId) => !reverted,
        "an admin can always unlink a linked vault under its own pool, class and asset");
}

// SR-RV-32: setting a request manager never fails for an admin on an added pool.
rule rvSrSetRequestManagerIsNeverRefusedForAWardOnAnOpenedPool(env e, SpokeRegistry.PoolId poolId,
    address manager_) {

    setupSpokeRegistryValidState(e);

    mathint wardBitBefore = _SpokeRegistry.wards(e.msg.sender);
    mathint createdAtBefore = ghostSrCreatedAt64;

    _SpokeRegistry.setRequestManager@withrevert(e, poolId, manager_);
    bool reverted = lastReverted;

    assert((e.msg.value == 0 && wardBitBefore == 1 && createdAtBefore != 0) => !reverted,
        "an admin can always set or clear an added pool's request manager");
}
