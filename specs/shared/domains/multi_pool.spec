// Pool domain, multi-pool mode: two distinct nonzero pinned pools, for isolation.

import "pool.spec";

function setupPoolMode() {
    require(ghostPoolA64 != ghostPoolB64, "SCOPE: two distinct pools");
    require(ghostPoolA64 != 0 && ghostPoolB64 != 0, "SAFE: pool zero is never a registered pool");
}
