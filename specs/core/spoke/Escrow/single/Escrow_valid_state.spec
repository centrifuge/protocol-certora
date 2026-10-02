import "../setup/Escrow_base.spec";

function requirePoolEscrowInvariants(env e) {
    requireInvariant reservedMatchesBucketSum(e);
}

function setupPoolEscrowValidState(env e) {
    setupPoolEscrow(e);
    requirePoolEscrowInvariants(e);
}

// PE-VS-01: a holding's reserved amount always equals the sum of its reservations.
invariant reservedMatchesBucketSum(env e)
    ghostPeReserved128 == PE_RESERVED_BUCKET_SUM()
filtered { f -> !EXCLUDED_FUNCTION_PE(f) } { preserved with (env eFunc) { SETUP_PE(e, eFunc); } }
