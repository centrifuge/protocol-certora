// MessageDispatcher, single lanes. Setup: the gateway face, reading no message.

// Own setup: _.send reads no message, for the four single lanes; native and wire summarize the same send.

import "MessageDispatcher_base.spec";

methods {
    function _.send(uint16 centrifugeId, bytes message, bool unpaidMode, address refund) external with (env e)
        => gatewaySendMdCVL(e, calledContract, centrifugeId, unpaidMode, refund) expect void UNRESOLVED;
}
