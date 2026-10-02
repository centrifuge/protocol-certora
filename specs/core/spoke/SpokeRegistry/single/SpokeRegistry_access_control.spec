import "../setup/SpokeRegistry_base.spec";

// SR-AC-01: only an admin can grant or revoke admin rights on the spoke registry.
rule acSrWardSetMovesOnlyForAWard(env e, method f, calldataarg args, address u)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    mathint wardBefore = _SpokeRegistry.wards(u);

    f(e, args);

    mathint wardAfter = _SpokeRegistry.wards(u);

    assert(wardAfter != wardBefore => senderWardBefore == 1, "only a ward can grant or revoke ward rights");
}

// SR-AC-02: only an admin can add a pool to the spoke.
rule acSrPoolEntryStampMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    mathint createdAtBefore = ghostSrCreatedAt64;

    f(e, args);

    mathint createdAtAfter = ghostSrCreatedAt64;

    assert(createdAtAfter != createdAtBefore => senderWardBefore == 1, "only a ward can change a pool's creation time");
}

// SR-AC-03: only an admin can set a share class's token or registrar.
rule acSrShareClassBindingMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    address shareTokenBefore = ghostSrShareToken;
    address registrarBefore = ghostSrRegistrar;

    f(e, args);

    address shareTokenAfter = ghostSrShareToken;
    address registrarAfter = ghostSrRegistrar;

    assert(shareTokenAfter != shareTokenBefore || registrarAfter != registrarBefore
        => senderWardBefore == 1,
        "a non-ward never rebinds a class's token or registrar");
}

// SR-AC-04: only an admin can change which pool and share class a token maps to.
rule acSrTokenLookupRowMovesOnlyForAWard(env e, method f, calldataarg args, address t)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    mathint tokenPoolIdBefore = ghostSrTokenPoolId64[t];
    bytes16 tokenScIdBefore = ghostSrTokenScId[t];

    f(e, args);

    mathint tokenPoolIdAfter = ghostSrTokenPoolId64[t];
    bytes16 tokenScIdAfter = ghostSrTokenScId[t];

    assert(tokenPoolIdAfter != tokenPoolIdBefore || tokenScIdAfter != tokenScIdBefore
        => senderWardBefore == 1,
        "a non-ward never remaps a token to another pool or class");
}

// SR-AC-05: only an admin can change a pool's request manager.
rule acSrRequestManagerMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    address requestManagerBefore = ghostSrRequestManager;

    f(e, args);

    address requestManagerAfter = ghostSrRequestManager;

    assert(requestManagerAfter != requestManagerBefore => senderWardBefore == 1,
        "a non-ward never swaps a pool's request manager");
}

// SR-AC-06: only an admin can grant or revoke pool manager rights.
rule acSrManagerRightsMoveOnlyForAWard(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    bool managerBefore = ghostSrManager[who];

    f(e, args);

    bool managerAfter = ghostSrManager[who];

    assert(managerAfter != managerBefore => senderWardBefore == 1, "a non-ward never seats or unseats a pool manager");
}

// SR-AC-07: only an admin can grant or revoke bridger rights (cross-chain share transfers).
rule acSrBridgerRightsMoveOnlyForAWard(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    bool bridgerBefore = ghostSrBridger[who];

    f(e, args);

    bool bridgerAfter = ghostSrBridger[who];

    assert(bridgerAfter != bridgerBefore => senderWardBefore == 1, "only a ward can grant or revoke bridger rights");
}

// SR-AC-08: only an admin can install, replace or remove a pool's policy.
rule acSrPolicyInstallMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;

    f(e, args);

    address policyAfter = ghostSrPolicy;
    mathint nonceAfter = ghostSrPolicyNonce64;

    assert(policyAfter != policyBefore || nonceAfter != nonceBefore => senderWardBefore == 1,
        "only a ward can change a pool's policy or its policy nonce");
}

// SR-AC-09: only an admin can grant an authorization.
rule acSrAuthorizationGrantedOnlyByAWard(env e, method f, calldataarg args, bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    mathint countBefore = ghostSrAuthorizations256[id];

    f(e, args);

    mathint countAfter = ghostSrAuthorizations256[id];

    assert(countAfter > countBefore => senderWardBefore == 1, "a non-ward never raises an authorization count");
}

// SR-AC-10: only an admin or the pool's installed policy can spend or revoke an authorization.
rule acSrAuthorizationSpentOrRevokedOnlyByAWardOrTheInstalledPolicy(env e, method f, calldataarg args, bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    address policyBefore = ghostSrPolicy;
    mathint countBefore = ghostSrAuthorizations256[id];

    f(e, args);

    mathint countAfter = ghostSrAuthorizations256[id];

    assert(countAfter < countBefore => senderWardBefore == 1 || caller == policyBefore,
        "only a ward or the installed policy can remove a grant");
}

// SR-AC-11: only an admin can register an asset or change its id mapping.
rule acSrAssetRegistryMovesOnlyForAWard(env e, method f, calldataarg args,
    SpokeRegistry.AssetId aid, address a, uint256 t)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    mathint counterBefore = ghostSrAssetCounter64;
    address forwardAssetBefore = ghostSrIdToAssetAsset[aid];
    mathint forwardTokenIdBefore = ghostSrIdToAssetTokenId256[aid];
    mathint reverseIdBefore = ghostSrAssetToId128[a][t];

    f(e, args);

    mathint counterAfter = ghostSrAssetCounter64;
    address forwardAssetAfter = ghostSrIdToAssetAsset[aid];
    mathint forwardTokenIdAfter = ghostSrIdToAssetTokenId256[aid];
    mathint reverseIdAfter = ghostSrAssetToId128[a][t];

    assert(counterAfter != counterBefore || forwardAssetAfter != forwardAssetBefore
        || forwardTokenIdAfter != forwardTokenIdBefore || reverseIdAfter != reverseIdBefore
        => senderWardBefore == 1,
        "only a ward can change asset numbering or its lookups");
}

// SR-AC-12: only an admin can register a vault or change what it is registered for.
rule acSrVaultRegistrationMovesOnlyForAWard(env e, method f, calldataarg args, address v)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    mathint vaultPoolIdBefore = ghostSrVaultPoolId64[v];
    bytes16 vaultScIdBefore = ghostSrVaultScId[v];
    mathint vaultAssetIdBefore = ghostSrVaultAssetId128[v];
    address vaultAssetBefore = ghostSrVaultAsset[v];
    mathint vaultTokenIdBefore = ghostSrVaultTokenId256[v];

    f(e, args);

    mathint vaultPoolIdAfter = ghostSrVaultPoolId64[v];
    bytes16 vaultScIdAfter = ghostSrVaultScId[v];
    mathint vaultAssetIdAfter = ghostSrVaultAssetId128[v];
    address vaultAssetAfter = ghostSrVaultAsset[v];
    mathint vaultTokenIdAfter = ghostSrVaultTokenId256[v];

    assert(vaultPoolIdAfter != vaultPoolIdBefore || vaultScIdAfter != vaultScIdBefore
        || vaultAssetIdAfter != vaultAssetIdBefore || vaultAssetAfter != vaultAssetBefore
        || vaultTokenIdAfter != vaultTokenIdBefore
        => senderWardBefore == 1,
        "only a ward can change a vault's registration");
}

// SR-AC-13: only an admin can link or unlink a vault.
rule acSrVaultLinkFlagMovesOnlyForAWard(env e, method f, calldataarg args, address v)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    bool isLinkedBefore = ghostSrVaultIsLinked[v];

    f(e, args);

    bool isLinkedAfter = ghostSrVaultIsLinked[v];

    assert(isLinkedAfter != isLinkedBefore => senderWardBefore == 1, "a non-ward never switches a vault on or off");
}

// SR-AC-14: only an admin can update a share class price.
rule acSrSharePriceMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    mathint priceBefore = ghostSrPricePoolPerShare128;
    mathint computedAtBefore = ghostSrPricePoolPerShareComputedAt64;

    f(e, args);

    mathint priceAfter = ghostSrPricePoolPerShare128;
    mathint computedAtAfter = ghostSrPricePoolPerShareComputedAt64;

    assert(priceAfter != priceBefore || computedAtAfter != computedAtBefore => senderWardBefore == 1,
        "only a ward can change a share price or its timestamp");
}

// SR-AC-15: only an admin can update an asset price.
rule acSrAssetPriceMovesOnlyForAWard(env e, method f, calldataarg args, SpokeRegistry.AssetId aid)
    filtered { f -> !EXCLUDED_FUNCTION_SR(f) } {

    setupSpokeRegistry(e);

    address caller = e.msg.sender;
    mathint senderWardBefore = _SpokeRegistry.wards(caller);
    mathint priceBefore = ghostSrPricePoolPerAsset128[aid];
    mathint computedAtBefore = ghostSrPricePoolPerAssetComputedAt64[aid];

    f(e, args);

    mathint priceAfter = ghostSrPricePoolPerAsset128[aid];
    mathint computedAtAfter = ghostSrPricePoolPerAssetComputedAt64[aid];

    assert(priceAfter != priceBefore || computedAtAfter != computedAtBefore => senderWardBefore == 1,
        "only a ward can change an asset price or its timestamp");
}
