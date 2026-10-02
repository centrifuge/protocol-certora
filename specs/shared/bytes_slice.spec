// BytesLib readers, summarized onto assembly-free twins raising SliceOutOfBounds.

using BytesSliceHarness as _BytesSlice;

methods {
    function _BytesSlice.slicePure(bytes data, uint256 start, uint256 length_) external returns (bytes memory) envfree;
    function _BytesSlice.sliceZeroPaddedPure(bytes data, uint256 start, uint256 length_) external returns (bytes memory) envfree;
    function _BytesSlice.toUint8Pure(bytes data, uint256 start) external returns (uint8) envfree;
    function _BytesSlice.toUint16Pure(bytes data, uint256 start) external returns (uint16) envfree;
    function _BytesSlice.toUint64Pure(bytes data, uint256 start) external returns (uint64) envfree;
    function _BytesSlice.toUint128Pure(bytes data, uint256 start) external returns (uint128) envfree;
    function _BytesSlice.toUint256Pure(bytes data, uint256 start) external returns (uint256) envfree;
    function _BytesSlice.toBytes32Pure(bytes data, uint256 start) external returns (bytes32) envfree;
    function _BytesSlice.toBytes16Pure(bytes data, uint256 start) external returns (bytes16) envfree;
    function _BytesSlice.toAddressPure(bytes data, uint256 start) external returns (address) envfree;

    // TRUSTED: hand-checked twins replace the unaligned mload readers.
    function BytesLib.slice(bytes memory data, uint256 start, uint256 length_) internal returns (bytes memory)
        => bytesSliceCVL(data, start, length_);
    function BytesLib.sliceZeroPadded(bytes memory data, uint256 start, uint256 length_) internal returns (bytes memory)
        => bytesSliceZeroPaddedCVL(data, start, length_);
    function BytesLib.toUint8(bytes memory data, uint256 start) internal returns (uint8)
        => bytesToUint8CVL(data, start);
    function BytesLib.toUint16(bytes memory data, uint256 start) internal returns (uint16)
        => bytesToUint16CVL(data, start);
    function BytesLib.toUint64(bytes memory data, uint256 start) internal returns (uint64)
        => bytesToUint64CVL(data, start);
    function BytesLib.toUint128(bytes memory data, uint256 start) internal returns (uint128)
        => bytesToUint128CVL(data, start);
    function BytesLib.toUint256(bytes memory data, uint256 start) internal returns (uint256)
        => bytesToUint256CVL(data, start);
    function BytesLib.toBytes32(bytes memory data, uint256 start) internal returns (bytes32)
        => bytesToBytes32CVL(data, start);
    function BytesLib.toBytes16(bytes memory data, uint256 start) internal returns (bytes16)
        => bytesToBytes16CVL(data, start);
    function BytesLib.toAddress(bytes memory data, uint256 start) internal returns (address)
        => bytesToAddressCVL(data, start);
}

function bytesSliceCVL(bytes data, uint256 start, uint256 length_) returns bytes {
    bytes value = _BytesSlice.slicePure@withrevert(data, start, length_);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}

function bytesSliceZeroPaddedCVL(bytes data, uint256 start, uint256 length_) returns bytes {
    bytes value = _BytesSlice.sliceZeroPaddedPure@withrevert(data, start, length_);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}

function bytesToUint8CVL(bytes data, uint256 start) returns uint8 {
    uint8 value = _BytesSlice.toUint8Pure@withrevert(data, start);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}

function bytesToUint16CVL(bytes data, uint256 start) returns uint16 {
    uint16 value = _BytesSlice.toUint16Pure@withrevert(data, start);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}

function bytesToUint64CVL(bytes data, uint256 start) returns uint64 {
    uint64 value = _BytesSlice.toUint64Pure@withrevert(data, start);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}

function bytesToUint128CVL(bytes data, uint256 start) returns uint128 {
    uint128 value = _BytesSlice.toUint128Pure@withrevert(data, start);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}

function bytesToUint256CVL(bytes data, uint256 start) returns uint256 {
    uint256 value = _BytesSlice.toUint256Pure@withrevert(data, start);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}

function bytesToBytes32CVL(bytes data, uint256 start) returns bytes32 {
    bytes32 value = _BytesSlice.toBytes32Pure@withrevert(data, start);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}

function bytesToBytes16CVL(bytes data, uint256 start) returns bytes16 {
    bytes16 value = _BytesSlice.toBytes16Pure@withrevert(data, start);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}

function bytesToAddressCVL(bytes data, uint256 start) returns address {
    address value = _BytesSlice.toAddressPure@withrevert(data, start);
    if (lastReverted) {
        revert("SliceOutOfBounds");
    }
    return value;
}
