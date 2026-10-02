import "Hub_LinkedHubCore_valid_state.spec";

// HU-HL-01: a holding deposit and an equal withdrawal cancel out on every ledger account.
rule hlHuAmountRoundTripKeepsEveryAccountNet(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint128 diff, mathint account) {

    setupHubLinkedHubCoreValidState(e);

    mathint netBefore = ghostAcTotalDebit128[account] - ghostAcTotalCredit128[account];

    _Hub.updateAccountingAmount(e, poolId, scId, assetId, true, diff);
    _Hub.updateAccountingAmount(e, poolId, scId, assetId, false, diff);

    mathint netAfter = ghostAcTotalDebit128[account] - ghostAcTotalCredit128[account];

    assert(netAfter == netBefore, "an equal amount booked in and out leaves every account's net unchanged");
}

// HU-HL-02: undoing a value increase restores a holding's account if gain and loss post elsewhere.
rule hlHuValueRoundTripKeepsTheHoldingAccountNetWhenGainAndLossAreOtherAccounts(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint128 diff) {

    setupHubLinkedHubCoreValidState(e);

    mathint own = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint gain = ghostHoAccountId256[assetId][VALUE_INCREASE_KIND_HU_CVL()];
    mathint loss = ghostHoAccountId256[assetId][VALUE_DECREASE_KIND_HU_CVL()];

    mathint netBefore = ghostAcTotalDebit128[own] - ghostAcTotalCredit128[own];

    _Hub.updateAccountingValue(e, poolId, scId, assetId, true, diff);
    _Hub.updateAccountingValue(e, poolId, scId, assetId, false, diff);

    mathint netAfter = ghostAcTotalDebit128[own] - ghostAcTotalCredit128[own];

    assert(own != gain && own != loss => netAfter == netBefore,
        "an equal gain and loss keep the asset account's net if not shared");
}

// HU-HL-03: a NotifyShareClass message carries the salt the share class was created with.
rule hlHuShareClassAnnouncementCarriesTheClassSalt(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    uint16 centrifugeId, bytes32 registrar, bytes payload, uint128 extraGasLimit, address refund) {

    setupHubLinkedHubCoreValidState(e);

    mathint sendsBefore = ghostMsSendCount;
    bytes32 classSaltBefore = ghostScMetadataSalt;

    _Hub.notifyShareClass(e, poolId, scId, centrifugeId, registrar, payload, extraGasLimit, refund);

    assert(ghostMsSendCount == sendsBefore + 1 && ghostMsLastKind == MS_NOTIFY_SHARE_CLASS()
        => ghostMsLastWord == classSaltBefore,
        "announcing a share class sends its original salt");
}

// HU-HL-04: a hub configuration update sets only the named dependency, to the given address.
rule hlHuFileWiresOnlyTheNamedSlot(env e, bytes32 what, address data) {

    setupHubLinkedHubCoreValidState(e);

    address gatewayBefore = _Hub.gateway;
    address feeAccrualBefore = _Hub.feeAccrual;
    address senderBefore = _Hub.sender;
    address multiAdapterBefore = _Hub.multiAdapter;

    _Hub.file(e, what, data);

    assert(_Hub.gateway == (what == FILE_GATEWAY_HU_CVL() ? data : gatewayBefore)
        && _Hub.feeAccrual == (what == FILE_FEE_ACCRUAL_HU_CVL() ? data : feeAccrualBefore)
        && _Hub.sender == (what == FILE_SENDER_HU_CVL() ? data : senderBefore)
        && _Hub.multiAdapter == (what == FILE_MULTI_ADAPTER_HU_CVL() ? data : multiAdapterBefore),
        "rewiring sets only the named dependency, to the address given");
}

// HU-HL-05: a NotifyShareClass message carries the share token registrar the caller chose.
rule hlHuShareClassAnnouncementCarriesTheCallersRegistrar(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, uint16 centrifugeId, bytes32 registrar, bytes payload, uint128 extraGasLimit,
    address refund) {

    setupHubLinkedHubCoreValidState(e);

    mathint sendsBefore = ghostMsSendCount;

    _Hub.notifyShareClass(e, poolId, scId, centrifugeId, registrar, payload, extraGasLimit, refund);

    assert(ghostMsSendCount == sendsBefore + 1 && ghostMsLastKind == MS_NOTIFY_SHARE_CLASS()
        => ghostHuLastRegistrar == registrar,
        "a share class announcement carries the registrar the caller named");
}

// HU-HL-06: a revaluation notifies a set snapshot hook exactly when its network is in sync.
rule hlHuRevaluationNotifiesTheHookExactlyWhenTheAssetsNetworkIsInSync(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId) {

    setupHubLinkedHubCoreValidState(e);

    uint16 cid = assert_uint16(assetId / ASSET_CHAIN_UNIT_HU_CVL());
    bool inSync = ghostHoIsSnapshot[cid];
    address hookBefore = ghostHoSnapshotHook;
    mathint syncsBefore = ghostHookOnSyncCount;

    _Hub.updateHoldingValue(e, poolId, scId, assetId);

    assert(ghostHookOnSyncCount == syncsBefore + ((inSync && hookBefore != 0) ? 1 : 0),
        "revaluing pings the hook once if set and in sync, else never");
    assert(ghostHookOnSyncCount != syncsBefore
        => (ghostHookOnSyncCid16 == cid && ghostHookOnSyncPool64 == poolId
            && ghostHookOnSyncScId == scId),
        "the notice names the asset's network, pool and share class");
}

// HU-HL-07: a holding posting books the amount on its designated debit and credit accounts only, zero on none.
rule hlHuJournalPrimitivePostsOneBalancedPair(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, bool isPositive, uint128 diff, bool valueLeg, mathint account) {

    setupHubLinkedHubCoreValidState(e);

    mathint debitRow = JOURNAL_DEBIT_ROW_HU(assetId, valueLeg, isPositive);
    mathint creditRow = JOURNAL_CREDIT_ROW_HU(assetId, valueLeg, isPositive);
    mathint debitBefore = ghostAcTotalDebit128[account];
    mathint creditBefore = ghostAcTotalCredit128[account];
    mathint stampBefore = ghostAcLastUpdated64[account];

    if (valueLeg) {
        _Hub.updateAccountingValue(e, poolId, scId, assetId, isPositive, diff);
    } else {
        _Hub.updateAccountingAmount(e, poolId, scId, assetId, isPositive, diff);
    }

    assert(ghostAcTotalDebit128[account] - debitBefore
            == ((diff != 0 && account == debitRow) ? diff : 0),
        "only the designated debit account is debited, by the amount");
    assert(ghostAcTotalCredit128[account] - creditBefore
            == ((diff != 0 && account == creditRow) ? diff : 0),
        "only the designated credit account is credited, by the amount");
    assert(diff == 0 => ghostAcLastUpdated64[account] == stampBefore, "a zero posting updates no account's timestamp");
}

// HU-HL-08: changing a pool's adapters sends that network one message naming the session installed locally.
rule hlHuSetAdaptersAnnouncesTheSessionItInstalls(env e, HubHarness.PoolId poolId, uint16 centrifugeId,
    address[] localAdapters, bytes32[] remoteAdapters, uint8 threshold, address refund) {

    setupHubLinkedHubCoreValidState(e);

    mathint sendsBefore = ghostMsSendCount;

    _Hub.setAdapters(e, poolId, centrifugeId, localAdapters, remoteAdapters, threshold, refund);

    assert(ghostMsSendCount == sendsBefore + 1 && ghostMsLastKind == MS_SET_POOL_ADAPTERS()
        && ghostMsLastSessionId16 == ghostMaActiveSessionId16
        && ghostMsLastCid16 == centrifugeId && ghostMsLastPool64 == poolId,
        "one update leaves for this pool and network, naming the local session");
}

// HU-HL-09: reconfiguring a network's adapters sends the remote update before it installs the new local set.
rule hlHuSetAdaptersSendsBeforeItInstalls(env e, HubHarness.PoolId poolId, uint16 centrifugeId,
    address[] localAdapters, bytes32[] remoteAdapters, uint8 threshold, address refund) {

    setupHubLinkedHubCoreValidState(e);

    mathint clockBefore = ghostCallClock;

    _Hub.setAdapters(e, poolId, centrifugeId, localAdapters, remoteAdapters, threshold, refund);

    mathint sentAt = ghostMsSetPoolAdaptersAt;
    mathint installedAt = ghostMaSetAdaptersAt;

    assert(sentAt >= clockBefore && sentAt < installedAt,
        "the remote update leaves in this call, before the local install");
}

// HU-HL-10: a value drop credits the holding's account in full and never raises its balance if debit-normal.
rule hlHuValuationDropNeverRaisesTheHoldingRowsValue(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, AccountingHarness.AccountId own) {

    setupHubLinkedHubCoreValidState(e);

    mathint ownRow = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint lossRow = ghostHoAccountId256[assetId][VALUE_DECREASE_KIND_HU_CVL()];
    require(own == ownRow, "SAFE: binds the account to the holding's asset account");

    mathint valueBefore = ghostHoAssetAmountValue128[assetId];
    mathint debitBefore = ghostAcTotalDebit128[ownRow];
    mathint creditBefore = ghostAcTotalCredit128[ownRow];
    mathint balanceBefore = accountValueSignedHU(poolId, own);

    _Hub.updateHoldingValue(e, poolId, scId, assetId);

    mathint valueAfter = ghostHoAssetAmountValue128[assetId];
    mathint drop = valueBefore - valueAfter;
    mathint balanceAfter = accountValueSignedHU(poolId, own);

    assert(drop > 0 => (ghostAcTotalCredit128[ownRow] == creditBefore + drop
            && ghostAcTotalDebit128[ownRow] == debitBefore + (ownRow == lossRow ? drop : 0)),
        "the full drop is credited, and debited only if also the loss account");
    assert(drop > 0 && ghostAcIsDebitNormal[ownRow] => balanceAfter <= balanceBefore,
        "a debit-normal holding account never gains balance on a drop");
}

// HU-HL-11: opening a holding books its tracked amount, priced by the given valuation, on its amount accounts.
rule hlHuInitializationBooksTheTrackedAmountAsPrincipal(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, address valuation, HubHarness.AccountId[4] accounts, mathint account) {

    setupHubLinkedHubCoreValidState(e);
    assumeUninitializedHoldingHasNoValue(assetId);

    mathint increased = ghostHoIncreasedAmount256[assetId];
    mathint decreased = ghostHoDecreasedAmount256[assetId];
    mathint tracked = increased >= decreased ? increased - decreased : 0;
    mathint debitBefore = ghostAcTotalDebit128[account];
    mathint creditBefore = ghostAcTotalCredit128[account];
    mathint quotesBefore = ghostValQuoteCount;

    _Hub.initializeHolding(e, poolId, scId, assetId, valuation, accounts);

    mathint value = ghostHoAssetAmountValue128[assetId];
    mathint debitRow = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint creditRow = ghostHoAccountId256[assetId][AMOUNT_CREDIT_KIND_HU_CVL()];

    assert(ghostValQuoteCount == quotesBefore + 1 && ghostValLastCallee == valuation
        && ghostValLastBase128 == tracked && value == ghostValLastQuote128,
        "one quote from the given valuation, for the tracked amount, is kept");
    assert(ghostAcTotalDebit128[account] - debitBefore == (account == debitRow ? value : 0)
        && ghostAcTotalCredit128[account] - creditBefore == (account == creditRow ? value : 0),
        "the value is debited and credited on the two amount accounts only");
}

// HU-HL-12: a share price update accrues fees once via any installed fee hook, for that pool and class.
rule hlHuSharePriceUpdateAccruesExactlyWhenAFeeHookIsInstalled(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.D18 price, uint64 computedAt) {

    setupHubLinkedHubCoreValidState(e);

    address accrualHook = _Hub.feeAccrual;
    mathint accrualsBefore = ghostFaAccrueCount;

    _Hub.updateSharePrice(e, poolId, scId, price, computedAt);

    assert(ghostFaAccrueCount == accrualsBefore + (accrualHook != 0 ? 1 : 0),
        "the fee hook is called once if installed, never otherwise");
    assert(ghostFaAccrueCount != accrualsBefore
        => (ghostFaLastCallee == accrualHook && ghostFaLastPool64 == poolId && ghostFaLastScId == scId),
        "the accrual goes to the installed hook, for this pool and class");
}

// HU-HL-13: a current-time share price update accrues fees once via any installed hook, for its pool and class.
rule hlHuSharePriceUpdateStampedNowAccruesExactlyWhenAFeeHookIsInstalled(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.D18 price) {

    setupHubLinkedHubCoreValidState(e);

    address accrualHook = _Hub.feeAccrual;
    mathint accrualsBefore = ghostFaAccrueCount;

    _Hub.updateSharePrice(e, poolId, scId, price);

    assert(ghostFaAccrueCount == accrualsBefore + (accrualHook != 0 ? 1 : 0),
        "the fee hook is called once if installed, never otherwise");
    assert(ghostFaAccrueCount != accrualsBefore
        => (ghostFaLastCallee == accrualHook && ghostFaLastPool64 == poolId && ghostFaLastScId == scId),
        "the accrual goes to the installed hook, for this pool and class");
}

// HU-HL-14: an asset price notice accrues fees once via any installed fee hook, for that pool and class.
rule hlHuAssetPriceNotificationAccruesExactlyWhenAFeeHookIsInstalled(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, address refund) {

    setupHubLinkedHubCoreValidState(e);

    address accrualHook = _Hub.feeAccrual;
    mathint accrualsBefore = ghostFaAccrueCount;

    _Hub.notifyAssetPrice(e, poolId, scId, assetId, refund);

    assert(ghostFaAccrueCount == accrualsBefore + (accrualHook != 0 ? 1 : 0),
        "the fee hook is called once if installed, never otherwise");
    assert(ghostFaAccrueCount != accrualsBefore
        => (ghostFaLastCallee == accrualHook && ghostFaLastPool64 == poolId && ghostFaLastScId == scId),
        "the accrual goes to the installed hook, for this pool and class");
}

// HU-HL-16: installing a policy, even the current one, voids earlier scheduled authorizations.
rule hlHuRuleBookInstallAlwaysOpensANewTenure(env e, HubHarness.PoolId poolId, address policy) {

    setupHubLinkedHubCoreValidState(e);

    mathint tenureBefore = ghostHrPolicyNonce64;

    _Hub.setPolicy(e, poolId, policy);

    assert(ghostHrPolicy == policy && ghostHrPolicyNonce64 == tenureBefore + 1,
        "setting a policy, even a repeat, installs it and adds one to its nonce");
}

// HU-HL-17: retrying a current-time share price update later gives the policy the same calldata.
rule hlHuSharePriceUpdateStampedNowAsksThePolicyAboutACallFreeOfTheClock(env e1, env e2, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.D18 price) {

    setupHubLinkedHubCoreValidState(e1);
    setupHub(e2);
    require(e2.msg.sender == e1.msg.sender && e2.msg.value == e1.msg.value, "SCOPE: the same manager retrying");
    require(e2.block.timestamp > e1.block.timestamp && e2.block.number > e1.block.number,
        "SCOPE: the retry comes later");
    require(ghostHrPolicy != 0, "SCOPE: a pool with a policy to ask");

    _Hub.updateSharePrice(e1, poolId, scId, price);
    bytes32 askedFirst = ghostPolicyLastDataHash;

    _Hub.updateSharePrice(e2, poolId, scId, price);

    assert(ghostPolicyLastDataHash == askedFirst, "the policy is asked about the same call whatever the time");
}

// HU-HL-18: a current-time share price update stores the price with the block time.
rule hlHuSharePriceUpdateStampedNowRecordsTheExecutionTime(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.D18 price) {

    setupHubLinkedHubCoreValidState(e);

    _Hub.updateSharePrice(e, poolId, scId, price);

    assert(ghostScPricePoolPerShare128 == to_mathint(price) && ghostScPriceComputedAt64 == to_mathint(e.block.timestamp),
        "the price is stored as given, stamped with the block time");
}
