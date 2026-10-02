import "setup/Escrow_multi_share_class.spec";

// --- state_transitions ---

// PE-ST-04: a call never changes the escrow holdings of two share classes at once.
rule stPeEscrowRowIsPerShareClass(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_PE(f) } {

    setupPoolEscrowMultiShareClass(e);

    mathint totalABefore = ghostPeClassTotal128[ghostShareClassA];
    mathint reservedABefore = ghostPeClassReserved128[ghostShareClassA];
    mathint totalBBefore = ghostPeClassTotal128[ghostShareClassB];
    mathint reservedBBefore = ghostPeClassReserved128[ghostShareClassB];

    f(e, args);

    assert(ghostPeClassTotal128[ghostShareClassA] != totalABefore
        || ghostPeClassReserved128[ghostShareClassA] != reservedABefore
        => ghostPeClassTotal128[ghostShareClassB] == totalBBefore
            && ghostPeClassReserved128[ghostShareClassB] == reservedBBefore,
        "when one share class's escrow holding moves, every other stays put");
}
