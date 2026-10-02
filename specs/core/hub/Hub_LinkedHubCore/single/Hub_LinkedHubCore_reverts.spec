import "Hub_LinkedHubCore_valid_state.spec";

// HU-RV-01: rewiring the hub fails for a non-admin or an unknown dependency name.
rule rvHuFileRefusesANonWardOrAnUnknownName(env e, bytes32 what, address dependency) {

    setupHubLinkedHubCoreValidState(e);

    mathint wardBefore = _Hub.wards[e.msg.sender];
    bool namedDependency = what == FILE_GATEWAY_HU_CVL() || what == FILE_FEE_ACCRUAL_HU_CVL()
        || what == FILE_SENDER_HU_CVL() || what == FILE_MULTI_ADAPTER_HU_CVL();

    _Hub.file@withrevert(e, what, dependency);
    bool reverted = lastReverted;

    assert((wardBefore != 1 || !namedDependency) => reverted,
        "rewiring the hub fails for a non-ward or a name it does not wire");
}

// HU-RV-02: a pool opens only once, by an admin, on this network, with a manager and a registered currency.
rule rvHuCreatePoolRefusesARepeatOrAnUnusableOpening(env e, HubHarness.PoolId poolId, address admin, HubHarness.AssetId currency) {

    setupHubLinkedHubCoreValidState(e);

    mathint wardBefore = _Hub.wards[e.msg.sender];
    mathint poolNetwork = poolId / 2^48;
    mathint localNetwork = ghostMsLocalCentrifugeId16;
    bool currencyRegistered = ghostHrAssetRegistered[currency];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _Hub.createPool@withrevert(e, poolId, admin, currency);
    bool reverted = lastReverted;

    assert((wardBefore != 1 || poolNetwork != localNetwork || admin == 0 || !currencyRegistered
            || poolCurrencyBefore != 0) => reverted,
        "pool creation fails for a non-ward, foreign id, no admin, unknown currency or repeat");
}

// HU-RV-03: setting a policy fails on a missing pool or for a caller neither admin nor pool manager.
rule rvHuSetPolicyRefusesAnUnauthorisedInstall(env e, HubHarness.PoolId poolId, address newPolicy) {

    setupHubLinkedHubCoreValidState(e);

    mathint wardBefore = _Hub.wards[e.msg.sender];
    bool managerBefore = ghostHrManager[e.msg.sender];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _Hub.setPolicy@withrevert(e, poolId, newPolicy);
    bool reverted = lastReverted;

    assert(((wardBefore != 1 && !managerBefore) || poolCurrencyBefore == 0) => reverted,
        "a policy change fails for a caller neither ward nor manager, or an unknown pool");
}

// HU-RV-04: a delayed call cannot be scheduled by a non-manager, without a policy or delay, or twice.
rule rvHuInitiateAuthorizationRefusesAnUnauthorisedOrDuplicateSchedule(env e, HubHarness.PoolId poolId, bytes data) {

    setupHubLinkedHubCoreValidState(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    address policyBefore = ghostHrPolicy;
    mathint delayBefore = ghostPolicyDelay48[e.msg.sender][keccak256(data)];
    bytes32 authKey = ghostHrAuthId[poolId][policyBefore][ghostHrPolicyNonce64][keccak256(data)];
    mathint scheduledBefore = ghostHrAuthorizedAfter48[authKey];

    _Hub.initiateAuthorization@withrevert(e, poolId, data);
    bool reverted = lastReverted;

    assert((!managerBefore || policyBefore == 0 || delayBefore == 0 || scheduledBefore != 0) => reverted,
        "scheduling fails for a non-manager, no policy, an in-policy call or a repeat");
}

// HU-RV-05: cancelling an authorization fails for a non-manager or when none is pending.
rule rvHuCancelAuthorizationRefusesANonManagerOrAnEmptySlot(env e, HubHarness.PoolId poolId, bytes data) {

    setupHubLinkedHubCoreValidState(e);
    address installedPolicy = ghostHrPolicy;

    bool managerBefore = ghostHrManager[e.msg.sender];
    bytes32 authKey = ghostHrAuthId[poolId][installedPolicy][ghostHrPolicyNonce64][keccak256(data)];
    mathint scheduledBefore = ghostHrAuthorizedAfter48[authKey];

    _Hub.cancelAuthorization@withrevert(e, poolId, data);
    bool reverted = lastReverted;

    assert((!managerBefore || scheduledBefore == 0) => reverted,
        "a non-manager, or no grant pending for that call, makes a cancel revert");
}

// HU-RV-06: changing a pool's managers fails for a non-manager, a missing pool, or the zero address.
rule rvHuUpdateHubManagerRefusesANonManagerOrANullSeat(env e, HubHarness.PoolId poolId, address who, bool canManage) {

    setupHubLinkedHubCoreValidState(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    mathint poolCurrencyBefore = ghostHrCurrency128;

    _Hub.updateHubManager@withrevert(e, poolId, who, canManage);
    bool reverted = lastReverted;

    assert((!managerBefore || poolCurrencyBefore == 0 || who == 0) => reverted,
        "manager edits revert for a non-manager, missing pool or address zero");
}

// HU-RV-07: a currency change fails for a non-manager, missing pool, unknown currency, or different decimals.
rule rvHuUpdateCurrencyRefusesARescalingRedenomination(env e, HubHarness.PoolId poolId, HubHarness.AssetId currency) {

    setupHubLinkedHubCoreValidState(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    mathint poolCurrencyBefore = ghostHrCurrency128;
    bool currencyRegistered = ghostHrAssetRegistered[currency];
    mathint newDecimals = ghostHrAssetDecimals8[currency];
    mathint oldDecimals = ghostHrAssetDecimals8[poolCurrencyBefore];

    _Hub.updateCurrency@withrevert(e, poolId, currency);
    bool reverted = lastReverted;

    assert((!managerBefore || poolCurrencyBefore == 0 || !currencyRegistered || newDecimals != oldDecimals)
            => reverted,
        "redenominating fails for a non-manager, unknown pool or currency, or other decimals");
}

// HU-RV-08: creating an account fails for a non-manager, an empty id, or an existing account.
rule rvHuCreateAccountRefusesARepeatOrAnUnusableOpening(env e, HubHarness.PoolId poolId, HubHarness.AccountId account,
    bool isDebitNormal) {

    setupHubLinkedHubCoreValidState(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    mathint lastUpdatedBefore = ghostAcLastUpdated64[account];

    _Hub.createAccount@withrevert(e, poolId, account, isDebitNormal);
    bool reverted = lastReverted;

    assert((!managerBefore || account == 0 || lastUpdatedBefore != 0) => reverted,
        "account creation fails for a non-manager, id zero or a repeat");
}

// HU-RV-09: a holding account change fails for a non-manager, a missing account or an unopened holding.
rule rvHuSetHoldingAccountIdRefusesAnAbsentRowOrHolding(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint8 kind, HubHarness.AccountId account) {

    setupHubLinkedHubCoreValidState(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    mathint lastUpdatedBefore = ghostAcLastUpdated64[account];
    address valuationBefore = ghostHoValuation[assetId];

    _Hub.setHoldingAccountId@withrevert(e, poolId, scId, assetId, kind, account);
    bool reverted = lastReverted;

    assert((!managerBefore || lastUpdatedBefore == 0 || valuationBefore == 0) => reverted,
        "an account swap on a holding needs a manager, a real account and an open holding");
}

// HU-RV-10: a price source change fails for a non-manager, the zero address, or an unopened holding.
rule rvHuUpdateHoldingValuationRefusesANullSourceOrClosedHolding(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, address valuation) {

    setupHubLinkedHubCoreValidState(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    address valuationBefore = ghostHoValuation[assetId];

    _Hub.updateHoldingValuation@withrevert(e, poolId, scId, assetId, valuation);
    bool reverted = lastReverted;

    assert((!managerBefore || valuation == 0 || valuationBefore == 0) => reverted,
        "swapping a holding's price source takes a manager, a real address, an open holding");
}

// HU-RV-11: a manager call fails unless it declares the attached ETH (none in a batch), or zero if remote.
rule rvHuManagerCallRefusesAMisdeclaredValue(env e, HubHarness.PoolId poolId, uint16 centrifugeId, bytes32 target,
    bytes payload, uint128 extraGasLimit, uint256 localValue, address refund) {

    setupHubLinkedHubCoreAnyTransient(e);

    mathint resolvedValue = huInBatchCVL(e) ? 0 : e.msg.value;
    bool localDestination = centrifugeId == ghostMsLocalCentrifugeId16;
    bool valueMismatch = localDestination ? localValue != resolvedValue : localValue != 0;

    _Hub.managerCall@withrevert(e, poolId, centrifugeId, target, payload, extraGasLimit, localValue, refund);
    bool reverted = lastReverted;

    assert(valueMismatch => reverted, "the declared ETH must be the attached ETH (none in a batch), or zero if remote");
}

// HU-RV-12: a request callback fails for any caller but the pool's request manager.
rule rvHuRequestCallbackRefusesAnyCallerButTheRegisteredManager(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, bytes payload, uint128 extraGasLimit, bool unpaidMode, address refund) {

    setupHubLinkedHubCoreValidState(e);

    address registeredManager = ghostHrHubRequestManager[assert_uint16(assetId / 2^112)];

    _Hub.requestCallback@withrevert(e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);
    bool reverted = lastReverted;

    assert((registeredManager == 0 || e.msg.sender != registeredManager) => reverted,
        "only the registered request manager's callback goes through");
}

// HU-RV-13: an asset price read on a holding not yet opened never fails.
rule rvHuPricePoolPerAssetAnswersForAnUnopenedHolding(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId) {

    setupHubLinkedHubCoreValidState(e);

    bool callCarriesEther = e.msg.value != 0;
    bool holdingOpen = holdingOpenedHU(poolId, scId, assetId);

    _Hub.pricePoolPerAsset@withrevert(e, poolId, scId, assetId);
    bool reverted = lastReverted;

    assert((!callCarriesEther && !holdingOpen) => !reverted,
        "an asset price read without ether never fails on a holding not yet opened");
}

// HU-RV-14: a holding opens only once, by a manager, with a share class, known asset, price source and accounts.
rule rvHuInitializeHoldingRefusesARepeatOrAnUnusableOpening(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, address valuation, HubHarness.AccountId[4] accounts) {

    setupHubLinkedHubCoreValidState(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    bool shareClassLive = ghostScShareClassIds;
    bool assetRegistered = ghostHrAssetRegistered[assetId];
    address valuationBefore = ghostHoValuation[assetId];
    bool anyAccountMissing = ghostAcLastUpdated64[accounts[0]] == 0
        || ghostAcLastUpdated64[accounts[1]] == 0
        || ghostAcLastUpdated64[accounts[2]] == 0
        || ghostAcLastUpdated64[accounts[3]] == 0;

    _Hub.initializeHolding@withrevert(e, poolId, scId, assetId, valuation, accounts);
    bool reverted = lastReverted;

    assert((!managerBefore || valuation == 0 || !shareClassLive || !assetRegistered
            || anyAccountMissing || valuationBefore != 0) => reverted,
        "opening a holding needs a manager, source, class, asset, all accounts, no repeat");
}

// HU-RV-15: every manager-facing pool entry fails for a non-manager, except an admin setting the pool's policy.
rule rvHuManagerFacingEntryRefusesANonManager(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) && !NON_MANAGER_ENTRY_HU(f) } {

    setupHubLinkedHubCoreValidState(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    bool wardInstallsRuleBook = f.selector == sig:_Hub.setPolicy(HubHarness.PoolId,address).selector
        && _Hub.wards[e.msg.sender] == 1;

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert((!managerBefore && !wardInstallsRuleBook) => reverted,
        "a caller who is not a manager is refused, bar a ward setting a policy");
}

// HU-RV-16: holding amount and value postings fail for a non-admin, even for a zero amount.
rule rvHuJournalPrimitivesRefuseANonWard(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, bool isPositive, uint128 diff, bool valueLeg) {

    setupHubLinkedHubCoreValidState(e);

    mathint wardBefore = _Hub.wards[e.msg.sender];

    if (valueLeg) {
        _Hub.updateAccountingValue@withrevert(e, poolId, scId, assetId, isPositive, diff);
    } else {
        _Hub.updateAccountingAmount@withrevert(e, poolId, scId, assetId, isPositive, diff);
    }
    bool reverted = lastReverted;

    assert(wardBefore != 1 => reverted, "a non-ward's posting is refused, whatever the amount");
}

// HU-RV-17: postings fail exactly on non-admin, excess ether, or if nonzero missing account, overflow, spent id.
rule rvHuJournalPrimitiveIsNeverRefusedUnbalanced(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, bool isPositive, uint128 diff, bool valueLeg) {

    setupHubLinkedHubCoreValidState(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");
    require(nativeBalances[_Hub] + e.msg.value <= max_uint256, "SAFE: no native balance overflows");

    mathint debitRow = JOURNAL_DEBIT_ROW_HU(assetId, valueLeg, isPositive);
    mathint creditRow = JOURNAL_CREDIT_ROW_HU(assetId, valueLeg, isPositive);
    bool postingFits = ghostAcLastUpdated64[debitRow] != 0 && ghostAcLastUpdated64[creditRow] != 0
        && ghostAcTotalDebit128[debitRow] + diff <= max_uint128
        && ghostAcTotalCredit128[creditRow] + diff <= max_uint128
        && ghostAcJournalIdCounter64 < max_uint64;
    bool accepted = _Hub.wards[e.msg.sender] == 1 && !VALUE_EXCEEDS_BALANCE_HU_CVL(e)
        && (diff == 0 || postingFits);

    if (valueLeg) {
        _Hub.updateAccountingValue@withrevert(e, poolId, scId, assetId, isPositive, diff);
    } else {
        _Hub.updateAccountingAmount@withrevert(e, poolId, scId, assetId, isPositive, diff);
    }
    bool reverted = lastReverted;

    assert(reverted <=> !accepted, "funded ward postings pass exactly if zero or fitting accounts and ids");
}

// HU-RV-18: changing a pool's adapters fails while the gateway is batching.
rule rvHuSetAdaptersRefusesWhileBatching(env e, HubHarness.PoolId poolId, uint16 centrifugeId,
    address[] localAdapters, bytes32[] remoteAdapters, uint8 threshold, address refund) {

    setupHubLinkedHubCoreValidState(e);

    bool batching = ghostGwIsBatching;

    _Hub.setAdapters@withrevert(e, poolId, centrifugeId, localAdapters, remoteAdapters, threshold, refund);
    bool reverted = lastReverted;

    assert(batching => reverted, "no adapter change goes through during a batch");
}

// HU-RV-19: policed pool entries fail on a refusing policy and on success ask it once, bar an admin setting one.
rule rvHuEnforcedEntryPassesTheInstalledPolicy(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) && !NON_MANAGER_ENTRY_HU(f)
        && f.selector != sig:_Hub.initiateAuthorization(HubHarness.PoolId,bytes).selector } {

    setupHubLinkedHubCoreValidState(e);

    address installedPolicy = ghostHrPolicy;
    bool wardInstallsRuleBook = f.selector == sig:_Hub.setPolicy(HubHarness.PoolId,address).selector
        && _Hub.wards[e.msg.sender] == 1;
    mathint enforcementsBefore = ghostPolicyEnforceCount;

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert((!wardInstallsRuleBook && installedPolicy != 0 && ghostPolicyRefuses[installedPolicy]) => reverted,
        "a refusing policy blocks the entry, bar a ward setting a policy");
    assert((!reverted && !wardInstallsRuleBook && installedPolicy != 0)
        => (ghostPolicyEnforceCount == enforcementsBefore + 1 && ghostPolicyLastCallee == installedPolicy
            && ghostPolicyLastPool64 == ghostPoolA64 && ghostPolicyLastCaller == e.msg.sender),
        "a success consulted the policy once, for this pool and caller");
    assert((!reverted && installedPolicy == 0) => ghostPolicyEnforceCount == enforcementsBefore,
        "a pool without a policy consults none");
}

// HU-RV-23: revoking a spoke call fails for a non-manager or a refusing policy; success sends one revocation.
rule rvHuSpokeCallRevokePassesThePolicy(env e, HubHarness.PoolId poolId, uint16 centrifugeId, bytes data, address refund) {

    setupHubLinkedHubCoreValidState(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    address installedPolicy = ghostHrPolicy;
    mathint enforcementsBefore = ghostPolicyEnforceCount;
    mathint sendsBefore = ghostMsSendCount;

    _Hub.unauthorizeSpokeCall@withrevert(e, poolId, centrifugeId, data, refund);
    bool reverted = lastReverted;

    assert(!managerBefore => reverted, "a non-manager cannot revoke a spoke call");
    assert((installedPolicy != 0 && ghostPolicyRefuses[installedPolicy]) => reverted,
        "a refusing policy blocks the revoke");
    assert((!reverted && installedPolicy != 0)
        => (ghostPolicyEnforceCount == enforcementsBefore + 1 && ghostPolicyLastCallee == installedPolicy
            && ghostPolicyLastPool64 == poolId && ghostPolicyLastCaller == e.msg.sender),
        "a revoke asks the installed policy once, for this pool and caller");
    assert(!reverted => (ghostMsSendCount == sendsBefore + 1 && ghostMsLastKind == MS_UNAUTHORIZE_SPOKE()
            && ghostMsLastCid16 == centrifugeId && ghostMsLastPool64 == poolId
            && ghostMsLastPayloadHash == keccak256(data)),
        "a revoke sends exactly one revocation of this call to this network");
}

// HU-RV-24: setting one of the hub's four dependencies never fails for an admin.
rule rvHuFileSucceedsForAWardNamingADependency(env e, bytes32 what, address dependency) {

    setupHubLinkedHubCoreValidState(e);

    bool namedDependency = what == FILE_GATEWAY_HU_CVL() || what == FILE_FEE_ACCRUAL_HU_CVL()
        || what == FILE_SENDER_HU_CVL() || what == FILE_MULTI_ADAPTER_HU_CVL();
    bool admin = _Hub.wards[e.msg.sender] == 1;

    _Hub.file@withrevert(e, what, dependency);
    bool reverted = lastReverted;

    assert((admin && namedDependency && e.msg.value == 0) => !reverted,
        "an admin's update of a known dependency always goes through");
}

// HU-RV-25: a restriction update, a vault update or a share class notice fails for a class never created.
rule rvHuShareClassMessagesRefuseAnUncreatedClass(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint16 centrifugeId, bytes32 word, HubHarness.VaultUpdateKind kind, bytes payload,
    uint128 extraGasLimit, address refund, uint8 which) {

    setupHubLinkedHubCoreValidState(e);

    bool shareClassLive = ghostScShareClassIds;

    if (which == 0) {
        _Hub.updateRestriction@withrevert(e, poolId, scId, centrifugeId, payload, extraGasLimit, refund);
    } else if (which == 1) {
        _Hub.updateVault@withrevert(e, poolId, scId, assetId, word, kind, payload, extraGasLimit, refund);
    } else {
        _Hub.notifyShareClass@withrevert(e, poolId, scId, centrifugeId, word, payload, extraGasLimit, refund);
    }
    bool reverted = lastReverted;

    assert(!shareClassLive => reverted, "no class message goes out for a class never created");
}

// HU-RV-26: an admin's policy change on an existing pool never fails and needs no policy approval.
rule rvHuWardPolicyInstallOutlivesARefusingRuleBook(env e, HubHarness.PoolId poolId, address policy) {

    setupHubLinkedHubCoreValidState(e);

    bool wardCaller = _Hub.wards[e.msg.sender] == 1;
    bool poolExists = ghostHrCurrency128 != 0;
    bool nonceHasRoom = ghostHrPolicyNonce64 < max_uint64;
    mathint enforcementsBefore = ghostPolicyEnforceCount;

    _Hub.setPolicy@withrevert(e, poolId, policy);
    bool reverted = lastReverted;

    assert((wardCaller && e.msg.value == 0 && poolExists && nonceHasRoom) => !reverted,
        "an admin's policy change on an existing pool always goes through");
    assert((!reverted && wardCaller) => ghostPolicyEnforceCount == enforcementsBefore,
        "an admin's policy change consults no policy");
}

// HU-RV-27: cancelling an authorization fails exactly for a non-manager, a refusing policy or none pending.
rule rvHuCancelAuthorizationIsNeverRefusedToAnAdmittedManager(env e, HubHarness.PoolId poolId, bytes data) {

    setupHubLinkedHubCoreValidState(e);
    require(e.msg.value == 0, "SCOPE: no ETH, the function is not payable");

    address installedPolicy = ghostHrPolicy;
    bool managerBefore = ghostHrManager[e.msg.sender];
    bool policyRefuses = installedPolicy != 0 && ghostPolicyRefuses[installedPolicy];
    mathint scheduledBefore = PENDING_AUTH_HU(installedPolicy, ghostHrPolicyNonce64, keccak256(data));

    _Hub.cancelAuthorization@withrevert(e, poolId, data);
    bool reverted = lastReverted;

    assert(reverted <=> (!managerBefore || policyRefuses || scheduledBefore == 0),
        "a cancel fails exactly for a non-manager, a refusing policy or nothing pending");
}
