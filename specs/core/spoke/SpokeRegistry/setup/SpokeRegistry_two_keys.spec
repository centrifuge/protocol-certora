// SpokeRegistry, two-keys lane. Setup: two distinct pools or classes.

// Own setup: setups requiring two distinct pools or classes; primary lanes pin one pool and one class.

// SAFE: one pool and class per call keeps the single mirrors exact.
import "SpokeRegistry_base.spec";

function setupTwoClassKeys(env e) {
    setupEnv(e);
    require(ghostPoolA64 != 0 && ghostPoolB64 != 0, "SAFE: pool zero is never a registered pool");
    require(ghostPoolA64 != ghostPoolB64 || ghostShareClassA != ghostShareClassB,
        "SCOPE: two distinct share classes, in one or two pools");
}

function SETUP_SR_TWO_KEYS(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupTwoClassKeys(e);
}

function setupTwoPools(env e) {
    setupEnv(e);
    setupShareClassMode();
    require(ghostPoolA64 != ghostPoolB64, "SCOPE: two distinct pools");
    require(ghostPoolA64 != 0 && ghostPoolB64 != 0, "SAFE: pool zero is never a registered pool");
}
