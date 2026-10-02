# Mutations for `HubHandler` (`src/core/hub/HubHandler.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/hub/Accounting.sol`, `src/core/hub/Holdings.sol`, `src/core/hub/Hub.sol`, `src/core/hub/HubRegistry.sol`, `src/core/hub/ShareClassManager.sol`, `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [3104](#hubhandler-3104) | A network's report flips the snapshot flag without spending that network's nonce, so the same position can be reported twice under one number.<br>Caught by: [`stHhSnapshotFlagCostsANonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L164) |
| [3109](#hubhandler-3109) | A revocation lowers the network's leg without lowering the class total, so the total stops following the legs it is made of.<br>Caught by: [`stHhShareLedgerMovesWithItsNetworkLegs`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L149) |
| [3110](#hubhandler-3110) | A decrease that leaves a holding short no longer updates the shortfall counts, so they stop following the short holdings.<br>Caught by: [`stHhNetworkDeficitCountFollowsTheShortRows`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L179) · [`stHhClassDeficitCountFollowsTheShortRows`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L194) |
| [4400](#hubhandler-4400) | file drops the ward gate, so any caller can repoint the hub, holdings, message sender or share class manager.<br>Caught by: [`acHhOnlyAWardMovesTheHubPointer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L21) · [`acHhOnlyAWardMovesTheHoldingsPointer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L37) · [`acHhOnlyAWardMovesTheSenderPointer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L53) · [`acHhOnlyAWardMovesTheShareClassManagerPointer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L70) |
| [4401](#hubhandler-4401) | updateAssets drops the ward gate, so any caller can move holdings, a network's snapshot state and the pool's ledger.<br>Caught by: [`acHhOnlyAWardMovesADepositHistory`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L121) · [`acHhOnlyAWardMovesAWithdrawalHistory`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L138) · [`acHhOnlyAWardMovesACarriedValue`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L155) · [`acHhOnlyAWardMovesTheDeficitCount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L172) · [`acHhOnlyAWardMovesASyncMarker`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L192) · [`acHhOnlyAWardMovesASnapshotNonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L208) · [`acHhOnlyAWardMovesALedgerDebit`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L278) · [`acHhOnlyAWardMovesALedgerCredit`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L295) · [`acHhOnlyAWardMovesTheJournalCounter`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L312) |
| [4402](#hubhandler-4402) | updateShares drops the ward gate, so any caller can move a network's minted and burned totals and the supply of the share class.<br>Caught by: [`acHhOnlyAWardMovesANetworkIssuedTotal`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L225) · [`acHhOnlyAWardMovesANetworkRevokedTotal`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L242) · [`acHhOnlyAWardMovesTheClassSupply`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L259) |
| [4403](#hubhandler-4403) | registerAsset drops the ward gate, so any caller can onboard an asset id and fix the precision every later price conversion reads.<br>Caught by: [`acHhOnlyAWardRegistersAnAsset`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L87) · [`acHhOnlyAWardMovesAnAssetDecimals`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L104) |
| [4404](#hubhandler-4404) | request drops the ward gate, so any caller can drive an investor order into the pool's registered request manager.<br>Caught by: [`acHhOnlyAWardForwardsAnInvestorRequest`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L329) |
| [4405](#hubhandler-4405) | initiateTransferShares drops the ward gate, so any caller can have the hub announce a share transfer to another network.<br>Caught by: [`acHhOnlyAWardSendsAnOutboundMessage`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L346) |
| [4406](#hubhandler-4406) | rely drops the ward gate, so any caller can add an address to the roll that feeds the hub its cross chain traffic.<br>Caught by: [`acHhOnlyAWardMovesTheWardSet`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L4) |
| [4410](#hubhandler-4410) | updateShares books a revocation as an issuance on the class total, so a revocation report inflates the class supply.<br>Caught by: [`hlHhShareReportMovesTheClassTotalInStep`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L276) |
| [4411](#hubhandler-4411) | _updateNetwork drops the per-network issuance write, so share reports and transfer mints never reach that network's issued total.<br>Caught by: [`hlHhShareReportLandsOnItsCounter`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L258) · [`hlHhTransferSendsTheAmountItMints`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L41) |
| [4412](#hubhandler-4412) | the outbound transfer message announces one share more than the ledgers move, so it overstates the amount sent.<br>Caught by: [`hlHhTransferDebitsOriginByTheSentAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L23) · [`hlHhHooklessTransferKeepsTheAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L105) |
| [4413](#hubhandler-4413) | the outbound transfer message swaps origin and target networks, so the burn and the mint are announced on the wrong chains.<br>Caught by: [`hlHhTransferKeepsTheOriginNetwork`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L59) · [`hlHhTransferKeepsTheTargetNetwork`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L74) |
| [4414](#hubhandler-4414) | the outbound execute transfer names the sending party as the recipient, so the shares are handed to the wrong account on the target network.<br>Caught by: [`hlHhHooklessTransferKeepsTheReceiver`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L89) |
| [4415](#hubhandler-4415) | the outbound execute transfer drops the caller's refund address, so the unspent gas payment no longer returns where the caller sent it.<br>Caught by: [`hlHhHooklessTransferKeepsTheRefund`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L121) |
| [4416](#hubhandler-4416) | a zero sized transfer updates the hub ledgers but sends no message, so the destination network never hears of it.<br>Caught by: [`hlHhTransferSendsExactlyOneMessage`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L137) · [`hlHhTransferSendsAnExecuteTransfer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L154) |
| [4417](#hubhandler-4417) | an asset report's deposit lands on the next asset id, so a neighbouring holding grows instead of the reported one.<br>Caught by: [`hlHhAssetReportLandsGrossOnItsSide`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L169) · [`hlHhAssetReportLeavesOtherIncreasesAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L207) · [`hlHhAssetReportLeavesOtherValuesAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L241) |
| [4418](#hubhandler-4418) | an asset report's withdrawal is booked on the next asset id, so a bystander holding's outflow moves instead.<br>Caught by: [`hlHhAssetReportLeavesOtherDecreasesAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L224) |
| [4419](#hubhandler-4419) | increase also nets the deposit against the outstanding withdrawal, so an inflow report shrinks the outflow total.<br>Caught by: [`hlHhAssetReportLeavesTheOppositeSideAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L188) |
| [4420](#hubhandler-4420) | a request with an empty body is dropped instead of forwarded, so the registered manager never receives it.<br>Caught by: [`hlHhRequestForwardsExactlyOnce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L292) · [`hlHhRequestReachesTheRegisteredManager`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L307) · [`hlHhRequestForwardsThePool`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L322) · [`hlHhRequestForwardsTheShareClass`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L335) · [`hlHhRequestForwardsTheAsset`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L348) · [`hlHhRequestForwardsThePayload`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L361) |
| [4430](#hubhandler-4430) | file no longer reverts on an unknown parameter name, so a mistyped rewiring silently succeeds and changes nothing.<br>Caught by: [`rvHhFileRefusesANonWardOrAnUnknownName`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L4) |
| [4431](#hubhandler-4431) | registerAsset drops the eighteen decimal cap, so a registration the handler must refuse for oversized precision goes through.<br>Caught by: [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292) |
| [4433](#hubhandler-4433) | updateShares skips the share class existence check, so share reports go through on an unknown class.<br>Caught by: [`rvHhUpdateSharesRefusesANonWardAnUnknownClassOrAMissedNonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L37) |
| [4434](#hubhandler-4434) | setSnapshot accepts any ordering number at or below the one it holds, so a replayed or reordered report is no longer turned away.<br>Caught by: [`rvHhUpdateAssetsRefusesANonWardOrAMissedNonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L55) · [`rvHhUpdateSharesRefusesANonWardAnUnknownClassOrAMissedNonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L37) |
| [4435](#hubhandler-4435) | rely drops the ward gate, so granting the handler's ward succeeds for a caller that holds none.<br>Caught by: [`rvHhRelyRefusesANonWard`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L159) |
| [4436](#hubhandler-4436) | deny drops the ward gate, so revoking the handler's ward succeeds for a caller that holds none.<br>Caught by: [`rvHhDenyRefusesANonWard`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L172) |
| [4437](#hubhandler-4437) | the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.<br>Caught by: [`rvHhRequestRefusesANonWardOrANetworkWithNoManager`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L20) · [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292) |
| [4440](#hubhandler-4440) | setSnapshot advances a network's ordering number by two, so the snapshot sequence skips a step on a single report.<br>Caught by: [`vtHhSnapshotSequenceStepsByAtMostOne`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L6) |
| [4441](#hubhandler-4441) | the pool's journal counter advances by two, so the journal numbering skips an id on every entry the handler drives.<br>Caught by: [`vtHhJournalSequenceStepsByAtMostOne`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L22) |
| [4443](#hubhandler-4443) | increase also nets the deposit against the recorded withdrawals, so a holding's outflow history shrinks on an inbound report.<br>Caught by: [`vtHhHoldingFlowHistoryNeverShrinks`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L55) |
| [4444](#hubhandler-4444) | a network's minted total is overwritten by the reported amount instead of accumulated, so the record of what a chain has minted can shrink.<br>Caught by: [`vtHhNetworkShareHistoryNeverShrinks`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L73) |
| [4445](#hubhandler-4445) | a debit overwrites the account's running debit total instead of accumulating into it, so a ledger row's posted history can shrink.<br>Caught by: [`vtHhLedgerRowTotalsNeverShrink`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L91) |
| [4448](#hubhandler-4448) | updateAssets moves the holding's value but posts zero to the ledger, so the holdings and the pool's books drift apart.<br>Caught by: [`postedDebitsCoverCarriedValue`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_valid_state.spec#L6) |
| [6500](#hubhandler-6500) | registerAsset stores the announced asset row without its live flag, so an asset the spoke announced never reads as registered.<br>Caught by: [`rcHhRegisterAssetIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L4) |
| [6501](#hubhandler-6501) | registerAsset refuses the highest precision it documents as accepted, so an asset declaring eighteen decimals can no longer be onboarded.<br>Caught by: [`rcHhRegisterAssetAtTheDecimalsCeilingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L20) |
| [6502](#hubhandler-6502) | registerAsset refuses an announcement that carries no decimals at all, so the floor of the accepted range is closed.<br>Caught by: [`rcHhRegisterAssetAtZeroDecimalsIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L36) |
| [6503](#hubhandler-6503) | registerAsset accepts only an asset the registry already knows, so a spoke can never announce a new one.<br>Caught by: [`rcHhRegisterThenReportOnTheAssetIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L459) |
| [6504](#hubhandler-6504) | the request manager gate is inverted, so a request whose network does have a live manager is turned away.<br>Caught by: [`rvHhRequestIsNeverRefusedOnANetworkThatHasAManager`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L185) |
| [6505](#hubhandler-6505) | request refuses a message that carries no body, so a bare notification never reaches the pool's request manager.<br>Caught by: [`rvHhRequestIsNeverRefusedOnANetworkThatHasAManager`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L185) |
| [6506](#hubhandler-6506) | increase values every realized deposit at zero, so an inflow on a live holding adds no value to the books.<br>Caught by: [`rcHhAssetDepositOnALiveHoldingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L52) |
| [6507](#hubhandler-6507) | decrease removes no carrying value for a realized withdrawal, so a reported outflow leaves the holding valued exactly as before.<br>Caught by: [`rcHhAssetWithdrawalOnALiveHoldingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L79) |
| [6508](#hubhandler-6508) | increase refuses flow on a holding the hub never opened, so a spoke report can no longer precede the ledger row.<br>Caught by: [`rcHhAssetReportOnAnUnopenedHoldingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L106) |
| [6509](#hubhandler-6509) | an asset report always leaves the reporting network out of sync, so a spoke can never close its asset batch.<br>Caught by: [`rcHhAssetReportClosingTheBatchIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L129) |
| [6510](#hubhandler-6510) | an asset report that moves nothing is denied the sync marker, so a network reporting no movement can no longer close its batch.<br>Caught by: [`rcHhEmptyAssetBatchClosingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L150) |
| [6511](#hubhandler-6511) | increase books half the flow the spoke reported, so a report can never land on the holding at the size it was sent.<br>Caught by: [`hlHhAssetReportLandsGrossOnItsSide`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L169) |
| [6512](#hubhandler-6512) | setSnapshot refuses the ordering number a network opens its history with, so a network's very first report is turned away.<br>Caught by: [`rcHhFirstAssetReportOfANetworkIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L171) |
| [6513](#hubhandler-6513) | decrease passes the old shortfall state as the new one, so a withdrawal never raises the shortfall count.<br>Caught by: [`rcHhAssetWithdrawalEnteringDeficitIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L188) |
| [6514](#hubhandler-6514) | increase passes the old shortfall state as the new one, so a deposit covering a shortfall never lowers the shortfall count.<br>Caught by: [`rcHhAssetDepositLeavingDeficitIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L211) |
| [6515](#hubhandler-6515) | a reported mint lands on the network's burn counter, so no network can ever raise the shares it reports as issued.<br>Caught by: [`hlHhShareReportLandsOnItsCounter`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L258) |
| [6516](#hubhandler-6516) | a reported burn lands on the network's mint counter, so no network can ever raise the shares it reports as revoked.<br>Caught by: [`hlHhShareReportLandsOnItsCounter`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L258) |
| [6517](#hubhandler-6517) | a revocation books one share fewer than reported on the class total, so class supply stays one share too high.<br>Caught by: [`hlHhShareReportMovesTheClassTotalInStep`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L276) |
| [6518](#hubhandler-6518) | a share report always leaves the reporting network out of sync, so a spoke can never close its share batch.<br>Caught by: [`rcHhShareReportClosingTheBatchIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L234) |
| [6519](#hubhandler-6519) | a share report that moves nothing is denied the sync marker, so a network cannot close its share batch without reporting movement.<br>Caught by: [`rcHhMarkerOnlyShareReportIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L255) |
| [6520](#hubhandler-6520) | the origin leg of a bridge mints instead of burning, so a transfer credits both networks and never debits the network the shares leave.<br>Caught by: [`hlHhTransferDebitsOriginByTheSentAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L23) · [`hlHhTransferSendsTheAmountItMints`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L41) |
| [6521](#hubhandler-6521) | the bridging hook's rewritten size is discarded, so a pool's hook can change everything about a transfer except the number of shares it moves.<br>Caught by: [`rcHhBridgeReachableWithAHookRewritingTheAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L278) |
| [6522](#hubhandler-6522) | the two legs of a bridge are swapped, so the shares are burned on the destination network and minted on the network they were leaving.<br>Caught by: [`rcHhBridgeLeavesAThirdNetworkAloneIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L302) |
| [6523](#hubhandler-6523) | a zero amount transfer returns before sending, so the destination network never hears of it.<br>Caught by: [`hlHhTransferDebitsOriginByTheSentAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L23) · [`hlHhHooklessTransferKeepsTheAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L105) · [`hlHhTransferSendsExactlyOneMessage`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L137) · [`hlHhTransferSendsAnExecuteTransfer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L154) |
| [6524](#hubhandler-6524) | the origin leg burns one share fewer than the transfer moves, so a network's whole position can never leave at once.<br>Caught by: [`rcHhBridgeEmptyingTheOriginNetworkIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L331) |
| [6525](#hubhandler-6525) | a network may no longer report burning more shares than it ever reported receiving, so the per network counters gain a floor they never had.<br>Caught by: [`rcHhBridgeDrivesTheOriginNetworkNegativeIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L353) · [`rcHhShareReportPastTheClassSupplyIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L557) |
| [6526](#hubhandler-6526) | the hub key writes the holdings slot, so the hub reference can never be repointed.<br>Caught by: [`rcHhFileRepointsTheHubIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L380) |
| [6527](#hubhandler-6527) | the holdings key writes the hub slot, so the holdings ledger can never be repointed.<br>Caught by: [`rcHhFileRepointsTheHoldingsLedgerIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L395) |
| [6528](#hubhandler-6528) | the sender key writes the share class manager slot, so the outbound sender can never be repointed.<br>Caught by: [`rcHhFileRepointsTheSenderIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L410) |
| [6529](#hubhandler-6529) | the share class manager key writes the sender slot, so the share class manager can never be repointed.<br>Caught by: [`rcHhFileRepointsTheShareClassBookIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L425) |
| [6530](#hubhandler-6530) | rely clears authority instead of granting it, so no new ward can ever be added to the handler.<br>Caught by: [`rcHhRelyThenDenyRoundTripIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L440) |
| [6531](#hubhandler-6531) | deny grants authority instead of withdrawing it, so a ward once added can never be removed.<br>Caught by: [`rcHhRelyThenDenyRoundTripIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L440) |
| [6532](#hubhandler-6532) | an issuance no longer credits the class total, so a mint and matching burn leave that total lower.<br>Caught by: [`rcHhIssueThenRevokeRestoresTheClassTotalIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L480) |
| [6533](#hubhandler-6533) | the sync marker latches once it is set, so a network that closes a batch can never open the next one.<br>Caught by: [`rcHhSnapshotSetThenClearedIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L503) |
| [6534](#hubhandler-6534) | a share transfer credits the destination one more share than it moves, so a round trip leaves both networks off by one.<br>Caught by: [`rcHhBridgeAndReturnLegIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L526) |
| [8055](#hubhandler-8055) | an asset report is booked under a fixed network instead of the reporting one, so its shortfalls land on the wrong network.<br>Caught by: [`hlHhReportOfAnotherNetworkLeavesTheTrackedCountersAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L502) |
| [8056](#hubhandler-8056) | asset flows are booked under the asset's home network instead of the reporting one, so shortfalls count against the wrong network.<br>Caught by: [`rcHhShortfallLandsOnTheReportingNetworkIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L577) |
| [8310](#hubhandler-8310) | filing the holdings ledger also repoints the hub, so one configuration call rewires two of the handler's dependencies.<br>Caught by: [`hlHhFileWiresOnlyTheNamedSlot`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L395) |
| [8311](#hubhandler-8311) | a share transfer also sends the target network's sync notice, so the snapshot hook hears a sync no report caused.<br>Caught by: [`vtHhSnapshotHookHearsOnlyAReport`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L109) |
| [8312](#hubhandler-8312) | an asset report that closes a network's batch notifies the snapshot hook twice, so the hook publishes the same pool price twice for one batch.<br>Caught by: [`hlHhAssetReportNotifiesTheHookExactlyOnAClosedBatch`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L414) |
| [8313](#hubhandler-8313) | a report that closes a network's batch never reaches the pool's snapshot hook, so the pool price is not republished when the batch is complete.<br>Caught by: [`hlHhSyncNotificationOnlyOnAClosedBatch`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L376) |
| [8314](#hubhandler-8314) | the class shortfall counter moves the wrong way, so the first report putting a class short underflows it and is refused.<br>Caught by: [`rvHhUninitializedAssetReportIsNeverStrandedByTheShortfallTally`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L73) · [`rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L235) |
| [8315](#hubhandler-8315) | revoking past a network's recorded net issuance now reverts, so a transfer out of a network whose report lags is refused.<br>Caught by: [`rvHhHooklessTransferIsNeverStrandedWhileTheCountersHaveRoom`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L130) |
| [8432](#hubhandler-8432) | a transfer books its amount on both class wide counters as well, so the class supply record moves on a bridge although the net stays put.<br>Caught by: [`hlHhTransferLeavesTheClassCountersAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L519) |
| [8433](#hubhandler-8433) | a transfer books its amount as a class wide issuance, so every bridge inflates the class supply.<br>Caught by: [`hlHhTransferConservesTheClassTotal`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L6) · [`hlHhTransferLeavesTheClassCountersAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L519) |
| [8434](#hubhandler-8434) | registerAsset lets a set precision grow, so a spoke can rescale an asset the hub already values at other decimals.<br>Caught by: [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292) |
| [8435](#hubhandler-8435) | registerAsset refuses every repeat again, so a spoke re-announcing a known asset at its own decimals is turned away.<br>Caught by: [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292) |
| [8436](#hubhandler-8436) | registerAsset drops the escape for a zero precision, so an asset first recorded with no decimals can never take its real ones.<br>Caught by: [`rcHhZeroDecimalAssetTakesItsDecimalsLaterIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L624) · [`rcHhZeroPrecisionAssetCanBeCorrectedByARepeatRegistration`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L639) |
| [8437](#hubhandler-8437) | transferShares skips the share class existence check, so a bridge of a class the hub never created goes through.<br>Caught by: [`rvHhTransferRefusesANonWardOrAnUnknownShareClass`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L113) |
| [8438](#hubhandler-8438) | increase narrows the increased amount back to 128 bits, so a report pushing it past that width is refused although the counter has room.<br>Caught by: [`rvHhUninitializedAssetReportIsNeverStrandedByTheShortfallTally`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L73) · [`rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L235) |
| [8439](#hubhandler-8439) | _updateNetwork narrows a network's issued count to 128 bits, so a transfer or report pushing it past that width fails although the counter has room.<br>Caught by: [`rvHhHooklessTransferIsNeverStrandedWhileTheCountersHaveRoom`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L130) · [`rvHhShareReportIsNeverStrandedWhileTheCountersHaveRoom`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L202) |
| [8829](#hubhandler-8829) | a zero valued amount posting is no longer skipped, so a report on an opened holding with no amount account fails although nothing is booked.<br>Caught by: [`rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L235) |
| [8830](#hubhandler-8830) | registerAsset accepts the empty asset id, so a spoke can register an asset under it and every later lookup of that id resolves.<br>Caught by: [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292) |
| [8831](#hubhandler-8831) | a repeat registration keeps the old precision, so an asset first recorded at zero decimals never takes its real ones although the call succeeds.<br>Caught by: [`rcHhZeroPrecisionAssetCanBeCorrectedByARepeatRegistration`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L639) · [`rcHhZeroDecimalAssetTakesItsDecimalsLaterIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L624) |
| [8832](#hubhandler-8832) | the outbound transfer drops the caller's extra gas limit, so a hookless transfer is executed on the target network with no added gas.<br>Caught by: [`hlHhHooklessTransferKeepsTheExtraGasLimit`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L536) |
| [8833](#hubhandler-8833) | the outbound transfer names an empty share class id, so the target network is told to credit shares of a class the hub never moved.<br>Caught by: [`hlHhTransferKeepsThePoolAndClass`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L550) |
| [9062](#hubhandler-9062) | a reported asset move books the raw asset quantity instead of its value, so the ledger drifts from the holding.<br>Caught by: [`stHhReportedAssetMoveIsBookedExactly`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L128) |
| [9063](#hubhandler-9063) | a debit stamps the account with the block number instead of the block time, so its activity time is wrong.<br>Caught by: [`vtHhAccountStampRecordsTheCurrentBlock`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L38) |
| [9085](#hubhandler-9085) | an asset report journals its value in the opposite direction, so a deposit credits the holding's account and debits its counterpart.<br>Caught by: [`hlHhAssetReportJournalsTheRealizedValueOnlyOnAnInitializedHolding`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L434) |

## HubHandler #3104

A network's report flips the snapshot flag without spending that network's nonce, so the same position can be reported twice under one number.

- **Mutant:** [`3104.sol`](3104.sol)
- **Caught by:** [`stHhSnapshotFlagCostsANonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L164)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 3104`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule stHhSnapshotFlagCostsANonce`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -105,7 +105,7 @@
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
         snapshot_.isSnapshot = isSnapshot;
-        snapshot_.nonce++;
+        // MUTATION: the report is recorded without spending the network's ordering number
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
 
```

## HubHandler #3109

A revocation lowers the network's leg without lowering the class total, so the total stops following the legs it is made of.

- **Mutant:** [`3109.sol`](3109.sol)
- **Caught by:** [`stHhShareLedgerMovesWithItsNetworkLegs`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L149)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 3109`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule stHhShareLedgerMovesWithItsNetworkLegs`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        // MUTATION: the class total does not follow the revoked leg
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## HubHandler #3110

A decrease that leaves a holding short no longer updates the shortfall counts, so they stop following the short holdings.

- **Mutant:** [`3110.sol`](3110.sol)
- **Caught by:** [`stHhNetworkDeficitCountFollowsTheShortRows`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L179) · [`stHhClassDeficitCountFollowsTheShortRows`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L194)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 3110`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule stHhNetworkDeficitCountFollowsTheShortRows stHhClassDeficitCountFollowsTheShortRows`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -182,7 +182,8 @@
         amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
 
         holding_.assetAmountValue -= amountValue;
-        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
+        // MUTATION: the count never learns the row went short
+        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, wasDeficit);
 
         emit Decrease(poolId, scId, assetId, amount_, amountValue);
     }
```

## HubHandler #4400

file drops the ward gate, so any caller can repoint the hub, holdings, message sender or share class manager.

- **Mutant:** [`4400.sol`](4400.sol)
- **Caught by:** [`acHhOnlyAWardMovesTheHubPointer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L21) · [`acHhOnlyAWardMovesTheHoldingsPointer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L37) · [`acHhOnlyAWardMovesTheSenderPointer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L53) · [`acHhOnlyAWardMovesTheShareClassManagerPointer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L70)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4400`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/access_control.conf --rule acHhOnlyAWardMovesTheHubPointer acHhOnlyAWardMovesTheHoldingsPointer acHhOnlyAWardMovesTheSenderPointer acHhOnlyAWardMovesTheShareClassManagerPointer`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -48,7 +48,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IHubHandler
-    function file(bytes32 what, address data) external auth {
+    function file(bytes32 what, address data) external { // MUTATION: the wiring switch is open to any caller
         if (what == "hub") hub = IHub(data);
         else if (what == "holdings") holdings = IHoldings(data);
         else if (what == "sender") sender = IHubMessageSender(data);
```

## HubHandler #4401

updateAssets drops the ward gate, so any caller can move holdings, a network's snapshot state and the pool's ledger.

- **Mutant:** [`4401.sol`](4401.sol)
- **Caught by:** [`acHhOnlyAWardMovesADepositHistory`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L121) · [`acHhOnlyAWardMovesAWithdrawalHistory`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L138) · [`acHhOnlyAWardMovesACarriedValue`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L155) · [`acHhOnlyAWardMovesTheDeficitCount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L172) · [`acHhOnlyAWardMovesASyncMarker`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L192) · [`acHhOnlyAWardMovesASnapshotNonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L208) · [`acHhOnlyAWardMovesALedgerDebit`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L278) · [`acHhOnlyAWardMovesALedgerCredit`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L295) · [`acHhOnlyAWardMovesTheJournalCounter`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L312)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4401`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/access_control.conf --rule acHhOnlyAWardMovesADepositHistory acHhOnlyAWardMovesAWithdrawalHistory acHhOnlyAWardMovesACarriedValue acHhOnlyAWardMovesTheDeficitCount acHhOnlyAWardMovesASyncMarker acHhOnlyAWardMovesASnapshotNonce acHhOnlyAWardMovesALedgerDebit acHhOnlyAWardMovesALedgerCredit acHhOnlyAWardMovesTheJournalCounter`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -84,7 +84,7 @@
         bool isIncrease,
         bool isSnapshot,
         uint64 nonce
-    ) external auth {
+    ) external { // MUTATION: an inbound asset report is accepted from any caller
         // The delta is valued at the hub-side valuation; the journaled value mirrors the holding
         // mutation exactly, so the accounts stay in sync with the holding.
         uint128 value = isIncrease
```

## HubHandler #4402

updateShares drops the ward gate, so any caller can move a network's minted and burned totals and the supply of the share class.

- **Mutant:** [`4402.sol`](4402.sol)
- **Caught by:** [`acHhOnlyAWardMovesANetworkIssuedTotal`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L225) · [`acHhOnlyAWardMovesANetworkRevokedTotal`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L242) · [`acHhOnlyAWardMovesTheClassSupply`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L259)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4402`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/access_control.conf --rule acHhOnlyAWardMovesANetworkIssuedTotal acHhOnlyAWardMovesANetworkRevokedTotal acHhOnlyAWardMovesTheClassSupply`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -107,7 +107,7 @@
         bool isIssuance,
         bool isSnapshot,
         uint64 nonce
-    ) external auth {
+    ) external { // MUTATION: an inbound share report is accepted from any caller
         shareClassManager.updateShares(centrifugeId, poolId, scId, amount, isIssuance);
 
         holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
```

## HubHandler #4403

registerAsset drops the ward gate, so any caller can onboard an asset id and fix the precision every later price conversion reads.

- **Mutant:** [`4403.sol`](4403.sol)
- **Caught by:** [`acHhOnlyAWardRegistersAnAsset`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L87) · [`acHhOnlyAWardMovesAnAssetDecimals`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L104)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4403`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/access_control.conf --rule acHhOnlyAWardRegistersAnAsset acHhOnlyAWardMovesAnAssetDecimals`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -62,7 +62,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IHubGatewayHandler
-    function registerAsset(AssetId assetId, uint8 decimals) external auth {
+    function registerAsset(AssetId assetId, uint8 decimals) external { // MUTATION: onboarding is open to any caller
         hubRegistry.registerAsset(assetId, decimals);
     }
 
```

## HubHandler #4404

request drops the ward gate, so any caller can drive an investor order into the pool's registered request manager.

- **Mutant:** [`4404.sol`](4404.sol)
- **Caught by:** [`acHhOnlyAWardForwardsAnInvestorRequest`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L329)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4404`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/access_control.conf --rule acHhOnlyAWardForwardsAnInvestorRequest`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -67,7 +67,7 @@
     }
 
     /// @inheritdoc IHubGatewayHandler
-    function request(PoolId poolId, ShareClassId scId, AssetId assetId, bytes calldata payload) external auth {
+    function request(PoolId poolId, ShareClassId scId, AssetId assetId, bytes calldata payload) external { // MUTATION: forwarding is open to any caller
         IHubRequestManager manager = hubRegistry.hubRequestManager(poolId, assetId.centrifugeId());
         require(address(manager) != address(0), InvalidRequestManager());
 
```

## HubHandler #4405

initiateTransferShares drops the ward gate, so any caller can have the hub announce a share transfer to another network.

- **Mutant:** [`4405.sol`](4405.sol)
- **Caught by:** [`acHhOnlyAWardSendsAnOutboundMessage`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L346)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4405`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/access_control.conf --rule acHhOnlyAWardSendsAnOutboundMessage`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -124,7 +124,7 @@
         uint128 amount,
         uint128 extraGasLimit,
         address refund
-    ) external payable auth {
+    ) external payable { // MUTATION: an outbound transfer is accepted from any caller
         IBridgingHook hook = hubRegistry.bridgingHook(poolId);
         if (address(hook) != address(0)) {
             BridgeSharesResult memory result = hook.onBridgeShares(
```

## HubHandler #4406

rely drops the ward gate, so any caller can add an address to the roll that feeds the hub its cross chain traffic.

- **Mutant:** [`4406.sol`](4406.sol)
- **Caught by:** [`acHhOnlyAWardMovesTheWardSet`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4406`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/access_control.conf --rule acHhOnlyAWardMovesTheWardSet`

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

## HubHandler #4410

updateShares books a revocation as an issuance on the class total, so a revocation report inflates the class supply.

- **Mutant:** [`4410.sol`](4410.sol)
- **Caught by:** [`hlHhShareReportMovesTheClassTotalInStep`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L276)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4410`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhShareReportMovesTheClassTotalInStep`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        else total.issuances += amount; // MUTATION: a revocation adds to the class total
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## HubHandler #4411

_updateNetwork drops the per-network issuance write, so share reports and transfer mints never reach that network's issued total.

- **Mutant:** [`4411.sol`](4411.sol)
- **Caught by:** [`hlHhShareReportLandsOnItsCounter`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L258) · [`hlHhTransferSendsTheAmountItMints`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4411`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhShareReportLandsOnItsCounter hlHhTransferSendsTheAmountItMints`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -160,7 +160,7 @@
         bool wasNegative = ipn.revocations > ipn.issuances;
 
         if (isIssuance) {
-            ipn.issuances += amount;
+            // ipn.issuances += amount; // MUTATION: removed per-network issuance write
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## HubHandler #4412

the outbound transfer message announces one share more than the ledgers move, so it overstates the amount sent.

- **Mutant:** [`4412.sol`](4412.sol)
- **Caught by:** [`hlHhTransferDebitsOriginByTheSentAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L23) · [`hlHhHooklessTransferKeepsTheAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L105)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4412`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhTransferDebitsOriginByTheSentAmount hlHhHooklessTransferKeepsTheAmount`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -151,7 +151,8 @@
         emit ForwardTransferShares(originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount);
 
         return sender.sendExecuteTransferShares{value: msg.value}(
-            originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund
+            // MUTATION: the announced size is one over the size the legs moved
+            originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount + 1, extraGasLimit, refund
         );
     }
 }
```

## HubHandler #4413

the outbound transfer message swaps origin and target networks, so the burn and the mint are announced on the wrong chains.

- **Mutant:** [`4413.sol`](4413.sol)
- **Caught by:** [`hlHhTransferKeepsTheOriginNetwork`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L59) · [`hlHhTransferKeepsTheTargetNetwork`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L74)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4413`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhTransferKeepsTheOriginNetwork hlHhTransferKeepsTheTargetNetwork`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -151,7 +151,8 @@
         emit ForwardTransferShares(originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount);
 
         return sender.sendExecuteTransferShares{value: msg.value}(
-            originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund
+            // MUTATION: the two networks are announced the wrong way round
+            targetCentrifugeId, originCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund
         );
     }
 }
```

## HubHandler #4414

the outbound execute transfer names the sending party as the recipient, so the shares are handed to the wrong account on the target network.

- **Mutant:** [`4414.sol`](4414.sol)
- **Caught by:** [`hlHhHooklessTransferKeepsTheReceiver`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L89)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4414`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhHooklessTransferKeepsTheReceiver`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -151,7 +151,8 @@
         emit ForwardTransferShares(originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount);
 
         return sender.sendExecuteTransferShares{value: msg.value}(
-            originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund
+            // MUTATION: the sending party is announced as the recipient
+            originCentrifugeId, targetCentrifugeId, poolId, scId, sender_, amount, extraGasLimit, refund
         );
     }
 }
```

## HubHandler #4415

the outbound execute transfer drops the caller's refund address, so the unspent gas payment no longer returns where the caller sent it.

- **Mutant:** [`4415.sol`](4415.sol)
- **Caught by:** [`hlHhHooklessTransferKeepsTheRefund`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4415`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhHooklessTransferKeepsTheRefund`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -151,7 +151,8 @@
         emit ForwardTransferShares(originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount);
 
         return sender.sendExecuteTransferShares{value: msg.value}(
-            originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund
+            // MUTATION: the refund address the caller gave is dropped
+            originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, address(0)
         );
     }
 }
```

## HubHandler #4416

a zero sized transfer updates the hub ledgers but sends no message, so the destination network never hears of it.

- **Mutant:** [`4416.sol`](4416.sol)
- **Caught by:** [`hlHhTransferSendsExactlyOneMessage`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L137) · [`hlHhTransferSendsAnExecuteTransfer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L154)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4416`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhTransferSendsExactlyOneMessage hlHhTransferSendsAnExecuteTransfer`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -150,6 +150,9 @@
 
         emit ForwardTransferShares(originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount);
 
+        // MUTATION: a zero sized transfer is settled locally and never announced
+        if (amount == 0) return;
+
         return sender.sendExecuteTransferShares{value: msg.value}(
             originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund
         );
```

## HubHandler #4417

an asset report's deposit lands on the next asset id, so a neighbouring holding grows instead of the reported one.

- **Mutant:** [`4417.sol`](4417.sol)
- **Caught by:** [`hlHhAssetReportLandsGrossOnItsSide`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L169) · [`hlHhAssetReportLeavesOtherIncreasesAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L207) · [`hlHhAssetReportLeavesOtherValuesAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L241)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4417`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhAssetReportLandsGrossOnItsSide hlHhAssetReportLeavesOtherIncreasesAlone hlHhAssetReportLeavesOtherValuesAlone`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -88,7 +88,8 @@
         // The delta is valued at the hub-side valuation; the journaled value mirrors the holding
         // mutation exactly, so the accounts stay in sync with the holding.
         uint128 value = isIncrease
-            ? holdings.increase(poolId, scId, assetId, centrifugeId, amount)
+            // MUTATION: the deposit lands one asset id past the reported holding
+            ? holdings.increase(poolId, scId, AssetId.wrap(assetId.raw() + 1), centrifugeId, amount)
             : holdings.decrease(poolId, scId, assetId, centrifugeId, amount);
 
         if (holdings.isInitialized(poolId, scId, assetId)) {
```

## HubHandler #4418

an asset report's withdrawal is booked on the next asset id, so a bystander holding's outflow moves instead.

- **Mutant:** [`4418.sol`](4418.sol)
- **Caught by:** [`hlHhAssetReportLeavesOtherDecreasesAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L224)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4418`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhAssetReportLeavesOtherDecreasesAlone`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -89,7 +89,8 @@
         // mutation exactly, so the accounts stay in sync with the holding.
         uint128 value = isIncrease
             ? holdings.increase(poolId, scId, assetId, centrifugeId, amount)
-            : holdings.decrease(poolId, scId, assetId, centrifugeId, amount);
+            // MUTATION: the withdrawal lands one asset id past the reported holding
+            : holdings.decrease(poolId, scId, AssetId.wrap(assetId.raw() + 1), centrifugeId, amount);
 
         if (holdings.isInitialized(poolId, scId, assetId)) {
             hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, value);
```

## HubHandler #4419

increase also nets the deposit against the outstanding withdrawal, so an inflow report shrinks the outflow total.

- **Mutant:** [`4419.sol`](4419.sol)
- **Caught by:** [`hlHhAssetReportLeavesTheOppositeSideAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4419`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhAssetReportLeavesTheOppositeSideAlone`

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

## HubHandler #4420

a request with an empty body is dropped instead of forwarded, so the registered manager never receives it.

- **Mutant:** [`4420.sol`](4420.sol)
- **Caught by:** [`hlHhRequestForwardsExactlyOnce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L292) · [`hlHhRequestReachesTheRegisteredManager`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L307) · [`hlHhRequestForwardsThePool`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L322) · [`hlHhRequestForwardsTheShareClass`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L335) · [`hlHhRequestForwardsTheAsset`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L348) · [`hlHhRequestForwardsThePayload`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L361)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4420`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhRequestForwardsExactlyOnce hlHhRequestReachesTheRegisteredManager hlHhRequestForwardsThePool hlHhRequestForwardsTheShareClass hlHhRequestForwardsTheAsset hlHhRequestForwardsThePayload`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -71,7 +71,8 @@
         IHubRequestManager manager = hubRegistry.hubRequestManager(poolId, assetId.centrifugeId());
         require(address(manager) != address(0), InvalidRequestManager());
 
-        IHubRequestManager(manager).request(poolId, scId, assetId, payload);
+        // MUTATION: a request carrying an empty body is dropped instead of forwarded
+        if (payload.length != 0) IHubRequestManager(manager).request(poolId, scId, assetId, payload);
     }
 
     /// @inheritdoc IHubGatewayHandler
```

## HubHandler #4430

file no longer reverts on an unknown parameter name, so a mistyped rewiring silently succeeds and changes nothing.

- **Mutant:** [`4430.sol`](4430.sol)
- **Caught by:** [`rvHhFileRefusesANonWardOrAnUnknownName`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4430`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhFileRefusesANonWardOrAnUnknownName`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -53,7 +53,7 @@
         else if (what == "holdings") holdings = IHoldings(data);
         else if (what == "sender") sender = IHubMessageSender(data);
         else if (what == "shareClassManager") shareClassManager = IShareClassManager(data);
-        else revert FileUnrecognizedParam();
+        // MUTATION: an undocumented parameter is accepted and quietly changes nothing
         emit File(what, data);
     }
 
```

## HubHandler #4431

registerAsset drops the eighteen decimal cap, so a registration the handler must refuse for oversized precision goes through.

- **Mutant:** [`4431.sol`](4431.sol)
- **Caught by:** [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4431`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -46,7 +46,7 @@
     /// @inheritdoc IHubRegistry
     function registerAsset(AssetId assetId, uint8 decimals_) external auth {
         require(!assetId.isNull(), EmptyAssetId());
-        require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
+        // MUTATION: removed the 18-decimal cap check
 
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
```

## HubHandler #4433

updateShares skips the share class existence check, so share reports go through on an unknown class.

- **Mutant:** [`4433.sol`](4433.sol)
- **Caught by:** [`rvHhUpdateSharesRefusesANonWardAnUnknownClassOrAMissedNonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4433`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhUpdateSharesRefusesANonWardAnUnknownClassOrAMissedNonce`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -92,7 +92,7 @@
         external
         auth
     {
-        require(exists(poolId, scId_), ShareClassNotFound());
+        // require(exists(poolId, scId_), ShareClassNotFound()); // MUTATION: removed share class existence check
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
```

## HubHandler #4434

setSnapshot accepts any ordering number at or below the one it holds, so a replayed or reordered report is no longer turned away.

- **Mutant:** [`4434.sol`](4434.sol)
- **Caught by:** [`rvHhUpdateAssetsRefusesANonWardOrAMissedNonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L55) · [`rvHhUpdateSharesRefusesANonWardAnUnknownClassOrAMissedNonce`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4434`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhUpdateAssetsRefusesANonWardOrAMissedNonce rvHhUpdateSharesRefusesANonWardAnUnknownClassOrAMissedNonce`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -102,7 +102,7 @@
         auth
     {
         Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
-        require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
+        require(snapshot_.nonce >= nonce, InvalidNonce(snapshot_.nonce, nonce)); // MUTATION: a stale ordering number is accepted
 
         snapshot_.isSnapshot = isSnapshot;
         snapshot_.nonce++;
```

## HubHandler #4435

rely drops the ward gate, so granting the handler's ward succeeds for a caller that holds none.

- **Mutant:** [`4435.sol`](4435.sol)
- **Caught by:** [`rvHhRelyRefusesANonWard`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L159)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4435`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhRelyRefusesANonWard`

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

## HubHandler #4436

deny drops the ward gate, so revoking the handler's ward succeeds for a caller that holds none.

- **Mutant:** [`4436.sol`](4436.sol)
- **Caught by:** [`rvHhDenyRefusesANonWard`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L172)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4436`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhDenyRefusesANonWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -28,7 +28,7 @@
     }
 
     /// @inheritdoc IAuth
-    function deny(address user) public auth {
+    function deny(address user) public { // MUTATION: the ward roll is trimmed by any caller
         wards[user] = 0;
         emit Deny(user);
     }
```

## HubHandler #4437

the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.

- **Mutant:** [`4437.sol`](4437.sol)
- **Caught by:** [`rvHhRequestRefusesANonWardOrANetworkWithNoManager`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L20) · [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4437`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhRequestRefusesANonWardOrANetworkWithNoManager rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`

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

## HubHandler #4440

setSnapshot advances a network's ordering number by two, so the snapshot sequence skips a step on a single report.

- **Mutant:** [`4440.sol`](4440.sol)
- **Caught by:** [`vtHhSnapshotSequenceStepsByAtMostOne`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4440`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule vtHhSnapshotSequenceStepsByAtMostOne`

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

## HubHandler #4441

the pool's journal counter advances by two, so the journal numbering skips an id on every entry the handler drives.

- **Mutant:** [`4441.sol`](4441.sol)
- **Caught by:** [`vtHhJournalSequenceStepsByAtMostOne`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4441`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule vtHhJournalSequenceStepsByAtMostOne`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -155,6 +155,8 @@
     }
 
     function _generateJournalId(PoolId poolId) internal returns (uint256) {
-        return uint256((uint256(poolId.raw()) << 128) | ++_poolJournalIdCounter[poolId]);
+        // MUTATION: the journal numbering advances by two and skips an id
+        _poolJournalIdCounter[poolId] += 2;
+        return uint256((uint256(poolId.raw()) << 128) | _poolJournalIdCounter[poolId]);
     }
 }
```

## HubHandler #4443

increase also nets the deposit against the recorded withdrawals, so a holding's outflow history shrinks on an inbound report.

- **Mutant:** [`4443.sol`](4443.sol)
- **Caught by:** [`vtHhHoldingFlowHistoryNeverShrinks`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L55)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4443`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule vtHhHoldingFlowHistoryNeverShrinks`

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

## HubHandler #4444

a network's minted total is overwritten by the reported amount instead of accumulated, so the record of what a chain has minted can shrink.

- **Mutant:** [`4444.sol`](4444.sol)
- **Caught by:** [`vtHhNetworkShareHistoryNeverShrinks`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L73)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4444`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule vtHhNetworkShareHistoryNeverShrinks`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -160,7 +160,7 @@
         bool wasNegative = ipn.revocations > ipn.issuances;
 
         if (isIssuance) {
-            ipn.issuances += amount;
+            ipn.issuances = amount; // MUTATION: the minted total is overwritten instead of accumulated
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## HubHandler #4445

a debit overwrites the account's running debit total instead of accumulating into it, so a ledger row's posted history can shrink.

- **Mutant:** [`4445.sol`](4445.sol)
- **Caught by:** [`vtHhLedgerRowTotalsNeverShrink`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L91)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4445`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule vtHhLedgerRowTotalsNeverShrink`

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

## HubHandler #4448

updateAssets moves the holding's value but posts zero to the ledger, so the holdings and the pool's books drift apart.

- **Mutant:** [`4448.sol`](4448.sol)
- **Caught by:** [`postedDebitsCoverCarriedValue`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_valid_state.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 4448`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/valid_state.conf --rule postedDebitsCoverCarriedValue`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -92,7 +92,7 @@
             : holdings.decrease(poolId, scId, assetId, centrifugeId, amount);
 
         if (holdings.isInitialized(poolId, scId, assetId)) {
-            hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, value);
+            hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, 0); // MUTATION: the carried value is booked on the holding but posted to the ledger as nothing
         }
 
         holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
```

## HubHandler #6500

registerAsset stores the announced asset row without its live flag, so an asset the spoke announced never reads as registered.

- **Mutant:** [`6500.sol`](6500.sol)
- **Caught by:** [`rcHhRegisterAssetIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6500`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhRegisterAssetIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -51,7 +51,7 @@
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
 
-        asset[assetId] = AssetInfo(true, decimals_);
+        asset[assetId] = AssetInfo(false, decimals_); // MUTATION: the row is stored without its live flag
 
         emit NewAsset(assetId, decimals_);
     }
```

## HubHandler #6501

registerAsset refuses the highest precision it documents as accepted, so an asset declaring eighteen decimals can no longer be onboarded.

- **Mutant:** [`6501.sol`](6501.sol)
- **Caught by:** [`rcHhRegisterAssetAtTheDecimalsCeilingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L20)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6501`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhRegisterAssetAtTheDecimalsCeilingIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -46,7 +46,7 @@
     /// @inheritdoc IHubRegistry
     function registerAsset(AssetId assetId, uint8 decimals_) external auth {
         require(!assetId.isNull(), EmptyAssetId());
-        require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
+        require(decimals_ < MAX_DECIMALS, TooManyDecimals()); // MUTATION: the ceiling itself is refused
 
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
```

## HubHandler #6502

registerAsset refuses an announcement that carries no decimals at all, so the floor of the accepted range is closed.

- **Mutant:** [`6502.sol`](6502.sol)
- **Caught by:** [`rcHhRegisterAssetAtZeroDecimalsIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6502`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhRegisterAssetAtZeroDecimalsIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -47,6 +47,7 @@
     function registerAsset(AssetId assetId, uint8 decimals_) external auth {
         require(!assetId.isNull(), EmptyAssetId());
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
+        require(decimals_ != 0, TooManyDecimals()); // MUTATION: an announcement carrying no decimals is refused
 
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
```

## HubHandler #6503

registerAsset accepts only an asset the registry already knows, so a spoke can never announce a new one.

- **Mutant:** [`6503.sol`](6503.sol)
- **Caught by:** [`rcHhRegisterThenReportOnTheAssetIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L459)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6503`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhRegisterThenReportOnTheAssetIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -49,7 +49,7 @@
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        require(current.registered && (current.decimals == 0 || current.decimals == decimals_), CannotChangeDecimals()); // MUTATION: only an already known asset may be announced
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubHandler #6504

the request manager gate is inverted, so a request whose network does have a live manager is turned away.

- **Mutant:** [`6504.sol`](6504.sol)
- **Caught by:** [`rvHhRequestIsNeverRefusedOnANetworkThatHasAManager`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L185)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6504`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhRequestIsNeverRefusedOnANetworkThatHasAManager`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -69,7 +69,7 @@
     /// @inheritdoc IHubGatewayHandler
     function request(PoolId poolId, ShareClassId scId, AssetId assetId, bytes calldata payload) external auth {
         IHubRequestManager manager = hubRegistry.hubRequestManager(poolId, assetId.centrifugeId());
-        require(address(manager) != address(0), InvalidRequestManager());
+        require(address(manager) == address(0), InvalidRequestManager()); // MUTATION: inverted manager gate
 
         IHubRequestManager(manager).request(poolId, scId, assetId, payload);
     }
```

## HubHandler #6505

request refuses a message that carries no body, so a bare notification never reaches the pool's request manager.

- **Mutant:** [`6505.sol`](6505.sol)
- **Caught by:** [`rvHhRequestIsNeverRefusedOnANetworkThatHasAManager`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L185)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6505`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhRequestIsNeverRefusedOnANetworkThatHasAManager`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -69,7 +69,7 @@
     /// @inheritdoc IHubGatewayHandler
     function request(PoolId poolId, ShareClassId scId, AssetId assetId, bytes calldata payload) external auth {
         IHubRequestManager manager = hubRegistry.hubRequestManager(poolId, assetId.centrifugeId());
-        require(address(manager) != address(0), InvalidRequestManager());
+        require(address(manager) != address(0) && payload.length != 0, InvalidRequestManager()); // MUTATION: a request with no body is refused
 
         IHubRequestManager(manager).request(poolId, scId, assetId, payload);
     }
```

## HubHandler #6506

increase values every realized deposit at zero, so an inflow on a live holding adds no value to the books.

- **Mutant:** [`6506.sol`](6506.sol)
- **Caught by:** [`rcHhAssetDepositOnALiveHoldingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L52)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6506`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhAssetDepositOnALiveHoldingIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -151,9 +151,7 @@
 
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
         // valuation. Uninitialized holdings track amount only; their value is established at initialization.
-        amountValue = realized != 0 && address(holding_.valuation) != address(0)
-            ? holding_.valuation.getQuote(poolId, scId, assetId, realized)
-            : 0;
+        amountValue = 0; // MUTATION: a realized increase is valued at nothing
 
         holding_.assetAmountValue += amountValue;
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
```

## HubHandler #6507

decrease removes no carrying value for a realized withdrawal, so a reported outflow leaves the holding valued exactly as before.

- **Mutant:** [`6507.sol`](6507.sol)
- **Caught by:** [`rcHhAssetWithdrawalOnALiveHoldingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L79)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6507`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhAssetWithdrawalOnALiveHoldingIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -179,7 +179,7 @@
         // storage mutation and can never over-journal. Deliberately NOT a live oracle quote like increase():
         // pro-rata preserves `amount == 0 => value == 0`, which a live quote would break when the price has
         // moved since the last update() (a full drain would leave residual value behind).
-        amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
+        amountValue = 0; // MUTATION: a realized decrease removes no carrying value
 
         holding_.assetAmountValue -= amountValue;
         _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
```

## HubHandler #6508

increase refuses flow on a holding the hub never opened, so a spoke report can no longer precede the ledger row.

- **Mutant:** [`6508.sol`](6508.sol)
- **Caught by:** [`rcHhAssetReportOnAnUnopenedHoldingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L106)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6508`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhAssetReportOnAnUnopenedHoldingIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -143,6 +143,7 @@
         returns (uint128 amountValue)
     {
         Holding storage holding_ = _holding[poolId][scId][assetId];
+        require(address(holding_.valuation) != address(0), HoldingNotFound()); // MUTATION: flow is refused on a holding the hub never opened
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
```

## HubHandler #6509

an asset report always leaves the reporting network out of sync, so a spoke can never close its asset batch.

- **Mutant:** [`6509.sol`](6509.sol)
- **Caught by:** [`rcHhAssetReportClosingTheBatchIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6509`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhAssetReportClosingTheBatchIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -95,7 +95,7 @@
             hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, value);
         }
 
-        holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
+        holdings.setSnapshot(poolId, scId, centrifugeId, false, nonce); // MUTATION: an asset report never marks the batch closed
     }
 
     /// @inheritdoc IHubGatewayHandler
```

## HubHandler #6510

an asset report that moves nothing is denied the sync marker, so a network reporting no movement can no longer close its batch.

- **Mutant:** [`6510.sol`](6510.sol)
- **Caught by:** [`rcHhEmptyAssetBatchClosingIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L150)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6510`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhEmptyAssetBatchClosingIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -95,7 +95,7 @@
             hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, value);
         }
 
-        holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
+        holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot && amount != 0, nonce); // MUTATION: a report that moves nothing cannot close the batch
     }
 
     /// @inheritdoc IHubGatewayHandler
```

## HubHandler #6511

increase books half the flow the spoke reported, so a report can never land on the holding at the size it was sent.

- **Mutant:** [`6511.sol`](6511.sol)
- **Caught by:** [`hlHhAssetReportLandsGrossOnItsSide`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L169)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6511`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhAssetReportLandsGrossOnItsSide`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -146,7 +146,7 @@
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
-        holding_.increasedAmount += amount_;
+        holding_.increasedAmount += amount_ / 2; // MUTATION: half the reported flow is booked
         uint128 realized = (_amount(holding_) - oldAmount).toUint128();
 
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
```

## HubHandler #6512

setSnapshot refuses the ordering number a network opens its history with, so a network's very first report is turned away.

- **Mutant:** [`6512.sol`](6512.sol)
- **Caught by:** [`rcHhFirstAssetReportOfANetworkIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L171)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6512`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhFirstAssetReportOfANetworkIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -102,7 +102,7 @@
         auth
     {
         Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
-        require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
+        require(snapshot_.nonce == nonce && nonce != 0, InvalidNonce(snapshot_.nonce, nonce)); // MUTATION: a network opening report is refused
 
         snapshot_.isSnapshot = isSnapshot;
         snapshot_.nonce++;
```

## HubHandler #6513

decrease passes the old shortfall state as the new one, so a withdrawal never raises the shortfall count.

- **Mutant:** [`6513.sol`](6513.sol)
- **Caught by:** [`rcHhAssetWithdrawalEnteringDeficitIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6513`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhAssetWithdrawalEnteringDeficitIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -182,7 +182,7 @@
         amountValue = oldAmount == 0 ? 0 : (uint256(holding_.assetAmountValue) * removedAmount / oldAmount).toUint128();
 
         holding_.assetAmountValue -= amountValue;
-        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
+        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, wasDeficit); // MUTATION: a withdrawal never reports a new shortfall
 
         emit Decrease(poolId, scId, assetId, amount_, amountValue);
     }
```

## HubHandler #6514

increase passes the old shortfall state as the new one, so a deposit covering a shortfall never lowers the shortfall count.

- **Mutant:** [`6514.sol`](6514.sol)
- **Caught by:** [`rcHhAssetDepositLeavingDeficitIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L211)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6514`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhAssetDepositLeavingDeficitIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -156,7 +156,7 @@
             : 0;
 
         holding_.assetAmountValue += amountValue;
-        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, holding_.decreasedAmount > holding_.increasedAmount);
+        _updateDeficit(poolId, scId, centrifugeId, wasDeficit, wasDeficit); // MUTATION: a deposit never clears a shortfall
 
         emit Increase(poolId, scId, assetId, amount_, amountValue);
     }
```

## HubHandler #6515

a reported mint lands on the network's burn counter, so no network can ever raise the shares it reports as issued.

- **Mutant:** [`6515.sol`](6515.sol)
- **Caught by:** [`hlHhShareReportLandsOnItsCounter`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L258)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6515`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhShareReportLandsOnItsCounter`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -160,7 +160,7 @@
         bool wasNegative = ipn.revocations > ipn.issuances;
 
         if (isIssuance) {
-            ipn.issuances += amount;
+            ipn.revocations += amount; // MUTATION: a reported mint lands on the burn counter
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## HubHandler #6516

a reported burn lands on the network's mint counter, so no network can ever raise the shares it reports as revoked.

- **Mutant:** [`6516.sol`](6516.sol)
- **Caught by:** [`hlHhShareReportLandsOnItsCounter`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L258)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6516`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhShareReportLandsOnItsCounter`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -163,7 +163,7 @@
             ipn.issuances += amount;
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
-            ipn.revocations += amount;
+            ipn.issuances += amount; // MUTATION: a reported burn lands on the mint counter
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
 
```

## HubHandler #6517

a revocation books one share fewer than reported on the class total, so class supply stays one share too high.

- **Mutant:** [`6517.sol`](6517.sol)
- **Caught by:** [`hlHhShareReportMovesTheClassTotalInStep`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L276)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6517`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhShareReportMovesTheClassTotalInStep`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        else total.revocations += amount - 1; // MUTATION: one share is always left behind
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## HubHandler #6518

a share report always leaves the reporting network out of sync, so a spoke can never close its share batch.

- **Mutant:** [`6518.sol`](6518.sol)
- **Caught by:** [`rcHhShareReportClosingTheBatchIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L234)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6518`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhShareReportClosingTheBatchIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -110,7 +110,7 @@
     ) external auth {
         shareClassManager.updateShares(centrifugeId, poolId, scId, amount, isIssuance);
 
-        holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
+        holdings.setSnapshot(poolId, scId, centrifugeId, false, nonce); // MUTATION: a share report never marks the batch closed
     }
 
     /// @inheritdoc IHubGatewayHandler
```

## HubHandler #6519

a share report that moves nothing is denied the sync marker, so a network cannot close its share batch without reporting movement.

- **Mutant:** [`6519.sol`](6519.sol)
- **Caught by:** [`rcHhMarkerOnlyShareReportIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L255)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6519`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhMarkerOnlyShareReportIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -110,7 +110,7 @@
     ) external auth {
         shareClassManager.updateShares(centrifugeId, poolId, scId, amount, isIssuance);
 
-        holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
+        holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot && amount != 0, nonce); // MUTATION: a share report that moves nothing cannot close the batch
     }
 
     /// @inheritdoc IHubGatewayHandler
```

## HubHandler #6520

the origin leg of a bridge mints instead of burning, so a transfer credits both networks and never debits the network the shares leave.

- **Mutant:** [`6520.sol`](6520.sol)
- **Caught by:** [`hlHhTransferDebitsOriginByTheSentAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L23) · [`hlHhTransferSendsTheAmountItMints`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6520`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhTransferDebitsOriginByTheSentAmount hlHhTransferSendsTheAmountItMints`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -111,7 +111,7 @@
     ) external auth {
         require(exists(poolId, scId_), ShareClassNotFound());
 
-        _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
+        _updateNetwork(poolId, scId_, fromCentrifugeId, amount, true); // MUTATION: the origin leg mints instead of burning
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
     }
 
```

## HubHandler #6521

the bridging hook's rewritten size is discarded, so a pool's hook can change everything about a transfer except the number of shares it moves.

- **Mutant:** [`6521.sol`](6521.sol)
- **Caught by:** [`rcHhBridgeReachableWithAHookRewritingTheAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L278)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6521`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhBridgeReachableWithAHookRewritingTheAmount`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -140,8 +140,8 @@
                     refund: refund
                 })
             );
-            (receiver, amount, extraGasLimit, refund) =
-            (result.receiver, result.amount, result.extraGasLimit, result.refund);
+            (receiver, extraGasLimit, refund) = // MUTATION: the hook's rewritten amount is discarded
+            (result.receiver, result.extraGasLimit, result.refund);
         }
 
         shareClassManager.transferShares(poolId, scId, originCentrifugeId, targetCentrifugeId, amount);
```

## HubHandler #6522

the two legs of a bridge are swapped, so the shares are burned on the destination network and minted on the network they were leaving.

- **Mutant:** [`6522.sol`](6522.sol)
- **Caught by:** [`rcHhBridgeLeavesAThirdNetworkAloneIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L302)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6522`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhBridgeLeavesAThirdNetworkAloneIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -144,7 +144,7 @@
             (result.receiver, result.amount, result.extraGasLimit, result.refund);
         }
 
-        shareClassManager.transferShares(poolId, scId, originCentrifugeId, targetCentrifugeId, amount);
+        shareClassManager.transferShares(poolId, scId, targetCentrifugeId, originCentrifugeId, amount); // MUTATION: the two legs are swapped
 
         holdings.callOnTransferSnapshot(poolId, scId, originCentrifugeId, targetCentrifugeId, amount);
 
```

## HubHandler #6523

a zero amount transfer returns before sending, so the destination network never hears of it.

- **Mutant:** [`6523.sol`](6523.sol)
- **Caught by:** [`hlHhTransferDebitsOriginByTheSentAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L23) · [`hlHhHooklessTransferKeepsTheAmount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L105) · [`hlHhTransferSendsExactlyOneMessage`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L137) · [`hlHhTransferSendsAnExecuteTransfer`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L154)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6523`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhTransferDebitsOriginByTheSentAmount hlHhHooklessTransferKeepsTheAmount hlHhTransferSendsExactlyOneMessage hlHhTransferSendsAnExecuteTransfer`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -150,6 +150,7 @@
 
         emit ForwardTransferShares(originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount);
 
+        if (amount == 0) return; // MUTATION: a transfer of nothing is settled but never announced
         return sender.sendExecuteTransferShares{value: msg.value}(
             originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund
         );
```

## HubHandler #6524

the origin leg burns one share fewer than the transfer moves, so a network's whole position can never leave at once.

- **Mutant:** [`6524.sol`](6524.sol)
- **Caught by:** [`rcHhBridgeEmptyingTheOriginNetworkIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L331)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6524`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhBridgeEmptyingTheOriginNetworkIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -111,7 +111,7 @@
     ) external auth {
         require(exists(poolId, scId_), ShareClassNotFound());
 
-        _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
+        _updateNetwork(poolId, scId_, fromCentrifugeId, amount - 1, false); // MUTATION: the origin leg burns one short of what leaves
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
     }
 
```

## HubHandler #6525

a network may no longer report burning more shares than it ever reported receiving, so the per network counters gain a floor they never had.

- **Mutant:** [`6525.sol`](6525.sol)
- **Caught by:** [`rcHhBridgeDrivesTheOriginNetworkNegativeIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L353) · [`rcHhShareReportPastTheClassSupplyIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L557)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6525`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhBridgeDrivesTheOriginNetworkNegativeIsReachable rcHhShareReportPastTheClassSupplyIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -163,6 +163,7 @@
             ipn.issuances += amount;
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
+            require(amount <= ipn.issuances - ipn.revocations, NegativeIssuance()); // MUTATION: a network may not burn past what it received
             ipn.revocations += amount;
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
```

## HubHandler #6526

the hub key writes the holdings slot, so the hub reference can never be repointed.

- **Mutant:** [`6526.sol`](6526.sol)
- **Caught by:** [`rcHhFileRepointsTheHubIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L380)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6526`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhFileRepointsTheHubIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -49,7 +49,7 @@
 
     /// @inheritdoc IHubHandler
     function file(bytes32 what, address data) external auth {
-        if (what == "hub") hub = IHub(data);
+        if (what == "hub") holdings = IHoldings(data); // MUTATION: the hub key writes the holdings slot
         else if (what == "holdings") holdings = IHoldings(data);
         else if (what == "sender") sender = IHubMessageSender(data);
         else if (what == "shareClassManager") shareClassManager = IShareClassManager(data);
```

## HubHandler #6527

the holdings key writes the hub slot, so the holdings ledger can never be repointed.

- **Mutant:** [`6527.sol`](6527.sol)
- **Caught by:** [`rcHhFileRepointsTheHoldingsLedgerIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L395)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6527`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhFileRepointsTheHoldingsLedgerIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -50,7 +50,7 @@
     /// @inheritdoc IHubHandler
     function file(bytes32 what, address data) external auth {
         if (what == "hub") hub = IHub(data);
-        else if (what == "holdings") holdings = IHoldings(data);
+        else if (what == "holdings") hub = IHub(data); // MUTATION: the holdings key writes the hub slot
         else if (what == "sender") sender = IHubMessageSender(data);
         else if (what == "shareClassManager") shareClassManager = IShareClassManager(data);
         else revert FileUnrecognizedParam();
```

## HubHandler #6528

the sender key writes the share class manager slot, so the outbound sender can never be repointed.

- **Mutant:** [`6528.sol`](6528.sol)
- **Caught by:** [`rcHhFileRepointsTheSenderIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L410)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6528`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhFileRepointsTheSenderIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -51,7 +51,7 @@
     function file(bytes32 what, address data) external auth {
         if (what == "hub") hub = IHub(data);
         else if (what == "holdings") holdings = IHoldings(data);
-        else if (what == "sender") sender = IHubMessageSender(data);
+        else if (what == "sender") shareClassManager = IShareClassManager(data); // MUTATION: the sender key writes the share class book slot
         else if (what == "shareClassManager") shareClassManager = IShareClassManager(data);
         else revert FileUnrecognizedParam();
         emit File(what, data);
```

## HubHandler #6529

the share class manager key writes the sender slot, so the share class manager can never be repointed.

- **Mutant:** [`6529.sol`](6529.sol)
- **Caught by:** [`rcHhFileRepointsTheShareClassBookIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L425)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6529`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhFileRepointsTheShareClassBookIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -52,7 +52,7 @@
         if (what == "hub") hub = IHub(data);
         else if (what == "holdings") holdings = IHoldings(data);
         else if (what == "sender") sender = IHubMessageSender(data);
-        else if (what == "shareClassManager") shareClassManager = IShareClassManager(data);
+        else if (what == "shareClassManager") sender = IHubMessageSender(data); // MUTATION: the share class book key writes the sender slot
         else revert FileUnrecognizedParam();
         emit File(what, data);
     }
```

## HubHandler #6530

rely clears authority instead of granting it, so no new ward can ever be added to the handler.

- **Mutant:** [`6530.sol`](6530.sol)
- **Caught by:** [`rcHhRelyThenDenyRoundTripIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L440)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6530`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhRelyThenDenyRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -23,7 +23,7 @@
 
     /// @inheritdoc IAuth
     function rely(address user) public auth {
-        wards[user] = 1;
+        wards[user] = 0; // MUTATION: rely clears authority instead of granting it
         emit Rely(user);
     }
 
```

## HubHandler #6531

deny grants authority instead of withdrawing it, so a ward once added can never be removed.

- **Mutant:** [`6531.sol`](6531.sol)
- **Caught by:** [`rcHhRelyThenDenyRoundTripIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L440)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6531`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhRelyThenDenyRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        wards[user] = 1; // MUTATION: deny grants authority instead of withdrawing it
         emit Deny(user);
     }
 }
```

## HubHandler #6532

an issuance no longer credits the class total, so a mint and matching burn leave that total lower.

- **Mutant:** [`6532.sol`](6532.sol)
- **Caught by:** [`rcHhIssueThenRevokeRestoresTheClassTotalIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L480)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6532`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhIssueThenRevokeRestoresTheClassTotalIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -95,7 +95,7 @@
         require(exists(poolId, scId_), ShareClassNotFound());
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
-        if (isIssuance) total.issuances += amount;
+        if (isIssuance) {} // MUTATION: an issuance never credits the class total
         else total.revocations += amount;
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
```

## HubHandler #6533

the sync marker latches once it is set, so a network that closes a batch can never open the next one.

- **Mutant:** [`6533.sol`](6533.sol)
- **Caught by:** [`rcHhSnapshotSetThenClearedIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L503)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6533`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhSnapshotSetThenClearedIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -104,7 +104,7 @@
         Snapshot storage snapshot_ = snapshot[poolId][scId][centrifugeId];
         require(snapshot_.nonce == nonce, InvalidNonce(snapshot_.nonce, nonce));
 
-        snapshot_.isSnapshot = isSnapshot;
+        snapshot_.isSnapshot = snapshot_.isSnapshot || isSnapshot; // MUTATION: the sync marker latches and never clears
         snapshot_.nonce++;
 
         emit SetSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
```

## HubHandler #6534

a share transfer credits the destination one more share than it moves, so a round trip leaves both networks off by one.

- **Mutant:** [`6534.sol`](6534.sol)
- **Caught by:** [`rcHhBridgeAndReturnLegIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L526)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 6534`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhBridgeAndReturnLegIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -112,7 +112,7 @@
         require(exists(poolId, scId_), ShareClassNotFound());
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
-        _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+        _updateNetwork(poolId, scId_, toCentrifugeId, amount + 1, true); // MUTATION: the destination is credited one more than the bridge moves
     }
 
     //----------------------------------------------------------------------------------------------
```

## HubHandler #8055

an asset report is booked under a fixed network instead of the reporting one, so its shortfalls land on the wrong network.

- **Mutant:** [`8055.sol`](8055.sol)
- **Caught by:** [`hlHhReportOfAnotherNetworkLeavesTheTrackedCountersAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L502)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8055`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhReportOfAnotherNetworkLeavesTheTrackedCountersAlone`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -88,8 +88,8 @@
         // The delta is valued at the hub-side valuation; the journaled value mirrors the holding
         // mutation exactly, so the accounts stay in sync with the holding.
         uint128 value = isIncrease
-            ? holdings.increase(poolId, scId, assetId, centrifugeId, amount)
-            : holdings.decrease(poolId, scId, assetId, centrifugeId, amount);
+            ? holdings.increase(poolId, scId, assetId, 0, amount) // MUTATION: a fixed network books the flow
+            : holdings.decrease(poolId, scId, assetId, 0, amount);
 
         if (holdings.isInitialized(poolId, scId, assetId)) {
             hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, value);
```

## HubHandler #8056

asset flows are booked under the asset's home network instead of the reporting one, so shortfalls count against the wrong network.

- **Mutant:** [`8056.sol`](8056.sol)
- **Caught by:** [`rcHhShortfallLandsOnTheReportingNetworkIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L577)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8056`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhShortfallLandsOnTheReportingNetworkIsReachable`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -88,8 +88,8 @@
         // The delta is valued at the hub-side valuation; the journaled value mirrors the holding
         // mutation exactly, so the accounts stay in sync with the holding.
         uint128 value = isIncrease
-            ? holdings.increase(poolId, scId, assetId, centrifugeId, amount)
-            : holdings.decrease(poolId, scId, assetId, centrifugeId, amount);
+            ? holdings.increase(poolId, scId, assetId, assetId.centrifugeId(), amount) // MUTATION: the asset id's own network books the flow
+            : holdings.decrease(poolId, scId, assetId, assetId.centrifugeId(), amount);
 
         if (holdings.isInitialized(poolId, scId, assetId)) {
             hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, value);
```

## HubHandler #8310

filing the holdings ledger also repoints the hub, so one configuration call rewires two of the handler's dependencies.

- **Mutant:** [`8310.sol`](8310.sol)
- **Caught by:** [`hlHhFileWiresOnlyTheNamedSlot`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L395)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8310`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhFileWiresOnlyTheNamedSlot`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -50,7 +50,7 @@
     /// @inheritdoc IHubHandler
     function file(bytes32 what, address data) external auth {
         if (what == "hub") hub = IHub(data);
-        else if (what == "holdings") holdings = IHoldings(data);
+        else if (what == "holdings") { holdings = IHoldings(data); hub = IHub(data); } // MUTATION: filing the holdings ledger also rewires the hub
         else if (what == "sender") sender = IHubMessageSender(data);
         else if (what == "shareClassManager") shareClassManager = IShareClassManager(data);
         else revert FileUnrecognizedParam();
```

## HubHandler #8311

a share transfer also sends the target network's sync notice, so the snapshot hook hears a sync no report caused.

- **Mutant:** [`8311.sol`](8311.sol)
- **Caught by:** [`vtHhSnapshotHookHearsOnlyAReport`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L109)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8311`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule vtHhSnapshotHookHearsOnlyAReport`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -146,7 +146,7 @@
 
         shareClassManager.transferShares(poolId, scId, originCentrifugeId, targetCentrifugeId, amount);
 
-        holdings.callOnTransferSnapshot(poolId, scId, originCentrifugeId, targetCentrifugeId, amount);
+        holdings.callOnTransferSnapshot(poolId, scId, originCentrifugeId, targetCentrifugeId, amount); holdings.callOnSyncSnapshot(poolId, scId, targetCentrifugeId); // MUTATION: a transfer also notifies a sync
 
         emit ForwardTransferShares(originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount);
 
```

## HubHandler #8312

an asset report that closes a network's batch notifies the snapshot hook twice, so the hook publishes the same pool price twice for one batch.

- **Mutant:** [`8312.sol`](8312.sol)
- **Caught by:** [`hlHhAssetReportNotifiesTheHookExactlyOnAClosedBatch`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L414)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8312`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhAssetReportNotifiesTheHookExactlyOnAClosedBatch`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -95,7 +95,7 @@
             hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, value);
         }
 
-        holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
+        holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce); holdings.callOnSyncSnapshot(poolId, scId, centrifugeId); // MUTATION: an asset report notifies the hook twice
     }
 
     /// @inheritdoc IHubGatewayHandler
```

## HubHandler #8313

a report that closes a network's batch never reaches the pool's snapshot hook, so the pool price is not republished when the batch is complete.

- **Mutant:** [`8313.sol`](8313.sol)
- **Caught by:** [`hlHhSyncNotificationOnlyOnAClosedBatch`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L376)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8313`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhSyncNotificationOnlyOnAClosedBatch`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -262,7 +262,7 @@
         if (!snapshot_.isSnapshot) return;
 
         ISnapshotHook hook = snapshotHook[poolId];
-        if (address(hook) != address(0)) hook.onSync(poolId, scId, centrifugeId);
+        if (address(hook) != address(0)) return; // MUTATION: the snapshot hook is never told of a closed batch
     }
 
     /// @dev Moves both deficit counters on a deficit-state crossing; no-op otherwise. The share class-network
```

## HubHandler #8314

the class shortfall counter moves the wrong way, so the first report putting a class short underflows it and is refused.

- **Mutant:** [`8314.sol`](8314.sol)
- **Caught by:** [`rvHhUninitializedAssetReportIsNeverStrandedByTheShortfallTally`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L73) · [`rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L235)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8314`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhUninitializedAssetReportIsNeverStrandedByTheShortfallTally rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -274,7 +274,7 @@
         if (wasDeficit == isDeficit) return;
 
         uint32 count =
-            isDeficit ? ++deficitCount[poolId][scId][centrifugeId] : --deficitCount[poolId][scId][centrifugeId];
+            isDeficit ? --deficitCount[poolId][scId][centrifugeId] : ++deficitCount[poolId][scId][centrifugeId]; // MUTATION: the share class deficit counter moves the wrong way
         uint32 networkCount =
             isDeficit ? ++networkDeficitCount[poolId][centrifugeId] : --networkDeficitCount[poolId][centrifugeId];
         emit UpdateDeficitCount(poolId, scId, centrifugeId, count, networkCount);
```

## HubHandler #8315

revoking past a network's recorded net issuance now reverts, so a transfer out of a network whose report lags is refused.

- **Mutant:** [`8315.sol`](8315.sol)
- **Caught by:** [`rvHhHooklessTransferIsNeverStrandedWhileTheCountersHaveRoom`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L130)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8315`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhHooklessTransferIsNeverStrandedWhileTheCountersHaveRoom`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -163,6 +163,7 @@
             ipn.issuances += amount;
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
+            require(amount <= ipn.issuances - ipn.revocations, NegativeIssuance()); // MUTATION: a network may not burn past what it received
             ipn.revocations += amount;
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
```

## HubHandler #8432

a transfer books its amount on both class wide counters as well, so the class supply record moves on a bridge although the net stays put.

- **Mutant:** [`8432.sol`](8432.sol)
- **Caught by:** [`hlHhTransferLeavesTheClassCountersAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L519)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8432`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhTransferLeavesTheClassCountersAlone`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -113,6 +113,8 @@
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+        issuanceAcrossNetworks[poolId][scId_].issuances += amount; // MUTATION: a transfer is booked on both class counters
+        issuanceAcrossNetworks[poolId][scId_].revocations += amount;
     }
 
     //----------------------------------------------------------------------------------------------
```

## HubHandler #8433

a transfer books its amount as a class wide issuance, so every bridge inflates the class supply.

- **Mutant:** [`8433.sol`](8433.sol)
- **Caught by:** [`hlHhTransferConservesTheClassTotal`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L6) · [`hlHhTransferLeavesTheClassCountersAlone`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L519)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8433`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhTransferConservesTheClassTotal hlHhTransferLeavesTheClassCountersAlone`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -113,6 +113,7 @@
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+        issuanceAcrossNetworks[poolId][scId_].issuances += amount; // MUTATION: a transfer is booked as a class issuance
     }
 
     //----------------------------------------------------------------------------------------------
```

## HubHandler #8434

registerAsset lets a set precision grow, so a spoke can rescale an asset the hub already values at other decimals.

- **Mutant:** [`8434.sol`](8434.sol)
- **Caught by:** [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8434`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -49,7 +49,7 @@
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        require(!current.registered || current.decimals == 0 || current.decimals <= decimals_, CannotChangeDecimals()); // MUTATION: a set precision may grow
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubHandler #8435

registerAsset refuses every repeat again, so a spoke re-announcing a known asset at its own decimals is turned away.

- **Mutant:** [`8435.sol`](8435.sol)
- **Caught by:** [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8435`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -49,7 +49,7 @@
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        require(!current.registered, CannotChangeDecimals()); // MUTATION: a known asset may never be announced again
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubHandler #8436

registerAsset drops the escape for a zero precision, so an asset first recorded with no decimals can never take its real ones.

- **Mutant:** [`8436.sol`](8436.sol)
- **Caught by:** [`rcHhZeroDecimalAssetTakesItsDecimalsLaterIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L624) · [`rcHhZeroPrecisionAssetCanBeCorrectedByARepeatRegistration`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L639)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8436`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhZeroDecimalAssetTakesItsDecimalsLaterIsReachable rcHhZeroPrecisionAssetCanBeCorrectedByARepeatRegistration`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -49,7 +49,7 @@
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        require(!current.registered || current.decimals == decimals_, CannotChangeDecimals()); // MUTATION: a zero precision is final
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubHandler #8437

transferShares skips the share class existence check, so a bridge of a class the hub never created goes through.

- **Mutant:** [`8437.sol`](8437.sol)
- **Caught by:** [`rvHhTransferRefusesANonWardOrAnUnknownShareClass`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L113)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8437`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhTransferRefusesANonWardOrAnUnknownShareClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -109,7 +109,7 @@
         uint16 toCentrifugeId,
         uint128 amount
     ) external auth {
-        require(exists(poolId, scId_), ShareClassNotFound());
+        // require(exists(poolId, scId_), ShareClassNotFound()); // MUTATION: removed share class existence check
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
```

## HubHandler #8438

increase narrows the increased amount back to 128 bits, so a report pushing it past that width is refused although the counter has room.

- **Mutant:** [`8438.sol`](8438.sol)
- **Caught by:** [`rvHhUninitializedAssetReportIsNeverStrandedByTheShortfallTally`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L73) · [`rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L235)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8438`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhUninitializedAssetReportIsNeverStrandedByTheShortfallTally rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -146,7 +146,7 @@
 
         bool wasDeficit = holding_.decreasedAmount > holding_.increasedAmount;
         uint256 oldAmount = _amount(holding_);
-        holding_.increasedAmount += amount_;
+        holding_.increasedAmount = (holding_.increasedAmount + amount_).toUint128(); // MUTATION: the increased amount is capped at 128 bits
         uint128 realized = (_amount(holding_) - oldAmount).toUint128();
 
         // Value only the realized increase (a preceding over-decrease is netted off first) at the hub-side
```

## HubHandler #8439

_updateNetwork narrows a network's issued count to 128 bits, so a transfer or report pushing it past that width fails although the counter has room.

- **Mutant:** [`8439.sol`](8439.sol)
- **Caught by:** [`rvHhHooklessTransferIsNeverStrandedWhileTheCountersHaveRoom`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L130) · [`rvHhShareReportIsNeverStrandedWhileTheCountersHaveRoom`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L202)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8439`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhHooklessTransferIsNeverStrandedWhileTheCountersHaveRoom rvHhShareReportIsNeverStrandedWhileTheCountersHaveRoom`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -160,7 +160,7 @@
         bool wasNegative = ipn.revocations > ipn.issuances;
 
         if (isIssuance) {
-            ipn.issuances += amount;
+            ipn.issuances = (ipn.issuances + amount).toUint128(); // MUTATION: the network issued counter is capped at 128 bits
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## HubHandler #8829

a zero valued amount posting is no longer skipped, so a report on an opened holding with no amount account fails although nothing is booked.

- **Mutant:** [`8829.sol`](8829.sol)
- **Caught by:** [`rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L235)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8829`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhOpenedAssetReportFailsOnlyOnAnOverflowOrAMissingAccount`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -539,7 +539,7 @@
     function _updateAccountingAmount(PoolId poolId, ShareClassId scId, AssetId assetId, bool isPositive, uint128 diff)
         internal
     {
-        if (diff == 0) return;
+        // MUTATION: a zero valued amount posting is journaled too
         if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.AmountCredit);
         else _journal(poolId, scId, assetId, diff, AccountKind.AmountCredit, AccountKind.AmountDebit);
     }
```

## HubHandler #8830

registerAsset accepts the empty asset id, so a spoke can register an asset under it and every later lookup of that id resolves.

- **Mutant:** [`8830.sol`](8830.sol)
- **Caught by:** [`rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L292)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8830`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhRegisterAssetRefusesExactlyANonWardAnOversizedPrecisionOrARescaling`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -45,7 +45,7 @@
 
     /// @inheritdoc IHubRegistry
     function registerAsset(AssetId assetId, uint8 decimals_) external auth {
-        require(!assetId.isNull(), EmptyAssetId());
+        // MUTATION: the null asset id is accepted
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
```

## HubHandler #8831

a repeat registration keeps the old precision, so an asset first recorded at zero decimals never takes its real ones although the call succeeds.

- **Mutant:** [`8831.sol`](8831.sol)
- **Caught by:** [`rcHhZeroPrecisionAssetCanBeCorrectedByARepeatRegistration`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L639) · [`rcHhZeroDecimalAssetTakesItsDecimalsLaterIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L624)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8831`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhZeroPrecisionAssetCanBeCorrectedByARepeatRegistration rcHhZeroDecimalAssetTakesItsDecimalsLaterIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -51,7 +51,7 @@
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
 
-        asset[assetId] = AssetInfo(true, decimals_);
+        asset[assetId] = AssetInfo(true, current.registered ? current.decimals : decimals_); // MUTATION: a repeat keeps the recorded precision
 
         emit NewAsset(assetId, decimals_);
     }
```

## HubHandler #8832

the outbound transfer drops the caller's extra gas limit, so a hookless transfer is executed on the target network with no added gas.

- **Mutant:** [`8832.sol`](8832.sol)
- **Caught by:** [`hlHhHooklessTransferKeepsTheExtraGasLimit`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L536)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8832`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhHooklessTransferKeepsTheExtraGasLimit`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -151,7 +151,7 @@
         emit ForwardTransferShares(originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount);
 
         return sender.sendExecuteTransferShares{value: msg.value}(
-            originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund
+            originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, 0, refund // MUTATION: the extra gas limit is dropped
         );
     }
 }
```

## HubHandler #8833

the outbound transfer names an empty share class id, so the target network is told to credit shares of a class the hub never moved.

- **Mutant:** [`8833.sol`](8833.sol)
- **Caught by:** [`hlHhTransferKeepsThePoolAndClass`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L550)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 8833`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhTransferKeepsThePoolAndClass`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -151,7 +151,7 @@
         emit ForwardTransferShares(originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount);
 
         return sender.sendExecuteTransferShares{value: msg.value}(
-            originCentrifugeId, targetCentrifugeId, poolId, scId, receiver, amount, extraGasLimit, refund
+            originCentrifugeId, targetCentrifugeId, poolId, ShareClassId.wrap(bytes16(0)), receiver, amount, extraGasLimit, refund // MUTATION: the message names the null class
         );
     }
 }
```

## HubHandler #9062

a reported asset move books the raw asset quantity instead of its value, so the ledger drifts from the holding.

- **Mutant:** [`9062.sol`](9062.sol)
- **Caught by:** [`stHhReportedAssetMoveIsBookedExactly`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L128)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 9062`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule stHhReportedAssetMoveIsBookedExactly`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -92,7 +92,7 @@
             : holdings.decrease(poolId, scId, assetId, centrifugeId, amount);
 
         if (holdings.isInitialized(poolId, scId, assetId)) {
-            hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, value);
+            hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, amount); // MUTATION: the raw asset quantity is booked instead of its value
         }
 
         holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
```

## HubHandler #9063

a debit stamps the account with the block number instead of the block time, so its activity time is wrong.

- **Mutant:** [`9063.sol`](9063.sol)
- **Caught by:** [`vtHhAccountStampRecordsTheCurrentBlock`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 9063`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule vtHhAccountStampRecordsTheCurrentBlock`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -95,7 +95,7 @@
 
         acc.totalDebit += value;
         debited += value;
-        acc.lastUpdated = uint64(block.timestamp);
+        acc.lastUpdated = uint64(block.number); // MUTATION: the debit is stamped with the block number instead of the block time
         emit Debit(_currentPoolId, account, value);
     }
 
```

## HubHandler #9085

an asset report journals its value in the opposite direction, so a deposit credits the holding's account and debits its counterpart.

- **Mutant:** [`9085.sol`](9085.sol)
- **Caught by:** [`hlHhAssetReportJournalsTheRealizedValueOnlyOnAnInitializedHolding`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_high_level.spec#L434)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubHandler 9085`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/high_level.conf --rule hlHhAssetReportJournalsTheRealizedValueOnlyOnAnInitializedHolding`

```diff
--- a/src/core/hub/HubHandler.sol
+++ b/src/core/hub/HubHandler.sol
@@ -92,7 +92,7 @@
             : holdings.decrease(poolId, scId, assetId, centrifugeId, amount);
 
         if (holdings.isInitialized(poolId, scId, assetId)) {
-            hub.updateAccountingAmount(poolId, scId, assetId, isIncrease, value);
+            hub.updateAccountingAmount(poolId, scId, assetId, !isIncrease, value); // MUTATION: the journal direction is flipped
         }
 
         holdings.setSnapshot(poolId, scId, centrifugeId, isSnapshot, nonce);
```

