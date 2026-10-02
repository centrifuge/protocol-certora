import "HubRegistry_single_pool_valid_state.spec";

// --- variable_transitions ---

// HR-VT-01: a call changes the manager rights of at most one account.
rule vtHrManagerRosterMovesOneAccountAtATime(env e, method f, calldataarg args, address who1, address who2)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);
    require(who1 != who2, "SCOPE: two distinct addresses");

    bool grantedFirstBefore = ghostHrManager[who1];
    bool grantedSecondBefore = ghostHrManager[who2];

    f(e, args);

    bool grantedFirstAfter = ghostHrManager[who1];
    bool grantedSecondAfter = ghostHrManager[who2];

    assert(grantedFirstAfter != grantedFirstBefore => grantedSecondAfter == grantedSecondBefore,
        "no call touches two accounts' manager rights");
}

// HR-VT-02: each call leaves a pool's policy nonce unchanged or advances it by one.
rule vtHrTenureCounterAdvancesByAtMostOne(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    mathint nonceBefore = ghostHrPolicyNonce64;

    f(e, args);

    mathint nonceAfter = ghostHrPolicyNonce64;

    assert(nonceAfter == nonceBefore || nonceAfter == nonceBefore + 1,
        "the policy nonce stays or steps up by exactly one");
}

// HR-VT-03: a call changes the hub request manager of at most one network.
rule vtHrRequestManagerMovesOneNetworkAtATime(env e, method f, calldataarg args, uint16 cid1, uint16 cid2)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);
    require(cid1 != cid2, "SCOPE: two distinct networks");

    address wiredFirstBefore = ghostHrHubRequestManager[cid1];
    address wiredSecondBefore = ghostHrHubRequestManager[cid2];

    f(e, args);

    address wiredFirstAfter = ghostHrHubRequestManager[cid1];
    address wiredSecondAfter = ghostHrHubRequestManager[cid2];

    assert(wiredFirstAfter != wiredFirstBefore => wiredSecondAfter == wiredSecondBefore,
        "no call rewires request managers on two networks");
}

// HR-VT-04: a call changes at most one pending authorization.
rule vtHrAuthLedgerMovesOneEntryAtATime(env e, method f, calldataarg args, bytes32 id1, bytes32 id2)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);
    require(id1 != id2, "SCOPE: two distinct authorizations");

    mathint pendingFirstBefore = ghostHrAuthorizedAfter48[id1];
    mathint pendingSecondBefore = ghostHrAuthorizedAfter48[id2];

    f(e, args);

    mathint pendingFirstAfter = ghostHrAuthorizedAfter48[id1];
    mathint pendingSecondAfter = ghostHrAuthorizedAfter48[id2];

    assert(pendingFirstAfter != pendingFirstBefore => pendingSecondAfter == pendingSecondBefore,
        "no call alters two authorization entries at once");
}

// HR-VT-05: pending authorizations change only by scheduling, canceling or consuming.
rule vtHrAuthLedgerMovesOnlyThroughItsThreeWriters(env e, method f, calldataarg args, bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    mathint pendingBefore = ghostHrAuthorizedAfter48[id];

    f(e, args);

    mathint pendingAfter = ghostHrAuthorizedAfter48[id];

    assert(pendingAfter != pendingBefore => AUTH_LEDGER_FUNCTION_HR(f),
        "only schedule, cancel and consume move the authorization ledger");
}

// HR-VT-06: pool manager rights change only through pool creation or a manager update.
rule vtHrManagerRightsMoveOnlyThroughTheirTwoWriters(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    bool grantedBefore = ghostHrManager[who];

    f(e, args);

    bool grantedAfter = ghostHrManager[who];

    assert(grantedAfter != grantedBefore => MANAGER_WRITER_FUNCTION_HR(f),
        "only pool registration and manager updates move manager rights");
}

// --- state_transitions ---

// HR-ST-01: changing a pool's policy always advances its policy nonce by one.
rule stHrPolicySwapOpensANewTenure(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    mathint nonceBefore = ghostHrPolicyNonce64;

    f(e, args);

    assert(ghostHrPolicy != policyBefore => ghostHrPolicyNonce64 == nonceBefore + 1,
        "a policy change advances the policy nonce by exactly one");
}

// HR-ST-02: a newly installed policy starts with no pending authorizations.
rule stHrNewTenureStartsWithNoSchedule(env e, method f, calldataarg args, address pol, bytes32 h)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    mathint nonceBefore = ghostHrPolicyNonce64;

    f(e, args);

    uint64 nonceAfter = ghostHrPolicyNonce64;

    assert(nonceAfter != nonceBefore
        => ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][pol][nonceAfter][h]] == 0,
        "a fresh policy nonce carries nothing scheduled");
}

// HR-ST-03: a newly scheduled authorization matures in the future, under the current policy.
rule stHrSchedulingMaturesAheadAndInTheLiveTenure(env e, method f, calldataarg args, address pol, uint64 n,
    bytes32 h)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    mathint nonceBefore = ghostHrPolicyNonce64;
    mathint pendingBefore = ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][pol][n][h]];

    f(e, args);

    mathint pendingAfter = ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][pol][n][h]];

    assert(pendingBefore == 0 && pendingAfter != 0
        => pendingAfter > e.block.timestamp && pol == policyBefore && n == nonceBefore,
        "a new authorization matures after now, under the live policy and nonce");
}

// HR-ST-04: a pending authorization is cleared only under the current policy, without changing that policy.
rule stHrDischargeLeavesTheTenureStanding(env e, method f, calldataarg args, address pol, uint64 n, bytes32 h)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    address policyBefore = ghostHrPolicy;
    mathint nonceBefore = ghostHrPolicyNonce64;
    mathint pendingBefore = ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][pol][n][h]];

    f(e, args);

    mathint pendingAfter = ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][pol][n][h]];

    assert(pendingBefore != 0 && pendingAfter == 0
        => pol == policyBefore && n == nonceBefore
            && ghostHrPolicy == policyBefore && ghostHrPolicyNonce64 == nonceBefore,
        "clearing an authorization needs the live policy and nonce, both kept");
}

// HR-ST-05: a pending authorization is created or cleared, never rescheduled in place.
rule stHrPendingMovesOnlyOffOrOntoZero(env e, method f, calldataarg args, bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    mathint before = ghostHrAuthorizedAfter48[id];

    f(e, args);

    assert(ghostHrAuthorizedAfter48[id] != before => before == 0 || ghostHrAuthorizedAfter48[id] == 0,
        "no pending authorization is shifted to a new time");
}

// HR-ST-06: a created pool never loses its currency, so it cannot stop existing.
rule stHrCurrencyNeverClears(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    mathint before = ghostHrCurrency128;

    f(e, args);

    assert(before != 0 => ghostHrCurrency128 != 0, "a pool's currency, once set, is never cleared");
}

// HR-ST-13: an asset stays registered, nonzero decimals never change, and only registration sets decimals.
rule stHrRegisteredAssetStaysAndASetPrecisionIsFinal(env e, method f, calldataarg args, mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    bool registeredBefore = ghostHrAssetRegistered[a];
    mathint decimalsBefore = ghostHrAssetDecimals8[a];

    f(e, args);

    assert(registeredBefore => ghostHrAssetRegistered[a], "an asset never leaves the registry");
    assert(decimalsBefore != 0 => ghostHrAssetDecimals8[a] == decimalsBefore, "an asset's nonzero decimals never change");
    assert(ghostHrAssetDecimals8[a] != decimalsBefore
        => f.selector == sig:_HubRegistry.registerAsset(HubRegistry.AssetId,uint8).selector,
        "only registration changes an asset's decimals");
}

// HR-ST-14: a pool's currency decimals never change once nonzero, and only asset registration sets them.
rule stHrPoolCurrencySetPrecisionIsStable(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistryValidState(e);

    mathint currencyBefore = ghostHrCurrency128;
    mathint decimalsBefore = ghostHrAssetDecimals8[currencyBefore];

    f(e, args);

    assert(currencyBefore != 0 && decimalsBefore != 0 && ghostHrCurrency128 != 0
        => ghostHrAssetDecimals8[ghostHrCurrency128] == decimalsBefore,
        "a pool's nonzero currency decimals survive currency swaps and re-registration");
    assert(currencyBefore != 0 && ghostHrCurrency128 != 0
            && ghostHrAssetDecimals8[ghostHrCurrency128] != decimalsBefore
        => f.selector == sig:_HubRegistry.registerAsset(HubRegistry.AssetId,uint8).selector,
        "only asset registration changes the pool's currency decimals");
}
