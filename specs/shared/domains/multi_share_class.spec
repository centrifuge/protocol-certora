// Share class domain, multi-class mode: two nonzero pinned class ids.

import "share_class.spec";

function setupShareClassMode() {
    require(ghostShareClassA != to_bytes16(0) && ghostShareClassB != to_bytes16(0),
        "SAFE: share class zero is never a registered class");
}
