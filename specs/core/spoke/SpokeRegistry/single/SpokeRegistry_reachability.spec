import "SpokeRegistry_valid_state.spec";

// SR-RC-01: a pool can be added, recording the current block time as its creation time.
rule rcSrAddPoolIsReachable(env e, SpokeRegistry.PoolId poolId) {

    setupSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrCreatedAt64;

    _SpokeRegistry.addPool(e, poolId);

    mathint stampAfter = ghostSrCreatedAt64;

    satisfy(stampBefore == 0 && stampAfter == e.block.timestamp && stampAfter != 0,
        "a pool can be opened, stamped with the current time");
}

// SR-RC-02: a newly added pool can read as active in the same transaction.
rule rcSrPoolReadsActiveRightAfterAddIsReachable(env e, SpokeRegistry.PoolId poolId) {

    setupSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrCreatedAt64;

    _SpokeRegistry.addPool(e, poolId);

    bool activeAfter = _SpokeRegistry.isPoolActive(e, poolId);

    satisfy(stampBefore == 0 && activeAfter, "a pool reads as active in the transaction that opened it");
}

// SR-RC-03: a share class can move to a new token, unmapping the old one.
rule rcSrTokenSwapRetiringTheOutgoingTokenIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, address shareToken_, address registrar_) {

    setupSpokeRegistryValidState(e);

    address incumbent = ghostSrShareToken;

    _SpokeRegistry.linkToken(e, poolId, scId, shareToken_, registrar_);

    address tokenAfter = ghostSrShareToken;
    mathint retiredPoolAfter = ghostSrTokenPoolId64[incumbent];
    bytes16 retiredClassAfter = ghostSrTokenScId[incumbent];
    mathint adoptedPoolAfter = ghostSrTokenPoolId64[shareToken_];

    satisfy(incumbent != 0 && incumbent != shareToken_ && tokenAfter == shareToken_
        && retiredPoolAfter == 0 && retiredClassAfter == to_bytes16(0)
        && adoptedPoolAfter == ghostPoolA64,
        "a class can move to a new token, the old token's lookup cleared");
}

// SR-RC-04: a share class can change its registrar while keeping its token.
rule rcSrRegistrarSwapKeepingTheIncumbentTokenIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, address registrar_) {

    setupSpokeRegistryValidState(e);

    address incumbent = ghostSrShareToken;
    address registrarBefore = ghostSrRegistrar;

    _SpokeRegistry.linkToken(e, poolId, scId, incumbent, registrar_);

    address tokenAfter = ghostSrShareToken;
    address registrarAfter = ghostSrRegistrar;
    mathint reversePoolAfter = ghostSrTokenPoolId64[incumbent];

    satisfy(incumbent != 0 && tokenAfter == incumbent && registrarAfter != registrarBefore
        && reversePoolAfter == ghostPoolA64,
        "a new registrar can take over while the class token stays");
}

// SR-RC-05: a request manager can be installed on a pool that had none.
rule rcSrSetRequestManagerIsReachable(env e, SpokeRegistry.PoolId poolId, address manager_) {

    setupSpokeRegistryValidState(e);

    address managerBefore = ghostSrRequestManager;

    _SpokeRegistry.setRequestManager(e, poolId, manager_);

    address managerAfter = ghostSrRequestManager;

    satisfy(managerBefore == 0 && managerAfter == manager_ && managerAfter != 0,
        "an empty request manager seat can be filled");
}

// SR-RC-06: a pool's request manager can be cleared, switching requests off.
rule rcSrClearingTheRequestManagerIsReachable(env e, SpokeRegistry.PoolId poolId, address manager_) {

    setupSpokeRegistryValidState(e);

    address managerBefore = ghostSrRequestManager;

    _SpokeRegistry.setRequestManager(e, poolId, manager_);

    address managerAfter = ghostSrRequestManager;

    satisfy(managerBefore != 0 && managerAfter == 0, "a pool can lose its request manager");
}

// SR-RC-07: manager rights can be granted to one account while another stays without them.
rule rcSrGrantingOneManagerSeatIsReachable(env e, SpokeRegistry.PoolId poolId, address who, address other) {

    setupSpokeRegistryValidState(e);

    bool whoBefore = ghostSrManager[who];

    _SpokeRegistry.updateManager(e, poolId, who, true);

    bool whoAfter = ghostSrManager[who];
    bool otherAfter = ghostSrManager[other];

    satisfy(who != other && !whoBefore && whoAfter && !otherAfter,
        "one account can become manager while another stays out");
}

// SR-RC-08: one of two pool managers can lose its rights while the other keeps them.
rule rcSrRevokingOneOfTwoManagerSeatsIsReachable(env e, SpokeRegistry.PoolId poolId, address who, address other) {

    setupSpokeRegistryValidState(e);

    bool whoBefore = ghostSrManager[who];
    bool otherBefore = ghostSrManager[other];

    _SpokeRegistry.updateManager(e, poolId, who, false);

    bool whoAfter = ghostSrManager[who];
    bool otherAfter = ghostSrManager[other];

    satisfy(who != other && whoBefore && otherBefore && !whoAfter && otherAfter,
        "one manager can be revoked while another keeps the right");
}

// SR-RC-09: an account can get bridger rights without holding manager rights.
rule rcSrGrantingTheBridgerSeatAloneIsReachable(env e, SpokeRegistry.PoolId poolId, address who) {

    setupSpokeRegistryValidState(e);

    bool bridgerBefore = ghostSrBridger[who];

    _SpokeRegistry.updateBridger(e, poolId, who, true);

    bool bridgerAfter = ghostSrBridger[who];
    bool managerAfter = ghostSrManager[who];

    satisfy(!bridgerBefore && bridgerAfter && !managerAfter,
        "bridger rights can be granted to an account that is not a manager");
}

// SR-RC-10: a pool's first policy can be installed, starting its install count at one.
rule rcSrFirstPolicyInstallIsReachable(env e, SpokeRegistry.PoolId poolId, address newPolicy) {

    setupSpokeRegistryValidState(e);

    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;

    _SpokeRegistry.setPolicy(e, poolId, newPolicy);

    address policyAfter = ghostSrPolicy;
    mathint nonceAfter = ghostSrPolicyNonce64;

    satisfy(policyBefore == 0 && nonceBefore == 0 && policyAfter == newPolicy && policyAfter != 0
        && nonceAfter == 1,
        "a pool's first policy can be installed, its policy nonce becoming one");
}

// SR-RC-11: a pool's policy can be replaced by another, advancing its install count.
rule rcSrPolicyReplacementIsReachable(env e, SpokeRegistry.PoolId poolId, address newPolicy) {

    setupSpokeRegistryValidState(e);

    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;

    _SpokeRegistry.setPolicy(e, poolId, newPolicy);

    address policyAfter = ghostSrPolicy;
    mathint nonceAfter = ghostSrPolicyNonce64;

    satisfy(policyBefore != 0 && newPolicy != policyBefore && newPolicy != 0 && policyAfter == newPolicy
        && nonceAfter == nonceBefore + 1,
        "a policy can be replaced by another, its nonce up by one");
}

// SR-RC-12: a pool's policy can be removed, which still advances its install count.
rule rcSrClearingThePolicyIsReachable(env e, SpokeRegistry.PoolId poolId, address clearedPolicy) {

    setupSpokeRegistryValidState(e);

    address policyBefore = ghostSrPolicy;
    mathint nonceBefore = ghostSrPolicyNonce64;

    _SpokeRegistry.setPolicy(e, poolId, clearedPolicy);

    address policyAfter = ghostSrPolicy;
    mathint nonceAfter = ghostSrPolicyNonce64;

    satisfy(policyBefore != 0 && policyAfter == 0 && nonceAfter == nonceBefore + 1,
        "a policy can be cleared, its nonce still up by one");
}

// SR-RC-13: an admin can grant an authorization under the pool's installed policy.
rule rcSrAuthorizeIsReachable(env e, SpokeRegistry.PoolId poolId, bytes data) {

    setupSpokeRegistryValidState(e);
    require(data.length == 0, "SCOPE: an empty authorization payload");

    bytes32 id = _SpokeRegistry.authId(e, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.authorize(e, poolId, data);

    mathint countAfter = ghostSrAuthorizations256[id];
    address policyAfter = ghostSrPolicy;

    satisfy(countBefore == 0 && countAfter == 1 && policyAfter != 0,
        "a first grant can be recorded under the installed policy");
}

// SR-RC-14: the same call can be authorized twice, with both grants counted.
rule rcSrTwoOutstandingGrantsAreReachable(env e, SpokeRegistry.PoolId poolId, bytes data) {

    setupSpokeRegistryValidState(e);
    require(data.length == 0, "SCOPE: an empty authorization payload");

    bytes32 id = _SpokeRegistry.authId(e, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.authorize(e, poolId, data);

    mathint countAfter = ghostSrAuthorizations256[id];

    satisfy(countBefore == 0 && countAfter == 2, "the same call can be granted twice, the count reaching two");
}

// SR-RC-15: an unspent authorization can be revoked, leaving none outstanding.
rule rcSrUnauthorizeEmptyingTheRowIsReachable(env e, SpokeRegistry.PoolId poolId, bytes data) {

    setupSpokeRegistryValidState(e);
    require(data.length == 0, "SCOPE: an empty authorization payload");

    bytes32 id = _SpokeRegistry.authId(e, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.authorize(e, poolId, data);

    mathint countMid = ghostSrAuthorizations256[id];

    _SpokeRegistry.unauthorize(e, poolId, data);

    mathint countAfter = ghostSrAuthorizations256[id];

    satisfy(countBefore == 0 && countMid == 1 && countAfter == 0,
        "a grant can be revoked before use, the count back to zero");
}

// SR-RC-16: the pool's policy can spend an authorization granted for it.
rule rcSrPolicyConsumingAGrantIsReachable(env e, env ePolicy, SpokeRegistry.PoolId poolId, address caller,
    bytes data) {

    setupSpokeRegistryValidState(e);
    setupSpokeRegistryValidState(ePolicy);
    require(data.length == 0, "SCOPE: an empty authorization payload");

    bytes32 id = _SpokeRegistry.authId(e, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.consumeAuthorization(ePolicy, poolId, caller, data);

    mathint countAfter = ghostSrAuthorizations256[id];
    address policyAfter = ghostSrPolicy;

    satisfy(countBefore == 0 && countAfter == 0 && ePolicy.msg.sender == policyAfter,
        "the installed policy can spend a grant, the count back to zero");
}

// SR-RC-17: the policy can spend one of two authorizations, leaving the other for later.
rule rcSrConsumingOneOfTwoGrantsIsReachable(env e, env ePolicy, SpokeRegistry.PoolId poolId, address caller,
    bytes data) {

    setupSpokeRegistryValidState(e);
    setupSpokeRegistryValidState(ePolicy);
    require(data.length == 0, "SCOPE: an empty authorization payload");

    bytes32 id = _SpokeRegistry.authId(e, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.consumeAuthorization(ePolicy, poolId, caller, data);

    mathint countAfter = ghostSrAuthorizations256[id];

    satisfy(countBefore == 0 && countAfter == 1, "one of two grants can be spent, leaving one standing");
}

// SR-RC-18: after a policy change, a revocation can leave the old policy's grant in place.
rule rcSrPolicySwapPuttingGrantsBeyondRevocationIsReachable(env e, SpokeRegistry.PoolId poolId,
    address newPolicy, bytes data) {

    setupSpokeRegistryValidState(e);
    require(data.length == 0, "SCOPE: an empty authorization payload");

    bytes32 idOld = _SpokeRegistry.authId(e, poolId, data);
    mathint orphanedBefore = ghostSrAuthorizations256[idOld];

    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.setPolicy(e, poolId, newPolicy);
    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.unauthorize(e, poolId, data);

    bytes32 idNew = _SpokeRegistry.authId(e, poolId, data);
    mathint orphanedAfter = ghostSrAuthorizations256[idOld];
    mathint currentAfter = ghostSrAuthorizations256[idNew];

    satisfy(idNew != idOld && orphanedBefore == 0 && orphanedAfter == 1 && currentAfter == 0,
        "after a policy swap a revocation clears the new grant, not the old");
}

// SR-RC-19: the first asset can be registered and resolves both ways between id and asset.
rule rcSrFirstAssetNumberIsReachable(env e, uint16 centrifugeId, address asset, uint256 tokenId) {

    setupSpokeRegistryValidState(e);

    mathint counterBefore = ghostSrAssetCounter64;

    SpokeRegistry.AssetId newId = _SpokeRegistry.createAssetId(e, centrifugeId, asset, tokenId);

    uint128 issuedId = newId;
    mathint counterAfter = ghostSrAssetCounter64;
    address forwardAssetAfter = ghostSrIdToAssetAsset[issuedId];
    mathint forwardTokenIdAfter = ghostSrIdToAssetTokenId256[issuedId];
    mathint reverseIdAfter = ghostSrAssetToId128[asset][tokenId];

    satisfy(counterBefore == 0 && counterAfter == 1 && forwardAssetAfter == asset
        && forwardTokenIdAfter == tokenId && reverseIdAfter == issuedId,
        "the first asset id can be issued, resolving both ways");
}

// SR-RC-20: a second asset can be registered under its own distinct id.
rule rcSrSecondAssetPairTakingItsOwnNumberIsReachable(env e, uint16 firstChainId, uint16 secondChainId,
    address firstAsset, address secondAsset, uint256 firstTokenId, uint256 secondTokenId) {

    setupSpokeRegistryValidState(e);

    mathint counterBefore = ghostSrAssetCounter64;

    SpokeRegistry.AssetId firstId = _SpokeRegistry.createAssetId(e, firstChainId, firstAsset, firstTokenId);
    SpokeRegistry.AssetId secondId = _SpokeRegistry.createAssetId(e, secondChainId, secondAsset, secondTokenId);

    uint128 firstIssued = firstId;
    uint128 secondIssued = secondId;
    mathint counterAfter = ghostSrAssetCounter64;
    address firstAssetAfter = ghostSrIdToAssetAsset[firstIssued];
    address secondAssetAfter = ghostSrIdToAssetAsset[secondIssued];

    satisfy(firstIssued != secondIssued && counterAfter == counterBefore + 2
        && firstAssetAfter == firstAsset && secondAssetAfter == secondAsset,
        "a second asset pair can get its own id, both resolving");
}

// SR-RC-21: an asset id can be issued for one token of a multi-token (ERC6909) contract.
rule rcSrNumberingAMultiTokenAssetPairIsReachable(env e, uint16 centrifugeId, address asset, uint256 tokenId) {

    setupSpokeRegistryValidState(e);
    require(tokenId != 0, "SCOPE: one token of a multi-token asset");

    SpokeRegistry.AssetId newId = _SpokeRegistry.createAssetId(e, centrifugeId, asset, tokenId);

    uint128 issuedId = newId;
    address forwardAssetAfter = ghostSrIdToAssetAsset[issuedId];
    mathint forwardTokenIdAfter = ghostSrIdToAssetTokenId256[issuedId];
    mathint reverseIdAfter = ghostSrAssetToId128[asset][tokenId];

    satisfy(forwardAssetAfter == asset && forwardTokenIdAfter == tokenId && reverseIdAfter == issuedId,
        "one token of a multi-token asset can get an id resolving both ways");
}

// SR-RC-22: an asset id can be issued under network id 1, the lowest valid one.
rule rcSrAssetNumberOnTheSmallestOriginChainIsReachable(env e, uint16 centrifugeId, address asset,
    uint256 tokenId) {

    setupSpokeRegistryValidState(e);
    require(centrifugeId == 1, "SCOPE: origin network 1, the smallest legal one");

    SpokeRegistry.AssetId newId = _SpokeRegistry.createAssetId(e, centrifugeId, asset, tokenId);

    uint128 issuedId = newId;
    mathint issuedChainHalf = issuedId / 2^112;
    address forwardAssetAfter = ghostSrIdToAssetAsset[issuedId];

    satisfy(issuedChainHalf == 1 && forwardAssetAfter == asset,
        "an asset id can be issued under the smallest network id");
}

// SR-RC-23: a new asset id can be looked up both ways at once, without reverting.
rule rcSrCheckedAssetLookupsAfterNumberingAreReachable(env e, uint16 centrifugeId, address asset,
    uint256 tokenId) {

    setupSpokeRegistryValidState(e);

    SpokeRegistry.AssetId newId = _SpokeRegistry.createAssetId(e, centrifugeId, asset, tokenId);

    SpokeRegistry.AssetId lookedUpId = _SpokeRegistry.assetToId(e, asset, tokenId, true);

    address resolvedAsset;
    uint256 resolvedTokenId;
    resolvedAsset, resolvedTokenId = _SpokeRegistry.idToAsset(e, newId, true);

    satisfy(lookedUpId == newId && resolvedAsset == asset
        && resolvedTokenId == tokenId,
        "both strict lookups answer for a pair just numbered");
}

// SR-RC-24: a vault can be registered for a share class and an ERC20 asset, still unlinked.
rule rcSrRegisterVaultIsReachable(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.AssetId assetId, address asset, uint256 tokenId, address factory, address vault_, bytes payload) {

    setupSpokeRegistryValidState(e);
    require(tokenId == 0, "SCOPE: a plain ERC20 asset");
    require(payload.length == 0, "SCOPE: an empty deployment payload");

    address vaultAssetBefore = ghostSrVaultAsset[vault_];

    _SpokeRegistry.registerVault(e, poolId, scId, assetId, asset, tokenId, factory, vault_, payload);

    address vaultAssetAfter = ghostSrVaultAsset[vault_];
    mathint vaultAssetIdAfter = ghostSrVaultAssetId128[vault_];
    mathint vaultPoolAfter = ghostSrVaultPoolId64[vault_];
    bool linkedAfter = ghostSrVaultIsLinked[vault_];

    satisfy(vaultAssetBefore == 0 && vaultAssetAfter == asset && vaultAssetIdAfter == assetId
        && vaultPoolAfter == ghostPoolA64 && !linkedAfter,
        "an ERC20 vault can be filed under a pool, not yet linked");
}

// SR-RC-25: a vault can be registered for one token of a multi-token asset contract.
rule rcSrRegisterMultiTokenVaultIsReachable(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.AssetId assetId, address asset, uint256 tokenId, address factory, address vault_, bytes payload) {

    setupSpokeRegistryValidState(e);
    require(tokenId != 0, "SCOPE: one token of a multi-token asset");
    require(payload.length == 0, "SCOPE: an empty deployment payload");

    address vaultAssetBefore = ghostSrVaultAsset[vault_];

    _SpokeRegistry.registerVault(e, poolId, scId, assetId, asset, tokenId, factory, vault_, payload);

    address vaultAssetAfter = ghostSrVaultAsset[vault_];
    mathint vaultTokenIdAfter = ghostSrVaultTokenId256[vault_];
    bool linkedAfter = ghostSrVaultIsLinked[vault_];

    satisfy(vaultAssetBefore == 0 && vaultAssetAfter == asset && vaultTokenIdAfter == tokenId
        && !linkedAfter,
        "an unlinked vault can be filed for a single token id");
}

// SR-RC-26: a registered vault can be linked so that it starts serving investors.
rule rcSrLinkVaultIsReachable(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.AssetId assetId, address vault_) {

    setupSpokeRegistryValidState(e);

    bool linkedBefore = ghostSrVaultIsLinked[vault_];
    address vaultAssetBefore = ghostSrVaultAsset[vault_];

    _SpokeRegistry.linkVault(e, poolId, scId, assetId, vault_);

    bool linkedAfter = ghostSrVaultIsLinked[vault_];

    satisfy(!linkedBefore && vaultAssetBefore != 0 && linkedAfter, "a registered vault can be linked");
}

// SR-RC-27: a linked vault can be unlinked while staying registered.
rule rcSrUnlinkVaultIsReachable(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.AssetId assetId, address vault_) {

    setupSpokeRegistryValidState(e);

    bool linkedBefore = ghostSrVaultIsLinked[vault_];

    _SpokeRegistry.unlinkVault(e, poolId, scId, assetId, vault_);

    bool linkedAfter = ghostSrVaultIsLinked[vault_];
    address vaultAssetAfter = ghostSrVaultAsset[vault_];

    satisfy(linkedBefore && !linkedAfter && vaultAssetAfter != 0, "unlinking need not drop a vault's registration");
}

// SR-RC-28: a vault can be linked, unlinked and linked again in one transaction.
rule rcSrWithdrawingAndRestoringVaultServiceIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, address vault_) {

    setupSpokeRegistryValidState(e);

    bool linkedBefore = ghostSrVaultIsLinked[vault_];

    _SpokeRegistry.linkVault(e, poolId, scId, assetId, vault_);

    bool linkedAfterFirstLink = ghostSrVaultIsLinked[vault_];

    _SpokeRegistry.unlinkVault(e, poolId, scId, assetId, vault_);

    bool linkedAfterUnlink = ghostSrVaultIsLinked[vault_];

    _SpokeRegistry.linkVault(e, poolId, scId, assetId, vault_);

    bool linkedAfter = ghostSrVaultIsLinked[vault_];
    address vaultAssetAfter = ghostSrVaultAsset[vault_];

    satisfy(!linkedBefore && linkedAfterFirstLink && !linkedAfterUnlink && linkedAfter && vaultAssetAfter != 0,
        "one transaction can link, drop and relink a vault");
}

// SR-RC-29: a newly linked vault can read back as linked and registered.
rule rcSrLinkedVaultReadingBackThroughItsViewsIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, address vault_) {

    setupSpokeRegistryValidState(e);

    bool linkedBefore = ghostSrVaultIsLinked[vault_];

    _SpokeRegistry.linkVault(e, poolId, scId, assetId, vault_);

    bool linkedRead = _SpokeRegistry.isLinked(e, vault_);
    bool registeredRead = _SpokeRegistry.isVaultRegistered(e, vault_);
    mathint vaultAssetIdAfter = ghostSrVaultAssetId128[vault_];

    satisfy(!linkedBefore && linkedRead && registeredRead && vaultAssetIdAfter == assetId,
        "the views confirm a freshly linked vault and its asset");
}

// SR-RC-30: a share class can receive its first price together with its computation time.
rule rcSrFirstSharePriceIsReachable(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeRegistry.updatePricePoolPerShare(e, poolId, scId, price, computedAt);

    mathint stampAfter = ghostSrPricePoolPerShareComputedAt64;
    mathint priceAfter = ghostSrPricePoolPerShare128;

    satisfy(stampBefore == 0 && stampAfter == computedAt && stampAfter != 0
        && priceAfter == price && priceAfter != 0,
        "a class's first share price can be stored with its stamp");
}

// SR-RC-31: a share price can be replaced by one computed at a later time.
rule rcSrSharePriceMovingToALaterStampIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeRegistry.updatePricePoolPerShare(e, poolId, scId, price, computedAt);

    mathint stampAfter = ghostSrPricePoolPerShareComputedAt64;
    mathint priceAfter = ghostSrPricePoolPerShare128;

    satisfy(stampBefore != 0 && stampAfter > stampBefore && priceAfter == price,
        "a share price can be moved to a later stamp");
}

// SR-RC-32: a share price can be corrected while keeping the same computation time.
rule rcSrSharePriceCorrectionAtTheSameStampIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.D18 price) {

    setupSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;
    mathint priceBefore = ghostSrPricePoolPerShare128;
    uint64 sameStamp = require_uint64(stampBefore);

    _SpokeRegistry.updatePricePoolPerShare(e, poolId, scId, price, sameStamp);

    mathint stampAfter = ghostSrPricePoolPerShareComputedAt64;
    mathint priceAfter = ghostSrPricePoolPerShare128;

    satisfy(stampBefore != 0 && stampAfter == stampBefore && priceAfter != priceBefore,
        "a share price can be corrected at its current stamp");
}

// SR-RC-33: an asset of a share class can receive its first price with its computation time.
rule rcSrFirstAssetPriceIsReachable(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.AssetId assetId, SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    uint128 pricedAssetId = assetId;
    mathint stampBefore = ghostSrPricePoolPerAssetComputedAt64[pricedAssetId];

    _SpokeRegistry.updatePricePoolPerAsset(e, poolId, scId, assetId, price, computedAt);

    mathint stampAfter = ghostSrPricePoolPerAssetComputedAt64[pricedAssetId];
    mathint priceAfter = ghostSrPricePoolPerAsset128[pricedAssetId];

    satisfy(stampBefore == 0 && stampAfter == computedAt && stampAfter != 0
        && priceAfter == price && priceAfter != 0,
        "an asset's first price can be stored with its stamp");
}

// SR-RC-34: a share price just written can be read back through the validity-checked read.
rule rcSrCheckedSharePriceReadAfterAWriteIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    mathint stampBefore = ghostSrPricePoolPerShareComputedAt64;

    _SpokeRegistry.updatePricePoolPerShare(e, poolId, scId, price, computedAt);

    SpokeRegistry.D18 readBack = _SpokeRegistry.pricePoolPerShare(e, poolId, scId, true);

    satisfy(stampBefore == 0 && readBack == price && price != 0,
        "a checked share price read returns the price just written");
}

// SR-RC-35: an asset price just written can be read back through the validity-checked read.
rule rcSrCheckedAssetPriceReadAfterAWriteIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId, SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);

    uint128 pricedAssetId = assetId;
    mathint stampBefore = ghostSrPricePoolPerAssetComputedAt64[pricedAssetId];

    _SpokeRegistry.updatePricePoolPerAsset(e, poolId, scId, assetId, price, computedAt);

    SpokeRegistry.D18 readBack = _SpokeRegistry.pricePoolPerAsset(e, poolId, scId, assetId, true);

    satisfy(stampBefore == 0 && readBack == price && price != 0,
        "a checked asset price read returns the price just written");
}

// SR-RC-36: a newly added admin can open a pool in the same transaction.
rule rcSrFreshWardOpeningAPoolIsReachable(env e, env eWard, SpokeRegistry.PoolId poolId, address newWard) {

    setupSpokeRegistryValidState(e);
    setupSpokeRegistryValidState(eWard);
    require(eWard.msg.sender == newWard, "SCOPE: the newly granted ward makes the call");

    mathint wardBefore = _SpokeRegistry.wards(newWard);
    mathint stampBefore = ghostSrCreatedAt64;

    _SpokeRegistry.rely(e, newWard);
    _SpokeRegistry.addPool(eWard, poolId);

    mathint wardAfter = _SpokeRegistry.wards(newWard);
    mathint stampAfter = ghostSrCreatedAt64;

    satisfy(wardBefore == 0 && wardAfter == 1 && stampBefore == 0
        && stampAfter == eWard.block.timestamp && stampAfter != 0,
        "a newly granted ward can open a pool right away");
}

// SR-RC-37: an admin can revoke another admin while keeping its own rights.
rule rcSrDenyLeavingTheCallersOwnSeatIsReachable(env e, address subject) {

    setupSpokeRegistryValidState(e);

    mathint subjectWardBefore = _SpokeRegistry.wards(subject);

    _SpokeRegistry.deny(e, subject);

    mathint subjectWardAfter = _SpokeRegistry.wards(subject);
    mathint callerWardAfter = _SpokeRegistry.wards(e.msg.sender);

    satisfy(subject != e.msg.sender && subjectWardBefore == 1 && subjectWardAfter == 0 && callerWardAfter == 1,
        "a ward can remove a peer and remain a ward itself");
}

// SR-RC-38: a pool can go from unregistered to a linked vault in one transaction.
rule rcSrWholePoolBringUpIsReachable(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    address shareToken_, address registrar_, uint16 centrifugeId, address asset, uint256 tokenId,
    address factory, address vault_, bytes payload) {

    setupSpokeRegistryValidState(e);
    require(payload.length == 0, "SCOPE: an empty deployment payload");

    mathint stampBefore = ghostSrCreatedAt64;

    _SpokeRegistry.addPool(e, poolId);
    _SpokeRegistry.addShareClass(e, poolId, scId, shareToken_, registrar_);
    SpokeRegistry.AssetId assetId = _SpokeRegistry.createAssetId(e, centrifugeId, asset, tokenId);
    _SpokeRegistry.registerVault(e, poolId, scId, assetId, asset, tokenId, factory, vault_, payload);
    _SpokeRegistry.linkVault(e, poolId, scId, assetId, vault_);

    address tokenAfter = ghostSrShareToken;
    address vaultAssetAfter = ghostSrVaultAsset[vault_];
    bool linkedAfter = ghostSrVaultIsLinked[vault_];

    satisfy(stampBefore == 0 && tokenAfter == shareToken_ && vaultAssetAfter == asset && linkedAfter,
        "one transaction can take a pool from nothing to a linked vault");
}

// SR-RC-39: one of two bridgers can lose bridger rights while the other keeps them.
rule rcSrRevokingOneOfTwoBridgerSeatsIsReachable(env e, SpokeRegistry.PoolId poolId, address who, address other) {

    setupSpokeRegistryValidState(e);

    bool whoBefore = ghostSrBridger[who];
    bool otherBefore = ghostSrBridger[other];

    _SpokeRegistry.updateBridger(e, poolId, who, false);

    bool whoAfter = ghostSrBridger[who];
    bool otherAfter = ghostSrBridger[other];

    satisfy(who != other && whoBefore && otherBefore && !whoAfter && otherAfter,
        "one bridger can be revoked while another keeps the right");
}

// SR-RC-40: an admin can store a share price a year old, and a later checked read returns it.
rule rcSrYearOldSharePriceIsAcceptedAndServedIsReachable(env e, env eRead, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.D18 price, uint64 computedAt) {

    setupSpokeRegistryValidState(e);
    setupSpokeRegistryValidState(eRead);
    require(eRead.block.timestamp >= e.block.timestamp, "SCOPE: the read comes no earlier than the write");

    _SpokeRegistry.updatePricePoolPerShare(e, poolId, scId, price, computedAt);

    SpokeRegistry.D18 readBack = _SpokeRegistry.pricePoolPerShare(eRead, poolId, scId, true);

    satisfy(e.block.timestamp - computedAt >= 31536000 && readBack == price && price != 0,
        "a year-old share price is accepted and served by the checked read");
}

// SR-RC-41: an admin can move a share class to a new token while its share price and timestamp stay.
rule rcSrTokenSwapKeepsTheStandingSharePriceIsReachable(env e, SpokeRegistry.PoolId poolId,
    SpokeRegistry.ShareClassId scId, SpokeRegistry.D18 price, uint64 computedAt, address shareToken_,
    address registrar_) {

    setupSpokeRegistryValidState(e);

    address incumbent = ghostSrShareToken;

    _SpokeRegistry.updatePricePoolPerShare(e, poolId, scId, price, computedAt);
    _SpokeRegistry.linkToken(e, poolId, scId, shareToken_, registrar_);

    satisfy(incumbent != 0 && shareToken_ != incumbent && ghostSrShareToken == shareToken_
        && price != 0 && ghostSrPricePoolPerShare128 == price
        && ghostSrPricePoolPerShareComputedAt64 == computedAt,
        "a token swap can leave the class's share price and timestamp in place");
}

// SR-RC-42: an admin can post a share price with no asset price, then an asset price older than it.
rule rcSrSharePriceLandsWithoutItsAssetPriceAndAnOlderAssetQuoteFollowsIsReachable(env e,
    SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId, SpokeRegistry.AssetId assetId,
    SpokeRegistry.D18 sharePrice, uint64 shareStamp, SpokeRegistry.D18 assetPrice, uint64 assetStamp) {

    setupSpokeRegistryValidState(e);

    uint128 pricedAssetId = assetId;
    mathint assetStampBefore = ghostSrPricePoolPerAssetComputedAt64[pricedAssetId];

    _SpokeRegistry.updatePricePoolPerShare(e, poolId, scId, sharePrice, shareStamp);

    mathint assetStampMid = ghostSrPricePoolPerAssetComputedAt64[pricedAssetId];

    _SpokeRegistry.updatePricePoolPerAsset(e, poolId, scId, assetId, assetPrice, assetStamp);

    satisfy(assetStampBefore == 0 && assetStampMid == 0 && shareStamp != 0 && assetStamp != 0
        && assetStamp < shareStamp
        && ghostSrPricePoolPerShareComputedAt64 == shareStamp
        && ghostSrPricePoolPerAssetComputedAt64[pricedAssetId] == assetStamp,
        "a share price can stand alone and an older asset price then follow");
}

// SR-RC-43: a pool's policy can spend two grants of the same call on behalf of two different callers.
rule rcSrOneGrantKeyIsSpentUnderTwoDistinctCallersIsReachable(env e, env ePolicy, SpokeRegistry.PoolId poolId,
    address callerA, address callerB, bytes data) {

    setupSpokeRegistryValidState(e);
    setupSpokeRegistryValidState(ePolicy);
    require(data.length == 0, "SCOPE: an empty authorization payload");

    bytes32 id = _SpokeRegistry.authId(e, poolId, data);
    mathint countBefore = ghostSrAuthorizations256[id];

    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.authorize(e, poolId, data);
    _SpokeRegistry.consumeAuthorization(ePolicy, poolId, callerA, data);

    mathint countAfterA = ghostSrAuthorizations256[id];

    _SpokeRegistry.consumeAuthorization(ePolicy, poolId, callerB, data);

    mathint countAfterB = ghostSrAuthorizations256[id];

    satisfy(callerA != callerB && countBefore == 0 && countAfterA == 1 && countAfterB == 0,
        "grants of one call can be spent for two different callers");
}

// SR-RC-46: an admin can link two vaults for the same pool, share class and asset.
rule rcSrTwoVaultsLinkedForOneAssetIsReachable(env e, SpokeRegistry.PoolId poolId, SpokeRegistry.ShareClassId scId,
    SpokeRegistry.AssetId assetId, address v1, address v2) {

    setupSpokeRegistryValidState(e);

    bool linked1Before = ghostSrVaultIsLinked[v1];
    bool linked2Before = ghostSrVaultIsLinked[v2];

    _SpokeRegistry.linkVault(e, poolId, scId, assetId, v1);
    _SpokeRegistry.linkVault(e, poolId, scId, assetId, v2);

    satisfy(v1 != v2 && !linked1Before && !linked2Before && ghostSrVaultIsLinked[v1] && ghostSrVaultIsLinked[v2]
        && ghostSrVaultAssetId128[v1] == assetId && ghostSrVaultAssetId128[v2] == assetId,
        "two vaults serve one pool, share class and asset side by side");
}
