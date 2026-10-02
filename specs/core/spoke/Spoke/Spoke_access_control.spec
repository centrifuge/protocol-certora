import "setup/Spoke_solo.spec";

// SP-AC-01: only an admin can grant or revoke admin rights on the spoke.
rule acSpWardListMovesOnlyForAWard(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    mathint callerWardBefore = _Spoke.wards[e.msg.sender];
    mathint wardBefore = _Spoke.wards[who];

    f(e, args);

    mathint wardAfter = _Spoke.wards[who];

    assert(wardAfter != wardBefore => callerWardBefore == 1,
        "a non-ward cannot change anyone's ward status on the spoke");
}

// SP-AC-02: only an admin can change the gateway the spoke sends messages through.
rule acSpGatewayIsRepointedOnlyByAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    mathint callerWardBefore = _Spoke.wards[e.msg.sender];
    address gatewayBefore = _Spoke.gateway;

    f(e, args);

    address gatewayAfter = _Spoke.gateway;

    assert(gatewayAfter != gatewayBefore => callerWardBefore == 1, "only a ward can repoint the gateway");
}

// SP-AC-03: only an admin can change the contract that sends the spoke's messages.
rule acSpMessageSenderIsRepointedOnlyByAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    mathint callerWardBefore = _Spoke.wards[e.msg.sender];
    address messageSenderBefore = _Spoke.sender;

    f(e, args);

    address messageSenderAfter = _Spoke.sender;

    assert(messageSenderAfter != messageSenderBefore => callerWardBefore == 1,
        "only a ward can repoint the message sender");
}

// SP-AC-04: only a pool manager can queue asset changes for the hub through the spoke, even in a batch.
rule acSpQueuedAssetDeltasComeOnlyFromAManager(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSoloAnyTransient(e);

    bool managerBefore = ghostSrManager[spResolvedSenderCVL(e)];
    mathint queuedBefore = ghostSqFaceQueueAssetsCount;

    f(e, args);

    mathint queuedAfter = ghostSqFaceQueueAssetsCount;

    assert(queuedAfter != queuedBefore => managerBefore, "a non-manager never queues an asset change for the hub");
}

// SP-AC-05: only a pool manager can queue share changes for the hub through the spoke, even in a batch.
rule acSpQueuedShareDeltasComeOnlyFromAManager(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSoloAnyTransient(e);

    bool managerBefore = ghostSrManager[spResolvedSenderCVL(e)];
    mathint queuedBefore = ghostSqFaceQueueSharesCount;

    f(e, args);

    mathint queuedAfter = ghostSqFaceQueueSharesCount;

    assert(queuedAfter != queuedBefore => managerBefore, "a non-manager never queues a share change for the hub");
}

// SP-AC-06: through the spoke, only a pool manager can change escrow balances or reservations, even in a batch.
rule acSpEscrowCustodyMovesOnlyForAManager(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSoloAnyTransient(e);

    bool managerBefore = ghostSrManager[spResolvedSenderCVL(e)];
    mathint escrowMovesBefore = ghostPeFaceMoveCount;

    f(e, args);

    mathint escrowMovesAfter = ghostPeFaceMoveCount;

    assert(escrowMovesAfter != escrowMovesBefore => managerBefore,
        "only a pool manager moves the pool escrow's balances");
}

// SP-AC-07: only a pool manager can submit queued asset or share updates to the hub, even in a batch.
rule acSpQueueSubmissionsLeaveOnlyForAManager(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSoloAnyTransient(e);

    bool managerBefore = ghostSrManager[spResolvedSenderCVL(e)];
    mathint sendsBefore = ghostMsSendCount;

    f(e, args);

    mathint sendsAfter = ghostMsSendCount;
    mathint lastKindAfter = ghostMsLastKind;

    assert(sendsAfter != sendsBefore
        && (lastKindAfter == MS_UPDATE_ASSETS() || lastKindAfter == MS_UPDATE_SHARES())
        => managerBefore,
        "asset or share updates reach the hub only from a pool manager");
}

// SP-AC-08: only a pool manager can issue new shares through the spoke.
rule acSpShareSupplyGrowsThroughTheSpokeOnlyForAManager(env e, method f, calldataarg args, address token)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    bool managerBefore = ghostSrManager[e.msg.sender];
    mathint supplyBefore = ghostERC20TotalSupply256[token];

    f(e, args);

    mathint supplyAfter = ghostERC20TotalSupply256[token];

    assert(supplyAfter > supplyBefore => managerBefore, "only a pool manager can grow any token's supply");
}

// SP-AC-09: only the holder or a pool manager can reduce a balance not approved to the spoke.
rule acSpUnauthorizedCannotReduceAHoldersBalance(env e, method f, calldataarg args, address token,
    address holder)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);
    require(holder != _Spoke, "SCOPE: user balances, not the spoke's own float");

    bool managerBefore = ghostSrManager[e.msg.sender];
    mathint allowanceBefore = ghostERC20Allowances256[token][holder][_Spoke];
    mathint balanceBefore = ghostERC20Balances128[token][holder];

    f(e, args);

    mathint balanceAfter = ghostERC20Balances128[token][holder];

    assert(e.msg.sender != holder && allowanceBefore == 0 && !managerBefore
        => balanceAfter >= balanceBefore,
        "a non-manager cannot debit others who gave the spoke no approval");
}

// SP-AC-10: only a listed bridger or an admin can start a cross-chain share transfer.
rule acSpBridgeStartsOnlyForABridgerOrAWard(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    bool bridgerBefore = ghostSrBridger[e.msg.sender];
    mathint callerWardBefore = _Spoke.wards[e.msg.sender];
    mathint bridgeSendsBefore = ghostMsInitiateTransferCount;

    f(e, args);

    mathint bridgeSendsAfter = ghostMsInitiateTransferCount;

    assert(bridgeSendsAfter != bridgeSendsBefore => (bridgerBefore || callerWardBefore == 1),
        "no bridge transfer starts unless a bridger or a ward calls");
}

// SP-AC-11: only the pool's request manager can send an investor request to the hub.
rule acSpInvestorRequestsLeaveOnlyForTheRequestManager(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    address requestManagerBefore = ghostSrRequestManager;
    mathint sendsBefore = ghostMsSendCount;

    f(e, args);

    mathint sendsAfter = ghostMsSendCount;
    mathint lastKindAfter = ghostMsLastKind;

    assert(sendsAfter != sendsBefore && lastKindAfter == MS_REQUEST()
        => e.msg.sender == requestManagerBefore,
        "a request message leaves only from the request manager");
}

// SP-AC-12: an approval to the spoke is spent only by its holder, an admin, or a manager's forced transfer.
rule acSpApprovalToTheSpokeIsSpentOnlyByItsOwnerAWardOrAManagersForcedTransfer(env e, method f,
    calldataarg args, address token, address holder)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);
    require(holder != _Spoke, "SCOPE: approvals users grant, not the spoke's own");

    mathint callerWardBefore = _Spoke.wards[e.msg.sender];
    bool managerBefore = ghostSrManager[e.msg.sender];
    mathint allowanceBefore = ghostERC20Allowances256[token][holder][_Spoke];

    f(e, args);

    mathint allowanceAfter = ghostERC20Allowances256[token][holder][_Spoke];
    bool forcedTransfer = managerBefore && f.selector == sig:_Spoke.transferSharesFrom(SpokeHarness.PoolId,
        SpokeHarness.ShareClassId,address,address,address,uint256).selector;

    assert(allowanceAfter < allowanceBefore => (e.msg.sender == holder || callerWardBefore == 1 || forcedTransfer),
        "only its holder, a ward or a forced transfer spends a spoke approval");
}

// SP-AC-13: registering an asset changes no one's admin, manager or bridger rights and no pool role.
rule acSpRegisterAssetSeatsNobodyInAnyPool(env e, uint16 centrifugeId, address asset, uint256 tokenId,
    address refund, address who) {

    setupSpokeSolo(e);

    mathint wardBefore = _Spoke.wards[who];
    bool managerBefore = ghostSrManager[who];
    bool bridgerBefore = ghostSrBridger[who];
    address requestManagerBefore = ghostSrRequestManager;
    address policyBefore = ghostSrPolicy;
    address registrarBefore = ghostSrRegistrar;
    mathint authCountBefore = ghostSrFaceAuthCount;

    _Spoke.registerAsset(e, centrifugeId, asset, tokenId, refund);

    mathint wardAfter = _Spoke.wards[who];
    bool managerAfter = ghostSrManager[who];
    bool bridgerAfter = ghostSrBridger[who];

    assert(wardAfter == wardBefore && managerAfter == managerBefore && bridgerAfter == bridgerBefore
        && ghostSrRequestManager == requestManagerBefore && ghostSrPolicy == policyBefore
        && ghostSrRegistrar == registrarBefore && ghostSrFaceAuthCount == authCountBefore,
        "an asset registration leaves every right and pool role as it was");
}

// SP-AC-14: the spoke changes a token's supply only through the share class's registrar, never directly.
rule acSpShareSupplyMovesOnlyThroughTheClassRegistrar(env e, method f, calldataarg args, address token)
    filtered { f -> !EXCLUDED_FUNCTION_SP(f) } {

    setupSpokeSolo(e);

    address registrarBefore = ghostSrRegistrar;
    mathint supplyBefore = ghostERC20TotalSupply256[token];
    mathint directCallsBefore = ghostSpDirectSupplyCalls;
    mathint registrarCallsBefore = ghostRegistrarSupplyCalls;

    f(e, args);

    mathint supplyAfter = ghostERC20TotalSupply256[token];

    assert(ghostSpDirectSupplyCalls == directCallsBefore
        && (supplyAfter != supplyBefore
            => ghostRegistrarSupplyCalls != registrarCallsBefore && ghostRegistrarLastSupplyCallee == registrarBefore),
        "supply moves only by a registrar mint or burn, never a direct one");
}
