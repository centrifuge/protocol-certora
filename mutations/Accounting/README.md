# Mutations for `Accounting` (`src/core/hub/Accounting.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [602](#accounting-602) | createAccount puts the creation stamp in the debit total, so the account looks uncreated yet carries debits.<br>Caught by: [`absentAccountIsEmpty`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L12) |
| [603](#accounting-603) | createAccount puts the creation stamp in the credit total, so the account looks uncreated yet carries credits.<br>Caught by: [`absentAccountIsEmpty`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L12) |
| [604](#accounting-604) | createAccount stores a zero creation stamp, so the ledger orientation flag is set on an account the ledger still reports as never created.<br>Caught by: [`absentAccountIsEmpty`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L12) |
| [605](#accounting-605) | createAccount no longer rejects the null account id, so the reserved zero account can be brought into existence.<br>Caught by: [`nullAccountNeverCreated`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L18) |
| [606](#accounting-606) | createAccount stamps a new account one second past the block time, so a fresh account reports an update from the future.<br>Caught by: [`lastUpdatedBetweenEnvFloorAndBlock`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L23) |
| [607](#accounting-607) | createAccount stamps a new account with the block number instead of the block time, so its update time is wrong.<br>Caught by: [`lastUpdatedBetweenEnvFloorAndBlock`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L23) |
| [608](#accounting-608) | createAccount inverts the duplicate check, so it re-creates only existing accounts and wipes their totals.<br>Caught by: [`vtAcAccountDebitNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L6) · [`vtAcAccountCreditNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L22) |
| [616](#accounting-616) | lock no longer refuses to close an unbalanced session, so a journal whose posted sides differ is admitted to close.<br>Caught by: [`rvAcLockRevertsIffThePostedSidesDiffer`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L85) |
| [617](#accounting-617) | The journal id counter is read without being incremented, so a pool can carry posted entries while its issue counter is still zero.<br>Caught by: [`postedHistoryImpliesAnIssuedJournalId`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L30) |
| [619](#accounting-619) | addCredit posts nothing to the account's credit total, so a journal pair's credit never lands on the row it names.<br>Caught by: [`hlAcJournalPairCreditsExactlyItsNamedRow`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L39) |
| [621](#accounting-621) | lock accepts a session whose debits merely reach the credits, so an unbalanced journal commits and the pool's books drift apart.<br>Caught by: [`journalDebitsEqualCredits`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L17) |
| [622](#accounting-622) | createAccountPair opens the same account in two pools at once, so one call writes both pools' books.<br>Caught by: [`stAcAccountRowsArePerPool`](../../specs/core/hub/Accounting/Accounting_multi_pool_properties.spec#L6) |
| [623](#accounting-623) | unlockPair reserves a journal id in a second pool while opening a session in the first, so one call advances two pools' journals.<br>Caught by: [`stAcJournalNumberingIsPerPool`](../../specs/core/hub/Accounting/Accounting_multi_pool_properties.spec#L35) |
| [629](#accounting-629) | createAccount no longer refuses an existing account, so a re-creation can flip a used account's orientation.<br>Caught by: [`stAcAccountOrientationIsPermanent`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L71) |
| [4000](#accounting-4000) | createAccount no longer refuses an existing account, so re-creating it resets its debit and credit totals to zero.<br>Caught by: [`vtAcAccountDebitNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L6) · [`vtAcAccountCreditNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L22) |
| [4001](#accounting-4001) | addDebit stamps the row one second before the current block, so a row last touched in this block is backdated by the posting.<br>Caught by: [`vtAcAccountStampNeverRegresses`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L38) |
| [4003](#accounting-4003) | lock accepts debits greater than or equal to credits, so a journal with excess debit still closes.<br>Caught by: [`hlAcSessionClosesOnlyOnEqualPostedValues`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L4) |
| [4004](#accounting-4004) | addDebit overwrites the account's debit total with the posted value instead of adding it, so earlier debits are lost.<br>Caught by: [`hlAcJournalPairDebitsExactlyItsNamedRow`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L22) |
| [4005](#accounting-4005) | addCredit overwrites the account's credit total with the posted value instead of adding it, so earlier credits are lost.<br>Caught by: [`hlAcJournalPairCreditsExactlyItsNamedRow`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L39) |
| [4006](#accounting-4006) | createAccount writes the creation stamp into the debit total, so opening an account moves the pool's recorded books outside any journal.<br>Caught by: [`stAcLedgerMovesOnlyThroughAJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L86) |
| [4008](#accounting-4008) | accountValue returns a debit normal account's gross debit total instead of its net balance, so the value is overstated.<br>Caught by: [`hlAcAccountValueReportsTheRowsNetMagnitude`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L78) |
| [4009](#accounting-4009) | accountValue reads the account's orientation inverted, so a balance on its normal side is reported as negative.<br>Caught by: [`hlAcAccountValueSignsByTheRowsOrientation`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L95) |
| [4010](#accounting-4010) | unlock no longer resets the running debit counter, so a reopened journal starts with the previous journal's debits.<br>Caught by: [`hlAcReopenedJournalStartsFromEmptyPostedSides`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L113) |
| [4012](#accounting-4012) | unlock no longer refuses while a journal is open, so a nested open wipes the running debit and credit totals.<br>Caught by: [`rvAcUnlockRefusesASecondOpenWhileAJournalStands`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L18) |
| [4013](#accounting-4013) | createAccount no longer refuses an existing account, so re-creation zeroes its totals and may flip its orientation.<br>Caught by: [`rvAcCreateAccountRefusesANonWardTheNullIdOrARowThatStands`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L32) |
| [4014](#accounting-4014) | addDebit overwrites the account's debit total instead of adding to it, so earlier posted debits are erased.<br>Caught by: [`vtAcAccountDebitNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L6) |
| [4015](#accounting-4015) | addCredit overwrites the account's credit total instead of adding to it, so earlier posted credits are erased.<br>Caught by: [`vtAcAccountCreditNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L22) |
| [4016](#accounting-4016) | lock accepts debits at least equal to credits, so a journal with excess debit closes unbalanced.<br>Caught by: [`rvAcLockRevertsIffThePostedSidesDiffer`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L85) |
| [4017](#accounting-4017) | addJournal skips the first debit leg, so a lone debit posts nothing and succeeds with no journal open.<br>Caught by: [`rvAcAddJournalOffSessionRefusesANonWardOrAnyEntry`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L106) |
| [4018](#accounting-4018) | accountValue no longer refuses an account the ledger never opened, so a missing row reads back as a settled one at zero.<br>Caught by: [`rvAcAccountValueRefusesARowTheLedgerNeverOpened`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L122) |
| [4020](#accounting-4020) | addDebit loses its ward gate, so a caller the ledger never authorised can charge an account through a journal a ward opened.<br>Caught by: [`rvAcAddDebitRefusesAnOutsiderInsideAnOpenJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L137) |
| [4021](#accounting-4021) | addCredit loses its ward gate, so a caller the ledger never authorised can credit an account through a journal a ward opened.<br>Caught by: [`rvAcAddCreditRefusesAnOutsiderInsideAnOpenJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L157) |
| [4022](#accounting-4022) | lock loses its ward gate, so an outsider can seal a journal a ward opened and strand the entries that call still has to post.<br>Caught by: [`rvAcLockRefusesAnOutsiderOnAnOpenJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L177) |
| [4023](#accounting-4023) | createAccount loses its ward gate, so any caller can open an account in any pool and set its orientation.<br>Caught by: [`acAcDebitHistoryMovesOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L4) · [`acAcCreditHistoryMovesOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L22) · [`acAcAccountStampMovesOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L40) · [`acAcAccountOpensOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L58) · [`acAcAccountOrientationIsSetOnlyByAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L74) |
| [4024](#accounting-4024) | unlock loses its ward gate, so any caller can leave the ledger open for posting and burn a number of the pool's journal sequence.<br>Caught by: [`acAcJournalNumberingAdvancesOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L107) · [`acAcSessionIsLeftOpenOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L125) |
| [4025](#accounting-4025) | claimWard is an entry point shipped without the ward gate, so any caller can seat itself in the ledger's own permission set.<br>Caught by: [`acAcPermissionsMoveOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L91) |
| [4027](#accounting-4027) | unlock mints a fresh journal id on every open, so a pool's journal cannot reopen inside one transaction under the id it already minted.<br>Caught by: [`hlAcSecondJournalOfAPoolReusesItsJournalId`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L56) |
| [4028](#accounting-4028) | createAccount stores a zero creation stamp, so the account looks uncreated and nothing can post to it.<br>Caught by: [`rcAcCreateDebitNormalAccountIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L214) · [`rcAcCreateCreditNormalAccountIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L233) · [`rcAcSecondRowOpensBesideALiveOneIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L252) · [`rcAcFirstRowOfAnEmptyChartIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L274) · [`rcAcRowsCreatedAndJournalledInOneTransactionIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L366) · [`rcAcFreshRowReadsBackThePostedValueIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L388) · [`rcAcDebitNormalRowReportsANegativeValueIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L405) · [`rcAcRowDebitedAndCreditedAlikeReadsZeroIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L422) |
| [4029](#accounting-4029) | addDebit never raises the session's running debit total, so a journal with a nonzero credit can never close.<br>Caught by: [`rcAcBalancedPairPostsAndClosesIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L43) · [`rcAcDebitFillsARowToTheCeilingIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L125) · [`rcAcCeilingPairPostsAndClosesIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L159) · [`rcAcJournalBatchReachesTheWholeChartIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L293) · [`rcAcOpenSessionReportsItsRunningSidesIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L439) |
| [4030](#accounting-4030) | addCredit never accumulates into the account row, so no credit reaches a row's credit side.<br>Caught by: [`rcAcCreditFillsARowToTheCeilingIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L142) · [`rcAcSaturatedDebitRowStillTakesACreditIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L182) |
| [4031](#accounting-4031) | addCredit never raises the session's running credit total, so a journal with nonzero debits can never close.<br>Caught by: [`rcAcTwoDebitsCloseAgainstOneCreditIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L67) |
| [4034](#accounting-4034) | addDebit never adds to the account's debit total, so a debit can never turn a credit heavy row debit heavy.<br>Caught by: [`rcAcDebitOvertakesACreditHeavyRowIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L198) |
| [4302](#accounting-4302) | addDebit posts nothing to the account's debit total, so a journal pair's debit never lands on the row it names.<br>Caught by: [`hlAcJournalPairDebitsExactlyItsNamedRow`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L22) |
| [7100](#accounting-7100) | rely refuses an address that holds no ward, so a fresh ward can never be granted.<br>Caught by: [`rcAcAuthorityGrantRoundTripIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L455) |
| [7101](#accounting-7101) | deny refuses a caller naming its own address, so a ward can never revoke its own rights.<br>Caught by: [`rcAcWardRevokesItselfIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L474) |
| [7102](#accounting-7102) | lock refuses exactly the journal that balances, so no balanced pair ever reaches the books.<br>Caught by: [`rcAcPassingJournalPairOnABalancedPairIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L488) |
| [7103](#accounting-7103) | addDebit loses the gate that asks whether the row was ever opened, so a charge lands on an account the ledger never created.<br>Caught by: [`rvAcAddDebitRefusesARowTheLedgerNeverOpened`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L51) |
| [7104](#accounting-7104) | addCredit loses the gate that asks whether the row was ever opened, so a credit lands on an account the ledger never created.<br>Caught by: [`rvAcAddCreditRefusesARowTheLedgerNeverOpened`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L68) |
| [7105](#accounting-7105) | accountValue reads its existence test backwards, so the books answer only for rows that were never opened.<br>Caught by: [`rvAcAccountValueAlwaysAnswersForARowThatStands`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L196) |
| [7106](#accounting-7106) | the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.<br>Caught by: [`rvAcUnlockRefusesANonWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L4) |
| [7107](#accounting-7107) | unlock rewinds the pool's journal counter instead of advancing it, so a number already spent is handed out a second time.<br>Caught by: [`vtAcJournalCounterNeverRewinds`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L54) |
| [8600](#accounting-8600) | addDebit no longer checks that a journal is open, so a ward can post a debit to the books while the ledger is closed.<br>Caught by: [`rvAcAddDebitIsRefusedOffSession`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L211) |
| [8601](#accounting-8601) | addCredit no longer checks that a journal is open, so a ward can post a credit to the books while the ledger is closed.<br>Caught by: [`rvAcAddCreditIsRefusedOffSession`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L222) |
| [8602](#accounting-8602) | lock no longer checks that a journal is open, so a close is admitted and announced for a journal that was never opened.<br>Caught by: [`rvAcLockIsRefusedOffSession`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L233) |
| [8603](#accounting-8603) | unlock no longer refuses the null pool, so a journal opens on the id that marks a closed ledger.<br>Caught by: [`rvAcUnlockRefusesTheNullPool`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L244) |
| [8604](#accounting-8604) | a journal id is minted from the pool's counter alone, without the pool in its high half, so two pools draw colliding ids.<br>Caught by: [`hlAcMintedJournalIdCarriesItsPool`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L131) |
| [8605](#accounting-8605) | unlock opens the session on a fixed pool instead of the pool it names, so the entries that follow land in another pool's books.<br>Caught by: [`hlAcUnlockOpensTheSessionOnTheNamedPool`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L144) |
| [8606](#accounting-8606) | the journal id read drops the pool from its key, so every opening mints a new id yet reports journal id zero.<br>Caught by: [`hlAcSecondPoolOfATransactionOpensUnderItsOwnId`](../../specs/core/hub/Accounting/Accounting_multi_pool_properties.spec#L69) |
| [9001](#accounting-9001) | opening an account rewinds the pool's journal numbering to zero, so ids already handed out are handed out again.<br>Caught by: [`issuedJournalIdsLieAtOrBelowTheHighWaterMark`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L36) |
| [9003](#accounting-9003) | lock also admits a close with no journal open while an earlier journal's debit total lingers, so an unopened session closes.<br>Caught by: [`rvAcLockIsRefusedAfterAClosedJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L257) |
| [9004](#accounting-9004) | setAccountMetadata also restamps the account's last update time, so relabelling an account makes it read as freshly posted to.<br>Caught by: [`hlAcSetAccountMetadataWritesOnlyItsAccountsMetadata`](../../specs/core/hub/Accounting/Accounting_metadata_properties.spec#L6) |
| [9041](#accounting-9041) | the journal id counter is never advanced, so every new journal reuses the pool's last id.<br>Caught by: [`rcAcUnlockOpensAJournalIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L4) · [`rcAcEmptyJournalOverAnUntouchedLedgerIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L22) · [`rcAcEmptyJournalBatchIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L320) |
| [9042](#accounting-9042) | addCredit no longer refreshes the row's update time, so a credit leaves the account's old timestamp in place.<br>Caught by: [`rcAcZeroValueCreditRestampsTheRowIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L106) |
| [9043](#accounting-9043) | addDebit no longer refreshes the row's update time, so a debit leaves the account's old timestamp in place.<br>Caught by: [`rcAcZeroValueDebitRestampsTheRowIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L87) · [`rcAcZeroValueJournalBatchIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L343) |
| [9044](#accounting-9044) | each journal id takes the counter before it advances, so a new journal reuses the id its pool issued last.<br>Caught by: [`stAcMintedJournalIdWasNeverIssuedBefore`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L105) |
| [9045](#accounting-9045) | the journal id is written under a key that omits the pool, so one pool's open overwrites another pool's id.<br>Caught by: [`stAcAPoolsJournalIdIsFixedForTheTransaction`](../../specs/core/hub/Accounting/Accounting_multi_pool_properties.spec#L52) |

## Accounting #602

createAccount puts the creation stamp in the debit total, so the account looks uncreated yet carries debits.

- **Mutant:** [`602.sol`](602.sol)
- **Caught by:** [`absentAccountIsEmpty`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L12)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 602`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_valid_state.conf --rule absentAccountIsEmpty`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -71,7 +71,7 @@
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
-        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[poolId][account] = Account(uint64(block.timestamp), 0, isDebitNormal, 0, ""); // MUTATION: stamp transposed into the debit total
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Accounting #603

createAccount puts the creation stamp in the credit total, so the account looks uncreated yet carries credits.

- **Mutant:** [`603.sol`](603.sol)
- **Caught by:** [`absentAccountIsEmpty`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L12)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 603`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_valid_state.conf --rule absentAccountIsEmpty`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -71,7 +71,7 @@
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
-        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[poolId][account] = Account(0, uint64(block.timestamp), isDebitNormal, 0, ""); // MUTATION: stamp transposed into the credit total
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Accounting #604

createAccount stores a zero creation stamp, so the ledger orientation flag is set on an account the ledger still reports as never created.

- **Mutant:** [`604.sol`](604.sol)
- **Caught by:** [`absentAccountIsEmpty`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L12)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 604`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_valid_state.conf --rule absentAccountIsEmpty`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -71,7 +71,7 @@
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
-        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[poolId][account] = Account(0, 0, isDebitNormal, 0, ""); // MUTATION: creation stamp dropped to zero
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Accounting #605

createAccount no longer rejects the null account id, so the reserved zero account can be brought into existence.

- **Mutant:** [`605.sol`](605.sol)
- **Caught by:** [`nullAccountNeverCreated`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L18)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 605`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_valid_state.conf --rule nullAccountNeverCreated`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -69,7 +69,7 @@
 
     /// @inheritdoc IAccounting
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
-        require(!account.isNull(), InvalidAccountId());
+        // MUTATION: removed the null account id check
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
         accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
         emit CreateAccount(poolId, account, isDebitNormal);
```

## Accounting #606

createAccount stamps a new account one second past the block time, so a fresh account reports an update from the future.

- **Mutant:** [`606.sol`](606.sol)
- **Caught by:** [`lastUpdatedBetweenEnvFloorAndBlock`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 606`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_valid_state.conf --rule lastUpdatedBetweenEnvFloorAndBlock`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -71,7 +71,7 @@
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
-        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp) + 1, ""); // MUTATION: stamp one past the block time
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Accounting #607

createAccount stamps a new account with the block number instead of the block time, so its update time is wrong.

- **Mutant:** [`607.sol`](607.sol)
- **Caught by:** [`lastUpdatedBetweenEnvFloorAndBlock`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 607`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_valid_state.conf --rule lastUpdatedBetweenEnvFloorAndBlock`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -71,7 +71,7 @@
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
-        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.number), ""); // MUTATION: stamped with the block number
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Accounting #608

createAccount inverts the duplicate check, so it re-creates only existing accounts and wipes their totals.

- **Mutant:** [`608.sol`](608.sol)
- **Caught by:** [`vtAcAccountDebitNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L6) · [`vtAcAccountCreditNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 608`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_transitions.conf --rule vtAcAccountDebitNeverDecreases vtAcAccountCreditNeverDecreases`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -70,7 +70,7 @@
     /// @inheritdoc IAccounting
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
-        require(accounts[poolId][account].lastUpdated == 0, AccountExists());
+        require(accounts[poolId][account].lastUpdated != 0, AccountExists()); // MUTATION: existence check inverted
         accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
         emit CreateAccount(poolId, account, isDebitNormal);
     }
```

## Accounting #616

lock no longer refuses to close an unbalanced session, so a journal whose posted sides differ is admitted to close.

- **Mutant:** [`616.sol`](616.sol)
- **Caught by:** [`rvAcLockRevertsIffThePostedSidesDiffer`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L85)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 616`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcLockRevertsIffThePostedSidesDiffer`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -57,7 +57,7 @@
     /// @inheritdoc IAccounting
     function lock() external auth {
         require(!_currentPoolId.isNull(), AccountingLocked());
-        require(debited == credited, Unbalanced());
+        // MUTATION: removed the balance check on lock
 
         emit EndJournalId(_currentPoolId, TransientJournal.journalId(_currentPoolId));
         _currentPoolId = PoolId.wrap(0);
```

## Accounting #617

The journal id counter is read without being incremented, so a pool can carry posted entries while its issue counter is still zero.

- **Mutant:** [`617.sol`](617.sol)
- **Caught by:** [`postedHistoryImpliesAnIssuedJournalId`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L30)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 617`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_valid_state.conf --rule postedHistoryImpliesAnIssuedJournalId`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -155,6 +155,6 @@
     }
 
     function _generateJournalId(PoolId poolId) internal returns (uint256) {
-        return uint256((uint256(poolId.raw()) << 128) | ++_poolJournalIdCounter[poolId]);
+        return uint256((uint256(poolId.raw()) << 128) | _poolJournalIdCounter[poolId]); // MUTATION: counter never advances
     }
 }
```

## Accounting #619

addCredit posts nothing to the account's credit total, so a journal pair's credit never lands on the row it names.

- **Mutant:** [`619.sol`](619.sol)
- **Caught by:** [`hlAcJournalPairCreditsExactlyItsNamedRow`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L39)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 619`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcJournalPairCreditsExactlyItsNamedRow`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -106,7 +106,7 @@
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        acc.totalCredit += value;
+        // MUTATION: removed the ledger credit posting
         credited += value;
         acc.lastUpdated = uint64(block.timestamp);
         emit Credit(_currentPoolId, account, value);
```

## Accounting #621

lock accepts a session whose debits merely reach the credits, so an unbalanced journal commits and the pool's books drift apart.

- **Mutant:** [`621.sol`](621.sol)
- **Caught by:** [`journalDebitsEqualCredits`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L17)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 621`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule journalDebitsEqualCredits`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -57,7 +57,7 @@
     /// @inheritdoc IAccounting
     function lock() external auth {
         require(!_currentPoolId.isNull(), AccountingLocked());
-        require(debited == credited, Unbalanced());
+        require(debited >= credited, Unbalanced()); // MUTATION: balance check weakened to at-least
 
         emit EndJournalId(_currentPoolId, TransientJournal.journalId(_currentPoolId));
         _currentPoolId = PoolId.wrap(0);
```

## Accounting #622

createAccountPair opens the same account in two pools at once, so one call writes both pools' books.

- **Mutant:** [`622.sol`](622.sol)
- **Caught by:** [`stAcAccountRowsArePerPool`](../../specs/core/hub/Accounting/Accounting_multi_pool_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 622`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/multi_pool_properties.conf --rule stAcAccountRowsArePerPool`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -72,6 +72,17 @@
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
         accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        emit CreateAccount(poolId, account, isDebitNormal);
+    }
+
+    /// @notice MUTATION: opens the same account in a second pool, so one call writes two pools' books.
+    function createAccountPair(PoolId poolId, PoolId mirrorPoolId, AccountId account, bool isDebitNormal)
+        external
+        auth
+    {
+        require(!account.isNull(), InvalidAccountId());
+        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[mirrorPoolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Accounting #623

unlockPair reserves a journal id in a second pool while opening a session in the first, so one call advances two pools' journals.

- **Mutant:** [`623.sol`](623.sol)
- **Caught by:** [`stAcJournalNumberingIsPerPool`](../../specs/core/hub/Accounting/Accounting_multi_pool_properties.spec#L35)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 623`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/multi_pool_properties.conf --rule stAcJournalNumberingIsPerPool`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -51,6 +51,19 @@
         if (TransientJournal.journalId(poolId) == 0) {
             TransientJournal.setJournalId(poolId, _generateJournalId(poolId));
         }
+        emit StartJournalId(poolId, TransientJournal.journalId(poolId));
+    }
+
+    /// @notice MUTATION: reserves a journal id in a second pool as well, so one call advances two pools' journals.
+    function unlockPair(PoolId poolId, PoolId mirrorPoolId) external auth {
+        require(PoolId.unwrap(_currentPoolId) == 0, AccountingAlreadyUnlocked());
+        require(!poolId.isNull() && !mirrorPoolId.isNull(), InvalidPoolId());
+        debited = 0;
+        credited = 0;
+        _currentPoolId = poolId;
+
+        TransientJournal.setJournalId(poolId, _generateJournalId(poolId));
+        TransientJournal.setJournalId(mirrorPoolId, _generateJournalId(mirrorPoolId));
         emit StartJournalId(poolId, TransientJournal.journalId(poolId));
     }
 
```

## Accounting #629

createAccount no longer refuses an existing account, so a re-creation can flip a used account's orientation.

- **Mutant:** [`629.sol`](629.sol)
- **Caught by:** [`stAcAccountOrientationIsPermanent`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L71)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 629`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_transitions.conf --rule stAcAccountOrientationIsPermanent`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -70,7 +70,7 @@
     /// @inheritdoc IAccounting
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
-        require(accounts[poolId][account].lastUpdated == 0, AccountExists());
+        // MUTATION: removed the duplicate account check
         accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
         emit CreateAccount(poolId, account, isDebitNormal);
     }
```

## Accounting #4000

createAccount no longer refuses an existing account, so re-creating it resets its debit and credit totals to zero.

- **Mutant:** [`4000.sol`](4000.sol)
- **Caught by:** [`vtAcAccountDebitNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L6) · [`vtAcAccountCreditNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4000`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_transitions.conf --rule vtAcAccountDebitNeverDecreases vtAcAccountCreditNeverDecreases`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -70,7 +70,7 @@
     /// @inheritdoc IAccounting
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
-        require(accounts[poolId][account].lastUpdated == 0, AccountExists());
+        // MUTATION: removed the duplicate account check
         accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
         emit CreateAccount(poolId, account, isDebitNormal);
     }
```

## Accounting #4001

addDebit stamps the row one second before the current block, so a row last touched in this block is backdated by the posting.

- **Mutant:** [`4001.sol`](4001.sol)
- **Caught by:** [`vtAcAccountStampNeverRegresses`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4001`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_transitions.conf --rule vtAcAccountStampNeverRegresses`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -95,7 +95,7 @@
 
         acc.totalDebit += value;
         debited += value;
-        acc.lastUpdated = uint64(block.timestamp);
+        acc.lastUpdated = uint64(block.timestamp) - 1; // MUTATION: the row is stamped one second before the block
         emit Debit(_currentPoolId, account, value);
     }
 
```

## Accounting #4003

lock accepts debits greater than or equal to credits, so a journal with excess debit still closes.

- **Mutant:** [`4003.sol`](4003.sol)
- **Caught by:** [`hlAcSessionClosesOnlyOnEqualPostedValues`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4003`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcSessionClosesOnlyOnEqualPostedValues`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -57,7 +57,7 @@
     /// @inheritdoc IAccounting
     function lock() external auth {
         require(!_currentPoolId.isNull(), AccountingLocked());
-        require(debited == credited, Unbalanced());
+        require(debited >= credited, Unbalanced()); // MUTATION: balance check weakened to at least
 
         emit EndJournalId(_currentPoolId, TransientJournal.journalId(_currentPoolId));
         _currentPoolId = PoolId.wrap(0);
```

## Accounting #4004

addDebit overwrites the account's debit total with the posted value instead of adding it, so earlier debits are lost.

- **Mutant:** [`4004.sol`](4004.sol)
- **Caught by:** [`hlAcJournalPairDebitsExactlyItsNamedRow`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4004`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcJournalPairDebitsExactlyItsNamedRow`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -93,7 +93,7 @@
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        acc.totalDebit += value;
+        acc.totalDebit = value; // MUTATION: the row's debit total is overwritten instead of accumulated
         debited += value;
         acc.lastUpdated = uint64(block.timestamp);
         emit Debit(_currentPoolId, account, value);
```

## Accounting #4005

addCredit overwrites the account's credit total with the posted value instead of adding it, so earlier credits are lost.

- **Mutant:** [`4005.sol`](4005.sol)
- **Caught by:** [`hlAcJournalPairCreditsExactlyItsNamedRow`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L39)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4005`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcJournalPairCreditsExactlyItsNamedRow`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -106,7 +106,7 @@
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        acc.totalCredit += value;
+        acc.totalCredit = value; // MUTATION: the row's credit total is overwritten instead of accumulated
         credited += value;
         acc.lastUpdated = uint64(block.timestamp);
         emit Credit(_currentPoolId, account, value);
```

## Accounting #4006

createAccount writes the creation stamp into the debit total, so opening an account moves the pool's recorded books outside any journal.

- **Mutant:** [`4006.sol`](4006.sol)
- **Caught by:** [`stAcLedgerMovesOnlyThroughAJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L86)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4006`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_transitions.conf --rule stAcLedgerMovesOnlyThroughAJournal`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -71,7 +71,7 @@
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
-        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[poolId][account] = Account(uint64(block.timestamp), 0, isDebitNormal, 0, ""); // MUTATION: stamp transposed into the debit total
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Accounting #4008

accountValue returns a debit normal account's gross debit total instead of its net balance, so the value is overstated.

- **Mutant:** [`4008.sol`](4008.sol)
- **Caught by:** [`hlAcAccountValueReportsTheRowsNetMagnitude`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L78)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4008`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcAccountValueReportsTheRowsNetMagnitude`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -135,7 +135,7 @@
         if (acc.isDebitNormal) {
             // For debit-normal accounts: Value = Total Debit - Total Credit
             if (acc.totalDebit >= acc.totalCredit) {
-                return (true, acc.totalDebit - acc.totalCredit);
+                return (true, acc.totalDebit); // MUTATION: the gross debit total is reported in place of the net position
             } else {
                 return (false, acc.totalCredit - acc.totalDebit);
             }
```

## Accounting #4009

accountValue reads the account's orientation inverted, so a balance on its normal side is reported as negative.

- **Mutant:** [`4009.sol`](4009.sol)
- **Caught by:** [`hlAcAccountValueSignsByTheRowsOrientation`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L95)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4009`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcAccountValueSignsByTheRowsOrientation`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -132,7 +132,7 @@
         Account storage acc = accounts[poolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        if (acc.isDebitNormal) {
+        if (!acc.isDebitNormal) { // MUTATION: the row's orientation is read inverted
             // For debit-normal accounts: Value = Total Debit - Total Credit
             if (acc.totalDebit >= acc.totalCredit) {
                 return (true, acc.totalDebit - acc.totalCredit);
```

## Accounting #4010

unlock no longer resets the running debit counter, so a reopened journal starts with the previous journal's debits.

- **Mutant:** [`4010.sol`](4010.sol)
- **Caught by:** [`hlAcReopenedJournalStartsFromEmptyPostedSides`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L113)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4010`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcReopenedJournalStartsFromEmptyPostedSides`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -44,7 +44,7 @@
     function unlock(PoolId poolId) external auth {
         require(PoolId.unwrap(_currentPoolId) == 0, AccountingAlreadyUnlocked());
         require(!poolId.isNull(), InvalidPoolId());
-        debited = 0;
+        // MUTATION: the running debit counter is no longer cleared on open
         credited = 0;
         _currentPoolId = poolId;
 
```

## Accounting #4012

unlock no longer refuses while a journal is open, so a nested open wipes the running debit and credit totals.

- **Mutant:** [`4012.sol`](4012.sol)
- **Caught by:** [`rvAcUnlockRefusesASecondOpenWhileAJournalStands`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L18)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4012`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcUnlockRefusesASecondOpenWhileAJournalStands`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -42,7 +42,7 @@
 
     /// @inheritdoc IAccounting
     function unlock(PoolId poolId) external auth {
-        require(PoolId.unwrap(_currentPoolId) == 0, AccountingAlreadyUnlocked());
+        // MUTATION: removed the already unlocked check
         require(!poolId.isNull(), InvalidPoolId());
         debited = 0;
         credited = 0;
```

## Accounting #4013

createAccount no longer refuses an existing account, so re-creation zeroes its totals and may flip its orientation.

- **Mutant:** [`4013.sol`](4013.sol)
- **Caught by:** [`rvAcCreateAccountRefusesANonWardTheNullIdOrARowThatStands`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L32)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4013`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcCreateAccountRefusesANonWardTheNullIdOrARowThatStands`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -70,7 +70,7 @@
     /// @inheritdoc IAccounting
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
-        require(accounts[poolId][account].lastUpdated == 0, AccountExists());
+        // MUTATION: removed the duplicate account check
         accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
         emit CreateAccount(poolId, account, isDebitNormal);
     }
```

## Accounting #4014

addDebit overwrites the account's debit total instead of adding to it, so earlier posted debits are erased.

- **Mutant:** [`4014.sol`](4014.sol)
- **Caught by:** [`vtAcAccountDebitNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4014`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_transitions.conf --rule vtAcAccountDebitNeverDecreases`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -93,7 +93,7 @@
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        acc.totalDebit += value;
+        acc.totalDebit = value; // MUTATION: the row's debit total is overwritten instead of accumulated
         debited += value;
         acc.lastUpdated = uint64(block.timestamp);
         emit Debit(_currentPoolId, account, value);
```

## Accounting #4015

addCredit overwrites the account's credit total instead of adding to it, so earlier posted credits are erased.

- **Mutant:** [`4015.sol`](4015.sol)
- **Caught by:** [`vtAcAccountCreditNeverDecreases`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4015`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_transitions.conf --rule vtAcAccountCreditNeverDecreases`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -106,7 +106,7 @@
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        acc.totalCredit += value;
+        acc.totalCredit = value; // MUTATION: the row's credit total is overwritten instead of accumulated
         credited += value;
         acc.lastUpdated = uint64(block.timestamp);
         emit Credit(_currentPoolId, account, value);
```

## Accounting #4016

lock accepts debits at least equal to credits, so a journal with excess debit closes unbalanced.

- **Mutant:** [`4016.sol`](4016.sol)
- **Caught by:** [`rvAcLockRevertsIffThePostedSidesDiffer`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L85)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4016`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcLockRevertsIffThePostedSidesDiffer`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -57,7 +57,7 @@
     /// @inheritdoc IAccounting
     function lock() external auth {
         require(!_currentPoolId.isNull(), AccountingLocked());
-        require(debited == credited, Unbalanced());
+        require(debited >= credited, Unbalanced()); // MUTATION: balance check weakened to at least
 
         emit EndJournalId(_currentPoolId, TransientJournal.journalId(_currentPoolId));
         _currentPoolId = PoolId.wrap(0);
```

## Accounting #4017

addJournal skips the first debit leg, so a lone debit posts nothing and succeeds with no journal open.

- **Mutant:** [`4017.sol`](4017.sol)
- **Caught by:** [`rvAcAddJournalOffSessionRefusesANonWardOrAnyEntry`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L106)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4017`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcAddJournalOffSessionRefusesANonWardOrAnyEntry`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -114,7 +114,7 @@
 
     /// @inheritdoc IAccounting
     function addJournal(JournalEntry[] memory debits, JournalEntry[] memory credits) external auth {
-        for (uint256 i; i < debits.length; i++) {
+        for (uint256 i = 1; i < debits.length; i++) { // MUTATION: the debit leg loop starts at the second entry
             addDebit(debits[i].accountId, debits[i].value);
         }
 
```

## Accounting #4018

accountValue no longer refuses an account the ledger never opened, so a missing row reads back as a settled one at zero.

- **Mutant:** [`4018.sol`](4018.sol)
- **Caught by:** [`rvAcAccountValueRefusesARowTheLedgerNeverOpened`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L122)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4018`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcAccountValueRefusesARowTheLedgerNeverOpened`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -130,7 +130,7 @@
     /// @inheritdoc IAccounting
     function accountValue(PoolId poolId, AccountId account) external view returns (bool, /* isPositive */ uint128) {
         Account storage acc = accounts[poolId][account];
-        require(acc.lastUpdated != 0, AccountDoesNotExist());
+        // MUTATION: removed the account existence check on the value read
 
         if (acc.isDebitNormal) {
             // For debit-normal accounts: Value = Total Debit - Total Credit
```

## Accounting #4020

addDebit loses its ward gate, so a caller the ledger never authorised can charge an account through a journal a ward opened.

- **Mutant:** [`4020.sol`](4020.sol)
- **Caught by:** [`rvAcAddDebitRefusesAnOutsiderInsideAnOpenJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L137)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4020`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcAddDebitRefusesAnOutsiderInsideAnOpenJournal`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -87,7 +87,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IAccounting
-    function addDebit(AccountId account, uint128 value) public auth {
+    function addDebit(AccountId account, uint128 value) public { // MUTATION: the ward gate is gone
         require(!_currentPoolId.isNull(), AccountingLocked());
 
         Account storage acc = accounts[_currentPoolId][account];
```

## Accounting #4021

addCredit loses its ward gate, so a caller the ledger never authorised can credit an account through a journal a ward opened.

- **Mutant:** [`4021.sol`](4021.sol)
- **Caught by:** [`rvAcAddCreditRefusesAnOutsiderInsideAnOpenJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L157)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4021`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcAddCreditRefusesAnOutsiderInsideAnOpenJournal`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -100,7 +100,7 @@
     }
 
     /// @inheritdoc IAccounting
-    function addCredit(AccountId account, uint128 value) public auth {
+    function addCredit(AccountId account, uint128 value) public { // MUTATION: the ward gate is gone
         require(!_currentPoolId.isNull(), AccountingLocked());
 
         Account storage acc = accounts[_currentPoolId][account];
```

## Accounting #4022

lock loses its ward gate, so an outsider can seal a journal a ward opened and strand the entries that call still has to post.

- **Mutant:** [`4022.sol`](4022.sol)
- **Caught by:** [`rvAcLockRefusesAnOutsiderOnAnOpenJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L177)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4022`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcLockRefusesAnOutsiderOnAnOpenJournal`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -55,7 +55,7 @@
     }
 
     /// @inheritdoc IAccounting
-    function lock() external auth {
+    function lock() external { // MUTATION: the ward gate is gone
         require(!_currentPoolId.isNull(), AccountingLocked());
         require(debited == credited, Unbalanced());
 
```

## Accounting #4023

createAccount loses its ward gate, so any caller can open an account in any pool and set its orientation.

- **Mutant:** [`4023.sol`](4023.sol)
- **Caught by:** [`acAcDebitHistoryMovesOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L4) · [`acAcCreditHistoryMovesOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L22) · [`acAcAccountStampMovesOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L40) · [`acAcAccountOpensOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L58) · [`acAcAccountOrientationIsSetOnlyByAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L74)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4023`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_access_control.conf --rule acAcDebitHistoryMovesOnlyForAWard acAcCreditHistoryMovesOnlyForAWard acAcAccountStampMovesOnlyForAWard acAcAccountOpensOnlyForAWard acAcAccountOrientationIsSetOnlyByAWard`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -68,7 +68,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IAccounting
-    function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
+    function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external { // MUTATION: the ward gate is gone
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
         accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
```

## Accounting #4024

unlock loses its ward gate, so any caller can leave the ledger open for posting and burn a number of the pool's journal sequence.

- **Mutant:** [`4024.sol`](4024.sol)
- **Caught by:** [`acAcJournalNumberingAdvancesOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L107) · [`acAcSessionIsLeftOpenOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L125)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4024`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_access_control.conf --rule acAcJournalNumberingAdvancesOnlyForAWard acAcSessionIsLeftOpenOnlyForAWard`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -41,7 +41,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IAccounting
-    function unlock(PoolId poolId) external auth {
+    function unlock(PoolId poolId) external { // MUTATION: the ward gate is gone
         require(PoolId.unwrap(_currentPoolId) == 0, AccountingAlreadyUnlocked());
         require(!poolId.isNull(), InvalidPoolId());
         debited = 0;
```

## Accounting #4025

claimWard is an entry point shipped without the ward gate, so any caller can seat itself in the ledger's own permission set.

- **Mutant:** [`4025.sol`](4025.sol)
- **Caught by:** [`acAcPermissionsMoveOnlyForAWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_access_control.spec#L91)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4025`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_access_control.conf --rule acAcPermissionsMoveOnlyForAWard`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -52,6 +52,11 @@
             TransientJournal.setJournalId(poolId, _generateJournalId(poolId));
         }
         emit StartJournalId(poolId, TransientJournal.journalId(poolId));
+    }
+
+    /// @notice MUTATION: a self service seat, an entry point shipped without the ward gate.
+    function claimWard() external {
+        wards[msg.sender] = 1;
     }
 
     /// @inheritdoc IAccounting
```

## Accounting #4027

unlock mints a fresh journal id on every open, so a pool's journal cannot reopen inside one transaction under the id it already minted.

- **Mutant:** [`4027.sol`](4027.sol)
- **Caught by:** [`hlAcSecondJournalOfAPoolReusesItsJournalId`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L56)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4027`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcSecondJournalOfAPoolReusesItsJournalId`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -48,9 +48,8 @@
         credited = 0;
         _currentPoolId = poolId;
 
-        if (TransientJournal.journalId(poolId) == 0) {
-            TransientJournal.setJournalId(poolId, _generateJournalId(poolId));
-        }
+        // MUTATION: the seed guard is gone, so every open mints a fresh id
+        TransientJournal.setJournalId(poolId, _generateJournalId(poolId));
         emit StartJournalId(poolId, TransientJournal.journalId(poolId));
     }
 
```

## Accounting #4028

createAccount stores a zero creation stamp, so the account looks uncreated and nothing can post to it.

- **Mutant:** [`4028.sol`](4028.sol)
- **Caught by:** [`rcAcCreateDebitNormalAccountIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L214) · [`rcAcCreateCreditNormalAccountIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L233) · [`rcAcSecondRowOpensBesideALiveOneIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L252) · [`rcAcFirstRowOfAnEmptyChartIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L274) · [`rcAcRowsCreatedAndJournalledInOneTransactionIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L366) · [`rcAcFreshRowReadsBackThePostedValueIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L388) · [`rcAcDebitNormalRowReportsANegativeValueIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L405) · [`rcAcRowDebitedAndCreditedAlikeReadsZeroIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L422)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4028`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcCreateDebitNormalAccountIsReachable rcAcCreateCreditNormalAccountIsReachable rcAcSecondRowOpensBesideALiveOneIsReachable rcAcFirstRowOfAnEmptyChartIsReachable rcAcRowsCreatedAndJournalledInOneTransactionIsReachable rcAcFreshRowReadsBackThePostedValueIsReachable rcAcDebitNormalRowReportsANegativeValueIsReachable rcAcRowDebitedAndCreditedAlikeReadsZeroIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -71,7 +71,7 @@
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
-        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[poolId][account] = Account(0, 0, isDebitNormal, 0, ""); // MUTATION: creation stamp dropped to zero
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Accounting #4029

addDebit never raises the session's running debit total, so a journal with a nonzero credit can never close.

- **Mutant:** [`4029.sol`](4029.sol)
- **Caught by:** [`rcAcBalancedPairPostsAndClosesIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L43) · [`rcAcDebitFillsARowToTheCeilingIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L125) · [`rcAcCeilingPairPostsAndClosesIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L159) · [`rcAcJournalBatchReachesTheWholeChartIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L293) · [`rcAcOpenSessionReportsItsRunningSidesIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L439)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4029`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcBalancedPairPostsAndClosesIsReachable rcAcDebitFillsARowToTheCeilingIsReachable rcAcCeilingPairPostsAndClosesIsReachable rcAcJournalBatchReachesTheWholeChartIsReachable rcAcOpenSessionReportsItsRunningSidesIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -94,7 +94,7 @@
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
         acc.totalDebit += value;
-        debited += value;
+        // MUTATION: the session's running debit counter is never raised
         acc.lastUpdated = uint64(block.timestamp);
         emit Debit(_currentPoolId, account, value);
     }
```

## Accounting #4030

addCredit never accumulates into the account row, so no credit reaches a row's credit side.

- **Mutant:** [`4030.sol`](4030.sol)
- **Caught by:** [`rcAcCreditFillsARowToTheCeilingIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L142) · [`rcAcSaturatedDebitRowStillTakesACreditIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L182)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4030`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcCreditFillsARowToTheCeilingIsReachable rcAcSaturatedDebitRowStillTakesACreditIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -106,7 +106,7 @@
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        acc.totalCredit += value;
+        // MUTATION: the credit never reaches the account row
         credited += value;
         acc.lastUpdated = uint64(block.timestamp);
         emit Credit(_currentPoolId, account, value);
```

## Accounting #4031

addCredit never raises the session's running credit total, so a journal with nonzero debits can never close.

- **Mutant:** [`4031.sol`](4031.sol)
- **Caught by:** [`rcAcTwoDebitsCloseAgainstOneCreditIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L67)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4031`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcTwoDebitsCloseAgainstOneCreditIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -107,7 +107,7 @@
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
         acc.totalCredit += value;
-        credited += value;
+        // MUTATION: the session's running credit counter is never raised
         acc.lastUpdated = uint64(block.timestamp);
         emit Credit(_currentPoolId, account, value);
     }
```

## Accounting #4034

addDebit never adds to the account's debit total, so a debit can never turn a credit heavy row debit heavy.

- **Mutant:** [`4034.sol`](4034.sol)
- **Caught by:** [`rcAcDebitOvertakesACreditHeavyRowIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L198)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4034`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcDebitOvertakesACreditHeavyRowIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -93,7 +93,7 @@
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        acc.totalDebit += value;
+        // MUTATION: the debit never reaches the account row
         debited += value;
         acc.lastUpdated = uint64(block.timestamp);
         emit Debit(_currentPoolId, account, value);
```

## Accounting #4302

addDebit posts nothing to the account's debit total, so a journal pair's debit never lands on the row it names.

- **Mutant:** [`4302.sol`](4302.sol)
- **Caught by:** [`hlAcJournalPairDebitsExactlyItsNamedRow`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 4302`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcJournalPairDebitsExactlyItsNamedRow`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -93,7 +93,7 @@
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        acc.totalDebit += value;
+        // MUTATION: removed the ledger debit posting
         debited += value;
         acc.lastUpdated = uint64(block.timestamp);
         emit Debit(_currentPoolId, account, value);
```

## Accounting #7100

rely refuses an address that holds no ward, so a fresh ward can never be granted.

- **Mutant:** [`7100.sol`](7100.sol)
- **Caught by:** [`rcAcAuthorityGrantRoundTripIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L455)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 7100`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcAuthorityGrantRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -23,6 +23,7 @@
 
     /// @inheritdoc IAuth
     function rely(address user) public auth {
+        require(wards[user] == 1, NotAuthorized()); // MUTATION: a seat is handed out only to an address that already holds one
         wards[user] = 1;
         emit Rely(user);
     }
```

## Accounting #7101

deny refuses a caller naming its own address, so a ward can never revoke its own rights.

- **Mutant:** [`7101.sol`](7101.sol)
- **Caught by:** [`rcAcWardRevokesItselfIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L474)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 7101`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcWardRevokesItselfIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,6 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
+        require(user != msg.sender, NotAuthorized()); // MUTATION: the caller's own seat is out of reach of a revocation
         wards[user] = 0;
         emit Deny(user);
     }
```

## Accounting #7102

lock refuses exactly the journal that balances, so no balanced pair ever reaches the books.

- **Mutant:** [`7102.sol`](7102.sol)
- **Caught by:** [`rcAcPassingJournalPairOnABalancedPairIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L488)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 7102`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcPassingJournalPairOnABalancedPairIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -57,7 +57,7 @@
     /// @inheritdoc IAccounting
     function lock() external auth {
         require(!_currentPoolId.isNull(), AccountingLocked());
-        require(debited == credited, Unbalanced());
+        require(debited != credited, Unbalanced()); // MUTATION: the balance test is inverted, so a balanced journal never closes
 
         emit EndJournalId(_currentPoolId, TransientJournal.journalId(_currentPoolId));
         _currentPoolId = PoolId.wrap(0);
```

## Accounting #7103

addDebit loses the gate that asks whether the row was ever opened, so a charge lands on an account the ledger never created.

- **Mutant:** [`7103.sol`](7103.sol)
- **Caught by:** [`rvAcAddDebitRefusesARowTheLedgerNeverOpened`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L51)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 7103`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcAddDebitRefusesARowTheLedgerNeverOpened`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -91,7 +91,7 @@
         require(!_currentPoolId.isNull(), AccountingLocked());
 
         Account storage acc = accounts[_currentPoolId][account];
-        require(acc.lastUpdated != 0, AccountDoesNotExist());
+        // MUTATION: the existence gate is gone
 
         acc.totalDebit += value;
         debited += value;
```

## Accounting #7104

addCredit loses the gate that asks whether the row was ever opened, so a credit lands on an account the ledger never created.

- **Mutant:** [`7104.sol`](7104.sol)
- **Caught by:** [`rvAcAddCreditRefusesARowTheLedgerNeverOpened`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L68)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 7104`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcAddCreditRefusesARowTheLedgerNeverOpened`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -104,7 +104,7 @@
         require(!_currentPoolId.isNull(), AccountingLocked());
 
         Account storage acc = accounts[_currentPoolId][account];
-        require(acc.lastUpdated != 0, AccountDoesNotExist());
+        // MUTATION: the existence gate is gone
 
         acc.totalCredit += value;
         credited += value;
```

## Accounting #7105

accountValue reads its existence test backwards, so the books answer only for rows that were never opened.

- **Mutant:** [`7105.sol`](7105.sol)
- **Caught by:** [`rvAcAccountValueAlwaysAnswersForARowThatStands`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L196)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 7105`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcAccountValueAlwaysAnswersForARowThatStands`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -130,7 +130,7 @@
     /// @inheritdoc IAccounting
     function accountValue(PoolId poolId, AccountId account) external view returns (bool, /* isPositive */ uint128) {
         Account storage acc = accounts[poolId][account];
-        require(acc.lastUpdated != 0, AccountDoesNotExist());
+        require(acc.lastUpdated == 0, AccountDoesNotExist()); // MUTATION: the existence test is inverted
 
         if (acc.isDebitNormal) {
             // For debit-normal accounts: Value = Total Debit - Total Credit
```

## Accounting #7106

the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.

- **Mutant:** [`7106.sol`](7106.sol)
- **Caught by:** [`rvAcUnlockRefusesANonWard`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 7106`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcUnlockRefusesANonWard`

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

## Accounting #7107

unlock rewinds the pool's journal counter instead of advancing it, so a number already spent is handed out a second time.

- **Mutant:** [`7107.sol`](7107.sol)
- **Caught by:** [`vtAcJournalCounterNeverRewinds`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 7107`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_transitions.conf --rule vtAcJournalCounterNeverRewinds`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -155,6 +155,6 @@
     }
 
     function _generateJournalId(PoolId poolId) internal returns (uint256) {
-        return uint256((uint256(poolId.raw()) << 128) | ++_poolJournalIdCounter[poolId]);
+        return uint256((uint256(poolId.raw()) << 128) | --_poolJournalIdCounter[poolId]); // MUTATION: unlock rewinds the counter
     }
 }
```

## Accounting #8600

addDebit no longer checks that a journal is open, so a ward can post a debit to the books while the ledger is closed.

- **Mutant:** [`8600.sol`](8600.sol)
- **Caught by:** [`rvAcAddDebitIsRefusedOffSession`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L211)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 8600`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcAddDebitIsRefusedOffSession`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -88,7 +88,7 @@
 
     /// @inheritdoc IAccounting
     function addDebit(AccountId account, uint128 value) public auth {
-        require(!_currentPoolId.isNull(), AccountingLocked());
+        // MUTATION: addDebit no longer checks that a journal is open
 
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
```

## Accounting #8601

addCredit no longer checks that a journal is open, so a ward can post a credit to the books while the ledger is closed.

- **Mutant:** [`8601.sol`](8601.sol)
- **Caught by:** [`rvAcAddCreditIsRefusedOffSession`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L222)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 8601`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcAddCreditIsRefusedOffSession`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -101,7 +101,7 @@
 
     /// @inheritdoc IAccounting
     function addCredit(AccountId account, uint128 value) public auth {
-        require(!_currentPoolId.isNull(), AccountingLocked());
+        // MUTATION: addCredit no longer checks that a journal is open
 
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
```

## Accounting #8602

lock no longer checks that a journal is open, so a close is admitted and announced for a journal that was never opened.

- **Mutant:** [`8602.sol`](8602.sol)
- **Caught by:** [`rvAcLockIsRefusedOffSession`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L233)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 8602`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcLockIsRefusedOffSession`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -56,7 +56,7 @@
 
     /// @inheritdoc IAccounting
     function lock() external auth {
-        require(!_currentPoolId.isNull(), AccountingLocked());
+        // MUTATION: lock no longer checks that a journal is open
         require(debited == credited, Unbalanced());
 
         emit EndJournalId(_currentPoolId, TransientJournal.journalId(_currentPoolId));
```

## Accounting #8603

unlock no longer refuses the null pool, so a journal opens on the id that marks a closed ledger.

- **Mutant:** [`8603.sol`](8603.sol)
- **Caught by:** [`rvAcUnlockRefusesTheNullPool`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L244)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 8603`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcUnlockRefusesTheNullPool`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -43,7 +43,7 @@
     /// @inheritdoc IAccounting
     function unlock(PoolId poolId) external auth {
         require(PoolId.unwrap(_currentPoolId) == 0, AccountingAlreadyUnlocked());
-        require(!poolId.isNull(), InvalidPoolId());
+        // MUTATION: unlock no longer refuses the null pool
         debited = 0;
         credited = 0;
         _currentPoolId = poolId;
```

## Accounting #8604

a journal id is minted from the pool's counter alone, without the pool in its high half, so two pools draw colliding ids.

- **Mutant:** [`8604.sol`](8604.sol)
- **Caught by:** [`hlAcMintedJournalIdCarriesItsPool`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L131)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 8604`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcMintedJournalIdCarriesItsPool`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -155,6 +155,6 @@
     }
 
     function _generateJournalId(PoolId poolId) internal returns (uint256) {
-        return uint256((uint256(poolId.raw()) << 128) | ++_poolJournalIdCounter[poolId]);
+        return uint256(++_poolJournalIdCounter[poolId]); // MUTATION: the pool is dropped from the journal id
     }
 }
```

## Accounting #8605

unlock opens the session on a fixed pool instead of the pool it names, so the entries that follow land in another pool's books.

- **Mutant:** [`8605.sol`](8605.sol)
- **Caught by:** [`hlAcUnlockOpensTheSessionOnTheNamedPool`](../../specs/core/hub/Accounting/single/Accounting_single_pool_high_level.spec#L144)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 8605`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_high_level.conf --rule hlAcUnlockOpensTheSessionOnTheNamedPool`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -46,7 +46,7 @@
         require(!poolId.isNull(), InvalidPoolId());
         debited = 0;
         credited = 0;
-        _currentPoolId = poolId;
+        _currentPoolId = PoolId.wrap(1); // MUTATION: the session always stands on pool one
 
         if (TransientJournal.journalId(poolId) == 0) {
             TransientJournal.setJournalId(poolId, _generateJournalId(poolId));
```

## Accounting #8606

the journal id read drops the pool from its key, so every opening mints a new id yet reports journal id zero.

- **Mutant:** [`8606.sol`](8606.sol)
- **Caught by:** [`hlAcSecondPoolOfATransactionOpensUnderItsOwnId`](../../specs/core/hub/Accounting/Accounting_multi_pool_properties.spec#L69)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 8606`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/multi_pool_properties.conf --rule hlAcSecondPoolOfATransactionOpensUnderItsOwnId`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -14,7 +14,7 @@
 /// So we're keeping a journal ID per pool in transient storage.
 library TransientJournal {
     function journalId(PoolId poolId) internal view returns (uint256) {
-        return TransientStorageLib.tloadUint256(keccak256(abi.encode("journalId", poolId)));
+        return TransientStorageLib.tloadUint256(keccak256(abi.encode("journalId"))); // MUTATION: the journal read drops the pool from its key
     }
 
     function setJournalId(PoolId poolId, uint256 value) internal {
```

## Accounting #9001

opening an account rewinds the pool's journal numbering to zero, so ids already handed out are handed out again.

- **Mutant:** [`9001.sol`](9001.sol)
- **Caught by:** [`issuedJournalIdsLieAtOrBelowTheHighWaterMark`](../../specs/core/hub/Accounting/single/Accounting_single_pool_valid_state.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 9001`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_valid_state.conf --rule issuedJournalIdsLieAtOrBelowTheHighWaterMark`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -72,6 +72,7 @@
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
         accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        _poolJournalIdCounter[poolId] = 0; // MUTATION: opening an account rewinds the pool's journal numbering
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Accounting #9003

lock also admits a close with no journal open while an earlier journal's debit total lingers, so an unopened session closes.

- **Mutant:** [`9003.sol`](9003.sol)
- **Caught by:** [`rvAcLockIsRefusedAfterAClosedJournal`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reverts.spec#L257)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 9003`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reverts.conf --rule rvAcLockIsRefusedAfterAClosedJournal`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -56,7 +56,7 @@
 
     /// @inheritdoc IAccounting
     function lock() external auth {
-        require(!_currentPoolId.isNull(), AccountingLocked());
+        require(!_currentPoolId.isNull() || debited != 0, AccountingLocked()); // MUTATION: a closed journal's leftover totals pass for an open one
         require(debited == credited, Unbalanced());
 
         emit EndJournalId(_currentPoolId, TransientJournal.journalId(_currentPoolId));
```

## Accounting #9004

setAccountMetadata also restamps the account's last update time, so relabelling an account makes it read as freshly posted to.

- **Mutant:** [`9004.sol`](9004.sol)
- **Caught by:** [`hlAcSetAccountMetadataWritesOnlyItsAccountsMetadata`](../../specs/core/hub/Accounting/Accounting_metadata_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 9004`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/metadata_properties.conf --rule hlAcSetAccountMetadataWritesOnlyItsAccountsMetadata`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -78,7 +78,7 @@
     /// @inheritdoc IAccounting
     function setAccountMetadata(PoolId poolId, AccountId account, bytes calldata metadata) external auth {
         require(accounts[poolId][account].lastUpdated != 0, AccountDoesNotExist());
-        accounts[poolId][account].metadata = metadata;
+        accounts[poolId][account].metadata = metadata; accounts[poolId][account].lastUpdated = uint64(block.timestamp); // MUTATION: the metadata write also restamps the account
         emit SetAccountMetadata(poolId, account, metadata);
     }
 
```

## Accounting #9041

the journal id counter is never advanced, so every new journal reuses the pool's last id.

- **Mutant:** [`9041.sol`](9041.sol)
- **Caught by:** [`rcAcUnlockOpensAJournalIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L4) · [`rcAcEmptyJournalOverAnUntouchedLedgerIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L22) · [`rcAcEmptyJournalBatchIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L320)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 9041`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcUnlockOpensAJournalIsReachable rcAcEmptyJournalOverAnUntouchedLedgerIsReachable rcAcEmptyJournalBatchIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -155,6 +155,6 @@
     }
 
     function _generateJournalId(PoolId poolId) internal returns (uint256) {
-        return uint256((uint256(poolId.raw()) << 128) | ++_poolJournalIdCounter[poolId]);
+        return uint256((uint256(poolId.raw()) << 128) | _poolJournalIdCounter[poolId]); // MUTATION: the id counter is never advanced
     }
 }
```

## Accounting #9042

addCredit no longer refreshes the row's update time, so a credit leaves the account's old timestamp in place.

- **Mutant:** [`9042.sol`](9042.sol)
- **Caught by:** [`rcAcZeroValueCreditRestampsTheRowIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L106)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 9042`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcZeroValueCreditRestampsTheRowIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -108,7 +108,7 @@
 
         acc.totalCredit += value;
         credited += value;
-        acc.lastUpdated = uint64(block.timestamp);
+        // MUTATION: addCredit no longer restamps the row
         emit Credit(_currentPoolId, account, value);
     }
 
```

## Accounting #9043

addDebit no longer refreshes the row's update time, so a debit leaves the account's old timestamp in place.

- **Mutant:** [`9043.sol`](9043.sol)
- **Caught by:** [`rcAcZeroValueDebitRestampsTheRowIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L87) · [`rcAcZeroValueJournalBatchIsReachable`](../../specs/core/hub/Accounting/single/Accounting_single_pool_reachability.spec#L343)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 9043`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_reachability.conf --rule rcAcZeroValueDebitRestampsTheRowIsReachable rcAcZeroValueJournalBatchIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -95,7 +95,7 @@
 
         acc.totalDebit += value;
         debited += value;
-        acc.lastUpdated = uint64(block.timestamp);
+        // MUTATION: addDebit no longer restamps the row
         emit Debit(_currentPoolId, account, value);
     }
 
```

## Accounting #9044

each journal id takes the counter before it advances, so a new journal reuses the id its pool issued last.

- **Mutant:** [`9044.sol`](9044.sol)
- **Caught by:** [`stAcMintedJournalIdWasNeverIssuedBefore`](../../specs/core/hub/Accounting/single/Accounting_single_pool_transitions.spec#L105)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 9044`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/single_pool_transitions.conf --rule stAcMintedJournalIdWasNeverIssuedBefore`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -155,6 +155,6 @@
     }
 
     function _generateJournalId(PoolId poolId) internal returns (uint256) {
-        return uint256((uint256(poolId.raw()) << 128) | ++_poolJournalIdCounter[poolId]);
+        return uint256((uint256(poolId.raw()) << 128) | _poolJournalIdCounter[poolId]++); // MUTATION: post increment mints the counter's old value
     }
 }
```

## Accounting #9045

the journal id is written under a key that omits the pool, so one pool's open overwrites another pool's id.

- **Mutant:** [`9045.sol`](9045.sol)
- **Caught by:** [`stAcAPoolsJournalIdIsFixedForTheTransaction`](../../specs/core/hub/Accounting/Accounting_multi_pool_properties.spec#L52)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Accounting 9045`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Accounting/multi_pool_properties.conf --rule stAcAPoolsJournalIdIsFixedForTheTransaction`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -18,7 +18,7 @@
     }
 
     function setJournalId(PoolId poolId, uint256 value) internal {
-        TransientStorageLib.tstore(keccak256(abi.encode("journalId", poolId)), value);
+        TransientStorageLib.tstore(keccak256(abi.encode("journalId")), value); // MUTATION: the journal write drops the pool from its key
     }
 }
 
```

