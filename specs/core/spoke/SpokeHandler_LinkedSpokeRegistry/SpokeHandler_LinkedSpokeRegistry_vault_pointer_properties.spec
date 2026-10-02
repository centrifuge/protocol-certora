import "setup/SpokeHandler_LinkedSpokeRegistry_vault_pointer.spec";

// --- reachability ---

// SH-RC-17: the hub can link an ERC-20 vault while the share token names no vault for that asset.
rule rcShLinkLeavesTheTokenVaultPointerUnset(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address vault, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address token = ghostSrShareToken;
    address asset = ghostSrIdToAssetAsset[assetId];
    mathint tokenId = ghostSrIdToAssetTokenId256[assetId];
    bool linkedBefore = ghostSrVaultIsLinked[vault];
    address pointerBefore = _ShareToken.vault[asset];

    _SpokeHandler.updateVault(e, poolId, scId, assetId, vault, SpokeHandler.VaultUpdateKind.Link, payload);

    bool linkedAfter = ghostSrVaultIsLinked[vault];
    address pointerAfter = _ShareToken.vault[asset];

    satisfy(token == _ShareToken && tokenId == 0 && asset != 0 && vault != 0
        && VALID_POOL(poolId) && VALID_SC(scId)
        && ghostSrVaultAsset[vault] == asset && ghostSrVaultTokenId256[vault] == 0
        && !linkedBefore && linkedAfter && pointerBefore == 0 && pointerAfter == 0,
        "a vault can be linked while the token's vault pointer stays empty");
}

// SH-RC-18: the hub can unlink an ERC-20 vault while the share token keeps naming it for that asset.
rule rcShUnlinkLeavesTheTokenPointingAtTheUnlinkedVault(env e, SpokeHandler.PoolId poolId,
    SpokeHandler.ShareClassId scId, SpokeHandler.AssetId assetId, address vault, bytes payload) {

    setupSpokeHandlerLinkedSpokeRegistryValidState(e);

    address token = ghostSrShareToken;
    address asset = ghostSrIdToAssetAsset[assetId];
    mathint tokenId = ghostSrIdToAssetTokenId256[assetId];
    bool linkedBefore = ghostSrVaultIsLinked[vault];
    address pointerBefore = _ShareToken.vault[asset];

    _SpokeHandler.updateVault(e, poolId, scId, assetId, vault, SpokeHandler.VaultUpdateKind.Unlink, payload);

    bool linkedAfter = ghostSrVaultIsLinked[vault];
    address pointerAfter = _ShareToken.vault[asset];

    satisfy(token == _ShareToken && tokenId == 0 && asset != 0 && vault != 0
        && VALID_POOL(poolId) && VALID_SC(scId)
        && ghostSrVaultAsset[vault] == asset && ghostSrVaultTokenId256[vault] == 0
        && linkedBefore && !linkedAfter && pointerBefore == vault && pointerAfter == vault,
        "a vault can be unlinked while the token's vault pointer still names it");
}
