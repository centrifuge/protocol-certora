// MultiAdapter, refund lane. Setup: a compiled refund sink and native balances.

// Own setup: RefundSink and native balances; only refund_properties.conf compiles the sink, with optimistic_fallback.

import "MultiAdapter_base.spec";

// UNSAFE: the refund address is the sink, re-entry goes unanalysed.
using RefundSink as _RefundSink;

function requireMaLiveAdapterApart(mathint i) {
    require(i >= ghostMaActiveListLength8
        || (ghostMaActiveList[i] != _MultiAdapter && ghostMaActiveList[i] != _RefundSink),
        "SCOPE: no adapter is the route or the refund address");
}

// Unrolled to eight: a quantified setup does not ground a send.
function setupMultiAdapterRefund(env e) {
    require(e.msg.sender != _RefundSink, "SCOPE: the sender is not the refund address");
    requireMaLiveAdapterApart(0);
    requireMaLiveAdapterApart(1);
    requireMaLiveAdapterApart(2);
    requireMaLiveAdapterApart(3);
    requireMaLiveAdapterApart(4);
    requireMaLiveAdapterApart(5);
    requireMaLiveAdapterApart(6);
    requireMaLiveAdapterApart(7);
    require(nativeBalances[_MultiAdapter] + e.msg.value <= max_uint256
        && nativeBalances[_RefundSink] + e.msg.value <= max_uint256,
        "SAFE: no balance overflows, ETH supply is far below 2^256");
}
