// HubRegistry, metadata lane. Setup: setMetadata kept, its bytes copied for real.

// Own setup: base cuts setMetadata; kept there, its bytes copy (loop_iter 16) would weigh on every rule.

import "../../../../shared/env.spec";

using HubRegistry as _HubRegistry;

// UNSAFE: loop and hash bounds leave metadata past 512 bytes unseen.
methods {
    // SAFE: a free id covers the keccak, no grant slot overlaps metadata.
    function HubRegistry._authId(HubRegistry.PoolId, address, uint64, bytes calldata) internal returns (bytes32)
        => NONDET;

    // SAFE: a free delay covers the policy's read-only answer.
    function _.authorizationDelay(uint64, address, bytes) external
        => NONDET;
}

definition EXCLUDED_FUNCTION_HR(method f) returns bool =
    f.isView || f.isPure || f.isFallback;
