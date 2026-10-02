// MessageDispatcher, native lane. Setup: the ETH a send takes in and the hash it sends.

// Own setup: _.send also hashes messages up to 91 bytes; single and wire give the same send their own summaries.

import "MessageDispatcher_entries.spec";

methods {
    function _.send(uint16 centrifugeId, bytes message, bool unpaidMode, address refund) external with (env e)
        => gatewaySendNativeMdCVL(e, calledContract, centrifugeId, message, unpaidMode, refund)
        expect void UNRESOLVED;
}

// UNSAFE: a refund callee takes ETH, never re-enters or force-sends.

persistent ghost bytes32 ghostGwLastSendHash;

// SAFE: only messages up to an asset report's 91 bytes are hashed.
function gatewaySendNativeMdCVL(env e, address callee, uint16 centrifugeId, bytes message, bool unpaidMode,
    address refund) {
    gatewaySendMdCVL(e, callee, centrifugeId, unpaidMode, refund);
    if (message.length <= 91) {
        ghostGwLastSendHash = keccak256(message);
    }
}

function setupMessageDispatcherNative(env e, address refund) {
    setupMessageDispatcher(e);
    require(_MessageDispatcher.gateway() != _MessageDispatcher && _MessageDispatcher.hubHandler() != _MessageDispatcher
            && _MessageDispatcher.envoy() != _MessageDispatcher && _MessageDispatcher.spokeHandler() != _MessageDispatcher
            && refund != _MessageDispatcher,
        "SAFE: no neighbour or refund is the dispatcher");
    require(nativeBalances[_MessageDispatcher] + e.msg.value <= max_uint256, "SAFE: the ETH supply fits in a word");
}
