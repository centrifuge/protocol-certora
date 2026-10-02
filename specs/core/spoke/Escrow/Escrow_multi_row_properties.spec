import "setup/Escrow_multi_row.spec";

// --- valid_state ---

// PE-VS-02: for every asset, the reserved amount equals the sum of that asset's reservations.
invariant everyAssetRowMatchesItsBucketSum(env e)
    forall address a. forall mathint t. VALID_ROW_PE(a, t)
        => ghostPeRowReserved128[a][t] == PE_ROW_BUCKET_SUM(a, t)
filtered { f -> !EXCLUDED_FUNCTION_PE(f) } { preserved with (env eFunc) { SETUP_PE_MR(e, eFunc); } }
