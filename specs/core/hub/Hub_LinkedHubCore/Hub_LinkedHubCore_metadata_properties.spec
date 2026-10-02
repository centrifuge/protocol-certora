import "setup/Hub_LinkedHubCore_metadata.spec";

// --- state_transitions ---

// HU-ST-07: no hub call leaves accounting unlocked, the metadata writers and the rescue included.
rule stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreMetadata(e);

    f(e, args);

    assert(ghostAcCurrentPoolT == 0, "no journal is still open when a hub call returns");
}

// --- high_level ---

// HU-HL-15: the metadata writers and the token rescue move no hub field and leave no batch transient set.
// UNSAFE: a rescued token or receiver is taken not to re-enter; recoverTokens holds no lock (Recoverable.sol:15,24).
rule hlHuMetadataWritersAndRescueWriteNoHubField(env e, method f, calldataarg args, address who)
    filtered { f -> HUB_STORAGE_SILENT_FUNCTION_HU(f) } {

    setupHubLinkedHubCoreMetadata(e);

    uint256 wardBefore = _Hub.wards[who];
    address gatewayBefore = _Hub.gateway;
    address feeAccrualBefore = _Hub.feeAccrual;
    address senderBefore = _Hub.sender;
    address multiAdapterBefore = _Hub.multiAdapter;

    f(e, args);

    assert(_Hub.wards[who] == wardBefore && _Hub.gateway == gatewayBefore && _Hub.feeAccrual == feeAccrualBefore
            && _Hub.sender == senderBefore && _Hub.multiAdapter == multiAdapterBefore
            && ghostHuSenderT == 0 && ghostHuInitiatorT == 0,
        "no hub field moves and no batch transient is left set");
}

// --- reverts ---

// HU-RV-20: pool metadata writes fail for a non-manager or refusing policy, and success asks the policy once.
rule rvHuPoolMetadataWriterPassesBothGates(env e, HubHarness.PoolId poolId, bytes metadata) {

    setupHubLinkedHubCoreMetadata(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    address installedPolicy = ghostHrPolicy;
    mathint enforcementsBefore = ghostPolicyEnforceCount;

    _Hub.setPoolMetadata@withrevert(e, poolId, metadata);
    bool reverted = lastReverted;

    assert(!managerBefore => reverted, "a caller who is not the pool's manager cannot set its metadata");
    assert((installedPolicy != 0 && ghostPolicyRefuses[installedPolicy]) => reverted,
        "an installed policy that refuses blocks the write");
    assert((!reverted && installedPolicy != 0)
        => (ghostPolicyEnforceCount == enforcementsBefore + 1 && ghostPolicyLastCallee == installedPolicy
            && ghostPolicyLastPool64 == poolId && ghostPolicyLastCaller == e.msg.sender),
        "a successful write consulted the policy once, for this pool and caller");
    assert((!reverted && installedPolicy == 0) => ghostPolicyEnforceCount == enforcementsBefore,
        "a pool without a policy consults none");
}

// HU-RV-21: account metadata writes fail for a non-manager or refusing policy, and success asks the policy once.
rule rvHuAccountMetadataWriterPassesBothGates(env e, HubHarness.PoolId poolId, HubHarness.AccountId account,
    bytes metadata) {

    setupHubLinkedHubCoreMetadata(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    address installedPolicy = ghostHrPolicy;
    mathint enforcementsBefore = ghostPolicyEnforceCount;

    _Hub.setAccountMetadata@withrevert(e, poolId, account, metadata);
    bool reverted = lastReverted;

    assert(!managerBefore => reverted, "a caller who is not the pool's manager cannot label its accounts");
    assert((installedPolicy != 0 && ghostPolicyRefuses[installedPolicy]) => reverted,
        "an installed policy that refuses blocks the write");
    assert((!reverted && installedPolicy != 0)
        => (ghostPolicyEnforceCount == enforcementsBefore + 1 && ghostPolicyLastCallee == installedPolicy
            && ghostPolicyLastPool64 == poolId && ghostPolicyLastCaller == e.msg.sender),
        "a successful write consulted the policy once, for this pool and caller");
    assert((!reverted && installedPolicy == 0) => ghostPolicyEnforceCount == enforcementsBefore,
        "a pool without a policy consults none");
}

// HU-RV-22: share class renames fail for a non-manager or refusing policy, and success asks the policy once.
rule rvHuShareClassMetadataWriterPassesBothGates(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    string name, string symbol) {

    setupHubLinkedHubCoreMetadata(e);

    bool managerBefore = ghostHrManager[e.msg.sender];
    address installedPolicy = ghostHrPolicy;
    mathint enforcementsBefore = ghostPolicyEnforceCount;

    _Hub.updateShareClassMetadata@withrevert(e, poolId, scId, name, symbol);
    bool reverted = lastReverted;

    assert(!managerBefore => reverted, "a caller who is not the pool's manager cannot rename its classes");
    assert((installedPolicy != 0 && ghostPolicyRefuses[installedPolicy]) => reverted,
        "an installed policy that refuses blocks the rename");
    assert((!reverted && installedPolicy != 0)
        => (ghostPolicyEnforceCount == enforcementsBefore + 1 && ghostPolicyLastCallee == installedPolicy
            && ghostPolicyLastPool64 == poolId && ghostPolicyLastCaller == e.msg.sender),
        "a successful rename consulted the policy once, for its pool and caller");
    assert((!reverted && installedPolicy == 0) => ghostPolicyEnforceCount == enforcementsBefore,
        "a pool without a policy consults none");
}
