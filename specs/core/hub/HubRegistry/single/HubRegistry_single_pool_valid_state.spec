import "../setup/HubRegistry_single_pool.spec";
import "../../../../shared/models/StdHubPolicy_cvl.spec";

function setupHubRegistryValidState(env e) {
    setupHubRegistry(e);
    requireInvariant assetDecimalsCapped(e);
    requireInvariant unregisteredAssetHasZeroDecimals(e);
    requireInvariant nullAssetNeverRegistered(e);
    requireInvariant poolCurrencyRegistered(e);
    requireInvariant managerImpliesPoolExists(e);
    requireInvariant zeroAddressNeverManager(e);
    requireInvariant policyImpliesPoolExists(e);
    requireInvariant nonceImpliesPoolExists(e);
    requireInvariant policyImpliesNonzeroNonce(e);
    requireInvariant bridgingHookImpliesPoolExists(e);
    requireInvariant requestManagerImpliesPoolExists(e);
    requireInvariant pendingAuthAboveEnvFloor(e);
    requireInvariant pendingNeverUnderNullPolicy(e);
    requireInvariant pendingNeverUnderZeroNonce(e);
    requireInvariant pendingNeverAheadOfNonce(e);
    requireInvariant pendingUnderCurrentNonceMatchesPolicy(e);
    requireInvariant nullAuthIdNeverPending(e);
}

// HR-VS-01: no asset has more than 18 decimals.
invariant assetDecimalsCapped(env e)
    forall mathint a. ghostHrAssetDecimals8[a] <= MAX_DECIMALS_CVL()
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-02: an unregistered asset has zero decimals.
invariant unregisteredAssetHasZeroDecimals(env e)
    forall mathint a. !ghostHrAssetRegistered[a] => ghostHrAssetDecimals8[a] == 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-03: the empty asset id is never registered.
invariant nullAssetNeverRegistered(env e)
    !ghostHrAssetRegistered[0]
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-04: the pool's denomination currency is always a registered asset.
invariant poolCurrencyRegistered(env e)
    ghostHrCurrency128 != 0 => ghostHrAssetRegistered[ghostHrCurrency128]
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-05: nobody holds manager rights on a pool before that pool is created.
invariant managerImpliesPoolExists(env e)
    forall address who. ghostHrManager[who] => ghostHrCurrency128 != 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-06: the zero address is never a pool manager.
invariant zeroAddressNeverManager(env e)
    !ghostHrManager[0]
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-07: a policy is only ever installed on a created pool.
invariant policyImpliesPoolExists(env e)
    ghostHrPolicy != 0 => ghostHrCurrency128 != 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-08: the policy nonce only ever advances on a created pool.
invariant nonceImpliesPoolExists(env e)
    ghostHrPolicyNonce64 != 0 => ghostHrCurrency128 != 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-09: an installed policy always has a non-zero policy nonce.
invariant policyImpliesNonzeroNonce(env e)
    ghostHrPolicy != 0 => ghostHrPolicyNonce64 >= 1
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-10: a bridging hook is only ever wired to a created pool.
invariant bridgingHookImpliesPoolExists(env e)
    ghostHrBridgingHook != 0 => ghostHrCurrency128 != 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-11: a hub request manager, on any network, is only ever wired to a created pool.
invariant requestManagerImpliesPoolExists(env e)
    forall uint16 cid. ghostHrHubRequestManager[cid] != 0 => ghostHrCurrency128 != 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-12: a pending authorization never matures before the earliest possible block time.
invariant pendingAuthAboveEnvFloor(env e)
    forall bytes32 id.
        ghostHrAuthorizedAfter48[id] != 0 => ghostHrAuthorizedAfter48[id] > MIN_BLOCK_TIMESTAMP()
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-13: no authorization is ever scheduled while a pool has no policy installed.
invariant pendingNeverUnderNullPolicy(env e)
    forall uint64 p. forall uint64 n. forall bytes32 h.
        ghostHrAuthorizedAfter48[ghostHrAuthId[p][0][n][h]] == 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-14: no authorization is pending under policy nonce zero.
invariant pendingNeverUnderZeroNonce(env e)
    forall uint64 p. forall address pol. forall bytes32 h.
        ghostHrAuthorizedAfter48[ghostHrAuthId[p][pol][0][h]] == 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) {
    requireInvariant policyImpliesNonzeroNonce(e);
    requireInvariant pendingNeverUnderNullPolicy(e);
    SETUP_HR(e, eFunc);
} }

// HR-VS-15: no authorization is pending under a future policy nonce.
invariant pendingNeverAheadOfNonce(env e)
    forall address pol. forall uint64 n. forall bytes32 h. n > ghostHrPolicyNonce64
        => ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][pol][n][h]] == 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }

// HR-VS-16: at the current nonce, all pending authorizations belong to the installed policy.
invariant pendingUnderCurrentNonceMatchesPolicy(env e)
    forall address pol. forall bytes32 h. pol != ghostHrPolicy
        => ghostHrAuthorizedAfter48[ghostHrAuthId[ghostPoolA64][pol][ghostHrPolicyNonce64][h]] == 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) {
    requireInvariant pendingNeverAheadOfNonce(e);
    SETUP_HR(e, eFunc);
} }

// HR-VS-17: the empty authorization id is never pending.
invariant nullAuthIdNeverPending(env e)
    ghostHrAuthorizedAfter48[to_bytes32(0)] == 0
filtered { f -> !EXCLUDED_FUNCTION_HR(f) } { preserved with (env eFunc) { SETUP_HR(e, eFunc); } }
