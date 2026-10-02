// ShareClassManager, unpinned lane. Setup: nothing pinned, metadata kept.

// Own setup: no pool, class or network pinned and updateMetadata kept; base cuts it and models three networks only.

import "../../../../shared/env.spec";
import "../../../../shared/domains/pool.spec";
import "../../HubRegistry/setup/HubRegistry_cvl.spec";

using ShareClassManager as _ShareClassManager;

definition EXCLUDED_FUNCTION_SC(method f) returns bool =
    f.isView || f.isPure || f.isFallback;

// SAFE: twin of newShareClassId, the pool id above the 64-bit index.
definition NEW_SHARE_CLASS_ID_SC_CVL(uint64 pool, mathint index) returns bytes16 =
    to_bytes16(require_uint128(pool * 2^64 + index));

function setupShareClassManagerUnpinned(env e) {
    setupEnv(e);
}
