// MultiAdapter. Setup: roster and vote mirrors, recording adapter models.

import "../../../../shared/env.spec";
import "../../../../shared/models/Gateway_cvl.spec";
import "../../../../shared/domains/single_pool.spec";
import "../../../../shared/domains/single_share_class.spec";
import "../../../../shared/models/MessageProcessor_cvl.spec";

using MultiAdapterHarness as _MultiAdapter;

methods {
    // UNSAFE: an adapter refuses its quote and its send alike, on a free per-adapter flag.
    function _.estimate(uint16 centrifugeId, bytes payload, uint256 gasLimit) external
        => maAdapterEstimateCVL(calledContract, centrifugeId, payload, gasLimit) expect uint256 UNRESOLVED;
    function _.send(uint16 centrifugeId, bytes payload, uint256 gasLimit, address refund) external with (env e)
        => maAdapterSendCVL(e, calledContract, centrifugeId, payload, gasLimit, refund) expect bytes32 UNRESOLVED;
}

definition EXCLUDED_FUNCTION_MA(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    ;

// SAFE: MAX_ADAPTER_COUNT retyped, the conf loop_iter matches it.
definition MAX_ADAPTERS_CVL() returns mathint = 8;

// SAFE: the key literals MultiAdapter.file spells inline.
definition FILE_GATEWAY_MA_CVL() returns bytes32 =
    to_bytes32(0x6761746577617900000000000000000000000000000000000000000000000000);

definition FILE_PARSER_MA_CVL() returns bytes32 =
    to_bytes32(0x7061727365720000000000000000000000000000000000000000000000000000);

definition FILE_MESSAGE_GAS_MA_CVL() returns bytes32 =
    to_bytes32(0x6d65737361676547617300000000000000000000000000000000000000000000);

// UNSAFE: one network id keys all rows, so network mixups go unseen.
persistent ghost uint16 ghostMaCid16;

persistent ghost mapping(address => bool) ghostMaManager {
    init_state axiom forall address a. !ghostMaManager[a];
}

hook Sload bool val _MultiAdapter.manager[KEY MultiAdapter.PoolId p][KEY address a] {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaManager[a] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter.manager[KEY MultiAdapter.PoolId p][KEY address a] bool val {
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaManager[a] = val;
}

persistent ghost uint16 ghostMaActiveSessionId16 {
    init_state axiom ghostMaActiveSessionId16 == 0;
}

hook Sload uint16 val _MultiAdapter.activeSessionId[KEY uint16 cid][KEY MultiAdapter.PoolId p] {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaActiveSessionId16 == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter.activeSessionId[KEY uint16 cid][KEY MultiAdapter.PoolId p] uint16 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaActiveSessionId16 = val;
}

persistent ghost uint16 ghostMaActiveSetSessionId16 {
    init_state axiom ghostMaActiveSetSessionId16 == 0;
    axiom ghostMaActiveSetSessionId16 >= 0 && ghostMaActiveSetSessionId16 <= max_uint16;
}

persistent ghost mathint ghostMaActiveListLength8 {
    init_state axiom ghostMaActiveListLength8 == 0;
    axiom ghostMaActiveListLength8 >= 0;
}

persistent ghost mapping(mathint => address) ghostMaActiveList {
    init_state axiom forall mathint i. ghostMaActiveList[i] == 0;
}

hook Sload uint16 val _MultiAdapter._activeAdapters[KEY uint16 cid][KEY MultiAdapter.PoolId p].sessionId {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaActiveSetSessionId16 == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter._activeAdapters[KEY uint16 cid][KEY MultiAdapter.PoolId p].sessionId uint16 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaActiveSetSessionId16 = val;
}

hook Sload uint256 val _MultiAdapter._activeAdapters[KEY uint16 cid][KEY MultiAdapter.PoolId p].list.length {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaActiveListLength8 == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter._activeAdapters[KEY uint16 cid][KEY MultiAdapter.PoolId p].list.length uint256 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(val <= MAX_ADAPTERS_CVL(), "SCOPE: a roster holds at most eight adapters");
    ghostMaActiveListLength8 = val;
    // Unrolled to eight: no length the cap admits reaches a slot past index 7.
    ghostMaActiveList[0] = 0 < val ? ghostMaActiveList[0] : 0;
    ghostMaActiveList[1] = 1 < val ? ghostMaActiveList[1] : 0;
    ghostMaActiveList[2] = 2 < val ? ghostMaActiveList[2] : 0;
    ghostMaActiveList[3] = 3 < val ? ghostMaActiveList[3] : 0;
    ghostMaActiveList[4] = 4 < val ? ghostMaActiveList[4] : 0;
    ghostMaActiveList[5] = 5 < val ? ghostMaActiveList[5] : 0;
    ghostMaActiveList[6] = 6 < val ? ghostMaActiveList[6] : 0;
    ghostMaActiveList[7] = 7 < val ? ghostMaActiveList[7] : 0;
}

hook Sload address val _MultiAdapter._activeAdapters[KEY uint16 cid][KEY MultiAdapter.PoolId p].list[INDEX uint256 i] {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaActiveList[i] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter._activeAdapters[KEY uint16 cid][KEY MultiAdapter.PoolId p].list[INDEX uint256 i] address val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaActiveList[i] = val;
}

persistent ghost mapping(uint16 => mathint) ghostMaSessionListLength8 {
    init_state axiom forall uint16 s. ghostMaSessionListLength8[s] == 0;
    axiom forall uint16 s. ghostMaSessionListLength8[s] >= 0;
}

persistent ghost mapping(uint16 => mapping(mathint => address)) ghostMaSessionList {
    init_state axiom forall uint16 s. forall mathint i. ghostMaSessionList[s][i] == 0;
}

hook Sload uint256 val _MultiAdapter.adapters[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid].(offset 0) {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaSessionListLength8[sid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter.adapters[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid].(offset 0) uint256 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(val <= MAX_ADAPTERS_CVL(), "SCOPE: a roster holds at most eight adapters");
    ghostMaSessionListLength8[sid] = val;
    // Unrolled to eight: no length the cap admits reaches a slot past index 7.
    ghostMaSessionList[sid][0] = 0 < val ? ghostMaSessionList[sid][0] : 0;
    ghostMaSessionList[sid][1] = 1 < val ? ghostMaSessionList[sid][1] : 0;
    ghostMaSessionList[sid][2] = 2 < val ? ghostMaSessionList[sid][2] : 0;
    ghostMaSessionList[sid][3] = 3 < val ? ghostMaSessionList[sid][3] : 0;
    ghostMaSessionList[sid][4] = 4 < val ? ghostMaSessionList[sid][4] : 0;
    ghostMaSessionList[sid][5] = 5 < val ? ghostMaSessionList[sid][5] : 0;
    ghostMaSessionList[sid][6] = 6 < val ? ghostMaSessionList[sid][6] : 0;
    ghostMaSessionList[sid][7] = 7 < val ? ghostMaSessionList[sid][7] : 0;
}

hook Sload address val _MultiAdapter.adapters[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][INDEX uint256 i] {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaSessionList[sid][i] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter.adapters[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][INDEX uint256 i] address val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaSessionList[sid][i] = val;
}

persistent ghost mapping(uint16 => mapping(address => mathint)) ghostMaAdapterId8 {
    init_state axiom forall uint16 s. forall address a. ghostMaAdapterId8[s][a] == 0;
    axiom forall uint16 s. forall address a.
        ghostMaAdapterId8[s][a] >= 0 && ghostMaAdapterId8[s][a] <= max_uint8;
}

persistent ghost mapping(uint16 => mapping(address => mathint)) ghostMaAdapterQuorum8 {
    init_state axiom forall uint16 s. forall address a. ghostMaAdapterQuorum8[s][a] == 0;
    axiom forall uint16 s. forall address a.
        ghostMaAdapterQuorum8[s][a] >= 0 && ghostMaAdapterQuorum8[s][a] <= max_uint8;
}

persistent ghost mapping(uint16 => mapping(address => mathint)) ghostMaAdapterThreshold8 {
    init_state axiom forall uint16 s. forall address a. ghostMaAdapterThreshold8[s][a] == 0;
    axiom forall uint16 s. forall address a.
        ghostMaAdapterThreshold8[s][a] >= 0 && ghostMaAdapterThreshold8[s][a] <= max_uint8;
}

persistent ghost mapping(uint16 => mathint) ghostMaBlockedThreshold8 {
    init_state axiom forall uint16 s. ghostMaBlockedThreshold8[s] == 0;
    axiom forall uint16 s. ghostMaBlockedThreshold8[s] >= 0 && ghostMaBlockedThreshold8[s] <= max_uint8;
}

persistent ghost mapping(uint16 => bool) ghostMaBlockedWasActive {
    init_state axiom forall uint16 s. !ghostMaBlockedWasActive[s];
}

persistent ghost mapping(uint16 => mathint) ghostMaBlockedListLength8 {
    init_state axiom forall uint16 s. ghostMaBlockedListLength8[s] == 0;
    axiom forall uint16 s. ghostMaBlockedListLength8[s] >= 0;
}

hook Sload uint256 val _MultiAdapter._blockedSessions[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid].list.length {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaBlockedListLength8[sid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter._blockedSessions[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid].list.length uint256 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(val <= MAX_ADAPTERS_CVL(), "SCOPE: a roster holds at most eight adapters");
    ghostMaBlockedListLength8[sid] = val;
}

definition BOUNDARIES_MULTI_ADAPTER() returns bool =
    ghostMaActiveListLength8 <= MAX_ADAPTERS_CVL()
    && (forall uint16 s. ghostMaSessionListLength8[s] <= MAX_ADAPTERS_CVL())
    && (forall uint16 s. ghostMaBlockedListLength8[s] <= MAX_ADAPTERS_CVL())
    ;

function setupMultiAdapter(env e) {
    setupEnv(e);
    setupPoolMode();
    require(ghostPoolA64 != 0, "UNSAFE: the global pool 0 roster is left out");
    setupShareClassMode();
    require(BOUNDARIES_MULTI_ADAPTER(), "SAFE: no roster exceeds the eight-adapter cap");
    require(_MultiAdapter.gateway != 0, "TRUSTED: gateway wired at deploy, never cleared");
    require(_MultiAdapter.parser != 0, "TRUSTED: parser wired at deploy, never cleared");
}

hook Sload uint8 val _MultiAdapter._adapterDetails[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][KEY address adapter].id {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaAdapterId8[sid][adapter] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter._adapterDetails[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][KEY address adapter].id uint8 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaAdapterId8[sid][adapter] = val;
}

hook Sload uint8 val _MultiAdapter._adapterDetails[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][KEY address adapter].quorum {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaAdapterQuorum8[sid][adapter] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter._adapterDetails[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][KEY address adapter].quorum uint8 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaAdapterQuorum8[sid][adapter] = val;
}

hook Sload uint8 val _MultiAdapter._adapterDetails[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][KEY address adapter].threshold {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaAdapterThreshold8[sid][adapter] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter._adapterDetails[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid][KEY address adapter].threshold uint8 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaAdapterThreshold8[sid][adapter] = val;
}

hook Sload uint8 val _MultiAdapter._blockedSessions[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid].threshold {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaBlockedThreshold8[sid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter._blockedSessions[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid].threshold uint8 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaBlockedThreshold8[sid] = val;
}

hook Sload bool val _MultiAdapter._blockedSessions[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid].wasActive {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    require(ghostMaBlockedWasActive[sid] == val, "SAFE: mirror tracks storage");
}

hook Sstore _MultiAdapter._blockedSessions[KEY uint16 cid][KEY MultiAdapter.PoolId p][KEY uint16 sid].wasActive bool val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    require(VALID_POOL(p), "SCOPE: modelled pools stand for any");
    ghostMaBlockedWasActive[sid] = val;
}

hook Sload int16 val _MultiAdapter._votes[KEY uint16 cid][KEY bytes32 k][INDEX uint256 i] {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
}

persistent ghost mathint ghostMaVoteForwardMark;
persistent ghost bool ghostMaVoteWrittenBeforeForward;
persistent ghost bool ghostMaVoteWrittenAfterForward;

hook Sstore _MultiAdapter._votes[KEY uint16 cid][KEY bytes32 k][INDEX uint256 i] int16 val {
    require(cid == ghostMaCid16, "UNSAFE: a single remote network");
    bool beforeForward = ghostGwHandleCount == ghostMaVoteForwardMark;
    ghostMaVoteWrittenBeforeForward = beforeForward ? true : ghostMaVoteWrittenBeforeForward;
    ghostMaVoteWrittenAfterForward = beforeForward ? ghostMaVoteWrittenAfterForward : true;
}

persistent ghost mathint ghostMaFaceSendCount {
    init_state axiom ghostMaFaceSendCount == 0;
    axiom ghostMaFaceSendCount >= 0;
}
persistent ghost mathint ghostMaFaceLastSendCid16;
persistent ghost bytes32 ghostMaFaceLastSendHash;
persistent ghost address ghostMaFaceLastSendRefund;
persistent ghost bytes1 ghostMaFaceLastSendByte0;
persistent ghost bytes1 ghostMaFaceLastSendByte1;
persistent ghost mathint ghostMaFaceLastSendLength;
persistent ghost mathint ghostMaFaceLastSendGasLimit256;
persistent ghost bool ghostMaFaceSendGasLimitVaried;
persistent ghost mapping(address => mathint) ghostMaFaceSendCountOf {
    init_state axiom forall address a. ghostMaFaceSendCountOf[a] == 0;
}
persistent ghost bool ghostMaFaceDispatchMisfunded {
    init_state axiom !ghostMaFaceDispatchMisfunded;
}

persistent ghost mathint ghostMaFaceLastQuote256;
persistent ghost address ghostMaFaceLastQuoteFrom;
persistent ghost bool ghostMaFaceDispatchQuotedByAnother;
persistent ghost mathint ghostMaFaceSendValueSum;
persistent ghost mathint ghostMaFaceQuoteCount {
    init_state axiom ghostMaFaceQuoteCount == 0;
    axiom ghostMaFaceQuoteCount >= 0;
}
persistent ghost mapping(address => bool) ghostMaFaceRefuses;

function maAdapterEstimateCVL(address adapter, uint16 centrifugeId, bytes payload, uint256 gasLimit) returns uint256 {
    if (ghostMaFaceRefuses[adapter]) {
        revert("AdapterRefuses");
    }
    ghostMaFaceQuoteCount = ghostMaFaceQuoteCount + 1;
    uint256 cost;
    ghostMaFaceLastQuote256 = cost;
    ghostMaFaceLastQuoteFrom = adapter;
    return cost;
}

function maAdapterSendCVL(env e, address adapter, uint16 centrifugeId, bytes payload, uint256 gasLimit, address refund) returns bytes32 {
    if (ghostMaFaceRefuses[adapter]) {
        revert("AdapterRefuses");
    }
    ghostMaFaceSendCount = ghostMaFaceSendCount + 1;
    ghostMaFaceSendCountOf[adapter] = ghostMaFaceSendCountOf[adapter] + 1;
    ghostMaFaceDispatchMisfunded = ghostMaFaceDispatchMisfunded || e.msg.value != ghostMaFaceLastQuote256;
    ghostMaFaceDispatchQuotedByAnother = ghostMaFaceDispatchQuotedByAnother || adapter != ghostMaFaceLastQuoteFrom;
    ghostMaFaceSendValueSum = ghostMaFaceSendValueSum + e.msg.value;
    ghostMaFaceLastSendCid16 = centrifugeId;
    ghostMaFaceLastSendLength = payload.length;
    ghostMaFaceSendGasLimitVaried = ghostMaFaceSendGasLimitVaried || gasLimit != ghostMaFaceLastSendGasLimit256;
    ghostMaFaceLastSendGasLimit256 = gasLimit;
    ghostMaFaceLastSendHash = keccak256(payload);
    ghostMaFaceLastSendRefund = refund;
    if (payload.length >= 2) {
        ghostMaFaceLastSendByte0 = payload[0];
        ghostMaFaceLastSendByte1 = payload[1];
    }
    bytes32 adapterData;
    return adapterData;
}

definition ROTATION_FUNCTION_MA(method f) returns bool =
    f.selector == sig:_MultiAdapter.setAdapters(uint16,MultiAdapterHarness.PoolId,address[],uint8,uint16).selector;

// SAFE: twin of ArrayLib.countPositiveValues over eight vote lanes.
definition POSITIVE_LANES_MA(mathint l0, mathint l1, mathint l2, mathint l3, mathint l4, mathint l5,
    mathint l6, mathint l7, mathint q) returns mathint =
    (q > 0 && l0 > 0 ? 1 : 0) + (q > 1 && l1 > 0 ? 1 : 0) + (q > 2 && l2 > 0 ? 1 : 0)
    + (q > 3 && l3 > 0 ? 1 : 0) + (q > 4 && l4 > 0 ? 1 : 0) + (q > 5 && l5 > 0 ? 1 : 0)
    + (q > 6 && l6 > 0 ? 1 : 0) + (q > 7 && l7 > 0 ? 1 : 0);

function SETUP_MA(env e, env eFunc) {
    requireSameEnv(e, eFunc);
    setupMultiAdapter(e);
}
