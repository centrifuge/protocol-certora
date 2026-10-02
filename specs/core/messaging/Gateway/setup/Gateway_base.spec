// Gateway. Setup: pause, processor, adapter and token models, and the entry filter.

import "../../../../shared/env.spec";
import "../../../../shared/bytes_slice.spec";
import "../../../../shared/models/IAdapter_cvl.spec";
import "../../../../shared/models/IMessageHandler_cvl.spec";
import "Gateway_message_model.spec";

using Gateway as _Gateway;
using RefundSink as _RefundSink;

methods {
    function _Gateway.wards(address) external returns (uint256) envfree;
    function _Gateway.manager(Gateway.PoolId, address) external returns (bool) envfree;
    function _Gateway.failedMessages(uint16, bytes32) external returns (uint256) envfree;
    function _Gateway.adapter() external returns (address) envfree;
    function _Gateway.processor() external returns (address) envfree;
    function _Gateway.messageGas() external returns (address) envfree;
    function _Gateway.localCentrifugeId() external returns (uint16) envfree;
    function _RefundSink.rejectMode() external returns (bool) envfree;

    function _.paused() external => gwPausedCVL() expect bool UNRESOLVED;

    // UNSAFE: the processor runs nothing, uses no gas, success is free.
    function ExcessivelySafeCallLib.excessivelySafeCall(address target, uint256 gasCap, uint256 value, uint16 maxCopy,
        bytes memory callData) internal returns (bool, bytes memory)
        => gwExcessivelySafeCallCVL(target, gasCap, value, maxCopy, callData);

    // SCOPE: a recovered ERC20 never refuses its transfer.
    function SafeTransferLib.safeTransfer(address token, address to, uint256 value) internal
        => gwTokenTransferCVL(token, to, value);

    // SCOPE: a recovered ERC6909 never reverts and returns a free flag.
    function _.transfer(address to, uint256 tokenId, uint256 amount) external
        => gwToken6909TransferCVL(calledContract, to, tokenId, amount) expect bool UNRESOLVED;
}

// SCOPE: withBatch and its flush out, re-entries run as own calls.
definition EXCLUDED_FUNCTION_GW(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    || f.selector == sig:_Gateway.withBatch(bytes,uint256,address).selector
    || f.selector == sig:_Gateway.withBatch(bytes,address).selector
    ;

definition TRAFFIC_ENTRY_GW(method f) returns bool =
    f.selector == sig:_Gateway.handle(uint16,bytes).selector
    || f.selector == sig:_Gateway.retry(uint16,bytes).selector
    || f.selector == sig:_Gateway.send(uint16,bytes,bool,address).selector
    || f.selector == sig:_Gateway.repay(uint16,bytes,address).selector
    ;

// SAFE: the names Gateway.file dispatches on (Gateway.sol:79-81).
definition FILE_MESSAGE_GAS_GW() returns bytes32 =
    to_bytes32(0x6d65737361676547617300000000000000000000000000000000000000000000);
definition FILE_PROCESSOR_GW() returns bytes32 =
    to_bytes32(0x70726f636573736f720000000000000000000000000000000000000000000000);
definition FILE_ADAPTER_GW() returns bytes32 =
    to_bytes32(0x6164617074657200000000000000000000000000000000000000000000000000);

// SAFE: twins of ETH_ADDRESS and MESSAGE_MAX_LENGTH.
definition ETH_ADDRESS_GW() returns address = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
definition MESSAGE_MAX_LENGTH_GW() returns mathint = 1000;

definition GA_IS_BATCHING() returns bool = _Gateway.isBatching;
definition GA_IS_SENDING_BATCH() returns bool = _Gateway._isSendingBatch;
definition GA_BATCHER() returns address = _Gateway._batcher;

persistent ghost bool ghostGwPaused;

persistent ghost mathint ghostGwPauseReads {
    init_state axiom ghostGwPauseReads == 0;
    axiom ghostGwPauseReads >= 0;
}

function gwPausedCVL() returns bool {
    ghostGwPauseReads = ghostGwPauseReads + 1;
    return ghostGwPaused;
}

persistent ghost mathint ghostGwEscCount {
    init_state axiom ghostGwEscCount == 0;
    axiom ghostGwEscCount >= 0;
}
persistent ghost address ghostGwEscTarget;
persistent ghost uint256 ghostGwEscValue256;
persistent ghost bool ghostGwEscLastSuccess;
persistent ghost bool ghostGwEscCapBroken;
persistent ghost mapping(bytes32 => mathint) ghostGwEscFailedOf;
persistent ghost mapping(mathint => bytes32) ghostGwEscHashAt;

function gwExcessivelySafeCallCVL(address target, uint256 gasCap, uint256 value, uint16 maxCopy, bytes callData)
    returns (bool, bytes) {
    ghostGwEscCount = ghostGwEscCount + 1;
    ghostGwEscTarget = target;
    ghostGwEscValue256 = value;
    ghostGwEscHashAt[ghostGwEscCount] = ghostGwLastProcessedHash;
    if (gasCap != ghostGwLastProcessingGas128 - ghostGwFailureReserve128) {
        ghostGwEscCapBroken = true;
    }
    if (!ghostGwSrcArmed) {
        ghostGwSrcPairBroken = true;
    }
    ghostGwSrcArmed = false;
    bool success;
    ghostGwEscLastSuccess = success;
    if (!success) {
        ghostGwEscFailedOf[ghostGwLastProcessedHash] = ghostGwEscFailedOf[ghostGwLastProcessedHash] + 1;
    }
    bytes returnData;
    require(returnData.length <= maxCopy, "SAFE: return data is capped at the copy limit");
    return (success, returnData);
}

persistent ghost mathint ghostGwTokenTransferCount {
    init_state axiom ghostGwTokenTransferCount == 0;
    axiom ghostGwTokenTransferCount >= 0;
}
persistent ghost bool ghostGwToken6909Ok;

function gwTokenTransferCVL(address token, address to, uint256 value) {
    ghostGwTokenTransferCount = ghostGwTokenTransferCount + 1;
}

function gwToken6909TransferCVL(address token, address to, uint256 tokenId, uint256 amount) returns bool {
    ghostGwTokenTransferCount = ghostGwTokenTransferCount + 1;
    return ghostGwToken6909Ok;
}

function setupGateway(env e) {
    setupEnv(e);
}
