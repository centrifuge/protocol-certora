// MessageDispatcher. Setup: wiring pointers, ward set and neighbour recorders.

import "../../../../shared/env.spec";
import "../../../../shared/bytes_slice.spec";
import "../../../spoke/SpokeHandler/setup/SpokeHandler_cvl.spec";
import "../../../hub/HubHandler/setup/HubHandler_cvl.spec";
import "../../../utils/Envoy/setup/Envoy_cvl.spec";
import "../../../../shared/models/Root_cvl.spec";
import "../../MultiAdapter/setup/MultiAdapter_cvl.spec";

using MessageDispatcher as _MessageDispatcher;

persistent ghost mathint ghostGwSendCount {
    init_state axiom ghostGwSendCount == 0;
    axiom ghostGwSendCount >= 0;
}
persistent ghost address ghostGwLastSendCallee;
persistent ghost mathint ghostGwLastSendCid16;
persistent ghost bool ghostGwLastSendUnpaid;
persistent ghost address ghostGwLastSendRefund;
persistent ghost mathint ghostGwLastSendValue;

// UNSAFE: delivery, payment and the gateway's use of ETH unanalysed.
function gatewaySendMdCVL(env e, address callee, uint16 centrifugeId, bool unpaidMode, address refund) {
    ghostGwSendCount = ghostGwSendCount + 1;
    ghostGwLastSendCallee = callee;
    ghostGwLastSendCid16 = centrifugeId;
    ghostGwLastSendUnpaid = unpaidMode;
    ghostGwLastSendRefund = refund;
    ghostGwLastSendValue = e.msg.value;
}

methods {
    function wards(address) external returns (uint256) envfree;
    function envoy() external returns (address) envfree;
    function gateway() external returns (address) envfree;
    function multiAdapter() external returns (address) envfree;
    function spokeHandler() external returns (address) envfree;
    function hubHandler() external returns (address) envfree;
    function localCentrifugeId() external returns (uint16) envfree;

    function BytesSliceHarness.stringToBytes32Pure(string source) external returns (bytes32) envfree;
    // TRUSTED: a hand-checked twin, as the cast leaves sends unresolved.
    function CastLib.toBytes32(string memory source) internal returns (bytes32) => stringToBytes32CVL(source);
}

function stringToBytes32CVL(string source) returns bytes32 {
    return _BytesSlice.stringToBytes32Pure(source);
}

// SCOPE: loop_iter 8 is MAX_ADAPTER_COUNT, longer lists are cut.

// SAFE: the key literals MessageDispatcher.file spells inline.
definition FILE_ENVOY_MD_CVL() returns bytes32 =
    to_bytes32(0x656e766f79000000000000000000000000000000000000000000000000000000);

definition FILE_GATEWAY_MD_CVL() returns bytes32 =
    to_bytes32(0x6761746577617900000000000000000000000000000000000000000000000000);

definition FILE_MULTI_ADAPTER_MD_CVL() returns bytes32 =
    to_bytes32(0x6d756c7469416461707465720000000000000000000000000000000000000000);

definition FILE_SPOKE_HANDLER_MD_CVL() returns bytes32 =
    to_bytes32(0x73706f6b6548616e646c65720000000000000000000000000000000000000000);

definition FILE_HUB_HANDLER_MD_CVL() returns bytes32 =
    to_bytes32(0x68756248616e646c657200000000000000000000000000000000000000000000);

definition EXCLUDED_FUNCTION_MD(method f) returns bool =
    f.isView || f.isPure || f.isFallback;

definition SEND_ENTRY_MD(method f) returns bool =
    !EXCLUDED_FUNCTION_MD(f) && f.selector != sig:file(bytes32,address).selector
        && f.selector != sig:rely(address).selector && f.selector != sig:deny(address).selector;

function setupMessageDispatcher(env e) {
    require(e.msg.sender != _MessageDispatcher, "SAFE: the dispatcher never calls itself");
}

definition DOWNSTREAM_CALLS() returns mathint =
    ghostShCallCount + ghostHhCallCount + ghostEnCallCount + ghostSaCallCount
        + ghostGwSendCount;
