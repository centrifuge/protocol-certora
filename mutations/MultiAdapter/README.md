# Mutations for `MultiAdapter` (`src/core/messaging/MultiAdapter.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [1802](#multiadapter-1802) | setAdapters no longer persists the advanced session counter, so the new roster is installed under a session id the counter never reached.<br>Caught by: [`sessionsAboveCounterEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L50) · [`activeSetSessionCurrentOrCleared`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L23) |
| [1803](#multiadapter-1803) | setAdapters steps the session counter backwards instead of forwards, leaving existing rosters and stashes above the counter.<br>Caught by: [`blockedAboveCounterEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L58) · [`sessionsAboveCounterEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L50) |
| [1804](#multiadapter-1804) | setAdapters no longer rejects a threshold above the adapter count, so a session can be installed with an unreachable vote threshold.<br>Caught by: [`registeredAdapterWellFormed`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L71) |
| [1805](#multiadapter-1805) | _installSession swaps the quorum and threshold fields, so an adapter row can record a quorum other than the roster size.<br>Caught by: [`adapterQuorumEqualsListLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L84) · [`registeredAdapterWellFormed`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L71) |
| [1806](#multiadapter-1806) | setAdapters reuses the current session id, so a new roster overwrites the live session, even session zero.<br>Caught by: [`sessionZeroNeverConfigured`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L66) · [`clearedActiveSetEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L28) · [`sessionThresholdUniform`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L95) · [`adapterIdPointsAtItsOwnSlot`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L119) |
| [1807](#multiadapter-1807) | _installSession assigns zero-based adapter ids, so the first adapter's row keeps the unregistered id while carrying live quorum data.<br>Caught by: [`listedAdapterHoldsItsIndex`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L107) · [`adapterIdPointsAtItsOwnSlot`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L119) |
| [1808](#multiadapter-1808) | _installSession starts registering at the second adapter, so the roster's first entry never receives its details row.<br>Caught by: [`listedAdapterHoldsItsIndex`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L107) |
| [1809](#multiadapter-1809) | blockSession inverts the active-session comparison, so blocking the live session stashes it as inactive and leaves the outbound route in place.<br>Caught by: [`blockedAtCounterWasActive`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L153) · [`blockedCounterClearsActiveSet`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L162) · [`activeSetMirrorsSessionList`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L36) |
| [1810](#multiadapter-1810) | blockSession no longer clears the outbound route when the blocked session is the active one, so sends keep fanning out to the stashed roster.<br>Caught by: [`activeSetMirrorsSessionList`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L36) · [`blockedCounterClearsActiveSet`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L162) |
| [1811](#multiadapter-1811) | blockSession clears only the route's session stamp and keeps its adapter list, leaving a roster behind on a cleared route.<br>Caught by: [`clearedActiveSetEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L28) · [`blockedCounterClearsActiveSet`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L162) |
| [1812](#multiadapter-1812) | blockSession stashes a session without removing its live adapter list, so the session is simultaneously live and blocked.<br>Caught by: [`blockedExcludesLive`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L131) · [`listedAdapterHoldsItsIndex`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L107) |
| [1813](#multiadapter-1813) | blockSession reads the threshold from the active session, so a blocked session can record a zero or oversized threshold.<br>Caught by: [`blockedThresholdWithinList`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L140) |
| [1814](#multiadapter-1814) | unblockSession restores the outbound route without checking the session is still current, so a stale session can overwrite the live route.<br>Caught by: [`activeSetSessionCurrentOrCleared`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L23) |
| [1816](#multiadapter-1816) | blocking a session stashes the live roster with its first entry duplicated, so the stashed list repeats an adapter.<br>Caught by: [`blockedListDistinct`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L174) |
| [1817](#multiadapter-1817) | The last adapter's details survive the block, so a row keeps a live quorum for a session whose roster is gone.<br>Caught by: [`adapterQuorumEqualsListLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L84) |
| [1818](#multiadapter-1818) | unblocking reinstalls the stashed roster at a threshold of one instead of the one it was stashed with.<br>Caught by: [`stMaUnblockRestoresExactlyWhatWasStashed`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L138) |
| [1819](#multiadapter-1819) | unblocking restores the active set without checking the session is still the current one, so a superseded roster takes the live route back.<br>Caught by: [`stMaUnblockReopensTheRouteOnlyForTheSessionInService`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L166) |
| [1820](#multiadapter-1820) | setAdapters stamps the new live roster with the previous session's number, so outbound sends carry a stale session.<br>Caught by: [`stMaSessionAdvanceRestampsTheRoute`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L75) |
| [1822](#multiadapter-1822) | Blocking records the session as idle whatever it was, so a stash forgets that the session it holds was the one in service.<br>Caught by: [`stMaBlockStashesTheLiveRosterWhole`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L90) |
| [1826](#multiadapter-1826) | Blocking any session clears the set in service, so retiring a superseded session blacks out the live route.<br>Caught by: [`stMaBlockingASupersededSessionKeepsTheRoute`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L119) |
| [4900](#multiadapter-4900) | execute decrements every vote lane instead of only the quorum's, so lanes outside the quorum lose a vote.<br>Caught by: [`hlMaExecuteSparesTheThirdLaneOutsideTheQuorum`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L54) |
| [4901](#multiadapter-4901) | execute forwards a payload on a single confirmation instead of the session's threshold, so one adapter alone drives the gateway.<br>Caught by: [`hlMaExecuteSpendsATallyOnlyAtTheThreshold`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L4) |
| [5400](#multiadapter-5400) | The ward gate no longer checks the caller, so any account can rewire routes, appoint managers and send messages.<br>Caught by: [`acMaOnlyWardMovesTheWardSet`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L4) · [`acMaOnlyWardModifiesManagerRights`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L20) · [`acMaOnlyWardRepointsTheGateway`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L37) · [`acMaOnlyWardRepointsTheParser`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L53) · [`acMaOnlyWardFansOutASend`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L69) · [`acMaOnlyWardRepointsTheMessageGas`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L260) |
| [5401](#multiadapter-5401) | The transport gate admits non-wards and refuses wards, so outsiders can set, block and unblock adapter sessions.<br>Caught by: [`acMaOnlyWardOrManagerAdvancesTheSession`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L86) · [`acMaOnlyWardOrManagerMovesTheLiveRoute`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L104) · [`acMaOnlyWardOrManagerMovesASessionRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L129) · [`acMaOnlyWardOrManagerMovesAnAdapterRegistration`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L152) · [`acMaOnlyWardOrManagerMovesTheBlockedStash`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L179) |
| [5402](#multiadapter-5402) | Inbound deliveries no longer check the caller is the named adapter or a pool manager, so anyone can vote and release messages.<br>Caught by: [`acMaOnlyAdapterOrManagerReachesTheGateway`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L241) |
| [5403](#multiadapter-5403) | The ward check no longer looks at the caller, so any account can rewire routes, seat managers and send messages.<br>Caught by: [`rvMaFileRefusesANonWardOrAnUnknownName`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L6) · [`rvMaUpdateManagerRefusesANonWard`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L21) · [`rvMaSendRefusesANonWard`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L291) |
| [5404](#multiadapter-5404) | The transport gate admits every non-ward and refuses wards, so outsiders can rotate adapter sets and block or unblock sessions.<br>Caught by: [`rvMaSetAdaptersRefusesWithoutTransportAuthority`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L34) · [`rvMaBlockSessionRefusesAnOutsiderOrASessionWithNoRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L132) · [`rvMaUnblockSessionRefusesWithoutTransportAuthority`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L149) |
| [5405](#multiadapter-5405) | Inbound deliveries no longer check the caller is the named adapter or a pool manager, so anyone can vote and release messages.<br>Caught by: [`rvMaHandleRefusesAStrangerSubmission`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L194) · [`rvMaVoteRefusesAStrangerSubmission`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L209) · [`rvMaExecuteRefusesAStrangerSubmission`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L224) |
| [5406](#multiadapter-5406) | An unregistered adapter is put on the first vote lane instead of refused, so any account can vote and release messages.<br>Caught by: [`rvMaExecuteRefusesAnUnregisteredAdapter`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L239) · [`rvMaHandleRefusesAnUnregisteredSender`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L252) · [`rvMaVoteRefusesAnUnregisteredSender`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L265) · [`rvMaExecuteRefusesAnUnregisteredSender`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L278) |
| [5407](#multiadapter-5407) | An adapter set may be installed with a threshold above its size, so that route can never reach consensus.<br>Caught by: [`rvMaSetAdaptersRefusesAnUnreachableThreshold`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L50) |
| [5408](#multiadapter-5408) | A non-empty adapter set may be installed with a zero threshold, so messages execute without any bridge confirming them.<br>Caught by: [`rvMaSetAdaptersRefusesAZeroThresholdOverALiveRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L65) |
| [5409](#multiadapter-5409) | An adapter set may list the same adapter twice, so the quorum counts a vote lane no adapter can fill.<br>Caught by: [`rvMaSetAdaptersRefusesARepeatedAdapter`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L81) |
| [5410](#multiadapter-5410) | An install takes whatever session id the caller names instead of the next one, so old or skipped sessions can be installed.<br>Caught by: [`rvMaSetAdaptersRefusesAnUnexpectedSessionId`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L97) |
| [5411](#multiadapter-5411) | A rotation onto a single adapter under full consensus is refused, so the documented one bridge recovery install is unavailable to governance.<br>Caught by: [`rvMaSetAdaptersOnAFreshRosterAlwaysGoesThroughForAWard`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L112) |
| [5412](#multiadapter-5412) | A session that was never blocked can be unblocked, so the call wipes that session's adapter list.<br>Caught by: [`rvMaUnblockSessionRefusesWithoutAStashedSession`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L165) |
| [5413](#multiadapter-5413) | unblockSession refuses a blocked session with one adapter, so such a session can never be restored.<br>Caught by: [`rvMaUnblockSessionOfASingleStashAlwaysGoesThroughForAWard`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L179) |
| [5414](#multiadapter-5414) | send on a route with no adapters in service now succeeds instead of refusing, so the message is silently dropped.<br>Caught by: [`rvMaSendRefusesWithoutALiveRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L304) |
| [5415](#multiadapter-5415) | A route with no adapters in service is quoted at zero instead of refused, so a disabled route looks usable and free.<br>Caught by: [`rvMaEstimateRefusesWithoutALiveRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L317) |
| [5416](#multiadapter-5416) | Reading the quorum or threshold of a route with no adapters in service now fails instead of answering zero.<br>Caught by: [`rvMaQuorumAlwaysAnswers`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L330) · [`rvMaThresholdAlwaysAnswers`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L342) |
| [5417](#multiadapter-5417) | Once a route's session counter is spent, the next session id wraps to zero instead of failing, so callers get a bogus id.<br>Caught by: [`rvMaNextActiveSessionIdRefusesARouteWhoseCounterIsSpent`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L354) |
| [5418](#multiadapter-5418) | An install adopts the session id the caller names instead of the next one, so the session id can jump or move backwards.<br>Caught by: [`vtMaSessionIdNeverRegresses`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L6) · [`vtMaSessionIdAdvancesByOneAtMost`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L21) |
| [5419](#multiadapter-5419) | A rotation deletes the superseded session's adapter list, so that session can no longer be blocked while its adapters still vote.<br>Caught by: [`vtMaRosterMoveSparesOtherSessions`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L36) |
| [5420](#multiadapter-5420) | A message that reaches consensus is handed to the gateway twice, so one round of adapter confirmations is executed as two deliveries downstream.<br>Caught by: [`hlMaExecuteForwardsExactlyOneMessage`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L74) · [`hlMaHandleForwardsAtMostOnce`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L100) |
| [5421](#multiadapter-5421) | An executed message reaches the gateway under this chain's own id instead of its source chain, so its origin is misattributed.<br>Caught by: [`hlMaExecuteForwardsOnTheArrivalChain`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L88) |
| [5422](#multiadapter-5422) | The vote entry now also executes once the threshold is met, so a proof only confirmation releases the message to the gateway.<br>Caught by: [`hlMaVoteNeverReachesTheGateway`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L114) |
| [5423](#multiadapter-5423) | Restoring a blocked session also makes it the active session, so the pool's session id can roll back to an older one.<br>Caught by: [`vtMaSessionIdMovesOnlyByRotation`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L58) |
| [5424](#multiadapter-5424) | A rotation registers the new adapters under the superseded session, so its pending messages are weighed against the wrong adapters.<br>Caught by: [`hlMaRotationKeepsEarlierSessionAdapterIds`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L128) · [`hlMaRotationKeepsEarlierSessionQuorums`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L144) · [`hlMaRotationKeepsEarlierSessionThresholds`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L161) |
| [5425](#multiadapter-5425) | Restoring a blocked session reinstalls it with a threshold of one instead of its saved threshold, so fewer confirmations release a message.<br>Caught by: [`hlMaBlockThenUnblockKeepsTheThreshold`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L178) |
| [5426](#multiadapter-5426) | Each roster adapter is dispatched to twice per send, so every bridge is paid for and delivers the message twice.<br>Caught by: [`hlMaSendFansOutOncePerRosterMember`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L196) |
| [5427](#multiadapter-5427) | Each adapter send names the local chain instead of the requested destination, so messages leave for the wrong chain.<br>Caught by: [`hlMaSendCarriesTheRequestedChain`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L212) |
| [5428](#multiadapter-5428) | Each adapter send names the messaging contract as refund address, so unspent gas never reaches the caller's refund address.<br>Caught by: [`hlMaSendCarriesTheRefundAddressItWasGiven`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L224) |
| [5429](#multiadapter-5429) | Outbound payloads carry session id zero instead of the route's live session, so the receiving chain cannot accept them.<br>Caught by: [`hlMaSendWrapsThePayloadWithTheLiveSessionId`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L236) |
| [5430](#multiadapter-5430) | A send deletes the route's adapter set after dispatching, so the first message disables the pool's transport.<br>Caught by: [`hlMaSendLeavesTheLiveRouteWhereItStands`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L254) |
| [7000](#multiadapter-7000) | A full set of eight adapters is now refused at install, so a route can hold at most seven.<br>Caught by: [`rcMaRosterCapInstallIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L24) |
| [7001](#multiadapter-7001) | Installing adapters now requires the threshold to equal the adapter count, so a set such as two of three is refused.<br>Caught by: [`rcMaIntermediateThresholdInstallIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L42) |
| [7002](#multiadapter-7002) | An empty adapter set is now refused as a zero threshold, so a route can no longer be cleared by installing no adapters.<br>Caught by: [`rcMaManagerHaltsARouteWithTheEmptySetIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L61) |
| [7003](#multiadapter-7003) | The quorum and threshold views return zero for a route with a single adapter, so such a route looks unconfigured.<br>Caught by: [`rcMaFirstRosterInstallIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L4) · [`rcMaBlockThenUnblockRestoresTheRouteIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L100) |
| [7004](#multiadapter-7004) | Blocking any session clears the outbound route, so retiring a superseded session also cuts the route in service.<br>Caught by: [`rcMaBlockingASupersededSessionKeepsTheRouteIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L125) |
| [7005](#multiadapter-7005) | Blocking the active session clears the route's adapter list but keeps its session id, so the route names a dead session.<br>Caught by: [`rcMaBlockingTheSessionInServiceIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L82) |
| [7006](#multiadapter-7006) | Unblocking a formerly active session always restores it as the route, so a replaced adapter set takes the traffic back.<br>Caught by: [`rcMaUnblockingASupersededSessionKeepsTheRouteIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L143) |
| [7007](#multiadapter-7007) | An outbound send skips the last adapter of the roster, so a route with a single bridge sends nothing.<br>Caught by: [`hlMaSendFansOutOncePerRosterMember`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L196) · [`hlMaSendCarriesTheRequestedChain`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L212) · [`hlMaSendCarriesTheRefundAddressItWasGiven`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L224) · [`hlMaSendReachesEachRosterMemberOnce`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L289) |
| [7008](#multiadapter-7008) | A delivery that reaches the threshold only records its vote, so the message is released only by an explicit execution.<br>Caught by: [`rcMaThresholdOneLetsOneAdapterForwardAloneIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L260) |
| [7009](#multiadapter-7009) | An explicit execution requires strictly more confirmations than the threshold, so a tally that exactly meets it cannot be executed.<br>Caught by: [`rcMaExecuteDrivesASilentLaneNegativeIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L280) |
| [7010](#multiadapter-7010) | Deliveries use the active session, not the one their payload names, so a replaced set's pending messages face the wrong adapters.<br>Caught by: [`rcMaSupersededSessionStillDeliversIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L304) |
| [7011](#multiadapter-7011) | A pool manager seat can only be granted, so a revocation leaves the account holding the rights it should lose.<br>Caught by: [`rcMaManagerSeatGrantAndRevokeIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L330) |
| [7012](#multiadapter-7012) | Setting the message parser through file now reverts, so it can never be set after deployment.<br>Caught by: [`rcMaFileRepointsBothWiringTargetsIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L347) |
| [7013](#multiadapter-7013) | Revoking a ward sets its seat to one instead of zero, so the account keeps its admin rights.<br>Caught by: [`rcMaWardSeatGrantAndRevokeIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L367) |
| [7014](#multiadapter-7014) | Unblocking restores the outbound set only when the session is no longer active, so the active route stays empty.<br>Caught by: [`rcMaSendResumesAfterABlockAndUnblockIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L162) |
| [7015](#multiadapter-7015) | A delivery completes the quorum only above the threshold, so in a two of two session no delivery releases the message.<br>Caught by: [`rcMaSecondDeliveryCompletesTheQuorumIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L195) |
| [8109](#multiadapter-8109) | A vote no longer checks the caller is the named adapter or a pool manager, so anyone can vote on an adapter's behalf.<br>Caught by: [`acMaOnlyAdapterOrManagerMovesAVoteTally`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L205) |
| [8110](#multiadapter-8110) | Executing a message consumes one vote lane past the quorum, so the next adapter outside the quorum loses a confirmation.<br>Caught by: [`hlMaExecuteSparesTheSecondLaneOutsideTheQuorum`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L34) |
| [8524](#multiadapter-8524) | Filing the gas model stores it as the parser instead, so the gas model never changes and the parser is replaced by it.<br>Caught by: [`stMaFileWritesExactlyTheDependencyItsKeyNames`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L199) |
| [8525](#multiadapter-8525) | The configuration update drops its admin check, so any account can repoint the gateway, the parser and the gas model.<br>Caught by: [`acMaOnlyWardRepointsTheGateway`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L37) · [`acMaOnlyWardRepointsTheParser`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L53) · [`acMaOnlyWardRepointsTheMessageGas`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L260) |
| [8526](#multiadapter-8526) | The gas model key is no longer recognised, so filing a gas model reverts and the dependency can never be set.<br>Caught by: [`rvMaFileAcceptsAWardUnderAKnownName`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L454) |
| [8527](#multiadapter-8527) | A message's pool is read from the gas model instead of the parser, so whoever files the gas model picks which adapters authenticate it.<br>Caught by: [`hlMaVoteAsksTheFiledParserNotTheGasModel`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L158) |
| [8700](#multiadapter-8700) | An outbound send hands every adapter a zero gas limit instead of the given one, so destination execution gets no gas.<br>Caught by: [`hlMaSendCarriesTheGasLimitItWasGiven`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L275) |
| [8701](#multiadapter-8701) | An outbound send dispatches to the first adapter once per roster member, so the other adapters never carry the message.<br>Caught by: [`hlMaSendReachesEachRosterMemberOnce`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L289) |
| [8702](#multiadapter-8702) | Each adapter is called unpaid while its quote still counts against the caller, so the fee stays stranded in the router.<br>Caught by: [`hlMaSendFundsEachDispatchWithItsOwnQuote`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L307) |
| [8705](#multiadapter-8705) | Inbound messages are checked against the session after their stamped one, so an adapter of that later session can deliver them.<br>Caught by: [`rvMaHandleRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L368) |
| [8706](#multiadapter-8706) | Explicit execution requires more confirmations than the threshold, so a tally reaching exactly the threshold is never released.<br>Caught by: [`rcMaExecuteReleasesThePayloadAfterTwoProofsIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L228) |
| [8876](#multiadapter-8876) | An explicit execution weighs the global pool's tally instead of the routed pool's own, so another pool's confirmations release the message.<br>Caught by: [`hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L169) |
| [8877](#multiadapter-8877) | Installing an adapter set first asks every new adapter for a quote, so one rejecting new adapter blocks the whole rotation.<br>Caught by: [`hlMaRotationCallsNoAdapter`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L385) |
| [8878](#multiadapter-8878) | A send skips an adapter whose quote fails instead of failing, so a rejecting active adapter silently drops out of the send.<br>Caught by: [`rvMaSendFailsWhenARosterAdapterRefuses`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L469) |
| [8879](#multiadapter-8879) | The pool's adapter manager may vote for an adapter only at a threshold of one, so it alone can no longer release a two of two message.<br>Caught by: [`rcMaManagerAloneReleasesATwoOfTwoMessageIsReachable`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L206) |
| [8880](#multiadapter-8880) | An outbound send starts at the second active adapter, so a rejecting first adapter no longer fails the send.<br>Caught by: [`rvMaSendFailsWhenARosterAdapterRefuses`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L469) |
| [8952](#multiadapter-8952) | unblockSession never clears the stash, so a restored session stays blocked and live at once.<br>Caught by: [`blockedExcludesLive`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L131) |
| [9060](#multiadapter-9060) | A rotation never stores the advanced session id, so the pool keeps its old id while the route moves on.<br>Caught by: [`hlMaRotationBumpsTheSessionToTheNamedTarget`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L348) |
| [9061](#multiadapter-9061) | Releasing a message no longer spends its confirmations, so the same message can be released again.<br>Caught by: [`hlMaExecuteLowersTheTallyItSpends`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L99) · [`hlMaExecuteSpendsTheTallyBeforeForwarding`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L85) |
| [9077](#multiadapter-9077) | Outbound messages go out without the session stamp, so every bridge reads the first two body bytes as the session.<br>Caught by: [`hlMaSendDispatchesTheStampedPayloadAtFullLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L321) |
| [9078](#multiadapter-9078) | Outbound messages carry the session stamp twice, so every bridge receives the body two bytes late.<br>Caught by: [`hlMaSendDispatchesTheStampedPayloadAtFullLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L321) |
| [9079](#multiadapter-9079) | Outbound messages carry a stray trailing byte, so every bridge receives a body one byte longer than was sent.<br>Caught by: [`hlMaSendDispatchesTheStampedPayloadAtFullLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L321) |
| [9087](#multiadapter-9087) | An outbound dispatch carries the session stamp alone and drops the message body, so every bridge delivers an empty message.<br>Caught by: [`hlMaSendDispatchesTheStampedPayloadAtFullLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L321) |
| [9421](#multiadapter-9421) | A vote checks the submitter instead of the named adapter, so an adapter outside the session gets a vote.<br>Caught by: [`rvMaVoteRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L383) |
| [9422](#multiadapter-9422) | An execution checks the submitter instead of the named adapter, so a tally is spent for an adapter outside the session.<br>Caught by: [`rvMaExecuteRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L397) |
| [9423](#multiadapter-9423) | A self delivery is credited to the transaction origin, so a relaying manager delivers as an adapter it is not.<br>Caught by: [`rvMaSelfDeliveryHandleRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L412) |
| [9424](#multiadapter-9424) | A self vote is credited to the transaction origin, so a relaying manager votes as an adapter it is not.<br>Caught by: [`rvMaSelfDeliveryVoteRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L426) |
| [9425](#multiadapter-9425) | A self execution is credited to the transaction origin, so a relaying manager spends a tally as an adapter it is not.<br>Caught by: [`rvMaSelfDeliveryExecuteRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L440) |
| [9426](#multiadapter-9426) | Unblocking the session in service restores the route with an empty roster, so it still cannot send.<br>Caught by: [`stMaUnblockReopensTheRouteOnlyForTheSessionInService`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L166) |
| [9427](#multiadapter-9427) | Submissions are checked against the previous session, so an adapter dropped from the stamped one still votes and executes.<br>Caught by: [`rvMaVoteRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L383) · [`rvMaExecuteRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L397) · [`rvMaSelfDeliveryHandleRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L412) · [`rvMaSelfDeliveryVoteRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L426) · [`rvMaSelfDeliveryExecuteRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L440) |
| [9428](#multiadapter-9428) | Unblocking restores the stashed adapter set into the next session, so the unblocked session stays without adapters.<br>Caught by: [`hlMaUnblockEmptiesTheStashIntoItsOwnSession`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L364) |
| [9620](#multiadapter-9620) | An adapter is looked up in the active session, not the payload's stamped one, so a message stamped with a future session collects votes.<br>Caught by: [`futureSessionTallyEmpty`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L22) |
| [9621](#multiadapter-9621) | an explicit execution accepts a tally one confirmation short of the threshold, so a payload is released before enough adapters agreed.<br>Caught by: [`hlMaExecuteForwardsOnlyOverAThresholdOfPositiveLanes`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L60) |
| [9622](#multiadapter-9622) | The gateway is called before the tally is spent and again after, so a released message is delivered twice.<br>Caught by: [`hlMaExecuteSpendsTheTallyBeforeForwarding`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L85) |
| [9623](#multiadapter-9623) | a released payload reaches the gateway with its session stamp still attached, so the gateway parses two stamp bytes as the message.<br>Caught by: [`hlMaExecuteHandsTheGatewayTheUnstampedMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L113) · [`hlMaHandleHandsTheGatewayTheUnstampedMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L127) |
| [9625](#multiadapter-9625) | A delivery that completes the quorum forwards the stamped payload, so the gateway reads the stamp bytes as the message.<br>Caught by: [`hlMaHandleHandsTheGatewayTheUnstampedMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L127) |
| [9626](#multiadapter-9626) | a send refunds one wei less than the surplus, so the route keeps a wei of every overpaid send.<br>Caught by: [`hlMaSendRefundsTheSurplusAndKeepsNoEth`](../../specs/core/messaging/MultiAdapter/MultiAdapter_refund_properties.spec#L7) |
| [9627](#multiadapter-9627) | each adapter is paid the quote the refund address gives instead of its own, so an adapter can be underpaid or overpaid for its delivery.<br>Caught by: [`hlMaSendPaysEachAdapterTheQuoteItGaveItself`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L335) |
| [9628](#multiadapter-9628) | a delivery that releases its payload records its confirmation again after the gateway call, so the spent tally is topped up behind the forward.<br>Caught by: [`hlMaHandleSpendsTheTallyBeforeForwarding`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L141) |
| [9630](#multiadapter-9630) | the vote key leaves out the routed pool, so every pool's deliveries of one stamped message count on one shared tally.<br>Caught by: [`hlMaVoteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L6) · [`hlMaHandleMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L36) · [`hlMaExecuteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L66) · [`hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L169) |
| [9631](#multiadapter-9631) | the vote key hashes the message without its session stamp, so confirmations cast under different sessions count on one tally.<br>Caught by: [`hlMaVoteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L6) · [`hlMaExecuteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L66) · [`hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L169) |
| [9632](#multiadapter-9632) | an inbound message is checked against the global pool's roster whatever pool the router names, so a pool's own adapter set never guards it.<br>Caught by: [`hlMaHandleIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L96) · [`hlMaVoteIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L108) · [`hlMaExecuteIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L120) |
| [9633](#multiadapter-9633) | a manager of the global pool may submit in any pool's adapter's name, so the routed pool's own managers no longer decide who submits.<br>Caught by: [`hlMaHandleIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L96) · [`hlMaVoteIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L108) · [`hlMaExecuteIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L120) |
| [9634](#multiadapter-9634) | the router is told a configured pool is unconfigured and the reverse, so a configured pool's message falls back to the global adapter set.<br>Caught by: [`hlMaVoteAsksTheRouterAboutTheMessagesOwnPoolsConfiguration`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L132) |
| [9635](#multiadapter-9635) | the router reads the stamped payload instead of the message, so the session bytes are parsed as the message type and pool.<br>Caught by: [`hlMaVoteHandsTheRouterTheUnstampedMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L146) |
| [9636](#multiadapter-9636) | a delivery needs strictly more confirmations than the threshold, so a one of one roster can never release anything.<br>Caught by: [`rcMaSamePayloadIsReleasedTwiceIsReachable`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L160) |
| [9637](#multiadapter-9637) | A refused refund is ignored instead of reverting the send, so the surplus silently stays in the contract.<br>Caught by: [`rcMaRejectingRefundAddressUndoesTheWholeFanOutIsReachable`](../../specs/core/messaging/MultiAdapter/MultiAdapter_refund_properties.spec#L33) |
| [9638](#multiadapter-9638) | only the adapter itself may deliver, so a pool manager can no longer submit a confirmation in a rostered adapter's name.<br>Caught by: [`rcMaAManagerReleasesAPayloadNoAdapterDeliveredIsReachable`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L185) |

## MultiAdapter #1802

setAdapters no longer persists the advanced session counter, so the new roster is installed under a session id the counter never reached.

- **Mutant:** [`1802.sol`](1802.sol)
- **Caught by:** [`sessionsAboveCounterEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L50) · [`activeSetSessionCurrentOrCleared`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1802`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule sessionsAboveCounterEmpty activeSetSessionCurrentOrCleared`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -99,7 +99,7 @@
         // Advance the session id to reset pending votes
         uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
         require(sessionId == targetSessionId, UnexpectedSessionId());
-        activeSessionId[centrifugeId][poolId] = sessionId;
+        // MUTATION: the advanced session counter is never persisted
 
         _installSession(centrifugeId, poolId, sessionId, addresses, threshold_);
         _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, addresses);
```

## MultiAdapter #1803

setAdapters steps the session counter backwards instead of forwards, leaving existing rosters and stashes above the counter.

- **Mutant:** [`1803.sol`](1803.sol)
- **Caught by:** [`blockedAboveCounterEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L58) · [`sessionsAboveCounterEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L50)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1803`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule blockedAboveCounterEmpty sessionsAboveCounterEmpty`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -97,7 +97,7 @@
         require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
 
         // Advance the session id to reset pending votes
-        uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
+        uint16 sessionId = activeSessionId[centrifugeId][poolId] - 1; // MUTATION: counter steps backwards
         require(sessionId == targetSessionId, UnexpectedSessionId());
         activeSessionId[centrifugeId][poolId] = sessionId;
 
```

## MultiAdapter #1804

setAdapters no longer rejects a threshold above the adapter count, so a session can be installed with an unreachable vote threshold.

- **Mutant:** [`1804.sol`](1804.sol)
- **Caught by:** [`registeredAdapterWellFormed`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L71)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1804`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule registeredAdapterWellFormed`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -94,7 +94,7 @@
         uint8 quorum_ = addresses.length.toUint8();
         require(quorum_ <= MAX_ADAPTER_COUNT, ExceedsMax());
         require(threshold_ > 0 || quorum_ == 0, ZeroThreshold());
-        require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
+        // MUTATION: removed the threshold-within-quorum check
 
         // Advance the session id to reset pending votes
         uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
```

## MultiAdapter #1805

_installSession swaps the quorum and threshold fields, so an adapter row can record a quorum other than the roster size.

- **Mutant:** [`1805.sol`](1805.sol)
- **Caught by:** [`adapterQuorumEqualsListLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L84) · [`registeredAdapterWellFormed`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L71)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1805`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule adapterQuorumEqualsListLength registeredAdapterWellFormed`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -157,7 +157,7 @@
         uint8 quorum_ = list.length.toUint8();
         for (uint8 i; i < quorum_; i++) {
             require(_adapterDetails[centrifugeId][poolId][sessionId][list[i]].id == 0, NoDuplicatesAllowed());
-            _adapterDetails[centrifugeId][poolId][sessionId][list[i]] = Adapter(i + 1, quorum_, threshold_);
+            _adapterDetails[centrifugeId][poolId][sessionId][list[i]] = Adapter(i + 1, threshold_, quorum_); // MUTATION: quorum and threshold transposed
         }
         adapters[centrifugeId][poolId][sessionId] = list;
     }
```

## MultiAdapter #1806

setAdapters reuses the current session id, so a new roster overwrites the live session, even session zero.

- **Mutant:** [`1806.sol`](1806.sol)
- **Caught by:** [`sessionZeroNeverConfigured`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L66) · [`clearedActiveSetEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L28) · [`sessionThresholdUniform`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L95) · [`adapterIdPointsAtItsOwnSlot`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L119)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1806`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule sessionZeroNeverConfigured clearedActiveSetEmpty sessionThresholdUniform adapterIdPointsAtItsOwnSlot`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -97,7 +97,7 @@
         require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
 
         // Advance the session id to reset pending votes
-        uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
+        uint16 sessionId = activeSessionId[centrifugeId][poolId]; // MUTATION: session id reused instead of advanced
         require(sessionId == targetSessionId, UnexpectedSessionId());
         activeSessionId[centrifugeId][poolId] = sessionId;
 
```

## MultiAdapter #1807

_installSession assigns zero-based adapter ids, so the first adapter's row keeps the unregistered id while carrying live quorum data.

- **Mutant:** [`1807.sol`](1807.sol)
- **Caught by:** [`listedAdapterHoldsItsIndex`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L107) · [`adapterIdPointsAtItsOwnSlot`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L119)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1807`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule listedAdapterHoldsItsIndex adapterIdPointsAtItsOwnSlot`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -157,7 +157,7 @@
         uint8 quorum_ = list.length.toUint8();
         for (uint8 i; i < quorum_; i++) {
             require(_adapterDetails[centrifugeId][poolId][sessionId][list[i]].id == 0, NoDuplicatesAllowed());
-            _adapterDetails[centrifugeId][poolId][sessionId][list[i]] = Adapter(i + 1, quorum_, threshold_);
+            _adapterDetails[centrifugeId][poolId][sessionId][list[i]] = Adapter(i, quorum_, threshold_); // MUTATION: zero-based adapter ids
         }
         adapters[centrifugeId][poolId][sessionId] = list;
     }
```

## MultiAdapter #1808

_installSession starts registering at the second adapter, so the roster's first entry never receives its details row.

- **Mutant:** [`1808.sol`](1808.sol)
- **Caught by:** [`listedAdapterHoldsItsIndex`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L107)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1808`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule listedAdapterHoldsItsIndex`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -155,7 +155,7 @@
         uint8 threshold_
     ) internal {
         uint8 quorum_ = list.length.toUint8();
-        for (uint8 i; i < quorum_; i++) {
+        for (uint8 i = 1; i < quorum_; i++) { // MUTATION: registration starts at the second adapter
             require(_adapterDetails[centrifugeId][poolId][sessionId][list[i]].id == 0, NoDuplicatesAllowed());
             _adapterDetails[centrifugeId][poolId][sessionId][list[i]] = Adapter(i + 1, quorum_, threshold_);
         }
```

## MultiAdapter #1809

blockSession inverts the active-session comparison, so blocking the live session stashes it as inactive and leaves the outbound route in place.

- **Mutant:** [`1809.sol`](1809.sol)
- **Caught by:** [`blockedAtCounterWasActive`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L153) · [`blockedCounterClearsActiveSet`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L162) · [`activeSetMirrorsSessionList`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1809`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule blockedAtCounterWasActive blockedCounterClearsActiveSet activeSetMirrorsSessionList`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -116,7 +116,7 @@
         // Move the session configuration out of the live storage so handle()/send() reject it through their
         // existing checks (InvalidAdapter / EmptyAdapterSet), avoiding an extra SLOAD on every message.
         Adapter memory first = _adapterDetails[centrifugeId][poolId][sessionId][list[0]];
-        bool wasActive = sessionId == activeSessionId[centrifugeId][poolId];
+        bool wasActive = sessionId != activeSessionId[centrifugeId][poolId]; // MUTATION: active-session comparison inverted
         _blockedSessions[centrifugeId][poolId][sessionId] = BlockedSession(first.threshold, wasActive, list);
 
         for (uint256 i; i < numAdapters; i++) {
```

## MultiAdapter #1810

blockSession no longer clears the outbound route when the blocked session is the active one, so sends keep fanning out to the stashed roster.

- **Mutant:** [`1810.sol`](1810.sol)
- **Caught by:** [`activeSetMirrorsSessionList`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L36) · [`blockedCounterClearsActiveSet`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L162)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1810`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule activeSetMirrorsSessionList blockedCounterClearsActiveSet`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -123,7 +123,7 @@
             delete _adapterDetails[centrifugeId][poolId][sessionId][list[i]];
         }
         delete adapters[centrifugeId][poolId][sessionId];
-        if (wasActive) delete _activeAdapters[centrifugeId][poolId];
+        // MUTATION: the active route is no longer cleared when its session is blocked
 
         emit BlockSession(centrifugeId, poolId, sessionId);
     }
```

## MultiAdapter #1811

blockSession clears only the route's session stamp and keeps its adapter list, leaving a roster behind on a cleared route.

- **Mutant:** [`1811.sol`](1811.sol)
- **Caught by:** [`clearedActiveSetEmpty`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L28) · [`blockedCounterClearsActiveSet`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L162)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1811`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule clearedActiveSetEmpty blockedCounterClearsActiveSet`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -123,7 +123,7 @@
             delete _adapterDetails[centrifugeId][poolId][sessionId][list[i]];
         }
         delete adapters[centrifugeId][poolId][sessionId];
-        if (wasActive) delete _activeAdapters[centrifugeId][poolId];
+        if (wasActive) delete _activeAdapters[centrifugeId][poolId].sessionId; // MUTATION: only the session stamp is cleared
 
         emit BlockSession(centrifugeId, poolId, sessionId);
     }
```

## MultiAdapter #1812

blockSession stashes a session without removing its live adapter list, so the session is simultaneously live and blocked.

- **Mutant:** [`1812.sol`](1812.sol)
- **Caught by:** [`blockedExcludesLive`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L131) · [`listedAdapterHoldsItsIndex`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L107)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1812`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule blockedExcludesLive listedAdapterHoldsItsIndex`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -122,7 +122,7 @@
         for (uint256 i; i < numAdapters; i++) {
             delete _adapterDetails[centrifugeId][poolId][sessionId][list[i]];
         }
-        delete adapters[centrifugeId][poolId][sessionId];
+        // MUTATION: the live adapter list is no longer removed when the session is stashed
         if (wasActive) delete _activeAdapters[centrifugeId][poolId];
 
         emit BlockSession(centrifugeId, poolId, sessionId);
```

## MultiAdapter #1813

blockSession reads the threshold from the active session, so a blocked session can record a zero or oversized threshold.

- **Mutant:** [`1813.sol`](1813.sol)
- **Caught by:** [`blockedThresholdWithinList`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L140)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1813`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule blockedThresholdWithinList`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -115,7 +115,7 @@
 
         // Move the session configuration out of the live storage so handle()/send() reject it through their
         // existing checks (InvalidAdapter / EmptyAdapterSet), avoiding an extra SLOAD on every message.
-        Adapter memory first = _adapterDetails[centrifugeId][poolId][sessionId][list[0]];
+        Adapter memory first = _adapterDetails[centrifugeId][poolId][activeSessionId[centrifugeId][poolId]][list[0]]; // MUTATION: threshold snapshot read from the active session
         bool wasActive = sessionId == activeSessionId[centrifugeId][poolId];
         _blockedSessions[centrifugeId][poolId][sessionId] = BlockedSession(first.threshold, wasActive, list);
 
```

## MultiAdapter #1814

unblockSession restores the outbound route without checking the session is still current, so a stale session can overwrite the live route.

- **Mutant:** [`1814.sol`](1814.sol)
- **Caught by:** [`activeSetSessionCurrentOrCleared`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1814`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule activeSetSessionCurrentOrCleared`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -137,7 +137,7 @@
         _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
 
         // Only restore the active set if this is still the active session; a later setAdapters may have replaced it.
-        if (blocked.wasActive && sessionId == activeSessionId[centrifugeId][poolId]) {
+        if (blocked.wasActive) { // MUTATION: staleness re-check dropped
             _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, blocked.list);
         }
 
```

## MultiAdapter #1816

blocking a session stashes the live roster with its first entry duplicated, so the stashed list repeats an adapter.

- **Mutant:** [`1816.sol`](1816.sol)
- **Caught by:** [`blockedListDistinct`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L174)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1816`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule blockedListDistinct`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -117,6 +117,7 @@
         // existing checks (InvalidAdapter / EmptyAdapterSet), avoiding an extra SLOAD on every message.
         Adapter memory first = _adapterDetails[centrifugeId][poolId][sessionId][list[0]];
         bool wasActive = sessionId == activeSessionId[centrifugeId][poolId];
+        list[numAdapters - 1] = list[0]; // MUTATION: the stashed roster repeats its first adapter
         _blockedSessions[centrifugeId][poolId][sessionId] = BlockedSession(first.threshold, wasActive, list);
 
         for (uint256 i; i < numAdapters; i++) {
```

## MultiAdapter #1817

The last adapter's details survive the block, so a row keeps a live quorum for a session whose roster is gone.

- **Mutant:** [`1817.sol`](1817.sol)
- **Caught by:** [`adapterQuorumEqualsListLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L84)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1817`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule adapterQuorumEqualsListLength`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -119,7 +119,8 @@
         bool wasActive = sessionId == activeSessionId[centrifugeId][poolId];
         _blockedSessions[centrifugeId][poolId][sessionId] = BlockedSession(first.threshold, wasActive, list);
 
-        for (uint256 i; i < numAdapters; i++) {
+        // MUTATION: the last adapter's details survive the block
+        for (uint256 i; i + 1 < numAdapters; i++) {
             delete _adapterDetails[centrifugeId][poolId][sessionId][list[i]];
         }
         delete adapters[centrifugeId][poolId][sessionId];
```

## MultiAdapter #1818

unblocking reinstalls the stashed roster at a threshold of one instead of the one it was stashed with.

- **Mutant:** [`1818.sol`](1818.sol)
- **Caught by:** [`stMaUnblockRestoresExactlyWhatWasStashed`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L138)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1818`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule stMaUnblockRestoresExactlyWhatWasStashed`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -134,7 +134,7 @@
         require(blocked.list.length != 0, SessionNotBlocked());
 
         // Move the configuration back into the live storage, rebuilding the per-adapter details.
-        _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
+        _installSession(centrifugeId, poolId, sessionId, blocked.list, 1); // MUTATION: restored at a different threshold
 
         // Only restore the active set if this is still the active session; a later setAdapters may have replaced it.
         if (blocked.wasActive && sessionId == activeSessionId[centrifugeId][poolId]) {
```

## MultiAdapter #1819

unblocking restores the active set without checking the session is still the current one, so a superseded roster takes the live route back.

- **Mutant:** [`1819.sol`](1819.sol)
- **Caught by:** [`stMaUnblockReopensTheRouteOnlyForTheSessionInService`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L166)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1819`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule stMaUnblockReopensTheRouteOnlyForTheSessionInService`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -137,7 +137,7 @@
         _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
 
         // Only restore the active set if this is still the active session; a later setAdapters may have replaced it.
-        if (blocked.wasActive && sessionId == activeSessionId[centrifugeId][poolId]) {
+        if (blocked.wasActive) { // MUTATION: a superseded session takes the route back
             _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, blocked.list);
         }
 
```

## MultiAdapter #1820

setAdapters stamps the new live roster with the previous session's number, so outbound sends carry a stale session.

- **Mutant:** [`1820.sol`](1820.sol)
- **Caught by:** [`stMaSessionAdvanceRestampsTheRoute`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L75)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1820`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule stMaSessionAdvanceRestampsTheRoute`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -102,7 +102,7 @@
         activeSessionId[centrifugeId][poolId] = sessionId;
 
         _installSession(centrifugeId, poolId, sessionId, addresses, threshold_);
-        _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, addresses);
+        _activeAdapters[centrifugeId][poolId] = Adapters(sessionId - 1, addresses); // MUTATION: stamped with the previous session
 
         emit SetAdapters(centrifugeId, poolId, sessionId, addresses, threshold_);
     }
```

## MultiAdapter #1822

Blocking records the session as idle whatever it was, so a stash forgets that the session it holds was the one in service.

- **Mutant:** [`1822.sol`](1822.sol)
- **Caught by:** [`stMaBlockStashesTheLiveRosterWhole`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L90)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1822`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule stMaBlockStashesTheLiveRosterWhole`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -117,7 +117,8 @@
         // existing checks (InvalidAdapter / EmptyAdapterSet), avoiding an extra SLOAD on every message.
         Adapter memory first = _adapterDetails[centrifugeId][poolId][sessionId][list[0]];
         bool wasActive = sessionId == activeSessionId[centrifugeId][poolId];
-        _blockedSessions[centrifugeId][poolId][sessionId] = BlockedSession(first.threshold, wasActive, list);
+        // MUTATION: the stash records the session as idle whatever it was
+        _blockedSessions[centrifugeId][poolId][sessionId] = BlockedSession(first.threshold, false, list);
 
         for (uint256 i; i < numAdapters; i++) {
             delete _adapterDetails[centrifugeId][poolId][sessionId][list[i]];
```

## MultiAdapter #1826

Blocking any session clears the set in service, so retiring a superseded session blacks out the live route.

- **Mutant:** [`1826.sol`](1826.sol)
- **Caught by:** [`stMaBlockingASupersededSessionKeepsTheRoute`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L119)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 1826`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule stMaBlockingASupersededSessionKeepsTheRoute`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -123,7 +123,7 @@
             delete _adapterDetails[centrifugeId][poolId][sessionId][list[i]];
         }
         delete adapters[centrifugeId][poolId][sessionId];
-        if (wasActive) delete _activeAdapters[centrifugeId][poolId];
+        delete _activeAdapters[centrifugeId][poolId]; /* MUTATION: the guard is dropped, every block clears the live route */
 
         emit BlockSession(centrifugeId, poolId, sessionId);
     }
```

## MultiAdapter #4900

execute decrements every vote lane instead of only the quorum's, so lanes outside the quorum lose a vote.

- **Mutant:** [`4900.sol`](4900.sol)
- **Caught by:** [`hlMaExecuteSparesTheThirdLaneOutsideTheQuorum`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 4900`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaExecuteSparesTheThirdLaneOutsideTheQuorum`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -237,7 +237,7 @@
         bytes32 voteKey,
         bytes calldata unwrappedPayload
     ) internal {
-        _votes[centrifugeId][voteKey].decreaseFirstNValues(details.quorum);
+        _votes[centrifugeId][voteKey].decreaseFirstNValues(MAX_ADAPTER_COUNT); // MUTATION: every lane is consumed, not just the quorum's
 
         bytes32 payloadId = keccak256(abi.encodePacked(centrifugeId, localCentrifugeId, payloadHash));
         emit Execute(centrifugeId, payloadId, payload, adapter);
```

## MultiAdapter #4901

execute forwards a payload on a single confirmation instead of the session's threshold, so one adapter alone drives the gateway.

- **Mutant:** [`4901.sol`](4901.sol)
- **Caught by:** [`hlMaExecuteSpendsATallyOnlyAtTheThreshold`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 4901`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaExecuteSpendsATallyOnlyAtTheThreshold`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -204,7 +204,7 @@
             _resolve(centrifugeId, payload, adapter);
 
         require(
-            _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= details.threshold, NotEnoughVotes()
+            _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= 1, NotEnoughVotes() // MUTATION: one confirmation passes for the whole threshold
         );
         _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload);
     }
```

## MultiAdapter #5400

The ward gate no longer checks the caller, so any account can rewire routes, appoint managers and send messages.

- **Mutant:** [`5400.sol`](5400.sol)
- **Caught by:** [`acMaOnlyWardMovesTheWardSet`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L4) · [`acMaOnlyWardModifiesManagerRights`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L20) · [`acMaOnlyWardRepointsTheGateway`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L37) · [`acMaOnlyWardRepointsTheParser`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L53) · [`acMaOnlyWardFansOutASend`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L69) · [`acMaOnlyWardRepointsTheMessageGas`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L260)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5400`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/access_control.conf --rule acMaOnlyWardMovesTheWardSet acMaOnlyWardModifiesManagerRights acMaOnlyWardRepointsTheGateway acMaOnlyWardRepointsTheParser acMaOnlyWardFansOutASend acMaOnlyWardRepointsTheMessageGas`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -17,7 +17,7 @@
 
     /// @dev Check if the msg.sender has permissions
     modifier auth() {
-        require(wards[msg.sender] == 1, NotAuthorized());
+        // MUTATION: the ward gate no longer looks at the caller
         _;
     }
 
```

## MultiAdapter #5401

The transport gate admits non-wards and refuses wards, so outsiders can set, block and unblock adapter sessions.

- **Mutant:** [`5401.sol`](5401.sol)
- **Caught by:** [`acMaOnlyWardOrManagerAdvancesTheSession`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L86) · [`acMaOnlyWardOrManagerMovesTheLiveRoute`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L104) · [`acMaOnlyWardOrManagerMovesASessionRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L129) · [`acMaOnlyWardOrManagerMovesAnAdapterRegistration`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L152) · [`acMaOnlyWardOrManagerMovesTheBlockedStash`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L179)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5401`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/access_control.conf --rule acMaOnlyWardOrManagerAdvancesTheSession acMaOnlyWardOrManagerMovesTheLiveRoute acMaOnlyWardOrManagerMovesASessionRoster acMaOnlyWardOrManagerMovesAnAdapterRegistration acMaOnlyWardOrManagerMovesTheBlockedStash`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -55,7 +55,7 @@
     }
 
     modifier onlyAuthOrManager(PoolId poolId) {
-        require(wards[msg.sender] == 1 || manager[poolId][msg.sender], NotAuthorized());
+        require(manager[poolId][msg.sender] || wards[msg.sender] != 1, NotAuthorized()); // MUTATION: the ward half of the transport gate is inverted
         _;
     }
 
```

## MultiAdapter #5402

Inbound deliveries no longer check the caller is the named adapter or a pool manager, so anyone can vote and release messages.

- **Mutant:** [`5402.sol`](5402.sol)
- **Caught by:** [`acMaOnlyAdapterOrManagerReachesTheGateway`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L241)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5402`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/access_control.conf --rule acMaOnlyAdapterOrManagerReachesTheGateway`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -257,7 +257,7 @@
         unwrappedPayload = payload[2:];
         PoolId poolId = _routePoolId(centrifugeId, unwrappedPayload);
 
-        require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
+        // MUTATION: anyone may submit a delivery, a vote or an execution on any adapter's behalf
 
         details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
         require(details.id != 0, InvalidAdapter());
```

## MultiAdapter #5403

The ward check no longer looks at the caller, so any account can rewire routes, seat managers and send messages.

- **Mutant:** [`5403.sol`](5403.sol)
- **Caught by:** [`rvMaFileRefusesANonWardOrAnUnknownName`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L6) · [`rvMaUpdateManagerRefusesANonWard`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L21) · [`rvMaSendRefusesANonWard`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L291)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5403`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaFileRefusesANonWardOrAnUnknownName rvMaUpdateManagerRefusesANonWard rvMaSendRefusesANonWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -17,7 +17,7 @@
 
     /// @dev Check if the msg.sender has permissions
     modifier auth() {
-        require(wards[msg.sender] == 1, NotAuthorized());
+        // MUTATION: the ward gate no longer looks at the caller
         _;
     }
 
```

## MultiAdapter #5404

The transport gate admits every non-ward and refuses wards, so outsiders can rotate adapter sets and block or unblock sessions.

- **Mutant:** [`5404.sol`](5404.sol)
- **Caught by:** [`rvMaSetAdaptersRefusesWithoutTransportAuthority`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L34) · [`rvMaBlockSessionRefusesAnOutsiderOrASessionWithNoRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L132) · [`rvMaUnblockSessionRefusesWithoutTransportAuthority`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L149)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5404`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSetAdaptersRefusesWithoutTransportAuthority rvMaBlockSessionRefusesAnOutsiderOrASessionWithNoRoster rvMaUnblockSessionRefusesWithoutTransportAuthority`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -55,7 +55,7 @@
     }
 
     modifier onlyAuthOrManager(PoolId poolId) {
-        require(wards[msg.sender] == 1 || manager[poolId][msg.sender], NotAuthorized());
+        require(manager[poolId][msg.sender] || wards[msg.sender] != 1, NotAuthorized()); // MUTATION: the ward half of the transport gate is inverted
         _;
     }
 
```

## MultiAdapter #5405

Inbound deliveries no longer check the caller is the named adapter or a pool manager, so anyone can vote and release messages.

- **Mutant:** [`5405.sol`](5405.sol)
- **Caught by:** [`rvMaHandleRefusesAStrangerSubmission`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L194) · [`rvMaVoteRefusesAStrangerSubmission`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L209) · [`rvMaExecuteRefusesAStrangerSubmission`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L224)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5405`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaHandleRefusesAStrangerSubmission rvMaVoteRefusesAStrangerSubmission rvMaExecuteRefusesAStrangerSubmission`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -257,7 +257,7 @@
         unwrappedPayload = payload[2:];
         PoolId poolId = _routePoolId(centrifugeId, unwrappedPayload);
 
-        require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
+        // MUTATION: anyone may submit a delivery, a vote or an execution on any adapter's behalf
 
         details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
         require(details.id != 0, InvalidAdapter());
```

## MultiAdapter #5406

An unregistered adapter is put on the first vote lane instead of refused, so any account can vote and release messages.

- **Mutant:** [`5406.sol`](5406.sol)
- **Caught by:** [`rvMaExecuteRefusesAnUnregisteredAdapter`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L239) · [`rvMaHandleRefusesAnUnregisteredSender`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L252) · [`rvMaVoteRefusesAnUnregisteredSender`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L265) · [`rvMaExecuteRefusesAnUnregisteredSender`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L278)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5406`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaExecuteRefusesAnUnregisteredAdapter rvMaHandleRefusesAnUnregisteredSender rvMaVoteRefusesAnUnregisteredSender rvMaExecuteRefusesAnUnregisteredSender`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -260,7 +260,7 @@
         require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
 
         details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
-        require(details.id != 0, InvalidAdapter());
+        if (details.id == 0) details.id = 1; // MUTATION: an unknown adapter is adopted onto the first lane
 
         payloadHash = keccak256(payload);
         voteKey = keccak256(abi.encodePacked(poolId.raw(), payload));
```

## MultiAdapter #5407

An adapter set may be installed with a threshold above its size, so that route can never reach consensus.

- **Mutant:** [`5407.sol`](5407.sol)
- **Caught by:** [`rvMaSetAdaptersRefusesAnUnreachableThreshold`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L50)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5407`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSetAdaptersRefusesAnUnreachableThreshold`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -94,7 +94,7 @@
         uint8 quorum_ = addresses.length.toUint8();
         require(quorum_ <= MAX_ADAPTER_COUNT, ExceedsMax());
         require(threshold_ > 0 || quorum_ == 0, ZeroThreshold());
-        require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
+        // MUTATION: an unreachable consensus bar is no longer refused
 
         // Advance the session id to reset pending votes
         uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
```

## MultiAdapter #5408

A non-empty adapter set may be installed with a zero threshold, so messages execute without any bridge confirming them.

- **Mutant:** [`5408.sol`](5408.sol)
- **Caught by:** [`rvMaSetAdaptersRefusesAZeroThresholdOverALiveRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L65)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5408`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSetAdaptersRefusesAZeroThresholdOverALiveRoster`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -93,7 +93,7 @@
     ) external onlyAuthOrManager(poolId) {
         uint8 quorum_ = addresses.length.toUint8();
         require(quorum_ <= MAX_ADAPTER_COUNT, ExceedsMax());
-        require(threshold_ > 0 || quorum_ == 0, ZeroThreshold());
+        // MUTATION: a live roster without a consensus bar is no longer refused
         require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
 
         // Advance the session id to reset pending votes
```

## MultiAdapter #5409

An adapter set may list the same adapter twice, so the quorum counts a vote lane no adapter can fill.

- **Mutant:** [`5409.sol`](5409.sol)
- **Caught by:** [`rvMaSetAdaptersRefusesARepeatedAdapter`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L81)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5409`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSetAdaptersRefusesARepeatedAdapter`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -156,7 +156,7 @@
     ) internal {
         uint8 quorum_ = list.length.toUint8();
         for (uint8 i; i < quorum_; i++) {
-            require(_adapterDetails[centrifugeId][poolId][sessionId][list[i]].id == 0, NoDuplicatesAllowed());
+            // MUTATION: a repeated adapter is no longer refused
             _adapterDetails[centrifugeId][poolId][sessionId][list[i]] = Adapter(i + 1, quorum_, threshold_);
         }
         adapters[centrifugeId][poolId][sessionId] = list;
```

## MultiAdapter #5410

An install takes whatever session id the caller names instead of the next one, so old or skipped sessions can be installed.

- **Mutant:** [`5410.sol`](5410.sol)
- **Caught by:** [`rvMaSetAdaptersRefusesAnUnexpectedSessionId`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L97)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5410`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSetAdaptersRefusesAnUnexpectedSessionId`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -97,8 +97,7 @@
         require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
 
         // Advance the session id to reset pending votes
-        uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
-        require(sessionId == targetSessionId, UnexpectedSessionId());
+        uint16 sessionId = targetSessionId; // MUTATION: the install takes the session id the caller names
         activeSessionId[centrifugeId][poolId] = sessionId;
 
         _installSession(centrifugeId, poolId, sessionId, addresses, threshold_);
```

## MultiAdapter #5411

A rotation onto a single adapter under full consensus is refused, so the documented one bridge recovery install is unavailable to governance.

- **Mutant:** [`5411.sol`](5411.sol)
- **Caught by:** [`rvMaSetAdaptersOnAFreshRosterAlwaysGoesThroughForAWard`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L112)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5411`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSetAdaptersOnAFreshRosterAlwaysGoesThroughForAWard`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -93,7 +93,7 @@
     ) external onlyAuthOrManager(poolId) {
         uint8 quorum_ = addresses.length.toUint8();
         require(quorum_ <= MAX_ADAPTER_COUNT, ExceedsMax());
-        require(threshold_ > 0 || quorum_ == 0, ZeroThreshold());
+        require(threshold_ > 1 || quorum_ == 0, ZeroThreshold()); // MUTATION: a single confirmation set is refused
         require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
 
         // Advance the session id to reset pending votes
```

## MultiAdapter #5412

A session that was never blocked can be unblocked, so the call wipes that session's adapter list.

- **Mutant:** [`5412.sol`](5412.sol)
- **Caught by:** [`rvMaUnblockSessionRefusesWithoutAStashedSession`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L165)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5412`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaUnblockSessionRefusesWithoutAStashedSession`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -131,7 +131,7 @@
     /// @inheritdoc IMultiAdapter
     function unblockSession(uint16 centrifugeId, PoolId poolId, uint16 sessionId) external onlyAuthOrManager(poolId) {
         BlockedSession memory blocked = _blockedSessions[centrifugeId][poolId][sessionId];
-        require(blocked.list.length != 0, SessionNotBlocked());
+        // MUTATION: a session with no stash is no longer refused
 
         // Move the configuration back into the live storage, rebuilding the per-adapter details.
         _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
```

## MultiAdapter #5413

unblockSession refuses a blocked session with one adapter, so such a session can never be restored.

- **Mutant:** [`5413.sol`](5413.sol)
- **Caught by:** [`rvMaUnblockSessionOfASingleStashAlwaysGoesThroughForAWard`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L179)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5413`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaUnblockSessionOfASingleStashAlwaysGoesThroughForAWard`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -131,7 +131,7 @@
     /// @inheritdoc IMultiAdapter
     function unblockSession(uint16 centrifugeId, PoolId poolId, uint16 sessionId) external onlyAuthOrManager(poolId) {
         BlockedSession memory blocked = _blockedSessions[centrifugeId][poolId][sessionId];
-        require(blocked.list.length != 0, SessionNotBlocked());
+        require(blocked.list.length > 1, SessionNotBlocked()); // MUTATION: a stash of one is treated as no stash
 
         // Move the configuration back into the live storage, rebuilding the per-adapter details.
         _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
```

## MultiAdapter #5414

send on a route with no adapters in service now succeeds instead of refusing, so the message is silently dropped.

- **Mutant:** [`5414.sol`](5414.sol)
- **Caught by:** [`rvMaSendRefusesWithoutALiveRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L304)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5414`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSendRefusesWithoutALiveRoster`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -279,7 +279,7 @@
     {
         PoolId poolId = _routePoolId(centrifugeId, payload);
         Adapters memory adapters_ = _activeAdapters[centrifugeId][poolId];
-        require(adapters_.list.length != 0, EmptyAdapterSet());
+        // MUTATION: an empty route no longer refuses outbound traffic
 
         bytes memory wrappedPayload = abi.encodePacked(adapters_.sessionId, payload);
         bytes32 payloadId = keccak256(abi.encodePacked(localCentrifugeId, centrifugeId, keccak256(wrappedPayload)));
```

## MultiAdapter #5415

A route with no adapters in service is quoted at zero instead of refused, so a disabled route looks usable and free.

- **Mutant:** [`5415.sol`](5415.sol)
- **Caught by:** [`rvMaEstimateRefusesWithoutALiveRoster`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L317)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5415`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaEstimateRefusesWithoutALiveRoster`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -314,7 +314,7 @@
     {
         PoolId poolId = _routePoolId(centrifugeId, payload);
         IAdapter[] memory adapters_ = _activeAdapters[centrifugeId][poolId].list;
-        require(adapters_.length != 0, EmptyAdapterSet());
+        // MUTATION: an empty route no longer refuses to quote
 
         // Account for the 2-byte session id prefix added in send(); non-zero bytes for max calldata cost.
         bytes memory wrappedPayload = abi.encodePacked(uint16((1 << 8) + 1), payload);
```

## MultiAdapter #5416

Reading the quorum or threshold of a route with no adapters in service now fails instead of answering zero.

- **Mutant:** [`5416.sol`](5416.sol)
- **Caught by:** [`rvMaQuorumAlwaysAnswers`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L330) · [`rvMaThresholdAlwaysAnswers`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L342)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5416`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaQuorumAlwaysAnswers rvMaThresholdAlwaysAnswers`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -367,7 +367,7 @@
 
     function _getFirstAdapterDetails(uint16 centrifugeId, PoolId poolId) internal view returns (Adapter memory) {
         Adapters memory adapters_ = _activeAdapters[centrifugeId][poolId];
-        if (adapters_.list.length == 0) return Adapter(0, 0, 0);
+        // MUTATION: the empty route answer is gone, so the getters index an empty roster
         return _adapterDetails[centrifugeId][poolId][adapters_.sessionId][adapters_.list[0]];
     }
 }
```

## MultiAdapter #5417

Once a route's session counter is spent, the next session id wraps to zero instead of failing, so callers get a bogus id.

- **Mutant:** [`5417.sol`](5417.sol)
- **Caught by:** [`rvMaNextActiveSessionIdRefusesARouteWhoseCounterIsSpent`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L354)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5417`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaNextActiveSessionIdRefusesARouteWhoseCounterIsSpent`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -355,7 +355,7 @@
 
     /// @inheritdoc IMultiAdapter
     function nextActiveSessionId(uint16 centrifugeId, PoolId poolId) external view returns (uint16) {
-        return activeSessionId[centrifugeId][poolId] + 1;
+        unchecked { return activeSessionId[centrifugeId][poolId] + 1; } // MUTATION: the spent counter wraps
     }
 
     /// @dev Send and handle apply the same rule, so both chains agree on the carrying set.
```

## MultiAdapter #5418

An install adopts the session id the caller names instead of the next one, so the session id can jump or move backwards.

- **Mutant:** [`5418.sol`](5418.sol)
- **Caught by:** [`vtMaSessionIdNeverRegresses`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L6) · [`vtMaSessionIdAdvancesByOneAtMost`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5418`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule vtMaSessionIdNeverRegresses vtMaSessionIdAdvancesByOneAtMost`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -97,8 +97,7 @@
         require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
 
         // Advance the session id to reset pending votes
-        uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
-        require(sessionId == targetSessionId, UnexpectedSessionId());
+        uint16 sessionId = targetSessionId; // MUTATION: the install takes the session id the caller names
         activeSessionId[centrifugeId][poolId] = sessionId;
 
         _installSession(centrifugeId, poolId, sessionId, addresses, threshold_);
```

## MultiAdapter #5419

A rotation deletes the superseded session's adapter list, so that session can no longer be blocked while its adapters still vote.

- **Mutant:** [`5419.sol`](5419.sol)
- **Caught by:** [`vtMaRosterMoveSparesOtherSessions`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5419`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule vtMaRosterMoveSparesOtherSessions`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -102,6 +102,7 @@
         activeSessionId[centrifugeId][poolId] = sessionId;
 
         _installSession(centrifugeId, poolId, sessionId, addresses, threshold_);
+        delete adapters[centrifugeId][poolId][sessionId - 1]; // MUTATION: the superseded roster is discarded
         _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, addresses);
 
         emit SetAdapters(centrifugeId, poolId, sessionId, addresses, threshold_);
```

## MultiAdapter #5420

A message that reaches consensus is handed to the gateway twice, so one round of adapter confirmations is executed as two deliveries downstream.

- **Mutant:** [`5420.sol`](5420.sol)
- **Caught by:** [`hlMaExecuteForwardsExactlyOneMessage`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L74) · [`hlMaHandleForwardsAtMostOnce`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L100)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5420`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaExecuteForwardsExactlyOneMessage hlMaHandleForwardsAtMostOnce`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -243,6 +243,7 @@
         emit Execute(centrifugeId, payloadId, payload, adapter);
 
         gateway.handle(centrifugeId, unwrappedPayload);
+        gateway.handle(centrifugeId, unwrappedPayload); // MUTATION: the forward is repeated
     }
 
     /// @dev Parse a wrapped payload and resolve `adapter`'s config and the payload hash. The caller must be
```

## MultiAdapter #5421

An executed message reaches the gateway under this chain's own id instead of its source chain, so its origin is misattributed.

- **Mutant:** [`5421.sol`](5421.sol)
- **Caught by:** [`hlMaExecuteForwardsOnTheArrivalChain`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L88)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5421`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaExecuteForwardsOnTheArrivalChain`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -242,7 +242,7 @@
         bytes32 payloadId = keccak256(abi.encodePacked(centrifugeId, localCentrifugeId, payloadHash));
         emit Execute(centrifugeId, payloadId, payload, adapter);
 
-        gateway.handle(centrifugeId, unwrappedPayload);
+        gateway.handle(localCentrifugeId, unwrappedPayload); // MUTATION: badged with the local chain
     }
 
     /// @dev Parse a wrapped payload and resolve `adapter`'s config and the payload hash. The caller must be
```

## MultiAdapter #5422

The vote entry now also executes once the threshold is met, so a proof only confirmation releases the message to the gateway.

- **Mutant:** [`5422.sol`](5422.sol)
- **Caught by:** [`hlMaVoteNeverReachesTheGateway`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L114)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5422`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaVoteNeverReachesTheGateway`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -189,8 +189,12 @@
 
     /// @inheritdoc IMultiAdapter
     function vote(uint16 centrifugeId, bytes calldata payload, IAdapter adapter) public {
-        (Adapter memory details, bytes32 payloadHash, bytes32 voteKey,) = _resolve(centrifugeId, payload, adapter);
-        _vote(centrifugeId, payload, adapter, details, payloadHash, voteKey);
+        (Adapter memory details, bytes32 payloadHash, bytes32 voteKey, bytes calldata unwrappedPayload) =
+            _resolve(centrifugeId, payload, adapter);
+        // MUTATION: the proof path also spends the tally and forwards
+        if (_vote(centrifugeId, payload, adapter, details, payloadHash, voteKey)) {
+            _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload);
+        }
     }
 
     /// @inheritdoc IAdapterEntrypoint
```

## MultiAdapter #5423

Restoring a blocked session also makes it the active session, so the pool's session id can roll back to an older one.

- **Mutant:** [`5423.sol`](5423.sol)
- **Caught by:** [`vtMaSessionIdMovesOnlyByRotation`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L58)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5423`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule vtMaSessionIdMovesOnlyByRotation`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -132,6 +132,7 @@
     function unblockSession(uint16 centrifugeId, PoolId poolId, uint16 sessionId) external onlyAuthOrManager(poolId) {
         BlockedSession memory blocked = _blockedSessions[centrifugeId][poolId][sessionId];
         require(blocked.list.length != 0, SessionNotBlocked());
+        activeSessionId[centrifugeId][poolId] = sessionId; // MUTATION: a restore takes the route back
 
         // Move the configuration back into the live storage, rebuilding the per-adapter details.
         _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
```

## MultiAdapter #5424

A rotation registers the new adapters under the superseded session, so its pending messages are weighed against the wrong adapters.

- **Mutant:** [`5424.sol`](5424.sol)
- **Caught by:** [`hlMaRotationKeepsEarlierSessionAdapterIds`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L128) · [`hlMaRotationKeepsEarlierSessionQuorums`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L144) · [`hlMaRotationKeepsEarlierSessionThresholds`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L161)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5424`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaRotationKeepsEarlierSessionAdapterIds hlMaRotationKeepsEarlierSessionQuorums hlMaRotationKeepsEarlierSessionThresholds`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -101,7 +101,7 @@
         require(sessionId == targetSessionId, UnexpectedSessionId());
         activeSessionId[centrifugeId][poolId] = sessionId;
 
-        _installSession(centrifugeId, poolId, sessionId, addresses, threshold_);
+        _installSession(centrifugeId, poolId, sessionId - 1, addresses, threshold_); // MUTATION: written into the superseded session
         _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, addresses);
 
         emit SetAdapters(centrifugeId, poolId, sessionId, addresses, threshold_);
```

## MultiAdapter #5425

Restoring a blocked session reinstalls it with a threshold of one instead of its saved threshold, so fewer confirmations release a message.

- **Mutant:** [`5425.sol`](5425.sol)
- **Caught by:** [`hlMaBlockThenUnblockKeepsTheThreshold`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L178)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5425`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaBlockThenUnblockKeepsTheThreshold`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -134,7 +134,7 @@
         require(blocked.list.length != 0, SessionNotBlocked());
 
         // Move the configuration back into the live storage, rebuilding the per-adapter details.
-        _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
+        _installSession(centrifugeId, poolId, sessionId, blocked.list, 1); // MUTATION: restored at a different threshold
 
         // Only restore the active set if this is still the active session; a later setAdapters may have replaced it.
         if (blocked.wasActive && sessionId == activeSessionId[centrifugeId][poolId]) {
```

## MultiAdapter #5426

Each roster adapter is dispatched to twice per send, so every bridge is paid for and delivers the message twice.

- **Mutant:** [`5426.sol`](5426.sol)
- **Caught by:** [`hlMaSendFansOutOncePerRosterMember`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L196)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5426`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendFansOutOncePerRosterMember`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -287,6 +287,7 @@
         uint256 totalCost;
         for (uint256 i = 0; i < adapters_.list.length; i++) {
             totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], gasLimit, refund);
+            totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], gasLimit, refund); // MUTATION: dispatched twice
         }
         if (msg.value > totalCost) SafeTransferLib.safeTransferETH(refund, msg.value - totalCost);
 
```

## MultiAdapter #5427

Each adapter send names the local chain instead of the requested destination, so messages leave for the wrong chain.

- **Mutant:** [`5427.sol`](5427.sol)
- **Caught by:** [`hlMaSendCarriesTheRequestedChain`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L212)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5427`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendCarriesTheRequestedChain`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -302,7 +302,7 @@
         address refund
     ) internal returns (uint256 cost) {
         cost = adapter.estimate(centrifugeId, payload, gasLimit);
-        bytes32 adapterData = adapter.send{value: cost}(centrifugeId, payload, gasLimit, refund);
+        bytes32 adapterData = adapter.send{value: cost}(localCentrifugeId, payload, gasLimit, refund); // MUTATION: badged with the local chain
         emit SendPayload(centrifugeId, payloadId, payload, adapter, adapterData, gasLimit, cost, refund);
     }
 
```

## MultiAdapter #5428

Each adapter send names the messaging contract as refund address, so unspent gas never reaches the caller's refund address.

- **Mutant:** [`5428.sol`](5428.sol)
- **Caught by:** [`hlMaSendCarriesTheRefundAddressItWasGiven`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L224)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5428`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendCarriesTheRefundAddressItWasGiven`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -302,7 +302,7 @@
         address refund
     ) internal returns (uint256 cost) {
         cost = adapter.estimate(centrifugeId, payload, gasLimit);
-        bytes32 adapterData = adapter.send{value: cost}(centrifugeId, payload, gasLimit, refund);
+        bytes32 adapterData = adapter.send{value: cost}(centrifugeId, payload, gasLimit, address(this)); // MUTATION: refunded to the route
         emit SendPayload(centrifugeId, payloadId, payload, adapter, adapterData, gasLimit, cost, refund);
     }
 
```

## MultiAdapter #5429

Outbound payloads carry session id zero instead of the route's live session, so the receiving chain cannot accept them.

- **Mutant:** [`5429.sol`](5429.sol)
- **Caught by:** [`hlMaSendWrapsThePayloadWithTheLiveSessionId`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L236)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5429`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendWrapsThePayloadWithTheLiveSessionId`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -281,7 +281,7 @@
         Adapters memory adapters_ = _activeAdapters[centrifugeId][poolId];
         require(adapters_.list.length != 0, EmptyAdapterSet());
 
-        bytes memory wrappedPayload = abi.encodePacked(adapters_.sessionId, payload);
+        bytes memory wrappedPayload = abi.encodePacked(uint16(0), payload); // MUTATION: stamped with the null epoch
         bytes32 payloadId = keccak256(abi.encodePacked(localCentrifugeId, centrifugeId, keccak256(wrappedPayload)));
 
         uint256 totalCost;
```

## MultiAdapter #5430

A send deletes the route's adapter set after dispatching, so the first message disables the pool's transport.

- **Mutant:** [`5430.sol`](5430.sol)
- **Caught by:** [`hlMaSendLeavesTheLiveRouteWhereItStands`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L254)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 5430`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendLeavesTheLiveRouteWhereItStands`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -289,6 +289,7 @@
             totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], gasLimit, refund);
         }
         if (msg.value > totalCost) SafeTransferLib.safeTransferETH(refund, msg.value - totalCost);
+        delete _activeAdapters[centrifugeId][poolId]; // MUTATION: the send consumes the roster it used
 
         return bytes32(0);
     }
```

## MultiAdapter #7000

A full set of eight adapters is now refused at install, so a route can hold at most seven.

- **Mutant:** [`7000.sol`](7000.sol)
- **Caught by:** [`rcMaRosterCapInstallIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L24)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7000`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaRosterCapInstallIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -92,7 +92,7 @@
         uint16 targetSessionId
     ) external onlyAuthOrManager(poolId) {
         uint8 quorum_ = addresses.length.toUint8();
-        require(quorum_ <= MAX_ADAPTER_COUNT, ExceedsMax());
+        require(quorum_ < MAX_ADAPTER_COUNT, ExceedsMax()); // MUTATION: a roster at the protocol cap is refused
         require(threshold_ > 0 || quorum_ == 0, ZeroThreshold());
         require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
 
```

## MultiAdapter #7001

Installing adapters now requires the threshold to equal the adapter count, so a set such as two of three is refused.

- **Mutant:** [`7001.sol`](7001.sol)
- **Caught by:** [`rcMaIntermediateThresholdInstallIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L42)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7001`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaIntermediateThresholdInstallIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -94,7 +94,7 @@
         uint8 quorum_ = addresses.length.toUint8();
         require(quorum_ <= MAX_ADAPTER_COUNT, ExceedsMax());
         require(threshold_ > 0 || quorum_ == 0, ZeroThreshold());
-        require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
+        require(threshold_ == quorum_, ThresholdHigherThanQuorum()); // MUTATION: only unanimity is accepted
 
         // Advance the session id to reset pending votes
         uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
```

## MultiAdapter #7002

An empty adapter set is now refused as a zero threshold, so a route can no longer be cleared by installing no adapters.

- **Mutant:** [`7002.sol`](7002.sol)
- **Caught by:** [`rcMaManagerHaltsARouteWithTheEmptySetIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L61)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7002`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaManagerHaltsARouteWithTheEmptySetIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -93,7 +93,7 @@
     ) external onlyAuthOrManager(poolId) {
         uint8 quorum_ = addresses.length.toUint8();
         require(quorum_ <= MAX_ADAPTER_COUNT, ExceedsMax());
-        require(threshold_ > 0 || quorum_ == 0, ZeroThreshold());
+        require(threshold_ > 0, ZeroThreshold()); // MUTATION: the empty adapter set is refused with the rest
         require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
 
         // Advance the session id to reset pending votes
```

## MultiAdapter #7003

The quorum and threshold views return zero for a route with a single adapter, so such a route looks unconfigured.

- **Mutant:** [`7003.sol`](7003.sol)
- **Caught by:** [`rcMaFirstRosterInstallIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L4) · [`rcMaBlockThenUnblockRestoresTheRouteIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L100)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7003`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaFirstRosterInstallIsReachable rcMaBlockThenUnblockRestoresTheRouteIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -367,7 +367,7 @@
 
     function _getFirstAdapterDetails(uint16 centrifugeId, PoolId poolId) internal view returns (Adapter memory) {
         Adapters memory adapters_ = _activeAdapters[centrifugeId][poolId];
-        if (adapters_.list.length == 0) return Adapter(0, 0, 0);
+        if (adapters_.list.length <= 1) return Adapter(0, 0, 0); // MUTATION: a single adapter route reads as unconfigured
         return _adapterDetails[centrifugeId][poolId][adapters_.sessionId][adapters_.list[0]];
     }
 }
```

## MultiAdapter #7004

Blocking any session clears the outbound route, so retiring a superseded session also cuts the route in service.

- **Mutant:** [`7004.sol`](7004.sol)
- **Caught by:** [`rcMaBlockingASupersededSessionKeepsTheRouteIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L125)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7004`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaBlockingASupersededSessionKeepsTheRouteIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -116,7 +116,7 @@
         // Move the session configuration out of the live storage so handle()/send() reject it through their
         // existing checks (InvalidAdapter / EmptyAdapterSet), avoiding an extra SLOAD on every message.
         Adapter memory first = _adapterDetails[centrifugeId][poolId][sessionId][list[0]];
-        bool wasActive = sessionId == activeSessionId[centrifugeId][poolId];
+        bool wasActive = true; // MUTATION: every block treats its session as the one in service
         _blockedSessions[centrifugeId][poolId][sessionId] = BlockedSession(first.threshold, wasActive, list);
 
         for (uint256 i; i < numAdapters; i++) {
```

## MultiAdapter #7005

Blocking the active session clears the route's adapter list but keeps its session id, so the route names a dead session.

- **Mutant:** [`7005.sol`](7005.sol)
- **Caught by:** [`rcMaBlockingTheSessionInServiceIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L82)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7005`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaBlockingTheSessionInServiceIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -123,7 +123,7 @@
             delete _adapterDetails[centrifugeId][poolId][sessionId][list[i]];
         }
         delete adapters[centrifugeId][poolId][sessionId];
-        if (wasActive) delete _activeAdapters[centrifugeId][poolId];
+        if (wasActive) delete _activeAdapters[centrifugeId][poolId].list; // MUTATION: the route keeps its session stamp
 
         emit BlockSession(centrifugeId, poolId, sessionId);
     }
```

## MultiAdapter #7006

Unblocking a formerly active session always restores it as the route, so a replaced adapter set takes the traffic back.

- **Mutant:** [`7006.sol`](7006.sol)
- **Caught by:** [`rcMaUnblockingASupersededSessionKeepsTheRouteIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L143)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7006`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaUnblockingASupersededSessionKeepsTheRouteIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -137,7 +137,7 @@
         _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
 
         // Only restore the active set if this is still the active session; a later setAdapters may have replaced it.
-        if (blocked.wasActive && sessionId == activeSessionId[centrifugeId][poolId]) {
+        if (blocked.wasActive) { // MUTATION: a stash takes the route back even after a rotation replaced it
             _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, blocked.list);
         }
 
```

## MultiAdapter #7007

An outbound send skips the last adapter of the roster, so a route with a single bridge sends nothing.

- **Mutant:** [`7007.sol`](7007.sol)
- **Caught by:** [`hlMaSendFansOutOncePerRosterMember`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L196) · [`hlMaSendCarriesTheRequestedChain`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L212) · [`hlMaSendCarriesTheRefundAddressItWasGiven`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L224) · [`hlMaSendReachesEachRosterMemberOnce`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L289)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7007`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendFansOutOncePerRosterMember hlMaSendCarriesTheRequestedChain hlMaSendCarriesTheRefundAddressItWasGiven hlMaSendReachesEachRosterMemberOnce`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -285,7 +285,7 @@
         bytes32 payloadId = keccak256(abi.encodePacked(localCentrifugeId, centrifugeId, keccak256(wrappedPayload)));
 
         uint256 totalCost;
-        for (uint256 i = 0; i < adapters_.list.length; i++) {
+        for (uint256 i = 0; i + 1 < adapters_.list.length; i++) { // MUTATION: the fan out skips the last member
             totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], gasLimit, refund);
         }
         if (msg.value > totalCost) SafeTransferLib.safeTransferETH(refund, msg.value - totalCost);
```

## MultiAdapter #7008

A delivery that reaches the threshold only records its vote, so the message is released only by an explicit execution.

- **Mutant:** [`7008.sol`](7008.sol)
- **Caught by:** [`rcMaThresholdOneLetsOneAdapterForwardAloneIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L260)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7008`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaThresholdOneLetsOneAdapterForwardAloneIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -177,9 +177,8 @@
     function handle(uint16 centrifugeId, bytes calldata payload, IAdapter adapter) public {
         (Adapter memory details, bytes32 payloadHash, bytes32 voteKey, bytes calldata unwrappedPayload) =
             _resolve(centrifugeId, payload, adapter);
-        if (_vote(centrifugeId, payload, adapter, details, payloadHash, voteKey)) {
-            _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload);
-        }
+        // MUTATION: reaching the bar no longer releases the payload, the delivery only records the vote
+        _vote(centrifugeId, payload, adapter, details, payloadHash, voteKey);
     }
 
     /// @inheritdoc IAdapterEntrypoint
```

## MultiAdapter #7009

An explicit execution requires strictly more confirmations than the threshold, so a tally that exactly meets it cannot be executed.

- **Mutant:** [`7009.sol`](7009.sol)
- **Caught by:** [`rcMaExecuteDrivesASilentLaneNegativeIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L280)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7009`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaExecuteDrivesASilentLaneNegativeIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -204,7 +204,8 @@
             _resolve(centrifugeId, payload, adapter);
 
         require(
-            _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= details.threshold, NotEnoughVotes()
+            // MUTATION: an execution now needs strictly more confirmations than the session's bar
+            _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) > details.threshold, NotEnoughVotes()
         );
         _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload);
     }
```

## MultiAdapter #7010

Deliveries use the active session, not the one their payload names, so a replaced set's pending messages face the wrong adapters.

- **Mutant:** [`7010.sol`](7010.sol)
- **Caught by:** [`rcMaSupersededSessionStillDeliversIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L304)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7010`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaSupersededSessionStillDeliversIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -259,6 +259,8 @@
 
         require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
 
+        // MUTATION: a delivery resolves against the session in service, not the one its payload names
+        sessionId = activeSessionId[centrifugeId][poolId];
         details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
         require(details.id != 0, InvalidAdapter());
 
```

## MultiAdapter #7011

A pool manager seat can only be granted, so a revocation leaves the account holding the rights it should lose.

- **Mutant:** [`7011.sol`](7011.sol)
- **Caught by:** [`rcMaManagerSeatGrantAndRevokeIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L330)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7011`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaManagerSeatGrantAndRevokeIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -75,7 +75,7 @@
 
     /// @inheritdoc IMultiAdapter
     function updateManager(PoolId poolId, address who, bool canManage) external auth {
-        manager[poolId][who] = canManage;
+        manager[poolId][who] = true; // MUTATION: the seat can only be handed out, never taken back
         emit UpdateManager(poolId, who, canManage);
     }
 
```

## MultiAdapter #7012

Setting the message parser through file now reverts, so it can never be set after deployment.

- **Mutant:** [`7012.sol`](7012.sol)
- **Caught by:** [`rcMaFileRepointsBothWiringTargetsIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L347)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7012`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaFileRepointsBothWiringTargetsIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -66,7 +66,7 @@
     /// @inheritdoc IMultiAdapter
     function file(bytes32 what, address instance) external auth {
         if (what == "gateway") gateway = IMessageHandler(instance);
-        else if (what == "parser") parser = IMessageParser(instance);
+        // MUTATION: the message parser can no longer be repointed
         else if (what == "messageGas") messageGas = IMessageGas(instance);
         else revert FileUnrecognizedParam();
 
```

## MultiAdapter #7013

Revoking a ward sets its seat to one instead of zero, so the account keeps its admin rights.

- **Mutant:** [`7013.sol`](7013.sol)
- **Caught by:** [`rcMaWardSeatGrantAndRevokeIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L367)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7013`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaWardSeatGrantAndRevokeIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        wards[user] = 1; // MUTATION: revoking a ward seat hands it back instead of withdrawing it
         emit Deny(user);
     }
 }
```

## MultiAdapter #7014

Unblocking restores the outbound set only when the session is no longer active, so the active route stays empty.

- **Mutant:** [`7014.sol`](7014.sol)
- **Caught by:** [`rcMaSendResumesAfterABlockAndUnblockIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L162)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7014`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaSendResumesAfterABlockAndUnblockIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -137,7 +137,7 @@
         _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
 
         // Only restore the active set if this is still the active session; a later setAdapters may have replaced it.
-        if (blocked.wasActive && sessionId == activeSessionId[centrifugeId][poolId]) {
+        if (blocked.wasActive && sessionId != activeSessionId[centrifugeId][poolId]) {
             _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, blocked.list);
         }
 
```

## MultiAdapter #7015

A delivery completes the quorum only above the threshold, so in a two of two session no delivery releases the message.

- **Mutant:** [`7015.sol`](7015.sol)
- **Caught by:** [`rcMaSecondDeliveryCompletesTheQuorumIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L195)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 7015`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaSecondDeliveryCompletesTheQuorumIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -220,7 +220,7 @@
         bytes32 voteKey
     ) internal returns (bool reached) {
         _votes[centrifugeId][voteKey][details.id - 1]++;
-        reached = _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= details.threshold;
+        reached = _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) > details.threshold;
 
         bytes32 payloadId = keccak256(abi.encodePacked(centrifugeId, localCentrifugeId, payloadHash));
         emit Vote(centrifugeId, payloadId, payload, adapter);
```

## MultiAdapter #8109

A vote no longer checks the caller is the named adapter or a pool manager, so anyone can vote on an adapter's behalf.

- **Mutant:** [`8109.sol`](8109.sol)
- **Caught by:** [`acMaOnlyAdapterOrManagerMovesAVoteTally`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L205)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8109`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/access_control.conf --rule acMaOnlyAdapterOrManagerMovesAVoteTally`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -189,8 +189,11 @@
 
     /// @inheritdoc IMultiAdapter
     function vote(uint16 centrifugeId, bytes calldata payload, IAdapter adapter) public {
-        (Adapter memory details, bytes32 payloadHash, bytes32 voteKey,) = _resolve(centrifugeId, payload, adapter);
-        _vote(centrifugeId, payload, adapter, details, payloadHash, voteKey);
+        // MUTATION: the adapter lookup of _resolve inline, without its caller check
+        PoolId poolId = _routePoolId(centrifugeId, payload[2:]);
+        Adapter memory details = _adapterDetails[centrifugeId][poolId][uint16(bytes2(payload[0:2]))][adapter];
+        require(details.id != 0, InvalidAdapter());
+        _vote(centrifugeId, payload, adapter, details, keccak256(payload), keccak256(abi.encodePacked(poolId.raw(), payload)));
     }
 
     /// @inheritdoc IAdapterEntrypoint
```

## MultiAdapter #8110

Executing a message consumes one vote lane past the quorum, so the next adapter outside the quorum loses a confirmation.

- **Mutant:** [`8110.sol`](8110.sol)
- **Caught by:** [`hlMaExecuteSparesTheSecondLaneOutsideTheQuorum`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L34)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8110`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaExecuteSparesTheSecondLaneOutsideTheQuorum`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -237,7 +237,7 @@
         bytes32 voteKey,
         bytes calldata unwrappedPayload
     ) internal {
-        _votes[centrifugeId][voteKey].decreaseFirstNValues(details.quorum);
+        _votes[centrifugeId][voteKey].decreaseFirstNValues(details.quorum + 1); // MUTATION: one lane past the quorum is consumed
 
         bytes32 payloadId = keccak256(abi.encodePacked(centrifugeId, localCentrifugeId, payloadHash));
         emit Execute(centrifugeId, payloadId, payload, adapter);
```

## MultiAdapter #8524

Filing the gas model stores it as the parser instead, so the gas model never changes and the parser is replaced by it.

- **Mutant:** [`8524.sol`](8524.sol)
- **Caught by:** [`stMaFileWritesExactlyTheDependencyItsKeyNames`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L199)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8524`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule stMaFileWritesExactlyTheDependencyItsKeyNames`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -67,7 +67,7 @@
     function file(bytes32 what, address instance) external auth {
         if (what == "gateway") gateway = IMessageHandler(instance);
         else if (what == "parser") parser = IMessageParser(instance);
-        else if (what == "messageGas") messageGas = IMessageGas(instance);
+        else if (what == "messageGas") parser = IMessageParser(instance); // MUTATION: the gas model key writes the parser slot
         else revert FileUnrecognizedParam();
 
         emit File(what, instance);
```

## MultiAdapter #8525

The configuration update drops its admin check, so any account can repoint the gateway, the parser and the gas model.

- **Mutant:** [`8525.sol`](8525.sol)
- **Caught by:** [`acMaOnlyWardRepointsTheGateway`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L37) · [`acMaOnlyWardRepointsTheParser`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L53) · [`acMaOnlyWardRepointsTheMessageGas`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_access_control.spec#L260)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8525`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/access_control.conf --rule acMaOnlyWardRepointsTheGateway acMaOnlyWardRepointsTheParser acMaOnlyWardRepointsTheMessageGas`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -64,7 +64,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IMultiAdapter
-    function file(bytes32 what, address instance) external auth {
+    function file(bytes32 what, address instance) external { // MUTATION: the ward gate on file is gone
         if (what == "gateway") gateway = IMessageHandler(instance);
         else if (what == "parser") parser = IMessageParser(instance);
         else if (what == "messageGas") messageGas = IMessageGas(instance);
```

## MultiAdapter #8526

The gas model key is no longer recognised, so filing a gas model reverts and the dependency can never be set.

- **Mutant:** [`8526.sol`](8526.sol)
- **Caught by:** [`rvMaFileAcceptsAWardUnderAKnownName`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L454)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8526`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaFileAcceptsAWardUnderAKnownName`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -67,7 +67,7 @@
     function file(bytes32 what, address instance) external auth {
         if (what == "gateway") gateway = IMessageHandler(instance);
         else if (what == "parser") parser = IMessageParser(instance);
-        else if (what == "messageGas") messageGas = IMessageGas(instance);
+        // MUTATION: the gas model key is no longer recognised
         else revert FileUnrecognizedParam();
 
         emit File(what, instance);
```

## MultiAdapter #8527

A message's pool is read from the gas model instead of the parser, so whoever files the gas model picks which adapters authenticate it.

- **Mutant:** [`8527.sol`](8527.sol)
- **Caught by:** [`hlMaVoteAsksTheFiledParserNotTheGasModel`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L158)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8527`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/unpinned_properties.conf --rule hlMaVoteAsksTheFiledParserNotTheGasModel`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -360,7 +360,7 @@
 
     /// @dev Send and handle apply the same rule, so both chains agree on the carrying set.
     function _routePoolId(uint16 centrifugeId, bytes calldata payload) internal view returns (PoolId) {
-        PoolId poolId = parser.messagePoolId(payload);
+        PoolId poolId = IMessageParser(address(messageGas)).messagePoolId(payload); // MUTATION: the pool is asked of the gas model
         bool poolConfigured = activeSessionId[centrifugeId][poolId] != 0;
         return parser.routePoolId(payload, poolConfigured);
     }
```

## MultiAdapter #8700

An outbound send hands every adapter a zero gas limit instead of the given one, so destination execution gets no gas.

- **Mutant:** [`8700.sol`](8700.sol)
- **Caught by:** [`hlMaSendCarriesTheGasLimitItWasGiven`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L275)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8700`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendCarriesTheGasLimitItWasGiven`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -286,7 +286,7 @@
 
         uint256 totalCost;
         for (uint256 i = 0; i < adapters_.list.length; i++) {
-            totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], gasLimit, refund);
+            totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], 0, refund); // MUTATION: every adapter is handed a zero gas limit
         }
         if (msg.value > totalCost) SafeTransferLib.safeTransferETH(refund, msg.value - totalCost);
 
```

## MultiAdapter #8701

An outbound send dispatches to the first adapter once per roster member, so the other adapters never carry the message.

- **Mutant:** [`8701.sol`](8701.sol)
- **Caught by:** [`hlMaSendReachesEachRosterMemberOnce`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L289)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8701`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendReachesEachRosterMemberOnce`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -286,7 +286,7 @@
 
         uint256 totalCost;
         for (uint256 i = 0; i < adapters_.list.length; i++) {
-            totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], gasLimit, refund);
+            totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[0], gasLimit, refund); // MUTATION: every dispatch goes to the first roster member
         }
         if (msg.value > totalCost) SafeTransferLib.safeTransferETH(refund, msg.value - totalCost);
 
```

## MultiAdapter #8702

Each adapter is called unpaid while its quote still counts against the caller, so the fee stays stranded in the router.

- **Mutant:** [`8702.sol`](8702.sol)
- **Caught by:** [`hlMaSendFundsEachDispatchWithItsOwnQuote`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L307)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8702`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendFundsEachDispatchWithItsOwnQuote`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -302,7 +302,7 @@
         address refund
     ) internal returns (uint256 cost) {
         cost = adapter.estimate(centrifugeId, payload, gasLimit);
-        bytes32 adapterData = adapter.send{value: cost}(centrifugeId, payload, gasLimit, refund);
+        bytes32 adapterData = adapter.send{value: 0}(centrifugeId, payload, gasLimit, refund); // MUTATION: the adapter dispatch is sent unpaid
         emit SendPayload(centrifugeId, payloadId, payload, adapter, adapterData, gasLimit, cost, refund);
     }
 
```

## MultiAdapter #8705

Inbound messages are checked against the session after their stamped one, so an adapter of that later session can deliver them.

- **Mutant:** [`8705.sol`](8705.sol)
- **Caught by:** [`rvMaHandleRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L368)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8705`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaHandleRefusesASessionTheAdapterIsNotIn`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -253,7 +253,7 @@
         view
         returns (Adapter memory details, bytes32 payloadHash, bytes32 voteKey, bytes calldata unwrappedPayload)
     {
-        uint16 sessionId = uint16(bytes2(payload[0:2]));
+        uint16 sessionId = uint16(bytes2(payload[0:2])) + 1; // MUTATION: the message is resolved against the next session
         unwrappedPayload = payload[2:];
         PoolId poolId = _routePoolId(centrifugeId, unwrappedPayload);
 
```

## MultiAdapter #8706

Explicit execution requires more confirmations than the threshold, so a tally reaching exactly the threshold is never released.

- **Mutant:** [`8706.sol`](8706.sol)
- **Caught by:** [`rcMaExecuteReleasesThePayloadAfterTwoProofsIsReachable`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reachability.spec#L228)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8706`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reachability.conf --rule rcMaExecuteReleasesThePayloadAfterTwoProofsIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -204,7 +204,7 @@
             _resolve(centrifugeId, payload, adapter);
 
         require(
-            _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= details.threshold, NotEnoughVotes()
+            _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) > details.threshold, NotEnoughVotes() // MUTATION: the explicit execution needs more than the threshold
         );
         _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload);
     }
```

## MultiAdapter #8876

An explicit execution weighs the global pool's tally instead of the routed pool's own, so another pool's confirmations release the message.

- **Mutant:** [`8876.sol`](8876.sol)
- **Caught by:** [`hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L169)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8876`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/unpinned_properties.conf --rule hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -204,7 +204,7 @@
             _resolve(centrifugeId, payload, adapter);
 
         require(
-            _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= details.threshold, NotEnoughVotes()
+            _votes[centrifugeId][keccak256(abi.encodePacked(PoolId.wrap(0).raw(), payload))].countPositiveValues(details.quorum) >= details.threshold, NotEnoughVotes() // MUTATION: the global pool's tally is weighed
         );
         _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload);
     }
```

## MultiAdapter #8877

Installing an adapter set first asks every new adapter for a quote, so one rejecting new adapter blocks the whole rotation.

- **Mutant:** [`8877.sol`](8877.sol)
- **Caught by:** [`hlMaRotationCallsNoAdapter`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L385)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8877`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaRotationCallsNoAdapter`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -95,6 +95,7 @@
         require(quorum_ <= MAX_ADAPTER_COUNT, ExceedsMax());
         require(threshold_ > 0 || quorum_ == 0, ZeroThreshold());
         require(threshold_ <= quorum_, ThresholdHigherThanQuorum());
+        for (uint256 i; i < addresses.length; i++) addresses[i].estimate(centrifugeId, "", 0); // MUTATION: every new adapter is asked for a quote
 
         // Advance the session id to reset pending votes
         uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
```

## MultiAdapter #8878

A send skips an adapter whose quote fails instead of failing, so a rejecting active adapter silently drops out of the send.

- **Mutant:** [`8878.sol`](8878.sol)
- **Caught by:** [`rvMaSendFailsWhenARosterAdapterRefuses`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L469)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8878`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSendFailsWhenARosterAdapterRefuses`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -301,7 +301,7 @@
         uint256 gasLimit,
         address refund
     ) internal returns (uint256 cost) {
-        cost = adapter.estimate(centrifugeId, payload, gasLimit);
+        try adapter.estimate(centrifugeId, payload, gasLimit) returns (uint256 quoted) { cost = quoted; } catch { return 0; } // MUTATION: a refusing adapter is skipped
         bytes32 adapterData = adapter.send{value: cost}(centrifugeId, payload, gasLimit, refund);
         emit SendPayload(centrifugeId, payloadId, payload, adapter, adapterData, gasLimit, cost, refund);
     }
```

## MultiAdapter #8879

The pool's adapter manager may vote for an adapter only at a threshold of one, so it alone can no longer release a two of two message.

- **Mutant:** [`8879.sol`](8879.sol)
- **Caught by:** [`rcMaManagerAloneReleasesATwoOfTwoMessageIsReachable`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L206)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8879`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule rcMaManagerAloneReleasesATwoOfTwoMessageIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -257,7 +257,7 @@
         unwrappedPayload = payload[2:];
         PoolId poolId = _routePoolId(centrifugeId, unwrappedPayload);
 
-        require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
+        require(msg.sender == address(adapter) || (manager[poolId][msg.sender] && _adapterDetails[centrifugeId][poolId][sessionId][adapter].threshold == 1), NotAuthorized()); // MUTATION: the manager carve-out holds at threshold one only
 
         details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
         require(details.id != 0, InvalidAdapter());
```

## MultiAdapter #8880

An outbound send starts at the second active adapter, so a rejecting first adapter no longer fails the send.

- **Mutant:** [`8880.sol`](8880.sol)
- **Caught by:** [`rvMaSendFailsWhenARosterAdapterRefuses`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L469)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8880`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSendFailsWhenARosterAdapterRefuses`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -285,7 +285,7 @@
         bytes32 payloadId = keccak256(abi.encodePacked(localCentrifugeId, centrifugeId, keccak256(wrappedPayload)));
 
         uint256 totalCost;
-        for (uint256 i = 0; i < adapters_.list.length; i++) {
+        for (uint256 i = 1; i < adapters_.list.length; i++) { // MUTATION: the first roster member is never carried
             totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], gasLimit, refund);
         }
         if (msg.value > totalCost) SafeTransferLib.safeTransferETH(refund, msg.value - totalCost);
```

## MultiAdapter #8952

unblockSession never clears the stash, so a restored session stays blocked and live at once.

- **Mutant:** [`8952.sol`](8952.sol)
- **Caught by:** [`blockedExcludesLive`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_valid_state.spec#L131)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 8952`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/valid_state.conf --rule blockedExcludesLive`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -141,7 +141,7 @@
             _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, blocked.list);
         }
 
-        delete _blockedSessions[centrifugeId][poolId][sessionId];
+        // MUTATION: the stash is no longer cleared on unblock
 
         emit UnblockSession(centrifugeId, poolId, sessionId);
     }
```

## MultiAdapter #9060

A rotation never stores the advanced session id, so the pool keeps its old id while the route moves on.

- **Mutant:** [`9060.sol`](9060.sol)
- **Caught by:** [`hlMaRotationBumpsTheSessionToTheNamedTarget`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L348)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9060`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaRotationBumpsTheSessionToTheNamedTarget`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -99,7 +99,7 @@
         // Advance the session id to reset pending votes
         uint16 sessionId = activeSessionId[centrifugeId][poolId] + 1;
         require(sessionId == targetSessionId, UnexpectedSessionId());
-        activeSessionId[centrifugeId][poolId] = sessionId;
+        // MUTATION: the advanced session id is never stored back into activeSessionId
 
         _installSession(centrifugeId, poolId, sessionId, addresses, threshold_);
         _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, addresses);
```

## MultiAdapter #9061

Releasing a message no longer spends its confirmations, so the same message can be released again.

- **Mutant:** [`9061.sol`](9061.sol)
- **Caught by:** [`hlMaExecuteLowersTheTallyItSpends`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L99) · [`hlMaExecuteSpendsTheTallyBeforeForwarding`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L85)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9061`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule hlMaExecuteLowersTheTallyItSpends hlMaExecuteSpendsTheTallyBeforeForwarding`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -237,7 +237,7 @@
         bytes32 voteKey,
         bytes calldata unwrappedPayload
     ) internal {
-        _votes[centrifugeId][voteKey].decreaseFirstNValues(details.quorum);
+        // MUTATION: the release no longer spends the tally (decreaseFirstNValues removed)
 
         bytes32 payloadId = keccak256(abi.encodePacked(centrifugeId, localCentrifugeId, payloadHash));
         emit Execute(centrifugeId, payloadId, payload, adapter);
```

## MultiAdapter #9077

Outbound messages go out without the session stamp, so every bridge reads the first two body bytes as the session.

- **Mutant:** [`9077.sol`](9077.sol)
- **Caught by:** [`hlMaSendDispatchesTheStampedPayloadAtFullLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L321)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9077`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendDispatchesTheStampedPayloadAtFullLength`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -281,7 +281,7 @@
         Adapters memory adapters_ = _activeAdapters[centrifugeId][poolId];
         require(adapters_.list.length != 0, EmptyAdapterSet());
 
-        bytes memory wrappedPayload = abi.encodePacked(adapters_.sessionId, payload);
+        bytes memory wrappedPayload = payload; // MUTATION: the session stamp is never prepended
         bytes32 payloadId = keccak256(abi.encodePacked(localCentrifugeId, centrifugeId, keccak256(wrappedPayload)));
 
         uint256 totalCost;
```

## MultiAdapter #9078

Outbound messages carry the session stamp twice, so every bridge receives the body two bytes late.

- **Mutant:** [`9078.sol`](9078.sol)
- **Caught by:** [`hlMaSendDispatchesTheStampedPayloadAtFullLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L321)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9078`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendDispatchesTheStampedPayloadAtFullLength`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -281,7 +281,7 @@
         Adapters memory adapters_ = _activeAdapters[centrifugeId][poolId];
         require(adapters_.list.length != 0, EmptyAdapterSet());
 
-        bytes memory wrappedPayload = abi.encodePacked(adapters_.sessionId, payload);
+        bytes memory wrappedPayload = abi.encodePacked(adapters_.sessionId, adapters_.sessionId, payload); // MUTATION: the session stamp is prepended twice
         bytes32 payloadId = keccak256(abi.encodePacked(localCentrifugeId, centrifugeId, keccak256(wrappedPayload)));
 
         uint256 totalCost;
```

## MultiAdapter #9079

Outbound messages carry a stray trailing byte, so every bridge receives a body one byte longer than was sent.

- **Mutant:** [`9079.sol`](9079.sol)
- **Caught by:** [`hlMaSendDispatchesTheStampedPayloadAtFullLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L321)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9079`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendDispatchesTheStampedPayloadAtFullLength`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -281,7 +281,7 @@
         Adapters memory adapters_ = _activeAdapters[centrifugeId][poolId];
         require(adapters_.list.length != 0, EmptyAdapterSet());
 
-        bytes memory wrappedPayload = abi.encodePacked(adapters_.sessionId, payload);
+        bytes memory wrappedPayload = abi.encodePacked(adapters_.sessionId, payload, bytes1(0)); // MUTATION: a stray zero byte is appended after the body
         bytes32 payloadId = keccak256(abi.encodePacked(localCentrifugeId, centrifugeId, keccak256(wrappedPayload)));
 
         uint256 totalCost;
```

## MultiAdapter #9087

An outbound dispatch carries the session stamp alone and drops the message body, so every bridge delivers an empty message.

- **Mutant:** [`9087.sol`](9087.sol)
- **Caught by:** [`hlMaSendDispatchesTheStampedPayloadAtFullLength`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L321)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9087`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendDispatchesTheStampedPayloadAtFullLength`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -281,7 +281,7 @@
         Adapters memory adapters_ = _activeAdapters[centrifugeId][poolId];
         require(adapters_.list.length != 0, EmptyAdapterSet());
 
-        bytes memory wrappedPayload = abi.encodePacked(adapters_.sessionId, payload);
+        bytes memory wrappedPayload = abi.encodePacked(adapters_.sessionId); // MUTATION: only the session stamp is dispatched
         bytes32 payloadId = keccak256(abi.encodePacked(localCentrifugeId, centrifugeId, keccak256(wrappedPayload)));
 
         uint256 totalCost;
```

## MultiAdapter #9421

A vote checks the submitter instead of the named adapter, so an adapter outside the session gets a vote.

- **Mutant:** [`9421.sol`](9421.sol)
- **Caught by:** [`rvMaVoteRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L383)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9421`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaVoteRefusesASessionTheAdapterIsNotIn`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -189,7 +189,7 @@
 
     /// @inheritdoc IMultiAdapter
     function vote(uint16 centrifugeId, bytes calldata payload, IAdapter adapter) public {
-        (Adapter memory details, bytes32 payloadHash, bytes32 voteKey,) = _resolve(centrifugeId, payload, adapter);
+        (Adapter memory details, bytes32 payloadHash, bytes32 voteKey,) = _resolve(centrifugeId, payload, IAdapter(msg.sender)); // MUTATION: the vote resolves the submitter, not the named adapter
         _vote(centrifugeId, payload, adapter, details, payloadHash, voteKey);
     }
 
```

## MultiAdapter #9422

An execution checks the submitter instead of the named adapter, so a tally is spent for an adapter outside the session.

- **Mutant:** [`9422.sol`](9422.sol)
- **Caught by:** [`rvMaExecuteRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L397)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9422`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaExecuteRefusesASessionTheAdapterIsNotIn`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -201,7 +201,7 @@
     /// @inheritdoc IMultiAdapter
     function execute(uint16 centrifugeId, bytes calldata payload, IAdapter adapter) public {
         (Adapter memory details, bytes32 payloadHash, bytes32 voteKey, bytes calldata unwrappedPayload) =
-            _resolve(centrifugeId, payload, adapter);
+            _resolve(centrifugeId, payload, IAdapter(msg.sender)); // MUTATION: the execution resolves the submitter, not the named adapter
 
         require(
             _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= details.threshold, NotEnoughVotes()
```

## MultiAdapter #9423

A self delivery is credited to the transaction origin, so a relaying manager delivers as an adapter it is not.

- **Mutant:** [`9423.sol`](9423.sol)
- **Caught by:** [`rvMaSelfDeliveryHandleRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L412)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9423`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSelfDeliveryHandleRefusesASessionTheSenderIsNotIn`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -170,7 +170,7 @@
     /// @dev Equivalent to vote() followed by execute(): cast this adapter's vote and, if it reaches the
     ///      threshold, consume the quorum's votes and forward to the gateway.
     function handle(uint16 centrifugeId, bytes calldata payload) external {
-        handle(centrifugeId, payload, IAdapter(msg.sender));
+        handle(centrifugeId, payload, IAdapter(tx.origin)); // MUTATION: the delivery is attributed to the transaction origin
     }
 
     /// @inheritdoc IMultiAdapter
```

## MultiAdapter #9424

A self vote is credited to the transaction origin, so a relaying manager votes as an adapter it is not.

- **Mutant:** [`9424.sol`](9424.sol)
- **Caught by:** [`rvMaSelfDeliveryVoteRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L426)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9424`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSelfDeliveryVoteRefusesASessionTheSenderIsNotIn`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -184,7 +184,7 @@
 
     /// @inheritdoc IAdapterEntrypoint
     function vote(uint16 centrifugeId, bytes calldata payload) external {
-        vote(centrifugeId, payload, IAdapter(msg.sender));
+        vote(centrifugeId, payload, IAdapter(tx.origin)); // MUTATION: the vote is attributed to the transaction origin
     }
 
     /// @inheritdoc IMultiAdapter
```

## MultiAdapter #9425

A self execution is credited to the transaction origin, so a relaying manager spends a tally as an adapter it is not.

- **Mutant:** [`9425.sol`](9425.sol)
- **Caught by:** [`rvMaSelfDeliveryExecuteRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L440)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9425`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaSelfDeliveryExecuteRefusesASessionTheSenderIsNotIn`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -195,7 +195,7 @@
 
     /// @inheritdoc IAdapterEntrypoint
     function execute(uint16 centrifugeId, bytes calldata payload) external {
-        execute(centrifugeId, payload, IAdapter(msg.sender));
+        execute(centrifugeId, payload, IAdapter(tx.origin)); // MUTATION: the execution is attributed to the transaction origin
     }
 
     /// @inheritdoc IMultiAdapter
```

## MultiAdapter #9426

Unblocking the session in service restores the route with an empty roster, so it still cannot send.

- **Mutant:** [`9426.sol`](9426.sol)
- **Caught by:** [`stMaUnblockReopensTheRouteOnlyForTheSessionInService`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_transitions.spec#L166)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9426`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/transitions.conf --rule stMaUnblockReopensTheRouteOnlyForTheSessionInService`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -138,7 +138,7 @@
 
         // Only restore the active set if this is still the active session; a later setAdapters may have replaced it.
         if (blocked.wasActive && sessionId == activeSessionId[centrifugeId][poolId]) {
-            _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, blocked.list);
+            _activeAdapters[centrifugeId][poolId] = Adapters(sessionId, new IAdapter[](0)); // MUTATION: the route is restamped but its roster is not restored
         }
 
         delete _blockedSessions[centrifugeId][poolId][sessionId];
```

## MultiAdapter #9427

Submissions are checked against the previous session, so an adapter dropped from the stamped one still votes and executes.

- **Mutant:** [`9427.sol`](9427.sol)
- **Caught by:** [`rvMaVoteRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L383) · [`rvMaExecuteRefusesASessionTheAdapterIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L397) · [`rvMaSelfDeliveryHandleRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L412) · [`rvMaSelfDeliveryVoteRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L426) · [`rvMaSelfDeliveryExecuteRefusesASessionTheSenderIsNotIn`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_reverts.spec#L440)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9427`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/reverts.conf --rule rvMaVoteRefusesASessionTheAdapterIsNotIn rvMaExecuteRefusesASessionTheAdapterIsNotIn rvMaSelfDeliveryHandleRefusesASessionTheSenderIsNotIn rvMaSelfDeliveryVoteRefusesASessionTheSenderIsNotIn rvMaSelfDeliveryExecuteRefusesASessionTheSenderIsNotIn`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -259,7 +259,7 @@
 
         require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
 
-        details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
+        details = _adapterDetails[centrifugeId][poolId][sessionId - 1][adapter]; // MUTATION: the submission is checked against the previous session
         require(details.id != 0, InvalidAdapter());
 
         payloadHash = keccak256(payload);
```

## MultiAdapter #9428

Unblocking restores the stashed adapter set into the next session, so the unblocked session stays without adapters.

- **Mutant:** [`9428.sol`](9428.sol)
- **Caught by:** [`hlMaUnblockEmptiesTheStashIntoItsOwnSession`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L364)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9428`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaUnblockEmptiesTheStashIntoItsOwnSession`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -134,7 +134,7 @@
         require(blocked.list.length != 0, SessionNotBlocked());
 
         // Move the configuration back into the live storage, rebuilding the per-adapter details.
-        _installSession(centrifugeId, poolId, sessionId, blocked.list, blocked.threshold);
+        _installSession(centrifugeId, poolId, sessionId + 1, blocked.list, blocked.threshold); // MUTATION: the stash is restored into the next session
 
         // Only restore the active set if this is still the active session; a later setAdapters may have replaced it.
         if (blocked.wasActive && sessionId == activeSessionId[centrifugeId][poolId]) {
```

## MultiAdapter #9620

An adapter is looked up in the active session, not the payload's stamped one, so a message stamped with a future session collects votes.

- **Mutant:** [`9620.sol`](9620.sol)
- **Caught by:** [`futureSessionTallyEmpty`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9620`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule futureSessionTallyEmpty`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -259,7 +259,7 @@
 
         require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
 
-        details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
+        details = _adapterDetails[centrifugeId][poolId][activeSessionId[centrifugeId][poolId]][adapter]; // MUTATION: the session in service replaces the stamped one
         require(details.id != 0, InvalidAdapter());
 
         payloadHash = keccak256(payload);
```

## MultiAdapter #9621

an explicit execution accepts a tally one confirmation short of the threshold, so a payload is released before enough adapters agreed.

- **Mutant:** [`9621.sol`](9621.sol)
- **Caught by:** [`hlMaExecuteForwardsOnlyOverAThresholdOfPositiveLanes`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L60)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9621`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule hlMaExecuteForwardsOnlyOverAThresholdOfPositiveLanes`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -204,7 +204,7 @@
             _resolve(centrifugeId, payload, adapter);
 
         require(
-            _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= details.threshold, NotEnoughVotes()
+            _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= details.threshold - 1, NotEnoughVotes() // MUTATION: one confirmation short passes
         );
         _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload);
     }
```

## MultiAdapter #9622

The gateway is called before the tally is spent and again after, so a released message is delivered twice.

- **Mutant:** [`9622.sol`](9622.sol)
- **Caught by:** [`hlMaExecuteSpendsTheTallyBeforeForwarding`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L85)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9622`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule hlMaExecuteSpendsTheTallyBeforeForwarding`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -237,7 +237,7 @@
         bytes32 voteKey,
         bytes calldata unwrappedPayload
     ) internal {
-        _votes[centrifugeId][voteKey].decreaseFirstNValues(details.quorum);
+        gateway.handle(centrifugeId, unwrappedPayload); _votes[centrifugeId][voteKey].decreaseFirstNValues(details.quorum); // MUTATION: the gateway hears the message before the tally is spent
 
         bytes32 payloadId = keccak256(abi.encodePacked(centrifugeId, localCentrifugeId, payloadHash));
         emit Execute(centrifugeId, payloadId, payload, adapter);
```

## MultiAdapter #9623

a released payload reaches the gateway with its session stamp still attached, so the gateway parses two stamp bytes as the message.

- **Mutant:** [`9623.sol`](9623.sol)
- **Caught by:** [`hlMaExecuteHandsTheGatewayTheUnstampedMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L113) · [`hlMaHandleHandsTheGatewayTheUnstampedMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L127)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9623`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule hlMaExecuteHandsTheGatewayTheUnstampedMessage hlMaHandleHandsTheGatewayTheUnstampedMessage`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -242,7 +242,7 @@
         bytes32 payloadId = keccak256(abi.encodePacked(centrifugeId, localCentrifugeId, payloadHash));
         emit Execute(centrifugeId, payloadId, payload, adapter);
 
-        gateway.handle(centrifugeId, unwrappedPayload);
+        gateway.handle(centrifugeId, payload); // MUTATION: the stamped payload is forwarded
     }
 
     /// @dev Parse a wrapped payload and resolve `adapter`'s config and the payload hash. The caller must be
```

## MultiAdapter #9625

A delivery that completes the quorum forwards the stamped payload, so the gateway reads the stamp bytes as the message.

- **Mutant:** [`9625.sol`](9625.sol)
- **Caught by:** [`hlMaHandleHandsTheGatewayTheUnstampedMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L127)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9625`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule hlMaHandleHandsTheGatewayTheUnstampedMessage`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -178,7 +178,7 @@
         (Adapter memory details, bytes32 payloadHash, bytes32 voteKey, bytes calldata unwrappedPayload) =
             _resolve(centrifugeId, payload, adapter);
         if (_vote(centrifugeId, payload, adapter, details, payloadHash, voteKey)) {
-            _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload);
+            _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, payload); // MUTATION: the delivery forwards the stamped payload
         }
     }
 
```

## MultiAdapter #9626

a send refunds one wei less than the surplus, so the route keeps a wei of every overpaid send.

- **Mutant:** [`9626.sol`](9626.sol)
- **Caught by:** [`hlMaSendRefundsTheSurplusAndKeepsNoEth`](../../specs/core/messaging/MultiAdapter/MultiAdapter_refund_properties.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9626`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/refund_properties.conf --rule hlMaSendRefundsTheSurplusAndKeepsNoEth`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -288,7 +288,7 @@
         for (uint256 i = 0; i < adapters_.list.length; i++) {
             totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], gasLimit, refund);
         }
-        if (msg.value > totalCost) SafeTransferLib.safeTransferETH(refund, msg.value - totalCost);
+        if (msg.value > totalCost) SafeTransferLib.safeTransferETH(refund, msg.value - totalCost - 1); // MUTATION: one wei is kept
 
         return bytes32(0);
     }
```

## MultiAdapter #9627

each adapter is paid the quote the refund address gives instead of its own, so an adapter can be underpaid or overpaid for its delivery.

- **Mutant:** [`9627.sol`](9627.sol)
- **Caught by:** [`hlMaSendPaysEachAdapterTheQuoteItGaveItself`](../../specs/core/messaging/MultiAdapter/single/MultiAdapter_high_level.spec#L335)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9627`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/high_level.conf --rule hlMaSendPaysEachAdapterTheQuoteItGaveItself`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -301,7 +301,7 @@
         uint256 gasLimit,
         address refund
     ) internal returns (uint256 cost) {
-        cost = adapter.estimate(centrifugeId, payload, gasLimit);
+        cost = IAdapter(refund).estimate(centrifugeId, payload, gasLimit); // MUTATION: the refund address quotes
         bytes32 adapterData = adapter.send{value: cost}(centrifugeId, payload, gasLimit, refund);
         emit SendPayload(centrifugeId, payloadId, payload, adapter, adapterData, gasLimit, cost, refund);
     }
```

## MultiAdapter #9628

a delivery that releases its payload records its confirmation again after the gateway call, so the spent tally is topped up behind the forward.

- **Mutant:** [`9628.sol`](9628.sol)
- **Caught by:** [`hlMaHandleSpendsTheTallyBeforeForwarding`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L141)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9628`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule hlMaHandleSpendsTheTallyBeforeForwarding`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -178,7 +178,7 @@
         (Adapter memory details, bytes32 payloadHash, bytes32 voteKey, bytes calldata unwrappedPayload) =
             _resolve(centrifugeId, payload, adapter);
         if (_vote(centrifugeId, payload, adapter, details, payloadHash, voteKey)) {
-            _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload);
+            _execute(centrifugeId, payload, adapter, details, payloadHash, voteKey, unwrappedPayload); _vote(centrifugeId, payload, adapter, details, payloadHash, voteKey); // MUTATION: the vote is recorded again after the forward
         }
     }
 
```

## MultiAdapter #9630

the vote key leaves out the routed pool, so every pool's deliveries of one stamped message count on one shared tally.

- **Mutant:** [`9630.sol`](9630.sol)
- **Caught by:** [`hlMaVoteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L6) · [`hlMaHandleMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L36) · [`hlMaExecuteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L66) · [`hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L169)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9630`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/unpinned_properties.conf --rule hlMaVoteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage hlMaHandleMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage hlMaExecuteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -263,7 +263,7 @@
         require(details.id != 0, InvalidAdapter());
 
         payloadHash = keccak256(payload);
-        voteKey = keccak256(abi.encodePacked(poolId.raw(), payload));
+        voteKey = keccak256(abi.encodePacked(PoolId.wrap(0).raw(), payload)); // MUTATION: the pool is dropped from the key
     }
 
     //----------------------------------------------------------------------------------------------
```

## MultiAdapter #9631

the vote key hashes the message without its session stamp, so confirmations cast under different sessions count on one tally.

- **Mutant:** [`9631.sol`](9631.sol)
- **Caught by:** [`hlMaVoteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L6) · [`hlMaExecuteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L66) · [`hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L169)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9631`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/unpinned_properties.conf --rule hlMaVoteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage hlMaExecuteMovesOnlyTheTallyOfItsOwnPoolSessionAndMessage hlMaExecuteForwardsOnlyOverTheRoutedPoolsOwnTally`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -263,7 +263,7 @@
         require(details.id != 0, InvalidAdapter());
 
         payloadHash = keccak256(payload);
-        voteKey = keccak256(abi.encodePacked(poolId.raw(), payload));
+        voteKey = keccak256(abi.encodePacked(poolId.raw(), unwrappedPayload)); // MUTATION: the session is dropped from the key
     }
 
     //----------------------------------------------------------------------------------------------
```

## MultiAdapter #9632

an inbound message is checked against the global pool's roster whatever pool the router names, so a pool's own adapter set never guards it.

- **Mutant:** [`9632.sol`](9632.sol)
- **Caught by:** [`hlMaHandleIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L96) · [`hlMaVoteIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L108) · [`hlMaExecuteIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L120)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9632`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/unpinned_properties.conf --rule hlMaHandleIsJudgedByTheRoutedPoolsRosterAndManagers hlMaVoteIsJudgedByTheRoutedPoolsRosterAndManagers hlMaExecuteIsJudgedByTheRoutedPoolsRosterAndManagers`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -259,7 +259,7 @@
 
         require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
 
-        details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
+        details = _adapterDetails[centrifugeId][PoolId.wrap(0)][sessionId][adapter]; // MUTATION: the global roster is read
         require(details.id != 0, InvalidAdapter());
 
         payloadHash = keccak256(payload);
```

## MultiAdapter #9633

a manager of the global pool may submit in any pool's adapter's name, so the routed pool's own managers no longer decide who submits.

- **Mutant:** [`9633.sol`](9633.sol)
- **Caught by:** [`hlMaHandleIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L96) · [`hlMaVoteIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L108) · [`hlMaExecuteIsJudgedByTheRoutedPoolsRosterAndManagers`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L120)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9633`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/unpinned_properties.conf --rule hlMaHandleIsJudgedByTheRoutedPoolsRosterAndManagers hlMaVoteIsJudgedByTheRoutedPoolsRosterAndManagers hlMaExecuteIsJudgedByTheRoutedPoolsRosterAndManagers`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -257,7 +257,7 @@
         unwrappedPayload = payload[2:];
         PoolId poolId = _routePoolId(centrifugeId, unwrappedPayload);
 
-        require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
+        require(msg.sender == address(adapter) || manager[PoolId.wrap(0)][msg.sender], NotAuthorized()); // MUTATION: the global pool's managers are asked
 
         details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
         require(details.id != 0, InvalidAdapter());
```

## MultiAdapter #9634

the router is told a configured pool is unconfigured and the reverse, so a configured pool's message falls back to the global adapter set.

- **Mutant:** [`9634.sol`](9634.sol)
- **Caught by:** [`hlMaVoteAsksTheRouterAboutTheMessagesOwnPoolsConfiguration`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L132)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9634`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/unpinned_properties.conf --rule hlMaVoteAsksTheRouterAboutTheMessagesOwnPoolsConfiguration`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -361,7 +361,7 @@
     /// @dev Send and handle apply the same rule, so both chains agree on the carrying set.
     function _routePoolId(uint16 centrifugeId, bytes calldata payload) internal view returns (PoolId) {
         PoolId poolId = parser.messagePoolId(payload);
-        bool poolConfigured = activeSessionId[centrifugeId][poolId] != 0;
+        bool poolConfigured = activeSessionId[centrifugeId][poolId] == 0; // MUTATION: the configuration flag is inverted
         return parser.routePoolId(payload, poolConfigured);
     }
 
```

## MultiAdapter #9635

the router reads the stamped payload instead of the message, so the session bytes are parsed as the message type and pool.

- **Mutant:** [`9635.sol`](9635.sol)
- **Caught by:** [`hlMaVoteHandsTheRouterTheUnstampedMessage`](../../specs/core/messaging/MultiAdapter/MultiAdapter_unpinned_properties.spec#L146)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9635`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/unpinned_properties.conf --rule hlMaVoteHandsTheRouterTheUnstampedMessage`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -255,7 +255,7 @@
     {
         uint16 sessionId = uint16(bytes2(payload[0:2]));
         unwrappedPayload = payload[2:];
-        PoolId poolId = _routePoolId(centrifugeId, unwrappedPayload);
+        PoolId poolId = _routePoolId(centrifugeId, payload); // MUTATION: the stamped payload is routed
 
         require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
 
```

## MultiAdapter #9636

a delivery needs strictly more confirmations than the threshold, so a one of one roster can never release anything.

- **Mutant:** [`9636.sol`](9636.sol)
- **Caught by:** [`rcMaSamePayloadIsReleasedTwiceIsReachable`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L160)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9636`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule rcMaSamePayloadIsReleasedTwiceIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -220,7 +220,7 @@
         bytes32 voteKey
     ) internal returns (bool reached) {
         _votes[centrifugeId][voteKey][details.id - 1]++;
-        reached = _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) >= details.threshold;
+        reached = _votes[centrifugeId][voteKey].countPositiveValues(details.quorum) > details.threshold; // MUTATION: the bar must be exceeded
 
         bytes32 payloadId = keccak256(abi.encodePacked(centrifugeId, localCentrifugeId, payloadHash));
         emit Vote(centrifugeId, payloadId, payload, adapter);
```

## MultiAdapter #9637

A refused refund is ignored instead of reverting the send, so the surplus silently stays in the contract.

- **Mutant:** [`9637.sol`](9637.sol)
- **Caught by:** [`rcMaRejectingRefundAddressUndoesTheWholeFanOutIsReachable`](../../specs/core/messaging/MultiAdapter/MultiAdapter_refund_properties.spec#L33)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9637`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/refund_properties.conf --rule rcMaRejectingRefundAddressUndoesTheWholeFanOutIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -288,7 +288,7 @@
         for (uint256 i = 0; i < adapters_.list.length; i++) {
             totalCost += _sendToAdapter(centrifugeId, payloadId, wrappedPayload, adapters_.list[i], gasLimit, refund);
         }
-        if (msg.value > totalCost) SafeTransferLib.safeTransferETH(refund, msg.value - totalCost);
+        if (msg.value > totalCost) refund.call{value: msg.value - totalCost}(""); // MUTATION: a refused refund is ignored
 
         return bytes32(0);
     }
```

## MultiAdapter #9638

only the adapter itself may deliver, so a pool manager can no longer submit a confirmation in a rostered adapter's name.

- **Mutant:** [`9638.sol`](9638.sol)
- **Caught by:** [`rcMaAManagerReleasesAPayloadNoAdapterDeliveredIsReachable`](../../specs/core/messaging/MultiAdapter/MultiAdapter_payload_properties.spec#L185)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MultiAdapter 9638`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MultiAdapter/payload_properties.conf --rule rcMaAManagerReleasesAPayloadNoAdapterDeliveredIsReachable`

```diff
--- a/src/core/messaging/MultiAdapter.sol
+++ b/src/core/messaging/MultiAdapter.sol
@@ -257,7 +257,7 @@
         unwrappedPayload = payload[2:];
         PoolId poolId = _routePoolId(centrifugeId, unwrappedPayload);
 
-        require(msg.sender == address(adapter) || manager[poolId][msg.sender], NotAuthorized());
+        require(msg.sender == address(adapter), NotAuthorized()); // MUTATION: the manager path is removed
 
         details = _adapterDetails[centrifugeId][poolId][sessionId][adapter];
         require(details.id != 0, InvalidAdapter());
```

