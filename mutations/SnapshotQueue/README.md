# Mutations for `SnapshotQueue` (`src/core/spoke/SnapshotQueue.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [1402](#snapshotqueue-1402) | netting the share queue down to an exact zero keeps the previous positive sign instead of canonicalizing it to non-positive.<br>Caught by: [`zeroDeltaIsNonPositive`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L10) |
| [1403](#snapshotqueue-1403) | an exact cancellation of the queued share delta is routed to the sign-flip branch, so a zero delta can come out flagged positive.<br>Caught by: [`zeroDeltaIsNonPositive`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L10) |
| [1404](#snapshotqueue-1404) | flushShares resets the queued delta but not its sign, so a drained share queue can still read as positive.<br>Caught by: [`zeroDeltaIsNonPositive`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L10) |
| [1405](#snapshotqueue-1405) | queueAssets no longer counts a previously empty asset row, so the queued asset counter falls behind the rows waiting to flush.<br>Caught by: [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15) |
| [1406](#snapshotqueue-1406) | queueAssets counts an asset row as new whenever either accumulator is empty, so a one-sided row is counted twice.<br>Caught by: [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15) |
| [1407](#snapshotqueue-1407) | queueAssets accepts zero amounts, counting an asset row into the queued asset counter while the row itself stays empty.<br>Caught by: [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15) |
| [1408](#snapshotqueue-1408) | flushAssets clears an asset row without releasing the queued asset counter, so drained rows stay counted forever.<br>Caught by: [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15) |
| [1409](#snapshotqueue-1409) | flushAssets treats a one-sided asset row as empty, so flushing it never releases the queued asset counter.<br>Caught by: [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15) |
| [1410](#snapshotqueue-1410) | flushAssets releases the queued asset counter but leaves the deposits behind, so a still-loaded row is reported as drained.<br>Caught by: [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15) |
| [1411](#snapshotqueue-1411) | flushAssets clears only the deposit side of the queue it hands over, so a drained asset queue keeps its withdrawals.<br>Caught by: [`stSqAssetFlushEmptiesTheRowAndSpendsOneOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L47) |
| [1412](#snapshotqueue-1412) | flushShares spends a nonce without clearing the net it hands over, so the remainder stays queued under a spent nonce.<br>Caught by: [`stSqShareFlushHandsOverTheWholeNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L69) |
| [1413](#snapshotqueue-1413) | queueAssets advances the queue nonce when it opens an asset row, so a nonce is spent with no update sent.<br>Caught by: [`stSqOpeningAnAssetRowSpendsNoOrdinalAndMovesNoShareNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L87) |
| [1414](#snapshotqueue-1414) | queueAssets loses the else, so a queued deposit is also recorded as a withdrawal of the same asset.<br>Caught by: [`stSqAssetFlowTakesOneSideOnly`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L104) |
| [1415](#snapshotqueue-1415) | queueSharesPair queues one share delta for two pools, so one call moves two pools' share rows.<br>Caught by: [`stSqShareRowIsPerPool`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_multi_pool_properties.spec#L6) |
| [1416](#snapshotqueue-1416) | queueAssetsPair queues one asset flow for two pools, so one call moves two pools' asset rows and both share counters.<br>Caught by: [`stSqAssetRowIsPerPool`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_multi_pool_properties.spec#L32) · [`stSqQueueSidesDoNotCrossPools`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_multi_pool_properties.spec#L53) |
| [1417](#snapshotqueue-1417) | flushAssets rewinds the nonce instead of advancing it, so a later report is filed under a number the hub has already seen.<br>Caught by: [`stSqNonceAdvancesByAtMostOne`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L121) |
| [1419](#snapshotqueue-1419) | flushShares advances the nonce by two, so the hub rejects every later report as out of order.<br>Caught by: [`stSqNonceAdvancesByAtMostOne`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L121) |
| [5100](#snapshotqueue-5100) | queueAssets runs without the ward gate, so any caller moves a pool's asset rows and the count of queued assets.<br>Caught by: [`acSqOnlyAWardMovesAnAssetRow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L23) · [`acSqOnlyAWardMovesTheOutstandingAssetCount`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L43) |
| [5101](#snapshotqueue-5101) | flushShares runs without the ward gate, so any caller hands a pool's queued share net to the hub and spends a report nonce.<br>Caught by: [`acSqOnlyAWardMovesTheShareNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L4) · [`acSqOnlyAWardSpendsAFlushOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L60) |
| [5102](#snapshotqueue-5102) | rely runs without the ward gate in the shared Auth mixin, so any caller seats itself among the wards that move the whole queue.<br>Caught by: [`acSqOnlyAWardMovesTheWardBit`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L76) |
| [5103](#snapshotqueue-5103) | flushShares reports a snapshot while one asset row is still queued, so the hub reads a half applied balance sheet.<br>Caught by: [`hlSqShareFlushReportsATruthfulSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L6) · [`hlSqZeroAmountQueueingCannotStallTheSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L169) |
| [5104](#snapshotqueue-5104) | flushAssets reports a snapshot without checking the share net is zero, so a class with queued shares reads as in sync.<br>Caught by: [`hlSqAssetFlushReportsATruthfulSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L20) |
| [5105](#snapshotqueue-5105) | flushAssets reports deposits plus withdrawals instead of their net, so the hub can book more asset movement than happened.<br>Caught by: [`hlSqAssetPayloadCarriesTheNetMagnitude`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L37) |
| [5106](#snapshotqueue-5106) | flushAssets marks a row with equal deposits and withdrawals as an increase, so a zero net reaches the hub as a deposit.<br>Caught by: [`hlSqAssetPayloadPointsTowardTheLargerSide`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L58) |
| [5107](#snapshotqueue-5107) | the share flush reports nothing whenever the queued net leans toward revocation, so shares a pool has revoked never reach the hub.<br>Caught by: [`hlSqSharePayloadCarriesTheNetMagnitude`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L78) |
| [5108](#snapshotqueue-5108) | a queued net that flips direction keeps its old sign, so the hub receives a revocation as an issuance or vice versa.<br>Caught by: [`hlSqSharePayloadCarriesTheNetSign`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L97) |
| [5109](#snapshotqueue-5109) | the asset flush drains only the side its payload pointed at, so the opposite side survives and is submitted to the hub a second time.<br>Caught by: [`hlSqSecondAssetFlushReportsNothing`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L116) |
| [5110](#snapshotqueue-5110) | the share flush clears the queued net only for an issuance, so a queued revocation is reported to the hub again.<br>Caught by: [`hlSqSecondShareFlushReportsNothing`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L129) |
| [5111](#snapshotqueue-5111) | a flush of an empty asset row spends no nonce, so two consecutive asset reports reach the hub filed under the same number.<br>Caught by: [`hlSqConsecutiveAssetFlushesSpendConsecutiveOrdinals`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L141) |
| [5112](#snapshotqueue-5112) | a flush of an empty share net spends no nonce, so two consecutive share reports reach the hub filed under the same number.<br>Caught by: [`hlSqConsecutiveShareFlushesSpendConsecutiveOrdinals`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L155) |
| [5113](#snapshotqueue-5113) | queueShares spends a report nonce, so the spoke's report stream advances without any queue being handed over.<br>Caught by: [`vtSqOnlyAFlushSpendsAnOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L30) |
| [5114](#snapshotqueue-5114) | queueAssets adds to a side without the overflow check, so an oversized total wraps to a small one instead of reverting.<br>Caught by: [`hlSqAssetPayloadPointsTowardTheLargerSide`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L58) |
| [5115](#snapshotqueue-5115) | the share netting grows the queued net with the width check removed, so a net that outgrows its width wraps instead of refusing the call.<br>Caught by: [`hlSqSharePayloadCarriesTheNetMagnitude`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L78) |
| [5116](#snapshotqueue-5116) | the asset flush always releases one pending row, so flushing an empty row can underflow the count and revert.<br>Caught by: [`rvSqFlushAssetsAlwaysAdmitsAWardWhileOrdinalsRemain`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L91) |
| [5117](#snapshotqueue-5117) | the share flush advances its nonce with the width check removed, so an exhausted nonce wraps back to the start instead of refusing the call.<br>Caught by: [`stSqNonceAdvancesByAtMostOne`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L121) |
| [5121](#snapshotqueue-5121) | the asset flush clears the row only on a snapshot, so the next flush resubmits totals the hub already has.<br>Caught by: [`hlSqSecondAssetFlushReportsNothing`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L116) |
| [5122](#snapshotqueue-5122) | queueAssetsTwoRows queues one flow into two asset rows of the same class, so a single call moves the amounts another asset still has waiting.<br>Caught by: [`vtSqAssetRowsMoveOneAtATime`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L6) |
| [6300](#snapshotqueue-6300) | queueAssets skips every nonzero amount, so real flows never queue and a zero amount counts an empty row as waiting.<br>Caught by: [`rcSqQueueAssetsCanOpenADepositRow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L4) · [`rcSqQueueAssetsCanOpenAWithdrawalRow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L19) · [`rcSqZeroAmountQueueLeavesTheSnapshotAvailable`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L117) |
| [6301](#snapshotqueue-6301) | queueAssets books a deposit as a withdrawal and a withdrawal as a deposit, so the hub receives every asset flow reversed.<br>Caught by: [`rcSqQueueAssetsCanAbsorbTheFullAccumulatorWidth`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L86) · [`rcSqQueueAssetsCanMakeAClassOutstandingWithOneUnit`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L102) · [`rcSqQueuedAssetsViewCanReadBackAFreshFlow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L602) |
| [6302](#snapshotqueue-6302) | queueAssets counts a row only when it is already loaded, so the outstanding count moves on later flows, not the first.<br>Caught by: [`rcSqQueueAssetsCanAccumulateASecondDeposit`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L34) · [`rcSqQueueAssetsCanLeaveThreeAssetsOutstandingAtOnce`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L69) |
| [6303](#snapshotqueue-6303) | queueAssets bumps the outstanding count on every call, zero amounts included, so the count runs ahead of the waiting rows.<br>Caught by: [`rcSqQueueAssetsCanHoldBothSidesOfOneRow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L53) |
| [6304](#snapshotqueue-6304) | queueShares turns away every real share delta and lets only a zero one through, so a mint or a burn never reaches the queued net.<br>Caught by: [`rcSqQueueSharesCanOpenAnIssuanceNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L134) · [`rcSqQueueSharesCanOpenARevocationNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L149) · [`rcSqQueueSharesCanAbsorbTheFullNetWidth`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L213) |
| [6305](#snapshotqueue-6305) | queueShares ignores a delta in the net's own direction or on an empty net, so nothing can open or grow it.<br>Caught by: [`rcSqQueueSharesCanGrowAnIssuanceNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L164) · [`rcSqALargerRevocationCanFlipTheQueuedNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L247) · [`rcSqQueuedSharesViewCanReadBackAFreshNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L582) |
| [6306](#snapshotqueue-6306) | an opposing share delta no longer eats into the waiting net, so a revocation can neither shrink a queued issuance nor cancel it.<br>Caught by: [`rcSqQueueSharesCanShrinkAnIssuanceNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L181) · [`rcSqQueueSharesCanCancelAnIssuanceNetExactly`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L198) |
| [6307](#snapshotqueue-6307) | flushShares reports the queued net with its direction reversed, so an issuance reaches the hub as a revocation.<br>Caught by: [`rcSqZeroShareQueueLeavesTheNetPayloadIntact`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L228) · [`rcSqShareFlushCanHandOverAnIssuanceAndReportASnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L400) |
| [6308](#snapshotqueue-6308) | flushShares flags a snapshot exactly when an asset row is still outstanding, so the flag reads backwards on every share report.<br>Caught by: [`rcSqShareFlushCanHandOverARevocationAndReportASnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L423) · [`rcSqShareFlushWithAnAssetRowOutstandingCanReportNoSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L441) · [`rcSqEmptyShareFlushStillSpendsAnOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L458) |
| [6309](#snapshotqueue-6309) | the share flush no longer spends a report nonce, so two consecutive share reports reach the hub filed under the same number.<br>Caught by: [`hlSqConsecutiveShareFlushesSpendConsecutiveOrdinals`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L155) |
| [6310](#snapshotqueue-6310) | flushAssets advances the nonce by two, so the hub rejects every later report as out of order.<br>Caught by: [`rcSqAssetFlushCanHandOverAndReportASnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L268) · [`rcSqEmptyAssetFlushStillSpendsAnOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L358) |
| [6311](#snapshotqueue-6311) | the asset flush reports every payload as a withdrawal, so a queued deposit reaches the hub pointing out of the pool.<br>Caught by: [`rcSqAssetFlushCanNetTowardTheDepositSide`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L322) |
| [6312](#snapshotqueue-6312) | the asset flush reports every payload as a deposit, so a queued withdrawal reaches the hub pointing into the pool.<br>Caught by: [`rcSqAssetFlushCanNetTowardTheWithdrawalSide`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L340) · [`rcSqOffsettingRowCanFlushZeroYetClearTheCount`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L380) |
| [6313](#snapshotqueue-6313) | the asset flush always tells the hub the class is in sync, so a partial hand over is reported as a complete one.<br>Caught by: [`rcSqAssetFlushWithASiblingRowOutstandingCanReportNoSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L290) · [`rcSqAnOutOfSyncClassCanBeBroughtBackIntoSync`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L478) |
| [6314](#snapshotqueue-6314) | the asset flush counts the row it just drained a second time instead of striking it off, so the outstanding count only ever grows.<br>Caught by: [`rcSqAssetFlushWithSharesOutstandingCanReportNoSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L306) · [`rcSqAnAssetRowCanBeReusedAfterAFlush`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L505) |
| [6315](#snapshotqueue-6315) | rely seats the caller instead of the account the call names, so a ward can never hand the queue seat on to anyone else.<br>Caught by: [`rcSqAFreshlyReliedAccountCanMoveTheQueue`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L546) |
| [6316](#snapshotqueue-6316) | deny leaves the seat it names standing, so authority over the queue can never be taken back once granted.<br>Caught by: [`rcSqDenyCanRemoveAnotherAccountsQueueSeat`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L531) · [`rcSqAWardCanDenyItself`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L567) |
| [6317](#snapshotqueue-6317) | queueShares runs without the ward gate, so any caller moves a pool's queued share net.<br>Caught by: [`rvSqQueueSharesRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L19) |
| [6318](#snapshotqueue-6318) | flushAssets runs without the ward gate, so any caller hands a pool's queued asset flow to the hub.<br>Caught by: [`rvSqFlushAssetsRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L34) |
| [6319](#snapshotqueue-6319) | deny runs without the ward gate, so an account holding no seat strips a ward of its permissions.<br>Caught by: [`rvSqDenyRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L77) |
| [6320](#snapshotqueue-6320) | the share flush leaves one unit on the row it drained, so the view never reports an emptied queue.<br>Caught by: [`stSqShareFlushHandsOverTheWholeNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L69) |
| [6321](#snapshotqueue-6321) | the asset flush leaves one unit on the row it drained, so the view never reports an emptied queue.<br>Caught by: [`hlSqSecondAssetFlushReportsNothing`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L116) |
| [6322](#snapshotqueue-6322) | the share flush refuses a queue whose net is already zero, so a ward can no longer spend a nonce on an empty row.<br>Caught by: [`rvSqFlushSharesAlwaysAdmitsAWardWhileOrdinalsRemain`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L109) |
| [6323](#snapshotqueue-6323) | the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.<br>Caught by: [`rvSqFlushSharesRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L49) · [`rvSqQueueAssetsRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L4) · [`rvSqRelyRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L63) |
| [9029](#snapshotqueue-9029) | opening a new asset queue raises the queued share amount instead of the count of waiting assets, so an asset flow reports shares nobody issued.<br>Caught by: [`stSqTheShareNetMovesOnlyUnderShareEntries`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L6) |
| [9030](#snapshotqueue-9030) | a share flush also zeroes the count of waiting asset queues, so the next share flush reports a snapshot while assets still wait.<br>Caught by: [`stSqAssetQueuesMoveOnlyUnderAssetEntries`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L27) |
| [9360](#snapshotqueue-9360) | a row holding only withdrawals is counted again on every new amount, so the queued asset count overstates the waiting rows.<br>Caught by: [`queuedAssetCounterCountsEveryNonEmptyRow`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_all_assets_properties.spec#L11) |
| [9361](#snapshotqueue-9361) | flushAssets clears the next asset's deposits, not its own, so its own are reported again and the neighbour's lost.<br>Caught by: [`hlSqAnAssetFlushEmptiesItsOwnRowOnly`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L55) |
| [9362](#snapshotqueue-9362) | a share flush bumps the queued asset count instead of the nonce, so the class seems to have one more waiting asset queue.<br>Caught by: [`hlSqAShareFlushClearsOnlyItsNet`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L84) |
| [9363](#snapshotqueue-9363) | a share flush carrying a nonzero share net no longer reports a snapshot, so the hub waits for a sync that already happened.<br>Caught by: [`hlSqShareFlushSnapshotMeansTheClassIsDrained`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_all_assets_properties.spec#L18) |
| [9364](#snapshotqueue-9364) | an asset flush reports a snapshot while other asset queues still wait, so the hub takes an unsynced class for a synced one.<br>Caught by: [`hlSqAssetFlushSnapshotMeansTheClassIsDrained`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_all_assets_properties.spec#L34) |
| [9365](#snapshotqueue-9365) | an asset flush wipes the queued share net instead of advancing the nonce, so share issuance or revocation waiting for the Hub is silently lost.<br>Caught by: [`hlSqAnAssetFlushEmptiesItsOwnRowOnly`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L55) |

## SnapshotQueue #1402

netting the share queue down to an exact zero keeps the previous positive sign instead of canonicalizing it to non-positive.

- **Mutant:** [`1402.sol`](1402.sol)
- **Caught by:** [`zeroDeltaIsNonPositive`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L10)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1402`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_valid_state.conf --rule zeroDeltaIsNonPositive`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -124,7 +124,7 @@
             newIsPositive = newDelta != 0 && isIssuance;
         } else if (delta >= shares) {
             newDelta = delta - shares;
-            newIsPositive = newDelta != 0 && isPositive;
+            newIsPositive = isPositive; // MUTATION: zero canonicalization dropped on the netting-down path
         } else {
             newDelta = shares - delta;
             newIsPositive = isIssuance;
```

## SnapshotQueue #1403

an exact cancellation of the queued share delta is routed to the sign-flip branch, so a zero delta can come out flagged positive.

- **Mutant:** [`1403.sol`](1403.sol)
- **Caught by:** [`zeroDeltaIsNonPositive`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L10)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1403`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_valid_state.conf --rule zeroDeltaIsNonPositive`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -122,7 +122,7 @@
         if (isIssuance == isPositive || delta == 0) {
             newDelta = delta + shares;
             newIsPositive = newDelta != 0 && isIssuance;
-        } else if (delta >= shares) {
+        } else if (delta > shares) { // MUTATION: exact cancellation rerouted to the sign-flip branch
             newDelta = delta - shares;
             newIsPositive = newDelta != 0 && isPositive;
         } else {
```

## SnapshotQueue #1404

flushShares resets the queued delta but not its sign, so a drained share queue can still read as positive.

- **Mutant:** [`1404.sol`](1404.sol)
- **Caught by:** [`zeroDeltaIsNonPositive`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L10)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1404`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_valid_state.conf --rule zeroDeltaIsNonPositive`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -101,7 +101,7 @@
         });
 
         shareQueue.delta = 0;
-        shareQueue.isPositive = false;
+        // MUTATION: removed the sign reset on share flush
         shareQueue.nonce++;
 
         emit SubmitQueuedShares(poolId, scId, data);
```

## SnapshotQueue #1405

queueAssets no longer counts a previously empty asset row, so the queued asset counter falls behind the rows waiting to flush.

- **Mutant:** [`1405.sol`](1405.sol)
- **Caught by:** [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1405`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_valid_state.conf --rule queuedAssetCounterMatchesOutstandingRows`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -34,7 +34,7 @@
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
-        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
+        // MUTATION: removed the queued asset counter increment
 
         if (isIncrease) assetQueue.deposits += amount;
         else assetQueue.withdrawals += amount;
```

## SnapshotQueue #1406

queueAssets counts an asset row as new whenever either accumulator is empty, so a one-sided row is counted twice.

- **Mutant:** [`1406.sol`](1406.sol)
- **Caught by:** [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1406`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_valid_state.conf --rule queuedAssetCounterMatchesOutstandingRows`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -34,7 +34,7 @@
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
-        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
+        if (assetQueue.deposits == 0 || assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++; // MUTATION: empty-row test weakened to either side
 
         if (isIncrease) assetQueue.deposits += amount;
         else assetQueue.withdrawals += amount;
```

## SnapshotQueue #1407

queueAssets accepts zero amounts, counting an asset row into the queued asset counter while the row itself stays empty.

- **Mutant:** [`1407.sol`](1407.sol)
- **Caught by:** [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1407`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_valid_state.conf --rule queuedAssetCounterMatchesOutstandingRows`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -30,7 +30,7 @@
         external
         auth
     {
-        if (amount == 0) return;
+        // MUTATION: removed the zero-amount early return
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
```

## SnapshotQueue #1408

flushAssets clears an asset row without releasing the queued asset counter, so drained rows stay counted forever.

- **Mutant:** [`1408.sol`](1408.sol)
- **Caught by:** [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1408`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_valid_state.conf --rule queuedAssetCounterMatchesOutstandingRows`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -80,7 +80,7 @@
         assetQueue.deposits = 0;
         assetQueue.withdrawals = 0;
         shareQueue.nonce++;
-        shareQueue.queuedAssetCounter -= assetCounter;
+        // MUTATION: removed the queued asset counter release
 
         emit SubmitQueuedAssets(poolId, scId, assetId, data);
     }
```

## SnapshotQueue #1409

flushAssets treats a one-sided asset row as empty, so flushing it never releases the queued asset counter.

- **Mutant:** [`1409.sol`](1409.sol)
- **Caught by:** [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1409`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_valid_state.conf --rule queuedAssetCounterMatchesOutstandingRows`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -66,7 +66,7 @@
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
 
-        uint32 assetCounter = (assetQueue.deposits != 0 || assetQueue.withdrawals != 0) ? 1 : 0;
+        uint32 assetCounter = (assetQueue.deposits != 0 && assetQueue.withdrawals != 0) ? 1 : 0; // MUTATION: nonempty-row test narrowed to both sides
 
         data = ISpokeMessageSender.UpdateData({
             netAmount: (assetQueue.deposits >= assetQueue.withdrawals)
```

## SnapshotQueue #1410

flushAssets releases the queued asset counter but leaves the deposits behind, so a still-loaded row is reported as drained.

- **Mutant:** [`1410.sol`](1410.sol)
- **Caught by:** [`queuedAssetCounterMatchesOutstandingRows`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_valid_state.spec#L15)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1410`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_valid_state.conf --rule queuedAssetCounterMatchesOutstandingRows`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -77,7 +77,7 @@
             nonce: shareQueue.nonce
         });
 
-        assetQueue.deposits = 0;
+        // MUTATION: removed the deposit clear on asset flush
         assetQueue.withdrawals = 0;
         shareQueue.nonce++;
         shareQueue.queuedAssetCounter -= assetCounter;
```

## SnapshotQueue #1411

flushAssets clears only the deposit side of the queue it hands over, so a drained asset queue keeps its withdrawals.

- **Mutant:** [`1411.sol`](1411.sol)
- **Caught by:** [`stSqAssetFlushEmptiesTheRowAndSpendsOneOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L47)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1411`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule stSqAssetFlushEmptiesTheRowAndSpendsOneOrdinal`

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

## SnapshotQueue #1412

flushShares spends a nonce without clearing the net it hands over, so the remainder stays queued under a spent nonce.

- **Mutant:** [`1412.sol`](1412.sol)
- **Caught by:** [`stSqShareFlushHandsOverTheWholeNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L69)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1412`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule stSqShareFlushHandsOverTheWholeNet`

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

## SnapshotQueue #1413

queueAssets advances the queue nonce when it opens an asset row, so a nonce is spent with no update sent.

- **Mutant:** [`1413.sol`](1413.sol)
- **Caught by:** [`stSqOpeningAnAssetRowSpendsNoOrdinalAndMovesNoShareNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L87)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1413`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule stSqOpeningAnAssetRowSpendsNoOrdinalAndMovesNoShareNet`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -34,7 +34,11 @@
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
-        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
+        // MUTATION: opening a queue also spends an ordinal
+        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) {
+            shareQueue.queuedAssetCounter++;
+            shareQueue.nonce++;
+        }
 
         if (isIncrease) assetQueue.deposits += amount;
         else assetQueue.withdrawals += amount;
```

## SnapshotQueue #1414

queueAssets loses the else, so a queued deposit is also recorded as a withdrawal of the same asset.

- **Mutant:** [`1414.sol`](1414.sol)
- **Caught by:** [`stSqAssetFlowTakesOneSideOnly`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L104)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1414`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule stSqAssetFlowTakesOneSideOnly`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -37,7 +37,7 @@
         if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
 
         if (isIncrease) assetQueue.deposits += amount;
-        else assetQueue.withdrawals += amount;
+        assetQueue.withdrawals += amount; // MUTATION: the else is gone, so both sides move
 
         emit QueueAssets(poolId, scId, assetId, amount, isIncrease);
     }
```

## SnapshotQueue #1415

queueSharesPair queues one share delta for two pools, so one call moves two pools' share rows.

- **Mutant:** [`1415.sol`](1415.sol)
- **Caught by:** [`stSqShareRowIsPerPool`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_multi_pool_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1415`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/multi_pool_properties.conf --rule stSqShareRowIsPerPool`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -51,6 +51,25 @@
             _netShares(shareQueue.delta, shareQueue.isPositive, shares, isIssuance);
 
         emit QueueShares(poolId, scId, shares, isIssuance);
+    }
+
+    /// @notice MUTATION: queues one share delta for two pools, writing both pools' share rows.
+    function queueSharesPair(
+        PoolId poolId,
+        PoolId siblingPoolId,
+        ShareClassId scId,
+        ShareClassId siblingScId,
+        uint128 shares,
+        bool isIssuance
+    ) external auth {
+        if (shares == 0) return;
+
+        ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
+        ShareQueueAmount storage sibling = queuedShares[siblingPoolId][siblingScId];
+        (shareQueue.delta, shareQueue.isPositive) =
+            _netShares(shareQueue.delta, shareQueue.isPositive, shares, isIssuance);
+        (sibling.delta, sibling.isPositive) =
+            _netShares(sibling.delta, sibling.isPositive, shares, isIssuance);
     }
 
     //----------------------------------------------------------------------------------------------
```

## SnapshotQueue #1416

queueAssetsPair queues one asset flow for two pools, so one call moves two pools' asset rows and both share counters.

- **Mutant:** [`1416.sol`](1416.sol)
- **Caught by:** [`stSqAssetRowIsPerPool`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_multi_pool_properties.spec#L32) · [`stSqQueueSidesDoNotCrossPools`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_multi_pool_properties.spec#L53)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1416`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/multi_pool_properties.conf --rule stSqAssetRowIsPerPool stSqQueueSidesDoNotCrossPools`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -51,6 +51,35 @@
             _netShares(shareQueue.delta, shareQueue.isPositive, shares, isIssuance);
 
         emit QueueShares(poolId, scId, shares, isIssuance);
+    }
+
+    /// @notice MUTATION: queues one asset flow for two pools, writing both pools' asset rows.
+    function queueAssetsPair(
+        PoolId poolId,
+        PoolId siblingPoolId,
+        ShareClassId scId,
+        ShareClassId siblingScId,
+        AssetId assetId,
+        uint128 amount,
+        bool isIncrease
+    ) external auth {
+        if (amount == 0) return;
+
+        ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
+        AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
+        ShareQueueAmount storage siblingShares = queuedShares[siblingPoolId][siblingScId];
+        AssetQueueAmount storage siblingAssets = queuedAssets[siblingPoolId][siblingScId][assetId];
+
+        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
+        if (siblingAssets.deposits == 0 && siblingAssets.withdrawals == 0) siblingShares.queuedAssetCounter++;
+
+        if (isIncrease) {
+            assetQueue.deposits += amount;
+            siblingAssets.deposits += amount;
+        } else {
+            assetQueue.withdrawals += amount;
+            siblingAssets.withdrawals += amount;
+        }
     }
 
     //----------------------------------------------------------------------------------------------
```

## SnapshotQueue #1417

flushAssets rewinds the nonce instead of advancing it, so a later report is filed under a number the hub has already seen.

- **Mutant:** [`1417.sol`](1417.sol)
- **Caught by:** [`stSqNonceAdvancesByAtMostOne`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1417`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule stSqNonceAdvancesByAtMostOne`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -79,7 +79,7 @@
 
         assetQueue.deposits = 0;
         assetQueue.withdrawals = 0;
-        shareQueue.nonce++;
+        shareQueue.nonce--; // MUTATION: the ordinal goes back
         shareQueue.queuedAssetCounter -= assetCounter;
 
         emit SubmitQueuedAssets(poolId, scId, assetId, data);
```

## SnapshotQueue #1419

flushShares advances the nonce by two, so the hub rejects every later report as out of order.

- **Mutant:** [`1419.sol`](1419.sol)
- **Caught by:** [`stSqNonceAdvancesByAtMostOne`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 1419`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule stSqNonceAdvancesByAtMostOne`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -102,7 +102,7 @@
 
         shareQueue.delta = 0;
         shareQueue.isPositive = false;
-        shareQueue.nonce++;
+        shareQueue.nonce += 2; // MUTATION: the ordinal jumps by two
 
         emit SubmitQueuedShares(poolId, scId, data);
     }
```

## SnapshotQueue #5100

queueAssets runs without the ward gate, so any caller moves a pool's asset rows and the count of queued assets.

- **Mutant:** [`5100.sol`](5100.sol)
- **Caught by:** [`acSqOnlyAWardMovesAnAssetRow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L23) · [`acSqOnlyAWardMovesTheOutstandingAssetCount`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L43)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5100`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_access_control.conf --rule acSqOnlyAWardMovesAnAssetRow acSqOnlyAWardMovesTheOutstandingAssetCount`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -28,7 +28,7 @@
     /// @inheritdoc ISnapshotQueue
     function queueAssets(PoolId poolId, ShareClassId scId, AssetId assetId, uint128 amount, bool isIncrease)
         external
-        auth
+        // MUTATION: queueing an asset flow no longer requires a ward
     {
         if (amount == 0) return;
 
```

## SnapshotQueue #5101

flushShares runs without the ward gate, so any caller hands a pool's queued share net to the hub and spends a report nonce.

- **Mutant:** [`5101.sol`](5101.sol)
- **Caught by:** [`acSqOnlyAWardMovesTheShareNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L4) · [`acSqOnlyAWardSpendsAFlushOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L60)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5101`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_access_control.conf --rule acSqOnlyAWardMovesTheShareNet acSqOnlyAWardSpendsAFlushOrdinal`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -88,7 +88,7 @@
     /// @inheritdoc ISnapshotQueue
     function flushShares(PoolId poolId, ShareClassId scId)
         external
-        auth
+        // MUTATION: handing over the queued share net no longer requires a ward
         returns (ISpokeMessageSender.UpdateData memory data)
     {
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
```

## SnapshotQueue #5102

rely runs without the ward gate in the shared Auth mixin, so any caller seats itself among the wards that move the whole queue.

- **Mutant:** [`5102.sol`](5102.sol)
- **Caught by:** [`acSqOnlyAWardMovesTheWardBit`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_access_control.spec#L76)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5102`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_access_control.conf --rule acSqOnlyAWardMovesTheWardBit`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -22,7 +22,7 @@
     }
 
     /// @inheritdoc IAuth
-    function rely(address user) public auth {
+    function rely(address user) public { // MUTATION: granting authority over the queue no longer requires a ward
         wards[user] = 1;
         emit Rely(user);
     }
```

## SnapshotQueue #5103

flushShares reports a snapshot while one asset row is still queued, so the hub reads a half applied balance sheet.

- **Mutant:** [`5103.sol`](5103.sol)
- **Caught by:** [`hlSqShareFlushReportsATruthfulSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L6) · [`hlSqZeroAmountQueueingCannotStallTheSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L169)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5103`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqShareFlushReportsATruthfulSnapshot hlSqZeroAmountQueueingCannotStallTheSnapshot`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -96,7 +96,7 @@
         data = ISpokeMessageSender.UpdateData({
             netAmount: shareQueue.delta,
             isIncrease: shareQueue.isPositive,
-            isSnapshot: shareQueue.queuedAssetCounter == 0,
+            isSnapshot: shareQueue.queuedAssetCounter <= 1, // MUTATION: one outstanding asset row still reads as in sync
             nonce: shareQueue.nonce
         });
 
```

## SnapshotQueue #5104

flushAssets reports a snapshot without checking the share net is zero, so a class with queued shares reads as in sync.

- **Mutant:** [`5104.sol`](5104.sol)
- **Caught by:** [`hlSqAssetFlushReportsATruthfulSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L20)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5104`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqAssetFlushReportsATruthfulSnapshot`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -73,7 +73,7 @@
                 ? assetQueue.deposits - assetQueue.withdrawals
                 : assetQueue.withdrawals - assetQueue.deposits,
             isIncrease: assetQueue.deposits > assetQueue.withdrawals,
-            isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
+            isSnapshot: shareQueue.queuedAssetCounter == assetCounter, // MUTATION: the zero share net requirement is dropped
             nonce: shareQueue.nonce
         });
 
```

## SnapshotQueue #5105

flushAssets reports deposits plus withdrawals instead of their net, so the hub can book more asset movement than happened.

- **Mutant:** [`5105.sol`](5105.sol)
- **Caught by:** [`hlSqAssetPayloadCarriesTheNetMagnitude`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5105`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqAssetPayloadCarriesTheNetMagnitude`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -69,9 +69,7 @@
         uint32 assetCounter = (assetQueue.deposits != 0 || assetQueue.withdrawals != 0) ? 1 : 0;
 
         data = ISpokeMessageSender.UpdateData({
-            netAmount: (assetQueue.deposits >= assetQueue.withdrawals)
-                ? assetQueue.deposits - assetQueue.withdrawals
-                : assetQueue.withdrawals - assetQueue.deposits,
+            netAmount: assetQueue.deposits + assetQueue.withdrawals, // MUTATION: the gross traffic is reported instead of the net
             isIncrease: assetQueue.deposits > assetQueue.withdrawals,
             isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
             nonce: shareQueue.nonce
```

## SnapshotQueue #5106

flushAssets marks a row with equal deposits and withdrawals as an increase, so a zero net reaches the hub as a deposit.

- **Mutant:** [`5106.sol`](5106.sol)
- **Caught by:** [`hlSqAssetPayloadPointsTowardTheLargerSide`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L58)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5106`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqAssetPayloadPointsTowardTheLargerSide`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -72,7 +72,7 @@
             netAmount: (assetQueue.deposits >= assetQueue.withdrawals)
                 ? assetQueue.deposits - assetQueue.withdrawals
                 : assetQueue.withdrawals - assetQueue.deposits,
-            isIncrease: assetQueue.deposits > assetQueue.withdrawals,
+            isIncrease: assetQueue.deposits >= assetQueue.withdrawals, // MUTATION: an exactly offsetting row reports as a deposit surplus
             isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
             nonce: shareQueue.nonce
         });
```

## SnapshotQueue #5107

the share flush reports nothing whenever the queued net leans toward revocation, so shares a pool has revoked never reach the hub.

- **Mutant:** [`5107.sol`](5107.sol)
- **Caught by:** [`hlSqSharePayloadCarriesTheNetMagnitude`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L78)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5107`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqSharePayloadCarriesTheNetMagnitude`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -94,7 +94,7 @@
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
 
         data = ISpokeMessageSender.UpdateData({
-            netAmount: shareQueue.delta,
+            netAmount: shareQueue.isPositive ? shareQueue.delta : 0, // MUTATION: a queued revocation is reported as nothing
             isIncrease: shareQueue.isPositive,
             isSnapshot: shareQueue.queuedAssetCounter == 0,
             nonce: shareQueue.nonce
```

## SnapshotQueue #5108

a queued net that flips direction keeps its old sign, so the hub receives a revocation as an issuance or vice versa.

- **Mutant:** [`5108.sol`](5108.sol)
- **Caught by:** [`hlSqSharePayloadCarriesTheNetSign`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L97)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5108`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqSharePayloadCarriesTheNetSign`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -127,7 +127,7 @@
             newIsPositive = newDelta != 0 && isPositive;
         } else {
             newDelta = shares - delta;
-            newIsPositive = isIssuance;
+            newIsPositive = isPositive; // MUTATION: a net that flips direction keeps the sign it had
         }
     }
 }
```

## SnapshotQueue #5109

the asset flush drains only the side its payload pointed at, so the opposite side survives and is submitted to the hub a second time.

- **Mutant:** [`5109.sol`](5109.sol)
- **Caught by:** [`hlSqSecondAssetFlushReportsNothing`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L116)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5109`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqSecondAssetFlushReportsNothing`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -77,8 +77,8 @@
             nonce: shareQueue.nonce
         });
 
-        assetQueue.deposits = 0;
-        assetQueue.withdrawals = 0;
+        if (data.isIncrease) assetQueue.deposits = 0;
+        else assetQueue.withdrawals = 0; // MUTATION: only the side the payload reported is drained
         shareQueue.nonce++;
         shareQueue.queuedAssetCounter -= assetCounter;
 
```

## SnapshotQueue #5110

the share flush clears the queued net only for an issuance, so a queued revocation is reported to the hub again.

- **Mutant:** [`5110.sol`](5110.sol)
- **Caught by:** [`hlSqSecondShareFlushReportsNothing`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5110`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqSecondShareFlushReportsNothing`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -100,7 +100,7 @@
             nonce: shareQueue.nonce
         });
 
-        shareQueue.delta = 0;
+        if (shareQueue.isPositive) shareQueue.delta = 0; // MUTATION: only an issuance net is consumed by the flush
         shareQueue.isPositive = false;
         shareQueue.nonce++;
 
```

## SnapshotQueue #5111

a flush of an empty asset row spends no nonce, so two consecutive asset reports reach the hub filed under the same number.

- **Mutant:** [`5111.sol`](5111.sol)
- **Caught by:** [`hlSqConsecutiveAssetFlushesSpendConsecutiveOrdinals`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L141)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5111`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqConsecutiveAssetFlushesSpendConsecutiveOrdinals`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -79,7 +79,7 @@
 
         assetQueue.deposits = 0;
         assetQueue.withdrawals = 0;
-        shareQueue.nonce++;
+        if (assetCounter != 0) shareQueue.nonce++; // MUTATION: a flush of an empty asset row spends no ordinal
         shareQueue.queuedAssetCounter -= assetCounter;
 
         emit SubmitQueuedAssets(poolId, scId, assetId, data);
```

## SnapshotQueue #5112

a flush of an empty share net spends no nonce, so two consecutive share reports reach the hub filed under the same number.

- **Mutant:** [`5112.sol`](5112.sol)
- **Caught by:** [`hlSqConsecutiveShareFlushesSpendConsecutiveOrdinals`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L155)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5112`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqConsecutiveShareFlushesSpendConsecutiveOrdinals`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -102,7 +102,7 @@
 
         shareQueue.delta = 0;
         shareQueue.isPositive = false;
-        shareQueue.nonce++;
+        if (data.netAmount != 0) shareQueue.nonce++; // MUTATION: a flush of an empty share net spends no ordinal
 
         emit SubmitQueuedShares(poolId, scId, data);
     }
```

## SnapshotQueue #5113

queueShares spends a report nonce, so the spoke's report stream advances without any queue being handed over.

- **Mutant:** [`5113.sol`](5113.sol)
- **Caught by:** [`vtSqOnlyAFlushSpendsAnOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L30)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5113`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule vtSqOnlyAFlushSpendsAnOrdinal`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -49,6 +49,7 @@
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         (shareQueue.delta, shareQueue.isPositive) =
             _netShares(shareQueue.delta, shareQueue.isPositive, shares, isIssuance);
+        shareQueue.nonce++; // MUTATION: queueing a share delta also spends a flush ordinal
 
         emit QueueShares(poolId, scId, shares, isIssuance);
     }
```

## SnapshotQueue #5114

queueAssets adds to a side without the overflow check, so an oversized total wraps to a small one instead of reverting.

- **Mutant:** [`5114.sol`](5114.sol)
- **Caught by:** [`hlSqAssetPayloadPointsTowardTheLargerSide`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L58)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5114`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqAssetPayloadPointsTowardTheLargerSide`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -36,8 +36,11 @@
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
         if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
 
-        if (isIncrease) assetQueue.deposits += amount;
-        else assetQueue.withdrawals += amount;
+        // MUTATION: the accumulator width check is gone, so an overflowing side wraps instead of reverting
+        unchecked {
+            if (isIncrease) assetQueue.deposits += amount;
+            else assetQueue.withdrawals += amount;
+        }
 
         emit QueueAssets(poolId, scId, assetId, amount, isIncrease);
     }
```

## SnapshotQueue #5115

the share netting grows the queued net with the width check removed, so a net that outgrows its width wraps instead of refusing the call.

- **Mutant:** [`5115.sol`](5115.sol)
- **Caught by:** [`hlSqSharePayloadCarriesTheNetMagnitude`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L78)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5115`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqSharePayloadCarriesTheNetMagnitude`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -120,7 +120,7 @@
         returns (uint128 newDelta, bool newIsPositive)
     {
         if (isIssuance == isPositive || delta == 0) {
-            newDelta = delta + shares;
+            unchecked { newDelta = delta + shares; } // MUTATION: the net width check is gone, so a growing net wraps instead of reverting
             newIsPositive = newDelta != 0 && isIssuance;
         } else if (delta >= shares) {
             newDelta = delta - shares;
```

## SnapshotQueue #5116

the asset flush always releases one pending row, so flushing an empty row can underflow the count and revert.

- **Mutant:** [`5116.sol`](5116.sol)
- **Caught by:** [`rvSqFlushAssetsAlwaysAdmitsAWardWhileOrdinalsRemain`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L91)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5116`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reverts.conf --rule rvSqFlushAssetsAlwaysAdmitsAWardWhileOrdinalsRemain`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -80,7 +80,7 @@
         assetQueue.deposits = 0;
         assetQueue.withdrawals = 0;
         shareQueue.nonce++;
-        shareQueue.queuedAssetCounter -= assetCounter;
+        shareQueue.queuedAssetCounter -= 1; // MUTATION: every flush releases one row, so an empty flush underflows the count
 
         emit SubmitQueuedAssets(poolId, scId, assetId, data);
     }
```

## SnapshotQueue #5117

the share flush advances its nonce with the width check removed, so an exhausted nonce wraps back to the start instead of refusing the call.

- **Mutant:** [`5117.sol`](5117.sol)
- **Caught by:** [`stSqNonceAdvancesByAtMostOne`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5117`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule stSqNonceAdvancesByAtMostOne`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -102,7 +102,7 @@
 
         shareQueue.delta = 0;
         shareQueue.isPositive = false;
-        shareQueue.nonce++;
+        unchecked { shareQueue.nonce++; } // MUTATION: the ordinal stream wraps at its width instead of reverting
 
         emit SubmitQueuedShares(poolId, scId, data);
     }
```

## SnapshotQueue #5121

the asset flush clears the row only on a snapshot, so the next flush resubmits totals the hub already has.

- **Mutant:** [`5121.sol`](5121.sol)
- **Caught by:** [`hlSqSecondAssetFlushReportsNothing`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L116)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5121`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqSecondAssetFlushReportsNothing`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -77,8 +77,10 @@
             nonce: shareQueue.nonce
         });
 
-        assetQueue.deposits = 0;
-        assetQueue.withdrawals = 0;
+        if (data.isSnapshot) { // MUTATION: the asset row is drained only when the flush claimed a snapshot
+            assetQueue.deposits = 0;
+            assetQueue.withdrawals = 0;
+        }
         shareQueue.nonce++;
         shareQueue.queuedAssetCounter -= assetCounter;
 
```

## SnapshotQueue #5122

queueAssetsTwoRows queues one flow into two asset rows of the same class, so a single call moves the amounts another asset still has waiting.

- **Mutant:** [`5122.sol`](5122.sol)
- **Caught by:** [`vtSqAssetRowsMoveOneAtATime`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 5122`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule vtSqAssetRowsMoveOneAtATime`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -40,6 +40,33 @@
         else assetQueue.withdrawals += amount;
 
         emit QueueAssets(poolId, scId, assetId, amount, isIncrease);
+    }
+
+    /// @notice MUTATION: queues one asset flow into two asset rows of the same pool and share class.
+    function queueAssetsTwoRows(
+        PoolId poolId,
+        ShareClassId scId,
+        AssetId assetId,
+        AssetId otherAssetId,
+        uint128 amount,
+        bool isIncrease
+    ) external auth {
+        if (amount == 0) return;
+
+        ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
+        AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
+        AssetQueueAmount storage otherQueue = queuedAssets[poolId][scId][otherAssetId];
+
+        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
+        if (otherQueue.deposits == 0 && otherQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
+
+        if (isIncrease) {
+            assetQueue.deposits += amount;
+            otherQueue.deposits += amount;
+        } else {
+            assetQueue.withdrawals += amount;
+            otherQueue.withdrawals += amount;
+        }
     }
 
     /// @inheritdoc ISnapshotQueue
```

## SnapshotQueue #6300

queueAssets skips every nonzero amount, so real flows never queue and a zero amount counts an empty row as waiting.

- **Mutant:** [`6300.sol`](6300.sol)
- **Caught by:** [`rcSqQueueAssetsCanOpenADepositRow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L4) · [`rcSqQueueAssetsCanOpenAWithdrawalRow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L19) · [`rcSqZeroAmountQueueLeavesTheSnapshotAvailable`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L117)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6300`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqQueueAssetsCanOpenADepositRow rcSqQueueAssetsCanOpenAWithdrawalRow rcSqZeroAmountQueueLeavesTheSnapshotAvailable`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -30,7 +30,7 @@
         external
         auth
     {
-        if (amount == 0) return;
+        if (amount != 0) return; // MUTATION: only a zero amount is queued, every real flow returns untouched
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
```

## SnapshotQueue #6301

queueAssets books a deposit as a withdrawal and a withdrawal as a deposit, so the hub receives every asset flow reversed.

- **Mutant:** [`6301.sol`](6301.sol)
- **Caught by:** [`rcSqQueueAssetsCanAbsorbTheFullAccumulatorWidth`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L86) · [`rcSqQueueAssetsCanMakeAClassOutstandingWithOneUnit`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L102) · [`rcSqQueuedAssetsViewCanReadBackAFreshFlow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L602)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6301`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqQueueAssetsCanAbsorbTheFullAccumulatorWidth rcSqQueueAssetsCanMakeAClassOutstandingWithOneUnit rcSqQueuedAssetsViewCanReadBackAFreshFlow`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -36,8 +36,9 @@
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
         if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
 
-        if (isIncrease) assetQueue.deposits += amount;
-        else assetQueue.withdrawals += amount;
+        // MUTATION: the two sides are swapped, so a deposit is queued as a withdrawal and the reverse
+        if (isIncrease) assetQueue.withdrawals += amount;
+        else assetQueue.deposits += amount;
 
         emit QueueAssets(poolId, scId, assetId, amount, isIncrease);
     }
```

## SnapshotQueue #6302

queueAssets counts a row only when it is already loaded, so the outstanding count moves on later flows, not the first.

- **Mutant:** [`6302.sol`](6302.sol)
- **Caught by:** [`rcSqQueueAssetsCanAccumulateASecondDeposit`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L34) · [`rcSqQueueAssetsCanLeaveThreeAssetsOutstandingAtOnce`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L69)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6302`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqQueueAssetsCanAccumulateASecondDeposit rcSqQueueAssetsCanLeaveThreeAssetsOutstandingAtOnce`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -34,7 +34,7 @@
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
-        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
+        if (assetQueue.deposits != 0 || assetQueue.withdrawals != 0) shareQueue.queuedAssetCounter++; // MUTATION: a row is counted when it is already loaded rather than when it is opened
 
         if (isIncrease) assetQueue.deposits += amount;
         else assetQueue.withdrawals += amount;
```

## SnapshotQueue #6303

queueAssets bumps the outstanding count on every call, zero amounts included, so the count runs ahead of the waiting rows.

- **Mutant:** [`6303.sol`](6303.sol)
- **Caught by:** [`rcSqQueueAssetsCanHoldBothSidesOfOneRow`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L53)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6303`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqQueueAssetsCanHoldBothSidesOfOneRow`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -30,8 +30,7 @@
         external
         auth
     {
-        if (amount == 0) return;
-
+        queuedShares[poolId][scId].queuedAssetCounter++; // MUTATION: every call counts the row again, zero amounts and already open rows alike
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
         if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
```

## SnapshotQueue #6304

queueShares turns away every real share delta and lets only a zero one through, so a mint or a burn never reaches the queued net.

- **Mutant:** [`6304.sol`](6304.sol)
- **Caught by:** [`rcSqQueueSharesCanOpenAnIssuanceNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L134) · [`rcSqQueueSharesCanOpenARevocationNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L149) · [`rcSqQueueSharesCanAbsorbTheFullNetWidth`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L213)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6304`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqQueueSharesCanOpenAnIssuanceNet rcSqQueueSharesCanOpenARevocationNet rcSqQueueSharesCanAbsorbTheFullNetWidth`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -44,7 +44,7 @@
 
     /// @inheritdoc ISnapshotQueue
     function queueShares(PoolId poolId, ShareClassId scId, uint128 shares, bool isIssuance) external auth {
-        if (shares == 0) return;
+        if (shares != 0) return; // MUTATION: only a zero share delta is netted, every real one returns untouched
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         (shareQueue.delta, shareQueue.isPositive) =
```

## SnapshotQueue #6305

queueShares ignores a delta in the net's own direction or on an empty net, so nothing can open or grow it.

- **Mutant:** [`6305.sol`](6305.sol)
- **Caught by:** [`rcSqQueueSharesCanGrowAnIssuanceNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L164) · [`rcSqALargerRevocationCanFlipTheQueuedNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L247) · [`rcSqQueuedSharesViewCanReadBackAFreshNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L582)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6305`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqQueueSharesCanGrowAnIssuanceNet rcSqALargerRevocationCanFlipTheQueuedNet rcSqQueuedSharesViewCanReadBackAFreshNet`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -120,7 +120,7 @@
         returns (uint128 newDelta, bool newIsPositive)
     {
         if (isIssuance == isPositive || delta == 0) {
-            newDelta = delta + shares;
+            newDelta = delta; // MUTATION: a delta in the direction the net already points adds nothing
             newIsPositive = newDelta != 0 && isIssuance;
         } else if (delta >= shares) {
             newDelta = delta - shares;
```

## SnapshotQueue #6306

an opposing share delta no longer eats into the waiting net, so a revocation can neither shrink a queued issuance nor cancel it.

- **Mutant:** [`6306.sol`](6306.sol)
- **Caught by:** [`rcSqQueueSharesCanShrinkAnIssuanceNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L181) · [`rcSqQueueSharesCanCancelAnIssuanceNetExactly`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L198)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6306`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqQueueSharesCanShrinkAnIssuanceNet rcSqQueueSharesCanCancelAnIssuanceNetExactly`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -123,7 +123,7 @@
             newDelta = delta + shares;
             newIsPositive = newDelta != 0 && isIssuance;
         } else if (delta >= shares) {
-            newDelta = delta - shares;
+            newDelta = delta; // MUTATION: an opposing delta no longer eats into the waiting net
             newIsPositive = newDelta != 0 && isPositive;
         } else {
             newDelta = shares - delta;
```

## SnapshotQueue #6307

flushShares reports the queued net with its direction reversed, so an issuance reaches the hub as a revocation.

- **Mutant:** [`6307.sol`](6307.sol)
- **Caught by:** [`rcSqZeroShareQueueLeavesTheNetPayloadIntact`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L228) · [`rcSqShareFlushCanHandOverAnIssuanceAndReportASnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L400)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6307`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqZeroShareQueueLeavesTheNetPayloadIntact rcSqShareFlushCanHandOverAnIssuanceAndReportASnapshot`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -95,7 +95,7 @@
 
         data = ISpokeMessageSender.UpdateData({
             netAmount: shareQueue.delta,
-            isIncrease: shareQueue.isPositive,
+            isIncrease: !shareQueue.isPositive, // MUTATION: the share payload is reported with its direction reversed
             isSnapshot: shareQueue.queuedAssetCounter == 0,
             nonce: shareQueue.nonce
         });
```

## SnapshotQueue #6308

flushShares flags a snapshot exactly when an asset row is still outstanding, so the flag reads backwards on every share report.

- **Mutant:** [`6308.sol`](6308.sol)
- **Caught by:** [`rcSqShareFlushCanHandOverARevocationAndReportASnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L423) · [`rcSqShareFlushWithAnAssetRowOutstandingCanReportNoSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L441) · [`rcSqEmptyShareFlushStillSpendsAnOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L458)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6308`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqShareFlushCanHandOverARevocationAndReportASnapshot rcSqShareFlushWithAnAssetRowOutstandingCanReportNoSnapshot rcSqEmptyShareFlushStillSpendsAnOrdinal`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -96,7 +96,7 @@
         data = ISpokeMessageSender.UpdateData({
             netAmount: shareQueue.delta,
             isIncrease: shareQueue.isPositive,
-            isSnapshot: shareQueue.queuedAssetCounter == 0,
+            isSnapshot: shareQueue.queuedAssetCounter != 0, // MUTATION: the class reads as in sync exactly when an asset row is still outstanding
             nonce: shareQueue.nonce
         });
 
```

## SnapshotQueue #6309

the share flush no longer spends a report nonce, so two consecutive share reports reach the hub filed under the same number.

- **Mutant:** [`6309.sol`](6309.sol)
- **Caught by:** [`hlSqConsecutiveShareFlushesSpendConsecutiveOrdinals`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L155)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6309`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqConsecutiveShareFlushesSpendConsecutiveOrdinals`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -102,7 +102,7 @@
 
         shareQueue.delta = 0;
         shareQueue.isPositive = false;
-        shareQueue.nonce++;
+        // MUTATION: the share flush no longer spends a report ordinal
 
         emit SubmitQueuedShares(poolId, scId, data);
     }
```

## SnapshotQueue #6310

flushAssets advances the nonce by two, so the hub rejects every later report as out of order.

- **Mutant:** [`6310.sol`](6310.sol)
- **Caught by:** [`rcSqAssetFlushCanHandOverAndReportASnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L268) · [`rcSqEmptyAssetFlushStillSpendsAnOrdinal`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L358)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6310`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqAssetFlushCanHandOverAndReportASnapshot rcSqEmptyAssetFlushStillSpendsAnOrdinal`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -79,7 +79,7 @@
 
         assetQueue.deposits = 0;
         assetQueue.withdrawals = 0;
-        shareQueue.nonce++;
+        shareQueue.nonce += 2; // MUTATION: the asset flush spends two report ordinals where one is due
         shareQueue.queuedAssetCounter -= assetCounter;
 
         emit SubmitQueuedAssets(poolId, scId, assetId, data);
```

## SnapshotQueue #6311

the asset flush reports every payload as a withdrawal, so a queued deposit reaches the hub pointing out of the pool.

- **Mutant:** [`6311.sol`](6311.sol)
- **Caught by:** [`rcSqAssetFlushCanNetTowardTheDepositSide`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L322)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6311`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqAssetFlushCanNetTowardTheDepositSide`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -72,7 +72,7 @@
             netAmount: (assetQueue.deposits >= assetQueue.withdrawals)
                 ? assetQueue.deposits - assetQueue.withdrawals
                 : assetQueue.withdrawals - assetQueue.deposits,
-            isIncrease: assetQueue.deposits > assetQueue.withdrawals,
+            isIncrease: false, // MUTATION: every asset payload is reported as a withdrawal
             isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
             nonce: shareQueue.nonce
         });
```

## SnapshotQueue #6312

the asset flush reports every payload as a deposit, so a queued withdrawal reaches the hub pointing into the pool.

- **Mutant:** [`6312.sol`](6312.sol)
- **Caught by:** [`rcSqAssetFlushCanNetTowardTheWithdrawalSide`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L340) · [`rcSqOffsettingRowCanFlushZeroYetClearTheCount`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L380)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6312`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqAssetFlushCanNetTowardTheWithdrawalSide rcSqOffsettingRowCanFlushZeroYetClearTheCount`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -72,7 +72,7 @@
             netAmount: (assetQueue.deposits >= assetQueue.withdrawals)
                 ? assetQueue.deposits - assetQueue.withdrawals
                 : assetQueue.withdrawals - assetQueue.deposits,
-            isIncrease: assetQueue.deposits > assetQueue.withdrawals,
+            isIncrease: true, // MUTATION: every asset payload is reported as a deposit
             isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
             nonce: shareQueue.nonce
         });
```

## SnapshotQueue #6313

the asset flush always tells the hub the class is in sync, so a partial hand over is reported as a complete one.

- **Mutant:** [`6313.sol`](6313.sol)
- **Caught by:** [`rcSqAssetFlushWithASiblingRowOutstandingCanReportNoSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L290) · [`rcSqAnOutOfSyncClassCanBeBroughtBackIntoSync`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L478)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6313`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqAssetFlushWithASiblingRowOutstandingCanReportNoSnapshot rcSqAnOutOfSyncClassCanBeBroughtBackIntoSync`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -73,7 +73,7 @@
                 ? assetQueue.deposits - assetQueue.withdrawals
                 : assetQueue.withdrawals - assetQueue.deposits,
             isIncrease: assetQueue.deposits > assetQueue.withdrawals,
-            isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
+            isSnapshot: true, // MUTATION: the asset flush always tells the hub the class is in sync
             nonce: shareQueue.nonce
         });
 
```

## SnapshotQueue #6314

the asset flush counts the row it just drained a second time instead of striking it off, so the outstanding count only ever grows.

- **Mutant:** [`6314.sol`](6314.sol)
- **Caught by:** [`rcSqAssetFlushWithSharesOutstandingCanReportNoSnapshot`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L306) · [`rcSqAnAssetRowCanBeReusedAfterAFlush`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L505)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6314`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqAssetFlushWithSharesOutstandingCanReportNoSnapshot rcSqAnAssetRowCanBeReusedAfterAFlush`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -80,7 +80,7 @@
         assetQueue.deposits = 0;
         assetQueue.withdrawals = 0;
         shareQueue.nonce++;
-        shareQueue.queuedAssetCounter -= assetCounter;
+        shareQueue.queuedAssetCounter += assetCounter; // MUTATION: the flushed row is counted a second time instead of struck off
 
         emit SubmitQueuedAssets(poolId, scId, assetId, data);
     }
```

## SnapshotQueue #6315

rely seats the caller instead of the account the call names, so a ward can never hand the queue seat on to anyone else.

- **Mutant:** [`6315.sol`](6315.sol)
- **Caught by:** [`rcSqAFreshlyReliedAccountCanMoveTheQueue`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L546)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6315`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqAFreshlyReliedAccountCanMoveTheQueue`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -23,7 +23,7 @@
 
     /// @inheritdoc IAuth
     function rely(address user) public auth {
-        wards[user] = 1;
+        wards[msg.sender] = 1; // MUTATION: the seat is handed to the caller instead of the account the call names
         emit Rely(user);
     }
 
```

## SnapshotQueue #6316

deny leaves the seat it names standing, so authority over the queue can never be taken back once granted.

- **Mutant:** [`6316.sol`](6316.sol)
- **Caught by:** [`rcSqDenyCanRemoveAnotherAccountsQueueSeat`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L531) · [`rcSqAWardCanDenyItself`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reachability.spec#L567)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6316`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reachability.conf --rule rcSqDenyCanRemoveAnotherAccountsQueueSeat rcSqAWardCanDenyItself`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        // MUTATION: the seat the call names is left standing
         emit Deny(user);
     }
 }
```

## SnapshotQueue #6317

queueShares runs without the ward gate, so any caller moves a pool's queued share net.

- **Mutant:** [`6317.sol`](6317.sol)
- **Caught by:** [`rvSqQueueSharesRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L19)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6317`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reverts.conf --rule rvSqQueueSharesRefusesANonWard`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -43,7 +43,7 @@
     }
 
     /// @inheritdoc ISnapshotQueue
-    function queueShares(PoolId poolId, ShareClassId scId, uint128 shares, bool isIssuance) external auth {
+    function queueShares(PoolId poolId, ShareClassId scId, uint128 shares, bool isIssuance) external { // MUTATION: the ward gate is gone
         if (shares == 0) return;
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
```

## SnapshotQueue #6318

flushAssets runs without the ward gate, so any caller hands a pool's queued asset flow to the hub.

- **Mutant:** [`6318.sol`](6318.sol)
- **Caught by:** [`rvSqFlushAssetsRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L34)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6318`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reverts.conf --rule rvSqFlushAssetsRefusesANonWard`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -60,9 +60,9 @@
     /// @inheritdoc ISnapshotQueue
     function flushAssets(PoolId poolId, ShareClassId scId, AssetId assetId)
         external
-        auth
+       
         returns (ISpokeMessageSender.UpdateData memory data)
-    {
+    { // MUTATION: the ward gate is gone
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
 
```

## SnapshotQueue #6319

deny runs without the ward gate, so an account holding no seat strips a ward of its permissions.

- **Mutant:** [`6319.sol`](6319.sol)
- **Caught by:** [`rvSqDenyRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L77)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6319`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reverts.conf --rule rvSqDenyRefusesANonWard`

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

## SnapshotQueue #6320

the share flush leaves one unit on the row it drained, so the view never reports an emptied queue.

- **Mutant:** [`6320.sol`](6320.sol)
- **Caught by:** [`stSqShareFlushHandsOverTheWholeNet`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_transitions.spec#L69)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6320`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_transitions.conf --rule stSqShareFlushHandsOverTheWholeNet`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -100,7 +100,7 @@
             nonce: shareQueue.nonce
         });
 
-        shareQueue.delta = 0;
+        shareQueue.delta = 1; // MUTATION: the share flush leaves one unit behind
         shareQueue.isPositive = false;
         shareQueue.nonce++;
 
```

## SnapshotQueue #6321

the asset flush leaves one unit on the row it drained, so the view never reports an emptied queue.

- **Mutant:** [`6321.sol`](6321.sol)
- **Caught by:** [`hlSqSecondAssetFlushReportsNothing`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_high_level.spec#L116)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6321`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_high_level.conf --rule hlSqSecondAssetFlushReportsNothing`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -77,7 +77,7 @@
             nonce: shareQueue.nonce
         });
 
-        assetQueue.deposits = 0;
+        assetQueue.deposits = 1; // MUTATION: the asset flush leaves one unit behind
         assetQueue.withdrawals = 0;
         shareQueue.nonce++;
         shareQueue.queuedAssetCounter -= assetCounter;
```

## SnapshotQueue #6322

the share flush refuses a queue whose net is already zero, so a ward can no longer spend a nonce on an empty row.

- **Mutant:** [`6322.sol`](6322.sol)
- **Caught by:** [`rvSqFlushSharesAlwaysAdmitsAWardWhileOrdinalsRemain`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L109)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6322`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reverts.conf --rule rvSqFlushSharesAlwaysAdmitsAWardWhileOrdinalsRemain`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -92,6 +92,7 @@
         returns (ISpokeMessageSender.UpdateData memory data)
     {
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
+        require(shareQueue.delta != 0, "nothing queued"); // MUTATION: an emptied share queue can no longer be flushed
 
         data = ISpokeMessageSender.UpdateData({
             netAmount: shareQueue.delta,
```

## SnapshotQueue #6323

the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.

- **Mutant:** [`6323.sol`](6323.sol)
- **Caught by:** [`rvSqFlushSharesRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L49) · [`rvSqQueueAssetsRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L4) · [`rvSqRelyRefusesANonWard`](../../specs/core/spoke/SnapshotQueue/single/SnapshotQueue_single_pool_reverts.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 6323`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/single_pool_reverts.conf --rule rvSqFlushSharesRefusesANonWard rvSqQueueAssetsRefusesANonWard rvSqRelyRefusesANonWard`

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

## SnapshotQueue #9029

opening a new asset queue raises the queued share amount instead of the count of waiting assets, so an asset flow reports shares nobody issued.

- **Mutant:** [`9029.sol`](9029.sol)
- **Caught by:** [`stSqTheShareNetMovesOnlyUnderShareEntries`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 9029`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/unpinned_properties.conf --rule stSqTheShareNetMovesOnlyUnderShareEntries`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -34,7 +34,7 @@
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
-        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
+        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.delta++; // MUTATION: a new asset queue raises the share amount
 
         if (isIncrease) assetQueue.deposits += amount;
         else assetQueue.withdrawals += amount;
```

## SnapshotQueue #9030

a share flush also zeroes the count of waiting asset queues, so the next share flush reports a snapshot while assets still wait.

- **Mutant:** [`9030.sol`](9030.sol)
- **Caught by:** [`stSqAssetQueuesMoveOnlyUnderAssetEntries`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L27)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 9030`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/unpinned_properties.conf --rule stSqAssetQueuesMoveOnlyUnderAssetEntries`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -101,7 +101,7 @@
         });
 
         shareQueue.delta = 0;
-        shareQueue.isPositive = false;
+        shareQueue.isPositive = false; shareQueue.queuedAssetCounter = 0; // MUTATION: the share flush forgets the waiting assets
         shareQueue.nonce++;
 
         emit SubmitQueuedShares(poolId, scId, data);
```

## SnapshotQueue #9360

a row holding only withdrawals is counted again on every new amount, so the queued asset count overstates the waiting rows.

- **Mutant:** [`9360.sol`](9360.sol)
- **Caught by:** [`queuedAssetCounterCountsEveryNonEmptyRow`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_all_assets_properties.spec#L11)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 9360`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/all_assets_properties.conf --rule queuedAssetCounterCountsEveryNonEmptyRow`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -34,7 +34,7 @@
 
         ShareQueueAmount storage shareQueue = queuedShares[poolId][scId];
         AssetQueueAmount storage assetQueue = queuedAssets[poolId][scId][assetId];
-        if (assetQueue.deposits == 0 && assetQueue.withdrawals == 0) shareQueue.queuedAssetCounter++;
+        if (assetQueue.deposits == 0) shareQueue.queuedAssetCounter++; // MUTATION: a row with only withdrawals is counted again
 
         if (isIncrease) assetQueue.deposits += amount;
         else assetQueue.withdrawals += amount;
```

## SnapshotQueue #9361

flushAssets clears the next asset's deposits, not its own, so its own are reported again and the neighbour's lost.

- **Mutant:** [`9361.sol`](9361.sol)
- **Caught by:** [`hlSqAnAssetFlushEmptiesItsOwnRowOnly`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L55)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 9361`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/unpinned_properties.conf --rule hlSqAnAssetFlushEmptiesItsOwnRowOnly`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -77,7 +77,7 @@
             nonce: shareQueue.nonce
         });
 
-        assetQueue.deposits = 0;
+        queuedAssets[poolId][scId][AssetId.wrap(assetId.raw() + 1)].deposits = 0; // MUTATION: the neighbouring asset's deposits are cleared instead of its own
         assetQueue.withdrawals = 0;
         shareQueue.nonce++;
         shareQueue.queuedAssetCounter -= assetCounter;
```

## SnapshotQueue #9362

a share flush bumps the queued asset count instead of the nonce, so the class seems to have one more waiting asset queue.

- **Mutant:** [`9362.sol`](9362.sol)
- **Caught by:** [`hlSqAShareFlushClearsOnlyItsNet`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L84)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 9362`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/unpinned_properties.conf --rule hlSqAShareFlushClearsOnlyItsNet`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -102,7 +102,7 @@
 
         shareQueue.delta = 0;
         shareQueue.isPositive = false;
-        shareQueue.nonce++;
+        shareQueue.queuedAssetCounter++; // MUTATION: the share flush moves the queued asset count
 
         emit SubmitQueuedShares(poolId, scId, data);
     }
```

## SnapshotQueue #9363

a share flush carrying a nonzero share net no longer reports a snapshot, so the hub waits for a sync that already happened.

- **Mutant:** [`9363.sol`](9363.sol)
- **Caught by:** [`hlSqShareFlushSnapshotMeansTheClassIsDrained`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_all_assets_properties.spec#L18)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 9363`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/all_assets_properties.conf --rule hlSqShareFlushSnapshotMeansTheClassIsDrained`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -96,7 +96,7 @@
         data = ISpokeMessageSender.UpdateData({
             netAmount: shareQueue.delta,
             isIncrease: shareQueue.isPositive,
-            isSnapshot: shareQueue.queuedAssetCounter == 0,
+            isSnapshot: shareQueue.queuedAssetCounter == 0 && shareQueue.delta == 0, // MUTATION: the net being handed over is read as still pending
             nonce: shareQueue.nonce
         });
 
```

## SnapshotQueue #9364

an asset flush reports a snapshot while other asset queues still wait, so the hub takes an unsynced class for a synced one.

- **Mutant:** [`9364.sol`](9364.sol)
- **Caught by:** [`hlSqAssetFlushSnapshotMeansTheClassIsDrained`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_all_assets_properties.spec#L34)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 9364`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/all_assets_properties.conf --rule hlSqAssetFlushSnapshotMeansTheClassIsDrained`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -73,7 +73,7 @@
                 ? assetQueue.deposits - assetQueue.withdrawals
                 : assetQueue.withdrawals - assetQueue.deposits,
             isIncrease: assetQueue.deposits > assetQueue.withdrawals,
-            isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter == assetCounter,
+            isSnapshot: shareQueue.delta == 0 && shareQueue.queuedAssetCounter >= assetCounter, // MUTATION: other waiting asset queues still read as a snapshot
             nonce: shareQueue.nonce
         });
 
```

## SnapshotQueue #9365

an asset flush wipes the queued share net instead of advancing the nonce, so share issuance or revocation waiting for the Hub is silently lost.

- **Mutant:** [`9365.sol`](9365.sol)
- **Caught by:** [`hlSqAnAssetFlushEmptiesItsOwnRowOnly`](../../specs/core/spoke/SnapshotQueue/SnapshotQueue_unpinned_properties.spec#L55)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SnapshotQueue 9365`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SnapshotQueue/unpinned_properties.conf --rule hlSqAnAssetFlushEmptiesItsOwnRowOnly`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -79,7 +79,7 @@
 
         assetQueue.deposits = 0;
         assetQueue.withdrawals = 0;
-        shareQueue.nonce++;
+        shareQueue.delta = 0; // MUTATION: an asset flush wipes the share net
         shareQueue.queuedAssetCounter -= assetCounter;
 
         emit SubmitQueuedAssets(poolId, scId, assetId, data);
```

