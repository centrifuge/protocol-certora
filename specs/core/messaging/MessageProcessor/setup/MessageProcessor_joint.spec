// MessageProcessor, joint lane. Setup: the real dispatcher and MessageLib's encoder.

// Own setup: the real MessageDispatcher and MessageCodecHarness; only joint_properties.conf compiles them.

import "MessageProcessor_base.spec";

using MessageDispatcher as _MessageDispatcher;
using MessageCodecHarness as _Codec;

methods {
    function _MessageDispatcher.localCentrifugeId() external returns (uint16) envfree;
    function _Codec.serializeInitiateTransferShares(uint16, uint64, bytes16, bytes32, uint128, uint128, uint128,
        bytes32) external returns (bytes) envfree;
    function _Codec.serializeSetPoolAdapters(uint64, uint8, uint16, bytes32[]) external returns (bytes) envfree;
}

function setupMessageProcessorJoint(env eDispatch, env eProcess) {
    setupMessageProcessor(eProcess);
    require(eDispatch.msg.sender != _MessageDispatcher && eDispatch.msg.sender != _MessageProcessor,
        "SCOPE: neither router calls itself or the other");
    require(eProcess.msg.sender != _MessageDispatcher, "SCOPE: neither router calls itself or the other");
}
