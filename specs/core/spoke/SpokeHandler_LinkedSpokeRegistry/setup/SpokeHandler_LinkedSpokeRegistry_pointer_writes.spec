// SpokeHandler, registry linked. Setup: share token vault pointer writes, counted.

// Own setup: updateVault counted; not in base, which vault_pointer imports and dispatches updateVault to a real token.

methods {
    // SAFE: no scene path calls it, a stray write is counted.
    function _.updateVault(address asset, address vault) external => shTokenVaultPointerWriteCVL() expect void;
}

persistent ghost mathint ghostShTokenPointerWrites;

function shTokenVaultPointerWriteCVL() {
    ghostShTokenPointerWrites = ghostShTokenPointerWrites + 1;
}
