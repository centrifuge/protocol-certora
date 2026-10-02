import "Hub_LinkedHubCore_valid_state.spec";

// HU-RC-01: a hub admin can create a pool and make another address its manager.
rule rcHuCreatePoolSeatsADelegateIsReachable(env e, HubHarness.PoolId poolId, address admin,
    HubHarness.AssetId currency) {

    setupHubLinkedHubCoreValidState(e);
    require(admin != e.msg.sender, "SCOPE: the manager named is not the opening ward");

    mathint poolCurrencyBefore = ghostHrCurrency128;
    bool adminSeatBefore = ghostHrManager[admin];

    _Hub.createPool(e, poolId, admin, currency);

    mathint poolCurrencyAfter = ghostHrCurrency128;
    bool adminSeatAfter = ghostHrManager[admin];

    satisfy(poolCurrencyBefore == 0 && poolCurrencyAfter != 0 && !adminSeatBefore && adminSeatAfter,
        "a ward can open a pool, naming another party its manager");
}

// HU-RC-02: a hub admin can create a pool and make itself its manager.
rule rcHuCreatePoolSeatsTheOpeningWardIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.AssetId currency) {

    setupHubLinkedHubCoreValidState(e);

    mathint poolCurrencyBefore = ghostHrCurrency128;
    bool callerSeatBefore = ghostHrManager[e.msg.sender];

    _Hub.createPool(e, poolId, e.msg.sender, currency);

    mathint poolCurrencyAfter = ghostHrCurrency128;
    bool callerSeatAfter = ghostHrManager[e.msg.sender];

    satisfy(poolCurrencyBefore == 0 && poolCurrencyAfter != 0 && !callerSeatBefore && callerSeatAfter,
        "a ward can open a pool naming itself its manager");
}

// HU-RC-03: a pool can be created with the lowest valid currency id.
rule rcHuCreatePoolAtTheSmallestCurrencyIsReachable(env e, HubHarness.PoolId poolId, address admin,
    HubHarness.AssetId currency) {

    setupHubLinkedHubCoreValidState(e);

    mathint poolCurrencyBefore = ghostHrCurrency128;

    _Hub.createPool(e, poolId, admin, currency);

    mathint poolCurrencyAfter = ghostHrCurrency128;

    satisfy(poolCurrencyBefore == 0 && poolCurrencyAfter == 1,
        "a pool can be opened in the smallest nonzero currency id");
}

// HU-RC-04: a pool can be created and given a second manager in one transaction.
rule rcHuPoolBirthThenDelegationIsReachable(env e, HubHarness.PoolId poolId, HubHarness.AssetId currency,
    address who) {

    setupHubLinkedHubCoreValidState(e);
    require(who != e.msg.sender, "SCOPE: the new manager is not the opening ward");

    mathint poolCurrencyBefore = ghostHrCurrency128;
    bool whoSeatBefore = ghostHrManager[who];

    _Hub.createPool(e, poolId, e.msg.sender, currency);
    _Hub.updateHubManager(e, poolId, who, true);

    mathint poolCurrencyAfter = ghostHrCurrency128;
    bool whoSeatAfter = ghostHrManager[who];
    bool callerSeatAfter = ghostHrManager[e.msg.sender];

    satisfy(poolCurrencyBefore == 0 && poolCurrencyAfter != 0 && !whoSeatBefore && whoSeatAfter
        && callerSeatAfter,
        "one transaction can open a pool and seat a second manager");
}

// HU-RC-05: a pool manager can appoint another manager alongside itself.
rule rcHuSecondOperatorAppointmentIsReachable(env e, HubHarness.PoolId poolId, address who) {

    setupHubLinkedHubCoreValidState(e);

    bool whoSeatBefore = ghostHrManager[who];

    _Hub.updateHubManager(e, poolId, who, true);

    bool whoSeatAfter = ghostHrManager[who];

    satisfy(who != e.msg.sender && !whoSeatBefore && whoSeatAfter, "a manager can appoint another party as manager");
}

// HU-RC-06: a pool manager can be appointed and removed again in one transaction.
rule rcHuOperatorSeatRoundTripIsReachable(env e, HubHarness.PoolId poolId, address who) {

    setupHubLinkedHubCoreValidState(e);

    bool whoSeatBefore = ghostHrManager[who];

    _Hub.updateHubManager(e, poolId, who, true);

    bool whoSeatMid = ghostHrManager[who];

    _Hub.updateHubManager(e, poolId, who, false);

    bool whoSeatAfter = ghostHrManager[who];

    satisfy(who != e.msg.sender && !whoSeatBefore && whoSeatMid && !whoSeatAfter,
        "another account can gain and lose a manager seat in one go");
}

// HU-RC-07: a pool manager can remove itself as manager.
rule rcHuOperatorCanStandItselfDownIsReachable(env e, HubHarness.PoolId poolId) {

    setupHubLinkedHubCoreValidState(e);

    bool callerSeatBefore = ghostHrManager[e.msg.sender];

    _Hub.updateHubManager(e, poolId, e.msg.sender, false);

    bool callerSeatAfter = ghostHrManager[e.msg.sender];

    satisfy(callerSeatBefore && !callerSeatAfter, "a manager can revoke its own seat");
}

// HU-RC-08: a hub admin who is not a pool manager can install a pool's first policy.
rule rcHuGovernanceInstallsTheFirstRuleBookIsReachable(env e, HubHarness.PoolId poolId, address policy) {

    setupHubLinkedHubCoreValidState(e);
    mathint callerWard = _Hub.wards[e.msg.sender];
    require(callerWard == 1 && !ghostHrManager[e.msg.sender], "SCOPE: a ward holding no manager seat on the pool");

    address ruleBookBefore = ghostHrPolicy;
    mathint tenureBefore = ghostHrPolicyNonce64;

    _Hub.setPolicy(e, poolId, policy);

    address ruleBookAfter = ghostHrPolicy;
    mathint tenureAfter = ghostHrPolicyNonce64;

    satisfy(ruleBookBefore == 0 && ruleBookAfter == policy && ruleBookAfter != 0
        && tenureAfter == tenureBefore + 1,
        "a ward with no manager seat can install a policy where none is set");
}

// HU-RC-09: a pool manager can replace a pool's policy with a different one.
rule rcHuOperatorSwapsTheRuleBookIsReachable(env e, HubHarness.PoolId poolId, address policy) {

    setupHubLinkedHubCoreValidState(e);
    mathint callerWard = _Hub.wards[e.msg.sender];
    require(callerWard != 1, "SCOPE: the caller is not a ward, so acts as manager");

    address ruleBookBefore = ghostHrPolicy;
    mathint tenureBefore = ghostHrPolicyNonce64;

    _Hub.setPolicy(e, poolId, policy);

    address ruleBookAfter = ghostHrPolicy;
    mathint tenureAfter = ghostHrPolicyNonce64;

    satisfy(ruleBookBefore != 0 && ruleBookAfter == policy && ruleBookAfter != ruleBookBefore
        && tenureAfter == tenureBefore + 1,
        "a pool's policy can be swapped, bumping its nonce by one");
}

// HU-RC-10: a pool's policy can be removed, leaving the pool unrestricted.
rule rcHuRuleBookCanBeRemovedIsReachable(env e, HubHarness.PoolId poolId, address policy) {

    setupHubLinkedHubCoreValidState(e);

    address ruleBookBefore = ghostHrPolicy;
    mathint tenureBefore = ghostHrPolicyNonce64;

    _Hub.setPolicy(e, poolId, policy);

    address ruleBookAfter = ghostHrPolicy;
    mathint tenureAfter = ghostHrPolicyNonce64;

    satisfy(ruleBookBefore != 0 && ruleBookAfter == 0 && tenureAfter == tenureBefore + 1,
        "a pool's policy can be removed, its nonce stepping once");
}

// HU-RC-11: a pool manager can schedule a timelocked call under the pool's policy.
rule rcHuPrivilegedCallSchedulingIsReachable(env e, HubHarness.PoolId poolId, bytes data) {

    setupHubLinkedHubCoreValidState(e);
    require(data.length == 0, "SCOPE: an empty scheduled call");

    bytes32 dataHash = keccak256(data);
    address ruleBookBefore = ghostHrPolicy;
    uint64 tenureBefore = ghostHrPolicyNonce64;
    mathint pendingBefore = PENDING_AUTH_HU(ruleBookBefore, tenureBefore, dataHash);

    _Hub.initiateAuthorization(e, poolId, data);

    mathint pendingAfter = PENDING_AUTH_HU(ruleBookBefore, tenureBefore, dataHash);

    satisfy(ruleBookBefore != 0 && pendingBefore == 0
        && pendingAfter > e.block.timestamp,
        "a manager can schedule an authorization that matures later");
}

// HU-RC-12: a privileged call can be scheduled and cancelled in one transaction.
rule rcHuScheduledCallWithdrawalIsReachable(env e, HubHarness.PoolId poolId, bytes data) {

    setupHubLinkedHubCoreValidState(e);
    require(data.length == 0, "SCOPE: an empty scheduled call");

    bytes32 dataHash = keccak256(data);
    address ruleBookBefore = ghostHrPolicy;
    uint64 tenureBefore = ghostHrPolicyNonce64;
    mathint pendingBefore = PENDING_AUTH_HU(ruleBookBefore, tenureBefore, dataHash);

    _Hub.initiateAuthorization(e, poolId, data);

    mathint pendingMid = PENDING_AUTH_HU(ruleBookBefore, tenureBefore, dataHash);

    _Hub.cancelAuthorization(e, poolId, data);

    mathint pendingAfter = PENDING_AUTH_HU(ruleBookBefore, tenureBefore, dataHash);

    satisfy(pendingBefore == 0 && pendingMid != 0 && pendingAfter == 0,
        "a scheduled authorization can be cancelled in the same transaction");
}

// HU-RC-13: a pool manager can add the pool's first share class, using up its salt.
rule rcHuFirstShareClassIsReachable(env e, HubHarness.PoolId poolId, string name, string symbol,
    bytes32 salt) {

    setupHubLinkedHubCoreValidState(e);
    require(name.length == 1 && symbol.length == 1, "SCOPE: a one-character name and symbol");

    mathint classCountBefore = ghostScShareClassCount32;
    bool classOnRecordBefore = ghostScShareClassIds;
    bool saltClaimedBefore = ghostScSalts[salt];

    HubHarness.ShareClassId classId = _Hub.addShareClass(e, poolId, name, symbol, salt);

    mathint classCountAfter = ghostScShareClassCount32;
    bool classOnRecordAfter = ghostScShareClassIds;
    bool saltClaimedAfter = ghostScSalts[salt];

    satisfy(classCountBefore == 0 && classCountAfter == 1 && !classOnRecordBefore && classOnRecordAfter
        && !saltClaimedBefore && saltClaimedAfter && classId == ghostShareClassA,
        "a pool with no class can gain one, its salt marked used");
}

// HU-RC-14: an asset or expense account can be opened as debit-normal.
rule rcHuDebitNormalRowCanBeOpenedIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.AccountId account) {

    setupHubLinkedHubCoreValidState(e);

    mathint rowStampBefore = ghostAcLastUpdated64[account];

    _Hub.createAccount(e, poolId, account, true);

    mathint rowStampAfter = ghostAcLastUpdated64[account];
    bool rowIsDebitNormalAfter = ghostAcIsDebitNormal[account];

    satisfy(rowStampBefore == 0 && rowStampAfter == e.block.timestamp && rowIsDebitNormalAfter,
        "a debit-normal account can be created, stamped now");
}

// HU-RC-15: an equity or liability account can be opened as credit-normal.
rule rcHuCreditNormalRowCanBeOpenedIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.AccountId account) {

    setupHubLinkedHubCoreValidState(e);

    mathint rowStampBefore = ghostAcLastUpdated64[account];

    _Hub.createAccount(e, poolId, account, false);

    mathint rowStampAfter = ghostAcLastUpdated64[account];
    bool rowIsDebitNormalAfter = ghostAcIsDebitNormal[account];

    satisfy(rowStampBefore == 0 && rowStampAfter == e.block.timestamp && !rowIsDebitNormalAfter,
        "a credit-normal account can be created, stamped now");
}

// HU-RC-16: two ledger accounts and a holding can be opened in one transaction.
rule rcHuAccountsThenHoldingIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, address valuation, HubHarness.AccountId debitRow,
    HubHarness.AccountId creditRow, HubHarness.AccountId[4] accounts) {

    setupHubLinkedHubCoreValidState(e);

    address rowValuationBefore = ghostHoValuation[assetId];

    _Hub.createAccount(e, poolId, debitRow, true);
    _Hub.createAccount(e, poolId, creditRow, false);
    _Hub.initializeHolding(e, poolId, scId, assetId, valuation, accounts);

    address rowValuationAfter = ghostHoValuation[assetId];
    bool debitRowIsDebitNormalAfter = ghostAcIsDebitNormal[debitRow];
    bool creditRowIsDebitNormalAfter = ghostAcIsDebitNormal[creditRow];
    mathint amountDebitSlotAfter = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint amountCreditSlotAfter = ghostHoAccountId256[assetId][AMOUNT_CREDIT_KIND_HU_CVL()];
    mathint valueIncreaseSlotAfter = ghostHoAccountId256[assetId][VALUE_INCREASE_KIND_HU_CVL()];
    mathint valueDecreaseSlotAfter = ghostHoAccountId256[assetId][VALUE_DECREASE_KIND_HU_CVL()];

    satisfy(rowValuationBefore == 0 && rowValuationAfter == valuation && rowValuationAfter != 0
        && debitRowIsDebitNormalAfter && !creditRowIsDebitNormalAfter
        && amountDebitSlotAfter != 0 && amountCreditSlotAfter != 0
        && valueIncreaseSlotAfter != 0 && valueDecreaseSlotAfter != 0,
        "two accounts and a holding wired to four accounts can open at once");
}

// HU-RC-17: opening a holding can book its whole initial value as principal in one journal.
rule rcHuHoldingOpeningValueBookedAsPrincipalIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, address valuation,
    HubHarness.AccountId[4] accounts) {

    setupHubLinkedHubCoreValidState(e);

    address rowValuationBefore = ghostHoValuation[assetId];
    mathint rowValueBefore = ghostHoAssetAmountValue128[assetId];
    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.initializeHolding(e, poolId, scId, assetId, valuation, accounts);

    address rowValuationAfter = ghostHoValuation[assetId];
    mathint rowValueAfter = ghostHoAssetAmountValue128[assetId];
    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(rowValuationBefore == 0 && rowValuationAfter != 0 && rowValueBefore == 0 && rowValueAfter > 0
        && ledgerDebitAfter - ledgerDebitBefore == rowValueAfter
        && ledgerCreditAfter - ledgerCreditBefore == rowValueAfter
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a new holding can post its full value, balanced, in a single journal");
}

// HU-RC-18: a holding with no value can be opened without posting any journal.
rule rcHuHoldingOpeningWithNothingToBookIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, address valuation,
    HubHarness.AccountId[4] accounts) {

    setupHubLinkedHubCoreValidState(e);

    address rowValuationBefore = ghostHoValuation[assetId];
    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.initializeHolding(e, poolId, scId, assetId, valuation, accounts);

    address rowValuationAfter = ghostHoValuation[assetId];
    mathint rowValueAfter = ghostHoAssetAmountValue128[assetId];
    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(rowValuationBefore == 0 && rowValuationAfter != 0 && rowValueAfter == 0
        && ledgerDebitAfter == ledgerDebitBefore && ledgerCreditAfter == ledgerCreditBefore
        && journalCounterAfter == journalCounterBefore && sessionPoolAfter == 0,
        "a holding can open at zero value, booking nothing");
}

// HU-RC-19: a holding can be opened with the same account on its debit and credit sides.
rule rcHuHoldingWithARepeatedSlotIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, address valuation,
    HubHarness.AccountId[4] accounts) {

    setupHubLinkedHubCoreValidState(e);

    address rowValuationBefore = ghostHoValuation[assetId];

    _Hub.initializeHolding(e, poolId, scId, assetId, valuation, accounts);

    address rowValuationAfter = ghostHoValuation[assetId];
    mathint amountDebitSlotAfter = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint amountCreditSlotAfter = ghostHoAccountId256[assetId][AMOUNT_CREDIT_KIND_HU_CVL()];

    satisfy(rowValuationBefore == 0 && rowValuationAfter != 0
        && amountDebitSlotAfter == amountCreditSlotAfter && amountDebitSlotAfter != 0,
        "one account can serve as both amount legs of a new holding");
}

// HU-RC-20: a holding's first mark-up can be booked in full as a balanced journal entry.
rule rcHuHoldingMarkUpIsBookedIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId) {

    setupHubLinkedHubCoreValidState(e);

    mathint rowValueBefore = ghostHoAssetAmountValue128[assetId];
    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateHoldingValue(e, poolId, scId, assetId);

    mathint rowValueAfter = ghostHoAssetAmountValue128[assetId];
    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(rowValueBefore == 0 && rowValueAfter > 0
        && ledgerDebitAfter - ledgerDebitBefore == rowValueAfter
        && ledgerCreditAfter - ledgerCreditBefore == rowValueAfter
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a revaluation can mark a zero-valued holding up, booking the gain");
}

// HU-RC-21: a holding that still has assets can be written down to zero value.
rule rcHuHoldingMarkDownToZeroIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId) {

    setupHubLinkedHubCoreValidState(e);
    require(ghostHoIncreasedAmount256[assetId] > ghostHoDecreasedAmount256[assetId],
        "SCOPE: the holding still holds a positive amount");

    mathint rowValueBefore = ghostHoAssetAmountValue128[assetId];
    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateHoldingValue(e, poolId, scId, assetId);

    mathint rowValueAfter = ghostHoAssetAmountValue128[assetId];
    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(rowValueBefore > 0 && rowValueAfter == 0
        && ledgerDebitAfter - ledgerDebitBefore == rowValueBefore
        && ledgerCreditAfter - ledgerCreditBefore == rowValueBefore
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a funded holding can be revalued to zero, booking the whole loss");
}

// HU-RC-22: a revaluation finding a holding's value unchanged can leave the books untouched.
rule rcHuRevaluationLeavingTheBooksUntouchedIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId) {

    setupHubLinkedHubCoreValidState(e);

    mathint rowValueBefore = ghostHoAssetAmountValue128[assetId];
    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateHoldingValue(e, poolId, scId, assetId);

    mathint rowValueAfter = ghostHoAssetAmountValue128[assetId];
    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(rowValueBefore > 0 && rowValueAfter == rowValueBefore
        && ledgerDebitAfter == ledgerDebitBefore && ledgerCreditAfter == ledgerCreditBefore
        && journalCounterAfter == journalCounterBefore && sessionPoolAfter == 0,
        "a revaluation can leave a valued holding and the books unchanged");
}

// HU-RC-23: an admin can book a deposit as a debit to the holding and a matching credit.
rule rcHuDepositPostingIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint128 diff) {

    setupHubLinkedHubCoreValidState(e);
    mathint holdingRow = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint counterpartRow = ghostHoAccountId256[assetId][AMOUNT_CREDIT_KIND_HU_CVL()];
    require(holdingRow != counterpartRow, "SCOPE: the two legs post to distinct accounts");

    mathint holdingDebitBefore = ghostAcTotalDebit128[holdingRow];
    mathint counterpartCreditBefore = ghostAcTotalCredit128[counterpartRow];
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateAccountingAmount(e, poolId, scId, assetId, true, diff);

    mathint holdingDebitAfter = ghostAcTotalDebit128[holdingRow];
    mathint counterpartCreditAfter = ghostAcTotalCredit128[counterpartRow];
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(diff > 0 && holdingDebitAfter == holdingDebitBefore + diff
        && counterpartCreditAfter == counterpartCreditBefore + diff
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a deposit can debit the holding and credit its counterpart account");
}

// HU-RC-24: an admin can book a withdrawal as the mirror image of a deposit.
rule rcHuWithdrawalPostingIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint128 diff) {

    setupHubLinkedHubCoreValidState(e);
    mathint holdingRow = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint counterpartRow = ghostHoAccountId256[assetId][AMOUNT_CREDIT_KIND_HU_CVL()];
    require(holdingRow != counterpartRow, "SCOPE: the two legs post to distinct accounts");

    mathint counterpartDebitBefore = ghostAcTotalDebit128[counterpartRow];
    mathint holdingCreditBefore = ghostAcTotalCredit128[holdingRow];
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateAccountingAmount(e, poolId, scId, assetId, false, diff);

    mathint counterpartDebitAfter = ghostAcTotalDebit128[counterpartRow];
    mathint holdingCreditAfter = ghostAcTotalCredit128[holdingRow];
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(diff > 0 && counterpartDebitAfter == counterpartDebitBefore + diff
        && holdingCreditAfter == holdingCreditBefore + diff
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a withdrawal can credit the holding and debit its counterpart account");
}

// HU-RC-25: an equal deposit and withdrawal can share one journal and cancel out.
rule rcHuAmountRoundTripIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint128 diff) {

    setupHubLinkedHubCoreValidState(e);
    mathint holdingRow = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];

    mathint holdingNetBefore = ghostAcTotalDebit128[holdingRow] - ghostAcTotalCredit128[holdingRow];
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateAccountingAmount(e, poolId, scId, assetId, true, diff);

    mathint holdingNetMid = ghostAcTotalDebit128[holdingRow] - ghostAcTotalCredit128[holdingRow];

    _Hub.updateAccountingAmount(e, poolId, scId, assetId, false, diff);

    mathint holdingNetAfter = ghostAcTotalDebit128[holdingRow] - ghostAcTotalCredit128[holdingRow];
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(diff > 0 && holdingNetMid != holdingNetBefore && holdingNetAfter == holdingNetBefore
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a deposit and equal withdrawal can restore the holding's net");
}

// HU-RC-26: a zero-amount booking can succeed and leave the books untouched.
rule rcHuZeroAmountPostingIsAcceptedIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, bool isPositive, uint128 diff) {

    setupHubLinkedHubCoreValidState(e);

    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateAccountingAmount(e, poolId, scId, assetId, isPositive, diff);

    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(diff == 0 && ledgerDebitAfter == ledgerDebitBefore
        && ledgerCreditAfter == ledgerCreditBefore && journalCounterAfter == journalCounterBefore
        && sessionPoolAfter == 0,
        "a zero amount posting can succeed and book nothing");
}

// HU-RC-27: the largest possible amount can be booked in one call onto empty accounts.
rule rcHuLargestAmountPostingIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint128 diff) {

    setupHubLinkedHubCoreValidState(e);
    mathint holdingRow = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint counterpartRow = ghostHoAccountId256[assetId][AMOUNT_CREDIT_KIND_HU_CVL()];

    mathint holdingDebitBefore = ghostAcTotalDebit128[holdingRow];
    mathint counterpartCreditBefore = ghostAcTotalCredit128[counterpartRow];

    _Hub.updateAccountingAmount(e, poolId, scId, assetId, true, diff);

    mathint holdingDebitAfter = ghostAcTotalDebit128[holdingRow];
    mathint counterpartCreditAfter = ghostAcTotalCredit128[counterpartRow];

    satisfy(diff == max_uint128 && holdingDebitBefore == 0 && counterpartCreditBefore == 0
        && holdingDebitAfter == max_uint128 && counterpartCreditAfter == max_uint128,
        "a posting of the largest amount can fill two empty accounts");
}

// HU-RC-28: an admin can book a value gain as a debit to the holding and a gain credit.
rule rcHuValueGainPostingIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint128 diff) {

    setupHubLinkedHubCoreValidState(e);
    mathint holdingRow = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint gainRow = ghostHoAccountId256[assetId][VALUE_INCREASE_KIND_HU_CVL()];
    require(holdingRow != gainRow, "SCOPE: the gain account is not the holding's own");

    mathint holdingDebitBefore = ghostAcTotalDebit128[holdingRow];
    mathint gainCreditBefore = ghostAcTotalCredit128[gainRow];
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateAccountingValue(e, poolId, scId, assetId, true, diff);

    mathint holdingDebitAfter = ghostAcTotalDebit128[holdingRow];
    mathint gainCreditAfter = ghostAcTotalCredit128[gainRow];
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(diff > 0 && holdingDebitAfter == holdingDebitBefore + diff
        && gainCreditAfter == gainCreditBefore + diff
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a value gain can debit the holding and credit its gain account");
}

// HU-RC-29: an admin can book a value loss as a loss debit and a credit to the holding.
rule rcHuValueLossPostingIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, uint128 diff) {

    setupHubLinkedHubCoreValidState(e);
    mathint holdingRow = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint lossRow = ghostHoAccountId256[assetId][VALUE_DECREASE_KIND_HU_CVL()];
    require(holdingRow != lossRow, "SCOPE: the loss account is not the holding's own");

    mathint lossDebitBefore = ghostAcTotalDebit128[lossRow];
    mathint holdingCreditBefore = ghostAcTotalCredit128[holdingRow];
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateAccountingValue(e, poolId, scId, assetId, false, diff);

    mathint lossDebitAfter = ghostAcTotalDebit128[lossRow];
    mathint holdingCreditAfter = ghostAcTotalCredit128[holdingRow];
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(diff > 0 && lossDebitAfter == lossDebitBefore + diff
        && holdingCreditAfter == holdingCreditBefore + diff
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a value loss can debit the loss account and credit the holding");
}

// HU-RC-30: a zero revaluation can succeed and leave the books untouched.
rule rcHuZeroValuePostingIsAcceptedIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, bool isPositive, uint128 diff) {

    setupHubLinkedHubCoreValidState(e);

    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateAccountingValue(e, poolId, scId, assetId, isPositive, diff);

    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(diff == 0 && ledgerDebitAfter == ledgerDebitBefore
        && ledgerCreditAfter == ledgerCreditBefore && journalCounterAfter == journalCounterBefore
        && sessionPoolAfter == 0,
        "a zero value posting can succeed and book nothing");
}

// HU-RC-31: a pool manager can post a balanced journal of one debit and one credit.
rule rcHuMinimalBalancedJournalIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.JournalEntry[] debits, HubHarness.JournalEntry[] credits) {

    setupHubLinkedHubCoreValidState(e);
    require(debits.length == 1 && credits.length == 1, "SCOPE: one entry on each side");

    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateJournal(e, poolId, debits, credits);

    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(ledgerDebitAfter - ledgerDebitBefore > 0
        && ledgerDebitAfter - ledgerDebitBefore == ledgerCreditAfter - ledgerCreditBefore
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a nonzero balanced journal of one entry a side can be posted");
}

// HU-RC-32: a pool manager can post a balanced journal of two debits and two credits.
rule rcHuWiderBalancedJournalIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.JournalEntry[] debits, HubHarness.JournalEntry[] credits) {

    setupHubLinkedHubCoreValidState(e);
    require(debits.length == 2 && credits.length == 2, "SCOPE: two entries on each side");

    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateJournal(e, poolId, debits, credits);

    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(ledgerDebitAfter - ledgerDebitBefore > 0
        && ledgerDebitAfter - ledgerDebitBefore == ledgerCreditAfter - ledgerCreditBefore
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "a nonzero balanced journal of two entries a side can be posted");
}

// HU-RC-33: an empty journal can be posted, using a journal number while booking nothing.
rule rcHuEmptyJournalIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.JournalEntry[] debits, HubHarness.JournalEntry[] credits) {

    setupHubLinkedHubCoreValidState(e);
    require(debits.length == 0 && credits.length == 0, "SCOPE: a batch with no entries");

    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterBefore = ghostAcJournalIdCounter64;

    _Hub.updateJournal(e, poolId, debits, credits);

    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();
    mathint journalCounterAfter = ghostAcJournalIdCounter64;
    mathint sessionPoolAfter = ghostAcCurrentPoolT;

    satisfy(ledgerDebitAfter == ledgerDebitBefore && ledgerCreditAfter == ledgerCreditBefore
        && journalCounterAfter == journalCounterBefore + 1 && sessionPoolAfter == 0,
        "an empty journal can post, booking nothing but using a journal id");
}

// HU-RC-34: a zero-value journal can mark an account updated without changing any balance.
rule rcHuZeroValuedJournalPairIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.JournalEntry[] debits, HubHarness.JournalEntry[] credits) {

    setupHubLinkedHubCoreValidState(e);
    require(debits.length == 1 && credits.length == 1, "SCOPE: one entry on each side");

    mathint debitedRow = debits[0].accountId;
    mathint debitedRowStampBefore = ghostAcLastUpdated64[debitedRow];
    mathint ledgerDebitBefore = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditBefore = AC_TOTAL_CREDIT_SUM();

    _Hub.updateJournal(e, poolId, debits, credits);

    mathint debitedRowStampAfter = ghostAcLastUpdated64[debitedRow];
    mathint ledgerDebitAfter = AC_TOTAL_DEBIT_SUM();
    mathint ledgerCreditAfter = AC_TOTAL_CREDIT_SUM();

    satisfy(debits[0].value == 0 && credits[0].value == 0
        && debitedRowStampBefore != e.block.timestamp
        && debitedRowStampAfter == e.block.timestamp
        && ledgerDebitAfter == ledgerDebitBefore && ledgerCreditAfter == ledgerCreditBefore,
        "a zero-valued journal can restamp an account without moving totals");
}

// HU-RC-35: a pool's NAV snapshot hook can be set and then removed again.
rule rcHuSnapshotHookRoundTripIsReachable(env e, HubHarness.PoolId poolId, address hookOn,
    address hookOff) {

    setupHubLinkedHubCoreValidState(e);

    address hookBefore = ghostHoSnapshotHook;

    _Hub.setSnapshotHook(e, poolId, hookOn);

    address hookMid = ghostHoSnapshotHook;

    _Hub.setSnapshotHook(e, poolId, hookOff);

    address hookAfter = ghostHoSnapshotHook;

    satisfy(hookBefore == 0 && hookMid != 0 && hookAfter == 0,
        "a snapshot hook can be set and removed in one transaction");
}

// HU-RC-36: a share class can be announced to a spoke in a single message with its payload.
rule rcHuShareClassAnnouncementIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, uint16 centrifugeId, bytes32 registrar, bytes payload,
    uint128 extraGasLimit, address refund) {

    setupHubLinkedHubCoreValidState(e);

    mathint sendsBefore = ghostMsSendCount;

    _Hub.notifyShareClass(e, poolId, scId, centrifugeId, registrar, payload, extraGasLimit, refund);

    mathint sendsAfter = ghostMsSendCount;
    mathint lastKindAfter = ghostMsLastKind;
    bytes16 lastScIdAfter = ghostMsLastScId;
    bytes32 lastPayloadHashAfter = ghostMsLastPayloadHash;

    satisfy(sendsAfter == sendsBefore + 1 && lastKindAfter == MS_NOTIFY_SHARE_CLASS()
        && lastScIdAfter == scId && lastPayloadHashAfter == keccak256(payload),
        "the hub can send one share class notice with its exact payload");
}

// HU-RC-37: the pool's request manager can send a paid request callback to its spoke.
rule rcHuPaidRequestCallbackIsReachable(env e, HubHarness.PoolId poolId, HubHarness.ShareClassId scId,
    HubHarness.AssetId assetId, bytes payload, uint128 extraGasLimit, address refund) {

    setupHubLinkedHubCoreValidState(e);

    mathint callbacksBefore = ghostMsRequestCallbackCount;

    _Hub.requestCallback(e, poolId, scId, assetId, payload, extraGasLimit, false, refund);

    mathint callbacksAfter = ghostMsRequestCallbackCount;
    bool unpaidAfter = ghostMsRequestCallbackUnpaid;
    bytes32 lastPayloadHashAfter = ghostMsLastPayloadHash;

    satisfy(callbacksAfter == callbacksBefore + 1 && !unpaidAfter
        && lastPayloadHashAfter == keccak256(payload),
        "a paid request callback can go out with its exact payload");
}

// HU-RC-38: the pool's request manager can send an unpaid request callback to its spoke.
rule rcHuUnpaidRequestCallbackIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, bytes payload, uint128 extraGasLimit,
    address refund) {

    setupHubLinkedHubCoreValidState(e);

    mathint callbacksBefore = ghostMsRequestCallbackCount;

    _Hub.requestCallback(e, poolId, scId, assetId, payload, extraGasLimit, true, refund);

    mathint callbacksAfter = ghostMsRequestCallbackCount;
    bool unpaidAfter = ghostMsRequestCallbackUnpaid;
    bytes32 lastPayloadHashAfter = ghostMsLastPayloadHash;

    satisfy(callbacksAfter == callbacksBefore + 1 && unpaidAfter
        && lastPayloadHashAfter == keccak256(payload),
        "an unpaid request callback can go out with its exact payload");
}

// HU-RC-39: an admin can grant hub admin rights to another account and revoke them again.
rule rcHuWardAuthorityRoundTripIsReachable(env e, address user) {

    setupHubLinkedHubCoreValidState(e);

    mathint userWardBefore = _Hub.wards[user];

    _Hub.rely(e, user);

    mathint userWardMid = _Hub.wards[user];

    _Hub.deny(e, user);

    mathint userWardAfter = _Hub.wards[user];

    satisfy(user != e.msg.sender && userWardBefore == 0 && userWardMid == 1 && userWardAfter == 0,
        "a ward can make and unmake another ward in one transaction");
}

// HU-RC-40: an admin can revoke its own hub admin rights.
rule rcHuWardCanStandItselfDownIsReachable(env e) {

    setupHubLinkedHubCoreValidState(e);

    mathint callerWardBefore = _Hub.wards[e.msg.sender];

    _Hub.deny(e, e.msg.sender);

    mathint callerWardAfter = _Hub.wards[e.msg.sender];

    satisfy(callerWardBefore == 1 && callerWardAfter == 0, "a hub ward can step down on its own");
}

// HU-RC-41: a pool can price an asset at par when its holding was never opened.
rule rcHuUnopenedHoldingPricesAtParIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId) {

    setupHubLinkedHubCoreValidState(e);

    address rowValuationBefore = ghostHoValuation[assetId];
    mathint quotedPrice = _Hub.pricePoolPerAsset(e, poolId, scId, assetId);

    satisfy(rowValuationBefore == 0 && quotedPrice == 10^18, "a price read on an unopened holding can return par");
}

// HU-RC-42: a pool's newly installed policy can be read back right away.
rule rcHuPassingPolicyReadIsReachable(env e, HubHarness.PoolId poolId, address newPolicy) {

    setupHubLinkedHubCoreValidState(e);

    _Hub.setPolicy(e, poolId, newPolicy);

    address installed = _Hub.policy@withrevert(e, poolId);
    bool reverted = lastReverted;

    satisfy(!reverted && installed == newPolicy, "a pool's policy can be read back right after it is set");
}

// HU-RC-43: an admin can replace a pool's policy without the old policy's consent.
rule rcHuGovernanceReplacesAStandingRuleBookIsReachable(env e, HubHarness.PoolId poolId, address policy) {

    setupHubLinkedHubCoreValidState(e);
    require(!_HubRegistry.manager[poolId][e.msg.sender], "SCOPE: a caller who is not the pool's manager");

    address ruleBookBefore = _Hub.policy(e, poolId);
    mathint tenureBefore = ghostHrPolicyNonce64;

    _Hub.setPolicy(e, poolId, policy);

    address ruleBookAfter = ghostHrPolicy;
    mathint tenureAfter = ghostHrPolicyNonce64;

    satisfy(ruleBookBefore != 0 && ruleBookAfter == policy && ruleBookAfter != ruleBookBefore
        && tenureAfter == tenureBefore + 1,
        "a ward can swap out a pool's installed policy, advancing its nonce");
}

// HU-RC-44: a manager's downward revaluation can raise the balance of a holding's credit-normal account.
rule rcHuValuationDropRaisesACreditNormalHoldingRowIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, AccountingHarness.AccountId own) {

    setupHubLinkedHubCoreValidState(e);
    mathint ownRow = ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()];
    mathint lossRow = ghostHoAccountId256[assetId][VALUE_DECREASE_KIND_HU_CVL()];
    require(own == ownRow, "SCOPE: binds the account to the holding's asset account");

    mathint valueBefore = ghostHoAssetAmountValue128[assetId];
    mathint balanceBefore = accountValueSignedHU(poolId, own);

    _Hub.updateHoldingValue(e, poolId, scId, assetId);

    mathint valueAfter = ghostHoAssetAmountValue128[assetId];
    mathint balanceAfter = accountValueSignedHU(poolId, own);

    satisfy(!ghostAcIsDebitNormal[ownRow] && ownRow != lossRow && valueAfter < valueBefore
        && balanceAfter > balanceBefore,
        "the holding's own account gains balance while its value falls");
}

// HU-RC-45: a manager can move a holding's own account by journal while the holding's value stays zero.
rule rcHuManualJournalMovesAHoldingRowButNotItsValueIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, AccountingHarness.AccountId own,
    HubHarness.JournalEntry[] debits, HubHarness.JournalEntry[] credits) {

    setupHubLinkedHubCoreValidState(e);
    require(debits.length == 1 && credits.length == 1, "SCOPE: one journal entry on each side");

    bool openedBefore = holdingOpenedHU(poolId, scId, assetId);
    mathint ownRow = holdingRowHU(poolId, scId, assetId, 0);
    mathint holdingValueBefore = holdingValueHU(poolId, scId, assetId);
    mathint balanceBefore = accountValueSignedHU(poolId, own);

    _Hub.updateJournal(e, poolId, debits, credits);

    mathint holdingValueAfter = holdingValueHU(poolId, scId, assetId);
    mathint balanceAfter = accountValueSignedHU(poolId, own);

    satisfy(openedBefore && own == ownRow && debits[0].accountId == ownRow && credits[0].accountId != ownRow
        && holdingValueBefore == 0 && balanceBefore == 0 && holdingValueAfter == 0 && balanceAfter != 0,
        "a journal can move the holding's account off zero, not its value");
}

// HU-RC-46: a manager can repoint a holding to an empty account, leaving its value matched by none.
rule rcHuRewiredHoldingRowLeavesItsValueUnmatchedIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, AccountingHarness.AccountId oldRow,
    HubHarness.AccountId freshRow) {

    setupHubLinkedHubCoreValidState(e);

    mathint slotBefore = holdingRowHU(poolId, scId, assetId, 0);
    mathint holdingValueBefore = holdingValueHU(poolId, scId, assetId);
    mathint oldBalanceBefore = accountValueSignedHU(poolId, oldRow);

    _Hub.setHoldingAccountId(e, poolId, scId, assetId, 0, freshRow);

    mathint slotAfter = holdingRowHU(poolId, scId, assetId, 0);
    mathint holdingValueAfter = holdingValueHU(poolId, scId, assetId);
    mathint freshBalanceAfter = accountValueSignedHU(poolId, freshRow);

    satisfy(slotBefore == oldRow && slotAfter == freshRow && oldRow != freshRow
        && holdingValueBefore > 0 && oldBalanceBefore == holdingValueBefore
        && holdingValueAfter == holdingValueBefore && freshBalanceAfter == 0,
        "the holding keeps its value while its new account holds nothing");
}

// HU-RC-47: a registry admin can change a network's request manager without telling the spoke.
rule rcHuRegistryDirectRequestManagerRewireSendsNoSyncIsReachable(env e, HubHarness.PoolId poolId,
    uint16 centrifugeId, address hubManager) {

    setupHubLinkedHubCoreValidState(e);

    address managerBefore = _HubRegistry.hubRequestManager(e, poolId, centrifugeId);
    mathint sendsBefore = ghostMsSendCount;

    _HubRegistry.setHubRequestManager(e, poolId, centrifugeId, hubManager);

    address managerAfter = ghostHrHubRequestManager[centrifugeId];

    satisfy(managerBefore != 0 && managerAfter == hubManager && hubManager != managerBefore
        && ghostMsSendCount == sendsBefore,
        "the hub's request manager changes with no message to the spoke");
}

// HU-RC-48: a manager can change a network's request manager through the hub and tell the spoke.
rule rcHuHubPathRequestManagerRewireDispatchesTheSyncIsReachable(env e, HubHarness.PoolId poolId,
    uint16 centrifugeId, address hubManager, bytes32 spokeManager, address refund) {

    setupHubLinkedHubCoreValidState(e);

    mathint sendsBefore = ghostMsSendCount;

    _Hub.setRequestManager(e, poolId, centrifugeId, hubManager, spokeManager, refund);

    satisfy(ghostHrHubRequestManager[centrifugeId] == hubManager
        && ghostMsSendCount == sendsBefore + 1 && ghostMsLastKind == MS_SET_REQUEST_MANAGER()
        && ghostMsLastWord == spokeManager,
        "the hub stores the manager and sends the spoke its counterpart");
}

// HU-RC-49: an admin can replace a pool's policy that refuses every call without asking it.
rule rcHuWardSwapsARefusingRuleBookWithoutItsConsentIsReachable(env e, HubHarness.PoolId poolId, address policy) {

    setupHubLinkedHubCoreValidState(e);

    address ruleBookBefore = _Hub.policy(e, poolId);
    mathint enforcementsBefore = ghostPolicyEnforceCount;

    _Hub.setPolicy(e, poolId, policy);

    satisfy(ruleBookBefore != 0 && ghostPolicyRefuses[ruleBookBefore] && ghostHrPolicy == policy
        && policy != ruleBookBefore && ghostPolicyEnforceCount == enforcementsBefore,
        "a refusing policy can be swapped out without being consulted");
}

// HU-RC-50: a pool manager can revoke a spoke call authorization with the policy's approval.
rule rcHuRevocationPassesAConsentingPolicyIsReachable(env e, HubHarness.PoolId poolId, uint16 centrifugeId,
    bytes data, address refund) {

    setupHubLinkedHubCoreValidState(e);

    address installedPolicy = ghostHrPolicy;
    mathint enforcementsBefore = ghostPolicyEnforceCount;
    mathint sendsBefore = ghostMsSendCount;

    _Hub.unauthorizeSpokeCall(e, poolId, centrifugeId, data, refund);

    satisfy(installedPolicy != 0 && ghostPolicyEnforceCount == enforcementsBefore + 1
        && ghostPolicyLastCallee == installedPolicy
        && ghostMsSendCount == sendsBefore + 1 && ghostMsLastKind == MS_UNAUTHORIZE_SPOKE(),
        "a manager's revocation under a policy asks it once and sends the revocation");
}

// HU-RC-51: a hub admin can repoint the hub's multi-adapter.
rule rcHuFileRepointsTheMultiAdapterIsReachable(env e, address data) {

    setupHubLinkedHubCoreValidState(e);

    address multiAdapterBefore = _Hub.multiAdapter;

    _Hub.file(e, FILE_MULTI_ADAPTER_HU_CVL(), data);

    satisfy(data != 0 && multiAdapterBefore != data && _Hub.multiAdapter == data,
        "an admin can move the hub onto another multi-adapter");
}

// HU-RC-52: a new pool's manager, not an admin, can install its first policy unchecked.
rule rcHuFreshPoolManagerInstallsTheFirstRuleBookUnpolicedIsReachable(env eWard, env eMgr, HubHarness.PoolId poolId,
    HubHarness.AssetId currency, address policy) {

    setupHubLinkedHubCoreValidState(eWard);
    setupHub(eMgr);
    require(_Hub.wards[eMgr.msg.sender] != 1, "SCOPE: the manager is not a hub admin");

    mathint poolCurrencyBefore = ghostHrCurrency128;

    _Hub.createPool(eWard, poolId, eMgr.msg.sender, currency);

    mathint enforcementsBefore = ghostPolicyEnforceCount;

    _Hub.setPolicy(eMgr, poolId, policy);

    satisfy(poolCurrencyBefore == 0 && policy != 0 && ghostHrPolicy == policy
        && ghostPolicyEnforceCount == enforcementsBefore,
        "a fresh pool's manager installs its first policy with no policy asked");
}

// HU-RC-53: a new holding can book its value as debit and credit on one shared account.
rule rcHuSharedAmountSlotsKeepTheHoldingAccountFlatIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, address valuation, HubHarness.AccountId[4] accounts,
    mathint own) {

    setupHubLinkedHubCoreValidState(e);
    assumeUninitializedHoldingHasNoValue(assetId);

    address rowValuationBefore = ghostHoValuation[assetId];
    mathint debitBefore = ghostAcTotalDebit128[own];
    mathint creditBefore = ghostAcTotalCredit128[own];

    _Hub.initializeHolding(e, poolId, scId, assetId, valuation, accounts);

    mathint value = ghostHoAssetAmountValue128[assetId];

    satisfy(rowValuationBefore == 0 && ghostHoAccountId256[assetId][AMOUNT_DEBIT_KIND_HU_CVL()] == own
        && ghostHoAccountId256[assetId][AMOUNT_CREDIT_KIND_HU_CVL()] == own && value > 0
        && ghostAcTotalDebit128[own] == debitBefore + value && ghostAcTotalCredit128[own] == creditBefore + value,
        "one account books both sides of a new holding's value, netting to zero");
}

// HU-RC-54: a pool manager can make a valued holding's debit and credit accounts the same.
rule rcHuHoldingAccountRepointedOntoItsCounterpartIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, HubHarness.AccountId counterpart) {

    setupHubLinkedHubCoreValidState(e);

    mathint slotBefore = holdingRowHU(poolId, scId, assetId, AMOUNT_DEBIT_KIND_HU_CVL());
    mathint creditSlot = holdingRowHU(poolId, scId, assetId, AMOUNT_CREDIT_KIND_HU_CVL());
    mathint holdingValueBefore = holdingValueHU(poolId, scId, assetId);

    _Hub.setHoldingAccountId(e, poolId, scId, assetId, AMOUNT_DEBIT_KIND_HU_CVL(), counterpart);

    satisfy(creditSlot != 0 && slotBefore != creditSlot && to_mathint(counterpart) == creditSlot
        && holdingValueBefore > 0
        && holdingRowHU(poolId, scId, assetId, AMOUNT_DEBIT_KIND_HU_CVL())
            == holdingRowHU(poolId, scId, assetId, AMOUNT_CREDIT_KIND_HU_CVL()),
        "a valued holding's debit account can be set to its credit account");
}

// HU-RC-55: a par asset price can be sent for an unknown asset and an uncreated share class.
rule rcHuAssetPriceNoticeForAnUnknownAssetAndClassIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, HubHarness.AssetId assetId, address refund) {

    setupHubLinkedHubCoreValidState(e);

    bool assetKnownBefore = ghostHrAssetRegistered[assetId];
    bool classLiveBefore = ghostScShareClassIds;
    mathint sendsBefore = ghostMsSendCount;

    _Hub.notifyAssetPrice(e, poolId, scId, assetId, refund);

    satisfy(!assetKnownBefore && !classLiveBefore && ghostMsSendCount == sendsBefore + 1
        && ghostMsLastKind == MS_NOTIFY_PRICE_ASSET() && ghostMsLastPool64 == to_mathint(poolId)
        && ghostMsLastScId == scId && ghostMsLastAssetId128 == to_mathint(assetId) && ghostMsLastAmount == 10^18,
        "the hub can announce a par price for an unknown asset on an uncreated class");
}

// HU-RC-56: a zero, unstamped share price can be sent for an uncreated share class.
rule rcHuSharePriceNoticeForAnUncreatedClassIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, uint16 centrifugeId, address refund) {

    setupHubLinkedHubCoreValidState(e);

    bool classLiveBefore = ghostScShareClassIds;
    mathint sendsBefore = ghostMsSendCount;

    _Hub.notifySharePrice(e, poolId, scId, centrifugeId, refund);

    satisfy(!classLiveBefore && ghostMsSendCount == sendsBefore + 1 && ghostMsLastKind == MS_NOTIFY_PRICE_SHARE()
        && ghostMsLastCid16 == to_mathint(centrifugeId) && ghostMsLastPool64 == to_mathint(poolId)
        && ghostMsLastScId == scId && ghostMsLastAmount == 0 && ghostMsLastComputedAt64 == 0,
        "the hub can announce a zero, unstamped price for an uncreated class");
}

// HU-RC-57: the pool's policy can approve a share class notice.
rule rcHuShareClassNoticeConsultsTheInstalledPolicyIsReachable(env e, HubHarness.PoolId poolId,
    HubHarness.ShareClassId scId, uint16 centrifugeId, bytes32 registrar, bytes payload, uint128 extraGasLimit,
    address refund) {

    setupHubLinkedHubCoreValidState(e);

    address installedPolicy = ghostHrPolicy;
    mathint enforcementsBefore = ghostPolicyEnforceCount;

    _Hub.notifyShareClass(e, poolId, scId, centrifugeId, registrar, payload, extraGasLimit, refund);

    satisfy(installedPolicy != 0 && ghostPolicyEnforceCount == enforcementsBefore + 1
        && ghostPolicyLastCallee == installedPolicy,
        "a share class notice passes an installed policy that is asked once");
}
