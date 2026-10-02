// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

// Stubs the confs list so an unresolved seam lands on real bytecode instead of havocking the scene.

// newToken's and newVault's results: the registry probes code.length, so a bare symbolic address
// would make those entries unreachable (SpokeRegistry_cvl.spec:152,211). Empty on purpose.

contract ShareTokenStub {
    uint256 public stubMarker = 1;
}

contract VaultStub {
    uint256 public stubMarker = 2;
}

// sendNotifyShareClass for the Hub scenes, redeclaring ShareClassMetadata because src carries two
// file-scope copies no wildcard entry resolves (type-collision, sanity_warnings_catalog.md).

contract HubSenderStub {
    struct ShareClassMetadata {
        string name;
        string symbol;
        uint8 decimals;
    }

    function sendNotifyShareClass(
        uint16,
        uint64,
        bytes16,
        ShareClassMetadata memory,
        bytes32,
        bytes32,
        bytes calldata,
        uint128,
        address
    ) external payable {}
}

// onBridgeShares for the HubHandler scenes, structs redeclared for the same reason. Only the TYPE
// is live: HubHandler_base.spec:15 summarises the call `=> NONDET`, so this body never runs and
// `result`/`lastCaller` are never read or written.

contract BridgingHookStub {
    struct BridgeSharesParams {
        uint16 originCentrifugeId;
        uint16 targetCentrifugeId;
        uint64 poolId;
        bytes16 scId;
        bytes32 sender;
        bytes32 receiver;
        uint128 amount;
        uint128 extraGasLimit;
        address refund;
    }

    struct BridgeSharesResult {
        bytes32 receiver;
        uint128 amount;
        uint128 extraGasLimit;
        address refund;
    }

    BridgeSharesResult public result;
    address public lastCaller;

    function onBridgeShares(BridgeSharesParams calldata) external returns (BridgeSharesResult memory) {
        lastCaller = msg.sender;
        return result;
    }
}
