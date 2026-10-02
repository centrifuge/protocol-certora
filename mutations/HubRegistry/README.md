# Mutations for `HubRegistry` (`src/core/hub/HubRegistry.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/types/PoolId.sol`, `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [1002](#hubregistry-1002) | registerAsset drops the 18-decimal cap check, so an asset can register with arbitrary precision.<br>Caught by: [`assetDecimalsCapped`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L26) |
| [1003](#hubregistry-1003) | registerAsset stores the decimals but never sets the registered flag, leaving precision on an unregistered row.<br>Caught by: [`unregisteredAssetHasZeroDecimals`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L31) |
| [1004](#hubregistry-1004) | registerAsset drops the empty-id check, so the null asset id can enter the registry.<br>Caught by: [`nullAssetNeverRegistered`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L36) |
| [1005](#hubregistry-1005) | registerPool no longer checks the pool currency is a registered asset, so a pool can be created denominated in an unknown asset.<br>Caught by: [`poolCurrencyRegistered`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L41) |
| [1006](#hubregistry-1006) | updateManager drops the pool-existence check, so manager rights can be granted on a pool that was never created.<br>Caught by: [`managerImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L46) |
| [1007](#hubregistry-1007) | updateManager drops the zero-address check, so the zero address can be granted manager rights.<br>Caught by: [`zeroAddressNeverManager`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L51) |
| [1008](#hubregistry-1008) | setPolicy drops the pool-existence check, so a policy installs and the nonce advances on a pool that was never created.<br>Caught by: [`policyImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L56) · [`nonceImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L61) |
| [1009](#hubregistry-1009) | setPolicy no longer advances the install nonce, so a predecessor's pending authorizations stay live and revive on reinstall.<br>Caught by: [`policyImpliesNonzeroNonce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L66) · [`pendingUnderCurrentNonceMatchesPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L109) |
| [1010](#hubregistry-1010) | setBridgingHook drops the pool-existence check, so a bridging hook can be wired to a pool that was never created.<br>Caught by: [`bridgingHookImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L71) |
| [1011](#hubregistry-1011) | setHubRequestManager drops the pool-existence check, so a request manager can be wired to a pool that was never created.<br>Caught by: [`requestManagerImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L76) |
| [1012](#hubregistry-1012) | initiateAuthorization stores the relative delay instead of the absolute maturity timestamp, so a pending authorization can mature in the past.<br>Caught by: [`pendingAuthAboveEnvFloor`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L81) |
| [1013](#hubregistry-1013) | initiateAuthorization keys the pending entry by the calling account instead of the installed policy, planting entries in foreign policy namespaces.<br>Caught by: [`pendingNeverUnderNullPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L87) · [`pendingUnderCurrentNonceMatchesPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L109) |
| [1014](#hubregistry-1014) | initiateAuthorization keys the pending entry one policy tenure behind, so the first policy's grants land under the reserved nonce zero.<br>Caught by: [`pendingNeverUnderZeroNonce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L93) |
| [1015](#hubregistry-1015) | initiateAuthorization keys the pending entry one policy tenure ahead, so reinstalling the same policy inherits a pre-scheduled grant.<br>Caught by: [`pendingNeverAheadOfNonce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L103) |
| [1018](#hubregistry-1018) | registerPool drops the zero-manager check, so a pool can be created with the zero address as its initial manager.<br>Caught by: [`zeroAddressNeverManager`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L51) |
| [1023](#hubregistry-1023) | registerPoolPair registers two pools under one manager in one call, so one call writes two pools' registry rows and rosters.<br>Caught by: [`stHrPoolRowIsPerPool`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L7) · [`stHrManagerRightsArePerPool`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L36) |
| [1024](#hubregistry-1024) | setHubRequestManagerFor wires one pool's request manager onto a sibling pool as well, so one call routes two pools' requests.<br>Caught by: [`stHrRequestManagerIsPerPool`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L53) |
| [1025](#hubregistry-1025) | initiateAuthorizationPair schedules one authorization across two pools, so one call opens a timelock in both namespaces.<br>Caught by: [`stHrPendingAuthIsPerPool`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L70) |
| [1027](#hubregistry-1027) | setPolicy installs a replacement without advancing the tenure, so reinstalling a policy later revives its old queued authorizations.<br>Caught by: [`stHrPolicySwapOpensANewTenure`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L113) |
| [1028](#hubregistry-1028) | initiateAuthorization stamps maturity at the scheduling moment itself, so a privileged action is ready the instant it is queued.<br>Caught by: [`stHrSchedulingMaturesAheadAndInTheLiveTenure`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L145) |
| [1029](#hubregistry-1029) | consuming an authorization also advances the pool's tenure, so discharging one action invalidates every other queued under the same policy.<br>Caught by: [`stHrDischargeLeavesTheTenureStanding`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L165) |
| [1031](#hubregistry-1031) | initiateAuthorization no longer rejects re-authorizing a live grant, so a second schedule silently resets the maturity clock in place.<br>Caught by: [`stHrPendingMovesOnlyOffOrOntoZero`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L185) |
| [1032](#hubregistry-1032) | registerAsset no longer rejects re-registering an asset at a different precision, so re-registering overwrites its decimals under holdings already priced against it.<br>Caught by: [`stHrRegisteredAssetStaysAndASetPrecisionIsFinal`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L212) · [`stHrPoolCurrencySetPrecisionIsStable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L230) |
| [1033](#hubregistry-1033) | updateCurrency no longer requires matching decimals, so swapping the currency changes the pool's unit precision.<br>Caught by: [`stHrPoolCurrencySetPrecisionIsStable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L230) |
| [1034](#hubregistry-1034) | updateCurrency clears the pool's currency instead of setting the new one, so a created pool silently becomes uncreated.<br>Caught by: [`stHrCurrencyNeverClears`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L199) |
| [1039](#hubregistry-1039) | setPolicy rewinds the tenure nonce instead of advancing it, so the new policy can land on a namespace a past tenure already populated.<br>Caught by: [`stHrNewTenureStartsWithNoSchedule`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L128) |
| [1041](#hubregistry-1041) | initiateAuthorization leaves the authorization id underived, so every scheduled grant is stamped under the zero id.<br>Caught by: [`nullAuthIdNeverPending`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L118) |
| [1042](#hubregistry-1042) | setHubRequestManager no longer checks the pool exists, so a request manager can be wired to a pool never created.<br>Caught by: [`requestManagerImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L76) |
| [4900](#hubregistry-4900) | The shared ward gate no longer looks at the caller, so every registry write the hub reserves for its wards is open to any account.<br>Caught by: [`acHrAssetRowMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L20) · [`acHrPoolCurrencyMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L40) · [`acHrManagerRightsMoveOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L57) · [`acHrPolicyRowMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L73) · [`acHrBridgingHookMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L93) · [`acHrRequestManagerMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L109) · [`acHrAuthorizationIsScheduledOnlyByAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L126) · [`acHrPendingAuthorizationMovesOnlyForAWardOrThePolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L143) |
| [4901](#hubregistry-4901) | rely loses its ward gate, so any account can hand itself authority over the registry.<br>Caught by: [`acHrWardRightsMoveOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L4) |
| [4902](#hubregistry-4902) | Pool creation seats the calling ward as a manager alongside the account it names, so one call hands out two manager seats.<br>Caught by: [`vtHrManagerRosterMovesOneAccountAtATime`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L6) |
| [4903](#hubregistry-4903) | Installing a policy advances the tenure counter by two, so the registry skips a namespace on every policy swap.<br>Caught by: [`vtHrTenureCounterAdvancesByAtMostOne`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L25) |
| [4904](#hubregistry-4904) | Wiring a request manager on one network also wires the next network id, so one call reroutes two chains worth of hub requests.<br>Caught by: [`vtHrRequestManagerMovesOneNetworkAtATime`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L41) |
| [4905](#hubregistry-4905) | Scheduling an authorization also stamps the same maturity into the next tenure namespace, so one call puts two entries on the timelock.<br>Caught by: [`vtHrAuthLedgerMovesOneEntryAtATime`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L60) |
| [4906](#hubregistry-4906) | consumeAuthorization no longer requires a scheduled entry, so an unscheduled call passes whenever the expiry reaches the current time.<br>Caught by: [`hlHrAuthorizationIsSpentOnlyOnce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L6) · [`hlHrConsumeSpendsOnlyALiveEntry`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L22) · [`hlHrCanceledAuthorizationNeverFires`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L71) |
| [4907](#hubregistry-4907) | consumeAuthorization admits a grant one second before it matures, so the veto window a sentinel was promised ends a second early.<br>Caught by: [`hlHrConsumeWaitsOutTheVetoDelay`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L38) |
| [4908](#hubregistry-4908) | consumeAuthorization admits a grant one second past the window the call names, so a stale grant still fires.<br>Caught by: [`hlHrConsumeRefusesAStaleGrant`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L54) |
| [4909](#hubregistry-4909) | Installing a policy also stamps a timelock entry, so the authorization ledger changes outside schedule, cancel and consume.<br>Caught by: [`vtHrAuthLedgerMovesOnlyThroughItsThreeWriters`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L79) |
| [4910](#hubregistry-4910) | Wiring a bridging hook also seats that hook as a pool manager, so manager rights move through a writer that never grants them.<br>Caught by: [`vtHrManagerRightsMoveOnlyThroughTheirTwoWriters`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L95) |
| [4912](#hubregistry-4912) | Pool creation no longer seats the account it names, so a pool is born with no manager at all.<br>Caught by: [`hlHrPoolCreationSeatsTheAccountItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L105) |
| [4913](#hubregistry-4913) | The token standard precision read answers the eighteen decimal registration cap instead of the precision the registry recorded.<br>Caught by: [`hlHrTokenPrecisionMatchesTheAssetRow`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L116) |
| [4914](#hubregistry-4914) | registerAsset applies its precision cap one decimal too tight, so an eighteen decimal asset can never be registered.<br>Caught by: [`rvHrRegisterAssetIsNeverRefusedToAWardOnAFreshAssetWithinTheCap`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L237) · [`rvHrRegisterAssetIsNeverRefusedToAWardFillingOrKeepingARegisteredPrecision`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L341) |
| [4915](#hubregistry-4915) | registerPool no longer checks its currency is a registered asset, so a pool can be created on an unknown asset.<br>Caught by: [`rvHrRegisterPoolRefusesAnUnusableOrRepeatedOpening`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L7) |
| [4916](#hubregistry-4916) | updateManager no longer refuses the zero address, so a manager seat can be handed to nobody.<br>Caught by: [`rvHrUpdateManagerRefusesANonWardAnAbsentPoolOrANullSeat`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L25) |
| [4917](#hubregistry-4917) | updateCurrency no longer checks the incoming currency accounts in the same precision, so a pool can be redenominated across scales.<br>Caught by: [`rvHrUpdateCurrencyRefusesANonWardAnAbsentPoolOrARescaling`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L41) |
| [4918](#hubregistry-4918) | Installing a policy no longer bumps its nonce, so reinstalling the same policy leaves its earlier grants consumable.<br>Caught by: [`rvHrRetiredGrantIsNeverConsumed`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L195) |
| [4919](#hubregistry-4919) | setHubRequestManager no longer checks the pool exists, so hub requests can be routed for a pool that was never created.<br>Caught by: [`rvHrSetHubRequestManagerRefusesANonWardOrAnAbsentPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L77) |
| [4920](#hubregistry-4920) | setBridgingHook refuses the zero address, so a pool can never unwire the hook that sits on its cross chain share movements.<br>Caught by: [`rvHrSetBridgingHookIsNeverRefusedToAWardOnALivePool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L93) |
| [4921](#hubregistry-4921) | initiateAuthorization no longer refuses a call that needs no delay, so it records a grant that matures instantly.<br>Caught by: [`rvHrInitiateAuthorizationRefusesANonWardAnInPolicyCallOrATakenSlot`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L109) |
| [4922](#hubregistry-4922) | cancelAuthorization no longer checks a grant is standing, so a veto of nothing succeeds and writes a misleading audit entry.<br>Caught by: [`rvHrCancelAuthorizationRefusesANonWardOrAnEmptySlot`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L129) |
| [4923](#hubregistry-4923) | consumeAuthorization refuses a grant at the very instant it matures, so the first second of the window is lost.<br>Caught by: [`rvHrConsumeAuthorizationIsNeverRefusedToThePolicyInsideItsWindow`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L147) |
| [4924](#hubregistry-4924) | decimals no longer checks the asset is registered, so an unknown asset reads back as zero decimals.<br>Caught by: [`rvHrTokenDecimalsRefusesAnAssetTheRegistryDoesNotCarry`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L170) |
| [4925](#hubregistry-4925) | authId refuses a pool that runs no policy, so a sentinel cannot compute the identifier of the grant it means to veto.<br>Caught by: [`rvHrAuthIdAlwaysAnswers`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L183) |
| [4928](#hubregistry-4928) | the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.<br>Caught by: [`rvHrRelyRefusesANonWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L211) · [`rvHrDenyRefusesANonWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L224) · [`rvHrRegisterAssetRefusesANonWardAnOversizedPrecisionOrARescale`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L322) · [`rvHrSetBridgingHookRefusesANonWardOrAnAbsentPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L378) |
| [6400](#hubregistry-6400) | registerAsset records one decimal more than declared, so every asset is registered at the wrong precision.<br>Caught by: [`rcHrRegisterAssetIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L4) · [`rcHrRegisterAssetAtThePrecisionCapIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L19) · [`rcHrRegisterAssetWithZeroPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L34) · [`rcHrRegisterAssetFillsAnUnsetPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L385) · [`rcHrRegisterAssetRepeatsAtItsOwnPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L399) |
| [6401](#hubregistry-6401) | registerAsset writes the asset's precision but leaves the row unregistered, so an asset never actually joins the registry.<br>Caught by: [`rcHrRegisterAssetIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L4) |
| [6402](#hubregistry-6402) | registerPool records the currency but never seats the named manager, so a new pool starts with no manager.<br>Caught by: [`rcHrRegisterPoolIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L48) · [`rcHrRegisterAssetThenRegisterPoolIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L67) |
| [6403](#hubregistry-6403) | Pool creation seats the manager it names but never records the denomination, so the pool never comes into existence.<br>Caught by: [`rcHrRegisterPoolIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L48) |
| [6404](#hubregistry-6404) | updateManager reads the flag it is handed backwards, so seating an account revokes it and revoking an account seats it.<br>Caught by: [`rcHrUpdateManagerSeatsAManagerIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L86) · [`rcHrUpdateManagerRevokesASeatIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L99) |
| [6405](#hubregistry-6405) | updateCurrency accepts only the denomination the pool already carries, so a live pool can never be redenominated onto another asset.<br>Caught by: [`rcHrUpdateCurrencyRedenominatesThePoolIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L112) |
| [6406](#hubregistry-6406) | setBridgingHook turns away the zero address, so an attached bridging hook can never be taken off again.<br>Caught by: [`rcHrSetBridgingHookDetachesIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L141) |
| [6408](#hubregistry-6408) | setHubRequestManager wires the neighbouring network instead of the one it is handed, so the network the pool named is never routed.<br>Caught by: [`rcHrSetHubRequestManagerWiresANetworkIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L155) |
| [6409](#hubregistry-6409) | setPolicy refuses a pool with no policy yet, so a pool's first policy can never be installed.<br>Caught by: [`rcHrSetPolicyInstallsTheFirstPolicyIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L171) |
| [6410](#hubregistry-6410) | setPolicy turns away the zero address, so an installed policy can never be uninstalled.<br>Caught by: [`rcHrSetPolicyUninstallsWithTheZeroAddressIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L187) |
| [6411](#hubregistry-6411) | Installing a policy leaves the tenure counter standing, so no install ever opens a new namespace.<br>Caught by: [`rcHrSetPolicyAtTheLastNamespaceIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L204) · [`rcHrPolicyViewsReportTheInstallIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L334) |
| [6412](#hubregistry-6412) | setPolicy checks the pool and announces the install but records nothing, so the pool keeps the policy and the tenure it already had.<br>Caught by: [`rcHrOrphanedScheduleCanBeRemadeAfterAPolicySwapIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L218) · [`rcHrAuthIdChangesAcrossAPolicySwapIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L354) |
| [6413](#hubregistry-6413) | initiateAuthorization stamps maturity at the scheduling moment itself, so a scheduled call is ready the instant it is queued.<br>Caught by: [`rcHrInitiateAuthorizationAtTheMaturityCeilingIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L241) |
| [6414](#hubregistry-6414) | initiateAuthorization refuses an empty payload, so the shortest schedulable call can never be put on the clock.<br>Caught by: [`rcHuPrivilegedCallSchedulingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L183) · [`rcHuScheduledCallWithdrawalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L203) |
| [6415](#hubregistry-6415) | cancelAuthorization refuses a grant that has not matured yet, so the veto window the delay exists for can never be used.<br>Caught by: [`rcHrCancelAuthorizationIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L260) |
| [6416](#hubregistry-6416) | consumeAuthorization turns away the pool's own policy and answers every other caller, so the policy can never discharge a grant it scheduled.<br>Caught by: [`rvHrConsumeAuthorizationIsNeverRefusedToThePolicyInsideItsWindow`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L147) · [`rvHrConsumeAuthorizationRefusesEveryCallerButTheInstalledPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L257) |
| [6417](#hubregistry-6417) | consumeAuthorization reads its maturity check backwards, so a grant can fire before its veto delay ends but never after.<br>Caught by: [`hlHrConsumeWaitsOutTheVetoDelay`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L38) |
| [6418](#hubregistry-6418) | consumeAuthorization refuses a grant at the very instant it matures, so the opening second of the window is lost.<br>Caught by: [`rcHrConsumeAuthorizationAtTheMaturityInstantIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L277) |
| [6419](#hubregistry-6419) | consumeAuthorization shuts the window a second early, so a grant can never be fired at the last instant the policy allows.<br>Caught by: [`rcHrConsumeAuthorizationAtTheExpiryEdgeIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L296) |
| [6420](#hubregistry-6420) | rely clears the ward slot instead of setting it, so authority can never be handed to an account that holds none.<br>Caught by: [`rcHrAuthorityRoundTripIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L316) |
| [6421](#hubregistry-6421) | deny sets the ward slot instead of clearing it, so authority can never be taken back from an account that holds it.<br>Caught by: [`rcHrAuthorityRoundTripIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L316) |
| [6422](#hubregistry-6422) | setPolicy records the caller instead of the policy it was handed, so the pool is governed by whoever configured it.<br>Caught by: [`rcHrPolicyViewsReportTheInstallIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L334) |
| [6423](#hubregistry-6423) | setPolicy bumps the tenure counter but writes the sitting rule book back, so a pool never leaves the policy it is already running under.<br>Caught by: [`hlHrSetPolicyInstallsExactlyTheAddressItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L129) |
| [8410](#hubregistry-8410) | registerAsset lets a set precision grow on re-registration, so an asset or a pool currency priced at six decimals can be moved to eight.<br>Caught by: [`stHrRegisteredAssetStaysAndASetPrecisionIsFinal`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L212) · [`stHrPoolCurrencySetPrecisionIsStable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L230) |
| [8411](#hubregistry-8411) | registerAsset lets any registered asset be rescaled to eighteen decimals, so a set precision is moved without a revert.<br>Caught by: [`rvHrRegisterAssetRefusesANonWardAnOversizedPrecisionOrARescale`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L322) |
| [8412](#hubregistry-8412) | registerAsset no longer lets an unset precision be filled, so an asset registered at zero decimals keeps them for good.<br>Caught by: [`rcHrRegisterAssetFillsAnUnsetPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L385) |
| [8413](#hubregistry-8413) | registerAsset refuses a ward who fills an unset precision, so a zero precision read off an uninitialized token can never be corrected.<br>Caught by: [`rvHrRegisterAssetIsNeverRefusedToAWardFillingOrKeepingARegisteredPrecision`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L341) |
| [8414](#hubregistry-8414) | registerAsset refuses a repeat at the stored nonzero precision, so an idempotent re-registration reverts.<br>Caught by: [`rcHrRegisterAssetRepeatsAtItsOwnPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L399) |
| [8620](#hubregistry-8620) | setPolicy keeps the old tenure when the same policy is reinstalled, so grants meant to be voided stay spendable.<br>Caught by: [`hlHrSetPolicyInstallsExactlyTheAddressItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L129) |
| [8621](#hubregistry-8621) | consumeAuthorization no longer deletes the grant it spends, so one veto window funds the same privileged call again and again.<br>Caught by: [`hlHrAuthorizationIsSpentOnlyOnce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L6) |
| [8622](#hubregistry-8622) | cancelAuthorization no longer deletes the grant it vetoes, so a canceled call still matures and can be fired.<br>Caught by: [`hlHrCanceledAuthorizationNeverFires`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L71) |
| [8623](#hubregistry-8623) | consumeAuthorization looks grants up one tenure back, so a grant voided by a reinstall can be spent and a current one never.<br>Caught by: [`hlHrConsumeSpendsOnlyALiveEntry`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L22) |
| [8625](#hubregistry-8625) | setPolicy keeps the tenure when the same policy is reinstalled, so grants scheduled before the reinstall stay spendable.<br>Caught by: [`rvHrRetiredGrantIsNeverConsumed`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L195) |
| [8805](#hubregistry-8805) | cancelAuthorization refuses a grant once it has matured, so a ward can no longer veto a matured call the policy has not yet fired.<br>Caught by: [`rvHrCancelAuthorizationIsNeverRefusedToAWardWithAPendingGrant`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L361) |
| [8806](#hubregistry-8806) | setBridgingHook checks the pool exists only when attaching a hook, so a hook can be cleared on a pool that was never created.<br>Caught by: [`rvHrSetBridgingHookRefusesANonWardOrAnAbsentPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L378) |
| [8807](#hubregistry-8807) | registerPool installs the named manager as the pool policy, so a new pool opens its first policy tenure at creation.<br>Caught by: [`hlHrPoolCreationLeavesThePoolWithoutAPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L193) |
| [8809](#hubregistry-8809) | registerPool fills a zero precision of the currency it names with eighteen decimals, so pool creation changes an asset's precision.<br>Caught by: [`stHrRegisteredAssetStaysAndASetPrecisionIsFinal`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L212) |
| [8810](#hubregistry-8810) | updateCurrency skips the decimals match when the sitting currency has zero decimals, so a currency swap moves the pool precision off zero.<br>Caught by: [`stHrPoolCurrencySetPrecisionIsStable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L230) |
| [8950](#hubregistry-8950) | setPolicy no longer checks that the pool exists, so a policy and a tenure can be installed on a pool that was never created.<br>Caught by: [`rvHrSetPolicyRefusesANonWardOrAnAbsentPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L62) |
| [9020](#hubregistry-9020) | registerAsset stores the 18 decimal cap instead of the precision it was given, so an asset reads back a precision it was never registered with.<br>Caught by: [`hlHrAssetRegistrationRecordsThePrecisionItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L142) |
| [9021](#hubregistry-9021) | registerPool also seats the ward that opens the pool, so a new pool starts with a second manager beside the one it names.<br>Caught by: [`hlHrPoolCreationRecordsTheCurrencyAndSoleManagerItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L153) |
| [9022](#hubregistry-9022) | consumeAuthorization also lets any ward spend a matured grant, so an authorization can be fired by an account other than the pool's installed policy.<br>Caught by: [`rvHrConsumeAuthorizationRefusesEveryCallerButTheInstalledPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L257) |
| [9023](#hubregistry-9023) | the asset keyed precision read no longer refuses an unknown asset, so an asset the registry never carried reads back as zero decimals.<br>Caught by: [`rvHrAssetIdPrecisionReadAnswersTheRowOrRefuses`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L292) |
| [9024](#hubregistry-9024) | the pool keyed precision read no longer refuses a pool that was never created, so such a pool reads back as zero decimals.<br>Caught by: [`rvHrPoolPrecisionReadAnswersItsCurrencyRowOrRefuses`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L307) |
| [9025](#hubregistry-9025) | updateManager refuses every revocation, so a manager seat once granted can never be taken back, the only one of a pool included.<br>Caught by: [`rcHrLivePoolLosesItsOnlyManagerIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L369) |
| [9026](#hubregistry-9026) | updateManager ignores a revocation of a held seat, so a manager the registry took back keeps managing the pool.<br>Caught by: [`hlHrRevokingTheOnlySeatLeavesALivePoolWithNoManager`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L166) |
| [9027](#hubregistry-9027) | the asset keyed precision read also refuses a registered asset of zero decimals, so a legal zero precision asset gets no answer.<br>Caught by: [`rvHrAssetIdPrecisionReadAnswersTheRowOrRefuses`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L292) |
| [9028](#hubregistry-9028) | the pool keyed precision read also refuses a live pool whose currency has zero decimals, so such a pool gets no answer.<br>Caught by: [`rvHrPoolPrecisionReadAnswersItsCurrencyRowOrRefuses`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L307) |
| [9037](#hubregistry-9037) | initiateAuthorization stamps maturity at the scheduling moment itself, so sentinels get no veto window before it matures.<br>Caught by: [`hlHrScheduledCallMaturesAfterExactlyThePolicyDelay`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L87) |
| [9038](#hubregistry-9038) | setBridgingHook announces the new hook but never records it, so a pool's bridging hook can never be attached or removed.<br>Caught by: [`rcHrSetBridgingHookAttachesIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L128) · [`rcHrSetBridgingHookDetachesIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L141) |
| [9153](#hubregistry-9153) | setHubRequestManager writes only when no manager is set, so a wired request manager can never be replaced.<br>Caught by: [`rcHuRegistryDirectRequestManagerRewireSendsNoSyncIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L982) |
| [9540](#hubregistry-9540) | setMetadata stores the written bytes without their first byte, so a pool reads back metadata one byte shorter than it was given.<br>Caught by: [`hlHrSetMetadataStoresTheBytesVerbatim`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L23) |
| [9541](#hubregistry-9541) | setMetadata writes the bytes under the next pool id, so one pool's metadata write rewrites a neighbouring pool's metadata.<br>Caught by: [`hlHrSetMetadataWritesOnlyItsPoolsMetadata`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L39) · [`hlHrSetMetadataStoresTheBytesVerbatim`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L23) |
| [9542](#hubregistry-9542) | setMetadata also clears the pool currency, so the pool it names reads as never created.<br>Caught by: [`hlHrSetMetadataWritesOnlyItsPoolsMetadata`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L39) |
| [9543](#hubregistry-9543) | updateCurrency also deletes the pool metadata, so changing a pool's currency erases its metadata.<br>Caught by: [`stHrOnlySetMetadataMovesMetadata`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L6) |
| [9544](#hubregistry-9544) | setMetadata stores zero bytes of the right length, so a pool reads back metadata with its content lost.<br>Caught by: [`hlHrSetMetadataStoresTheBytesVerbatim`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L23) |
| [9940](#hubregistry-9940) | The pool id packs the chain one bit too low, so the chain overlaps the local id and two different pools can share one id.<br>Caught by: [`hlHrPoolIdIsTheChainOverTheLocalId`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L179) |
| [9941](#hubregistry-9941) | The null pool test matches every id up to chain one's first pool, so the registry refuses to open that real pool.<br>Caught by: [`rvHrRegisterPoolAdmitsAUsableOpeningOfAChainedPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L271) |

## HubRegistry #1002

registerAsset drops the 18-decimal cap check, so an asset can register with arbitrary precision.

- **Mutant:** [`1002.sol`](1002.sol)
- **Caught by:** [`assetDecimalsCapped`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L26)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1002`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule assetDecimalsCapped`

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

## HubRegistry #1003

registerAsset stores the decimals but never sets the registered flag, leaving precision on an unregistered row.

- **Mutant:** [`1003.sol`](1003.sol)
- **Caught by:** [`unregisteredAssetHasZeroDecimals`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1003`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule unregisteredAssetHasZeroDecimals`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -51,7 +51,7 @@
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
 
-        asset[assetId] = AssetInfo(true, decimals_);
+        asset[assetId].decimals = decimals_; // MUTATION: registered flag never set
 
         emit NewAsset(assetId, decimals_);
     }
```

## HubRegistry #1004

registerAsset drops the empty-id check, so the null asset id can enter the registry.

- **Mutant:** [`1004.sol`](1004.sol)
- **Caught by:** [`nullAssetNeverRegistered`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1004`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule nullAssetNeverRegistered`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -45,7 +45,7 @@
 
     /// @inheritdoc IHubRegistry
     function registerAsset(AssetId assetId, uint8 decimals_) external auth {
-        require(!assetId.isNull(), EmptyAssetId());
+        // MUTATION: removed the empty-asset-id check
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
```

## HubRegistry #1005

registerPool no longer checks the pool currency is a registered asset, so a pool can be created denominated in an unknown asset.

- **Mutant:** [`1005.sol`](1005.sol)
- **Caught by:** [`poolCurrencyRegistered`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1005`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule poolCurrencyRegistered`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -61,7 +61,7 @@
         require(!poolId_.isNull(), InvalidPool());
         require(manager_ != address(0), EmptyAccount());
         require(!currency_.isNull(), EmptyCurrency());
-        require(isRegistered(currency_), AssetNotFound());
+        // MUTATION: removed the registered-currency check
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
         manager[poolId_][manager_] = true;
```

## HubRegistry #1006

updateManager drops the pool-existence check, so manager rights can be granted on a pool that was never created.

- **Mutant:** [`1006.sol`](1006.sol)
- **Caught by:** [`managerImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L46)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1006`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule managerImpliesPoolExists`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -76,7 +76,7 @@
 
     /// @inheritdoc IHubRegistry
     function updateManager(PoolId poolId_, address who, bool canManage) external auth {
-        require(exists(poolId_), NonExistingPool());
+        // MUTATION: removed the pool-existence check
         require(who != address(0), EmptyAccount());
 
         manager[poolId_][who] = canManage;
```

## HubRegistry #1007

updateManager drops the zero-address check, so the zero address can be granted manager rights.

- **Mutant:** [`1007.sol`](1007.sol)
- **Caught by:** [`zeroAddressNeverManager`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L51)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1007`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule zeroAddressNeverManager`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -77,7 +77,7 @@
     /// @inheritdoc IHubRegistry
     function updateManager(PoolId poolId_, address who, bool canManage) external auth {
         require(exists(poolId_), NonExistingPool());
-        require(who != address(0), EmptyAccount());
+        // MUTATION: removed the zero-address check
 
         manager[poolId_][who] = canManage;
 
```

## HubRegistry #1008

setPolicy drops the pool-existence check, so a policy installs and the nonce advances on a pool that was never created.

- **Mutant:** [`1008.sol`](1008.sol)
- **Caught by:** [`policyImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L56) · [`nonceImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L61)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1008`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule policyImpliesPoolExists nonceImpliesPoolExists`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -107,7 +107,7 @@
 
     /// @inheritdoc IHubRegistry
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
-        require(exists(poolId_), NonExistingPool());
+        // MUTATION: removed the pool-existence check
 
         _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
 
```

## HubRegistry #1009

setPolicy no longer advances the install nonce, so a predecessor's pending authorizations stay live and revive on reinstall.

- **Mutant:** [`1009.sol`](1009.sol)
- **Caught by:** [`policyImpliesNonzeroNonce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L66) · [`pendingUnderCurrentNonceMatchesPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L109)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1009`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule policyImpliesNonzeroNonce pendingUnderCurrentNonceMatchesPolicy`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce); // MUTATION: install nonce not advanced
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #1010

setBridgingHook drops the pool-existence check, so a bridging hook can be wired to a pool that was never created.

- **Mutant:** [`1010.sol`](1010.sol)
- **Caught by:** [`bridgingHookImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L71)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1010`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule bridgingHookImpliesPoolExists`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -125,7 +125,7 @@
 
     /// @inheritdoc IHubRegistry
     function setBridgingHook(PoolId poolId_, IBridgingHook hook_) external auth {
-        require(exists(poolId_), NonExistingPool());
+        // MUTATION: removed the pool-existence check
 
         bridgingHook[poolId_] = hook_;
         emit SetBridgingHook(poolId_, address(hook_));
```

## HubRegistry #1011

setHubRequestManager drops the pool-existence check, so a request manager can be wired to a pool that was never created.

- **Mutant:** [`1011.sol`](1011.sol)
- **Caught by:** [`requestManagerImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L76)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1011`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule requestManagerImpliesPoolExists`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -116,7 +116,7 @@
 
     /// @inheritdoc IHubRegistry
     function setHubRequestManager(PoolId poolId_, uint16 centrifugeId, IHubRequestManager manager_) external auth {
-        require(exists(poolId_), NonExistingPool());
+        // MUTATION: removed the pool-existence check
 
         hubRequestManager[poolId_][centrifugeId] = manager_;
 
```

## HubRegistry #1012

initiateAuthorization stores the relative delay instead of the absolute maturity timestamp, so a pending authorization can mature in the past.

- **Mutant:** [`1012.sol`](1012.sol)
- **Caught by:** [`pendingAuthAboveEnvFloor`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L81)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1012`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule pendingAuthAboveEnvFloor`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -148,7 +148,7 @@
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
         require(authorizedAfter[id] == 0, AlreadyAuthorized());
 
-        uint48 validAfter = uint48(block.timestamp) + delaySeconds;
+        uint48 validAfter = delaySeconds; // MUTATION: stores the relative delay, not the maturity time
         authorizedAfter[id] = validAfter;
         emit AuthorizationScheduled(poolId_, caller, id, validAfter, data);
     }
```

## HubRegistry #1013

initiateAuthorization keys the pending entry by the calling account instead of the installed policy, planting entries in foreign policy namespaces.

- **Mutant:** [`1013.sol`](1013.sol)
- **Caught by:** [`pendingNeverUnderNullPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L87) · [`pendingUnderCurrentNonceMatchesPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L109)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1013`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule pendingNeverUnderNullPolicy pendingUnderCurrentNonceMatchesPolicy`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -145,7 +145,7 @@
         require(delaySeconds != 0, InPolicy());
 
         // Reject re-authorizing: it would silently reset the maturity clock, so cancel first.
-        bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId_, caller, info.nonce, data); // MUTATION: keyed by the caller, not the installed policy
         require(authorizedAfter[id] == 0, AlreadyAuthorized());
 
         uint48 validAfter = uint48(block.timestamp) + delaySeconds;
```

## HubRegistry #1014

initiateAuthorization keys the pending entry one policy tenure behind, so the first policy's grants land under the reserved nonce zero.

- **Mutant:** [`1014.sol`](1014.sol)
- **Caught by:** [`pendingNeverUnderZeroNonce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L93)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1014`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule pendingNeverUnderZeroNonce`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -145,7 +145,7 @@
         require(delaySeconds != 0, InPolicy());
 
         // Reject re-authorizing: it would silently reset the maturity clock, so cancel first.
-        bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId_, address(info.policy), info.nonce - 1, data); // MUTATION: keyed one tenure behind
         require(authorizedAfter[id] == 0, AlreadyAuthorized());
 
         uint48 validAfter = uint48(block.timestamp) + delaySeconds;
```

## HubRegistry #1015

initiateAuthorization keys the pending entry one policy tenure ahead, so reinstalling the same policy inherits a pre-scheduled grant.

- **Mutant:** [`1015.sol`](1015.sol)
- **Caught by:** [`pendingNeverAheadOfNonce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L103)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1015`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule pendingNeverAheadOfNonce`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -145,7 +145,7 @@
         require(delaySeconds != 0, InPolicy());
 
         // Reject re-authorizing: it would silently reset the maturity clock, so cancel first.
-        bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId_, address(info.policy), info.nonce + 1, data); // MUTATION: keyed one tenure ahead
         require(authorizedAfter[id] == 0, AlreadyAuthorized());
 
         uint48 validAfter = uint48(block.timestamp) + delaySeconds;
```

## HubRegistry #1018

registerPool drops the zero-manager check, so a pool can be created with the zero address as its initial manager.

- **Mutant:** [`1018.sol`](1018.sol)
- **Caught by:** [`zeroAddressNeverManager`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L51)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1018`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule zeroAddressNeverManager`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -59,7 +59,7 @@
     /// @inheritdoc IHubRegistry
     function registerPool(PoolId poolId_, address manager_, AssetId currency_) external auth {
         require(!poolId_.isNull(), InvalidPool());
-        require(manager_ != address(0), EmptyAccount());
+        // MUTATION: removed the zero-manager check
         require(!currency_.isNull(), EmptyCurrency());
         require(isRegistered(currency_), AssetNotFound());
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
```

## HubRegistry #1023

registerPoolPair registers two pools under one manager in one call, so one call writes two pools' registry rows and rosters.

- **Mutant:** [`1023.sol`](1023.sol)
- **Caught by:** [`stHrPoolRowIsPerPool`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L7) · [`stHrManagerRightsArePerPool`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1023`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/multi_pool_properties.conf --rule stHrPoolRowIsPerPool stHrManagerRightsArePerPool`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -66,6 +66,23 @@
 
         manager[poolId_][manager_] = true;
         currency[poolId_] = currency_;
+
+        emit NewPool(poolId_, manager_, currency_);
+    }
+
+    /// @notice MUTATION: registers two pools under one manager in one call, writing both pools' rows.
+    function registerPoolPair(PoolId poolId_, PoolId siblingPoolId, address manager_, AssetId currency_)
+        external
+        auth
+    {
+        require(!poolId_.isNull() && !siblingPoolId.isNull(), InvalidPool());
+        require(manager_ != address(0), EmptyAccount());
+        require(isRegistered(currency_), AssetNotFound());
+
+        manager[poolId_][manager_] = true;
+        currency[poolId_] = currency_;
+        manager[siblingPoolId][manager_] = true;
+        currency[siblingPoolId] = currency_;
 
         emit NewPool(poolId_, manager_, currency_);
     }
```

## HubRegistry #1024

setHubRequestManagerFor wires one pool's request manager onto a sibling pool as well, so one call routes two pools' requests.

- **Mutant:** [`1024.sol`](1024.sol)
- **Caught by:** [`stHrRequestManagerIsPerPool`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L53)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1024`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/multi_pool_properties.conf --rule stHrRequestManagerIsPerPool`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -119,6 +119,21 @@
         require(exists(poolId_), NonExistingPool());
 
         hubRequestManager[poolId_][centrifugeId] = manager_;
+
+        emit SetHubRequestManager(poolId_, centrifugeId, manager_);
+    }
+
+    /// @notice MUTATION: wires one pool's request manager onto a sibling pool as well.
+    function setHubRequestManagerFor(
+        PoolId poolId_,
+        PoolId siblingPoolId,
+        uint16 centrifugeId,
+        IHubRequestManager manager_
+    ) external auth {
+        require(exists(poolId_), NonExistingPool());
+
+        hubRequestManager[poolId_][centrifugeId] = manager_;
+        hubRequestManager[siblingPoolId][centrifugeId] = manager_;
 
         emit SetHubRequestManager(poolId_, centrifugeId, manager_);
     }
```

## HubRegistry #1025

initiateAuthorizationPair schedules one authorization across two pools, so one call opens a timelock in both namespaces.

- **Mutant:** [`1025.sol`](1025.sol)
- **Caught by:** [`stHrPendingAuthIsPerPool`](../../specs/core/hub/HubRegistry/HubRegistry_multi_pool_properties.spec#L70)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1025`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/multi_pool_properties.conf --rule stHrPendingAuthIsPerPool`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -151,6 +151,23 @@
         uint48 validAfter = uint48(block.timestamp) + delaySeconds;
         authorizedAfter[id] = validAfter;
         emit AuthorizationScheduled(poolId_, caller, id, validAfter, data);
+    }
+
+    /// @notice MUTATION: schedules one authorization across two pools, writing both namespaces.
+    function initiateAuthorizationPair(PoolId poolId_, PoolId siblingPoolId, address caller, bytes calldata data)
+        external
+        auth
+    {
+        PolicyInfo memory info = _policy[poolId_];
+        PolicyInfo memory sibling = _policy[siblingPoolId];
+        require(address(info.policy) != address(0) && address(sibling.policy) != address(0), PolicyNotInstalled());
+
+        uint48 delaySeconds = info.policy.authorizationDelay(poolId_, caller, data);
+        require(delaySeconds != 0, InPolicy());
+
+        uint48 validAfter = uint48(block.timestamp) + delaySeconds;
+        authorizedAfter[_authId(poolId_, address(info.policy), info.nonce, data)] = validAfter;
+        authorizedAfter[_authId(siblingPoolId, address(sibling.policy), sibling.nonce, data)] = validAfter;
     }
 
     /// @inheritdoc IHubRegistry
```

## HubRegistry #1027

setPolicy installs a replacement without advancing the tenure, so reinstalling a policy later revives its old queued authorizations.

- **Mutant:** [`1027.sol`](1027.sol)
- **Caught by:** [`stHrPolicySwapOpensANewTenure`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L113)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1027`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrPolicySwapOpensANewTenure`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce); // MUTATION: the tenure does not advance
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #1028

initiateAuthorization stamps maturity at the scheduling moment itself, so a privileged action is ready the instant it is queued.

- **Mutant:** [`1028.sol`](1028.sol)
- **Caught by:** [`stHrSchedulingMaturesAheadAndInTheLiveTenure`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L145)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1028`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrSchedulingMaturesAheadAndInTheLiveTenure`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -148,7 +148,7 @@
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
         require(authorizedAfter[id] == 0, AlreadyAuthorized());
 
-        uint48 validAfter = uint48(block.timestamp) + delaySeconds;
+        uint48 validAfter = uint48(block.timestamp); // MUTATION: the delay is not applied
         authorizedAfter[id] = validAfter;
         emit AuthorizationScheduled(poolId_, caller, id, validAfter, data);
     }
```

## HubRegistry #1029

consuming an authorization also advances the pool's tenure, so discharging one action invalidates every other queued under the same policy.

- **Mutant:** [`1029.sol`](1029.sol)
- **Caught by:** [`stHrDischargeLeavesTheTenureStanding`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L165)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1029`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrDischargeLeavesTheTenureStanding`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -176,6 +176,8 @@
             Unauthorized()
         );
         delete authorizedAfter[id];
+        // MUTATION: the discharge moves the tenure with it
+        _policy[poolId_] = PolicyInfo(info.policy, info.nonce + 1);
         emit AuthorizationConsumed(poolId_, caller, id);
     }
 
```

## HubRegistry #1031

initiateAuthorization no longer rejects re-authorizing a live grant, so a second schedule silently resets the maturity clock in place.

- **Mutant:** [`1031.sol`](1031.sol)
- **Caught by:** [`stHrPendingMovesOnlyOffOrOntoZero`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L185)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1031`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrPendingMovesOnlyOffOrOntoZero`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -146,7 +146,7 @@
 
         // Reject re-authorizing: it would silently reset the maturity clock, so cancel first.
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
-        require(authorizedAfter[id] == 0, AlreadyAuthorized());
+        // MUTATION: removed the re-authorization guard
 
         uint48 validAfter = uint48(block.timestamp) + delaySeconds;
         authorizedAfter[id] = validAfter;
```

## HubRegistry #1032

registerAsset no longer rejects re-registering an asset at a different precision, so re-registering overwrites its decimals under holdings already priced against it.

- **Mutant:** [`1032.sol`](1032.sol)
- **Caught by:** [`stHrRegisteredAssetStaysAndASetPrecisionIsFinal`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L212) · [`stHrPoolCurrencySetPrecisionIsStable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L230)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1032`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrRegisteredAssetStaysAndASetPrecisionIsFinal stHrPoolCurrencySetPrecisionIsStable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -48,8 +48,7 @@
         require(!assetId.isNull(), EmptyAssetId());
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
-        AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        // MUTATION: removed the decimals-change guard on re-registration
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubRegistry #1033

updateCurrency no longer requires matching decimals, so swapping the currency changes the pool's unit precision.

- **Mutant:** [`1033.sol`](1033.sol)
- **Caught by:** [`stHrPoolCurrencySetPrecisionIsStable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L230)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1033`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrPoolCurrencySetPrecisionIsStable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -98,7 +98,7 @@
         require(exists(poolId_), NonExistingPool());
         require(!currency_.isNull(), EmptyCurrency());
         require(isRegistered(currency_), AssetNotFound());
-        require(asset[currency_].decimals == asset[currency[poolId_]].decimals, CurrencyDecimalsMismatch());
+        // MUTATION: removed the decimals-match check on re-denomination
 
         currency[poolId_] = currency_;
 
```

## HubRegistry #1034

updateCurrency clears the pool's currency instead of setting the new one, so a created pool silently becomes uncreated.

- **Mutant:** [`1034.sol`](1034.sol)
- **Caught by:** [`stHrCurrencyNeverClears`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L199)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1034`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrCurrencyNeverClears`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -100,7 +100,7 @@
         require(isRegistered(currency_), AssetNotFound());
         require(asset[currency_].decimals == asset[currency[poolId_]].decimals, CurrencyDecimalsMismatch());
 
-        currency[poolId_] = currency_;
+        currency[poolId_] = AssetId.wrap(0); // MUTATION: re-denomination clears the pool's currency
 
         emit UpdateCurrency(poolId_, currency_);
     }
```

## HubRegistry #1039

setPolicy rewinds the tenure nonce instead of advancing it, so the new policy can land on a namespace a past tenure already populated.

- **Mutant:** [`1039.sol`](1039.sol)
- **Caught by:** [`stHrNewTenureStartsWithNoSchedule`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L128)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1039`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrNewTenureStartsWithNoSchedule`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce - 1); // MUTATION: the tenure rewinds instead of advancing
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #1041

initiateAuthorization leaves the authorization id underived, so every scheduled grant is stamped under the zero id.

- **Mutant:** [`1041.sol`](1041.sol)
- **Caught by:** [`nullAuthIdNeverPending`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L118)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1041`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule nullAuthIdNeverPending`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -145,7 +145,7 @@
         require(delaySeconds != 0, InPolicy());
 
         // Reject re-authorizing: it would silently reset the maturity clock, so cancel first.
-        bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
+        bytes32 id; // MUTATION: the authorization id is left underived, so every grant lands on the zero id
         require(authorizedAfter[id] == 0, AlreadyAuthorized());
 
         uint48 validAfter = uint48(block.timestamp) + delaySeconds;
```

## HubRegistry #1042

setHubRequestManager no longer checks the pool exists, so a request manager can be wired to a pool never created.

- **Mutant:** [`1042.sol`](1042.sol)
- **Caught by:** [`requestManagerImpliesPoolExists`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_valid_state.spec#L76)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 1042`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_valid_state.conf --rule requestManagerImpliesPoolExists`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -116,7 +116,7 @@
 
     /// @inheritdoc IHubRegistry
     function setHubRequestManager(PoolId poolId_, uint16 centrifugeId, IHubRequestManager manager_) external auth {
-        require(exists(poolId_), NonExistingPool());
+        // MUTATION: the pool no longer has to exist
 
         hubRequestManager[poolId_][centrifugeId] = manager_;
 
```

## HubRegistry #4900

The shared ward gate no longer looks at the caller, so every registry write the hub reserves for its wards is open to any account.

- **Mutant:** [`4900.sol`](4900.sol)
- **Caught by:** [`acHrAssetRowMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L20) · [`acHrPoolCurrencyMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L40) · [`acHrManagerRightsMoveOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L57) · [`acHrPolicyRowMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L73) · [`acHrBridgingHookMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L93) · [`acHrRequestManagerMovesOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L109) · [`acHrAuthorizationIsScheduledOnlyByAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L126) · [`acHrPendingAuthorizationMovesOnlyForAWardOrThePolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L143)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4900`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_access_control.conf --rule acHrAssetRowMovesOnlyForAWard acHrPoolCurrencyMovesOnlyForAWard acHrManagerRightsMoveOnlyForAWard acHrPolicyRowMovesOnlyForAWard acHrBridgingHookMovesOnlyForAWard acHrRequestManagerMovesOnlyForAWard acHrAuthorizationIsScheduledOnlyByAWard acHrPendingAuthorizationMovesOnlyForAWardOrThePolicy`

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

## HubRegistry #4901

rely loses its ward gate, so any account can hand itself authority over the registry.

- **Mutant:** [`4901.sol`](4901.sol)
- **Caught by:** [`acHrWardRightsMoveOnlyForAWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4901`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_access_control.conf --rule acHrWardRightsMoveOnlyForAWard`

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

## HubRegistry #4902

Pool creation seats the calling ward as a manager alongside the account it names, so one call hands out two manager seats.

- **Mutant:** [`4902.sol`](4902.sol)
- **Caught by:** [`vtHrManagerRosterMovesOneAccountAtATime`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4902`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule vtHrManagerRosterMovesOneAccountAtATime`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -65,6 +65,7 @@
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
         manager[poolId_][manager_] = true;
+        manager[poolId_][msg.sender] = true; // MUTATION: the creating caller is seated alongside the named manager
         currency[poolId_] = currency_;
 
         emit NewPool(poolId_, manager_, currency_);
```

## HubRegistry #4903

Installing a policy advances the tenure counter by two, so the registry skips a namespace on every policy swap.

- **Mutant:** [`4903.sol`](4903.sol)
- **Caught by:** [`vtHrTenureCounterAdvancesByAtMostOne`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L25)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4903`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule vtHrTenureCounterAdvancesByAtMostOne`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 2); // MUTATION: the tenure counter advances by two
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #4904

Wiring a request manager on one network also wires the next network id, so one call reroutes two chains worth of hub requests.

- **Mutant:** [`4904.sol`](4904.sol)
- **Caught by:** [`vtHrRequestManagerMovesOneNetworkAtATime`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4904`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule vtHrRequestManagerMovesOneNetworkAtATime`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -119,6 +119,7 @@
         require(exists(poolId_), NonExistingPool());
 
         hubRequestManager[poolId_][centrifugeId] = manager_;
+        hubRequestManager[poolId_][centrifugeId + 1] = manager_; // MUTATION: the neighbouring network is rerouted alongside
 
         emit SetHubRequestManager(poolId_, centrifugeId, manager_);
     }
```

## HubRegistry #4905

Scheduling an authorization also stamps the same maturity into the next tenure namespace, so one call puts two entries on the timelock.

- **Mutant:** [`4905.sol`](4905.sol)
- **Caught by:** [`vtHrAuthLedgerMovesOneEntryAtATime`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L60)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4905`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule vtHrAuthLedgerMovesOneEntryAtATime`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -150,6 +150,7 @@
 
         uint48 validAfter = uint48(block.timestamp) + delaySeconds;
         authorizedAfter[id] = validAfter;
+        authorizedAfter[_authId(poolId_, address(info.policy), info.nonce + 1, data)] = validAfter; // MUTATION: the next tenure namespace is stamped alongside
         emit AuthorizationScheduled(poolId_, caller, id, validAfter, data);
     }
 
```

## HubRegistry #4906

consumeAuthorization no longer requires a scheduled entry, so an unscheduled call passes whenever the expiry reaches the current time.

- **Mutant:** [`4906.sol`](4906.sol)
- **Caught by:** [`hlHrAuthorizationIsSpentOnlyOnce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L6) · [`hlHrConsumeSpendsOnlyALiveEntry`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L22) · [`hlHrCanceledAuthorizationNeverFires`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L71)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4906`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrAuthorizationIsSpentOnlyOnce hlHrConsumeSpendsOnlyALiveEntry hlHrCanceledAuthorizationNeverFires`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -172,7 +172,7 @@
         // Matured and not yet expired: a stale auth fails closed, so it can't be fired much later (once
         // the baseline has drifted) with no fresh veto window.
         require(
-            validAfter != 0 && block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry,
+            block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry, // MUTATION: the liveness clause is gone
             Unauthorized()
         );
         delete authorizedAfter[id];
```

## HubRegistry #4907

consumeAuthorization admits a grant one second before it matures, so the veto window a sentinel was promised ends a second early.

- **Mutant:** [`4907.sol`](4907.sol)
- **Caught by:** [`hlHrConsumeWaitsOutTheVetoDelay`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4907`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrConsumeWaitsOutTheVetoDelay`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -172,7 +172,7 @@
         // Matured and not yet expired: a stale auth fails closed, so it can't be fired much later (once
         // the baseline has drifted) with no fresh veto window.
         require(
-            validAfter != 0 && block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry,
+            validAfter != 0 && block.timestamp + 1 >= validAfter && block.timestamp <= uint256(validAfter) + expiry, // MUTATION: maturity is admitted a second early
             Unauthorized()
         );
         delete authorizedAfter[id];
```

## HubRegistry #4908

consumeAuthorization admits a grant one second past the window the call names, so a stale grant still fires.

- **Mutant:** [`4908.sol`](4908.sol)
- **Caught by:** [`hlHrConsumeRefusesAStaleGrant`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4908`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrConsumeRefusesAStaleGrant`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -172,7 +172,7 @@
         // Matured and not yet expired: a stale auth fails closed, so it can't be fired much later (once
         // the baseline has drifted) with no fresh veto window.
         require(
-            validAfter != 0 && block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry,
+            validAfter != 0 && block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry + 1, // MUTATION: the window closes a second late
             Unauthorized()
         );
         delete authorizedAfter[id];
```

## HubRegistry #4909

Installing a policy also stamps a timelock entry, so the authorization ledger changes outside schedule, cancel and consume.

- **Mutant:** [`4909.sol`](4909.sol)
- **Caught by:** [`vtHrAuthLedgerMovesOnlyThroughItsThreeWriters`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L79)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4909`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule vtHrAuthLedgerMovesOnlyThroughItsThreeWriters`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -110,6 +110,7 @@
         require(exists(poolId_), NonExistingPool());
 
         _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        authorizedAfter[bytes32(uint256(uint160(address(policy_))))] = uint48(block.timestamp); // MUTATION: the install stamps the timelock
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #4910

Wiring a bridging hook also seats that hook as a pool manager, so manager rights move through a writer that never grants them.

- **Mutant:** [`4910.sol`](4910.sol)
- **Caught by:** [`vtHrManagerRightsMoveOnlyThroughTheirTwoWriters`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L95)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4910`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule vtHrManagerRightsMoveOnlyThroughTheirTwoWriters`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -128,6 +128,7 @@
         require(exists(poolId_), NonExistingPool());
 
         bridgingHook[poolId_] = hook_;
+        manager[poolId_][address(hook_)] = true; // MUTATION: wiring the hook also seats it as a pool manager
         emit SetBridgingHook(poolId_, address(hook_));
     }
 
```

## HubRegistry #4912

Pool creation no longer seats the account it names, so a pool is born with no manager at all.

- **Mutant:** [`4912.sol`](4912.sol)
- **Caught by:** [`hlHrPoolCreationSeatsTheAccountItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L105)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4912`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrPoolCreationSeatsTheAccountItNames`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -64,7 +64,7 @@
         require(isRegistered(currency_), AssetNotFound());
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
-        manager[poolId_][manager_] = true;
+        // MUTATION: pool creation no longer seats the manager it names
         currency[poolId_] = currency_;
 
         emit NewPool(poolId_, manager_, currency_);
```

## HubRegistry #4913

The token standard precision read answers the eighteen decimal registration cap instead of the precision the registry recorded.

- **Mutant:** [`4913.sol`](4913.sol)
- **Caught by:** [`hlHrTokenPrecisionMatchesTheAssetRow`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L116)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4913`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrTokenPrecisionMatchesTheAssetRow`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -235,7 +235,7 @@
     function decimals(uint256 asset_) external view returns (uint8 decimals_) {
         AssetInfo memory info = asset[AssetId.wrap(asset_.toUint128())];
         require(info.registered, AssetNotFound());
-        decimals_ = info.decimals;
+        decimals_ = MAX_DECIMALS; // MUTATION: the read answers the registration cap, not the asset's own precision
     }
 
     /// @inheritdoc IHubRegistry
```

## HubRegistry #4914

registerAsset applies its precision cap one decimal too tight, so an eighteen decimal asset can never be registered.

- **Mutant:** [`4914.sol`](4914.sol)
- **Caught by:** [`rvHrRegisterAssetIsNeverRefusedToAWardOnAFreshAssetWithinTheCap`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L237) · [`rvHrRegisterAssetIsNeverRefusedToAWardFillingOrKeepingARegisteredPrecision`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L341)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4914`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrRegisterAssetIsNeverRefusedToAWardOnAFreshAssetWithinTheCap rvHrRegisterAssetIsNeverRefusedToAWardFillingOrKeepingARegisteredPrecision`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -46,7 +46,7 @@
     /// @inheritdoc IHubRegistry
     function registerAsset(AssetId assetId, uint8 decimals_) external auth {
         require(!assetId.isNull(), EmptyAssetId());
-        require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
+        require(decimals_ < MAX_DECIMALS, TooManyDecimals()); // MUTATION: the cap refuses the asset that sits exactly on it
 
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
```

## HubRegistry #4915

registerPool no longer checks its currency is a registered asset, so a pool can be created on an unknown asset.

- **Mutant:** [`4915.sol`](4915.sol)
- **Caught by:** [`rvHrRegisterPoolRefusesAnUnusableOrRepeatedOpening`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4915`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrRegisterPoolRefusesAnUnusableOrRepeatedOpening`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -61,7 +61,7 @@
         require(!poolId_.isNull(), InvalidPool());
         require(manager_ != address(0), EmptyAccount());
         require(!currency_.isNull(), EmptyCurrency());
-        require(isRegistered(currency_), AssetNotFound());
+        // MUTATION: the currency no longer has to be a registered asset
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
         manager[poolId_][manager_] = true;
```

## HubRegistry #4916

updateManager no longer refuses the zero address, so a manager seat can be handed to nobody.

- **Mutant:** [`4916.sol`](4916.sol)
- **Caught by:** [`rvHrUpdateManagerRefusesANonWardAnAbsentPoolOrANullSeat`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L25)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4916`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrUpdateManagerRefusesANonWardAnAbsentPoolOrANullSeat`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -77,7 +77,7 @@
     /// @inheritdoc IHubRegistry
     function updateManager(PoolId poolId_, address who, bool canManage) external auth {
         require(exists(poolId_), NonExistingPool());
-        require(who != address(0), EmptyAccount());
+        // MUTATION: the zero account is no longer refused a manager seat
 
         manager[poolId_][who] = canManage;
 
```

## HubRegistry #4917

updateCurrency no longer checks the incoming currency accounts in the same precision, so a pool can be redenominated across scales.

- **Mutant:** [`4917.sol`](4917.sol)
- **Caught by:** [`rvHrUpdateCurrencyRefusesANonWardAnAbsentPoolOrARescaling`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4917`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrUpdateCurrencyRefusesANonWardAnAbsentPoolOrARescaling`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -98,7 +98,7 @@
         require(exists(poolId_), NonExistingPool());
         require(!currency_.isNull(), EmptyCurrency());
         require(isRegistered(currency_), AssetNotFound());
-        require(asset[currency_].decimals == asset[currency[poolId_]].decimals, CurrencyDecimalsMismatch());
+        // MUTATION: the precision of the incoming currency no longer has to match
 
         currency[poolId_] = currency_;
 
```

## HubRegistry #4918

Installing a policy no longer bumps its nonce, so reinstalling the same policy leaves its earlier grants consumable.

- **Mutant:** [`4918.sol`](4918.sol)
- **Caught by:** [`rvHrRetiredGrantIsNeverConsumed`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L195)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4918`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrRetiredGrantIsNeverConsumed`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce); // MUTATION: the install leaves the tenure counter standing
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #4919

setHubRequestManager no longer checks the pool exists, so hub requests can be routed for a pool that was never created.

- **Mutant:** [`4919.sol`](4919.sol)
- **Caught by:** [`rvHrSetHubRequestManagerRefusesANonWardOrAnAbsentPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L77)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4919`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrSetHubRequestManagerRefusesANonWardOrAnAbsentPool`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -116,7 +116,7 @@
 
     /// @inheritdoc IHubRegistry
     function setHubRequestManager(PoolId poolId_, uint16 centrifugeId, IHubRequestManager manager_) external auth {
-        require(exists(poolId_), NonExistingPool());
+        // MUTATION: the pool no longer has to exist
 
         hubRequestManager[poolId_][centrifugeId] = manager_;
 
```

## HubRegistry #4920

setBridgingHook refuses the zero address, so a pool can never unwire the hook that sits on its cross chain share movements.

- **Mutant:** [`4920.sol`](4920.sol)
- **Caught by:** [`rvHrSetBridgingHookIsNeverRefusedToAWardOnALivePool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L93)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4920`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrSetBridgingHookIsNeverRefusedToAWardOnALivePool`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -126,6 +126,7 @@
     /// @inheritdoc IHubRegistry
     function setBridgingHook(PoolId poolId_, IBridgingHook hook_) external auth {
         require(exists(poolId_), NonExistingPool());
+        require(address(hook_) != address(0), EmptyAccount()); // MUTATION: the zero hook can no longer unwire the pool
 
         bridgingHook[poolId_] = hook_;
         emit SetBridgingHook(poolId_, address(hook_));
```

## HubRegistry #4921

initiateAuthorization no longer refuses a call that needs no delay, so it records a grant that matures instantly.

- **Mutant:** [`4921.sol`](4921.sol)
- **Caught by:** [`rvHrInitiateAuthorizationRefusesANonWardAnInPolicyCallOrATakenSlot`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L109)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4921`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrInitiateAuthorizationRefusesANonWardAnInPolicyCallOrATakenSlot`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -142,7 +142,7 @@
 
         // Only an out-of-policy call may be authorized: an in-policy call would mature instantly.
         uint48 delaySeconds = info.policy.authorizationDelay(poolId_, caller, data);
-        require(delaySeconds != 0, InPolicy());
+        // MUTATION: an in policy call is scheduled like any other
 
         // Reject re-authorizing: it would silently reset the maturity clock, so cancel first.
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
```

## HubRegistry #4922

cancelAuthorization no longer checks a grant is standing, so a veto of nothing succeeds and writes a misleading audit entry.

- **Mutant:** [`4922.sol`](4922.sol)
- **Caught by:** [`rvHrCancelAuthorizationRefusesANonWardOrAnEmptySlot`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4922`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrCancelAuthorizationRefusesANonWardOrAnEmptySlot`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -157,7 +157,7 @@
     function cancelAuthorization(PoolId poolId_, address caller, bytes calldata data) external auth {
         bytes32 id = authId(poolId_, data);
         // Revert on a no-op cancel rather than writing a misleading audit entry.
-        require(authorizedAfter[id] != 0, Unauthorized());
+        // MUTATION: a cancel of nothing is accepted
         delete authorizedAfter[id];
         emit AuthorizationCanceled(poolId_, caller, id);
     }
```

## HubRegistry #4923

consumeAuthorization refuses a grant at the very instant it matures, so the first second of the window is lost.

- **Mutant:** [`4923.sol`](4923.sol)
- **Caught by:** [`rvHrConsumeAuthorizationIsNeverRefusedToThePolicyInsideItsWindow`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L147)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4923`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrConsumeAuthorizationIsNeverRefusedToThePolicyInsideItsWindow`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -172,7 +172,7 @@
         // Matured and not yet expired: a stale auth fails closed, so it can't be fired much later (once
         // the baseline has drifted) with no fresh veto window.
         require(
-            validAfter != 0 && block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry,
+            validAfter != 0 && block.timestamp > validAfter && block.timestamp <= uint256(validAfter) + expiry, // MUTATION: the maturity instant itself is refused
             Unauthorized()
         );
         delete authorizedAfter[id];
```

## HubRegistry #4924

decimals no longer checks the asset is registered, so an unknown asset reads back as zero decimals.

- **Mutant:** [`4924.sol`](4924.sol)
- **Caught by:** [`rvHrTokenDecimalsRefusesAnAssetTheRegistryDoesNotCarry`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L170)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4924`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrTokenDecimalsRefusesAnAssetTheRegistryDoesNotCarry`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -234,7 +234,7 @@
     /// @inheritdoc IERC6909Decimals
     function decimals(uint256 asset_) external view returns (uint8 decimals_) {
         AssetInfo memory info = asset[AssetId.wrap(asset_.toUint128())];
-        require(info.registered, AssetNotFound());
+        // MUTATION: an unregistered asset is answered instead of refused
         decimals_ = info.decimals;
     }
 
```

## HubRegistry #4925

authId refuses a pool that runs no policy, so a sentinel cannot compute the identifier of the grant it means to veto.

- **Mutant:** [`4925.sol`](4925.sol)
- **Caught by:** [`rvHrAuthIdAlwaysAnswers`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L183)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4925`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrAuthIdAlwaysAnswers`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -190,6 +190,7 @@
     ///      resurrect authorizations matured under its earlier tenure.
     function authId(PoolId poolId_, bytes calldata data) public view returns (bytes32) {
         PolicyInfo memory info = _policy[poolId_];
+        require(address(info.policy) != address(0), PolicyNotInstalled()); // MUTATION: the id read refuses a pool with no policy installed
         return _authId(poolId_, address(info.policy), info.nonce, data);
     }
 
```

## HubRegistry #4928

the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.

- **Mutant:** [`4928.sol`](4928.sol)
- **Caught by:** [`rvHrRelyRefusesANonWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L211) · [`rvHrDenyRefusesANonWard`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L224) · [`rvHrRegisterAssetRefusesANonWardAnOversizedPrecisionOrARescale`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L322) · [`rvHrSetBridgingHookRefusesANonWardOrAnAbsentPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L378)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 4928`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrRelyRefusesANonWard rvHrDenyRefusesANonWard rvHrRegisterAssetRefusesANonWardAnOversizedPrecisionOrARescale rvHrSetBridgingHookRefusesANonWardOrAnAbsentPool`

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

## HubRegistry #6400

registerAsset records one decimal more than declared, so every asset is registered at the wrong precision.

- **Mutant:** [`6400.sol`](6400.sol)
- **Caught by:** [`rcHrRegisterAssetIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L4) · [`rcHrRegisterAssetAtThePrecisionCapIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L19) · [`rcHrRegisterAssetWithZeroPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L34) · [`rcHrRegisterAssetFillsAnUnsetPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L385) · [`rcHrRegisterAssetRepeatsAtItsOwnPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L399)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6400`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrRegisterAssetIsReachable rcHrRegisterAssetAtThePrecisionCapIsReachable rcHrRegisterAssetWithZeroPrecisionIsReachable rcHrRegisterAssetFillsAnUnsetPrecisionIsReachable rcHrRegisterAssetRepeatsAtItsOwnPrecisionIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -51,7 +51,7 @@
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
 
-        asset[assetId] = AssetInfo(true, decimals_);
+        asset[assetId] = AssetInfo(true, decimals_ + 1); // MUTATION: the row records one decimal more than the caller declares
 
         emit NewAsset(assetId, decimals_);
     }
```

## HubRegistry #6401

registerAsset writes the asset's precision but leaves the row unregistered, so an asset never actually joins the registry.

- **Mutant:** [`6401.sol`](6401.sol)
- **Caught by:** [`rcHrRegisterAssetIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6401`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrRegisterAssetIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -51,7 +51,7 @@
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
 
-        asset[assetId] = AssetInfo(true, decimals_);
+        asset[assetId] = AssetInfo(false, decimals_); // MUTATION: the row is written but never marked registered
 
         emit NewAsset(assetId, decimals_);
     }
```

## HubRegistry #6402

registerPool records the currency but never seats the named manager, so a new pool starts with no manager.

- **Mutant:** [`6402.sol`](6402.sol)
- **Caught by:** [`rcHrRegisterPoolIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L48) · [`rcHrRegisterAssetThenRegisterPoolIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L67)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6402`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrRegisterPoolIsReachable rcHrRegisterAssetThenRegisterPoolIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -64,7 +64,7 @@
         require(isRegistered(currency_), AssetNotFound());
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
-        manager[poolId_][manager_] = true;
+        // MUTATION: pool creation no longer seats the manager it names
         currency[poolId_] = currency_;
 
         emit NewPool(poolId_, manager_, currency_);
```

## HubRegistry #6403

Pool creation seats the manager it names but never records the denomination, so the pool never comes into existence.

- **Mutant:** [`6403.sol`](6403.sol)
- **Caught by:** [`rcHrRegisterPoolIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L48)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6403`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrRegisterPoolIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -65,7 +65,7 @@
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
         manager[poolId_][manager_] = true;
-        currency[poolId_] = currency_;
+        // MUTATION: pool creation never records the pool's denomination
 
         emit NewPool(poolId_, manager_, currency_);
     }
```

## HubRegistry #6404

updateManager reads the flag it is handed backwards, so seating an account revokes it and revoking an account seats it.

- **Mutant:** [`6404.sol`](6404.sol)
- **Caught by:** [`rcHrUpdateManagerSeatsAManagerIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L86) · [`rcHrUpdateManagerRevokesASeatIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L99)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6404`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrUpdateManagerSeatsAManagerIsReachable rcHrUpdateManagerRevokesASeatIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -79,7 +79,7 @@
         require(exists(poolId_), NonExistingPool());
         require(who != address(0), EmptyAccount());
 
-        manager[poolId_][who] = canManage;
+        manager[poolId_][who] = !canManage; // MUTATION: the seating flag is read backwards
 
         emit UpdateManager(poolId_, who, canManage);
     }
```

## HubRegistry #6405

updateCurrency accepts only the denomination the pool already carries, so a live pool can never be redenominated onto another asset.

- **Mutant:** [`6405.sol`](6405.sol)
- **Caught by:** [`rcHrUpdateCurrencyRedenominatesThePoolIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L112)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6405`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrUpdateCurrencyRedenominatesThePoolIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -98,7 +98,7 @@
         require(exists(poolId_), NonExistingPool());
         require(!currency_.isNull(), EmptyCurrency());
         require(isRegistered(currency_), AssetNotFound());
-        require(asset[currency_].decimals == asset[currency[poolId_]].decimals, CurrencyDecimalsMismatch());
+        require(currency_ == currency[poolId_], CurrencyDecimalsMismatch()); // MUTATION: only the denomination already installed is accepted
 
         currency[poolId_] = currency_;
 
```

## HubRegistry #6406

setBridgingHook turns away the zero address, so an attached bridging hook can never be taken off again.

- **Mutant:** [`6406.sol`](6406.sol)
- **Caught by:** [`rcHrSetBridgingHookDetachesIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L141)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6406`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrSetBridgingHookDetachesIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -126,6 +126,7 @@
     /// @inheritdoc IHubRegistry
     function setBridgingHook(PoolId poolId_, IBridgingHook hook_) external auth {
         require(exists(poolId_), NonExistingPool());
+        require(address(hook_) != address(0), EmptyAccount()); // MUTATION: the zero hook is refused
 
         bridgingHook[poolId_] = hook_;
         emit SetBridgingHook(poolId_, address(hook_));
```

## HubRegistry #6408

setHubRequestManager wires the neighbouring network instead of the one it is handed, so the network the pool named is never routed.

- **Mutant:** [`6408.sol`](6408.sol)
- **Caught by:** [`rcHrSetHubRequestManagerWiresANetworkIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L155)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6408`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrSetHubRequestManagerWiresANetworkIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -118,7 +118,7 @@
     function setHubRequestManager(PoolId poolId_, uint16 centrifugeId, IHubRequestManager manager_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        hubRequestManager[poolId_][centrifugeId] = manager_;
+        hubRequestManager[poolId_][centrifugeId + 1] = manager_; // MUTATION: the neighbouring network is wired instead
 
         emit SetHubRequestManager(poolId_, centrifugeId, manager_);
     }
```

## HubRegistry #6409

setPolicy refuses a pool with no policy yet, so a pool's first policy can never be installed.

- **Mutant:** [`6409.sol`](6409.sol)
- **Caught by:** [`rcHrSetPolicyInstallsTheFirstPolicyIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L171)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6409`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrSetPolicyInstallsTheFirstPolicyIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -108,6 +108,7 @@
     /// @inheritdoc IHubRegistry
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
+        require(address(_policy[poolId_].policy) != address(0), PolicyNotInstalled()); // MUTATION: a pool with no policy yet is refused
 
         _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
 
```

## HubRegistry #6410

setPolicy turns away the zero address, so an installed policy can never be uninstalled.

- **Mutant:** [`6410.sol`](6410.sol)
- **Caught by:** [`rcHrSetPolicyUninstallsWithTheZeroAddressIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L187)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6410`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrSetPolicyUninstallsWithTheZeroAddressIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -108,6 +108,7 @@
     /// @inheritdoc IHubRegistry
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
+        require(address(policy_) != address(0), EmptyAccount()); // MUTATION: the zero policy is refused
 
         _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
 
```

## HubRegistry #6411

Installing a policy leaves the tenure counter standing, so no install ever opens a new namespace.

- **Mutant:** [`6411.sol`](6411.sol)
- **Caught by:** [`rcHrSetPolicyAtTheLastNamespaceIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L204) · [`rcHrPolicyViewsReportTheInstallIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L334)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6411`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrSetPolicyAtTheLastNamespaceIsReachable rcHrPolicyViewsReportTheInstallIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce); // MUTATION: the install leaves the tenure counter standing
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #6412

setPolicy checks the pool and announces the install but records nothing, so the pool keeps the policy and the tenure it already had.

- **Mutant:** [`6412.sol`](6412.sol)
- **Caught by:** [`rcHrOrphanedScheduleCanBeRemadeAfterAPolicySwapIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L218) · [`rcHrAuthIdChangesAcrossAPolicySwapIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L354)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6412`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrOrphanedScheduleCanBeRemadeAfterAPolicySwapIsReachable rcHrAuthIdChangesAcrossAPolicySwapIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        // MUTATION: the install records neither the policy nor a new tenure
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #6413

initiateAuthorization stamps maturity at the scheduling moment itself, so a scheduled call is ready the instant it is queued.

- **Mutant:** [`6413.sol`](6413.sol)
- **Caught by:** [`rcHrInitiateAuthorizationAtTheMaturityCeilingIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L241)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6413`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrInitiateAuthorizationAtTheMaturityCeilingIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -148,7 +148,7 @@
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
         require(authorizedAfter[id] == 0, AlreadyAuthorized());
 
-        uint48 validAfter = uint48(block.timestamp) + delaySeconds;
+        uint48 validAfter = uint48(block.timestamp); // MUTATION: the delay is not applied
         authorizedAfter[id] = validAfter;
         emit AuthorizationScheduled(poolId_, caller, id, validAfter, data);
     }
```

## HubRegistry #6414

initiateAuthorization refuses an empty payload, so the shortest schedulable call can never be put on the clock.

- **Mutant:** [`6414.sol`](6414.sol)
- **Caught by:** [`rcHuPrivilegedCallSchedulingIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L183) · [`rcHuScheduledCallWithdrawalIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L203)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6414`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuPrivilegedCallSchedulingIsReachable rcHuScheduledCallWithdrawalIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -139,6 +139,7 @@
     function initiateAuthorization(PoolId poolId_, address caller, bytes calldata data) external auth {
         PolicyInfo memory info = _policy[poolId_];
         require(address(info.policy) != address(0), PolicyNotInstalled());
+        require(data.length != 0, Unauthorized()); // MUTATION: an empty payload is refused
 
         // Only an out-of-policy call may be authorized: an in-policy call would mature instantly.
         uint48 delaySeconds = info.policy.authorizationDelay(poolId_, caller, data);
```

## HubRegistry #6415

cancelAuthorization refuses a grant that has not matured yet, so the veto window the delay exists for can never be used.

- **Mutant:** [`6415.sol`](6415.sol)
- **Caught by:** [`rcHrCancelAuthorizationIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L260)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6415`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrCancelAuthorizationIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -157,7 +157,7 @@
     function cancelAuthorization(PoolId poolId_, address caller, bytes calldata data) external auth {
         bytes32 id = authId(poolId_, data);
         // Revert on a no-op cancel rather than writing a misleading audit entry.
-        require(authorizedAfter[id] != 0, Unauthorized());
+        require(authorizedAfter[id] != 0 && block.timestamp >= authorizedAfter[id], Unauthorized()); // MUTATION: an unmatured grant is refused
         delete authorizedAfter[id];
         emit AuthorizationCanceled(poolId_, caller, id);
     }
```

## HubRegistry #6416

consumeAuthorization turns away the pool's own policy and answers every other caller, so the policy can never discharge a grant it scheduled.

- **Mutant:** [`6416.sol`](6416.sol)
- **Caught by:** [`rvHrConsumeAuthorizationIsNeverRefusedToThePolicyInsideItsWindow`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L147) · [`rvHrConsumeAuthorizationRefusesEveryCallerButTheInstalledPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L257)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6416`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrConsumeAuthorizationIsNeverRefusedToThePolicyInsideItsWindow rvHrConsumeAuthorizationRefusesEveryCallerButTheInstalledPolicy`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -165,7 +165,7 @@
     /// @inheritdoc IHubRegistry
     function consumeAuthorization(PoolId poolId_, address caller, bytes calldata data, uint48 expiry) external {
         PolicyInfo memory info = _policy[poolId_];
-        require(msg.sender == address(info.policy), CallerNotPolicy());
+        require(msg.sender != address(info.policy), CallerNotPolicy()); // MUTATION: the pool's own policy is the one caller turned away
 
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
         uint48 validAfter = authorizedAfter[id];
```

## HubRegistry #6417

consumeAuthorization reads its maturity check backwards, so a grant can fire before its veto delay ends but never after.

- **Mutant:** [`6417.sol`](6417.sol)
- **Caught by:** [`hlHrConsumeWaitsOutTheVetoDelay`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6417`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrConsumeWaitsOutTheVetoDelay`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -172,7 +172,7 @@
         // Matured and not yet expired: a stale auth fails closed, so it can't be fired much later (once
         // the baseline has drifted) with no fresh veto window.
         require(
-            validAfter != 0 && block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry,
+            validAfter != 0 && block.timestamp <= validAfter && block.timestamp <= uint256(validAfter) + expiry, // MUTATION: the maturity comparison is reversed
             Unauthorized()
         );
         delete authorizedAfter[id];
```

## HubRegistry #6418

consumeAuthorization refuses a grant at the very instant it matures, so the opening second of the window is lost.

- **Mutant:** [`6418.sol`](6418.sol)
- **Caught by:** [`rcHrConsumeAuthorizationAtTheMaturityInstantIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L277)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6418`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrConsumeAuthorizationAtTheMaturityInstantIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -172,7 +172,7 @@
         // Matured and not yet expired: a stale auth fails closed, so it can't be fired much later (once
         // the baseline has drifted) with no fresh veto window.
         require(
-            validAfter != 0 && block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry,
+            validAfter != 0 && block.timestamp > validAfter && block.timestamp <= uint256(validAfter) + expiry, // MUTATION: the maturity instant itself is refused
             Unauthorized()
         );
         delete authorizedAfter[id];
```

## HubRegistry #6419

consumeAuthorization shuts the window a second early, so a grant can never be fired at the last instant the policy allows.

- **Mutant:** [`6419.sol`](6419.sol)
- **Caught by:** [`rcHrConsumeAuthorizationAtTheExpiryEdgeIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L296)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6419`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrConsumeAuthorizationAtTheExpiryEdgeIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -172,7 +172,7 @@
         // Matured and not yet expired: a stale auth fails closed, so it can't be fired much later (once
         // the baseline has drifted) with no fresh veto window.
         require(
-            validAfter != 0 && block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry,
+            validAfter != 0 && block.timestamp >= validAfter && block.timestamp < uint256(validAfter) + expiry, // MUTATION: the window shuts a second early
             Unauthorized()
         );
         delete authorizedAfter[id];
```

## HubRegistry #6420

rely clears the ward slot instead of setting it, so authority can never be handed to an account that holds none.

- **Mutant:** [`6420.sol`](6420.sol)
- **Caught by:** [`rcHrAuthorityRoundTripIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L316)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6420`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrAuthorityRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -23,7 +23,7 @@
 
     /// @inheritdoc IAuth
     function rely(address user) public auth {
-        wards[user] = 1;
+        wards[user] = 0; // MUTATION: the grant clears the ward instead of setting it
         emit Rely(user);
     }
 
```

## HubRegistry #6421

deny sets the ward slot instead of clearing it, so authority can never be taken back from an account that holds it.

- **Mutant:** [`6421.sol`](6421.sol)
- **Caught by:** [`rcHrAuthorityRoundTripIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L316)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6421`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrAuthorityRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        wards[user] = 1; // MUTATION: the revocation sets the ward instead of clearing it
         emit Deny(user);
     }
 }
```

## HubRegistry #6422

setPolicy records the caller instead of the policy it was handed, so the pool is governed by whoever configured it.

- **Mutant:** [`6422.sol`](6422.sol)
- **Caught by:** [`rcHrPolicyViewsReportTheInstallIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L334)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6422`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrPolicyViewsReportTheInstallIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(IHubPolicy(msg.sender), _policy[poolId_].nonce + 1); // MUTATION: the install records the caller rather than the policy it was handed
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #6423

setPolicy bumps the tenure counter but writes the sitting rule book back, so a pool never leaves the policy it is already running under.

- **Mutant:** [`6423.sol`](6423.sol)
- **Caught by:** [`hlHrSetPolicyInstallsExactlyTheAddressItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 6423`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrSetPolicyInstallsExactlyTheAddressItNames`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(_policy[poolId_].policy, _policy[poolId_].nonce + 1); // MUTATION: the sitting policy is written back
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #8410

registerAsset lets a set precision grow on re-registration, so an asset or a pool currency priced at six decimals can be moved to eight.

- **Mutant:** [`8410.sol`](8410.sol)
- **Caught by:** [`stHrRegisteredAssetStaysAndASetPrecisionIsFinal`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L212) · [`stHrPoolCurrencySetPrecisionIsStable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L230)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8410`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrRegisteredAssetStaysAndASetPrecisionIsFinal stHrPoolCurrencySetPrecisionIsStable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -49,7 +49,7 @@
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        require(!current.registered || current.decimals == 0 || current.decimals <= decimals_, CannotChangeDecimals()); // MUTATION: a set precision may be raised
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubRegistry #8411

registerAsset lets any registered asset be rescaled to eighteen decimals, so a set precision is moved without a revert.

- **Mutant:** [`8411.sol`](8411.sol)
- **Caught by:** [`rvHrRegisterAssetRefusesANonWardAnOversizedPrecisionOrARescale`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L322)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8411`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrRegisterAssetRefusesANonWardAnOversizedPrecisionOrARescale`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -49,7 +49,7 @@
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        require(!current.registered || current.decimals == 0 || current.decimals == decimals_ || decimals_ == MAX_DECIMALS, CannotChangeDecimals()); // MUTATION: a rescale to the cap passes the guard
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubRegistry #8412

registerAsset no longer lets an unset precision be filled, so an asset registered at zero decimals keeps them for good.

- **Mutant:** [`8412.sol`](8412.sol)
- **Caught by:** [`rcHrRegisterAssetFillsAnUnsetPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L385)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8412`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrRegisterAssetFillsAnUnsetPrecisionIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -49,7 +49,7 @@
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        require(!current.registered || current.decimals == decimals_, CannotChangeDecimals()); // MUTATION: a stored zero may no longer be replaced
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubRegistry #8413

registerAsset refuses a ward who fills an unset precision, so a zero precision read off an uninitialized token can never be corrected.

- **Mutant:** [`8413.sol`](8413.sol)
- **Caught by:** [`rvHrRegisterAssetIsNeverRefusedToAWardFillingOrKeepingARegisteredPrecision`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L341)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8413`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrRegisterAssetIsNeverRefusedToAWardFillingOrKeepingARegisteredPrecision`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -49,7 +49,7 @@
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        require(!current.registered || current.decimals == decimals_, CannotChangeDecimals()); // MUTATION: a stored zero may no longer be replaced
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubRegistry #8414

registerAsset refuses a repeat at the stored nonzero precision, so an idempotent re-registration reverts.

- **Mutant:** [`8414.sol`](8414.sol)
- **Caught by:** [`rcHrRegisterAssetRepeatsAtItsOwnPrecisionIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L399)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8414`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrRegisterAssetRepeatsAtItsOwnPrecisionIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -49,7 +49,7 @@
         require(decimals_ <= MAX_DECIMALS, TooManyDecimals());
 
         AssetInfo memory current = asset[assetId];
-        require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
+        require(!current.registered || current.decimals == 0, CannotChangeDecimals()); // MUTATION: only a stored zero may be re-registered
 
         asset[assetId] = AssetInfo(true, decimals_);
 
```

## HubRegistry #8620

setPolicy keeps the old tenure when the same policy is reinstalled, so grants meant to be voided stay spendable.

- **Mutant:** [`8620.sol`](8620.sol)
- **Caught by:** [`hlHrSetPolicyInstallsExactlyTheAddressItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8620`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrSetPolicyInstallsExactlyTheAddressItNames`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(policy_, address(policy_) == address(_policy[poolId_].policy) ? _policy[poolId_].nonce : _policy[poolId_].nonce + 1); // MUTATION: a same address reinstall keeps the old tenure
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #8621

consumeAuthorization no longer deletes the grant it spends, so one veto window funds the same privileged call again and again.

- **Mutant:** [`8621.sol`](8621.sol)
- **Caught by:** [`hlHrAuthorizationIsSpentOnlyOnce`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8621`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrAuthorizationIsSpentOnlyOnce`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -175,7 +175,7 @@
             validAfter != 0 && block.timestamp >= validAfter && block.timestamp <= uint256(validAfter) + expiry,
             Unauthorized()
         );
-        delete authorizedAfter[id];
+        // MUTATION: a consumed grant is no longer deleted
         emit AuthorizationConsumed(poolId_, caller, id);
     }
 
```

## HubRegistry #8622

cancelAuthorization no longer deletes the grant it vetoes, so a canceled call still matures and can be fired.

- **Mutant:** [`8622.sol`](8622.sol)
- **Caught by:** [`hlHrCanceledAuthorizationNeverFires`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L71)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8622`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrCanceledAuthorizationNeverFires`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -158,7 +158,7 @@
         bytes32 id = authId(poolId_, data);
         // Revert on a no-op cancel rather than writing a misleading audit entry.
         require(authorizedAfter[id] != 0, Unauthorized());
-        delete authorizedAfter[id];
+        // MUTATION: a canceled grant is no longer deleted
         emit AuthorizationCanceled(poolId_, caller, id);
     }
 
```

## HubRegistry #8623

consumeAuthorization looks grants up one tenure back, so a grant voided by a reinstall can be spent and a current one never.

- **Mutant:** [`8623.sol`](8623.sol)
- **Caught by:** [`hlHrConsumeSpendsOnlyALiveEntry`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8623`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrConsumeSpendsOnlyALiveEntry`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -167,7 +167,7 @@
         PolicyInfo memory info = _policy[poolId_];
         require(msg.sender == address(info.policy), CallerNotPolicy());
 
-        bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId_, address(info.policy), info.nonce - 1, data); // MUTATION: consume looks up the previous tenure
         uint48 validAfter = authorizedAfter[id];
         // Matured and not yet expired: a stale auth fails closed, so it can't be fired much later (once
         // the baseline has drifted) with no fresh veto window.
```

## HubRegistry #8625

setPolicy keeps the tenure when the same policy is reinstalled, so grants scheduled before the reinstall stay spendable.

- **Mutant:** [`8625.sol`](8625.sol)
- **Caught by:** [`rvHrRetiredGrantIsNeverConsumed`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L195)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8625`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrRetiredGrantIsNeverConsumed`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -109,7 +109,7 @@
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
+        _policy[poolId_] = PolicyInfo(policy_, address(policy_) == address(_policy[poolId_].policy) ? _policy[poolId_].nonce : _policy[poolId_].nonce + 1); // MUTATION: a same address reinstall keeps the old tenure
 
         emit SetPolicy(poolId_, policy_);
     }
```

## HubRegistry #8805

cancelAuthorization refuses a grant once it has matured, so a ward can no longer veto a matured call the policy has not yet fired.

- **Mutant:** [`8805.sol`](8805.sol)
- **Caught by:** [`rvHrCancelAuthorizationIsNeverRefusedToAWardWithAPendingGrant`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L361)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8805`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrCancelAuthorizationIsNeverRefusedToAWardWithAPendingGrant`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -157,7 +157,7 @@
     function cancelAuthorization(PoolId poolId_, address caller, bytes calldata data) external auth {
         bytes32 id = authId(poolId_, data);
         // Revert on a no-op cancel rather than writing a misleading audit entry.
-        require(authorizedAfter[id] != 0, Unauthorized());
+        require(authorizedAfter[id] != 0 && authorizedAfter[id] > block.timestamp, Unauthorized()); // MUTATION: a matured grant can no longer be canceled
         delete authorizedAfter[id];
         emit AuthorizationCanceled(poolId_, caller, id);
     }
```

## HubRegistry #8806

setBridgingHook checks the pool exists only when attaching a hook, so a hook can be cleared on a pool that was never created.

- **Mutant:** [`8806.sol`](8806.sol)
- **Caught by:** [`rvHrSetBridgingHookRefusesANonWardOrAnAbsentPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L378)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8806`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrSetBridgingHookRefusesANonWardOrAnAbsentPool`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -125,7 +125,7 @@
 
     /// @inheritdoc IHubRegistry
     function setBridgingHook(PoolId poolId_, IBridgingHook hook_) external auth {
-        require(exists(poolId_), NonExistingPool());
+        if (address(hook_) != address(0)) require(exists(poolId_), NonExistingPool()); // MUTATION: clearing skips the pool check
 
         bridgingHook[poolId_] = hook_;
         emit SetBridgingHook(poolId_, address(hook_));
```

## HubRegistry #8807

registerPool installs the named manager as the pool policy, so a new pool opens its first policy tenure at creation.

- **Mutant:** [`8807.sol`](8807.sol)
- **Caught by:** [`hlHrPoolCreationLeavesThePoolWithoutAPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L193)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8807`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrPoolCreationLeavesThePoolWithoutAPolicy`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -66,6 +66,7 @@
 
         manager[poolId_][manager_] = true;
         currency[poolId_] = currency_;
+        _policy[poolId_] = PolicyInfo(IHubPolicy(manager_), 1); // MUTATION: creation installs a policy
 
         emit NewPool(poolId_, manager_, currency_);
     }
```

## HubRegistry #8809

registerPool fills a zero precision of the currency it names with eighteen decimals, so pool creation changes an asset's precision.

- **Mutant:** [`8809.sol`](8809.sol)
- **Caught by:** [`stHrRegisteredAssetStaysAndASetPrecisionIsFinal`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L212)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8809`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrRegisteredAssetStaysAndASetPrecisionIsFinal`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -66,6 +66,7 @@
 
         manager[poolId_][manager_] = true;
         currency[poolId_] = currency_;
+        if (asset[currency_].decimals == 0) asset[currency_].decimals = MAX_DECIMALS; // MUTATION: pool creation writes a precision
 
         emit NewPool(poolId_, manager_, currency_);
     }
```

## HubRegistry #8810

updateCurrency skips the decimals match when the sitting currency has zero decimals, so a currency swap moves the pool precision off zero.

- **Mutant:** [`8810.sol`](8810.sol)
- **Caught by:** [`stHrPoolCurrencySetPrecisionIsStable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_transitions.spec#L230)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8810`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_transitions.conf --rule stHrPoolCurrencySetPrecisionIsStable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -98,7 +98,7 @@
         require(exists(poolId_), NonExistingPool());
         require(!currency_.isNull(), EmptyCurrency());
         require(isRegistered(currency_), AssetNotFound());
-        require(asset[currency_].decimals == asset[currency[poolId_]].decimals, CurrencyDecimalsMismatch());
+        require(asset[currency[poolId_]].decimals == 0 || asset[currency_].decimals == asset[currency[poolId_]].decimals, CurrencyDecimalsMismatch()); // MUTATION: a zero precision currency swaps freely
 
         currency[poolId_] = currency_;
 
```

## HubRegistry #8950

setPolicy no longer checks that the pool exists, so a policy and a tenure can be installed on a pool that was never created.

- **Mutant:** [`8950.sol`](8950.sol)
- **Caught by:** [`rvHrSetPolicyRefusesANonWardOrAnAbsentPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L62)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 8950`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrSetPolicyRefusesANonWardOrAnAbsentPool`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -107,7 +107,7 @@
 
     /// @inheritdoc IHubRegistry
     function setPolicy(PoolId poolId_, IHubPolicy policy_) external auth {
-        require(exists(poolId_), NonExistingPool());
+        // MUTATION: the install no longer checks that the pool was ever created
 
         _policy[poolId_] = PolicyInfo(policy_, _policy[poolId_].nonce + 1);
 
```

## HubRegistry #9020

registerAsset stores the 18 decimal cap instead of the precision it was given, so an asset reads back a precision it was never registered with.

- **Mutant:** [`9020.sol`](9020.sol)
- **Caught by:** [`hlHrAssetRegistrationRecordsThePrecisionItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L142)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9020`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrAssetRegistrationRecordsThePrecisionItNames`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -51,7 +51,7 @@
         AssetInfo memory current = asset[assetId];
         require(!current.registered || current.decimals == 0 || current.decimals == decimals_, CannotChangeDecimals());
 
-        asset[assetId] = AssetInfo(true, decimals_);
+        asset[assetId] = AssetInfo(true, MAX_DECIMALS); // MUTATION: the cap is recorded instead of the precision named
 
         emit NewAsset(assetId, decimals_);
     }
```

## HubRegistry #9021

registerPool also seats the ward that opens the pool, so a new pool starts with a second manager beside the one it names.

- **Mutant:** [`9021.sol`](9021.sol)
- **Caught by:** [`hlHrPoolCreationRecordsTheCurrencyAndSoleManagerItNames`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L153)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9021`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrPoolCreationRecordsTheCurrencyAndSoleManagerItNames`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -64,7 +64,7 @@
         require(isRegistered(currency_), AssetNotFound());
         require(currency[poolId_].isNull(), PoolAlreadyRegistered());
 
-        manager[poolId_][manager_] = true;
+        manager[poolId_][manager_] = true; manager[poolId_][msg.sender] = true; // MUTATION: the opening ward is seated too
         currency[poolId_] = currency_;
 
         emit NewPool(poolId_, manager_, currency_);
```

## HubRegistry #9022

consumeAuthorization also lets any ward spend a matured grant, so an authorization can be fired by an account other than the pool's installed policy.

- **Mutant:** [`9022.sol`](9022.sol)
- **Caught by:** [`rvHrConsumeAuthorizationRefusesEveryCallerButTheInstalledPolicy`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L257)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9022`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrConsumeAuthorizationRefusesEveryCallerButTheInstalledPolicy`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -165,7 +165,7 @@
     /// @inheritdoc IHubRegistry
     function consumeAuthorization(PoolId poolId_, address caller, bytes calldata data, uint48 expiry) external {
         PolicyInfo memory info = _policy[poolId_];
-        require(msg.sender == address(info.policy), CallerNotPolicy());
+        require(msg.sender == address(info.policy) || wards[msg.sender] == 1, CallerNotPolicy()); // MUTATION: a ward may consume too
 
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
         uint48 validAfter = authorizedAfter[id];
```

## HubRegistry #9023

the asset keyed precision read no longer refuses an unknown asset, so an asset the registry never carried reads back as zero decimals.

- **Mutant:** [`9023.sol`](9023.sol)
- **Caught by:** [`rvHrAssetIdPrecisionReadAnswersTheRowOrRefuses`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L292)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9023`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrAssetIdPrecisionReadAnswersTheRowOrRefuses`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -220,7 +220,7 @@
     /// @inheritdoc IHubRegistry
     function decimals(AssetId assetId) public view returns (uint8 decimals_) {
         AssetInfo memory info = asset[assetId];
-        require(info.registered, AssetNotFound());
+        // MUTATION: the asset keyed read no longer refuses an unregistered asset
         decimals_ = info.decimals;
     }
 
```

## HubRegistry #9024

the pool keyed precision read no longer refuses a pool that was never created, so such a pool reads back as zero decimals.

- **Mutant:** [`9024.sol`](9024.sol)
- **Caught by:** [`rvHrPoolPrecisionReadAnswersItsCurrencyRowOrRefuses`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L307)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9024`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrPoolPrecisionReadAnswersItsCurrencyRowOrRefuses`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -227,7 +227,7 @@
     /// @inheritdoc IHubRegistry
     function decimals(PoolId poolId_) public view returns (uint8 decimals_) {
         AssetInfo memory info = asset[currency[poolId_]];
-        require(info.registered, AssetNotFound());
+        // MUTATION: the pool keyed read no longer refuses a pool whose currency is not registered
         decimals_ = info.decimals;
     }
 
```

## HubRegistry #9025

updateManager refuses every revocation, so a manager seat once granted can never be taken back, the only one of a pool included.

- **Mutant:** [`9025.sol`](9025.sol)
- **Caught by:** [`rcHrLivePoolLosesItsOnlyManagerIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L369)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9025`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrLivePoolLosesItsOnlyManagerIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -77,7 +77,7 @@
     /// @inheritdoc IHubRegistry
     function updateManager(PoolId poolId_, address who, bool canManage) external auth {
         require(exists(poolId_), NonExistingPool());
-        require(who != address(0), EmptyAccount());
+        require(who != address(0) && canManage, EmptyAccount()); // MUTATION: a revocation is refused
 
         manager[poolId_][who] = canManage;
 
```

## HubRegistry #9026

updateManager ignores a revocation of a held seat, so a manager the registry took back keeps managing the pool.

- **Mutant:** [`9026.sol`](9026.sol)
- **Caught by:** [`hlHrRevokingTheOnlySeatLeavesALivePoolWithNoManager`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L166)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9026`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrRevokingTheOnlySeatLeavesALivePoolWithNoManager`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -79,7 +79,7 @@
         require(exists(poolId_), NonExistingPool());
         require(who != address(0), EmptyAccount());
 
-        manager[poolId_][who] = canManage;
+        manager[poolId_][who] = canManage || manager[poolId_][who]; // MUTATION: a held seat survives its revocation
 
         emit UpdateManager(poolId_, who, canManage);
     }
```

## HubRegistry #9027

the asset keyed precision read also refuses a registered asset of zero decimals, so a legal zero precision asset gets no answer.

- **Mutant:** [`9027.sol`](9027.sol)
- **Caught by:** [`rvHrAssetIdPrecisionReadAnswersTheRowOrRefuses`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L292)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9027`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrAssetIdPrecisionReadAnswersTheRowOrRefuses`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -220,7 +220,7 @@
     /// @inheritdoc IHubRegistry
     function decimals(AssetId assetId) public view returns (uint8 decimals_) {
         AssetInfo memory info = asset[assetId];
-        require(info.registered, AssetNotFound());
+        require(info.registered && info.decimals != 0, AssetNotFound()); // MUTATION: a registered zero precision asset is refused
         decimals_ = info.decimals;
     }
 
```

## HubRegistry #9028

the pool keyed precision read also refuses a live pool whose currency has zero decimals, so such a pool gets no answer.

- **Mutant:** [`9028.sol`](9028.sol)
- **Caught by:** [`rvHrPoolPrecisionReadAnswersItsCurrencyRowOrRefuses`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L307)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9028`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrPoolPrecisionReadAnswersItsCurrencyRowOrRefuses`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -227,7 +227,7 @@
     /// @inheritdoc IHubRegistry
     function decimals(PoolId poolId_) public view returns (uint8 decimals_) {
         AssetInfo memory info = asset[currency[poolId_]];
-        require(info.registered, AssetNotFound());
+        require(info.registered && info.decimals != 0, AssetNotFound()); // MUTATION: a live pool with a zero precision currency is refused
         decimals_ = info.decimals;
     }
 
```

## HubRegistry #9037

initiateAuthorization stamps maturity at the scheduling moment itself, so sentinels get no veto window before it matures.

- **Mutant:** [`9037.sol`](9037.sol)
- **Caught by:** [`hlHrScheduledCallMaturesAfterExactlyThePolicyDelay`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L87)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9037`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrScheduledCallMaturesAfterExactlyThePolicyDelay`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -148,7 +148,7 @@
         bytes32 id = _authId(poolId_, address(info.policy), info.nonce, data);
         require(authorizedAfter[id] == 0, AlreadyAuthorized());
 
-        uint48 validAfter = uint48(block.timestamp) + delaySeconds;
+        uint48 validAfter = uint48(block.timestamp); // MUTATION: the policy delay is not applied
         authorizedAfter[id] = validAfter;
         emit AuthorizationScheduled(poolId_, caller, id, validAfter, data);
     }
```

## HubRegistry #9038

setBridgingHook announces the new hook but never records it, so a pool's bridging hook can never be attached or removed.

- **Mutant:** [`9038.sol`](9038.sol)
- **Caught by:** [`rcHrSetBridgingHookAttachesIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L128) · [`rcHrSetBridgingHookDetachesIsReachable`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reachability.spec#L141)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9038`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reachability.conf --rule rcHrSetBridgingHookAttachesIsReachable rcHrSetBridgingHookDetachesIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -127,7 +127,7 @@
     function setBridgingHook(PoolId poolId_, IBridgingHook hook_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        bridgingHook[poolId_] = hook_;
+        // MUTATION: the handed hook is never recorded, only the event is emitted
         emit SetBridgingHook(poolId_, address(hook_));
     }
 
```

## HubRegistry #9153

setHubRequestManager writes only when no manager is set, so a wired request manager can never be replaced.

- **Mutant:** [`9153.sol`](9153.sol)
- **Caught by:** [`rcHuRegistryDirectRequestManagerRewireSendsNoSyncIsReachable`](../../specs/core/hub/Hub_LinkedHubCore/single/Hub_LinkedHubCore_reachability.spec#L982)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9153`
- **Run on clean src:** `certoraRun certora/confs/core/hub/Hub_LinkedHubCore/reachability.conf --rule rcHuRegistryDirectRequestManagerRewireSendsNoSyncIsReachable`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -118,7 +118,7 @@
     function setHubRequestManager(PoolId poolId_, uint16 centrifugeId, IHubRequestManager manager_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        hubRequestManager[poolId_][centrifugeId] = manager_;
+        if (address(hubRequestManager[poolId_][centrifugeId]) == address(0)) hubRequestManager[poolId_][centrifugeId] = manager_; // MUTATION: a wired request manager can no longer be replaced
 
         emit SetHubRequestManager(poolId_, centrifugeId, manager_);
     }
```

## HubRegistry #9540

setMetadata stores the written bytes without their first byte, so a pool reads back metadata one byte shorter than it was given.

- **Mutant:** [`9540.sol`](9540.sol)
- **Caught by:** [`hlHrSetMetadataStoresTheBytesVerbatim`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9540`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/metadata_properties.conf --rule hlHrSetMetadataStoresTheBytesVerbatim`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -88,7 +88,7 @@
     function setMetadata(PoolId poolId_, bytes calldata metadata_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        metadata[poolId_] = metadata_;
+        metadata[poolId_] = metadata_[1:]; // MUTATION: the first byte is dropped
 
         emit SetMetadata(poolId_, metadata_);
     }
```

## HubRegistry #9541

setMetadata writes the bytes under the next pool id, so one pool's metadata write rewrites a neighbouring pool's metadata.

- **Mutant:** [`9541.sol`](9541.sol)
- **Caught by:** [`hlHrSetMetadataWritesOnlyItsPoolsMetadata`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L39) · [`hlHrSetMetadataStoresTheBytesVerbatim`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9541`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/metadata_properties.conf --rule hlHrSetMetadataWritesOnlyItsPoolsMetadata hlHrSetMetadataStoresTheBytesVerbatim`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -88,7 +88,7 @@
     function setMetadata(PoolId poolId_, bytes calldata metadata_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        metadata[poolId_] = metadata_;
+        metadata[PoolId.wrap(poolId_.raw() + 1)] = metadata_; // MUTATION: the neighbouring pool is written
 
         emit SetMetadata(poolId_, metadata_);
     }
```

## HubRegistry #9542

setMetadata also clears the pool currency, so the pool it names reads as never created.

- **Mutant:** [`9542.sol`](9542.sol)
- **Caught by:** [`hlHrSetMetadataWritesOnlyItsPoolsMetadata`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L39)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9542`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/metadata_properties.conf --rule hlHrSetMetadataWritesOnlyItsPoolsMetadata`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -88,7 +88,7 @@
     function setMetadata(PoolId poolId_, bytes calldata metadata_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        metadata[poolId_] = metadata_;
+        metadata[poolId_] = metadata_; currency[poolId_] = AssetId.wrap(0); // MUTATION: the currency is cleared too
 
         emit SetMetadata(poolId_, metadata_);
     }
```

## HubRegistry #9543

updateCurrency also deletes the pool metadata, so changing a pool's currency erases its metadata.

- **Mutant:** [`9543.sol`](9543.sol)
- **Caught by:** [`stHrOnlySetMetadataMovesMetadata`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9543`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/metadata_properties.conf --rule stHrOnlySetMetadataMovesMetadata`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -100,7 +100,7 @@
         require(isRegistered(currency_), AssetNotFound());
         require(asset[currency_].decimals == asset[currency[poolId_]].decimals, CurrencyDecimalsMismatch());
 
-        currency[poolId_] = currency_;
+        currency[poolId_] = currency_; delete metadata[poolId_]; // MUTATION: the metadata is erased too
 
         emit UpdateCurrency(poolId_, currency_);
     }
```

## HubRegistry #9544

setMetadata stores zero bytes of the right length, so a pool reads back metadata with its content lost.

- **Mutant:** [`9544.sol`](9544.sol)
- **Caught by:** [`hlHrSetMetadataStoresTheBytesVerbatim`](../../specs/core/hub/HubRegistry/HubRegistry_metadata_properties.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9544`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/metadata_properties.conf --rule hlHrSetMetadataStoresTheBytesVerbatim`

```diff
--- a/src/core/hub/HubRegistry.sol
+++ b/src/core/hub/HubRegistry.sol
@@ -88,7 +88,7 @@
     function setMetadata(PoolId poolId_, bytes calldata metadata_) external auth {
         require(exists(poolId_), NonExistingPool());
 
-        metadata[poolId_] = metadata_;
+        metadata[poolId_] = new bytes(metadata_.length); // MUTATION: the length is kept and the content zeroed
 
         emit SetMetadata(poolId_, metadata_);
     }
```

## HubRegistry #9940

The pool id packs the chain one bit too low, so the chain overlaps the local id and two different pools can share one id.

- **Mutant:** [`9940.sol`](9940.sol)
- **Caught by:** [`hlHrPoolIdIsTheChainOverTheLocalId`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_high_level.spec#L179)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9940`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_high_level.conf --rule hlHrPoolIdIsTheChainOverTheLocalId`

```diff
--- a/src/core/types/PoolId.sol
+++ b/src/core/types/PoolId.sol
@@ -8,7 +8,7 @@
 }
 
 function newPoolId(uint16 centrifugeId_, uint48 localPoolId) pure returns (PoolId) {
-    return PoolId.wrap((uint64(centrifugeId_) << 48) | uint64(localPoolId));
+    return PoolId.wrap((uint64(centrifugeId_) << 47) | uint64(localPoolId)); // MUTATION: the chain is shifted by 47 bits instead of 48
 }
 
 function isNull(PoolId poolId) pure returns (bool) {
```

## HubRegistry #9941

The null pool test matches every id up to chain one's first pool, so the registry refuses to open that real pool.

- **Mutant:** [`9941.sol`](9941.sol)
- **Caught by:** [`rvHrRegisterPoolAdmitsAUsableOpeningOfAChainedPool`](../../specs/core/hub/HubRegistry/single/HubRegistry_single_pool_reverts.spec#L271)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh HubRegistry 9941`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubRegistry/single_pool_reverts.conf --rule rvHrRegisterPoolAdmitsAUsableOpeningOfAChainedPool`

```diff
--- a/src/core/types/PoolId.sol
+++ b/src/core/types/PoolId.sol
@@ -12,7 +12,7 @@
 }
 
 function isNull(PoolId poolId) pure returns (bool) {
-    return PoolId.unwrap(poolId) == 0;
+    return PoolId.unwrap(poolId) <= 2 ** 48; // MUTATION: every id up to the first pool of chain one reads as null
 }
 
 function isEqual(PoolId a, PoolId b) pure returns (bool) {
```

