// EscrowFactory. Setup: the harness link and its trusted deploy wiring.

import "../../../../../shared/env.spec";

using EscrowFactoryHarness as _PoolEscrowFactory;

methods {
    // Alias-qualified: a bare entry would bind to the conf's main contract.
    function _PoolEscrowFactory.wards(address) external returns (uint256) envfree;
    function _PoolEscrowFactory.spoke() external returns (address) envfree;
    function _PoolEscrowFactory.root() external returns (address) envfree;
}

definition EXCLUDED_FUNCTION_PEF(method f) returns bool =
    f.isView || f.isPure || f.isFallback;

// SAFE: the file key "spoke" as left-aligned ASCII.
definition FILE_KEY_SPOKE_PEF_CVL() returns bytes32 =
    to_bytes32(0x73706f6b65000000000000000000000000000000000000000000000000000000);

function setupPoolEscrowFactory(env e) {
    setupEnv(e);
    require(e.msg.sender != _PoolEscrowFactory, "SAFE: the factory never calls itself");
    require(_PoolEscrowFactory.spoke != 0, "TRUSTED: spoke wired at deploy, never cleared");
    require(_PoolEscrowFactory.root != _PoolEscrowFactory && _PoolEscrowFactory.spoke != _PoolEscrowFactory,
        "TRUSTED: governance never sets the factory as root or spoke");
}
