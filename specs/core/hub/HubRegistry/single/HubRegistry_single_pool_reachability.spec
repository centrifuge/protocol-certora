import "HubRegistry_single_pool_valid_state.spec";

// HR-RC-01: a new asset can be registered with its own decimals.
rule rcHrRegisterAssetIsReachable(env e, HubRegistry.AssetId assetId, uint8 decimals_) {
    setupHubRegistryValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];

    _HubRegistry.registerAsset(e, assetId, decimals_);

    bool registeredAfter = ghostHrAssetRegistered[assetId];
    mathint decimalsAfter = ghostHrAssetDecimals8[assetId];

    satisfy(!registeredBefore && registeredAfter && decimalsAfter == decimals_ && decimalsAfter > 0,
        "an asset can join the registry with nonzero decimals of its choosing");
}

// HR-RC-02: an asset can be registered with the maximum of 18 decimals.
rule rcHrRegisterAssetAtThePrecisionCapIsReachable(env e, HubRegistry.AssetId assetId) {
    setupHubRegistryValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];

    _HubRegistry.registerAsset(e, assetId, 18);

    bool registeredAfter = ghostHrAssetRegistered[assetId];
    mathint decimalsAfter = ghostHrAssetDecimals8[assetId];

    satisfy(!registeredBefore && registeredAfter && decimalsAfter == MAX_DECIMALS_CVL(),
        "a new asset can be registered at exactly the 18-decimal cap");
}

// HR-RC-03: an asset can be registered with zero decimals.
rule rcHrRegisterAssetWithZeroPrecisionIsReachable(env e, HubRegistry.AssetId assetId) {
    setupHubRegistryValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];

    _HubRegistry.registerAsset(e, assetId, 0);

    bool registeredAfter = ghostHrAssetRegistered[assetId];
    mathint decimalsAfter = ghostHrAssetDecimals8[assetId];

    satisfy(!registeredBefore && registeredAfter && decimalsAfter == 0, "a decimal-less asset can be registered");
}

// HR-RC-04: a pool can be created with its currency and first manager.
rule rcHrRegisterPoolIsReachable(env e, HubRegistry.PoolId poolId_, address manager_,
    HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);

    mathint currencyBefore = ghostHrCurrency128;
    bool seatBefore = ghostHrManager[manager_];

    _HubRegistry.registerPool(e, poolId_, manager_, currency_);

    mathint currencyAfter = ghostHrCurrency128;
    bool seatAfter = ghostHrManager[manager_];

    satisfy(currencyBefore == 0 && !seatBefore && currencyAfter == currency_
        && currencyAfter != 0 && seatAfter,
        "a fresh pool can get a nonzero currency and a manager seat");
}

// HR-RC-05: an asset and a pool in that currency can be set up from an empty registry.
rule rcHrRegisterAssetThenRegisterPoolIsReachable(env e, HubRegistry.PoolId poolId_, address manager_,
    HubRegistry.AssetId currency_, uint8 decimals_) {

    setupHubRegistryValidState(e);

    require(forall mathint x. !ghostHrAssetRegistered[x], "SCOPE: no asset registered yet");

    _HubRegistry.registerAsset(e, currency_, decimals_);
    _HubRegistry.registerPool(e, poolId_, manager_, currency_);

    bool currencyRegisteredAfter = ghostHrAssetRegistered[currency_];
    mathint currencyAfter = ghostHrCurrency128;
    bool seatAfter = ghostHrManager[manager_];

    satisfy(currencyRegisteredAfter && currencyAfter == currency_ && seatAfter,
        "an asset and a pool in it can be set up from empty in one transaction");
}

// HR-RC-06: a new manager can be added to an existing pool.
rule rcHrUpdateManagerSeatsAManagerIsReachable(env e, HubRegistry.PoolId poolId_, address who) {
    setupHubRegistryValidState(e);

    bool seatBefore = ghostHrManager[who];

    _HubRegistry.updateManager(e, poolId_, who, true);

    bool seatAfter = ghostHrManager[who];

    satisfy(!seatBefore && seatAfter, "an account without a seat can be made a manager");
}

// HR-RC-07: a pool manager can have its rights revoked.
rule rcHrUpdateManagerRevokesASeatIsReachable(env e, HubRegistry.PoolId poolId_, address who) {
    setupHubRegistryValidState(e);

    bool seatBefore = ghostHrManager[who];

    _HubRegistry.updateManager(e, poolId_, who, false);

    bool seatAfter = ghostHrManager[who];

    satisfy(seatBefore && !seatAfter, "a manager can be removed from a pool");
}

// HR-RC-08: an existing pool can switch to another currency with the same decimals.
rule rcHrUpdateCurrencyRedenominatesThePoolIsReachable(env e, HubRegistry.PoolId poolId_,
    HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);

    mathint currencyBefore = ghostHrCurrency128;

    _HubRegistry.updateCurrency(e, poolId_, currency_);

    mathint currencyAfter = ghostHrCurrency128;

    satisfy(currencyBefore != 0 && currencyAfter == currency_ && currencyAfter != currencyBefore,
        "a live pool can be moved to a different currency");
}

// HR-RC-09: a bridging hook can be set on a pool that had none.
rule rcHrSetBridgingHookAttachesIsReachable(env e, HubRegistry.PoolId poolId_, address hook_) {
    setupHubRegistryValidState(e);

    address hookBefore = ghostHrBridgingHook;

    _HubRegistry.setBridgingHook(e, poolId_, hook_);

    address hookAfter = ghostHrBridgingHook;

    satisfy(hookBefore == 0 && hookAfter == hook_ && hookAfter != 0, "a hookless pool can get a bridging hook");
}

// HR-RC-10: a pool's bridging hook can be removed.
rule rcHrSetBridgingHookDetachesIsReachable(env e, HubRegistry.PoolId poolId_) {
    setupHubRegistryValidState(e);

    address noHook = 0;
    address hookBefore = ghostHrBridgingHook;

    _HubRegistry.setBridgingHook(e, poolId_, noHook);

    address hookAfter = ghostHrBridgingHook;

    satisfy(hookBefore != 0 && hookAfter == 0, "a pool with a bridging hook can go back to none");
}

// HR-RC-11: an admin can set a pool's request manager for a network that had none.
rule rcHrSetHubRequestManagerWiresANetworkIsReachable(env e, HubRegistry.PoolId poolId_, uint16 centrifugeId_,
    address manager_) {

    setupHubRegistryValidState(e);

    address wiredBefore = ghostHrHubRequestManager[centrifugeId_];

    _HubRegistry.setHubRequestManager(e, poolId_, centrifugeId_, manager_);

    address wiredAfter = ghostHrHubRequestManager[centrifugeId_];

    satisfy(wiredBefore == 0 && wiredAfter == manager_ && wiredAfter != 0,
        "a request manager can be set for a network that had none");
}

// HR-RC-12: a pool with no policy yet can have its first one installed.
rule rcHrSetPolicyInstallsTheFirstPolicyIsReachable(env e, HubRegistry.PoolId poolId_, address policy_) {
    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    mathint nonceBefore = ghostHrPolicyNonce64;

    _HubRegistry.setPolicy(e, poolId_, policy_);

    address policyAfter = ghostHrPolicy;
    mathint nonceAfter = ghostHrPolicyNonce64;

    satisfy(policyBefore == 0 && nonceBefore == 0 && policyAfter == policy_ && policyAfter != 0 && nonceAfter == 1,
        "a first policy can be installed on a pool, its nonce becoming one");
}

// HR-RC-13: an installed policy can be removed, which also voids pending authorizations.
rule rcHrSetPolicyUninstallsWithTheZeroAddressIsReachable(env e, HubRegistry.PoolId poolId_) {
    setupHubRegistryValidState(e);

    address noPolicy = 0;
    address policyBefore = ghostHrPolicy;
    mathint nonceBefore = ghostHrPolicyNonce64;

    _HubRegistry.setPolicy(e, poolId_, noPolicy);

    address policyAfter = ghostHrPolicy;
    mathint nonceAfter = ghostHrPolicyNonce64;

    satisfy(policyBefore != 0 && policyAfter == 0 && nonceAfter == nonceBefore + 1,
        "a policy can be removed, and the policy nonce still advances by one");
}

// HR-RC-14: a pool can still make its last allowed policy change.
rule rcHrSetPolicyAtTheLastNamespaceIsReachable(env e, HubRegistry.PoolId poolId_, address policy_) {
    setupHubRegistryValidState(e);

    require(ghostHrPolicyNonce64 == max_uint64 - 1, "SCOPE: the policy nonce is one below its maximum");

    _HubRegistry.setPolicy(e, poolId_, policy_);

    address policyAfter = ghostHrPolicy;
    mathint nonceAfter = ghostHrPolicyNonce64;

    satisfy(policyAfter == policy_ && nonceAfter == max_uint64, "a policy install can reach the maximum policy nonce");
}

// HR-RC-15: a policy change lets the same call be scheduled again under the new policy.
rule rcHrOrphanedScheduleCanBeRemadeAfterAPolicySwapIsReachable(env e, HubRegistry.PoolId poolId_, address caller,
    bytes data, address newPolicy) {

    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    bytes32 dataHash = keccak256(data);

    require(newPolicy != policyBefore, "SCOPE: the swap installs a different policy");

    _HubRegistry.initiateAuthorization(e, poolId_, caller, data);
    _HubRegistry.setPolicy(e, poolId_, newPolicy);
    _HubRegistry.initiateAuthorization(e, poolId_, caller, data);

    mathint orphanedGrant = PENDING_HR(policyBefore, nonceBefore, dataHash);
    mathint freshGrant = PENDING_HR(ghostHrPolicy, ghostHrPolicyNonce64, dataHash);

    satisfy(orphanedGrant != 0 && freshGrant != 0 && ghostHrPolicy == newPolicy,
        "a policy swap lets a call be rescheduled, its old grant left orphaned");
}

// HR-RC-16: an authorization can mature at the latest time the registry can record.
rule rcHrInitiateAuthorizationAtTheMaturityCeilingIsReachable(env e, HubRegistry.PoolId poolId_, address caller,
    bytes data) {

    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    bytes32 dataHash = keccak256(data);
    mathint pendingBefore = PENDING_HR(policyBefore, nonceBefore, dataHash);

    _HubRegistry.initiateAuthorization(e, poolId_, caller, data);

    mathint pendingAfter = PENDING_HR(policyBefore, nonceBefore, dataHash);

    satisfy(pendingBefore == 0 && pendingAfter == max_uint48,
        "a scheduled call can mature at the latest time its stamp can hold");
}

// HR-RC-17: a pending authorization can be canceled before it matures.
rule rcHrCancelAuthorizationIsReachable(env e, HubRegistry.PoolId poolId_, address caller, bytes data) {
    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    bytes32 dataHash = keccak256(data);
    mathint pendingBefore = PENDING_HR(policyBefore, nonceBefore, dataHash);

    _HubRegistry.cancelAuthorization(e, poolId_, caller, data);

    mathint pendingAfter = PENDING_HR(policyBefore, nonceBefore, dataHash);

    satisfy(pendingBefore > e.block.timestamp && pendingAfter == 0,
        "a scheduled grant can be withdrawn while still pending");
}

// HR-RC-18: an authorization can be consumed at the exact moment it matures.
rule rcHrConsumeAuthorizationAtTheMaturityInstantIsReachable(env e, HubRegistry.PoolId poolId_, address caller,
    bytes data, uint48 expiry) {

    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    bytes32 dataHash = keccak256(data);
    mathint pendingBefore = PENDING_HR(policyBefore, nonceBefore, dataHash);

    _HubRegistry.consumeAuthorization(e, poolId_, caller, data, expiry);

    mathint pendingAfter = PENDING_HR(policyBefore, nonceBefore, dataHash);

    satisfy(pendingBefore != 0 && pendingAfter == 0 && e.block.timestamp == pendingBefore,
        "a grant maturing this very block can be used right away");
}

// HR-RC-19: an authorization can be consumed at the last second of its expiry window.
rule rcHrConsumeAuthorizationAtTheExpiryEdgeIsReachable(env e, HubRegistry.PoolId poolId_, address caller,
    bytes data, uint48 expiry) {

    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    bytes32 dataHash = keccak256(data);
    mathint pendingBefore = PENDING_HR(policyBefore, nonceBefore, dataHash);

    _HubRegistry.consumeAuthorization(e, poolId_, caller, data, expiry);

    mathint pendingAfter = PENDING_HR(policyBefore, nonceBefore, dataHash);

    satisfy(pendingBefore != 0 && pendingAfter == 0 && expiry > 0
        && e.block.timestamp == pendingBefore + expiry,
        "a grant can be consumed on the last instant of a nonzero expiry window");
}

// HR-RC-20: admin rights can be granted and revoked again in one transaction.
rule rcHrAuthorityRoundTripIsReachable(env e, address user) {
    setupHubRegistryValidState(e);

    uint256 wardBefore = _HubRegistry.wards(e, user);

    _HubRegistry.rely(e, user);

    uint256 wardGranted = _HubRegistry.wards(e, user);

    _HubRegistry.deny(e, user);

    uint256 wardAfter = _HubRegistry.wards(e, user);

    satisfy(wardBefore == 0 && wardGranted == 1 && wardAfter == 0,
        "an account can become a ward and lose it within one transaction");
}

// HR-RC-21: a new policy can be installed on a pool, advancing its policy nonce by one.
rule rcHrPolicyViewsReportTheInstallIsReachable(env e, HubRegistry.PoolId poolId_, address policy_) {
    setupHubRegistryValidState(e);

    address policyBefore = _HubRegistry.policy(e, poolId_);
    require(policy_ != 0 && policy_ != e.msg.sender && policy_ != policyBefore,
        "SCOPE: a new policy, neither the caller nor the sitting one");

    uint64 nonceBefore = _HubRegistry.policyNonce(e, poolId_);

    _HubRegistry.setPolicy(e, poolId_, policy_);

    address policyAfter = _HubRegistry.policy(e, poolId_);
    uint64 nonceAfter = _HubRegistry.policyNonce(e, poolId_);

    satisfy(policyAfter == policy_ && policyAfter != 0
        && nonceAfter == nonceBefore + 1,
        "the policy views can show a new policy and a nonce one higher");
}

// HR-RC-22: a policy change can give an unchanged call a new authorization id.
rule rcHrAuthIdChangesAcrossAPolicySwapIsReachable(env e, HubRegistry.PoolId poolId_, bytes data,
    address newPolicy) {

    setupHubRegistryValidState(e);

    bytes32 idBefore = _HubRegistry.authId(e, poolId_, data);

    _HubRegistry.setPolicy(e, poolId_, newPolicy);

    bytes32 idAfter = _HubRegistry.authId(e, poolId_, data);

    satisfy(idAfter != idBefore, "swapping the policy can re-key an unchanged payload");
}

// HR-RC-23: an admin can create a pool and then remove its only manager.
rule rcHrLivePoolLosesItsOnlyManagerIsReachable(env e, HubRegistry.PoolId poolId_, address manager_,
    HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);

    _HubRegistry.registerPool(e, poolId_, manager_, currency_);

    bool seatOpened = ghostHrManager[manager_];

    _HubRegistry.updateManager(e, poolId_, manager_, false);

    satisfy(seatOpened && ghostHrCurrency128 != 0 && !ghostHrManager[manager_],
        "a pool can stay live after losing its only manager");
}

// HR-RC-24: an asset registered with zero decimals can later get nonzero decimals.
rule rcHrRegisterAssetFillsAnUnsetPrecisionIsReachable(env e, HubRegistry.AssetId assetId, uint8 decimals_) {
    setupHubRegistryValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];
    mathint decimalsBefore = ghostHrAssetDecimals8[assetId];

    _HubRegistry.registerAsset(e, assetId, decimals_);

    satisfy(registeredBefore && decimalsBefore == 0 && decimals_ > 0
        && ghostHrAssetDecimals8[assetId] == decimals_,
        "an asset with zero decimals can be re-registered with nonzero decimals");
}

// HR-RC-25: an asset can be registered again with the same nonzero decimals.
rule rcHrRegisterAssetRepeatsAtItsOwnPrecisionIsReachable(env e, HubRegistry.AssetId assetId, uint8 decimals_) {
    setupHubRegistryValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];
    mathint decimalsBefore = ghostHrAssetDecimals8[assetId];

    _HubRegistry.registerAsset(e, assetId, decimals_);

    satisfy(registeredBefore && decimalsBefore != 0 && decimalsBefore == decimals_
        && ghostHrAssetDecimals8[assetId] == decimalsBefore,
        "an asset can be re-registered with its same nonzero decimals");
}
