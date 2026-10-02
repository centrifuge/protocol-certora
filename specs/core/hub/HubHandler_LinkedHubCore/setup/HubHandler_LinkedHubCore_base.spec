// HubHandler, linked hub core lane. Setup: the handler compiled with the real hub core.

import "../../HubHandler/setup/HubHandler_base.spec";
import "../../Hub/setup/Hub_base.spec";
import "../../Holdings/setup/Holdings_single_pool.spec";
import "../../ShareClassManager/setup/ShareClassManager_single_pool.spec";
import "../../HubRegistry/setup/HubRegistry_single_pool.spec";
import "../../Accounting/setup/Accounting_single_pool.spec";

function setupHubHandlerLinkedHubCore(env e) {
    setupHubHandler(e);
    setupHub(e);
    setupHoldings(e);
    setupShareClassManager(e);
    setupHubRegistry(e);
    setupAccounting(e);
    require(_Holdings.wards[_HubHandler] == 1 && _ShareClassManager.wards[_HubHandler] == 1
        && _HubRegistry.wards[_HubHandler] == 1 && _Hub.wards[_HubHandler] == 1 && _Accounting.wards[_Hub] == 1,
        "TRUSTED: deploy wires the hub core wards the handler needs");
    require(forall uint128 a. forall uint8 k.
        ghostHoAccountId256[a][k] == 0 || VALID_ACCOUNT(ghostHoAccountId256[a][k]),
        "SCOPE: holdings wire only modelled accounts");
}

// SAFE: AssetId.centrifugeId, the raw id shifted down by 112 bits.
definition ASSET_CENTRIFUGE_ID_HH_CVL(uint128 assetId) returns mathint = assetId / 2^112;

// SAFE: the four key literals HubHandler.file spells inline.
definition FILE_HUB_HH_CVL() returns bytes32 =
    to_bytes32(0x6875620000000000000000000000000000000000000000000000000000000000);

definition FILE_HOLDINGS_HH_CVL() returns bytes32 =
    to_bytes32(0x686f6c64696e6773000000000000000000000000000000000000000000000000);

definition FILE_SENDER_HH_CVL() returns bytes32 =
    to_bytes32(0x73656e6465720000000000000000000000000000000000000000000000000000);

definition FILE_SHARE_CLASS_MANAGER_HH_CVL() returns bytes32 =
    to_bytes32(0x7368617265436c6173734d616e61676572000000000000000000000000000000);

function setupHubHandlerLinkedHubCoreValidState(env e) {
    setupHubHandlerLinkedHubCore(e);
    assumeAbsentAccountIsEmpty();
    assumeNullAccountNeverCreated();
}

function SETUP_HH(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupHubHandlerLinkedHubCoreValidState(e);
}
