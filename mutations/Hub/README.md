# Mutations for `Hub` (`src/core/hub/Hub.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/hub/Accounting.sol`, `src/core/hub/Holdings.sol`, `src/core/hub/HubRegistry.sol`, `src/core/hub/ShareClassManager.sol`, `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [1](#hub-1) | createPool no longer checks that the pool id carries the hub's own network prefix, so a foreign pool can be registered locally.<br>Caught by: [`registeredPoolIsLocal`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L46) |
| [2](#hub-2) | createPool checks the pool id against the currency's network instead of the hub's, so a foreign pool can register.<br>Caught by: [`registeredPoolIsLocal`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L46) |
| [3](#hub-3) | initializeHolding verifies the existence of only the first three journal accounts, so the fourth is linked without ever being created.<br>Caught by: [`holdingAccountIdsExist`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L25) · [`initializedHoldingHasAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L31) |
| [4](#hub-4) | initializeHolding re-checks the first journal account on every loop pass, so the other three are linked without existence checks.<br>Caught by: [`holdingAccountIdsExist`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L25) · [`initializedHoldingHasAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L31) |
| [5](#hub-5) | setHoldingAccountId no longer checks the account exists in the ledger, so a holding can reference an absent or null account id.<br>Caught by: [`holdingAccountIdsExist`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L25) · [`initializedHoldingHasAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L31) |
| [6](#hub-6) | initializeHolding no longer checks the asset is registered, so a holding can be initialized for an unknown asset.<br>Caught by: [`initializedHoldingAssetRegistered`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L41) |
| [7](#hub-7) | initializeHolding checks that the pool exists instead of that the asset is registered, so a holding can be initialized for an unknown asset.<br>Caught by: [`initializedHoldingAssetRegistered`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L41) |
| [3006](#hub-3006) | initializeHolding no longer checks that the four journal accounts exist, so a holding wires itself to void accounts.<br>Caught by: [`holdingAccountIdsExist`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L25) · [`initializedHoldingHasAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L31) |
| [3012](#hub-3012) | updateHoldingValuation rewires an account slot while it changes the price source, so a repricing redirects where entries post.<br>Caught by: [`stHuPriceSourceSwapNeverRewiresTheAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L174) |
| [3013](#hub-3013) | A policy swap installs the replacement under the number the old policy ran on, so authorizations granted under the previous rule book survive the change.<br>Caught by: [`stHuPolicySwapAdvancesTheAuthorizationNamespace`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L121) |
| [3020](#hub-3020) | unlock reuses the prior journal id instead of advancing the counter, so a ledger move is filed under a stale journal.<br>Caught by: [`stHuLedgerMoveIsFiledUnderAFreshJournal`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L136) |
| [3046](#hub-3046) | addCredit never adds the value to the account's credit total, so the pool's debits and credits stop balancing.<br>Caught by: [`journalDebitsEqualCredits`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L17) |
| [4800](#hub-4800) | rely drops the ward gate, so any caller can hand itself the authority the hub reserves for the root and the guardians.<br>Caught by: [`acHuWardSetMovesOnlyForAWard`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L4) |
| [4801](#hub-4801) | file drops the ward gate, so any caller can repoint the hub's gateway, sender, adapter set or fee hook.<br>Caught by: [`acHuWiringMovesOnlyForAWard`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L21) |
| [4802](#hub-4802) | createPool drops the ward gate, so any caller can open a pool and thereby set its accounting currency and seat its first manager.<br>Caught by: [`acHuPoolCurrencyMovesOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L46) · [`acHuManagerSeatMovesOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L65) |
| [4803](#hub-4803) | setPolicy drops the ward or manager check, so any caller can install a pool's policy and void its pending authorizations.<br>Caught by: [`acHuPoolPolicyMovesOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L85) |
| [4804](#hub-4804) | The pool gate admits hub wards instead of pool managers, so a ward with no seat can act as the pool's manager.<br>Caught by: [`acHuAuthorizationLedgerMovesThroughTheHubOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L107) · [`acHuBridgingHookMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L126) · [`acHuRequestManagerSeatMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L143) · [`acHuSnapshotHookMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L162) · [`acHuShareClassRegisterMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L237) · [`acHuSharePriceMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L264) · [`acHuAccountCreationNeedsAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L284) · [`acHuOutboundInstructionNeedsAPoolManagerOrARequestFulfilment`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L382) |
| [4805](#hub-4805) | initializeHolding drops the pool gate, so any caller can open a holding and set its price source, ledger accounts and value.<br>Caught by: [`acHuHoldingValuationMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L180) · [`acHuHoldingAccountWiringMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L199) · [`acHuHoldingValueMovesThroughTheHubOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L218) |
| [4806](#hub-4806) | updateJournal drops the pool gate, so any caller can post debits and credits into a pool's books.<br>Caught by: [`acHuAccountDebitMovesThroughTheHubOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L302) · [`acHuAccountCreditMovesThroughTheHubOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L322) · [`acHuJournalCounterMovesThroughTheHubOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L342) |
| [4807](#hub-4807) | requestCallback finds the request manager on the hub's network, not the asset's, so a local manager answers for other networks.<br>Caught by: [`acHuRequestCallbackNeedsTheRegisteredRequestManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L361) |
| [4808](#hub-4808) | Every hub posting credits the amount credit account whatever kind it names, so an equal round trip no longer nets to zero.<br>Caught by: [`hlHuAmountRoundTripKeepsEveryAccountNet`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L4) · [`hlHuValueRoundTripKeepsTheHoldingAccountNetWhenGainAndLossAreOtherAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L20) |
| [4809](#hub-4809) | a revaluation clears the holding's amount credit slot, so a pool's account wiring moves on an entry that was never meant to touch it.<br>Caught by: [`vtHuAccountWiringMovesOnlyThroughWiringEntries`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L54) |
| [4810](#hub-4810) | Setting a holding account also clears the holding's price source, so its valuation changes outside the valuation setters.<br>Caught by: [`vtHuValuationMovesOnlyThroughItsInstallers`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L70) |
| [4811](#hub-4811) | Opening a holding also installs its price source as the pool's snapshot hook, so the hook changes outside its setter.<br>Caught by: [`vtHuSnapshotHookMovesOnlyThroughItsSetter`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L86) |
| [4813](#hub-4813) | The pool gate no longer requires a manager seat, so the entries it guards stop refusing callers the pool never appointed.<br>Caught by: [`rvHuSetPolicyRefusesAnUnauthorisedInstall`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L39) · [`rvHuCancelAuthorizationRefusesANonManagerOrAnEmptySlot`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L73) · [`rvHuUpdateHubManagerRefusesANonManagerOrANullSeat`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L90) · [`rvHuUpdateCurrencyRefusesARescalingRedenomination`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L105) · [`rvHuCreateAccountRefusesARepeatOrAnUnusableOpening`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L124) · [`rvHuSetHoldingAccountIdRefusesAnAbsentRowOrHolding`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L140) · [`rvHuUpdateHoldingValuationRefusesANullSourceOrClosedHolding`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L157) · [`rvHuInitializeHoldingRefusesARepeatOrAnUnusableOpening`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L220) · [`rvHuSpokeCallRevokePassesThePolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L344) · [`rvHuCancelAuthorizationIsNeverRefusedToAnAdmittedManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L426) |
| [4814](#hub-4814) | file accepts a dependency name the hub does not wire instead of refusing it, so a call that rewires nothing still succeeds.<br>Caught by: [`rvHuFileRefusesANonWardOrAnUnknownName`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L4) |
| [4815](#hub-4815) | registering a pool no longer refuses the null opening operator, so a pool opens seated on an address nobody can ever act from.<br>Caught by: [`rvHuCreatePoolRefusesARepeatOrAnUnusableOpening`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L20) |
| [4816](#hub-4816) | Scheduling an authorization no longer refuses a call the policy already allows, so a zero delay call enters the timelock.<br>Caught by: [`rvHuInitiateAuthorizationRefusesAnUnauthorisedOrDuplicateSchedule`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L55) |
| [4817](#hub-4817) | managerCall no longer matches the declared local value to the destination, so a misdeclared call is sent instead of refused.<br>Caught by: [`rvHuManagerCallRefusesAMisdeclaredValue`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L173) |
| [4818](#hub-4818) | requestCallback no longer checks the caller is the pool's request manager, so anyone can push a request result to the spoke.<br>Caught by: [`rvHuRequestCallbackRefusesAnyCallerButTheRegisteredManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L189) |
| [4820](#hub-4820) | The asset price read no longer falls back to par for an unopened holding, so it reverts instead of answering.<br>Caught by: [`rvHuPricePoolPerAssetAnswersForAnUnopenedHolding`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L204) |
| [4821](#hub-4821) | installing a rule book advances the pool's authorization tenure by two, so the tenure skips a number.<br>Caught by: [`vtHuAuthorizationTenureStepsByAtMostOne`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L6) |
| [4822](#hub-4822) | opening a journal advances the pool's journal numbering by two, so the sequence skips a number and the audit trail carries a gap.<br>Caught by: [`vtHuJournalSequenceStepsByAtMostOne`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L22) |
| [4823](#hub-4823) | adding a share class advances the pool's class numbering by two, so an index is skipped.<br>Caught by: [`vtHuShareClassSequenceStepsByAtMostOne`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L38) |
| [4825](#hub-4825) | initializeHolding no longer checks the share class exists, so a holding opens on a class never created.<br>Caught by: [`initializedHoldingImpliesShareClassExists`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L51) |
| [4826](#hub-4826) | the pool gate admits hub wards instead of pool managers, so a ward can open a ledger row on a pool never created.<br>Caught by: [`ledgerAccountImpliesRegisteredPool`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L56) |
| [6200](#hub-6200) | opening a pool records its currency but never seats the named operator, so the pool starts with no manager.<br>Caught by: [`rcHuCreatePoolSeatsADelegateIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L4) · [`rcHuCreatePoolSeatsTheOpeningWardIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L23) |
| [6201](#hub-6201) | pool registration treats the smallest usable asset id as an empty currency, so the bottom edge of the asset id space cannot denominate a pool.<br>Caught by: [`rcHuCreatePoolAtTheSmallestCurrencyIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L41) |
| [6202](#hub-6202) | the seat entry clears the operator seat whatever the flag asks for, so an appointment withdraws the seat it meant to grant.<br>Caught by: [`rcHuPoolBirthThenDelegationIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L57) · [`rcHuSecondOperatorAppointmentIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L79) · [`rcHuOperatorSeatRoundTripIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L93) |
| [6203](#hub-6203) | an operator is refused any change to its own seat, so standing down needs a second operator to act for it.<br>Caught by: [`rcHuOperatorCanStandItselfDownIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L112) |
| [6204](#hub-6204) | installing a rule book always runs the operator gate, so a hub ward without a pool seat can no longer install one.<br>Caught by: [`rcHuGovernanceInstallsTheFirstRuleBookIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L126) |
| [6205](#hub-6205) | installing a rule book is reserved to hub wards, so a sitting pool operator can no longer swap the book its pool runs under.<br>Caught by: [`rcHuOperatorSwapsTheRuleBookIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L146) |
| [6206](#hub-6206) | the rule book setter refuses the null address, so a pool that installed a policy can never be left unrestricted.<br>Caught by: [`rcHuRuleBookCanBeRemovedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L166) |
| [6207](#hub-6207) | a scheduled privileged call matures in the very block that scheduled it, the veto window the rule book asked for dropped from the maturity.<br>Caught by: [`rcHuPrivilegedCallSchedulingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L183) |
| [6208](#hub-6208) | withdrawing a scheduled call only succeeds when nothing is scheduled, so a standing authorization can never be taken back.<br>Caught by: [`rcHuScheduledCallWithdrawalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L203) |
| [6209](#hub-6209) | adding a share class demands a salt that was already spent, so no share class can be branded with a fresh one.<br>Caught by: [`rcHuFirstShareClassIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L226) |
| [6210](#hub-6210) | every ledger row opens credit normal whatever the caller asked, so no debit normal asset or expense account can exist.<br>Caught by: [`rcHuDebitNormalRowCanBeOpenedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L248) · [`rcHuAccountsThenHoldingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L282) |
| [6211](#hub-6211) | every ledger row opens debit normal whatever the caller asked, so no credit normal equity or liability account can exist.<br>Caught by: [`rcHuCreditNormalRowCanBeOpenedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L265) |
| [6212](#hub-6212) | opening a holding books nothing, so the value the holding already carried never reaches the books as principal.<br>Caught by: [`rcHuHoldingOpeningValueBookedAsPrincipalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L310) |
| [6213](#hub-6213) | an amount posting of zero opens a journal instead of returning, so a movement of nothing still spends the pool an identity.<br>Caught by: [`rcHuHoldingOpeningWithNothingToBookIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L339) · [`rcHuZeroAmountPostingIsAcceptedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L542) |
| [6214](#hub-6214) | opening a holding rejects two neighbouring posting slots wired to one ledger row, a shape the opening call documents as legal.<br>Caught by: [`rcHuHoldingWithARepeatedSlotIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L366) · [`rcHuSharedAmountSlotsKeepTheHoldingAccountFlatIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1083) |
| [6215](#hub-6215) | a revaluation reports the difference but never stores the new value, so the holding keeps its old value.<br>Caught by: [`rcHuHoldingMarkUpIsBookedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L386) · [`rcHuHoldingMarkDownToZeroIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L412) |
| [6216](#hub-6216) | A zero revaluation opens a journal instead of returning, so remarking a holding at its current value spends a journal id.<br>Caught by: [`rcHuRevaluationLeavingTheBooksUntouchedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L440) · [`rcHuZeroValuePostingIsAcceptedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L638) |
| [6217](#hub-6217) | a deposit posts as a withdrawal and a withdrawal as a deposit, so each amount movement lands on the books the wrong way about.<br>Caught by: [`rcHuDepositPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L465) · [`rcHuWithdrawalPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L491) |
| [6218](#hub-6218) | every unlock mints a fresh journal identity, so two postings made in one transaction for one pool are filed apart instead of together.<br>Caught by: [`rcHuAmountRoundTripIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L517) |
| [6219](#hub-6219) | holding postings narrow the amount to sixty four bits on both legs, so larger amounts are booked truncated.<br>Caught by: [`rcHuLargestAmountPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L565) |
| [6220](#hub-6220) | a revaluation gain posts as a loss and a loss as a gain, so each value movement lands on the books the wrong way about.<br>Caught by: [`rcHuValueGainPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L586) · [`rcHuValueLossPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L612) |
| [6221](#hub-6221) | a manager authored batch never closes the session it opened, so the ledger is handed back unlocked once the entry returns.<br>Caught by: [`rcHuMinimalBalancedJournalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L661) · [`rcHuWiderBalancedJournalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L685) |
| [6222](#hub-6222) | an empty batch now returns at once, so it no longer opens a journal or uses up a journal number.<br>Caught by: [`rcHuEmptyJournalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L709) |
| [6223](#hub-6223) | the ledger refuses a debit entry that carries no value, so a pair of zero valued entries cannot be posted at all.<br>Caught by: [`rcHuZeroValuedJournalPairIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L732) |
| [6224](#hub-6224) | installing the null snapshot hook is silently ignored, so once NAV automation is switched on for a pool it can never be switched off.<br>Caught by: [`rcHuSnapshotHookRoundTripIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L757) |
| [6225](#hub-6225) | announcing a share class puts two identical messages on the wire, so one call costs the pool a duplicate announcement.<br>Caught by: [`rcHuShareClassAnnouncementIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L777) |
| [6226](#hub-6226) | the request callback flips the payment mode on its way out, so a paid callback travels as unpaid and an unpaid one as paid.<br>Caught by: [`rcHuPaidRequestCallbackIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L798) · [`rcHuUnpaidRequestCallbackIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L817) |
| [6227](#hub-6227) | withdrawing authority leaves the ward roll untouched, so a grant of the ward can never be taken back.<br>Caught by: [`rcHuWardAuthorityRoundTripIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L837) · [`rcHuWardCanStandItselfDownIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L856) |
| [6228](#hub-6228) | an unopened holding is priced at half par instead of par, so the default price is wrong.<br>Caught by: [`rcHuUnopenedHoldingPricesAtParIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L870) · [`rcHuAssetPriceNoticeForAnUnknownAssetAndClassIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1124) |
| [6229](#hub-6229) | setPolicy stores a rule book one address away from the one it was handed, so reading a pool's policy back never returns what was installed.<br>Caught by: [`rcHuPassingPolicyReadIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L882) |
| [8060](#hub-8060) | a new manager entry books share issuance and revocation directly, so share counts move without any spoke report.<br>Caught by: [`stHuShareLedgerIsNeverMovedByTheHub`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L242) |
| [8061](#hub-8061) | a new manager entry decreases a holding directly, so a manager can push its share class and network into deficit.<br>Caught by: [`stHuDeficitGateIsNeverMovedByTheHub`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L262) |
| [8062](#hub-8062) | the share class announcement swaps the salt and the registrar, so the spoke gets a salt the class was never created with.<br>Caught by: [`hlHuShareClassAnnouncementCarriesTheClassSalt`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L41) |
| [8108](#hub-8108) | the pool's policy is shown the call headed by the block time, so it misreads which call it gates and a scheduled authorization never matches a later retry.<br>Caught by: [`hlHuSharePriceUpdateStampedNowAsksThePolicyAboutACallFreeOfTheClock`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L296) |
| [8300](#hub-8300) | reinstalling a pool's current policy is skipped, so its nonce stays put and earlier authorizations stay spendable.<br>Caught by: [`hlHuRuleBookInstallAlwaysOpensANewTenure`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L283) |
| [8301](#hub-8301) | filing the outbound sender also repoints the gateway, so one configuration call rewires two of the hub's dependencies.<br>Caught by: [`hlHuFileWiresOnlyTheNamedSlot`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L57) |
| [8302](#hub-8302) | a share class announcement sends a zero registrar instead of the one its caller named, so the spoke never learns it.<br>Caught by: [`hlHuShareClassAnnouncementCarriesTheCallersRegistrar`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L76) |
| [8303](#hub-8303) | a revaluation checks the pool's home network for sync instead of the asset's, so the snapshot hook fires for the wrong network.<br>Caught by: [`hlHuRevaluationNotifiesTheHookExactlyWhenTheAssetsNetworkIsInSync`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L92) |
| [8304](#hub-8304) | switching a holding's price source also notifies the snapshot hook, so the hook publishes a pool price on a call that revalued nothing.<br>Caught by: [`vtHuSnapshotHookHearsOnlyARevaluation`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L103) |
| [8430](#hub-8430) | a revocation of a spoke call authorization is checked for the manager only and never asks the pool's policy, so a policy cannot see or refuse it.<br>Caught by: [`rcHuRevocationPassesAConsentingPolicyIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1031) |
| [8431](#hub-8431) | a revocation of a spoke call authorization is checked for the manager only, so a refusing policy no longer blocks it.<br>Caught by: [`rvHuEnforcedEntryPassesTheInstalledPolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L319) · [`rvHuSpokeCallRevokePassesThePolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L344) |
| [8812](#hub-8812) | revoking a spoke call sends an authorization instead, so the spoke is granted the call the manager meant to revoke.<br>Caught by: [`rvHuSpokeCallRevokePassesThePolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L344) |
| [8815](#hub-8815) | a share price update stamped now records a time one second before it ran, so the price looks older than it is.<br>Caught by: [`hlHuSharePriceUpdateStampedNowRecordsTheExecutionTime`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L315) |
| [8816](#hub-8816) | a pool notice forwards the raw call value, so a batched notice spends ETH the batch already paid to the gateway.<br>Caught by: [`vtHuEveryOutboundSendCarriesTheAttachedValue`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L277) |
| [8817](#hub-8817) | repointing the multi adapter rewires the fee accrual contract instead, so the hub can never move onto another multi adapter.<br>Caught by: [`rcHuFileRepointsTheMultiAdapterIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1049) |
| [8818](#hub-8818) | the multi adapter key is no longer recognized, so a ward's attempt to repoint the multi adapter reverts.<br>Caught by: [`rvHuFileSucceedsForAWardNamingADependency`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L370) |
| [8819](#hub-8819) | a manager who is no ward may only replace an installed policy, so a fresh pool's first policy needs a ward.<br>Caught by: [`rcHuFreshPoolManagerInstallsTheFirstRuleBookUnpolicedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1062) |
| [8820](#hub-8820) | opening a holding rejects one account as both amount debit and amount credit, so a holding can no longer book both on one account.<br>Caught by: [`rcHuSharedAmountSlotsKeepTheHoldingAccountFlatIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1083) · [`rcHuHoldingWithARepeatedSlotIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L366) |
| [8821](#hub-8821) | setHoldingAccountId refuses the account in the counterpart amount slot, so a holding's own account can never be moved onto it.<br>Caught by: [`rcHuHoldingAccountRepointedOntoItsCounterpartIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1105) |
| [8822](#hub-8822) | updateRestriction no longer checks the share class exists, so a restriction update goes out for a class never created.<br>Caught by: [`rvHuShareClassMessagesRefuseAnUncreatedClass`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L386) |
| [8823](#hub-8823) | notifyAssetPrice checks the share class exists, so no price notice goes out for a class never created.<br>Caught by: [`rcHuAssetPriceNoticeForAnUnknownAssetAndClassIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1124) |
| [8824](#hub-8824) | notifySharePrice checks the share class exists, so no share price notice goes out for a class never created.<br>Caught by: [`rcHuSharePriceNoticeForAnUncreatedClassIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1142) |
| [8825](#hub-8825) | notifyShareClass checks only the manager seat, so an installed policy is never asked about a share class notice.<br>Caught by: [`rcHuShareClassNoticeConsultsTheInstalledPolicyIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1159) |
| [8826](#hub-8826) | installing a policy always runs the manager and policy checks, so a ward who is no manager, or faces a refusing policy, is refused.<br>Caught by: [`rvHuWardPolicyInstallOutlivesARefusingRuleBook`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L407) |
| [8827](#hub-8827) | cancelAuthorization refuses to cancel a pending manager change, so a manager cannot veto its own removal.<br>Caught by: [`rvHuCancelAuthorizationIsNeverRefusedToAnAdmittedManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L426) |
| [8828](#hub-8828) | a manager call checks its declared value against the raw call value, so a batched local call declaring the batch's ETH passes.<br>Caught by: [`rvHuManagerCallRefusesAMisdeclaredValue`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L173) |
| [9007](#hub-9007) | writing a pool's metadata also unplugs the hub's fee accrual, so every pool stops accruing fees after one metadata change.<br>Caught by: [`hlHuMetadataWritersAndRescueWriteNoHubField`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L20) |
| [9033](#hub-9033) | A holding markdown no longer posts to the ledger, so a value loss leaves the pool's books unchanged.<br>Caught by: [`stHuValueMoveIsBookedExactly`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L154) |
| [9034](#hub-9034) | Registering a pool no longer records its currency, so the pool gains a manager seat without a currency.<br>Caught by: [`stHrOperatorSeatNeedsItsOwnPoolsCurrency`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L88) |
| [9035](#hub-9035) | Opening a ledger account no longer checks that it exists, so reopening a live row wipes its debit and credit totals.<br>Caught by: [`stHuLedgerTotalsMoveOnlyThroughJournalling`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L224) |
| [9036](#hub-9036) | The credit leg of a holding's posting is booked as a debit, so every nonzero posting reverts unbalanced.<br>Caught by: [`rvHuJournalPrimitiveIsNeverRefusedUnbalanced`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L278) |
| [9140](#hub-9140) | announcing a pool to a spoke skips the manager and policy checks, so any caller can announce the pool.<br>Caught by: [`rvHuManagerFacingEntryRefusesANonManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L243) |
| [9141](#hub-9141) | posting a holding amount needs a pool manager instead of a hub admin, so a manager can book amounts no spoke reported.<br>Caught by: [`rvHuJournalPrimitivesRefuseANonWard`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L260) |
| [9142](#hub-9142) | a holding's posting pair never closes the ledger session it opened, so the hub leaves the ledger unlocked and unchecked for balance.<br>Caught by: [`stHuEveryHubCallLeavesTheLedgerLocked`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L190) |
| [9144](#hub-9144) | adapter changes are no longer refused during a batch, so the announcement can travel over a set the destination lacks.<br>Caught by: [`rvHuSetAdaptersRefusesWhileBatching`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L305) |
| [9145](#hub-9145) | a withdrawal is posted like a deposit, debiting the holding's own account and crediting its counterpart instead of the other way about.<br>Caught by: [`hlHuJournalPrimitivePostsOneBalancedPair`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L113) |
| [9146](#hub-9146) | the adapter announcement names the session after the one installed locally, so the destination and the hub converge on different sessions.<br>Caught by: [`hlHuSetAdaptersAnnouncesTheSessionItInstalls`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L140) |
| [9147](#hub-9147) | both revaluation postings book the holding's own account on the wrong side, so a write down debits it instead of crediting it.<br>Caught by: [`hlHuValuationDropNeverRaisesTheHoldingRowsValue`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L173) |
| [9148](#hub-9148) | both amount postings book the holding's own account on the wrong side, so an increase credits it instead of debiting it.<br>Caught by: [`stHuProtocolValueMovesLandOnTheHoldingsOwnRow`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L201) |
| [9149](#hub-9149) | a hub admin bypasses the manager gate only while no policy is set, so a standing policy can no longer be replaced without its consent.<br>Caught by: [`rcHuGovernanceReplacesAStandingRuleBookIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L895) |
| [9150](#hub-9150) | a write down debits the holding's own account instead of crediting it, so a drop can no longer raise a credit normal account.<br>Caught by: [`rcHuValuationDropRaisesACreditNormalHoldingRowIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L914) |
| [9151](#hub-9151) | a manager authored journal opens and closes the ledger without posting its entries, so no manual journal can move a holding's account.<br>Caught by: [`rcHuManualJournalMovesAHoldingRowButNotItsValueIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L936) |
| [9152](#hub-9152) | a holding's own amount debit slot can no longer be repointed, so no rewiring can leave its carried value unmatched by the account it names.<br>Caught by: [`rcHuRewiredHoldingRowLeavesItsValueUnmatchedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L959) |
| [9154](#hub-9154) | rewiring a request manager through the hub no longer tells the spoke, so hub and spoke route requests to mismatched managers.<br>Caught by: [`rcHuHubPathRequestManagerRewireDispatchesTheSyncIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1000) |
| [9477](#hub-9477) | opening a holding books its tracked amount's value as a gain instead of principal, so the credit hits the gain account.<br>Caught by: [`hlHuInitializationBooksTheTrackedAmountAsPrincipal`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L201) |
| [9478](#hub-9478) | a share price update no longer calls the installed fee hook, so fees stop accruing on every share price move.<br>Caught by: [`hlHuSharePriceUpdateAccruesExactlyWhenAFeeHookIsInstalled`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L229) · [`hlHuSharePriceUpdateStampedNowAccruesExactlyWhenAFeeHookIsInstalled`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L247) |
| [9479](#hub-9479) | the pool's policy is told the hub is the caller, so a per caller policy judges the wrong party.<br>Caught by: [`rvHuEnforcedEntryPassesTheInstalledPolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L319) · [`rvHuSpokeCallRevokePassesThePolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L344) |
| [9480](#hub-9480) | writing pool metadata skips the manager and policy checks, so any caller can rewrite what the pool publishes.<br>Caught by: [`rvHuPoolMetadataWriterPassesBothGates`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L42) |
| [9481](#hub-9481) | writing an account's metadata opens a ledger session for the pool and returns without closing it, so the ledger stays unlocked after the call.<br>Caught by: [`stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L6) |
| [9482](#hub-9482) | a hub admin replacing a pool's policy must first pass the standing policy, so the governance override can be blocked by the policy it replaces.<br>Caught by: [`rcHuWardSwapsARefusingRuleBookWithoutItsConsentIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1016) |
| [9483](#hub-9483) | an asset price notification no longer calls the installed fee hook, so fees stop accruing on every asset price broadcast.<br>Caught by: [`hlHuAssetPriceNotificationAccruesExactlyWhenAFeeHookIsInstalled`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L265) |
| [9484](#hub-9484) | writing an account's metadata no longer asks for a pool manager or passes the pool's policy, so any caller can relabel the pool's ledger accounts.<br>Caught by: [`rvHuAccountMetadataWriterPassesBothGates`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L65) |
| [9485](#hub-9485) | renaming a share class skips the manager and policy checks, so any caller can rename a class and its symbol.<br>Caught by: [`rvHuShareClassMetadataWriterPassesBothGates`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L89) |
| [9486](#hub-9486) | writing a pool's metadata opens a ledger session for the pool and returns without closing it, so the ledger stays unlocked after the call.<br>Caught by: [`stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L6) |
| [9487](#hub-9487) | renaming a share class opens a ledger session for the pool and returns without closing it, so the ledger stays unlocked after the call.<br>Caught by: [`stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L6) |
| [9710](#hub-9710) | the hub installs the new local adapter set before sending the remote update, so the update may never arrive.<br>Caught by: [`hlHuSetAdaptersSendsBeforeItInstalls`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L156) |

## Hub #1

createPool no longer checks that the pool id carries the hub's own network prefix, so a foreign pool can be registered locally.

- **Mutant:** [`1.sol`](1.sol)
- **Caught by:** [`registeredPoolIsLocal`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L46)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 1`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule registeredPoolIsLocal`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -93,7 +93,7 @@
 
     /// @inheritdoc ICreatePool
     function createPool(PoolId poolId, address admin, AssetId currency) external payable auth {
-        require(poolId.centrifugeId() == sender.localCentrifugeId(), InvalidPoolId());
+        // MUTATION: removed the local network prefix check on the pool id
         hubRegistry.registerPool(poolId, admin, currency);
     }
 
```

## Hub #2

createPool checks the pool id against the currency's network instead of the hub's, so a foreign pool can register.

- **Mutant:** [`2.sol`](2.sol)
- **Caught by:** [`registeredPoolIsLocal`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L46)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 2`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule registeredPoolIsLocal`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -93,7 +93,7 @@
 
     /// @inheritdoc ICreatePool
     function createPool(PoolId poolId, address admin, AssetId currency) external payable auth {
-        require(poolId.centrifugeId() == sender.localCentrifugeId(), InvalidPoolId());
+        require(poolId.centrifugeId() == currency.centrifugeId(), InvalidPoolId()); // MUTATION: pool id validated against the currency network
         hubRegistry.registerPool(poolId, admin, currency);
     }
 
```

## Hub #3

initializeHolding verifies the existence of only the first three journal accounts, so the fourth is linked without ever being created.

- **Mutant:** [`3.sol`](3.sol)
- **Caught by:** [`holdingAccountIdsExist`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L25) · [`initializedHoldingHasAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 3`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule holdingAccountIdsExist initializedHoldingHasAccounts`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -336,7 +336,7 @@
         _requireSC(poolId, scId);
 
         require(hubRegistry.isRegistered(assetId), IHubRegistry.AssetNotFound());
-        for (uint256 i; i < accounts.length; i++) {
+        for (uint256 i; i < accounts.length - 1; i++) { // MUTATION: existence loop stops one account early
             require(accounting.exists(poolId, accounts[i]), IAccounting.AccountDoesNotExist());
         }
 
```

## Hub #4

initializeHolding re-checks the first journal account on every loop pass, so the other three are linked without existence checks.

- **Mutant:** [`4.sol`](4.sol)
- **Caught by:** [`holdingAccountIdsExist`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L25) · [`initializedHoldingHasAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule holdingAccountIdsExist initializedHoldingHasAccounts`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -337,7 +337,7 @@
 
         require(hubRegistry.isRegistered(assetId), IHubRegistry.AssetNotFound());
         for (uint256 i; i < accounts.length; i++) {
-            require(accounting.exists(poolId, accounts[i]), IAccounting.AccountDoesNotExist());
+            require(accounting.exists(poolId, accounts[0]), IAccounting.AccountDoesNotExist()); // MUTATION: checks the first account on every iteration
         }
 
         holdings.initialize(poolId, scId, assetId, valuation, accounts);
```

## Hub #5

setHoldingAccountId no longer checks the account exists in the ledger, so a holding can reference an absent or null account id.

- **Mutant:** [`5.sol`](5.sol)
- **Caught by:** [`holdingAccountIdsExist`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L25) · [`initializedHoldingHasAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 5`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule holdingAccountIdsExist initializedHoldingHasAccounts`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -371,7 +371,7 @@
         payable
         enforced(poolId)
     {
-        require(accounting.exists(poolId, accountId), IAccounting.AccountDoesNotExist());
+        // MUTATION: removed the account existence check before linking
 
         holdings.setAccountId(poolId, scId, assetId, kind, accountId);
     }
```

## Hub #6

initializeHolding no longer checks the asset is registered, so a holding can be initialized for an unknown asset.

- **Mutant:** [`6.sol`](6.sol)
- **Caught by:** [`initializedHoldingAssetRegistered`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule initializedHoldingAssetRegistered`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -335,7 +335,7 @@
     ) external payable enforced(poolId) {
         _requireSC(poolId, scId);
 
-        require(hubRegistry.isRegistered(assetId), IHubRegistry.AssetNotFound());
+        // MUTATION: removed the asset registration check
         for (uint256 i; i < accounts.length; i++) {
             require(accounting.exists(poolId, accounts[i]), IAccounting.AccountDoesNotExist());
         }
```

## Hub #7

initializeHolding checks that the pool exists instead of that the asset is registered, so a holding can be initialized for an unknown asset.

- **Mutant:** [`7.sol`](7.sol)
- **Caught by:** [`initializedHoldingAssetRegistered`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 7`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule initializedHoldingAssetRegistered`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -335,7 +335,7 @@
     ) external payable enforced(poolId) {
         _requireSC(poolId, scId);
 
-        require(hubRegistry.isRegistered(assetId), IHubRegistry.AssetNotFound());
+        require(hubRegistry.exists(poolId), IHubRegistry.AssetNotFound()); // MUTATION: checks pool existence instead of asset registration
         for (uint256 i; i < accounts.length; i++) {
             require(accounting.exists(poolId, accounts[i]), IAccounting.AccountDoesNotExist());
         }
```

## Hub #3006

initializeHolding no longer checks that the four journal accounts exist, so a holding wires itself to void accounts.

- **Mutant:** [`3006.sol`](3006.sol)
- **Caught by:** [`holdingAccountIdsExist`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L25) · [`initializedHoldingHasAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 3006`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule holdingAccountIdsExist initializedHoldingHasAccounts`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -336,9 +336,7 @@
         _requireSC(poolId, scId);
 
         require(hubRegistry.isRegistered(assetId), IHubRegistry.AssetNotFound());
-        for (uint256 i; i < accounts.length; i++) {
-            require(accounting.exists(poolId, accounts[i]), IAccounting.AccountDoesNotExist());
-        }
+        // MUTATION: the four journal accounts are no longer required to exist
 
         holdings.initialize(poolId, scId, assetId, valuation, accounts);
 
```

## Hub #3012

updateHoldingValuation rewires an account slot while it changes the price source, so a repricing redirects where entries post.

- **Mutant:** [`3012.sol`](3012.sol)
- **Caught by:** [`stHuPriceSourceSwapNeverRewiresTheAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L174)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 3012`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule stHuPriceSourceSwapNeverRewiresTheAccounts`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -363,6 +363,8 @@
         enforced(poolId)
     {
         holdings.updateValuation(poolId, scId, assetId, valuation);
+        // MUTATION: the repricing also rewires the amount-debit slot
+        holdings.setAccountId(poolId, scId, assetId, uint8(AccountKind.AmountDebit), AccountId.wrap(0));
     }
 
     /// @inheritdoc IHub
```

## Hub #3013

A policy swap installs the replacement under the number the old policy ran on, so authorizations granted under the previous rule book survive the change.

- **Mutant:** [`3013.sol`](3013.sol)
- **Caught by:** [`stHuPolicySwapAdvancesTheAuthorizationNamespace`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 3013`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule stHuPolicySwapAdvancesTheAuthorizationNamespace`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,8 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        // MUTATION: the replacement is installed under the number the old policy ran on
+        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce);
 
         emit SetPolicy(poolId_, policy_);
     }
```

## Hub #3020

unlock reuses the prior journal id instead of advancing the counter, so a ledger move is filed under a stale journal.

- **Mutant:** [`3020.sol`](3020.sol)
- **Caught by:** [`stHuLedgerMoveIsFiledUnderAFreshJournal`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L136)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 3020`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule stHuLedgerMoveIsFiledUnderAFreshJournal`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -155,6 +155,6 @@
     }
 
     function _generateJournalId(PoolId poolId) internal returns (uint256) {
-        return uint256((uint256(poolId.raw()) << 128) | ++_poolJournalIdCounter[poolId]);
+        return uint256((uint256(poolId.raw()) << 128) | _poolJournalIdCounter[poolId] /* MUTATION: no ++, journal id not fresh */);
     }
 }
```

## Hub #3046

addCredit never adds the value to the account's credit total, so the pool's debits and credits stop balancing.

- **Mutant:** [`3046.sol`](3046.sol)
- **Caught by:** [`journalDebitsEqualCredits`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L17)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 3046`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule journalDebitsEqualCredits`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -106,7 +106,7 @@
         Account storage acc = accounts[_currentPoolId][account];
         require(acc.lastUpdated != 0, AccountDoesNotExist());
 
-        acc.totalCredit += value;
+        // MUTATION: the credit is not accumulated into the account row, breaking double-entry at rest
         credited += value;
         acc.lastUpdated = uint64(block.timestamp);
         emit Credit(_currentPoolId, account, value);
```

## Hub #4800

rely drops the ward gate, so any caller can hand itself the authority the hub reserves for the root and the guardians.

- **Mutant:** [`4800.sol`](4800.sol)
- **Caught by:** [`acHuWardSetMovesOnlyForAWard`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4800`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/access_control.conf --rule acHuWardSetMovesOnlyForAWard`

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

## Hub #4801

file drops the ward gate, so any caller can repoint the hub's gateway, sender, adapter set or fee hook.

- **Mutant:** [`4801.sol`](4801.sol)
- **Caught by:** [`acHuWiringMovesOnlyForAWard`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4801`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/access_control.conf --rule acHuWiringMovesOnlyForAWard`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -82,7 +82,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IHub
-    function file(bytes32 what, address data) external auth {
+    function file(bytes32 what, address data) external { // MUTATION: the wiring switch is open to any caller
         if (what == "gateway") gateway = IGateway(data);
         else if (what == "feeAccrual") feeAccrual = IFeeAccrual(data);
         else if (what == "sender") sender = IHubMessageSender(data);
```

## Hub #4802

createPool drops the ward gate, so any caller can open a pool and thereby set its accounting currency and seat its first manager.

- **Mutant:** [`4802.sol`](4802.sol)
- **Caught by:** [`acHuPoolCurrencyMovesOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L46) · [`acHuManagerSeatMovesOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L65)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4802`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/access_control.conf --rule acHuPoolCurrencyMovesOnlyForAWardOrManager acHuManagerSeatMovesOnlyForAWardOrManager`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -92,7 +92,7 @@
     }
 
     /// @inheritdoc ICreatePool
-    function createPool(PoolId poolId, address admin, AssetId currency) external payable auth {
+    function createPool(PoolId poolId, address admin, AssetId currency) external payable { // MUTATION: pool creation is open to any caller
         require(poolId.centrifugeId() == sender.localCentrifugeId(), InvalidPoolId());
         hubRegistry.registerPool(poolId, admin, currency);
     }
```

## Hub #4803

setPolicy drops the ward or manager check, so any caller can install a pool's policy and void its pending authorizations.

- **Mutant:** [`4803.sol`](4803.sol)
- **Caught by:** [`acHuPoolPolicyMovesOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L85)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4803`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/access_control.conf --rule acHuPoolPolicyMovesOnlyForAWardOrManager`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -99,7 +99,7 @@
 
     /// @inheritdoc IHub
     function setPolicy(PoolId poolId, IHubPolicy policy_) external {
-        if (wards[msgSender()] != 1) _enforce(poolId);
+        // MUTATION: neither a ward nor a manager seat is required to install a rule book
 
         hubRegistry.setPolicy(poolId, policy_);
     }
```

## Hub #4804

The pool gate admits hub wards instead of pool managers, so a ward with no seat can act as the pool's manager.

- **Mutant:** [`4804.sol`](4804.sol)
- **Caught by:** [`acHuAuthorizationLedgerMovesThroughTheHubOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L107) · [`acHuBridgingHookMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L126) · [`acHuRequestManagerSeatMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L143) · [`acHuSnapshotHookMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L162) · [`acHuShareClassRegisterMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L237) · [`acHuSharePriceMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L264) · [`acHuAccountCreationNeedsAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L284) · [`acHuOutboundInstructionNeedsAPoolManagerOrARequestFulfilment`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L382)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4804`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/access_control.conf --rule acHuAuthorizationLedgerMovesThroughTheHubOnlyForAPoolManager acHuBridgingHookMovesOnlyForAPoolManager acHuRequestManagerSeatMovesOnlyForAPoolManager acHuSnapshotHookMovesOnlyForAPoolManager acHuShareClassRegisterMovesOnlyForAPoolManager acHuSharePriceMovesOnlyForAPoolManager acHuAccountCreationNeedsAPoolManager acHuOutboundInstructionNeedsAPoolManagerOrARequestFulfilment`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -596,7 +596,7 @@
     //----------------------------------------------------------------------------------------------
 
     function _enforce(PoolId poolId) internal {
-        _requireManager(poolId);
+        require(wards[msgSender()] == 1, IHub.NotManager()); // MUTATION: a hub ward passes as a manager of every pool
 
         IHubPolicy policy_ = hubRegistry.policy(poolId);
         if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), msg.data);
```

## Hub #4805

initializeHolding drops the pool gate, so any caller can open a holding and set its price source, ledger accounts and value.

- **Mutant:** [`4805.sol`](4805.sol)
- **Caught by:** [`acHuHoldingValuationMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L180) · [`acHuHoldingAccountWiringMovesOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L199) · [`acHuHoldingValueMovesThroughTheHubOnlyForAPoolManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L218)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4805`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/access_control.conf --rule acHuHoldingValuationMovesOnlyForAPoolManager acHuHoldingAccountWiringMovesOnlyForAPoolManager acHuHoldingValueMovesThroughTheHubOnlyForAPoolManager`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -332,7 +332,7 @@
         AssetId assetId,
         IValuation valuation,
         AccountId[4] calldata accounts
-    ) external payable enforced(poolId) {
+    ) external payable { // MUTATION: opening a holding no longer needs a manager seat
         _requireSC(poolId, scId);
 
         require(hubRegistry.isRegistered(assetId), IHubRegistry.AssetNotFound());
```

## Hub #4806

updateJournal drops the pool gate, so any caller can post debits and credits into a pool's books.

- **Mutant:** [`4806.sol`](4806.sol)
- **Caught by:** [`acHuAccountDebitMovesThroughTheHubOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L302) · [`acHuAccountCreditMovesThroughTheHubOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L322) · [`acHuJournalCounterMovesThroughTheHubOnlyForAWardOrManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L342)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4806`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/access_control.conf --rule acHuAccountDebitMovesThroughTheHubOnlyForAWardOrManager acHuAccountCreditMovesThroughTheHubOnlyForAWardOrManager acHuJournalCounterMovesThroughTheHubOnlyForAWardOrManager`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -380,7 +380,7 @@
     function updateJournal(PoolId poolId, JournalEntry[] memory debits, JournalEntry[] memory credits)
         external
         payable
-        enforced(poolId)
+        // MUTATION: posting a journal no longer needs a manager seat
     {
         accounting.unlock(poolId);
         accounting.addJournal(debits, credits);
```

## Hub #4807

requestCallback finds the request manager on the hub's network, not the asset's, so a local manager answers for other networks.

- **Mutant:** [`4807.sol`](4807.sol)
- **Caught by:** [`acHuRequestCallbackNeedsTheRegisteredRequestManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_access_control.spec#L361)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4807`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/access_control.conf --rule acHuRequestCallbackNeedsTheRegisteredRequestManager`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -514,7 +514,7 @@
         bool unpaidMode,
         address refund
     ) external payable {
-        IHubRequestManager manager = hubRegistry.hubRequestManager(poolId, assetId.centrifugeId());
+        IHubRequestManager manager = hubRegistry.hubRequestManager(poolId, sender.localCentrifugeId()); // MUTATION: the request manager is looked up on the hub's own network
         require(address(manager) != address(0), InvalidRequestManager());
         require(msg.sender == address(manager), NotAuthorized());
 
```

## Hub #4808

Every hub posting credits the amount credit account whatever kind it names, so an equal round trip no longer nets to zero.

- **Mutant:** [`4808.sol`](4808.sol)
- **Caught by:** [`hlHuAmountRoundTripKeepsEveryAccountNet`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L4) · [`hlHuValueRoundTripKeepsTheHoldingAccountNetWhenGainAndLossAreOtherAccounts`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L20)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4808`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuAmountRoundTripKeepsEveryAccountNet hlHuValueRoundTripKeepsTheHoldingAccountNetWhenGainAndLossAreOtherAccounts`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -574,7 +574,7 @@
     ) private {
         accounting.unlock(poolId);
         accounting.addDebit(holdings.accountId(poolId, scId, assetId, uint8(debitKind)), diff);
-        accounting.addCredit(holdings.accountId(poolId, scId, assetId, uint8(creditKind)), diff);
+        accounting.addCredit(holdings.accountId(poolId, scId, assetId, uint8(AccountKind.AmountCredit)), diff); // MUTATION: every credit leg lands on the amount credit slot
         accounting.lock();
     }
 
```

## Hub #4809

a revaluation clears the holding's amount credit slot, so a pool's account wiring moves on an entry that was never meant to touch it.

- **Mutant:** [`4809.sol`](4809.sol)
- **Caught by:** [`vtHuAccountWiringMovesOnlyThroughWiringEntries`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4809`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule vtHuAccountWiringMovesOnlyThroughWiringEntries`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -202,6 +202,7 @@
         diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
 
         holding_.assetAmountValue = currentAmountValue;
+        accountId[poolId][scId][assetId][1] = AccountId.wrap(0); // MUTATION: a revaluation clears the holding's amount credit slot
 
         emit Update(poolId, scId, assetId, isPositive, diffValue);
     }
```

## Hub #4810

Setting a holding account also clears the holding's price source, so its valuation changes outside the valuation setters.

- **Mutant:** [`4810.sol`](4810.sol)
- **Caught by:** [`vtHuValuationMovesOnlyThroughItsInstallers`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L70)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4810`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule vtHuValuationMovesOnlyThroughItsInstallers`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -71,6 +71,7 @@
         require(address(holding_.valuation) != address(0), HoldingNotFound());
 
         accountId[poolId][scId][assetId][kind] = accountId_;
+        holding_.valuation = IValuation(address(0)); // MUTATION: wiring an account slot drops the holding's price source
 
         emit SetAccountId(poolId, scId, assetId, kind, accountId_);
     }
```

## Hub #4811

Opening a holding also installs its price source as the pool's snapshot hook, so the hook changes outside its setter.

- **Mutant:** [`4811.sol`](4811.sol)
- **Caught by:** [`vtHuSnapshotHookMovesOnlyThroughItsSetter`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L86)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4811`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule vtHuSnapshotHookMovesOnlyThroughItsSetter`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -54,6 +54,7 @@
         require(address(holding_.valuation) == address(0), AlreadyInitialized());
 
         holding_.valuation = valuation_;
+        snapshotHook[poolId] = ISnapshotHook(address(valuation_)); // MUTATION: opening a holding installs its price source as the pool's snapshot hook
 
         for (uint256 i; i < 4; i++) {
             accountId[poolId][scId][assetId][uint8(i)] = accounts[i];
```

## Hub #4813

The pool gate no longer requires a manager seat, so the entries it guards stop refusing callers the pool never appointed.

- **Mutant:** [`4813.sol`](4813.sol)
- **Caught by:** [`rvHuSetPolicyRefusesAnUnauthorisedInstall`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L39) · [`rvHuCancelAuthorizationRefusesANonManagerOrAnEmptySlot`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L73) · [`rvHuUpdateHubManagerRefusesANonManagerOrANullSeat`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L90) · [`rvHuUpdateCurrencyRefusesARescalingRedenomination`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L105) · [`rvHuCreateAccountRefusesARepeatOrAnUnusableOpening`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L124) · [`rvHuSetHoldingAccountIdRefusesAnAbsentRowOrHolding`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L140) · [`rvHuUpdateHoldingValuationRefusesANullSourceOrClosedHolding`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L157) · [`rvHuInitializeHoldingRefusesARepeatOrAnUnusableOpening`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L220) · [`rvHuSpokeCallRevokePassesThePolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L344) · [`rvHuCancelAuthorizationIsNeverRefusedToAnAdmittedManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L426)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4813`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuSetPolicyRefusesAnUnauthorisedInstall rvHuCancelAuthorizationRefusesANonManagerOrAnEmptySlot rvHuUpdateHubManagerRefusesANonManagerOrANullSeat rvHuUpdateCurrencyRefusesARescalingRedenomination rvHuCreateAccountRefusesARepeatOrAnUnusableOpening rvHuSetHoldingAccountIdRefusesAnAbsentRowOrHolding rvHuUpdateHoldingValuationRefusesANullSourceOrClosedHolding rvHuInitializeHoldingRefusesARepeatOrAnUnusableOpening rvHuSpokeCallRevokePassesThePolicy rvHuCancelAuthorizationIsNeverRefusedToAnAdmittedManager`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -596,7 +596,7 @@
     //----------------------------------------------------------------------------------------------
 
     function _enforce(PoolId poolId) internal {
-        _requireManager(poolId);
+        // MUTATION: a manager seat is no longer required to drive a pool
 
         IHubPolicy policy_ = hubRegistry.policy(poolId);
         if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), msg.data);
```

## Hub #4814

file accepts a dependency name the hub does not wire instead of refusing it, so a call that rewires nothing still succeeds.

- **Mutant:** [`4814.sol`](4814.sol)
- **Caught by:** [`rvHuFileRefusesANonWardOrAnUnknownName`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4814`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuFileRefusesANonWardOrAnUnknownName`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -87,7 +87,7 @@
         else if (what == "feeAccrual") feeAccrual = IFeeAccrual(data);
         else if (what == "sender") sender = IHubMessageSender(data);
         else if (what == "multiAdapter") multiAdapter = IMultiAdapter(data);
-        else revert FileUnrecognizedParam();
+        // MUTATION: an unrecognized dependency name no longer refuses the call
         emit File(what, data);
     }
 
```

## Hub #4815

registering a pool no longer refuses the null opening operator, so a pool opens seated on an address nobody can ever act from.

- **Mutant:** [`4815.sol`](4815.sol)
- **Caught by:** [`rvHuCreatePoolRefusesARepeatOrAnUnusableOpening`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L20)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4815`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuCreatePoolRefusesARepeatOrAnUnusableOpening`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -59,7 +59,7 @@
     /// @inheritdoc IHubRegistry
     function registerPool(PoolId poolId_, address manager_, AssetId currency_) external auth {
         require(!poolId_.isNull(), InvalidPool());
-        require(manager_ != address(0), EmptyAccount());
+        // MUTATION: the opening operator may be the null address
         require(!currency_.isNull(), EmptyCurrency());
         require(isRegistered(currency_), AssetNotFound());
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
```

## Hub #4816

Scheduling an authorization no longer refuses a call the policy already allows, so a zero delay call enters the timelock.

- **Mutant:** [`4816.sol`](4816.sol)
- **Caught by:** [`rvHuInitiateAuthorizationRefusesAnUnauthorisedOrDuplicateSchedule`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L55)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4816`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuInitiateAuthorizationRefusesAnUnauthorisedOrDuplicateSchedule`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -142,7 +142,7 @@
 
         // Only an out-of-policy call may be authorized: an in-policy call would mature instantly.
         uint48 delaySeconds = info.policy.authorizationDelay(poolId_, caller, data);
-        require(delaySeconds != 0, InPolicy());
+        // MUTATION: a call the rule book already allows may be scheduled too
 
         // Reject re-authorizing: it would silently reset the maturity clock, so cancel first.
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
```

## Hub #4817

managerCall no longer matches the declared local value to the destination, so a misdeclared call is sent instead of refused.

- **Mutant:** [`4817.sol`](4817.sol)
- **Caught by:** [`rvHuManagerCallRefusesAMisdeclaredValue`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L173)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4817`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuManagerCallRefusesAMisdeclaredValue`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -489,10 +489,7 @@
         address refund
     ) external payable enforced(poolId) {
         // Gas is explicit: a local call is funded entirely by `msg.value`, a remote call carries none.
-        require(
-            centrifugeId == sender.localCentrifugeId() ? localValue == msgValue() : localValue == 0,
-            ManagerCallUnexpectedValue()
-        );
+        // MUTATION: a manager call no longer has to declare the value its destination allows
 
         emit ManagerCall(centrifugeId, poolId, target, payload);
         sender.sendManagerCallFromHub{value: msgValue()}(
```

## Hub #4818

requestCallback no longer checks the caller is the pool's request manager, so anyone can push a request result to the spoke.

- **Mutant:** [`4818.sol`](4818.sol)
- **Caught by:** [`rvHuRequestCallbackRefusesAnyCallerButTheRegisteredManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L189)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4818`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuRequestCallbackRefusesAnyCallerButTheRegisteredManager`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -516,7 +516,7 @@
     ) external payable {
         IHubRequestManager manager = hubRegistry.hubRequestManager(poolId, assetId.centrifugeId());
         require(address(manager) != address(0), InvalidRequestManager());
-        require(msg.sender == address(manager), NotAuthorized());
+        // MUTATION: the caller no longer has to be the pool's registered request manager
 
         sender.sendRequestCallback{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);
     }
```

## Hub #4820

The asset price read no longer falls back to par for an unopened holding, so it reverts instead of answering.

- **Mutant:** [`4820.sol`](4820.sol)
- **Caught by:** [`rvHuPricePoolPerAssetAnswersForAnUnopenedHolding`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L204)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4820`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuPricePoolPerAssetAnswersForAnUnopenedHolding`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -585,7 +585,7 @@
     /// @inheritdoc IHub
     function pricePoolPerAsset(PoolId poolId, ShareClassId scId, AssetId assetId) public view returns (D18) {
         // Assume price of 1.0 if the holding is not initialized yet
-        if (!holdings.isInitialized(poolId, scId, assetId)) return d18(1, 1);
+        // MUTATION: an unopened holding no longer falls back to par
 
         IValuation valuation = holdings.valuation(poolId, scId, assetId);
         return valuation.getPrice(poolId, scId, assetId);
```

## Hub #4821

installing a rule book advances the pool's authorization tenure by two, so the tenure skips a number.

- **Mutant:** [`4821.sol`](4821.sol)
- **Caught by:** [`vtHuAuthorizationTenureStepsByAtMostOne`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4821`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule vtHuAuthorizationTenureStepsByAtMostOne`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 2); // MUTATION: the authorization tenure advances by two
 
         emit SetPolicy(poolId_, policy_);
     }
```

## Hub #4822

opening a journal advances the pool's journal numbering by two, so the sequence skips a number and the audit trail carries a gap.

- **Mutant:** [`4822.sol`](4822.sol)
- **Caught by:** [`vtHuJournalSequenceStepsByAtMostOne`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4822`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule vtHuJournalSequenceStepsByAtMostOne`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -155,6 +155,6 @@
     }
 
     function _generateJournalId(PoolId poolId) internal returns (uint256) {
-        return uint256((uint256(poolId.raw()) << 128) | ++_poolJournalIdCounter[poolId]);
+        return uint256((uint256(poolId.raw()) << 128) | (_poolJournalIdCounter[poolId] += 2)); // MUTATION: the per pool journal counter advances by two
     }
 }
```

## Hub #4823

adding a share class advances the pool's class numbering by two, so an index is skipped.

- **Mutant:** [`4823.sol`](4823.sol)
- **Caught by:** [`vtHuShareClassSequenceStepsByAtMostOne`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4823`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule vtHuShareClassSequenceStepsByAtMostOne`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -50,7 +50,7 @@
 
         scId_ = previewNextShareClassId(poolId);
 
-        uint32 index = ++shareClassCount[poolId];
+        uint32 index = (shareClassCount[poolId] += 2); // MUTATION: the share class numbering advances by two
         shareClassIds[poolId][scId_] = true;
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
```

## Hub #4825

initializeHolding no longer checks the share class exists, so a holding opens on a class never created.

- **Mutant:** [`4825.sol`](4825.sol)
- **Caught by:** [`initializedHoldingImpliesShareClassExists`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L51)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4825`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule initializedHoldingImpliesShareClassExists`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -333,7 +333,7 @@
         IValuation valuation,
         AccountId[4] calldata accounts
     ) external payable enforced(poolId) {
-        _requireSC(poolId, scId);
+        // MUTATION: removed the share class gate
 
         require(hubRegistry.isRegistered(assetId), IHubRegistry.AssetNotFound());
         for (uint256 i; i < accounts.length; i++) {
```

## Hub #4826

the pool gate admits hub wards instead of pool managers, so a ward can open a ledger row on a pool never created.

- **Mutant:** [`4826.sol`](4826.sol)
- **Caught by:** [`ledgerAccountImpliesRegisteredPool`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_valid_state.spec#L56)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 4826`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/valid_state.conf --rule ledgerAccountImpliesRegisteredPool`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -596,7 +596,7 @@
     //----------------------------------------------------------------------------------------------
 
     function _enforce(PoolId poolId) internal {
-        _requireManager(poolId);
+        require(wards[msgSender()] == 1, IHub.NotManager()); // MUTATION: a hub ward passes as a manager of every pool
 
         IHubPolicy policy_ = hubRegistry.policy(poolId);
         if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), msg.data);
```

## Hub #6200

opening a pool records its currency but never seats the named operator, so the pool starts with no manager.

- **Mutant:** [`6200.sol`](6200.sol)
- **Caught by:** [`rcHuCreatePoolSeatsADelegateIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L4) · [`rcHuCreatePoolSeatsTheOpeningWardIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6200`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuCreatePoolSeatsADelegateIsReachable rcHuCreatePoolSeatsTheOpeningWardIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -64,7 +64,7 @@
         require(isRegistered(currency_), AssetNotFound());
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
-        manager[poolId_][manager_] = true;
+        // MUTATION: the opening operator is never seated
         currency[poolId_] = currency_;
 
         emit NewPool(poolId_, manager_, currency_);
```

## Hub #6201

pool registration treats the smallest usable asset id as an empty currency, so the bottom edge of the asset id space cannot denominate a pool.

- **Mutant:** [`6201.sol`](6201.sol)
- **Caught by:** [`rcHuCreatePoolAtTheSmallestCurrencyIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6201`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuCreatePoolAtTheSmallestCurrencyIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -60,7 +60,7 @@
     function registerPool(PoolId poolId_, address manager_, AssetId currency_) external auth {
         require(!poolId_.isNull(), InvalidPool());
         require(manager_ != address(0), EmptyAccount());
-        require(!currency_.isNull(), EmptyCurrency());
+        require(currency_.raw() > 1, EmptyCurrency()); // MUTATION: the smallest asset id counts as empty
         require(isRegistered(currency_), AssetNotFound());
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
```

## Hub #6202

the seat entry clears the operator seat whatever the flag asks for, so an appointment withdraws the seat it meant to grant.

- **Mutant:** [`6202.sol`](6202.sol)
- **Caught by:** [`rcHuPoolBirthThenDelegationIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L57) · [`rcHuSecondOperatorAppointmentIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L79) · [`rcHuOperatorSeatRoundTripIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L93)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6202`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuPoolBirthThenDelegationIsReachable rcHuSecondOperatorAppointmentIsReachable rcHuOperatorSeatRoundTripIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -79,7 +79,7 @@
         require(exists(poolId_), NonExistingPool());
         require(who != address(0), EmptyAccount());
 
-        manager[poolId_][who] = canManage;
+        manager[poolId_][who] = false; // MUTATION: the seat is cleared whatever the flag asks
 
         emit UpdateManager(poolId_, who, canManage);
     }
```

## Hub #6203

an operator is refused any change to its own seat, so standing down needs a second operator to act for it.

- **Mutant:** [`6203.sol`](6203.sol)
- **Caught by:** [`rcHuOperatorCanStandItselfDownIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L112)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6203`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuOperatorCanStandItselfDownIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -185,6 +185,7 @@
 
     /// @inheritdoc IHub
     function updateHubManager(PoolId poolId, address who, bool canManage) external payable enforced(poolId) {
+        require(who != msgSender(), IHub.NotManager()); // MUTATION: an operator may not move its own seat
         hubRegistry.updateManager(poolId, who, canManage);
     }
 
```

## Hub #6204

installing a rule book always runs the operator gate, so a hub ward without a pool seat can no longer install one.

- **Mutant:** [`6204.sol`](6204.sol)
- **Caught by:** [`rcHuGovernanceInstallsTheFirstRuleBookIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L126)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6204`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuGovernanceInstallsTheFirstRuleBookIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -99,7 +99,7 @@
 
     /// @inheritdoc IHub
     function setPolicy(PoolId poolId, IHubPolicy policy_) external {
-        if (wards[msgSender()] != 1) _enforce(poolId);
+        _enforce(poolId); // MUTATION: a hub ward no longer bypasses the operator gate
 
         hubRegistry.setPolicy(poolId, policy_);
     }
```

## Hub #6205

installing a rule book is reserved to hub wards, so a sitting pool operator can no longer swap the book its pool runs under.

- **Mutant:** [`6205.sol`](6205.sol)
- **Caught by:** [`rcHuOperatorSwapsTheRuleBookIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L146)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6205`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuOperatorSwapsTheRuleBookIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -99,7 +99,7 @@
 
     /// @inheritdoc IHub
     function setPolicy(PoolId poolId, IHubPolicy policy_) external {
-        if (wards[msgSender()] != 1) _enforce(poolId);
+        require(wards[msgSender()] == 1, NotAuthorized()); // MUTATION: only a hub ward may install a rule book
 
         hubRegistry.setPolicy(poolId, policy_);
     }
```

## Hub #6206

the rule book setter refuses the null address, so a pool that installed a policy can never be left unrestricted.

- **Mutant:** [`6206.sol`](6206.sol)
- **Caught by:** [`rcHuRuleBookCanBeRemovedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L166)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6206`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuRuleBookCanBeRemovedIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -108,6 +108,7 @@
     /// @inheritdoc IHubRegistry
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
+        require(address(policy_) != address(0), PolicyNotInstalled()); // MUTATION: the null rule book is refused
 
         _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
 
```

## Hub #6207

a scheduled privileged call matures in the very block that scheduled it, the veto window the rule book asked for dropped from the maturity.

- **Mutant:** [`6207.sol`](6207.sol)
- **Caught by:** [`rcHuPrivilegedCallSchedulingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L183)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6207`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuPrivilegedCallSchedulingIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -148,7 +148,7 @@
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
         require(authorizedAfter[id] == 0, AlreadyAuthorized());
 
-        uint48 validAfter = uint48(block.timestamp) + delaySeconds;
+        uint48 validAfter = uint48(block.timestamp); // MUTATION: the maturity ignores the veto window
         authorizedAfter[id] = validAfter;
         emit AuthorizationScheduled(poolId_, caller, id, validAfter, data);
     }
```

## Hub #6208

withdrawing a scheduled call only succeeds when nothing is scheduled, so a standing authorization can never be taken back.

- **Mutant:** [`6208.sol`](6208.sol)
- **Caught by:** [`rcHuScheduledCallWithdrawalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L203)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6208`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuScheduledCallWithdrawalIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -157,7 +157,7 @@
     function cancelAuthorization(PoolId poolId_, address caller, bytes calldata data) external auth {
         bytes32 id = authId(poolId_, data);
         // Revert on a no-op cancel rather than writing a misleading audit entry.
-        require(authorizedAfter[id] != 0, Unauthorized());
+        require(authorizedAfter[id] == 0, Unauthorized()); // MUTATION: only an unscheduled call may be withdrawn
         delete authorizedAfter[id];
         emit AuthorizationCanceled(poolId_, caller, id);
     }
```

## Hub #6209

adding a share class demands a salt that was already spent, so no share class can be branded with a fresh one.

- **Mutant:** [`6209.sol`](6209.sol)
- **Caught by:** [`rcHuFirstShareClassIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L226)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6209`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuFirstShareClassIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -46,7 +46,7 @@
 
         PoolId prefixedPoolId = PoolId.wrap(uint64(bytes8(salt)));
         require(poolId == prefixedPoolId, InvalidSalt());
-        require(!salts[salt], AlreadyUsedSalt());
+        require(salts[salt], AlreadyUsedSalt()); // MUTATION: only an already spent salt is admitted
 
         scId_ = previewNextShareClassId(poolId);
 
```

## Hub #6210

every ledger row opens credit normal whatever the caller asked, so no debit normal asset or expense account can exist.

- **Mutant:** [`6210.sol`](6210.sol)
- **Caught by:** [`rcHuDebitNormalRowCanBeOpenedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L248) · [`rcHuAccountsThenHoldingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L282)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6210`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuDebitNormalRowCanBeOpenedIsReachable rcHuAccountsThenHoldingIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -71,7 +71,7 @@
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
-        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[poolId][account] = Account(0, 0, false, uint64(block.timestamp), ""); // MUTATION: every row opens credit normal
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Hub #6211

every ledger row opens debit normal whatever the caller asked, so no credit normal equity or liability account can exist.

- **Mutant:** [`6211.sol`](6211.sol)
- **Caught by:** [`rcHuCreditNormalRowCanBeOpenedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L265)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6211`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuCreditNormalRowCanBeOpenedIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -71,7 +71,7 @@
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
         require(accounts[poolId][account].lastUpdated == 0, AccountExists());
-        accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
+        accounts[poolId][account] = Account(0, 0, true, uint64(block.timestamp), ""); // MUTATION: every row opens debit normal
         emit CreateAccount(poolId, account, isDebitNormal);
     }
 
```

## Hub #6212

opening a holding books nothing, so the value the holding already carried never reaches the books as principal.

- **Mutant:** [`6212.sol`](6212.sol)
- **Caught by:** [`rcHuHoldingOpeningValueBookedAsPrincipalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L310)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6212`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuHoldingOpeningValueBookedAsPrincipalIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -345,7 +345,7 @@
         // If increase/decrease was called before initialize, the tracked amount carries no value yet:
         // establish it at the valuation and book it as principal.
         (, uint128 initialValue) = holdings.update(poolId, scId, assetId);
-        _updateAccountingAmount(poolId, scId, assetId, true, initialValue);
+        _updateAccountingAmount(poolId, scId, assetId, true, 0); // MUTATION: the opening value is never booked
     }
 
     /// @inheritdoc IHub
```

## Hub #6213

an amount posting of zero opens a journal instead of returning, so a movement of nothing still spends the pool an identity.

- **Mutant:** [`6213.sol`](6213.sol)
- **Caught by:** [`rcHuHoldingOpeningWithNothingToBookIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L339) · [`rcHuZeroAmountPostingIsAcceptedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L542)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6213`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuHoldingOpeningWithNothingToBookIsReachable rcHuZeroAmountPostingIsAcceptedIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -539,7 +539,7 @@
     function _updateAccountingAmount(PoolId poolId, ShareClassId scId, AssetId assetId, bool isPositive, uint128 diff)
         internal
     {
-        if (diff == 0) return;
+        // MUTATION: a zero amount posting no longer returns early
         if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.AmountCredit);
         else _journal(poolId, scId, assetId, diff, AccountKind.AmountCredit, AccountKind.AmountDebit);
     }
```

## Hub #6214

opening a holding rejects two neighbouring posting slots wired to one ledger row, a shape the opening call documents as legal.

- **Mutant:** [`6214.sol`](6214.sol)
- **Caught by:** [`rcHuHoldingWithARepeatedSlotIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L366) · [`rcHuSharedAmountSlotsKeepTheHoldingAccountFlatIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1083)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6214`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuHoldingWithARepeatedSlotIsReachable rcHuSharedAmountSlotsKeepTheHoldingAccountFlatIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -338,6 +338,8 @@
         require(hubRegistry.isRegistered(assetId), IHubRegistry.AssetNotFound());
         for (uint256 i; i < accounts.length; i++) {
             require(accounting.exists(poolId, accounts[i]), IAccounting.AccountDoesNotExist());
+            // MUTATION: neighbouring posting slots may no longer share one ledger row
+            require(i == 0 || accounts[i] != accounts[i - 1], IAccounting.AccountDoesNotExist());
         }
 
         holdings.initialize(poolId, scId, assetId, valuation, accounts);
```

## Hub #6215

a revaluation reports the difference but never stores the new value, so the holding keeps its old value.

- **Mutant:** [`6215.sol`](6215.sol)
- **Caught by:** [`rcHuHoldingMarkUpIsBookedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L386) · [`rcHuHoldingMarkDownToZeroIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L412)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6215`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuHoldingMarkUpIsBookedIsReachable rcHuHoldingMarkDownToZeroIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -201,7 +201,7 @@
         isPositive = currentAmountValue >= holding_.assetAmountValue;
         diffValue = isPositive ? currentAmountValue - holding_.assetAmountValue : holding_.assetAmountValue - currentAmountValue; // forgefmt: disable-line
 
-        holding_.assetAmountValue = currentAmountValue;
+        // MUTATION: the revalued amount is never written back
 
         emit Update(poolId, scId, assetId, isPositive, diffValue);
     }
```

## Hub #6216

A zero revaluation opens a journal instead of returning, so remarking a holding at its current value spends a journal id.

- **Mutant:** [`6216.sol`](6216.sol)
- **Caught by:** [`rcHuRevaluationLeavingTheBooksUntouchedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L440) · [`rcHuZeroValuePostingIsAcceptedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L638)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6216`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuRevaluationLeavingTheBooksUntouchedIsReachable rcHuZeroValuePostingIsAcceptedIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -558,7 +558,7 @@
     function _updateAccountingValue(PoolId poolId, ShareClassId scId, AssetId assetId, bool isPositive, uint128 diff)
         internal
     {
-        if (diff == 0) return;
+        // MUTATION: a zero revaluation no longer returns early
         if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.ValueIncrease);
         else _journal(poolId, scId, assetId, diff, AccountKind.ValueDecrease, AccountKind.AmountDebit);
     }
```

## Hub #6217

a deposit posts as a withdrawal and a withdrawal as a deposit, so each amount movement lands on the books the wrong way about.

- **Mutant:** [`6217.sol`](6217.sol)
- **Caught by:** [`rcHuDepositPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L465) · [`rcHuWithdrawalPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L491)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6217`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuDepositPostingIsReachable rcHuWithdrawalPostingIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -540,7 +540,7 @@
         internal
     {
         if (diff == 0) return;
-        if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.AmountCredit);
+        if (!isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.AmountCredit); // MUTATION: the deposit and withdrawal legs are swapped
         else _journal(poolId, scId, assetId, diff, AccountKind.AmountCredit, AccountKind.AmountDebit);
     }
 
```

## Hub #6218

every unlock mints a fresh journal identity, so two postings made in one transaction for one pool are filed apart instead of together.

- **Mutant:** [`6218.sol`](6218.sol)
- **Caught by:** [`rcHuAmountRoundTripIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L517)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6218`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuAmountRoundTripIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -48,9 +48,8 @@
         credited = 0;
         _currentPoolId = poolId;
 
-        if (TransientJournal.journalId(poolId) == 0) {
-            TransientJournal.setJournalId(poolId, _generateJournalId(poolId));
-        }
+        // MUTATION: every unlock mints a fresh journal identity
+        TransientJournal.setJournalId(poolId, _generateJournalId(poolId));
         emit StartJournalId(poolId, TransientJournal.journalId(poolId));
     }
 
```

## Hub #6219

holding postings narrow the amount to sixty four bits on both legs, so larger amounts are booked truncated.

- **Mutant:** [`6219.sol`](6219.sol)
- **Caught by:** [`rcHuLargestAmountPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L565)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6219`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuLargestAmountPostingIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -573,8 +573,9 @@
         AccountKind creditKind
     ) private {
         accounting.unlock(poolId);
-        accounting.addDebit(holdings.accountId(poolId, scId, assetId, uint8(debitKind)), diff);
-        accounting.addCredit(holdings.accountId(poolId, scId, assetId, uint8(creditKind)), diff);
+        // MUTATION: the posted amount is narrowed to sixty four bits on both legs
+        accounting.addDebit(holdings.accountId(poolId, scId, assetId, uint8(debitKind)), uint64(diff));
+        accounting.addCredit(holdings.accountId(poolId, scId, assetId, uint8(creditKind)), uint64(diff));
         accounting.lock();
     }
 
```

## Hub #6220

a revaluation gain posts as a loss and a loss as a gain, so each value movement lands on the books the wrong way about.

- **Mutant:** [`6220.sol`](6220.sol)
- **Caught by:** [`rcHuValueGainPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L586) · [`rcHuValueLossPostingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L612)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6220`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuValueGainPostingIsReachable rcHuValueLossPostingIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -559,7 +559,7 @@
         internal
     {
         if (diff == 0) return;
-        if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.ValueIncrease);
+        if (!isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.ValueIncrease); // MUTATION: the gain and loss legs are swapped
         else _journal(poolId, scId, assetId, diff, AccountKind.ValueDecrease, AccountKind.AmountDebit);
     }
 
```

## Hub #6221

a manager authored batch never closes the session it opened, so the ledger is handed back unlocked once the entry returns.

- **Mutant:** [`6221.sol`](6221.sol)
- **Caught by:** [`rcHuMinimalBalancedJournalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L661) · [`rcHuWiderBalancedJournalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L685)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6221`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuMinimalBalancedJournalIsReachable rcHuWiderBalancedJournalIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -384,7 +384,7 @@
     {
         accounting.unlock(poolId);
         accounting.addJournal(debits, credits);
-        accounting.lock();
+        // MUTATION: the batch entry never closes the session it opened
     }
 
     //----------------------------------------------------------------------------------------------
```

## Hub #6222

an empty batch now returns at once, so it no longer opens a journal or uses up a journal number.

- **Mutant:** [`6222.sol`](6222.sol)
- **Caught by:** [`rcHuEmptyJournalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L709)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6222`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuEmptyJournalIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -382,6 +382,7 @@
         payable
         enforced(poolId)
     {
+        if (debits.length == 0 && credits.length == 0) return; // MUTATION: an empty batch returns at once
         accounting.unlock(poolId);
         accounting.addJournal(debits, credits);
         accounting.lock();
```

## Hub #6223

the ledger refuses a debit entry that carries no value, so a pair of zero valued entries cannot be posted at all.

- **Mutant:** [`6223.sol`](6223.sol)
- **Caught by:** [`rcHuZeroValuedJournalPairIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L732)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6223`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuZeroValuedJournalPairIsReachable`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -91,7 +91,7 @@
         require(!_currentPoolId.isNull(), AccountingLocked());
 
         Account storage acc = accounts[_currentPoolId][account];
-        require(acc.lastUpdated != 0, AccountDoesNotExist());
+        require(acc.lastUpdated != 0 && value != 0, AccountDoesNotExist()); // MUTATION: a zero valued debit is refused
 
         acc.totalDebit += value;
         debited += value;
```

## Hub #6224

installing the null snapshot hook is silently ignored, so once NAV automation is switched on for a pool it can never be switched off.

- **Mutant:** [`6224.sol`](6224.sol)
- **Caught by:** [`rcHuSnapshotHookRoundTripIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L757)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6224`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuSnapshotHookRoundTripIsReachable`

```diff
--- a/src/core/hub/Holdings.sol
+++ b/src/core/hub/Holdings.sol
@@ -91,7 +91,7 @@
     function setSnapshotHook(PoolId poolId, ISnapshotHook hook) external auth {
         require(hubRegistry.exists(poolId), NonExistingPool());
 
-        snapshotHook[poolId] = hook;
+        if (address(hook) != address(0)) snapshotHook[poolId] = hook; // MUTATION: clearing the hook is ignored
 
         emit SetSnapshotHook(poolId, hook);
     }
```

## Hub #6225

announcing a share class puts two identical messages on the wire, so one call costs the pool a duplicate announcement.

- **Mutant:** [`6225.sol`](6225.sol)
- **Caught by:** [`rcHuShareClassAnnouncementIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L777)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6225`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuShareClassAnnouncementIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -416,6 +416,10 @@
         sender.sendNotifyShareClass{value: msgValue()}(
             centrifugeId, poolId, scId, metadata, salt, registrar, payload, extraGasLimit, refund
         );
+        // MUTATION: the announcement goes out a second time
+        sender.sendNotifyShareClass{value: msgValue()}(
+            centrifugeId, poolId, scId, metadata, salt, registrar, payload, extraGasLimit, refund
+        );
     }
 
     /// @dev Reads a share class's creation metadata into a struct, keeping the name/symbol locals out of the
```

## Hub #6226

the request callback flips the payment mode on its way out, so a paid callback travels as unpaid and an unpaid one as paid.

- **Mutant:** [`6226.sol`](6226.sol)
- **Caught by:** [`rcHuPaidRequestCallbackIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L798) · [`rcHuUnpaidRequestCallbackIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L817)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6226`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuPaidRequestCallbackIsReachable rcHuUnpaidRequestCallbackIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -518,7 +518,8 @@
         require(address(manager) != address(0), InvalidRequestManager());
         require(msg.sender == address(manager), NotAuthorized());
 
-        sender.sendRequestCallback{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, unpaidMode, refund);
+        // MUTATION: the payment mode is inverted on the way out
+        sender.sendRequestCallback{value: msgValue()}(poolId, scId, assetId, payload, extraGasLimit, !unpaidMode, refund);
     }
 
     //----------------------------------------------------------------------------------------------
```

## Hub #6227

withdrawing authority leaves the ward roll untouched, so a grant of the ward can never be taken back.

- **Mutant:** [`6227.sol`](6227.sol)
- **Caught by:** [`rcHuWardAuthorityRoundTripIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L837) · [`rcHuWardCanStandItselfDownIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L856)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6227`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuWardAuthorityRoundTripIsReachable rcHuWardCanStandItselfDownIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        // MUTATION: the authority is never withdrawn
         emit Deny(user);
     }
 }
```

## Hub #6228

an unopened holding is priced at half par instead of par, so the default price is wrong.

- **Mutant:** [`6228.sol`](6228.sol)
- **Caught by:** [`rcHuUnopenedHoldingPricesAtParIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L870) · [`rcHuAssetPriceNoticeForAnUnknownAssetAndClassIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1124)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6228`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuUnopenedHoldingPricesAtParIsReachable rcHuAssetPriceNoticeForAnUnknownAssetAndClassIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -585,7 +585,7 @@
     /// @inheritdoc IHub
     function pricePoolPerAsset(PoolId poolId, ShareClassId scId, AssetId assetId) public view returns (D18) {
         // Assume price of 1.0 if the holding is not initialized yet
-        if (!holdings.isInitialized(poolId, scId, assetId)) return d18(1, 1);
+        if (!holdings.isInitialized(poolId, scId, assetId)) return d18(1, 2); // MUTATION: the default answer is half par
 
         IValuation valuation = holdings.valuation(poolId, scId, assetId);
         return valuation.getPrice(poolId, scId, assetId);
```

## Hub #6229

setPolicy stores a rule book one address away from the one it was handed, so reading a pool's policy back never returns what was installed.

- **Mutant:** [`6229.sol`](6229.sol)
- **Caught by:** [`rcHuPassingPolicyReadIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L882)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 6229`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuPassingPolicyReadIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(IHubPolicy(address(uint160(address(policy_)) + 1)), _policy[poolId_].nonce + 1); // MUTATION: the rule book stored is never the one installed
 
         emit SetPolicy(poolId_, policy_);
     }
```

## Hub #8060

a new manager entry books share issuance and revocation directly, so share counts move without any spoke report.

- **Mutant:** [`8060.sol`](8060.sol)
- **Caught by:** [`stHuShareLedgerIsNeverMovedByTheHub`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L242)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8060`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule stHuShareLedgerIsNeverMovedByTheHub`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -311,6 +311,15 @@
         updateSharePrice(poolId, scId, pricePoolPerShare, uint64(block.timestamp));
     }
 
+    /// @notice MUTATION: books issuance and revocation straight into the share class ledger.
+    function updateShares(PoolId poolId, ShareClassId scId, uint16 centrifugeId, uint128 amount, bool isIssuance)
+        external
+        payable
+        enforced(poolId)
+    {
+        shareClassManager.updateShares(centrifugeId, poolId, scId, amount, isIssuance);
+    }
+
     /// @inheritdoc IHub
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external payable enforced(poolId) {
         accounting.createAccount(poolId, account, isDebitNormal);
```

## Hub #8061

a new manager entry decreases a holding directly, so a manager can push its share class and network into deficit.

- **Mutant:** [`8061.sol`](8061.sol)
- **Caught by:** [`stHuDeficitGateIsNeverMovedByTheHub`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L262)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8061`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule stHuDeficitGateIsNeverMovedByTheHub`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -356,6 +356,17 @@
         holdings.callOnSyncSnapshot(poolId, scId, assetId.centrifugeId());
     }
 
+    /// @notice MUTATION: writes a holding down through the flow ledger the deficit gate counts.
+    function writeOffHolding(
+        PoolId poolId,
+        ShareClassId scId,
+        AssetId assetId,
+        uint16 centrifugeId,
+        uint128 amount
+    ) external payable enforced(poolId) {
+        holdings.decrease(poolId, scId, assetId, centrifugeId, amount);
+    }
+
     /// @inheritdoc IHub
     function updateHoldingValuation(PoolId poolId, ShareClassId scId, AssetId assetId, IValuation valuation)
         external
```

## Hub #8062

the share class announcement swaps the salt and the registrar, so the spoke gets a salt the class was never created with.

- **Mutant:** [`8062.sol`](8062.sol)
- **Caught by:** [`hlHuShareClassAnnouncementCarriesTheClassSalt`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8062`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuShareClassAnnouncementCarriesTheClassSalt`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -414,7 +414,7 @@
 
         emit NotifyShareClass(centrifugeId, poolId, scId, payload);
         sender.sendNotifyShareClass{value: msgValue()}(
-            centrifugeId, poolId, scId, metadata, salt, registrar, payload, extraGasLimit, refund
+            centrifugeId, poolId, scId, metadata, registrar, salt, payload, extraGasLimit, refund // MUTATION: the announcement carries the registrar word where the class salt belongs
         );
     }
 
```

## Hub #8108

the pool's policy is shown the call headed by the block time, so it misreads which call it gates and a scheduled authorization never matches a later retry.

- **Mutant:** [`8108.sol`](8108.sol)
- **Caught by:** [`hlHuSharePriceUpdateStampedNowAsksThePolicyAboutACallFreeOfTheClock`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L296)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8108`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuSharePriceUpdateStampedNowAsksThePolicyAboutACallFreeOfTheClock`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -599,7 +599,7 @@
         _requireManager(poolId);
 
         IHubPolicy policy_ = hubRegistry.policy(poolId);
-        if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), msg.data);
+        if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), abi.encodePacked(block.timestamp, msg.data)); // MUTATION: the policy payload leads with the clock
     }
 
     /// @dev Reverts unless the resolved sender is a registered manager for `poolId`.
```

## Hub #8300

reinstalling a pool's current policy is skipped, so its nonce stays put and earlier authorizations stay spendable.

- **Mutant:** [`8300.sol`](8300.sol)
- **Caught by:** [`hlHuRuleBookInstallAlwaysOpensANewTenure`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L283)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8300`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuRuleBookInstallAlwaysOpensANewTenure`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -101,7 +101,7 @@
     function setPolicy(PoolId poolId, IHubPolicy policy_) external {
         if (wards[msgSender()] != 1) _enforce(poolId);
 
-        hubRegistry.setPolicy(poolId, policy_);
+        if (address(policy_) != address(hubRegistry.policy(poolId))) hubRegistry.setPolicy(poolId, policy_); // MUTATION: re-installing the sitting rule book is skipped
     }
 
     /// @inheritdoc IHub
```

## Hub #8301

filing the outbound sender also repoints the gateway, so one configuration call rewires two of the hub's dependencies.

- **Mutant:** [`8301.sol`](8301.sol)
- **Caught by:** [`hlHuFileWiresOnlyTheNamedSlot`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L57)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8301`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuFileWiresOnlyTheNamedSlot`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -85,7 +85,7 @@
     function file(bytes32 what, address data) external auth {
         if (what == "gateway") gateway = IGateway(data);
         else if (what == "feeAccrual") feeAccrual = IFeeAccrual(data);
-        else if (what == "sender") sender = IHubMessageSender(data);
+        else if (what == "sender") { sender = IHubMessageSender(data); gateway = IGateway(data); } // MUTATION: filing the sender also rewires the gateway
         else if (what == "multiAdapter") multiAdapter = IMultiAdapter(data);
         else revert FileUnrecognizedParam();
         emit File(what, data);
```

## Hub #8302

a share class announcement sends a zero registrar instead of the one its caller named, so the spoke never learns it.

- **Mutant:** [`8302.sol`](8302.sol)
- **Caught by:** [`hlHuShareClassAnnouncementCarriesTheCallersRegistrar`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L76)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8302`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuShareClassAnnouncementCarriesTheCallersRegistrar`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -414,7 +414,7 @@
 
         emit NotifyShareClass(centrifugeId, poolId, scId, payload);
         sender.sendNotifyShareClass{value: msgValue()}(
-            centrifugeId, poolId, scId, metadata, salt, registrar, payload, extraGasLimit, refund
+            centrifugeId, poolId, scId, metadata, salt, bytes32(0), payload, extraGasLimit, refund // MUTATION: the registrar the caller named is dropped
         );
     }
 
```

## Hub #8303

a revaluation checks the pool's home network for sync instead of the asset's, so the snapshot hook fires for the wrong network.

- **Mutant:** [`8303.sol`](8303.sol)
- **Caught by:** [`hlHuRevaluationNotifiesTheHookExactlyWhenTheAssetsNetworkIsInSync`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L92)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8303`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuRevaluationNotifiesTheHookExactlyWhenTheAssetsNetworkIsInSync`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -353,7 +353,7 @@
         (bool isPositive, uint128 diff) = holdings.update(poolId, scId, assetId);
         _updateAccountingValue(poolId, scId, assetId, isPositive, diff);
 
-        holdings.callOnSyncSnapshot(poolId, scId, assetId.centrifugeId());
+        holdings.callOnSyncSnapshot(poolId, scId, poolId.centrifugeId()); // MUTATION: the hub's own network in place of the asset's
     }
 
     /// @inheritdoc IHub
```

## Hub #8304

switching a holding's price source also notifies the snapshot hook, so the hook publishes a pool price on a call that revalued nothing.

- **Mutant:** [`8304.sol`](8304.sol)
- **Caught by:** [`vtHuSnapshotHookHearsOnlyARevaluation`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L103)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8304`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule vtHuSnapshotHookHearsOnlyARevaluation`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -362,7 +362,7 @@
         payable
         enforced(poolId)
     {
-        holdings.updateValuation(poolId, scId, assetId, valuation);
+        holdings.updateValuation(poolId, scId, assetId, valuation); holdings.callOnSyncSnapshot(poolId, scId, assetId.centrifugeId()); // MUTATION: a price source swap also notifies the hook
     }
 
     /// @inheritdoc IHub
```

## Hub #8430

a revocation of a spoke call authorization is checked for the manager only and never asks the pool's policy, so a policy cannot see or refuse it.

- **Mutant:** [`8430.sol`](8430.sol)
- **Caught by:** [`rcHuRevocationPassesAConsentingPolicyIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1031)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8430`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuRevocationPassesAConsentingPolicyIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -239,7 +239,7 @@
     function unauthorizeSpokeCall(PoolId poolId, uint16 centrifugeId, bytes calldata data, address refund)
         external
         payable
-        enforced(poolId)
+        onlyManager(poolId) // MUTATION: the revocation skips the pool's policy
     {
         emit UnauthorizeSpokeCall(centrifugeId, poolId, data);
         sender.sendUnauthorizeSpokeCall{value: msgValue()}(centrifugeId, poolId, data, refund);
```

## Hub #8431

a revocation of a spoke call authorization is checked for the manager only, so a refusing policy no longer blocks it.

- **Mutant:** [`8431.sol`](8431.sol)
- **Caught by:** [`rvHuEnforcedEntryPassesTheInstalledPolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L319) · [`rvHuSpokeCallRevokePassesThePolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L344)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8431`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuEnforcedEntryPassesTheInstalledPolicy rvHuSpokeCallRevokePassesThePolicy`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -239,7 +239,7 @@
     function unauthorizeSpokeCall(PoolId poolId, uint16 centrifugeId, bytes calldata data, address refund)
         external
         payable
-        enforced(poolId)
+        onlyManager(poolId) // MUTATION: the revocation skips the pool's policy
     {
         emit UnauthorizeSpokeCall(centrifugeId, poolId, data);
         sender.sendUnauthorizeSpokeCall{value: msgValue()}(centrifugeId, poolId, data, refund);
```

## Hub #8812

revoking a spoke call sends an authorization instead, so the spoke is granted the call the manager meant to revoke.

- **Mutant:** [`8812.sol`](8812.sol)
- **Caught by:** [`rvHuSpokeCallRevokePassesThePolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L344)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8812`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuSpokeCallRevokePassesThePolicy`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -242,7 +242,7 @@
         enforced(poolId)
     {
         emit UnauthorizeSpokeCall(centrifugeId, poolId, data);
-        sender.sendUnauthorizeSpokeCall{value: msgValue()}(centrifugeId, poolId, data, refund);
+        sender.sendAuthorizeSpokeCall{value: msgValue()}(centrifugeId, poolId, data, refund); // MUTATION: the revocation is sent as an authorization
     }
 
     //----------------------------------------------------------------------------------------------
```

## Hub #8815

a share price update stamped now records a time one second before it ran, so the price looks older than it is.

- **Mutant:** [`8815.sol`](8815.sol)
- **Caught by:** [`hlHuSharePriceUpdateStampedNowRecordsTheExecutionTime`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L315)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8815`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuSharePriceUpdateStampedNowRecordsTheExecutionTime`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -308,7 +308,7 @@
 
     /// @inheritdoc IHub
     function updateSharePrice(PoolId poolId, ShareClassId scId, D18 pricePoolPerShare) external payable {
-        updateSharePrice(poolId, scId, pricePoolPerShare, uint64(block.timestamp));
+        updateSharePrice(poolId, scId, pricePoolPerShare, uint64(block.timestamp) - 1); // MUTATION: the stamp lags the execution time
     }
 
     /// @inheritdoc IHub
```

## Hub #8816

a pool notice forwards the raw call value, so a batched notice spends ETH the batch already paid to the gateway.

- **Mutant:** [`8816.sol`](8816.sol)
- **Caught by:** [`vtHuEveryOutboundSendCarriesTheAttachedValue`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L277)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8816`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule vtHuEveryOutboundSendCarriesTheAttachedValue`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -394,7 +394,7 @@
     /// @inheritdoc IHub
     function notifyPool(PoolId poolId, uint16 centrifugeId, address refund) external payable enforced(poolId) {
         emit NotifyPool(centrifugeId, poolId);
-        sender.sendNotifyPool{value: msgValue()}(centrifugeId, poolId, refund);
+        sender.sendNotifyPool{value: msg.value}(centrifugeId, poolId, refund); // MUTATION: the batch value is forwarded again
     }
 
     /// @inheritdoc IHub
```

## Hub #8817

repointing the multi adapter rewires the fee accrual contract instead, so the hub can never move onto another multi adapter.

- **Mutant:** [`8817.sol`](8817.sol)
- **Caught by:** [`rcHuFileRepointsTheMultiAdapterIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1049)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8817`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuFileRepointsTheMultiAdapterIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -86,7 +86,7 @@
         if (what == "gateway") gateway = IGateway(data);
         else if (what == "feeAccrual") feeAccrual = IFeeAccrual(data);
         else if (what == "sender") sender = IHubMessageSender(data);
-        else if (what == "multiAdapter") multiAdapter = IMultiAdapter(data);
+        else if (what == "multiAdapter") feeAccrual = IFeeAccrual(data); // MUTATION: the multi adapter key rewires the fee hook
         else revert FileUnrecognizedParam();
         emit File(what, data);
     }
```

## Hub #8818

the multi adapter key is no longer recognized, so a ward's attempt to repoint the multi adapter reverts.

- **Mutant:** [`8818.sol`](8818.sol)
- **Caught by:** [`rvHuFileSucceedsForAWardNamingADependency`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L370)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8818`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuFileSucceedsForAWardNamingADependency`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -86,7 +86,7 @@
         if (what == "gateway") gateway = IGateway(data);
         else if (what == "feeAccrual") feeAccrual = IFeeAccrual(data);
         else if (what == "sender") sender = IHubMessageSender(data);
-        else if (what == "multiAdapter") multiAdapter = IMultiAdapter(data);
+        else if (what == "multiAdapterV2") multiAdapter = IMultiAdapter(data); // MUTATION: the multi adapter key is not filed
         else revert FileUnrecognizedParam();
         emit File(what, data);
     }
```

## Hub #8819

a manager who is no ward may only replace an installed policy, so a fresh pool's first policy needs a ward.

- **Mutant:** [`8819.sol`](8819.sol)
- **Caught by:** [`rcHuFreshPoolManagerInstallsTheFirstRuleBookUnpolicedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1062)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8819`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuFreshPoolManagerInstallsTheFirstRuleBookUnpolicedIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -99,7 +99,7 @@
 
     /// @inheritdoc IHub
     function setPolicy(PoolId poolId, IHubPolicy policy_) external {
-        if (wards[msgSender()] != 1) _enforce(poolId);
+        if (wards[msgSender()] != 1) { _enforce(poolId); require(address(hubRegistry.policy(poolId)) != address(0), IHub.NotManager()); } // MUTATION: a manager cannot install the first policy
 
         hubRegistry.setPolicy(poolId, policy_);
     }
```

## Hub #8820

opening a holding rejects one account as both amount debit and amount credit, so a holding can no longer book both on one account.

- **Mutant:** [`8820.sol`](8820.sol)
- **Caught by:** [`rcHuSharedAmountSlotsKeepTheHoldingAccountFlatIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1083) · [`rcHuHoldingWithARepeatedSlotIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L366)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8820`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuSharedAmountSlotsKeepTheHoldingAccountFlatIsReachable rcHuHoldingWithARepeatedSlotIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -340,6 +340,7 @@
             require(accounting.exists(poolId, accounts[i]), IAccounting.AccountDoesNotExist());
         }
 
+        require(accounts[0] != accounts[1], IAccounting.AccountDoesNotExist()); // MUTATION: the amount slots must differ
         holdings.initialize(poolId, scId, assetId, valuation, accounts);
 
         // If increase/decrease was called before initialize, the tracked amount carries no value yet:
```

## Hub #8821

setHoldingAccountId refuses the account in the counterpart amount slot, so a holding's own account can never be moved onto it.

- **Mutant:** [`8821.sol`](8821.sol)
- **Caught by:** [`rcHuHoldingAccountRepointedOntoItsCounterpartIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1105)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8821`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuHoldingAccountRepointedOntoItsCounterpartIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -373,6 +373,7 @@
     {
         require(accounting.exists(poolId, accountId), IAccounting.AccountDoesNotExist());
 
+        require(holdings.accountId(poolId, scId, assetId, kind ^ 1) != accountId, IAccounting.AccountDoesNotExist()); // MUTATION: the counterpart slot's account is refused
         holdings.setAccountId(poolId, scId, assetId, kind, accountId);
     }
 
```

## Hub #8822

updateRestriction no longer checks the share class exists, so a restriction update goes out for a class never created.

- **Mutant:** [`8822.sol`](8822.sol)
- **Caught by:** [`rvHuShareClassMessagesRefuseAnUncreatedClass`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L386)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8822`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuShareClassMessagesRefuseAnUncreatedClass`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -267,7 +267,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable enforced(poolId) {
-        _requireSC(poolId, scId);
+        // MUTATION: the share class existence check is dropped
 
         emit UpdateRestriction(centrifugeId, poolId, scId, payload);
         sender.sendUpdateRestriction{value: msgValue()}(centrifugeId, poolId, scId, payload, extraGasLimit, refund);
```

## Hub #8823

notifyAssetPrice checks the share class exists, so no price notice goes out for a class never created.

- **Mutant:** [`8823.sol`](8823.sol)
- **Caught by:** [`rcHuAssetPriceNoticeForAnUnknownAssetAndClassIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1124)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8823`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuAssetPriceNoticeForAnUnknownAssetAndClassIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -467,6 +467,7 @@
         payable
         enforced(poolId)
     {
+        _requireSC(poolId, scId); // MUTATION: the share class must exist
         D18 pricePoolPerAsset_ = pricePoolPerAsset(poolId, scId, assetId);
         emit NotifyAssetPrice(assetId.centrifugeId(), poolId, scId, assetId, pricePoolPerAsset_);
         sender.sendNotifyPricePoolPerAsset{value: msgValue()}(poolId, scId, assetId, pricePoolPerAsset_, refund);
```

## Hub #8824

notifySharePrice checks the share class exists, so no share price notice goes out for a class never created.

- **Mutant:** [`8824.sol`](8824.sol)
- **Caught by:** [`rcHuSharePriceNoticeForAnUncreatedClassIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1142)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8824`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuSharePriceNoticeForAnUncreatedClassIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -453,6 +453,7 @@
         payable
         enforced(poolId)
     {
+        _requireSC(poolId, scId); // MUTATION: the share class must exist
         (D18 pricePoolPerShare, uint64 computedAt) = shareClassManager.pricePoolPerShare(poolId, scId);
 
         emit NotifySharePrice(centrifugeId, poolId, scId, pricePoolPerShare, computedAt);
```

## Hub #8825

notifyShareClass checks only the manager seat, so an installed policy is never asked about a share class notice.

- **Mutant:** [`8825.sol`](8825.sol)
- **Caught by:** [`rcHuShareClassNoticeConsultsTheInstalledPolicyIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1159)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8825`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuShareClassNoticeConsultsTheInstalledPolicyIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -407,7 +407,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable {
-        _enforce(poolId);
+        _requireManager(poolId); // MUTATION: the policy is skipped
         _requireSC(poolId, scId);
 
         (ShareClassMetadata memory metadata, bytes32 salt) = _shareClassMetadata(poolId, scId);
```

## Hub #8826

installing a policy always runs the manager and policy checks, so a ward who is no manager, or faces a refusing policy, is refused.

- **Mutant:** [`8826.sol`](8826.sol)
- **Caught by:** [`rvHuWardPolicyInstallOutlivesARefusingRuleBook`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L407)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8826`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuWardPolicyInstallOutlivesARefusingRuleBook`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -99,7 +99,7 @@
 
     /// @inheritdoc IHub
     function setPolicy(PoolId poolId, IHubPolicy policy_) external {
-        if (wards[msgSender()] != 1) _enforce(poolId);
+        _enforce(poolId); // MUTATION: a ward no longer bypasses the gate
 
         hubRegistry.setPolicy(poolId, policy_);
     }
```

## Hub #8827

cancelAuthorization refuses to cancel a pending manager change, so a manager cannot veto its own removal.

- **Mutant:** [`8827.sol`](8827.sol)
- **Caught by:** [`rvHuCancelAuthorizationIsNeverRefusedToAnAdmittedManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L426)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8827`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuCancelAuthorizationIsNeverRefusedToAnAdmittedManager`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -120,6 +120,7 @@
 
     /// @inheritdoc IHub
     function cancelAuthorization(PoolId poolId, bytes calldata data) external enforced(poolId) {
+        require(data.length < 4 || bytes4(data[:4]) != IHub.updateHubManager.selector, IHub.NotManager()); // MUTATION: a pending manager change cannot be canceled
         hubRegistry.cancelAuthorization(poolId, msgSender(), data);
     }
 
```

## Hub #8828

a manager call checks its declared value against the raw call value, so a batched local call declaring the batch's ETH passes.

- **Mutant:** [`8828.sol`](8828.sol)
- **Caught by:** [`rvHuManagerCallRefusesAMisdeclaredValue`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L173)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 8828`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuManagerCallRefusesAMisdeclaredValue`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -490,7 +490,7 @@
     ) external payable enforced(poolId) {
         // Gas is explicit: a local call is funded entirely by `msg.value`, a remote call carries none.
         require(
-            centrifugeId == sender.localCentrifugeId() ? localValue == msgValue() : localValue == 0,
+            centrifugeId == sender.localCentrifugeId() ? localValue == msg.value : localValue == 0, // MUTATION: the batch value counts as declared
             ManagerCallUnexpectedValue()
         );
 
```

## Hub #9007

writing a pool's metadata also unplugs the hub's fee accrual, so every pool stops accruing fees after one metadata change.

- **Mutant:** [`9007.sol`](9007.sol)
- **Caught by:** [`hlHuMetadataWritersAndRescueWriteNoHubField`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L20)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9007`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/metadata_properties.conf --rule hlHuMetadataWritersAndRescueWriteNoHubField`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -162,7 +162,7 @@
 
     /// @inheritdoc IHub
     function setPoolMetadata(PoolId poolId, bytes calldata metadata) external payable enforced(poolId) {
-        hubRegistry.setMetadata(poolId, metadata);
+        hubRegistry.setMetadata(poolId, metadata); feeAccrual = IFeeAccrual(address(0)); // MUTATION: the metadata write also unplugs the fee accrual
     }
 
     /// @inheritdoc IHub
```

## Hub #9033

A holding markdown no longer posts to the ledger, so a value loss leaves the pool's books unchanged.

- **Mutant:** [`9033.sol`](9033.sol)
- **Caught by:** [`stHuValueMoveIsBookedExactly`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L154)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9033`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule stHuValueMoveIsBookedExactly`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -560,7 +560,7 @@
     {
         if (diff == 0) return;
         if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.ValueIncrease);
-        else _journal(poolId, scId, assetId, diff, AccountKind.ValueDecrease, AccountKind.AmountDebit);
+        // MUTATION: the value-decrease posting leg of _updateAccountingValue removed
     }
 
     /// @dev Unlock, post the debit/credit pair against the given account slots, then lock.
```

## Hub #9034

Registering a pool no longer records its currency, so the pool gains a manager seat without a currency.

- **Mutant:** [`9034.sol`](9034.sol)
- **Caught by:** [`stHrOperatorSeatNeedsItsOwnPoolsCurrency`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L88)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9034`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/multi_pool_properties.conf --rule stHrOperatorSeatNeedsItsOwnPoolsCurrency`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -65,7 +65,7 @@
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
         manager[poolId_][manager_] = true;
-        currency[poolId_] = currency_;
+        // MUTATION: registerPool no longer records the new pool's currency
 
         emit NewPool(poolId_, manager_, currency_);
     }
```

## Hub #9035

Opening a ledger account no longer checks that it exists, so reopening a live row wipes its debit and credit totals.

- **Mutant:** [`9035.sol`](9035.sol)
- **Caught by:** [`stHuLedgerTotalsMoveOnlyThroughJournalling`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L224)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9035`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule stHuLedgerTotalsMoveOnlyThroughJournalling`

```diff
--- a/src/core/hub/Accounting.sol
+++ b/src/core/hub/Accounting.sol
@@ -70,7 +70,7 @@
     /// @inheritdoc IAccounting
     function createAccount(PoolId poolId, AccountId account, bool isDebitNormal) external auth {
         require(!account.isNull(), InvalidAccountId());
-        require(accounts[poolId][account].lastUpdated == 0, AccountExists());
+        // MUTATION: the AccountExists check on createAccount removed
         accounts[poolId][account] = Account(0, 0, isDebitNormal, uint64(block.timestamp), "");
         emit CreateAccount(poolId, account, isDebitNormal);
     }
```

## Hub #9036

The credit leg of a holding's posting is booked as a debit, so every nonzero posting reverts unbalanced.

- **Mutant:** [`9036.sol`](9036.sol)
- **Caught by:** [`rvHuJournalPrimitiveIsNeverRefusedUnbalanced`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L278)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9036`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuJournalPrimitiveIsNeverRefusedUnbalanced`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -574,7 +574,7 @@
     ) private {
         accounting.unlock(poolId);
         accounting.addDebit(holdings.accountId(poolId, scId, assetId, uint8(debitKind)), diff);
-        accounting.addCredit(holdings.accountId(poolId, scId, assetId, uint8(creditKind)), diff);
+        accounting.addDebit(holdings.accountId(poolId, scId, assetId, uint8(creditKind)), diff); // MUTATION: copy-paste slip, the credit leg calls addDebit
         accounting.lock();
     }
 
```

## Hub #9140

announcing a pool to a spoke skips the manager and policy checks, so any caller can announce the pool.

- **Mutant:** [`9140.sol`](9140.sol)
- **Caught by:** [`rvHuManagerFacingEntryRefusesANonManager`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L243)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9140`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuManagerFacingEntryRefusesANonManager`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -392,7 +392,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IHub
-    function notifyPool(PoolId poolId, uint16 centrifugeId, address refund) external payable enforced(poolId) {
+    function notifyPool(PoolId poolId, uint16 centrifugeId, address refund) external payable { // MUTATION: announcing a pool no longer asks for a manager seat
         emit NotifyPool(centrifugeId, poolId);
         sender.sendNotifyPool{value: msgValue()}(centrifugeId, poolId, refund);
     }
```

## Hub #9141

posting a holding amount needs a pool manager instead of a hub admin, so a manager can book amounts no spoke reported.

- **Mutant:** [`9141.sol`](9141.sol)
- **Caught by:** [`rvHuJournalPrimitivesRefuseANonWard`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L260)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9141`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuJournalPrimitivesRefuseANonWard`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -531,7 +531,7 @@
     function updateAccountingAmount(PoolId poolId, ShareClassId scId, AssetId assetId, bool isPositive, uint128 diff)
         external
         payable
-        auth
+        onlyManager(poolId) // MUTATION: a pool manager posts amount entries in place of a hub ward
     {
         _updateAccountingAmount(poolId, scId, assetId, isPositive, diff);
     }
```

## Hub #9142

a holding's posting pair never closes the ledger session it opened, so the hub leaves the ledger unlocked and unchecked for balance.

- **Mutant:** [`9142.sol`](9142.sol)
- **Caught by:** [`stHuEveryHubCallLeavesTheLedgerLocked`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L190)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9142`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule stHuEveryHubCallLeavesTheLedgerLocked`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -575,7 +575,7 @@
         accounting.unlock(poolId);
         accounting.addDebit(holdings.accountId(poolId, scId, assetId, uint8(debitKind)), diff);
         accounting.addCredit(holdings.accountId(poolId, scId, assetId, uint8(creditKind)), diff);
-        accounting.lock();
+        // MUTATION: a posting pair never closes the session it opened
     }
 
     //----------------------------------------------------------------------------------------------
```

## Hub #9144

adapter changes are no longer refused during a batch, so the announcement can travel over a set the destination lacks.

- **Mutant:** [`9144.sol`](9144.sol)
- **Caught by:** [`rvHuSetAdaptersRefusesWhileBatching`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L305)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9144`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuSetAdaptersRefusesWhileBatching`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -138,7 +138,7 @@
     ) external payable enforced(poolId) {
         // Batching would defer the send until after the new set is applied, routing over a set the
         // destination lacks, so it is disallowed here.
-        require(!gateway.isBatching(), CannotSetAdaptersWhileBatching());
+        // MUTATION: reconfiguring the adapters is no longer refused while batching
 
         // Send the remote update before applying the local set: SetPoolAdapters routes over the pool's
         // own set, so it must travel over the set still shared with the destination.
```

## Hub #9145

a withdrawal is posted like a deposit, debiting the holding's own account and crediting its counterpart instead of the other way about.

- **Mutant:** [`9145.sol`](9145.sol)
- **Caught by:** [`hlHuJournalPrimitivePostsOneBalancedPair`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L113)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9145`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuJournalPrimitivePostsOneBalancedPair`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -541,7 +541,7 @@
     {
         if (diff == 0) return;
         if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.AmountCredit);
-        else _journal(poolId, scId, assetId, diff, AccountKind.AmountCredit, AccountKind.AmountDebit);
+        else _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.AmountCredit); // MUTATION: a withdrawal is posted like a deposit
     }
 
     /// @inheritdoc IHub
```

## Hub #9146

the adapter announcement names the session after the one installed locally, so the destination and the hub converge on different sessions.

- **Mutant:** [`9146.sol`](9146.sol)
- **Caught by:** [`hlHuSetAdaptersAnnouncesTheSessionItInstalls`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L140)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9146`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuSetAdaptersAnnouncesTheSessionItInstalls`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -144,7 +144,7 @@
         // own set, so it must travel over the set still shared with the destination.
         uint16 targetSessionId = multiAdapter.nextActiveSessionId(centrifugeId, poolId);
         sender.sendSetPoolAdapters{value: msgValue()}(
-            centrifugeId, poolId, remoteAdapters, threshold, targetSessionId, refund
+            centrifugeId, poolId, remoteAdapters, threshold, targetSessionId + 1, refund // MUTATION: the remote side is told the session after the one installed
         );
 
         multiAdapter.setAdapters(centrifugeId, poolId, localAdapters, threshold, targetSessionId);
```

## Hub #9147

both revaluation postings book the holding's own account on the wrong side, so a write down debits it instead of crediting it.

- **Mutant:** [`9147.sol`](9147.sol)
- **Caught by:** [`hlHuValuationDropNeverRaisesTheHoldingRowsValue`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L173)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9147`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuValuationDropNeverRaisesTheHoldingRowsValue`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -559,8 +559,8 @@
         internal
     {
         if (diff == 0) return;
-        if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.ValueIncrease);
-        else _journal(poolId, scId, assetId, diff, AccountKind.ValueDecrease, AccountKind.AmountDebit);
+        if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.ValueIncrease, AccountKind.AmountDebit);
+        else _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.ValueDecrease); // MUTATION: both revaluation legs post the holding's own row on the wrong side
     }
 
     /// @dev Unlock, post the debit/credit pair against the given account slots, then lock.
```

## Hub #9148

both amount postings book the holding's own account on the wrong side, so an increase credits it instead of debiting it.

- **Mutant:** [`9148.sol`](9148.sol)
- **Caught by:** [`stHuProtocolValueMovesLandOnTheHoldingsOwnRow`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_transitions.spec#L201)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9148`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/transitions.conf --rule stHuProtocolValueMovesLandOnTheHoldingsOwnRow`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -540,8 +540,8 @@
         internal
     {
         if (diff == 0) return;
-        if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.AmountCredit);
-        else _journal(poolId, scId, assetId, diff, AccountKind.AmountCredit, AccountKind.AmountDebit);
+        if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountCredit, AccountKind.AmountDebit);
+        else _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.AmountCredit); // MUTATION: both amount legs post the holding's own row on the wrong side
     }
 
     /// @inheritdoc IHub
```

## Hub #9149

a hub admin bypasses the manager gate only while no policy is set, so a standing policy can no longer be replaced without its consent.

- **Mutant:** [`9149.sol`](9149.sol)
- **Caught by:** [`rcHuGovernanceReplacesAStandingRuleBookIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L895)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9149`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuGovernanceReplacesAStandingRuleBookIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -99,7 +99,7 @@
 
     /// @inheritdoc IHub
     function setPolicy(PoolId poolId, IHubPolicy policy_) external {
-        if (wards[msgSender()] != 1) _enforce(poolId);
+        if (wards[msgSender()] != 1 || address(hubRegistry.policy(poolId)) != address(0)) _enforce(poolId); // MUTATION: a standing rule book is always consulted
 
         hubRegistry.setPolicy(poolId, policy_);
     }
```

## Hub #9150

a write down debits the holding's own account instead of crediting it, so a drop can no longer raise a credit normal account.

- **Mutant:** [`9150.sol`](9150.sol)
- **Caught by:** [`rcHuValuationDropRaisesACreditNormalHoldingRowIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L914)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9150`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuValuationDropRaisesACreditNormalHoldingRowIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -560,7 +560,7 @@
     {
         if (diff == 0) return;
         if (isPositive) _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.ValueIncrease);
-        else _journal(poolId, scId, assetId, diff, AccountKind.ValueDecrease, AccountKind.AmountDebit);
+        else _journal(poolId, scId, assetId, diff, AccountKind.AmountDebit, AccountKind.ValueDecrease); // MUTATION: a write down debits the holding's own row
     }
 
     /// @dev Unlock, post the debit/credit pair against the given account slots, then lock.
```

## Hub #9151

a manager authored journal opens and closes the ledger without posting its entries, so no manual journal can move a holding's account.

- **Mutant:** [`9151.sol`](9151.sol)
- **Caught by:** [`rcHuManualJournalMovesAHoldingRowButNotItsValueIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L936)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9151`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuManualJournalMovesAHoldingRowButNotItsValueIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -383,7 +383,7 @@
         enforced(poolId)
     {
         accounting.unlock(poolId);
-        accounting.addJournal(debits, credits);
+        // MUTATION: a manager journal posts nothing
         accounting.lock();
     }
 
```

## Hub #9152

a holding's own amount debit slot can no longer be repointed, so no rewiring can leave its carried value unmatched by the account it names.

- **Mutant:** [`9152.sol`](9152.sol)
- **Caught by:** [`rcHuRewiredHoldingRowLeavesItsValueUnmatchedIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L959)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9152`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuRewiredHoldingRowLeavesItsValueUnmatchedIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -371,7 +371,7 @@
         payable
         enforced(poolId)
     {
-        require(accounting.exists(poolId, accountId), IAccounting.AccountDoesNotExist());
+        require(accounting.exists(poolId, accountId) && kind != uint8(AccountKind.AmountDebit), IAccounting.AccountDoesNotExist()); // MUTATION: the holding's own slot can no longer be repointed
 
         holdings.setAccountId(poolId, scId, assetId, kind, accountId);
     }
```

## Hub #9154

rewiring a request manager through the hub no longer tells the spoke, so hub and spoke route requests to mismatched managers.

- **Mutant:** [`9154.sol`](9154.sol)
- **Caught by:** [`rcHuHubPathRequestManagerRewireDispatchesTheSyncIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1000)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9154`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuHubPathRequestManagerRewireDispatchesTheSyncIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -212,7 +212,7 @@
         hubRegistry.setHubRequestManager(poolId, centrifugeId, hubManager);
 
         emit SetSpokeRequestManager(centrifugeId, poolId, spokeManager);
-        sender.sendSetRequestManager{value: msgValue()}(centrifugeId, poolId, spokeManager, refund);
+        // MUTATION: the spoke is never told its new request manager
     }
 
     /// @inheritdoc IHub
```

## Hub #9477

opening a holding books its tracked amount's value as a gain instead of principal, so the credit hits the gain account.

- **Mutant:** [`9477.sol`](9477.sol)
- **Caught by:** [`hlHuInitializationBooksTheTrackedAmountAsPrincipal`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L201)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9477`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuInitializationBooksTheTrackedAmountAsPrincipal`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -345,7 +345,7 @@
         // If increase/decrease was called before initialize, the tracked amount carries no value yet:
         // establish it at the valuation and book it as principal.
         (, uint128 initialValue) = holdings.update(poolId, scId, assetId);
-        _updateAccountingAmount(poolId, scId, assetId, true, initialValue);
+        _updateAccountingValue(poolId, scId, assetId, true, initialValue); // MUTATION: the opening value is journaled as a gain
     }
 
     /// @inheritdoc IHub
```

## Hub #9478

a share price update no longer calls the installed fee hook, so fees stop accruing on every share price move.

- **Mutant:** [`9478.sol`](9478.sol)
- **Caught by:** [`hlHuSharePriceUpdateAccruesExactlyWhenAFeeHookIsInstalled`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L229) · [`hlHuSharePriceUpdateStampedNowAccruesExactlyWhenAFeeHookIsInstalled`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L247)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9478`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuSharePriceUpdateAccruesExactlyWhenAFeeHookIsInstalled hlHuSharePriceUpdateStampedNowAccruesExactlyWhenAFeeHookIsInstalled`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -303,7 +303,7 @@
         enforced(poolId)
     {
         shareClassManager.updateSharePrice(poolId, scId, pricePoolPerShare, computedAt);
-        _accrue(poolId, scId);
+        // MUTATION: a share price update no longer accrues fees, the _accrue(poolId, scId) call is removed
     }
 
     /// @inheritdoc IHub
```

## Hub #9479

the pool's policy is told the hub is the caller, so a per caller policy judges the wrong party.

- **Mutant:** [`9479.sol`](9479.sol)
- **Caught by:** [`rvHuEnforcedEntryPassesTheInstalledPolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L319) · [`rvHuSpokeCallRevokePassesThePolicy`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reverts.spec#L344)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9479`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reverts.conf --rule rvHuEnforcedEntryPassesTheInstalledPolicy rvHuSpokeCallRevokePassesThePolicy`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -599,7 +599,7 @@
         _requireManager(poolId);
 
         IHubPolicy policy_ = hubRegistry.policy(poolId);
-        if (address(policy_) != address(0)) policy_.enforce(poolId, msgSender(), msg.data);
+        if (address(policy_) != address(0)) policy_.enforce(poolId, address(this), msg.data); // MUTATION: the rule book is told the hub is the caller
     }
 
     /// @dev Reverts unless the resolved sender is a registered manager for `poolId`.
```

## Hub #9480

writing pool metadata skips the manager and policy checks, so any caller can rewrite what the pool publishes.

- **Mutant:** [`9480.sol`](9480.sol)
- **Caught by:** [`rvHuPoolMetadataWriterPassesBothGates`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L42)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9480`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/metadata_properties.conf --rule rvHuPoolMetadataWriterPassesBothGates`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -161,7 +161,7 @@
     }
 
     /// @inheritdoc IHub
-    function setPoolMetadata(PoolId poolId, bytes calldata metadata) external payable enforced(poolId) {
+    function setPoolMetadata(PoolId poolId, bytes calldata metadata) external payable { // MUTATION: pool metadata is written without the manager seat or the rule book
         hubRegistry.setMetadata(poolId, metadata);
     }
 
```

## Hub #9481

writing an account's metadata opens a ledger session for the pool and returns without closing it, so the ledger stays unlocked after the call.

- **Mutant:** [`9481.sol`](9481.sol)
- **Caught by:** [`stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9481`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/metadata_properties.conf --rule stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -322,7 +322,7 @@
         payable
         enforced(poolId)
     {
-        accounting.setAccountMetadata(poolId, account, metadata);
+        accounting.unlock(poolId); accounting.setAccountMetadata(poolId, account, metadata); // MUTATION: the ledger session is opened and never closed
     }
 
     /// @inheritdoc IHub
```

## Hub #9482

a hub admin replacing a pool's policy must first pass the standing policy, so the governance override can be blocked by the policy it replaces.

- **Mutant:** [`9482.sol`](9482.sol)
- **Caught by:** [`rcHuWardSwapsARefusingRuleBookWithoutItsConsentIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L1016)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9482`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuWardSwapsARefusingRuleBookWithoutItsConsentIsReachable`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -99,7 +99,7 @@
 
     /// @inheritdoc IHub
     function setPolicy(PoolId poolId, IHubPolicy policy_) external {
-        if (wards[msgSender()] != 1) _enforce(poolId);
+        if (wards[msgSender()] != 1) _enforce(poolId); else if (address(hubRegistry.policy(poolId)) != address(0)) hubRegistry.policy(poolId).enforce(poolId, msgSender(), msg.data); // MUTATION: a ward's swap must also pass the standing rule book
 
         hubRegistry.setPolicy(poolId, policy_);
     }
```

## Hub #9483

an asset price notification no longer calls the installed fee hook, so fees stop accruing on every asset price broadcast.

- **Mutant:** [`9483.sol`](9483.sol)
- **Caught by:** [`hlHuAssetPriceNotificationAccruesExactlyWhenAFeeHookIsInstalled`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L265)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9483`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuAssetPriceNotificationAccruesExactlyWhenAFeeHookIsInstalled`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -471,7 +471,7 @@
         emit NotifyAssetPrice(assetId.centrifugeId(), poolId, scId, assetId, pricePoolPerAsset_);
         sender.sendNotifyPricePoolPerAsset{value: msgValue()}(poolId, scId, assetId, pricePoolPerAsset_, refund);
 
-        _accrue(poolId, scId);
+        // MUTATION: an asset price notification no longer accrues fees, the _accrue(poolId, scId) call is removed
     }
 
     //----------------------------------------------------------------------------------------------
```

## Hub #9484

writing an account's metadata no longer asks for a pool manager or passes the pool's policy, so any caller can relabel the pool's ledger accounts.

- **Mutant:** [`9484.sol`](9484.sol)
- **Caught by:** [`rvHuAccountMetadataWriterPassesBothGates`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L65)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9484`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/metadata_properties.conf --rule rvHuAccountMetadataWriterPassesBothGates`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -320,7 +320,7 @@
     function setAccountMetadata(PoolId poolId, AccountId account, bytes calldata metadata)
         external
         payable
-        enforced(poolId)
+        // MUTATION: account metadata is written without the manager seat or the rule book
     {
         accounting.setAccountMetadata(poolId, account, metadata);
     }
```

## Hub #9485

renaming a share class skips the manager and policy checks, so any caller can rename a class and its symbol.

- **Mutant:** [`9485.sol`](9485.sol)
- **Caught by:** [`rvHuShareClassMetadataWriterPassesBothGates`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L89)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9485`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/metadata_properties.conf --rule rvHuShareClassMetadataWriterPassesBothGates`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -174,7 +174,7 @@
     function updateShareClassMetadata(PoolId poolId, ShareClassId scId, string calldata name, string calldata symbol)
         external
         payable
-        enforced(poolId)
+        // MUTATION: share class metadata is written without the manager seat or the rule book
     {
         shareClassManager.updateMetadata(poolId, scId, name, symbol);
     }
```

## Hub #9486

writing a pool's metadata opens a ledger session for the pool and returns without closing it, so the ledger stays unlocked after the call.

- **Mutant:** [`9486.sol`](9486.sol)
- **Caught by:** [`stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9486`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/metadata_properties.conf --rule stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -162,7 +162,7 @@
 
     /// @inheritdoc IHub
     function setPoolMetadata(PoolId poolId, bytes calldata metadata) external payable enforced(poolId) {
-        hubRegistry.setMetadata(poolId, metadata);
+        accounting.unlock(poolId); hubRegistry.setMetadata(poolId, metadata); // MUTATION: the ledger session is opened and never closed
     }
 
     /// @inheritdoc IHub
```

## Hub #9487

renaming a share class opens a ledger session for the pool and returns without closing it, so the ledger stays unlocked after the call.

- **Mutant:** [`9487.sol`](9487.sol)
- **Caught by:** [`stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive`](../../specs/core/hub/Hub_LinkedHubCore/Hub_LinkedHubCore_metadata_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9487`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/metadata_properties.conf --rule stHuEveryHubCallLeavesTheLedgerLockedWithTheWritersLive`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -176,7 +176,7 @@
         payable
         enforced(poolId)
     {
-        shareClassManager.updateMetadata(poolId, scId, name, symbol);
+        accounting.unlock(poolId); shareClassManager.updateMetadata(poolId, scId, name, symbol); // MUTATION: the ledger session is opened and never closed
     }
 
     //----------------------------------------------------------------------------------------------
```

## Hub #9710

the hub installs the new local adapter set before sending the remote update, so the update may never arrive.

- **Mutant:** [`9710.sol`](9710.sol)
- **Caught by:** [`hlHuSetAdaptersSendsBeforeItInstalls`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_high_level.spec#L156)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Hub 9710`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/high_level.conf --rule hlHuSetAdaptersSendsBeforeItInstalls`

```diff
--- a/src/core/hub/Hub.sol
+++ b/src/core/hub/Hub.sol
@@ -143,11 +143,12 @@
         // Send the remote update before applying the local set: SetPoolAdapters routes over the pool's
         // own set, so it must travel over the set still shared with the destination.
         uint16 targetSessionId = multiAdapter.nextActiveSessionId(centrifugeId, poolId);
+        // MUTATION: the new local set is installed before the remote update is sent
+        multiAdapter.setAdapters(centrifugeId, poolId, localAdapters, threshold, targetSessionId);
+
         sender.sendSetPoolAdapters{value: msgValue()}(
             centrifugeId, poolId, remoteAdapters, threshold, targetSessionId, refund
         );
-
-        multiAdapter.setAdapters(centrifugeId, poolId, localAdapters, threshold, targetSessionId);
     }
 
     /// @inheritdoc IHub
```

