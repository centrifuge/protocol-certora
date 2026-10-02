// Vault factory model: one ghost address stands in for every deployed vault.

methods {
    // SCOPE: no vault is deployed, one ghost address answers every call.
    function _.newVault(uint64 poolId, bytes16 scId, address asset, uint256 tokenId, address token, bytes payload) external
        => hmNewVaultCVL() expect address;

    // SCOPE: an address preview no scoped logic consumes.
    function _.getVault(uint64 poolId, bytes16 scId, address asset, uint256 tokenId, address token, bytes payload) external
        => NONDET;
}

// TRUSTED: the factory's vault is never at the null address.
persistent ghost address ghostHmNewVault {
    axiom ghostHmNewVault != 0;
}

function hmNewVaultCVL() returns address {
    return ghostHmNewVault;
}
