// Spoke policy model: the enforce gate the Spoke calls on a guarded call.

methods {
    // UNSAFE: drops the policy's revert and the authorization it spends.
    function _.enforce(uint64 poolId, address caller, bytes data) external
        => NONDET;
}
