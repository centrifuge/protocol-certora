// SpokeHandler, registry linked, vault-pointer lane. Setup: a real share token.

// Own setup: a real ShareToken for updateVault, compiled only in its conf; pointer_writes counts that call instead.

import "SpokeHandler_LinkedSpokeRegistry_base.spec";

using ShareToken as _ShareToken;

methods {
    // SAFE: the real share token is the one updateVault target in scene.
    function _.updateVault(address asset, address vault) external => DISPATCHER(true);
}
