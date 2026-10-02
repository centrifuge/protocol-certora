import "HubRegistry_single_pool_valid_state.spec";

// HR-AC-01: only an admin can grant or revoke admin rights on the hub registry.
rule acHrWardRightsMoveOnlyForAWard(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint senderWardBefore = _HubRegistry.wards[e.msg.sender];
    mathint userWardBefore = _HubRegistry.wards[user];

    f(e, args);

    mathint userWardAfter = _HubRegistry.wards[user];

    assert(userWardAfter != userWardBefore => senderWardBefore == 1, "only a ward can grant or revoke ward rights");
}

// HR-AC-02: only an admin can register an asset or change its decimals.
rule acHrAssetRowMovesOnlyForAWard(env e, method f, calldataarg args, uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint senderWardBefore = _HubRegistry.wards[e.msg.sender];
    bool registeredBefore = ghostHrAssetRegistered[a];
    mathint decimalsBefore = ghostHrAssetDecimals8[a];

    f(e, args);

    bool registeredAfter = ghostHrAssetRegistered[a];
    mathint decimalsAfter = ghostHrAssetDecimals8[a];

    assert((registeredAfter != registeredBefore || decimalsAfter != decimalsBefore)
        => senderWardBefore == 1,
        "a stranger never lists an asset or edits its decimals");
}

// HR-AC-03: only an admin can create a pool or change its currency.
rule acHrPoolCurrencyMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint senderWardBefore = _HubRegistry.wards[e.msg.sender];
    mathint currencyBefore = ghostHrCurrency128;

    f(e, args);

    mathint currencyAfter = ghostHrCurrency128;

    assert(currencyAfter != currencyBefore => senderWardBefore == 1,
        "only a ward can set or change the pool's currency");
}

// HR-AC-04: only an admin can grant or revoke pool manager rights.
rule acHrManagerRightsMoveOnlyForAWard(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint senderWardBefore = _HubRegistry.wards[e.msg.sender];
    bool managerBefore = ghostHrManager[who];

    f(e, args);

    bool managerAfter = ghostHrManager[who];

    assert(managerAfter != managerBefore => senderWardBefore == 1, "a stranger never adds or removes a pool manager");
}

// HR-AC-05: only an admin can set a pool's policy.
rule acHrPolicyRowMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint senderWardBefore = _HubRegistry.wards[e.msg.sender];
    address policyBefore = ghostHrPolicy;
    mathint nonceBefore = ghostHrPolicyNonce64;

    f(e, args);

    address policyAfter = ghostHrPolicy;
    mathint nonceAfter = ghostHrPolicyNonce64;

    assert((policyAfter != policyBefore || nonceAfter != nonceBefore)
        => senderWardBefore == 1,
        "only a ward can change the pool's policy or its nonce");
}

// HR-AC-06: only an admin can set a pool's bridging hook.
rule acHrBridgingHookMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint senderWardBefore = _HubRegistry.wards[e.msg.sender];
    address hookBefore = ghostHrBridgingHook;

    f(e, args);

    address hookAfter = ghostHrBridgingHook;

    assert(hookAfter != hookBefore => senderWardBefore == 1, "a stranger never changes a pool's bridging hook");
}

// HR-AC-07: only an admin can set a pool's request manager for a network.
rule acHrRequestManagerMovesOnlyForAWard(env e, method f, calldataarg args, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint senderWardBefore = _HubRegistry.wards[e.msg.sender];
    address managerBefore = ghostHrHubRequestManager[cid];

    f(e, args);

    address managerAfter = ghostHrHubRequestManager[cid];

    assert(managerAfter != managerBefore => senderWardBefore == 1,
        "only a ward can repoint a network's request manager");
}

// HR-AC-08: only an admin can schedule a time-locked authorization.
rule acHrAuthorizationIsScheduledOnlyByAWard(env e, method f, calldataarg args, bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint senderWardBefore = _HubRegistry.wards[e.msg.sender];
    mathint pendingBefore = ghostHrAuthorizedAfter48[id];

    f(e, args);

    mathint pendingAfter = ghostHrAuthorizedAfter48[id];

    assert(pendingBefore == 0 && pendingAfter != 0 => senderWardBefore == 1,
        "only a ward can put an authorization on the timelock");
}

// HR-AC-09: only an admin or the pool's policy can change a pending authorization.
rule acHrPendingAuthorizationMovesOnlyForAWardOrThePolicy(env e, method f, calldataarg args, bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint senderWardBefore = _HubRegistry.wards[e.msg.sender];
    address policyBefore = ghostHrPolicy;
    mathint pendingBefore = ghostHrAuthorizedAfter48[id];

    f(e, args);

    mathint pendingAfter = ghostHrAuthorizedAfter48[id];

    assert(pendingAfter != pendingBefore
        => (senderWardBefore == 1 || e.msg.sender == policyBefore),
        "only a ward or the installed policy can move an authorization");
}
