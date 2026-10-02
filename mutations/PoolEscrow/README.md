# Mutations for `PoolEscrow` (`src/core/spoke/Escrow.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/misc/Auth.sol`, `src/misc/Recoverable.sol`.

| # | What we test |
|---|---|
| [2402](#poolescrow-2402) | reserve raises the row's aggregate reserved total without recording the hold in its per-reserver bucket, so the total drifts above the sum of holds.<br>Caught by: [`reservedMatchesBucketSum`](../../specs/core/spoke/Escrow/single/Escrow_valid_state.spec#L13) |
| [2403](#poolescrow-2403) | unreserve lowers the reserved total by the bucket's remainder instead of the released amount, so it desyncs from the holds.<br>Caught by: [`reservedMatchesBucketSum`](../../specs/core/spoke/Escrow/single/Escrow_valid_state.spec#L13) |
| [2404](#poolescrow-2404) | reserve books the hold under the transaction sender instead of the reserving caller, so the wrong bucket moves.<br>Caught by: [`reservedMatchesBucketSum`](../../specs/core/spoke/Escrow/single/Escrow_valid_state.spec#L13) |
| [2407](#poolescrow-2407) | withdraw no longer bounds the payout by the balance free of earmarks, so a call can pay out reserved funds.<br>Caught by: [`stPePayoutBoundedByFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_transitions.spec#L6) |
| [2411](#poolescrow-2411) | reserve writes the hold into the caller's bucket and into the zero reserver's bucket as well, so one call moves two buckets.<br>Caught by: [`stPeOneCallTouchesOneBucket`](../../specs/core/spoke/Escrow/single/Escrow_transitions.spec#L21) |
| [2413](#poolescrow-2413) | a new reserveFor books the hold in one asset's bucket but raises another asset's reserved total, so both rows desync.<br>Caught by: [`everyAssetRowMatchesItsBucketSum`](../../specs/core/spoke/Escrow/Escrow_multi_row_properties.spec#L6) |
| [5200](#poolescrow-5200) | deposit runs without its ward gate, so an account the escrow never relied can credit the pool's custody books.<br>Caught by: [`acPeOnlyWardMovesTheCustodyTotal`](../../specs/core/spoke/Escrow/single/Escrow_access_control.spec#L4) |
| [5201](#poolescrow-5201) | reserve runs without its ward gate, so any account can raise the reserved total and a reserver's bucket.<br>Caught by: [`acPeOnlyWardMovesTheAggregateHold`](../../specs/core/spoke/Escrow/single/Escrow_access_control.spec#L20) · [`acPeOnlyWardMovesAReservationBucket`](../../specs/core/spoke/Escrow/single/Escrow_access_control.spec#L36) |
| [5202](#poolescrow-5202) | rely runs without its ward gate, so an account the escrow never relied can seat itself on the roll that moves the pool's assets.<br>Caught by: [`acPeOnlyWardMovesAWardSeat`](../../specs/core/spoke/Escrow/single/Escrow_access_control.spec#L53) |
| [5203](#poolescrow-5203) | availableBalanceOf reports the gross custody total and ignores the earmarks, so the view advertises as free an amount that is already held.<br>Caught by: [`hlPeAvailableBalanceIsTheUnreservedCustody`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L4) |
| [5204](#poolescrow-5204) | withdraw debits the row's earmark instead of its custody, so a payout leaves the custody total untouched and quietly releases a hold.<br>Caught by: [`hlPeSweepingTheFreeBalanceLeavesTheEarmarks`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L19) · [`hlPeTakeInThenPayOutRestoresTheCustody`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L51) · [`hlPeCustodyRoundTripTouchesNoHold`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L67) |
| [5205](#poolescrow-5205) | reserve overwrites the key's standing hold instead of adding to it, so the earlier hold in that bucket is lost.<br>Caught by: [`hlPeReserveThenReleaseRestoresTheBucket`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L35) |
| [5206](#poolescrow-5206) | reserve records the hold in the reserver's bucket but never raises the row's aggregate earmark, so a fresh hold caps no payout at all.<br>Caught by: [`hlPeAnyHoldCapsEveryPayout`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L83) |
| [5207](#poolescrow-5207) | deposit books the credit in an unchecked block, so a total that cannot fit its width wraps instead of turning the call away.<br>Caught by: [`stPeOnlyAWithdrawalLowersTheCustodyTotal`](../../specs/core/spoke/Escrow/single/Escrow_transitions.spec#L38) |
| [5208](#poolescrow-5208) | withdraw refuses a payout of exactly the free balance, so the advertised free balance can never be withdrawn in full.<br>Caught by: [`rcPeWithdrawSweepsTheAdvertisedFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L55) |
| [5209](#poolescrow-5209) | reserve raises the row's reserved total in an unchecked block, so it can overflow and wrap instead of reverting.<br>Caught by: [`reservedMatchesBucketSum`](../../specs/core/spoke/Escrow/single/Escrow_valid_state.spec#L13) |
| [5210](#poolescrow-5210) | unreserve refuses a release of the named bucket's whole balance, so a key cannot hand back everything it placed on hold.<br>Caught by: [`rvPeUnreserveAlwaysAdmitsAKeyReleasingItsWholeBucket`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L157) |
| [5212](#poolescrow-5212) | deny refuses to remove the caller itself, so a ward can no longer step down.<br>Caught by: [`rvPeDenyAlwaysAdmitsAWardStandingItselfDown`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L174) |
| [5213](#poolescrow-5213) | availableBalanceOf loses its floor at zero, so the view reverts whenever holds exceed the custody total.<br>Caught by: [`rvPeAvailableBalanceOfAlwaysAnswers`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L100) |
| [5214](#poolescrow-5214) | authTransferTo runs without its ward gate, so an outsider can move the escrow's tokens to any receiver it names.<br>Caught by: [`rvPeAuthTransferToRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L113) |
| [5215](#poolescrow-5215) | recoverTokens for ether and plain tokens runs without its ward gate, so the escape hatch meant for stray assets answers an outsider.<br>Caught by: [`rvPeRecoverTokensRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L128) |
| [5216](#poolescrow-5216) | recoverTokens by token id runs without its ward gate, so an outsider can pull any nonzero id ERC6909 token out.<br>Caught by: [`rvPeRecoverTokensByTokenIdRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L142) |
| [6802](#poolescrow-6802) | deposit turns away every row whose token id is set, so the ERC6909 side of the custody book can never be credited at all.<br>Caught by: [`rcPeDepositBooksAnErc6909Row`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L4) |
| [6803](#poolescrow-6803) | deposit also earmarks everything it credits, so deposits never add to the free balance.<br>Caught by: [`rcPeDepositReopensAFullyEncumberedRow`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L21) |
| [6804](#poolescrow-6804) | withdraw bounds the payout by the earmark instead of the free balance, so an unearmarked row pays nothing.<br>Caught by: [`rcPeWithdrawEmptiesAnUnencumberedRow`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L39) |
| [6805](#poolescrow-6805) | availableBalanceOf advertises one unit more than the row holds free, so paying out the advertised amount reverts.<br>Caught by: [`rcPeWithdrawSweepsTheAdvertisedFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L55) · [`rcPeHoldPayoutReleaseWidensTheFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L338) |
| [6806](#poolescrow-6806) | withdraw demands the payout equal the whole free balance, so no partial payout can leave funds free.<br>Caught by: [`rcPeWithdrawLeavesTheRowStillPaying`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L73) |
| [6807](#poolescrow-6807) | withdraw turns away every payout naming the null address, so the accounting only entry to that receiver can never be booked.<br>Caught by: [`rcPeWithdrawBooksAPayoutToANullReceiver`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L91) |
| [6808](#poolescrow-6808) | reserve fills the key's bucket but never raises the row's earmark, so no hold narrows the free balance.<br>Caught by: [`rcPeReserveOpensABucket`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L107) · [`rcPeReserveEncumbersTheWholeFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L231) |
| [6809](#poolescrow-6809) | reserve requires the bucket key to be a ward, so no hold can be booked for an account without authority.<br>Caught by: [`rcPeReserveBooksABucketForAnUnauthorizedKey`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L126) |
| [6810](#poolescrow-6810) | unreserve requires the bucket key to be the calling account, so a ward cannot release another party's hold.<br>Caught by: [`rcPeUnreserveEmptiesAForeignBucket`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L144) |
| [6811](#poolescrow-6811) | reserve books the hold under the transaction sender rather than under the named key, so only one party's bucket on a row can ever move.<br>Caught by: [`rcPeTwoReserversHoldOneRowAtOnce`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L165) |
| [6812](#poolescrow-6812) | reserve sets the row's earmark to the newest hold instead of adding it, so a second hold displaces the first.<br>Caught by: [`rcPeOneReserverHoldsTwoReasons`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L188) |
| [6813](#poolescrow-6813) | reserve refuses any hold that would earmark more than the row holds, so a hold can no longer be placed ahead of the funds.<br>Caught by: [`rcPeReserveBeyondCustodyFreezesTheRow`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L212) · [`rcPeReleaseLetsAnOverEncumberedRowPayOutAgain`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L315) |
| [6814](#poolescrow-6814) | unreserve refuses a release equal to the whole bucket, so no hold can ever be fully released.<br>Caught by: [`rcPeUnreserveClearsTheRowsEarmark`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L251) |
| [6815](#poolescrow-6815) | unreserve requires a release to equal the whole bucket, so part of a hold can no longer be released.<br>Caught by: [`rcPeUnreserveLeavesTheBucketStillHolding`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L269) |
| [6816](#poolescrow-6816) | unreserve zeroes the row's reserved total instead of lowering it, so other parties' holds drop out of it.<br>Caught by: [`rcPeReleasingOneBucketLeavesTheOtherHeld`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L288) |
| [6817](#poolescrow-6817) | rely refuses any account not already a ward, so no new account can ever be granted a seat.<br>Caught by: [`rcPeFreshlyReliedAccountBooksADeposit`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L380) |
| [6818](#poolescrow-6818) | deny refuses to strip any seat but the caller's own, so a ward can no longer remove another account from the roll.<br>Caught by: [`rcPeDenyRevokesAnotherWard`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L364) |
| [6820](#poolescrow-6820) | unreserve runs without its ward gate, so an account the escrow never relied releases a hold it never placed.<br>Caught by: [`rvPeUnreserveRefusesANonWardOrAShortBucket`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L54) |
| [6821](#poolescrow-6821) | deny runs without the ward gate, so an account holding no seat strips a ward of its permissions.<br>Caught by: [`rvPeDenyRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L86) |
| [6822](#poolescrow-6822) | the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.<br>Caught by: [`rvPeDepositRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L4) · [`rvPeReserveRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L39) · [`rvPeRelyRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L72) |
| [8106](#poolescrow-8106) | recoverTokens pays a plain token back to the escrow itself instead of the named receiver, so an ERC20 recovery moves nothing out of custody.<br>Caught by: [`rcPeRecoverTokensMovesCustodyWithoutTheLedger`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L108) |
| [8802](#poolescrow-8802) | a new deposit entry credits one value to two share classes, so one class's booking also inflates a sibling's holding.<br>Caught by: [`stPeEscrowRowIsPerShareClass`](../../specs/core/spoke/Escrow/Escrow_multi_share_class_properties.spec#L6) |
| [8920](#poolescrow-8920) | withdraw refuses every payout while any amount of the holding is reserved, so a reservation freezes the free balance beside it.<br>Caught by: [`rvPeWithdrawAlwaysAdmitsAWardWithinTheFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L188) |
| [8953](#poolescrow-8953) | withdraw runs without its ward gate, so an account the escrow never relied books a payout out of the pool's custody.<br>Caught by: [`rvPeWithdrawRefusesANonWardOrAPayoutBeyondTheFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L19) |
| [9009](#poolescrow-9009) | a forced ERC20 transfer out of the escrow pays the caller instead of the named receiver, so the caller pockets the tokens.<br>Caught by: [`hlPeCustodyMoversWriteNoBook`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L31) |
| [9018](#poolescrow-9018) | a deposit is also credited to the asset's plain token row, so one deposit of a tokenised asset raises two holdings.<br>Caught by: [`stPeACallMovesAtMostOneHoldingRow`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L43) |
| [9019](#poolescrow-9019) | releasing a reservation debits the holding's total instead of its reserved amount, so the escrow books a payout nobody made.<br>Caught by: [`vtPeTotalMovesOnlyOnFlowsAndReservedOnlyOnReservations`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L13) |
| [9046](#poolescrow-9046) | reserve raises the reserved total but never writes the key's bucket, so the bucket does not read back the new hold.<br>Caught by: [`rcPeBucketReadsBackTheHold`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L402) |
| [9047](#poolescrow-9047) | unreserve sets the row's reserved total to this key's remaining hold, so other keys' holds are silently released.<br>Caught by: [`hlPeUnreserveMirrorsBucketAndAggregateExactly`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L148) |
| [9390](#poolescrow-9390) | reserve adds the hold to the caller's ward seat, not the reserved total, so wards change outside rely and deny.<br>Caught by: [`acPeWardSeatMovesOnlyThroughRelyOrDeny`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L178) |
| [9391](#poolescrow-9391) | deposit credits the neighbouring tokenId's row instead of its own, so booked custody lands on a row the call never named.<br>Caught by: [`hlPeDepositMovesExactlyItsOwnRow`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L70) |
| [9392](#poolescrow-9392) | withdraw debits only half the paid out amount from the row's custody total, so the books keep claiming funds that already left.<br>Caught by: [`hlPeWithdrawMovesExactlyItsOwnRow`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L95) |
| [9393](#poolescrow-9393) | reserve raises the row's custody total instead of its earmark, so a hold inflates what the escrow claims to hold and caps nothing.<br>Caught by: [`hlPeReserveMirrorsBucketAndAggregateExactly`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L120) |
| [9395](#poolescrow-9395) | reserve overwrites the row's earmark with the new hold instead of adding to it, so the aggregate forgets every hold already standing against the row.<br>Caught by: [`reservedIsTheSumOfEveryBucket`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L6) |
| [9396](#poolescrow-9396) | rely sets the account's seat to 2 instead of 1, so the auth gate never recognises a freshly relied account.<br>Caught by: [`acPeWardSeatMovesOnlyThroughRelyOrDeny`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L178) |
| [9397](#poolescrow-9397) | withdraw checks and debits the next token id's row instead of its own, so a payout drains another holding.<br>Caught by: [`hlPeWithdrawMovesExactlyItsOwnRow`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L95) |
| [9580](#poolescrow-9580) | authTransferTo skips the ERC20 balance check, so a payout beyond the escrow's balance is left to the token to refuse.<br>Caught by: [`rvPeAuthTransferToRefusesAShortCustody`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L64) |
| [9581](#poolescrow-9581) | authTransferTo pays out the escrow's whole ERC20 balance instead of the amount asked for, so one forced transfer empties the custody of that token.<br>Caught by: [`hlPeAuthTransferToMovesExactlyTheAmount`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L6) |
| [9582](#poolescrow-9582) | authTransferTo sends a plain ERC20 payout down the ERC6909 path, so a forced transfer of an ERC20 moves none of the escrow's ERC20 custody.<br>Caught by: [`rcPeAuthTransferToMovesCustodyWithoutTheLedger`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L81) |

## PoolEscrow #2402

reserve raises the row's aggregate reserved total without recording the hold in its per-reserver bucket, so the total drifts above the sum of holds.

- **Mutant:** [`2402.sol`](2402.sol)
- **Caught by:** [`reservedMatchesBucketSum`](../../specs/core/spoke/Escrow/single/Escrow_valid_state.spec#L13)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 2402`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/valid_state.conf --rule reservedMatchesBucketSum`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -59,7 +59,7 @@
         Holding storage holding_ = holding[scId][asset][tokenId];
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
-        reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
+        // MUTATION: dropped the per-reserver bucket update
         holding_.reserved += value;
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
```

## PoolEscrow #2403

unreserve lowers the reserved total by the bucket's remainder instead of the released amount, so it desyncs from the holds.

- **Mutant:** [`2403.sol`](2403.sol)
- **Caught by:** [`reservedMatchesBucketSum`](../../specs/core/spoke/Escrow/single/Escrow_valid_state.spec#L13)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 2403`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/valid_state.conf --rule reservedMatchesBucketSum`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -77,7 +77,7 @@
 
         uint128 newReservedAmount = currentReserved - value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved -= value;
+        holding_.reserved -= newReservedAmount; // MUTATION: releases the remaining bucket balance instead of the requested amount
 
         emit DecreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #2404

reserve books the hold under the transaction sender instead of the reserving caller, so the wrong bucket moves.

- **Mutant:** [`2404.sol`](2404.sol)
- **Caught by:** [`reservedMatchesBucketSum`](../../specs/core/spoke/Escrow/single/Escrow_valid_state.spec#L13)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 2404`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/valid_state.conf --rule reservedMatchesBucketSum`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -59,7 +59,7 @@
         Holding storage holding_ = holding[scId][asset][tokenId];
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
-        reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
+        reservedBy[scId][msg.sender][reason][asset][tokenId] = newReservedAmount; // MUTATION: bucket keyed by msg.sender instead of caller
         holding_.reserved += value;
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
```

## PoolEscrow #2407

withdraw no longer bounds the payout by the balance free of earmarks, so a call can pay out reserved funds.

- **Mutant:** [`2407.sol`](2407.sol)
- **Caught by:** [`stPePayoutBoundedByFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 2407`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/transitions.conf --rule stPePayoutBoundedByFreeBalance`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -45,7 +45,7 @@
         require(holding_.total >= holding_.reserved, InsufficientBalance(asset, tokenId, value, 0));
 
         uint128 balance = holding_.total - holding_.reserved;
-        require(balance >= value, InsufficientBalance(asset, tokenId, value, balance));
+        // MUTATION: the free balance no longer bounds the payout
 
         holding_.total -= value;
         emit Withdraw(asset, tokenId, poolId, scId, receiver, value);
```

## PoolEscrow #2411

reserve writes the hold into the caller's bucket and into the zero reserver's bucket as well, so one call moves two buckets.

- **Mutant:** [`2411.sol`](2411.sol)
- **Caught by:** [`stPeOneCallTouchesOneBucket`](../../specs/core/spoke/Escrow/single/Escrow_transitions.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 2411`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/transitions.conf --rule stPeOneCallTouchesOneBucket`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -60,6 +60,8 @@
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
+        // MUTATION: a second bucket is written by the same call
+        reservedBy[scId][address(0)][reason][asset][tokenId] += value;
         holding_.reserved += value;
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
```

## PoolEscrow #2413

a new reserveFor books the hold in one asset's bucket but raises another asset's reserved total, so both rows desync.

- **Mutant:** [`2413.sol`](2413.sol)
- **Caught by:** [`everyAssetRowMatchesItsBucketSum`](../../specs/core/spoke/Escrow/Escrow_multi_row_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 2413`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/multi_row_properties.conf --rule everyAssetRowMatchesItsBucketSum`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -49,6 +49,21 @@
 
         holding_.total -= value;
         emit Withdraw(asset, tokenId, poolId, scId, receiver, value);
+    }
+
+    /// @notice MUTATION: charges the hold to one row's bucket while raising another row's earmark.
+    function reserveFor(
+        ShareClassId scId,
+        address asset,
+        uint256 tokenId,
+        address earmarkAsset,
+        uint256 earmarkTokenId,
+        uint128 value,
+        address caller,
+        bytes32 reason
+    ) external auth {
+        reservedBy[scId][caller][reason][asset][tokenId] += value;
+        holding[scId][earmarkAsset][earmarkTokenId].reserved += value;
     }
 
     /// @inheritdoc IEscrow
```

## PoolEscrow #5200

deposit runs without its ward gate, so an account the escrow never relied can credit the pool's custody books.

- **Mutant:** [`5200.sol`](5200.sol)
- **Caught by:** [`acPeOnlyWardMovesTheCustodyTotal`](../../specs/core/spoke/Escrow/single/Escrow_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5200`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/access_control.conf --rule acPeOnlyWardMovesTheCustodyTotal`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -30,7 +30,7 @@
     }
 
     /// @inheritdoc IEscrow
-    function deposit(ShareClassId scId, address asset, uint256 tokenId, uint128 value) external auth {
+    function deposit(ShareClassId scId, address asset, uint256 tokenId, uint128 value) external { // MUTATION: the booking gate no longer asks for a ward
         holding[scId][asset][tokenId].total += value;
 
         emit Deposit(asset, tokenId, poolId, scId, value);
```

## PoolEscrow #5201

reserve runs without its ward gate, so any account can raise the reserved total and a reserver's bucket.

- **Mutant:** [`5201.sol`](5201.sol)
- **Caught by:** [`acPeOnlyWardMovesTheAggregateHold`](../../specs/core/spoke/Escrow/single/Escrow_access_control.spec#L20) · [`acPeOnlyWardMovesAReservationBucket`](../../specs/core/spoke/Escrow/single/Escrow_access_control.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5201`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/access_control.conf --rule acPeOnlyWardMovesTheAggregateHold acPeOnlyWardMovesAReservationBucket`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -54,7 +54,7 @@
     /// @inheritdoc IEscrow
     function reserve(ShareClassId scId, address asset, uint256 tokenId, uint128 value, address caller, bytes32 reason)
         external
-        auth
+        // MUTATION: the hold gate no longer asks for a ward
     {
         Holding storage holding_ = holding[scId][asset][tokenId];
 
```

## PoolEscrow #5202

rely runs without its ward gate, so an account the escrow never relied can seat itself on the roll that moves the pool's assets.

- **Mutant:** [`5202.sol`](5202.sol)
- **Caught by:** [`acPeOnlyWardMovesAWardSeat`](../../specs/core/spoke/Escrow/single/Escrow_access_control.spec#L53)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5202`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/access_control.conf --rule acPeOnlyWardMovesAWardSeat`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -22,7 +22,7 @@
     }
 
     /// @inheritdoc IAuth
-    function rely(address user) public auth {
+    function rely(address user) public { // MUTATION: the ward roll is extended by any caller
         wards[user] = 1;
         emit Rely(user);
     }
```

## PoolEscrow #5203

availableBalanceOf reports the gross custody total and ignores the earmarks, so the view advertises as free an amount that is already held.

- **Mutant:** [`5203.sol`](5203.sol)
- **Caught by:** [`hlPeAvailableBalanceIsTheUnreservedCustody`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5203`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/high_level.conf --rule hlPeAvailableBalanceIsTheUnreservedCustody`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -103,6 +103,6 @@
     function availableBalanceOf(ShareClassId scId, address asset, uint256 tokenId) public view returns (uint128) {
         Holding storage holding_ = holding[scId][asset][tokenId];
         if (holding_.total < holding_.reserved) return 0;
-        return holding_.total - holding_.reserved;
+        return holding_.total; // MUTATION: the view reports gross custody and ignores the holds
     }
 }
```

## PoolEscrow #5204

withdraw debits the row's earmark instead of its custody, so a payout leaves the custody total untouched and quietly releases a hold.

- **Mutant:** [`5204.sol`](5204.sol)
- **Caught by:** [`hlPeSweepingTheFreeBalanceLeavesTheEarmarks`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L19) · [`hlPeTakeInThenPayOutRestoresTheCustody`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L51) · [`hlPeCustodyRoundTripTouchesNoHold`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L67)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5204`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/high_level.conf --rule hlPeSweepingTheFreeBalanceLeavesTheEarmarks hlPeTakeInThenPayOutRestoresTheCustody hlPeCustodyRoundTripTouchesNoHold`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -47,7 +47,7 @@
         uint128 balance = holding_.total - holding_.reserved;
         require(balance >= value, InsufficientBalance(asset, tokenId, value, balance));
 
-        holding_.total -= value;
+        holding_.reserved -= value; // MUTATION: the payout is debited from the earmark instead of custody
         emit Withdraw(asset, tokenId, poolId, scId, receiver, value);
     }
 
```

## PoolEscrow #5205

reserve overwrites the key's standing hold instead of adding to it, so the earlier hold in that bucket is lost.

- **Mutant:** [`5205.sol`](5205.sol)
- **Caught by:** [`hlPeReserveThenReleaseRestoresTheBucket`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L35)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5205`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/high_level.conf --rule hlPeReserveThenReleaseRestoresTheBucket`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -59,7 +59,7 @@
         Holding storage holding_ = holding[scId][asset][tokenId];
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
-        reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
+        reservedBy[scId][caller][reason][asset][tokenId] = value; // MUTATION: the new hold overwrites the key's standing hold
         holding_.reserved += value;
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
```

## PoolEscrow #5206

reserve records the hold in the reserver's bucket but never raises the row's aggregate earmark, so a fresh hold caps no payout at all.

- **Mutant:** [`5206.sol`](5206.sol)
- **Caught by:** [`hlPeAnyHoldCapsEveryPayout`](../../specs/core/spoke/Escrow/single/Escrow_high_level.spec#L83)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5206`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/high_level.conf --rule hlPeAnyHoldCapsEveryPayout`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -60,7 +60,7 @@
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved += value;
+        // MUTATION: the aggregate earmark is no longer raised by the new hold
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #5207

deposit books the credit in an unchecked block, so a total that cannot fit its width wraps instead of turning the call away.

- **Mutant:** [`5207.sol`](5207.sol)
- **Caught by:** [`stPeOnlyAWithdrawalLowersTheCustodyTotal`](../../specs/core/spoke/Escrow/single/Escrow_transitions.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5207`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/transitions.conf --rule stPeOnlyAWithdrawalLowersTheCustodyTotal`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -31,7 +31,7 @@
 
     /// @inheritdoc IEscrow
     function deposit(ShareClassId scId, address asset, uint256 tokenId, uint128 value) external auth {
-        holding[scId][asset][tokenId].total += value;
+        unchecked { holding[scId][asset][tokenId].total += value; } // MUTATION: the booking no longer refuses a total that will not fit
 
         emit Deposit(asset, tokenId, poolId, scId, value);
     }
```

## PoolEscrow #5208

withdraw refuses a payout of exactly the free balance, so the advertised free balance can never be withdrawn in full.

- **Mutant:** [`5208.sol`](5208.sol)
- **Caught by:** [`rcPeWithdrawSweepsTheAdvertisedFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L55)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5208`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeWithdrawSweepsTheAdvertisedFreeBalance`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -45,7 +45,7 @@
         require(holding_.total >= holding_.reserved, InsufficientBalance(asset, tokenId, value, 0));
 
         uint128 balance = holding_.total - holding_.reserved;
-        require(balance >= value, InsufficientBalance(asset, tokenId, value, balance));
+        require(balance > value, InsufficientBalance(asset, tokenId, value, balance)); // MUTATION: the payout gate refuses the whole free balance
 
         holding_.total -= value;
         emit Withdraw(asset, tokenId, poolId, scId, receiver, value);
```

## PoolEscrow #5209

reserve raises the row's reserved total in an unchecked block, so it can overflow and wrap instead of reverting.

- **Mutant:** [`5209.sol`](5209.sol)
- **Caught by:** [`reservedMatchesBucketSum`](../../specs/core/spoke/Escrow/single/Escrow_valid_state.spec#L13)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5209`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/valid_state.conf --rule reservedMatchesBucketSum`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -60,7 +60,7 @@
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved += value;
+        unchecked { holding_.reserved += value; } // MUTATION: the aggregate hold no longer refuses a value that will not fit
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #5210

unreserve refuses a release of the named bucket's whole balance, so a key cannot hand back everything it placed on hold.

- **Mutant:** [`5210.sol`](5210.sol)
- **Caught by:** [`rvPeUnreserveAlwaysAdmitsAKeyReleasingItsWholeBucket`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L157)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5210`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeUnreserveAlwaysAdmitsAKeyReleasingItsWholeBucket`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -73,7 +73,7 @@
         Holding storage holding_ = holding[scId][asset][tokenId];
 
         uint128 currentReserved = reservedBy[scId][caller][reason][asset][tokenId];
-        require(currentReserved >= value, InsufficientReserve());
+        require(currentReserved > value, InsufficientReserve()); // MUTATION: releasing the bucket's whole balance is refused
 
         uint128 newReservedAmount = currentReserved - value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
```

## PoolEscrow #5212

deny refuses to remove the caller itself, so a ward can no longer step down.

- **Mutant:** [`5212.sol`](5212.sol)
- **Caught by:** [`rvPeDenyAlwaysAdmitsAWardStandingItselfDown`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L174)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5212`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeDenyAlwaysAdmitsAWardStandingItselfDown`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,6 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
+        require(user != msg.sender, NotAuthorized()); // MUTATION: the ward roll refuses to remove the caller's own seat
         wards[user] = 0;
         emit Deny(user);
     }
```

## PoolEscrow #5213

availableBalanceOf loses its floor at zero, so the view reverts whenever holds exceed the custody total.

- **Mutant:** [`5213.sol`](5213.sol)
- **Caught by:** [`rvPeAvailableBalanceOfAlwaysAnswers`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L100)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5213`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeAvailableBalanceOfAlwaysAnswers`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -102,7 +102,7 @@
     /// @inheritdoc IEscrow
     function availableBalanceOf(ShareClassId scId, address asset, uint256 tokenId) public view returns (uint128) {
         Holding storage holding_ = holding[scId][asset][tokenId];
-        if (holding_.total < holding_.reserved) return 0;
+        // MUTATION: the floor at zero is gone, so an over reserved row underflows
         return holding_.total - holding_.reserved;
     }
 }
```

## PoolEscrow #5214

authTransferTo runs without its ward gate, so an outsider can move the escrow's tokens to any receiver it names.

- **Mutant:** [`5214.sol`](5214.sol)
- **Caught by:** [`rvPeAuthTransferToRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L113)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5214`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeAuthTransferToRefusesANonWard`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -83,7 +83,7 @@
     }
 
     /// @inheritdoc IEscrow
-    function authTransferTo(address asset, uint256 tokenId, address receiver, uint256 amount) external auth {
+    function authTransferTo(address asset, uint256 tokenId, address receiver, uint256 amount) external { // MUTATION: the payout gate no longer asks for a ward
         if (tokenId == 0) {
             uint256 balance = IERC20(asset).balanceOf(address(this));
             require(balance >= amount, InsufficientBalance(asset, tokenId, amount, balance));
```

## PoolEscrow #5215

recoverTokens for ether and plain tokens runs without its ward gate, so the escape hatch meant for stray assets answers an outsider.

- **Mutant:** [`5215.sol`](5215.sol)
- **Caught by:** [`rvPeRecoverTokensRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L128)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5215`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeRecoverTokensRefusesANonWard`

```diff
--- a/src/misc/Recoverable.sol
+++ b/src/misc/Recoverable.sol
@@ -12,7 +12,7 @@
 ///         receiver address.
 abstract contract Recoverable is Auth, IRecoverable {
     /// @inheritdoc IRecoverable
-    function recoverTokens(address token, address receiver, uint256 amount) public auth {
+    function recoverTokens(address token, address receiver, uint256 amount) public { // MUTATION: the recovery gate no longer asks for a ward
         if (token == ETH_ADDRESS) {
             SafeTransferLib.safeTransferETH(receiver, amount);
         } else {
```

## PoolEscrow #5216

recoverTokens by token id runs without its ward gate, so an outsider can pull any nonzero id ERC6909 token out.

- **Mutant:** [`5216.sol`](5216.sol)
- **Caught by:** [`rvPeRecoverTokensByTokenIdRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L142)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 5216`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeRecoverTokensByTokenIdRefusesANonWard`

```diff
--- a/src/misc/Recoverable.sol
+++ b/src/misc/Recoverable.sol
@@ -21,7 +21,7 @@
     }
 
     /// @inheritdoc IRecoverable
-    function recoverTokens(address token, uint256 tokenId, address receiver, uint256 amount) external auth {
+    function recoverTokens(address token, uint256 tokenId, address receiver, uint256 amount) external { // MUTATION: the multi token recovery gate no longer asks for a ward
         if (tokenId == 0) {
             recoverTokens(token, receiver, amount);
         } else {
```

## PoolEscrow #6802

deposit turns away every row whose token id is set, so the ERC6909 side of the custody book can never be credited at all.

- **Mutant:** [`6802.sol`](6802.sol)
- **Caught by:** [`rcPeDepositBooksAnErc6909Row`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6802`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeDepositBooksAnErc6909Row`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -31,6 +31,7 @@
 
     /// @inheritdoc IEscrow
     function deposit(ShareClassId scId, address asset, uint256 tokenId, uint128 value) external auth {
+        require(tokenId == 0, InsufficientReserve()); // MUTATION: the booking gate turns away every ERC6909 row
         holding[scId][asset][tokenId].total += value;
 
         emit Deposit(asset, tokenId, poolId, scId, value);
```

## PoolEscrow #6803

deposit also earmarks everything it credits, so deposits never add to the free balance.

- **Mutant:** [`6803.sol`](6803.sol)
- **Caught by:** [`rcPeDepositReopensAFullyEncumberedRow`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6803`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeDepositReopensAFullyEncumberedRow`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -32,6 +32,7 @@
     /// @inheritdoc IEscrow
     function deposit(ShareClassId scId, address asset, uint256 tokenId, uint128 value) external auth {
         holding[scId][asset][tokenId].total += value;
+        holding[scId][asset][tokenId].reserved += value; // MUTATION: the booking earmarks whatever it credits
 
         emit Deposit(asset, tokenId, poolId, scId, value);
     }
```

## PoolEscrow #6804

withdraw bounds the payout by the earmark instead of the free balance, so an unearmarked row pays nothing.

- **Mutant:** [`6804.sol`](6804.sol)
- **Caught by:** [`rcPeWithdrawEmptiesAnUnencumberedRow`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L39)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6804`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeWithdrawEmptiesAnUnencumberedRow`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -44,7 +44,7 @@
         Holding storage holding_ = holding[scId][asset][tokenId];
         require(holding_.total >= holding_.reserved, InsufficientBalance(asset, tokenId, value, 0));
 
-        uint128 balance = holding_.total - holding_.reserved;
+        uint128 balance = holding_.reserved; // MUTATION: the payout is bounded by the earmark, not by the free balance
         require(balance >= value, InsufficientBalance(asset, tokenId, value, balance));
 
         holding_.total -= value;
```

## PoolEscrow #6805

availableBalanceOf advertises one unit more than the row holds free, so paying out the advertised amount reverts.

- **Mutant:** [`6805.sol`](6805.sol)
- **Caught by:** [`rcPeWithdrawSweepsTheAdvertisedFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L55) · [`rcPeHoldPayoutReleaseWidensTheFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L338)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6805`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeWithdrawSweepsTheAdvertisedFreeBalance rcPeHoldPayoutReleaseWidensTheFreeBalance`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -103,6 +103,6 @@
     function availableBalanceOf(ShareClassId scId, address asset, uint256 tokenId) public view returns (uint128) {
         Holding storage holding_ = holding[scId][asset][tokenId];
         if (holding_.total < holding_.reserved) return 0;
-        return holding_.total - holding_.reserved;
+        return holding_.total - holding_.reserved + 1; // MUTATION: the view advertises one unit more than the row holds free
     }
 }
```

## PoolEscrow #6806

withdraw demands the payout equal the whole free balance, so no partial payout can leave funds free.

- **Mutant:** [`6806.sol`](6806.sol)
- **Caught by:** [`rcPeWithdrawLeavesTheRowStillPaying`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L73)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6806`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeWithdrawLeavesTheRowStillPaying`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -45,7 +45,7 @@
         require(holding_.total >= holding_.reserved, InsufficientBalance(asset, tokenId, value, 0));
 
         uint128 balance = holding_.total - holding_.reserved;
-        require(balance >= value, InsufficientBalance(asset, tokenId, value, balance));
+        require(balance == value, InsufficientBalance(asset, tokenId, value, balance)); // MUTATION: the payout gate insists the caller take the whole free balance
 
         holding_.total -= value;
         emit Withdraw(asset, tokenId, poolId, scId, receiver, value);
```

## PoolEscrow #6807

withdraw turns away every payout naming the null address, so the accounting only entry to that receiver can never be booked.

- **Mutant:** [`6807.sol`](6807.sol)
- **Caught by:** [`rcPeWithdrawBooksAPayoutToANullReceiver`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L91)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6807`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeWithdrawBooksAPayoutToANullReceiver`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -41,6 +41,7 @@
         external
         auth
     {
+        require(receiver != address(0), InsufficientBalance(asset, tokenId, value, 0)); // MUTATION: the payout gate turns away the null receiver
         Holding storage holding_ = holding[scId][asset][tokenId];
         require(holding_.total >= holding_.reserved, InsufficientBalance(asset, tokenId, value, 0));
 
```

## PoolEscrow #6808

reserve fills the key's bucket but never raises the row's earmark, so no hold narrows the free balance.

- **Mutant:** [`6808.sol`](6808.sol)
- **Caught by:** [`rcPeReserveOpensABucket`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L107) · [`rcPeReserveEncumbersTheWholeFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L231)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6808`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeReserveOpensABucket rcPeReserveEncumbersTheWholeFreeBalance`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -60,7 +60,7 @@
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved += value;
+        // MUTATION: the row's aggregate earmark is left where it was
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #6809

reserve requires the bucket key to be a ward, so no hold can be booked for an account without authority.

- **Mutant:** [`6809.sol`](6809.sol)
- **Caught by:** [`rcPeReserveBooksABucketForAnUnauthorizedKey`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L126)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6809`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeReserveBooksABucketForAnUnauthorizedKey`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -57,6 +57,7 @@
         auth
     {
         Holding storage holding_ = holding[scId][asset][tokenId];
+        require(wards[caller] == 1, NotAuthorized()); // MUTATION: the bucket key must now be a ward itself
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
```

## PoolEscrow #6810

unreserve requires the bucket key to be the calling account, so a ward cannot release another party's hold.

- **Mutant:** [`6810.sol`](6810.sol)
- **Caught by:** [`rcPeUnreserveEmptiesAForeignBucket`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L144)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6810`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeUnreserveEmptiesAForeignBucket`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -71,6 +71,7 @@
         auth
     {
         Holding storage holding_ = holding[scId][asset][tokenId];
+        require(caller == msg.sender, NotAuthorized()); // MUTATION: only the key's own account may release its bucket
 
         uint128 currentReserved = reservedBy[scId][caller][reason][asset][tokenId];
         require(currentReserved >= value, InsufficientReserve());
```

## PoolEscrow #6811

reserve books the hold under the transaction sender rather than under the named key, so only one party's bucket on a row can ever move.

- **Mutant:** [`6811.sol`](6811.sol)
- **Caught by:** [`rcPeTwoReserversHoldOneRowAtOnce`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L165)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6811`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeTwoReserversHoldOneRowAtOnce`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -59,7 +59,7 @@
         Holding storage holding_ = holding[scId][asset][tokenId];
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
-        reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
+        reservedBy[scId][msg.sender][reason][asset][tokenId] = newReservedAmount; // MUTATION: the hold lands in the sender's bucket, not the named key's
         holding_.reserved += value;
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
```

## PoolEscrow #6812

reserve sets the row's earmark to the newest hold instead of adding it, so a second hold displaces the first.

- **Mutant:** [`6812.sol`](6812.sol)
- **Caught by:** [`rcPeOneReserverHoldsTwoReasons`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6812`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeOneReserverHoldsTwoReasons`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -60,7 +60,7 @@
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved += value;
+        holding_.reserved = value; // MUTATION: the aggregate earmark is set to the newest hold, not raised by it
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #6813

reserve refuses any hold that would earmark more than the row holds, so a hold can no longer be placed ahead of the funds.

- **Mutant:** [`6813.sol`](6813.sol)
- **Caught by:** [`rcPeReserveBeyondCustodyFreezesTheRow`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L212) · [`rcPeReleaseLetsAnOverEncumberedRowPayOutAgain`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L315)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6813`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeReserveBeyondCustodyFreezesTheRow rcPeReleaseLetsAnOverEncumberedRowPayOutAgain`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -57,6 +57,7 @@
         auth
     {
         Holding storage holding_ = holding[scId][asset][tokenId];
+        require(holding_.reserved + value <= holding_.total, InsufficientReserve()); // MUTATION: the hold gate refuses to earmark more than the row holds
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
```

## PoolEscrow #6814

unreserve refuses a release equal to the whole bucket, so no hold can ever be fully released.

- **Mutant:** [`6814.sol`](6814.sol)
- **Caught by:** [`rcPeUnreserveClearsTheRowsEarmark`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L251)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6814`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeUnreserveClearsTheRowsEarmark`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -73,7 +73,7 @@
         Holding storage holding_ = holding[scId][asset][tokenId];
 
         uint128 currentReserved = reservedBy[scId][caller][reason][asset][tokenId];
-        require(currentReserved >= value, InsufficientReserve());
+        require(currentReserved > value, InsufficientReserve()); // MUTATION: a key can never hand back everything it placed on hold
 
         uint128 newReservedAmount = currentReserved - value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
```

## PoolEscrow #6815

unreserve requires a release to equal the whole bucket, so part of a hold can no longer be released.

- **Mutant:** [`6815.sol`](6815.sol)
- **Caught by:** [`rcPeUnreserveLeavesTheBucketStillHolding`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L269)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6815`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeUnreserveLeavesTheBucketStillHolding`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -73,7 +73,7 @@
         Holding storage holding_ = holding[scId][asset][tokenId];
 
         uint128 currentReserved = reservedBy[scId][caller][reason][asset][tokenId];
-        require(currentReserved >= value, InsufficientReserve());
+        require(currentReserved == value, InsufficientReserve()); // MUTATION: the release gate insists the bucket be emptied in one call
 
         uint128 newReservedAmount = currentReserved - value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
```

## PoolEscrow #6816

unreserve zeroes the row's reserved total instead of lowering it, so other parties' holds drop out of it.

- **Mutant:** [`6816.sol`](6816.sol)
- **Caught by:** [`rcPeReleasingOneBucketLeavesTheOtherHeld`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L288)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6816`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeReleasingOneBucketLeavesTheOtherHeld`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -77,7 +77,7 @@
 
         uint128 newReservedAmount = currentReserved - value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved -= value;
+        holding_.reserved = 0; // MUTATION: the release clears the row's aggregate earmark outright
 
         emit DecreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #6817

rely refuses any account not already a ward, so no new account can ever be granted a seat.

- **Mutant:** [`6817.sol`](6817.sol)
- **Caught by:** [`rcPeFreshlyReliedAccountBooksADeposit`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L380)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6817`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeFreshlyReliedAccountBooksADeposit`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -23,6 +23,7 @@
 
     /// @inheritdoc IAuth
     function rely(address user) public auth {
+        require(wards[user] == 1, NotAuthorized()); // MUTATION: the roll only reaffirms a seat an account already holds
         wards[user] = 1;
         emit Rely(user);
     }
```

## PoolEscrow #6818

deny refuses to strip any seat but the caller's own, so a ward can no longer remove another account from the roll.

- **Mutant:** [`6818.sol`](6818.sol)
- **Caught by:** [`rcPeDenyRevokesAnotherWard`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L364)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6818`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeDenyRevokesAnotherWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,6 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
+        require(user == msg.sender, NotAuthorized()); // MUTATION: only a ward's own seat can be stripped
         wards[user] = 0;
         emit Deny(user);
     }
```

## PoolEscrow #6820

unreserve runs without its ward gate, so an account the escrow never relied releases a hold it never placed.

- **Mutant:** [`6820.sol`](6820.sol)
- **Caught by:** [`rvPeUnreserveRefusesANonWardOrAShortBucket`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6820`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeUnreserveRefusesANonWardOrAShortBucket`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -68,8 +68,8 @@
     /// @inheritdoc IEscrow
     function unreserve(ShareClassId scId, address asset, uint256 tokenId, uint128 value, address caller, bytes32 reason)
         external
-        auth
-    {
+       
+    { // MUTATION: the ward gate is gone
         Holding storage holding_ = holding[scId][asset][tokenId];
 
         uint128 currentReserved = reservedBy[scId][caller][reason][asset][tokenId];
```

## PoolEscrow #6821

deny runs without the ward gate, so an account holding no seat strips a ward of its permissions.

- **Mutant:** [`6821.sol`](6821.sol)
- **Caught by:** [`rvPeDenyRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L86)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6821`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeDenyRefusesANonWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -28,7 +28,7 @@
     }
 
     /// @inheritdoc IAuth
-    function deny(address user) public auth {
+    function deny(address user) public { // MUTATION: the ward gate is gone
         wards[user] = 0;
         emit Deny(user);
     }
```

## PoolEscrow #6822

the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.

- **Mutant:** [`6822.sol`](6822.sol)
- **Caught by:** [`rvPeDepositRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L4) · [`rvPeReserveRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L39) · [`rvPeRelyRefusesANonWard`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L72)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 6822`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeDepositRefusesANonWard rvPeReserveRefusesANonWard rvPeRelyRefusesANonWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -17,7 +17,7 @@
 
     /// @dev Check if the msg.sender has permissions
     modifier auth() {
-        require(wards[msg.sender] == 1, NotAuthorized());
+        // MUTATION: the shared ward gate no longer looks at the caller
         _;
     }
 
```

## PoolEscrow #8106

recoverTokens pays a plain token back to the escrow itself instead of the named receiver, so an ERC20 recovery moves nothing out of custody.

- **Mutant:** [`8106.sol`](8106.sol)
- **Caught by:** [`rcPeRecoverTokensMovesCustodyWithoutTheLedger`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L108)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 8106`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/custody_properties.conf --rule rcPeRecoverTokensMovesCustodyWithoutTheLedger`

```diff
--- a/src/misc/Recoverable.sol
+++ b/src/misc/Recoverable.sol
@@ -16,7 +16,7 @@
         if (token == ETH_ADDRESS) {
             SafeTransferLib.safeTransferETH(receiver, amount);
         } else {
-            SafeTransferLib.safeTransfer(token, receiver, amount);
+            SafeTransferLib.safeTransfer(token, address(this), amount); // MUTATION: the plain token leg pays the escrow itself
         }
     }
 
```

## PoolEscrow #8802

a new deposit entry credits one value to two share classes, so one class's booking also inflates a sibling's holding.

- **Mutant:** [`8802.sol`](8802.sol)
- **Caught by:** [`stPeEscrowRowIsPerShareClass`](../../specs/core/spoke/Escrow/Escrow_multi_share_class_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 8802`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/multi_share_class_properties.conf --rule stPeEscrowRowIsPerShareClass`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -34,6 +34,15 @@
         holding[scId][asset][tokenId].total += value;
 
         emit Deposit(asset, tokenId, poolId, scId, value);
+    }
+
+    /// @notice MUTATION: books one deposit under two share classes at once.
+    function depositSplit(ShareClassId scId, ShareClassId siblingScId, address asset, uint256 tokenId, uint128 value)
+        external
+        auth
+    {
+        holding[scId][asset][tokenId].total += value;
+        holding[siblingScId][asset][tokenId].total += value;
     }
 
     /// @inheritdoc IEscrow
```

## PoolEscrow #8920

withdraw refuses every payout while any amount of the holding is reserved, so a reservation freezes the free balance beside it.

- **Mutant:** [`8920.sol`](8920.sol)
- **Caught by:** [`rvPeWithdrawAlwaysAdmitsAWardWithinTheFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 8920`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeWithdrawAlwaysAdmitsAWardWithinTheFreeBalance`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -42,7 +42,7 @@
         auth
     {
         Holding storage holding_ = holding[scId][asset][tokenId];
-        require(holding_.total >= holding_.reserved, InsufficientBalance(asset, tokenId, value, 0));
+        require(holding_.total >= holding_.reserved && holding_.reserved == 0, InsufficientBalance(asset, tokenId, value, 0)); // MUTATION: any standing hold freezes the payout
 
         uint128 balance = holding_.total - holding_.reserved;
         require(balance >= value, InsufficientBalance(asset, tokenId, value, balance));
```

## PoolEscrow #8953

withdraw runs without its ward gate, so an account the escrow never relied books a payout out of the pool's custody.

- **Mutant:** [`8953.sol`](8953.sol)
- **Caught by:** [`rvPeWithdrawRefusesANonWardOrAPayoutBeyondTheFreeBalance`](../../specs/core/spoke/Escrow/single/Escrow_reverts.spec#L19)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 8953`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reverts.conf --rule rvPeWithdrawRefusesANonWardOrAPayoutBeyondTheFreeBalance`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -38,8 +38,7 @@
 
     /// @inheritdoc IEscrow
     function withdraw(ShareClassId scId, address asset, uint256 tokenId, address receiver, uint128 value)
-        external
-        auth
+        external // MUTATION: the payout gate no longer asks for a ward
     {
         Holding storage holding_ = holding[scId][asset][tokenId];
         require(holding_.total >= holding_.reserved, InsufficientBalance(asset, tokenId, value, 0));
```

## PoolEscrow #9009

a forced ERC20 transfer out of the escrow pays the caller instead of the named receiver, so the caller pockets the tokens.

- **Mutant:** [`9009.sol`](9009.sol)
- **Caught by:** [`hlPeCustodyMoversWriteNoBook`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9009`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/custody_properties.conf --rule hlPeCustodyMoversWriteNoBook`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -88,7 +88,7 @@
             uint256 balance = IERC20(asset).balanceOf(address(this));
             require(balance >= amount, InsufficientBalance(asset, tokenId, amount, balance));
 
-            SafeTransferLib.safeTransfer(asset, receiver, amount);
+            SafeTransferLib.safeTransfer(asset, msg.sender, amount); // MUTATION: the forced transfer pays the caller
         } else {
             uint256 balance = IERC6909(asset).balanceOf(address(this), tokenId);
             require(balance >= amount, InsufficientBalance(asset, tokenId, amount, balance));
```

## PoolEscrow #9018

a deposit is also credited to the asset's plain token row, so one deposit of a tokenised asset raises two holdings.

- **Mutant:** [`9018.sol`](9018.sol)
- **Caught by:** [`stPeACallMovesAtMostOneHoldingRow`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L43)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9018`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule stPeACallMovesAtMostOneHoldingRow`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -31,7 +31,7 @@
 
     /// @inheritdoc IEscrow
     function deposit(ShareClassId scId, address asset, uint256 tokenId, uint128 value) external auth {
-        holding[scId][asset][tokenId].total += value;
+        holding[scId][asset][tokenId].total += value; holding[scId][asset][0].total += value; // MUTATION: the deposit is also credited to the plain token row
 
         emit Deposit(asset, tokenId, poolId, scId, value);
     }
```

## PoolEscrow #9019

releasing a reservation debits the holding's total instead of its reserved amount, so the escrow books a payout nobody made.

- **Mutant:** [`9019.sol`](9019.sol)
- **Caught by:** [`vtPeTotalMovesOnlyOnFlowsAndReservedOnlyOnReservations`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L13)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9019`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule vtPeTotalMovesOnlyOnFlowsAndReservedOnlyOnReservations`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -77,7 +77,7 @@
 
         uint128 newReservedAmount = currentReserved - value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved -= value;
+        holding_.total -= value; // MUTATION: the release debits the total
 
         emit DecreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #9046

reserve raises the reserved total but never writes the key's bucket, so the bucket does not read back the new hold.

- **Mutant:** [`9046.sol`](9046.sol)
- **Caught by:** [`rcPeBucketReadsBackTheHold`](../../specs/core/spoke/Escrow/single/Escrow_reachability.spec#L402)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9046`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/reachability.conf --rule rcPeBucketReadsBackTheHold`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -59,7 +59,7 @@
         Holding storage holding_ = holding[scId][asset][tokenId];
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
-        reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
+        // MUTATION: reserve no longer stores the new hold in the key's bucket
         holding_.reserved += value;
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
```

## PoolEscrow #9047

unreserve sets the row's reserved total to this key's remaining hold, so other keys' holds are silently released.

- **Mutant:** [`9047.sol`](9047.sol)
- **Caught by:** [`hlPeUnreserveMirrorsBucketAndAggregateExactly`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L148)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9047`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule hlPeUnreserveMirrorsBucketAndAggregateExactly`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -77,7 +77,7 @@
 
         uint128 newReservedAmount = currentReserved - value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved -= value;
+        holding_.reserved = newReservedAmount; // MUTATION: the row's reserved total is set to this key's remaining hold
 
         emit DecreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #9390

reserve adds the hold to the caller's ward seat, not the reserved total, so wards change outside rely and deny.

- **Mutant:** [`9390.sol`](9390.sol)
- **Caught by:** [`acPeWardSeatMovesOnlyThroughRelyOrDeny`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L178)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9390`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule acPeWardSeatMovesOnlyThroughRelyOrDeny`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -60,7 +60,7 @@
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved += value;
+        wards[caller] += value; // MUTATION: the hold lands on the caller's ward seat
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #9391

deposit credits the neighbouring tokenId's row instead of its own, so booked custody lands on a row the call never named.

- **Mutant:** [`9391.sol`](9391.sol)
- **Caught by:** [`hlPeDepositMovesExactlyItsOwnRow`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L70)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9391`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule hlPeDepositMovesExactlyItsOwnRow`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -31,7 +31,7 @@
 
     /// @inheritdoc IEscrow
     function deposit(ShareClassId scId, address asset, uint256 tokenId, uint128 value) external auth {
-        holding[scId][asset][tokenId].total += value;
+        holding[scId][asset][tokenId + 1].total += value; // MUTATION: the neighbouring tokenId's row is credited
 
         emit Deposit(asset, tokenId, poolId, scId, value);
     }
```

## PoolEscrow #9392

withdraw debits only half the paid out amount from the row's custody total, so the books keep claiming funds that already left.

- **Mutant:** [`9392.sol`](9392.sol)
- **Caught by:** [`hlPeWithdrawMovesExactlyItsOwnRow`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L95)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9392`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule hlPeWithdrawMovesExactlyItsOwnRow`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -47,7 +47,7 @@
         uint128 balance = holding_.total - holding_.reserved;
         require(balance >= value, InsufficientBalance(asset, tokenId, value, balance));
 
-        holding_.total -= value;
+        holding_.total -= value / 2; // MUTATION: half the payout is debited
         emit Withdraw(asset, tokenId, poolId, scId, receiver, value);
     }
 
```

## PoolEscrow #9393

reserve raises the row's custody total instead of its earmark, so a hold inflates what the escrow claims to hold and caps nothing.

- **Mutant:** [`9393.sol`](9393.sol)
- **Caught by:** [`hlPeReserveMirrorsBucketAndAggregateExactly`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L120)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9393`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule hlPeReserveMirrorsBucketAndAggregateExactly`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -60,7 +60,7 @@
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved += value;
+        holding_.total += value; // MUTATION: the hold is booked on the custody total
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #9395

reserve overwrites the row's earmark with the new hold instead of adding to it, so the aggregate forgets every hold already standing against the row.

- **Mutant:** [`9395.sol`](9395.sol)
- **Caught by:** [`reservedIsTheSumOfEveryBucket`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9395`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule reservedIsTheSumOfEveryBucket`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -60,7 +60,7 @@
 
         uint128 newReservedAmount = reservedBy[scId][caller][reason][asset][tokenId] + value;
         reservedBy[scId][caller][reason][asset][tokenId] = newReservedAmount;
-        holding_.reserved += value;
+        holding_.reserved = value; // MUTATION: the aggregate is overwritten
 
         emit IncreaseReserve(asset, tokenId, poolId, scId, caller, reason, value, newReservedAmount);
     }
```

## PoolEscrow #9396

rely sets the account's seat to 2 instead of 1, so the auth gate never recognises a freshly relied account.

- **Mutant:** [`9396.sol`](9396.sol)
- **Caught by:** [`acPeWardSeatMovesOnlyThroughRelyOrDeny`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L178)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9396`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule acPeWardSeatMovesOnlyThroughRelyOrDeny`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -23,7 +23,7 @@
 
     /// @inheritdoc IAuth
     function rely(address user) public auth {
-        wards[user] = 1;
+        wards[user] = 2; // MUTATION: rely seats the account off the binary roll
         emit Rely(user);
     }
 
```

## PoolEscrow #9397

withdraw checks and debits the next token id's row instead of its own, so a payout drains another holding.

- **Mutant:** [`9397.sol`](9397.sol)
- **Caught by:** [`hlPeWithdrawMovesExactlyItsOwnRow`](../../specs/core/spoke/Escrow/Escrow_unpinned_properties.spec#L95)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9397`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/unpinned_properties.conf --rule hlPeWithdrawMovesExactlyItsOwnRow`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -41,7 +41,7 @@
         external
         auth
     {
-        Holding storage holding_ = holding[scId][asset][tokenId];
+        Holding storage holding_ = holding[scId][asset][tokenId + 1]; // MUTATION: the payout lands on the neighbouring row
         require(holding_.total >= holding_.reserved, InsufficientBalance(asset, tokenId, value, 0));
 
         uint128 balance = holding_.total - holding_.reserved;
```

## PoolEscrow #9580

authTransferTo skips the ERC20 balance check, so a payout beyond the escrow's balance is left to the token to refuse.

- **Mutant:** [`9580.sol`](9580.sol)
- **Caught by:** [`rvPeAuthTransferToRefusesAShortCustody`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L64)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9580`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/custody_properties.conf --rule rvPeAuthTransferToRefusesAShortCustody`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -86,7 +86,7 @@
     function authTransferTo(address asset, uint256 tokenId, address receiver, uint256 amount) external auth {
         if (tokenId == 0) {
             uint256 balance = IERC20(asset).balanceOf(address(this));
-            require(balance >= amount, InsufficientBalance(asset, tokenId, amount, balance));
+            // MUTATION: the ERC20 leg's balance check is removed
 
             SafeTransferLib.safeTransfer(asset, receiver, amount);
         } else {
```

## PoolEscrow #9581

authTransferTo pays out the escrow's whole ERC20 balance instead of the amount asked for, so one forced transfer empties the custody of that token.

- **Mutant:** [`9581.sol`](9581.sol)
- **Caught by:** [`hlPeAuthTransferToMovesExactlyTheAmount`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9581`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/custody_properties.conf --rule hlPeAuthTransferToMovesExactlyTheAmount`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -88,7 +88,7 @@
             uint256 balance = IERC20(asset).balanceOf(address(this));
             require(balance >= amount, InsufficientBalance(asset, tokenId, amount, balance));
 
-            SafeTransferLib.safeTransfer(asset, receiver, amount);
+            SafeTransferLib.safeTransfer(asset, receiver, balance); // MUTATION: the whole balance leaves, not the amount
         } else {
             uint256 balance = IERC6909(asset).balanceOf(address(this), tokenId);
             require(balance >= amount, InsufficientBalance(asset, tokenId, amount, balance));
```

## PoolEscrow #9582

authTransferTo sends a plain ERC20 payout down the ERC6909 path, so a forced transfer of an ERC20 moves none of the escrow's ERC20 custody.

- **Mutant:** [`9582.sol`](9582.sol)
- **Caught by:** [`rcPeAuthTransferToMovesCustodyWithoutTheLedger`](../../specs/core/spoke/Escrow/Escrow_custody_properties.spec#L81)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrow 9582`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Escrow/custody_properties.conf --rule rcPeAuthTransferToMovesCustodyWithoutTheLedger`

```diff
--- a/src/core/spoke/Escrow.sol
+++ b/src/core/spoke/Escrow.sol
@@ -84,7 +84,7 @@
 
     /// @inheritdoc IEscrow
     function authTransferTo(address asset, uint256 tokenId, address receiver, uint256 amount) external auth {
-        if (tokenId == 0) {
+        if (tokenId != 0) { // MUTATION: the ERC20 leg is taken for token ids and skipped for plain tokens
             uint256 balance = IERC20(asset).balanceOf(address(this));
             require(balance >= amount, InsufficientBalance(asset, tokenId, amount, balance));
 
```

