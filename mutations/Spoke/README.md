# Mutations for `Spoke` (`src/core/spoke/Spoke.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/spoke/SnapshotQueue.sol`, `src/core/utils/BatchedMulticall.sol`, `src/misc/Auth.sol`, `src/misc/Recoverable.sol`, `src/misc/ReentrancyProtection.sol`.

| # | What we test |
|---|---|
| [205](#spoke-205) | deposit moves the escrow balance without queueing the move for the hub, so the hub's view of the pool's assets falls behind.<br>Caught by: [`stSpSpendableBalanceMoveIsQueuedForTheHub`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L31) |
| [206](#spoke-206) | A flushed asset queue keeps its outstanding slot, so the share class never again reports a complete snapshot.<br>Caught by: [`stSpDrainingAQueueRowSpendsANonceAndItsSlot`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L54) |
| [207](#spoke-207) | issue mints local shares without queueing the issuance for the hub, so local supply moves unreported.<br>Caught by: [`stSpShareSupplyMovesOnlyAsReported`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L73) |
| [210](#spoke-210) | A flushed asset queue does not advance the nonce, so the next report reaches the hub under the same nonce.<br>Caught by: [`stSpDrainingAQueueRowSpendsANonceAndItsSlot`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L54) |
| [211](#spoke-211) | Every escrow move is queued for the hub in the opposite direction, so a deposit is reported as a withdrawal.<br>Caught by: [`stSpQueuedMoveIsBackedByTheEscrow`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L114) |
| [216](#spoke-216) | A noted deposit is queued for the hub without crediting the escrow, so the hub is told of a move the escrow never made.<br>Caught by: [`stSpQueuedMoveIsBackedByTheEscrow`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L114) |
| [4600](#spoke-4600) | A cross chain share transfer of zero shares is accepted, so an empty transfer message is sent to the destination.<br>Caught by: [`vtSpBridgeNeverAnnouncesAnEmptyTransfer`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L6) |
| [4601](#spoke-4601) | A cross chain share transfer may name this very network as its destination, so shares burned here are announced for a mint here.<br>Caught by: [`vtSpBridgeNeverAnnouncesBackToThisNetwork`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L23) |
| [4602](#spoke-4602) | An asset the registry has never seen is announced under the null asset number, because the fresh number is minted for known assets only.<br>Caught by: [`vtSpAssetRegistrationNeverAnnouncesTheNullId`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L43) |
| [4603](#spoke-4603) | An asset registration announces one decimal more than the ceiling check inspected, so a precision the pool accounting cannot represent reaches the hub.<br>Caught by: [`vtSpAssetRegistrationRespectsTheDecimalsCeiling`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L62) |
| [4604](#spoke-4604) | A bridge transfer hands the same announcement over twice, so one call costs the pool two messages and two fees.<br>Caught by: [`vtSpOneCallHandsOverAtMostOneMessage`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L79) |
| [4605](#spoke-4605) | A bridge transfer pulls the shares from the named sender instead of the owner, so the wrong account is charged.<br>Caught by: [`hlSpBridgeDebitsTheNamedOwner`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L4) · [`hlSpBridgeSpendsTheOwnersApproval`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L106) |
| [4606](#spoke-4606) | A bridge transfer parks the shares on the spoke instead of burning them, so the bridged shares exist on both chains.<br>Caught by: [`hlSpBridgeBurnsTheBridgedShares`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L22) · [`hlSpBridgeParksNoSharesOnTheSpoke`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L40) |
| [4607](#spoke-4607) | A bridge transfer announces itself to the destination chain twice, so one burn here can be minted two times there.<br>Caught by: [`hlSpBridgeAnnouncesExactlyOneTransfer`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L59) |
| [4608](#spoke-4608) | The outbound announcement carries the gas limit in the amount slot, so the destination mints an unrelated number.<br>Caught by: [`hlSpBridgeAnnouncesTheBurnedAmount`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L76) |
| [4609](#spoke-4609) | The outbound announcement swaps the named sender and the named receiver, so bridged shares are minted at the destination for the wrong party.<br>Caught by: [`hlSpBridgeAnnouncesTheNamedReceiver`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L91) |
| [4610](#spoke-4610) | A bridge transfer also queues a revocation for the hub, so shares reminted on the destination count as destroyed.<br>Caught by: [`hlSpBridgeReportsNoShareMovementToTheHub`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L126) |
| [4611](#spoke-4611) | Noting a deposit that already reached the escrow also pulls the tokens from the caller, so the holdings are paid twice.<br>Caught by: [`hlSpNoteDepositMovesNoTokens`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L143) |
| [4612](#spoke-4612) | The balance sheet gate no longer requires a pool manager, so any caller can move escrow, queues and share supply.<br>Caught by: [`acSpQueuedAssetDeltasComeOnlyFromAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L54) · [`acSpQueuedShareDeltasComeOnlyFromAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L70) · [`acSpEscrowCustodyMovesOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L86) · [`acSpQueueSubmissionsLeaveOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L103) · [`acSpShareSupplyGrowsThroughTheSpokeOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L123) · [`acSpUnauthorizedCannotReduceAHoldersBalance`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L139) |
| [4613](#spoke-4613) | A bridge transfer no longer checks the caller is the owner or a ward, so anyone can bridge a holder's approved shares.<br>Caught by: [`acSpApprovalToTheSpokeIsSpentOnlyByItsOwnerAWardOrAManagersForcedTransfer`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L197) |
| [4614](#spoke-4614) | A bridge transfer no longer checks the bridger seat, so an owner the pool never listed can move shares off this network.<br>Caught by: [`acSpBridgeStartsOnlyForABridgerOrAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L160) |
| [4615](#spoke-4615) | The request entry no longer checks its caller, so anybody can file an investor request with the hub in the pool's name.<br>Caught by: [`acSpInvestorRequestsLeaveOnlyForTheRequestManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L178) |
| [4616](#spoke-4616) | The balance sheet gate no longer requires a pool manager, so no balance sheet entry refuses a non-manager caller.<br>Caught by: [`rvSpDepositRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L18) · [`rvSpNoteDepositRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L32) · [`rvSpWithdrawRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L46) · [`rvSpWithdrawReservedRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L60) · [`rvSpReserveRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L75) · [`rvSpUnreserveRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L89) · [`rvSpSubmitQueuedAssetsRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L104) · [`rvSpIssueRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L118) · [`rvSpRevokeRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L132) · [`rvSpWithdrawSharesRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L146) · [`rvSpSubmitQueuedSharesRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L160) · [`rvSpTransferSharesFromRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L174) |
| [4617](#spoke-4617) | The ward gate no longer looks at the caller, so rewiring the spoke and handing out or withdrawing its keys is open to everyone.<br>Caught by: [`rvSpFileRefusesANonWardOrAnUnknownName`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L4) · [`rvSpRelyRefusesANonWard`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L269) · [`rvSpDenyRefusesANonWard`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L282) |
| [4618](#spoke-4618) | Balance sheet entries also demand a ward seat, so a plain pool manager can no longer submit queued positions.<br>Caught by: [`rvSpSubmitQueuedAssetsIsNeverRefusedToASeatedManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L295) · [`rvSpSubmitQueuedSharesIsNeverRefusedToASeatedManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L317) |
| [4619](#spoke-4619) | The spoke side manager call is closed behind the pool manager seat, so the entry the interface promises to every caller refuses one.<br>Caught by: [`rvSpManagerCallIsNeverRefusedToAnyCaller`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L339) |
| [4620](#spoke-4620) | A bridge transfer no longer checks the caller is the owner or a ward, so a stranger can bridge the owner's shares.<br>Caught by: [`rvSpBridgeRefusesAStrangerToTheOwner`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L188) |
| [4621](#spoke-4621) | A bridge transfer no longer checks the bridger seat, so an owner the pool never listed can still move holdings off this network.<br>Caught by: [`rvSpBridgeRefusesANonBridgerOwner`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L205) |
| [4622](#spoke-4622) | A bridge transfer of nothing is accepted, so a burn of zero is announced to the destination chain instead of being refused.<br>Caught by: [`rvSpBridgeRefusesAZeroAmount`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L221) |
| [4623](#spoke-4623) | A bridge transfer addressed to this very network is accepted, so shares are burned here for a mint that is asked of this same chain.<br>Caught by: [`rvSpBridgeRefusesALocalDestination`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L237) |
| [4624](#spoke-4624) | The request entry no longer checks its caller, so a request reaches the hub for a caller who is not the pool's registered request manager.<br>Caught by: [`rvSpRequestRefusesAnyCallerButTheRegisteredManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L253) |
| [5300](#spoke-5300) | file drops its authorisation, so any caller repoints the gateway and the outbound message sender.<br>Caught by: [`acSpGatewayIsRepointedOnlyByAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L21) · [`acSpMessageSenderIsRepointedOnlyByAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L37) |
| [5301](#spoke-5301) | rely drops its authorisation, so any caller adds itself or anybody else to the ward list.<br>Caught by: [`acSpWardListMovesOnlyForAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L4) |
| [5302](#spoke-5302) | deny drops its authorisation, so any caller strips a ward of its permissions.<br>Caught by: [`acSpWardListMovesOnlyForAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L4) |
| [6000](#spoke-6000) | Asset registration is closed behind the ward gate, so an ordinary caller can no longer register a new asset.<br>Caught by: [`rcSpRegisterAssetMintsAFreshIdForAnUnknownErc20`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L4) |
| [6001](#spoke-6001) | An asset announcement always mints a fresh id, so a pair the registry already carries can never be announced a second time.<br>Caught by: [`rcSpRegisterAssetReannouncesTheStoredIdIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L25) |
| [6002](#spoke-6002) | A tranche is minted its id under the plain token row of the registry, so the tranche itself is left without one.<br>Caught by: [`rcSpRegisterAssetMintsAFreshIdForAnErc6909Tranche`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L45) |
| [6003](#spoke-6003) | The decimals ceiling is read as an exclusive bound, so a token sitting exactly at the precision the pool accounting supports is turned away.<br>Caught by: [`rcSpRegisterAssetAtTheDecimalsCeilingIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L65) |
| [6004](#spoke-6004) | A deposit is queued for the hub in the opposite direction, so money arriving in the pool is reported as money leaving it.<br>Caught by: [`rcSpFirstDepositIntoAnEmptyRowIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L82) · [`rcSpDepositIntoAHoldingRowIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L104) |
| [6005](#spoke-6005) | A plain token deposit credits the pool escrow without charging the payer, so the payer keeps the funds.<br>Caught by: [`rcSpDepositOfThePayersWholeBalanceIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L128) |
| [6006](#spoke-6006) | A deposit of a tranche credits the pool escrow without moving any units, so the escrow is told it holds tranche units that never arrived.<br>Caught by: [`rcSpDepositOfAnErc6909TrancheIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L148) |
| [6007](#spoke-6007) | Noting a deposit queues the arrival for the hub without crediting the escrow, so custody never records the holding.<br>Caught by: [`rcSpNoteDepositCreditsCustodyWithoutMovingTokens`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L172) |
| [6008](#spoke-6008) | A deposit of nothing is refused, so a pool cannot use the entry to report an arrival of size zero.<br>Caught by: [`rcSpZeroAmountDepositIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L196) |
| [6009](#spoke-6009) | A withdrawal debits custody and reports it to the hub without paying out, so the receiver gets nothing.<br>Caught by: [`rcSpWithdrawPaysTheReceiverIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L217) · [`rcSpWithdrawToTheCallerThemselvesIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L281) |
| [6010](#spoke-6010) | A withdrawal requires a free balance strictly above the amount, so the whole free balance can never be withdrawn.<br>Caught by: [`rcSpWithdrawEmptiesTheFreeBalanceExactlyIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L242) · [`rcSpWithdrawLeavesTheHeldPartBehindIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L260) |
| [6011](#spoke-6011) | Placing a hold is reported to the hub as an increase, so funds set aside are announced as arriving.<br>Caught by: [`rcSpFirstHoldOnARowIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L303) · [`rcSpHoldBeyondTheRowsCustodyIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L933) |
| [6012](#spoke-6012) | A hold is reported to the hub but never booked in escrow, so the funds stay spendable.<br>Caught by: [`rcSpHoldOnTheWholeFreeBalanceIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L326) · [`rcSpHoldThenReleaseRoundTripIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L850) |
| [6013](#spoke-6013) | Lifting a hold is reported to the hub as a decrease, so funds returning to the accounted holding are announced as funds leaving it.<br>Caught by: [`rcSpReleaseOfTheWholeHoldIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L350) |
| [6014](#spoke-6014) | Paying held funds out reports the departure to the hub again, so a decrease already announced at hold time counts twice.<br>Caught by: [`rcSpWithdrawReservedPaysHeldFundsOutIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L375) · [`rcSpHoldThenPayOutIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L776) |
| [6015](#spoke-6015) | An issuance is queued for the hub as a revocation, so shares being created are reported to the hub as shares destroyed.<br>Caught by: [`rcSpIssueMintsSharesIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L401) · [`rcSpZeroShareIssuanceIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L424) |
| [6016](#spoke-6016) | A revocation pulls the shares onto the spoke without destroying them, so supply the hub was told had gone still exists.<br>Caught by: [`rcSpRevokeBurnsTheCallersSharesIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L446) · [`rcSpRevokeDownToAnEmptyClassIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L472) |
| [6017](#spoke-6017) | Handing custodied shares to an investor moves nothing, so the pool escrow keeps every share a claim was meant to release.<br>Caught by: [`rcSpWithdrawSharesHandsCustodyOutIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L492) · [`rcSpIssueThenWithdrawSharesIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L801) |
| [6018](#spoke-6018) | A forced share transfer moves the holding the wrong way, so the account meant to receive the shares is the one that pays them.<br>Caught by: [`rcSpTransferSharesFromMovesAHoldingIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L518) |
| [6019](#spoke-6019) | Submitting a pool's asset report drains the queue but never sends it, so the cleared flows never reach the hub.<br>Caught by: [`rcSpSubmitQueuedAssetsReportsToTheHubIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L540) · [`rcSpDepositThenSubmitQueuedAssetsIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L825) |
| [6020](#spoke-6020) | Submitting a pool's share report drains the queue but never sends it, so the cleared share movements never reach the hub.<br>Caught by: [`rcSpSubmitQueuedSharesWithNoExtraGasIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L559) |
| [6021](#spoke-6021) | The bridge admits a ward acting for somebody else and nobody else, so a holder can no longer send their own shares to another network.<br>Caught by: [`rcSpBridgeDrivenByTheOwnerIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L578) · [`rcSpBridgeThroughTheShortEntryPointIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L654) |
| [6022](#spoke-6022) | The bridge requires the caller to be both the owner and a ward, so a ward can no longer bridge for somebody else.<br>Caught by: [`rcSpBridgeDrivenByAWardForTheOwnerIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L605) |
| [6023](#spoke-6023) | The outbound announcement of a bridge carries one unit less than was burned here, so every transfer strands a unit that exists on no network.<br>Caught by: [`rcSpBridgeOfTheWholeHoldingIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L630) |
| [6024](#spoke-6024) | An investor request from the request manager is accepted but never relayed, so the hub never receives it.<br>Caught by: [`rcSpPaidRequestIsRelayedIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L675) · [`rcSpUnpaidRequestIsRelayedIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L695) |
| [6025](#spoke-6025) | managerCall now requires the pool manager role, so a caller without it can no longer relay a call to the hub.<br>Caught by: [`rcSpManagerCallFromAnUnseatedCallerIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L715) |
| [6026](#spoke-6026) | Granting authority announces the new seat without writing it, so an account told it was given the keys never actually holds them.<br>Caught by: [`rcSpRelyThenDenyRoundTripIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L736) |
| [6027](#spoke-6027) | Withdrawing authority announces the removal without clearing the seat, so a key that was taken back is still held.<br>Caught by: [`rcSpRelyThenDenyRoundTripIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L736) |
| [6028](#spoke-6028) | withdraw pays an ERC6909 asset out under token id zero, so the receiver never gets the units it was owed.<br>Caught by: [`rcSpWithdrawOfAnErc6909TrancheIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L875) |
| [6029](#spoke-6029) | A deposit moves the escrow row without reporting the arrival to the hub, so only one leg of a round trip is ever announced.<br>Caught by: [`rcSpDepositThenWithdrawRoundTripIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L755) |
| [6030](#spoke-6030) | file answers to "sender" on the gateway leg, so the gateway cannot be repointed and a new sender lands in the gateway slot.<br>Caught by: [`rcSpFileRepointsTheGatewayIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L903) · [`rcSpFileRepointsTheMessageSenderIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L918) |
| [6031](#spoke-6031) | A plain token deposit credits the pool escrow without charging the payer, so custody is booked for tokens that never moved.<br>Caught by: [`stSpEscrowCustodyMovesWithItsTokens`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L97) |
| [6033](#spoke-6033) | the queue lookup no longer insists the (asset, tokenId) pair is registered, so a queued row can name an asset id the registry never minted.<br>Caught by: [`queuedAssetRowImpliesRegisteredAsset`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L23) · [`escrowedRowImpliesRegisteredAsset`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L29) |
| [6034](#spoke-6034) | noteDeposit drops its manager and policy gate, so anyone can book custody and queue work for a pool the spoke never created.<br>Caught by: [`escrowedCustodyImpliesCreatedPool`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L35) · [`queueActivityImpliesCreatedPool`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L40) |
| [6036](#spoke-6036) | registerAsset builds the asset id from the destination chain instead of this spoke's own, so a local asset carries a foreign network.<br>Caught by: [`registeredAssetIsLocal`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L46) |
| [6037](#spoke-6037) | A deposit of a plain token credits the pool escrow without ever charging the payer, so custody is booked against tokens that never arrived.<br>Caught by: [`escrowCustodyIsBackedOrNoted`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L53) |
| [6038](#spoke-6038) | withdraw drops the escrow's book but never moves the token, so custody falls while the tokens stay put.<br>Caught by: [`hlSpWithdrawMovesTokensAndBookTogether`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L589) |
| [6039](#spoke-6039) | withdrawReserved moves the token but never drops the escrow's book, so tokens leave while custody still claims them.<br>Caught by: [`hlSpWithdrawReservedMovesTokensAndBookTogether`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L611) |
| [8500](#spoke-8500) | Revocation force pulls the caller's shares instead of using their approval, so the approval stays unspent.<br>Caught by: [`hlSpRevokeSpendsTheCallersApproval`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L161) |
| [8501](#spoke-8501) | A manager's forced share transfer forwards the holder as sender, so the named sender's approval is never spent.<br>Caught by: [`hlSpTransferSharesFromSpendsTheNamedSendersApproval`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L178) |
| [8502](#spoke-8502) | A deposit is paid out of the asset contract's own balance instead of the caller's, so the pool books assets its depositor never paid.<br>Caught by: [`hlSpDepositDebitsTheCaller`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L195) |
| [8503](#spoke-8503) | An asset registration is announced to this network instead of the network named, so the hub the caller addressed never learns the asset.<br>Caught by: [`hlSpRegisterAssetAnnouncesToTheNamedNetwork`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L213) |
| [8504](#spoke-8504) | Repointing the gateway also repoints the outbound message sender to the same address, so one configuration change silently rewires both routes.<br>Caught by: [`hlSpFileRepointsOnlyTheNamedRoute`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L226) |
| [8505](#spoke-8505) | Issued shares are minted to the caller instead of the recipient named.<br>Caught by: [`hlSpIssueMintsToTheRecipientNamed`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L241) |
| [8506](#spoke-8506) | A withdrawal pays the caller instead of the receiver named, so funds leave the escrow to the wrong address.<br>Caught by: [`hlSpWithdrawalPaysTheReceiverNamed`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L257) |
| [8507](#spoke-8507) | A withdrawal of reserved funds pays the caller instead of the receiver named, so the held funds leave the escrow to the wrong address.<br>Caught by: [`hlSpReservedWithdrawalPaysTheReceiverNamed`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L275) |
| [8508](#spoke-8508) | A share payout goes to the caller instead of the receiver named.<br>Caught by: [`hlSpSharePayoutReachesTheReceiverNamed`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L294) |
| [8509](#spoke-8509) | A bridge transfer admits pool managers instead of wards, so a manager can spend a holder's approval and bridge their shares away.<br>Caught by: [`acSpApprovalToTheSpokeIsSpentOnlyByItsOwnerAWardOrAManagersForcedTransfer`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L197) |
| [8510](#spoke-8510) | A manager call names the spoke itself as its caller on the wire, so the hub checks the spoke's permissions instead of the caller's.<br>Caught by: [`hlSpManagerCallNamesItsCallerOnTheWire`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L311) |
| [8511](#spoke-8511) | A bridge transfer announces the share owner as sender instead of the named sender, so the destination misattributes the transfer.<br>Caught by: [`hlSpBridgeAnnouncesTheNamedSender`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L329) |
| [8512](#spoke-8512) | The short bridge entry names the spoke itself as the sender instead of the caller, so the destination attributes every such transfer to the protocol.<br>Caught by: [`hlSpShortBridgeAnnouncesTheCallerAsSender`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L344) |
| [8513](#spoke-8513) | A request is always relayed as paid, whatever payment mode the request manager asked for.<br>Caught by: [`hlSpRequestRelaysThePaymentModeItWasHanded`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L357) |
| [8514](#spoke-8514) | A share report is sent without the payment its caller attached, so the message leaves unpaid and the ether stays on the spoke.<br>Caught by: [`vtSpEveryOutboundSendCarriesTheAttachedValue`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L94) |
| [8515](#spoke-8515) | A revocation burns without approving the registrar first, so the burn spends any standing approval and its remainder stays open.<br>Caught by: [`hlSpRevokeLeavesNoApprovalToTheRegistrar`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L371) |
| [8516](#spoke-8516) | A bridge transfer approves the registrar without limit instead of the bridged amount, so a standing approval over spoke shares remains.<br>Caught by: [`hlSpBridgeLeavesNoApprovalToTheRegistrar`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L385) |
| [8517](#spoke-8517) | A bridge transfer checks the restriction for the named sender instead of the owner, so a vetoed owner can still bridge.<br>Caught by: [`rvSpBridgeRefusesAnOwnerTheRegistrarVetoes`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L355) |
| [8642](#spoke-8642) | Registration refuses assets of fewer than two decimals, so an asset of zero decimals can no longer be registered with the hub.<br>Caught by: [`rcSpRegisterAssetAtZeroDecimalsIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L1040) |
| [8929](#spoke-8929) | Bridging a share class that has no share token succeeds quietly, so the caller sees success while nothing is burnt or sent.<br>Caught by: [`rvSpBridgeRefusesAnUnregisteredShareClass`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L392) |
| [8930](#spoke-8930) | A request also refuses the gateway as direct caller, so when the gateway is a pool's request manager no batched request can be relayed.<br>Caught by: [`rcSpBatchedRequestPassesTheGateWhenTheGatewayIsTheRequestManagerIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L1057) |
| [9008](#spoke-9008) | a token rescue also makes its receiver an admin of the contract, so whoever receives rescued tokens gains every ward right.<br>Caught by: [`hlSpRecoverTokensMovesOnlyTheRescuedBalances`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L469) |
| [9011](#spoke-9011) | An ERC20 token rescue transfers a zero amount, so rescued tokens never leave the contract.<br>Caught by: [`rcSpARescueToTheEscrowLeavesUnbookedTokens`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_reachability.spec#L64) |
| [9066](#spoke-9066) | noteDeposit queues the flow without booking it in escrow, so the noted amount never reaches custody.<br>Caught by: [`hlSpNoteDepositBooksExactlyItsAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L566) · [`hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L634) |
| [9270](#spoke-9270) | Setting the gateway keeps the old gateway, so an admin's switch to a new gateway silently does nothing.<br>Caught by: [`hlSpFileWritesTheValueIntoTheNamedRoute`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L401) |
| [9271](#spoke-9271) | Setting the gateway to the zero address is refused, so an admin can no longer disconnect the spoke from its gateway.<br>Caught by: [`rcSpFileAcceptsTheNullAddress`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L979) |
| [9272](#spoke-9272) | Configuring the spoke refuses the gateway as caller, so a gateway made an admin still cannot configure the spoke.<br>Caught by: [`rcSpAWardCanSeatTheGatewayOnTheWardRoll`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L959) |
| [9273](#spoke-9273) | A withdrawal pays out of the next pool id's escrow instead of its own, so one pool's manager drains its neighbour.<br>Caught by: [`hlSpEscrowResolvedEntryNeverMovesAnotherPoolsEscrowTokens`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L416) |
| [9274](#spoke-9274) | Registering an asset also seats its caller as a manager of pool 1, so anyone can seize that pool's balance sheet.<br>Caught by: [`acSpRegisterAssetSeatsNobodyInAnyPool`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L219) |
| [9275](#spoke-9275) | A cross-chain share transfer to a malformed receiver is refused, so shares no longer burn toward an undeliverable address.<br>Caught by: [`rcSpBridgeToAnUndeliverableReceiverBurnsAndAnnounces`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L993) |
| [9276](#spoke-9276) | A bridge transfer requires the announced sender to be the caller or the owner, so no third party can be named.<br>Caught by: [`rcSpBridgeAnnouncesASenderNeitherCallerNorOwner`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L1018) |
| [9700](#spoke-9700) | While a batch is open any caller acts as the batch initiator, so a reentrant account borrows the initiator's rights.<br>Caught by: [`rvSpDepositRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L18) · [`rvSpNoteDepositRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L32) · [`rvSpWithdrawRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L46) · [`rvSpWithdrawReservedRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L60) · [`rvSpReserveRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L75) · [`rvSpUnreserveRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L89) · [`rvSpSubmitQueuedAssetsRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L104) · [`rvSpIssueRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L118) · [`rvSpRevokeRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L132) · [`rvSpWithdrawSharesRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L146) · [`rvSpSubmitQueuedSharesRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L160) · [`rvSpTransferSharesFromRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L174) · [`rvSpBridgeRefusesAStrangerToTheOwner`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L188) |
| [9701](#spoke-9701) | A request checks the resolved caller, not the direct one, so the gateway passes inside a batch the request manager opened.<br>Caught by: [`rvSpRequestRefusesAnyCallerButTheRegisteredManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L253) |
| [9702](#spoke-9702) | A manager call names the direct caller on the wire, so inside a batch the hub sees the gateway, not the initiator.<br>Caught by: [`hlSpManagerCallNamesItsCallerOnTheWire`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L311) |
| [9703](#spoke-9703) | A manager call forwards the raw call value, so inside a batch it spends ether already paid for the whole batch.<br>Caught by: [`hlSpManagerCallNamesItsCallerOnTheWire`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L311) |
| [9704](#spoke-9704) | Calls on the batch callback forward their call value instead of none, so each batched message spends the batch's ether.<br>Caught by: [`vtSpEveryOutboundSendCarriesTheAttachedValue`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L94) |
| [9705](#spoke-9705) | The manager check reads the direct caller, so inside a batch it checks the gateway instead of the initiator.<br>Caught by: [`acSpQueuedAssetDeltasComeOnlyFromAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L54) · [`acSpQueuedShareDeltasComeOnlyFromAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L70) · [`acSpEscrowCustodyMovesOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L86) · [`acSpQueueSubmissionsLeaveOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L103) |
| [9706](#spoke-9706) | The re-entrancy lock no longer checks who re-enters, so another contract can register assets or bridge shares mid-call.<br>Caught by: [`rvSpProtectedEntriesRefuseAForeignReentrantCaller`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L371) |
| [9707](#spoke-9707) | A bridge transfer sends its message before burning the shares, so the destination is told of a burn not yet made.<br>Caught by: [`hlSpBridgeBurnsBeforeItAnnounces`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L449) |
| [9708](#spoke-9708) | The transfer restriction is asked about this network instead of the destination, so a blocked destination can pass.<br>Caught by: [`rvSpBridgeRefusesAnOwnerTheRegistrarVetoes`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L355) |
| [9709](#spoke-9709) | Issuance calls mint on the share token instead of its registrar, so the registrar is skipped when shares are issued.<br>Caught by: [`acSpShareSupplyMovesOnlyThroughTheClassRegistrar`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L245) |
| [9944](#spoke-9944) | The spoke no longer checks an asset's decimals against the ceiling, so a token with more than eighteen decimals is announced to the hub.<br>Caught by: [`vtSpAssetRegistrationRespectsTheDecimalsCeiling`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L62) |

## Spoke #205

deposit moves the escrow balance without queueing the move for the hub, so the hub's view of the pool's assets falls behind.

- **Mutant:** [`205.sol`](205.sol)
- **Caught by:** [`stSpSpendableBalanceMoveIsQueuedForTheHub`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 205`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/transitions.conf --rule stSpSpendableBalanceMoveIsQueuedForTheHub`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -124,7 +124,7 @@
     {
         IEscrow escrow_ = escrow(poolId);
         escrow_.deposit(scId, asset, tokenId, amount);
-        _queueAssets(poolId, scId, asset, tokenId, amount, true);
+        // MUTATION: the deposit is not queued for the hub
 
         if (tokenId == 0) {
             SafeTransferLib.safeTransferFrom(asset, msgSender(), address(escrow_), amount);
```

## Spoke #206

A flushed asset queue keeps its outstanding slot, so the share class never again reports a complete snapshot.

- **Mutant:** [`206.sol`](206.sol)
- **Caught by:** [`stSpDrainingAQueueRowSpendsANonceAndItsSlot`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 206`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/transitions.conf --rule stSpDrainingAQueueRowSpendsANonceAndItsSlot`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -80,7 +80,7 @@
         assetQueue.deposits = 0;
         assetQueue.withdrawals = 0;
         shareQueue.nonce++;
-        shareQueue.queuedAssetCounter -= assetCounter;
+        // MUTATION: the drained row keeps its outstanding slot
 
         emit SubmitQueuedAssets(poolId, scId, assetId, data);
     }
```

## Spoke #207

issue mints local shares without queueing the issuance for the hub, so local supply moves unreported.

- **Mutant:** [`207.sol`](207.sol)
- **Caught by:** [`stSpShareSupplyMovesOnlyAsReported`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L73)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 207`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/transitions.conf --rule stSpShareSupplyMovesOnlyAsReported`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -233,7 +233,7 @@
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
 
-        snapshotQueue.queueShares(poolId, scId, shares, true);
+        // MUTATION: the issuance is minted without being queued for the hub
         registrar.mint(address(token), to, shares);
 
         emit Issue(poolId, scId, msgSender(), to, shares);
```

## Spoke #210

A flushed asset queue does not advance the nonce, so the next report reaches the hub under the same nonce.

- **Mutant:** [`210.sol`](210.sol)
- **Caught by:** [`stSpDrainingAQueueRowSpendsANonceAndItsSlot`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 210`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/transitions.conf --rule stSpDrainingAQueueRowSpendsANonceAndItsSlot`

```diff
--- a/src/core/spoke/SnapshotQueue.sol
+++ b/src/core/spoke/SnapshotQueue.sol
@@ -79,7 +79,7 @@
 
         assetQueue.deposits = 0;
         assetQueue.withdrawals = 0;
-        shareQueue.nonce++;
+        // MUTATION: the drained row is reported under the number the last one used
         shareQueue.queuedAssetCounter -= assetCounter;
 
         emit SubmitQueuedAssets(poolId, scId, assetId, data);
```

## Spoke #211

Every escrow move is queued for the hub in the opposite direction, so a deposit is reported as a withdrawal.

- **Mutant:** [`211.sol`](211.sol)
- **Caught by:** [`stSpQueuedMoveIsBackedByTheEscrow`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L114)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 211`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule stSpQueuedMoveIsBackedByTheEscrow`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -427,7 +427,7 @@
         uint128 amount,
         bool isIncrease
     ) internal {
-        snapshotQueue.queueAssets(poolId, scId, spokeRegistry.assetToId(asset, tokenId, true), amount, isIncrease);
+        snapshotQueue.queueAssets(poolId, scId, spokeRegistry.assetToId(asset, tokenId, true), amount, !isIncrease); /* MUTATION: the queue is told the opposite direction */
     }
 
     function _safeGetAssetDecimals(address asset, uint256 tokenId) internal view returns (uint8) {
```

## Spoke #216

A noted deposit is queued for the hub without crediting the escrow, so the hub is told of a move the escrow never made.

- **Mutant:** [`216.sol`](216.sol)
- **Caught by:** [`stSpQueuedMoveIsBackedByTheEscrow`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L114)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 216`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule stSpQueuedMoveIsBackedByTheEscrow`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -140,7 +140,7 @@
         payable
         enforced(poolId)
     {
-        escrow(poolId).deposit(scId, asset, tokenId, amount);
+        /* MUTATION: the escrow credit is removed */
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
 
         emit NoteDeposit(poolId, scId, msgSender(), asset, tokenId, amount);
```

## Spoke #4600

A cross chain share transfer of zero shares is accepted, so an empty transfer message is sent to the destination.

- **Mutant:** [`4600.sol`](4600.sol)
- **Caught by:** [`vtSpBridgeNeverAnnouncesAnEmptyTransfer`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4600`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule vtSpBridgeNeverAnnouncesAnEmptyTransfer`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -309,7 +309,7 @@
     ) public payable protected {
         require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
-        require(amount != 0, EmptyAmount());
+        // MUTATION: the empty amount guard is removed
 
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(share) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
```

## Spoke #4601

A cross chain share transfer may name this very network as its destination, so shares burned here are announced for a mint here.

- **Mutant:** [`4601.sol`](4601.sol)
- **Caught by:** [`vtSpBridgeNeverAnnouncesBackToThisNetwork`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4601`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule vtSpBridgeNeverAnnouncesBackToThisNetwork`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -313,7 +313,7 @@
 
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(share) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        require(centrifugeId != sender.localCentrifugeId(), LocalTransferNotAllowed());
+        // MUTATION: the local destination guard is removed
         require(registrar.canBridge(address(share), owner, centrifugeId, amount), BridgeNotAllowed());
 
         SafeTransferLib.safeTransferFrom(address(share), owner, address(this), amount);
```

## Spoke #4602

An asset the registry has never seen is announced under the null asset number, because the fresh number is minted for known assets only.

- **Mutant:** [`4602.sol`](4602.sol)
- **Caught by:** [`vtSpAssetRegistrationNeverAnnouncesTheNullId`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L43)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4602`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule vtSpAssetRegistrationNeverAnnouncesTheNullId`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -103,7 +103,7 @@
         }
 
         assetId = spokeRegistry.assetToId(asset, tokenId);
-        bool isInitialization = assetId.isNull();
+        bool isInitialization = !assetId.isNull(); // MUTATION: the fresh id is minted for a known asset, never for an unknown one
         if (isInitialization) {
             assetId = spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, tokenId);
         }
```

## Spoke #4603

An asset registration announces one decimal more than the ceiling check inspected, so a precision the pool accounting cannot represent reaches the hub.

- **Mutant:** [`4603.sol`](4603.sol)
- **Caught by:** [`vtSpAssetRegistrationRespectsTheDecimalsCeiling`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L62)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4603`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule vtSpAssetRegistrationRespectsTheDecimalsCeiling`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -109,7 +109,7 @@
         }
 
         emit RegisterAsset(centrifugeId, assetId, asset, tokenId, name, symbol, decimals, isInitialization);
-        sender.sendRegisterAsset{value: msgValue()}(centrifugeId, assetId, decimals, refund);
+        sender.sendRegisterAsset{value: msgValue()}(centrifugeId, assetId, decimals + 1, refund); // MUTATION: the announced precision is one above the checked one
     }
 
     //----------------------------------------------------------------------------------------------
```

## Spoke #4604

A bridge transfer hands the same announcement over twice, so one call costs the pool two messages and two fees.

- **Mutant:** [`4604.sol`](4604.sol)
- **Caught by:** [`vtSpOneCallHandsOverAtMostOneMessage`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L79)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4604`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule vtSpOneCallHandsOverAtMostOneMessage`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -333,6 +333,18 @@
             remoteExtraGasLimit,
             refund
         );
+        // MUTATION: the same announcement is handed over a second time
+        sender.sendInitiateTransferShares{value: msgValue()}(
+            centrifugeId,
+            poolId,
+            scId,
+            sender_.toBytes32(),
+            receiver,
+            amount,
+            extraGasLimit,
+            remoteExtraGasLimit,
+            refund
+        );
     }
 
     /// @inheritdoc ISpoke
```

## Spoke #4605

A bridge transfer pulls the shares from the named sender instead of the owner, so the wrong account is charged.

- **Mutant:** [`4605.sol`](4605.sol)
- **Caught by:** [`hlSpBridgeDebitsTheNamedOwner`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L4) · [`hlSpBridgeSpendsTheOwnersApproval`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L106)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4605`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpBridgeDebitsTheNamedOwner hlSpBridgeSpendsTheOwnersApproval`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -316,7 +316,7 @@
         require(centrifugeId != sender.localCentrifugeId(), LocalTransferNotAllowed());
         require(registrar.canBridge(address(share), owner, centrifugeId, amount), BridgeNotAllowed());
 
-        SafeTransferLib.safeTransferFrom(address(share), owner, address(this), amount);
+        SafeTransferLib.safeTransferFrom(address(share), sender_, address(this), amount); // MUTATION: the shares are pulled from the named message sender
         SafeTransferLib.safeApprove(address(share), address(registrar), amount);
         registrar.burn(address(share), address(this), amount);
 
```

## Spoke #4606

A bridge transfer parks the shares on the spoke instead of burning them, so the bridged shares exist on both chains.

- **Mutant:** [`4606.sol`](4606.sol)
- **Caught by:** [`hlSpBridgeBurnsTheBridgedShares`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L22) · [`hlSpBridgeParksNoSharesOnTheSpoke`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L40)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4606`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpBridgeBurnsTheBridgedShares hlSpBridgeParksNoSharesOnTheSpoke`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -318,7 +318,7 @@
 
         SafeTransferLib.safeTransferFrom(address(share), owner, address(this), amount);
         SafeTransferLib.safeApprove(address(share), address(registrar), amount);
-        registrar.burn(address(share), address(this), amount);
+        // MUTATION: the bridged shares are not burned
 
         emit InitiateTransferShares(centrifugeId, poolId, scId, sender_, owner, receiver, amount);
 
```

## Spoke #4607

A bridge transfer announces itself to the destination chain twice, so one burn here can be minted two times there.

- **Mutant:** [`4607.sol`](4607.sol)
- **Caught by:** [`hlSpBridgeAnnouncesExactlyOneTransfer`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L59)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4607`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpBridgeAnnouncesExactlyOneTransfer`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -333,6 +333,18 @@
             remoteExtraGasLimit,
             refund
         );
+        // MUTATION: the same announcement is handed over a second time
+        sender.sendInitiateTransferShares{value: msgValue()}(
+            centrifugeId,
+            poolId,
+            scId,
+            sender_.toBytes32(),
+            receiver,
+            amount,
+            extraGasLimit,
+            remoteExtraGasLimit,
+            refund
+        );
     }
 
     /// @inheritdoc ISpoke
```

## Spoke #4608

The outbound announcement carries the gas limit in the amount slot, so the destination mints an unrelated number.

- **Mutant:** [`4608.sol`](4608.sol)
- **Caught by:** [`hlSpBridgeAnnouncesTheBurnedAmount`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L76)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4608`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpBridgeAnnouncesTheBurnedAmount`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -328,7 +328,7 @@
             scId,
             sender_.toBytes32(),
             receiver,
-            amount,
+            extraGasLimit, // MUTATION: the gas limit travels in the amount slot
             extraGasLimit,
             remoteExtraGasLimit,
             refund
```

## Spoke #4609

The outbound announcement swaps the named sender and the named receiver, so bridged shares are minted at the destination for the wrong party.

- **Mutant:** [`4609.sol`](4609.sol)
- **Caught by:** [`hlSpBridgeAnnouncesTheNamedReceiver`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L91)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4609`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpBridgeAnnouncesTheNamedReceiver`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -326,8 +326,8 @@
             centrifugeId,
             poolId,
             scId,
-            sender_.toBytes32(),
             receiver,
+            sender_.toBytes32(), // MUTATION: the named sender and receiver are swapped
             amount,
             extraGasLimit,
             remoteExtraGasLimit,
```

## Spoke #4610

A bridge transfer also queues a revocation for the hub, so shares reminted on the destination count as destroyed.

- **Mutant:** [`4610.sol`](4610.sol)
- **Caught by:** [`hlSpBridgeReportsNoShareMovementToTheHub`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L126)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4610`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpBridgeReportsNoShareMovementToTheHub`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -310,6 +310,7 @@
         require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
         require(amount != 0, EmptyAmount());
+        snapshotQueue.queueShares(poolId, scId, amount, false); // MUTATION: the bridged burn is reported to the hub as a revocation
 
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(share) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
```

## Spoke #4611

Noting a deposit that already reached the escrow also pulls the tokens from the caller, so the holdings are paid twice.

- **Mutant:** [`4611.sol`](4611.sol)
- **Caught by:** [`hlSpNoteDepositMovesNoTokens`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L143)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4611`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpNoteDepositMovesNoTokens`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -142,6 +142,7 @@
     {
         escrow(poolId).deposit(scId, asset, tokenId, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
+        SafeTransferLib.safeTransferFrom(asset, msgSender(), address(escrow(poolId)), amount); // MUTATION: the booked deposit also pulls the tokens
 
         emit NoteDeposit(poolId, scId, msgSender(), asset, tokenId, amount);
     }
```

## Spoke #4612

The balance sheet gate no longer requires a pool manager, so any caller can move escrow, queues and share supply.

- **Mutant:** [`4612.sol`](4612.sol)
- **Caught by:** [`acSpQueuedAssetDeltasComeOnlyFromAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L54) · [`acSpQueuedShareDeltasComeOnlyFromAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L70) · [`acSpEscrowCustodyMovesOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L86) · [`acSpQueueSubmissionsLeaveOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L103) · [`acSpShareSupplyGrowsThroughTheSpokeOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L123) · [`acSpUnauthorizedCannotReduceAHoldersBalance`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L139)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4612`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpQueuedAssetDeltasComeOnlyFromAManager acSpQueuedShareDeltasComeOnlyFromAManager acSpEscrowCustodyMovesOnlyForAManager acSpQueueSubmissionsLeaveOnlyForAManager acSpShareSupplyGrowsThroughTheSpokeOnlyForAManager acSpUnauthorizedCannotReduceAHoldersBalance`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -412,7 +412,7 @@
     /// @dev Reverts unless the resolved sender is a manager for `poolId`, then applies the pool's
     ///      policy if one is installed.
     function _enforce(PoolId poolId) internal {
-        require(spokeRegistry.manager(poolId, msgSender()), NotManager());
+        // MUTATION: the pool manager seat is no longer required
 
         IPolicy policy_ = spokeRegistry.policy(poolId);
         if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), msg.data);
```

## Spoke #4613

A bridge transfer no longer checks the caller is the owner or a ward, so anyone can bridge a holder's approved shares.

- **Mutant:** [`4613.sol`](4613.sol)
- **Caught by:** [`acSpApprovalToTheSpokeIsSpentOnlyByItsOwnerAWardOrAManagersForcedTransfer`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L197)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4613`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpApprovalToTheSpokeIsSpentOnlyByItsOwnerAWardOrAManagersForcedTransfer`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -307,7 +307,7 @@
         uint128 remoteExtraGasLimit,
         address refund
     ) public payable protected {
-        require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
+        // MUTATION: the caller is no longer checked against the named owner
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
         require(amount != 0, EmptyAmount());
 
```

## Spoke #4614

A bridge transfer no longer checks the bridger seat, so an owner the pool never listed can move shares off this network.

- **Mutant:** [`4614.sol`](4614.sol)
- **Caught by:** [`acSpBridgeStartsOnlyForABridgerOrAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L160)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4614`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpBridgeStartsOnlyForABridgerOrAWard`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -308,7 +308,7 @@
         address refund
     ) public payable protected {
         require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
-        require(spokeRegistry.bridger(poolId, owner), NotBridger());
+        // MUTATION: the bridger seat of the owner is no longer required
         require(amount != 0, EmptyAmount());
 
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
```

## Spoke #4615

The request entry no longer checks its caller, so anybody can file an investor request with the hub in the pool's name.

- **Mutant:** [`4615.sol`](4615.sol)
- **Caught by:** [`acSpInvestorRequestsLeaveOnlyForTheRequestManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L178)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4615`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpInvestorRequestsLeaveOnlyForTheRequestManager`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -365,7 +365,7 @@
     ) external payable {
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
-        require(msg.sender == address(manager), NotAuthorized());
+        // MUTATION: the caller is no longer checked against the request manager
 
         sender.sendRequest{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, unpaid, refund);
     }
```

## Spoke #4616

The balance sheet gate no longer requires a pool manager, so no balance sheet entry refuses a non-manager caller.

- **Mutant:** [`4616.sol`](4616.sol)
- **Caught by:** [`rvSpDepositRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L18) · [`rvSpNoteDepositRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L32) · [`rvSpWithdrawRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L46) · [`rvSpWithdrawReservedRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L60) · [`rvSpReserveRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L75) · [`rvSpUnreserveRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L89) · [`rvSpSubmitQueuedAssetsRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L104) · [`rvSpIssueRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L118) · [`rvSpRevokeRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L132) · [`rvSpWithdrawSharesRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L146) · [`rvSpSubmitQueuedSharesRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L160) · [`rvSpTransferSharesFromRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L174)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4616`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpDepositRefusesANonManager rvSpNoteDepositRefusesANonManager rvSpWithdrawRefusesANonManager rvSpWithdrawReservedRefusesANonManager rvSpReserveRefusesANonManager rvSpUnreserveRefusesANonManager rvSpSubmitQueuedAssetsRefusesANonManager rvSpIssueRefusesANonManager rvSpRevokeRefusesANonManager rvSpWithdrawSharesRefusesANonManager rvSpSubmitQueuedSharesRefusesANonManager rvSpTransferSharesFromRefusesANonManager`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -412,7 +412,7 @@
     /// @dev Reverts unless the resolved sender is a manager for `poolId`, then applies the pool's
     ///      policy if one is installed.
     function _enforce(PoolId poolId) internal {
-        require(spokeRegistry.manager(poolId, msgSender()), NotManager());
+        // MUTATION: the pool manager seat is no longer required
 
         IPolicy policy_ = spokeRegistry.policy(poolId);
         if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), msg.data);
```

## Spoke #4617

The ward gate no longer looks at the caller, so rewiring the spoke and handing out or withdrawing its keys is open to everyone.

- **Mutant:** [`4617.sol`](4617.sol)
- **Caught by:** [`rvSpFileRefusesANonWardOrAnUnknownName`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L4) · [`rvSpRelyRefusesANonWard`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L269) · [`rvSpDenyRefusesANonWard`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L282)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4617`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpFileRefusesANonWardOrAnUnknownName rvSpRelyRefusesANonWard rvSpDenyRefusesANonWard`

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

## Spoke #4618

Balance sheet entries also demand a ward seat, so a plain pool manager can no longer submit queued positions.

- **Mutant:** [`4618.sol`](4618.sol)
- **Caught by:** [`rvSpSubmitQueuedAssetsIsNeverRefusedToASeatedManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L295) · [`rvSpSubmitQueuedSharesIsNeverRefusedToASeatedManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L317)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4618`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpSubmitQueuedAssetsIsNeverRefusedToASeatedManager rvSpSubmitQueuedSharesIsNeverRefusedToASeatedManager`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -412,7 +412,7 @@
     /// @dev Reverts unless the resolved sender is a manager for `poolId`, then applies the pool's
     ///      policy if one is installed.
     function _enforce(PoolId poolId) internal {
-        require(spokeRegistry.manager(poolId, msgSender()), NotManager());
+        require(spokeRegistry.manager(poolId, msgSender()) && wards[msgSender()] == 1, NotManager()); // MUTATION: a ward seat is demanded on top of the manager seat
 
         IPolicy policy_ = spokeRegistry.policy(poolId);
         if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), msg.data);
```

## Spoke #4619

The spoke side manager call is closed behind the pool manager seat, so the entry the interface promises to every caller refuses one.

- **Mutant:** [`4619.sol`](4619.sol)
- **Caught by:** [`rvSpManagerCallIsNeverRefusedToAnyCaller`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L339)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4619`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpManagerCallIsNeverRefusedToAnyCaller`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -374,6 +374,7 @@
     function managerCall(PoolId poolId, bytes32 target, bytes calldata payload, uint128 extraGasLimit, address refund)
         external
         payable
+        enforced(poolId) // MUTATION: the open entry is closed behind the pool manager seat
     {
         emit ManagerCall(poolId.centrifugeId(), poolId, target, payload, msgSender());
 
```

## Spoke #4620

A bridge transfer no longer checks the caller is the owner or a ward, so a stranger can bridge the owner's shares.

- **Mutant:** [`4620.sol`](4620.sol)
- **Caught by:** [`rvSpBridgeRefusesAStrangerToTheOwner`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4620`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpBridgeRefusesAStrangerToTheOwner`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -307,7 +307,7 @@
         uint128 remoteExtraGasLimit,
         address refund
     ) public payable protected {
-        require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
+        // MUTATION: the caller is no longer checked against the named owner
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
         require(amount != 0, EmptyAmount());
 
```

## Spoke #4621

A bridge transfer no longer checks the bridger seat, so an owner the pool never listed can still move holdings off this network.

- **Mutant:** [`4621.sol`](4621.sol)
- **Caught by:** [`rvSpBridgeRefusesANonBridgerOwner`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L205)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4621`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpBridgeRefusesANonBridgerOwner`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -308,7 +308,7 @@
         address refund
     ) public payable protected {
         require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
-        require(spokeRegistry.bridger(poolId, owner), NotBridger());
+        // MUTATION: the bridger seat of the owner is no longer required
         require(amount != 0, EmptyAmount());
 
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
```

## Spoke #4622

A bridge transfer of nothing is accepted, so a burn of zero is announced to the destination chain instead of being refused.

- **Mutant:** [`4622.sol`](4622.sol)
- **Caught by:** [`rvSpBridgeRefusesAZeroAmount`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L221)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4622`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpBridgeRefusesAZeroAmount`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -309,7 +309,7 @@
     ) public payable protected {
         require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
-        require(amount != 0, EmptyAmount());
+        // MUTATION: the empty amount guard is removed
 
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(share) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
```

## Spoke #4623

A bridge transfer addressed to this very network is accepted, so shares are burned here for a mint that is asked of this same chain.

- **Mutant:** [`4623.sol`](4623.sol)
- **Caught by:** [`rvSpBridgeRefusesALocalDestination`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L237)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4623`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpBridgeRefusesALocalDestination`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -313,7 +313,7 @@
 
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(share) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        require(centrifugeId != sender.localCentrifugeId(), LocalTransferNotAllowed());
+        // MUTATION: the local destination guard is removed
         require(registrar.canBridge(address(share), owner, centrifugeId, amount), BridgeNotAllowed());
 
         SafeTransferLib.safeTransferFrom(address(share), owner, address(this), amount);
```

## Spoke #4624

The request entry no longer checks its caller, so a request reaches the hub for a caller who is not the pool's registered request manager.

- **Mutant:** [`4624.sol`](4624.sol)
- **Caught by:** [`rvSpRequestRefusesAnyCallerButTheRegisteredManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L253)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 4624`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpRequestRefusesAnyCallerButTheRegisteredManager`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -365,7 +365,7 @@
     ) external payable {
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
-        require(msg.sender == address(manager), NotAuthorized());
+        // MUTATION: the caller is no longer checked against the request manager
 
         sender.sendRequest{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, unpaid, refund);
     }
```

## Spoke #5300

file drops its authorisation, so any caller repoints the gateway and the outbound message sender.

- **Mutant:** [`5300.sol`](5300.sol)
- **Caught by:** [`acSpGatewayIsRepointedOnlyByAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L21) · [`acSpMessageSenderIsRepointedOnlyByAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 5300`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpGatewayIsRepointedOnlyByAWard acSpMessageSenderIsRepointedOnlyByAWard`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -69,7 +69,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpoke
-    function file(bytes32 what, address data) external auth {
+    function file(bytes32 what, address data) external { // MUTATION: authorisation dropped
         if (what == "gateway") gateway = IGateway(data);
         else if (what == "sender") sender = ISpokeMessageSender(data);
         else revert FileUnrecognizedParam();
```

## Spoke #5301

rely drops its authorisation, so any caller adds itself or anybody else to the ward list.

- **Mutant:** [`5301.sol`](5301.sol)
- **Caught by:** [`acSpWardListMovesOnlyForAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 5301`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpWardListMovesOnlyForAWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -22,7 +22,7 @@
     }
 
     /// @inheritdoc IAuth
-    function rely(address user) public auth {
+    function rely(address user) public { // MUTATION: authorisation dropped
         wards[user] = 1;
         emit Rely(user);
     }
```

## Spoke #5302

deny drops its authorisation, so any caller strips a ward of its permissions.

- **Mutant:** [`5302.sol`](5302.sol)
- **Caught by:** [`acSpWardListMovesOnlyForAWard`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 5302`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpWardListMovesOnlyForAWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -28,7 +28,7 @@
     }
 
     /// @inheritdoc IAuth
-    function deny(address user) public auth {
+    function deny(address user) public { // MUTATION: authorisation dropped
         wards[user] = 0;
         emit Deny(user);
     }
```

## Spoke #6000

Asset registration is closed behind the ward gate, so an ordinary caller can no longer register a new asset.

- **Mutant:** [`6000.sol`](6000.sol)
- **Caught by:** [`rcSpRegisterAssetMintsAFreshIdForAnUnknownErc20`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6000`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpRegisterAssetMintsAFreshIdForAnUnknownErc20`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -85,6 +85,7 @@
         external
         payable
         protected
+        auth // MUTATION: asset registration is closed behind the ward gate
         returns (AssetId assetId)
     {
         uint8 decimals = _safeGetAssetDecimals(asset, tokenId);
```

## Spoke #6001

An asset announcement always mints a fresh id, so a pair the registry already carries can never be announced a second time.

- **Mutant:** [`6001.sol`](6001.sol)
- **Caught by:** [`rcSpRegisterAssetReannouncesTheStoredIdIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L25)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6001`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpRegisterAssetReannouncesTheStoredIdIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -104,9 +104,8 @@
 
         assetId = spokeRegistry.assetToId(asset, tokenId);
         bool isInitialization = assetId.isNull();
-        if (isInitialization) {
-            assetId = spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, tokenId);
-        }
+        // MUTATION: the mint no longer asks whether the pair is already on file
+        assetId = spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, tokenId);
 
         emit RegisterAsset(centrifugeId, assetId, asset, tokenId, name, symbol, decimals, isInitialization);
         sender.sendRegisterAsset{value: msgValue()}(centrifugeId, assetId, decimals, refund);
```

## Spoke #6002

A tranche is minted its id under the plain token row of the registry, so the tranche itself is left without one.

- **Mutant:** [`6002.sol`](6002.sol)
- **Caught by:** [`rcSpRegisterAssetMintsAFreshIdForAnErc6909Tranche`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L45)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6002`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpRegisterAssetMintsAFreshIdForAnErc6909Tranche`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -105,7 +105,7 @@
         assetId = spokeRegistry.assetToId(asset, tokenId);
         bool isInitialization = assetId.isNull();
         if (isInitialization) {
-            assetId = spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, tokenId);
+            assetId = spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, 0); // MUTATION: the tranche is filed under the plain token row
         }
 
         emit RegisterAsset(centrifugeId, assetId, asset, tokenId, name, symbol, decimals, isInitialization);
```

## Spoke #6003

The decimals ceiling is read as an exclusive bound, so a token sitting exactly at the precision the pool accounting supports is turned away.

- **Mutant:** [`6003.sol`](6003.sol)
- **Caught by:** [`rcSpRegisterAssetAtTheDecimalsCeilingIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L65)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6003`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpRegisterAssetAtTheDecimalsCeilingIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -88,7 +88,7 @@
         returns (AssetId assetId)
     {
         uint8 decimals = _safeGetAssetDecimals(asset, tokenId);
-        require(decimals <= MAX_DECIMALS, TooManyDecimals());
+        require(decimals < MAX_DECIMALS, TooManyDecimals()); // MUTATION: the ceiling itself is now refused
 
         string memory name;
         string memory symbol;
```

## Spoke #6004

A deposit is queued for the hub in the opposite direction, so money arriving in the pool is reported as money leaving it.

- **Mutant:** [`6004.sol`](6004.sol)
- **Caught by:** [`rcSpFirstDepositIntoAnEmptyRowIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L82) · [`rcSpDepositIntoAHoldingRowIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L104)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6004`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpFirstDepositIntoAnEmptyRowIsReachable rcSpDepositIntoAHoldingRowIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -124,7 +124,7 @@
     {
         IEscrow escrow_ = escrow(poolId);
         escrow_.deposit(scId, asset, tokenId, amount);
-        _queueAssets(poolId, scId, asset, tokenId, amount, true);
+        _queueAssets(poolId, scId, asset, tokenId, amount, false); // MUTATION: the credit is reported to the hub as a decrease
 
         if (tokenId == 0) {
             SafeTransferLib.safeTransferFrom(asset, msgSender(), address(escrow_), amount);
```

## Spoke #6005

A plain token deposit credits the pool escrow without charging the payer, so the payer keeps the funds.

- **Mutant:** [`6005.sol`](6005.sol)
- **Caught by:** [`rcSpDepositOfThePayersWholeBalanceIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L128)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6005`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpDepositOfThePayersWholeBalanceIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -127,7 +127,7 @@
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
 
         if (tokenId == 0) {
-            SafeTransferLib.safeTransferFrom(asset, msgSender(), address(escrow_), amount);
+            // MUTATION: the payer is never charged for the deposit
         } else {
             require(IERC6909(asset).transferFrom(msgSender(), address(escrow_), tokenId, amount), TransferFailed());
         }
```

## Spoke #6006

A deposit of a tranche credits the pool escrow without moving any units, so the escrow is told it holds tranche units that never arrived.

- **Mutant:** [`6006.sol`](6006.sol)
- **Caught by:** [`rcSpDepositOfAnErc6909TrancheIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L148)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6006`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpDepositOfAnErc6909TrancheIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -129,7 +129,7 @@
         if (tokenId == 0) {
             SafeTransferLib.safeTransferFrom(asset, msgSender(), address(escrow_), amount);
         } else {
-            require(IERC6909(asset).transferFrom(msgSender(), address(escrow_), tokenId, amount), TransferFailed());
+            // MUTATION: the tranche units are never pulled from the payer
         }
         emit Deposit(poolId, scId, msgSender(), asset, tokenId, amount);
     }
```

## Spoke #6007

Noting a deposit queues the arrival for the hub without crediting the escrow, so custody never records the holding.

- **Mutant:** [`6007.sol`](6007.sol)
- **Caught by:** [`rcSpNoteDepositCreditsCustodyWithoutMovingTokens`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L172)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6007`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpNoteDepositCreditsCustodyWithoutMovingTokens`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -140,7 +140,7 @@
         payable
         enforced(poolId)
     {
-        escrow(poolId).deposit(scId, asset, tokenId, amount);
+        // MUTATION: the noted deposit books nothing into custody
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
 
         emit NoteDeposit(poolId, scId, msgSender(), asset, tokenId, amount);
```

## Spoke #6008

A deposit of nothing is refused, so a pool cannot use the entry to report an arrival of size zero.

- **Mutant:** [`6008.sol`](6008.sol)
- **Caught by:** [`rcSpZeroAmountDepositIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L196)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6008`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpZeroAmountDepositIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -122,6 +122,7 @@
         payable
         enforced(poolId)
     {
+        require(amount != 0, EmptyAmount()); // MUTATION: a deposit of nothing is refused
         IEscrow escrow_ = escrow(poolId);
         escrow_.deposit(scId, asset, tokenId, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
```

## Spoke #6009

A withdrawal debits custody and reports it to the hub without paying out, so the receiver gets nothing.

- **Mutant:** [`6009.sol`](6009.sol)
- **Caught by:** [`rcSpWithdrawPaysTheReceiverIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L217) · [`rcSpWithdrawToTheCallerThemselvesIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L281)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6009`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpWithdrawPaysTheReceiverIsReachable rcSpWithdrawToTheCallerThemselvesIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -159,7 +159,7 @@
 
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
-        escrow_.authTransferTo(asset, tokenId, receiver, amount);
+        // MUTATION: the receiver is never paid the tokens
 
         emit Withdraw(poolId, scId, asset, tokenId, receiver, amount);
     }
```

## Spoke #6010

A withdrawal requires a free balance strictly above the amount, so the whole free balance can never be withdrawn.

- **Mutant:** [`6010.sol`](6010.sol)
- **Caught by:** [`rcSpWithdrawEmptiesTheFreeBalanceExactlyIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L242) · [`rcSpWithdrawLeavesTheHeldPartBehindIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L260)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6010`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpWithdrawEmptiesTheFreeBalanceExactlyIsReachable rcSpWithdrawLeavesTheHeldPartBehindIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -156,6 +156,7 @@
         uint128 amount
     ) external payable enforced(poolId) {
         IEscrow escrow_ = escrow(poolId);
+        require(amount < escrow_.availableBalanceOf(scId, asset, tokenId), IEscrow.InsufficientBalance(asset, tokenId, amount, 0)); // MUTATION: the whole free balance is no longer payable
 
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
```

## Spoke #6011

Placing a hold is reported to the hub as an increase, so funds set aside are announced as arriving.

- **Mutant:** [`6011.sol`](6011.sol)
- **Caught by:** [`rcSpFirstHoldOnARowIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L303) · [`rcSpHoldBeyondTheRowsCustodyIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L933)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6011`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpFirstHoldOnARowIsReachable rcSpHoldBeyondTheRowsCustodyIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -195,7 +195,7 @@
         bytes32 reason
     ) external payable enforced(poolId) {
         escrow(poolId).reserve(scId, asset, tokenId, amount, reserver, reason);
-        _queueAssets(poolId, scId, asset, tokenId, amount, false);
+        _queueAssets(poolId, scId, asset, tokenId, amount, true); // MUTATION: the hold is reported to the hub as an increase
     }
 
     /// @inheritdoc ISpoke
```

## Spoke #6012

A hold is reported to the hub but never booked in escrow, so the funds stay spendable.

- **Mutant:** [`6012.sol`](6012.sol)
- **Caught by:** [`rcSpHoldOnTheWholeFreeBalanceIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L326) · [`rcSpHoldThenReleaseRoundTripIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L850)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6012`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpHoldOnTheWholeFreeBalanceIsReachable rcSpHoldThenReleaseRoundTripIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -194,7 +194,7 @@
         address reserver,
         bytes32 reason
     ) external payable enforced(poolId) {
-        escrow(poolId).reserve(scId, asset, tokenId, amount, reserver, reason);
+        // MUTATION: the hold is never booked on the escrow row
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
     }
 
```

## Spoke #6013

Lifting a hold is reported to the hub as a decrease, so funds returning to the accounted holding are announced as funds leaving it.

- **Mutant:** [`6013.sol`](6013.sol)
- **Caught by:** [`rcSpReleaseOfTheWholeHoldIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L350)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6013`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpReleaseOfTheWholeHoldIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -209,7 +209,7 @@
         bytes32 reason
     ) external payable enforced(poolId) {
         escrow(poolId).unreserve(scId, asset, tokenId, amount, reserver, reason);
-        _queueAssets(poolId, scId, asset, tokenId, amount, true);
+        _queueAssets(poolId, scId, asset, tokenId, amount, false); // MUTATION: the release is reported to the hub as a decrease
     }
 
     /// @inheritdoc ISpoke
```

## Spoke #6014

Paying held funds out reports the departure to the hub again, so a decrease already announced at hold time counts twice.

- **Mutant:** [`6014.sol`](6014.sol)
- **Caught by:** [`rcSpWithdrawReservedPaysHeldFundsOutIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L375) · [`rcSpHoldThenPayOutIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L776)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6014`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpWithdrawReservedPaysHeldFundsOutIsReachable rcSpHoldThenPayOutIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -180,6 +180,7 @@
         escrow_.unreserve(scId, asset, tokenId, amount, reserver, reason);
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
         escrow_.authTransferTo(asset, tokenId, receiver, amount);
+        _queueAssets(poolId, scId, asset, tokenId, amount, false); // MUTATION: the payout of held funds is reported to the hub again
 
         emit Withdraw(poolId, scId, asset, tokenId, receiver, amount);
     }
```

## Spoke #6015

An issuance is queued for the hub as a revocation, so shares being created are reported to the hub as shares destroyed.

- **Mutant:** [`6015.sol`](6015.sol)
- **Caught by:** [`rcSpIssueMintsSharesIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L401) · [`rcSpZeroShareIssuanceIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L424)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6015`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpIssueMintsSharesIsReachable rcSpZeroShareIssuanceIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -233,7 +233,7 @@
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
 
-        snapshotQueue.queueShares(poolId, scId, shares, true);
+        snapshotQueue.queueShares(poolId, scId, shares, false); // MUTATION: the mint is reported to the hub as a revocation
         registrar.mint(address(token), to, shares);
 
         emit Issue(poolId, scId, msgSender(), to, shares);
```

## Spoke #6016

A revocation pulls the shares onto the spoke without destroying them, so supply the hub was told had gone still exists.

- **Mutant:** [`6016.sol`](6016.sol)
- **Caught by:** [`rcSpRevokeBurnsTheCallersSharesIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L446) · [`rcSpRevokeDownToAnEmptyClassIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L472)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6016`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpRevokeBurnsTheCallersSharesIsReachable rcSpRevokeDownToAnEmptyClassIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -247,7 +247,7 @@
         snapshotQueue.queueShares(poolId, scId, shares, false);
         SafeTransferLib.safeTransferFrom(address(token), msgSender(), address(this), shares);
         SafeTransferLib.safeApprove(address(token), address(registrar), shares);
-        registrar.burn(address(token), address(this), shares);
+        // MUTATION: the pulled shares are parked on the spoke instead of being destroyed
 
         emit Revoke(poolId, scId, msgSender(), msgSender(), shares);
     }
```

## Spoke #6017

Handing custodied shares to an investor moves nothing, so the pool escrow keeps every share a claim was meant to release.

- **Mutant:** [`6017.sol`](6017.sol)
- **Caught by:** [`rcSpWithdrawSharesHandsCustodyOutIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L492) · [`rcSpIssueThenWithdrawSharesIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L801)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6017`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpWithdrawSharesHandsCustodyOutIsReachable rcSpIssueThenWithdrawSharesIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -260,7 +260,7 @@
     {
         IERC20 token = spokeRegistry.shareToken(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        escrow(poolId).authTransferTo(address(token), 0, receiver, amount);
+        // MUTATION: custody keeps the shares instead of handing them to the receiver
 
         emit WithdrawShares(poolId, scId, receiver, amount);
     }
```

## Spoke #6018

A forced share transfer moves the holding the wrong way, so the account meant to receive the shares is the one that pays them.

- **Mutant:** [`6018.sol`](6018.sol)
- **Caught by:** [`rcSpTransferSharesFromMovesAHoldingIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L518)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6018`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpTransferSharesFromMovesAHoldingIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -286,7 +286,7 @@
     ) external payable enforced(poolId) {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        registrar.authTransferFrom(address(token), sender_, from, to, amount);
+        registrar.authTransferFrom(address(token), sender_, to, from, amount); // MUTATION: the holding moves in the opposite direction
         emit TransferSharesFrom(poolId, scId, sender_, from, to, amount);
     }
 
```

## Spoke #6019

Submitting a pool's asset report drains the queue but never sends it, so the cleared flows never reach the hub.

- **Mutant:** [`6019.sol`](6019.sol)
- **Caught by:** [`rcSpSubmitQueuedAssetsReportsToTheHubIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L540) · [`rcSpDepositThenSubmitQueuedAssetsIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L825)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6019`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpSubmitQueuedAssetsReportsToTheHubIsReachable rcSpDepositThenSubmitQueuedAssetsIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -221,7 +221,7 @@
         address refund
     ) external payable enforced(poolId) {
         ISpokeMessageSender.UpdateData memory data = snapshotQueue.flushAssets(poolId, scId, assetId);
-        sender.sendUpdateAssets{value: msgValue()}(poolId, scId, assetId, data, extraGasLimit, refund);
+        // MUTATION: the asset report never leaves the spoke
     }
 
     //----------------------------------------------------------------------------------------------
```

## Spoke #6020

Submitting a pool's share report drains the queue but never sends it, so the cleared share movements never reach the hub.

- **Mutant:** [`6020.sol`](6020.sol)
- **Caught by:** [`rcSpSubmitQueuedSharesWithNoExtraGasIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L559)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6020`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpSubmitQueuedSharesWithNoExtraGasIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -272,7 +272,7 @@
         enforced(poolId)
     {
         ISpokeMessageSender.UpdateData memory data = snapshotQueue.flushShares(poolId, scId);
-        sender.sendUpdateShares{value: msgValue()}(poolId, scId, data, extraGasLimit, refund);
+        // MUTATION: the share report never leaves the spoke
     }
 
     /// @inheritdoc ISpoke
```

## Spoke #6021

The bridge admits a ward acting for somebody else and nobody else, so a holder can no longer send their own shares to another network.

- **Mutant:** [`6021.sol`](6021.sol)
- **Caught by:** [`rcSpBridgeDrivenByTheOwnerIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L578) · [`rcSpBridgeThroughTheShortEntryPointIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L654)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6021`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpBridgeDrivenByTheOwnerIsReachable rcSpBridgeThroughTheShortEntryPointIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -307,7 +307,7 @@
         uint128 remoteExtraGasLimit,
         address refund
     ) public payable protected {
-        require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
+        require(msgSender() != owner && wards[msgSender()] == 1, NotAuthorized()); // MUTATION: only a ward acting for somebody else may bridge
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
         require(amount != 0, EmptyAmount());
 
```

## Spoke #6022

The bridge requires the caller to be both the owner and a ward, so a ward can no longer bridge for somebody else.

- **Mutant:** [`6022.sol`](6022.sol)
- **Caught by:** [`rcSpBridgeDrivenByAWardForTheOwnerIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L605)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6022`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpBridgeDrivenByAWardForTheOwnerIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -307,7 +307,7 @@
         uint128 remoteExtraGasLimit,
         address refund
     ) public payable protected {
-        require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
+        require(msgSender() == owner && wards[msgSender()] == 1, NotAuthorized()); // MUTATION: the caller must be the owner and a ward at once
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
         require(amount != 0, EmptyAmount());
 
```

## Spoke #6023

The outbound announcement of a bridge carries one unit less than was burned here, so every transfer strands a unit that exists on no network.

- **Mutant:** [`6023.sol`](6023.sol)
- **Caught by:** [`rcSpBridgeOfTheWholeHoldingIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L630)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6023`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpBridgeOfTheWholeHoldingIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -328,7 +328,7 @@
             scId,
             sender_.toBytes32(),
             receiver,
-            amount,
+            amount - 1, // MUTATION: the announcement carries one unit less than was burned
             extraGasLimit,
             remoteExtraGasLimit,
             refund
```

## Spoke #6024

An investor request from the request manager is accepted but never relayed, so the hub never receives it.

- **Mutant:** [`6024.sol`](6024.sol)
- **Caught by:** [`rcSpPaidRequestIsRelayedIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L675) · [`rcSpUnpaidRequestIsRelayedIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L695)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6024`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpPaidRequestIsRelayedIsReachable rcSpUnpaidRequestIsRelayedIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -367,7 +367,7 @@
         require(address(manager) != address(0), InvalidRequestManager());
         require(msg.sender == address(manager), NotAuthorized());
 
-        sender.sendRequest{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, unpaid, refund);
+        // MUTATION: the investor request never leaves the spoke
     }
 
     /// @inheritdoc ISpoke
```

## Spoke #6025

managerCall now requires the pool manager role, so a caller without it can no longer relay a call to the hub.

- **Mutant:** [`6025.sol`](6025.sol)
- **Caught by:** [`rcSpManagerCallFromAnUnseatedCallerIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L715)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6025`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpManagerCallFromAnUnseatedCallerIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -374,6 +374,7 @@
     function managerCall(PoolId poolId, bytes32 target, bytes calldata payload, uint128 extraGasLimit, address refund)
         external
         payable
+        enforced(poolId) // MUTATION: the relay is closed behind the pool manager seat
     {
         emit ManagerCall(poolId.centrifugeId(), poolId, target, payload, msgSender());
 
```

## Spoke #6026

Granting authority announces the new seat without writing it, so an account told it was given the keys never actually holds them.

- **Mutant:** [`6026.sol`](6026.sol)
- **Caught by:** [`rcSpRelyThenDenyRoundTripIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L736)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6026`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpRelyThenDenyRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -23,7 +23,7 @@
 
     /// @inheritdoc IAuth
     function rely(address user) public auth {
-        wards[user] = 1;
+        // MUTATION: the fresh seat is never written
         emit Rely(user);
     }
 
```

## Spoke #6027

Withdrawing authority announces the removal without clearing the seat, so a key that was taken back is still held.

- **Mutant:** [`6027.sol`](6027.sol)
- **Caught by:** [`rcSpRelyThenDenyRoundTripIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L736)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6027`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpRelyThenDenyRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        // MUTATION: the seat is left in place
         emit Deny(user);
     }
 }
```

## Spoke #6028

withdraw pays an ERC6909 asset out under token id zero, so the receiver never gets the units it was owed.

- **Mutant:** [`6028.sol`](6028.sol)
- **Caught by:** [`rcSpWithdrawOfAnErc6909TrancheIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L875)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6028`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpWithdrawOfAnErc6909TrancheIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -159,7 +159,7 @@
 
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
-        escrow_.authTransferTo(asset, tokenId, receiver, amount);
+        escrow_.authTransferTo(asset, 0, receiver, amount); // MUTATION: a tranche payout is attempted as a plain token transfer
 
         emit Withdraw(poolId, scId, asset, tokenId, receiver, amount);
     }
```

## Spoke #6029

A deposit moves the escrow row without reporting the arrival to the hub, so only one leg of a round trip is ever announced.

- **Mutant:** [`6029.sol`](6029.sol)
- **Caught by:** [`rcSpDepositThenWithdrawRoundTripIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L755)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6029`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpDepositThenWithdrawRoundTripIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -124,7 +124,7 @@
     {
         IEscrow escrow_ = escrow(poolId);
         escrow_.deposit(scId, asset, tokenId, amount);
-        _queueAssets(poolId, scId, asset, tokenId, amount, true);
+        // MUTATION: the deposit is never reported to the hub
 
         if (tokenId == 0) {
             SafeTransferLib.safeTransferFrom(asset, msgSender(), address(escrow_), amount);
```

## Spoke #6030

file answers to "sender" on the gateway leg, so the gateway cannot be repointed and a new sender lands in the gateway slot.

- **Mutant:** [`6030.sol`](6030.sol)
- **Caught by:** [`rcSpFileRepointsTheGatewayIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L903) · [`rcSpFileRepointsTheMessageSenderIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L918)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6030`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpFileRepointsTheGatewayIsReachable rcSpFileRepointsTheMessageSenderIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -70,7 +70,7 @@
 
     /// @inheritdoc ISpoke
     function file(bytes32 what, address data) external auth {
-        if (what == "gateway") gateway = IGateway(data);
+        if (what == "sender") gateway = IGateway(data); // MUTATION: both legs answer to the same parameter name
         else if (what == "sender") sender = ISpokeMessageSender(data);
         else revert FileUnrecognizedParam();
         emit File(what, data);
```

## Spoke #6031

A plain token deposit credits the pool escrow without charging the payer, so custody is booked for tokens that never moved.

- **Mutant:** [`6031.sol`](6031.sol)
- **Caught by:** [`stSpEscrowCustodyMovesWithItsTokens`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_transitions.spec#L97)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6031`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/transitions.conf --rule stSpEscrowCustodyMovesWithItsTokens`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -127,7 +127,7 @@
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
 
         if (tokenId == 0) {
-            SafeTransferLib.safeTransferFrom(asset, msgSender(), address(escrow_), amount);
+            // MUTATION: the payer is never charged for the deposit
         } else {
             require(IERC6909(asset).transferFrom(msgSender(), address(escrow_), tokenId, amount), TransferFailed());
         }
```

## Spoke #6033

the queue lookup no longer insists the (asset, tokenId) pair is registered, so a queued row can name an asset id the registry never minted.

- **Mutant:** [`6033.sol`](6033.sol)
- **Caught by:** [`queuedAssetRowImpliesRegisteredAsset`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L23) · [`escrowedRowImpliesRegisteredAsset`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L29)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6033`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/valid_state.conf --rule queuedAssetRowImpliesRegisteredAsset escrowedRowImpliesRegisteredAsset`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -427,7 +427,7 @@
         uint128 amount,
         bool isIncrease
     ) internal {
-        snapshotQueue.queueAssets(poolId, scId, spokeRegistry.assetToId(asset, tokenId, true), amount, isIncrease);
+        snapshotQueue.queueAssets(poolId, scId, spokeRegistry.assetToId(asset, tokenId, false), amount, isIncrease); // MUTATION: the registry lookup no longer insists the pair is known
     }
 
     function _safeGetAssetDecimals(address asset, uint256 tokenId) internal view returns (uint8) {
```

## Spoke #6034

noteDeposit drops its manager and policy gate, so anyone can book custody and queue work for a pool the spoke never created.

- **Mutant:** [`6034.sol`](6034.sol)
- **Caught by:** [`escrowedCustodyImpliesCreatedPool`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L35) · [`queueActivityImpliesCreatedPool`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L40)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6034`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/valid_state.conf --rule escrowedCustodyImpliesCreatedPool queueActivityImpliesCreatedPool`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -138,8 +138,7 @@
     function noteDeposit(PoolId poolId, ShareClassId scId, address asset, uint256 tokenId, uint128 amount)
         external
         payable
-        enforced(poolId)
-    {
+    { // MUTATION: removed the pool gate
         escrow(poolId).deposit(scId, asset, tokenId, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
 
```

## Spoke #6036

registerAsset builds the asset id from the destination chain instead of this spoke's own, so a local asset carries a foreign network.

- **Mutant:** [`6036.sol`](6036.sol)
- **Caught by:** [`registeredAssetIsLocal`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L46)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6036`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/valid_state.conf --rule registeredAssetIsLocal`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -105,7 +105,7 @@
         assetId = spokeRegistry.assetToId(asset, tokenId);
         bool isInitialization = assetId.isNull();
         if (isInitialization) {
-            assetId = spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, tokenId);
+            assetId = spokeRegistry.createAssetId(centrifugeId, asset, tokenId); // MUTATION: the destination chain is minted into the id instead of this spoke's own
         }
 
         emit RegisterAsset(centrifugeId, assetId, asset, tokenId, name, symbol, decimals, isInitialization);
```

## Spoke #6037

A deposit of a plain token credits the pool escrow without ever charging the payer, so custody is booked against tokens that never arrived.

- **Mutant:** [`6037.sol`](6037.sol)
- **Caught by:** [`escrowCustodyIsBackedOrNoted`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_valid_state.spec#L53)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6037`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/valid_state.conf --rule escrowCustodyIsBackedOrNoted`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -127,7 +127,7 @@
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
 
         if (tokenId == 0) {
-            SafeTransferLib.safeTransferFrom(asset, msgSender(), address(escrow_), amount);
+            // MUTATION: the payer is never charged for the deposit
         } else {
             require(IERC6909(asset).transferFrom(msgSender(), address(escrow_), tokenId, amount), TransferFailed());
         }
```

## Spoke #6038

withdraw drops the escrow's book but never moves the token, so custody falls while the tokens stay put.

- **Mutant:** [`6038.sol`](6038.sol)
- **Caught by:** [`hlSpWithdrawMovesTokensAndBookTogether`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L589)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6038`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpWithdrawMovesTokensAndBookTogether`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -159,7 +159,7 @@
 
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
-        escrow_.authTransferTo(asset, tokenId, receiver, amount);
+        // MUTATION: the token never leaves the escrow
 
         emit Withdraw(poolId, scId, asset, tokenId, receiver, amount);
     }
```

## Spoke #6039

withdrawReserved moves the token but never drops the escrow's book, so tokens leave while custody still claims them.

- **Mutant:** [`6039.sol`](6039.sol)
- **Caught by:** [`hlSpWithdrawReservedMovesTokensAndBookTogether`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L611)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 6039`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpWithdrawReservedMovesTokensAndBookTogether`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -178,7 +178,7 @@
         IEscrow escrow_ = escrow(poolId);
 
         escrow_.unreserve(scId, asset, tokenId, amount, reserver, reason);
-        escrow_.withdraw(scId, asset, tokenId, receiver, amount);
+        // MUTATION: the book is never dropped for the reserved withdrawal
         escrow_.authTransferTo(asset, tokenId, receiver, amount);
 
         emit Withdraw(poolId, scId, asset, tokenId, receiver, amount);
```

## Spoke #8500

Revocation force pulls the caller's shares instead of using their approval, so the approval stays unspent.

- **Mutant:** [`8500.sol`](8500.sol)
- **Caught by:** [`hlSpRevokeSpendsTheCallersApproval`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L161)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8500`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpRevokeSpendsTheCallersApproval`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -245,7 +245,7 @@
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
 
         snapshotQueue.queueShares(poolId, scId, shares, false);
-        SafeTransferLib.safeTransferFrom(address(token), msgSender(), address(this), shares);
+        registrar.authTransferFrom(address(token), msgSender(), msgSender(), address(this), shares); // MUTATION: the shares are force pulled without the caller's approval
         SafeTransferLib.safeApprove(address(token), address(registrar), shares);
         registrar.burn(address(token), address(this), shares);
 
```

## Spoke #8501

A manager's forced share transfer forwards the holder as sender, so the named sender's approval is never spent.

- **Mutant:** [`8501.sol`](8501.sol)
- **Caught by:** [`hlSpTransferSharesFromSpendsTheNamedSendersApproval`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L178)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8501`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpTransferSharesFromSpendsTheNamedSendersApproval`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -286,7 +286,7 @@
     ) external payable enforced(poolId) {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        registrar.authTransferFrom(address(token), sender_, from, to, amount);
+        registrar.authTransferFrom(address(token), from, from, to, amount); // MUTATION: the holder is forwarded as the sender
         emit TransferSharesFrom(poolId, scId, sender_, from, to, amount);
     }
 
```

## Spoke #8502

A deposit is paid out of the asset contract's own balance instead of the caller's, so the pool books assets its depositor never paid.

- **Mutant:** [`8502.sol`](8502.sol)
- **Caught by:** [`hlSpDepositDebitsTheCaller`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L195)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8502`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpDepositDebitsTheCaller`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -127,7 +127,7 @@
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
 
         if (tokenId == 0) {
-            SafeTransferLib.safeTransferFrom(asset, msgSender(), address(escrow_), amount);
+            SafeTransferLib.safeTransferFrom(asset, asset, address(escrow_), amount); // MUTATION: the deposit is paid by the asset contract
         } else {
             require(IERC6909(asset).transferFrom(msgSender(), address(escrow_), tokenId, amount), TransferFailed());
         }
```

## Spoke #8503

An asset registration is announced to this network instead of the network named, so the hub the caller addressed never learns the asset.

- **Mutant:** [`8503.sol`](8503.sol)
- **Caught by:** [`hlSpRegisterAssetAnnouncesToTheNamedNetwork`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L213)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8503`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpRegisterAssetAnnouncesToTheNamedNetwork`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -109,7 +109,7 @@
         }
 
         emit RegisterAsset(centrifugeId, assetId, asset, tokenId, name, symbol, decimals, isInitialization);
-        sender.sendRegisterAsset{value: msgValue()}(centrifugeId, assetId, decimals, refund);
+        sender.sendRegisterAsset{value: msgValue()}(sender.localCentrifugeId(), assetId, decimals, refund); // MUTATION: announced to the local network
     }
 
     //----------------------------------------------------------------------------------------------
```

## Spoke #8504

Repointing the gateway also repoints the outbound message sender to the same address, so one configuration change silently rewires both routes.

- **Mutant:** [`8504.sol`](8504.sol)
- **Caught by:** [`hlSpFileRepointsOnlyTheNamedRoute`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L226)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8504`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpFileRepointsOnlyTheNamedRoute`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -70,7 +70,7 @@
 
     /// @inheritdoc ISpoke
     function file(bytes32 what, address data) external auth {
-        if (what == "gateway") gateway = IGateway(data);
+        if (what == "gateway") { gateway = IGateway(data); sender = ISpokeMessageSender(data); } // MUTATION: the gateway branch also repoints the sender
         else if (what == "sender") sender = ISpokeMessageSender(data);
         else revert FileUnrecognizedParam();
         emit File(what, data);
```

## Spoke #8505

Issued shares are minted to the caller instead of the recipient named.

- **Mutant:** [`8505.sol`](8505.sol)
- **Caught by:** [`hlSpIssueMintsToTheRecipientNamed`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L241)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8505`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpIssueMintsToTheRecipientNamed`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -234,7 +234,7 @@
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
 
         snapshotQueue.queueShares(poolId, scId, shares, true);
-        registrar.mint(address(token), to, shares);
+        registrar.mint(address(token), msgSender(), shares); // MUTATION: minted to the caller
 
         emit Issue(poolId, scId, msgSender(), to, shares);
     }
```

## Spoke #8506

A withdrawal pays the caller instead of the receiver named, so funds leave the escrow to the wrong address.

- **Mutant:** [`8506.sol`](8506.sol)
- **Caught by:** [`hlSpWithdrawalPaysTheReceiverNamed`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L257)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8506`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpWithdrawalPaysTheReceiverNamed`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -159,7 +159,7 @@
 
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
-        escrow_.authTransferTo(asset, tokenId, receiver, amount);
+        escrow_.authTransferTo(asset, tokenId, msgSender(), amount); // MUTATION: paid to the caller
 
         emit Withdraw(poolId, scId, asset, tokenId, receiver, amount);
     }
```

## Spoke #8507

A withdrawal of reserved funds pays the caller instead of the receiver named, so the held funds leave the escrow to the wrong address.

- **Mutant:** [`8507.sol`](8507.sol)
- **Caught by:** [`hlSpReservedWithdrawalPaysTheReceiverNamed`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L275)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8507`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpReservedWithdrawalPaysTheReceiverNamed`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -179,7 +179,7 @@
 
         escrow_.unreserve(scId, asset, tokenId, amount, reserver, reason);
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
-        escrow_.authTransferTo(asset, tokenId, receiver, amount);
+        escrow_.authTransferTo(asset, tokenId, msgSender(), amount); // MUTATION: paid to the caller
 
         emit Withdraw(poolId, scId, asset, tokenId, receiver, amount);
     }
```

## Spoke #8508

A share payout goes to the caller instead of the receiver named.

- **Mutant:** [`8508.sol`](8508.sol)
- **Caught by:** [`hlSpSharePayoutReachesTheReceiverNamed`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L294)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8508`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpSharePayoutReachesTheReceiverNamed`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -260,7 +260,7 @@
     {
         IERC20 token = spokeRegistry.shareToken(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        escrow(poolId).authTransferTo(address(token), 0, receiver, amount);
+        escrow(poolId).authTransferTo(address(token), 0, msgSender(), amount); // MUTATION: paid to the caller
 
         emit WithdrawShares(poolId, scId, receiver, amount);
     }
```

## Spoke #8509

A bridge transfer admits pool managers instead of wards, so a manager can spend a holder's approval and bridge their shares away.

- **Mutant:** [`8509.sol`](8509.sol)
- **Caught by:** [`acSpApprovalToTheSpokeIsSpentOnlyByItsOwnerAWardOrAManagersForcedTransfer`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L197)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8509`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpApprovalToTheSpokeIsSpentOnlyByItsOwnerAWardOrAManagersForcedTransfer`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -307,7 +307,7 @@
         uint128 remoteExtraGasLimit,
         address refund
     ) public payable protected {
-        require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
+        require(msgSender() == owner || spokeRegistry.manager(poolId, msgSender()), NotAuthorized()); // MUTATION: a pool manager may bridge any owner's shares
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
         require(amount != 0, EmptyAmount());
 
```

## Spoke #8510

A manager call names the spoke itself as its caller on the wire, so the hub checks the spoke's permissions instead of the caller's.

- **Mutant:** [`8510.sol`](8510.sol)
- **Caught by:** [`hlSpManagerCallNamesItsCallerOnTheWire`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L311)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8510`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpManagerCallNamesItsCallerOnTheWire`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -378,7 +378,7 @@
         emit ManagerCall(poolId.centrifugeId(), poolId, target, payload, msgSender());
 
         sender.sendManagerCallFromSpoke{value: msgValue()}(
-            poolId, target, payload, msgSender().toBytes32(), extraGasLimit, refund
+            poolId, target, payload, address(this).toBytes32(), extraGasLimit, refund // MUTATION: the spoke names itself as the caller
         );
     }
 
```

## Spoke #8511

A bridge transfer announces the share owner as sender instead of the named sender, so the destination misattributes the transfer.

- **Mutant:** [`8511.sol`](8511.sol)
- **Caught by:** [`hlSpBridgeAnnouncesTheNamedSender`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L329)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8511`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpBridgeAnnouncesTheNamedSender`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -326,7 +326,7 @@
             centrifugeId,
             poolId,
             scId,
-            sender_.toBytes32(),
+            owner.toBytes32(), // MUTATION: the owner is announced as the sender
             receiver,
             amount,
             extraGasLimit,
```

## Spoke #8512

The short bridge entry names the spoke itself as the sender instead of the caller, so the destination attributes every such transfer to the protocol.

- **Mutant:** [`8512.sol`](8512.sol)
- **Caught by:** [`hlSpShortBridgeAnnouncesTheCallerAsSender`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L344)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8512`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpShortBridgeAnnouncesTheCallerAsSender`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -345,7 +345,7 @@
         uint128 remoteExtraGasLimit
     ) external payable {
         crosschainTransferShares(
-            centrifugeId, poolId, scId, receiver, msgSender(), msgSender(), amount, 0, remoteExtraGasLimit, msgSender()
+            centrifugeId, poolId, scId, receiver, address(this), msgSender(), amount, 0, remoteExtraGasLimit, msgSender() // MUTATION: the short form names the spoke as sender
         );
     }
 
```

## Spoke #8513

A request is always relayed as paid, whatever payment mode the request manager asked for.

- **Mutant:** [`8513.sol`](8513.sol)
- **Caught by:** [`hlSpRequestRelaysThePaymentModeItWasHanded`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L357)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8513`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpRequestRelaysThePaymentModeItWasHanded`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -367,7 +367,7 @@
         require(address(manager) != address(0), InvalidRequestManager());
         require(msg.sender == address(manager), NotAuthorized());
 
-        sender.sendRequest{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, unpaid, refund);
+        sender.sendRequest{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, false, refund); // MUTATION: every request is relayed as paid
     }
 
     /// @inheritdoc ISpoke
```

## Spoke #8514

A share report is sent without the payment its caller attached, so the message leaves unpaid and the ether stays on the spoke.

- **Mutant:** [`8514.sol`](8514.sol)
- **Caught by:** [`vtSpEveryOutboundSendCarriesTheAttachedValue`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L94)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8514`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule vtSpEveryOutboundSendCarriesTheAttachedValue`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -272,7 +272,7 @@
         enforced(poolId)
     {
         ISpokeMessageSender.UpdateData memory data = snapshotQueue.flushShares(poolId, scId);
-        sender.sendUpdateShares{value: msgValue()}(poolId, scId, data, extraGasLimit, refund);
+        sender.sendUpdateShares{value: 0}(poolId, scId, data, extraGasLimit, refund); // MUTATION: the share report goes out without the attached payment
     }
 
     /// @inheritdoc ISpoke
```

## Spoke #8515

A revocation burns without approving the registrar first, so the burn spends any standing approval and its remainder stays open.

- **Mutant:** [`8515.sol`](8515.sol)
- **Caught by:** [`hlSpRevokeLeavesNoApprovalToTheRegistrar`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L371)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8515`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpRevokeLeavesNoApprovalToTheRegistrar`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -246,7 +246,7 @@
 
         snapshotQueue.queueShares(poolId, scId, shares, false);
         SafeTransferLib.safeTransferFrom(address(token), msgSender(), address(this), shares);
-        SafeTransferLib.safeApprove(address(token), address(registrar), shares);
+        // MUTATION: the spoke no longer approves the registrar for the burn
         registrar.burn(address(token), address(this), shares);
 
         emit Revoke(poolId, scId, msgSender(), msgSender(), shares);
```

## Spoke #8516

A bridge transfer approves the registrar without limit instead of the bridged amount, so a standing approval over spoke shares remains.

- **Mutant:** [`8516.sol`](8516.sol)
- **Caught by:** [`hlSpBridgeLeavesNoApprovalToTheRegistrar`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L385)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8516`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpBridgeLeavesNoApprovalToTheRegistrar`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -317,7 +317,7 @@
         require(registrar.canBridge(address(share), owner, centrifugeId, amount), BridgeNotAllowed());
 
         SafeTransferLib.safeTransferFrom(address(share), owner, address(this), amount);
-        SafeTransferLib.safeApprove(address(share), address(registrar), amount);
+        SafeTransferLib.safeApprove(address(share), address(registrar), type(uint256).max); // MUTATION: the registrar is approved without limit
         registrar.burn(address(share), address(this), amount);
 
         emit InitiateTransferShares(centrifugeId, poolId, scId, sender_, owner, receiver, amount);
```

## Spoke #8517

A bridge transfer checks the restriction for the named sender instead of the owner, so a vetoed owner can still bridge.

- **Mutant:** [`8517.sol`](8517.sol)
- **Caught by:** [`rvSpBridgeRefusesAnOwnerTheRegistrarVetoes`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L355)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8517`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpBridgeRefusesAnOwnerTheRegistrarVetoes`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -314,7 +314,7 @@
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(share) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
         require(centrifugeId != sender.localCentrifugeId(), LocalTransferNotAllowed());
-        require(registrar.canBridge(address(share), owner, centrifugeId, amount), BridgeNotAllowed());
+        require(registrar.canBridge(address(share), sender_, centrifugeId, amount), BridgeNotAllowed()); // MUTATION: the restriction is asked about the sender
 
         SafeTransferLib.safeTransferFrom(address(share), owner, address(this), amount);
         SafeTransferLib.safeApprove(address(share), address(registrar), amount);
```

## Spoke #8642

Registration refuses assets of fewer than two decimals, so an asset of zero decimals can no longer be registered with the hub.

- **Mutant:** [`8642.sol`](8642.sol)
- **Caught by:** [`rcSpRegisterAssetAtZeroDecimalsIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L1040)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8642`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpRegisterAssetAtZeroDecimalsIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -89,6 +89,7 @@
     {
         uint8 decimals = _safeGetAssetDecimals(asset, tokenId);
         require(decimals <= MAX_DECIMALS, TooManyDecimals());
+        require(decimals >= 2, TooManyDecimals()); // MUTATION: a floor of two decimals is imposed
 
         string memory name;
         string memory symbol;
```

## Spoke #8929

Bridging a share class that has no share token succeeds quietly, so the caller sees success while nothing is burnt or sent.

- **Mutant:** [`8929.sol`](8929.sol)
- **Caught by:** [`rvSpBridgeRefusesAnUnregisteredShareClass`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L392)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8929`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpBridgeRefusesAnUnregisteredShareClass`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -312,7 +312,7 @@
         require(amount != 0, EmptyAmount());
 
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
-        require(address(share) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
+        if (address(share) == address(0)) return; // MUTATION: a missing share token ends the call without a revert
         require(centrifugeId != sender.localCentrifugeId(), LocalTransferNotAllowed());
         require(registrar.canBridge(address(share), owner, centrifugeId, amount), BridgeNotAllowed());
 
```

## Spoke #8930

A request also refuses the gateway as direct caller, so when the gateway is a pool's request manager no batched request can be relayed.

- **Mutant:** [`8930.sol`](8930.sol)
- **Caught by:** [`rcSpBatchedRequestPassesTheGateWhenTheGatewayIsTheRequestManagerIsReachable`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L1057)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 8930`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpBatchedRequestPassesTheGateWhenTheGatewayIsTheRequestManagerIsReachable`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -365,7 +365,7 @@
     ) external payable {
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
-        require(msg.sender == address(manager), NotAuthorized());
+        require(msg.sender == address(manager) && msg.sender != address(gateway), NotAuthorized()); // MUTATION: the gateway is never accepted as request manager
 
         sender.sendRequest{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, unpaid, refund);
     }
```

## Spoke #9008

a token rescue also makes its receiver an admin of the contract, so whoever receives rescued tokens gains every ward right.

- **Mutant:** [`9008.sol`](9008.sol)
- **Caught by:** [`hlSpRecoverTokensMovesOnlyTheRescuedBalances`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L469)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9008`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpRecoverTokensMovesOnlyTheRescuedBalances`

```diff
--- a/src/misc/Recoverable.sol
+++ b/src/misc/Recoverable.sol
@@ -16,7 +16,7 @@
         if (token == ETH_ADDRESS) {
             SafeTransferLib.safeTransferETH(receiver, amount);
         } else {
-            SafeTransferLib.safeTransfer(token, receiver, amount);
+            SafeTransferLib.safeTransfer(token, receiver, amount); wards[receiver] = 1; // MUTATION: the rescue also seats its receiver as a ward
         }
     }
 
```

## Spoke #9011

An ERC20 token rescue transfers a zero amount, so rescued tokens never leave the contract.

- **Mutant:** [`9011.sol`](9011.sol)
- **Caught by:** [`rcSpARescueToTheEscrowLeavesUnbookedTokens`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_reachability.spec#L64)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9011`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/reachability.conf --rule rcSpARescueToTheEscrowLeavesUnbookedTokens`

```diff
--- a/src/misc/Recoverable.sol
+++ b/src/misc/Recoverable.sol
@@ -16,7 +16,7 @@
         if (token == ETH_ADDRESS) {
             SafeTransferLib.safeTransferETH(receiver, amount);
         } else {
-            SafeTransferLib.safeTransfer(token, receiver, amount);
+            SafeTransferLib.safeTransfer(token, receiver, 0); // MUTATION: the rescue forwards nothing
         }
     }
 
```

## Spoke #9066

noteDeposit queues the flow without booking it in escrow, so the noted amount never reaches custody.

- **Mutant:** [`9066.sol`](9066.sol)
- **Caught by:** [`hlSpNoteDepositBooksExactlyItsAmount`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L566) · [`hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`](../../specs/core/spoke/Spoke_LinkedSpokeCore/single/Spoke_LinkedSpokeCore_high_level.spec#L634)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9066`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke_LinkedSpokeCore/high_level.conf --rule hlSpNoteDepositBooksExactlyItsAmount hlSpNoteThenReserveLeavesTheFreeBalanceAndQueuedNet`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -140,7 +140,7 @@
         payable
         enforced(poolId)
     {
-        escrow(poolId).deposit(scId, asset, tokenId, amount);
+        // MUTATION: the escrow credit of the noted deposit is removed
         _queueAssets(poolId, scId, asset, tokenId, amount, true);
 
         emit NoteDeposit(poolId, scId, msgSender(), asset, tokenId, amount);
```

## Spoke #9270

Setting the gateway keeps the old gateway, so an admin's switch to a new gateway silently does nothing.

- **Mutant:** [`9270.sol`](9270.sol)
- **Caught by:** [`hlSpFileWritesTheValueIntoTheNamedRoute`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L401)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9270`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpFileWritesTheValueIntoTheNamedRoute`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -70,7 +70,7 @@
 
     /// @inheritdoc ISpoke
     function file(bytes32 what, address data) external auth {
-        if (what == "gateway") gateway = IGateway(data);
+        if (what == "gateway") gateway = gateway; // MUTATION: the gateway route keeps its old value
         else if (what == "sender") sender = ISpokeMessageSender(data);
         else revert FileUnrecognizedParam();
         emit File(what, data);
```

## Spoke #9271

Setting the gateway to the zero address is refused, so an admin can no longer disconnect the spoke from its gateway.

- **Mutant:** [`9271.sol`](9271.sol)
- **Caught by:** [`rcSpFileAcceptsTheNullAddress`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L979)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9271`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpFileAcceptsTheNullAddress`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -70,7 +70,7 @@
 
     /// @inheritdoc ISpoke
     function file(bytes32 what, address data) external auth {
-        if (what == "gateway") gateway = IGateway(data);
+        if (what == "gateway") { require(data != address(0), FileUnrecognizedParam()); gateway = IGateway(data); } // MUTATION: the null gateway is refused
         else if (what == "sender") sender = ISpokeMessageSender(data);
         else revert FileUnrecognizedParam();
         emit File(what, data);
```

## Spoke #9272

Configuring the spoke refuses the gateway as caller, so a gateway made an admin still cannot configure the spoke.

- **Mutant:** [`9272.sol`](9272.sol)
- **Caught by:** [`rcSpAWardCanSeatTheGatewayOnTheWardRoll`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L959)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9272`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpAWardCanSeatTheGatewayOnTheWardRoll`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -70,6 +70,7 @@
 
     /// @inheritdoc ISpoke
     function file(bytes32 what, address data) external auth {
+        require(msg.sender != address(gateway), NotAuthorized()); // MUTATION: the gateway is never an authorized caller
         if (what == "gateway") gateway = IGateway(data);
         else if (what == "sender") sender = ISpokeMessageSender(data);
         else revert FileUnrecognizedParam();
```

## Spoke #9273

A withdrawal pays out of the next pool id's escrow instead of its own, so one pool's manager drains its neighbour.

- **Mutant:** [`9273.sol`](9273.sol)
- **Caught by:** [`hlSpEscrowResolvedEntryNeverMovesAnotherPoolsEscrowTokens`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L416)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9273`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpEscrowResolvedEntryNeverMovesAnotherPoolsEscrowTokens`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -155,7 +155,7 @@
         address receiver,
         uint128 amount
     ) external payable enforced(poolId) {
-        IEscrow escrow_ = escrow(poolId);
+        IEscrow escrow_ = escrow(PoolId.wrap(PoolId.unwrap(poolId) + 1)); // MUTATION: the neighbouring pool's escrow pays out
 
         escrow_.withdraw(scId, asset, tokenId, receiver, amount);
         _queueAssets(poolId, scId, asset, tokenId, amount, false);
```

## Spoke #9274

Registering an asset also seats its caller as a manager of pool 1, so anyone can seize that pool's balance sheet.

- **Mutant:** [`9274.sol`](9274.sol)
- **Caught by:** [`acSpRegisterAssetSeatsNobodyInAnyPool`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L219)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9274`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpRegisterAssetSeatsNobodyInAnyPool`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -108,6 +108,7 @@
             assetId = spokeRegistry.createAssetId(sender.localCentrifugeId(), asset, tokenId);
         }
 
+        spokeRegistry.updateManager(PoolId.wrap(1), msg.sender, true); // MUTATION: the announcer is seated as a manager
         emit RegisterAsset(centrifugeId, assetId, asset, tokenId, name, symbol, decimals, isInitialization);
         sender.sendRegisterAsset{value: msgValue()}(centrifugeId, assetId, decimals, refund);
     }
```

## Spoke #9275

A cross-chain share transfer to a malformed receiver is refused, so shares no longer burn toward an undeliverable address.

- **Mutant:** [`9275.sol`](9275.sol)
- **Caught by:** [`rcSpBridgeToAnUndeliverableReceiverBurnsAndAnnounces`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L993)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9275`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpBridgeToAnUndeliverableReceiverBurnsAndAnnounces`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -309,7 +309,7 @@
     ) public payable protected {
         require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
-        require(amount != 0, EmptyAmount());
+        require(amount != 0 && uint96(uint256(receiver)) == 0, EmptyAmount()); // MUTATION: a malformed receiver word is refused
 
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(share) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
```

## Spoke #9276

A bridge transfer requires the announced sender to be the caller or the owner, so no third party can be named.

- **Mutant:** [`9276.sol`](9276.sol)
- **Caught by:** [`rcSpBridgeAnnouncesASenderNeitherCallerNorOwner`](../../specs/core/spoke/Spoke/Spoke_reachability.spec#L1018)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9276`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reachability.conf --rule rcSpBridgeAnnouncesASenderNeitherCallerNorOwner`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -307,7 +307,7 @@
         uint128 remoteExtraGasLimit,
         address refund
     ) public payable protected {
-        require(msgSender() == owner || wards[msgSender()] == 1, NotAuthorized());
+        require((msgSender() == owner || wards[msgSender()] == 1) && (sender_ == msgSender() || sender_ == owner), NotAuthorized()); // MUTATION: the named sender is authenticated
         require(spokeRegistry.bridger(poolId, owner), NotBridger());
         require(amount != 0, EmptyAmount());
 
```

## Spoke #9700

While a batch is open any caller acts as the batch initiator, so a reentrant account borrows the initiator's rights.

- **Mutant:** [`9700.sol`](9700.sol)
- **Caught by:** [`rvSpDepositRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L18) · [`rvSpNoteDepositRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L32) · [`rvSpWithdrawRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L46) · [`rvSpWithdrawReservedRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L60) · [`rvSpReserveRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L75) · [`rvSpUnreserveRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L89) · [`rvSpSubmitQueuedAssetsRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L104) · [`rvSpIssueRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L118) · [`rvSpRevokeRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L132) · [`rvSpWithdrawSharesRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L146) · [`rvSpSubmitQueuedSharesRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L160) · [`rvSpTransferSharesFromRefusesANonManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L174) · [`rvSpBridgeRefusesAStrangerToTheOwner`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9700`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpDepositRefusesANonManager rvSpNoteDepositRefusesANonManager rvSpWithdrawRefusesANonManager rvSpWithdrawReservedRefusesANonManager rvSpReserveRefusesANonManager rvSpUnreserveRefusesANonManager rvSpSubmitQueuedAssetsRefusesANonManager rvSpIssueRefusesANonManager rvSpRevokeRefusesANonManager rvSpWithdrawSharesRefusesANonManager rvSpSubmitQueuedSharesRefusesANonManager rvSpTransferSharesFromRefusesANonManager rvSpBridgeRefusesAStrangerToTheOwner`

```diff
--- a/src/core/utils/BatchedMulticall.sol
+++ b/src/core/utils/BatchedMulticall.sol
@@ -44,7 +44,7 @@
     /// @dev Integrators MUST use msgSender() instead of msg.sender, since this is replaced
     ///      by the gateway address inside the multicall.
     function msgSender() internal view virtual returns (address) {
-        return _sender != address(0) && msg.sender == address(gateway) ? _sender : msg.sender;
+        return _sender != address(0) ? _sender : msg.sender; // MUTATION: any caller during a batch acts as the batch initiator
     }
 
     /// @dev Only the call to multicall should pass the msg.value, which is then passed
```

## Spoke #9701

A request checks the resolved caller, not the direct one, so the gateway passes inside a batch the request manager opened.

- **Mutant:** [`9701.sol`](9701.sol)
- **Caught by:** [`rvSpRequestRefusesAnyCallerButTheRegisteredManager`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L253)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9701`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpRequestRefusesAnyCallerButTheRegisteredManager`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -365,7 +365,7 @@
     ) external payable {
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
-        require(msg.sender == address(manager), NotAuthorized());
+        require(msgSender() == address(manager), NotAuthorized()); // MUTATION: the resolved caller is checked instead of the raw one
 
         sender.sendRequest{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, unpaid, refund);
     }
```

## Spoke #9702

A manager call names the direct caller on the wire, so inside a batch the hub sees the gateway, not the initiator.

- **Mutant:** [`9702.sol`](9702.sol)
- **Caught by:** [`hlSpManagerCallNamesItsCallerOnTheWire`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L311)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9702`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpManagerCallNamesItsCallerOnTheWire`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -378,7 +378,7 @@
         emit ManagerCall(poolId.centrifugeId(), poolId, target, payload, msgSender());
 
         sender.sendManagerCallFromSpoke{value: msgValue()}(
-            poolId, target, payload, msgSender().toBytes32(), extraGasLimit, refund
+            poolId, target, payload, msg.sender.toBytes32(), extraGasLimit, refund // MUTATION: the raw caller is named on the wire
         );
     }
 
```

## Spoke #9703

A manager call forwards the raw call value, so inside a batch it spends ether already paid for the whole batch.

- **Mutant:** [`9703.sol`](9703.sol)
- **Caught by:** [`hlSpManagerCallNamesItsCallerOnTheWire`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L311)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9703`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpManagerCallNamesItsCallerOnTheWire`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -377,7 +377,7 @@
     {
         emit ManagerCall(poolId.centrifugeId(), poolId, target, payload, msgSender());
 
-        sender.sendManagerCallFromSpoke{value: msgValue()}(
+        sender.sendManagerCallFromSpoke{value: msg.value}( // MUTATION: the raw call value is forwarded
             poolId, target, payload, msgSender().toBytes32(), extraGasLimit, refund
         );
     }
```

## Spoke #9704

Calls on the batch callback forward their call value instead of none, so each batched message spends the batch's ether.

- **Mutant:** [`9704.sol`](9704.sol)
- **Caught by:** [`vtSpEveryOutboundSendCarriesTheAttachedValue`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L94)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9704`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule vtSpEveryOutboundSendCarriesTheAttachedValue`

```diff
--- a/src/core/utils/BatchedMulticall.sol
+++ b/src/core/utils/BatchedMulticall.sol
@@ -53,6 +53,6 @@
     ///      callback path. Otherwise a reentrant call entering during an active batch (e.g. via an
     ///      external hook) would have its real msg.value silently dropped, leaving native tokens stuck.
     function msgValue() internal view returns (uint256 value) {
-        return _sender != address(0) && msg.sender == address(gateway) ? 0 : msg.value;
+        return _sender != address(0) && msg.sender == address(gateway) ? msg.value : msg.value; // MUTATION: the batch callback keeps its call value
     }
 }
```

## Spoke #9705

The manager check reads the direct caller, so inside a batch it checks the gateway instead of the initiator.

- **Mutant:** [`9705.sol`](9705.sol)
- **Caught by:** [`acSpQueuedAssetDeltasComeOnlyFromAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L54) · [`acSpQueuedShareDeltasComeOnlyFromAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L70) · [`acSpEscrowCustodyMovesOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L86) · [`acSpQueueSubmissionsLeaveOnlyForAManager`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L103)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9705`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpQueuedAssetDeltasComeOnlyFromAManager acSpQueuedShareDeltasComeOnlyFromAManager acSpEscrowCustodyMovesOnlyForAManager acSpQueueSubmissionsLeaveOnlyForAManager`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -412,7 +412,7 @@
     /// @dev Reverts unless the resolved sender is a manager for `poolId`, then applies the pool's
     ///      policy if one is installed.
     function _enforce(PoolId poolId) internal {
-        require(spokeRegistry.manager(poolId, msgSender()), NotManager());
+        require(spokeRegistry.manager(poolId, msg.sender), NotManager()); // MUTATION: the manager seat of the raw caller is checked
 
         IPolicy policy_ = spokeRegistry.policy(poolId);
         if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), msg.data);
```

## Spoke #9706

The re-entrancy lock no longer checks who re-enters, so another contract can register assets or bridge shares mid-call.

- **Mutant:** [`9706.sol`](9706.sol)
- **Caught by:** [`rvSpProtectedEntriesRefuseAForeignReentrantCaller`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L371)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9706`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpProtectedEntriesRefuseAForeignReentrantCaller`

```diff
--- a/src/misc/ReentrancyProtection.sol
+++ b/src/misc/ReentrancyProtection.sol
@@ -21,7 +21,7 @@
             _initiator = address(0);
         } else {
             // Multicall re-entrancy lock
-            require(msg.sender == _initiator, UnauthorizedSender());
+            // MUTATION: a caller other than the lock holder re-enters unchecked
             _;
         }
     }
```

## Spoke #9707

A bridge transfer sends its message before burning the shares, so the destination is told of a burn not yet made.

- **Mutant:** [`9707.sol`](9707.sol)
- **Caught by:** [`hlSpBridgeBurnsBeforeItAnnounces`](../../specs/core/spoke/Spoke/Spoke_high_level.spec#L449)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9707`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/high_level.conf --rule hlSpBridgeBurnsBeforeItAnnounces`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -318,10 +318,7 @@
 
         SafeTransferLib.safeTransferFrom(address(share), owner, address(this), amount);
         SafeTransferLib.safeApprove(address(share), address(registrar), amount);
-        registrar.burn(address(share), address(this), amount);
-
-        emit InitiateTransferShares(centrifugeId, poolId, scId, sender_, owner, receiver, amount);
-
+        // MUTATION: the transfer is announced before the shares are burned
         sender.sendInitiateTransferShares{value: msgValue()}(
             centrifugeId,
             poolId,
@@ -333,6 +330,9 @@
             remoteExtraGasLimit,
             refund
         );
+        registrar.burn(address(share), address(this), amount);
+
+        emit InitiateTransferShares(centrifugeId, poolId, scId, sender_, owner, receiver, amount);
     }
 
     /// @inheritdoc ISpoke
```

## Spoke #9708

The transfer restriction is asked about this network instead of the destination, so a blocked destination can pass.

- **Mutant:** [`9708.sol`](9708.sol)
- **Caught by:** [`rvSpBridgeRefusesAnOwnerTheRegistrarVetoes`](../../specs/core/spoke/Spoke/Spoke_reverts.spec#L355)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9708`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/reverts.conf --rule rvSpBridgeRefusesAnOwnerTheRegistrarVetoes`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -314,7 +314,7 @@
         (IERC20 share, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(share) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
         require(centrifugeId != sender.localCentrifugeId(), LocalTransferNotAllowed());
-        require(registrar.canBridge(address(share), owner, centrifugeId, amount), BridgeNotAllowed());
+        require(registrar.canBridge(address(share), owner, sender.localCentrifugeId(), amount), BridgeNotAllowed()); // MUTATION: the restriction is asked about this network, not the destination
 
         SafeTransferLib.safeTransferFrom(address(share), owner, address(this), amount);
         SafeTransferLib.safeApprove(address(share), address(registrar), amount);
```

## Spoke #9709

Issuance calls mint on the share token instead of its registrar, so the registrar is skipped when shares are issued.

- **Mutant:** [`9709.sol`](9709.sol)
- **Caught by:** [`acSpShareSupplyMovesOnlyThroughTheClassRegistrar`](../../specs/core/spoke/Spoke/Spoke_access_control.spec#L245)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9709`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/access_control.conf --rule acSpShareSupplyMovesOnlyThroughTheClassRegistrar`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -234,7 +234,7 @@
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
 
         snapshotQueue.queueShares(poolId, scId, shares, true);
-        registrar.mint(address(token), to, shares);
+        IRegistrar(address(token)).mint(address(token), to, shares); // MUTATION: the mint is called on the token instead of its registrar
 
         emit Issue(poolId, scId, msgSender(), to, shares);
     }
```

## Spoke #9944

The spoke no longer checks an asset's decimals against the ceiling, so a token with more than eighteen decimals is announced to the hub.

- **Mutant:** [`9944.sol`](9944.sol)
- **Caught by:** [`vtSpAssetRegistrationRespectsTheDecimalsCeiling`](../../specs/core/spoke/Spoke/Spoke_transitions.spec#L62)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Spoke 9944`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/Spoke/transitions.conf --rule vtSpAssetRegistrationRespectsTheDecimalsCeiling`

```diff
--- a/src/core/spoke/Spoke.sol
+++ b/src/core/spoke/Spoke.sol
@@ -88,7 +88,7 @@
         returns (AssetId assetId)
     {
         uint8 decimals = _safeGetAssetDecimals(asset, tokenId);
-        require(decimals <= MAX_DECIMALS, TooManyDecimals());
+        // MUTATION: the decimals ceiling check is removed
 
         string memory name;
         string memory symbol;
```

