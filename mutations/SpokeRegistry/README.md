# Mutations for `SpokeRegistry` (`src/core/spoke/SpokeRegistry.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/types/AssetId.sol`, `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [1202](#spokeregistry-1202) | addPool stamps the pool one second ahead of the current block time, so the creation record points at a future moment.<br>Caught by: [`poolCreatedAtNotFuture`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L47) |
| [1203](#spokeregistry-1203) | addPool records the block number instead of the block timestamp, so the creation stamp can sit far below any real chain time.<br>Caught by: [`poolCreatedAboveEnvFloor`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L52) |
| [1204](#spokeregistry-1204) | _linkToken stores the share token but never stores the registrar, leaving the class with a token and no registrar.<br>Caught by: [`shareTokenIffRegistrar`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L57) |
| [1205](#spokeregistry-1205) | addShareClass no longer checks the pool exists, so a share class can be created on a pool that was never added.<br>Caught by: [`shareClassImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L62) |
| [1207](#spokeregistry-1207) | relinking clears only the pool half of the outgoing token's lookup row, leaving its class half behind without a pool reference.<br>Caught by: [`tokenRowScIdImpliesPoolId`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L67) |
| [1208](#spokeregistry-1208) | _linkToken registers the share token without writing its reverse lookup row, so the token no longer resolves back to its pool and class.<br>Caught by: [`shareTokenHasCanonicalReverseRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L72) |
| [1209](#spokeregistry-1209) | replacing a share token leaves the outgoing token's lookup row in place, so a stale token still claims the pool and class.<br>Caught by: [`onlyCurrentShareTokenHoldsALookupRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L81) |
| [1210](#spokeregistry-1210) | _linkToken drops the deployed-contract check, so an address without code, even zero, can be linked as a share token.<br>Caught by: [`nullTokenRowPoolIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L89) · [`shareTokenIffRegistrar`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L57) · [`onlyADeployedContractOwnsATokenRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L278) |
| [1211](#spokeregistry-1211) | setRequestManager skips the pool existence check, so a request manager can be installed on a pool that was never added.<br>Caught by: [`requestManagerImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L94) |
| [1212](#spokeregistry-1212) | updateManager skips the pool existence check, so manager rights can be granted on a pool that was never added.<br>Caught by: [`managerImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L99) |
| [1213](#spokeregistry-1213) | updateBridger skips the pool existence check, so bridger rights can be granted on a pool that was never added.<br>Caught by: [`bridgerImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L104) |
| [1214](#spokeregistry-1214) | setPolicy installs the policy without advancing the install nonce, so the first installed policy carries a zero nonce.<br>Caught by: [`policyImpliesNonzeroNonce`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L109) |
| [1215](#spokeregistry-1215) | setPolicy skips the pool existence check, so a policy nonce starts moving on a pool that was never added.<br>Caught by: [`policyNonceImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L114) |
| [1216](#spokeregistry-1216) | authorize leaves the authorization id underived, so every grant is counted under the zero id.<br>Caught by: [`nullAuthIdRowEmpty`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L119) |
| [1217](#spokeregistry-1217) | authorize drops the policy-installed check, so authorizations can be granted on a pool where no policy was ever set.<br>Caught by: [`noPolicyEverMeansNoAuthorizations`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L125) |
| [1218](#spokeregistry-1218) | createAssetId records the forward asset row but never writes the reverse lookup, so the new id does not resolve back to itself.<br>Caught by: [`assetForwardResolvesBack`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L133) |
| [1219](#spokeregistry-1219) | createAssetId writes the reverse lookup but never records the forward asset row, so the filed id points at an empty registry entry.<br>Caught by: [`assetReverseResolvesBack`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L142) |
| [1220](#spokeregistry-1220) | createAssetId no longer advances the asset counter, so an issued id falls outside the range the counter has covered.<br>Caught by: [`registeredAssetIdWellFormed`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L154) |
| [1221](#spokeregistry-1221) | createAssetId accepts the zero asset address, registering an id whose registry row has no asset behind it.<br>Caught by: [`unregisteredAssetRowEmpty`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L163) · [`nullAssetNeverRegistered`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L168) |
| [1222](#spokeregistry-1222) | updatePricePoolPerShare drops the share class existence check, so a share price is stored for a class that does not exist.<br>Caught by: [`sharePriceStampImpliesShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L173) · [`sharePriceValueImpliesShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L178) |
| [1223](#spokeregistry-1223) | updatePricePoolPerAsset drops the share class existence check, so an asset price is stored for a class that does not exist.<br>Caught by: [`assetPriceStampImpliesShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L183) · [`assetPriceValueImpliesShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L188) |
| [1224](#spokeregistry-1224) | updatePricePoolPerAsset drops the asset registration check, so a price is stored for an asset id the registry does not know.<br>Caught by: [`assetPriceStampImpliesRegisteredAsset`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L193) · [`assetPriceValueImpliesRegisteredAsset`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L198) |
| [1225](#spokeregistry-1225) | linkVault drops the registered-vault check, so a vault that was never registered can be marked linked.<br>Caught by: [`linkedVaultIsRegistered`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L203) |
| [1226](#spokeregistry-1226) | registerVault skips the asset pair cross-check, so a vault row can record a zero or mismatched asset for its asset id.<br>Caught by: [`unregisteredVaultPoolIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L208) · [`unregisteredVaultScIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L213) · [`unregisteredVaultAssetIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L218) · [`unregisteredVaultTokenIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L223) |
| [1227](#spokeregistry-1227) | registerVault validates only the asset address and no longer the token id, so the stored vault row can disagree with the asset registry.<br>Caught by: [`registeredVaultMatchesAssetRegistry`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L228) |
| [1228](#spokeregistry-1228) | registerVault drops the share class existence check, so a vault can be registered outside the live share class.<br>Caught by: [`registeredVaultSitsOnALiveShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L240) |
| [1229](#spokeregistry-1229) | registerVault drops the deployed-contract check, so the zero address can be registered as a vault.<br>Caught by: [`nullVaultNeverRegistered`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L249) · [`onlyADeployedContractHoldsAVaultRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L293) |
| [1230](#spokeregistry-1230) | _linkToken keys the reverse row by the old token, not the new one, so a first link fills the null address row.<br>Caught by: [`nullTokenRowPoolIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L89) |
| [1231](#spokeregistry-1231) | registerVault records only the share class of the vault row, so a row with no asset carries a live class id.<br>Caught by: [`unregisteredVaultScIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L213) |
| [1232](#spokeregistry-1232) | registerVault stores the vault already linked, so registration by itself puts it into service.<br>Caught by: [`stSrRegisteredVaultStartsUnlinked`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L150) |
| [1235](#spokeregistry-1235) | setPolicy installs a replacement without advancing the install counter, so authorizations granted under the outgoing policy stay reachable.<br>Caught by: [`stSrPolicySwapAdvancesTheInstallCounter`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L164) |
| [1236](#spokeregistry-1236) | authorize files the grant under the install counter before the current one, so a grant lands in a retired policy tenure.<br>Caught by: [`stSrGrantsLandOnlyOnTheInstalledPolicy`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L179) |
| [1237](#spokeregistry-1237) | createAssetId mints the id before advancing the counter, so the first registered asset gets number zero.<br>Caught by: [`registeredAssetIdWellFormed`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L154) |
| [1238](#spokeregistry-1238) | A share price update no longer refuses an older stamp, so a stale cross-chain price can overwrite a fresher one.<br>Caught by: [`stSrPriceStampsNeverRewind`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L198) |
| [1240](#spokeregistry-1240) | An asset price update no longer refuses an older stamp.<br>Caught by: [`stSrPriceStampsNeverRewind`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L198) |
| [1247](#spokeregistry-1247) | A grant files two authorizations at once.<br>Caught by: [`stSrAuthorizationLedgerStepsByOneInTheStandingNamespace`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L211) |
| [1248](#spokeregistry-1248) | A revocation is keyed to the previous tenure, so it strikes a retired row instead of the standing one.<br>Caught by: [`stSrAuthorizationLedgerStepsByOneInTheStandingNamespace`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L211) |
| [1251](#spokeregistry-1251) | A registered vault can be registered again, so a live vault is re-pointed to another row.<br>Caught by: [`stSrRegisteredVaultKeepsItsIdentity`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L228) |
| [1252](#spokeregistry-1252) | A pool can be added again, so its entry stamp is rewritten.<br>Caught by: [`stSrPoolEntryStampIsWrittenOnce`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L244) |
| [1258](#spokeregistry-1258) | authorize files the grant one policy nonce ahead, so the installed policy cannot spend it until a later reinstall.<br>Caught by: [`noAuthorizationsAheadOfTenure`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L263) |
| [1259](#spokeregistry-1259) | authorize files the grant under the calling ward instead of the installed policy, so that policy cannot spend it.<br>Caught by: [`currentTenureAuthorizationsCarryTheInstalledPolicy`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L269) |
| [1260](#spokeregistry-1260) | authorize files the grant under nonce 0 instead of the installed one, so no installed policy can ever spend it.<br>Caught by: [`noAuthorizationsUnderZeroNonce`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L254) |
| [4500](#spokeregistry-4500) | isPoolActive is inverted, so gated entries accept a pool never opened and refuse an opened one.<br>Caught by: [`rvSrAddShareClassRefusesARepeatOrAnUnusableRegistration`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L19) · [`rvSrLinkTokenRefusesANonWardADeadPoolOrAnUnusableToken`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L38) · [`rvSrSetRequestManagerRefusesANonWardOrAPoolNeverOpened`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L56) · [`rvSrUpdateManagerRefusesANonWardOrAPoolNeverOpened`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L72) · [`rvSrUpdateBridgerRefusesANonWardOrAPoolNeverOpened`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L88) · [`rvSrSetPolicyRefusesANonWardOrAPoolNeverOpened`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L104) |
| [4501](#spokeregistry-4501) | hasShareClass is inverted, so vault registration and price updates accept a class that holds no token.<br>Caught by: [`rvSrRegisterVaultRefusesARepeatOrAMismatchedRegistration`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L167) · [`rvSrUpdatePricePoolPerShareRefusesANonWardADeadClassOrAnOlderStamp`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L251) · [`rvSrUpdatePricePoolPerAssetRefusesANonWardAnUnknownAssetOrAnOlderStamp`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L270) |
| [4502](#spokeregistry-4502) | addPool drops the entry latch, so a pool already opened is accepted a second time instead of being refused.<br>Caught by: [`rvSrAddPoolRefusesANonWardOrAPoolAlreadyOpen`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L4) |
| [4503](#spokeregistry-4503) | authorize drops the policy installed check, so a grant is accepted on a pool that never seated a policy.<br>Caught by: [`rvSrAuthorizeRefusesANonWardOrAPoolWithNoPolicy`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L118) |
| [4504](#spokeregistry-4504) | unauthorize loses its ward gate, so a revocation from a caller with no standing is accepted instead of refused.<br>Caught by: [`rvSrUnauthorizeRefusesANonWardOrAGrantThatDoesNotStand`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L132) |
| [4505](#spokeregistry-4505) | consumeAuthorization drops the installed policy check, so any caller can spend the pool's outstanding grants.<br>Caught by: [`rvSrConsumeAuthorizationRefusesAnyCallerButThePolicyOrAnEmptySlot`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L149) |
| [4506](#spokeregistry-4506) | linkVault drops the already linked latch, so a vault that is already in service is linked again instead of being refused.<br>Caught by: [`rvSrLinkVaultRefusesAnUnknownOrAlreadyLinkedVault`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L190) |
| [4507](#spokeregistry-4507) | unlinkVault drops the linked check, so a vault that carries no routing flag is unlinked again instead of being refused.<br>Caught by: [`rvSrUnlinkVaultRefusesAnUnroutedOrMismatchedVault`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L213) |
| [4508](#spokeregistry-4508) | createAssetId drops the real asset check, so numbering the zero address is accepted instead of refused.<br>Caught by: [`rvSrCreateAssetIdRefusesANonWardANullAssetOrAPairAlreadyNumbered`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L235) |
| [4509](#spokeregistry-4509) | idToAsset reads its fail closed flag inverted, so on an unregistered id strict lookups return null and plain ones revert.<br>Caught by: [`rvSrIdToAssetFailClosedRefusesAnUnregisteredId`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L290) · [`rvSrIdToAssetLookupAlwaysAnswers`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L305) |
| [4510](#spokeregistry-4510) | assetToId reads its fail closed flag inverted, so on an unregistered pair strict lookups return null and plain ones revert.<br>Caught by: [`rvSrAssetToIdFailClosedRefusesAnUnregisteredPair`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L318) · [`rvSrAssetToIdLookupAlwaysAnswers`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L332) |
| [4511](#spokeregistry-4511) | pricePoolPerShare reads its validity flag inverted, so for a never set price checked reads succeed and unchecked ones revert.<br>Caught by: [`rvSrPricePoolPerShareCheckedRefusesANeverComputedPrice`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L345) |
| [4512](#spokeregistry-4512) | pricePoolPerAsset reads its validity flag inverted, so for a never set price checked reads succeed and unchecked ones revert.<br>Caught by: [`rvSrPricePoolPerAssetCheckedRefusesANeverComputedPrice`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L359) |
| [4513](#spokeregistry-4513) | addPool loses its ward gate, so any caller opens a pool on this spoke and writes its entry stamp.<br>Caught by: [`acSrPoolEntryStampMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L21) |
| [4514](#spokeregistry-4514) | addShareClass loses its ward gate, so any caller binds a share class to its own token and registrar.<br>Caught by: [`acSrShareClassBindingMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L38) · [`acSrTokenLookupRowMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L59) |
| [4515](#spokeregistry-4515) | setRequestManager loses its ward gate, so any caller reroutes the pool's investor requests to a manager of its own.<br>Caught by: [`acSrRequestManagerMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L80) |
| [4516](#spokeregistry-4516) | updateManager loses its ward gate, so any caller grants or withdraws the pool manager standing the spoke honours.<br>Caught by: [`acSrManagerRightsMoveOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L98) |
| [4517](#spokeregistry-4517) | updateBridger loses its ward gate, so any caller grants or withdraws the bridger standing the spoke honours.<br>Caught by: [`acSrBridgerRightsMoveOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L115) |
| [4518](#spokeregistry-4518) | setPolicy loses its ward gate, so any caller seats a policy of its own on the pool and advances its install counter.<br>Caught by: [`acSrPolicyInstallMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L132) |
| [4519](#spokeregistry-4519) | authorize loses its ward gate, so any caller files a grant the pool never approved on the hub.<br>Caught by: [`acSrAuthorizationGrantedOnlyByAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L152) |
| [4520](#spokeregistry-4520) | unauthorize loses its ward gate, so any caller can revoke a grant the pool has outstanding.<br>Caught by: [`acSrAuthorizationSpentOrRevokedOnlyByAWardOrTheInstalledPolicy`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L169) |
| [4521](#spokeregistry-4521) | createAssetId loses its ward gate, so any caller mints an asset number and moves the registry's asset bijection.<br>Caught by: [`acSrAssetRegistryMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L188) |
| [4522](#spokeregistry-4522) | registerVault loses its ward gate, so any caller enters an unvetted vault in the registry under the pool's own identity.<br>Caught by: [`acSrVaultRegistrationMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L215) |
| [4523](#spokeregistry-4523) | linkVault loses its ward gate, so any caller puts a registered vault into service.<br>Caught by: [`acSrVaultLinkFlagMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L244) |
| [4524](#spokeregistry-4524) | updatePricePoolPerShare loses its ward gate, so any caller misprices the issuance and redemption of every share the class serves.<br>Caught by: [`acSrSharePriceMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L261) |
| [4525](#spokeregistry-4525) | updatePricePoolPerAsset loses its ward gate, so any caller misprices the asset leg of every deposit and withdrawal the pool settles.<br>Caught by: [`acSrAssetPriceMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L281) |
| [4526](#spokeregistry-4526) | consumeAuthorization also makes the caller it was handed a ward, so the pool's policy can mint registry admins.<br>Caught by: [`acSrWardSetMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L4) |
| [4527](#spokeregistry-4527) | authorize files two grants per call, so one consumption or one revocation leaves a grant outstanding.<br>Caught by: [`hlSrConsumptionSpendsExactlyOneGrant`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L4) · [`hlSrAuthorizationLedgerCountsGrants`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L42) |
| [4528](#spokeregistry-4528) | setPolicy leaves the install counter unchanged, so a policy seated again can still spend grants from its earlier tenure.<br>Caught by: [`hlSrPolicySwapOrphansOutstandingGrants`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L21) |
| [4529](#spokeregistry-4529) | createAssetId never writes the reverse lookup, so the asset pair does not resolve to its new id.<br>Caught by: [`hlSrCreatedAssetPairResolvesToIssuedId`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L59) |
| [4530](#spokeregistry-4530) | createAssetId never writes the forward asset row, so a new id resolves to neither its asset nor its token id.<br>Caught by: [`hlSrCreatedAssetIdResolvesToItsAsset`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L74) · [`hlSrCreatedAssetIdResolvesToItsTokenId`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L87) |
| [4531](#spokeregistry-4531) | setPolicy also raises the grant count of the zero authorization id, so grants change outside grant, revoke and consume.<br>Caught by: [`vtSrAuthorizationLedgerMovesOnlyThroughItsThreeWriters`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L111) |
| [4532](#spokeregistry-4532) | updatePricePoolPerAsset stores the new stamp but not the price, so the asset keeps its stale quote.<br>Caught by: [`hlSrAssetQuoteIsStoredExactlyAsSent`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L102) |
| [4533](#spokeregistry-4533) | _linkToken drops the deployed contract check, so a class can be relinked to the zero address and lose its token.<br>Caught by: [`vtSrShareTokenNeverClears`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L6) |
| [4534](#spokeregistry-4534) | setPolicy raises the policy nonce by two, so every install skips a nonce.<br>Caught by: [`vtSrPolicyTenureCounterStepsForwardByOne`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L21) |
| [4535](#spokeregistry-4535) | createAssetId decrements the asset counter, so it re-mints an issued number and rebinds it to another token.<br>Caught by: [`vtSrAssetCounterStepsForwardByOne`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L37) · [`vtSrIssuedAssetNumberKeepsItsBinding`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L53) |
| [4536](#spokeregistry-4536) | createAssetId drops the already registered check, so a registered token is numbered again and its id changes.<br>Caught by: [`vtSrRegisteredAssetKeepsItsNumber`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L72) |
| [4537](#spokeregistry-4537) | updateManager also clears the caller's own manager seat, so one call changes the roles of two accounts.<br>Caught by: [`vtSrPoolRolesMoveOneAccountAtATime`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L87) |
| [4538](#spokeregistry-4538) | The ward gate no longer looks at the caller, so handing out or withdrawing the registry's keys is open to everyone.<br>Caught by: [`rvSrRelyRefusesANonWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L373) · [`rvSrDenyRefusesANonWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L386) |
| [6100](#spokeregistry-6100) | Opening a pool no longer records the entry stamp, so a pool that was just added carries no creation time at all.<br>Caught by: [`rcSrAddPoolIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L4) |
| [6101](#spokeregistry-6101) | addPool's entry check is inverted, so opening a pool is refused unless it was already opened.<br>Caught by: [`rcSrFreshWardOpeningAPoolIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L644) · [`rcSrWholePoolBringUpIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L681) |
| [6102](#spokeregistry-6102) | The activity probe answers backwards, so a pool that was just opened reads as closed everywhere the registry checks it.<br>Caught by: [`rcSrPoolReadsActiveRightAfterAddIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L19) |
| [6103](#spokeregistry-6103) | addShareClass's duplicate check is inverted, so only a class that already holds a token can be registered.<br>Caught by: [`rvSrAddShareClassRefusesARepeatOrAnUnusableRegistration`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L19) |
| [6104](#spokeregistry-6104) | Relinking keeps the outgoing token's reverse lookup, so the old token still claims the class and a registrar swap is refused.<br>Caught by: [`rcSrTokenSwapRetiringTheOutgoingTokenIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L33) · [`rcSrRegistrarSwapKeepingTheIncumbentTokenIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L54) |
| [6105](#spokeregistry-6105) | Setting a request manager never stores it, so a pool's requests can be neither switched on nor off.<br>Caught by: [`rcSrSetRequestManagerIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L74) · [`rcSrClearingTheRequestManagerIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L89) |
| [6106](#spokeregistry-6106) | The manager seat is stored as the opposite of what the call asks for, so granting takes the seat away and revoking hands it out.<br>Caught by: [`rcSrGrantingOneManagerSeatIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L103) · [`rcSrRevokingOneOfTwoManagerSeatsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L119) |
| [6107](#spokeregistry-6107) | The bridger seat is stored as the opposite of what the call asks for, so granting takes the seat away and revoking hands it out.<br>Caught by: [`rcSrGrantingTheBridgerSeatAloneIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L136) · [`rcSrRevokingOneOfTwoBridgerSeatsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L705) |
| [6108](#spokeregistry-6108) | Installing a policy no longer advances its nonce, so reinstalling a policy revives the grants of its earlier tenure.<br>Caught by: [`rcSrFirstPolicyInstallIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L152) |
| [6109](#spokeregistry-6109) | Installing a policy is refused on any pool that already carries one, so a sitting policy can never be replaced and never cleared.<br>Caught by: [`rcSrPolicyReplacementIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L170) · [`rcSrClearingThePolicyIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L188) |
| [6110](#spokeregistry-6110) | A granted authorization is announced but never counted, so nothing can ever spend it.<br>Caught by: [`rcSrAuthorizeIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L205) |
| [6111](#spokeregistry-6111) | A revocation leaves the ledger row standing, so a grant survives the call that was meant to withdraw it.<br>Caught by: [`rcSrUnauthorizeEmptyingTheRowIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L240) · [`rcSrPolicySwapPuttingGrantsBeyondRevocationIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L302) |
| [6112](#spokeregistry-6112) | The policy spends a grant without taking it off the ledger, so one authorization can be used over and over.<br>Caught by: [`rcSrPolicyConsumingAGrantIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L261) · [`rcSrConsumingOneOfTwoGrantsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L282) |
| [6113](#spokeregistry-6113) | Numbering an asset leaves the issuing counter where it stands, so every asset of one origin chain is handed the very same number.<br>Caught by: [`rcSrFirstAssetNumberIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L325) · [`rcSrSecondAssetPairTakingItsOwnNumberIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L345) |
| [6114](#spokeregistry-6114) | Numbering now refuses any nonzero token id, so a token inside a multi token contract never gets an asset number.<br>Caught by: [`rcSrNumberingAMultiTokenAssetPairIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L367) |
| [6115](#spokeregistry-6115) | Numbering is refused on the smallest legal origin chain, so the low end of the chain namespace is unusable.<br>Caught by: [`rcSrAssetNumberOnTheSmallestOriginChainIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L384) |
| [6116](#spokeregistry-6116) | Numbering an asset files only the forward row, so the pair can never be resolved back to the number it was handed.<br>Caught by: [`rcSrCheckedAssetLookupsAfterNumberingAreReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L401) |
| [6117](#spokeregistry-6117) | Registering a vault puts it into service straight away, so a vault starts routing investor flows before anyone links it.<br>Caught by: [`rcSrRegisterVaultIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L420) · [`rcSrRegisterMultiTokenVaultIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L442) |
| [6118](#spokeregistry-6118) | Linking a vault never switches its service flag on, so a vault the pool just put into service still reads as out of service.<br>Caught by: [`rcSrLinkVaultIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L463) · [`rcSrLinkedVaultReadingBackThroughItsViewsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L520) · [`rcSrTwoVaultsLinkedForOneAssetIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L804) |
| [6119](#spokeregistry-6119) | Unlinking a vault never switches its service flag off, so service can never be withdrawn from a live vault.<br>Caught by: [`rcSrUnlinkVaultIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L479) · [`rcSrWithdrawingAndRestoringVaultServiceIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L495) |
| [6120](#spokeregistry-6120) | The share price gate turns strict, so a quote can never be corrected at the stamp it already carries.<br>Caught by: [`rcSrSharePriceCorrectionAtTheSameStampIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L573) |
| [6121](#spokeregistry-6121) | A share price update stores the quote but not its stamp, so the class keeps reading as never priced.<br>Caught by: [`rcSrFirstSharePriceIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L538) · [`rcSrSharePriceMovingToALaterStampIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L556) · [`rcSrCheckedSharePriceReadAfterAWriteIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L611) |
| [6122](#spokeregistry-6122) | An asset price update stores the quote but not its stamp, so the asset keeps reading as never priced.<br>Caught by: [`rcSrFirstAssetPriceIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L592) · [`rcSrCheckedAssetPriceReadAfterAWriteIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L627) |
| [6123](#spokeregistry-6123) | Revoking authority clears the caller's own seat instead of the named account's, so the target keeps its rights.<br>Caught by: [`rcSrDenyLeavingTheCallersOwnSeatIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L665) |
| [6124](#spokeregistry-6124) | A grant latches the ledger row at one, so authorizing the same call twice records only a single outstanding grant.<br>Caught by: [`rcSrTwoOutstandingGrantsAreReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L223) |
| [8630](#spokeregistry-8630) | A share price update no longer refuses a stamp later than the current block, so a future quote is stored and honest updates are refused as older until then.<br>Caught by: [`sharePriceStampNotFuture`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L283) |
| [8631](#spokeregistry-8631) | An asset price update no longer refuses a stamp later than the current block, so a future quote is stored and honest updates are refused as older until then.<br>Caught by: [`assetPriceStampNotFuture`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L288) |
| [8632](#spokeregistry-8632) | A share price update refuses a stamp equal to the current block time, so a quote computed in the block it is relayed in is refused.<br>Caught by: [`rvSrHonestSharePriceUpdateIsAccepted`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L427) |
| [8633](#spokeregistry-8633) | An asset price update refuses a stamp equal to the current block time, so a quote computed in the block it is relayed in is refused.<br>Caught by: [`rvSrHonestAssetPriceUpdateIsAccepted`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L445) |
| [8634](#spokeregistry-8634) | A share price update accepts a stamp one second past the current block time, so a quote from just ahead of the block lands.<br>Caught by: [`rvSrSharePriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L464) |
| [8635](#spokeregistry-8635) | An asset price update accepts a stamp one second past the current block time, so a quote from just ahead of the block lands.<br>Caught by: [`rvSrAssetPriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L476) |
| [8921](#spokeregistry-8921) | A share price update no longer refuses a stamp later than the current block, so a quote from the future is accepted.<br>Caught by: [`rvSrSharePriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L464) |
| [8922](#spokeregistry-8922) | An asset price update no longer refuses a stamp later than the current block, so a quote from the future is accepted.<br>Caught by: [`rvSrAssetPriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L476) |
| [8923](#spokeregistry-8923) | registerVault checks the vault only against the zero address, so an address without code can be registered as a vault.<br>Caught by: [`onlyADeployedContractHoldsAVaultRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L293) |
| [8924](#spokeregistry-8924) | registerVault refuses a taken vault only when the same pool names it, so another pool can take over a vault already registered.<br>Caught by: [`stSrRegisteredVaultIsNeverTakenByAnotherPool`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L98) |
| [8925](#spokeregistry-8925) | unlinkVault also demands the vault sit on token id zero, so a linked vault of a multi token asset can never be unlinked.<br>Caught by: [`rvSrUnlinkVaultIsNeverRefusedForALinkedVaultFiledUnderItsIds`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L488) |
| [8926](#spokeregistry-8926) | setRequestManager refuses a pool that already has a request manager, so an installed manager can be neither replaced nor cleared.<br>Caught by: [`rvSrSetRequestManagerIsNeverRefusedForAWardOnAnOpenedPool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L509) |
| [8927](#spokeregistry-8927) | linkVault records every link in one shared flag, so after one vault is linked no second vault can be linked anywhere.<br>Caught by: [`rcSrTwoVaultsLinkedForOneAssetIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L804) |
| [9031](#spokeregistry-9031) | unlinking a vault also unlinks the caller's own entry, so one unlink can take a second vault out of service.<br>Caught by: [`stSrAtMostOneVaultLinkMovesPerCall`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L255) |
| [9067](#spokeregistry-9067) | A share price update stamps its local arrival time, not the hub's computation time, so the quote's age is wrong.<br>Caught by: [`hlSrShareQuoteIsStoredExactlyAsSent`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L118) |
| [9068](#spokeregistry-9068) | A share class is bound with the token's own address as registrar, so mint authority is not the named registrar.<br>Caught by: [`hlSrShareClassBindsExactlyTheTokenAndRegistrarNamed`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L132) |
| [9069](#spokeregistry-9069) | addPool records the block number instead of the block time, so the pool's creation stamp is not when it opened.<br>Caught by: [`hlSrAddedPoolIsStampedWithTheBlockTime`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L154) |
| [9070](#spokeregistry-9070) | registerVault stores a new vault already linked, so a vault goes live without ever passing through linkVault.<br>Caught by: [`vtSrVaultLinkMovesOnlyOnLinkOrUnlink`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L130) |
| [9200](#spokeregistry-9200) | addPool no longer refuses the null pool id, so a ward can open pool zero and give it an activation stamp.<br>Caught by: [`rvSrAddPoolRefusesTheNullPool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L399) |
| [9202](#spokeregistry-9202) | A token swap clears the incoming token's lookup, not the outgoing one's, so the retired token still maps to the class.<br>Caught by: [`hlSrTokenSwapDeletesTheOutgoingTokensRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L168) |
| [9203](#spokeregistry-9203) | granting or withdrawing the bridger seat also sets the manager seat of the same account, so the two roles are no longer independent.<br>Caught by: [`stSrRoleSeatsMoveOnlyOnTheirOwnWriter`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L271) |
| [9204](#spokeregistry-9204) | the checked share price read refuses quotes older than one day, so core enforces a freshness window it is documented not to have.<br>Caught by: [`rcSrYearOldSharePriceIsAcceptedAndServedIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L722) |
| [9206](#spokeregistry-9206) | linking a share token also wipes the class's share price, so a token swap resets the price the class already carried.<br>Caught by: [`rcSrTokenSwapKeepsTheStandingSharePriceIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L738) |
| [9207](#spokeregistry-9207) | an asset quote older than the class's share quote is now refused, so the two prices are forced into one order.<br>Caught by: [`rcSrSharePriceLandsWithoutItsAssetPriceAndAnOlderAssetQuoteFollowsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L756) |
| [9208](#spokeregistry-9208) | a consumption keys the grant by the named caller instead of the policy, so only the policy itself can be named as caller.<br>Caught by: [`rcSrOneGrantKeyIsSpentUnderTwoDistinctCallersIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L779) |
| [9209](#spokeregistry-9209) | A consumption now also requires the named caller to be the policy, so no grant can be spent for another caller.<br>Caught by: [`rvSrStandingGrantIsSpendableUnderAnyNamedCaller`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L410) |
| [9210](#spokeregistry-9210) | linking a vault also marks the vault at the neighbouring address as linked, so an operation on one vault reaches another vault's link.<br>Caught by: [`hlSrLinkCallMovesOnlyItsOwnVaultsFlag`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L200) |
| [9241](#spokeregistry-9241) | linking a vault also writes the share token's vault pointer for the asset, so a link can no longer leave the pointer unset.<br>Caught by: [`rcShLinkLeavesTheTokenVaultPointerUnset`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/SpokeHandler_LinkedSpokeRegistry_vault_pointer_properties.spec#L6) |
| [9242](#spokeregistry-9242) | unlinking a vault also clears the share token's vault pointer, so an unlink no longer leaves the token naming it.<br>Caught by: [`rcShUnlinkLeavesTheTokenPointingAtTheUnlinkedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/SpokeHandler_LinkedSpokeRegistry_vault_pointer_properties.spec#L30) |
| [9243](#spokeregistry-9243) | linking a vault also writes the share token's vault pointer for the asset, so a link message reaches into the token.<br>Caught by: [`hlShLinkAndUnlinkNeverTouchATokenVaultPointer`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L322) |
| [9560](#spokeregistry-9560) | the check that the incoming token owns no lookup row is dropped, so a class can adopt a token another class holds.<br>Caught by: [`twoClassKeysNeverShareAToken`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L60) |
| [9561](#spokeregistry-9561) | the lookup row written for a linked token keeps only its pool half, so the token no longer resolves to its own share class.<br>Caught by: [`classTokenResolvesBack`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L39) |
| [9562](#spokeregistry-9562) | a token swap never retires the outgoing token's lookup row, so the retired token still resolves to a class that no longer holds it.<br>Caught by: [`lookupRowPointsBack`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L50) |
| [9563](#spokeregistry-9563) | the deployed contract check on the linked token always passes, so the zero address can be linked and claims a lookup row.<br>Caught by: [`nullAddressOwnsNoLookupRowOnAnyKey`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L72) |
| [9564](#spokeregistry-9564) | linking a token writes the neighbouring class's row instead of the named one, so the token looks up to a class not holding it.<br>Caught by: [`classTokenResolvesBack`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L39) · [`lookupRowPointsBack`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L50) |
| [9565](#spokeregistry-9565) | a manager grant or revoke is written on the neighbouring pool's seat instead of the named pool's.<br>Caught by: [`hlSrRoleGrantLandsOnTheNamedPoolOnly`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L119) |
| [9566](#spokeregistry-9566) | a manager grant or revoke also lands on the same account's seat in the neighbouring pool, so one call moves two pools' rosters.<br>Caught by: [`stSrRoleSeatsArePerPool`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L79) |
| [9567](#spokeregistry-9567) | linking a token never writes it into the class row, so the class keeps its old token or none.<br>Caught by: [`rcSrTokenSwapBesideALiveSecondClassIsReachable`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L168) · [`rcSrSecondClassGoesLiveBesideALiveFirstClassIsReachable`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L147) |
| [9943](#spokeregistry-9943) | the asset id packs the chain at bit 64 instead of 112, so the decoder reads chain zero from every new id.<br>Caught by: [`hlSrIssuedAssetIdIsTheChainOverTheCounter`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L186) |

## SpokeRegistry #1202

addPool stamps the pool one second ahead of the current block time, so the creation record points at a future moment.

- **Mutant:** [`1202.sol`](1202.sol)
- **Caught by:** [`poolCreatedAtNotFuture`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L47)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1202`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule poolCreatedAtNotFuture`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -63,7 +63,7 @@
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
         require(pool_.createdAt == 0, PoolAlreadyAdded());
-        pool_.createdAt = uint64(block.timestamp);
+        pool_.createdAt = uint64(block.timestamp + 1); // MUTATION: stamps pool creation one second in the future
 
         emit AddPool(poolId);
     }
```

## SpokeRegistry #1203

addPool records the block number instead of the block timestamp, so the creation stamp can sit far below any real chain time.

- **Mutant:** [`1203.sol`](1203.sol)
- **Caught by:** [`poolCreatedAboveEnvFloor`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L52)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1203`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule poolCreatedAboveEnvFloor`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -63,7 +63,7 @@
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
         require(pool_.createdAt == 0, PoolAlreadyAdded());
-        pool_.createdAt = uint64(block.timestamp);
+        pool_.createdAt = uint64(block.number); // MUTATION: records the block number instead of the timestamp
 
         emit AddPool(poolId);
     }
```

## SpokeRegistry #1204

_linkToken stores the share token but never stores the registrar, leaving the class with a token and no registrar.

- **Mutant:** [`1204.sol`](1204.sol)
- **Caught by:** [`shareTokenIffRegistrar`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L57)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1204`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule shareTokenIffRegistrar`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -96,7 +96,7 @@
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
         shareClass_.shareToken = IERC20(shareToken_);
-        shareClass_.registrar = registrar_;
+        // MUTATION: registrar assignment removed, the class keeps a token with no registrar
         tokenDetails[shareToken_] = TokenDetails(poolId, scId);
         emit AddShareClass(poolId, scId, shareToken_, registrar_);
     }
```

## SpokeRegistry #1205

addShareClass no longer checks the pool exists, so a share class can be created on a pool that was never added.

- **Mutant:** [`1205.sol`](1205.sol)
- **Caught by:** [`shareClassImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L62)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1205`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule shareClassImpliesActivePool`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -70,7 +70,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function addShareClass(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) external auth {
-        require(isPoolActive(poolId), InvalidPool());
+        // MUTATION: pool existence check removed from addShareClass
         require(address(shareClass[poolId][scId].shareToken) == address(0), ShareClassAlreadyRegistered());
 
         _linkToken(poolId, scId, shareToken_, registrar_);
```

## SpokeRegistry #1207

relinking clears only the pool half of the outgoing token's lookup row, leaving its class half behind without a pool reference.

- **Mutant:** [`1207.sol`](1207.sol)
- **Caught by:** [`tokenRowScIdImpliesPoolId`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L67)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1207`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule tokenRowScIdImpliesPoolId`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -91,7 +91,7 @@
         // Retire the outgoing token's reverse lookup before the uniqueness check, so relinking the same
         // token with a new registrar is allowed (swap the registrar, keep the token address). Reordered
         // relative to the check so the same-token case does not trip TokenAlreadyRegistered on itself.
-        if (address(shareClass_.shareToken) != address(0)) delete tokenDetails[address(shareClass_.shareToken)];
+        if (address(shareClass_.shareToken) != address(0)) tokenDetails[address(shareClass_.shareToken)].poolId = PoolId.wrap(0); // MUTATION: retires only the pool half of the outgoing token row
 
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
```

## SpokeRegistry #1208

_linkToken registers the share token without writing its reverse lookup row, so the token no longer resolves back to its pool and class.

- **Mutant:** [`1208.sol`](1208.sol)
- **Caught by:** [`shareTokenHasCanonicalReverseRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L72)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1208`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule shareTokenHasCanonicalReverseRow`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -97,7 +97,7 @@
 
         shareClass_.shareToken = IERC20(shareToken_);
         shareClass_.registrar = registrar_;
-        tokenDetails[shareToken_] = TokenDetails(poolId, scId);
+        // MUTATION: reverse lookup row is never written for the linked token
         emit AddShareClass(poolId, scId, shareToken_, registrar_);
     }
 
```

## SpokeRegistry #1209

replacing a share token leaves the outgoing token's lookup row in place, so a stale token still claims the pool and class.

- **Mutant:** [`1209.sol`](1209.sol)
- **Caught by:** [`onlyCurrentShareTokenHoldsALookupRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L81)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1209`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule onlyCurrentShareTokenHoldsALookupRow`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -91,7 +91,7 @@
         // Retire the outgoing token's reverse lookup before the uniqueness check, so relinking the same
         // token with a new registrar is allowed (swap the registrar, keep the token address). Reordered
         // relative to the check so the same-token case does not trip TokenAlreadyRegistered on itself.
-        if (address(shareClass_.shareToken) != address(0)) delete tokenDetails[address(shareClass_.shareToken)];
+        // MUTATION: outgoing token's reverse lookup row is never retired
 
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
```

## SpokeRegistry #1210

_linkToken drops the deployed-contract check, so an address without code, even zero, can be linked as a share token.

- **Mutant:** [`1210.sol`](1210.sol)
- **Caught by:** [`nullTokenRowPoolIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L89) · [`shareTokenIffRegistrar`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L57) · [`onlyADeployedContractOwnsATokenRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L278)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1210`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule nullTokenRowPoolIdZero shareTokenIffRegistrar onlyADeployedContractOwnsATokenRow`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -84,7 +84,7 @@
 
     function _linkToken(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) internal {
         // Must already be deployed, so a registrar cannot reserve another pool's future token address
-        require(shareToken_.code.length > 0, NotAContract());
+        // MUTATION: deployed-contract check removed, the zero address can be linked as a share token
         require(address(registrar_) != address(0), EmptyRegistrar());
 
         ShareClassDetails storage shareClass_ = shareClass[poolId][scId];
```

## SpokeRegistry #1211

setRequestManager skips the pool existence check, so a request manager can be installed on a pool that was never added.

- **Mutant:** [`1211.sol`](1211.sol)
- **Caught by:** [`requestManagerImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L94)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1211`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule requestManagerImpliesActivePool`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -103,7 +103,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function setRequestManager(PoolId poolId, ISpokeRequestManager manager_) external auth {
-        require(isPoolActive(poolId), InvalidPool());
+        // MUTATION: pool existence check removed from setRequestManager
         requestManager[poolId] = manager_;
         emit SetRequestManager(poolId, manager_);
     }
```

## SpokeRegistry #1212

updateManager skips the pool existence check, so manager rights can be granted on a pool that was never added.

- **Mutant:** [`1212.sol`](1212.sol)
- **Caught by:** [`managerImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L99)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1212`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule managerImpliesActivePool`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -139,7 +139,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function updateManager(PoolId poolId, address who, bool canManage) external auth {
-        require(isPoolActive(poolId), InvalidPool());
+        // MUTATION: pool existence check removed from updateManager
         manager[poolId][who] = canManage;
         emit UpdateManager(poolId, who, canManage);
     }
```

## SpokeRegistry #1213

updateBridger skips the pool existence check, so bridger rights can be granted on a pool that was never added.

- **Mutant:** [`1213.sol`](1213.sol)
- **Caught by:** [`bridgerImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L104)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1213`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule bridgerImpliesActivePool`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -146,7 +146,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function updateBridger(PoolId poolId, address who, bool canBridge) external auth {
-        require(isPoolActive(poolId), InvalidPool());
+        // MUTATION: pool existence check removed from updateBridger
         bridger[poolId][who] = canBridge;
         emit UpdateBridger(poolId, who, canBridge);
     }
```

## SpokeRegistry #1214

setPolicy installs the policy without advancing the install nonce, so the first installed policy carries a zero nonce.

- **Mutant:** [`1214.sol`](1214.sol)
- **Caught by:** [`policyImpliesNonzeroNonce`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L109)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1214`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule policyImpliesNonzeroNonce`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -158,7 +158,7 @@
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce); // MUTATION: policy install no longer advances the nonce
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeRegistry #1215

setPolicy skips the pool existence check, so a policy nonce starts moving on a pool that was never added.

- **Mutant:** [`1215.sol`](1215.sol)
- **Caught by:** [`policyNonceImpliesActivePool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L114)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1215`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule policyNonceImpliesActivePool`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -157,7 +157,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
-        require(isPoolActive(poolId), InvalidPool());
+        // MUTATION: pool existence check removed from setPolicy
         _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
         emit SetPolicy(poolId, policy_);
     }
```

## SpokeRegistry #1216

authorize leaves the authorization id underived, so every grant is counted under the zero id.

- **Mutant:** [`1216.sol`](1216.sol)
- **Caught by:** [`nullAuthIdRowEmpty`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L119)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1216`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule nullAuthIdRowEmpty`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -167,7 +167,7 @@
         PolicyInfo memory info = _policy[poolId];
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
-        bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
+        bytes32 id; // MUTATION: authorization id left underived, grants land on the zero id
         authorizations[id]++;
         emit AuthorizationGranted(poolId, id, data);
     }
```

## SpokeRegistry #1217

authorize drops the policy-installed check, so authorizations can be granted on a pool where no policy was ever set.

- **Mutant:** [`1217.sol`](1217.sol)
- **Caught by:** [`noPolicyEverMeansNoAuthorizations`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L125)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1217`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule noPolicyEverMeansNoAuthorizations`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -165,7 +165,7 @@
     /// @inheritdoc ISpokeRegistry
     function authorize(PoolId poolId, bytes calldata data) external auth {
         PolicyInfo memory info = _policy[poolId];
-        require(address(info.policy) != address(0), PolicyNotInstalled());
+        // MUTATION: policy installed check removed, grants can be issued before any policy was set
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
         authorizations[id]++;
```

## SpokeRegistry #1218

createAssetId records the forward asset row but never writes the reverse lookup, so the new id does not resolve back to itself.

- **Mutant:** [`1218.sol`](1218.sol)
- **Caught by:** [`assetForwardResolvesBack`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L133)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1218`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule assetForwardResolvesBack`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -314,7 +314,7 @@
         assetId = newAssetId(centrifugeId, _assetCounter);
 
         _idToAsset[assetId] = AssetIdKey(asset, tokenId);
-        _assetToId[asset][tokenId] = assetId;
+        // MUTATION: reverse asset lookup is never written
     }
 
     /// @inheritdoc ISpokeRegistry
```

## SpokeRegistry #1219

createAssetId writes the reverse lookup but never records the forward asset row, so the filed id points at an empty registry entry.

- **Mutant:** [`1219.sol`](1219.sol)
- **Caught by:** [`assetReverseResolvesBack`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L142)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1219`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule assetReverseResolvesBack`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -313,7 +313,7 @@
         _assetCounter++;
         assetId = newAssetId(centrifugeId, _assetCounter);
 
-        _idToAsset[assetId] = AssetIdKey(asset, tokenId);
+        // MUTATION: forward asset row is never written
         _assetToId[asset][tokenId] = assetId;
     }
 
```

## SpokeRegistry #1220

createAssetId no longer advances the asset counter, so an issued id falls outside the range the counter has covered.

- **Mutant:** [`1220.sol`](1220.sol)
- **Caught by:** [`registeredAssetIdWellFormed`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L154)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1220`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule registeredAssetIdWellFormed`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -310,7 +310,7 @@
         require(centrifugeId != 0, InvalidCentrifugeId());
         require(_assetToId[asset][tokenId].isNull(), AssetAlreadyRegistered());
 
-        _assetCounter++;
+        // MUTATION: asset counter is never advanced
         assetId = newAssetId(centrifugeId, _assetCounter);
 
         _idToAsset[assetId] = AssetIdKey(asset, tokenId);
```

## SpokeRegistry #1221

createAssetId accepts the zero asset address, registering an id whose registry row has no asset behind it.

- **Mutant:** [`1221.sol`](1221.sol)
- **Caught by:** [`unregisteredAssetRowEmpty`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L163) · [`nullAssetNeverRegistered`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L168)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1221`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule unregisteredAssetRowEmpty nullAssetNeverRegistered`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -306,7 +306,7 @@
         auth
         returns (AssetId assetId)
     {
-        require(asset != address(0), UnknownAsset());
+        // MUTATION: zero asset address check removed
         require(centrifugeId != 0, InvalidCentrifugeId());
         require(_assetToId[asset][tokenId].isNull(), AssetAlreadyRegistered());
 
```

## SpokeRegistry #1222

updatePricePoolPerShare drops the share class existence check, so a share price is stored for a class that does not exist.

- **Mutant:** [`1222.sol`](1222.sol)
- **Caught by:** [`sharePriceStampImpliesShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L173) · [`sharePriceValueImpliesShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L178)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1222`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule sharePriceStampImpliesShareClass sharePriceValueImpliesShareClass`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -351,7 +351,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
-        require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
+        // MUTATION: share class existence check removed from updatePricePoolPerShare
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
```

## SpokeRegistry #1223

updatePricePoolPerAsset drops the share class existence check, so an asset price is stored for a class that does not exist.

- **Mutant:** [`1223.sol`](1223.sol)
- **Caught by:** [`assetPriceStampImpliesShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L183) · [`assetPriceValueImpliesShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1223`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule assetPriceStampImpliesShareClass assetPriceValueImpliesShareClass`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -366,7 +366,7 @@
         external
         auth
     {
-        require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
+        // MUTATION: share class existence check removed from updatePricePoolPerAsset
         require(isRegistered(assetId), UnknownAsset());
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
```

## SpokeRegistry #1224

updatePricePoolPerAsset drops the asset registration check, so a price is stored for an asset id the registry does not know.

- **Mutant:** [`1224.sol`](1224.sol)
- **Caught by:** [`assetPriceStampImpliesRegisteredAsset`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L193) · [`assetPriceValueImpliesRegisteredAsset`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L198)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1224`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule assetPriceStampImpliesRegisteredAsset assetPriceValueImpliesRegisteredAsset`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -367,7 +367,7 @@
         auth
     {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
-        require(isRegistered(assetId), UnknownAsset());
+        // MUTATION: asset registration check removed from updatePricePoolPerAsset
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
```

## SpokeRegistry #1225

linkVault drops the registered-vault check, so a vault that was never registered can be marked linked.

- **Mutant:** [`1225.sol`](1225.sol)
- **Caught by:** [`linkedVaultIsRegistered`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L203)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1225`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule linkedVaultIsRegistered`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -257,7 +257,7 @@
 
         VaultDetails storage vaultDetails_ = _vaultDetails[vault_];
         require(!vaultDetails_.isLinked, AlreadyLinkedVault());
-        require(vaultDetails_.asset != address(0), UnknownVault());
+        // MUTATION: unknown vault check removed, an unregistered vault can be linked
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
```

## SpokeRegistry #1226

registerVault skips the asset pair cross-check, so a vault row can record a zero or mismatched asset for its asset id.

- **Mutant:** [`1226.sol`](1226.sol)
- **Caught by:** [`unregisteredVaultPoolIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L208) · [`unregisteredVaultScIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L213) · [`unregisteredVaultAssetIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L218) · [`unregisteredVaultTokenIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L223)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1226`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule unregisteredVaultPoolIdZero unregisteredVaultScIdZero unregisteredVaultAssetIdZero unregisteredVaultTokenIdZero`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -241,7 +241,7 @@
 
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         require(assetIdKey.asset != address(0), UnknownAsset());
-        require(assetIdKey.asset == asset && assetIdKey.tokenId == tokenId, UnknownAsset());
+        // MUTATION: asset identity cross-check removed from registerVault
 
         require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
         require(vault_.code.length > 0, NotAContract());
```

## SpokeRegistry #1227

registerVault validates only the asset address and no longer the token id, so the stored vault row can disagree with the asset registry.

- **Mutant:** [`1227.sol`](1227.sol)
- **Caught by:** [`registeredVaultMatchesAssetRegistry`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L228)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1227`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule registeredVaultMatchesAssetRegistry`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -241,7 +241,7 @@
 
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         require(assetIdKey.asset != address(0), UnknownAsset());
-        require(assetIdKey.asset == asset && assetIdKey.tokenId == tokenId, UnknownAsset());
+        require(assetIdKey.asset == asset, UnknownAsset()); // MUTATION: token id half of the asset identity check dropped
 
         require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
         require(vault_.code.length > 0, NotAContract());
```

## SpokeRegistry #1228

registerVault drops the share class existence check, so a vault can be registered outside the live share class.

- **Mutant:** [`1228.sol`](1228.sol)
- **Caught by:** [`registeredVaultSitsOnALiveShareClass`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L240)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1228`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule registeredVaultSitsOnALiveShareClass`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -237,7 +237,7 @@
         address vault_,
         bytes calldata payload
     ) external auth {
-        require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
+        // MUTATION: share class existence check removed from registerVault
 
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         require(assetIdKey.asset != address(0), UnknownAsset());
```

## SpokeRegistry #1229

registerVault drops the deployed-contract check, so the zero address can be registered as a vault.

- **Mutant:** [`1229.sol`](1229.sol)
- **Caught by:** [`nullVaultNeverRegistered`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L249) · [`onlyADeployedContractHoldsAVaultRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L293)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1229`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule nullVaultNeverRegistered onlyADeployedContractHoldsAVaultRow`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -244,7 +244,7 @@
         require(assetIdKey.asset == asset && assetIdKey.tokenId == tokenId, UnknownAsset());
 
         require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
-        require(vault_.code.length > 0, NotAContract());
+        // MUTATION: deployed-contract check removed, the zero address can be registered as a vault
 
         _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
         emit DeployVault(poolId, scId, asset, tokenId, factory, vault_, payload);
```

## SpokeRegistry #1230

_linkToken keys the reverse row by the old token, not the new one, so a first link fills the null address row.

- **Mutant:** [`1230.sol`](1230.sol)
- **Caught by:** [`nullTokenRowPoolIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L89)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1230`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule nullTokenRowPoolIdZero`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -95,9 +95,10 @@
 
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
+        // MUTATION: reverse row written before the class update, keyed off the still-stored token
+        tokenDetails[address(shareClass_.shareToken)] = TokenDetails(poolId, scId);
         shareClass_.shareToken = IERC20(shareToken_);
         shareClass_.registrar = registrar_;
-        tokenDetails[shareToken_] = TokenDetails(poolId, scId);
         emit AddShareClass(poolId, scId, shareToken_, registrar_);
     }
 
```

## SpokeRegistry #1231

registerVault records only the share class of the vault row, so a row with no asset carries a live class id.

- **Mutant:** [`1231.sol`](1231.sol)
- **Caught by:** [`unregisteredVaultScIdZero`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L213)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1231`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule unregisteredVaultScIdZero`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -246,7 +246,8 @@
         require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
         require(vault_.code.length > 0, NotAContract());
 
-        _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
+        // MUTATION: only the class id is stamped, the rest of the row is never recorded
+        _vaultDetails[vault_].scId = scId;
         emit DeployVault(poolId, scId, asset, tokenId, factory, vault_, payload);
     }
 
```

## SpokeRegistry #1232

registerVault stores the vault already linked, so registration by itself puts it into service.

- **Mutant:** [`1232.sol`](1232.sol)
- **Caught by:** [`stSrRegisteredVaultStartsUnlinked`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L150)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1232`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrRegisteredVaultStartsUnlinked`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -246,7 +246,7 @@
         require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
         require(vault_.code.length > 0, NotAContract());
 
-        _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
+        _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, true); // MUTATION: registered already linked
         emit DeployVault(poolId, scId, asset, tokenId, factory, vault_, payload);
     }
 
```

## SpokeRegistry #1235

setPolicy installs a replacement without advancing the install counter, so authorizations granted under the outgoing policy stay reachable.

- **Mutant:** [`1235.sol`](1235.sol)
- **Caught by:** [`stSrPolicySwapAdvancesTheInstallCounter`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L164)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1235`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrPolicySwapAdvancesTheInstallCounter`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -158,7 +158,7 @@
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce); // MUTATION: the install counter stands still
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeRegistry #1236

authorize files the grant under the install counter before the current one, so a grant lands in a retired policy tenure.

- **Mutant:** [`1236.sol`](1236.sol)
- **Caught by:** [`stSrGrantsLandOnlyOnTheInstalledPolicy`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L179)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1236`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrGrantsLandOnlyOnTheInstalledPolicy`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -167,7 +167,7 @@
         PolicyInfo memory info = _policy[poolId];
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
-        bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId, address(info.policy), info.nonce - 1, data); // MUTATION: filed one tenure back
         authorizations[id]++;
         emit AuthorizationGranted(poolId, id, data);
     }
```

## SpokeRegistry #1237

createAssetId mints the id before advancing the counter, so the first registered asset gets number zero.

- **Mutant:** [`1237.sol`](1237.sol)
- **Caught by:** [`registeredAssetIdWellFormed`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L154)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1237`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule registeredAssetIdWellFormed`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -310,8 +310,8 @@
         require(centrifugeId != 0, InvalidCentrifugeId());
         require(_assetToId[asset][tokenId].isNull(), AssetAlreadyRegistered());
 
+        assetId = newAssetId(centrifugeId, _assetCounter); // MUTATION: minted before the counter advances
         _assetCounter++;
-        assetId = newAssetId(centrifugeId, _assetCounter);
 
         _idToAsset[assetId] = AssetIdKey(asset, tokenId);
         _assetToId[asset][tokenId] = assetId;
```

## SpokeRegistry #1238

A share price update no longer refuses an older stamp, so a stale cross-chain price can overwrite a fresher one.

- **Mutant:** [`1238.sol`](1238.sol)
- **Caught by:** [`stSrPriceStampsNeverRewind`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L198)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1238`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrPriceStampsNeverRewind`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -354,7 +354,7 @@
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
-        require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
+        /* MUTATION: the older-price guard is removed */
 
         poolPerShare.price = price;
         poolPerShare.computedAt = computedAt;
```

## SpokeRegistry #1240

An asset price update no longer refuses an older stamp.

- **Mutant:** [`1240.sol`](1240.sol)
- **Caught by:** [`stSrPriceStampsNeverRewind`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L198)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1240`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrPriceStampsNeverRewind`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -371,7 +371,7 @@
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
-        require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
+        /* MUTATION: the older-price guard is removed */
 
         poolPerAsset.price = price;
         poolPerAsset.computedAt = computedAt;
```

## SpokeRegistry #1247

A grant files two authorizations at once.

- **Mutant:** [`1247.sol`](1247.sol)
- **Caught by:** [`stSrAuthorizationLedgerStepsByOneInTheStandingNamespace`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L211)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1247`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrAuthorizationLedgerStepsByOneInTheStandingNamespace`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -168,7 +168,7 @@
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
-        authorizations[id]++;
+        authorizations[id] += 2; /* MUTATION: double-filed */
         emit AuthorizationGranted(poolId, id, data);
     }
 
```

## SpokeRegistry #1248

A revocation is keyed to the previous tenure, so it strikes a retired row instead of the standing one.

- **Mutant:** [`1248.sol`](1248.sol)
- **Caught by:** [`stSrAuthorizationLedgerStepsByOneInTheStandingNamespace`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L211)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1248`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrAuthorizationLedgerStepsByOneInTheStandingNamespace`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -175,7 +175,7 @@
     /// @inheritdoc ISpokeRegistry
     function unauthorize(PoolId poolId, bytes calldata data) external auth {
         PolicyInfo memory info = _policy[poolId];
-        bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId, address(info.policy), info.nonce - 1, data); /* MUTATION: keyed to the previous tenure */
         uint256 count = authorizations[id];
         require(count != 0, NoOutstandingAuthorization());
 
```

## SpokeRegistry #1251

A registered vault can be registered again, so a live vault is re-pointed to another row.

- **Mutant:** [`1251.sol`](1251.sol)
- **Caught by:** [`stSrRegisteredVaultKeepsItsIdentity`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L228)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1251`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrRegisteredVaultKeepsItsIdentity`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -243,7 +243,7 @@
         require(assetIdKey.asset != address(0), UnknownAsset());
         require(assetIdKey.asset == asset && assetIdKey.tokenId == tokenId, UnknownAsset());
 
-        require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
+        /* MUTATION: the registration latch is removed */
         require(vault_.code.length > 0, NotAContract());
 
         _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
```

## SpokeRegistry #1252

A pool can be added again, so its entry stamp is rewritten.

- **Mutant:** [`1252.sol`](1252.sol)
- **Caught by:** [`stSrPoolEntryStampIsWrittenOnce`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L244)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1252`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrPoolEntryStampIsWrittenOnce`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -62,7 +62,7 @@
     function addPool(PoolId poolId) external auth {
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
-        require(pool_.createdAt == 0, PoolAlreadyAdded());
+        /* MUTATION: the entry latch is removed */
         pool_.createdAt = uint64(block.timestamp);
 
         emit AddPool(poolId);
```

## SpokeRegistry #1258

authorize files the grant one policy nonce ahead, so the installed policy cannot spend it until a later reinstall.

- **Mutant:** [`1258.sol`](1258.sol)
- **Caught by:** [`noAuthorizationsAheadOfTenure`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L263)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1258`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule noAuthorizationsAheadOfTenure`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -167,7 +167,7 @@
         PolicyInfo memory info = _policy[poolId];
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
-        bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId, address(info.policy), info.nonce + 1, data); // MUTATION: keyed one tenure ahead
         authorizations[id]++;
         emit AuthorizationGranted(poolId, id, data);
     }
```

## SpokeRegistry #1259

authorize files the grant under the calling ward instead of the installed policy, so that policy cannot spend it.

- **Mutant:** [`1259.sol`](1259.sol)
- **Caught by:** [`currentTenureAuthorizationsCarryTheInstalledPolicy`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L269)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1259`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule currentTenureAuthorizationsCarryTheInstalledPolicy`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -167,7 +167,7 @@
         PolicyInfo memory info = _policy[poolId];
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
-        bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId, msg.sender, info.nonce, data); // MUTATION: keyed by the caller, not the seated policy
         authorizations[id]++;
         emit AuthorizationGranted(poolId, id, data);
     }
```

## SpokeRegistry #1260

authorize files the grant under nonce 0 instead of the installed one, so no installed policy can ever spend it.

- **Mutant:** [`1260.sol`](1260.sol)
- **Caught by:** [`noAuthorizationsUnderZeroNonce`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L254)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 1260`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule noAuthorizationsUnderZeroNonce`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -167,7 +167,7 @@
         PolicyInfo memory info = _policy[poolId];
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
-        bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId, address(info.policy), 0, data); // MUTATION: filed in the reserved zero-nonce namespace
         authorizations[id]++;
         emit AuthorizationGranted(poolId, id, data);
     }
```

## SpokeRegistry #4500

isPoolActive is inverted, so gated entries accept a pool never opened and refuse an opened one.

- **Mutant:** [`4500.sol`](4500.sol)
- **Caught by:** [`rvSrAddShareClassRefusesARepeatOrAnUnusableRegistration`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L19) · [`rvSrLinkTokenRefusesANonWardADeadPoolOrAnUnusableToken`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L38) · [`rvSrSetRequestManagerRefusesANonWardOrAPoolNeverOpened`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L56) · [`rvSrUpdateManagerRefusesANonWardOrAPoolNeverOpened`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L72) · [`rvSrUpdateBridgerRefusesANonWardOrAPoolNeverOpened`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L88) · [`rvSrSetPolicyRefusesANonWardOrAPoolNeverOpened`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L104)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4500`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrAddShareClassRefusesARepeatOrAnUnusableRegistration rvSrLinkTokenRefusesANonWardADeadPoolOrAnUnusableToken rvSrSetRequestManagerRefusesANonWardOrAPoolNeverOpened rvSrUpdateManagerRefusesANonWardOrAPoolNeverOpened rvSrUpdateBridgerRefusesANonWardOrAPoolNeverOpened rvSrSetPolicyRefusesANonWardOrAPoolNeverOpened`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -110,7 +110,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function isPoolActive(PoolId poolId) public view returns (bool) {
-        return pool[poolId].createdAt > 0;
+        return pool[poolId].createdAt == 0; // MUTATION: the pool activity test is inverted
     }
 
     /// @inheritdoc ISpokeRegistry
```

## SpokeRegistry #4501

hasShareClass is inverted, so vault registration and price updates accept a class that holds no token.

- **Mutant:** [`4501.sol`](4501.sol)
- **Caught by:** [`rvSrRegisterVaultRefusesARepeatOrAMismatchedRegistration`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L167) · [`rvSrUpdatePricePoolPerShareRefusesANonWardADeadClassOrAnOlderStamp`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L251) · [`rvSrUpdatePricePoolPerAssetRefusesANonWardAnUnknownAssetOrAnOlderStamp`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L270)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4501`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrRegisterVaultRefusesARepeatOrAMismatchedRegistration rvSrUpdatePricePoolPerShareRefusesANonWardADeadClassOrAnOlderStamp rvSrUpdatePricePoolPerAssetRefusesANonWardAnUnknownAssetOrAnOlderStamp`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -115,7 +115,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function hasShareClass(PoolId poolId, ShareClassId scId) public view returns (bool) {
-        return address(shareClass[poolId][scId].shareToken) != address(0);
+        return address(shareClass[poolId][scId].shareToken) == address(0); // MUTATION: the share class test is inverted
     }
 
     /// @inheritdoc ISpokeRegistry
```

## SpokeRegistry #4502

addPool drops the entry latch, so a pool already opened is accepted a second time instead of being refused.

- **Mutant:** [`4502.sol`](4502.sol)
- **Caught by:** [`rvSrAddPoolRefusesANonWardOrAPoolAlreadyOpen`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4502`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrAddPoolRefusesANonWardOrAPoolAlreadyOpen`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -62,7 +62,7 @@
     function addPool(PoolId poolId) external auth {
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
-        require(pool_.createdAt == 0, PoolAlreadyAdded());
+        // MUTATION: the entry latch is removed
         pool_.createdAt = uint64(block.timestamp);
 
         emit AddPool(poolId);
```

## SpokeRegistry #4503

authorize drops the policy installed check, so a grant is accepted on a pool that never seated a policy.

- **Mutant:** [`4503.sol`](4503.sol)
- **Caught by:** [`rvSrAuthorizeRefusesANonWardOrAPoolWithNoPolicy`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L118)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4503`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrAuthorizeRefusesANonWardOrAPoolWithNoPolicy`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -165,7 +165,7 @@
     /// @inheritdoc ISpokeRegistry
     function authorize(PoolId poolId, bytes calldata data) external auth {
         PolicyInfo memory info = _policy[poolId];
-        require(address(info.policy) != address(0), PolicyNotInstalled());
+        // MUTATION: policy installed check removed, grants can be issued before any policy was set
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
         authorizations[id]++;
```

## SpokeRegistry #4504

unauthorize loses its ward gate, so a revocation from a caller with no standing is accepted instead of refused.

- **Mutant:** [`4504.sol`](4504.sol)
- **Caught by:** [`rvSrUnauthorizeRefusesANonWardOrAGrantThatDoesNotStand`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L132)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4504`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrUnauthorizeRefusesANonWardOrAGrantThatDoesNotStand`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -173,7 +173,7 @@
     }
 
     /// @inheritdoc ISpokeRegistry
-    function unauthorize(PoolId poolId, bytes calldata data) external auth {
+    function unauthorize(PoolId poolId, bytes calldata data) external { // MUTATION: the ward gate is gone
         PolicyInfo memory info = _policy[poolId];
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
         uint256 count = authorizations[id];
```

## SpokeRegistry #4505

consumeAuthorization drops the installed policy check, so any caller can spend the pool's outstanding grants.

- **Mutant:** [`4505.sol`](4505.sol)
- **Caught by:** [`rvSrConsumeAuthorizationRefusesAnyCallerButThePolicyOrAnEmptySlot`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L149)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4505`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrConsumeAuthorizationRefusesAnyCallerButThePolicyOrAnEmptySlot`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -186,7 +186,7 @@
     /// @inheritdoc ISpokeRegistry
     function consumeAuthorization(PoolId poolId, address caller, bytes calldata data) external {
         PolicyInfo memory info = _policy[poolId];
-        require(msg.sender == address(info.policy), CallerNotPolicy());
+        // MUTATION: the installed policy check is gone, any caller spends the grant
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
         uint256 count = authorizations[id];
```

## SpokeRegistry #4506

linkVault drops the already linked latch, so a vault that is already in service is linked again instead of being refused.

- **Mutant:** [`4506.sol`](4506.sol)
- **Caught by:** [`rvSrLinkVaultRefusesAnUnknownOrAlreadyLinkedVault`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L190)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4506`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrLinkVaultRefusesAnUnknownOrAlreadyLinkedVault`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -256,7 +256,7 @@
         require(assetIdKey.asset != address(0), UnknownAsset());
 
         VaultDetails storage vaultDetails_ = _vaultDetails[vault_];
-        require(!vaultDetails_.isLinked, AlreadyLinkedVault());
+        // MUTATION: the already linked latch is removed
         require(vaultDetails_.asset != address(0), UnknownVault());
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
```

## SpokeRegistry #4507

unlinkVault drops the linked check, so a vault that carries no routing flag is unlinked again instead of being refused.

- **Mutant:** [`4507.sol`](4507.sol)
- **Caught by:** [`rvSrUnlinkVaultRefusesAnUnroutedOrMismatchedVault`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L213)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4507`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrUnlinkVaultRefusesAnUnroutedOrMismatchedVault`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -272,7 +272,7 @@
         require(assetIdKey.asset != address(0), UnknownAsset());
 
         VaultDetails storage vaultDetails_ = _vaultDetails[vault_];
-        require(vaultDetails_.isLinked, AlreadyUnlinkedVault());
+        // MUTATION: the linked vault check is removed
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
```

## SpokeRegistry #4508

createAssetId drops the real asset check, so numbering the zero address is accepted instead of refused.

- **Mutant:** [`4508.sol`](4508.sol)
- **Caught by:** [`rvSrCreateAssetIdRefusesANonWardANullAssetOrAPairAlreadyNumbered`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L235)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4508`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrCreateAssetIdRefusesANonWardANullAssetOrAPairAlreadyNumbered`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -306,7 +306,7 @@
         auth
         returns (AssetId assetId)
     {
-        require(asset != address(0), UnknownAsset());
+        // MUTATION: zero asset address check removed
         require(centrifugeId != 0, InvalidCentrifugeId());
         require(_assetToId[asset][tokenId].isNull(), AssetAlreadyRegistered());
 
```

## SpokeRegistry #4509

idToAsset reads its fail closed flag inverted, so on an unregistered id strict lookups return null and plain ones revert.

- **Mutant:** [`4509.sol`](4509.sol)
- **Caught by:** [`rvSrIdToAssetFailClosedRefusesAnUnregisteredId`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L290) · [`rvSrIdToAssetLookupAlwaysAnswers`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L305)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4509`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrIdToAssetFailClosedRefusesAnUnregisteredId rvSrIdToAssetLookupAlwaysAnswers`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -330,7 +330,7 @@
     /// @inheritdoc ISpokeRegistry
     function idToAsset(AssetId assetId, bool revertOnNull) public view returns (address asset, uint256 tokenId) {
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
-        require(!revertOnNull || assetIdKey.asset != address(0), UnknownAsset());
+        require(revertOnNull || assetIdKey.asset != address(0), UnknownAsset()); // MUTATION: the fail closed flag is read inverted
         return (assetIdKey.asset, assetIdKey.tokenId);
     }
 
```

## SpokeRegistry #4510

assetToId reads its fail closed flag inverted, so on an unregistered pair strict lookups return null and plain ones revert.

- **Mutant:** [`4510.sol`](4510.sol)
- **Caught by:** [`rvSrAssetToIdFailClosedRefusesAnUnregisteredPair`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L318) · [`rvSrAssetToIdLookupAlwaysAnswers`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L332)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4510`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrAssetToIdFailClosedRefusesAnUnregisteredPair rvSrAssetToIdLookupAlwaysAnswers`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -342,7 +342,7 @@
     /// @inheritdoc ISpokeRegistry
     function assetToId(address asset, uint256 tokenId, bool revertOnNull) public view returns (AssetId assetId) {
         assetId = _assetToId[asset][tokenId];
-        require(!revertOnNull || !assetId.isNull(), UnknownAsset());
+        require(revertOnNull || !assetId.isNull(), UnknownAsset()); // MUTATION: the fail closed flag is read inverted
     }
 
     //----------------------------------------------------------------------------------------------
```

## SpokeRegistry #4511

pricePoolPerShare reads its validity flag inverted, so for a never set price checked reads succeed and unchecked ones revert.

- **Mutant:** [`4511.sol`](4511.sol)
- **Caught by:** [`rvSrPricePoolPerShareCheckedRefusesANeverComputedPrice`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L345)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4511`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrPricePoolPerShareCheckedRefusesANeverComputedPrice`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -381,7 +381,7 @@
     /// @inheritdoc ISpokeRegistry
     function pricePoolPerShare(PoolId poolId, ShareClassId scId, bool checkValidity) public view returns (D18 price) {
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
-        require(!checkValidity || poolPerShare.isValid(), InvalidPrice());
+        require(checkValidity || poolPerShare.isValid(), InvalidPrice()); // MUTATION: the validity flag is read inverted
 
         return poolPerShare.price;
     }
```

## SpokeRegistry #4512

pricePoolPerAsset reads its validity flag inverted, so for a never set price checked reads succeed and unchecked ones revert.

- **Mutant:** [`4512.sol`](4512.sol)
- **Caught by:** [`rvSrPricePoolPerAssetCheckedRefusesANeverComputedPrice`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L359)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4512`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrPricePoolPerAssetCheckedRefusesANeverComputedPrice`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -393,7 +393,7 @@
         returns (D18 price)
     {
         Price memory poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
-        require(!checkValidity || poolPerAsset.isValid(), InvalidPrice());
+        require(checkValidity || poolPerAsset.isValid(), InvalidPrice()); // MUTATION: the validity flag is read inverted
 
         return poolPerAsset.price;
     }
```

## SpokeRegistry #4513

addPool loses its ward gate, so any caller opens a pool on this spoke and writes its entry stamp.

- **Mutant:** [`4513.sol`](4513.sol)
- **Caught by:** [`acSrPoolEntryStampMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4513`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrPoolEntryStampMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -59,7 +59,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeRegistry
-    function addPool(PoolId poolId) external auth {
+    function addPool(PoolId poolId) external { // MUTATION: the ward gate is gone
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
         require(pool_.createdAt == 0, PoolAlreadyAdded());
```

## SpokeRegistry #4514

addShareClass loses its ward gate, so any caller binds a share class to its own token and registrar.

- **Mutant:** [`4514.sol`](4514.sol)
- **Caught by:** [`acSrShareClassBindingMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L38) · [`acSrTokenLookupRowMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L59)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4514`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrShareClassBindingMovesOnlyForAWard acSrTokenLookupRowMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -69,7 +69,7 @@
     }
 
     /// @inheritdoc ISpokeRegistry
-    function addShareClass(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) external auth {
+    function addShareClass(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) external { // MUTATION: the ward gate is gone
         require(isPoolActive(poolId), InvalidPool());
         require(address(shareClass[poolId][scId].shareToken) == address(0), ShareClassAlreadyRegistered());
 
```

## SpokeRegistry #4515

setRequestManager loses its ward gate, so any caller reroutes the pool's investor requests to a manager of its own.

- **Mutant:** [`4515.sol`](4515.sol)
- **Caught by:** [`acSrRequestManagerMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L80)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4515`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrRequestManagerMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -102,7 +102,7 @@
     }
 
     /// @inheritdoc ISpokeRegistry
-    function setRequestManager(PoolId poolId, ISpokeRequestManager manager_) external auth {
+    function setRequestManager(PoolId poolId, ISpokeRequestManager manager_) external { // MUTATION: the ward gate is gone
         require(isPoolActive(poolId), InvalidPool());
         requestManager[poolId] = manager_;
         emit SetRequestManager(poolId, manager_);
```

## SpokeRegistry #4516

updateManager loses its ward gate, so any caller grants or withdraws the pool manager standing the spoke honours.

- **Mutant:** [`4516.sol`](4516.sol)
- **Caught by:** [`acSrManagerRightsMoveOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L98)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4516`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrManagerRightsMoveOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -138,7 +138,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeRegistry
-    function updateManager(PoolId poolId, address who, bool canManage) external auth {
+    function updateManager(PoolId poolId, address who, bool canManage) external { // MUTATION: the ward gate is gone
         require(isPoolActive(poolId), InvalidPool());
         manager[poolId][who] = canManage;
         emit UpdateManager(poolId, who, canManage);
```

## SpokeRegistry #4517

updateBridger loses its ward gate, so any caller grants or withdraws the bridger standing the spoke honours.

- **Mutant:** [`4517.sol`](4517.sol)
- **Caught by:** [`acSrBridgerRightsMoveOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L115)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4517`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrBridgerRightsMoveOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -145,7 +145,7 @@
     }
 
     /// @inheritdoc ISpokeRegistry
-    function updateBridger(PoolId poolId, address who, bool canBridge) external auth {
+    function updateBridger(PoolId poolId, address who, bool canBridge) external { // MUTATION: the ward gate is gone
         require(isPoolActive(poolId), InvalidPool());
         bridger[poolId][who] = canBridge;
         emit UpdateBridger(poolId, who, canBridge);
```

## SpokeRegistry #4518

setPolicy loses its ward gate, so any caller seats a policy of its own on the pool and advances its install counter.

- **Mutant:** [`4518.sol`](4518.sol)
- **Caught by:** [`acSrPolicyInstallMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L132)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4518`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrPolicyInstallMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -156,7 +156,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeRegistry
-    function setPolicy(PoolId poolId, IPolicy policy_) external auth {
+    function setPolicy(PoolId poolId, IPolicy policy_) external { // MUTATION: the ward gate is gone
         require(isPoolActive(poolId), InvalidPool());
         _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
         emit SetPolicy(poolId, policy_);
```

## SpokeRegistry #4519

authorize loses its ward gate, so any caller files a grant the pool never approved on the hub.

- **Mutant:** [`4519.sol`](4519.sol)
- **Caught by:** [`acSrAuthorizationGrantedOnlyByAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L152)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4519`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrAuthorizationGrantedOnlyByAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -163,7 +163,7 @@
     }
 
     /// @inheritdoc ISpokeRegistry
-    function authorize(PoolId poolId, bytes calldata data) external auth {
+    function authorize(PoolId poolId, bytes calldata data) external { // MUTATION: the ward gate is gone
         PolicyInfo memory info = _policy[poolId];
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
```

## SpokeRegistry #4520

unauthorize loses its ward gate, so any caller can revoke a grant the pool has outstanding.

- **Mutant:** [`4520.sol`](4520.sol)
- **Caught by:** [`acSrAuthorizationSpentOrRevokedOnlyByAWardOrTheInstalledPolicy`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L169)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4520`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrAuthorizationSpentOrRevokedOnlyByAWardOrTheInstalledPolicy`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -173,7 +173,7 @@
     }
 
     /// @inheritdoc ISpokeRegistry
-    function unauthorize(PoolId poolId, bytes calldata data) external auth {
+    function unauthorize(PoolId poolId, bytes calldata data) external { // MUTATION: the ward gate is gone
         PolicyInfo memory info = _policy[poolId];
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
         uint256 count = authorizations[id];
```

## SpokeRegistry #4521

createAssetId loses its ward gate, so any caller mints an asset number and moves the registry's asset bijection.

- **Mutant:** [`4521.sol`](4521.sol)
- **Caught by:** [`acSrAssetRegistryMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4521`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrAssetRegistryMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -303,7 +303,7 @@
     /// @inheritdoc ISpokeRegistry
     function createAssetId(uint16 centrifugeId, address asset, uint256 tokenId)
         external
-        auth
+        // MUTATION: the ward gate is gone
         returns (AssetId assetId)
     {
         require(asset != address(0), UnknownAsset());
```

## SpokeRegistry #4522

registerVault loses its ward gate, so any caller enters an unvetted vault in the registry under the pool's own identity.

- **Mutant:** [`4522.sol`](4522.sol)
- **Caught by:** [`acSrVaultRegistrationMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L215)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4522`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrVaultRegistrationMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -236,7 +236,7 @@
         IVaultFactory factory,
         address vault_,
         bytes calldata payload
-    ) external auth {
+    ) external { // MUTATION: the ward gate is gone
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
 
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
```

## SpokeRegistry #4523

linkVault loses its ward gate, so any caller puts a registered vault into service.

- **Mutant:** [`4523.sol`](4523.sol)
- **Caught by:** [`acSrVaultLinkFlagMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L244)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4523`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrVaultLinkFlagMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -251,7 +251,7 @@
     }
 
     /// @inheritdoc ISpokeRegistry
-    function linkVault(PoolId poolId, ShareClassId scId, AssetId assetId, address vault_) external auth {
+    function linkVault(PoolId poolId, ShareClassId scId, AssetId assetId, address vault_) external { // MUTATION: the ward gate is gone
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         require(assetIdKey.asset != address(0), UnknownAsset());
 
```

## SpokeRegistry #4524

updatePricePoolPerShare loses its ward gate, so any caller misprices the issuance and redemption of every share the class serves.

- **Mutant:** [`4524.sol`](4524.sol)
- **Caught by:** [`acSrSharePriceMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L261)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4524`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrSharePriceMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -350,7 +350,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeRegistry
-    function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
+    function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external { // MUTATION: the ward gate is gone
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
```

## SpokeRegistry #4525

updatePricePoolPerAsset loses its ward gate, so any caller misprices the asset leg of every deposit and withdrawal the pool settles.

- **Mutant:** [`4525.sol`](4525.sol)
- **Caught by:** [`acSrAssetPriceMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L281)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4525`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrAssetPriceMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -364,7 +364,7 @@
     /// @inheritdoc ISpokeRegistry
     function updatePricePoolPerAsset(PoolId poolId, ShareClassId scId, AssetId assetId, D18 price, uint64 computedAt)
         external
-        auth
+        // MUTATION: the ward gate is gone
     {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         require(isRegistered(assetId), UnknownAsset());
```

## SpokeRegistry #4526

consumeAuthorization also makes the caller it was handed a ward, so the pool's policy can mint registry admins.

- **Mutant:** [`4526.sol`](4526.sol)
- **Caught by:** [`acSrWardSetMovesOnlyForAWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4526`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/access_control.conf --rule acSrWardSetMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -193,6 +193,7 @@
         require(count != 0, NoOutstandingAuthorization());
 
         authorizations[id] = count - 1;
+        wards[caller] = 1; // MUTATION: consumption seats the named caller as a ward
         emit AuthorizationConsumed(poolId, caller, id);
     }
 
```

## SpokeRegistry #4527

authorize files two grants per call, so one consumption or one revocation leaves a grant outstanding.

- **Mutant:** [`4527.sol`](4527.sol)
- **Caught by:** [`hlSrConsumptionSpendsExactlyOneGrant`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L4) · [`hlSrAuthorizationLedgerCountsGrants`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L42)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4527`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrConsumptionSpendsExactlyOneGrant hlSrAuthorizationLedgerCountsGrants`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -168,7 +168,7 @@
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
-        authorizations[id]++;
+        authorizations[id] += 2; // MUTATION: double-filed
         emit AuthorizationGranted(poolId, id, data);
     }
 
```

## SpokeRegistry #4528

setPolicy leaves the install counter unchanged, so a policy seated again can still spend grants from its earlier tenure.

- **Mutant:** [`4528.sol`](4528.sol)
- **Caught by:** [`hlSrPolicySwapOrphansOutstandingGrants`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4528`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrPolicySwapOrphansOutstandingGrants`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -158,7 +158,7 @@
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce); // MUTATION: the install counter stands still
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeRegistry #4529

createAssetId never writes the reverse lookup, so the asset pair does not resolve to its new id.

- **Mutant:** [`4529.sol`](4529.sol)
- **Caught by:** [`hlSrCreatedAssetPairResolvesToIssuedId`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L59)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4529`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrCreatedAssetPairResolvesToIssuedId`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -314,7 +314,7 @@
         assetId = newAssetId(centrifugeId, _assetCounter);
 
         _idToAsset[assetId] = AssetIdKey(asset, tokenId);
-        _assetToId[asset][tokenId] = assetId;
+        // MUTATION: reverse asset lookup is never written
     }
 
     /// @inheritdoc ISpokeRegistry
```

## SpokeRegistry #4530

createAssetId never writes the forward asset row, so a new id resolves to neither its asset nor its token id.

- **Mutant:** [`4530.sol`](4530.sol)
- **Caught by:** [`hlSrCreatedAssetIdResolvesToItsAsset`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L74) · [`hlSrCreatedAssetIdResolvesToItsTokenId`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L87)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4530`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrCreatedAssetIdResolvesToItsAsset hlSrCreatedAssetIdResolvesToItsTokenId`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -313,7 +313,7 @@
         _assetCounter++;
         assetId = newAssetId(centrifugeId, _assetCounter);
 
-        _idToAsset[assetId] = AssetIdKey(asset, tokenId);
+        // MUTATION: forward asset row is never written
         _assetToId[asset][tokenId] = assetId;
     }
 
```

## SpokeRegistry #4531

setPolicy also raises the grant count of the zero authorization id, so grants change outside grant, revoke and consume.

- **Mutant:** [`4531.sol`](4531.sol)
- **Caught by:** [`vtSrAuthorizationLedgerMovesOnlyThroughItsThreeWriters`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L111)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4531`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule vtSrAuthorizationLedgerMovesOnlyThroughItsThreeWriters`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -159,6 +159,7 @@
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
         _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        authorizations[bytes32(0)]++; // MUTATION: the installer files a bootstrap grant
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeRegistry #4532

updatePricePoolPerAsset stores the new stamp but not the price, so the asset keeps its stale quote.

- **Mutant:** [`4532.sol`](4532.sol)
- **Caught by:** [`hlSrAssetQuoteIsStoredExactlyAsSent`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L102)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4532`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrAssetQuoteIsStoredExactlyAsSent`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -373,7 +373,7 @@
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
         require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
 
-        poolPerAsset.price = price;
+        // MUTATION: the quote value is never stored, only its stamp
         poolPerAsset.computedAt = computedAt;
         emit UpdateAssetPrice(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, price, computedAt);
     }
```

## SpokeRegistry #4533

_linkToken drops the deployed contract check, so a class can be relinked to the zero address and lose its token.

- **Mutant:** [`4533.sol`](4533.sol)
- **Caught by:** [`vtSrShareTokenNeverClears`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4533`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule vtSrShareTokenNeverClears`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -84,7 +84,7 @@
 
     function _linkToken(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) internal {
         // Must already be deployed, so a registrar cannot reserve another pool's future token address
-        require(shareToken_.code.length > 0, NotAContract());
+        // MUTATION: deployed-contract check removed, the zero address can be linked as a share token
         require(address(registrar_) != address(0), EmptyRegistrar());
 
         ShareClassDetails storage shareClass_ = shareClass[poolId][scId];
```

## SpokeRegistry #4534

setPolicy raises the policy nonce by two, so every install skips a nonce.

- **Mutant:** [`4534.sol`](4534.sol)
- **Caught by:** [`vtSrPolicyTenureCounterStepsForwardByOne`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4534`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule vtSrPolicyTenureCounterStepsForwardByOne`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -158,7 +158,7 @@
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 2); // MUTATION: the tenure counter jumps two at a time
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeRegistry #4535

createAssetId decrements the asset counter, so it re-mints an issued number and rebinds it to another token.

- **Mutant:** [`4535.sol`](4535.sol)
- **Caught by:** [`vtSrAssetCounterStepsForwardByOne`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L37) · [`vtSrIssuedAssetNumberKeepsItsBinding`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L53)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4535`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule vtSrAssetCounterStepsForwardByOne vtSrIssuedAssetNumberKeepsItsBinding`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -310,7 +310,7 @@
         require(centrifugeId != 0, InvalidCentrifugeId());
         require(_assetToId[asset][tokenId].isNull(), AssetAlreadyRegistered());
 
-        _assetCounter++;
+        _assetCounter--; // MUTATION: the numbering counter is walked backwards
         assetId = newAssetId(centrifugeId, _assetCounter);
 
         _idToAsset[assetId] = AssetIdKey(asset, tokenId);
```

## SpokeRegistry #4536

createAssetId drops the already registered check, so a registered token is numbered again and its id changes.

- **Mutant:** [`4536.sol`](4536.sol)
- **Caught by:** [`vtSrRegisteredAssetKeepsItsNumber`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L72)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4536`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule vtSrRegisteredAssetKeepsItsNumber`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -308,7 +308,7 @@
     {
         require(asset != address(0), UnknownAsset());
         require(centrifugeId != 0, InvalidCentrifugeId());
-        require(_assetToId[asset][tokenId].isNull(), AssetAlreadyRegistered());
+        // MUTATION: the already numbered latch is removed
 
         _assetCounter++;
         assetId = newAssetId(centrifugeId, _assetCounter);
```

## SpokeRegistry #4537

updateManager also clears the caller's own manager seat, so one call changes the roles of two accounts.

- **Mutant:** [`4537.sol`](4537.sol)
- **Caught by:** [`vtSrPoolRolesMoveOneAccountAtATime`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L87)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4537`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule vtSrPoolRolesMoveOneAccountAtATime`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -140,6 +140,7 @@
     /// @inheritdoc ISpokeRegistry
     function updateManager(PoolId poolId, address who, bool canManage) external auth {
         require(isPoolActive(poolId), InvalidPool());
+        manager[poolId][msg.sender] = false; // MUTATION: seating a manager withdraws the caller's own seat
         manager[poolId][who] = canManage;
         emit UpdateManager(poolId, who, canManage);
     }
```

## SpokeRegistry #4538

The ward gate no longer looks at the caller, so handing out or withdrawing the registry's keys is open to everyone.

- **Mutant:** [`4538.sol`](4538.sol)
- **Caught by:** [`rvSrRelyRefusesANonWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L373) · [`rvSrDenyRefusesANonWard`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L386)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 4538`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrRelyRefusesANonWard rvSrDenyRefusesANonWard`

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

## SpokeRegistry #6100

Opening a pool no longer records the entry stamp, so a pool that was just added carries no creation time at all.

- **Mutant:** [`6100.sol`](6100.sol)
- **Caught by:** [`rcSrAddPoolIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6100`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrAddPoolIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -63,7 +63,7 @@
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
         require(pool_.createdAt == 0, PoolAlreadyAdded());
-        pool_.createdAt = uint64(block.timestamp);
+        // MUTATION: the entry stamp is never written
 
         emit AddPool(poolId);
     }
```

## SpokeRegistry #6101

addPool's entry check is inverted, so opening a pool is refused unless it was already opened.

- **Mutant:** [`6101.sol`](6101.sol)
- **Caught by:** [`rcSrFreshWardOpeningAPoolIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L644) · [`rcSrWholePoolBringUpIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L681)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6101`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrFreshWardOpeningAPoolIsReachable rcSrWholePoolBringUpIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -62,7 +62,8 @@
     function addPool(PoolId poolId) external auth {
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
-        require(pool_.createdAt == 0, PoolAlreadyAdded());
+        // MUTATION: the entry latch admits only a pool that was already opened
+        require(pool_.createdAt != 0, PoolAlreadyAdded());
         pool_.createdAt = uint64(block.timestamp);
 
         emit AddPool(poolId);
```

## SpokeRegistry #6102

The activity probe answers backwards, so a pool that was just opened reads as closed everywhere the registry checks it.

- **Mutant:** [`6102.sol`](6102.sol)
- **Caught by:** [`rcSrPoolReadsActiveRightAfterAddIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L19)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6102`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrPoolReadsActiveRightAfterAddIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -110,7 +110,8 @@
 
     /// @inheritdoc ISpokeRegistry
     function isPoolActive(PoolId poolId) public view returns (bool) {
-        return pool[poolId].createdAt > 0;
+        // MUTATION: the activity probe answers backwards
+        return pool[poolId].createdAt == 0;
     }
 
     /// @inheritdoc ISpokeRegistry
```

## SpokeRegistry #6103

addShareClass's duplicate check is inverted, so only a class that already holds a token can be registered.

- **Mutant:** [`6103.sol`](6103.sol)
- **Caught by:** [`rvSrAddShareClassRefusesARepeatOrAnUnusableRegistration`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L19)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6103`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrAddShareClassRefusesARepeatOrAnUnusableRegistration`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -71,7 +71,8 @@
     /// @inheritdoc ISpokeRegistry
     function addShareClass(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        require(address(shareClass[poolId][scId].shareToken) == address(0), ShareClassAlreadyRegistered());
+        // MUTATION: the latch admits only a class that already holds a token
+        require(address(shareClass[poolId][scId].shareToken) != address(0), ShareClassAlreadyRegistered());
 
         _linkToken(poolId, scId, shareToken_, registrar_);
     }
```

## SpokeRegistry #6104

Relinking keeps the outgoing token's reverse lookup, so the old token still claims the class and a registrar swap is refused.

- **Mutant:** [`6104.sol`](6104.sol)
- **Caught by:** [`rcSrTokenSwapRetiringTheOutgoingTokenIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L33) · [`rcSrRegistrarSwapKeepingTheIncumbentTokenIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6104`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrTokenSwapRetiringTheOutgoingTokenIsReachable rcSrRegistrarSwapKeepingTheIncumbentTokenIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -91,7 +91,7 @@
         // Retire the outgoing token's reverse lookup before the uniqueness check, so relinking the same
         // token with a new registrar is allowed (swap the registrar, keep the token address). Reordered
         // relative to the check so the same-token case does not trip TokenAlreadyRegistered on itself.
-        if (address(shareClass_.shareToken) != address(0)) delete tokenDetails[address(shareClass_.shareToken)];
+        // MUTATION: the outgoing token keeps its reverse lookup row
 
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
```

## SpokeRegistry #6105

Setting a request manager never stores it, so a pool's requests can be neither switched on nor off.

- **Mutant:** [`6105.sol`](6105.sol)
- **Caught by:** [`rcSrSetRequestManagerIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L74) · [`rcSrClearingTheRequestManagerIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L89)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6105`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrSetRequestManagerIsReachable rcSrClearingTheRequestManagerIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -104,7 +104,7 @@
     /// @inheritdoc ISpokeRegistry
     function setRequestManager(PoolId poolId, ISpokeRequestManager manager_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        requestManager[poolId] = manager_;
+        // MUTATION: the request manager row is never written
         emit SetRequestManager(poolId, manager_);
     }
 
```

## SpokeRegistry #6106

The manager seat is stored as the opposite of what the call asks for, so granting takes the seat away and revoking hands it out.

- **Mutant:** [`6106.sol`](6106.sol)
- **Caught by:** [`rcSrGrantingOneManagerSeatIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L103) · [`rcSrRevokingOneOfTwoManagerSeatsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L119)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6106`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrGrantingOneManagerSeatIsReachable rcSrRevokingOneOfTwoManagerSeatsIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -140,7 +140,8 @@
     /// @inheritdoc ISpokeRegistry
     function updateManager(PoolId poolId, address who, bool canManage) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        manager[poolId][who] = canManage;
+        // MUTATION: the seat is stored as the negation of the flag the call carries
+        manager[poolId][who] = !canManage;
         emit UpdateManager(poolId, who, canManage);
     }
 
```

## SpokeRegistry #6107

The bridger seat is stored as the opposite of what the call asks for, so granting takes the seat away and revoking hands it out.

- **Mutant:** [`6107.sol`](6107.sol)
- **Caught by:** [`rcSrGrantingTheBridgerSeatAloneIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L136) · [`rcSrRevokingOneOfTwoBridgerSeatsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L705)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6107`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrGrantingTheBridgerSeatAloneIsReachable rcSrRevokingOneOfTwoBridgerSeatsIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -147,7 +147,8 @@
     /// @inheritdoc ISpokeRegistry
     function updateBridger(PoolId poolId, address who, bool canBridge) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        bridger[poolId][who] = canBridge;
+        // MUTATION: the seat is stored as the negation of the flag the call carries
+        bridger[poolId][who] = !canBridge;
         emit UpdateBridger(poolId, who, canBridge);
     }
 
```

## SpokeRegistry #6108

Installing a policy no longer advances its nonce, so reinstalling a policy revives the grants of its earlier tenure.

- **Mutant:** [`6108.sol`](6108.sol)
- **Caught by:** [`rcSrFirstPolicyInstallIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L152)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6108`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrFirstPolicyInstallIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -158,7 +158,8 @@
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        // MUTATION: the tenure counter stays where it stands
+        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce);
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeRegistry #6109

Installing a policy is refused on any pool that already carries one, so a sitting policy can never be replaced and never cleared.

- **Mutant:** [`6109.sol`](6109.sol)
- **Caught by:** [`rcSrPolicyReplacementIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L170) · [`rcSrClearingThePolicyIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6109`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrPolicyReplacementIsReachable rcSrClearingThePolicyIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -157,7 +157,8 @@
 
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
-        require(isPoolActive(poolId), InvalidPool());
+        // MUTATION: the gate also refuses a pool that already carries a policy
+        require(isPoolActive(poolId) && address(_policy[poolId].policy) == address(0), InvalidPool());
         _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
         emit SetPolicy(poolId, policy_);
     }
```

## SpokeRegistry #6110

A granted authorization is announced but never counted, so nothing can ever spend it.

- **Mutant:** [`6110.sol`](6110.sol)
- **Caught by:** [`rcSrAuthorizeIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L205)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6110`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrAuthorizeIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -168,7 +168,7 @@
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
-        authorizations[id]++;
+        // MUTATION: the grant is never counted
         emit AuthorizationGranted(poolId, id, data);
     }
 
```

## SpokeRegistry #6111

A revocation leaves the ledger row standing, so a grant survives the call that was meant to withdraw it.

- **Mutant:** [`6111.sol`](6111.sol)
- **Caught by:** [`rcSrUnauthorizeEmptyingTheRowIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L240) · [`rcSrPolicySwapPuttingGrantsBeyondRevocationIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L302)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6111`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrUnauthorizeEmptyingTheRowIsReachable rcSrPolicySwapPuttingGrantsBeyondRevocationIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -179,7 +179,8 @@
         uint256 count = authorizations[id];
         require(count != 0, NoOutstandingAuthorization());
 
-        authorizations[id] = count - 1;
+        // MUTATION: the revocation leaves the count standing
+        authorizations[id] = count;
         emit AuthorizationRevoked(poolId, id, data);
     }
 
```

## SpokeRegistry #6112

The policy spends a grant without taking it off the ledger, so one authorization can be used over and over.

- **Mutant:** [`6112.sol`](6112.sol)
- **Caught by:** [`rcSrPolicyConsumingAGrantIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L261) · [`rcSrConsumingOneOfTwoGrantsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L282)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6112`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrPolicyConsumingAGrantIsReachable rcSrConsumingOneOfTwoGrantsIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -192,7 +192,8 @@
         uint256 count = authorizations[id];
         require(count != 0, NoOutstandingAuthorization());
 
-        authorizations[id] = count - 1;
+        // MUTATION: the spend leaves the count standing
+        authorizations[id] = count;
         emit AuthorizationConsumed(poolId, caller, id);
     }
 
```

## SpokeRegistry #6113

Numbering an asset leaves the issuing counter where it stands, so every asset of one origin chain is handed the very same number.

- **Mutant:** [`6113.sol`](6113.sol)
- **Caught by:** [`rcSrFirstAssetNumberIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L325) · [`rcSrSecondAssetPairTakingItsOwnNumberIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L345)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6113`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrFirstAssetNumberIsReachable rcSrSecondAssetPairTakingItsOwnNumberIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -310,7 +310,7 @@
         require(centrifugeId != 0, InvalidCentrifugeId());
         require(_assetToId[asset][tokenId].isNull(), AssetAlreadyRegistered());
 
-        _assetCounter++;
+        // MUTATION: the issuing counter never advances
         assetId = newAssetId(centrifugeId, _assetCounter);
 
         _idToAsset[assetId] = AssetIdKey(asset, tokenId);
```

## SpokeRegistry #6114

Numbering now refuses any nonzero token id, so a token inside a multi token contract never gets an asset number.

- **Mutant:** [`6114.sol`](6114.sol)
- **Caught by:** [`rcSrNumberingAMultiTokenAssetPairIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L367)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6114`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrNumberingAMultiTokenAssetPairIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -308,7 +308,8 @@
     {
         require(asset != address(0), UnknownAsset());
         require(centrifugeId != 0, InvalidCentrifugeId());
-        require(_assetToId[asset][tokenId].isNull(), AssetAlreadyRegistered());
+        // MUTATION: the gate also refuses any pair that names a token id
+        require(_assetToId[asset][tokenId].isNull() && tokenId == 0, AssetAlreadyRegistered());
 
         _assetCounter++;
         assetId = newAssetId(centrifugeId, _assetCounter);
```

## SpokeRegistry #6115

Numbering is refused on the smallest legal origin chain, so the low end of the chain namespace is unusable.

- **Mutant:** [`6115.sol`](6115.sol)
- **Caught by:** [`rcSrAssetNumberOnTheSmallestOriginChainIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L384)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6115`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrAssetNumberOnTheSmallestOriginChainIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -307,7 +307,8 @@
         returns (AssetId assetId)
     {
         require(asset != address(0), UnknownAsset());
-        require(centrifugeId != 0, InvalidCentrifugeId());
+        // MUTATION: the smallest legal origin chain is refused alongside the null one
+        require(centrifugeId > 1, InvalidCentrifugeId());
         require(_assetToId[asset][tokenId].isNull(), AssetAlreadyRegistered());
 
         _assetCounter++;
```

## SpokeRegistry #6116

Numbering an asset files only the forward row, so the pair can never be resolved back to the number it was handed.

- **Mutant:** [`6116.sol`](6116.sol)
- **Caught by:** [`rcSrCheckedAssetLookupsAfterNumberingAreReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L401)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6116`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrCheckedAssetLookupsAfterNumberingAreReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -314,7 +314,7 @@
         assetId = newAssetId(centrifugeId, _assetCounter);
 
         _idToAsset[assetId] = AssetIdKey(asset, tokenId);
-        _assetToId[asset][tokenId] = assetId;
+        // MUTATION: the reverse lookup is never filed
     }
 
     /// @inheritdoc ISpokeRegistry
```

## SpokeRegistry #6117

Registering a vault puts it into service straight away, so a vault starts routing investor flows before anyone links it.

- **Mutant:** [`6117.sol`](6117.sol)
- **Caught by:** [`rcSrRegisterVaultIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L420) · [`rcSrRegisterMultiTokenVaultIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L442)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6117`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrRegisterVaultIsReachable rcSrRegisterMultiTokenVaultIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -246,7 +246,8 @@
         require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
         require(vault_.code.length > 0, NotAContract());
 
-        _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
+        // MUTATION: the vault row enters already in service
+        _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, true);
         emit DeployVault(poolId, scId, asset, tokenId, factory, vault_, payload);
     }
 
```

## SpokeRegistry #6118

Linking a vault never switches its service flag on, so a vault the pool just put into service still reads as out of service.

- **Mutant:** [`6118.sol`](6118.sol)
- **Caught by:** [`rcSrLinkVaultIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L463) · [`rcSrLinkedVaultReadingBackThroughItsViewsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L520) · [`rcSrTwoVaultsLinkedForOneAssetIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L804)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6118`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrLinkVaultIsReachable rcSrLinkedVaultReadingBackThroughItsViewsIsReachable rcSrTwoVaultsLinkedForOneAssetIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -261,7 +261,7 @@
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
-        vaultDetails_.isLinked = true;
+        // MUTATION: service is never switched on
 
         emit LinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeRegistry #6119

Unlinking a vault never switches its service flag off, so service can never be withdrawn from a live vault.

- **Mutant:** [`6119.sol`](6119.sol)
- **Caught by:** [`rcSrUnlinkVaultIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L479) · [`rcSrWithdrawingAndRestoringVaultServiceIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L495)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6119`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrUnlinkVaultIsReachable rcSrWithdrawingAndRestoringVaultServiceIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -276,7 +276,7 @@
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
-        vaultDetails_.isLinked = false;
+        // MUTATION: service is never switched off
 
         emit UnlinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeRegistry #6120

The share price gate turns strict, so a quote can never be corrected at the stamp it already carries.

- **Mutant:** [`6120.sol`](6120.sol)
- **Caught by:** [`rcSrSharePriceCorrectionAtTheSameStampIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L573)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6120`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrSharePriceCorrectionAtTheSameStampIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -354,7 +354,8 @@
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
-        require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
+        // MUTATION: the stamp gate turns strict and refuses the stamp already carried
+        require(computedAt > poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
         poolPerShare.computedAt = computedAt;
```

## SpokeRegistry #6121

A share price update stores the quote but not its stamp, so the class keeps reading as never priced.

- **Mutant:** [`6121.sol`](6121.sol)
- **Caught by:** [`rcSrFirstSharePriceIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L538) · [`rcSrSharePriceMovingToALaterStampIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L556) · [`rcSrCheckedSharePriceReadAfterAWriteIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L611)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6121`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrFirstSharePriceIsReachable rcSrSharePriceMovingToALaterStampIsReachable rcSrCheckedSharePriceReadAfterAWriteIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -357,7 +357,7 @@
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
-        poolPerShare.computedAt = computedAt;
+        // MUTATION: the stamp of the quote is never written
         emit UpdateSharePrice(poolId, scId, price, computedAt);
     }
 
```

## SpokeRegistry #6122

An asset price update stores the quote but not its stamp, so the asset keeps reading as never priced.

- **Mutant:** [`6122.sol`](6122.sol)
- **Caught by:** [`rcSrFirstAssetPriceIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L592) · [`rcSrCheckedAssetPriceReadAfterAWriteIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L627)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6122`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrFirstAssetPriceIsReachable rcSrCheckedAssetPriceReadAfterAWriteIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -374,7 +374,7 @@
         require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
 
         poolPerAsset.price = price;
-        poolPerAsset.computedAt = computedAt;
+        // MUTATION: the stamp of the quote is never written
         emit UpdateAssetPrice(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, price, computedAt);
     }
 
```

## SpokeRegistry #6123

Revoking authority clears the caller's own seat instead of the named account's, so the target keeps its rights.

- **Mutant:** [`6123.sol`](6123.sol)
- **Caught by:** [`rcSrDenyLeavingTheCallersOwnSeatIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L665)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6123`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrDenyLeavingTheCallersOwnSeatIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,8 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        // MUTATION: the withdrawal lands on the caller instead of the named account
+        wards[msg.sender] = 0;
         emit Deny(user);
     }
 }
```

## SpokeRegistry #6124

A grant latches the ledger row at one, so authorizing the same call twice records only a single outstanding grant.

- **Mutant:** [`6124.sol`](6124.sol)
- **Caught by:** [`rcSrTwoOutstandingGrantsAreReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L223)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 6124`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrTwoOutstandingGrantsAreReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -168,7 +168,8 @@
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
-        authorizations[id]++;
+        // MUTATION: the row is latched at one grant instead of accumulating
+        authorizations[id] = 1;
         emit AuthorizationGranted(poolId, id, data);
     }
 
```

## SpokeRegistry #8630

A share price update no longer refuses a stamp later than the current block, so a future quote is stored and honest updates are refused as older until then.

- **Mutant:** [`8630.sol`](8630.sol)
- **Caught by:** [`sharePriceStampNotFuture`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L283)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8630`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule sharePriceStampNotFuture`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -353,7 +353,7 @@
     function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard is removed, so a share price stamped ahead of the clock lands
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
```

## SpokeRegistry #8631

An asset price update no longer refuses a stamp later than the current block, so a future quote is stored and honest updates are refused as older until then.

- **Mutant:** [`8631.sol`](8631.sol)
- **Caught by:** [`assetPriceStampNotFuture`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L288)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8631`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule assetPriceStampNotFuture`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -370,7 +370,7 @@
         require(isRegistered(assetId), UnknownAsset());
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard is removed, so an asset price stamped ahead of the clock lands
         require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
 
         poolPerAsset.price = price;
```

## SpokeRegistry #8632

A share price update refuses a stamp equal to the current block time, so a quote computed in the block it is relayed in is refused.

- **Mutant:** [`8632.sol`](8632.sol)
- **Caught by:** [`rvSrHonestSharePriceUpdateIsAccepted`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L427)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8632`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrHonestSharePriceUpdateIsAccepted`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -353,7 +353,8 @@
     function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard turns strict and refuses a price stamped in the current block
+        require(computedAt < block.timestamp, CannotSetFuturePrice());
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
```

## SpokeRegistry #8633

An asset price update refuses a stamp equal to the current block time, so a quote computed in the block it is relayed in is refused.

- **Mutant:** [`8633.sol`](8633.sol)
- **Caught by:** [`rvSrHonestAssetPriceUpdateIsAccepted`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L445)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8633`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrHonestAssetPriceUpdateIsAccepted`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -370,7 +370,8 @@
         require(isRegistered(assetId), UnknownAsset());
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard turns strict and refuses a price stamped in the current block
+        require(computedAt < block.timestamp, CannotSetFuturePrice());
         require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
 
         poolPerAsset.price = price;
```

## SpokeRegistry #8634

A share price update accepts a stamp one second past the current block time, so a quote from just ahead of the block lands.

- **Mutant:** [`8634.sol`](8634.sol)
- **Caught by:** [`rvSrSharePriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L464)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8634`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrSharePriceStampedAheadOfTheClockIsRefused`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -353,7 +353,8 @@
     function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard lets a price one second ahead of the clock through
+        require(computedAt <= block.timestamp + 1, CannotSetFuturePrice());
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
```

## SpokeRegistry #8635

An asset price update accepts a stamp one second past the current block time, so a quote from just ahead of the block lands.

- **Mutant:** [`8635.sol`](8635.sol)
- **Caught by:** [`rvSrAssetPriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L476)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8635`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrAssetPriceStampedAheadOfTheClockIsRefused`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -370,7 +370,8 @@
         require(isRegistered(assetId), UnknownAsset());
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard lets a price one second ahead of the clock through
+        require(computedAt <= block.timestamp + 1, CannotSetFuturePrice());
         require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
 
         poolPerAsset.price = price;
```

## SpokeRegistry #8921

A share price update no longer refuses a stamp later than the current block, so a quote from the future is accepted.

- **Mutant:** [`8921.sol`](8921.sol)
- **Caught by:** [`rvSrSharePriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L464)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8921`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrSharePriceStampedAheadOfTheClockIsRefused`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -353,7 +353,7 @@
     function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard is removed, so a share price stamped ahead of the clock lands
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
```

## SpokeRegistry #8922

An asset price update no longer refuses a stamp later than the current block, so a quote from the future is accepted.

- **Mutant:** [`8922.sol`](8922.sol)
- **Caught by:** [`rvSrAssetPriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L476)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8922`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrAssetPriceStampedAheadOfTheClockIsRefused`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -370,7 +370,7 @@
         require(isRegistered(assetId), UnknownAsset());
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard is removed, so an asset price stamped ahead of the clock lands
         require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
 
         poolPerAsset.price = price;
```

## SpokeRegistry #8923

registerVault checks the vault only against the zero address, so an address without code can be registered as a vault.

- **Mutant:** [`8923.sol`](8923.sol)
- **Caught by:** [`onlyADeployedContractHoldsAVaultRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_valid_state.spec#L293)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8923`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/valid_state.conf --rule onlyADeployedContractHoldsAVaultRow`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -244,7 +244,8 @@
         require(assetIdKey.asset == asset && assetIdKey.tokenId == tokenId, UnknownAsset());
 
         require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
-        require(vault_.code.length > 0, NotAContract());
+        // MUTATION: the deployed contract check shrinks to a zero address check
+        require(vault_ != address(0), NotAContract());
 
         _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
         emit DeployVault(poolId, scId, asset, tokenId, factory, vault_, payload);
```

## SpokeRegistry #8924

registerVault refuses a taken vault only when the same pool names it, so another pool can take over a vault already registered.

- **Mutant:** [`8924.sol`](8924.sol)
- **Caught by:** [`stSrRegisteredVaultIsNeverTakenByAnotherPool`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L98)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8924`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/two_keys_properties.conf --rule stSrRegisteredVaultIsNeverTakenByAnotherPool`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -243,7 +243,8 @@
         require(assetIdKey.asset != address(0), UnknownAsset());
         require(assetIdKey.asset == asset && assetIdKey.tokenId == tokenId, UnknownAsset());
 
-        require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
+        // MUTATION: a vault already registered is refused only to its own pool
+        require(_vaultDetails[vault_].asset == address(0) || !(_vaultDetails[vault_].poolId == poolId), AlreadyRegisteredVault());
         require(vault_.code.length > 0, NotAContract());
 
         _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
```

## SpokeRegistry #8925

unlinkVault also demands the vault sit on token id zero, so a linked vault of a multi token asset can never be unlinked.

- **Mutant:** [`8925.sol`](8925.sol)
- **Caught by:** [`rvSrUnlinkVaultIsNeverRefusedForALinkedVaultFiledUnderItsIds`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L488)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8925`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrUnlinkVaultIsNeverRefusedForALinkedVaultFiledUnderItsIds`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -273,7 +273,8 @@
 
         VaultDetails storage vaultDetails_ = _vaultDetails[vault_];
         require(vaultDetails_.isLinked, AlreadyUnlinkedVault());
-        require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
+        // MUTATION: unlinking also demands token id zero, a multi token vault stays in service
+        require(vaultDetails_.assetId.raw() == assetId.raw() && vaultDetails_.tokenId == 0, UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
         vaultDetails_.isLinked = false;
```

## SpokeRegistry #8926

setRequestManager refuses a pool that already has a request manager, so an installed manager can be neither replaced nor cleared.

- **Mutant:** [`8926.sol`](8926.sol)
- **Caught by:** [`rvSrSetRequestManagerIsNeverRefusedForAWardOnAnOpenedPool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L509)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8926`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrSetRequestManagerIsNeverRefusedForAWardOnAnOpenedPool`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -103,7 +103,8 @@
 
     /// @inheritdoc ISpokeRegistry
     function setRequestManager(PoolId poolId, ISpokeRequestManager manager_) external auth {
-        require(isPoolActive(poolId), InvalidPool());
+        // MUTATION: a request manager, once installed, locks the entry
+        require(isPoolActive(poolId) && address(requestManager[poolId]) == address(0), InvalidPool());
         requestManager[poolId] = manager_;
         emit SetRequestManager(poolId, manager_);
     }
```

## SpokeRegistry #8927

linkVault records every link in one shared flag, so after one vault is linked no second vault can be linked anywhere.

- **Mutant:** [`8927.sol`](8927.sol)
- **Caught by:** [`rcSrTwoVaultsLinkedForOneAssetIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L804)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 8927`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrTwoVaultsLinkedForOneAssetIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -256,7 +256,9 @@
         require(assetIdKey.asset != address(0), UnknownAsset());
 
         VaultDetails storage vaultDetails_ = _vaultDetails[vault_];
-        require(!vaultDetails_.isLinked, AlreadyLinkedVault());
+        // MUTATION: one latch for every vault, a second link is refused as already linked
+        require(!vaultDetails_.isLinked && !_vaultDetails[address(0)].isLinked, AlreadyLinkedVault());
+        _vaultDetails[address(0)].isLinked = true;
         require(vaultDetails_.asset != address(0), UnknownVault());
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
```

## SpokeRegistry #9031

unlinking a vault also unlinks the caller's own entry, so one unlink can take a second vault out of service.

- **Mutant:** [`9031.sol`](9031.sol)
- **Caught by:** [`stSrAtMostOneVaultLinkMovesPerCall`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L255)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9031`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrAtMostOneVaultLinkMovesPerCall`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -276,7 +276,7 @@
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
-        vaultDetails_.isLinked = false;
+        vaultDetails_.isLinked = false; _vaultDetails[msg.sender].isLinked = false; // MUTATION: the unlink also clears the caller's own link
 
         emit UnlinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeRegistry #9067

A share price update stamps its local arrival time, not the hub's computation time, so the quote's age is wrong.

- **Mutant:** [`9067.sol`](9067.sol)
- **Caught by:** [`hlSrShareQuoteIsStoredExactlyAsSent`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L118)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9067`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrShareQuoteIsStoredExactlyAsSent`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -357,7 +357,7 @@
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
-        poolPerShare.computedAt = computedAt;
+        poolPerShare.computedAt = uint64(block.timestamp); // MUTATION: the quote is stamped with its arrival time, not the hub's computation time
         emit UpdateSharePrice(poolId, scId, price, computedAt);
     }
 
```

## SpokeRegistry #9068

A share class is bound with the token's own address as registrar, so mint authority is not the named registrar.

- **Mutant:** [`9068.sol`](9068.sol)
- **Caught by:** [`hlSrShareClassBindsExactlyTheTokenAndRegistrarNamed`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L132)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9068`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrShareClassBindsExactlyTheTokenAndRegistrarNamed`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -96,7 +96,7 @@
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
         shareClass_.shareToken = IERC20(shareToken_);
-        shareClass_.registrar = registrar_;
+        shareClass_.registrar = IRegistrar(shareToken_); // MUTATION: copy-paste of the token line binds the token's own address as registrar
         tokenDetails[shareToken_] = TokenDetails(poolId, scId);
         emit AddShareClass(poolId, scId, shareToken_, registrar_);
     }
```

## SpokeRegistry #9069

addPool records the block number instead of the block time, so the pool's creation stamp is not when it opened.

- **Mutant:** [`9069.sol`](9069.sol)
- **Caught by:** [`hlSrAddedPoolIsStampedWithTheBlockTime`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L154)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9069`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrAddedPoolIsStampedWithTheBlockTime`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -63,7 +63,7 @@
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
         require(pool_.createdAt == 0, PoolAlreadyAdded());
-        pool_.createdAt = uint64(block.timestamp);
+        pool_.createdAt = uint64(block.number); // MUTATION: the pool is stamped with the block number instead of the block time
 
         emit AddPool(poolId);
     }
```

## SpokeRegistry #9070

registerVault stores a new vault already linked, so a vault goes live without ever passing through linkVault.

- **Mutant:** [`9070.sol`](9070.sol)
- **Caught by:** [`vtSrVaultLinkMovesOnlyOnLinkOrUnlink`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L130)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9070`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule vtSrVaultLinkMovesOnlyOnLinkOrUnlink`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -246,7 +246,7 @@
         require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
         require(vault_.code.length > 0, NotAContract());
 
-        _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
+        _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, true); // MUTATION: a freshly registered vault is stored already linked
         emit DeployVault(poolId, scId, asset, tokenId, factory, vault_, payload);
     }
 
```

## SpokeRegistry #9200

addPool no longer refuses the null pool id, so a ward can open pool zero and give it an activation stamp.

- **Mutant:** [`9200.sol`](9200.sol)
- **Caught by:** [`rvSrAddPoolRefusesTheNullPool`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L399)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9200`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrAddPoolRefusesTheNullPool`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -60,7 +60,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function addPool(PoolId poolId) external auth {
-        require(!poolId.isNull(), InvalidPool());
+        // MUTATION: the null pool check is removed
         Pool storage pool_ = pool[poolId];
         require(pool_.createdAt == 0, PoolAlreadyAdded());
         pool_.createdAt = uint64(block.timestamp);
```

## SpokeRegistry #9202

A token swap clears the incoming token's lookup, not the outgoing one's, so the retired token still maps to the class.

- **Mutant:** [`9202.sol`](9202.sol)
- **Caught by:** [`hlSrTokenSwapDeletesTheOutgoingTokensRow`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L168)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9202`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrTokenSwapDeletesTheOutgoingTokensRow`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -91,7 +91,7 @@
         // Retire the outgoing token's reverse lookup before the uniqueness check, so relinking the same
         // token with a new registrar is allowed (swap the registrar, keep the token address). Reordered
         // relative to the check so the same-token case does not trip TokenAlreadyRegistered on itself.
-        if (address(shareClass_.shareToken) != address(0)) delete tokenDetails[address(shareClass_.shareToken)];
+        if (address(shareClass_.shareToken) != address(0)) delete tokenDetails[shareToken_]; // MUTATION: the incoming token's row is cleared, not the outgoing one
 
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
```

## SpokeRegistry #9203

granting or withdrawing the bridger seat also sets the manager seat of the same account, so the two roles are no longer independent.

- **Mutant:** [`9203.sol`](9203.sol)
- **Caught by:** [`stSrRoleSeatsMoveOnlyOnTheirOwnWriter`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_transitions.spec#L271)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9203`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/transitions.conf --rule stSrRoleSeatsMoveOnlyOnTheirOwnWriter`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -147,7 +147,7 @@
     /// @inheritdoc ISpokeRegistry
     function updateBridger(PoolId poolId, address who, bool canBridge) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        bridger[poolId][who] = canBridge;
+        bridger[poolId][who] = canBridge; manager[poolId][who] = canBridge; // MUTATION: the bridger writer moves the manager seat too
         emit UpdateBridger(poolId, who, canBridge);
     }
 
```

## SpokeRegistry #9204

the checked share price read refuses quotes older than one day, so core enforces a freshness window it is documented not to have.

- **Mutant:** [`9204.sol`](9204.sol)
- **Caught by:** [`rcSrYearOldSharePriceIsAcceptedAndServedIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L722)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9204`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrYearOldSharePriceIsAcceptedAndServedIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -381,7 +381,7 @@
     /// @inheritdoc ISpokeRegistry
     function pricePoolPerShare(PoolId poolId, ShareClassId scId, bool checkValidity) public view returns (D18 price) {
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
-        require(!checkValidity || poolPerShare.isValid(), InvalidPrice());
+        require(!checkValidity || (poolPerShare.isValid() && block.timestamp - poolPerShare.computedAt <= 1 days), InvalidPrice()); // MUTATION: a one day freshness window
 
         return poolPerShare.price;
     }
```

## SpokeRegistry #9206

linking a share token also wipes the class's share price, so a token swap resets the price the class already carried.

- **Mutant:** [`9206.sol`](9206.sol)
- **Caught by:** [`rcSrTokenSwapKeepsTheStandingSharePriceIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L738)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9206`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrTokenSwapKeepsTheStandingSharePriceIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -95,7 +95,7 @@
 
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
-        shareClass_.shareToken = IERC20(shareToken_);
+        shareClass_.shareToken = IERC20(shareToken_); shareClass_.pricePoolPerShare.price = D18.wrap(0); // MUTATION: the token link resets the share price
         shareClass_.registrar = registrar_;
         tokenDetails[shareToken_] = TokenDetails(poolId, scId);
         emit AddShareClass(poolId, scId, shareToken_, registrar_);
```

## SpokeRegistry #9207

an asset quote older than the class's share quote is now refused, so the two prices are forced into one order.

- **Mutant:** [`9207.sol`](9207.sol)
- **Caught by:** [`rcSrSharePriceLandsWithoutItsAssetPriceAndAnOlderAssetQuoteFollowsIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L756)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9207`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrSharePriceLandsWithoutItsAssetPriceAndAnOlderAssetQuoteFollowsIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -371,7 +371,7 @@
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
-        require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
+        require(computedAt >= poolPerAsset.computedAt && computedAt >= shareClass[poolId][scId].pricePoolPerShare.computedAt, CannotSetOlderPrice()); // MUTATION: the asset quote is ordered after the share quote
 
         poolPerAsset.price = price;
         poolPerAsset.computedAt = computedAt;
```

## SpokeRegistry #9208

a consumption keys the grant by the named caller instead of the policy, so only the policy itself can be named as caller.

- **Mutant:** [`9208.sol`](9208.sol)
- **Caught by:** [`rcSrOneGrantKeyIsSpentUnderTwoDistinctCallersIsReachable`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reachability.spec#L779)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9208`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reachability.conf --rule rcSrOneGrantKeyIsSpentUnderTwoDistinctCallersIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -188,7 +188,7 @@
         PolicyInfo memory info = _policy[poolId];
         require(msg.sender == address(info.policy), CallerNotPolicy());
 
-        bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId, caller, info.nonce, data); // MUTATION: the grant key is scoped to the named caller
         uint256 count = authorizations[id];
         require(count != 0, NoOutstandingAuthorization());
 
```

## SpokeRegistry #9209

A consumption now also requires the named caller to be the policy, so no grant can be spent for another caller.

- **Mutant:** [`9209.sol`](9209.sol)
- **Caught by:** [`rvSrStandingGrantIsSpendableUnderAnyNamedCaller`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_reverts.spec#L410)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9209`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/reverts.conf --rule rvSrStandingGrantIsSpendableUnderAnyNamedCaller`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -186,7 +186,7 @@
     /// @inheritdoc ISpokeRegistry
     function consumeAuthorization(PoolId poolId, address caller, bytes calldata data) external {
         PolicyInfo memory info = _policy[poolId];
-        require(msg.sender == address(info.policy), CallerNotPolicy());
+        require(msg.sender == address(info.policy) && caller == msg.sender, CallerNotPolicy()); // MUTATION: the grant is spendable only for the policy as caller
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
         uint256 count = authorizations[id];
```

## SpokeRegistry #9210

linking a vault also marks the vault at the neighbouring address as linked, so an operation on one vault reaches another vault's link.

- **Mutant:** [`9210.sol`](9210.sol)
- **Caught by:** [`hlSrLinkCallMovesOnlyItsOwnVaultsFlag`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L200)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9210`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrLinkCallMovesOnlyItsOwnVaultsFlag`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -262,6 +262,7 @@
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
         vaultDetails_.isLinked = true;
+        _vaultDetails[address(uint160(vault_) ^ 1)].isLinked = true; // MUTATION: linking one vault also links its neighbouring address
 
         emit LinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeRegistry #9241

linking a vault also writes the share token's vault pointer for the asset, so a link can no longer leave the pointer unset.

- **Mutant:** [`9241.sol`](9241.sol)
- **Caught by:** [`rcShLinkLeavesTheTokenVaultPointerUnset`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/SpokeHandler_LinkedSpokeRegistry_vault_pointer_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9241`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/vault_pointer_properties.conf --rule rcShLinkLeavesTheTokenVaultPointerUnset`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -262,6 +262,7 @@
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
         vaultDetails_.isLinked = true;
+        (bool ok,) = address(shareClass[poolId][scId].shareToken).call(abi.encodeWithSelector(bytes4(0x1b451d28), assetIdKey.asset, vault_)); require(ok); // MUTATION: linking also points the share token at the vault
 
         emit LinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeRegistry #9242

unlinking a vault also clears the share token's vault pointer, so an unlink no longer leaves the token naming it.

- **Mutant:** [`9242.sol`](9242.sol)
- **Caught by:** [`rcShUnlinkLeavesTheTokenPointingAtTheUnlinkedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/SpokeHandler_LinkedSpokeRegistry_vault_pointer_properties.spec#L30)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9242`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/vault_pointer_properties.conf --rule rcShUnlinkLeavesTheTokenPointingAtTheUnlinkedVault`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -277,6 +277,7 @@
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
         vaultDetails_.isLinked = false;
+        (bool ok,) = address(shareClass[poolId][scId].shareToken).call(abi.encodeWithSelector(bytes4(0x1b451d28), assetIdKey.asset, address(0))); require(ok); // MUTATION: unlinking also clears the share token's vault pointer
 
         emit UnlinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeRegistry #9243

linking a vault also writes the share token's vault pointer for the asset, so a link message reaches into the token.

- **Mutant:** [`9243.sol`](9243.sol)
- **Caught by:** [`hlShLinkAndUnlinkNeverTouchATokenVaultPointer`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L322)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9243`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShLinkAndUnlinkNeverTouchATokenVaultPointer`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -262,6 +262,7 @@
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
         vaultDetails_.isLinked = true;
+        (bool ok,) = address(shareClass[poolId][scId].shareToken).call(abi.encodeWithSelector(bytes4(0x1b451d28), assetIdKey.asset, vault_)); require(ok); // MUTATION: linking also points the share token at the vault
 
         emit LinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeRegistry #9560

the check that the incoming token owns no lookup row is dropped, so a class can adopt a token another class holds.

- **Mutant:** [`9560.sol`](9560.sol)
- **Caught by:** [`twoClassKeysNeverShareAToken`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L60)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9560`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/two_keys_properties.conf --rule twoClassKeysNeverShareAToken`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -93,7 +93,7 @@
         // relative to the check so the same-token case does not trip TokenAlreadyRegistered on itself.
         if (address(shareClass_.shareToken) != address(0)) delete tokenDetails[address(shareClass_.shareToken)];
 
-        require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
+        // MUTATION: the incoming token is no longer checked against the lookup rows of other classes
 
         shareClass_.shareToken = IERC20(shareToken_);
         shareClass_.registrar = registrar_;
```

## SpokeRegistry #9561

the lookup row written for a linked token keeps only its pool half, so the token no longer resolves to its own share class.

- **Mutant:** [`9561.sol`](9561.sol)
- **Caught by:** [`classTokenResolvesBack`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L39)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9561`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/two_keys_properties.conf --rule classTokenResolvesBack`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -97,7 +97,7 @@
 
         shareClass_.shareToken = IERC20(shareToken_);
         shareClass_.registrar = registrar_;
-        tokenDetails[shareToken_] = TokenDetails(poolId, scId);
+        tokenDetails[shareToken_].poolId = poolId; // MUTATION: the lookup row loses its class half
         emit AddShareClass(poolId, scId, shareToken_, registrar_);
     }
 
```

## SpokeRegistry #9562

a token swap never retires the outgoing token's lookup row, so the retired token still resolves to a class that no longer holds it.

- **Mutant:** [`9562.sol`](9562.sol)
- **Caught by:** [`lookupRowPointsBack`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L50)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9562`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/two_keys_properties.conf --rule lookupRowPointsBack`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -91,7 +91,7 @@
         // Retire the outgoing token's reverse lookup before the uniqueness check, so relinking the same
         // token with a new registrar is allowed (swap the registrar, keep the token address). Reordered
         // relative to the check so the same-token case does not trip TokenAlreadyRegistered on itself.
-        if (address(shareClass_.shareToken) != address(0)) delete tokenDetails[address(shareClass_.shareToken)];
+        if (address(shareClass_.shareToken) != address(0)) {} // MUTATION: the outgoing token's lookup row is never retired
 
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
```

## SpokeRegistry #9563

the deployed contract check on the linked token always passes, so the zero address can be linked and claims a lookup row.

- **Mutant:** [`9563.sol`](9563.sol)
- **Caught by:** [`nullAddressOwnsNoLookupRowOnAnyKey`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L72)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9563`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/two_keys_properties.conf --rule nullAddressOwnsNoLookupRowOnAnyKey`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -84,7 +84,7 @@
 
     function _linkToken(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) internal {
         // Must already be deployed, so a registrar cannot reserve another pool's future token address
-        require(shareToken_.code.length > 0, NotAContract());
+        require(shareToken_.code.length >= 0, NotAContract()); // MUTATION: the deployed contract check always passes
         require(address(registrar_) != address(0), EmptyRegistrar());
 
         ShareClassDetails storage shareClass_ = shareClass[poolId][scId];
```

## SpokeRegistry #9564

linking a token writes the neighbouring class's row instead of the named one, so the token looks up to a class not holding it.

- **Mutant:** [`9564.sol`](9564.sol)
- **Caught by:** [`classTokenResolvesBack`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L39) · [`lookupRowPointsBack`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L50)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9564`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/two_keys_properties.conf --rule classTokenResolvesBack lookupRowPointsBack`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -87,7 +87,7 @@
         require(shareToken_.code.length > 0, NotAContract());
         require(address(registrar_) != address(0), EmptyRegistrar());
 
-        ShareClassDetails storage shareClass_ = shareClass[poolId][scId];
+        ShareClassDetails storage shareClass_ = shareClass[poolId][ShareClassId.wrap(scId.raw() ^ bytes16(uint128(1)))]; // MUTATION: the link lands on the neighbouring class's row
         // Retire the outgoing token's reverse lookup before the uniqueness check, so relinking the same
         // token with a new registrar is allowed (swap the registrar, keep the token address). Reordered
         // relative to the check so the same-token case does not trip TokenAlreadyRegistered on itself.
```

## SpokeRegistry #9565

a manager grant or revoke is written on the neighbouring pool's seat instead of the named pool's.

- **Mutant:** [`9565.sol`](9565.sol)
- **Caught by:** [`hlSrRoleGrantLandsOnTheNamedPoolOnly`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L119)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9565`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/two_keys_properties.conf --rule hlSrRoleGrantLandsOnTheNamedPoolOnly`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -140,7 +140,7 @@
     /// @inheritdoc ISpokeRegistry
     function updateManager(PoolId poolId, address who, bool canManage) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        manager[poolId][who] = canManage;
+        manager[PoolId.wrap(poolId.raw() ^ 1)][who] = canManage; // MUTATION: the manager seat is written on the neighbouring pool
         emit UpdateManager(poolId, who, canManage);
     }
 
```

## SpokeRegistry #9566

a manager grant or revoke also lands on the same account's seat in the neighbouring pool, so one call moves two pools' rosters.

- **Mutant:** [`9566.sol`](9566.sol)
- **Caught by:** [`stSrRoleSeatsArePerPool`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L79)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9566`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/two_keys_properties.conf --rule stSrRoleSeatsArePerPool`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -140,7 +140,7 @@
     /// @inheritdoc ISpokeRegistry
     function updateManager(PoolId poolId, address who, bool canManage) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        manager[poolId][who] = canManage;
+        manager[poolId][who] = canManage; manager[PoolId.wrap(poolId.raw() ^ 1)][who] = canManage; // MUTATION: the manager write also lands on the neighbouring pool
         emit UpdateManager(poolId, who, canManage);
     }
 
```

## SpokeRegistry #9567

linking a token never writes it into the class row, so the class keeps its old token or none.

- **Mutant:** [`9567.sol`](9567.sol)
- **Caught by:** [`rcSrTokenSwapBesideALiveSecondClassIsReachable`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L168) · [`rcSrSecondClassGoesLiveBesideALiveFirstClassIsReachable`](../../specs/core/spoke/SpokeRegistry/SpokeRegistry_two_keys_properties.spec#L147)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9567`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/two_keys_properties.conf --rule rcSrTokenSwapBesideALiveSecondClassIsReachable rcSrSecondClassGoesLiveBesideALiveFirstClassIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -95,7 +95,7 @@
 
         require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
 
-        shareClass_.shareToken = IERC20(shareToken_);
+        // MUTATION: the class row keeps its old token when a new one is linked
         shareClass_.registrar = registrar_;
         tokenDetails[shareToken_] = TokenDetails(poolId, scId);
         emit AddShareClass(poolId, scId, shareToken_, registrar_);
```

## SpokeRegistry #9943

the asset id packs the chain at bit 64 instead of 112, so the decoder reads chain zero from every new id.

- **Mutant:** [`9943.sol`](9943.sol)
- **Caught by:** [`hlSrIssuedAssetIdIsTheChainOverTheCounter`](../../specs/core/spoke/SpokeRegistry/single/SpokeRegistry_high_level.spec#L186)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeRegistry 9943`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeRegistry/high_level.conf --rule hlSrIssuedAssetIdIsTheChainOverTheCounter`

```diff
--- a/src/core/types/AssetId.sol
+++ b/src/core/types/AssetId.sol
@@ -18,7 +18,7 @@
 }
 
 function newAssetId(uint16 centrifugeId_, uint64 counter) pure returns (AssetId) {
-    return AssetId.wrap((uint128(centrifugeId_) << 112) + counter);
+    return AssetId.wrap((uint128(centrifugeId_) << 64) + counter); // MUTATION: the chain is shifted by 64 bits instead of 112
 }
 
 function newAssetId(uint32 isoCode) pure returns (AssetId) {
```

