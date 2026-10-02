import "../setup/SpokeHandler_LinkedSpokeRegistry_base.spec";

// SH-AC-01: only a handler admin can grant or revoke admin rights on the spoke handler.
rule acShWardRosterMovesOnlyForAWard(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint wardBefore = _SpokeHandler.wards[user];

    f(e, args);

    mathint wardAfter = _SpokeHandler.wards[user];

    assert(wardAfter != wardBefore => callerWardBefore == 1, "only a ward can grant or revoke ward rights");
}

// SH-AC-02: only a handler admin can point the handler at a different spoke registry.
rule acShRegistryPointerMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    address registryBefore = _SpokeHandler.spokeRegistry;

    f(e, args);

    address registryAfter = _SpokeHandler.spokeRegistry;

    assert(registryAfter != registryBefore => callerWardBefore == 1, "only a ward can repoint the handler's registry");
}

// SH-AC-03: only a handler admin can point the handler at a different escrow factory.
rule acShEscrowFactoryPointerMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    address factoryBefore = _SpokeHandler.escrowFactory;

    f(e, args);

    address factoryAfter = _SpokeHandler.escrowFactory;

    assert(factoryAfter != factoryBefore => callerWardBefore == 1,
        "only a ward can repoint the handler's escrow factory");
}

// SH-AC-04: only a handler admin can register a pool on the spoke.
rule acShPoolRowMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint createdBefore = ghostSrCreatedAt64;

    f(e, args);

    mathint createdAfter = ghostSrCreatedAt64;

    assert(createdAfter != createdBefore => callerWardBefore == 1, "a non-ward never touches a pool's opening stamp");
}

// SH-AC-05: through the handler, only its admin can set a share class's token and registrar.
rule acShShareClassBindingMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    address tokenBefore = ghostSrShareToken;
    address registrarBefore = ghostSrRegistrar;

    f(e, args);

    address tokenAfter = ghostSrShareToken;
    address registrarAfter = ghostSrRegistrar;

    assert(tokenAfter != tokenBefore || registrarAfter != registrarBefore => callerWardBefore == 1,
        "only a ward can change a share class's token or registrar");
}

// SH-AC-06: through the handler, only its admin can change which class a share token belongs to.
rule acShTokenLookupMovesOnlyForAWard(env e, method f, calldataarg args, address t)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint poolBefore = ghostSrTokenPoolId64[t];
    bytes16 scBefore = ghostSrTokenScId[t];

    f(e, args);

    mathint poolAfter = ghostSrTokenPoolId64[t];
    bytes16 scAfter = ghostSrTokenScId[t];

    assert(poolAfter != poolBefore || scAfter != scBefore => callerWardBefore == 1,
        "only a ward can change which pool and class a token is filed under");
}

// SH-AC-07: through the handler, only its admin can grant or revoke a pool manager role.
rule acShManagerSeatMovesOnlyForAWard(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    bool seatBefore = ghostSrManager[who];

    f(e, args);

    bool seatAfter = ghostSrManager[who];

    assert(seatAfter != seatBefore => callerWardBefore == 1, "only a ward can grant or revoke pool manager rights");
}

// SH-AC-08: through the handler, only its admin can grant or revoke a pool's share bridging role.
rule acShBridgerSeatMovesOnlyForAWard(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    bool seatBefore = ghostSrBridger[who];

    f(e, args);

    bool seatAfter = ghostSrBridger[who];

    assert(seatAfter != seatBefore => callerWardBefore == 1, "only a ward can grant or revoke bridger rights");
}

// SH-AC-09: through the handler, only its admin can change a pool's policy.
rule acShPolicyRowMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;

    f(e, args);

    address policyAfter = ghostSrPolicy;
    mathint nonceAfter = ghostSrPolicyNonce64;

    assert(policyAfter != policyBefore || nonceAfter != nonceBefore => callerWardBefore == 1,
        "only a ward can change a pool's policy or its policy nonce");
}

// SH-AC-10: through the handler, only its admin can grant or revoke a pool authorization.
rule acShAuthorizationLedgerMovesOnlyForAWard(env e, method f, calldataarg args, bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint countBefore = ghostSrAuthorizations256[id];

    f(e, args);

    mathint countAfter = ghostSrAuthorizations256[id];

    assert(countAfter != countBefore => callerWardBefore == 1, "only a ward can grant or revoke an authorization");
}

// SH-AC-11: through the handler, only its admin can update a share class price or its timestamp.
rule acShSharePriceMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint priceBefore = ghostSrPricePoolPerShare128;
    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    f(e, args);

    mathint priceAfter = ghostSrPricePoolPerShare128;
    mathint stampAfter = ghostSrPricePoolPerShareComputedAt64;

    assert(priceAfter != priceBefore || stampAfter != stampBefore => callerWardBefore == 1,
        "only a ward can change a share price or its timestamp");
}

// SH-AC-12: through the handler, only its admin can update an asset price or its timestamp.
rule acShAssetPriceMovesOnlyForAWard(env e, method f, calldataarg args, SpokeHandler.AssetId aid)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint priceBefore = ghostSrPricePoolPerAsset128[aid];
    mathint stampBefore = ghostSrPricePoolPerAssetComputedAt64[aid];

    f(e, args);

    mathint priceAfter = ghostSrPricePoolPerAsset128[aid];
    mathint stampAfter = ghostSrPricePoolPerAssetComputedAt64[aid];

    assert(priceAfter != priceBefore || stampAfter != stampBefore => callerWardBefore == 1,
        "only a ward can change an asset price or its timestamp");
}

// SH-AC-13: only a handler admin can change a vault's registration or its linked status.
rule acShVaultRowMovesOnlyForAWard(env e, method f, calldataarg args, address v)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint poolBefore = ghostSrVaultPoolId64[v];
    bytes16 scBefore = ghostSrVaultScId[v];
    mathint assetIdBefore = ghostSrVaultAssetId128[v];
    address assetBefore = ghostSrVaultAsset[v];
    mathint tokenIdBefore = ghostSrVaultTokenId256[v];
    bool linkedBefore = ghostSrVaultIsLinked[v];

    f(e, args);

    mathint poolAfter = ghostSrVaultPoolId64[v];
    bytes16 scAfter = ghostSrVaultScId[v];
    mathint assetIdAfter = ghostSrVaultAssetId128[v];
    address assetAfter = ghostSrVaultAsset[v];
    mathint tokenIdAfter = ghostSrVaultTokenId256[v];
    bool linkedAfter = ghostSrVaultIsLinked[v];

    assert(poolAfter != poolBefore || scAfter != scBefore || assetIdAfter != assetIdBefore
            || assetAfter != assetBefore || tokenIdAfter != tokenIdBefore || linkedAfter != linkedBefore
        => callerWardBefore == 1,
        "a non-ward never alters a vault's record or its link");
}

// SH-AC-14: through the handler, only its admin can change a pool's request manager.
rule acShRequestManagerPointerMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    address managerBefore = ghostSrRequestManager;

    f(e, args);

    address managerAfter = ghostSrRequestManager;

    assert(managerAfter != managerBefore => callerWardBefore == 1, "only a ward can change a pool's request manager");
}

// SH-AC-15: through the handler, only its admin can change a share token's total supply.
rule acShShareSupplyMovesOnlyForAWard(env e, method f, calldataarg args, address t)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint supplyBefore = ghostERC20TotalSupply256[t];

    f(e, args);

    mathint supplyAfter = ghostERC20TotalSupply256[t];

    assert(supplyAfter != supplyBefore => callerWardBefore == 1, "only a ward can change a token's supply");
}

// SH-AC-16: through the handler, only its admin can change a holder's share balance.
rule acShHolderBalanceMovesOnlyForAWard(env e, method f, calldataarg args, address t, address a)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint balanceBefore = ghostERC20Balances128[t][a];

    f(e, args);

    mathint balanceAfter = ghostERC20Balances128[t][a];

    assert(balanceAfter != balanceBefore => callerWardBefore == 1, "only a ward can move a holder's token balance");
}

// SH-AC-17: through the handler, only its admin can send the request manager a request callback.
rule acShRequestCallbackGoesOutOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SH(f) } {

    setupSpokeHandlerLinkedSpokeRegistry(e);

    mathint callerWardBefore = _SpokeHandler.wards[e.msg.sender];
    mathint callbacksBefore = ghostHmCallbackCount;

    f(e, args);

    mathint callbacksAfter = ghostHmCallbackCount;

    assert(callbacksAfter != callbacksBefore => callerWardBefore == 1, "only a ward can send a request callback");
}
