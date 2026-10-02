# Mutations for `Holdings` (`src/core/hub/Holdings.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [802](#holdings-802) | setSnapshotHook no longer checks that the pool exists, so a snapshot hook can be attached to an unregistered pool.<br>Caught by: [`snapshotHookImpliesPoolExists`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L16) |
| [803](#holdings-803) | setSnapshotHook inverts the pool existence check, accepting unregistered pools and rejecting registered ones.<br>Caught by: [`snapshotHookImpliesPoolExists`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L16) |
| [804](#holdings-804) | increase computes the prior deficit flag with transposed operands, so the deficit counter moves on the wrong transitions.<br>Caught by: [`networkDeficitCountMatchesTheShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L21) |
| [805](#holdings-805) | decrease treats an exactly netted holding as a deficit, bumping the deficit counter on a row that holds no deficit.<br>Caught by: [`networkDeficitCountMatchesTheShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L21) |
| [806](#holdings-806) | the network deficit counter moves in the wrong direction on a deficit-state crossing, incrementing on exit and decrementing on entry.<br>Caught by: [`networkDeficitCountMatchesTheShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L21) |
| [807](#holdings-807) | the deficit no-op guard is inverted, so state crossings are skipped and steady states move the counter.<br>Caught by: [`networkDeficitCountMatchesTheShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L21) |
| [810](#holdings-810) | decrease removes value pro-rata to the remaining amount instead of the removed amount, so a full drain leaves residual value behind.<br>Caught by: [`emptyHoldingCarriesNoValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L32) |
| [811](#holdings-811) | update quotes the cumulative increased amount instead of the current net amount, so an emptied holding is revalued as if still held.<br>Caught by: [`emptyHoldingCarriesNoValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L32) |
| [812](#holdings-812) | setAccountId inverts the initialization check, wiring journal accounts onto holdings that were never initialized.<br>Caught by: [`accountIdImpliesInitialized`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L43) |
| [813](#holdings-813) | initialize stores the account ids but never records the valuation, leaving journal accounts wired to an uninitialized holding.<br>Caught by: [`accountIdImpliesInitialized`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L43) |
| [814](#holdings-814) | setSnapshot marks the row in sync without advancing the nonce, so a synced snapshot still shows an untouched nonce.<br>Caught by: [`snapshotFlagImpliesAStartedNonce`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L38) |
| [815](#holdings-815) | setSnapshot decrements the snapshot nonce instead of incrementing it, so a synced row can return to a zero nonce.<br>Caught by: [`snapshotFlagImpliesAStartedNonce`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L38) |
| [816](#holdings-816) | increase nets the deposit against the outstanding withdrawal instead of only recording it, so one call moves both sides of the flow record.<br>Caught by: [`stHoInflowAndOutflowNeverMoveTogether`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L121) |
| [817](#holdings-817) | transferHolding moves a position between two assets of the same class in one call, so one call restates two holdings.<br>Caught by: [`stHoOneCallTouchesOneHolding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L136) |
| [818](#holdings-818) | increase subtracts the realized value instead of adding it, so a deposit writes the holding's carrying value down.<br>Caught by: [`stHoInflowNeverLowersValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L167) |
| [819](#holdings-819) | decrease adds the removed value instead of subtracting it, so a withdrawal writes the holding's carrying value up.<br>Caught by: [`stHoOutflowNeverRaisesValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L182) |
| [820](#holdings-820) | initialize prices the holding at open off a unit probe, so creation funds a carrying value no deposit ever paid for.<br>Caught by: [`stHoOpeningAHoldingFundsNothing`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L197) |
| [821](#holdings-821) | setSnapshot advances the nonce by two, so a flipped marker skips a nonce.<br>Caught by: [`stHoSnapshotFlagMovesWithItsNonce`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L217) |
| [822](#holdings-822) | migrateHolding moves a holding and its ledger wiring to another pool, so one call writes two pools' books.<br>Caught by: [`stHoHoldingRowIsPerPool`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L7) · [`stHoAccountWiringIsPerPool`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L36) |
| [823](#holdings-823) | setSnapshotPair marks two pools in sync off one round, so one call moves two pools' snapshot rows.<br>Caught by: [`stHoSnapshotRowIsPerPool`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L53) |
| [824](#holdings-824) | increaseFor books flow on one pool while counting its deficit under another, so a pool's flow moves a sibling's counter.<br>Caught by: [`stHoDeficitCountAndHookIgnoreASiblingsFlow`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L74) |
| [825](#holdings-825) | increaseForClass books flow on one class but reads the deficit crossing off another, so the pool's deficit count goes stale.<br>Caught by: [`networkDeficitCountSpansEveryShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L13) |
| [4100](#holdings-4100) | The current amount loses its zero floor, so an overdrawn holding reverts every read and update that computes it.<br>Caught by: [`rvHoDecreaseNeverStallsOnAnOversizedOutflow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L150) · [`rvHoIncreaseBeforeTheRowIsOpenedIsNeverRefusedToAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L131) · [`rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L210) · [`rvHoAmountViewsRefuseOnlyANetPastUint128`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L228) · [`rvHoIncreaseOnAnOpenHoldingFailsOnlyOnAnOverflowingTotalOrValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L246) |
| [4101](#holdings-4101) | initialize no longer refuses an open holding, so reopening it silently overwrites its price source and journal accounts.<br>Caught by: [`rvHoInitializeRefusesANonWardANullSourceOrAnOpenRow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L4) |
| [4102](#holdings-4102) | setAccountId inverts the initialization check, so wiring a journal account is refused on an open holding and accepted on one that was never opened.<br>Caught by: [`rvHoSetAccountIdRefusesANonWardOrAnUnopenedHolding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L21) |
| [4103](#holdings-4103) | updateValuation no longer requires the holding to be open, so a price source can be pinned onto a row the pool never opened.<br>Caught by: [`rvHoUpdateValuationRefusesANonWardANullSourceOrAnUnopenedHolding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L37) |
| [4104](#holdings-4104) | setSnapshotHook no longer checks that the pool exists, so a snapshot hook can be attached to a pool the hub registry does not know.<br>Caught by: [`rvHoSetSnapshotHookRefusesANonWardOrAnUnknownPool`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L54) |
| [4105](#holdings-4105) | setSnapshot no longer checks the nonce it was handed, so a stale or out of order cross network update is accepted instead of refused.<br>Caught by: [`rvHoSetSnapshotRefusesANonWardOrAnOutOfOrderNonce`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L69) |
| [4106](#holdings-4106) | The sync notification also bumps the sequence number, so resending it on a network whose sequence is exhausted reverts.<br>Caught by: [`rvHoCallOnSyncSnapshotIsNeverRefusedToAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L85) |
| [4107](#holdings-4107) | The cross network transfer notice now requires an installed hook, so it reverts on every pool without one.<br>Caught by: [`rvHoCallOnTransferSnapshotIsNeverRefusedToAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L101) |
| [4108](#holdings-4108) | increase overwrites the lifetime deposit total with the new amount instead of adding to it, so earlier deposits are lost.<br>Caught by: [`hlHoDepositHistoryRecordsTheInflowAndSurvivesTheOutflow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L4) |
| [4109](#holdings-4109) | Reading a price source no longer refuses an unopened holding, so an absent row answers with the zero address.<br>Caught by: [`rvHoValuationRefusesAnUnopenedHolding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L168) |
| [4110](#holdings-4110) | The sync notification bumps the sequence number again, so marking a network synced advances its nonce twice.<br>Caught by: [`hlHoPublishingASyncMarkerAlwaysAdvancesTheSequence`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L87) |
| [4111](#holdings-4111) | decrease rebases the row onto its net amount and zeroes the withdrawal counter, so both flow histories are lost.<br>Caught by: [`hlHoDepositHistoryRecordsTheInflowAndSurvivesTheOutflow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L4) · [`hlHoWithdrawalHistoryRecordsTheWholeOutflow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L21) |
| [4112](#holdings-4112) | increase subtracts the realized value from the holding instead of adding it, so the value it reports is not the value it books.<br>Caught by: [`hlHoIncreaseReturnsTheValueItBooked`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L38) |
| [4113](#holdings-4113) | decrease adds the removed value to the holding instead of subtracting it, so the value it reports is not the value it removes.<br>Caught by: [`hlHoDecreaseReturnsTheValueItRemoved`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L54) |
| [4114](#holdings-4114) | update reports the new total value instead of the change it applied, so the journal books the whole value as a move.<br>Caught by: [`hlHoUpdateReportsTheRevaluationItWrote`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L70) |
| [4115](#holdings-4115) | updateValuation also copies the first journal account onto the second, so repointing a price source reroutes the holding's ledger entries.<br>Caught by: [`vtHoAccountWiringMovesOnlyThroughItsTwoWriters`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L67) |
| [4116](#holdings-4116) | callOnTransferSnapshot deletes the pool's hook after notifying it, so later syncs and transfers no longer reach it.<br>Caught by: [`vtHoSnapshotHookMovesOnlyThroughItsSetter`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L85) |
| [4117](#holdings-4117) | decrease resets the inflow total to the net amount and the outflow total to zero, so both lifetime totals shrink.<br>Caught by: [`vtHoDepositHistoryNeverShrinks`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L6) · [`vtHoWithdrawalHistoryNeverShrinks`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L21) |
| [4118](#holdings-4118) | updateValuation accepts the zero address as a price source, so repointing a holding erases the record that the pool ever opened it.<br>Caught by: [`vtHoOpenedHoldingIsNeverClosed`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L36) |
| [4119](#holdings-4119) | setSnapshot decrements the snapshot nonce instead of incrementing it, so a network's ordering sequence runs backwards instead of advancing one step.<br>Caught by: [`vtHoSnapshotNonceStepsByAtMostOne`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L51) |
| [6600](#holdings-6600) | opening a holding demands that the row already be open, so a pool can never open the first holding of its share class.<br>Caught by: [`rcHoOpeningThePoolsFirstHoldingIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L4) |
| [6601](#holdings-6601) | initialize wires only three of the four ledger accounts, so the fourth journal kind is left unrouted after opening.<br>Caught by: [`rcHoOpeningWiringAllFourLedgerAccountsIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L25) |
| [6602](#holdings-6602) | the opening call never records the price source it was handed, so a row opened beside a live sibling still reports no price source.<br>Caught by: [`rcHoOpeningASecondHoldingIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L42) |
| [6603](#holdings-6603) | increase values a deposit only when it realizes nothing, so a real deposit is always booked at zero value.<br>Caught by: [`rcHoBookingADepositIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L60) |
| [6605](#holdings-6605) | increase now refuses a zero amount instead of absorbing it, so an empty deposit report reverts.<br>Caught by: [`rcHoZeroDepositIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L78) |
| [6606](#holdings-6606) | a deposit is valued at par instead of by its price source, so a holding priced at zero still books value.<br>Caught by: [`rcHoDepositPricedAtNothingIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L98) |
| [6607](#holdings-6607) | a deposit is refused until the holding has a price source, so a report for an unopened holding reverts.<br>Caught by: [`rcHoBookingADepositBeforeTheRowIsOpenedIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L118) |
| [6608](#holdings-6608) | a holding netted exactly back to balance still counts as short, so an exact repayment leaves the deficit counts raised.<br>Caught by: [`rcHoClearingADeficitExactlyIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L138) |
| [6609](#holdings-6609) | a withdrawal reports the value removed but never deducts it, so the holding keeps its full carrying value.<br>Caught by: [`rcHoBookingAWithdrawalIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L160) |
| [6610](#holdings-6610) | a withdrawal larger than the position is refused, so a pool can no longer take out more than a row holds.<br>Caught by: [`rcHoWithdrawingPastThePositionIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L178) |
| [6611](#holdings-6611) | a withdrawal sized exactly to the position is refused, so a pool can never close a holding to precisely nothing.<br>Caught by: [`rcHoClosingThePositionExactlyIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L203) |
| [6612](#holdings-6612) | a withdrawal on a row that is already short is refused, so a shortfall can never be deepened once it opens.<br>Caught by: [`rcHoDeepeningADeficitIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L224) |
| [6613](#holdings-6613) | entering deficit pins the pool network deficit counter to one instead of adding a row to it, so a second short row is never counted.<br>Caught by: [`rcHoDeficitCountCarryingASecondShortRowIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L245) |
| [6614](#holdings-6614) | a withdrawal is refused until the holding has a price source, so an outflow for an unopened holding reverts.<br>Caught by: [`rcHoBookingAWithdrawalBeforeTheRowIsOpenedIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L265) |
| [6615](#holdings-6615) | a revaluation can only ever mark a holding down, so a price rise never reaches the pool carrying value.<br>Caught by: [`rcHoRevaluationUpwardIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L286) |
| [6616](#holdings-6616) | a revaluation can only ever mark a holding up, so a price fall never reaches the pool carrying value.<br>Caught by: [`rcHoRevaluationDownwardIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L303) |
| [6617](#holdings-6617) | a revaluation that would leave the carrying value exactly where it is refuses instead of being absorbed.<br>Caught by: [`rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L210) |
| [6618](#holdings-6618) | a revaluation is refused on a row that carries no position, so an empty holding can never be repriced.<br>Caught by: [`rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L210) |
| [6619](#holdings-6619) | the in sync marker is never published, so a network can be stepped through its sequence but never declared reconciled.<br>Caught by: [`rcHoMarkingANetworkInSyncIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L321) |
| [6620](#holdings-6620) | the in sync marker latches on, so a network that has been declared reconciled can never be marked out of sync again.<br>Caught by: [`rcHoMarkingANetworkOutOfSyncIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L339) |
| [6621](#holdings-6621) | the ordering sequence advances only when a network is marked in sync, so a desync is not counted as a step.<br>Caught by: [`rcHoSyncAndDesyncRoundTripIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L357) |
| [6623](#holdings-6623) | the automation setter detaches instead of attaching, so a pool can never route its NAV notifications to a callee.<br>Caught by: [`rcHoAttachingNavAutomationIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L379) |
| [6624](#holdings-6624) | the snapshot hook setter refuses the zero address, so a hook can be attached but never removed.<br>Caught by: [`rcHoAutomationAttachAndDetachRoundTripIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L393) |
| [6625](#holdings-6625) | rewiring a ledger account records the request but never moves the account the holding points at.<br>Caught by: [`rcHoRewiringALedgerAccountIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L412) |
| [6626](#holdings-6626) | repointing a holding leaves the price source it already had in place, so a position can never be moved onto another oracle.<br>Caught by: [`rcHoSwappingThePriceSourceIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L428) |
| [6627](#holdings-6627) | revoking authority emits the event but never clears the ward, so granted authority can never be taken back.<br>Caught by: [`rcHoWardGrantAndRevokeRoundTripIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L451) |
| [6628](#holdings-6628) | a deposit reports the value it was quoted but never adds it to the carrying value, so funding a position leaves its book empty.<br>Caught by: [`rcHoOpeningAndFullyClosingAPositionIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L470) |
| [6629](#holdings-6629) | the pool network deficit counter only ever climbs, so leaving a deficit never takes the row back off the count.<br>Caught by: [`rcHoEnteringAndLeavingADeficitIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L491) |
| [7200](#holdings-7200) | booking an inflow no longer requires write rights, so anyone can move a holding's amount, value and deficit count.<br>Caught by: [`acHoDepositHistoryMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L20) · [`acHoCarryingValueMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L54) · [`acHoDeficitCountMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L152) |
| [7201](#holdings-7201) | booking an outflow no longer requires the caller to hold write rights, so anyone can inflate a position's withdrawal history.<br>Caught by: [`acHoWithdrawalHistoryMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L37) |
| [7202](#holdings-7202) | rewiring a position to a different journal account no longer requires the caller to hold write rights.<br>Caught by: [`acHoJournalWiringMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L87) |
| [7203](#holdings-7203) | repointing a position at a different price source no longer requires the caller to hold write rights.<br>Caught by: [`acHoPriceSourceMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L70) |
| [7204](#holdings-7204) | repointing a pool at a different snapshot hook no longer requires the caller to hold write rights.<br>Caught by: [`acHoSnapshotHookMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L104) |
| [7205](#holdings-7205) | setting the sync marker no longer requires write rights, so anyone can flip it and burn its nonce.<br>Caught by: [`acHoSyncMarkerMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L120) · [`acHoSnapshotNonceMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L136) |
| [7206](#holdings-7206) | granting write rights no longer requires the caller to hold them, so any address can make itself a ward of the ledger.<br>Caught by: [`acHoWardRightsMoveOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L4) |
| [7207](#holdings-7207) | booking an inflow no longer requires the caller to hold write rights, so the call succeeds where it must have failed.<br>Caught by: [`rvHoIncreaseRefusesANonWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L117) |
| [7208](#holdings-7208) | replaying the sync notification no longer requires write rights, so any caller drives the pool's NAV automation.<br>Caught by: [`rvHoCallOnSyncSnapshotRefusesANonWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L182) |
| [7209](#holdings-7209) | notifying the hook of a cross network transfer no longer requires write rights, so any caller drives it.<br>Caught by: [`rvHoCallOnTransferSnapshotRefusesANonWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L196) |
| [8000](#holdings-8000) | the share class deficit counter is read but never moved on a crossing, so a class with short rows reports none.<br>Caught by: [`deficitCountMatchesTheClassShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L48) |
| [8001](#holdings-8001) | increaseCountedUnder books inflow on one class but moves another class's deficit count, so per class counts go wrong.<br>Caught by: [`deficitCountIsKeptPerShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L18) |
| [8002](#holdings-8002) | a new shortfall is counted on network zero instead of the named network, so the wrong network's rollup rises.<br>Caught by: [`hlHoEnteringADeficitBooksTheNamedNetworkOnly`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L39) |
| [8003](#holdings-8003) | the sync gate is inverted, so the snapshot hook fires while the network is out of sync and never once it is synced.<br>Caught by: [`hlHoSyncNotificationCarriesTheMarkersOwnKeys`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L102) |
| [8004](#holdings-8004) | a cleared shortfall is released from network zero instead of the named network, so the named network stays counted short.<br>Caught by: [`hlHoLeavingADeficitReleasesTheNamedNetworkOnly`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L65) |
| [8005](#holdings-8005) | the pool network rollup is overwritten with the acting class's count, so two classes short on one network report one.<br>Caught by: [`rcHoTwoShareClassesShortOnOneNetworkIsReachable`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L142) |
| [8006](#holdings-8006) | publishing a sync marker clears that share class network's shortfall tally, so a network with short rows reports none from the next marker on.<br>Caught by: [`stHoDeficitCountersMoveOnlyThroughTheFlowEntries`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L251) |
| [8007](#holdings-8007) | each crossing also copies the network rollup onto the next network id, so the rollups no longer sum to the short rows.<br>Caught by: [`deficitCountsSumToTheShortRowsAcrossTheNetworks`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L7) |
| [8008](#holdings-8008) | a release floors both shortfall tallies at zero instead of reverting, so a network counting none accepts the release.<br>Caught by: [`rvHoLeavingADeficitIsRefusedWhenTheNamedNetworkCountsNone`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L93) |
| [8009](#holdings-8009) | a row lifted out of shortfall is never counted out, so a network's shortfall count only ever rises.<br>Caught by: [`rcHoShortfallAttributionCanOutliveItsNetworkIsReachable`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L120) |
| [8052](#holdings-8052) | the share class shortfall counter moves the wrong way, so entering shortfall counts down and leaving it counts up.<br>Caught by: [`stHhClassDeficitCountFollowsTheShortRows`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L194) |
| [8053](#holdings-8053) | the sync gate is inverted, so the snapshot hook hears every report except the one that marks the network synced.<br>Caught by: [`hlHhSyncNotificationOnlyOnAClosedBatch`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L376) |
| [8058](#holdings-8058) | a crossing moves the network rollup but not the share class shortfall counter, so the class count goes stale.<br>Caught by: [`rcHhAssetWithdrawalEnteringDeficitIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L188) · [`rcHhAssetDepositLeavingDeficitIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L211) |
| [8070](#holdings-8070) | a crossing moves the pool network rollup while the share class tally stands still, so the event reports a class count no crossing ever changed.<br>Caught by: [`rcHoClearingADeficitExactlyIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L138) · [`rcHoWithdrawingPastThePositionIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L178) · [`rcHoDeficitCountCarryingASecondShortRowIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L245) · [`rcHoEnteringAndLeavingADeficitIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L491) |
| [8100](#holdings-8100) | publishing a sync marker also advances the neighbouring network's snapshot nonce, so one network's marker moves another network's snapshot row.<br>Caught by: [`stHoSnapshotRowIsPerNetwork`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L232) |
| [8101](#holdings-8101) | increaseAcrossClasses books one inflow on two share classes of the pool at once, so flow on one class restates the other class's holding row.<br>Caught by: [`stHoFlowRowIsPerShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L26) |
| [8102](#holdings-8102) | replaying the sync notification no longer reads the stored marker, so a network in sync is never renotified to the pool's NAV hook.<br>Caught by: [`hlHoReplayNotifiesUnderTheMarkersOwnKeys`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L121) |
| [8103](#holdings-8103) | increase refuses inflow unless the network shortfall tally equals the class tally, so a sibling class's shortfall blocks deposits.<br>Caught by: [`rvHoIncreaseBeforeOpeningIsNeverRefusedOverASiblingClassShortfall`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L125) |
| [8104](#holdings-8104) | clearDeficit lets any caller wipe a share class network's shortfall tally, so the class counter moves without the ledger's authority.<br>Caught by: [`acHoDeficitCountMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L152) |
| [8105](#holdings-8105) | increaseTagging books inflow in one pool but bumps a shortfall count in another pool, so one pool's flow moves another's.<br>Caught by: [`stHoDeficitCountAndHookIgnoreASiblingsFlow`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L74) |
| [8415](#holdings-8415) | a revaluation prices an oversized net amount on its truncated low bits instead of refusing, so the holding is marked to a wrong value.<br>Caught by: [`rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L210) |
| [8416](#holdings-8416) | the amount view truncates an oversized net amount instead of refusing, so a huge holding reads as a smaller one.<br>Caught by: [`rvHoAmountViewsRefuseOnlyANetPastUint128`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L228) |
| [8417](#holdings-8417) | the holding view truncates an oversized net amount instead of refusing, so a huge holding reads as a smaller one.<br>Caught by: [`rvHoAmountViewsRefuseOnlyANetPastUint128`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L228) |
| [8418](#holdings-8418) | the holding view truncates each lifetime total before netting them, so a holding with very large totals can report a wrong amount.<br>Caught by: [`hlHoHoldingViewReportsTheFlooredNetOfWideTotals`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L238) |
| [8811](#holdings-8811) | increase quotes the whole position instead of the added amount, so an admin's inflow to an open holding with an oversized net reverts though no total or value overflows.<br>Caught by: [`rvHoIncreaseOnAnOpenHoldingFailsOnlyOnAnOverflowingTotalOrValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L246) |
| [9012](#holdings-9012) | the pool's network shortfall rollup is updated on the next network id, so the named network's rollup never moves.<br>Caught by: [`stHoDeficitCountsOfAtMostOneNetworkMovePerCall`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L17) |
| [9013](#holdings-9013) | setSnapshot writes the flag under a fixed share class but the nonce under the named one, so one call moves two classes.<br>Caught by: [`stHoSnapshotRowIsPerShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L82) |
| [9032](#holdings-9032) | replaying a sync notice also spends the network's sequence number, so a replay moves the nonce without any snapshot update.<br>Caught by: [`vtHoSnapshotSequenceMovesOnlyThroughItsPublisher`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L102) |
| [9048](#holdings-9048) | A holding's price source can be reset to the zero address, so a valued holding keeps its value with no valuation.<br>Caught by: [`uninitializedHoldingHasNoValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L26) |
| [9049](#holdings-9049) | The pool's deficit counter on a network is not lowered when a holding recovers, so it overcounts holdings in deficit.<br>Caught by: [`networkDeficitCountIsItsNetworksShortRowCensus`](../../specs/core/hub/Holdings/Holdings_census_properties.spec#L7) |
| [9058](#holdings-9058) | A share class's deficit counter on a network is not lowered when a holding recovers, so it overcounts holdings in deficit.<br>Caught by: [`deficitCountIsItsClassNetworksShortRowCensus`](../../specs/core/hub/Holdings/Holdings_census_properties.spec#L12) |
| [9080](#holdings-9080) | decrease removes carrying value only on a full drain, so a partial withdrawal leaves all the value on the book.<br>Caught by: [`hlHoDecreaseRemovesValueProRataToTheRealizedAmount`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L142) |
| [9081](#holdings-9081) | every inflow calls the snapshot hook regardless of the sync marker, so it can fire while books are out of step.<br>Caught by: [`stHoSyncNotificationOnlyUnderAnInSyncMarker`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L268) |
| [9082](#holdings-9082) | update also writes the new carrying value onto the same asset in a sibling share class, so revaluing one class restates another.<br>Caught by: [`stHoHoldingRowIsPerShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L47) |
| [9083](#holdings-9083) | setting a snapshot uses one fixed share class's row, so all classes of a pool share one nonce sequence.<br>Caught by: [`hlHoSetSnapshotBumpsTheNamedClassesNonce`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L104) |
| [9084](#holdings-9084) | setting a snapshot uses one fixed pool's row, so all pools share one nonce sequence.<br>Caught by: [`hlHoSetSnapshotBumpsTheNamedPoolsNonce`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L99) |
| [9086](#holdings-9086) | an accepted report no longer advances its network's snapshot sequence, so the same asset or share report can be replayed under the same nonce.<br>Caught by: [`hlHhAcceptedAssetReportSpendsItsNetworksNonceOnce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L465) · [`hlHhAcceptedShareReportSpendsItsNetworksNonceOnce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L484) |
| [9470](#holdings-9470) | a deposit into a holding in shortfall is priced on its full size, so the shortfall repayment is booked as value.<br>Caught by: [`hlHoIncreaseQuotesOnlyTheRealizedAmount`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L163) |
| [9471](#holdings-9471) | a deposit into a holding in shortfall is priced on its full size, so the shortfall repayment is priced too.<br>Caught by: [`rcHoNettingInflowPricesOnlyItsPositivePart`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L540) |
| [9472](#holdings-9472) | a revaluation prices a holding's gross deposits instead of its net amount, so a holding with withdrawals is overvalued.<br>Caught by: [`hlHoUpdateMarksTheBookToTheQuoteOfItsAmount`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L187) |
| [9473](#holdings-9473) | a partial withdrawal is priced at a live quote of the removed amount, capped at the carrying value, instead of pro rata to the book.<br>Caught by: [`hlHoDecreaseNeverConsultsTheOracle`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L210) |
| [9474](#holdings-9474) | a partial withdrawal books off a live quote capped at the carrying value, so it no longer removes a pro rata share.<br>Caught by: [`rcHoDecreaseBooksOffTheQuoteJustTaken`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L516) |
| [9475](#holdings-9475) | moving a holding onto another price source asks the new source for a quote of the position and throws the answer away.<br>Caught by: [`hlHoPriceSourceSwapLeavesTheCarryingValueStanding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L223) |
| [9476](#holdings-9476) | switching a holding's price source queries the new source for a discarded quote, so a swap is no longer quote free.<br>Caught by: [`rcHoStaleValueSurvivesAPriceSourceSwapOnALivePosition`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L557) |
| [9522](#holdings-9522) | the pool's deficit counter on a network stops rising at two, so a third holding in deficit goes uncounted.<br>Caught by: [`rcHoCensusReachesThreeShortRowsOnOneNetwork`](../../specs/core/hub/Holdings/Holdings_census_properties.spec#L19) |

## Holdings #802

setSnapshotHook no longer checks that the pool exists, so a snapshot hook can be attached to an unregistered pool.

- **Mutant:** [`802.sol`](802.sol)
- **Caught by:** [`snapshotHookImpliesPoolExists`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L16)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 802`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule snapshotHookImpliesPoolExists`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -89,7 +89,7 @@
 
     /// @inheritdoc IHoldings
     function setSnapshotHook(PoolId poolId, ISnapshotHook hook) external auth {
-        require(hubRegistry.exists(poolId), NonExistingPool());
+        // MUTATION: removed the pool existence check
 
         snapshotHook[poolId] = hook;
 
```

## Holdings #803

setSnapshotHook inverts the pool existence check, accepting unregistered pools and rejecting registered ones.

- **Mutant:** [`803.sol`](803.sol)
- **Caught by:** [`snapshotHookImpliesPoolExists`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L16)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 803`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule snapshotHookImpliesPoolExists`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -89,7 +89,7 @@
 
     /// @inheritdoc IHoldings
     function setSnapshotHook(PoolId poolId, ISnapshotHook hook) external auth {
-        require(hubRegistry.exists(poolId), NonExistingPool());
+        require(!hubRegistry.exists(poolId), NonExistingPool()); // MUTATION: inverted pool existence check
 
         snapshotHook[poolId] = hook;
 
```

## Holdings #804

increase computes the prior deficit flag with transposed operands, so the deficit counter moves on the wrong transitions.

- **Mutant:** [`804.sol`](804.sol)
- **Caught by:** [`networkDeficitCountMatchesTheShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 804`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule networkDeficitCountMatchesTheShortRows`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -144,7 +144,7 @@
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
 
-        bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
+        bool wasDeficit = holding_.increasedAmount > holding_.decreasedAmount; // MUTATION: transposed deficit comparison
         uint256 oldAmount = _amount(holding_);
         holding_.increasedAmount += amount_;
         uint128 realized = (_amount(holding_) - oldAmount).toUint128();
```

## Holdings #805

decrease treats an exactly netted holding as a deficit, bumping the deficit counter on a row that holds no deficit.

- **Mutant:** [`805.sol`](805.sol)
- **Caught by:** [`networkDeficitCountMatchesTheShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 805`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule networkDeficitCountMatchesTheShortRows`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -182,7 +182,7 @@
         amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
 
         holding_.assetAmountValue -= amountValue;
-        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
+        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount >= holding_.increasedAmount); // MUTATION: deficit boundary widened to >=
 
         emit Decrease(poolId, scId, assetId, amount_, amountValue);
     }
```

## Holdings #806

the network deficit counter moves in the wrong direction on a deficit-state crossing, incrementing on exit and decrementing on entry.

- **Mutant:** [`806.sol`](806.sol)
- **Caught by:** [`networkDeficitCountMatchesTheShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 806`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule networkDeficitCountMatchesTheShortRows`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -276,7 +276,7 @@
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
         uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+            isDeficit ? --networkDeficitCount[poolId][centrifugeId] : ++networkDeficitCount[poolId][centrifugeId]; // MUTATION: swapped increment and decrement branches
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

## Holdings #807

the deficit no-op guard is inverted, so state crossings are skipped and steady states move the counter.

- **Mutant:** [`807.sol`](807.sol)
- **Caught by:** [`networkDeficitCountMatchesTheShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 807`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule networkDeficitCountMatchesTheShortRows`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -271,7 +271,7 @@
     function _updateDeficit(PoolId poolId, ShareClassId scId, uint16 centrifugeId, bool wasDeficit, bool isDeficit)
         internal
     {
-        if (wasDeficit == isDeficit) return;
+        if (wasDeficit != isDeficit) return; // MUTATION: inverted no-op guard
 
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
```

## Holdings #810

decrease removes value pro-rata to the remaining amount instead of the removed amount, so a full drain leaves residual value behind.

- **Mutant:** [`810.sol`](810.sol)
- **Caught by:** [`emptyHoldingCarriesNoValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L32)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 810`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule emptyHoldingCarriesNoValue`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -179,7 +179,7 @@
         // storage mutation and can never over-journal. Deliberately NOT a live oracle quote like increase():
         // pro-rata preserves `amount == 0 => value == 0`, which a live quote would break when the price has
         // moved since the last update() (a full drain would leave residual value behind).
-        amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
+        amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * (oldAmount - removedAmount) / oldAmount).toUint128(); // MUTATION: pro-rata over remaining instead of removed amount
 
         holding_.assetAmountValue -= amountValue;
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
```

## Holdings #811

update quotes the cumulative increased amount instead of the current net amount, so an emptied holding is revalued as if still held.

- **Mutant:** [`811.sol`](811.sol)
- **Caught by:** [`emptyHoldingCarriesNoValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L32)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 811`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule emptyHoldingCarriesNoValue`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -196,7 +196,7 @@
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
-        uint128 currentAmountValue = holding_.valuation.getQuote(poolId, scId, assetId, _amount(holding_).toUint128());
+        uint128 currentAmountValue = holding_.valuation.getQuote(poolId, scId, assetId, holding_.increasedAmount.toUint128()); // MUTATION: quote base uses cumulative increases
 
         isPositive = currentAmountValue >= holding_.assetAmountValue;
         diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
```

## Holdings #812

setAccountId inverts the initialization check, wiring journal accounts onto holdings that were never initialized.

- **Mutant:** [`812.sol`](812.sol)
- **Caught by:** [`accountIdImpliesInitialized`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L43)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 812`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule accountIdImpliesInitialized`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -68,7 +68,7 @@
         auth
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
-        require(address(holding_.valuation) != address(0), HoldingNotFound());
+        require(address(holding_.valuation) == address(0), HoldingNotFound()); // MUTATION: inverted initialization check
 
         accountId[poolId][scId][assetId][kind] = accountId_;
 
```

## Holdings #813

initialize stores the account ids but never records the valuation, leaving journal accounts wired to an uninitialized holding.

- **Mutant:** [`813.sol`](813.sol)
- **Caught by:** [`accountIdImpliesInitialized`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L43)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 813`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule accountIdImpliesInitialized`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -53,7 +53,7 @@
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) == address(0), AlreadyInitialized());
 
-        holding_.valuation = valuation_;
+        // MUTATION: removed the valuation write
 
         for (uint256 i; i < 4; i++) {
             accountId[poolId][scId][assetId][uint8(i)] = accounts[i];
```

## Holdings #814

setSnapshot marks the row in sync without advancing the nonce, so a synced snapshot still shows an untouched nonce.

- **Mutant:** [`814.sol`](814.sol)
- **Caught by:** [`snapshotFlagImpliesAStartedNonce`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 814`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule snapshotFlagImpliesAStartedNonce`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -105,7 +105,7 @@
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
         snapshot_.isSnapshot = isSnapshot;
-        snapshot_.nonce++;
+        // MUTATION: removed the nonce bump
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
```

## Holdings #815

setSnapshot decrements the snapshot nonce instead of incrementing it, so a synced row can return to a zero nonce.

- **Mutant:** [`815.sol`](815.sol)
- **Caught by:** [`snapshotFlagImpliesAStartedNonce`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 815`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule snapshotFlagImpliesAStartedNonce`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -105,7 +105,7 @@
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
         snapshot_.isSnapshot = isSnapshot;
-        snapshot_.nonce++;
+        snapshot_.nonce--; // MUTATION: nonce decremented instead of incremented
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
```

## Holdings #816

increase nets the deposit against the outstanding withdrawal instead of only recording it, so one call moves both sides of the flow record.

- **Mutant:** [`816.sol`](816.sol)
- **Caught by:** [`stHoInflowAndOutflowNeverMoveTogether`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 816`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule stHoInflowAndOutflowNeverMoveTogether`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -147,6 +147,8 @@
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
         holding_.increasedAmount += amount_;
+        // MUTATION: the deposit is netted against the outstanding withdrawal
+        holding_.decreasedAmount -= holding_.decreasedAmount < amount_ ? holding_.decreasedAmount : amount_;
         uint128 realized = (_amount(holding_) - oldAmount).toUint128();
 
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
```

## Holdings #817

transferHolding moves a position between two assets of the same class in one call, so one call restates two holdings.

- **Mutant:** [`817.sol`](817.sol)
- **Caught by:** [`stHoOneCallTouchesOneHolding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L136)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 817`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule stHoOneCallTouchesOneHolding`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -73,6 +73,23 @@
         accountId[poolId][scId][assetId][kind] = accountId_;
 
         emit SetAccountId(poolId, scId, assetId, kind, accountId_);
+    }
+
+    /// @notice MUTATION: moves a position between two assets of the same class, restating both holdings.
+    function transferHolding(
+        PoolId poolId,
+        ShareClassId scId,
+        AssetId fromAssetId,
+        AssetId toAssetId,
+        uint128 amount_
+    ) external auth {
+        Holding storage from_ = _holding[poolId][scId][fromAssetId];
+        Holding storage to_ = _holding[poolId][scId][toAssetId];
+        require(address(from_.valuation) != address(0), HoldingNotFound());
+        require(address(to_.valuation) != address(0), HoldingNotFound());
+
+        from_.decreasedAmount += amount_;
+        to_.increasedAmount += amount_;
     }
 
     /// @inheritdoc IHoldings
```

## Holdings #818

increase subtracts the realized value instead of adding it, so a deposit writes the holding's carrying value down.

- **Mutant:** [`818.sol`](818.sol)
- **Caught by:** [`stHoInflowNeverLowersValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L167)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 818`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule stHoInflowNeverLowersValue`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -155,7 +155,7 @@
             ? holding_.valuation.getQuote(poolId, scId, assetId, realized)
             : 0;
 
-        holding_.assetAmountValue += amountValue;
+        holding_.assetAmountValue -= amountValue; // MUTATION: the realized increase is subtracted
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
 
         emit Increase(poolId, scId, assetId, amount_, amountValue);
```

## Holdings #819

decrease adds the removed value instead of subtracting it, so a withdrawal writes the holding's carrying value up.

- **Mutant:** [`819.sol`](819.sol)
- **Caught by:** [`stHoOutflowNeverRaisesValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L182)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 819`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule stHoOutflowNeverRaisesValue`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -181,7 +181,7 @@
         // moved since the last update() (a full drain would leave residual value behind).
         amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
 
-        holding_.assetAmountValue -= amountValue;
+        holding_.assetAmountValue += amountValue; // MUTATION: the removed value is added
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
 
         emit Decrease(poolId, scId, assetId, amount_, amountValue);
```

## Holdings #820

initialize prices the holding at open off a unit probe, so creation funds a carrying value no deposit ever paid for.

- **Mutant:** [`820.sol`](820.sol)
- **Caught by:** [`stHoOpeningAHoldingFundsNothing`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L197)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 820`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule stHoOpeningAHoldingFundsNothing`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -54,6 +54,8 @@
         require(address(holding_.valuation) == address(0), AlreadyInitialized());
 
         holding_.valuation = valuation_;
+        // MUTATION: the holding is priced at open instead of at its first deposit
+        holding_.assetAmountValue = valuation_.getQuote(poolId, scId, assetId, 1);
 
         for (uint256 i; i < 4; i++) {
             accountId[poolId][scId][assetId][uint8(i)] = accounts[i];
```

## Holdings #821

setSnapshot advances the nonce by two, so a flipped marker skips a nonce.

- **Mutant:** [`821.sol`](821.sol)
- **Caught by:** [`stHoSnapshotFlagMovesWithItsNonce`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L217)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 821`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule stHoSnapshotFlagMovesWithItsNonce`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -105,7 +105,7 @@
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
         snapshot_.isSnapshot = isSnapshot;
-        snapshot_.nonce++;
+        snapshot_.nonce += 2; // MUTATION: the sequence skips a step
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
```

## Holdings #822

migrateHolding moves a holding and its ledger wiring to another pool, so one call writes two pools' books.

- **Mutant:** [`822.sol`](822.sol)
- **Caught by:** [`stHoHoldingRowIsPerPool`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L7) · [`stHoAccountWiringIsPerPool`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 822`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_pool_properties.conf --rule stHoHoldingRowIsPerPool stHoAccountWiringIsPerPool`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -73,6 +73,32 @@
         accountId[poolId][scId][assetId][kind] = accountId_;
 
         emit SetAccountId(poolId, scId, assetId, kind, accountId_);
+    }
+
+    /// @notice MUTATION: moves a holding and its ledger wiring to another pool, writing both pools' books.
+    function migrateHolding(
+        PoolId fromPoolId,
+        PoolId toPoolId,
+        ShareClassId fromScId,
+        ShareClassId toScId,
+        AssetId assetId
+    ) external auth {
+        Holding storage from_ = _holding[fromPoolId][fromScId][assetId];
+        Holding storage to_ = _holding[toPoolId][toScId][assetId];
+        require(address(from_.valuation) != address(0), HoldingNotFound());
+
+        to_.increasedAmount = from_.increasedAmount;
+        to_.decreasedAmount = from_.decreasedAmount;
+        to_.assetAmountValue = from_.assetAmountValue;
+        to_.valuation = from_.valuation;
+        from_.increasedAmount = 0;
+        from_.decreasedAmount = 0;
+        from_.assetAmountValue = 0;
+
+        for (uint256 i; i < 4; i++) {
+            accountId[toPoolId][toScId][assetId][uint8(i)] = accountId[fromPoolId][fromScId][assetId][uint8(i)];
+            accountId[fromPoolId][fromScId][assetId][uint8(i)] = AccountId.wrap(0);
+        }
     }
 
     /// @inheritdoc IHoldings
```

## Holdings #823

setSnapshotPair marks two pools in sync off one round, so one call moves two pools' snapshot rows.

- **Mutant:** [`823.sol`](823.sol)
- **Caught by:** [`stHoSnapshotRowIsPerPool`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L53)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 823`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_pool_properties.conf --rule stHoSnapshotRowIsPerPool`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -73,6 +73,24 @@
         accountId[poolId][scId][assetId][kind] = accountId_;
 
         emit SetAccountId(poolId, scId, assetId, kind, accountId_);
+    }
+
+    /// @notice MUTATION: marks two pools in sync off one round, writing both pools' snapshot rows.
+    function setSnapshotPair(
+        PoolId poolId,
+        PoolId siblingPoolId,
+        ShareClassId scId,
+        ShareClassId siblingScId,
+        uint16 centrifugeId,
+        bool isSnapshot
+    ) external auth {
+        Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
+        Snapshot storage sibling_ = snapshot[siblingPoolId][siblingScId][centrifugeId];
+
+        snapshot_.isSnapshot = isSnapshot;
+        snapshot_.nonce++;
+        sibling_.isSnapshot = isSnapshot;
+        sibling_.nonce++;
     }
 
     /// @inheritdoc IHoldings
```

## Holdings #824

increaseFor books flow on one pool while counting its deficit under another, so a pool's flow moves a sibling's counter.

- **Mutant:** [`824.sol`](824.sol)
- **Caught by:** [`stHoDeficitCountAndHookIgnoreASiblingsFlow`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L74)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 824`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_pool_properties.conf --rule stHoDeficitCountAndHookIgnoreASiblingsFlow`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -73,6 +73,22 @@
         accountId[poolId][scId][assetId][kind] = accountId_;
 
         emit SetAccountId(poolId, scId, assetId, kind, accountId_);
+    }
+
+    /// @notice MUTATION: books flow on one pool while counting its deficit under another.
+    function increaseFor(
+        PoolId poolId,
+        PoolId deficitPoolId,
+        ShareClassId scId,
+        AssetId assetId,
+        uint16 centrifugeId,
+        uint128 amount_
+    ) external auth {
+        Holding storage holding_ = _holding[poolId][scId][assetId];
+
+        bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
+        holding_.increasedAmount += amount_;
+        _updateDeficit(deficitPoolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
     }
 
     /// @inheritdoc IHoldings
```

## Holdings #825

increaseForClass books flow on one class but reads the deficit crossing off another, so the pool's deficit count goes stale.

- **Mutant:** [`825.sol`](825.sol)
- **Caught by:** [`networkDeficitCountSpansEveryShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L13)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 825`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_share_class_properties.conf --rule networkDeficitCountSpansEveryShareClass`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -73,6 +73,23 @@
         accountId[poolId][scId][assetId][kind] = accountId_;
 
         emit SetAccountId(poolId, scId, assetId, kind, accountId_);
+    }
+
+    /// @notice MUTATION: books flow on one class while reading the crossing off another class's row.
+    function increaseForClass(
+        PoolId poolId,
+        ShareClassId scId,
+        ShareClassId deficitScId,
+        AssetId assetId,
+        uint16 centrifugeId,
+        uint128 amount_
+    ) external auth {
+        Holding storage holding_ = _holding[poolId][scId][assetId];
+        Holding storage other_ = _holding[poolId][deficitScId][assetId];
+
+        bool wasDeficit = other_.decreasedAmount > other_.increasedAmount;
+        holding_.increasedAmount += amount_;
+        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, other_.decreasedAmount > other_.increasedAmount);
     }
 
     /// @inheritdoc IHoldings
```

## Holdings #4100

The current amount loses its zero floor, so an overdrawn holding reverts every read and update that computes it.

- **Mutant:** [`4100.sol`](4100.sol)
- **Caught by:** [`rvHoDecreaseNeverStallsOnAnOversizedOutflow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L150) · [`rvHoIncreaseBeforeTheRowIsOpenedIsNeverRefusedToAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L131) · [`rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L210) · [`rvHoAmountViewsRefuseOnlyANetPastUint128`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L228) · [`rvHoIncreaseOnAnOpenHoldingFailsOnlyOnAnOverflowingTotalOrValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L246)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4100`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoDecreaseNeverStallsOnAnOversizedOutflow rvHoIncreaseBeforeTheRowIsOpenedIsNeverRefusedToAWard rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet rvHoAmountViewsRefuseOnlyANetPastUint128 rvHoIncreaseOnAnOpenHoldingFailsOnlyOnAnOverflowingTotalOrValue`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -282,9 +282,6 @@
 
     /// @dev Current amount, derived from the cumulative counters and floored at zero.
     function _amount(Holding storage holding_) internal view returns (uint256) {
-        return
-            holding_.increasedAmount >= holding_.decreasedAmount
-                ? holding_.increasedAmount - holding_.decreasedAmount
-                : 0;
+        return holding_.increasedAmount - holding_.decreasedAmount; // MUTATION: the zero floor on the current amount is dropped
     }
 }
```

## Holdings #4101

initialize no longer refuses an open holding, so reopening it silently overwrites its price source and journal accounts.

- **Mutant:** [`4101.sol`](4101.sol)
- **Caught by:** [`rvHoInitializeRefusesANonWardANullSourceOrAnOpenRow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4101`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoInitializeRefusesANonWardANullSourceOrAnOpenRow`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -51,7 +51,7 @@
         require(address(valuation_) != address(0), WrongValuation());
 
         Holding storage holding_ = _holding[poolId][scId][assetId];
-        require(address(holding_.valuation) == address(0), AlreadyInitialized());
+        // MUTATION: removed the one-shot initialization guard
 
         holding_.valuation = valuation_;
 
```

## Holdings #4102

setAccountId inverts the initialization check, so wiring a journal account is refused on an open holding and accepted on one that was never opened.

- **Mutant:** [`4102.sol`](4102.sol)
- **Caught by:** [`rvHoSetAccountIdRefusesANonWardOrAnUnopenedHolding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4102`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoSetAccountIdRefusesANonWardOrAnUnopenedHolding`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -68,7 +68,7 @@
         auth
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
-        require(address(holding_.valuation) != address(0), HoldingNotFound());
+        require(address(holding_.valuation) == address(0), HoldingNotFound()); // MUTATION: inverted initialization check
 
         accountId[poolId][scId][assetId][kind] = accountId_;
 
```

## Holdings #4103

updateValuation no longer requires the holding to be open, so a price source can be pinned onto a row the pool never opened.

- **Mutant:** [`4103.sol`](4103.sol)
- **Caught by:** [`rvHoUpdateValuationRefusesANonWardANullSourceOrAnUnopenedHolding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4103`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoUpdateValuationRefusesANonWardANullSourceOrAnUnopenedHolding`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -80,7 +80,7 @@
         require(address(valuation_) != address(0), WrongValuation());
 
         Holding storage holding_ = _holding[poolId][scId][assetId];
-        require(address(holding_.valuation) != address(0), HoldingNotFound());
+        // MUTATION: removed the open-holding check
 
         holding_.valuation = valuation_;
 
```

## Holdings #4104

setSnapshotHook no longer checks that the pool exists, so a snapshot hook can be attached to a pool the hub registry does not know.

- **Mutant:** [`4104.sol`](4104.sol)
- **Caught by:** [`rvHoSetSnapshotHookRefusesANonWardOrAnUnknownPool`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4104`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoSetSnapshotHookRefusesANonWardOrAnUnknownPool`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -89,7 +89,7 @@
 
     /// @inheritdoc IHoldings
     function setSnapshotHook(PoolId poolId, ISnapshotHook hook) external auth {
-        require(hubRegistry.exists(poolId), NonExistingPool());
+        // MUTATION: removed the pool existence check
 
         snapshotHook[poolId] = hook;
 
```

## Holdings #4105

setSnapshot no longer checks the nonce it was handed, so a stale or out of order cross network update is accepted instead of refused.

- **Mutant:** [`4105.sol`](4105.sol)
- **Caught by:** [`rvHoSetSnapshotRefusesANonWardOrAnOutOfOrderNonce`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L69)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4105`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoSetSnapshotRefusesANonWardOrAnOutOfOrderNonce`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -102,7 +102,7 @@
         auth
     {
         Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
-        require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
+        // MUTATION: removed the replay guard on the snapshot sequence
 
         snapshot_.isSnapshot = isSnapshot;
         snapshot_.nonce++;
```

## Holdings #4106

The sync notification also bumps the sequence number, so resending it on a network whose sequence is exhausted reverts.

- **Mutant:** [`4106.sol`](4106.sol)
- **Caught by:** [`rvHoCallOnSyncSnapshotIsNeverRefusedToAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L85)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4106`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoCallOnSyncSnapshotIsNeverRefusedToAWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -261,6 +261,9 @@
     function _callOnSync(PoolId poolId, ShareClassId scId, uint16 centrifugeId, Snapshot memory snapshot_) internal {
         if (!snapshot_.isSnapshot) return;
 
+        // MUTATION: the sync notification burns a sequence number of its own
+        snapshot[poolId][scId][centrifugeId].nonce++;
+
         ISnapshotHook hook = snapshotHook[poolId];
         if (address(hook) != address(0)) hook.onSync(poolId, scId, centrifugeId);
     }
```

## Holdings #4107

The cross network transfer notice now requires an installed hook, so it reverts on every pool without one.

- **Mutant:** [`4107.sol`](4107.sol)
- **Caught by:** [`rvHoCallOnTransferSnapshotIsNeverRefusedToAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L101)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4107`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoCallOnTransferSnapshotIsNeverRefusedToAWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -127,9 +127,8 @@
         uint128 amount_
     ) external auth {
         ISnapshotHook hook = snapshotHook[poolId];
-        if (address(hook) != address(0)) {
-            hook.onTransfer(poolId, scId, originCentrifugeId, targetCentrifugeId, amount_);
-        }
+        require(address(hook) != address(0), HoldingNotFound()); // MUTATION: a pool with no hook installed now has the errand refused instead of skipped
+        hook.onTransfer(poolId, scId, originCentrifugeId, targetCentrifugeId, amount_);
     }
 
     //----------------------------------------------------------------------------------------------
```

## Holdings #4108

increase overwrites the lifetime deposit total with the new amount instead of adding to it, so earlier deposits are lost.

- **Mutant:** [`4108.sol`](4108.sol)
- **Caught by:** [`hlHoDepositHistoryRecordsTheInflowAndSurvivesTheOutflow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4108`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoDepositHistoryRecordsTheInflowAndSurvivesTheOutflow`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -146,7 +146,7 @@
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
-        holding_.increasedAmount += amount_;
+        holding_.increasedAmount = amount_; // MUTATION: the deposit counter is overwritten instead of accumulated
         uint128 realized = (_amount(holding_) - oldAmount).toUint128();
 
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
```

## Holdings #4109

Reading a price source no longer refuses an unopened holding, so an absent row answers with the zero address.

- **Mutant:** [`4109.sol`](4109.sol)
- **Caught by:** [`rvHoValuationRefusesAnUnopenedHolding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L168)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4109`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoValuationRefusesAnUnopenedHolding`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -239,7 +239,7 @@
     /// @inheritdoc IHoldings
     function valuation(PoolId poolId, ShareClassId scId, AssetId assetId) external view returns (IValuation) {
         Holding storage holding_ = _holding[poolId][scId][assetId];
-        require(address(holding_.valuation) != address(0), HoldingNotFound());
+        // MUTATION: removed the open-holding check
 
         return holding_.valuation;
     }
```

## Holdings #4110

The sync notification bumps the sequence number again, so marking a network synced advances its nonce twice.

- **Mutant:** [`4110.sol`](4110.sol)
- **Caught by:** [`hlHoPublishingASyncMarkerAlwaysAdvancesTheSequence`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L87)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4110`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoPublishingASyncMarkerAlwaysAdvancesTheSequence`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -261,6 +261,9 @@
     function _callOnSync(PoolId poolId, ShareClassId scId, uint16 centrifugeId, Snapshot memory snapshot_) internal {
         if (!snapshot_.isSnapshot) return;
 
+        // MUTATION: the sync notification burns a sequence number of its own
+        snapshot[poolId][scId][centrifugeId].nonce++;
+
         ISnapshotHook hook = snapshotHook[poolId];
         if (address(hook) != address(0)) hook.onSync(poolId, scId, centrifugeId);
     }
```

## Holdings #4111

decrease rebases the row onto its net amount and zeroes the withdrawal counter, so both flow histories are lost.

- **Mutant:** [`4111.sol`](4111.sol)
- **Caught by:** [`hlHoDepositHistoryRecordsTheInflowAndSurvivesTheOutflow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L4) · [`hlHoWithdrawalHistoryRecordsTheWholeOutflow`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4111`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoDepositHistoryRecordsTheInflowAndSurvivesTheOutflow hlHoWithdrawalHistoryRecordsTheWholeOutflow`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -172,6 +172,9 @@
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
         holding_.decreasedAmount += amount_;
+        // MUTATION: the row is rebased onto its net position, discarding both flow histories
+        holding_.increasedAmount = _amount(holding_);
+        holding_.decreasedAmount = 0;
         uint128 removedAmount = (oldAmount - _amount(holding_)).toUint128();
 
         // Remove carrying value pro-rata to the realized decrease (an over-decrease is capped at the current
```

## Holdings #4112

increase subtracts the realized value from the holding instead of adding it, so the value it reports is not the value it books.

- **Mutant:** [`4112.sol`](4112.sol)
- **Caught by:** [`hlHoIncreaseReturnsTheValueItBooked`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4112`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoIncreaseReturnsTheValueItBooked`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -155,7 +155,7 @@
             ? holding_.valuation.getQuote(poolId, scId, assetId, realized)
             : 0;
 
-        holding_.assetAmountValue += amountValue;
+        holding_.assetAmountValue -= amountValue; // MUTATION: the realized increase is subtracted
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
 
         emit Increase(poolId, scId, assetId, amount_, amountValue);
```

## Holdings #4113

decrease adds the removed value to the holding instead of subtracting it, so the value it reports is not the value it removes.

- **Mutant:** [`4113.sol`](4113.sol)
- **Caught by:** [`hlHoDecreaseReturnsTheValueItRemoved`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4113`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoDecreaseReturnsTheValueItRemoved`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -181,7 +181,7 @@
         // moved since the last update() (a full drain would leave residual value behind).
         amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
 
-        holding_.assetAmountValue -= amountValue;
+        holding_.assetAmountValue += amountValue; // MUTATION: the removed value is added
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
 
         emit Decrease(poolId, scId, assetId, amount_, amountValue);
```

## Holdings #4114

update reports the new total value instead of the change it applied, so the journal books the whole value as a move.

- **Mutant:** [`4114.sol`](4114.sol)
- **Caught by:** [`hlHoUpdateReportsTheRevaluationItWrote`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L70)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4114`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoUpdateReportsTheRevaluationItWrote`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -199,7 +199,7 @@
         uint128 currentAmountValue = holding_.valuation.getQuote(poolId, scId, assetId, _amount(holding_).toUint128());
 
         isPositive = currentAmountValue >= holding_.assetAmountValue;
-        diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
+        diffValue = currentAmountValue; // MUTATION: the revaluation reports the new total instead of the move
 
         holding_.assetAmountValue = currentAmountValue;
 
```

## Holdings #4115

updateValuation also copies the first journal account onto the second, so repointing a price source reroutes the holding's ledger entries.

- **Mutant:** [`4115.sol`](4115.sol)
- **Caught by:** [`vtHoAccountWiringMovesOnlyThroughItsTwoWriters`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L67)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4115`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule vtHoAccountWiringMovesOnlyThroughItsTwoWriters`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -83,6 +83,8 @@
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
         holding_.valuation = valuation_;
+        // MUTATION: repointing the price source also rewires the second journal account onto the first
+        accountId[poolId][scId][assetId][1] = accountId[poolId][scId][assetId][0];
 
         emit UpdateValuation(poolId, scId, assetId, valuation_);
     }
```

## Holdings #4116

callOnTransferSnapshot deletes the pool's hook after notifying it, so later syncs and transfers no longer reach it.

- **Mutant:** [`4116.sol`](4116.sol)
- **Caught by:** [`vtHoSnapshotHookMovesOnlyThroughItsSetter`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L85)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4116`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule vtHoSnapshotHookMovesOnlyThroughItsSetter`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -129,6 +129,8 @@
         ISnapshotHook hook = snapshotHook[poolId];
         if (address(hook) != address(0)) {
             hook.onTransfer(poolId, scId, originCentrifugeId, targetCentrifugeId, amount_);
+            // MUTATION: the hook is detached once it has been notified
+            delete snapshotHook[poolId];
         }
     }
 
```

## Holdings #4117

decrease resets the inflow total to the net amount and the outflow total to zero, so both lifetime totals shrink.

- **Mutant:** [`4117.sol`](4117.sol)
- **Caught by:** [`vtHoDepositHistoryNeverShrinks`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L6) · [`vtHoWithdrawalHistoryNeverShrinks`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4117`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule vtHoDepositHistoryNeverShrinks vtHoWithdrawalHistoryNeverShrinks`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -172,6 +172,9 @@
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
         holding_.decreasedAmount += amount_;
+        // MUTATION: the row is rebased onto its net position, discarding both flow histories
+        holding_.increasedAmount = _amount(holding_);
+        holding_.decreasedAmount = 0;
         uint128 removedAmount = (oldAmount - _amount(holding_)).toUint128();
 
         // Remove carrying value pro-rata to the realized decrease (an over-decrease is capped at the current
```

## Holdings #4118

updateValuation accepts the zero address as a price source, so repointing a holding erases the record that the pool ever opened it.

- **Mutant:** [`4118.sol`](4118.sol)
- **Caught by:** [`vtHoOpenedHoldingIsNeverClosed`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4118`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule vtHoOpenedHoldingIsNeverClosed`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -77,7 +77,7 @@
 
     /// @inheritdoc IHoldings
     function updateValuation(PoolId poolId, ShareClassId scId, AssetId assetId, IValuation valuation_) external auth {
-        require(address(valuation_) != address(0), WrongValuation());
+        // MUTATION: removed the check that the new price source is a real one
 
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) != address(0), HoldingNotFound());
```

## Holdings #4119

setSnapshot decrements the snapshot nonce instead of incrementing it, so a network's ordering sequence runs backwards instead of advancing one step.

- **Mutant:** [`4119.sol`](4119.sol)
- **Caught by:** [`vtHoSnapshotNonceStepsByAtMostOne`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L51)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 4119`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule vtHoSnapshotNonceStepsByAtMostOne`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -105,7 +105,7 @@
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
         snapshot_.isSnapshot = isSnapshot;
-        snapshot_.nonce++;
+        snapshot_.nonce--; // MUTATION: nonce decremented instead of incremented
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
```

## Holdings #6600

opening a holding demands that the row already be open, so a pool can never open the first holding of its share class.

- **Mutant:** [`6600.sol`](6600.sol)
- **Caught by:** [`rcHoOpeningThePoolsFirstHoldingIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6600`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoOpeningThePoolsFirstHoldingIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -51,7 +51,7 @@
         require(address(valuation_) != address(0), WrongValuation());
 
         Holding storage holding_ = _holding[poolId][scId][assetId];
-        require(address(holding_.valuation) == address(0), AlreadyInitialized());
+        require(address(holding_.valuation) != address(0), AlreadyInitialized()); // MUTATION: the one shot opening guard is inverted, so opening demands an already open row
 
         holding_.valuation = valuation_;
 
```

## Holdings #6601

initialize wires only three of the four ledger accounts, so the fourth journal kind is left unrouted after opening.

- **Mutant:** [`6601.sol`](6601.sol)
- **Caught by:** [`rcHoOpeningWiringAllFourLedgerAccountsIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L25)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6601`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoOpeningWiringAllFourLedgerAccountsIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -55,7 +55,7 @@
 
         holding_.valuation = valuation_;
 
-        for (uint256 i; i < 4; i++) {
+        for (uint256 i; i < 3; i++) { // MUTATION: the opening call wires only three of the four ledger accounts
             accountId[poolId][scId][assetId][uint8(i)] = accounts[i];
         }
 
```

## Holdings #6602

the opening call never records the price source it was handed, so a row opened beside a live sibling still reports no price source.

- **Mutant:** [`6602.sol`](6602.sol)
- **Caught by:** [`rcHoOpeningASecondHoldingIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L42)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6602`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoOpeningASecondHoldingIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -53,7 +53,7 @@
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) == address(0), AlreadyInitialized());
 
-        holding_.valuation = valuation_;
+        // MUTATION: the opening call never records the price source it was handed
 
         for (uint256 i; i < 4; i++) {
             accountId[poolId][scId][assetId][uint8(i)] = accounts[i];
```

## Holdings #6603

increase values a deposit only when it realizes nothing, so a real deposit is always booked at zero value.

- **Mutant:** [`6603.sol`](6603.sol)
- **Caught by:** [`rcHoBookingADepositIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L60)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6603`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoBookingADepositIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -151,7 +151,7 @@
 
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
         // valuation. Uninitialized holdings track amount only; their value is established at initialization.
-        amountValue = realized != 0 && address(holding_.valuation) != address(0)
+        amountValue = realized == 0 && address(holding_.valuation) != address(0) // MUTATION: the realized increase test is inverted, so a real deposit is never valued
             ? holding_.valuation.getQuote(poolId, scId, assetId, realized)
             : 0;
 
```

## Holdings #6605

increase now refuses a zero amount instead of absorbing it, so an empty deposit report reverts.

- **Mutant:** [`6605.sol`](6605.sol)
- **Caught by:** [`rcHoZeroDepositIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L78)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6605`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoZeroDepositIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -143,6 +143,8 @@
         returns (uint128 amountValue)
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
+        // MUTATION: an empty deposit is turned away instead of being absorbed
+        require(amount_ != 0, WrongAssetId());
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
```

## Holdings #6606

a deposit is valued at par instead of by its price source, so a holding priced at zero still books value.

- **Mutant:** [`6606.sol`](6606.sol)
- **Caught by:** [`rcHoDepositPricedAtNothingIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L98)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6606`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoDepositPricedAtNothingIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -152,7 +152,7 @@
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
         // valuation. Uninitialized holdings track amount only; their value is established at initialization.
         amountValue = realized != 0 && address(holding_.valuation) != address(0)
-            ? holding_.valuation.getQuote(poolId, scId, assetId, realized)
+            ? realized // MUTATION: the deposit is valued at par instead of at the price source the row reports
             : 0;
 
         holding_.assetAmountValue += amountValue;
```

## Holdings #6607

a deposit is refused until the holding has a price source, so a report for an unopened holding reverts.

- **Mutant:** [`6607.sol`](6607.sol)
- **Caught by:** [`rcHoBookingADepositBeforeTheRowIsOpenedIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L118)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6607`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoBookingADepositBeforeTheRowIsOpenedIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -143,6 +143,8 @@
         returns (uint128 amountValue)
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
+        // MUTATION: a deposit is refused until the row has a price source attached
+        require(address(holding_.valuation) != address(0), HoldingNotFound());
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
```

## Holdings #6608

a holding netted exactly back to balance still counts as short, so an exact repayment leaves the deficit counts raised.

- **Mutant:** [`6608.sol`](6608.sol)
- **Caught by:** [`rcHoClearingADeficitExactlyIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L138)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6608`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoClearingADeficitExactlyIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -156,7 +156,8 @@
             : 0;
 
         holding_.assetAmountValue += amountValue;
-        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
+        // MUTATION: a row netted back to its boundary is still counted as short
+        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount >= holding_.increasedAmount);
 
         emit Increase(poolId, scId, assetId, amount_, amountValue);
     }
```

## Holdings #6609

a withdrawal reports the value removed but never deducts it, so the holding keeps its full carrying value.

- **Mutant:** [`6609.sol`](6609.sol)
- **Caught by:** [`rcHoBookingAWithdrawalIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L160)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6609`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoBookingAWithdrawalIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -181,7 +181,7 @@
         // moved since the last update() (a full drain would leave residual value behind).
         amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
 
-        holding_.assetAmountValue -= amountValue;
+        // MUTATION: the withdrawal reports the value it removed but never takes it off the carrying value
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
 
         emit Decrease(poolId, scId, assetId, amount_, amountValue);
```

## Holdings #6610

a withdrawal larger than the position is refused, so a pool can no longer take out more than a row holds.

- **Mutant:** [`6610.sol`](6610.sol)
- **Caught by:** [`rcHoWithdrawingPastThePositionIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L178)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6610`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoWithdrawingPastThePositionIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -168,6 +168,8 @@
         returns (uint128 amountValue)
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
+        // MUTATION: a withdrawal larger than the position is refused instead of being admitted
+        require(amount_ <= _amount(holding_), WrongAssetId());
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
```

## Holdings #6611

a withdrawal sized exactly to the position is refused, so a pool can never close a holding to precisely nothing.

- **Mutant:** [`6611.sol`](6611.sol)
- **Caught by:** [`rcHoClosingThePositionExactlyIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L203)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6611`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoClosingThePositionExactlyIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -168,6 +168,8 @@
         returns (uint128 amountValue)
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
+        // MUTATION: a withdrawal sized exactly to the position is refused
+        require(amount_ != _amount(holding_), WrongAssetId());
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
```

## Holdings #6612

a withdrawal on a row that is already short is refused, so a shortfall can never be deepened once it opens.

- **Mutant:** [`6612.sol`](6612.sol)
- **Caught by:** [`rcHoDeepeningADeficitIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L224)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6612`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoDeepeningADeficitIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -168,6 +168,8 @@
         returns (uint128 amountValue)
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
+        // MUTATION: a withdrawal on a row that is already short is refused
+        require(holding_.increasedAmount >= holding_.decreasedAmount, HoldingNotFound());
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
```

## Holdings #6613

entering deficit pins the pool network deficit counter to one instead of adding a row to it, so a second short row is never counted.

- **Mutant:** [`6613.sol`](6613.sol)
- **Caught by:** [`rcHoDeficitCountCarryingASecondShortRowIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L245)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6613`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoDeficitCountCarryingASecondShortRowIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -275,9 +275,10 @@
 
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
-        uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
-        emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
+        // MUTATION: entering deficit pins the pool network counter to one instead of adding a row to it
+        if (isDeficit) networkDeficitCount[poolId][centrifugeId] = 1;
+        else --networkDeficitCount[poolId][centrifugeId];
+        emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkDeficitCount[poolId][centrifugeId]);
     }
 
     /// @dev Current amount, derived from the cumulative counters and floored at zero.
```

## Holdings #6614

a withdrawal is refused until the holding has a price source, so an outflow for an unopened holding reverts.

- **Mutant:** [`6614.sol`](6614.sol)
- **Caught by:** [`rcHoBookingAWithdrawalBeforeTheRowIsOpenedIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L265)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6614`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoBookingAWithdrawalBeforeTheRowIsOpenedIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -168,6 +168,8 @@
         returns (uint128 amountValue)
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
+        // MUTATION: a withdrawal is refused until the row has a price source attached
+        require(address(holding_.valuation) != address(0), HoldingNotFound());
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
```

## Holdings #6615

a revaluation can only ever mark a holding down, so a price rise never reaches the pool carrying value.

- **Mutant:** [`6615.sol`](6615.sol)
- **Caught by:** [`rcHoRevaluationUpwardIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L286)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6615`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoRevaluationUpwardIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -201,7 +201,9 @@
         isPositive = currentAmountValue >= holding_.assetAmountValue;
         diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
 
-        holding_.assetAmountValue = currentAmountValue;
+        // MUTATION: a revaluation can only ever mark a holding down
+        holding_.assetAmountValue =
+            currentAmountValue < holding_.assetAmountValue ? currentAmountValue : holding_.assetAmountValue;
 
         emit Update(poolId, scId, assetId, isPositive, diffValue);
     }
```

## Holdings #6616

a revaluation can only ever mark a holding up, so a price fall never reaches the pool carrying value.

- **Mutant:** [`6616.sol`](6616.sol)
- **Caught by:** [`rcHoRevaluationDownwardIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L303)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6616`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoRevaluationDownwardIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -201,7 +201,9 @@
         isPositive = currentAmountValue >= holding_.assetAmountValue;
         diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
 
-        holding_.assetAmountValue = currentAmountValue;
+        // MUTATION: a revaluation can only ever mark a holding up
+        holding_.assetAmountValue =
+            currentAmountValue > holding_.assetAmountValue ? currentAmountValue : holding_.assetAmountValue;
 
         emit Update(poolId, scId, assetId, isPositive, diffValue);
     }
```

## Holdings #6617

a revaluation that would leave the carrying value exactly where it is refuses instead of being absorbed.

- **Mutant:** [`6617.sol`](6617.sol)
- **Caught by:** [`rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L210)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6617`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -197,6 +197,8 @@
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
         uint128 currentAmountValue = holding_.valuation.getQuote(poolId, scId, assetId, _amount(holding_).toUint128());
+        // MUTATION: a revaluation that would leave the carrying value where it is refuses instead
+        require(currentAmountValue != holding_.assetAmountValue, HoldingNotFound());
 
         isPositive = currentAmountValue >= holding_.assetAmountValue;
         diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
```

## Holdings #6618

a revaluation is refused on a row that carries no position, so an empty holding can never be repriced.

- **Mutant:** [`6618.sol`](6618.sol)
- **Caught by:** [`rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L210)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6618`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -195,6 +195,8 @@
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) != address(0), HoldingNotFound());
+        // MUTATION: a revaluation is refused on a row that carries no position
+        require(_amount(holding_) != 0, HoldingNotFound());
 
         uint128 currentAmountValue = holding_.valuation.getQuote(poolId, scId, assetId, _amount(holding_).toUint128());
 
```

## Holdings #6619

the in sync marker is never published, so a network can be stepped through its sequence but never declared reconciled.

- **Mutant:** [`6619.sol`](6619.sol)
- **Caught by:** [`rcHoMarkingANetworkInSyncIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L321)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6619`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoMarkingANetworkInSyncIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -104,7 +104,7 @@
         Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
-        snapshot_.isSnapshot = isSnapshot;
+        snapshot_.isSnapshot = false; // MUTATION: the in sync marker is never published
         snapshot_.nonce++;
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
```

## Holdings #6620

the in sync marker latches on, so a network that has been declared reconciled can never be marked out of sync again.

- **Mutant:** [`6620.sol`](6620.sol)
- **Caught by:** [`rcHoMarkingANetworkOutOfSyncIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L339)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6620`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoMarkingANetworkOutOfSyncIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -104,7 +104,7 @@
         Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
-        snapshot_.isSnapshot = isSnapshot;
+        snapshot_.isSnapshot = true; // MUTATION: the marker latches on and can never be taken back off
         snapshot_.nonce++;
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
```

## Holdings #6621

the ordering sequence advances only when a network is marked in sync, so a desync is not counted as a step.

- **Mutant:** [`6621.sol`](6621.sol)
- **Caught by:** [`rcHoSyncAndDesyncRoundTripIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L357)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6621`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoSyncAndDesyncRoundTripIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -105,7 +105,7 @@
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
         snapshot_.isSnapshot = isSnapshot;
-        snapshot_.nonce++;
+        if (isSnapshot) snapshot_.nonce++; // MUTATION: the ordering sequence advances only when a network is marked in sync
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
```

## Holdings #6623

the automation setter detaches instead of attaching, so a pool can never route its NAV notifications to a callee.

- **Mutant:** [`6623.sol`](6623.sol)
- **Caught by:** [`rcHoAttachingNavAutomationIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L379)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6623`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoAttachingNavAutomationIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -91,7 +91,7 @@
     function setSnapshotHook(PoolId poolId, ISnapshotHook hook) external auth {
         require(hubRegistry.exists(poolId), NonExistingPool());
 
-        snapshotHook[poolId] = hook;
+        delete snapshotHook[poolId]; // MUTATION: the setter detaches automation instead of attaching what it was handed
 
         emit SetSnapshotHook(poolId, hook);
     }
```

## Holdings #6624

the snapshot hook setter refuses the zero address, so a hook can be attached but never removed.

- **Mutant:** [`6624.sol`](6624.sol)
- **Caught by:** [`rcHoAutomationAttachAndDetachRoundTripIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L393)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6624`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoAutomationAttachAndDetachRoundTripIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -90,6 +90,8 @@
     /// @inheritdoc IHoldings
     function setSnapshotHook(PoolId poolId, ISnapshotHook hook) external auth {
         require(hubRegistry.exists(poolId), NonExistingPool());
+        // MUTATION: the setter refuses the zero callee, so automation can be attached but never taken off
+        require(address(hook) != address(0), WrongValuation());
 
         snapshotHook[poolId] = hook;
 
```

## Holdings #6625

rewiring a ledger account records the request but never moves the account the holding points at.

- **Mutant:** [`6625.sol`](6625.sol)
- **Caught by:** [`rcHoRewiringALedgerAccountIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L412)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6625`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoRewiringALedgerAccountIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -70,7 +70,7 @@
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
-        accountId[poolId][scId][assetId][kind] = accountId_;
+        // MUTATION: rewiring records the request but never moves the account the holding points at
 
         emit SetAccountId(poolId, scId, assetId, kind, accountId_);
     }
```

## Holdings #6626

repointing a holding leaves the price source it already had in place, so a position can never be moved onto another oracle.

- **Mutant:** [`6626.sol`](6626.sol)
- **Caught by:** [`rcHoSwappingThePriceSourceIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L428)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6626`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoSwappingThePriceSourceIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -82,7 +82,7 @@
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
-        holding_.valuation = valuation_;
+        // MUTATION: repointing leaves the price source the row already had in place
 
         emit UpdateValuation(poolId, scId, assetId, valuation_);
     }
```

## Holdings #6627

revoking authority emits the event but never clears the ward, so granted authority can never be taken back.

- **Mutant:** [`6627.sol`](6627.sol)
- **Caught by:** [`rcHoWardGrantAndRevokeRoundTripIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L451)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6627`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoWardGrantAndRevokeRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        // MUTATION: the revocation records the event but never takes the ward off the roll
         emit Deny(user);
     }
 }
```

## Holdings #6628

a deposit reports the value it was quoted but never adds it to the carrying value, so funding a position leaves its book empty.

- **Mutant:** [`6628.sol`](6628.sol)
- **Caught by:** [`rcHoOpeningAndFullyClosingAPositionIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L470)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6628`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoOpeningAndFullyClosingAPositionIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -155,7 +155,7 @@
             ? holding_.valuation.getQuote(poolId, scId, assetId, realized)
             : 0;
 
-        holding_.assetAmountValue += amountValue;
+        // MUTATION: the deposit reports the value it was quoted but never adds it to the carrying value
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
 
         emit Increase(poolId, scId, assetId, amount_, amountValue);
```

## Holdings #6629

the pool network deficit counter only ever climbs, so leaving a deficit never takes the row back off the count.

- **Mutant:** [`6629.sol`](6629.sol)
- **Caught by:** [`rcHoEnteringAndLeavingADeficitIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L491)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 6629`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoEnteringAndLeavingADeficitIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -276,7 +276,8 @@
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
         uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+            // MUTATION: leaving deficit no longer takes the row back off the count
+            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : networkDeficitCount[poolId][centrifugeId];
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

## Holdings #7200

booking an inflow no longer requires write rights, so anyone can move a holding's amount, value and deficit count.

- **Mutant:** [`7200.sol`](7200.sol)
- **Caught by:** [`acHoDepositHistoryMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L20) · [`acHoCarryingValueMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L54) · [`acHoDeficitCountMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L152)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7200`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_access_control.conf --rule acHoDepositHistoryMovesOnlyForAWard acHoCarryingValueMovesOnlyForAWard acHoDeficitCountMovesOnlyForAWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -139,8 +139,7 @@
     /// @inheritdoc IHoldings
     function increase(PoolId poolId, ShareClassId scId, AssetId assetId, uint16 centrifugeId, uint128 amount_)
         external
-        auth
-        returns (uint128 amountValue)
+        returns (uint128 amountValue) // MUTATION: increase loses its ward gate
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
 
```

## Holdings #7201

booking an outflow no longer requires the caller to hold write rights, so anyone can inflate a position's withdrawal history.

- **Mutant:** [`7201.sol`](7201.sol)
- **Caught by:** [`acHoWithdrawalHistoryMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7201`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_access_control.conf --rule acHoWithdrawalHistoryMovesOnlyForAWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -164,8 +164,7 @@
     /// @inheritdoc IHoldings
     function decrease(PoolId poolId, ShareClassId scId, AssetId assetId, uint16 centrifugeId, uint128 amount_)
         external
-        auth
-        returns (uint128 amountValue)
+        returns (uint128 amountValue) // MUTATION: decrease loses its ward gate
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
 
```

## Holdings #7202

rewiring a position to a different journal account no longer requires the caller to hold write rights.

- **Mutant:** [`7202.sol`](7202.sol)
- **Caught by:** [`acHoJournalWiringMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L87)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7202`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_access_control.conf --rule acHoJournalWiringMovesOnlyForAWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -64,8 +64,7 @@
 
     /// @inheritdoc IHoldings
     function setAccountId(PoolId poolId, ShareClassId scId, AssetId assetId, uint8 kind, AccountId accountId_)
-        external
-        auth
+        external // MUTATION: the journal wiring setter loses its ward gate
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) != address(0), HoldingNotFound());
```

## Holdings #7203

repointing a position at a different price source no longer requires the caller to hold write rights.

- **Mutant:** [`7203.sol`](7203.sol)
- **Caught by:** [`acHoPriceSourceMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L70)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7203`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_access_control.conf --rule acHoPriceSourceMovesOnlyForAWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -76,7 +76,7 @@
     }
 
     /// @inheritdoc IHoldings
-    function updateValuation(PoolId poolId, ShareClassId scId, AssetId assetId, IValuation valuation_) external auth {
+    function updateValuation(PoolId poolId, ShareClassId scId, AssetId assetId, IValuation valuation_) external { // MUTATION: the price source setter loses its ward gate
         require(address(valuation_) != address(0), WrongValuation());
 
         Holding storage holding_ = _holding[poolId][scId][assetId];
```

## Holdings #7204

repointing a pool at a different snapshot hook no longer requires the caller to hold write rights.

- **Mutant:** [`7204.sol`](7204.sol)
- **Caught by:** [`acHoSnapshotHookMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L104)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7204`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_access_control.conf --rule acHoSnapshotHookMovesOnlyForAWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -88,7 +88,7 @@
     }
 
     /// @inheritdoc IHoldings
-    function setSnapshotHook(PoolId poolId, ISnapshotHook hook) external auth {
+    function setSnapshotHook(PoolId poolId, ISnapshotHook hook) external { // MUTATION: the snapshot hook setter loses its ward gate
         require(hubRegistry.exists(poolId), NonExistingPool());
 
         snapshotHook[poolId] = hook;
```

## Holdings #7205

setting the sync marker no longer requires write rights, so anyone can flip it and burn its nonce.

- **Mutant:** [`7205.sol`](7205.sol)
- **Caught by:** [`acHoSyncMarkerMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L120) · [`acHoSnapshotNonceMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L136)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7205`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_access_control.conf --rule acHoSyncMarkerMovesOnlyForAWard acHoSnapshotNonceMovesOnlyForAWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -98,8 +98,7 @@
 
     /// @inheritdoc IHoldings
     function setSnapshot(PoolId poolId, ShareClassId scId, uint16 centrifugeId, bool isSnapshot, uint64 nonce)
-        external
-        auth
+        external // MUTATION: the snapshot marker setter loses its ward gate
     {
         Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
```

## Holdings #7206

granting write rights no longer requires the caller to hold them, so any address can make itself a ward of the ledger.

- **Mutant:** [`7206.sol`](7206.sol)
- **Caught by:** [`acHoWardRightsMoveOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7206`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_access_control.conf --rule acHoWardRightsMoveOnlyForAWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -22,7 +22,7 @@
     }
 
     /// @inheritdoc IAuth
-    function rely(address user) public auth {
+    function rely(address user) public { // MUTATION: granting write rights no longer requires holding them
         wards[user] = 1;
         emit Rely(user);
     }
```

## Holdings #7207

booking an inflow no longer requires the caller to hold write rights, so the call succeeds where it must have failed.

- **Mutant:** [`7207.sol`](7207.sol)
- **Caught by:** [`rvHoIncreaseRefusesANonWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L117)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7207`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoIncreaseRefusesANonWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -139,8 +139,7 @@
     /// @inheritdoc IHoldings
     function increase(PoolId poolId, ShareClassId scId, AssetId assetId, uint16 centrifugeId, uint128 amount_)
         external
-        auth
-        returns (uint128 amountValue)
+        returns (uint128 amountValue) // MUTATION: increase loses its ward gate
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
 
```

## Holdings #7208

replaying the sync notification no longer requires write rights, so any caller drives the pool's NAV automation.

- **Mutant:** [`7208.sol`](7208.sol)
- **Caught by:** [`rvHoCallOnSyncSnapshotRefusesANonWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L182)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7208`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoCallOnSyncSnapshotRefusesANonWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -113,7 +113,7 @@
     }
 
     /// @inheritdoc IHoldings
-    function callOnSyncSnapshot(PoolId poolId, ShareClassId scId, uint16 centrifugeId) external auth {
+    function callOnSyncSnapshot(PoolId poolId, ShareClassId scId, uint16 centrifugeId) external { // MUTATION: the ward gate is gone
         Snapshot memory snapshot_ = snapshot[poolId][scId][centrifugeId];
         _callOnSync(poolId, scId, centrifugeId, snapshot_);
     }
```

## Holdings #7209

notifying the hook of a cross network transfer no longer requires write rights, so any caller drives it.

- **Mutant:** [`7209.sol`](7209.sol)
- **Caught by:** [`rvHoCallOnTransferSnapshotRefusesANonWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L196)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 7209`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoCallOnTransferSnapshotRefusesANonWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -125,7 +125,7 @@
         uint16 originCentrifugeId,
         uint16 targetCentrifugeId,
         uint128 amount_
-    ) external auth {
+    ) external { // MUTATION: the ward gate is gone
         ISnapshotHook hook = snapshotHook[poolId];
         if (address(hook) != address(0)) {
             hook.onTransfer(poolId, scId, originCentrifugeId, targetCentrifugeId, amount_);
```

## Holdings #8000

the share class deficit counter is read but never moved on a crossing, so a class with short rows reports none.

- **Mutant:** [`8000.sol`](8000.sol)
- **Caught by:** [`deficitCountMatchesTheClassShortRows`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L48)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8000`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule deficitCountMatchesTheClassShortRows`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -273,8 +273,7 @@
     {
         if (wasDeficit == isDeficit) return;
 
-        uint32 count =
-            isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
+        uint32 count = deficitCount[poolId][scId][centrifugeId]; // MUTATION: the class counter no longer moves
         uint32 networkCount =
             isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
```

## Holdings #8001

increaseCountedUnder books inflow on one class but moves another class's deficit count, so per class counts go wrong.

- **Mutant:** [`8001.sol`](8001.sol)
- **Caught by:** [`deficitCountIsKeptPerShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L18)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8001`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_share_class_properties.conf --rule deficitCountIsKeptPerShareClass`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -280,6 +280,21 @@
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
+    /// @notice MUTATION: books flow on one class while counting its crossing under another class.
+    function increaseCountedUnder(
+        PoolId poolId,
+        ShareClassId scId,
+        ShareClassId countedScId,
+        AssetId assetId,
+        uint16 centrifugeId,
+        uint128 amount_
+    ) external auth {
+        Holding storage holding_ = _holding[poolId][scId][assetId];
+
+        bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
+        holding_.increasedAmount += amount_;
+        _updateDeficit(poolId, countedScId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
+    }
     /// @dev Current amount, derived from the cumulative counters and floored at zero.
     function _amount(Holding storage holding_) internal view returns (uint256) {
         return
```

## Holdings #8002

a new shortfall is counted on network zero instead of the named network, so the wrong network's rollup rises.

- **Mutant:** [`8002.sol`](8002.sol)
- **Caught by:** [`hlHoEnteringADeficitBooksTheNamedNetworkOnly`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L39)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8002`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_network_properties.conf --rule hlHoEnteringADeficitBooksTheNamedNetworkOnly`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -276,7 +276,7 @@
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
         uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+            isDeficit ? ++networkDeficitCount[poolId][0] : --networkDeficitCount[poolId][centrifugeId]; // MUTATION: the entry lands on a fixed network bucket
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

## Holdings #8003

the sync gate is inverted, so the snapshot hook fires while the network is out of sync and never once it is synced.

- **Mutant:** [`8003.sol`](8003.sol)
- **Caught by:** [`hlHoSyncNotificationCarriesTheMarkersOwnKeys`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L102)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8003`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoSyncNotificationCarriesTheMarkersOwnKeys`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -259,7 +259,7 @@
     //----------------------------------------------------------------------------------------------
 
     function _callOnSync(PoolId poolId, ShareClassId scId, uint16 centrifugeId, Snapshot memory snapshot_) internal {
-        if (!snapshot_.isSnapshot) return;
+        if (snapshot_.isSnapshot) return; // MUTATION: the sync gate is inverted
 
         ISnapshotHook hook = snapshotHook[poolId];
         if (address(hook) != address(0)) hook.onSync(poolId, scId, centrifugeId);
```

## Holdings #8004

a cleared shortfall is released from network zero instead of the named network, so the named network stays counted short.

- **Mutant:** [`8004.sol`](8004.sol)
- **Caught by:** [`hlHoLeavingADeficitReleasesTheNamedNetworkOnly`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L65)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8004`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_network_properties.conf --rule hlHoLeavingADeficitReleasesTheNamedNetworkOnly`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -276,7 +276,7 @@
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
         uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][0]; // MUTATION: the release lands on a fixed network bucket
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

## Holdings #8005

the pool network rollup is overwritten with the acting class's count, so two classes short on one network report one.

- **Mutant:** [`8005.sol`](8005.sol)
- **Caught by:** [`rcHoTwoShareClassesShortOnOneNetworkIsReachable`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L142)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8005`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_share_class_properties.conf --rule rcHoTwoShareClassesShortOnOneNetworkIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -275,8 +275,7 @@
 
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
-        uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+        uint32 networkCount = networkDeficitCount[poolId][centrifugeId] = count; // MUTATION: the rollup mirrors the acting class
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

## Holdings #8006

publishing a sync marker clears that share class network's shortfall tally, so a network with short rows reports none from the next marker on.

- **Mutant:** [`8006.sol`](8006.sol)
- **Caught by:** [`stHoDeficitCountersMoveOnlyThroughTheFlowEntries`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L251)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8006`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule stHoDeficitCountersMoveOnlyThroughTheFlowEntries`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -106,6 +106,7 @@
 
         snapshot_.isSnapshot = isSnapshot;
         snapshot_.nonce++;
+        delete deficitCount[poolId][scId][centrifugeId]; // MUTATION: a published marker clears the class tally
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
```

## Holdings #8007

each crossing also copies the network rollup onto the next network id, so the rollups no longer sum to the short rows.

- **Mutant:** [`8007.sol`](8007.sol)
- **Caught by:** [`deficitCountsSumToTheShortRowsAcrossTheNetworks`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8007`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_network_properties.conf --rule deficitCountsSumToTheShortRowsAcrossTheNetworks`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -277,6 +277,7 @@
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
         uint32 networkCount =
             isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+        networkDeficitCount[poolId][centrifugeId + 1] = networkCount; // MUTATION: the crossing mirrors onto the neighbouring network
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

## Holdings #8008

a release floors both shortfall tallies at zero instead of reverting, so a network counting none accepts the release.

- **Mutant:** [`8008.sol`](8008.sol)
- **Caught by:** [`rvHoLeavingADeficitIsRefusedWhenTheNamedNetworkCountsNone`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L93)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8008`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_network_properties.conf --rule rvHoLeavingADeficitIsRefusedWhenTheNamedNetworkCountsNone`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -273,10 +273,16 @@
     {
         if (wasDeficit == isDeficit) return;
 
-        uint32 count =
-            isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
-        uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+        uint32 count = isDeficit // MUTATION: a release floors both tallies at zero instead of refusing
+            ? ++deficitCount[poolId][scId][centrifugeId]
+            : (deficitCount[poolId][scId][centrifugeId] == 0 ? uint32(0) : --deficitCount[poolId][scId][centrifugeId]);
+        uint32 networkCount = isDeficit
+            ? ++networkDeficitCount[poolId][centrifugeId]
+            : (
+                networkDeficitCount[poolId][centrifugeId] == 0
+                    ? uint32(0)
+                    : --networkDeficitCount[poolId][centrifugeId]
+            );
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

## Holdings #8009

a row lifted out of shortfall is never counted out, so a network's shortfall count only ever rises.

- **Mutant:** [`8009.sol`](8009.sol)
- **Caught by:** [`rcHoShortfallAttributionCanOutliveItsNetworkIsReachable`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L120)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8009`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_network_properties.conf --rule rcHoShortfallAttributionCanOutliveItsNetworkIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -271,7 +271,7 @@
     function _updateDeficit(PoolId poolId, ShareClassId scId, uint16 centrifugeId, bool wasDeficit, bool isDeficit)
         internal
     {
-        if (wasDeficit == isDeficit) return;
+        if (wasDeficit == isDeficit || !isDeficit) return; // MUTATION: a row lifted out of shortfall is not counted out
 
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
```

## Holdings #8052

the share class shortfall counter moves the wrong way, so entering shortfall counts down and leaving it counts up.

- **Mutant:** [`8052.sol`](8052.sol)
- **Caught by:** [`stHhClassDeficitCountFollowsTheShortRows`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L194)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8052`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule stHhClassDeficitCountFollowsTheShortRows`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -274,7 +274,7 @@
         if (wasDeficit == isDeficit) return;
 
         uint32 count =
-            isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
+            isDeficit ? --deficitCount[poolId][scId][centrifugeId] : ++deficitCount[poolId][scId][centrifugeId]; // MUTATION: the class counter moves the wrong way
         uint32 networkCount =
             isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
```

## Holdings #8053

the sync gate is inverted, so the snapshot hook hears every report except the one that marks the network synced.

- **Mutant:** [`8053.sol`](8053.sol)
- **Caught by:** [`hlHhSyncNotificationOnlyOnAClosedBatch`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L376)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8053`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhSyncNotificationOnlyOnAClosedBatch`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -259,7 +259,7 @@
     //----------------------------------------------------------------------------------------------
 
     function _callOnSync(PoolId poolId, ShareClassId scId, uint16 centrifugeId, Snapshot memory snapshot_) internal {
-        if (!snapshot_.isSnapshot) return;
+        if (snapshot_.isSnapshot) return; // MUTATION: the hook hears every report but the closing one
 
         ISnapshotHook hook = snapshotHook[poolId];
         if (address(hook) != address(0)) hook.onSync(poolId, scId, centrifugeId);
```

## Holdings #8058

a crossing moves the network rollup but not the share class shortfall counter, so the class count goes stale.

- **Mutant:** [`8058.sol`](8058.sol)
- **Caught by:** [`rcHhAssetWithdrawalEnteringDeficitIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L188) · [`rcHhAssetDepositLeavingDeficitIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L211)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8058`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhAssetWithdrawalEnteringDeficitIsReachable rcHhAssetDepositLeavingDeficitIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -273,8 +273,7 @@
     {
         if (wasDeficit == isDeficit) return;
 
-        uint32 count =
-            isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
+        uint32 count = deficitCount[poolId][scId][centrifugeId]; // MUTATION: the class counter no longer moves
         uint32 networkCount =
             isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
```

## Holdings #8070

a crossing moves the pool network rollup while the share class tally stands still, so the event reports a class count no crossing ever changed.

- **Mutant:** [`8070.sol`](8070.sol)
- **Caught by:** [`rcHoClearingADeficitExactlyIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L138) · [`rcHoWithdrawingPastThePositionIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L178) · [`rcHoDeficitCountCarryingASecondShortRowIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L245) · [`rcHoEnteringAndLeavingADeficitIsReachable`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L491)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8070`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoClearingADeficitExactlyIsReachable rcHoWithdrawingPastThePositionIsReachable rcHoDeficitCountCarryingASecondShortRowIsReachable rcHoEnteringAndLeavingADeficitIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -273,8 +273,7 @@
     {
         if (wasDeficit == isDeficit) return;
 
-        uint32 count =
-            isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
+        uint32 count = deficitCount[poolId][scId][centrifugeId]; // MUTATION: the crossing skips the share class tally
         uint32 networkCount =
             isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
```

## Holdings #8100

publishing a sync marker also advances the neighbouring network's snapshot nonce, so one network's marker moves another network's snapshot row.

- **Mutant:** [`8100.sol`](8100.sol)
- **Caught by:** [`stHoSnapshotRowIsPerNetwork`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L232)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8100`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule stHoSnapshotRowIsPerNetwork`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -106,6 +106,7 @@
 
         snapshot_.isSnapshot = isSnapshot;
         snapshot_.nonce++;
+        snapshot[poolId][scId][centrifugeId ^ 1].nonce++; // MUTATION: the neighbouring network's nonce moves too
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
```

## Holdings #8101

increaseAcrossClasses books one inflow on two share classes of the pool at once, so flow on one class restates the other class's holding row.

- **Mutant:** [`8101.sol`](8101.sol)
- **Caught by:** [`stHoFlowRowIsPerShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L26)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8101`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_share_class_properties.conf --rule stHoFlowRowIsPerShareClass`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -161,6 +161,26 @@
         emit Increase(poolId, scId, assetId, amount_, amountValue);
     }
 
+    /// @notice MUTATION: books one inflow on two share classes of the pool at once.
+    function increaseAcrossClasses(
+        PoolId poolId,
+        ShareClassId scId,
+        ShareClassId otherScId,
+        AssetId assetId,
+        uint16 centrifugeId,
+        uint128 amount_
+    ) external auth {
+        Holding storage holding_ = _holding[poolId][scId][assetId];
+        Holding storage other_ = _holding[poolId][otherScId][assetId];
+
+        bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
+        bool otherWasDeficit = other_.decreasedAmount > other_.increasedAmount;
+        holding_.increasedAmount += amount_;
+        other_.increasedAmount += amount_;
+        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
+        _updateDeficit(poolId, otherScId, centrifugeId, otherWasDeficit, other_.decreasedAmount > other_.increasedAmount);
+    }
+
     /// @inheritdoc IHoldings
     function decrease(PoolId poolId, ShareClassId scId, AssetId assetId, uint16 centrifugeId, uint128 amount_)
         external
```

## Holdings #8102

replaying the sync notification no longer reads the stored marker, so a network in sync is never renotified to the pool's NAV hook.

- **Mutant:** [`8102.sol`](8102.sol)
- **Caught by:** [`hlHoReplayNotifiesUnderTheMarkersOwnKeys`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8102`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoReplayNotifiesUnderTheMarkersOwnKeys`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -114,7 +114,7 @@
 
     /// @inheritdoc IHoldings
     function callOnSyncSnapshot(PoolId poolId, ShareClassId scId, uint16 centrifugeId) external auth {
-        Snapshot memory snapshot_ = snapshot[poolId][scId][centrifugeId];
+        Snapshot memory snapshot_; // MUTATION: the replay reads a fresh marker, never in sync
         _callOnSync(poolId, scId, centrifugeId, snapshot_);
     }
 
```

## Holdings #8103

increase refuses inflow unless the network shortfall tally equals the class tally, so a sibling class's shortfall blocks deposits.

- **Mutant:** [`8103.sol`](8103.sol)
- **Caught by:** [`rvHoIncreaseBeforeOpeningIsNeverRefusedOverASiblingClassShortfall`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L125)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8103`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_share_class_properties.conf --rule rvHoIncreaseBeforeOpeningIsNeverRefusedOverASiblingClassShortfall`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -156,6 +156,7 @@
             : 0;
 
         holding_.assetAmountValue += amountValue;
+        require(networkDeficitCount[poolId][centrifugeId] == deficitCount[poolId][scId][centrifugeId]); // MUTATION: the counters must agree
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
 
         emit Increase(poolId, scId, assetId, amount_, amountValue);
```

## Holdings #8104

clearDeficit lets any caller wipe a share class network's shortfall tally, so the class counter moves without the ledger's authority.

- **Mutant:** [`8104.sol`](8104.sol)
- **Caught by:** [`acHoDeficitCountMovesOnlyForAWard`](../../specs/core/hub/Holdings/single/Holdings_single_pool_access_control.spec#L152)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8104`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_access_control.conf --rule acHoDeficitCountMovesOnlyForAWard`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -110,6 +110,11 @@
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
         _callOnSync(poolId, scId, centrifugeId, snapshot_);
+    }
+
+    /// @notice MUTATION: an open entry that wipes a share class network's shortfall tally.
+    function clearDeficit(PoolId poolId, ShareClassId scId, uint16 centrifugeId) external {
+        deficitCount[poolId][scId][centrifugeId] = 0;
     }
 
     /// @inheritdoc IHoldings
```

## Holdings #8105

increaseTagging books inflow in one pool but bumps a shortfall count in another pool, so one pool's flow moves another's.

- **Mutant:** [`8105.sol`](8105.sol)
- **Caught by:** [`stHoDeficitCountAndHookIgnoreASiblingsFlow`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L74)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8105`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_pool_properties.conf --rule stHoDeficitCountAndHookIgnoreASiblingsFlow`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -161,6 +161,20 @@
         emit Increase(poolId, scId, assetId, amount_, amountValue);
     }
 
+    /// @notice MUTATION: books flow on one pool's row and tallies a shortfall on another pool's share class.
+    function increaseTagging(
+        PoolId poolId,
+        PoolId tallyPoolId,
+        ShareClassId scId,
+        ShareClassId tallyScId,
+        AssetId assetId,
+        uint16 centrifugeId,
+        uint128 amount_
+    ) external auth {
+        _holding[poolId][scId][assetId].increasedAmount += amount_;
+        deficitCount[tallyPoolId][tallyScId][centrifugeId] += 1;
+    }
+
     /// @inheritdoc IHoldings
     function decrease(PoolId poolId, ShareClassId scId, AssetId assetId, uint16 centrifugeId, uint128 amount_)
         external
```

## Holdings #8415

a revaluation prices an oversized net amount on its truncated low bits instead of refusing, so the holding is marked to a wrong value.

- **Mutant:** [`8415.sol`](8415.sol)
- **Caught by:** [`rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L210)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8415`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoUpdateRefusesOnlyANonWardAnUnopenedRowOrAnOversizedNet`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -196,7 +196,7 @@
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
-        uint128 currentAmountValue = holding_.valuation.getQuote(poolId, scId, assetId, _amount(holding_).toUint128());
+        uint128 currentAmountValue = holding_.valuation.getQuote(poolId, scId, assetId, uint128(_amount(holding_))); // MUTATION: an oversized net is truncated instead of refused
 
         isPositive = currentAmountValue >= holding_.assetAmountValue;
         diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
```

## Holdings #8416

the amount view truncates an oversized net amount instead of refusing, so a huge holding reads as a smaller one.

- **Mutant:** [`8416.sol`](8416.sol)
- **Caught by:** [`rvHoAmountViewsRefuseOnlyANetPastUint128`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L228)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8416`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoAmountViewsRefuseOnlyANetPastUint128`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -223,7 +223,7 @@
 
     /// @inheritdoc IHoldings
     function amount(PoolId poolId, ShareClassId scId, AssetId assetId) external view returns (uint128 amount_) {
-        return _amount(_holding[poolId][scId][assetId]).toUint128();
+        return uint128(_amount(_holding[poolId][scId][assetId])); // MUTATION: an oversized net is truncated instead of refused
     }
 
     /// @inheritdoc IHoldings
```

## Holdings #8417

the holding view truncates an oversized net amount instead of refusing, so a huge holding reads as a smaller one.

- **Mutant:** [`8417.sol`](8417.sol)
- **Caught by:** [`rvHoAmountViewsRefuseOnlyANetPastUint128`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L228)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8417`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoAmountViewsRefuseOnlyANetPastUint128`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -251,7 +251,7 @@
         returns (uint128 assetAmount, uint128 assetAmountValue, IValuation valuation_)
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
-        return (_amount(holding_).toUint128(), holding_.assetAmountValue, holding_.valuation);
+        return (uint128(_amount(holding_)), holding_.assetAmountValue, holding_.valuation); // MUTATION: an oversized net is truncated instead of refused
     }
 
     //----------------------------------------------------------------------------------------------
```

## Holdings #8418

the holding view truncates each lifetime total before netting them, so a holding with very large totals can report a wrong amount.

- **Mutant:** [`8418.sol`](8418.sol)
- **Caught by:** [`hlHoHoldingViewReportsTheFlooredNetOfWideTotals`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L238)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8418`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoHoldingViewReportsTheFlooredNetOfWideTotals`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -251,7 +251,7 @@
         returns (uint128 assetAmount, uint128 assetAmountValue, IValuation valuation_)
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
-        return (_amount(holding_).toUint128(), holding_.assetAmountValue, holding_.valuation);
+        return (uint128(holding_.increasedAmount) >= uint128(holding_.decreasedAmount) ? uint128(holding_.increasedAmount) - uint128(holding_.decreasedAmount) : 0, holding_.assetAmountValue, holding_.valuation); // MUTATION: the net is taken on counters cut to uint128
     }
 
     //----------------------------------------------------------------------------------------------
```

## Holdings #8811

increase quotes the whole position instead of the added amount, so an admin's inflow to an open holding with an oversized net reverts though no total or value overflows.

- **Mutant:** [`8811.sol`](8811.sol)
- **Caught by:** [`rvHoIncreaseOnAnOpenHoldingFailsOnlyOnAnOverflowingTotalOrValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reverts.spec#L246)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 8811`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reverts.conf --rule rvHoIncreaseOnAnOpenHoldingFailsOnlyOnAnOverflowingTotalOrValue`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -152,7 +152,7 @@
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
         // valuation. Uninitialized holdings track amount only; their value is established at initialization.
         amountValue = realized != 0 && address(holding_.valuation) != address(0)
-            ? holding_.valuation.getQuote(poolId, scId, assetId, realized)
+            ? holding_.valuation.getQuote(poolId, scId, assetId, _amount(holding_).toUint128()) // MUTATION: the deposit is quoted on the narrowed whole position, not the realized part
             : 0;
 
         holding_.assetAmountValue += amountValue;
```

## Holdings #9012

the pool's network shortfall rollup is updated on the next network id, so the named network's rollup never moves.

- **Mutant:** [`9012.sol`](9012.sol)
- **Caught by:** [`stHoDeficitCountsOfAtMostOneNetworkMovePerCall`](../../specs/core/hub/Holdings/Holdings_multi_network_properties.spec#L17)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9012`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_network_properties.conf --rule stHoDeficitCountsOfAtMostOneNetworkMovePerCall`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -276,7 +276,7 @@
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
         uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+            isDeficit ? ++networkDeficitCount[poolId][centrifugeId + 1] : --networkDeficitCount[poolId][centrifugeId + 1]; // MUTATION: the rollup is kept one network over
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

## Holdings #9013

setSnapshot writes the flag under a fixed share class but the nonce under the named one, so one call moves two classes.

- **Mutant:** [`9013.sol`](9013.sol)
- **Caught by:** [`stHoSnapshotRowIsPerShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L82)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9013`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_share_class_properties.conf --rule stHoSnapshotRowIsPerShareClass`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -104,7 +104,7 @@
         Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
-        snapshot_.isSnapshot = isSnapshot;
+        snapshot[poolId][ShareClassId.wrap(bytes16(uint128(1)))][centrifugeId].isSnapshot = isSnapshot; // MUTATION: the flag is written under a fixed class
         snapshot_.nonce++;
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
```

## Holdings #9032

replaying a sync notice also spends the network's sequence number, so a replay moves the nonce without any snapshot update.

- **Mutant:** [`9032.sol`](9032.sol)
- **Caught by:** [`vtHoSnapshotSequenceMovesOnlyThroughItsPublisher`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L102)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9032`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule vtHoSnapshotSequenceMovesOnlyThroughItsPublisher`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -115,7 +115,7 @@
     /// @inheritdoc IHoldings
     function callOnSyncSnapshot(PoolId poolId, ShareClassId scId, uint16 centrifugeId) external auth {
         Snapshot memory snapshot_ = snapshot[poolId][scId][centrifugeId];
-        _callOnSync(poolId, scId, centrifugeId, snapshot_);
+        snapshot[poolId][scId][centrifugeId].nonce++; _callOnSync(poolId, scId, centrifugeId, snapshot_); // MUTATION: a replay spends a sequence number
     }
 
     /// @inheritdoc IHoldings
```

## Holdings #9048

A holding's price source can be reset to the zero address, so a valued holding keeps its value with no valuation.

- **Mutant:** [`9048.sol`](9048.sol)
- **Caught by:** [`uninitializedHoldingHasNoValue`](../../specs/core/hub/Holdings/single/Holdings_single_pool_valid_state.spec#L26)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9048`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_valid_state.conf --rule uninitializedHoldingHasNoValue`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -77,7 +77,7 @@
 
     /// @inheritdoc IHoldings
     function updateValuation(PoolId poolId, ShareClassId scId, AssetId assetId, IValuation valuation_) external auth {
-        require(address(valuation_) != address(0), WrongValuation());
+        // MUTATION: removed the check that the new price source is not the zero address
 
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) != address(0), HoldingNotFound());
```

## Holdings #9049

The pool's deficit counter on a network is not lowered when a holding recovers, so it overcounts holdings in deficit.

- **Mutant:** [`9049.sol`](9049.sol)
- **Caught by:** [`networkDeficitCountIsItsNetworksShortRowCensus`](../../specs/core/hub/Holdings/Holdings_census_properties.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9049`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/census_properties.conf --rule networkDeficitCountIsItsNetworksShortRowCensus`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -276,7 +276,7 @@
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
         uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : networkDeficitCount[poolId][centrifugeId]; // MUTATION: the pool rollup is no longer lowered when a holding leaves deficit
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

## Holdings #9058

A share class's deficit counter on a network is not lowered when a holding recovers, so it overcounts holdings in deficit.

- **Mutant:** [`9058.sol`](9058.sol)
- **Caught by:** [`deficitCountIsItsClassNetworksShortRowCensus`](../../specs/core/hub/Holdings/Holdings_census_properties.spec#L12)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9058`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/census_properties.conf --rule deficitCountIsItsClassNetworksShortRowCensus`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -274,7 +274,7 @@
         if (wasDeficit == isDeficit) return;
 
         uint32 count =
-            isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
+            isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : deficitCount[poolId][scId][centrifugeId]; // MUTATION: the class counter is no longer lowered when a holding leaves deficit
         uint32 networkCount =
             isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
```

## Holdings #9080

decrease removes carrying value only on a full drain, so a partial withdrawal leaves all the value on the book.

- **Mutant:** [`9080.sol`](9080.sol)
- **Caught by:** [`hlHoDecreaseRemovesValueProRataToTheRealizedAmount`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L142)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9080`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoDecreaseRemovesValueProRataToTheRealizedAmount`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -179,7 +179,7 @@
         // storage mutation and can never over-journal. Deliberately NOT a live oracle quote like increase():
         // pro-rata preserves `amount == 0 => value == 0`, which a live quote would break when the price has
         // moved since the last update() (a full drain would leave residual value behind).
-        amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
+        amountValue = removedAmount == oldAmount ? holding_.assetAmountValue : 0; // MUTATION: only a full drain removes value
 
         holding_.assetAmountValue -= amountValue;
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
```

## Holdings #9081

every inflow calls the snapshot hook regardless of the sync marker, so it can fire while books are out of step.

- **Mutant:** [`9081.sol`](9081.sol)
- **Caught by:** [`stHoSyncNotificationOnlyUnderAnInSyncMarker`](../../specs/core/hub/Holdings/single/Holdings_single_pool_transitions.spec#L268)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9081`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_transitions.conf --rule stHoSyncNotificationOnlyUnderAnInSyncMarker`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -159,6 +159,7 @@
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
 
         emit Increase(poolId, scId, assetId, amount_, amountValue);
+        if (address(snapshotHook[poolId]) != address(0)) snapshotHook[poolId].onSync(poolId, scId, centrifugeId); // MUTATION: a deposit notifies the hook unconditionally
     }
 
     /// @inheritdoc IHoldings
```

## Holdings #9082

update also writes the new carrying value onto the same asset in a sibling share class, so revaluing one class restates another.

- **Mutant:** [`9082.sol`](9082.sol)
- **Caught by:** [`stHoHoldingRowIsPerShareClass`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L47)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9082`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_share_class_properties.conf --rule stHoHoldingRowIsPerShareClass`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -202,6 +202,7 @@
         diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
 
         holding_.assetAmountValue = currentAmountValue;
+        _holding[poolId][ShareClassId.wrap(~ShareClassId.unwrap(scId))][assetId].assetAmountValue = currentAmountValue; // MUTATION: the revaluation also lands on a sibling class
 
         emit Update(poolId, scId, assetId, isPositive, diffValue);
     }
```

## Holdings #9083

setting a snapshot uses one fixed share class's row, so all classes of a pool share one nonce sequence.

- **Mutant:** [`9083.sol`](9083.sol)
- **Caught by:** [`hlHoSetSnapshotBumpsTheNamedClassesNonce`](../../specs/core/hub/Holdings/Holdings_multi_share_class_properties.spec#L104)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9083`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_share_class_properties.conf --rule hlHoSetSnapshotBumpsTheNamedClassesNonce`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -101,7 +101,7 @@
         external
         auth
     {
-        Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
+        Snapshot storage snapshot_ = snapshot[poolId][ShareClassId.wrap(bytes16(uint128(1)))][centrifugeId]; // MUTATION: the row is keyed by a constant class
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
         snapshot_.isSnapshot = isSnapshot;
```

## Holdings #9084

setting a snapshot uses one fixed pool's row, so all pools share one nonce sequence.

- **Mutant:** [`9084.sol`](9084.sol)
- **Caught by:** [`hlHoSetSnapshotBumpsTheNamedPoolsNonce`](../../specs/core/hub/Holdings/Holdings_multi_pool_properties.spec#L99)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9084`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/multi_pool_properties.conf --rule hlHoSetSnapshotBumpsTheNamedPoolsNonce`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -101,7 +101,7 @@
         external
         auth
     {
-        Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
+        Snapshot storage snapshot_ = snapshot[PoolId.wrap(1)][scId][centrifugeId]; // MUTATION: the row is keyed by a constant pool
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
         snapshot_.isSnapshot = isSnapshot;
```

## Holdings #9086

an accepted report no longer advances its network's snapshot sequence, so the same asset or share report can be replayed under the same nonce.

- **Mutant:** [`9086.sol`](9086.sol)
- **Caught by:** [`hlHhAcceptedAssetReportSpendsItsNetworksNonceOnce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L465) · [`hlHhAcceptedShareReportSpendsItsNetworksNonceOnce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L484)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9086`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhAcceptedAssetReportSpendsItsNetworksNonceOnce hlHhAcceptedShareReportSpendsItsNetworksNonceOnce`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -105,7 +105,7 @@
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
         snapshot_.isSnapshot = isSnapshot;
-        snapshot_.nonce++;
+        // MUTATION: the snapshot sequence is no longer advanced
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
```

## Holdings #9470

a deposit into a holding in shortfall is priced on its full size, so the shortfall repayment is booked as value.

- **Mutant:** [`9470.sol`](9470.sol)
- **Caught by:** [`hlHoIncreaseQuotesOnlyTheRealizedAmount`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L163)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9470`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoIncreaseQuotesOnlyTheRealizedAmount`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -152,7 +152,7 @@
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
         // valuation. Uninitialized holdings track amount only; their value is established at initialization.
         amountValue = realized != 0 && address(holding_.valuation) != address(0)
-            ? holding_.valuation.getQuote(poolId, scId, assetId, realized)
+            ? holding_.valuation.getQuote(poolId, scId, assetId, amount_) // MUTATION: the whole inflow is quoted
             : 0;
 
         holding_.assetAmountValue += amountValue;
```

## Holdings #9471

a deposit into a holding in shortfall is priced on its full size, so the shortfall repayment is priced too.

- **Mutant:** [`9471.sol`](9471.sol)
- **Caught by:** [`rcHoNettingInflowPricesOnlyItsPositivePart`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L540)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9471`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoNettingInflowPricesOnlyItsPositivePart`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -152,7 +152,7 @@
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
         // valuation. Uninitialized holdings track amount only; their value is established at initialization.
         amountValue = realized != 0 && address(holding_.valuation) != address(0)
-            ? holding_.valuation.getQuote(poolId, scId, assetId, realized)
+            ? holding_.valuation.getQuote(poolId, scId, assetId, amount_) // MUTATION: the whole inflow is quoted
             : 0;
 
         holding_.assetAmountValue += amountValue;
```

## Holdings #9472

a revaluation prices a holding's gross deposits instead of its net amount, so a holding with withdrawals is overvalued.

- **Mutant:** [`9472.sol`](9472.sol)
- **Caught by:** [`hlHoUpdateMarksTheBookToTheQuoteOfItsAmount`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L187)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9472`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoUpdateMarksTheBookToTheQuoteOfItsAmount`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -196,7 +196,7 @@
         Holding storage holding_ = _holding[poolId][scId][assetId];
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
-        uint128 currentAmountValue = holding_.valuation.getQuote(poolId, scId, assetId, _amount(holding_).toUint128());
+        uint128 currentAmountValue = holding_.valuation.getQuote(poolId, scId, assetId, (_amount(holding_) == 0 ? 0 : holding_.increasedAmount).toUint128()); // MUTATION: a live row is quoted on its gross deposits
 
         isPositive = currentAmountValue >= holding_.assetAmountValue;
         diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
```

## Holdings #9473

a partial withdrawal is priced at a live quote of the removed amount, capped at the carrying value, instead of pro rata to the book.

- **Mutant:** [`9473.sol`](9473.sol)
- **Caught by:** [`hlHoDecreaseNeverConsultsTheOracle`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L210)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9473`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoDecreaseNeverConsultsTheOracle`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -179,7 +179,7 @@
         // storage mutation and can never over-journal. Deliberately NOT a live oracle quote like increase():
         // pro-rata preserves `amount == 0 => value == 0`, which a live quote would break when the price has
         // moved since the last update() (a full drain would leave residual value behind).
-        amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
+        amountValue = oldAmount == 0 ? 0 : removedAmount == oldAmount ? holding_.assetAmountValue : MathLib.min(holding_.valuation.getQuote(poolId, scId, assetId, removedAmount), holding_.assetAmountValue).toUint128(); // MUTATION: a partial withdrawal takes a live quote
 
         holding_.assetAmountValue -= amountValue;
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
```

## Holdings #9474

a partial withdrawal books off a live quote capped at the carrying value, so it no longer removes a pro rata share.

- **Mutant:** [`9474.sol`](9474.sol)
- **Caught by:** [`rcHoDecreaseBooksOffTheQuoteJustTaken`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L516)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9474`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoDecreaseBooksOffTheQuoteJustTaken`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -179,7 +179,7 @@
         // storage mutation and can never over-journal. Deliberately NOT a live oracle quote like increase():
         // pro-rata preserves `amount == 0 => value == 0`, which a live quote would break when the price has
         // moved since the last update() (a full drain would leave residual value behind).
-        amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
+        amountValue = oldAmount == 0 ? 0 : removedAmount == oldAmount ? holding_.assetAmountValue : MathLib.min(holding_.valuation.getQuote(poolId, scId, assetId, removedAmount), holding_.assetAmountValue).toUint128(); // MUTATION: a partial withdrawal takes a live quote
 
         holding_.assetAmountValue -= amountValue;
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
```

## Holdings #9475

moving a holding onto another price source asks the new source for a quote of the position and throws the answer away.

- **Mutant:** [`9475.sol`](9475.sol)
- **Caught by:** [`hlHoPriceSourceSwapLeavesTheCarryingValueStanding`](../../specs/core/hub/Holdings/single/Holdings_single_pool_high_level.spec#L223)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9475`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_high_level.conf --rule hlHoPriceSourceSwapLeavesTheCarryingValueStanding`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -83,6 +83,7 @@
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
         holding_.valuation = valuation_;
+        valuation_.getQuote(poolId, scId, assetId, _amount(holding_).toUint128()); // MUTATION: the new source is asked for a discarded quote
 
         emit UpdateValuation(poolId, scId, assetId, valuation_);
     }
```

## Holdings #9476

switching a holding's price source queries the new source for a discarded quote, so a swap is no longer quote free.

- **Mutant:** [`9476.sol`](9476.sol)
- **Caught by:** [`rcHoStaleValueSurvivesAPriceSourceSwapOnALivePosition`](../../specs/core/hub/Holdings/single/Holdings_single_pool_reachability.spec#L557)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9476`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/single_pool_reachability.conf --rule rcHoStaleValueSurvivesAPriceSourceSwapOnALivePosition`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -83,6 +83,7 @@
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
         holding_.valuation = valuation_;
+        valuation_.getQuote(poolId, scId, assetId, _amount(holding_).toUint128()); // MUTATION: the new source is asked for a discarded quote
 
         emit UpdateValuation(poolId, scId, assetId, valuation_);
     }
```

## Holdings #9522

the pool's deficit counter on a network stops rising at two, so a third holding in deficit goes uncounted.

- **Mutant:** [`9522.sol`](9522.sol)
- **Caught by:** [`rcHoCensusReachesThreeShortRowsOnOneNetwork`](../../specs/core/hub/Holdings/Holdings_census_properties.spec#L19)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Holdings 9522`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Holdings/census_properties.conf --rule rcHoCensusReachesThreeShortRowsOnOneNetwork`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -276,7 +276,7 @@
         uint32 count =
             isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
         uint32 networkCount =
-            isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
+            isDeficit ? (networkDeficitCount[poolId][centrifugeId] = networkDeficitCount[poolId][centrifugeId] >= 2 ? 2 : networkDeficitCount[poolId][centrifugeId] + 1) : --networkDeficitCount[poolId][centrifugeId]; // MUTATION: the pool rollup saturates at two
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
     }
 
```

