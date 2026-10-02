// SpokeHandler, registry linked, entry-gate lane. Setup: the metadata writer left real.

// Own setup: keeps updateShareMetadata; base cuts it, its strings feeding no property of the other lanes.

import "../../../../shared/env.spec";
import "../../../../shared/tokens/erc20.spec";
import "../../../../shared/tokens/safe_transfer_lib.spec";
import "../../../../shared/models/ShareTokenRegistrar_cvl.spec";
import "../../../../shared/models/ISnapshotHook_cvl.spec";
import "../../../../shared/models/IFeeAccrual_cvl.spec";
import "../../../../shared/models/IHubRequestManager_cvl.spec";
import "../../../../shared/models/ISpokeRequestManager_cvl.spec";
import "../../../../shared/models/IVaultFactory_cvl.spec";
import "../../SpokeRegistry/setup/SpokeRegistry_base.spec";
import "../../factories/EscrowFactory/setup/EscrowFactory_cvl.spec";

using SpokeHandler as _SpokeHandler;

function setupSpokeHandlerEntryGate(env e) {
    setupEnv(e);
}
