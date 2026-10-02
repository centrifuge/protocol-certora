// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {Hub} from "../../src/core/hub/Hub.sol";
import {IHoldings} from "../../src/core/hub/interfaces/IHoldings.sol";
import {IAccounting} from "../../src/core/hub/interfaces/IAccounting.sol";
import {IGateway} from "../../src/core/messaging/interfaces/IGateway.sol";
import {IHubRegistry} from "../../src/core/hub/interfaces/IHubRegistry.sol";
import {IMultiAdapter} from "../../src/core/messaging/interfaces/IMultiAdapter.sol";
import {IShareClassManager} from "../../src/core/hub/interfaces/IShareClassManager.sol";

// The parametric surface for the Hub scenes; empty since the cleanup, kept for symmetry with SpokeHarness.
contract HubHarness is Hub {
    constructor(
        IGateway gateway_,
        IHoldings holdings_,
        IAccounting accounting_,
        IHubRegistry hubRegistry_,
        IMultiAdapter multiAdapter_,
        IShareClassManager shareClassManager_,
        address deployer
    ) Hub(gateway_, holdings_, accounting_, hubRegistry_, multiAdapter_, shareClassManager_, deployer) {}
}
