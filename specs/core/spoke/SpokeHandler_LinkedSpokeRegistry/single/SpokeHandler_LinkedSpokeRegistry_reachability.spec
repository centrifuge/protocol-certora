import "../setup/SpokeHandler_LinkedSpokeRegistry_base.spec";

// SH-RC-01: a new pool can be registered on the spoke together with its escrow.
rule rcShAddPoolOpensThePoolIsReachable(env e, SpokeHandler.PoolId poolId) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint createdBefore = ghostSrCreatedAt64;
    mathint escrowsBefore = ghostEfNewEscrowCount;

    _SpokeHandler.addPool(e, poolId);

    mathint createdAfter = ghostSrCreatedAt64;
    mathint escrowsAfter = ghostEfNewEscrowCount;

    satisfy(createdBefore == 0 && createdAfter == e.block.timestamp
        && escrowsAfter == escrowsBefore + 1,
        "an unknown pool can be opened now, with one new escrow");
}

// SH-RC-02: a linked vault can be unlinked while keeping its registered asset.
rule rcShUnlinkSwitchesOffALinkedVaultIsReachable(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address vault, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address assetBefore = ghostSrVaultAsset[vault];
    bool linkedBefore = ghostSrVaultIsLinked[vault];

    _SpokeHandler.updateVault(e, poolId, scId, assetId, vault,
        SpokeHandler.VaultUpdateKind.Unlink, payload);

    address assetAfter = ghostSrVaultAsset[vault];
    bool linkedAfter = ghostSrVaultIsLinked[vault];

    satisfy(linkedBefore && !linkedAfter && assetBefore != 0 && assetAfter == assetBefore,
        "a vault can go offline without losing its asset");
}

// SH-RC-03: a zero-amount incoming share transfer can succeed, changing no supply or balance.
rule rcShTransferSharesForAnEmptyLegIsReachable(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, address recv, uint128 amount) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bytes32 receiver = to_bytes32(recv) << 96;
    address token = ghostSrShareToken;
    mathint supplyBefore = ghostERC20TotalSupply256[token];
    mathint recvBalanceBefore = ghostERC20Balances128[token][recv];
    mathint handlerBalanceBefore = ghostERC20Balances128[token][_SpokeHandler];

    _SpokeHandler.executeTransferShares(e, poolId, scId, receiver, amount);

    mathint supplyAfter = ghostERC20TotalSupply256[token];
    mathint recvBalanceAfter = ghostERC20Balances128[token][recv];
    mathint handlerBalanceAfter = ghostERC20Balances128[token][_SpokeHandler];

    satisfy(amount == 0 && supplyAfter == supplyBefore
        && recvBalanceAfter == recvBalanceBefore
        && handlerBalanceAfter == handlerBalanceBefore,
        "a zero bridge arrival can succeed, supply and balances unchanged");
}

// SH-RC-04: shares bridged in can be addressed to the handler itself and stay on it.
rule rcShTransferSharesAddressedToTheHandlerIsReachable(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, address recv, uint128 amount) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bytes32 receiver = to_bytes32(recv) << 96;
    address token = ghostSrShareToken;
    mathint supplyBefore = ghostERC20TotalSupply256[token];
    mathint handlerBalanceBefore = ghostERC20Balances128[token][_SpokeHandler];

    _SpokeHandler.executeTransferShares(e, poolId, scId, receiver, amount);

    mathint supplyAfter = ghostERC20TotalSupply256[token];
    mathint handlerBalanceAfter = ghostERC20Balances128[token][_SpokeHandler];

    satisfy(recv == _SpokeHandler && amount > 0
        && supplyAfter == supplyBefore + amount
        && handlerBalanceAfter == handlerBalanceBefore + amount,
        "a bridge arrival addressed to the handler leaves the shares on it");
}

// SH-RC-05: an account can be granted and then stripped of pool manager rights.
rule rcShManagerSeatRoundTripIsReachable(env e, SpokeHandler.PoolId poolId, address who) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bool seatBefore = ghostSrManager[who];

    _SpokeHandler.updateManager(e, poolId, who, true);

    bool seatBetween = ghostSrManager[who];

    _SpokeHandler.updateManager(e, poolId, who, false);

    bool seatAfter = ghostSrManager[who];

    satisfy(!seatBefore && seatBetween && !seatAfter, "manager rights can be granted and revoked again");
}

// SH-RC-06: an account can be granted and then stripped of share bridging rights.
rule rcShBridgerSeatRoundTripIsReachable(env e, SpokeHandler.PoolId poolId, address who) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bool seatBefore = ghostSrBridger[who];

    _SpokeHandler.updateBridger(e, poolId, who, true);

    bool seatBetween = ghostSrBridger[who];

    _SpokeHandler.updateBridger(e, poolId, who, false);

    bool seatAfter = ghostSrBridger[who];

    satisfy(!seatBefore && seatBetween && !seatAfter, "bridger rights can be granted and revoked again");
}

// SH-RC-07: a pool's policy can be removed, which also invalidates its outstanding authorizations.
rule rcShPolicyRemovalIsReachable(env e, SpokeHandler.PoolId poolId, address newPolicy) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;

    _SpokeHandler.setPolicy(e, poolId, newPolicy);

    address policyAfter = ghostSrPolicy;
    mathint nonceAfter = ghostSrPolicyNonce64;

    satisfy(newPolicy == 0 && policyBefore != 0 && policyAfter == 0
        && nonceAfter == nonceBefore + 1,
        "a pool's policy can be removed, its nonce still stepping by one");
}

// SH-RC-08: the same call can hold two outstanding authorizations at once.
rule rcShGrantsStackOnOneRowIsReachable(env e, SpokeHandler.PoolId poolId, bytes data) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address policyBefore = ghostSrPolicy;
    uint64 nonceBefore = ghostSrPolicyNonce64;
    bytes32 id = ghostSrAuthId[poolId][policyBefore][nonceBefore][keccak256(data)];
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeHandler.authorize(e, poolId, data);

    mathint countBetween = ghostSrAuthorizations256[id];

    _SpokeHandler.authorize(e, poolId, data);

    mathint countAfter = ghostSrAuthorizations256[id];

    satisfy(countBetween == countBefore + 1 && countAfter == countBefore + 2,
        "the same call can be granted twice, both grants standing");
}

// SH-RC-09: a share price can be replaced by a more recent one.
rule rcShSharePriceMovingToALaterStampIsReachable(env e, SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId,
    SpokeHandler.D18 price, uint64 computedAt) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeHandler.updatePricePoolPerShare(e, poolId, scId, price, computedAt);

    mathint priceAfter = ghostSrPricePoolPerShare128;
    mathint stampAfter = ghostSrPricePoolPerShareComputedAt64;

    satisfy(priceAfter == price && stampAfter == computedAt
        && stampAfter > stampBefore,
        "a fresher share price can replace the one on record");
}

// SH-RC-10: a non-zero share price can be replaced by a zero price.
rule rcShSharePriceCanBeMarkedToZeroIsReachable(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.D18 price, uint64 computedAt) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint priceBefore = ghostSrPricePoolPerShare128;
    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeHandler.updatePricePoolPerShare(e, poolId, scId, price, computedAt);

    mathint priceAfter = ghostSrPricePoolPerShare128;
    mathint stampAfter = ghostSrPricePoolPerShareComputedAt64;

    satisfy(priceBefore > 0 && price == 0 && priceAfter == 0
        && stampAfter > stampBefore,
        "a priced class can be marked to zero at a newer stamp");
}

// SH-RC-11: a registered asset's price can be replaced by a more recent one.
rule rcShAssetPriceMovingToALaterStampIsReachable(env e, SpokeHandler.PoolId poolId, SpokeHandler.ShareClassId scId,
    SpokeHandler.AssetId assetId, SpokeHandler.D18 price, uint64 computedAt) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address assetRowBefore = ghostSrIdToAssetAsset[assetId];
    mathint stampBefore = ghostSrPricePoolPerAssetComputedAt64[assetId];

    _SpokeHandler.updatePricePoolPerAsset(e, poolId, scId, assetId, price, computedAt);

    mathint priceAfter = ghostSrPricePoolPerAsset128[assetId];
    mathint stampAfter = ghostSrPricePoolPerAssetComputedAt64[assetId];

    satisfy(assetRowBefore != 0 && priceAfter == price
        && stampAfter == computedAt && stampAfter > stampBefore,
        "a fresher price for a registered asset can replace the old one");
}

// SH-RC-12: a pool without a request manager can be assigned one.
rule rcShRequestManagerAppointmentIsReachable(env e, SpokeHandler.PoolId poolId, address manager) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address managerBefore = ghostSrRequestManager;

    _SpokeHandler.setRequestManager(e, poolId, manager);

    address managerAfter = ghostSrRequestManager;

    satisfy(managerBefore == 0 && manager != 0 && managerAfter == manager,
        "a manager-less pool can gain a request manager");
}

// SH-RC-13: a pool's request manager can be removed by setting the zero address.
rule rcShRequestManagerWithdrawalIsReachable(env e, SpokeHandler.PoolId poolId, address manager,
    address replacement) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    _SpokeHandler.setRequestManager(e, poolId, manager);

    address managerBetween = ghostSrRequestManager;

    _SpokeHandler.setRequestManager(e, poolId, replacement);

    address managerAfter = ghostSrRequestManager;

    satisfy(manager != 0 && managerBetween == manager && replacement == 0 && managerAfter == 0,
        "a seated request manager can be unset again");
}

// SH-RC-14: an admin can repoint the handler to a different escrow factory.
rule rcShFileRepointsTheEscrowFactoryIsReachable(env e, address data) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address factoryBefore = _SpokeHandler.escrowFactory;

    _SpokeHandler.file(e, FILE_KEY_ESCROW_FACTORY_SH_CVL(), data);

    address factoryAfter = _SpokeHandler.escrowFactory;

    satisfy(data != 0 && factoryAfter == data && factoryAfter != factoryBefore,
        "the handler can be repointed to another escrow factory");
}

// SH-RC-15: an admin can repoint the handler to a different spoke registry.
rule rcShFileRepointsTheSpokeRegistryIsReachable(env e, address data) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address registryBefore = _SpokeHandler.spokeRegistry;

    _SpokeHandler.file(e, FILE_KEY_SPOKE_REGISTRY_SH_CVL(), data);

    address registryAfter = _SpokeHandler.spokeRegistry;

    satisfy(data != 0 && registryAfter == data && registryAfter != registryBefore,
        "the handler can be repointed to another registry");
}

// SH-RC-16: admin rights over the handler can be granted and then revoked.
rule rcShWardRoundTripIsReachable(env e, address u) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint wardBefore = _SpokeHandler.wards(e, u);

    _SpokeHandler.rely(e, u);

    mathint wardBetween = _SpokeHandler.wards(e, u);

    _SpokeHandler.deny(e, u);

    mathint wardAfter = _SpokeHandler.wards(e, u);

    satisfy(wardBefore == 0 && wardBetween == 1 && wardAfter == 0,
        "ward rights can be granted and revoked in one transaction");
}

// SH-RC-19: a share price stamped at the spoke's current time can be recorded.
rule rcShSharePriceStampedAtTheLocalClockIsReachable(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.D18 price, uint64 computedAt) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeHandler.updatePricePoolPerShare(e, poolId, scId, price, computedAt);

    mathint stampAfter = ghostSrPricePoolPerShareComputedAt64;

    satisfy(computedAt == e.block.timestamp && stampAfter == computedAt && stampAfter > stampBefore,
        "the hub can stamp a share price at the spoke's current time");
}

// SH-RC-20: a registered asset's price stamped at the spoke's current time can be recorded.
rule rcShAssetPriceStampedAtTheLocalClockIsReachable(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, SpokeHandler.D18 price, uint64 computedAt) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrPricePoolPerAssetComputedAt64[assetId];

    _SpokeHandler.updatePricePoolPerAsset(e, poolId, scId, assetId, price, computedAt);

    mathint stampAfter = ghostSrPricePoolPerAssetComputedAt64[assetId];

    satisfy(computedAt == e.block.timestamp && stampAfter == computedAt && stampAfter > stampBefore,
        "the hub can stamp an asset price at the spoke's current time");
}
