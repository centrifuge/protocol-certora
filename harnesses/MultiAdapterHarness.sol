// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {PoolId} from "../../src/core/types/PoolId.sol";
import {MultiAdapter} from "../../src/core/messaging/MultiAdapter.sol";
import {IAdapter} from "../../src/core/messaging/interfaces/IAdapter.sol";
import {IMessageHandler} from "../../src/core/messaging/interfaces/IMessageHandler.sol";
import {MAX_ADAPTER_COUNT} from "../../src/core/messaging/interfaces/IMultiAdapter.sol";

// Getters for storage no hook mirrors; both total, so a rule quantifying over slots stays non-vacuous.
contract MultiAdapterHarness is MultiAdapter {
    constructor(uint16 localCentrifugeId_, IMessageHandler gateway_, address deployer)
        MultiAdapter(localCentrifugeId_, gateway_, deployer)
    {}

    // The stashed roster has no ghost mirror.
    function blockedListAt(uint16 centrifugeId, PoolId poolId, uint16 sessionId, uint256 i)
        external
        view
        returns (address)
    {
        IAdapter[] storage list = _blockedSessions[centrifugeId][poolId][sessionId].list;
        return i < list.length ? address(list[i]) : address(0);
    }

    // Packed int16[8]: the per-element Sstore hook collapses to lane 0, so only a const-indexed getter
    // reads a lane faithfully.
    function voteAt(uint16 centrifugeId, bytes32 voteKey, uint256 i) external view returns (int16) {
        return i < MAX_ADAPTER_COUNT ? _votes[centrifugeId][voteKey][i] : int16(0);
    }
}
