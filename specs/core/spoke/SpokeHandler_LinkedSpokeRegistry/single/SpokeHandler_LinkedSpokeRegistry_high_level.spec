import "../setup/SpokeHandler_LinkedSpokeRegistry_base.spec";
import "../setup/SpokeHandler_LinkedSpokeRegistry_pointer_writes.spec";

// SH-HL-01: an incoming cross-chain share transfer mints exactly the transferred amount.
rule hlShExecuteTransferSharesMintsExactlyTheBridgedAmount(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, bytes32 receiver, uint128 amount) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address token = ghostSrShareToken;
    mathint supplyBefore = ghostERC20TotalSupply256[token];

    _SpokeHandler.executeTransferShares(e, poolId, scId, receiver, amount);

    mathint supplyAfter = ghostERC20TotalSupply256[token];

    assert(supplyAfter == supplyBefore + amount, "a bridge arrival raises the share supply by exactly the amount");
}

// SH-HL-02: the receiver of an incoming share transfer gets the full transferred amount.
rule hlShExecuteTransferSharesPaysTheReceiverInFull(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, bytes32 receiver, address recv, uint128 amount) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);
    require(receiver == to_bytes32(recv) << 96, "SAFE: binds the receiver to its encoded address");

    address token = ghostSrShareToken;
    mathint recvBalanceBefore = ghostERC20Balances128[token][recv];

    _SpokeHandler.executeTransferShares(e, poolId, scId, receiver, amount);

    mathint recvBalanceAfter = ghostERC20Balances128[token][recv];

    assert(recvBalanceAfter == recvBalanceBefore + amount,
        "the receiver's balance rises by exactly the bridged amount");
}

// SH-HL-03: the handler keeps none of the shares it mints for a transfer to another receiver.
rule hlShExecuteTransferSharesAddressedPastTheHandlerLeavesNoResidue(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, bytes32 receiver, address recv, uint128 amount) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);
    require(receiver == to_bytes32(recv) << 96, "SAFE: binds the receiver to its encoded address");
    require(recv != _SpokeHandler, "SCOPE: receiver not the handler, SH-HL-02 covers it");

    address token = ghostSrShareToken;
    mathint handlerBalanceBefore = ghostERC20Balances128[token][_SpokeHandler];

    _SpokeHandler.executeTransferShares(e, poolId, scId, receiver, amount);

    mathint handlerBalanceAfter = ghostERC20Balances128[token][_SpokeHandler];

    assert(handlerBalanceAfter == handlerBalanceBefore, "the handler keeps none of the minted shares");
}

// SH-HL-04: a deploy-and-link vault update leaves the new vault linked.
rule hlShDeployAndLinkLeavesTheNewVaultLinked(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address factory, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address vault = ghostHmNewVault;

    _SpokeHandler.updateVault(e, poolId, scId, assetId, factory, SpokeHandler.VaultUpdateKind.DeployAndLink, payload);

    bool linkedAfter = ghostSrVaultIsLinked[vault];

    assert(linkedAfter, "deploy-and-link never yields an unlinked vault");
}

// SH-HL-05: a deploy-and-link update registers the vault for the named pool, class and asset.
rule hlShDeployAndLinkRegistersTheVaultRowTheMessageNames(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address factory, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address vault = ghostHmNewVault;
    address assetRowBefore = ghostSrIdToAssetAsset[assetId];
    mathint tokenIdRowBefore = ghostSrIdToAssetTokenId256[assetId];

    _SpokeHandler.updateVault(e, poolId, scId, assetId, factory, SpokeHandler.VaultUpdateKind.DeployAndLink, payload);

    mathint poolAfter = ghostSrVaultPoolId64[vault];
    bytes16 scAfter = ghostSrVaultScId[vault];
    mathint assetIdAfter = ghostSrVaultAssetId128[vault];
    address assetAfter = ghostSrVaultAsset[vault];
    mathint tokenIdAfter = ghostSrVaultTokenId256[vault];

    assert(poolAfter == poolId && scAfter == scId && assetIdAfter == assetId
        && assetAfter == assetRowBefore && tokenIdAfter == tokenIdRowBefore,
        "a deployed vault is registered under the pool, class and asset named");
}

// SH-HL-06: linking then unlinking a vault restores its original linked status.
rule hlShLinkThenUnlinkRestoresTheRoutingFlag(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address vault, bytes payload1, bytes payload2) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bool linkedBefore = ghostSrVaultIsLinked[vault];

    _SpokeHandler.updateVault(e, poolId, scId, assetId, vault, SpokeHandler.VaultUpdateKind.Link, payload1);
    _SpokeHandler.updateVault(e, poolId, scId, assetId, vault, SpokeHandler.VaultUpdateKind.Unlink, payload2);

    bool linkedAfter = ghostSrVaultIsLinked[vault];

    assert(linkedAfter == linkedBefore, "linking then unlinking restores a vault's link flag");
}

// SH-HL-07: linking then unlinking a vault leaves its pool, share class and asset unchanged.
rule hlShLinkThenUnlinkLeavesTheVaultIdentityUntouched(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address vault, bytes payload1, bytes payload2) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address assetBefore = ghostSrVaultAsset[vault];
    mathint poolBefore = ghostSrVaultPoolId64[vault];
    bytes16 scBefore = ghostSrVaultScId[vault];
    mathint assetIdBefore = ghostSrVaultAssetId128[vault];
    mathint tokenIdBefore = ghostSrVaultTokenId256[vault];

    _SpokeHandler.updateVault(e, poolId, scId, assetId, vault, SpokeHandler.VaultUpdateKind.Link, payload1);
    _SpokeHandler.updateVault(e, poolId, scId, assetId, vault, SpokeHandler.VaultUpdateKind.Unlink, payload2);

    address assetAfter = ghostSrVaultAsset[vault];
    mathint poolAfter = ghostSrVaultPoolId64[vault];
    bytes16 scAfter = ghostSrVaultScId[vault];
    mathint assetIdAfter = ghostSrVaultAssetId128[vault];
    mathint tokenIdAfter = ghostSrVaultTokenId256[vault];

    assert(assetAfter == assetBefore && poolAfter == poolBefore && scAfter == scBefore
        && assetIdAfter == assetIdBefore && tokenIdAfter == tokenIdBefore,
        "linking then unlinking leaves a vault's registration untouched");
}

// SH-HL-08: registering a pool requests exactly one escrow from the escrow factory.
rule hlShAddPoolAsksTheEscrowFactoryExactlyOnce(env e, SpokeHandler.PoolId poolId) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint deploysBefore = ghostEfNewEscrowCount;

    _SpokeHandler.addPool(e, poolId);

    mathint deploysAfter = ghostEfNewEscrowCount;

    assert(deploysAfter == deploysBefore + 1, "adding a pool calls the escrow factory exactly once");
}

// SH-HL-09: registering a pool creates the escrow for that same pool.
rule hlShAddPoolAsksTheEscrowFactoryForThatPool(env e, SpokeHandler.PoolId poolId) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    _SpokeHandler.addPool(e, poolId);

    mathint deployedPoolAfter = ghostEfLastNewEscrowPool64;

    assert(deployedPoolAfter == poolId, "the escrow factory is asked for the pool being added");
}

// SH-HL-10: a request callback is delivered exactly once.
rule hlShRequestCallbackIsDeliveredExactlyOnce(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint callbacksBefore = ghostHmCallbackCount;

    _SpokeHandler.requestCallback(e, poolId, scId, assetId, payload);

    mathint callbacksAfter = ghostHmCallbackCount;

    assert(callbacksAfter == callbacksBefore + 1, "each callback message triggers one delivery, no more");
}

// SH-HL-11: a request callback goes to the pool's registered request manager.
rule hlShRequestCallbackReachesTheRegisteredManager(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address managerBefore = ghostSrRequestManager;

    _SpokeHandler.requestCallback(e, poolId, scId, assetId, payload);

    address calleeAfter = ghostHmCallbackManager;

    assert(calleeAfter == managerBefore, "the callback lands at the request manager the pool had");
}

// SH-HL-12: an authorization granted then revoked leaves all authorizations as they were.
rule hlShGrantThenRevokeLeavesTheLedgerUntouched(env e, SpokeHandler.PoolId poolId, bytes data, bytes32 id) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeHandler.authorize(e, poolId, data);
    _SpokeHandler.unauthorize(e, poolId, data);

    mathint countAfter = ghostSrAuthorizations256[id];

    assert(countAfter == countBefore, "a grant and its revocation leave every grant count unchanged");
}

// SH-HL-13: a new share token uses the message's salt, which must encode the pool's id.
rule hlShAddShareClassDeploysUnderTheMessagesPoolBrandedSalt(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, string name, string symbol, uint8 decimals, bytes32 salt,
    address registrar, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    _SpokeHandler.addShareClass(e, poolId, scId, name, symbol, decimals, salt, registrar, payload);

    assert(ghostRegistrarLastNewTokenSalt == salt
        && (ghostRegistrarLastNewTokenSalt >> 192) == to_bytes32(require_uint256(poolId)),
        "the token deploys under the given salt, which starts with the pool id");
}

// SH-HL-14: a request callback reaches the manager with the pool the message names.
rule hlShRequestCallbackDeliversThePool(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    _SpokeHandler.requestCallback(e, poolId, scId, assetId, payload);

    mathint poolAfter = ghostHmCallbackPool64;

    assert(poolAfter == poolId, "a request callback carries the pool it names");
}

// SH-HL-15: a request callback reaches the manager with the share class the message names.
rule hlShRequestCallbackDeliversTheShareClass(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    _SpokeHandler.requestCallback(e, poolId, scId, assetId, payload);

    bytes16 scIdAfter = ghostHmCallbackScId;

    assert(scIdAfter == scId, "a request callback carries the share class it names");
}

// SH-HL-16: a request callback reaches the manager with the asset the message names.
rule hlShRequestCallbackDeliversTheAsset(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    _SpokeHandler.requestCallback(e, poolId, scId, assetId, payload);

    mathint assetIdAfter = ghostHmCallbackAssetId128;

    assert(assetIdAfter == assetId, "a request callback carries the asset it names");
}

// SH-HL-17: a request callback reaches the manager with its payload unaltered.
rule hlShRequestCallbackDeliversThePayload(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    bytes32 payloadHash = keccak256(payload);

    _SpokeHandler.requestCallback(e, poolId, scId, assetId, payload);

    bytes32 payloadHashAfter = ghostHmCallbackPayloadHash;

    assert(payloadHashAfter == payloadHash, "a request callback carries its payload unchanged");
}

// SH-HL-18: a new share class is bound to the named registrar and the token that registrar deployed.
rule hlShAddShareClassBindsTheRegistrarTheMessageNames(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, string name, string symbol, uint8 decimals, bytes32 salt,
    address registrar, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    _SpokeHandler.addShareClass(e, poolId, scId, name, symbol, decimals, salt, registrar, payload);

    assert(ghostSrRegistrar == registrar && ghostSrShareToken == ghostRegistrarNewToken,
        "the class records the message's registrar and its fresh token");
}

// SH-HL-19: updating the registry or escrow factory address changes only that address.
rule hlShFileMovesOnlyThePointerItNames(env e, bytes32 what, address data) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address registryBefore = _SpokeHandler.spokeRegistry;
    address factoryBefore = _SpokeHandler.escrowFactory;

    _SpokeHandler.file(e, what, data);

    assert(what == FILE_KEY_SPOKE_REGISTRY_SH_CVL()
        => (_SpokeHandler.spokeRegistry == data && _SpokeHandler.escrowFactory == factoryBefore),
        "repointing the registry sets it, the escrow factory untouched");
    assert(what == FILE_KEY_ESCROW_FACTORY_SH_CVL()
        => (_SpokeHandler.escrowFactory == data && _SpokeHandler.spokeRegistry == registryBefore),
        "repointing the escrow factory sets it, the registry untouched");
}

// SH-HL-20: a restriction update is passed unaltered to the registrar of the class's token.
rule hlShUpdateRestrictionReachesTheClassTokenWithItsPayload(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, bytes update) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address token = ghostSrShareToken;
    bytes32 updateHash = keccak256(update);

    _SpokeHandler.updateRestriction(e, poolId, scId, update);

    assert(ghostRegistrarLastRestrictionToken == token && ghostRegistrarLastRestrictionHash == updateHash,
        "a restriction update goes to the class token with the payload as sent");
}

// SH-HL-21: a link or unlink message never writes a share token's vault pointer.
rule hlShLinkAndUnlinkNeverTouchATokenVaultPointer(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address vault,
    SpokeHandler.VaultUpdateKind kind, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);
    require(kind == SpokeHandler.VaultUpdateKind.Link || kind == SpokeHandler.VaultUpdateKind.Unlink,
        "SCOPE: link and unlink only, the factory is a model");

    mathint writesBefore = ghostShTokenPointerWrites;

    _SpokeHandler.updateVault(e, poolId, scId, assetId, vault, kind, payload);

    mathint writesAfter = ghostShTokenPointerWrites;

    assert(writesAfter == writesBefore, "no share token is told of the vault change");
}

// SH-HL-23: setting a policy, even the current one, installs it and voids outstanding authorizations.
rule hlShSetPolicyAlwaysAdvancesTheNamespace(env e, SpokeHandler.PoolId poolId, address policy) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    mathint nonceBefore = ghostSrPolicyNonce64;

    _SpokeHandler.setPolicy(e, poolId, policy);

    assert(ghostSrPolicy == policy && ghostSrPolicyNonce64 == nonceBefore + 1,
        "setting a policy installs it and steps the nonce, even if unchanged");
}
