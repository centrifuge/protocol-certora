// Hub, linked hub core lane. Setup: the hub on real registry, holdings, ledger, classes.

import "../../Hub/setup/Hub_base.spec";
import "../../HubRegistry/setup/HubRegistry_single_pool.spec";
import "../../Holdings/setup/Holdings_single_pool.spec";
import "../../Accounting/setup/Accounting_single_pool.spec";
import "../../ShareClassManager/setup/ShareClassManager_single_pool.spec";

function setupHubLinkedHubCore(env e) {
    setupHubLinkedHubCoreAnyTransient(e);
    requireHubTransientsEmpty();
}

// No valid-state pack: its invariants are proved from calls with empty transients.
function setupHubLinkedHubCoreAnyTransient(env e) {
    setupHubAnyTransient(e);
    setupHubRegistry(e);
    setupHoldings(e);
    setupAccounting(e);
    setupShareClassManager(e);
    require(_HubRegistry.wards[_Hub] == 1 && _Holdings.wards[_Hub] == 1 && _Accounting.wards[_Hub] == 1
        && _ShareClassManager.wards[_Hub] == 1,
        "TRUSTED: deployment makes the hub a ward of its ledgers");
    require(forall uint128 a. forall uint8 k.
        ghostHoAccountId256[a][k] == 0 || VALID_ACCOUNT(ghostHoAccountId256[a][k]),
        "SCOPE: holdings wire only modelled accounts");
}

// SAFE: AssetId.centrifugeId, the raw id shifted down by 112 bits.
definition ASSET_CHAIN_UNIT_HU_CVL() returns mathint = 2^112;

// SAFE: AccountKind enum positions, which no getter exposes.
definition AMOUNT_DEBIT_KIND_HU_CVL() returns uint8 = 0;

definition VALUE_INCREASE_KIND_HU_CVL() returns uint8 = 2;

definition VALUE_DECREASE_KIND_HU_CVL() returns uint8 = 3;

definition WIRING_FUNCTION_HU(method f) returns bool =
    f.selector == sig:_Hub.initializeHolding(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,address,HubHarness.AccountId[4]).selector
    || f.selector == sig:_Hub.setHoldingAccountId(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,uint8,HubHarness.AccountId).selector;

definition VALUATION_FUNCTION_HU(method f) returns bool =
    f.selector == sig:_Hub.initializeHolding(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,address,HubHarness.AccountId[4]).selector
    || f.selector == sig:_Hub.updateHoldingValuation(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,address).selector;

definition JOURNALLING_FUNCTION_HU(method f) returns bool =
    f.selector == sig:_Hub.updateJournal(HubHarness.PoolId,HubHarness.JournalEntry[],HubHarness.JournalEntry[]).selector
    || f.selector == sig:_Hub.updateAccountingAmount(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,bool,uint128).selector
    || f.selector == sig:_Hub.updateAccountingValue(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,bool,uint128).selector
    || f.selector == sig:_Hub.initializeHolding(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,address,HubHarness.AccountId[4]).selector
    || f.selector == sig:_Hub.updateHoldingValue(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId).selector;

definition AMOUNT_CREDIT_KIND_HU_CVL() returns uint8 = 1;

definition PENDING_AUTH_HU(address pol, uint64 tenure, bytes32 dataHash) returns mathint =
    ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][pol][tenure][dataHash]];

// SAFE: the key literals Hub.file spells inline, with no getter.
definition FILE_GATEWAY_HU_CVL() returns bytes32 =
    to_bytes32(0x6761746577617900000000000000000000000000000000000000000000000000);

definition FILE_FEE_ACCRUAL_HU_CVL() returns bytes32 =
    to_bytes32(0x6665654163637275616c00000000000000000000000000000000000000000000);

definition FILE_SENDER_HU_CVL() returns bytes32 =
    to_bytes32(0x73656e6465720000000000000000000000000000000000000000000000000000);

definition FILE_MULTI_ADAPTER_HU_CVL() returns bytes32 =
    to_bytes32(0x6d756c7469416461707465720000000000000000000000000000000000000000);

// SAFE: a call funding more than its caller holds never runs.
definition VALUE_EXCEEDS_BALANCE_HU_CVL(env e) returns bool =
    e.msg.value > nativeBalances[e.msg.sender];

definition NON_MANAGER_ENTRY_HU(method f) returns bool =
    f.selector == sig:_Hub.file(bytes32,address).selector
    || f.selector == sig:_Hub.createPool(HubHarness.PoolId,address,HubHarness.AssetId).selector
    || f.selector == sig:_Hub.requestCallback(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,bytes,uint128,bool,address).selector
    || f.selector == sig:_Hub.updateAccountingAmount(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,bool,uint128).selector
    || f.selector == sig:_Hub.updateAccountingValue(HubHarness.PoolId,HubHarness.ShareClassId,HubHarness.AssetId,bool,uint128).selector
    || f.selector == sig:_Hub.rely(address).selector
    || f.selector == sig:_Hub.deny(address).selector;

definition JOURNAL_DEBIT_ROW_HU(uint128 a, bool valueLeg, bool isPositive) returns mathint =
    isPositive ? ghostHoAccountId256[a][AMOUNT_DEBIT_KIND_HU_CVL()]
        : ghostHoAccountId256[a][valueLeg ? VALUE_DECREASE_KIND_HU_CVL() : AMOUNT_CREDIT_KIND_HU_CVL()];

definition JOURNAL_CREDIT_ROW_HU(uint128 a, bool valueLeg, bool isPositive) returns mathint =
    isPositive ? ghostHoAccountId256[a][valueLeg ? VALUE_INCREASE_KIND_HU_CVL() : AMOUNT_CREDIT_KIND_HU_CVL()]
        : ghostHoAccountId256[a][AMOUNT_DEBIT_KIND_HU_CVL()];

function accountValueSignedHU(HubHarness.PoolId poolId, AccountingHarness.AccountId account) returns mathint {
    env eView;
    bool isPositive;
    uint128 reported;
    isPositive, reported = _Accounting.accountValue(eView, poolId, account);
    return isPositive ? to_mathint(reported) : -to_mathint(reported);
}

function holdingValueHU(HubHarness.PoolId poolId, HubHarness.ShareClassId scId, HubHarness.AssetId assetId) returns mathint {
    env eView;
    return _Holdings.value(eView, poolId, scId, assetId);
}

function holdingRowHU(HubHarness.PoolId poolId, HubHarness.ShareClassId scId, HubHarness.AssetId assetId, uint8 kind)
    returns mathint {
    env eView;
    return _Holdings.accountId(eView, poolId, scId, assetId, kind);
}

function holdingOpenedHU(HubHarness.PoolId poolId, HubHarness.ShareClassId scId, HubHarness.AssetId assetId) returns bool {
    env eView;
    return _Holdings.isInitialized(eView, poolId, scId, assetId);
}

function assumeUninitializedHoldingHasNoValue(uint128 a) {
    require(ghostHoValuation[a] == 0 => ghostHoAssetAmountValue128[a] == 0,
        "PROVED: uninitializedHoldingHasNoValue (Holdings)");
}

methods {
    // UNSAFE: executeMulticall is cut, no batched call is analysed.
    function _Hub.executeMulticall(bytes[]) external
        => NONDET DELETE;

    // SCOPE: the ward-gated recoverTokens rescue is cut here, its footprint proved in the metadata lane.
    function _Hub.recoverTokens(address, address, uint256) external
        => NONDET DELETE;
    function _Hub.recoverTokens(address, uint256, address, uint256) external
        => NONDET DELETE;

    // SCOPE: no rule reads free form bytes or strings, writers are cut.
    function _Hub.setPoolMetadata(HubHarness.PoolId, bytes) external
        => NONDET DELETE;
    function _Hub.setAccountMetadata(HubHarness.PoolId, HubHarness.AccountId, bytes) external
        => NONDET DELETE;
    function _Hub.updateShareClassMetadata(HubHarness.PoolId, HubHarness.ShareClassId, string, string) external
        => NONDET DELETE;

    // SCOPE: its struct is declared twice in source, so not in the model.
    function _.sendNotifyShareClass(uint16 centrifugeId, uint64 poolId, bytes16 scId, HubSenderStub.ShareClassMetadata metadata, bytes32 salt, bytes32 registrar, bytes payload, uint128 extraGasLimit, address refund) external with (env e)
        => huNotifyShareClassCVL(e, centrifugeId, poolId, scId, salt, registrar, payload, refund) expect void;

    unresolved external in HubHarness.notifyShareClass(uint64,bytes16,uint16,bytes32,bytes,uint128,address) => DISPATCH [
        HubSenderStub.sendNotifyShareClass(uint16,uint64,bytes16,HubSenderStub.ShareClassMetadata,bytes32,bytes32,bytes,uint128,address)
    ] default NONDET;
}

persistent ghost bytes32 ghostHuLastRegistrar;

function huNotifyShareClassCVL(env e, uint16 cid, uint64 pool, bytes16 scId, bytes32 salt, bytes32 registrar,
    bytes payload, address refund) {
    msNotifyShareClassCVL(e, cid, pool, scId, salt, payload, refund);
    ghostHuLastRegistrar = registrar;
}

function SETUP_HU(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupHubLinkedHubCore(e);
}
