import "setup/ShareClassManager_multi_share_class.spec";
import "../HubRegistry/setup/HubRegistry_cvl.spec";

// --- valid_state ---

function setupShareClassManagerMultiClassValidState(env e) {
    setupShareClassManager(e);
    requireInvariant classSaltSetImpliesRegisteredPerClass(e);
    requireInvariant registeredClassIndexWithinCount(e);
    requireInvariant classSaltConsumedPerClass(e);
    requireInvariant classSaltsDistinct(e);
    requireInvariant classWithinCountIsRegistered(e);
    requireInvariant registeredClassCarriesASalt(e);
    requireInvariant classTotalIssuanceIsNetworkNetSum(e);
    requireInvariant classUncreatedRowsZero(e);
    requireInvariant classNegativeNetworkCountMatchesItsShortNetworks(e);
}

function SETUP_SC_MC(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupShareClassManagerMultiClassValidState(e);
}

// SC-VS-12: only a registered share class can have a salt.
invariant classSaltSetImpliesRegisteredPerClass(env e)
    (ghostScClassMetadataSalt[ghostShareClassA] != to_bytes32(0) => ghostScClassShareClassIds[ghostShareClassA])
    && (ghostScClassMetadataSalt[ghostShareClassB] != to_bytes32(0) => ghostScClassShareClassIds[ghostShareClassB])
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC_MC(e, eFunc); } }

// SC-VS-13: a registered share class never has an index beyond the pool's class count.
invariant registeredClassIndexWithinCount(env e)
    (ghostScClassShareClassIds[ghostShareClassA] => ghostScClassShareClassCount32 >= SC_CLASS_INDEX(ghostShareClassA))
    && (ghostScClassShareClassIds[ghostShareClassB] => ghostScClassShareClassCount32 >= SC_CLASS_INDEX(ghostShareClassB))
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC_MC(e, eFunc); } }

// SC-VS-15: two share classes of a pool never have the same salt.
invariant classSaltsDistinct(env e)
    (ghostShareClassA != ghostShareClassB
        && ghostScClassMetadataSalt[ghostShareClassA] != to_bytes32(0)
        && ghostScClassMetadataSalt[ghostShareClassB] != to_bytes32(0))
        => ghostScClassMetadataSalt[ghostShareClassA] != ghostScClassMetadataSalt[ghostShareClassB]
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) {
    requireInvariant classSaltConsumedPerClass(e);
    SETUP_SC_MC(e, eFunc);
} }

// SC-VS-16: a share class's salt is always recorded as used.
invariant classSaltConsumedPerClass(env e)
    (ghostScClassMetadataSalt[ghostShareClassA] != to_bytes32(0)
        => ghostScSalts[ghostScClassMetadataSalt[ghostShareClassA]])
    && (ghostScClassMetadataSalt[ghostShareClassB] != to_bytes32(0)
        => ghostScSalts[ghostScClassMetadataSalt[ghostShareClassB]])
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC_MC(e, eFunc); } }

// SC-VS-17: every index up to the pool's class count belongs to a registered share class.
invariant classWithinCountIsRegistered(env e)
    (ghostScClassShareClassCount32 >= SC_CLASS_INDEX(ghostShareClassA) => ghostScClassShareClassIds[ghostShareClassA])
    && (ghostScClassShareClassCount32 >= SC_CLASS_INDEX(ghostShareClassB) => ghostScClassShareClassIds[ghostShareClassB])
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC_MC(e, eFunc); } }

// SC-VS-18: every registered share class has a salt.
invariant registeredClassCarriesASalt(env e)
    (ghostScClassShareClassIds[ghostShareClassA] => ghostScClassMetadataSalt[ghostShareClassA] != to_bytes32(0))
    && (ghostScClassShareClassIds[ghostShareClassB] => ghostScClassMetadataSalt[ghostShareClassB] != to_bytes32(0))
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC_MC(e, eFunc); } }

// SC-VS-19: a share class's total supply is its net issuance summed over all networks.
invariant classTotalIssuanceIsNetworkNetSum(env e)
    SC_CLASS_TOTAL_ISSUANCE(ghostShareClassA) == SC_CLASS_NET_ISSUANCE_SUM(ghostShareClassA)
    && SC_CLASS_TOTAL_ISSUANCE(ghostShareClassB) == SC_CLASS_NET_ISSUANCE_SUM(ghostShareClassB)
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC_MC(e, eFunc); } }

// SC-VS-20: a share class that was never created has no supply, price, or network shares.
invariant classUncreatedRowsZero(env e)
    forall bytes16 c. (VALID_SC(c) && !ghostScClassShareClassIds[c]) => (
        ghostScClassTotalIssuances256[c] == 0
        && ghostScClassTotalRevocations256[c] == 0
        && ghostScClassNegativeNetworkCount32[c] == 0
        && ghostScClassPricePoolPerShare128[c] == 0
        && ghostScClassPriceComputedAt64[c] == 0
        && (forall uint16 cid. VALID_CID(cid) =>
            (ghostScClassIssuances256[c][cid] == 0 && ghostScClassRevocations256[c][cid] == 0))
    )
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC_MC(e, eFunc); } }

// SC-VS-23: a share class correctly counts its networks that revoked more than they issued.
invariant classNegativeNetworkCountMatchesItsShortNetworks(env e)
    ghostScClassNegativeNetworkCount32[ghostShareClassA] == SC_CLASS_NEGATIVE_NETWORK_CARDINALITY(ghostShareClassA)
    && ghostScClassNegativeNetworkCount32[ghostShareClassB] == SC_CLASS_NEGATIVE_NETWORK_CARDINALITY(ghostShareClassB)
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC_MC(e, eFunc); } }

// --- state_transitions ---

// SC-ST-04: a change to one share class leaves the pool's other share class untouched.
rule stScClassRowIsPerClass(env e, method f, calldataarg args, bytes16 c1, bytes16 c2)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);
    require(SC_CLASS_PAIR(c1, c2), "SCOPE: two distinct share classes");

    bool ids1Before = ghostScClassShareClassIds[c1];
    bytes32 salt1Before = ghostScClassMetadataSalt[c1];
    mathint issuances1Before = ghostScClassTotalIssuances256[c1];
    mathint revocations1Before = ghostScClassTotalRevocations256[c1];
    mathint negative1Before = ghostScClassNegativeNetworkCount32[c1];
    mathint price1Before = ghostScClassPricePoolPerShare128[c1];
    mathint stamp1Before = ghostScClassPriceComputedAt64[c1];
    bool ids2Before = ghostScClassShareClassIds[c2];
    bytes32 salt2Before = ghostScClassMetadataSalt[c2];
    mathint issuances2Before = ghostScClassTotalIssuances256[c2];
    mathint revocations2Before = ghostScClassTotalRevocations256[c2];
    mathint negative2Before = ghostScClassNegativeNetworkCount32[c2];
    mathint price2Before = ghostScClassPricePoolPerShare128[c2];
    mathint stamp2Before = ghostScClassPriceComputedAt64[c2];

    f(e, args);

    assert(ghostScClassShareClassIds[c1] != ids1Before || ghostScClassMetadataSalt[c1] != salt1Before
        || ghostScClassTotalIssuances256[c1] != issuances1Before
        || ghostScClassTotalRevocations256[c1] != revocations1Before
        || ghostScClassNegativeNetworkCount32[c1] != negative1Before
        || ghostScClassPricePoolPerShare128[c1] != price1Before
        || ghostScClassPriceComputedAt64[c1] != stamp1Before
        => ghostScClassShareClassIds[c2] == ids2Before && ghostScClassMetadataSalt[c2] == salt2Before
            && ghostScClassTotalIssuances256[c2] == issuances2Before
            && ghostScClassTotalRevocations256[c2] == revocations2Before
            && ghostScClassNegativeNetworkCount32[c2] == negative2Before
            && ghostScClassPricePoolPerShare128[c2] == price2Before
            && ghostScClassPriceComputedAt64[c2] == stamp2Before,
        "share class state moves for one class only");
}

// SC-ST-05: a class's share changes on a network never touch another class's shares there.
rule stScNetworkLedgerIsPerClass(env e, method f, calldataarg args, bytes16 c1, bytes16 c2, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);
    require(SC_CLASS_PAIR(c1, c2), "SCOPE: two distinct share classes");

    mathint issuances1Before = ghostScClassIssuances256[c1][cid];
    mathint revocations1Before = ghostScClassRevocations256[c1][cid];
    mathint issuances2Before = ghostScClassIssuances256[c2][cid];
    mathint revocations2Before = ghostScClassRevocations256[c2][cid];

    f(e, args);

    assert(ghostScClassIssuances256[c1][cid] != issuances1Before
        || ghostScClassRevocations256[c1][cid] != revocations1Before
        => ghostScClassIssuances256[c2][cid] == issuances2Before
            && ghostScClassRevocations256[c2][cid] == revocations2Before,
        "a network ledger moves in one class only");
}

// SC-ST-06: a pool's share class count never decreases and grows by at most one per call.
rule stScClassCountStepsByOne(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);

    mathint before = ghostScClassShareClassCount32;

    f(e, args);

    assert(ghostScClassShareClassCount32 == before || ghostScClassShareClassCount32 == before + 1,
        "the share class count stays or rises by one per call");
}

// SC-ST-07: a share class's salt never changes once set.
rule stScClassSaltIsWriteOnce(env e, method f, calldataarg args, bytes16 c)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    // A set salt sits on a class the counter has reached, so no mint rewrites it.
    setupShareClassManagerMultiClassValidState(e);

    bytes32 saltBefore = ghostScClassMetadataSalt[c];

    f(e, args);

    assert(saltBefore != to_bytes32(0) => ghostScClassMetadataSalt[c] == saltBefore,
        "a set class salt is never rewritten or cleared");
}
