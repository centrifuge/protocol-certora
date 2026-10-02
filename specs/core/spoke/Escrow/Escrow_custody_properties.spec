import "setup/Escrow_custody.spec";

// --- high_level ---

// PE-HL-07: a forced transfer sends exactly the named amount of the token to the named receiver, once.
rule hlPeAuthTransferToMovesExactlyTheAmount(env e, address asset, uint256 tokenId, address receiver,
    uint256 amount) {

    setupPoolEscrowCustody(e);

    mathint movesBefore = ghostPeCustodyMoveCount;
    mathint custodyBefore = PE_CUSTODY_BAL(asset, tokenId, _PoolEscrow);
    mathint receiverBefore = PE_CUSTODY_BAL(asset, tokenId, receiver);

    _PoolEscrow.authTransferTo(e, asset, tokenId, receiver, amount);

    mathint movesAfter = ghostPeCustodyMoveCount;
    mathint custodyAfter = PE_CUSTODY_BAL(asset, tokenId, _PoolEscrow);
    mathint receiverAfter = PE_CUSTODY_BAL(asset, tokenId, receiver);

    assert(movesAfter == movesBefore + 1
        && ghostPeCustodyLastToken == asset && ghostPeCustodyLastTo == receiver
        && ghostPeCustodyLastTokenId == tokenId && ghostPeCustodyLastAmount == amount,
        "one transfer of the named token, id and amount reaches the receiver");
    assert(receiver != _PoolEscrow
        => custodyAfter == custodyBefore - amount && receiverAfter == receiverBefore + amount,
        "an outside receiver gains and the escrow loses exactly the amount");
}

// PE-HL-08: a forced transfer or token recovery writes no holding, reservation or ward, under any key.
rule hlPeCustodyMoversWriteNoBook(env e, uint8 mode, address asset, uint256 tokenId, address receiver,
    uint256 amount, Escrow.ShareClassId sc, address a, uint256 t, address r, bytes32 n, address who,
    address token, uint256 id, address acct) {

    setupPoolEscrowCustody(e);

    uint128 totalBefore = _PoolEscrow.holding[sc][a][t].total;
    uint128 reservedBefore = _PoolEscrow.holding[sc][a][t].reserved;
    uint128 bucketBefore = _PoolEscrow.reservedBy[sc][r][n][a][t];
    uint256 wardBefore = _PoolEscrow.wards[who];
    mathint balance20Before = ghostPeTok20Bal[token][acct];
    mathint balance6909Before = ghostPeTok6909Bal[token][id][acct];

    if (mode == 0) {
        _PoolEscrow.authTransferTo(e, asset, tokenId, receiver, amount);
    } else if (mode == 1) {
        _PoolEscrow.recoverTokens(e, asset, receiver, amount);
    } else {
        _PoolEscrow.recoverTokens(e, asset, tokenId, receiver, amount);
    }

    assert(_PoolEscrow.holding[sc][a][t].total == totalBefore
            && _PoolEscrow.holding[sc][a][t].reserved == reservedBefore
            && _PoolEscrow.reservedBy[sc][r][n][a][t] == bucketBefore && _PoolEscrow.wards[who] == wardBefore,
        "no holding, reservation or ward moves");
    assert((acct != _PoolEscrow && acct != receiver) => (ghostPeTok20Bal[token][acct] == balance20Before
            && ghostPeTok6909Bal[token][id][acct] == balance6909Before),
        "only the escrow's and the receiver's balances move");
}

// --- reverts ---

// PE-RV-13: a forced transfer of more than the escrow holds fails, even on a token that would allow it.
rule rvPeAuthTransferToRefusesAShortCustody(env e, address asset, uint256 tokenId, address receiver,
    uint256 amount) {

    setupPoolEscrowCustody(e);

    mathint custodyBefore = PE_CUSTODY_BAL(asset, tokenId, _PoolEscrow);
    bool custodyIsShort = custodyBefore < amount;

    _PoolEscrow.authTransferTo@withrevert(e, asset, tokenId, receiver, amount);
    bool reverted = lastReverted;

    assert(custodyIsShort => reverted, "a transfer beyond the escrow's balance fails, ERC20 or ERC6909");
}

// --- reachability ---

// PE-RC-22: an admin can force tokens out of a fully backed holding, its recorded total left as it was.
rule rcPeAuthTransferToMovesCustodyWithoutTheLedger(env e, Escrow.ShareClassId scId, address asset,
    address receiver, uint256 amount) {

    setupPoolEscrowCustody(e);

    uint128 totalBefore;
    uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(scId, asset, 0);
    mathint custodyBefore = ghostPeTok20Bal[asset][_PoolEscrow];
    mathint movesBefore = ghostPeCustodyMoveCount;

    _PoolEscrow.authTransferTo(e, asset, 0, receiver, amount);

    uint128 totalAfter;
    uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(scId, asset, 0);
    mathint custodyAfter = ghostPeTok20Bal[asset][_PoolEscrow];
    mathint movesAfter = ghostPeCustodyMoveCount;

    satisfy(amount > 0 && receiver != _PoolEscrow && totalBefore == custodyBefore
        && totalAfter == totalBefore && movesAfter == movesBefore + 1
        && ghostPeCustodyLastToken == asset && ghostPeCustodyLastTo == receiver
        && ghostPeCustodyLastAmount == amount && custodyAfter == custodyBefore - amount,
        "a forced transfer can leave the recorded total above the balance");
}

// PE-RC-23: an admin can recover tokens from a fully backed holding, its recorded total left as it was.
rule rcPeRecoverTokensMovesCustodyWithoutTheLedger(env e, Escrow.ShareClassId scId, address asset,
    address receiver, uint256 amount) {

    setupPoolEscrowCustody(e);

    uint128 totalBefore;
    uint128 reservedBefore;
    totalBefore, reservedBefore = _PoolEscrow.holding(scId, asset, 0);
    mathint custodyBefore = ghostPeTok20Bal[asset][_PoolEscrow];
    mathint movesBefore = ghostPeCustodyMoveCount;

    _PoolEscrow.recoverTokens(e, asset, receiver, amount);

    uint128 totalAfter;
    uint128 reservedAfter;
    totalAfter, reservedAfter = _PoolEscrow.holding(scId, asset, 0);
    mathint custodyAfter = ghostPeTok20Bal[asset][_PoolEscrow];
    mathint movesAfter = ghostPeCustodyMoveCount;

    satisfy(asset != PE_ETH_ADDRESS() && amount > 0 && receiver != _PoolEscrow
        && totalBefore == custodyBefore
        && totalAfter == totalBefore && movesAfter == movesBefore + 1
        && ghostPeCustodyLastToken == asset && ghostPeCustodyLastTo == receiver
        && ghostPeCustodyLastAmount == amount && custodyAfter == custodyBefore - amount,
        "a token recovery can leave the recorded total above the balance");
}
