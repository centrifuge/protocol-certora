// StdHubPolicy. Model: the delay and enforce answers, for scenes not compiling it.

methods {
    // UNSAFE: one delay per caller and calldata, and it never reverts.
    function _.authorizationDelay(uint64 poolId, address caller, bytes data) external
        => policyAuthorizationDelayCVL(calledContract, poolId, caller, data) expect uint48;

    // UNSAFE: one free refusal bit per policy, no authorization consumed.
    function _.enforce(uint64 poolId, address caller, bytes data) external
        => policyEnforceCVL(calledContract, poolId, caller, data) expect void UNRESOLVED;
}

persistent ghost mapping(address => bool) ghostPolicyRefuses;

persistent ghost mathint ghostPolicyEnforceCount {
    init_state axiom ghostPolicyEnforceCount == 0;
    axiom ghostPolicyEnforceCount >= 0;
}
persistent ghost address ghostPolicyLastCallee;
persistent ghost uint64 ghostPolicyLastPool64;
persistent ghost address ghostPolicyLastCaller;
persistent ghost bytes32 ghostPolicyLastDataHash;

function policyEnforceCVL(address policy, uint64 poolId, address caller, bytes data) {
    if (ghostPolicyRefuses[policy]) {
        revert("PolicyRefuses");
    }
    ghostPolicyEnforceCount = ghostPolicyEnforceCount + 1;
    ghostPolicyLastCallee = policy;
    ghostPolicyLastPool64 = poolId;
    ghostPolicyLastCaller = caller;
    ghostPolicyLastDataHash = keccak256(data);
}

persistent ghost mapping(address => mapping(bytes32 => mathint)) ghostPolicyDelay48 {
    init_state axiom forall address c. forall bytes32 h. ghostPolicyDelay48[c][h] == 0;
    axiom forall address c. forall bytes32 h.
        ghostPolicyDelay48[c][h] >= 0 && ghostPolicyDelay48[c][h] <= max_uint48;
}

persistent ghost address ghostPolicyDelayCallee;
persistent ghost uint64 ghostPolicyDelayPool64;

function policyAuthorizationDelayCVL(address policy, uint64 poolId, address caller, bytes data) returns uint48 {
    ghostPolicyDelayCallee = policy;
    ghostPolicyDelayPool64 = poolId;
    return require_uint48(ghostPolicyDelay48[caller][keccak256(data)]);
}
