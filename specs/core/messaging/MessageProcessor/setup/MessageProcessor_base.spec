// MessageProcessor. Setup: wiring, ward set, neighbour recorders and BytesLib twins.

import "../../../../shared/env.spec";
import "../../../../shared/bytes_slice.spec";
import "../../../spoke/SpokeHandler/setup/SpokeHandler_cvl.spec";
import "../../../hub/HubHandler/setup/HubHandler_cvl.spec";
import "../../../utils/Envoy/setup/Envoy_cvl.spec";
import "../../../../shared/models/Root_cvl.spec";

using MessageProcessor as _MessageProcessor;
using MultiAdapterStub as _MultiAdapterStub;
using ScheduleAuthStub as _ScheduleAuthStub;

methods {
    function _MessageProcessor.wards(address) external returns (uint256) envfree;
    function _MessageProcessor.gateway() external returns (address) envfree;
    function _MessageProcessor.multiAdapter() external returns (address) envfree;
    function _MessageProcessor.spokeHandler() external returns (address) envfree;
    function _MessageProcessor.hubHandler() external returns (address) envfree;
    function _MessageProcessor.envoy() external returns (address) envfree;
    function _MessageProcessor.scheduleAuth() external returns (address) envfree;
    function _MessageProcessor.messageLength(bytes) external returns (uint16) envfree;
    function _MessageProcessor.messagePoolId(bytes) external returns (MessageProcessor.PoolId) envfree;
    function _MessageProcessor.routePoolId(bytes, bool) external returns (MessageProcessor.PoolId) envfree;
    function _MessageProcessor.messageSourceCentrifugeId(bytes) external returns (uint16) envfree;

    // SCOPE: setAdapters and both upgrade authority calls reach handle with no sighash.
    unresolved external in MessageProcessor.handle(uint16,bytes) => DISPATCH [
        MultiAdapterStub.setAdapters(uint16,uint64,address[],uint8,uint16),
        ScheduleAuthStub.scheduleRely(address),
        ScheduleAuthStub.cancelRely(address)
    ] default NONDET;
    // UNSAFE: as Root_cvl, the stand-in only counts the call.
    function ScheduleAuthStub.scheduleRely(address target) external => scheduleAuthEntryCVL(401);
    function ScheduleAuthStub.cancelRely(address target) external => scheduleAuthEntryCVL(402);
    // UNSAFE: setAdapters only records, its effects and refusals dropped.
    function MultiAdapterStub.setAdapters(uint16 centrifugeId, uint64 poolId, address[] adapters, uint8 threshold,
        uint16 targetSessionId) external
        => mpSetAdaptersCVL(calledContract, centrifugeId, poolId, targetSessionId);
    function _.setAdapters(uint16 centrifugeId, uint64 poolId, address[] adapters, uint8 threshold,
        uint16 targetSessionId) external
        => mpSetAdaptersCVL(calledContract, centrifugeId, poolId, targetSessionId) expect void UNRESOLVED;

    // SAFE: no rule reads a name or symbol, any bounded string stands in.
    function CastLib.bytes128ToString(bytes memory) internal returns (string memory) => anyNameMpCVL();
    function CastLib.toString(bytes32) internal returns (string memory) => anySymbolMpCVL();
}

persistent ghost mathint ghostMaSetAdaptersCount {
    init_state axiom ghostMaSetAdaptersCount == 0;
    axiom ghostMaSetAdaptersCount >= 0;
}
persistent ghost address ghostMaLastSetAdaptersCallee;
persistent ghost uint16 ghostMaLastSetAdaptersCid16;
persistent ghost uint64 ghostMaLastSetAdaptersPool64;
persistent ghost uint16 ghostMaLastSetAdaptersSession16;
// Adapter router call tag, numbered like the handler call tags (5xx).
persistent ghost mathint ghostMaLastEntry;

function mpSetAdaptersCVL(address callee, uint16 centrifugeId, uint64 poolId, uint16 targetSessionId) {
    ghostMaSetAdaptersCount = ghostMaSetAdaptersCount + 1;
    ghostMaLastSetAdaptersCallee = callee;
    ghostMaLastSetAdaptersCid16 = centrifugeId;
    ghostMaLastSetAdaptersPool64 = poolId;
    ghostMaLastSetAdaptersSession16 = targetSessionId;
    ghostMaLastEntry = 501;
}

function anyNameMpCVL() returns string {
    string s;
    require(s.length <= 128, "SAFE: a name is at most 128 bytes");
    return s;
}

function anySymbolMpCVL() returns string {
    string s;
    require(s.length <= 32, "SAFE: a symbol is at most 32 bytes");
    return s;
}

// SCOPE: loop_iter 8 is MAX_ADAPTER_COUNT, longer lists are cut.

// SAFE: retyped MessageType codes of MessageLib.sol:11-47.
definition MT_SCHEDULE_UPGRADE() returns mathint = 1;
definition MT_CANCEL_UPGRADE() returns mathint = 2;
definition MT_REGISTER_ASSET() returns mathint = 3;
definition MT_SET_POOL_ADAPTERS() returns mathint = 4;
definition MT_NOTIFY_POOL() returns mathint = 5;
definition MT_NOTIFY_SHARE_CLASS() returns mathint = 6;
definition MT_NOTIFY_PRICE_POOL_PER_SHARE() returns mathint = 7;
definition MT_NOTIFY_PRICE_POOL_PER_ASSET() returns mathint = 8;
definition MT_NOTIFY_SHARE_METADATA() returns mathint = 9;
definition MT_INITIATE_TRANSFER_SHARES() returns mathint = 10;
definition MT_EXECUTE_TRANSFER_SHARES() returns mathint = 11;
definition MT_UPDATE_RESTRICTION() returns mathint = 12;
definition MT_UPDATE_VAULT() returns mathint = 13;
definition MT_UPDATE_ASSETS() returns mathint = 14;
definition MT_UPDATE_SHARES() returns mathint = 15;
definition MT_REQUEST() returns mathint = 16;
definition MT_REQUEST_CALLBACK() returns mathint = 17;
definition MT_SET_REQUEST_MANAGER() returns mathint = 18;
definition MT_MANAGER_CALL_FROM_SPOKE() returns mathint = 19;
definition MT_MANAGER_CALL_FROM_HUB() returns mathint = 20;
definition MT_UPDATE_MANAGER() returns mathint = 21;
definition MT_SET_POLICY() returns mathint = 22;
definition MT_AUTHORIZE_SPOKE_CALL() returns mathint = 23;
definition MT_UNAUTHORIZE_SPOKE_CALL() returns mathint = 24;

// SAFE: retyped MessageLib.MAINNET_CENTRIFUGE_ID.
definition MAINNET_CID_MP() returns mathint = 1;

definition HUB_KIND_MP(mathint k) returns bool =
    k == MT_REGISTER_ASSET() || k == MT_INITIATE_TRANSFER_SHARES() || k == MT_UPDATE_ASSETS()
        || k == MT_UPDATE_SHARES() || k == MT_REQUEST() || k == MT_MANAGER_CALL_FROM_SPOKE();

definition ROOT_KIND_MP(mathint k) returns bool =
    k == MT_SCHEDULE_UPGRADE() || k == MT_CANCEL_UPGRADE();

definition SPOKE_KIND_MP(mathint k) returns bool =
    k >= MT_SET_POOL_ADAPTERS() && k <= MT_UNAUTHORIZE_SPOKE_CALL() && !HUB_KIND_MP(k);

definition EXCLUDED_FUNCTION_MP(method f) returns bool =
    f.isView || f.isPure || f.isFallback;

definition DOWNSTREAM_MP() returns mathint =
    ghostShCallCount + ghostHhCallCount + ghostEnCallCount + ghostSaCallCount + ghostMaSetAdaptersCount;

definition LAST_ENTRY_MP() returns mathint =
    ghostShLastEntry + ghostHhLastEntry + ghostEnLastEntry + ghostSaLastEntry + ghostMaLastEntry;

// The handler call tag each message type selects; a manager update selects by kind.
definition ENTRY_OF_MP(mathint k) returns mathint =
    k == MT_SCHEDULE_UPGRADE() ? 401 : k == MT_CANCEL_UPGRADE() ? 402 : k == MT_REGISTER_ASSET() ? 201
    : k == MT_SET_POOL_ADAPTERS() ? 501 : k == MT_NOTIFY_POOL() ? 101 : k == MT_NOTIFY_SHARE_CLASS() ? 102
    : k == MT_NOTIFY_PRICE_POOL_PER_SHARE() ? 104 : k == MT_NOTIFY_PRICE_POOL_PER_ASSET() ? 105
    : k == MT_NOTIFY_SHARE_METADATA() ? 103 : k == MT_INITIATE_TRANSFER_SHARES() ? 203
    : k == MT_EXECUTE_TRANSFER_SHARES() ? 112 : k == MT_UPDATE_RESTRICTION() ? 106 : k == MT_UPDATE_VAULT() ? 107
    : k == MT_UPDATE_ASSETS() ? 204 : k == MT_UPDATE_SHARES() ? 205 : k == MT_REQUEST() ? 202
    : k == MT_REQUEST_CALLBACK() ? 113 : k == MT_SET_REQUEST_MANAGER() ? 108 : k == MT_MANAGER_CALL_FROM_SPOKE() ? 302
    : k == MT_MANAGER_CALL_FROM_HUB() ? 301 : k == MT_SET_POLICY() ? 111 : k == MT_AUTHORIZE_SPOKE_CALL() ? 109
    : k == MT_UNAUTHORIZE_SPOKE_CALL() ? 110 : 0;

function clearEntriesMp() {
    ghostShLastEntry = 0;
    ghostHhLastEntry = 0;
    ghostEnLastEntry = 0;
    ghostSaLastEntry = 0;
    ghostMaLastEntry = 0;
}

function setupMessageProcessor(env e) {
    require(e.msg.sender != _MessageProcessor, "SCOPE: the processor is not its own caller");
}

// TRUSTED: deployment wires all six pointers to deployed contracts.
function assumeMpNeighboursAnswer() {
    assumeMpNeighbourAnswers(_MessageProcessor.hubHandler());
    assumeMpNeighbourAnswers(_MessageProcessor.spokeHandler());
    assumeMpNeighbourAnswers(_MessageProcessor.envoy());
    assumeMpNeighbourAnswers(_MessageProcessor.gateway());
    assumeMpNeighbourAnswers(_MessageProcessor.multiAdapter());
    assumeMpNeighbourAnswers(_MessageProcessor.scheduleAuth());
}

function assumeMpNeighbourAnswers(address p) {
    require(nativeCodesize[p] > 0, "TRUSTED: governance wires only deployed contracts");
    require(p != _MessageProcessor && p != _BytesSlice && p != _MultiAdapterStub && p != _ScheduleAuthStub,
        "SCOPE: no neighbour is the processor or a stand-in");
}

// The word's low 12 bytes are clear, as CastLib.toAddress requires.
function addressWordAtMp(bytes message, uint256 start) returns bool {
    return _BytesSlice.toUint256Pure(message, start) % 2^96 == 0;
}

function adapterEntryMp(bytes message, mathint count, uint256 i) returns bool {
    if (i >= count) {
        return true;
    }
    return addressWordAtMp(message, require_uint256(14 + 32 * i));
}

// A message that MessageLib's deserializers and handle's casts all accept.
function wellFormedMp(bytes message) returns bool {
    mathint len = message.length;
    if (len < 1) {
        return false;
    }
    mathint k = _BytesSlice.toUint8Pure(message, 0);
    if (k == MT_SCHEDULE_UPGRADE() || k == MT_CANCEL_UPGRADE()) {
        return len >= 33 && addressWordAtMp(message, 1);
    }
    if (k == MT_REGISTER_ASSET()) {
        return len >= 18;
    }
    if (k == MT_SET_POOL_ADAPTERS()) {
        if (len < 14) {
            return false;
        }
        mathint count = _BytesSlice.toUint16Pure(message, 12);
        return count <= 8 && len >= 14 + 32 * count
            && adapterEntryMp(message, count, 0) && adapterEntryMp(message, count, 1)
            && adapterEntryMp(message, count, 2) && adapterEntryMp(message, count, 3)
            && adapterEntryMp(message, count, 4) && adapterEntryMp(message, count, 5)
            && adapterEntryMp(message, count, 6) && adapterEntryMp(message, count, 7);
    }
    if (k == MT_NOTIFY_POOL()) {
        return len >= 9;
    }
    if (k == MT_NOTIFY_SHARE_CLASS()) {
        return len >= 268 && len >= 268 + _BytesSlice.toUint16Pure(message, 266) && addressWordAtMp(message, 218);
    }
    if (k == MT_NOTIFY_PRICE_POOL_PER_SHARE()) {
        return len >= 49;
    }
    if (k == MT_NOTIFY_PRICE_POOL_PER_ASSET()) {
        return len >= 65;
    }
    if (k == MT_NOTIFY_SHARE_METADATA()) {
        return len >= 201;
    }
    if (k == MT_INITIATE_TRANSFER_SHARES()) {
        return len >= 139;
    }
    if (k == MT_EXECUTE_TRANSFER_SHARES()) {
        return len >= 89;
    }
    if (k == MT_UPDATE_RESTRICTION()) {
        return len >= 43 && len >= 43 + _BytesSlice.toUint16Pure(message, 41);
    }
    if (k == MT_UPDATE_VAULT()) {
        return len >= 92 && len >= 92 + _BytesSlice.toUint16Pure(message, 90)
            && _BytesSlice.toUint8Pure(message, 73) <= 2 && addressWordAtMp(message, 41);
    }
    if (k == MT_UPDATE_ASSETS()) {
        return len >= 91;
    }
    if (k == MT_UPDATE_SHARES()) {
        return len >= 75;
    }
    if (k == MT_REQUEST() || k == MT_REQUEST_CALLBACK() || k == MT_MANAGER_CALL_FROM_HUB()) {
        return len >= 59 && len >= 59 + _BytesSlice.toUint16Pure(message, 57)
            && (k != MT_MANAGER_CALL_FROM_HUB() || addressWordAtMp(message, 9));
    }
    if (k == MT_SET_REQUEST_MANAGER() || k == MT_SET_POLICY()) {
        return len >= 41 && addressWordAtMp(message, 9);
    }
    if (k == MT_MANAGER_CALL_FROM_SPOKE()) {
        return len >= 91 && len >= 91 + _BytesSlice.toUint16Pure(message, 89) && addressWordAtMp(message, 9);
    }
    if (k == MT_UPDATE_MANAGER()) {
        return len >= 43 && _BytesSlice.toUint8Pure(message, 9) <= 3 && addressWordAtMp(message, 10);
    }
    if (k == MT_AUTHORIZE_SPOKE_CALL() || k == MT_UNAUTHORIZE_SPOKE_CALL()) {
        return len >= 11 && len >= 11 + _BytesSlice.toUint16Pure(message, 9);
    }
    return false;
}

// The byte length each message type's decoder reads.
function decodedLengthMp(bytes m) returns mathint {
    mathint k = _BytesSlice.toUint8Pure(m, 0);
    if (ROOT_KIND_MP(k)) {
        return 33;
    }
    if (k == MT_REGISTER_ASSET()) {
        return 18;
    }
    if (k == MT_SET_POOL_ADAPTERS()) {
        return 14 + 32 * _BytesSlice.toUint16Pure(m, 12);
    }
    if (k == MT_NOTIFY_POOL()) {
        return 9;
    }
    if (k == MT_NOTIFY_SHARE_CLASS()) {
        return 268 + _BytesSlice.toUint16Pure(m, 266);
    }
    if (k == MT_NOTIFY_PRICE_POOL_PER_SHARE()) {
        return 49;
    }
    if (k == MT_NOTIFY_PRICE_POOL_PER_ASSET()) {
        return 65;
    }
    if (k == MT_NOTIFY_SHARE_METADATA()) {
        return 201;
    }
    if (k == MT_INITIATE_TRANSFER_SHARES()) {
        return 139;
    }
    if (k == MT_EXECUTE_TRANSFER_SHARES()) {
        return 89;
    }
    if (k == MT_UPDATE_RESTRICTION()) {
        return 43 + _BytesSlice.toUint16Pure(m, 41);
    }
    if (k == MT_UPDATE_VAULT()) {
        return 92 + _BytesSlice.toUint16Pure(m, 90);
    }
    if (k == MT_UPDATE_ASSETS()) {
        return 91;
    }
    if (k == MT_UPDATE_SHARES()) {
        return 75;
    }
    if (k == MT_REQUEST() || k == MT_REQUEST_CALLBACK() || k == MT_MANAGER_CALL_FROM_HUB()) {
        return 59 + _BytesSlice.toUint16Pure(m, 57);
    }
    if (k == MT_SET_REQUEST_MANAGER() || k == MT_SET_POLICY()) {
        return 41;
    }
    if (k == MT_MANAGER_CALL_FROM_SPOKE()) {
        return 91 + _BytesSlice.toUint16Pure(m, 89);
    }
    if (k == MT_UPDATE_MANAGER()) {
        return 43;
    }
    return 11 + _BytesSlice.toUint16Pure(m, 9);
}
