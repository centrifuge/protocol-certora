// Holdings. Setup: valuation and snapshot hook modelled in CVL, asset and network pins.

import "../../../../shared/env.spec";
import "../../../../shared/models/IValuation_cvl.spec";
import "../../../../shared/models/ISnapshotHook_cvl.spec";

using Holdings as _Holdings;

definition EXCLUDED_FUNCTION_HO(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

// UNSAFE: two asset rows, one mutating and one witnessing the frame.
persistent ghost uint128 ghostHoAssetE1;

persistent ghost uint128 ghostHoAssetE2 {
    axiom ghostHoAssetE2 != ghostHoAssetE1;
}

definition VALID_ASSET_HO(uint128 a) returns bool =
    a == ghostHoAssetE1 || a == ghostHoAssetE2;

// UNSAFE: the deficit counters' network key is one symbolic id.
persistent ghost uint16 ghostHoCid16;

function setupHoldings(env e) {
    setupEnv(e);
    setupPoolMode();
    setupShareClassMode();
    require(e.msg.sender != _Holdings, "SAFE: the holdings ledger never calls itself");
}
