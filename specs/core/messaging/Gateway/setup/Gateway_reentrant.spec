// Gateway, reentrant lane. Setup: the real flush, an adapter repaying from its send.

// Own setup: a linked ReentrantAdapter repaying from its send; base's IAdapter model would summarize that send away.

import "../../../../shared/env.spec";
import "../../../../shared/bytes_slice.spec";
import "Gateway_message_model.spec";
import "Gateway_batching.spec";
import "Gateway_callback.spec";

using Gateway as _Gateway;
using ReentrantAdapter as _ReentrantAdapter;
using RefundSink as _RefundSink;

methods {
    function _Gateway.wards(address) external returns (uint256) envfree;
    function _Gateway.adapter() external returns (address) envfree;
    function _ReentrantAdapter.quote() external returns (uint256) envfree;
    function _RefundSink.rejectMode() external returns (bool) envfree;

    function _.paused() external => gwReentrantPausedCVL() expect bool UNRESOLVED;
}

definition GA_IS_BATCHING() returns bool = _Gateway.isBatching;
definition GA_IS_SENDING_BATCH() returns bool = _Gateway._isSendingBatch;
definition GA_BATCHER() returns address = _Gateway._batcher;

persistent ghost bool ghostGwPaused;
persistent ghost bool ghostGwLastPauseReadMidFlush;

function gwReentrantPausedCVL() returns bool {
    ghostGwLastPauseReadMidFlush = GA_IS_SENDING_BATCH();
    return ghostGwPaused;
}
