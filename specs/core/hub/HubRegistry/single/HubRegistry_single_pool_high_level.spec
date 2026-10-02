// HubRegistry, single-pool lane. High level: auth hatch, writer fences, answer precision.

import "HubRegistry_single_pool_valid_state.spec";

// HR-HL-01: an authorization can be consumed at most once.
rule hlHrAuthorizationIsSpentOnlyOnce(env e1, env e2, HubRegistry.PoolId poolId_, address caller1,
    address caller2, bytes data1, bytes data2, uint48 expiry1, uint48 expiry2) {

    setupHubRegistryValidState(e1);
    setupHubRegistryValidState(e2);

    bytes32 hashFirst = keccak256(data1);
    bytes32 hashSecond = keccak256(data2);

    _HubRegistry.consumeAuthorization(e1, poolId_, caller1, data1, expiry1);
    _HubRegistry.consumeAuthorization(e2, poolId_, caller2, data2, expiry2);

    assert(hashSecond != hashFirst, "two consumptions in a row never carry the same payload");
}

// HR-HL-02: consuming succeeds only for an authorization that is actually scheduled.
rule hlHrConsumeSpendsOnlyALiveEntry(env e, HubRegistry.PoolId poolId_, address caller, bytes data,
    uint48 expiry) {

    setupHubRegistryValidState(e);

    bytes32 dataHash = keccak256(data);
    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    mathint pendingBefore = PENDING_HR(policyBefore, nonceBefore, dataHash);

    _HubRegistry.consumeAuthorization(e, poolId_, caller, data, expiry);

    assert(pendingBefore != 0, "a consumption succeeds only on a pending authorization");
}

// HR-HL-03: an authorization cannot be consumed before its delay has passed.
rule hlHrConsumeWaitsOutTheVetoDelay(env e, HubRegistry.PoolId poolId_, address caller, bytes data,
    uint48 expiry) {

    setupHubRegistryValidState(e);

    bytes32 dataHash = keccak256(data);
    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    mathint pendingBefore = PENDING_HR(policyBefore, nonceBefore, dataHash);

    _HubRegistry.consumeAuthorization(e, poolId_, caller, data, expiry);

    assert(e.block.timestamp >= pendingBefore, "a consumption never fires before the authorization matures");
}

// HR-HL-04: an authorization cannot be consumed after its expiry window closes.
rule hlHrConsumeRefusesAStaleGrant(env e, HubRegistry.PoolId poolId_, address caller, bytes data,
    uint48 expiry) {

    setupHubRegistryValidState(e);

    bytes32 dataHash = keccak256(data);
    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    mathint pendingBefore = PENDING_HR(policyBefore, nonceBefore, dataHash);

    _HubRegistry.consumeAuthorization(e, poolId_, caller, data, expiry);

    assert(e.block.timestamp <= pendingBefore + expiry,
        "an authorization is consumed no later than its expiry after maturity");
}

// HR-HL-05: a canceled authorization cannot then be consumed.
rule hlHrCanceledAuthorizationNeverFires(env e1, env e2, HubRegistry.PoolId poolId_, address caller1,
    address caller2, bytes dataCanceled, bytes dataConsumed, uint48 expiry) {

    setupHubRegistryValidState(e1);
    setupHubRegistryValidState(e2);

    bytes32 hashCanceled = keccak256(dataCanceled);
    bytes32 hashConsumed = keccak256(dataConsumed);

    _HubRegistry.cancelAuthorization(e1, poolId_, caller1, dataCanceled);
    _HubRegistry.consumeAuthorization(e2, poolId_, caller2, dataConsumed, expiry);

    assert(hashConsumed != hashCanceled, "a consumption right after a cancel is never for the cancelled payload");
}

// HR-HL-06: an authorization matures after exactly the delay the pool's policy sets.
rule hlHrScheduledCallMaturesAfterExactlyThePolicyDelay(env e, HubRegistry.PoolId poolId_, address caller, bytes data) {

    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    uint64 nonceBefore = ghostHrPolicyNonce64;
    bytes32 dataHash = keccak256(data);
    mathint delayBefore = ghostPolicyDelay48[caller][dataHash];

    _HubRegistry.initiateAuthorization(e, poolId_, caller, data);

    mathint pendingAfter = PENDING_HR(policyBefore, nonceBefore, dataHash);

    assert(pendingAfter == e.block.timestamp + delayBefore,
        "a scheduled call matures exactly its policy delay from now");
}

// HR-HL-07: creating a pool makes the named account its manager.
rule hlHrPoolCreationSeatsTheAccountItNames(env e, HubRegistry.PoolId poolId_, address manager_,
    HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);

    _HubRegistry.registerPool(e, poolId_, manager_, currency_);

    assert(ghostHrManager[manager_], "the new pool's manager list includes the account passed in");
}

// HR-HL-08: the registry reports an asset's decimals as recorded at registration.
rule hlHrTokenPrecisionMatchesTheAssetRow(env e, uint256 asset_) {

    setupHubRegistryValidState(e);

    mathint assetRaw = asset_;
    mathint recordedBefore = ghostHrAssetDecimals8[assetRaw];

    uint8 answered = _HubRegistry.decimals(e, asset_);

    assert(answered == recordedBefore, "the token precision read returns the recorded asset decimals");
}

// HR-HL-09: setting a policy installs it and voids pending authorizations, even if unchanged.
rule hlHrSetPolicyInstallsExactlyTheAddressItNames(env e, HubRegistry.PoolId poolId_, address policy_) {

    setupHubRegistryValidState(e);

    mathint nonceBefore = ghostHrPolicyNonce64;

    _HubRegistry.setPolicy(e, poolId_, policy_);

    assert(ghostHrPolicy == policy_ && ghostHrPolicyNonce64 == nonceBefore + 1,
        "setting a policy, even a repeat, installs it and adds one to its nonce");
}

// HR-HL-10: registering an asset records it with exactly the precision the call names.
rule hlHrAssetRegistrationRecordsThePrecisionItNames(env e, HubRegistry.AssetId assetId, uint8 decimals_) {

    setupHubRegistryValidState(e);

    _HubRegistry.registerAsset(e, assetId, decimals_);

    assert(ghostHrAssetRegistered[assetId] && ghostHrAssetDecimals8[assetId] == decimals_,
        "the asset is registered with the decimals given");
}

// HR-HL-11: creating a pool records the currency it names and makes the named manager its only manager.
rule hlHrPoolCreationRecordsTheCurrencyAndSoleManagerItNames(env e, HubRegistry.PoolId poolId_, address manager_,
    HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);

    _HubRegistry.registerPool(e, poolId_, manager_, currency_);

    assert(ghostHrCurrency128 == currency_ && ghostHrManager[manager_]
        && (forall address w. w != manager_ => !ghostHrManager[w]),
        "the new pool has the given currency and the given manager alone");
}

// HR-HL-12: removing the only manager of a newly created pool leaves the pool live with no manager.
rule hlHrRevokingTheOnlySeatLeavesALivePoolWithNoManager(env e, HubRegistry.PoolId poolId_, address manager_,
    HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);

    _HubRegistry.registerPool(e, poolId_, manager_, currency_);
    _HubRegistry.updateManager(e, poolId_, manager_, false);

    assert(ghostHrCurrency128 != 0 && (forall address w. !ghostHrManager[w]),
        "the pool stays registered with no manager left");
}

// HR-HL-14: a pool id is the network id above the local id, distinct per pair and nonzero on a nonzero network.
rule hlHrPoolIdIsTheChainOverTheLocalId(env e, uint16 c1, uint48 l1, uint16 c2, uint48 l2) {

    setupHubRegistryValidState(e);

    HubRegistry.PoolId p1 = _HubRegistry.poolId(e, c1, l1);
    HubRegistry.PoolId p2 = _HubRegistry.poolId(e, c2, l2);

    assert(p1 == c1 * 2^48 + l1
        && (p1 == p2 => (c1 == c2 && l1 == l2))
        && (c1 != 0 => p1 != 0),
        "network above local id, one id per pair, nonzero off network 0");
}

// HR-HL-16: creating a pool installs no policy and leaves its policy nonce at zero.
rule hlHrPoolCreationLeavesThePoolWithoutAPolicy(env e, HubRegistry.PoolId poolId_, address manager_,
    HubRegistry.AssetId currency_) {

    setupHubRegistryValidState(e);

    mathint nonceBefore = ghostHrPolicyNonce64;

    _HubRegistry.registerPool(e, poolId_, manager_, currency_);

    assert(ghostHrPolicy == 0 && ghostHrPolicyNonce64 == nonceBefore && nonceBefore == 0,
        "a new pool has no policy and its policy nonce stays at zero");
}
