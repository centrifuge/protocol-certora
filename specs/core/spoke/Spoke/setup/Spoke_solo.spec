// Spoke, solo lane. Setup: SpokeRegistry, SnapshotQueue and Escrow as models.

// Own setup: registry, queue and escrow as CVL models; Spoke_base is shared with the linked core, which runs them real.

import "Spoke_base.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/single_share_class.spec";
import "../../SpokeRegistry/setup/SpokeRegistry_cvl.spec";
import "../../SnapshotQueue/setup/SnapshotQueue_cvl.spec";
import "../../Escrow/setup/Escrow_cvl.spec";

function setupSpokeSolo(env e) {
    setupSpoke(e);
    setupPoolMode();
    setupShareClassMode();
    assumeShareTokenIffRegistrar();
}

function setupSpokeValidState(env e) {
    setupSpokeSolo(e);
}

function setupSpokeSoloAnyTransient(env e) {
    setupSpokeAnyTransient(e);
    setupPoolMode();
    setupShareClassMode();
    assumeShareTokenIffRegistrar();
}

// msgSender(): the multicall caller inside a gateway batch, else msg.sender.
function spResolvedSenderCVL(env e) returns address {
    return spInBatchCVL(e) ? ghostSpSenderT : e.msg.sender;
}

function spInBatchCVL(env e) returns bool {
    return ghostSpSenderT != 0 && e.msg.sender == _Spoke.gateway;
}

// SCOPE: a direct token mint or burn is only counted, never applied.
methods {
    function _.mint(address, uint256) external => spDirectSupplyCallCVL() expect void;
    function _.burn(address, uint256) external => spDirectSupplyCallCVL() expect void;
}

persistent ghost mathint ghostSpDirectSupplyCalls;

function spDirectSupplyCallCVL() {
    ghostSpDirectSupplyCalls = ghostSpDirectSupplyCalls + 1;
}
