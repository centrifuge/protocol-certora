// EscrowFactory, wiring lane. Setup: the real factory, child ward calls in order.

// Own setup: plain newEscrow, child rely and deny recorded in order; base runs the harness on a linked escrow.

import "../../../../../shared/env.spec";

using EscrowFactory as _PoolEscrowFactory;

methods {
    function _PoolEscrowFactory.root() external returns (address) envfree;
    function _PoolEscrowFactory.spoke() external returns (address) envfree;

    // UNSAFE: the child's auth and ward writes dropped, calls recorded.
    function _.rely(address who) external => pefWardCallCVL(calledContract, who, true) expect void UNRESOLVED;
    function _.deny(address who) external => pefWardCallCVL(calledContract, who, false) expect void UNRESOLVED;
}

persistent ghost mathint ghostPefN;
persistent ghost mapping(mathint => address) ghostPefTarget;
persistent ghost mapping(mathint => address) ghostPefWho;
persistent ghost mapping(mathint => bool) ghostPefIsRely;

function pefWardCallCVL(address target, address who, bool isRely) {
    ghostPefTarget[ghostPefN] = target;
    ghostPefWho[ghostPefN] = who;
    ghostPefIsRely[ghostPefN] = isRely;
    ghostPefN = ghostPefN + 1;
}

function setupPoolEscrowFactoryWiring(env e) {
    setupEnv(e);
    require(ghostPefN == 0, "SAFE: the ward call record starts empty");
}
