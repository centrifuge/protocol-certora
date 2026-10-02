// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {PoolId} from "../../src/core/types/PoolId.sol";
import {AssetId} from "../../src/core/types/AssetId.sol";
import {IHubRegistry} from "../../src/core/hub/interfaces/IHubRegistry.sol";

/// @dev Names the decimals(AssetId) and decimals(PoolId) overloads, which CVL cannot tell from decimals(uint256).
contract HubRegistryDecimalsHarness {
    IHubRegistry public registry;

    function assetDecimals(AssetId assetId) external view returns (uint8) {
        return registry.decimals(assetId);
    }

    function poolDecimals(PoolId poolId_) external view returns (uint8) {
        return registry.decimals(poolId_);
    }
}
