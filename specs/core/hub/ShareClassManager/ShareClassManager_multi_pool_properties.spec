import "setup/ShareClassManager_multi_pool.spec";
import "../HubRegistry/setup/HubRegistry_cvl.spec";

// --- valid_state ---

function setupShareClassManagerMultiPoolValidState(env e) {
    setupShareClassManager(e);
    requireInvariant poolSaltPrefixIsOwnPool(e);
}

function SETUP_SC_MP(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupShareClassManagerMultiPoolValidState(e);
}

// SC-VS-14: a pool's share class salt always begins with that pool's own id.
invariant poolSaltPrefixIsOwnPool(env e)
    (ghostScPoolMetadataSalt[ghostPoolA64] != to_bytes32(0)
        => (ghostScPoolMetadataSalt[ghostPoolA64] >> 192) == to_bytes32(assert_uint256(ghostPoolA64)))
    && (ghostScPoolMetadataSalt[ghostPoolB64] != to_bytes32(0)
        => (ghostScPoolMetadataSalt[ghostPoolB64] >> 192) == to_bytes32(assert_uint256(ghostPoolB64)))
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC_MP(e, eFunc); } }

// --- state_transitions ---

// SC-ST-02: a change to one pool's share class leaves another pool's share class untouched.
rule stScClassRowIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);
    require(SC_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint countPBefore = ghostScPoolShareClassCount32[p];
    bool idsPBefore = ghostScPoolShareClassIds[p];
    bytes32 saltPBefore = ghostScPoolMetadataSalt[p];
    mathint issuancesPBefore = ghostScPoolTotalIssuances256[p];
    mathint revocationsPBefore = ghostScPoolTotalRevocations256[p];
    mathint negativePBefore = ghostScPoolNegativeNetworkCount32[p];
    mathint pricePBefore = ghostScPoolPricePoolPerShare128[p];
    mathint stampPBefore = ghostScPoolPriceComputedAt64[p];
    mathint countQBefore = ghostScPoolShareClassCount32[q];
    bool idsQBefore = ghostScPoolShareClassIds[q];
    bytes32 saltQBefore = ghostScPoolMetadataSalt[q];
    mathint issuancesQBefore = ghostScPoolTotalIssuances256[q];
    mathint revocationsQBefore = ghostScPoolTotalRevocations256[q];
    mathint negativeQBefore = ghostScPoolNegativeNetworkCount32[q];
    mathint priceQBefore = ghostScPoolPricePoolPerShare128[q];
    mathint stampQBefore = ghostScPoolPriceComputedAt64[q];

    f(e, args);

    assert(ghostScPoolShareClassCount32[p] != countPBefore || ghostScPoolShareClassIds[p] != idsPBefore
        || ghostScPoolMetadataSalt[p] != saltPBefore || ghostScPoolTotalIssuances256[p] != issuancesPBefore
        || ghostScPoolTotalRevocations256[p] != revocationsPBefore
        || ghostScPoolNegativeNetworkCount32[p] != negativePBefore
        || ghostScPoolPricePoolPerShare128[p] != pricePBefore || ghostScPoolPriceComputedAt64[p] != stampPBefore
        => ghostScPoolShareClassCount32[q] == countQBefore && ghostScPoolShareClassIds[q] == idsQBefore
            && ghostScPoolMetadataSalt[q] == saltQBefore && ghostScPoolTotalIssuances256[q] == issuancesQBefore
            && ghostScPoolTotalRevocations256[q] == revocationsQBefore
            && ghostScPoolNegativeNetworkCount32[q] == negativeQBefore
            && ghostScPoolPricePoolPerShare128[q] == priceQBefore
            && ghostScPoolPriceComputedAt64[q] == stampQBefore,
        "share class state moves in one pool only");
}

// SC-ST-03: a pool's share changes on a network never touch another pool's shares there.
rule stScNetworkLedgerIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_SC(f) } {

    setupShareClassManager(e);
    require(SC_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint issuancesPBefore = ghostScPoolIssuances256[p][cid];
    mathint revocationsPBefore = ghostScPoolRevocations256[p][cid];
    mathint issuancesQBefore = ghostScPoolIssuances256[q][cid];
    mathint revocationsQBefore = ghostScPoolRevocations256[q][cid];

    f(e, args);

    assert(ghostScPoolIssuances256[p][cid] != issuancesPBefore
        || ghostScPoolRevocations256[p][cid] != revocationsPBefore
        => ghostScPoolIssuances256[q][cid] == issuancesQBefore
            && ghostScPoolRevocations256[q][cid] == revocationsQBefore,
        "a network ledger moves in one pool only");
}
