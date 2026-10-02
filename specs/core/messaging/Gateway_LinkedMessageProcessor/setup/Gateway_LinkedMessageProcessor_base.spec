// Gateway_LinkedMessageProcessor. Setup: the real MessageProcessor and GasService, pause and forwarding models.

import "../../../../shared/env.spec";
import "../../../../shared/bytes_slice.spec";
import "../../Gateway/setup/Gateway_batching.spec";

using Gateway as _Gateway;
using MessageProcessor as _MessageProcessor;

methods {
    function _Gateway.wards(address) external returns (uint256) envfree;

    function _.paused() external => ghostGwPaused expect bool UNRESOLVED;
}

// SAFE: mainnet's network id (MessageLib.sol:74).
definition MAINNET_CENTRIFUGE_ID_GW() returns uint16 = 1;

// SAFE: message types run from 1 to 24 (MessageLib.sol:11-47).
definition UNKNOWN_TYPE_GW(uint8 kind) returns bool = kind == 0 || kind > 24;

// SAFE: types that must come from their pool's home network.
definition POOL_HOMED_TYPE_GW(uint8 kind) returns bool =
    kind == 4 || (kind >= 5 && kind <= 24 && kind != 10 && kind != 14 && kind != 15 && kind != 16 && kind != 19);

persistent ghost bool ghostGwPaused;

persistent ghost mathint ghostGwForwardCount {
    init_state axiom ghostGwForwardCount == 0;
    axiom ghostGwForwardCount >= 0;
}
persistent ghost uint16 ghostGwLastForwardCid16;

// UNSAFE: _safeProcess is cut, keeping only its budget underflow.
function gwForwardCVL(uint16 centrifugeId, uint128 gasLimit, uint128 failureGasReserve) {
    if (gasLimit < failureGasReserve) {
        revert("the capped budget underflows");
    }
    ghostGwForwardCount = ghostGwForwardCount + 1;
    ghostGwLastForwardCid16 = centrifugeId;
}
