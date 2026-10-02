// SpokeHandler. Setup: token and hub-side neighbours as CVL models, deploy wiring.

import "../../../../shared/env.spec";
import "../../../../shared/tokens/erc20.spec";
import "../../../../shared/tokens/safe_transfer_lib.spec";
import "../../../../shared/models/ShareTokenRegistrar_cvl.spec";
import "../../../../shared/models/ISnapshotHook_cvl.spec";
import "../../../../shared/models/IFeeAccrual_cvl.spec";
import "../../../../shared/models/IHubRequestManager_cvl.spec";
import "../../../../shared/models/ISpokeRequestManager_cvl.spec";
import "../../../../shared/models/IVaultFactory_cvl.spec";

using SpokeHandler as _SpokeHandler;

methods {
    // SCOPE: metadata strings feed no property and write no registry row.
    function _SpokeHandler.updateShareMetadata(SpokeHandler.PoolId, SpokeHandler.ShareClassId, string, string) external
        => NONDET DELETE;
}

definition EXCLUDED_FUNCTION_SH(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

function setupSpokeHandler(env e) {
    setupEnv(e);
    setupERC20();
    require(_SpokeHandler.escrowFactory != 0, "TRUSTED: escrow factory wired at deploy, never cleared");
}
