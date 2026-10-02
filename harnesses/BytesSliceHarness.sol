// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {BytesLib} from "../../src/misc/libraries/BytesLib.sol";

/// @dev Assembly-free twins of the BytesLib readers a payload is parsed with: the source's unaligned mload
///      defeats the Prover's pointer analysis of every method that inlines one, which then loses the sighash
///      of that method's own calls. Each twin keeps the source's bound and window; a scene summarizes them
///      through certora/specs/shared/bytes_slice.spec.
contract BytesSliceHarness {
    // Twin of BytesLib.slice (BytesLib.sol:12): the same two bounds, and a calldata slice for the copy, which
    // is loop-free as well as assembly-free.
    function slicePure(bytes calldata data, uint256 start, uint256 length_) external pure returns (bytes memory) {
        unchecked {
            require(length_ + 31 >= length_, BytesLib.SliceOverflow());
        }
        require(data.length >= start + length_, BytesLib.SliceOutOfBounds());
        return data[start:start + length_];
    }

    // Twin of BytesLib.sliceZeroPadded (BytesLib.sol:73): the fitting case is slice itself, the short case is
    // slice over the tail the data has, concatenated with the zero padding the source allocates.
    function sliceZeroPaddedPure(bytes calldata data, uint256 start, uint256 length_)
        external
        pure
        returns (bytes memory)
    {
        if (data.length >= start + length_) {
            unchecked {
                require(length_ + 31 >= length_, BytesLib.SliceOverflow());
            }
            return data[start:start + length_];
        }
        uint256 head = data.length - start;
        unchecked {
            require(head + 31 >= head, BytesLib.SliceOverflow());
        }
        return bytes.concat(data[start:data.length], new bytes(length_ + start - data.length));
    }

    // Twin of BytesLib.toUint8 (BytesLib.sol:97): the lowest byte of the word at start + 1 is data[start].
    function toUint8Pure(bytes calldata data, uint256 start) external pure returns (uint8) {
        require(data.length >= start + 1, BytesLib.SliceOutOfBounds());
        return uint8(data[start]);
    }

    // Twin of BytesLib.toUint16 (BytesLib.sol:108): the lowest 2 bytes of the word at start + 2.
    function toUint16Pure(bytes calldata data, uint256 start) external pure returns (uint16) {
        require(data.length >= start + 2, BytesLib.SliceOutOfBounds());
        return uint16(bytes2(data[start:start + 2]));
    }

    // Twin of BytesLib.toUint64 (BytesLib.sol:130): the lowest 8 bytes of the word at start + 8.
    function toUint64Pure(bytes calldata data, uint256 start) external pure returns (uint64) {
        require(data.length >= start + 8, BytesLib.SliceOutOfBounds());
        return uint64(bytes8(data[start:start + 8]));
    }

    // Twin of BytesLib.toUint128 (BytesLib.sol:141): the lowest 16 bytes of the word at start + 16.
    function toUint128Pure(bytes calldata data, uint256 start) external pure returns (uint128) {
        require(data.length >= start + 16, BytesLib.SliceOutOfBounds());
        return uint128(bytes16(data[start:start + 16]));
    }

    // Twin of BytesLib.toUint256 (BytesLib.sol:152): the whole word at start + 32.
    function toUint256Pure(bytes calldata data, uint256 start) external pure returns (uint256) {
        require(data.length >= start + 32, BytesLib.SliceOutOfBounds());
        return uint256(bytes32(data[start:start + 32]));
    }

    // Twin of BytesLib.toBytes32 (BytesLib.sol:163): the whole word at start + 32.
    function toBytes32Pure(bytes calldata data, uint256 start) external pure returns (bytes32) {
        require(data.length >= start + 32, BytesLib.SliceOutOfBounds());
        return bytes32(data[start:start + 32]);
    }

    // Twin of BytesLib.toBytes16 (BytesLib.sol:174): the bytes16 assignment keeps the 16 leading bytes of the
    // word at start + 32, which are data[start .. start + 15].
    function toBytes16Pure(bytes calldata data, uint256 start) external pure returns (bytes16) {
        require(data.length >= start + 16, BytesLib.SliceOutOfBounds());
        return bytes16(data[start:start + 16]);
    }

    // Twin of BytesLib.toAddress (BytesLib.sol:86): the source divides the word at start + 32 by 2^96, which
    // keeps its 20 leading bytes.
    function toAddressPure(bytes calldata data, uint256 start) external pure returns (address) {
        require(data.length >= start + 20, BytesLib.SliceOutOfBounds());
        return address(bytes20(data[start:start + 20]));
    }

    // Twin of CastLib.toBytes32(string): the leading 32 bytes, zero padded, never reverting.
    function stringToBytes32Pure(string calldata source) external pure returns (bytes32) {
        return bytes32(bytes(source));
    }
}
