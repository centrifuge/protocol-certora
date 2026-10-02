import "single/MultiAdapter_valid_state.spec";
import "setup/MultiAdapter_refund.spec";

// --- high_level ---

// MA-HL-25: a send refunds any ETH its adapters were not paid, and pays any shortfall from its own balance.
rule hlMaSendRefundsTheSurplusAndKeepsNoEth(env e, uint16 cid, bytes payload, uint256 gasLimit) {

    setupMultiAdapterValidState(e);
    setupMultiAdapterRefund(e);
    require(!_RefundSink.rejectMode, "SCOPE: a refund address that accepts ETH");

    mathint routeBalanceBefore = nativeBalances[_MultiAdapter];
    mathint refundBalanceBefore = nativeBalances[_RefundSink];
    mathint paidBefore = ghostMaFaceSendValueSum;

    _MultiAdapter.send(e, cid, payload, gasLimit, _RefundSink);

    mathint paid = ghostMaFaceSendValueSum - paidBefore;
    mathint value = e.msg.value;

    assert(value > paid => nativeBalances[_MultiAdapter] == routeBalanceBefore
            && nativeBalances[_RefundSink] == refundBalanceBefore + value - paid,
        "an overpaid send refunds the whole surplus and keeps none");
    assert(value <= paid => nativeBalances[_RefundSink] == refundBalanceBefore
            && nativeBalances[_MultiAdapter] == routeBalanceBefore + value - paid,
        "an underpaid send refunds nothing and covers the gap itself");
}

// --- reachability ---

// MA-RC-19: a refund address that refuses the surplus can undo a send after its adapter was paid.
rule rcMaRejectingRefundAddressUndoesTheWholeFanOutIsReachable(env e, uint16 cid, bytes payload, uint256 gasLimit) {

    // Plain setup: a send under the valid state does not ground.
    setupMultiAdapter(e);
    setupMultiAdapterRefund(e);
    require(ghostMaActiveListLength8 == 1, "SCOPE: a one-adapter route");
    require(ghostMaActiveSetSessionId16 == ghostMaActiveSessionId16 && ghostMaActiveSessionId16 != 0,
        "PROVED: clearedActiveSetEmpty, activeSetSessionCurrentOrCleared (MultiAdapter)");
    require(nativeBalances[ghostMaActiveList[0]] + e.msg.value <= max_uint256,
        "SAFE: the paid adapter's balance stays below 2^256");
    require(_RefundSink.rejectMode, "SCOPE: a refund address that refuses ETH");
    require(payload.length == 32, "SCOPE: a one-word message");

    mathint dispatchCountBefore = ghostMaFaceSendCount;

    _MultiAdapter.send@withrevert(e, cid, payload, gasLimit, _RefundSink);
    bool reverted = lastReverted;

    satisfy(reverted && ghostMaFaceSendCount == dispatchCountBefore + 1 && e.msg.value > ghostMaFaceLastQuote256,
        "a refusing refund address can revert a send after its dispatch");
}
