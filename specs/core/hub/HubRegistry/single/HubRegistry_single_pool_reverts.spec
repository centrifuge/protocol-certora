import "HubRegistry_single_pool_valid_state.spec";

// CVL cannot tell decimals(AssetId)/decimals(PoolId) from decimals(uint256), so this harness names them.
using HubRegistryDecimalsHarness as _HubRegistryDecimals;

// HR-RV-01: pool registration fails for a non-admin, no manager, an unregistered currency, or a repeat.
rule rvHrRegisterPoolRefusesAnUnusableOrRepeatedOpening(env e, HubRegistry.PoolId poolId_,
    address manager_, HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    bool currencyRegisteredBefore = ghostHrAssetRegistered[currency_];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _HubRegistry.registerPool@withrevert(e, poolId_, manager_, currency_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || manager_ == 0 || !currencyRegisteredBefore || poolCurrencyBefore != 0)
        => reverted,
        "opening a pool fails for a non-ward, no manager, an unknown currency or a repeat");
}

// HR-RV-02: a manager update fails for a non-admin, a nonexistent pool, or the zero address.
rule rvHrUpdateManagerRefusesANonWardAnAbsentPoolOrANullSeat(env e, HubRegistry.PoolId poolId_,
    address who, bool canManage) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _HubRegistry.updateManager@withrevert(e, poolId_, who, canManage);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || poolCurrencyBefore == 0 || who == 0) => reverted,
        "a manager change fails for a non-ward, no pool or a null account");
}

// HR-RV-03: a currency change fails for a non-admin, missing pool, unregistered asset or different decimals.
rule rvHrUpdateCurrencyRefusesANonWardAnAbsentPoolOrARescaling(env e, HubRegistry.PoolId poolId_,
    HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint currencyRaw = currency_;
    bool currencyRegisteredBefore = ghostHrAssetRegistered[currencyRaw];
    mathint poolCurrencyBefore = ghostHrCurrency128;
    mathint incomingDecimalsBefore = ghostHrAssetDecimals8[currencyRaw];
    mathint sittingDecimalsBefore = ghostHrAssetDecimals8[poolCurrencyBefore];

    _HubRegistry.updateCurrency@withrevert(e, poolId_, currency_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || poolCurrencyBefore == 0 || !currencyRegisteredBefore
            || incomingDecimalsBefore != sittingDecimalsBefore) => reverted,
        "a currency change fails for a non-ward, no pool, an unknown currency or new decimals");
}

// HR-RV-04: installing a policy fails for a non-admin or on a nonexistent pool.
rule rvHrSetPolicyRefusesANonWardOrAnAbsentPool(env e, HubRegistry.PoolId poolId_, address policy_) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _HubRegistry.setPolicy@withrevert(e, poolId_, policy_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || poolCurrencyBefore == 0) => reverted,
        "a stranger or a missing pool makes policy installation revert");
}

// HR-RV-05: setting a hub request manager fails for a non-admin or on a nonexistent pool.
rule rvHrSetHubRequestManagerRefusesANonWardOrAnAbsentPool(env e, HubRegistry.PoolId poolId_,
    uint16 centrifugeId, address manager_) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _HubRegistry.setHubRequestManager@withrevert(e, poolId_, centrifugeId, manager_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || poolCurrencyBefore == 0) => reverted,
        "a stranger or a missing pool makes setting a request manager revert");
}

// HR-RV-06: an admin can always set or clear an existing pool's bridging hook.
rule rvHrSetBridgingHookIsNeverRefusedToAWardOnALivePool(env e, HubRegistry.PoolId poolId_, address hook_) {

    setupHubRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _HubRegistry.setBridgingHook@withrevert(e, poolId_, hook_);
    bool reverted = lastReverted;

    assert((wardBitBefore == 1 && poolCurrencyBefore != 0) => !reverted,
        "a ward can always set a live pool's bridging hook, zero included");
}

// HR-RV-07: scheduling a call fails for a non-admin, no policy, a call with no delay, or one already pending.
rule rvHrInitiateAuthorizationRefusesANonWardAnInPolicyCallOrATakenSlot(env e, HubRegistry.PoolId poolId_,
    address caller, bytes data) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    bytes32 dataHash = keccak256(data);
    mathint delayBefore = ghostPolicyDelay48[caller][dataHash];
    mathint pendingBefore = ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][policyBefore][nonceBefore][dataHash]];

    _HubRegistry.initiateAuthorization@withrevert(e, poolId_, caller, data);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || policyBefore == 0 || delayBefore == 0 || pendingBefore != 0) => reverted,
        "scheduling fails for a non-ward, no policy, an in-policy call or a pending grant");
}

// HR-RV-08: cancelling an authorization fails for a non-admin or when none is pending.
rule rvHrCancelAuthorizationRefusesANonWardOrAnEmptySlot(env e, HubRegistry.PoolId poolId_,
    address caller, bytes data) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    bytes32 dataHash = keccak256(data);
    mathint pendingBefore =
        ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][ghostHrPolicy][ghostHrPolicyNonce64][dataHash]];

    _HubRegistry.cancelAuthorization@withrevert(e, poolId_, caller, data);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || pendingBefore == 0) => reverted,
        "a stranger, or no grant pending for that call, makes a cancel revert");
}

// HR-RV-09: the pool's policy can always consume a matured authorization until it expires.
rule rvHrConsumeAuthorizationIsNeverRefusedToThePolicyInsideItsWindow(env e, HubRegistry.PoolId poolId_,
    address caller, bytes data, uint48 expiry) {

    setupHubRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    address policyBefore = ghostHrPolicy;
    address senderBefore = e.msg.sender;
    bytes32 dataHash = keccak256(data);
    mathint maturityBefore =
        ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][policyBefore][ghostHrPolicyNonce64][dataHash]];
    mathint now = e.block.timestamp;
    mathint windowEnd = maturityBefore + expiry;

    _HubRegistry.consumeAuthorization@withrevert(e, poolId_, caller, data, expiry);
    bool reverted = lastReverted;

    assert((senderBefore == policyBefore && maturityBefore != 0 && now >= maturityBefore
            && now <= windowEnd) => !reverted,
        "the pool's policy can always consume a pending grant inside its window");
}

// HR-RV-10: reading an unregistered asset's decimals fails rather than returning zero.
rule rvHrTokenDecimalsRefusesAnAssetTheRegistryDoesNotCarry(env e, uint256 asset_) {

    setupHubRegistryValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[asset_];

    _HubRegistry.decimals@withrevert(e, asset_);
    bool reverted = lastReverted;

    assert(!registeredBefore => reverted, "reading the decimals of an unregistered asset fails");
}

// HR-RV-11: computing an authorization id never fails, even for a pool without a policy.
rule rvHrAuthIdAlwaysAnswers(env e, HubRegistry.PoolId poolId_, bytes data) {

    setupHubRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    _HubRegistry.authId@withrevert(e, poolId_, data);
    bool reverted = lastReverted;

    assert(!reverted, "the authorization id can always be computed");
}

// HR-RV-12: a policy install voids earlier authorizations, even when it reinstalls the same policy.
rule rvHrRetiredGrantIsNeverConsumed(env e, env ePolicy, HubRegistry.PoolId poolId_, address caller,
    bytes data, address policyNew, uint48 expiry) {

    setupHubRegistryValidState(e);
    setupHubRegistryValidState(ePolicy);

    _HubRegistry.initiateAuthorization(e, poolId_, caller, data);
    _HubRegistry.setPolicy(e, poolId_, policyNew);

    _HubRegistry.consumeAuthorization@withrevert(ePolicy, poolId_, caller, data, expiry);
    bool reverted = lastReverted;

    assert(reverted, "right after a policy install, an earlier grant cannot be consumed");
}

// HR-RV-13: granting admin rights fails for a non-admin caller.
rule rvHrRelyRefusesANonWard(env e, address user) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];

    _HubRegistry.rely@withrevert(e, user);
    bool reverted = lastReverted;

    assert(wardBitBefore != 1 => reverted, "a non-ward cannot grant ward rights");
}

// HR-RV-14: revoking admin rights fails for a non-admin caller.
rule rvHrDenyRefusesANonWard(env e, address user) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];

    _HubRegistry.deny@withrevert(e, user);
    bool reverted = lastReverted;

    assert(wardBitBefore != 1 => reverted, "a non-ward cannot revoke ward rights");
}

// HR-RV-15: an admin can always register a new, non-empty asset id with up to 18 decimals.
rule rvHrRegisterAssetIsNeverRefusedToAWardOnAFreshAssetWithinTheCap(env e, HubRegistry.AssetId assetId,
    uint8 decimals_) {

    setupHubRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");
    require(assetId != 0, "SCOPE: a nonzero asset id, HR-VS-03 covers the null one");

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint declaredDecimals = decimals_;
    bool registeredBefore = ghostHrAssetRegistered[assetId];

    _HubRegistry.registerAsset@withrevert(e, assetId, decimals_);
    bool reverted = lastReverted;

    assert((wardBitBefore == 1 && !registeredBefore && declaredDecimals <= MAX_DECIMALS_CVL())
        => !reverted,
        "a ward's fresh asset of up to 18 decimals always registers");
}

// HR-RV-16: consuming an authorization fails for every caller but the pool's policy, admins included.
rule rvHrConsumeAuthorizationRefusesEveryCallerButTheInstalledPolicy(env e, HubRegistry.PoolId poolId_,
    address caller, bytes data, uint48 expiry) {

    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;

    _HubRegistry.consumeAuthorization@withrevert(e, poolId_, caller, data, expiry);
    bool reverted = lastReverted;

    assert(e.msg.sender != policyBefore => reverted, "only the pool's policy can consume an authorization");
}

// HR-RV-17: an admin never fails to register a new pool of a nonzero network with a manager and known currency.
rule rvHrRegisterPoolAdmitsAUsableOpeningOfAChainedPool(env e, uint16 centrifugeId, uint48 localId,
    address manager_, HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    HubRegistry.PoolId poolId_ = _HubRegistry.poolId(e, centrifugeId, localId);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    bool currencyRegisteredBefore = ghostHrAssetRegistered[currency_];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _HubRegistry.registerPool@withrevert(e, poolId_, manager_, currency_);
    bool reverted = lastReverted;

    assert((wardBitBefore == 1 && centrifugeId != 0 && manager_ != 0 && currencyRegisteredBefore
            && poolCurrencyBefore == 0) => !reverted,
        "a ward's new pool with manager and known currency opens off network 0");
}

// HR-RV-18: reading an asset's decimals fails exactly if it is unregistered or ETH is sent, else gives them.
rule rvHrAssetIdPrecisionReadAnswersTheRowOrRefuses(env e, HubRegistry.AssetId assetId) {

    setupHubRegistryValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[assetId];
    mathint recordedBefore = ghostHrAssetDecimals8[assetId];

    uint8 answered = _HubRegistryDecimals.assetDecimals@withrevert(e, assetId);
    bool reverted = lastReverted;

    assert((reverted <=> (!registeredBefore || e.msg.value != 0)) && (!reverted => answered == recordedBefore),
        "fails only for an unknown asset or sent ETH, else returns its decimals");
}

// HR-RV-19: reading a pool's decimals fails exactly for a missing pool or sent ETH, else gives its currency's.
rule rvHrPoolPrecisionReadAnswersItsCurrencyRowOrRefuses(env e, HubRegistry.PoolId poolId_) {

    setupHubRegistryValidState(e);

    mathint poolCurrencyBefore = ghostHrCurrency128;
    mathint recordedBefore = ghostHrAssetDecimals8[poolCurrencyBefore];

    uint8 answered = _HubRegistryDecimals.poolDecimals@withrevert(e, poolId_);
    bool reverted = lastReverted;

    assert((reverted <=> (poolCurrencyBefore == 0 || e.msg.value != 0)) && (!reverted => answered == recordedBefore),
        "fails only for a missing pool or sent ETH, else returns its currency's decimals");
}

// HR-RV-20: asset registration fails for a non-admin, over 18 decimals, or changing nonzero decimals.
rule rvHrRegisterAssetRefusesANonWardAnOversizedPrecisionOrARescale(env e, HubRegistry.AssetId assetId,
    uint8 decimals_) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint declaredDecimals = decimals_;
    bool registeredBefore = ghostHrAssetRegistered[assetId];
    mathint decimalsBefore = ghostHrAssetDecimals8[assetId];

    _HubRegistry.registerAsset@withrevert(e, assetId, decimals_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || declaredDecimals > MAX_DECIMALS_CVL()
            || (registeredBefore && decimalsBefore != 0 && decimalsBefore != declaredDecimals)) => reverted,
        "a stranger, over 18 decimals or changing nonzero decimals makes registration revert");
}

// HR-RV-21: an admin can always re-register an asset with unchanged decimals, or up to 18 if they were zero.
rule rvHrRegisterAssetIsNeverRefusedToAWardFillingOrKeepingARegisteredPrecision(env e,
    HubRegistry.AssetId assetId, uint8 decimals_) {

    setupHubRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint declaredDecimals = decimals_;
    bool registeredBefore = ghostHrAssetRegistered[assetId];
    mathint decimalsBefore = ghostHrAssetDecimals8[assetId];

    _HubRegistry.registerAsset@withrevert(e, assetId, decimals_);
    bool reverted = lastReverted;

    assert((wardBitBefore == 1 && registeredBefore && declaredDecimals <= MAX_DECIMALS_CVL()
            && (decimalsBefore == 0 || decimalsBefore == declaredDecimals)) => !reverted,
        "an admin can always re-register unchanged decimals, or up to 18 if they were zero");
}

// HR-RV-22: an admin can always cancel an authorization pending under the current policy.
rule rvHrCancelAuthorizationIsNeverRefusedToAWardWithAPendingGrant(env e, HubRegistry.PoolId poolId_,
    address caller, bytes data) {

    setupHubRegistryValidState(e);
    require(e.msg.value == 0, "SCOPE: no ether, the entry is not payable");

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint pendingBefore = PENDING_HR(ghostHrPolicy, ghostHrPolicyNonce64, keccak256(data));

    _HubRegistry.cancelAuthorization@withrevert(e, poolId_, caller, data);
    bool reverted = lastReverted;

    assert((wardBitBefore == 1 && pendingBefore != 0) => !reverted,
        "an admin can always cancel an authorization pending under the current policy");
}

// HR-RV-23: setting a bridging hook fails for a non-admin, a pool never created, or sent ETH.
rule rvHrSetBridgingHookRefusesANonWardOrAnAbsentPool(env e, HubRegistry.PoolId poolId_, address hook_) {

    setupHubRegistryValidState(e);

    mathint wardBitBefore = _HubRegistry.wards[e.msg.sender];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _HubRegistry.setBridgingHook@withrevert(e, poolId_, hook_);
    bool reverted = lastReverted;

    assert((wardBitBefore != 1 || poolCurrencyBefore == 0 || e.msg.value != 0) => reverted,
        "a stranger, a missing pool or sent ETH makes setting a bridging hook revert");
}
