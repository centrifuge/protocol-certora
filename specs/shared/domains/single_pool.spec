// Pool domain, single-pool mode: both pinned pool ids are one nonzero pool.

import "pool.spec";

function setupPoolMode() {
    require(ghostPoolA64 == ghostPoolB64, "SCOPE: one modelled pool, standing for any");
    require(ghostPoolA64 != 0, "SAFE: pool zero is never a registered pool");
}
