// Spoke. Setup: token, registrar, factory and messaging models, the transients.

import "../../../../shared/env.spec";
import "../../../../shared/tokens/erc20.spec";
import "../../../../shared/tokens/erc6909.spec";
import "../../../../shared/models/ShareTokenRegistrar_cvl.spec";
import "../../factories/EscrowFactory/setup/EscrowFactory_cvl.spec";
import "../../../messaging/MessageDispatcher/setup/MessageDispatcher_cvl.spec";
import "../../../../shared/models/Gateway_cvl.spec";
import "../../../../shared/models/IPolicy_cvl.spec";

using SpokeHarness as _Spoke;

methods {
    // UNSAFE: multicall is cut, no batch is analysed.
    function _Spoke.multicall(bytes[]) external
        => NONDET DELETE;

    // UNSAFE: executeMulticall is cut, no batched call is analysed.
    function _Spoke.executeMulticall(bytes[]) external
        => NONDET DELETE;

    // UNSAFE: name and symbol of a caller-supplied token return anything.
    function _.name() external
        => NONDET;
    function _.symbol() external
        => NONDET;
    function _.name(uint256 tokenId) external
        => NONDET;
    function _.symbol(uint256 tokenId) external
        => NONDET;
}

definition EXCLUDED_FUNCTION_SP(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

// Spoke's internal MAX_DECIMALS, which has no getter.
definition MAX_DECIMALS_CVL() returns mathint = 18;

persistent ghost address ghostSpSenderT {
    init_state axiom ghostSpSenderT == 0;
}
persistent ghost address ghostSpInitiatorT {
    init_state axiom ghostSpInitiatorT == 0;
}
hook Tload address v _Spoke._sender {
    require(ghostSpSenderT == v, "SAFE: mirror tracks storage");
}
hook Tstore _Spoke._sender address v {
    ghostSpSenderT = v;
}
hook Tload address v _Spoke._initiator {
    require(ghostSpInitiatorT == v, "SAFE: mirror tracks storage");
}
hook Tstore _Spoke._initiator address v {
    ghostSpInitiatorT = v;
}

function setupSpoke(env e) {
    setupSpokeAnyTransient(e);
    require(ghostSpInitiatorT == 0 && ghostSpSenderT == 0, "SAFE: transient storage starts empty");
}

// Transients stay arbitrary: a call may arrive mid-batch from the gateway.
function setupSpokeAnyTransient(env e) {
    setupEnv(e);
    setupERC20();
    setupERC6909();
    require(e.msg.sender != _Spoke, "SAFE: the spoke never calls itself");
    require(_Spoke.gateway != 0, "TRUSTED: gateway wired at deploy, never cleared");
    require(_Spoke.sender != 0, "TRUSTED: message sender wired after deploy, never cleared");
    require(_Spoke.wards[_Spoke.gateway] == 0, "TRUSTED: the gateway is never made a spoke ward");
}

// Left aligned, as Solidity encodes a bytes32 string literal.
definition FILE_GATEWAY_SP_CVL() returns bytes32 =
    to_bytes32(0x6761746577617900000000000000000000000000000000000000000000000000);

definition FILE_SENDER_SP_CVL() returns bytes32 =
    to_bytes32(0x73656e6465720000000000000000000000000000000000000000000000000000);
