import "setup/HubRegistry_multi_pool.spec";
import "../../../shared/models/StdHubPolicy_cvl.spec";

// --- state_transitions ---

// HR-ST-07: no call changes the currency, policy or bridging hook of two pools at once.
rule stHrPoolRowIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);
    require(HR_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint currencyPBefore = ghostHrPoolCurrency128[p];
    address policyPBefore = ghostHrPoolPolicy[p];
    mathint noncePBefore = ghostHrPoolPolicyNonce64[p];
    address hookPBefore = ghostHrPoolBridgingHook[p];
    mathint currencyQBefore = ghostHrPoolCurrency128[q];
    address policyQBefore = ghostHrPoolPolicy[q];
    mathint nonceQBefore = ghostHrPoolPolicyNonce64[q];
    address hookQBefore = ghostHrPoolBridgingHook[q];

    f(e, args);

    assert(ghostHrPoolCurrency128[p] != currencyPBefore
        || ghostHrPoolPolicy[p] != policyPBefore
        || ghostHrPoolPolicyNonce64[p] != noncePBefore
        || ghostHrPoolBridgingHook[p] != hookPBefore
        => ghostHrPoolCurrency128[q] == currencyQBefore
            && ghostHrPoolPolicy[q] == policyQBefore
            && ghostHrPoolPolicyNonce64[q] == nonceQBefore
            && ghostHrPoolBridgingHook[q] == hookQBefore,
        "touching one pool's settings leaves every other pool's untouched");
}

// HR-ST-08: no call changes manager rights on two pools at once.
rule stHrManagerRightsArePerPool(env e, method f, calldataarg args, uint64 p, uint64 q,
    address who1, address who2) filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);
    require(HR_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    bool grantedPBefore = ghostHrPoolManager[p][who1];
    bool grantedQBefore = ghostHrPoolManager[q][who2];

    f(e, args);

    assert(ghostHrPoolManager[p][who1] != grantedPBefore
        => ghostHrPoolManager[q][who2] == grantedQBefore,
        "manager rights move in one pool only");
}

// HR-ST-09: no call changes the request manager of two pools on one network at once.
rule stHrRequestManagerIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q, uint16 cid)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);
    require(HR_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    address wiredPBefore = ghostHrPoolHubRequestManager[p][cid];
    address wiredQBefore = ghostHrPoolHubRequestManager[q][cid];

    f(e, args);

    assert(ghostHrPoolHubRequestManager[p][cid] != wiredPBefore
        => ghostHrPoolHubRequestManager[q][cid] == wiredQBefore,
        "a call re-routes a network's request manager in one pool only");
}

// HR-ST-10: no call changes pending authorizations of two pools at once.
rule stHrPendingAuthIsPerPool(env e, method f, calldataarg args, uint64 p, uint64 q,
    address pol1, uint64 n1, bytes32 h1, address pol2, uint64 n2, bytes32 h2)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);
    require(HR_POOL_PAIR(p, q), "SCOPE: two distinct pools");

    mathint pendingPBefore = ghostHrAuthorizedAfter48[ghostHrAuthId[p][pol1][n1][h1]];
    mathint pendingQBefore = ghostHrAuthorizedAfter48[ghostHrAuthId[q][pol2][n2][h2]];

    f(e, args);

    assert(ghostHrAuthorizedAfter48[ghostHrAuthId[p][pol1][n1][h1]] != pendingPBefore
        => ghostHrAuthorizedAfter48[ghostHrAuthId[q][pol2][n2][h2]] == pendingQBefore,
        "a call moving one pool's pending grants leaves another pool's alone");
}

// HR-ST-11: manager rights are granted only on a registered pool or when creating it.
rule stHrOperatorSeatNeedsItsOwnPoolsCurrency(env e, method f, calldataarg args, uint64 p, address who)
    filtered { f -> !EXCLUDED_FUNCTION_HR(f) } {

    setupHubRegistry(e);

    bool seatBefore = ghostHrPoolManager[p][who];
    mathint currencyBefore = ghostHrPoolCurrency128[p];

    f(e, args);

    assert(!seatBefore && ghostHrPoolManager[p][who] && currencyBefore == 0
        => ghostHrPoolCurrency128[p] != 0,
        "a currencyless pool gains a manager only if it gains a currency");
}
