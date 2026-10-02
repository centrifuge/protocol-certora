// Hub. Setup: every neighbour modelled in CVL, manager transients read from the contract.

import "../../../../shared/env.spec";
import "../../../../shared/models/StdHubPolicy_cvl.spec";
import "../../../../shared/models/IValuation_cvl.spec";
import "../../../messaging/MessageDispatcher/setup/MessageDispatcher_cvl.spec";
import "../../../../shared/models/Gateway_cvl.spec";
import "../../../messaging/MultiAdapter/setup/MultiAdapter_cvl.spec";
import "../../../../shared/models/ISnapshotHook_cvl.spec";
import "../../../../shared/models/IFeeAccrual_cvl.spec";
import "../../../../shared/models/IHubRequestManager_cvl.spec";
import "../../../../shared/models/ISpokeRequestManager_cvl.spec";
import "../../../../shared/models/IVaultFactory_cvl.spec";
import "../../../../shared/math.spec";

using HubHarness as _Hub;

methods {
    // UNSAFE: multicall is cut, no batch is analysed.
    function _Hub.multicall(bytes[]) external
        => NONDET DELETE;
}

definition EXCLUDED_FUNCTION_HU(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

persistent ghost address ghostHuInitiatorT {
    init_state axiom ghostHuInitiatorT == 0;
}

hook Tload address v _Hub._initiator {
    require(ghostHuInitiatorT == v, "SAFE: mirror tracks storage");
}

hook Tstore _Hub._initiator address v {
    ghostHuInitiatorT = v;
}

persistent ghost address ghostHuSenderT {
    init_state axiom ghostHuSenderT == 0;
}
hook Tload address v _Hub._sender {
    require(ghostHuSenderT == v, "SAFE: mirror tracks storage");
}
hook Tstore _Hub._sender address v {
    ghostHuSenderT = v;
}

function setupHub(env e) {
    setupHubAnyTransient(e);
    requireHubTransientsEmpty();
}

// Transients stay arbitrary: a call may arrive mid-batch from the gateway.
function setupHubAnyTransient(env e) {
    setupEnv(e);
    require(e.msg.sender != _Hub, "SAFE: the hub never calls itself");
    require(_Hub.gateway != 0, "TRUSTED: gateway wired at deploy, never cleared");
    require(_Hub.sender != 0, "TRUSTED: sender wired at deploy, never cleared");
    require(_Hub.multiAdapter != 0, "TRUSTED: multi-adapter wired at deploy, never cleared");
}

function requireHubTransientsEmpty() {
    require(ghostHuSenderT == 0 && ghostHuInitiatorT == 0, "SAFE: transient storage starts empty");
}

function huInBatchCVL(env e) returns bool {
    return ghostHuSenderT != 0 && e.msg.sender == _Hub.gateway;
}
