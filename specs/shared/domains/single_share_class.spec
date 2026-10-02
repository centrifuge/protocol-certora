// Share class domain, single-class mode: both pinned ids are one nonzero class.

import "share_class.spec";

function setupShareClassMode() {
    require(ghostShareClassA == ghostShareClassB, "SCOPE: one modelled share class, standing for any");
    require(ghostShareClassA != to_bytes16(0), "SAFE: share class zero is never a registered class");
}
