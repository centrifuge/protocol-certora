// Hub. Model: getters and call recorders, for scenes not compiling it.

import "../../../../shared/bytes_slice.spec";

methods {
    function _.sender() external => ghostHuSender expect address UNRESOLVED;
    function _.hubRegistry() external => huHubRegistryCVL(calledContract) expect address UNRESOLVED;
    function _.shareClassManager() external => ghostHuShareClassManager expect address UNRESOLVED;
    function _.holdings() external => ghostHuHoldings expect address UNRESOLVED;
    function _.accounting() external => ghostHuAccounting expect address UNRESOLVED;

    // UNSAFE: calls recorded only, effects, re-entry and ETH dropped.
    function _.createPool(uint64 poolId, address admin, uint128 currency) external
        => huCreatePoolCVL(calledContract, poolId, admin, currency) expect void UNRESOLVED;
    function _.cancelAuthorization(uint64 poolId, bytes data) external
        => huCancelAuthorizationCVL(calledContract, poolId, data) expect void UNRESOLVED;
    function _.createAccount(uint64 poolId, uint256 account, bool isDebitNormal) external
        => huCreateAccountCVL(calledContract, poolId, account, isDebitNormal) expect void UNRESOLVED;
    function _.setAccountMetadata(uint64 poolId, uint256 account, bytes metadata) external
        => huSetAccountMetadataCVL(calledContract, poolId, account, metadata) expect void UNRESOLVED;
    function _.initializeHolding(uint64 poolId, bytes16 scId, uint128 assetId, address valuation, uint256[4] accounts) external
        => huInitializeHoldingCVL(calledContract, poolId, scId, assetId, valuation, accounts) expect void UNRESOLVED;
    function _.updateHoldingValue(uint64 poolId, bytes16 scId, uint128 assetId) external
        => huUpdateHoldingValueCVL(calledContract, poolId, scId, assetId) expect void UNRESOLVED;
    function _.updateHoldingValuation(uint64 poolId, bytes16 scId, uint128 assetId, address valuation) external
        => huUpdateHoldingValuationCVL(calledContract, poolId, scId, assetId, valuation) expect void UNRESOLVED;
    function _.updateSharePrice(uint64 poolId, bytes16 scId, uint128 pricePoolPerShare) external
        => huUpdateSharePriceCVL(calledContract, poolId, scId, pricePoolPerShare) expect void UNRESOLVED;
    function _.managerCall(uint64 poolId, uint16 centrifugeId, bytes32 target, bytes payload, uint128 extraGasLimit, uint256 localValue, address refund) external with (env e)
        => huManagerCallCVL(calledContract, e, poolId, centrifugeId, target, payload, extraGasLimit, localValue, refund) expect void UNRESOLVED;
    function _.requestCallback(uint64 poolId, bytes16 scId, uint128 assetId, bytes payload, uint128 extraGasLimit, bool unpaidMode, address refund) external with (env e)
        => huRequestCallbackCVL(calledContract, e, poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund) expect void UNRESOLVED;
}

persistent ghost address ghostHuSender;
persistent ghost address ghostHuHubRegistry;
persistent ghost address ghostHuShareClassManager;
persistent ghost address ghostHuHoldings;
persistent ghost address ghostHuAccounting;
persistent ghost address ghostHuHubRegistryCallee;

persistent ghost bool ghostHuFaceReverts;

persistent ghost mathint ghostHuFaceCreatePoolCount {
    init_state axiom ghostHuFaceCreatePoolCount == 0;
    axiom ghostHuFaceCreatePoolCount >= 0;
}
persistent ghost mathint ghostHuFaceCancelAuthorizationCount {
    init_state axiom ghostHuFaceCancelAuthorizationCount == 0;
    axiom ghostHuFaceCancelAuthorizationCount >= 0;
}
persistent ghost mathint ghostHuFaceCreateAccountCount {
    init_state axiom ghostHuFaceCreateAccountCount == 0;
    axiom ghostHuFaceCreateAccountCount >= 0;
}
persistent ghost mathint ghostHuFaceSetAccountMetadataCount {
    init_state axiom ghostHuFaceSetAccountMetadataCount == 0;
    axiom ghostHuFaceSetAccountMetadataCount >= 0;
}
persistent ghost mathint ghostHuFaceInitializeHoldingCount {
    init_state axiom ghostHuFaceInitializeHoldingCount == 0;
    axiom ghostHuFaceInitializeHoldingCount >= 0;
}
persistent ghost mathint ghostHuFaceUpdateHoldingValueCount {
    init_state axiom ghostHuFaceUpdateHoldingValueCount == 0;
    axiom ghostHuFaceUpdateHoldingValueCount >= 0;
}
persistent ghost mathint ghostHuFaceUpdateHoldingValuationCount {
    init_state axiom ghostHuFaceUpdateHoldingValuationCount == 0;
    axiom ghostHuFaceUpdateHoldingValuationCount >= 0;
}
persistent ghost mathint ghostHuFaceUpdateSharePriceCount {
    init_state axiom ghostHuFaceUpdateSharePriceCount == 0;
    axiom ghostHuFaceUpdateSharePriceCount >= 0;
}
persistent ghost mathint ghostHuFaceManagerCallCount {
    init_state axiom ghostHuFaceManagerCallCount == 0;
    axiom ghostHuFaceManagerCallCount >= 0;
}
persistent ghost mathint ghostHuFaceRequestCallbackCount {
    init_state axiom ghostHuFaceRequestCallbackCount == 0;
    axiom ghostHuFaceRequestCallbackCount >= 0;
}

persistent ghost address ghostHuFaceLastCallee;
persistent ghost uint64 ghostHuFaceLastPoolId64;
persistent ghost bytes16 ghostHuFaceLastScId;
persistent ghost uint128 ghostHuFaceLastAssetId128;
persistent ghost bytes32 ghostHuFaceLastPayloadHash;
persistent ghost uint256 ghostHuFaceLastValue256;
persistent ghost uint128 ghostHuFaceLastExtraGasLimit128;
persistent ghost address ghostHuFaceLastRefund;
persistent ghost address ghostHuFaceLastAdmin;
persistent ghost uint128 ghostHuFaceLastCurrency128;
persistent ghost uint256 ghostHuFaceLastAccount256;
persistent ghost uint256 ghostHuFaceLastAccounts0;
persistent ghost uint256 ghostHuFaceLastAccounts1;
persistent ghost uint256 ghostHuFaceLastAccounts2;
persistent ghost uint256 ghostHuFaceLastAccounts3;
persistent ghost bool ghostHuFaceLastIsDebitNormal;
persistent ghost address ghostHuFaceLastValuation;
persistent ghost uint128 ghostHuFaceLastPrice128;
persistent ghost uint16 ghostHuFaceLastCentrifugeId16;
persistent ghost bytes32 ghostHuFaceLastTarget;
persistent ghost uint256 ghostHuFaceLastLocalValue256;
persistent ghost bool ghostHuFaceLastUnpaidMode;
persistent ghost mathint ghostHuFaceLastPayloadLength;
persistent ghost uint8 ghostHuFaceLastPayloadKind8;
persistent ghost uint256 ghostHuFaceLastPayloadId256;
persistent ghost uint128 ghostHuFaceLastPayloadFirst128;
persistent ghost uint128 ghostHuFaceLastPayloadSecond128;

function huHubRegistryCVL(address callee) returns address {
    ghostHuHubRegistryCallee = callee;
    return ghostHuHubRegistry;
}

function huEnterCVL(address callee) {
    havoc ghostHuFaceReverts;
    if (ghostHuFaceReverts) {
        revert("hub refused the call");
    }
    ghostHuFaceLastCallee = callee;
}

function huRecordKeyCVL(uint64 poolId, bytes16 scId, uint128 assetId) {
    ghostHuFaceLastPoolId64 = poolId;
    ghostHuFaceLastScId = scId;
    ghostHuFaceLastAssetId128 = assetId;
}

function huCreatePoolCVL(address callee, uint64 poolId, address admin, uint128 currency) {
    huEnterCVL(callee);
    ghostHuFaceCreatePoolCount = ghostHuFaceCreatePoolCount + 1;
    ghostHuFaceLastPoolId64 = poolId;
    ghostHuFaceLastAdmin = admin;
    ghostHuFaceLastCurrency128 = currency;
}

function huCancelAuthorizationCVL(address callee, uint64 poolId, bytes data) {
    huEnterCVL(callee);
    ghostHuFaceCancelAuthorizationCount = ghostHuFaceCancelAuthorizationCount + 1;
    ghostHuFaceLastPoolId64 = poolId;
    ghostHuFaceLastPayloadHash = keccak256(data);
}

function huCreateAccountCVL(address callee, uint64 poolId, uint256 account, bool isDebitNormal) {
    huEnterCVL(callee);
    ghostHuFaceCreateAccountCount = ghostHuFaceCreateAccountCount + 1;
    ghostHuFaceLastPoolId64 = poolId;
    ghostHuFaceLastAccount256 = account;
    ghostHuFaceLastIsDebitNormal = isDebitNormal;
}

function huSetAccountMetadataCVL(address callee, uint64 poolId, uint256 account, bytes metadata) {
    huEnterCVL(callee);
    ghostHuFaceSetAccountMetadataCount = ghostHuFaceSetAccountMetadataCount + 1;
    ghostHuFaceLastPoolId64 = poolId;
    ghostHuFaceLastAccount256 = account;
    ghostHuFaceLastPayloadHash = keccak256(metadata);
}

function huInitializeHoldingCVL(address callee, uint64 poolId, bytes16 scId, uint128 assetId, address valuation, uint256[4] accounts) {
    huEnterCVL(callee);
    ghostHuFaceInitializeHoldingCount = ghostHuFaceInitializeHoldingCount + 1;
    huRecordKeyCVL(poolId, scId, assetId);
    ghostHuFaceLastValuation = valuation;
    ghostHuFaceLastAccounts0 = accounts[0];
    ghostHuFaceLastAccounts1 = accounts[1];
    ghostHuFaceLastAccounts2 = accounts[2];
    ghostHuFaceLastAccounts3 = accounts[3];
}

function huUpdateHoldingValueCVL(address callee, uint64 poolId, bytes16 scId, uint128 assetId) {
    huEnterCVL(callee);
    ghostHuFaceUpdateHoldingValueCount = ghostHuFaceUpdateHoldingValueCount + 1;
    huRecordKeyCVL(poolId, scId, assetId);
}

function huUpdateHoldingValuationCVL(address callee, uint64 poolId, bytes16 scId, uint128 assetId, address valuation) {
    huEnterCVL(callee);
    ghostHuFaceUpdateHoldingValuationCount = ghostHuFaceUpdateHoldingValuationCount + 1;
    huRecordKeyCVL(poolId, scId, assetId);
    ghostHuFaceLastValuation = valuation;
}

function huUpdateSharePriceCVL(address callee, uint64 poolId, bytes16 scId, uint128 pricePoolPerShare) {
    huEnterCVL(callee);
    ghostHuFaceUpdateSharePriceCount = ghostHuFaceUpdateSharePriceCount + 1;
    ghostHuFaceLastPoolId64 = poolId;
    ghostHuFaceLastScId = scId;
    ghostHuFaceLastPrice128 = pricePoolPerShare;
}

function huManagerCallCVL(address callee, env e, uint64 poolId, uint16 centrifugeId, bytes32 target, bytes payload,
    uint128 extraGasLimit, uint256 localValue, address refund) {
    huEnterCVL(callee);
    ghostHuFaceManagerCallCount = ghostHuFaceManagerCallCount + 1;
    ghostHuFaceLastPoolId64 = poolId;
    ghostHuFaceLastCentrifugeId16 = centrifugeId;
    ghostHuFaceLastTarget = target;
    ghostHuFaceLastPayloadHash = keccak256(payload);
    ghostHuFaceLastExtraGasLimit128 = extraGasLimit;
    ghostHuFaceLastLocalValue256 = localValue;
    ghostHuFaceLastRefund = refund;
    ghostHuFaceLastValue256 = e.msg.value;
}

function huRequestCallbackCVL(address callee, env e, uint64 poolId, bytes16 scId, uint128 assetId, bytes payload,
    uint128 extraGasLimit, bool unpaidMode, address refund) {
    huEnterCVL(callee);
    ghostHuFaceRequestCallbackCount = ghostHuFaceRequestCallbackCount + 1;
    huRecordKeyCVL(poolId, scId, assetId);
    ghostHuFaceLastPayloadHash = keccak256(payload);
    ghostHuFaceLastPayloadLength = payload.length;
    if (payload.length >= 65) {
        ghostHuFaceLastPayloadKind8 = _BytesSlice.toUint8Pure(payload, 0);
        ghostHuFaceLastPayloadId256 = _BytesSlice.toUint256Pure(payload, 1);
        ghostHuFaceLastPayloadFirst128 = _BytesSlice.toUint128Pure(payload, 33);
        ghostHuFaceLastPayloadSecond128 = _BytesSlice.toUint128Pure(payload, 49);
    }
    ghostHuFaceLastExtraGasLimit128 = extraGasLimit;
    ghostHuFaceLastUnpaidMode = unpaidMode;
    ghostHuFaceLastRefund = refund;
    ghostHuFaceLastValue256 = e.msg.value;
}
