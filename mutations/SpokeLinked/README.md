# Mutations for `SpokeLinked` (`src/core/spoke/Spoke.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/spoke/Escrow.sol`, `src/core/spoke/SnapshotQueue.sol`.

| # | What we test |
|---|---|
| [5500](#spokelinked-5500) | A payout leaves the escrow without ever being taken off the custody total, so the pool's books keep counting money that has already left.<br>Caught by: [`hlSpDepositThenWithdrawRestoresCustody`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L4) · [`hlSpWithdrawReservedPaysOutTheRequestedAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L112) |
| [5501](#spokelinked-5501) | A withdrawal is queued for the hub as a deposit, so money leaving the pool is reported as arriving.<br>Caught by: [`hlSpDepositThenWithdrawRestoresTheQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L21) |
| [5502](#spokelinked-5502) | Taking a hold also takes the funds off the custody total, so an earmark shrinks what the escrow says it keeps.<br>Caught by: [`hlSpReserveThenUnreserveLeavesCustodyUntouched`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L39) · [`hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L634) |
| [5503](#spokelinked-5503) | Releasing a hold never lowers the row's aggregate hold, so a spent or cancelled earmark keeps blocking the pool from spending its own money.<br>Caught by: [`hlSpReserveThenUnreserveRestoresTheAggregateHold`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L57) · [`hlSpWithdrawReservedConsumesTheHold`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L129) |
| [5504](#spokelinked-5504) | Releasing a hold never lowers the reserver's own bucket, so it keeps an earmark that was already freed.<br>Caught by: [`hlSpReserveThenUnreserveRestoresTheReserversBucket`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L75) |
| [5505](#spokelinked-5505) | Releasing a hold is queued for the hub as a withdrawal, so a hold and its release report two departures.<br>Caught by: [`hlSpReserveThenUnreserveRestoresTheQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L93) |
| [5506](#spokelinked-5506) | Paying out reserved funds queues the departure for the hub again, so a decrease already reported at reserve counts twice.<br>Caught by: [`hlSpWithdrawReservedLeavesTheQueueUntouched`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L147) |
| [5507](#spokelinked-5507) | A revoke pulls the shares from the pool escrow instead of the caller, so a manager burns investors' shares for free.<br>Caught by: [`hlSpRevokePullsSharesFromTheCaller`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L175) |
| [5508](#spokelinked-5508) | A revoke collects the shares but never burns them, so they sit on the spoke still counted in the supply.<br>Caught by: [`hlSpRevokeBurnsThePulledShares`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L191) · [`hlSpRevokeParksNoSharesOnTheSpoke`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L207) |
| [5509](#spokelinked-5509) | A revoke is queued for the hub as an issuance, so burning shares is reported as creating them.<br>Caught by: [`hlSpRevokeQueuesTheBurnAsADecrease`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L223) |
| [5510](#spokelinked-5510) | Registering an asset sends its announcement to the hub twice, so the hub receives a duplicate registration.<br>Caught by: [`hlSpRegisterAssetSendsOneRegistrationAnnouncement`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L238) |
| [5511](#spokelinked-5511) | A first registration discards the freshly created asset id, so the hub is told the null id, not the stored one.<br>Caught by: [`hlSpRegisterAssetAnnouncesTheStoredId`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L255) |
| [5512](#spokelinked-5512) | An asset flush is sent to the hub as a share update, so the flushed asset's flow lands on share supply.<br>Caught by: [`hlSpAssetFlushAnnouncesAnUpdateForTheFlushedRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L269) |
| [5513](#spokelinked-5513) | An asset flush reports deposits plus withdrawals instead of their net, so the hub moves the holding by the gross traffic.<br>Caught by: [`hlSpAssetFlushReportsTheRowsNetSize`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L285) |
| [5514](#spokelinked-5514) | An asset row whose deposits and withdrawals cancel is reported as an increase, so the hub reads a zero flow as arriving money.<br>Caught by: [`hlSpAssetFlushReportsTheRowsNetDirection`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L304) |
| [5515](#spokelinked-5515) | An asset flush is sent under the next report's sequence number, so the hub receives reports numbered out of sequence.<br>Caught by: [`hlSpAssetFlushReportsTheStoredSequenceNumber`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L322) |
| [5516](#spokelinked-5516) | An asset flush clears only the deposit side of the row, so the reported withdrawals are reported again next time.<br>Caught by: [`hlSpAssetFlushEmptiesTheRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L337) |
| [5517](#spokelinked-5517) | A share flush is sent to the hub as an asset update, so a share supply change lands on an asset holding.<br>Caught by: [`hlSpShareFlushAnnouncesAShareUpdate`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L352) |
| [5518](#spokelinked-5518) | A share flush clears the queued net before building the report, so the hub is told zero and the movement is lost.<br>Caught by: [`hlSpShareFlushReportsTheQueuedNetSize`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L365) |
| [5519](#spokelinked-5519) | A share flush reports the queued direction inverted, so shares the pool issued are applied at the hub as shares revoked.<br>Caught by: [`hlSpShareFlushReportsTheQueuedNetDirection`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L380) |
| [5520](#spokelinked-5520) | A share flush is sent under the next report's sequence number, so the hub receives reports numbered out of sequence.<br>Caught by: [`hlSpShareFlushReportsTheStoredSequenceNumber`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L395) |
| [5521](#spokelinked-5521) | A share flush reports the queued net but leaves it standing, so the same share movement is reported again next time.<br>Caught by: [`hlSpShareFlushClearsTheQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L410) |
| [5522](#spokelinked-5522) | a withdrawal may name no receiver but the escrow itself, so custody can never leave the pool's own escrow.<br>Caught by: [`rcSpWithdrawToAnotherAddressIsReachable`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_reachability.spec#L4) |
| [8931](#spokelinked-8931) | A noted deposit is queued for the hub as a withdrawal, so money arriving in the pool is reported as leaving.<br>Caught by: [`hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L634) |
| [9071](#spokelinked-9071) | A deposit is booked on the token id zero row instead of its own, so an ERC6909 deposit credits another id's custody.<br>Caught by: [`hlSpEscrowEntryMovesItsOwnRowByExactlyTheAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/Spoke_LinkedSpokeCore_rows_properties.spec#L6) · [`hlSpEscrowEntryTouchesOnlyItsOwnRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/Spoke_LinkedSpokeCore_rows_properties.spec#L43) |
| [9072](#spokelinked-9072) | Placing a hold calls the escrow's release instead, so the reserver's bucket and the total hold shrink rather than grow.<br>Caught by: [`hlSpReserveRaisesBucketAndHoldByExactlyTheAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L423) · [`hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L634) |
| [9073](#spokelinked-9073) | Releasing a hold calls the escrow's reserve instead, so the reserver's bucket and the total hold grow rather than shrink.<br>Caught by: [`hlSpUnreserveLowersBucketAndHoldByExactlyTheAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L446) |
| [9321](#spokelinked-9321) | A withdrawal is booked on the token id zero row instead of its own, so one ERC6909 id drains another's custody.<br>Caught by: [`hlSpEscrowEntryTouchesOnlyItsOwnRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/Spoke_LinkedSpokeCore_rows_properties.spec#L43) |
| [9324](#spokelinked-9324) | A zero asset entry now counts an empty row as pending, so the next share report to the hub is not marked a snapshot.<br>Caught by: [`hlSpZeroAmountEntryLeavesTheQueueUntouched`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L469) |
| [9325](#spokelinked-9325) | A share report to the hub spends no sequence number, so the next report reuses it and the hub cannot order them.<br>Caught by: [`hlSpFlushSpendsExactlyOneNonce`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L514) |
| [9326](#spokelinked-9326) | Registering an asset makes the caller a ward of the spoke, so anyone registering a token becomes its admin.<br>Caught by: [`hlSpRegisterAssetGrantsNoSeat`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L533) |
| [9327](#spokelinked-9327) | registering an already known asset now reverts, so it cannot be announced to another network or refreshed at the hub.<br>Caught by: [`rcSpReRegistrationCanAnnounceNewDecimalsUnderTheSameId`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_reachability.spec#L25) |
| [9328](#spokelinked-9328) | a share payout from the escrow moves no tokens, so a manager's share withdrawal pays the receiver nothing.<br>Caught by: [`rcSpSharePayoutDrainsABookedShareTokenRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_reachability.spec#L42) |
| [9329](#spokelinked-9329) | issuing shares also restamps the share price as fresh, so a stale price passes as current without a hub update.<br>Caught by: [`vtSpNoSpokeEntryMovesAPrice`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L6) |
| [9610](#spokelinked-9610) | a withdrawal resolves the next pool id's escrow instead of its own, so one pool's manager spends another pool's custody.<br>Caught by: [`hlSpEscrowResolvedEntryLeavesAnotherPoolsEscrowAlone`](../../specs/core/spoke/Spoke_LinkedSpokeCore/Spoke_LinkedSpokeCore_multi_pool_properties.spec#L6) |

## SpokeLinked #5500

A payout leaves the escrow without ever being taken off the custody total, so the pool's books keep counting money that has already left.

- **Mutant:** [`5500.sol`](5500.sol)
- **Caught by:** [`hlSpDepositThenWithdrawRestoresCustody`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L4) · [`hlSpWithdrawReservedPaysOutTheRequestedAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L112)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5500`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpDepositThenWithdrawRestoresCustody hlSpWithdrawReservedPaysOutTheRequestedAmount`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -47,7 +47,7 @@
         uint128 balance = holding_.total - holding_.reserved;
         require(balance >= value, InsufficientBalance(asset, tokenId, value, balance));
 
-        holding_.total -= value;
+        // MUTATION: the payout is never taken off the custody total
         emit Withdraw(asset, tokenId, poolId, scId, receiver, value);
     }
 
```

## SpokeLinked #5501

A withdrawal is queued for the hub as a deposit, so money leaving the pool is reported as arriving.

- **Mutant:** [`5501.sol`](5501.sol)
- **Caught by:** [`hlSpDepositThenWithdrawRestoresTheQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5501`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpDepositThenWithdrawRestoresTheQueuedNet`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -158,7 +158,7 @@
         IEscrow escrow_ = escrow(poolId);
 
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
-        _queueAssets(poolId, scId, asset, tokenId, amount, false);
+        _queueAssets(poolId, scId, asset, tokenId, amount, true); // MUTATION: the payout is queued as a deposit
         escrow_.authTransferTo(asset, tokenId, receiver, amount);
 
         emit Withdraw(poolId, scId, asset, tokenId, receiver, amount);
```

## SpokeLinked #5502

Taking a hold also takes the funds off the custody total, so an earmark shrinks what the escrow says it keeps.

- **Mutant:** [`5502.sol`](5502.sol)
- **Caught by:** [`hlSpReserveThenUnreserveLeavesCustodyUntouched`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L39) · [`hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L634)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5502`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpReserveThenUnreserveLeavesCustodyUntouched hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -61,6 +61,7 @@
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
         holding_.reserved += value;
+        holding_.total -= value; // MUTATION: a hold also takes the funds out of custody
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## SpokeLinked #5503

Releasing a hold never lowers the row's aggregate hold, so a spent or cancelled earmark keeps blocking the pool from spending its own money.

- **Mutant:** [`5503.sol`](5503.sol)
- **Caught by:** [`hlSpReserveThenUnreserveRestoresTheAggregateHold`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L57) · [`hlSpWithdrawReservedConsumesTheHold`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5503`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpReserveThenUnreserveRestoresTheAggregateHold hlSpWithdrawReservedConsumesTheHold`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -77,7 +77,7 @@
 
         uint128 newReservedAmount = currentReserved - value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved -= value;
+        // MUTATION: the release never lowers the row's aggregate hold
 
         emit DecreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## SpokeLinked #5504

Releasing a hold never lowers the reserver's own bucket, so it keeps an earmark that was already freed.

- **Mutant:** [`5504.sol`](5504.sol)
- **Caught by:** [`hlSpReserveThenUnreserveRestoresTheReserversBucket`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L75)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5504`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpReserveThenUnreserveRestoresTheReserversBucket`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -76,7 +76,7 @@
         require(currentReserved >= value, InsufficientReserve());
 
         uint128 newReservedAmount = currentReserved - value;
-        reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
+        // MUTATION: dropped the per reserver bucket release
         holding_.reserved -= value;
 
         emit DecreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
```

## SpokeLinked #5505

Releasing a hold is queued for the hub as a withdrawal, so a hold and its release report two departures.

- **Mutant:** [`5505.sol`](5505.sol)
- **Caught by:** [`hlSpReserveThenUnreserveRestoresTheQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L93)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5505`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpReserveThenUnreserveRestoresTheQueuedNet`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -209,7 +209,7 @@
         bytes32 reason
     ) external payable enforced(poolId) {
         escrow(poolId).unreserve(scId, asset, tokenId, amount, reserver, reason);
-        _queueAssets(poolId, scId, asset, tokenId, amount, true);
+        _queueAssets(poolId, scId, asset, tokenId, amount, false); // MUTATION: the release is queued as a withdrawal
     }
 
     /// @inheritdoc ISpoke
```

## SpokeLinked #5506

Paying out reserved funds queues the departure for the hub again, so a decrease already reported at reserve counts twice.

- **Mutant:** [`5506.sol`](5506.sol)
- **Caught by:** [`hlSpWithdrawReservedLeavesTheQueueUntouched`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L147)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5506`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpWithdrawReservedLeavesTheQueueUntouched`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -179,6 +179,7 @@
 
         escrow_.unreserve(scId, asset, tokenId, amount, reserver, reason);
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
+        _queueAssets(poolId, scId, asset, tokenId, amount, false); // MUTATION: the reserved payout is reported again
         escrow_.authTransferTo(asset, tokenId, receiver, amount);
 
         emit Withdraw(poolId, scId, asset, tokenId, receiver, amount);
```

## SpokeLinked #5507

A revoke pulls the shares from the pool escrow instead of the caller, so a manager burns investors' shares for free.

- **Mutant:** [`5507.sol`](5507.sol)
- **Caught by:** [`hlSpRevokePullsSharesFromTheCaller`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L175)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5507`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpRevokePullsSharesFromTheCaller`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -245,7 +245,7 @@
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
 
         snapshotQueue.queueShares(poolId, scId, shares, false);
-        SafeTransferLib.safeTransferFrom(address(token), msgSender(), address(this), shares);
+        SafeTransferLib.safeTransferFrom(address(token), address(escrow(poolId)), address(this), shares); // MUTATION: the shares come from the pool escrow
         SafeTransferLib.safeApprove(address(token), address(registrar), shares);
         registrar.burn(address(token), address(this), shares);
 
```

## SpokeLinked #5508

A revoke collects the shares but never burns them, so they sit on the spoke still counted in the supply.

- **Mutant:** [`5508.sol`](5508.sol)
- **Caught by:** [`hlSpRevokeBurnsThePulledShares`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L191) · [`hlSpRevokeParksNoSharesOnTheSpoke`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L207)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5508`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpRevokeBurnsThePulledShares hlSpRevokeParksNoSharesOnTheSpoke`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -247,7 +247,7 @@
         snapshotQueue.queueShares(poolId, scId, shares, false);
         SafeTransferLib.safeTransferFrom(address(token), msgSender(), address(this), shares);
         SafeTransferLib.safeApprove(address(token), address(registrar), shares);
-        registrar.burn(address(token), address(this), shares);
+        // MUTATION: the pulled shares are never burned
 
         emit Revoke(poolId, scId, msgSender(), msgSender(), shares);
     }
```

## SpokeLinked #5509

A revoke is queued for the hub as an issuance, so burning shares is reported as creating them.

- **Mutant:** [`5509.sol`](5509.sol)
- **Caught by:** [`hlSpRevokeQueuesTheBurnAsADecrease`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L223)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5509`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpRevokeQueuesTheBurnAsADecrease`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -244,7 +244,7 @@
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
 
-        snapshotQueue.queueShares(poolId, scId, shares, false);
+        snapshotQueue.queueShares(poolId, scId, shares, true); // MUTATION: the burn is queued as an issuance
         SafeTransferLib.safeTransferFrom(address(token), msgSender(), address(this), shares);
         SafeTransferLib.safeApprove(address(token), address(registrar), shares);
         registrar.burn(address(token), address(this), shares);
```

## SpokeLinked #5510

Registering an asset sends its announcement to the hub twice, so the hub receives a duplicate registration.

- **Mutant:** [`5510.sol`](5510.sol)
- **Caught by:** [`hlSpRegisterAssetSendsOneRegistrationAnnouncement`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L238)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5510`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpRegisterAssetSendsOneRegistrationAnnouncement`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -110,6 +110,7 @@
 
         emit RegisterAsset(centrifugeId, assetId, asset, tokenId, name, symbol, decimals, isInitialization);
         sender.sendRegisterAsset{value: msgValue()}(centrifugeId, assetId, decimals, refund);
+        sender.sendRegisterAsset(centrifugeId, assetId, decimals, refund); // MUTATION: the registration is announced a second time
     }
 
     //----------------------------------------------------------------------------------------------
```

## SpokeLinked #5511

A first registration discards the freshly created asset id, so the hub is told the null id, not the stored one.

- **Mutant:** [`5511.sol`](5511.sol)
- **Caught by:** [`hlSpRegisterAssetAnnouncesTheStoredId`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L255)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5511`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpRegisterAssetAnnouncesTheStoredId`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -105,7 +105,7 @@
         assetId = spokeRegistry.assetToId(asset, tokenId);
         bool isInitialization = assetId.isNull();
         if (isInitialization) {
-            assetId = spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, tokenId);
+            spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, tokenId); // MUTATION: the freshly created id is discarded
         }
 
         emit RegisterAsset(centrifugeId, assetId, asset, tokenId, name, symbol, decimals, isInitialization);
```

## SpokeLinked #5512

An asset flush is sent to the hub as a share update, so the flushed asset's flow lands on share supply.

- **Mutant:** [`5512.sol`](5512.sol)
- **Caught by:** [`hlSpAssetFlushAnnouncesAnUpdateForTheFlushedRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L269)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5512`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpAssetFlushAnnouncesAnUpdateForTheFlushedRow`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -221,7 +221,7 @@
         address refund
     ) external payable enforced(poolId) {
         ISpokeMessageSender.UpdateData memory data = snapshotQueue.flushAssets(poolId, scId, assetId);
-        sender.sendUpdateAssets{value: msgValue()}(poolId, scId, assetId, data, extraGasLimit, refund);
+        sender.sendUpdateShares{value: msgValue()}(poolId, scId, data, extraGasLimit, refund); // MUTATION: the asset flush is announced as a share update
     }
 
     //----------------------------------------------------------------------------------------------
```

## SpokeLinked #5513

An asset flush reports deposits plus withdrawals instead of their net, so the hub moves the holding by the gross traffic.

- **Mutant:** [`5513.sol`](5513.sol)
- **Caught by:** [`hlSpAssetFlushReportsTheRowsNetSize`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L285)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5513`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpAssetFlushReportsTheRowsNetSize`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -69,9 +69,7 @@
         uint32 assetCounter = (assetQueue.deposits != 0 || assetQueue.withdrawals != 0) ? 1 : 0;
 
         data = ISpokeMessageSender.UpdateData({
-            netAmount: (assetQueue.deposits >= assetQueue.withdrawals)
-                ? assetQueue.deposits - assetQueue.withdrawals
-                : assetQueue.withdrawals - assetQueue.deposits,
+            netAmount: assetQueue.deposits + assetQueue.withdrawals, // MUTATION: the row's gross traffic is reported instead of its net
             isIncrease: assetQueue.deposits > assetQueue.withdrawals,
             isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
             nonce: shareQueue.nonce
```

## SpokeLinked #5514

An asset row whose deposits and withdrawals cancel is reported as an increase, so the hub reads a zero flow as arriving money.

- **Mutant:** [`5514.sol`](5514.sol)
- **Caught by:** [`hlSpAssetFlushReportsTheRowsNetDirection`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L304)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5514`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpAssetFlushReportsTheRowsNetDirection`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -72,7 +72,7 @@
             netAmount: (assetQueue.deposits >= assetQueue.withdrawals)
                 ? assetQueue.deposits - assetQueue.withdrawals
                 : assetQueue.withdrawals - assetQueue.deposits,
-            isIncrease: assetQueue.deposits > assetQueue.withdrawals,
+            isIncrease: assetQueue.deposits >= assetQueue.withdrawals, // MUTATION: an exactly cancelled row is reported as an increase
             isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
             nonce: shareQueue.nonce
         });
```

## SpokeLinked #5515

An asset flush is sent under the next report's sequence number, so the hub receives reports numbered out of sequence.

- **Mutant:** [`5515.sol`](5515.sol)
- **Caught by:** [`hlSpAssetFlushReportsTheStoredSequenceNumber`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L322)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5515`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpAssetFlushReportsTheStoredSequenceNumber`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -74,7 +74,7 @@
                 : assetQueue.withdrawals - assetQueue.deposits,
             isIncrease: assetQueue.deposits > assetQueue.withdrawals,
             isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
-            nonce: shareQueue.nonce
+            nonce: shareQueue.nonce + 1 // MUTATION: filed under the number the next flush will use
         });
 
         assetQueue.deposits = 0;
```

## SpokeLinked #5516

An asset flush clears only the deposit side of the row, so the reported withdrawals are reported again next time.

- **Mutant:** [`5516.sol`](5516.sol)
- **Caught by:** [`hlSpAssetFlushEmptiesTheRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L337)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5516`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpAssetFlushEmptiesTheRow`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -78,7 +78,7 @@
         });
 
         assetQueue.deposits = 0;
-        assetQueue.withdrawals = 0;
+        // MUTATION: the withdrawal side survives the flush
         shareQueue.nonce++;
         shareQueue.queuedAssetCounter -= assetCounter;
 
```

## SpokeLinked #5517

A share flush is sent to the hub as an asset update, so a share supply change lands on an asset holding.

- **Mutant:** [`5517.sol`](5517.sol)
- **Caught by:** [`hlSpShareFlushAnnouncesAShareUpdate`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L352)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5517`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpShareFlushAnnouncesAShareUpdate`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -272,7 +272,7 @@
         enforced(poolId)
     {
         ISpokeMessageSender.UpdateData memory data = snapshotQueue.flushShares(poolId, scId);
-        sender.sendUpdateShares{value: msgValue()}(poolId, scId, data, extraGasLimit, refund);
+        sender.sendUpdateAssets{value: msgValue()}(poolId, scId, AssetId.wrap(0), data, extraGasLimit, refund); // MUTATION: the share flush is announced as an asset update
     }
 
     /// @inheritdoc ISpoke
```

## SpokeLinked #5518

A share flush clears the queued net before building the report, so the hub is told zero and the movement is lost.

- **Mutant:** [`5518.sol`](5518.sol)
- **Caught by:** [`hlSpShareFlushReportsTheQueuedNetSize`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L365)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5518`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpShareFlushReportsTheQueuedNetSize`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -93,6 +93,8 @@
     {
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
 
+        shareQueue.delta = 0; // MUTATION: the net is cleared before the report is assembled
+
         data = ISpokeMessageSender.UpdateData({
             netAmount: shareQueue.delta,
             isIncrease: shareQueue.isPositive,
@@ -100,7 +102,6 @@
             nonce: shareQueue.nonce
         });
 
-        shareQueue.delta = 0;
         shareQueue.isPositive = false;
         shareQueue.nonce++;
 
```

## SpokeLinked #5519

A share flush reports the queued direction inverted, so shares the pool issued are applied at the hub as shares revoked.

- **Mutant:** [`5519.sol`](5519.sol)
- **Caught by:** [`hlSpShareFlushReportsTheQueuedNetDirection`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L380)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5519`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpShareFlushReportsTheQueuedNetDirection`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -95,7 +95,7 @@
 
         data = ISpokeMessageSender.UpdateData({
             netAmount: shareQueue.delta,
-            isIncrease: shareQueue.isPositive,
+            isIncrease: !shareQueue.isPositive, // MUTATION: the queued direction is reported inverted
             isSnapshot: shareQueue.queuedAssetCounter == 0,
             nonce: shareQueue.nonce
         });
```

## SpokeLinked #5520

A share flush is sent under the next report's sequence number, so the hub receives reports numbered out of sequence.

- **Mutant:** [`5520.sol`](5520.sol)
- **Caught by:** [`hlSpShareFlushReportsTheStoredSequenceNumber`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L395)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5520`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpShareFlushReportsTheStoredSequenceNumber`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -97,7 +97,7 @@
             netAmount: shareQueue.delta,
             isIncrease: shareQueue.isPositive,
             isSnapshot: shareQueue.queuedAssetCounter == 0,
-            nonce: shareQueue.nonce
+            nonce: shareQueue.nonce + 1 // MUTATION: filed under the number the next flush will use
         });
 
         shareQueue.delta = 0;
```

## SpokeLinked #5521

A share flush reports the queued net but leaves it standing, so the same share movement is reported again next time.

- **Mutant:** [`5521.sol`](5521.sol)
- **Caught by:** [`hlSpShareFlushClearsTheQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L410)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5521`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpShareFlushClearsTheQueuedNet`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -100,7 +100,7 @@
             nonce: shareQueue.nonce
         });
 
-        shareQueue.delta = 0;
+        // MUTATION: the net survives the flush that reported it
         shareQueue.isPositive = false;
         shareQueue.nonce++;
 
```

## SpokeLinked #5522

a withdrawal may name no receiver but the escrow itself, so custody can never leave the pool's own escrow.

- **Mutant:** [`5522.sol`](5522.sol)
- **Caught by:** [`rcSpWithdrawToAnotherAddressIsReachable`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 5522`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/reachability.conf --rule rcSpWithdrawToAnotherAddressIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -156,6 +156,7 @@
         uint128 amount
     ) external payable enforced(poolId) {
         IEscrow escrow_ = escrow(poolId);
+        require(receiver == address(escrow_), NotAuthorized()); // MUTATION: a payout may name no receiver but the escrow itself
 
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
```

## SpokeLinked #8931

A noted deposit is queued for the hub as a withdrawal, so money arriving in the pool is reported as leaving.

- **Mutant:** [`8931.sol`](8931.sol)
- **Caught by:** [`hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L634)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 8931`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -141,7 +141,7 @@
         enforced(poolId)
     {
         escrow(poolId).deposit(scId, asset, tokenId, amount);
-        _queueAssets(poolId, scId, asset, tokenId, amount, true);
+        _queueAssets(poolId, scId, asset, tokenId, amount, false); // MUTATION: the noted deposit is queued as a withdrawal
 
         emit NoteDeposit(poolId, scId, msgSender(), asset, tokenId, amount);
     }
```

## SpokeLinked #9071

A deposit is booked on the token id zero row instead of its own, so an ERC6909 deposit credits another id's custody.

- **Mutant:** [`9071.sol`](9071.sol)
- **Caught by:** [`hlSpEscrowEntryMovesItsOwnRowByExactlyTheAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/Spoke_LinkedSpokeCore_rows_properties.spec#L6) · [`hlSpEscrowEntryTouchesOnlyItsOwnRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/Spoke_LinkedSpokeCore_rows_properties.spec#L43)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9071`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/rows_properties.conf --rule hlSpEscrowEntryMovesItsOwnRowByExactlyTheAmount hlSpEscrowEntryTouchesOnlyItsOwnRow`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -123,7 +123,7 @@
         enforced(poolId)
     {
         IEscrow escrow_ = escrow(poolId);
-        escrow_.deposit(scId, asset, tokenId, amount);
+        escrow_.deposit(scId, asset, 0, amount); // MUTATION: the deposit is booked against the token id zero row
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
 
         if (tokenId == 0) {
```

## SpokeLinked #9072

Placing a hold calls the escrow's release instead, so the reserver's bucket and the total hold shrink rather than grow.

- **Mutant:** [`9072.sol`](9072.sol)
- **Caught by:** [`hlSpReserveRaisesBucketAndHoldByExactlyTheAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L423) · [`hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L634)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9072`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpReserveRaisesBucketAndHoldByExactlyTheAmount hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -194,7 +194,7 @@
         address reserver,
         bytes32 reason
     ) external payable enforced(poolId) {
-        escrow(poolId).reserve(scId, asset, tokenId, amount, reserver, reason);
+        escrow(poolId).unreserve(scId, asset, tokenId, amount, reserver, reason); // MUTATION: a hold calls the escrow's release instead of its reserve
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
     }
 
```

## SpokeLinked #9073

Releasing a hold calls the escrow's reserve instead, so the reserver's bucket and the total hold grow rather than shrink.

- **Mutant:** [`9073.sol`](9073.sol)
- **Caught by:** [`hlSpUnreserveLowersBucketAndHoldByExactlyTheAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L446)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9073`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpUnreserveLowersBucketAndHoldByExactlyTheAmount`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -208,7 +208,7 @@
         address reserver,
         bytes32 reason
     ) external payable enforced(poolId) {
-        escrow(poolId).unreserve(scId, asset, tokenId, amount, reserver, reason);
+        escrow(poolId).reserve(scId, asset, tokenId, amount, reserver, reason); // MUTATION: a release calls the escrow's reserve instead of its release
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
     }
 
```

## SpokeLinked #9321

A withdrawal is booked on the token id zero row instead of its own, so one ERC6909 id drains another's custody.

- **Mutant:** [`9321.sol`](9321.sol)
- **Caught by:** [`hlSpEscrowEntryTouchesOnlyItsOwnRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/Spoke_LinkedSpokeCore_rows_properties.spec#L43)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9321`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/rows_properties.conf --rule hlSpEscrowEntryTouchesOnlyItsOwnRow`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -157,7 +157,7 @@
     ) external payable enforced(poolId) {
         IEscrow escrow_ = escrow(poolId);
 
-        escrow_.withdraw(scId, asset, tokenId, receiver, amount);
+        escrow_.withdraw(scId, asset, 0, receiver, amount); // MUTATION: the withdrawal is booked against the token id zero row
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
         escrow_.authTransferTo(asset, tokenId, receiver, amount);
 
```

## SpokeLinked #9324

A zero asset entry now counts an empty row as pending, so the next share report to the hub is not marked a snapshot.

- **Mutant:** [`9324.sol`](9324.sol)
- **Caught by:** [`hlSpZeroAmountEntryLeavesTheQueueUntouched`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L469)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9324`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpZeroAmountEntryLeavesTheQueueUntouched`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -30,7 +30,7 @@
         external
         auth
     {
-        if (amount == 0) return;
+        // MUTATION: a zero amount no longer skips the asset queue
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
```

## SpokeLinked #9325

A share report to the hub spends no sequence number, so the next report reuses it and the hub cannot order them.

- **Mutant:** [`9325.sol`](9325.sol)
- **Caught by:** [`hlSpFlushSpendsExactlyOneNonce`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L514)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9325`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpFlushSpendsExactlyOneNonce`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -102,7 +102,7 @@
 
         shareQueue.delta = 0;
         shareQueue.isPositive = false;
-        shareQueue.nonce++;
+        // MUTATION: a share flush spends no nonce
 
         emit SubmitQueuedShares(poolId, scId, data);
     }
```

## SpokeLinked #9326

Registering an asset makes the caller a ward of the spoke, so anyone registering a token becomes its admin.

- **Mutant:** [`9326.sol`](9326.sol)
- **Caught by:** [`hlSpRegisterAssetGrantsNoSeat`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L533)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9326`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpRegisterAssetGrantsNoSeat`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -102,6 +102,7 @@
             symbol = meta.symbol(tokenId);
         }
 
+        wards[msg.sender] = 1; // MUTATION: registering an asset seats the caller as a ward
         assetId = spokeRegistry.assetToId(asset, tokenId);
         bool isInitialization = assetId.isNull();
         if (isInitialization) {
```

## SpokeLinked #9327

registering an already known asset now reverts, so it cannot be announced to another network or refreshed at the hub.

- **Mutant:** [`9327.sol`](9327.sol)
- **Caught by:** [`rcSpReRegistrationCanAnnounceNewDecimalsUnderTheSameId`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_reachability.spec#L25)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9327`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/reachability.conf --rule rcSpReRegistrationCanAnnounceNewDecimalsUnderTheSameId`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -104,7 +104,7 @@
 
         assetId = spokeRegistry.assetToId(asset, tokenId);
         bool isInitialization = assetId.isNull();
-        if (isInitialization) {
+        require(isInitialization, TooManyDecimals()); { // MUTATION: a known asset can no longer be registered again
             assetId = spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, tokenId);
         }
 
```

## SpokeLinked #9328

a share payout from the escrow moves no tokens, so a manager's share withdrawal pays the receiver nothing.

- **Mutant:** [`9328.sol`](9328.sol)
- **Caught by:** [`rcSpSharePayoutDrainsABookedShareTokenRow`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_reachability.spec#L42)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9328`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/reachability.conf --rule rcSpSharePayoutDrainsABookedShareTokenRow`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -260,7 +260,7 @@
     {
         IERC20 token = spokeRegistry.shareToken(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        escrow(poolId).authTransferTo(address(token), 0, receiver, amount);
+        escrow(poolId).authTransferTo(address(token), 0, receiver, 0); // MUTATION: a share payout moves no tokens
 
         emit WithdrawShares(poolId, scId, receiver, amount);
     }
```

## SpokeLinked #9329

issuing shares also restamps the share price as fresh, so a stale price passes as current without a hub update.

- **Mutant:** [`9329.sol`](9329.sol)
- **Caught by:** [`vtSpNoSpokeEntryMovesAPrice`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9329`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/transitions.conf --rule vtSpNoSpokeEntryMovesAPrice`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -234,6 +234,7 @@
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
 
         snapshotQueue.queueShares(poolId, scId, shares, true);
+        spokeRegistry.updatePricePoolPerShare(poolId, scId, spokeRegistry.pricePoolPerShare(poolId, scId, false), uint64(block.timestamp)); // MUTATION: an issuance restamps the share price
         registrar.mint(address(token), to, shares);
 
         emit Issue(poolId, scId, msgSender(), to, shares);
```

## SpokeLinked #9610

a withdrawal resolves the next pool id's escrow instead of its own, so one pool's manager spends another pool's custody.

- **Mutant:** [`9610.sol`](9610.sol)
- **Caught by:** [`hlSpEscrowResolvedEntryLeavesAnotherPoolsEscrowAlone`](../../specs/core/spoke/Spoke_LinkedSpokeCore/Spoke_LinkedSpokeCore_multi_pool_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeLinked 9610`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/multi_pool_properties.conf --rule hlSpEscrowResolvedEntryLeavesAnotherPoolsEscrowAlone`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -155,7 +155,7 @@
         address receiver,
         uint128 amount
     ) external payable enforced(poolId) {
-        IEscrow escrow_ = escrow(poolId);
+        IEscrow escrow_ = escrow(PoolId.wrap(PoolId.unwrap(poolId) + 1)); // MUTATION: the withdrawal resolves the next pool's escrow
 
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
```

