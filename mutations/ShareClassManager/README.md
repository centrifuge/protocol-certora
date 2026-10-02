# Mutations for `ShareClassManager` (`src/core/hub/ShareClassManager.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/hub/interfaces/IShareClassManager.sol`, `src/core/types/ShareClassId.sol`, `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [401](#shareclassmanager-401) | addShareClass reads the next index without saving the increment, so the pool's class counter never advances.<br>Caught by: [`shareClassExistsIffCounted`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L22) |
| [402](#shareclassmanager-402) | addShareClass never records the new class in the share class registry, leaving a counted and salted class that is not on record.<br>Caught by: [`shareClassExistsIffCounted`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L22) · [`shareClassExistsIffSaltSet`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L27) |
| [403](#shareclassmanager-403) | addShareClass consumes the salt in the global registry but never stores it on the class metadata, so the recorded class carries an empty salt.<br>Caught by: [`shareClassExistsIffSaltSet`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L27) |
| [404](#shareclassmanager-404) | addShareClass stores the salt on the class metadata without marking it consumed in the global salt registry, leaving the stored salt reusable.<br>Caught by: [`classSaltConsumed`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L73) |
| [405](#shareclassmanager-405) | addShareClass accepts a salt whose leading bytes name a foreign pool, so a stored class salt is no longer branded with its own pool id.<br>Caught by: [`saltPrefixIsPool`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L67) · [`nullSaltNeverConsumed`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L78) |
| [406](#shareclassmanager-406) | addShareClass no longer checks the hub registry, so a share class can be created inside a pool that was never registered.<br>Caught by: [`existingClassPoolRegistered`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L52) |
| [407](#shareclassmanager-407) | updateShares skips the share class existence check, so issuance and revocation amounts accumulate on a class that was never created.<br>Caught by: [`uncreatedClassNetworkIssuancesZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L32) · [`uncreatedClassNetworkRevocationsZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L37) |
| [408](#shareclassmanager-408) | updateSharePrice skips the share class existence check, so a price and its timestamp are stored for a class that was never created.<br>Caught by: [`uncreatedClassPriceZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L42) · [`uncreatedClassPriceStampZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L47) |
| [409](#shareclassmanager-409) | updateSharePrice inverts the timestamp gate and accepts prices computed after the current block time, so a stored price stamp can lie in the future.<br>Caught by: [`priceStampNotFuture`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L62) |
| [411](#shareclassmanager-411) | updateShares records a network issuance without adding it to the class total, so total issuance drifts below the per-network net sum.<br>Caught by: [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57) |
| [412](#shareclassmanager-412) | An issuance is recorded on both legs of the network ledger, so a mint also counts as a burn on that chain.<br>Caught by: [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [414](#shareclassmanager-414) | updateSharesPair books one share movement on two networks at once, so a call aimed at one chain moves another chain's ledger.<br>Caught by: [`stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L129) |
| [415](#shareclassmanager-415) | updateSharesForPools books one share movement for two pools at once, so a call aimed at one pool moves another pool's class row and network ledger.<br>Caught by: [`stScClassRowIsPerPool`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_pool_properties.spec#L27) · [`stScNetworkLedgerIsPerPool`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_pool_properties.spec#L67) |
| [416](#shareclassmanager-416) | A new updateSharesForClasses books one share movement on two classes, so a sibling class's totals and ledger move too.<br>Caught by: [`stScClassRowIsPerClass`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L95) · [`stScNetworkLedgerIsPerClass`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L134) |
| [417](#shareclassmanager-417) | addShareClass advances the class counter by two, so the pool's class sequence skips an index.<br>Caught by: [`stScClassCountStepsByOne`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L155) |
| [418](#shareclassmanager-418) | addShareClass never records the new class in the share class registry, so a minted class carries a metadata salt while staying off record.<br>Caught by: [`classSaltSetImpliesRegisteredPerClass`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L25) · [`classWithinCountIsRegistered`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L56) |
| [419](#shareclassmanager-419) | addShareClass never saves the incremented class counter, so a registered class sits at an index beyond the pool's count.<br>Caught by: [`registeredClassIndexWithinCount`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L31) |
| [420](#shareclassmanager-420) | previewNextShareClassId skips an index, so a class is minted at index count+2 while the counter only advances to count+1.<br>Caught by: [`registeredClassIndexWithinCount`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L31) |
| [421](#shareclassmanager-421) | addShareClass accepts a salt whose leading bytes name a foreign pool, so a stored class salt is no longer branded with its own pool id.<br>Caught by: [`poolSaltPrefixIsOwnPool`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_pool_properties.spec#L17) |
| [422](#shareclassmanager-422) | addShareClass stores the class salt without marking it used, so another class can take the same salt again.<br>Caught by: [`classSaltConsumedPerClass`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L48) |
| [423](#shareclassmanager-423) | addShareClass marks the salt used but never stores it on the class, so a registered class carries an empty salt.<br>Caught by: [`registeredClassCarriesASalt`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L62) |
| [424](#shareclassmanager-424) | updateShares records a network issuance without adding it to the class total, so a class's total drifts below its own per-network net.<br>Caught by: [`classTotalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L68) |
| [425](#shareclassmanager-425) | updateShares skips the share class existence check, so issuance and revocation accumulate on a class of the pool that was never created.<br>Caught by: [`classUncreatedRowsZero`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L74) |
| [449](#shareclassmanager-449) | updateShares adds a revocation amount to the class total instead of subtracting it, so the total splits from the per-network net sum.<br>Caught by: [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57) |
| [481](#shareclassmanager-481) | previewNextShareClassId uses the current count, not the next, so a new class reuses the latest id and overwrites its salt.<br>Caught by: [`stScClassSaltIsWriteOnce`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L169) |
| [487](#shareclassmanager-487) | addShareClass no longer rejects an already-consumed salt, so a second share class of the pool can be created with the first class's salt.<br>Caught by: [`stScCreationClaimsAFreeIdentity`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L68) |
| [491](#shareclassmanager-491) | updateShares adds an issuance to the class total without recording it on the issuing network, so the total exceeds the per-network net sum.<br>Caught by: [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57) |
| [5000](#shareclassmanager-5000) | addShareClass runs without the ward gate, so any caller can create a class, spend a salt and advance the class counter.<br>Caught by: [`acScOnlyAWardMovesTheClassCounter`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L20) · [`acScOnlyAWardMovesTheClassRoster`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L36) · [`acScOnlyAWardMovesTheSaltRegistry`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L53) · [`acScOnlyAWardMovesTheClassSalt`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L69) |
| [5001](#shareclassmanager-5001) | updateShares runs without the ward gate, so any caller can move a class supply and a network's issued and revoked totals.<br>Caught by: [`acScOnlyAWardMovesTheClassSupply`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L85) · [`acScOnlyAWardMovesANetworkIssuedTotal`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L104) · [`acScOnlyAWardMovesANetworkRevokedTotal`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L120) · [`acScOnlyAWardMovesTheNegativeNetworkCount`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L168) |
| [5002](#shareclassmanager-5002) | updateSharePrice runs without the ward gate, so any caller can publish a class price and the timestamp that dates it.<br>Caught by: [`acScOnlyAWardMovesTheSharePrice`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L136) · [`acScOnlyAWardMovesThePriceTimestamp`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L152) |
| [5003](#shareclassmanager-5003) | rely runs without the ward gate, so any caller can promote an address into the roll that operates the share class book.<br>Caught by: [`acScOnlyAWardMovesTheWardSet`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L4) |
| [5004](#shareclassmanager-5004) | A new ward-only correctShares subtracts from a network's issued and revoked totals, so both totals can decrease.<br>Caught by: [`vtScNetworkIssuedTotalNeverDecreases`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L6) · [`vtScNetworkRevokedTotalNeverDecreases`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L21) |
| [5005](#shareclassmanager-5005) | updateShares adds a revocation to the class total instead of subtracting it, so a burn inflates the supply.<br>Caught by: [`hlScCrossChainTransferConservesClassSupply`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L4) |
| [5006](#shareclassmanager-5006) | A revocation lowers the network's issued total instead of raising its revoked total, so no revocation is recorded.<br>Caught by: [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [5007](#shareclassmanager-5007) | updateShares raises the class total on an issuance without recording it on the issuing network, so the network that received the shares shows none.<br>Caught by: [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [5008](#shareclassmanager-5008) | updateShares registers the class and restamps its price time instead of checking it exists, so a share move alters both.<br>Caught by: [`stScClassIdentityMovesOnlyOnCreation`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L85) · [`stScSharePriceMovesOnlyOnRepricing`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L109) |
| [5009](#shareclassmanager-5009) | addShareClass returns and emits the next class's id instead of the one it wrote, so the caller gets a nonexistent class.<br>Caught by: [`hlScCreationHandsOutThePreviewedId`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L21) · [`hlScCreationMatchesTheIndexedPreview`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L48) |
| [5010](#shareclassmanager-5010) | updateSharePrice stores the block time instead of the given timestamp, so a backdated price reads as fresh.<br>Caught by: [`hlScRepricingStoresTheGivenPriceAndStamp`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L33) |
| [5011](#shareclassmanager-5011) | the ward gate no longer checks the caller, so every guarded entry point of the share class book answers an outsider.<br>Caught by: [`rvScRelyRefusesANonWard`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L90) · [`rvScDenyRefusesANonWard`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L104) |
| [5012](#shareclassmanager-5012) | addShareClass no longer refuses a salt that was already spent, so a creation carrying a consumed salt is admitted.<br>Caught by: [`rvScAddShareClassRefusesACreationThatDoesNotCheckOut`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L4) |
| [5013](#shareclassmanager-5013) | updateSharePrice no longer refuses a stamp later than the current block, so a price dated in the future is accepted.<br>Caught by: [`rvScUpdateSharePriceRefusesANonWardAnUnknownClassOrAFutureStamp`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L27) |
| [5014](#shareclassmanager-5014) | updateShares records the class on the roster instead of requiring it, so a share movement against a class that was never created is admitted.<br>Caught by: [`rvScUpdateSharesRefusesANonWardOrAnUnknownClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L45) |
| [5015](#shareclassmanager-5015) | issuance refuses a network whose issued and revoked totals are equal, so a flat network fails instead of reading zero.<br>Caught by: [`rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L245) |
| [5016](#shareclassmanager-5016) | previewNextShareClassId adds in a wider type then truncates, so a full class counter wraps to index zero instead of refusing.<br>Caught by: [`rvScPreviewNextShareClassIdRefusesAPoolWhoseClassCounterIsFull`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L77) |
| [5017](#shareclassmanager-5017) | addShareClass never records the new class on the roster, so the id it hands back does not read back as an existing class.<br>Caught by: [`rcScFirstClassCreationIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L4) |
| [6900](#shareclassmanager-6900) | addShareClass computes the next index without saving it, so the class counter stays put and the next preview repeats the id.<br>Caught by: [`rcScFirstClassCreationIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L4) |
| [6901](#shareclassmanager-6901) | addShareClass sets the new class's registry flag to false instead of true, so the created class never comes on record.<br>Caught by: [`rcScFirstClassCreationIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L4) |
| [6902](#shareclassmanager-6902) | updateSharePrice refuses a stamp equal to the current block time, so a price computed this block cannot be published.<br>Caught by: [`rcScPricePublishedAtTheCurrentBlockIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L27) |
| [6903](#shareclassmanager-6903) | Publishing a price overwrites the supplied computation time with the current block clock, so a price computed earlier loses its own stamp.<br>Caught by: [`rcScBackdatedPriceKeepsItsOwnStamp`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L42) |
| [6904](#shareclassmanager-6904) | updateSharePrice also refuses stamps older than the stored one, so an earlier computed price can no longer replace it.<br>Caught by: [`rcScOlderPriceReplacesTheStoredOne`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L58) |
| [6905](#shareclassmanager-6905) | Publishing a zero price leaves the stored price in place, so a share class can never be written down to nothing.<br>Caught by: [`rcScPriceCanBeWrittenDownToZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L76) |
| [6907](#shareclassmanager-6907) | A share revocation is recorded on the network ledger without lowering the class supply, so burning shares leaves the class total where it was.<br>Caught by: [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [6908](#shareclassmanager-6908) | An issuance credits the issuing network one share more than issued, so network ledgers no longer sum to the class supply.<br>Caught by: [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57) |
| [6909](#shareclassmanager-6909) | A share issuance is recorded on the network ledger without raising the class supply, so a class emptied to zero can never be filled again.<br>Caught by: [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [6910](#shareclassmanager-6910) | A share issuance raises the class supply by one share more than was issued, so even a movement of nothing moves the books.<br>Caught by: [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [6911](#shareclassmanager-6911) | The per network view subtracts issued from revoked, so any network holding shares fails the query instead of answering.<br>Caught by: [`rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L245) |
| [6912](#shareclassmanager-6912) | A revocation is refused once a network's cumulative burns would pass its cumulative mints, so a network can never run a deficit.<br>Caught by: [`rcScNetworkRevocationsCanExceedItsIssuances`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L107) |
| [6913](#shareclassmanager-6913) | Granting authority emits the grant without writing the seat, so the party named is never actually admitted.<br>Caught by: [`rcScRelyThenDenyRoundTripIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L124) |
| [6914](#shareclassmanager-6914) | Withdrawing authority installs the seat instead of clearing it, so a party that was denied keeps its powers.<br>Caught by: [`rcScRelyThenDenyRoundTripIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L124) |
| [6915](#shareclassmanager-6915) | A revocation lowers the class supply but not the revoking network's ledger, so that network still shows the burned shares.<br>Caught by: [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [6916](#shareclassmanager-6916) | A share revocation takes one share more off the class supply than was burned, so the class supply falls below the sum its networks hold.<br>Caught by: [`hlScCrossChainTransferConservesClassSupply`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L4) · [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [6918](#shareclassmanager-6918) | issuance reports zero for a network that revoked more than it issued instead of refusing the read, so a deficit reads as an empty network.<br>Caught by: [`rvScIssuanceRefusesANetworkInRevocationDeficit`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L61) |
| [8011](#shareclassmanager-8011) | updateShares and transferShares never report a crossing, so a network that revokes more than it issued is not counted as negative.<br>Caught by: [`negativeNetworkCountMatchesTheShortNetworks`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L83) |
| [8012](#shareclassmanager-8012) | A network whose revocations equal its issuances reads as already negative, so its next update miscounts the networks in deficit.<br>Caught by: [`negativeNetworkCountMatchesTheShortNetworks`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L83) |
| [8013](#shareclassmanager-8013) | A new function books shares on one class but moves another class's deficit network count, so both counts go wrong.<br>Caught by: [`classNegativeNetworkCountMatchesItsShortNetworks`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L87) |
| [8014](#shareclassmanager-8014) | A revocation now also reads the net class supply, so a report that leaves the class in deficit is refused.<br>Caught by: [`rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L118) |
| [8015](#shareclassmanager-8015) | totalIssuance returns zero for a class in revocation deficit instead of refusing, so a deficit reads as an empty class.<br>Caught by: [`rvScTotalIssuanceRefusesAClassInRevocationDeficit`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L141) |
| [8016](#shareclassmanager-8016) | totalIssuance refuses a class whose revocations exactly match its issuances, so a fully retired class cannot report its zero supply.<br>Caught by: [`rvScTotalIssuanceAnswersAClassNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L262) |
| [8017](#shareclassmanager-8017) | a revocation is taken off the class issued counter instead of added to its revoked counter, so the cumulative issued total walks backwards.<br>Caught by: [`vtScClassIssuedTotalNeverDecreases`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L36) |
| [8018](#shareclassmanager-8018) | an issuance is taken off the class revoked counter instead of added to its issued counter, so the cumulative revoked total walks backwards.<br>Caught by: [`vtScClassRevokedTotalNeverDecreases`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L51) |
| [8019](#shareclassmanager-8019) | updateShares books every issuance as a revocation and every revocation as an issuance, so supply moves the wrong way.<br>Caught by: [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [8040](#shareclassmanager-8040) | totalIssuance adds the revoked counter instead of subtracting it, so a class that burned shares reports inflated supply.<br>Caught by: [`hlScSupplyViewsReportIssuedMinusRevoked`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L97) |
| [8041](#shareclassmanager-8041) | The deficit network count now rises on every report leaving a network short and never falls, so it overcounts short networks.<br>Caught by: [`rcScNegativeNetworkCountOpensAndCloses`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L142) |
| [8042](#shareclassmanager-8042) | a revocation past the class supply is refused again, so a burn reported before its mint can never leave the class short.<br>Caught by: [`rcScRefusedClassSupplyIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L162) |
| [8043](#shareclassmanager-8043) | updateSharePrice resets the short network count, so a class in shortfall reads as whole after any repricing.<br>Caught by: [`stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L129) |
| [8045](#shareclassmanager-8045) | a network issuance leg is also credited to the next network id, so a network the call never named gains shares.<br>Caught by: [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63) |
| [8050](#shareclassmanager-8050) | a revocation past the class supply is refused again, so a burn reported before its mint is stranded with its nonce unspent.<br>Caught by: [`rvHhShareReportIsNeverStrandedWhileTheCountersHaveRoom`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L202) |
| [8051](#shareclassmanager-8051) | the deficit update of a network leg passes the old state as the new one, so the short network count never moves.<br>Caught by: [`rcHhShareReportPastTheClassSupplyIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L557) |
| [8054](#shareclassmanager-8054) | The post-update deficit test is transposed, so solvent reports are counted and networks going short are not.<br>Caught by: [`stHhNegativeNetworkCountFollowsTheShortNetworks`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L209) |
| [8057](#shareclassmanager-8057) | a network leaving its shortfall is never counted back out, so the short network count never comes down.<br>Caught by: [`rcHhBridgeClearsAShortTargetNetworkIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L600) |
| [8200](#shareclassmanager-8200) | The issued and revoked fields swap order, so a raw class or network read returns the revoked figure as issued.<br>Caught by: [`rvScRawCountersAlwaysAnswerWithTheLedger`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L157) |
| [8201](#shareclassmanager-8201) | updateMetadata runs without its ward gate, so any caller can rename a share class and change its symbol.<br>Caught by: [`rvScUpdateMetadataRefusesANonWardAnUnknownClassOrBadLengths`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L119) |
| [8419](#shareclassmanager-8419) | transferShares also raises the class issued and revoked totals, so moving shares between networks is booked as supply issued and revoked.<br>Caught by: [`hlScTransferSharesMovesOnlyTheTwoNetworkLegs`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L139) |
| [8420](#shareclassmanager-8420) | transferShares also raises the class issued and revoked totals, so a transfer between networks changes the class supply totals.<br>Caught by: [`stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L129) |
| [8421](#shareclassmanager-8421) | transferShares issues on the source network and revokes on the destination, so shares move the wrong way between networks.<br>Caught by: [`hlScTransferSharesMovesOnlyTheTwoNetworkLegs`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L139) |
| [8422](#shareclassmanager-8422) | transferShares skips the share class existence check, so a transfer on a class that was never created goes through.<br>Caught by: [`rvScTransferSharesRefusesANonWardOrAnUnknownClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L181) |
| [8423](#shareclassmanager-8423) | updateShares and transferShares reject a revocation beyond the network's issued total, so a transfer that leaves a network in deficit fails.<br>Caught by: [`rvScTransferSharesNeverRefusesAWardWhileTheLegsHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L196) · [`rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L118) |
| [8424](#shareclassmanager-8424) | updateShares and transferShares cap a network's issued total at 128 bits, so an issuance or transfer that the 256-bit counter holds fails.<br>Caught by: [`rvScTransferSharesNeverRefusesAWardWhileTheLegsHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L196) · [`rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L118) |
| [8425](#shareclassmanager-8425) | the network issuance query truncates a supply past 128 bits to its low bits instead of failing, so an oversized network reports a wrong small supply.<br>Caught by: [`rvScIssuanceRefusesANetworkNetPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L217) |
| [8426](#shareclassmanager-8426) | totalIssuance truncates a class supply past 128 bits to its low bits instead of failing, so an oversized class reports a wrong small supply.<br>Caught by: [`rvScTotalIssuanceRefusesAClassNetPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L231) |
| [8427](#shareclassmanager-8427) | the network issuance query narrows the issued and revoked totals separately instead of their difference, so it fails for a network whose issued total passed 128 bits although its supply fits.<br>Caught by: [`rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L245) |
| [8428](#shareclassmanager-8428) | totalIssuance narrows the issued and revoked totals separately instead of their difference, so it fails for a class whose issued total passed 128 bits although its supply fits.<br>Caught by: [`rvScTotalIssuanceAnswersAClassNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L262) |
| [8429](#shareclassmanager-8429) | updateShares and transferShares cap a network's issued total at 128 bits, so no issuance can lift a network's supply past that width.<br>Caught by: [`rcScNetworkNetPastUint128IsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L178) |
| [8951](#shareclassmanager-8951) | addShareClass no longer refuses a consumed salt, so two classes of a pool can carry the same salt.<br>Caught by: [`classSaltsDistinct`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L37) |
| [9005](#shareclassmanager-9005) | renaming a share class also clears the salt it was created under, so the class forgets the identity its token was deployed with.<br>Caught by: [`hlScUpdateMetadataWritesOnlyItsClassesStrings`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L71) |
| [9050](#shareclassmanager-9050) | The class id shifts the pool id only 16 bits above the index, so two pool and index pairs can share an id.<br>Caught by: [`hlScShareClassIdIsInjectiveInPoolAndIndex`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L111) |
| [9051](#shareclassmanager-9051) | updateMetadata also winds the pool's class counter back by one, so a class on record sits at an index above the pool's class count.<br>Caught by: [`recordedClassIdSitsUnderItsPoolWithinCount`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L6) |
| [9052](#shareclassmanager-9052) | addShareClass also records the new class id under the next pool id, so one class id is on record under two pools.<br>Caught by: [`classIdIsOnRecordUnderOnePoolOnly`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L13) · [`recordedClassIdSitsUnderItsPoolWithinCount`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L6) |
| [9053](#shareclassmanager-9053) | updateMetadata takes the class it renames off record, so an existing class stops existing after a metadata update.<br>Caught by: [`stScRecordedClassStaysRecorded`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L27) |
| [9054](#shareclassmanager-9054) | addShareClass always mints the index one id, so every later class reuses the pool's first class id.<br>Caught by: [`hlScCreationMintsTheNextFreshIndex`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L42) |
| [9055](#shareclassmanager-9055) | updateShares books a revocation on the network but not on the class total, so the class supply stays above the net summed over every network.<br>Caught by: [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57) |
| [9057](#shareclassmanager-9057) | a network issuance leg is booked on its revoked counter, so the revoked sum rises instead of the issued sum.<br>Caught by: [`hlScAnUpdateMovesItsLegByItsAmount`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L121) |
| [9065](#shareclassmanager-9065) | A share issuance credits the issuing network but never the class supply, so the class total stays where it was.<br>Caught by: [`rcScClassSupplyCanReachItsStoredCeiling`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L91) |
| [9942](#shareclassmanager-9942) | The class id shifts the pool by 32 bits instead of 64, so the pool no longer sits in the high eight bytes.<br>Caught by: [`hlScClassIdIsThePoolOverTheIndex`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L60) |

## ShareClassManager #401

addShareClass reads the next index without saving the increment, so the pool's class counter never advances.

- **Mutant:** [`401.sol`](401.sol)
- **Caught by:** [`shareClassExistsIffCounted`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 401`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule shareClassExistsIffCounted`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -50,7 +50,7 @@
 
         scId_ = previewNextShareClassId(poolId);
 
-        uint32 index = ++shareClassCount[poolId];
+        uint32 index = shareClassCount[poolId] + 1; // MUTATION: index read without persisting the increment
         shareClassIds[poolId][scId_] = true;
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
```

## ShareClassManager #402

addShareClass never records the new class in the share class registry, leaving a counted and salted class that is not on record.

- **Mutant:** [`402.sol`](402.sol)
- **Caught by:** [`shareClassExistsIffCounted`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L22) · [`shareClassExistsIffSaltSet`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L27)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 402`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule shareClassExistsIffCounted shareClassExistsIffSaltSet`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -51,7 +51,7 @@
         scId_ = previewNextShareClassId(poolId);
 
         uint32 index = ++shareClassCount[poolId];
-        shareClassIds[poolId][scId_] = true;
+        // shareClassIds[poolId][scId_] = true; // MUTATION: removed share class registration write
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
 
```

## ShareClassManager #403

addShareClass consumes the salt in the global registry but never stores it on the class metadata, so the recorded class carries an empty salt.

- **Mutant:** [`403.sol`](403.sol)
- **Caught by:** [`shareClassExistsIffSaltSet`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L27)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 403`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule shareClassExistsIffSaltSet`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -56,7 +56,7 @@
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
 
         salts[salt] = true;
-        meta.salt = salt;
+        // meta.salt = salt; // MUTATION: removed metadata salt write
 
         emit AddShareClass(poolId, scId_, index, name, symbol, salt);
     }
```

## ShareClassManager #404

addShareClass stores the salt on the class metadata without marking it consumed in the global salt registry, leaving the stored salt reusable.

- **Mutant:** [`404.sol`](404.sol)
- **Caught by:** [`classSaltConsumed`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L73)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 404`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule classSaltConsumed`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -55,7 +55,7 @@
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
 
-        salts[salt] = true;
+        // salts[salt] = true; // MUTATION: removed salt consumption write
         meta.salt = salt;
 
         emit AddShareClass(poolId, scId_, index, name, symbol, salt);
```

## ShareClassManager #405

addShareClass accepts a salt whose leading bytes name a foreign pool, so a stored class salt is no longer branded with its own pool id.

- **Mutant:** [`405.sol`](405.sol)
- **Caught by:** [`saltPrefixIsPool`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L67) · [`nullSaltNeverConsumed`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L78)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 405`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule saltPrefixIsPool nullSaltNeverConsumed`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -45,7 +45,7 @@
         require(hubRegistry.exists(poolId), IHubRegistry.NonExistingPool());
 
         PoolId prefixedPoolId = PoolId.wrap(uint64(bytes8(salt)));
-        require(poolId == prefixedPoolId, InvalidSalt());
+        // require(poolId == prefixedPoolId, InvalidSalt()); // MUTATION: removed salt pool-prefix check
         require(!salts[salt], AlreadyUsedSalt());
 
         scId_ = previewNextShareClassId(poolId);
```

## ShareClassManager #406

addShareClass no longer checks the hub registry, so a share class can be created inside a pool that was never registered.

- **Mutant:** [`406.sol`](406.sol)
- **Caught by:** [`existingClassPoolRegistered`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L52)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 406`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule existingClassPoolRegistered`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -42,7 +42,7 @@
         auth
         returns (ShareClassId scId_)
     {
-        require(hubRegistry.exists(poolId), IHubRegistry.NonExistingPool());
+        // require(hubRegistry.exists(poolId), IHubRegistry.NonExistingPool()); // MUTATION: removed pool existence check
 
         PoolId prefixedPoolId = PoolId.wrap(uint64(bytes8(salt)));
         require(poolId == prefixedPoolId, InvalidSalt());
```

## ShareClassManager #407

updateShares skips the share class existence check, so issuance and revocation amounts accumulate on a class that was never created.

- **Mutant:** [`407.sol`](407.sol)
- **Caught by:** [`uncreatedClassNetworkIssuancesZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L32) · [`uncreatedClassNetworkRevocationsZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 407`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule uncreatedClassNetworkIssuancesZero uncreatedClassNetworkRevocationsZero`

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

## ShareClassManager #408

updateSharePrice skips the share class existence check, so a price and its timestamp are stored for a class that was never created.

- **Mutant:** [`408.sol`](408.sol)
- **Caught by:** [`uncreatedClassPriceZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L42) · [`uncreatedClassPriceStampZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L47)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 408`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule uncreatedClassPriceZero uncreatedClassPriceStampZero`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -66,7 +66,7 @@
         external
         auth
     {
-        require(exists(poolId, scId_), ShareClassNotFound());
+        // require(exists(poolId, scId_), ShareClassNotFound()); // MUTATION: removed share class existence check
         Price storage p = pricePoolPerShare[poolId][scId_];
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
 
```

## ShareClassManager #409

updateSharePrice inverts the timestamp gate and accepts prices computed after the current block time, so a stored price stamp can lie in the future.

- **Mutant:** [`409.sol`](409.sol)
- **Caught by:** [`priceStampNotFuture`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L62)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 409`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule priceStampNotFuture`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -68,7 +68,7 @@
     {
         require(exists(poolId, scId_), ShareClassNotFound());
         Price storage p = pricePoolPerShare[poolId][scId_];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        require(computedAt >= block.timestamp, CannotSetFuturePrice()); // MUTATION: flipped <= to >=
 
         p.price = pricePoolPerShare_;
         p.computedAt = computedAt;
```

## ShareClassManager #411

updateShares records a network issuance without adding it to the class total, so total issuance drifts below the per-network net sum.

- **Mutant:** [`411.sol`](411.sol)
- **Caught by:** [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 411`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule totalIssuanceIsNetworkNetSum`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -95,7 +95,7 @@
         require(exists(poolId, scId_), ShareClassNotFound());
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
-        if (isIssuance) total.issuances += amount;
+        if (isIssuance) {} // MUTATION: removed total issuance update
         else total.revocations += amount;
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
```

## ShareClassManager #412

An issuance is recorded on both legs of the network ledger, so a mint also counts as a burn on that chain.

- **Mutant:** [`412.sol`](412.sol)
- **Caught by:** [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 412`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -161,6 +161,7 @@
 
         if (isIssuance) {
             ipn.issuances += amount;
+            ipn.revocations += amount; // MUTATION: the issuance also books a revocation
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## ShareClassManager #414

updateSharesPair books one share movement on two networks at once, so a call aimed at one chain moves another chain's ledger.

- **Mutant:** [`414.sol`](414.sol)
- **Caught by:** [`stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 414`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_transitions.conf --rule stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -113,6 +113,38 @@
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+    }
+
+    /// @notice MUTATION: books one share movement on two networks at once.
+    function updateSharesPair(
+        uint16 centrifugeId,
+        uint16 siblingCentrifugeId,
+        PoolId poolId,
+        ShareClassId scId_,
+        uint128 amount,
+        bool isIssuance
+    ) external auth {
+        require(exists(poolId, scId_), ShareClassNotFound());
+
+        IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
+        IssuanceCounters storage sibling = issuancePerNetwork[poolId][scId_][siblingCentrifugeId];
+        bool wasNegative = ipn.revocations > ipn.issuances;
+        bool siblingWasNegative = sibling.revocations > sibling.issuances;
+
+        if (isIssuance) {
+            ipn.issuances += amount;
+            sibling.issuances += amount;
+            issuanceAcrossNetworks[poolId][scId_].issuances += amount;
+        } else {
+            ipn.revocations += amount;
+            sibling.revocations += amount;
+            issuanceAcrossNetworks[poolId][scId_].revocations += amount;
+        }
+
+        _updateNegativeCount(poolId, scId_, centrifugeId, wasNegative, ipn.revocations > ipn.issuances);
+        _updateNegativeCount(
+            poolId, scId_, siblingCentrifugeId, siblingWasNegative, sibling.revocations > sibling.issuances
+        );
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #415

updateSharesForPools books one share movement for two pools at once, so a call aimed at one pool moves another pool's class row and network ledger.

- **Mutant:** [`415.sol`](415.sol)
- **Caught by:** [`stScClassRowIsPerPool`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_pool_properties.spec#L27) · [`stScNetworkLedgerIsPerPool`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_pool_properties.spec#L67)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 415`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_pool_properties.conf --rule stScClassRowIsPerPool stScNetworkLedgerIsPerPool`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -113,6 +113,41 @@
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+    }
+
+    /// @notice MUTATION: books one share movement for two pools at once.
+    function updateSharesForPools(
+        uint16 centrifugeId,
+        PoolId poolId,
+        PoolId siblingPoolId,
+        ShareClassId scId_,
+        ShareClassId siblingScId,
+        uint128 amount,
+        bool isIssuance
+    ) external auth {
+        require(exists(poolId, scId_), ShareClassNotFound());
+
+        IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
+        IssuanceCounters storage sibling = issuancePerNetwork[siblingPoolId][siblingScId][centrifugeId];
+        bool wasNegative = ipn.revocations > ipn.issuances;
+        bool siblingWasNegative = sibling.revocations > sibling.issuances;
+
+        if (isIssuance) {
+            ipn.issuances += amount;
+            sibling.issuances += amount;
+            issuanceAcrossNetworks[poolId][scId_].issuances += amount;
+            issuanceAcrossNetworks[siblingPoolId][siblingScId].issuances += amount;
+        } else {
+            ipn.revocations += amount;
+            sibling.revocations += amount;
+            issuanceAcrossNetworks[poolId][scId_].revocations += amount;
+            issuanceAcrossNetworks[siblingPoolId][siblingScId].revocations += amount;
+        }
+
+        _updateNegativeCount(poolId, scId_, centrifugeId, wasNegative, ipn.revocations > ipn.issuances);
+        _updateNegativeCount(
+            siblingPoolId, siblingScId, centrifugeId, siblingWasNegative, sibling.revocations > sibling.issuances
+        );
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #416

A new updateSharesForClasses books one share movement on two classes, so a sibling class's totals and ledger move too.

- **Mutant:** [`416.sol`](416.sol)
- **Caught by:** [`stScClassRowIsPerClass`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L95) · [`stScNetworkLedgerIsPerClass`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L134)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 416`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule stScClassRowIsPerClass stScNetworkLedgerIsPerClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -113,6 +113,40 @@
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+    }
+
+    /// @notice MUTATION: books one share movement for two classes of the same pool at once.
+    function updateSharesForClasses(
+        uint16 centrifugeId,
+        PoolId poolId,
+        ShareClassId scId_,
+        ShareClassId siblingScId,
+        uint128 amount,
+        bool isIssuance
+    ) external auth {
+        require(exists(poolId, scId_), ShareClassNotFound());
+
+        IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
+        IssuanceCounters storage sibling = issuancePerNetwork[poolId][siblingScId][centrifugeId];
+        bool wasNegative = ipn.revocations > ipn.issuances;
+        bool siblingWasNegative = sibling.revocations > sibling.issuances;
+
+        if (isIssuance) {
+            ipn.issuances += amount;
+            sibling.issuances += amount;
+            issuanceAcrossNetworks[poolId][scId_].issuances += amount;
+            issuanceAcrossNetworks[poolId][siblingScId].issuances += amount;
+        } else {
+            ipn.revocations += amount;
+            sibling.revocations += amount;
+            issuanceAcrossNetworks[poolId][scId_].revocations += amount;
+            issuanceAcrossNetworks[poolId][siblingScId].revocations += amount;
+        }
+
+        _updateNegativeCount(poolId, scId_, centrifugeId, wasNegative, ipn.revocations > ipn.issuances);
+        _updateNegativeCount(
+            poolId, siblingScId, centrifugeId, siblingWasNegative, sibling.revocations > sibling.issuances
+        );
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #417

addShareClass advances the class counter by two, so the pool's class sequence skips an index.

- **Mutant:** [`417.sol`](417.sol)
- **Caught by:** [`stScClassCountStepsByOne`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L155)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 417`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule stScClassCountStepsByOne`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -50,7 +50,8 @@
 
         scId_ = previewNextShareClassId(poolId);
 
-        uint32 index = ++shareClassCount[poolId];
+        shareClassCount[poolId] += 2; // MUTATION: the sequence skips an index
+        uint32 index = shareClassCount[poolId];
         shareClassIds[poolId][scId_] = true;
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
```

## ShareClassManager #418

addShareClass never records the new class in the share class registry, so a minted class carries a metadata salt while staying off record.

- **Mutant:** [`418.sol`](418.sol)
- **Caught by:** [`classSaltSetImpliesRegisteredPerClass`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L25) · [`classWithinCountIsRegistered`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L56)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 418`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule classSaltSetImpliesRegisteredPerClass classWithinCountIsRegistered`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -51,7 +51,7 @@
         scId_ = previewNextShareClassId(poolId);
 
         uint32 index = ++shareClassCount[poolId];
-        shareClassIds[poolId][scId_] = true;
+        // shareClassIds[poolId][scId_] = true; // MUTATION: the class is not recorded on the registry
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
 
```

## ShareClassManager #419

addShareClass never saves the incremented class counter, so a registered class sits at an index beyond the pool's count.

- **Mutant:** [`419.sol`](419.sol)
- **Caught by:** [`registeredClassIndexWithinCount`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 419`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule registeredClassIndexWithinCount`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -50,7 +50,7 @@
 
         scId_ = previewNextShareClassId(poolId);
 
-        uint32 index = ++shareClassCount[poolId];
+        uint32 index = shareClassCount[poolId] + 1; // MUTATION: the incremented counter is not persisted
         shareClassIds[poolId][scId_] = true;
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
```

## ShareClassManager #420

previewNextShareClassId skips an index, so a class is minted at index count+2 while the counter only advances to count+1.

- **Mutant:** [`420.sol`](420.sol)
- **Caught by:** [`registeredClassIndexWithinCount`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 420`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule registeredClassIndexWithinCount`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -121,7 +121,7 @@
 
     /// @inheritdoc IShareClassManager
     function previewNextShareClassId(PoolId poolId) public view returns (ShareClassId scId) {
-        return newShareClassId(poolId, shareClassCount[poolId] + 1);
+        return newShareClassId(poolId, shareClassCount[poolId] + 2); // MUTATION: the previewed index skips one
     }
 
     /// @inheritdoc IShareClassManager
```

## ShareClassManager #421

addShareClass accepts a salt whose leading bytes name a foreign pool, so a stored class salt is no longer branded with its own pool id.

- **Mutant:** [`421.sol`](421.sol)
- **Caught by:** [`poolSaltPrefixIsOwnPool`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_pool_properties.spec#L17)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 421`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_pool_properties.conf --rule poolSaltPrefixIsOwnPool`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -45,7 +45,7 @@
         require(hubRegistry.exists(poolId), IHubRegistry.NonExistingPool());
 
         PoolId prefixedPoolId = PoolId.wrap(uint64(bytes8(salt)));
-        require(poolId == prefixedPoolId, InvalidSalt());
+        // require(poolId == prefixedPoolId, InvalidSalt()); // MUTATION: removed salt pool-prefix check
         require(!salts[salt], AlreadyUsedSalt());
 
         scId_ = previewNextShareClassId(poolId);
```

## ShareClassManager #422

addShareClass stores the class salt without marking it used, so another class can take the same salt again.

- **Mutant:** [`422.sol`](422.sol)
- **Caught by:** [`classSaltConsumedPerClass`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L48)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 422`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule classSaltConsumedPerClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -55,7 +55,7 @@
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
 
-        salts[salt] = true;
+        // salts[salt] = true; // MUTATION: removed salt consumption write
         meta.salt = salt;
 
         emit AddShareClass(poolId, scId_, index, name, symbol, salt);
```

## ShareClassManager #423

addShareClass marks the salt used but never stores it on the class, so a registered class carries an empty salt.

- **Mutant:** [`423.sol`](423.sol)
- **Caught by:** [`registeredClassCarriesASalt`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L62)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 423`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule registeredClassCarriesASalt`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -56,7 +56,7 @@
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
 
         salts[salt] = true;
-        meta.salt = salt;
+        // meta.salt = salt; // MUTATION: removed metadata salt write
 
         emit AddShareClass(poolId, scId_, index, name, symbol, salt);
     }
```

## ShareClassManager #424

updateShares records a network issuance without adding it to the class total, so a class's total drifts below its own per-network net.

- **Mutant:** [`424.sol`](424.sol)
- **Caught by:** [`classTotalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L68)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 424`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule classTotalIssuanceIsNetworkNetSum`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -95,7 +95,7 @@
         require(exists(poolId, scId_), ShareClassNotFound());
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
-        if (isIssuance) total.issuances += amount;
+        if (isIssuance) {} // MUTATION: removed total issuance update
         else total.revocations += amount;
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
```

## ShareClassManager #425

updateShares skips the share class existence check, so issuance and revocation accumulate on a class of the pool that was never created.

- **Mutant:** [`425.sol`](425.sol)
- **Caught by:** [`classUncreatedRowsZero`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L74)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 425`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule classUncreatedRowsZero`

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

## ShareClassManager #449

updateShares adds a revocation amount to the class total instead of subtracting it, so the total splits from the per-network net sum.

- **Mutant:** [`449.sol`](449.sol)
- **Caught by:** [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 449`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule totalIssuanceIsNetworkNetSum`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        else total.issuances += amount; // MUTATION: revocation adds to total
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## ShareClassManager #481

previewNextShareClassId uses the current count, not the next, so a new class reuses the latest id and overwrites its salt.

- **Mutant:** [`481.sol`](481.sol)
- **Caught by:** [`stScClassSaltIsWriteOnce`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L169)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 481`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule stScClassSaltIsWriteOnce`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -121,7 +121,7 @@
 
     /// @inheritdoc IShareClassManager
     function previewNextShareClassId(PoolId poolId) public view returns (ShareClassId scId) {
-        return newShareClassId(poolId, shareClassCount[poolId] + 1);
+        return newShareClassId(poolId, shareClassCount[poolId]); // MUTATION: id derived from the current count, not the next
     }
 
     /// @inheritdoc IShareClassManager
```

## ShareClassManager #487

addShareClass no longer rejects an already-consumed salt, so a second share class of the pool can be created with the first class's salt.

- **Mutant:** [`487.sol`](487.sol)
- **Caught by:** [`stScCreationClaimsAFreeIdentity`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L68)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 487`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_transitions.conf --rule stScCreationClaimsAFreeIdentity`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -46,7 +46,7 @@
 
         PoolId prefixedPoolId = PoolId.wrap(uint64(bytes8(salt)));
         require(poolId == prefixedPoolId, InvalidSalt());
-        require(!salts[salt], AlreadyUsedSalt());
+        // require(!salts[salt], AlreadyUsedSalt()); // MUTATION: removed salt reuse check
 
         scId_ = previewNextShareClassId(poolId);
 
```

## ShareClassManager #491

updateShares adds an issuance to the class total without recording it on the issuing network, so the total exceeds the per-network net sum.

- **Mutant:** [`491.sol`](491.sol)
- **Caught by:** [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 491`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule totalIssuanceIsNetworkNetSum`

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

## ShareClassManager #5000

addShareClass runs without the ward gate, so any caller can create a class, spend a salt and advance the class counter.

- **Mutant:** [`5000.sol`](5000.sol)
- **Caught by:** [`acScOnlyAWardMovesTheClassCounter`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L20) · [`acScOnlyAWardMovesTheClassRoster`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L36) · [`acScOnlyAWardMovesTheSaltRegistry`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L53) · [`acScOnlyAWardMovesTheClassSalt`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L69)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5000`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_access_control.conf --rule acScOnlyAWardMovesTheClassCounter acScOnlyAWardMovesTheClassRoster acScOnlyAWardMovesTheSaltRegistry acScOnlyAWardMovesTheClassSalt`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -39,7 +39,7 @@
     /// @inheritdoc IShareClassManager
     function addShareClass(PoolId poolId, string calldata name, string calldata symbol, bytes32 salt)
         external
-        auth
+        // auth // MUTATION: creation no longer requires a ward
         returns (ShareClassId scId_)
     {
         require(hubRegistry.exists(poolId), IHubRegistry.NonExistingPool());
```

## ShareClassManager #5001

updateShares runs without the ward gate, so any caller can move a class supply and a network's issued and revoked totals.

- **Mutant:** [`5001.sol`](5001.sol)
- **Caught by:** [`acScOnlyAWardMovesTheClassSupply`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L85) · [`acScOnlyAWardMovesANetworkIssuedTotal`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L104) · [`acScOnlyAWardMovesANetworkRevokedTotal`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L120) · [`acScOnlyAWardMovesTheNegativeNetworkCount`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L168)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5001`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_access_control.conf --rule acScOnlyAWardMovesTheClassSupply acScOnlyAWardMovesANetworkIssuedTotal acScOnlyAWardMovesANetworkRevokedTotal acScOnlyAWardMovesTheNegativeNetworkCount`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -90,7 +90,7 @@
     /// @inheritdoc IShareClassManager
     function updateShares(uint16 centrifugeId, PoolId poolId, ShareClassId scId_, uint128 amount, bool isIssuance)
         external
-        auth
+        // auth // MUTATION: a share movement no longer requires a ward
     {
         require(exists(poolId, scId_), ShareClassNotFound());
 
```

## ShareClassManager #5002

updateSharePrice runs without the ward gate, so any caller can publish a class price and the timestamp that dates it.

- **Mutant:** [`5002.sol`](5002.sol)
- **Caught by:** [`acScOnlyAWardMovesTheSharePrice`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L136) · [`acScOnlyAWardMovesThePriceTimestamp`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L152)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5002`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_access_control.conf --rule acScOnlyAWardMovesTheSharePrice acScOnlyAWardMovesThePriceTimestamp`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -64,7 +64,7 @@
     /// @inheritdoc IShareClassManager
     function updateSharePrice(PoolId poolId, ShareClassId scId_, D18 pricePoolPerShare_, uint64 computedAt)
         external
-        auth
+        // auth // MUTATION: a repricing no longer requires a ward
     {
         require(exists(poolId, scId_), ShareClassNotFound());
         Price storage p = pricePoolPerShare[poolId][scId_];
```

## ShareClassManager #5003

rely runs without the ward gate, so any caller can promote an address into the roll that operates the share class book.

- **Mutant:** [`5003.sol`](5003.sol)
- **Caught by:** [`acScOnlyAWardMovesTheWardSet`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5003`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_access_control.conf --rule acScOnlyAWardMovesTheWardSet`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -22,7 +22,7 @@
     }
 
     /// @inheritdoc IAuth
-    function rely(address user) public auth {
+    function rely(address user) public { // MUTATION: granting authority no longer requires a ward
         wards[user] = 1;
         emit Rely(user);
     }
```

## ShareClassManager #5004

A new ward-only correctShares subtracts from a network's issued and revoked totals, so both totals can decrease.

- **Mutant:** [`5004.sol`](5004.sol)
- **Caught by:** [`vtScNetworkIssuedTotalNeverDecreases`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L6) · [`vtScNetworkRevokedTotalNeverDecreases`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5004`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_transitions.conf --rule vtScNetworkIssuedTotalNeverDecreases vtScNetworkRevokedTotalNeverDecreases`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -113,6 +113,19 @@
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+    }
+
+    // MUTATION: a correction entry point that walks back both legs of a network ledger
+    function correctShares(uint16 centrifugeId, PoolId poolId, ShareClassId scId_, uint128 issued, uint128 revoked)
+        external
+        auth
+    {
+        require(exists(poolId, scId_), ShareClassNotFound());
+
+        IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
+
+        ipn.issuances -= issued;
+        ipn.revocations -= revoked;
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #5005

updateShares adds a revocation to the class total instead of subtracting it, so a burn inflates the supply.

- **Mutant:** [`5005.sol`](5005.sol)
- **Caught by:** [`hlScCrossChainTransferConservesClassSupply`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5005`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScCrossChainTransferConservesClassSupply`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        else total.issuances += amount; // MUTATION: a revocation raises the class supply
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## ShareClassManager #5006

A revocation lowers the network's issued total instead of raising its revoked total, so no revocation is recorded.

- **Mutant:** [`5006.sol`](5006.sol)
- **Caught by:** [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5006`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -163,7 +163,7 @@
             ipn.issuances += amount;
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
-            ipn.revocations += amount;
+            ipn.issuances -= amount; // MUTATION: the revocation is netted off the issued leg
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
 
```

## ShareClassManager #5007

updateShares raises the class total on an issuance without recording it on the issuing network, so the network that received the shares shows none.

- **Mutant:** [`5007.sol`](5007.sol)
- **Caught by:** [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5007`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -160,7 +160,7 @@
         bool wasNegative = ipn.revocations > ipn.issuances;
 
         if (isIssuance) {
-            ipn.issuances += amount;
+            // ipn.issuances += amount; // MUTATION: the issuing network is not credited
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## ShareClassManager #5008

updateShares registers the class and restamps its price time instead of checking it exists, so a share move alters both.

- **Mutant:** [`5008.sol`](5008.sol)
- **Caught by:** [`stScClassIdentityMovesOnlyOnCreation`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L85) · [`stScSharePriceMovesOnlyOnRepricing`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L109)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5008`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_transitions.conf --rule stScClassIdentityMovesOnlyOnCreation stScSharePriceMovesOnlyOnRepricing`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -92,7 +92,8 @@
         external
         auth
     {
-        require(exists(poolId, scId_), ShareClassNotFound());
+        shareClassIds[poolId][scId_] = true; // MUTATION: the movement registers the class instead of requiring it
+        pricePoolPerShare[poolId][scId_].computedAt = uint64(block.timestamp); // MUTATION: and restamps its price as fresh
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
```

## ShareClassManager #5009

addShareClass returns and emits the next class's id instead of the one it wrote, so the caller gets a nonexistent class.

- **Mutant:** [`5009.sol`](5009.sol)
- **Caught by:** [`hlScCreationHandsOutThePreviewedId`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L21) · [`hlScCreationMatchesTheIndexedPreview`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L48)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5009`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScCreationHandsOutThePreviewedId hlScCreationMatchesTheIndexedPreview`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -57,6 +57,8 @@
 
         salts[salt] = true;
         meta.salt = salt;
+
+        scId_ = previewNextShareClassId(poolId); // MUTATION: the returned id is decoupled from the written id
 
         emit AddShareClass(poolId, scId_, index, name, symbol, salt);
     }
```

## ShareClassManager #5010

updateSharePrice stores the block time instead of the given timestamp, so a backdated price reads as fresh.

- **Mutant:** [`5010.sol`](5010.sol)
- **Caught by:** [`hlScRepricingStoresTheGivenPriceAndStamp`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L33)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5010`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScRepricingStoresTheGivenPriceAndStamp`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -71,7 +71,7 @@
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
 
         p.price = pricePoolPerShare_;
-        p.computedAt = computedAt;
+        p.computedAt = uint64(block.timestamp); // MUTATION: the stamp stored is the chain clock, not the one handed in
         emit UpdatePricePoolPerShare(poolId, scId_, pricePoolPerShare_, computedAt);
     }
 
```

## ShareClassManager #5011

the ward gate no longer checks the caller, so every guarded entry point of the share class book answers an outsider.

- **Mutant:** [`5011.sol`](5011.sol)
- **Caught by:** [`rvScRelyRefusesANonWard`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L90) · [`rvScDenyRefusesANonWard`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L104)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5011`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScRelyRefusesANonWard rvScDenyRefusesANonWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -17,7 +17,7 @@
 
     /// @dev Check if the msg.sender has permissions
     modifier auth() {
-        require(wards[msg.sender] == 1, NotAuthorized());
+        // require(wards[msg.sender] == 1, NotAuthorized()); // MUTATION: the gate admits every caller
         _;
     }
 
```

## ShareClassManager #5012

addShareClass no longer refuses a salt that was already spent, so a creation carrying a consumed salt is admitted.

- **Mutant:** [`5012.sol`](5012.sol)
- **Caught by:** [`rvScAddShareClassRefusesACreationThatDoesNotCheckOut`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5012`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScAddShareClassRefusesACreationThatDoesNotCheckOut`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -46,7 +46,7 @@
 
         PoolId prefixedPoolId = PoolId.wrap(uint64(bytes8(salt)));
         require(poolId == prefixedPoolId, InvalidSalt());
-        require(!salts[salt], AlreadyUsedSalt());
+        // require(!salts[salt], AlreadyUsedSalt()); // MUTATION: a spent salt no longer closes the gate
 
         scId_ = previewNextShareClassId(poolId);
 
```

## ShareClassManager #5013

updateSharePrice no longer refuses a stamp later than the current block, so a price dated in the future is accepted.

- **Mutant:** [`5013.sol`](5013.sol)
- **Caught by:** [`rvScUpdateSharePriceRefusesANonWardAnUnknownClassOrAFutureStamp`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L27)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5013`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScUpdateSharePriceRefusesANonWardAnUnknownClassOrAFutureStamp`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -68,7 +68,7 @@
     {
         require(exists(poolId, scId_), ShareClassNotFound());
         Price storage p = pricePoolPerShare[poolId][scId_];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // require(computedAt <= block.timestamp, CannotSetFuturePrice()); // MUTATION: a forward dated stamp is admitted
 
         p.price = pricePoolPerShare_;
         p.computedAt = computedAt;
```

## ShareClassManager #5014

updateShares records the class on the roster instead of requiring it, so a share movement against a class that was never created is admitted.

- **Mutant:** [`5014.sol`](5014.sol)
- **Caught by:** [`rvScUpdateSharesRefusesANonWardOrAnUnknownClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L45)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5014`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScUpdateSharesRefusesANonWardOrAnUnknownClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -92,7 +92,7 @@
         external
         auth
     {
-        require(exists(poolId, scId_), ShareClassNotFound());
+        shareClassIds[poolId][scId_] = true; // MUTATION: the movement registers the class instead of requiring it
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
```

## ShareClassManager #5015

issuance refuses a network whose issued and revoked totals are equal, so a flat network fails instead of reading zero.

- **Mutant:** [`5015.sol`](5015.sol)
- **Caught by:** [`rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L245)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5015`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -137,7 +137,7 @@
     /// @inheritdoc IShareClassManager
     function issuance(PoolId poolId, ShareClassId scId_, uint16 centrifugeId) public view returns (uint128) {
         IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
-        require(ipn.issuances >= ipn.revocations, NegativeIssuance());
+        require(ipn.issuances > ipn.revocations, NegativeIssuance()); // MUTATION: the equal boundary is refused
         return (ipn.issuances - ipn.revocations).toUint128();
     }
 
```

## ShareClassManager #5016

previewNextShareClassId adds in a wider type then truncates, so a full class counter wraps to index zero instead of refusing.

- **Mutant:** [`5016.sol`](5016.sol)
- **Caught by:** [`rvScPreviewNextShareClassIdRefusesAPoolWhoseClassCounterIsFull`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L77)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5016`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScPreviewNextShareClassIdRefusesAPoolWhoseClassCounterIsFull`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -121,7 +121,7 @@
 
     /// @inheritdoc IShareClassManager
     function previewNextShareClassId(PoolId poolId) public view returns (ShareClassId scId) {
-        return newShareClassId(poolId, shareClassCount[poolId] + 1);
+        return newShareClassId(poolId, uint32(uint256(shareClassCount[poolId]) + 1)); // MUTATION: the full counter wraps instead of reverting
     }
 
     /// @inheritdoc IShareClassManager
```

## ShareClassManager #5017

addShareClass never records the new class on the roster, so the id it hands back does not read back as an existing class.

- **Mutant:** [`5017.sol`](5017.sol)
- **Caught by:** [`rcScFirstClassCreationIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 5017`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScFirstClassCreationIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -51,7 +51,7 @@
         scId_ = previewNextShareClassId(poolId);
 
         uint32 index = ++shareClassCount[poolId];
-        shareClassIds[poolId][scId_] = true;
+        // shareClassIds[poolId][scId_] = true; // MUTATION: the created class is never put on the roster
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
 
```

## ShareClassManager #6900

addShareClass computes the next index without saving it, so the class counter stays put and the next preview repeats the id.

- **Mutant:** [`6900.sol`](6900.sol)
- **Caught by:** [`rcScFirstClassCreationIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6900`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScFirstClassCreationIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -50,7 +50,7 @@
 
         scId_ = previewNextShareClassId(poolId);
 
-        uint32 index = ++shareClassCount[poolId];
+        uint32 index = shareClassCount[poolId] + 1; // MUTATION: the raised count is never saved
         shareClassIds[poolId][scId_] = true;
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
```

## ShareClassManager #6901

addShareClass sets the new class's registry flag to false instead of true, so the created class never comes on record.

- **Mutant:** [`6901.sol`](6901.sol)
- **Caught by:** [`rcScFirstClassCreationIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6901`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScFirstClassCreationIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -51,7 +51,7 @@
         scId_ = previewNextShareClassId(poolId);
 
         uint32 index = ++shareClassCount[poolId];
-        shareClassIds[poolId][scId_] = true;
+        shareClassIds[poolId][scId_] = false; // MUTATION: the registry flag is cleared instead of set
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
 
```

## ShareClassManager #6902

updateSharePrice refuses a stamp equal to the current block time, so a price computed this block cannot be published.

- **Mutant:** [`6902.sol`](6902.sol)
- **Caught by:** [`rcScPricePublishedAtTheCurrentBlockIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L27)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6902`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScPricePublishedAtTheCurrentBlockIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -68,7 +68,7 @@
     {
         require(exists(poolId, scId_), ShareClassNotFound());
         Price storage p = pricePoolPerShare[poolId][scId_];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        require(computedAt < block.timestamp, CannotSetFuturePrice()); // MUTATION: the current block is no longer admitted
 
         p.price = pricePoolPerShare_;
         p.computedAt = computedAt;
```

## ShareClassManager #6903

Publishing a price overwrites the supplied computation time with the current block clock, so a price computed earlier loses its own stamp.

- **Mutant:** [`6903.sol`](6903.sol)
- **Caught by:** [`rcScBackdatedPriceKeepsItsOwnStamp`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L42)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6903`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScBackdatedPriceKeepsItsOwnStamp`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -71,7 +71,7 @@
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
 
         p.price = pricePoolPerShare_;
-        p.computedAt = computedAt;
+        p.computedAt = uint64(block.timestamp); // MUTATION: the stamp is taken from the clock, not the caller
         emit UpdatePricePoolPerShare(poolId, scId_, pricePoolPerShare_, computedAt);
     }
 
```

## ShareClassManager #6904

updateSharePrice also refuses stamps older than the stored one, so an earlier computed price can no longer replace it.

- **Mutant:** [`6904.sol`](6904.sol)
- **Caught by:** [`rcScOlderPriceReplacesTheStoredOne`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L58)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6904`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScOlderPriceReplacesTheStoredOne`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -68,7 +68,7 @@
     {
         require(exists(poolId, scId_), ShareClassNotFound());
         Price storage p = pricePoolPerShare[poolId][scId_];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        require(computedAt <= block.timestamp && computedAt >= p.computedAt, CannotSetFuturePrice()); // MUTATION: a stamp older than the stored one is refused
 
         p.price = pricePoolPerShare_;
         p.computedAt = computedAt;
```

## ShareClassManager #6905

Publishing a zero price leaves the stored price in place, so a share class can never be written down to nothing.

- **Mutant:** [`6905.sol`](6905.sol)
- **Caught by:** [`rcScPriceCanBeWrittenDownToZero`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L76)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6905`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScPriceCanBeWrittenDownToZero`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -70,7 +70,7 @@
         Price storage p = pricePoolPerShare[poolId][scId_];
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
 
-        p.price = pricePoolPerShare_;
+        if (D18.unwrap(pricePoolPerShare_) != 0) p.price = pricePoolPerShare_; // MUTATION: a zero price leaves the stored one in place
         p.computedAt = computedAt;
         emit UpdatePricePoolPerShare(poolId, scId_, pricePoolPerShare_, computedAt);
     }
```

## ShareClassManager #6907

A share revocation is recorded on the network ledger without lowering the class supply, so burning shares leaves the class total where it was.

- **Mutant:** [`6907.sol`](6907.sol)
- **Caught by:** [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6907`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        // else total.revocations += amount; // MUTATION: the class supply is not lowered
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## ShareClassManager #6908

An issuance credits the issuing network one share more than issued, so network ledgers no longer sum to the class supply.

- **Mutant:** [`6908.sol`](6908.sol)
- **Caught by:** [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6908`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule totalIssuanceIsNetworkNetSum`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -160,7 +160,7 @@
         bool wasNegative = ipn.revocations > ipn.issuances;
 
         if (isIssuance) {
-            ipn.issuances += amount;
+            ipn.issuances += amount + 1; // MUTATION: the issued leg is credited one share too many
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## ShareClassManager #6909

A share issuance is recorded on the network ledger without raising the class supply, so a class emptied to zero can never be filled again.

- **Mutant:** [`6909.sol`](6909.sol)
- **Caught by:** [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6909`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -95,7 +95,7 @@
         require(exists(poolId, scId_), ShareClassNotFound());
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
-        if (isIssuance) total.issuances += amount;
+        if (isIssuance) {} // total.issuances += amount; // MUTATION: the class supply is not raised
         else total.revocations += amount;
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
```

## ShareClassManager #6910

A share issuance raises the class supply by one share more than was issued, so even a movement of nothing moves the books.

- **Mutant:** [`6910.sol`](6910.sol)
- **Caught by:** [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6910`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -95,7 +95,7 @@
         require(exists(poolId, scId_), ShareClassNotFound());
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
-        if (isIssuance) total.issuances += amount;
+        if (isIssuance) total.issuances += amount + 1; // MUTATION: the class supply is raised one share too far
         else total.revocations += amount;
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
```

## ShareClassManager #6911

The per network view subtracts issued from revoked, so any network holding shares fails the query instead of answering.

- **Mutant:** [`6911.sol`](6911.sol)
- **Caught by:** [`rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L245)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6911`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -138,7 +138,7 @@
     function issuance(PoolId poolId, ShareClassId scId_, uint16 centrifugeId) public view returns (uint128) {
         IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
         require(ipn.issuances >= ipn.revocations, NegativeIssuance());
-        return (ipn.issuances - ipn.revocations).toUint128();
+        return (ipn.revocations - ipn.issuances).toUint128(); // MUTATION: the difference is taken the other way round
     }
 
     /// @inheritdoc IShareClassManager
```

## ShareClassManager #6912

A revocation is refused once a network's cumulative burns would pass its cumulative mints, so a network can never run a deficit.

- **Mutant:** [`6912.sol`](6912.sol)
- **Caught by:** [`rcScNetworkRevocationsCanExceedItsIssuances`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L107)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6912`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScNetworkRevocationsCanExceedItsIssuances`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -164,6 +164,7 @@
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
+            require(ipn.revocations <= ipn.issuances, NegativeIssuance()); // MUTATION: a network deficit is refused
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
 
```

## ShareClassManager #6913

Granting authority emits the grant without writing the seat, so the party named is never actually admitted.

- **Mutant:** [`6913.sol`](6913.sol)
- **Caught by:** [`rcScRelyThenDenyRoundTripIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L124)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6913`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScRelyThenDenyRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -23,7 +23,7 @@
 
     /// @inheritdoc IAuth
     function rely(address user) public auth {
-        wards[user] = 1;
+        // wards[user] = 1; // MUTATION: the grant never writes the seat
         emit Rely(user);
     }
 
```

## ShareClassManager #6914

Withdrawing authority installs the seat instead of clearing it, so a party that was denied keeps its powers.

- **Mutant:** [`6914.sol`](6914.sol)
- **Caught by:** [`rcScRelyThenDenyRoundTripIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L124)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6914`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScRelyThenDenyRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        wards[user] = 1; // MUTATION: the withdrawal installs a seat instead of clearing one
         emit Deny(user);
     }
 }
```

## ShareClassManager #6915

A revocation lowers the class supply but not the revoking network's ledger, so that network still shows the burned shares.

- **Mutant:** [`6915.sol`](6915.sol)
- **Caught by:** [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6915`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -163,7 +163,7 @@
             ipn.issuances += amount;
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
-            ipn.revocations += amount;
+            // ipn.revocations += amount; // MUTATION: the revoked leg is never written
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
 
```

## ShareClassManager #6916

A share revocation takes one share more off the class supply than was burned, so the class supply falls below the sum its networks hold.

- **Mutant:** [`6916.sol`](6916.sol)
- **Caught by:** [`hlScCrossChainTransferConservesClassSupply`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L4) · [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6916`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScCrossChainTransferConservesClassSupply hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        else total.revocations += amount + 1; // MUTATION: the class supply is lowered one share too far
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## ShareClassManager #6918

issuance reports zero for a network that revoked more than it issued instead of refusing the read, so a deficit reads as an empty network.

- **Mutant:** [`6918.sol`](6918.sol)
- **Caught by:** [`rvScIssuanceRefusesANetworkInRevocationDeficit`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L61)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 6918`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScIssuanceRefusesANetworkInRevocationDeficit`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -137,8 +137,8 @@
     /// @inheritdoc IShareClassManager
     function issuance(PoolId poolId, ShareClassId scId_, uint16 centrifugeId) public view returns (uint128) {
         IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
-        require(ipn.issuances >= ipn.revocations, NegativeIssuance());
-        return (ipn.issuances - ipn.revocations).toUint128();
+        // MUTATION: a network in deficit degrades to zero instead of being refused
+        return ipn.issuances >= ipn.revocations ? (ipn.issuances - ipn.revocations).toUint128() : 0;
     }
 
     /// @inheritdoc IShareClassManager
```

## ShareClassManager #8011

updateShares and transferShares never report a crossing, so a network that revokes more than it issued is not counted as negative.

- **Mutant:** [`8011.sol`](8011.sol)
- **Caught by:** [`negativeNetworkCountMatchesTheShortNetworks`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L83)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8011`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule negativeNetworkCountMatchesTheShortNetworks`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -167,7 +167,7 @@
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
 
-        _updateNegativeCount(poolId, scId_, centrifugeId, wasNegative, ipn.revocations > ipn.issuances);
+        // MUTATION: the negative network count is never moved
     }
 
     /// @dev Moves the count of networks that have revoked more than they have reported issuing, on a crossing
```

## ShareClassManager #8012

A network whose revocations equal its issuances reads as already negative, so its next update miscounts the networks in deficit.

- **Mutant:** [`8012.sol`](8012.sol)
- **Caught by:** [`negativeNetworkCountMatchesTheShortNetworks`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L83)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8012`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule negativeNetworkCountMatchesTheShortNetworks`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -157,7 +157,7 @@
         internal
     {
         IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
-        bool wasNegative = ipn.revocations > ipn.issuances;
+        bool wasNegative = ipn.revocations >= ipn.issuances; // MUTATION: a flat network reads as negative
 
         if (isIssuance) {
             ipn.issuances += amount;
```

## ShareClassManager #8013

A new function books shares on one class but moves another class's deficit network count, so both counts go wrong.

- **Mutant:** [`8013.sol`](8013.sol)
- **Caught by:** [`classNegativeNetworkCountMatchesItsShortNetworks`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L87)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8013`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule classNegativeNetworkCountMatchesItsShortNetworks`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -113,6 +113,32 @@
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+    }
+
+    /// @notice MUTATION: books a movement on one class while counting its crossing under another class.
+    function updateSharesCountedUnder(
+        uint16 centrifugeId,
+        PoolId poolId,
+        ShareClassId scId_,
+        ShareClassId countedScId,
+        uint128 amount,
+        bool isIssuance
+    ) external auth {
+        require(exists(poolId, scId_), ShareClassNotFound());
+
+        IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
+        IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
+        bool wasNegative = ipn.revocations > ipn.issuances;
+
+        if (isIssuance) {
+            ipn.issuances += amount;
+            total.issuances += amount;
+        } else {
+            ipn.revocations += amount;
+            total.revocations += amount;
+        }
+
+        _updateNegativeCount(poolId, countedScId, centrifugeId, wasNegative, ipn.revocations > ipn.issuances);
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #8014

A revocation now also reads the net class supply, so a report that leaves the class in deficit is refused.

- **Mutant:** [`8014.sol`](8014.sol)
- **Caught by:** [`rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L118)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8014`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        else { total.revocations += amount; totalIssuance(poolId, scId_); } // MUTATION: an over revocation is refused
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## ShareClassManager #8015

totalIssuance returns zero for a class in revocation deficit instead of refusing, so a deficit reads as an empty class.

- **Mutant:** [`8015.sol`](8015.sol)
- **Caught by:** [`rvScTotalIssuanceRefusesAClassInRevocationDeficit`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L141)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8015`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScTotalIssuanceRefusesAClassInRevocationDeficit`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -144,8 +144,7 @@
     /// @inheritdoc IShareClassManager
     function totalIssuance(PoolId poolId, ShareClassId scId_) public view returns (uint128) {
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
-        require(total.issuances >= total.revocations, NegativeIssuance());
-        return (total.issuances - total.revocations).toUint128();
+        return total.issuances > total.revocations ? (total.issuances - total.revocations).toUint128() : 0; // MUTATION: a deficit reads as zero
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #8016

totalIssuance refuses a class whose revocations exactly match its issuances, so a fully retired class cannot report its zero supply.

- **Mutant:** [`8016.sol`](8016.sol)
- **Caught by:** [`rvScTotalIssuanceAnswersAClassNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L262)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8016`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScTotalIssuanceAnswersAClassNeitherInDeficitNorPastUint128`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -144,7 +144,7 @@
     /// @inheritdoc IShareClassManager
     function totalIssuance(PoolId poolId, ShareClassId scId_) public view returns (uint128) {
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
-        require(total.issuances >= total.revocations, NegativeIssuance());
+        require(total.issuances > total.revocations, NegativeIssuance()); // MUTATION: a flat class is refused
         return (total.issuances - total.revocations).toUint128();
     }
 
```

## ShareClassManager #8017

a revocation is taken off the class issued counter instead of added to its revoked counter, so the cumulative issued total walks backwards.

- **Mutant:** [`8017.sol`](8017.sol)
- **Caught by:** [`vtScClassIssuedTotalNeverDecreases`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8017`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_transitions.conf --rule vtScClassIssuedTotalNeverDecreases`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        else total.issuances -= amount; // MUTATION: a revocation lowers the issued counter
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## ShareClassManager #8018

an issuance is taken off the class revoked counter instead of added to its issued counter, so the cumulative revoked total walks backwards.

- **Mutant:** [`8018.sol`](8018.sol)
- **Caught by:** [`vtScClassRevokedTotalNeverDecreases`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L51)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8018`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_transitions.conf --rule vtScClassRevokedTotalNeverDecreases`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -95,7 +95,7 @@
         require(exists(poolId, scId_), ShareClassNotFound());
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
-        if (isIssuance) total.issuances += amount;
+        if (isIssuance) total.revocations -= amount; // MUTATION: an issuance lowers the revoked counter
         else total.revocations += amount;
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
```

## ShareClassManager #8019

updateShares books every issuance as a revocation and every revocation as an issuance, so supply moves the wrong way.

- **Mutant:** [`8019.sol`](8019.sol)
- **Caught by:** [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8019`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -93,6 +93,7 @@
         auth
     {
         require(exists(poolId, scId_), ShareClassNotFound());
+        isIssuance = !isIssuance; // MUTATION: an issuance books the revoked legs and a revocation the issued legs
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
```

## ShareClassManager #8040

totalIssuance adds the revoked counter instead of subtracting it, so a class that burned shares reports inflated supply.

- **Mutant:** [`8040.sol`](8040.sol)
- **Caught by:** [`hlScSupplyViewsReportIssuedMinusRevoked`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L97)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8040`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyViewsReportIssuedMinusRevoked`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -145,7 +145,7 @@
     function totalIssuance(PoolId poolId, ShareClassId scId_) public view returns (uint128) {
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         require(total.issuances >= total.revocations, NegativeIssuance());
-        return (total.issuances - total.revocations).toUint128();
+        return (total.issuances + total.revocations).toUint128(); // MUTATION: the revoked counter is added to the supply
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #8041

The deficit network count now rises on every report leaving a network short and never falls, so it overcounts short networks.

- **Mutant:** [`8041.sol`](8041.sol)
- **Caught by:** [`rcScNegativeNetworkCountOpensAndCloses`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L142)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8041`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScNegativeNetworkCountOpensAndCloses`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -179,7 +179,7 @@
         bool wasNegative,
         bool isNegative
     ) internal {
-        if (wasNegative == isNegative) return;
+        if (!isNegative) return; // MUTATION: leaving the deficit is never counted back
 
         uint32 count = isNegative ? ++negativeNetworkCount[poolId][scId_] : --negativeNetworkCount[poolId][scId_];
         emit UpdateNegativeNetworkCount(poolId, scId_, centrifugeId, count);
```

## ShareClassManager #8042

a revocation past the class supply is refused again, so a burn reported before its mint can never leave the class short.

- **Mutant:** [`8042.sol`](8042.sol)
- **Caught by:** [`rcScRefusedClassSupplyIsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L162)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8042`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScRefusedClassSupplyIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        else { total.revocations += amount; require(total.issuances >= total.revocations, NegativeIssuance()); } // MUTATION: the supply is floored again
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## ShareClassManager #8043

updateSharePrice resets the short network count, so a class in shortfall reads as whole after any repricing.

- **Mutant:** [`8043.sol`](8043.sol)
- **Caught by:** [`stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8043`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_transitions.conf --rule stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -72,6 +72,7 @@
 
         p.price = pricePoolPerShare_;
         p.computedAt = computedAt;
+        negativeNetworkCount[poolId][scId_] = 0; // MUTATION: a repricing clears the shortfall tally
         emit UpdatePricePoolPerShare(poolId, scId_, pricePoolPerShare_, computedAt);
     }
 
```

## ShareClassManager #8045

a network issuance leg is also credited to the next network id, so a network the call never named gains shares.

- **Mutant:** [`8045.sol`](8045.sol)
- **Caught by:** [`hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8045`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScSupplyUpdateBooksOneLegOfTheNetworkAndTheClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -160,7 +160,7 @@
         bool wasNegative = ipn.revocations > ipn.issuances;
 
         if (isIssuance) {
-            ipn.issuances += amount;
+            ipn.issuances += amount; issuancePerNetwork[poolId][scId_][centrifugeId + 1].issuances += amount; // MUTATION: the neighbouring network is credited with the same issuance
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## ShareClassManager #8050

a revocation past the class supply is refused again, so a burn reported before its mint is stranded with its nonce unspent.

- **Mutant:** [`8050.sol`](8050.sol)
- **Caught by:** [`rvHhShareReportIsNeverStrandedWhileTheCountersHaveRoom`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reverts.spec#L202)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8050`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reverts.conf --rule rvHhShareReportIsNeverStrandedWhileTheCountersHaveRoom`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        else { total.revocations += amount; require(total.issuances >= total.revocations, NegativeIssuance()); } // MUTATION: an over revocation is refused again
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## ShareClassManager #8051

the deficit update of a network leg passes the old state as the new one, so the short network count never moves.

- **Mutant:** [`8051.sol`](8051.sol)
- **Caught by:** [`rcHhShareReportPastTheClassSupplyIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L557)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8051`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhShareReportPastTheClassSupplyIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -167,7 +167,7 @@
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
 
-        _updateNegativeCount(poolId, scId_, centrifugeId, wasNegative, ipn.revocations > ipn.issuances);
+        _updateNegativeCount(poolId, scId_, centrifugeId, wasNegative, wasNegative); // MUTATION: the crossing is never seen
     }
 
     /// @dev Moves the count of networks that have revoked more than they have reported issuing, on a crossing
```

## ShareClassManager #8054

The post-update deficit test is transposed, so solvent reports are counted and networks going short are not.

- **Mutant:** [`8054.sol`](8054.sol)
- **Caught by:** [`stHhNegativeNetworkCountFollowsTheShortNetworks`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_transitions.spec#L209)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8054`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/transitions.conf --rule stHhNegativeNetworkCountFollowsTheShortNetworks`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -167,7 +167,7 @@
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
 
-        _updateNegativeCount(poolId, scId_, centrifugeId, wasNegative, ipn.revocations > ipn.issuances);
+        _updateNegativeCount(poolId, scId_, centrifugeId, wasNegative, ipn.issuances > ipn.revocations); // MUTATION: transposed crossing test
     }
 
     /// @dev Moves the count of networks that have revoked more than they have reported issuing, on a crossing
```

## ShareClassManager #8057

a network leaving its shortfall is never counted back out, so the short network count never comes down.

- **Mutant:** [`8057.sol`](8057.sol)
- **Caught by:** [`rcHhBridgeClearsAShortTargetNetworkIsReachable`](../../specs/core/hub/HubHandler_LinkedHubCore/HubHandler_LinkedHubCore_reachability.spec#L600)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8057`
- **Run on clean src:** `certoraRun certora/confs/core/hub/HubHandler_LinkedHubCore/reachability.conf --rule rcHhBridgeClearsAShortTargetNetworkIsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -179,7 +179,7 @@
         bool wasNegative,
         bool isNegative
     ) internal {
-        if (wasNegative == isNegative) return;
+        if (wasNegative == isNegative || !isNegative) return; // MUTATION: the release leg never fires
 
         uint32 count = isNegative ? ++negativeNetworkCount[poolId][scId_] : --negativeNetworkCount[poolId][scId_];
         emit UpdateNegativeNetworkCount(poolId, scId_, centrifugeId, count);
```

## ShareClassManager #8200

The issued and revoked fields swap order, so a raw class or network read returns the revoked figure as issued.

- **Mutant:** [`8200.sol`](8200.sol)
- **Caught by:** [`rvScRawCountersAlwaysAnswerWithTheLedger`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L157)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8200`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScRawCountersAlwaysAnswerWithTheLedger`

```diff
--- a/src/core/hub/interfaces/IShareClassManager.sol
+++ b/src/core/hub/interfaces/IShareClassManager.sol
@@ -25,10 +25,7 @@
 }
 
 struct IssuanceCounters {
-    /// @dev Total accumulated amount of shares issued
-    uint256 issuances;
-    /// @dev Total accumulated amount of shares revoked
-    uint256 revocations;
+    uint256 revocations; uint256 issuances; // MUTATION: the two counters trade places, so every raw read answers the revoked figure first
 }
 
 interface IShareClassManager {
```

## ShareClassManager #8201

updateMetadata runs without its ward gate, so any caller can rename a share class and change its symbol.

- **Mutant:** [`8201.sol`](8201.sol)
- **Caught by:** [`rvScUpdateMetadataRefusesANonWardAnUnknownClassOrBadLengths`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L119)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8201`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/unpinned_properties.conf --rule rvScUpdateMetadataRefusesANonWardAnUnknownClassOrBadLengths`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -78,7 +78,7 @@
     /// @inheritdoc IShareClassManager
     function updateMetadata(PoolId poolId, ShareClassId scId_, string calldata name, string calldata symbol)
         external
-        auth
+        // MUTATION: the metadata update no longer asks for a ward
     {
         require(exists(poolId, scId_), ShareClassNotFound());
 
```

## ShareClassManager #8419

transferShares also raises the class issued and revoked totals, so moving shares between networks is booked as supply issued and revoked.

- **Mutant:** [`8419.sol`](8419.sol)
- **Caught by:** [`hlScTransferSharesMovesOnlyTheTwoNetworkLegs`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L139)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8419`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScTransferSharesMovesOnlyTheTwoNetworkLegs`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -113,6 +113,8 @@
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+        issuanceAcrossNetworks[poolId][scId_].issuances += amount; // MUTATION: a transfer is booked as class supply
+        issuanceAcrossNetworks[poolId][scId_].revocations += amount;
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #8420

transferShares also raises the class issued and revoked totals, so a transfer between networks changes the class supply totals.

- **Mutant:** [`8420.sol`](8420.sol)
- **Caught by:** [`stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_transitions.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8420`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_transitions.conf --rule stScClassTotalsMoveOnlyOnASupplyUpdateNetworkLegsAlsoOnATransfer`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -113,6 +113,8 @@
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+        issuanceAcrossNetworks[poolId][scId_].issuances += amount; // MUTATION: a transfer is booked as class supply
+        issuanceAcrossNetworks[poolId][scId_].revocations += amount;
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #8421

transferShares issues on the source network and revokes on the destination, so shares move the wrong way between networks.

- **Mutant:** [`8421.sol`](8421.sol)
- **Caught by:** [`hlScTransferSharesMovesOnlyTheTwoNetworkLegs`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L139)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8421`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScTransferSharesMovesOnlyTheTwoNetworkLegs`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -111,8 +111,8 @@
     ) external auth {
         require(exists(poolId, scId_), ShareClassNotFound());
 
-        _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
-        _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
+        _updateNetwork(poolId, scId_, fromCentrifugeId, amount, true); // MUTATION: the two legs are swapped
+        _updateNetwork(poolId, scId_, toCentrifugeId, amount, false);
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #8422

transferShares skips the share class existence check, so a transfer on a class that was never created goes through.

- **Mutant:** [`8422.sol`](8422.sol)
- **Caught by:** [`rvScTransferSharesRefusesANonWardOrAnUnknownClass`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L181)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8422`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScTransferSharesRefusesANonWardOrAnUnknownClass`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -109,7 +109,7 @@
         uint16 toCentrifugeId,
         uint128 amount
     ) external auth {
-        require(exists(poolId, scId_), ShareClassNotFound());
+        // require(exists(poolId, scId_), ShareClassNotFound()); // MUTATION: a transfer skips the class check
 
         _updateNetwork(poolId, scId_, fromCentrifugeId, amount, false);
         _updateNetwork(poolId, scId_, toCentrifugeId, amount, true);
```

## ShareClassManager #8423

updateShares and transferShares reject a revocation beyond the network's issued total, so a transfer that leaves a network in deficit fails.

- **Mutant:** [`8423.sol`](8423.sol)
- **Caught by:** [`rvScTransferSharesNeverRefusesAWardWhileTheLegsHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L196) · [`rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L118)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8423`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScTransferSharesNeverRefusesAWardWhileTheLegsHaveRoom rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -164,6 +164,7 @@
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
+            require(ipn.revocations <= ipn.issuances, NegativeIssuance()); // MUTATION: a network deficit is refused
             emit RemoteRevokeShares(centrifugeId, poolId, scId_, amount);
         }
 
```

## ShareClassManager #8424

updateShares and transferShares cap a network's issued total at 128 bits, so an issuance or transfer that the 256-bit counter holds fails.

- **Mutant:** [`8424.sol`](8424.sol)
- **Caught by:** [`rvScTransferSharesNeverRefusesAWardWhileTheLegsHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L196) · [`rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L118)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8424`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScTransferSharesNeverRefusesAWardWhileTheLegsHaveRoom rvScUpdateSharesNeverRefusesAWardWhileTheCountersHaveRoom`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -161,6 +161,7 @@
 
         if (isIssuance) {
             ipn.issuances += amount;
+            require(ipn.issuances <= type(uint128).max); // MUTATION: the issued leg is capped at the old uint128 width
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## ShareClassManager #8425

the network issuance query truncates a supply past 128 bits to its low bits instead of failing, so an oversized network reports a wrong small supply.

- **Mutant:** [`8425.sol`](8425.sol)
- **Caught by:** [`rvScIssuanceRefusesANetworkNetPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L217)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8425`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScIssuanceRefusesANetworkNetPastUint128`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -138,7 +138,7 @@
     function issuance(PoolId poolId, ShareClassId scId_, uint16 centrifugeId) public view returns (uint128) {
         IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
         require(ipn.issuances >= ipn.revocations, NegativeIssuance());
-        return (ipn.issuances - ipn.revocations).toUint128();
+        return uint128(ipn.issuances - ipn.revocations); // MUTATION: an oversized net is truncated instead of refused
     }
 
     /// @inheritdoc IShareClassManager
```

## ShareClassManager #8426

totalIssuance truncates a class supply past 128 bits to its low bits instead of failing, so an oversized class reports a wrong small supply.

- **Mutant:** [`8426.sol`](8426.sol)
- **Caught by:** [`rvScTotalIssuanceRefusesAClassNetPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L231)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8426`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScTotalIssuanceRefusesAClassNetPastUint128`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -145,7 +145,7 @@
     function totalIssuance(PoolId poolId, ShareClassId scId_) public view returns (uint128) {
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         require(total.issuances >= total.revocations, NegativeIssuance());
-        return (total.issuances - total.revocations).toUint128();
+        return uint128(total.issuances - total.revocations); // MUTATION: an oversized net is truncated instead of refused
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #8427

the network issuance query narrows the issued and revoked totals separately instead of their difference, so it fails for a network whose issued total passed 128 bits although its supply fits.

- **Mutant:** [`8427.sol`](8427.sol)
- **Caught by:** [`rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L245)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8427`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScIssuanceAnswersANetworkNeitherInDeficitNorPastUint128`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -138,7 +138,7 @@
     function issuance(PoolId poolId, ShareClassId scId_, uint16 centrifugeId) public view returns (uint128) {
         IssuanceCounters storage ipn = issuancePerNetwork[poolId][scId_][centrifugeId];
         require(ipn.issuances >= ipn.revocations, NegativeIssuance());
-        return (ipn.issuances - ipn.revocations).toUint128();
+        return ipn.issuances.toUint128() - ipn.revocations.toUint128(); // MUTATION: each leg is narrowed instead of the net
     }
 
     /// @inheritdoc IShareClassManager
```

## ShareClassManager #8428

totalIssuance narrows the issued and revoked totals separately instead of their difference, so it fails for a class whose issued total passed 128 bits although its supply fits.

- **Mutant:** [`8428.sol`](8428.sol)
- **Caught by:** [`rvScTotalIssuanceAnswersAClassNeitherInDeficitNorPastUint128`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reverts.spec#L262)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8428`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reverts.conf --rule rvScTotalIssuanceAnswersAClassNeitherInDeficitNorPastUint128`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -145,7 +145,7 @@
     function totalIssuance(PoolId poolId, ShareClassId scId_) public view returns (uint128) {
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         require(total.issuances >= total.revocations, NegativeIssuance());
-        return (total.issuances - total.revocations).toUint128();
+        return total.issuances.toUint128() - total.revocations.toUint128(); // MUTATION: each total is narrowed instead of the net
     }
 
     //----------------------------------------------------------------------------------------------
```

## ShareClassManager #8429

updateShares and transferShares cap a network's issued total at 128 bits, so no issuance can lift a network's supply past that width.

- **Mutant:** [`8429.sol`](8429.sol)
- **Caught by:** [`rcScNetworkNetPastUint128IsReachable`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L178)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8429`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScNetworkNetPastUint128IsReachable`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -161,6 +161,7 @@
 
         if (isIssuance) {
             ipn.issuances += amount;
+            require(ipn.issuances <= type(uint128).max); // MUTATION: the issued leg is capped at the old uint128 width
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## ShareClassManager #8951

addShareClass no longer refuses a consumed salt, so two classes of a pool can carry the same salt.

- **Mutant:** [`8951.sol`](8951.sol)
- **Caught by:** [`classSaltsDistinct`](../../specs/core/hub/ShareClassManager/ShareClassManager_multi_share_class_properties.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 8951`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/multi_share_class_properties.conf --rule classSaltsDistinct`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -46,7 +46,7 @@
 
         PoolId prefixedPoolId = PoolId.wrap(uint64(bytes8(salt)));
         require(poolId == prefixedPoolId, InvalidSalt());
-        require(!salts[salt], AlreadyUsedSalt());
+        // require(!salts[salt], AlreadyUsedSalt()); // MUTATION: a consumed salt no longer closes the gate
 
         scId_ = previewNextShareClassId(poolId);
 
```

## ShareClassManager #9005

renaming a share class also clears the salt it was created under, so the class forgets the identity its token was deployed with.

- **Mutant:** [`9005.sol`](9005.sol)
- **Caught by:** [`hlScUpdateMetadataWritesOnlyItsClassesStrings`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L71)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9005`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/unpinned_properties.conf --rule hlScUpdateMetadataWritesOnlyItsClassesStrings`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -197,6 +197,6 @@
 
         meta = metadata[poolId][scId_];
         meta.name = name;
-        meta.symbol = symbol;
+        meta.symbol = symbol; meta.salt = bytes32(0); // MUTATION: the rename also clears the class salt
     }
 }
```

## ShareClassManager #9050

The class id shifts the pool id only 16 bits above the index, so two pool and index pairs can share an id.

- **Mutant:** [`9050.sol`](9050.sol)
- **Caught by:** [`hlScShareClassIdIsInjectiveInPoolAndIndex`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L111)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9050`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScShareClassIdIsInjectiveInPoolAndIndex`

```diff
--- a/src/core/types/ShareClassId.sol
+++ b/src/core/types/ShareClassId.sol
@@ -22,7 +22,7 @@
 }
 
 function newShareClassId(PoolId poolId, uint32 index_) pure returns (ShareClassId scId) {
-    return ShareClassId.wrap(bytes16((uint128(PoolId.unwrap(poolId)) << 64) + index_));
+    return ShareClassId.wrap(bytes16((uint128(PoolId.unwrap(poolId)) << 16) + index_)); // MUTATION: the pool id is shifted by 16 bits instead of 64
 }
 
 using {isNull, index, raw, equals as ==} for ShareClassId global;
```

## ShareClassManager #9051

updateMetadata also winds the pool's class counter back by one, so a class on record sits at an index above the pool's class count.

- **Mutant:** [`9051.sol`](9051.sol)
- **Caught by:** [`recordedClassIdSitsUnderItsPoolWithinCount`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9051`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/unpinned_properties.conf --rule recordedClassIdSitsUnderItsPoolWithinCount`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -82,7 +82,7 @@
     {
         require(exists(poolId, scId_), ShareClassNotFound());
 
-        _updateMetadata(poolId, scId_, name, symbol);
+        _updateMetadata(poolId, scId_, name, symbol); shareClassCount[poolId]--; // MUTATION: a metadata update rewinds the class counter
 
         emit UpdateMetadata(poolId, scId_, name, symbol);
     }
```

## ShareClassManager #9052

addShareClass also records the new class id under the next pool id, so one class id is on record under two pools.

- **Mutant:** [`9052.sol`](9052.sol)
- **Caught by:** [`classIdIsOnRecordUnderOnePoolOnly`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L13) · [`recordedClassIdSitsUnderItsPoolWithinCount`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9052`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/unpinned_properties.conf --rule classIdIsOnRecordUnderOnePoolOnly recordedClassIdSitsUnderItsPoolWithinCount`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -51,7 +51,7 @@
         scId_ = previewNextShareClassId(poolId);
 
         uint32 index = ++shareClassCount[poolId];
-        shareClassIds[poolId][scId_] = true;
+        shareClassIds[poolId][scId_] = true; shareClassIds[PoolId.wrap(poolId.raw() + 1)][scId_] = true; // MUTATION: the class is also recorded under the next pool
 
         ShareClassMetadata storage meta = _updateMetadata(poolId, scId_, name, symbol);
 
```

## ShareClassManager #9053

updateMetadata takes the class it renames off record, so an existing class stops existing after a metadata update.

- **Mutant:** [`9053.sol`](9053.sol)
- **Caught by:** [`stScRecordedClassStaysRecorded`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L27)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9053`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/unpinned_properties.conf --rule stScRecordedClassStaysRecorded`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -82,7 +82,7 @@
     {
         require(exists(poolId, scId_), ShareClassNotFound());
 
-        _updateMetadata(poolId, scId_, name, symbol);
+        _updateMetadata(poolId, scId_, name, symbol); shareClassIds[poolId][scId_] = false; // MUTATION: a metadata update removes the class from record
 
         emit UpdateMetadata(poolId, scId_, name, symbol);
     }
```

## ShareClassManager #9054

addShareClass always mints the index one id, so every later class reuses the pool's first class id.

- **Mutant:** [`9054.sol`](9054.sol)
- **Caught by:** [`hlScCreationMintsTheNextFreshIndex`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L42)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9054`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/unpinned_properties.conf --rule hlScCreationMintsTheNextFreshIndex`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -48,7 +48,7 @@
         require(poolId == prefixedPoolId, InvalidSalt());
         require(!salts[salt], AlreadyUsedSalt());
 
-        scId_ = previewNextShareClassId(poolId);
+        scId_ = previewShareClassId(poolId, 1); // MUTATION: the id of index one instead of the next index
 
         uint32 index = ++shareClassCount[poolId];
         shareClassIds[poolId][scId_] = true;
```

## ShareClassManager #9055

updateShares books a revocation on the network but not on the class total, so the class supply stays above the net summed over every network.

- **Mutant:** [`9055.sol`](9055.sol)
- **Caught by:** [`totalIssuanceIsNetworkNetSum`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_valid_state.spec#L57)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9055`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_valid_state.conf --rule totalIssuanceIsNetworkNetSum`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -96,7 +96,7 @@
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
         if (isIssuance) total.issuances += amount;
-        else total.revocations += amount;
+        // else total.revocations += amount; // MUTATION: the class total misses the revocation
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
     }
```

## ShareClassManager #9057

a network issuance leg is booked on its revoked counter, so the revoked sum rises instead of the issued sum.

- **Mutant:** [`9057.sol`](9057.sol)
- **Caught by:** [`hlScAnUpdateMovesItsLegByItsAmount`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_high_level.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9057`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_high_level.conf --rule hlScAnUpdateMovesItsLegByItsAmount`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -160,7 +160,7 @@
         bool wasNegative = ipn.revocations > ipn.issuances;
 
         if (isIssuance) {
-            ipn.issuances += amount;
+            ipn.revocations += amount; // MUTATION: the issuance is booked on the network's revoked leg
             emit RemoteIssueShares(centrifugeId, poolId, scId_, amount);
         } else {
             ipn.revocations += amount;
```

## ShareClassManager #9065

A share issuance credits the issuing network but never the class supply, so the class total stays where it was.

- **Mutant:** [`9065.sol`](9065.sol)
- **Caught by:** [`rcScClassSupplyCanReachItsStoredCeiling`](../../specs/core/hub/ShareClassManager/single/ShareClassManager_single_pool_reachability.spec#L91)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9065`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/single_pool_reachability.conf --rule rcScClassSupplyCanReachItsStoredCeiling`

```diff
--- a/src/core/hub/ShareClassManager.sol
+++ b/src/core/hub/ShareClassManager.sol
@@ -95,7 +95,7 @@
         require(exists(poolId, scId_), ShareClassNotFound());
 
         IssuanceCounters storage total = issuanceAcrossNetworks[poolId][scId_];
-        if (isIssuance) total.issuances += amount;
+        if (isIssuance) {} // MUTATION: the class supply write of an issuance is removed
         else total.revocations += amount;
 
         _updateNetwork(poolId, scId_, centrifugeId, amount, isIssuance);
```

## ShareClassManager #9942

The class id shifts the pool by 32 bits instead of 64, so the pool no longer sits in the high eight bytes.

- **Mutant:** [`9942.sol`](9942.sol)
- **Caught by:** [`hlScClassIdIsThePoolOverTheIndex`](../../specs/core/hub/ShareClassManager/ShareClassManager_unpinned_properties.spec#L60)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh ShareClassManager 9942`
- **Run on clean src:** `certoraRun certora/confs/core/hub/ShareClassManager/unpinned_properties.conf --rule hlScClassIdIsThePoolOverTheIndex`

```diff
--- a/src/core/types/ShareClassId.sol
+++ b/src/core/types/ShareClassId.sol
@@ -22,7 +22,7 @@
 }
 
 function newShareClassId(PoolId poolId, uint32 index_) pure returns (ShareClassId scId) {
-    return ShareClassId.wrap(bytes16((uint128(PoolId.unwrap(poolId)) << 64) + index_));
+    return ShareClassId.wrap(bytes16((uint128(PoolId.unwrap(poolId)) << 32) + index_)); // MUTATION: the pool id is shifted by 32 bits instead of 64
 }
 
 using {isNull, index, raw, equals as ==} for ShareClassId global;
```

