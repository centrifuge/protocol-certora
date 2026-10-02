// Gateway. Setup: batch gas slots, buffers and the locator array as ghosts.

// Own setup: batch slots, buffers and the locator as ghosts; its importers each summarize paused unlike base.

methods {
    // SAFE: a batch's two slots are keccak images of network and pool.
    function Gateway._gasLimitSlot(uint16 centrifugeId, Gateway.PoolId poolId) internal returns (bytes32)
        => gwGasSlotCVL(centrifugeId, poolId);
    function Gateway._outboundBatchSlot(uint16 centrifugeId, Gateway.PoolId poolId) internal returns (bytes32)
        => gwBatchSlotCVL(centrifugeId, poolId);

    function TransientStorageLib.tstore(bytes32 slot, uint256 value) internal => gwGasStoreCVL(slot, value);
    function TransientStorageLib.tloadUint128(bytes32 slot) internal returns (uint128) => gwGasLoadCVL(slot);

    // SCOPE: a buffer is its length and a content token, its bytes free.
    function TransientBytesLib.get(bytes32 key) internal returns (bytes memory) => gwBufGetCVL(key);
    function TransientBytesLib.append(bytes32 key, bytes memory value) internal => gwBufAppendCVL(key, value);
    function TransientBytesLib.clear(bytes32 key) internal => gwBufClearCVL(key);

    // SAFE: the gateway keeps one locator array, at BATCH_LOCATORS_SLOT.
    function TransientArrayLib.push(bytes32 key, bytes32 value) internal => gwLocPushCVL(value);
    function TransientArrayLib.getBytes32(bytes32 key) internal returns (bytes32[] memory) => gwLocGetCVL();
    function TransientArrayLib.clear(bytes32 key) internal => gwLocClearCVL();

    // SAFE: the locator is its GW_LOCATOR twin, the prover drops its packed pool bytes.
    function Gateway._encodeLocator(uint16 centrifugeId, Gateway.PoolId poolId) internal returns (bytes32)
        => gwLocatorCVL(centrifugeId, poolId);
}

ghost gwGasSlotKey(uint16, uint64) returns bytes32;
ghost gwBatchSlotKey(uint16, uint64) returns bytes32;
ghost gwAppendTok(bytes32, bytes32) returns bytes32;

ghost mapping(bytes32 => uint256) ghostGwGasSlot256;
ghost mapping(bytes32 => uint256) ghostGwBufLen256;
ghost mapping(bytes32 => bytes32) ghostGwBufTok;
ghost uint256 ghostGwLocCount;
ghost mapping(uint256 => bytes32) ghostGwLocAt;

// SAFE: _encodeLocator twin, two network bytes then eight pool bytes.
definition GW_LOCATOR(uint16 c, uint64 p) returns bytes32 =
    to_bytes32(require_uint256(c * 2^240 + p * 2^176));

function gwLocatorCVL(uint16 centrifugeId, Gateway.PoolId poolId) returns bytes32 {
    return GW_LOCATOR(centrifugeId, poolId);
}

function gwGasSlotCVL(uint16 centrifugeId, Gateway.PoolId poolId) returns bytes32 {
    return gwGasSlotKey(centrifugeId, poolId);
}

function gwBatchSlotCVL(uint16 centrifugeId, Gateway.PoolId poolId) returns bytes32 {
    return gwBatchSlotKey(centrifugeId, poolId);
}

function gwGasStoreCVL(bytes32 slot, uint256 value) {
    ghostGwGasSlot256[slot] = value;
}

function gwGasLoadCVL(bytes32 slot) returns uint128 {
    return require_uint128(ghostGwGasSlot256[slot] % 2^128);
}

function gwBufGetCVL(bytes32 key) returns bytes {
    bytes data;
    require(data.length == ghostGwBufLen256[key], "SAFE: a buffer reads back at its filled length");
    return data;
}

function gwBufAppendCVL(bytes32 key, bytes value) {
    mathint len = ghostGwBufLen256[key] + value.length;
    if (len > max_uint256) {
        revert("region length overflow");
    }
    ghostGwBufLen256[key] = require_uint256(len);
    ghostGwBufTok[key] = gwAppendTok(ghostGwBufTok[key], keccak256(value));
}

function gwBufClearCVL(bytes32 key) {
    ghostGwBufLen256[key] = 0;
    ghostGwBufTok[key] = to_bytes32(0);
}

function gwLocPushCVL(bytes32 value) {
    if (ghostGwLocCount == max_uint256) {
        revert("locator count overflow");
    }
    ghostGwLocAt[ghostGwLocCount] = value;
    ghostGwLocCount = require_uint256(ghostGwLocCount + 1);
}

// SCOPE: entries past the third are free, unread at loop_iter 3.
function gwLocGetCVL() returns bytes32[] {
    bytes32[] locators;
    require(locators.length == ghostGwLocCount, "SAFE: the array reads back every locator pushed");
    require(locators.length > 0 => locators[0] == ghostGwLocAt[0], "SAFE: the first locator reads back as pushed");
    require(locators.length > 1 => locators[1] == ghostGwLocAt[1], "SAFE: the second locator reads back as pushed");
    require(locators.length > 2 => locators[2] == ghostGwLocAt[2], "SAFE: the third locator reads back as pushed");
    return locators;
}

function gwLocClearCVL() {
    ghostGwLocCount = 0;
}
