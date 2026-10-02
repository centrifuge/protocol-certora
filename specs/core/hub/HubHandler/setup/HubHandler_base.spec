// HubHandler. Setup: hub-side neighbours modelled in CVL, plus the assumed deploy wiring.

import "../../../../shared/env.spec";
import "../../../messaging/MessageDispatcher/setup/MessageDispatcher_cvl.spec";
import "../../../../shared/models/ISnapshotHook_cvl.spec";
import "../../../../shared/models/IFeeAccrual_cvl.spec";
import "../../../../shared/models/IHubRequestManager_cvl.spec";
import "../../../../shared/models/ISpokeRequestManager_cvl.spec";
import "../../../../shared/models/IVaultFactory_cvl.spec";

using HubHandler as _HubHandler;

methods {
    // SCOPE: bridging hook is arbitrary code, its ledger effects dropped.
    function _.onBridgeShares(BridgingHookStub.BridgeSharesParams) external
        => NONDET;
}

definition EXCLUDED_FUNCTION_HH(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

function setupHubHandler(env e) {
    setupEnv(e);
    require(_HubHandler.sender != 0, "TRUSTED: sender wired at deploy, never cleared");
}
