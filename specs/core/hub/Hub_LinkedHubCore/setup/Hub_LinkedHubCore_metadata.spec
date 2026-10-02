// Hub, linked hub core metadata lane. Setup: the core pins, metadata writers kept.

// Own setup: base cuts the metadata writers and recoverTokens; kept there, they would join every parametric rule.

import "../../Hub/setup/Hub_base.spec";
import "../../HubRegistry/setup/HubRegistry_single_pool.spec";
import "../../Holdings/setup/Holdings_single_pool.spec";
import "../../Accounting/setup/Accounting_single_pool.spec";
import "../../ShareClassManager/setup/ShareClassManager_single_pool.spec";

function setupHubLinkedHubCoreMetadata(env e) {
    setupHub(e);
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

definition HUB_STORAGE_SILENT_FUNCTION_HU(method f) returns bool =
    f.selector == sig:_Hub.setPoolMetadata(HubHarness.PoolId,bytes).selector
    || f.selector == sig:_Hub.setAccountMetadata(HubHarness.PoolId,HubHarness.AccountId,bytes).selector
    || f.selector == sig:_Hub.updateShareClassMetadata(HubHarness.PoolId,HubHarness.ShareClassId,string,string).selector
    || f.selector == sig:_Hub.recoverTokens(address,address,uint256).selector
    || f.selector == sig:_Hub.recoverTokens(address,uint256,address,uint256).selector;
