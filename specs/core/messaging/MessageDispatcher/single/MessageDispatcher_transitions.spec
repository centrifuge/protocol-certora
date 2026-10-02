import "../setup/MessageDispatcher_single.spec";

// --- variable_transitions ---

// MD-VT-01: each dispatcher call reaches at most one destination, local or cross-chain.
rule vtMdEachEntryReachesAtMostOneNeighbour(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_MD(f) } {

    setupMessageDispatcher(e);

    mathint callsBefore = DOWNSTREAM_CALLS();

    f(e, args);

    assert(DOWNSTREAM_CALLS() <= callsBefore + 1, "one entry makes at most one downstream call");
}
