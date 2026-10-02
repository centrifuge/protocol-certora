import "Hub_LinkedHubCore_valid_state.spec";

// HU-AC-01: only a hub admin can grant or revoke hub admin rights.
rule acHuWardSetMovesOnlyForAWard(env e, method f, calldataarg args, address user)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);

    mathint callerWardBefore = _Hub.wards[e.msg.sender];
    mathint userWardBefore = _Hub.wards[user];

    f(e, args);

    mathint userWardAfter = _Hub.wards[user];

    assert(userWardAfter != userWardBefore => callerWardBefore == 1,
        "a non-ward never changes anyone's hub ward rights");
}

// HU-AC-02: only a hub admin can change the hub's messaging contracts or its fee accrual hook.
rule acHuWiringMovesOnlyForAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);

    mathint callerWardBefore = _Hub.wards[e.msg.sender];
    address gatewayBefore = _Hub.gateway;
    address feeAccrualBefore = _Hub.feeAccrual;
    address senderBefore = _Hub.sender;
    address multiAdapterBefore = _Hub.multiAdapter;

    f(e, args);

    address gatewayAfter = _Hub.gateway;
    address feeAccrualAfter = _Hub.feeAccrual;
    address senderAfter = _Hub.sender;
    address multiAdapterAfter = _Hub.multiAdapter;

    assert((gatewayAfter != gatewayBefore || feeAccrualAfter != feeAccrualBefore
            || senderAfter != senderBefore || multiAdapterAfter != multiAdapterBefore)
        => callerWardBefore == 1,
        "only a ward can repoint the hub's gateway, fee hook, sender or adapter");
}

// HU-AC-03: only a hub admin or a pool manager can change a pool's accounting currency.
rule acHuPoolCurrencyMovesOnlyForAWardOrManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    mathint callerWardBefore = _Hub.wards[e.msg.sender];
    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint currencyBefore = ghostHrCurrency128;

    f(e, args);

    mathint currencyAfter = ghostHrCurrency128;

    assert(currencyAfter != currencyBefore => (callerWardBefore == 1 || callerIsManagerBefore),
        "the pool's currency stays put unless a ward or manager calls");
}

// HU-AC-04: only a hub admin or a pool manager can add or remove a pool manager.
rule acHuManagerSeatMovesOnlyForAWardOrManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId,
    address who)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    mathint callerWardBefore = _Hub.wards[e.msg.sender];
    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    bool seatBefore = ghostHrManager[who];

    f(e, args);

    bool seatAfter = ghostHrManager[who];

    assert(seatAfter != seatBefore => (callerWardBefore == 1 || callerIsManagerBefore),
        "manager seats stay put unless a ward or manager calls");
}

// HU-AC-05: only a hub admin or a pool manager can set a pool's policy.
rule acHuPoolPolicyMovesOnlyForAWardOrManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    mathint callerWardBefore = _Hub.wards[e.msg.sender];
    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    address policyBefore = ghostHrPolicy;
    mathint nonceBefore = ghostHrPolicyNonce64;

    f(e, args);

    address policyAfter = ghostHrPolicy;
    mathint nonceAfter = ghostHrPolicyNonce64;

    assert((policyAfter != policyBefore || nonceAfter != nonceBefore)
        => (callerWardBefore == 1 || callerIsManagerBefore),
        "only a ward or a pool manager can change the pool policy or its nonce");
}

// HU-AC-06: only a pool manager can change a pool's pending timelocked calls via the hub.
rule acHuAuthorizationLedgerMovesThroughTheHubOnlyForAPoolManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId,
    bytes32 id)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint validAfterBefore = ghostHrAuthorizedAfter48[id];

    f(e, args);

    mathint validAfterAfter = ghostHrAuthorizedAfter48[id];

    assert(validAfterAfter != validAfterBefore => callerIsManagerBefore,
        "only a pool manager can change a pending authorization");
}

// HU-AC-07: only a pool manager can change a pool's bridging hook.
rule acHuBridgingHookMovesOnlyForAPoolManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    address hookBefore = ghostHrBridgingHook;

    f(e, args);

    address hookAfter = ghostHrBridgingHook;

    assert(hookAfter != hookBefore => callerIsManagerBefore, "a non-manager never repoints the bridging hook");
}

// HU-AC-08: only a pool manager can set a pool's request manager for a network.
rule acHuRequestManagerSeatMovesOnlyForAPoolManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId,
    uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    address requestManagerBefore = ghostHrHubRequestManager[cid];

    f(e, args);

    address requestManagerAfter = ghostHrHubRequestManager[cid];

    assert(requestManagerAfter != requestManagerBefore => callerIsManagerBefore,
        "a non-manager never changes a network's request manager");
}

// HU-AC-09: only a pool manager can change a pool's snapshot hook.
rule acHuSnapshotHookMovesOnlyForAPoolManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    address snapshotHookBefore = ghostHoSnapshotHook;

    f(e, args);

    address snapshotHookAfter = ghostHoSnapshotHook;

    assert(snapshotHookAfter != snapshotHookBefore => callerIsManagerBefore,
        "a non-manager never repoints the snapshot hook");
}

// HU-AC-10: only a pool manager can install or change a holding's valuation.
rule acHuHoldingValuationMovesOnlyForAPoolManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId,
    uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    address valuationBefore = ghostHoValuation[a];

    f(e, args);

    address valuationAfter = ghostHoValuation[a];

    assert(valuationAfter != valuationBefore => callerIsManagerBefore,
        "only a pool manager can set or swap a holding's price source");
}

// HU-AC-11: only a pool manager can set which ledger accounts a holding posts to.
rule acHuHoldingAccountWiringMovesOnlyForAPoolManager(env e, method f, calldataarg args,
    HubRegistry.PoolId poolId, uint128 a, uint8 k)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint accountBefore = ghostHoAccountId256[a][k];

    f(e, args);

    mathint accountAfter = ghostHoAccountId256[a][k];

    assert(accountAfter != accountBefore => callerIsManagerBefore,
        "only a pool manager can rewire a holding's ledger accounts");
}

// HU-AC-12: only a pool manager can change a holding's booked value through the hub.
rule acHuHoldingValueMovesThroughTheHubOnlyForAPoolManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId,
    uint128 a)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint valueBefore = ghostHoAssetAmountValue128[a];

    f(e, args);

    mathint valueAfter = ghostHoAssetAmountValue128[a];

    assert(valueAfter != valueBefore => callerIsManagerBefore,
        "a non-manager never moves a holding's value via the hub");
}

// HU-AC-13: only a pool manager can add a share class or use up a share class salt.
rule acHuShareClassRegisterMovesOnlyForAPoolManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId,
    bytes32 s)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint classCountBefore = ghostScShareClassCount32;
    bool classRegisteredBefore = ghostScShareClassIds;
    bytes32 classSaltBefore = ghostScMetadataSalt;
    bool saltConsumedBefore = ghostScSalts[s];

    f(e, args);

    mathint classCountAfter = ghostScShareClassCount32;
    bool classRegisteredAfter = ghostScShareClassIds;
    bytes32 classSaltAfter = ghostScMetadataSalt;
    bool saltConsumedAfter = ghostScSalts[s];

    assert((classCountAfter != classCountBefore || classRegisteredAfter != classRegisteredBefore
            || classSaltAfter != classSaltBefore || saltConsumedAfter != saltConsumedBefore)
        => callerIsManagerBefore,
        "only a pool manager can change the share class register or its salts");
}

// HU-AC-14: only a pool manager can change a share class price or its timestamp.
rule acHuSharePriceMovesOnlyForAPoolManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint priceBefore = ghostScPricePoolPerShare128;
    mathint computedAtBefore = ghostScPriceComputedAt64;

    f(e, args);

    mathint priceAfter = ghostScPricePoolPerShare128;
    mathint computedAtAfter = ghostScPriceComputedAt64;

    assert((priceAfter != priceBefore || computedAtAfter != computedAtBefore) => callerIsManagerBefore,
        "share prices and their stamps stay put unless a manager calls");
}

// HU-AC-15: only a pool manager can open a new ledger account.
rule acHuAccountCreationNeedsAPoolManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId, mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint lastUpdatedBefore = ghostAcLastUpdated64[a];

    f(e, args);

    mathint lastUpdatedAfter = ghostAcLastUpdated64[a];

    assert(lastUpdatedBefore == 0 && lastUpdatedAfter != 0 => callerIsManagerBefore,
        "new ledger accounts appear only on a manager's call");
}

// HU-AC-16: only a hub admin or a pool manager can post debits to a pool's ledger account.
rule acHuAccountDebitMovesThroughTheHubOnlyForAWardOrManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId,
    mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    mathint callerWardBefore = _Hub.wards[e.msg.sender];
    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint debitBefore = ghostAcTotalDebit128[a];

    f(e, args);

    mathint debitAfter = ghostAcTotalDebit128[a];

    assert(debitAfter != debitBefore => (callerWardBefore == 1 || callerIsManagerBefore),
        "only a ward or a pool manager can change an account's debit total");
}

// HU-AC-17: only a hub admin or a pool manager can post credits to a pool's ledger account.
rule acHuAccountCreditMovesThroughTheHubOnlyForAWardOrManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId,
    mathint a)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    mathint callerWardBefore = _Hub.wards[e.msg.sender];
    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint creditBefore = ghostAcTotalCredit128[a];

    f(e, args);

    mathint creditAfter = ghostAcTotalCredit128[a];

    assert(creditAfter != creditBefore => (callerWardBefore == 1 || callerIsManagerBefore),
        "only a ward or a pool manager can change an account's credit total");
}

// HU-AC-18: only a hub admin or a pool manager can record a new journal in a pool's ledger.
rule acHuJournalCounterMovesThroughTheHubOnlyForAWardOrManager(env e, method f, calldataarg args, HubRegistry.PoolId poolId)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    mathint callerWardBefore = _Hub.wards[e.msg.sender];
    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint counterBefore = ghostAcJournalIdCounter64;

    f(e, args);

    mathint counterAfter = ghostAcJournalIdCounter64;

    assert(counterAfter != counterBefore => (callerWardBefore == 1 || callerIsManagerBefore),
        "only a ward or a pool manager can change the pool's journal counter");
}

// HU-AC-19: only a pool's request manager for a network can send request callbacks there.
rule acHuRequestCallbackNeedsTheRegisteredRequestManager(env e, method f, calldataarg args,
    HubRegistry.PoolId poolId, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    address registeredManagerBefore = _HubRegistry.hubRequestManager[poolId][cid];
    mathint callbacksBefore = ghostMsRequestCallbackCount;

    f(e, args);

    mathint callbacksAfter = ghostMsRequestCallbackCount;
    mathint calledChain = ghostMsLastAssetId128 / ASSET_CHAIN_UNIT_HU_CVL();

    assert(callbacksAfter != callbacksBefore && calledChain == cid
        => e.msg.sender == registeredManagerBefore,
        "a request callback to a network comes only from its request manager");
}

// HU-AC-20: the hub sends a cross-chain message only for a pool manager or a request callback.
rule acHuOutboundInstructionNeedsAPoolManagerOrARequestFulfilment(env e, method f, calldataarg args, HubRegistry.PoolId poolId)
    filtered { f -> !EXCLUDED_FUNCTION_HU(f) } {

    setupHubLinkedHubCore(e);
    require(VALID_POOL(poolId), "SCOPE: the modelled pool");

    bool callerIsManagerBefore = _HubRegistry.manager[poolId][e.msg.sender];
    mathint sendsBefore = ghostMsSendCount;
    mathint callbacksBefore = ghostMsRequestCallbackCount;

    f(e, args);

    mathint sendsAfter = ghostMsSendCount;
    mathint callbacksAfter = ghostMsRequestCallbackCount;

    assert(sendsAfter != sendsBefore => (callerIsManagerBefore || callbacksAfter != callbacksBefore),
        "without a manager, a message leaves only with a request callback");
}
