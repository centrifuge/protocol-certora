import "../setup/ShareClassManager_single_pool.spec";
import "../../HubRegistry/setup/HubRegistry_cvl.spec";

function setupShareClassManagerValidState(env e) {
    setupShareClassManager(e);
    requireInvariant shareClassExistsIffCounted(e);
    requireInvariant shareClassExistsIffSaltSet(e);
    requireInvariant uncreatedClassNetworkIssuancesZero(e);
    requireInvariant uncreatedClassNetworkRevocationsZero(e);
    requireInvariant uncreatedClassPriceZero(e);
    requireInvariant uncreatedClassPriceStampZero(e);
    requireInvariant existingClassPoolRegistered(e);
    requireInvariant totalIssuanceIsNetworkNetSum(e);
    requireInvariant priceStampNotFuture(e);
    requireInvariant saltPrefixIsPool(e);
    requireInvariant classSaltConsumed(e);
    requireInvariant nullSaltNeverConsumed(e);
    requireInvariant negativeNetworkCountMatchesTheShortNetworks(e);
}

// SC-VS-01: a pool's first share class exists exactly when the pool has created a class.
invariant shareClassExistsIffCounted(env e)
    ghostScShareClassIds <=> ghostScShareClassCount32 >= 1
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-02: a share class exists exactly when its salt is set.
invariant shareClassExistsIffSaltSet(env e)
    ghostScShareClassIds <=> ghostScMetadataSalt != to_bytes32(0)
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-03: a share class never created has no issuance on any network.
invariant uncreatedClassNetworkIssuancesZero(env e)
    forall uint16 cid. !ghostScShareClassIds => ghostScIssuances256[cid] == 0
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-04: a share class never created has no revocations on any network.
invariant uncreatedClassNetworkRevocationsZero(env e)
    forall uint16 cid. !ghostScShareClassIds => ghostScRevocations256[cid] == 0
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-05: a share class never created has no share price.
invariant uncreatedClassPriceZero(env e)
    !ghostScShareClassIds => ghostScPricePoolPerShare128 == 0
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-06: a share class never created has no price timestamp.
invariant uncreatedClassPriceStampZero(env e)
    !ghostScShareClassIds => ghostScPriceComputedAt64 == 0
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-07: a share class only exists inside a pool the hub registry knows.
invariant existingClassPoolRegistered(env e)
    ghostScShareClassIds => ghostHrCurrency128 != 0
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-08: a class's total supply is the sum of every network's net issuance.
invariant totalIssuanceIsNetworkNetSum(env e)
    SC_TOTAL_ISSUANCE() == SC_NET_ISSUANCE_SUM()
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-09: price timestamps never run ahead of the chain clock.
invariant priceStampNotFuture(env e)
    ghostScPriceComputedAt64 <= e.block.timestamp
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-10: every share class salt starts with its pool's id.
invariant saltPrefixIsPool(env e)
    ghostScMetadataSalt != to_bytes32(0)
        => (ghostScMetadataSalt >> 192) == to_bytes32(assert_uint256(ghostPoolA64))
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-11: a share class's salt is always marked as used.
invariant classSaltConsumed(env e)
    ghostScMetadataSalt != to_bytes32(0) => ghostScSalts[ghostScMetadataSalt]
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-21: the empty salt is never marked used.
invariant nullSaltNeverConsumed(env e)
    !ghostScSalts[to_bytes32(0)]
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }

// SC-VS-22: the negative-network count equals the networks that revoked more than they issued.
invariant negativeNetworkCountMatchesTheShortNetworks(env e)
    ghostScNegativeNetworkCount32 == SC_NEGATIVE_NETWORK_CARDINALITY()
filtered { f -> !EXCLUDED_FUNCTION_SC(f) } { preserved with (env eFunc) { SETUP_SC(e, eFunc); } }
