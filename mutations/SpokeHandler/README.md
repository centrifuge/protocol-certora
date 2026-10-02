# Mutations for `SpokeHandler` (`src/core/spoke/SpokeHandler.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/spoke/SpokeRegistry.sol`, `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [3205](#spokehandler-3205) | setPolicy installs a replacement without advancing the install counter, so outstanding authorizations survive the swap.<br>Caught by: [`stShPolicySwapAdvancesTheAuthorizationNamespace`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L136) |
| [3206](#spokehandler-3206) | updatePricePoolPerShare drops the existence check, so a price is seeded onto a share class that was never created.<br>Caught by: [`stShPricesNeedTheRowsTheyPriceTo`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L168) |
| [3207](#spokehandler-3207) | addPool enters the pool in the registry without deploying its escrow, so a live pool can exist with no custody contract behind it.<br>Caught by: [`stShPoolRowNeedsTheEscrowDeployBehindIt`](../../specs/core/spoke/SpokeHandler_LinkedRegistryFactory/SpokeHandler_LinkedRegistryFactory_properties.spec#L6) |
| [3208](#spokehandler-3208) | linking a vault also moves the asset id it serves, so a link toggle changes the vault's identity.<br>Caught by: [`stShVaultLinkNeverMovesItsIdentity`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L95) |
| [3209](#spokehandler-3209) | filing an authorization also advances the policy nonce, so an authorization moves while the namespace it is filed under shifts.<br>Caught by: [`stShAuthorizationsMoveOnlyWithinAStandingNamespace`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L151) |
| [3210](#spokehandler-3210) | addShareClass files the token's reverse lookup under a neighbour pool, so the newly bound token no longer looks back to its own class.<br>Caught by: [`stShShareClassBindsTheRegistrarsTokenAndItsLookupBack`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L117) |
| [3219](#spokehandler-3219) | addShareClass binds the registry itself instead of the registrar's new token, so the class points at the wrong contract.<br>Caught by: [`stShShareClassBindsTheRegistrarsTokenAndItsLookupBack`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L117) |
| [4700](#spokehandler-4700) | file loses its ward gate, so any caller repoints the handler at a registry and an escrow factory of its own.<br>Caught by: [`acShRegistryPointerMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L20) · [`acShEscrowFactoryPointerMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L36) |
| [4701](#spokehandler-4701) | addPool loses its ward gate, so any caller opens a pool on this spoke and stamps its registry row.<br>Caught by: [`acShPoolRowMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L53) |
| [4702](#spokehandler-4702) | addShareClass loses its ward gate, so any caller binds a share class to a registrar and token of its own.<br>Caught by: [`acShShareClassBindingMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L69) · [`acShTokenLookupMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L88) |
| [4703](#spokehandler-4703) | updateManager loses its ward gate, so any caller hands out or withdraws the manager seat that runs a pool's balance sheet.<br>Caught by: [`acShManagerSeatMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L107) |
| [4704](#spokehandler-4704) | updateBridger loses its ward gate, so any caller hands out or withdraws the right to burn a pool's shares for a cross chain transfer.<br>Caught by: [`acShBridgerSeatMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L123) |
| [4705](#spokehandler-4705) | setPolicy loses its ward gate, so any caller swaps a pool's policy and voids its pending authorizations.<br>Caught by: [`acShPolicyRowMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L139) |
| [4706](#spokehandler-4706) | authorize loses its ward gate, so any caller files a standing permission in the pool's consume only ledger.<br>Caught by: [`acShAuthorizationLedgerMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L158) |
| [4707](#spokehandler-4707) | updatePricePoolPerShare loses its ward gate, so any caller reprices a share class and every local vault settles against the number it invented.<br>Caught by: [`acShSharePriceMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L174) |
| [4708](#spokehandler-4708) | updatePricePoolPerAsset loses its ward gate, so any caller misprices the asset leg every deposit and withdrawal settles through.<br>Caught by: [`acShAssetPriceMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L193) |
| [4709](#spokehandler-4709) | updateVault loses its ward gate, so any caller registers a vault of its own or switches an existing one into and out of the router.<br>Caught by: [`acShVaultRowMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L212) |
| [4710](#spokehandler-4710) | setRequestManager loses its ward gate, so any caller makes itself the callee of every request the hub sends this pool.<br>Caught by: [`acShRequestManagerPointerMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L241) |
| [4711](#spokehandler-4711) | executeTransferShares loses its ward gate, so any caller mints shares to any receiver with no transfer from the hub.<br>Caught by: [`acShShareSupplyMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L257) · [`acShHolderBalanceMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L273) |
| [4712](#spokehandler-4712) | requestCallback loses its ward gate, so any caller drives the pool's request pipeline with traffic the hub never sent.<br>Caught by: [`acShRequestCallbackGoesOutOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L289) |
| [4713](#spokehandler-4713) | The auth modifier's ward test is inverted, so only non-wards pass and any of them can make itself a ward.<br>Caught by: [`acShWardRosterMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L4) |
| [4714](#spokehandler-4714) | file no longer refuses a name it does not know, so a wiring message naming nothing is accepted in silence instead of rejected.<br>Caught by: [`rvShFileRefusesANonWardOrAnUnknownName`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L4) |
| [4715](#spokehandler-4715) | addPool's existence check is inverted, so a new pool is refused and a pool already added is added again.<br>Caught by: [`rvShAddPoolRefusesAnUntrustedCallerOrAPoolAlreadyOpen`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L19) |
| [4716](#spokehandler-4716) | the share token uniqueness test is read inverted, so a token another class already claims is accepted and a token still free is refused.<br>Caught by: [`rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L35) · [`rvShAddShareClassAcceptsACleanRegistration`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L329) |
| [4717](#spokehandler-4717) | isPoolActive requires a creation time in the future, so every pool the hub opened reads inactive and its updates fail.<br>Caught by: [`rvShUpdateManagerIsNeverRefusedOnAPoolTheHubOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L380) |
| [4718](#spokehandler-4718) | hasShareClass checks the registrar slot instead of the token slot, so a class with a registrar but no token reads as present.<br>Caught by: [`rvShUpdatePricePoolPerShareRefusesAnUntrustedCallerAnAbsentClassOrAnOlderStamp`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L143) · [`rvShUpdatePricePoolPerAssetRefusesAnUntrustedCallerAnUnknownRowOrAnOlderStamp`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L162) |
| [4719](#spokehandler-4719) | authorize drops the installed policy check, so a grant is filed on a pool with no policy instead of refused.<br>Caught by: [`rvShAuthorizeRefusesAnUntrustedCallerOrAPoolWithNoRuleBook`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L108) |
| [4720](#spokehandler-4720) | unauthorize demands two outstanding grants where one is enough, so the last grant a pool holds can no longer be revoked.<br>Caught by: [`rvShUnauthorizeIsNeverRefusedOnAGrantThatStands`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L398) |
| [4721](#spokehandler-4721) | updateRestriction drops the share token check, so a restriction is pushed at a class this chain does not carry instead of being refused.<br>Caught by: [`rvShUpdateRestrictionRefusesAnUntrustedCallerOrAClassTheSpokeDoesNotCarry`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L218) |
| [4722](#spokehandler-4722) | executeTransferShares casts the receiver word unchecked, so a word with nonzero trailing bytes is paid out instead of refused.<br>Caught by: [`rvShExecuteTransferSharesRefusesAnAbsentClassOrAMalformedReceiver`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L236) |
| [4723](#spokehandler-4723) | linkVault drops the registered vault check, so a link message activates an address never registered as a vault.<br>Caught by: [`rvShUpdateVaultLinkRefusesAnUnknownOrMismatchedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L257) |
| [4724](#spokehandler-4724) | requestCallback inverts its manager check, so a callback to a pool with a request manager is refused.<br>Caught by: [`rvShRequestCallbackIsNeverRefusedOnAPoolThatHasARequestManager`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L417) |
| [4725](#spokehandler-4725) | rely loses its ward gate in the shared Auth mixin, so authority over the handler is handed on by an account that never held it.<br>Caught by: [`rvShRelyRefusesANonWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L354) |
| [4726](#spokehandler-4726) | deny loses its ward gate in the shared Auth mixin, so authority over the handler is withdrawn by an account that never held it.<br>Caught by: [`rvShDenyRefusesANonWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L367) |
| [4727](#spokehandler-4727) | executeTransferShares mints one share more than it delivers, so every bridge arrival inflates supply by one.<br>Caught by: [`hlShExecuteTransferSharesMintsExactlyTheBridgedAmount`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L5) |
| [4728](#spokehandler-4728) | executeTransferShares sends the minted shares to the handler itself, so the named receiver gets nothing.<br>Caught by: [`hlShExecuteTransferSharesPaysTheReceiverInFull`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L21) · [`hlShExecuteTransferSharesAddressedPastTheHandlerLeavesNoResidue`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L39) |
| [4729](#spokehandler-4729) | updateRestriction also mints one share to the handler, so a restriction message inflates the share supply.<br>Caught by: [`vtShShareSupplyMovesOnlyOnTheTransferExecutor`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L41) |
| [4730](#spokehandler-4730) | deploy and link registers the new vault but never links it, so the vault is left unroutable.<br>Caught by: [`hlShDeployAndLinkLeavesTheNewVaultLinked`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L57) |
| [4732](#spokehandler-4732) | unlinkVault shifts the vault's asset id instead of clearing its link flag, so the vault stays linked under a wrong asset.<br>Caught by: [`hlShLinkThenUnlinkRestoresTheRoutingFlag`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L95) · [`hlShLinkThenUnlinkLeavesTheVaultIdentityUntouched`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L111) |
| [4733](#spokehandler-4733) | the bridger role update also sets the manager role, so a bridging grant hands out balance sheet control.<br>Caught by: [`vtShManagerSeatMovesOnlyOnItsRoleMessage`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L59) |
| [4734](#spokehandler-4734) | the manager role update also sets the bridger role, so a manager grant hands out share bridging rights.<br>Caught by: [`vtShBridgerSeatMovesOnlyOnItsRoleMessage`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L76) |
| [4735](#spokehandler-4735) | addPool only looks up the escrow address instead of deploying it, so the pool opens with no escrow deployed.<br>Caught by: [`hlShAddPoolAsksTheEscrowFactoryExactlyOnce`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L137) · [`hlShAddPoolAsksTheEscrowFactoryForThatPool`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L151) |
| [4736](#spokehandler-4736) | a fulfillment coming back from the hub is handed to the pool's request manager twice, so one inbound request is processed as two.<br>Caught by: [`hlShRequestCallbackIsDeliveredExactlyOnce`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L163) |
| [4737](#spokehandler-4737) | requestCallback calls the escrow factory instead of the pool's request manager, so the manager never gets the callback.<br>Caught by: [`hlShRequestCallbackReachesTheRegisteredManager`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L178) |
| [4738](#spokehandler-4738) | a revocation checks the row and then writes it back unchanged, so a grant survives the revocation that was meant to cancel it.<br>Caught by: [`hlShGrantThenRevokeLeavesTheLedgerUntouched`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L193) |
| [4739](#spokehandler-4739) | addShareClass drops the already registered check, so a live class can be rebound to another token and registrar.<br>Caught by: [`vtShLiveShareClassKeepsItsTokenAndRegistrar`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L7) · [`vtShShareTokenKeepsThePoolItBacks`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L25) |
| [4740](#spokehandler-4740) | unlinkVault drops the asset match check, so an unlink naming the wrong asset switches the vault off instead of reverting.<br>Caught by: [`rvShUpdateVaultUnlinkRefusesAnUnroutedOrMismatchedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L282) |
| [6701](#spokehandler-6701) | addShareClass's taken slot check is inverted, so a new share class is refused and only an already bound one passes.<br>Caught by: [`rvShAddShareClassAcceptsACleanRegistration`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L329) · [`rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L35) |
| [6702](#spokehandler-6702) | addShareClass now admits only a pool never opened, so an opened pool can never get a share class.<br>Caught by: [`rvShAddShareClassAcceptsACleanRegistration`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L329) · [`rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L35) |
| [6704](#spokehandler-6704) | the vault link check is inverted, so an unlinked vault can never be linked and a linked one is accepted again.<br>Caught by: [`rvShUpdateVaultLinkRefusesAnUnknownOrMismatchedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L257) |
| [6705](#spokehandler-6705) | the unlink gate admits only a vault already out of service, so a vault in service can never be taken out of service.<br>Caught by: [`rcShUnlinkSwitchesOffALinkedVaultIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L22) |
| [6706](#spokehandler-6706) | an unlink sets the routing flag instead of clearing it, so a linked vault can never be taken out of service.<br>Caught by: [`rcShUnlinkSwitchesOffALinkedVaultIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L22) |
| [6707](#spokehandler-6707) | executeTransferShares pays the receiver one unit less than it mints, so the handler keeps a residue of every transfer.<br>Caught by: [`hlShExecuteTransferSharesPaysTheReceiverInFull`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L21) · [`hlShExecuteTransferSharesAddressedPastTheHandlerLeavesNoResidue`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L39) |
| [6708](#spokehandler-6708) | the bridge arrival leg burns where it should mint, so shares are destroyed rather than created on the destination side of a transfer.<br>Caught by: [`hlShExecuteTransferSharesMintsExactlyTheBridgedAmount`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L5) |
| [6709](#spokehandler-6709) | executeTransferShares mints the amount truncated to 64 bits, so a large transfer creates fewer shares than it carries.<br>Caught by: [`hlShExecuteTransferSharesMintsExactlyTheBridgedAmount`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L5) · [`hlShExecuteTransferSharesPaysTheReceiverInFull`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L21) |
| [6710](#spokehandler-6710) | executeTransferShares now refuses a zero amount, so an empty transfer message fails instead of passing through.<br>Caught by: [`rcShTransferSharesForAnEmptyLegIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L41) |
| [6711](#spokehandler-6711) | executeTransferShares mints to the caller, not the handler, so the receiver is paid from the handler's own holdings.<br>Caught by: [`rcShTransferSharesAddressedToTheHandlerIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L65) |
| [6712](#spokehandler-6712) | the manager seat message always seats whatever flag it carries, so the seat that runs a pool's balance sheet can never be withdrawn.<br>Caught by: [`rcShManagerSeatRoundTripIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L87) |
| [6713](#spokehandler-6713) | the bridge seat latches once granted, so the right to burn a pool's shares for a cross chain transfer can never be withdrawn.<br>Caught by: [`rcShBridgerSeatRoundTripIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L105) |
| [6714](#spokehandler-6714) | setPolicy clears the pool's policy instead of installing the one named, so manager calls skip the policy check.<br>Caught by: [`hlShSetPolicyAlwaysAdvancesTheNamespace`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L340) |
| [6715](#spokehandler-6715) | setPolicy ignores a zero policy, so a pool's policy can never be removed and its nonce does not advance.<br>Caught by: [`rcShPolicyRemovalIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L123) |
| [6716](#spokehandler-6716) | a grant is filed one namespace past the rule book in force, so the row a later consumption will look at never grows.<br>Caught by: [`rcShGrantsStackOnOneRowIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L141) |
| [6717](#spokehandler-6717) | the authorization ledger latches a flag instead of counting, so one call can never hold two outstanding grants at once.<br>Caught by: [`rcShGrantsStackOnOneRowIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L141) |
| [6718](#spokehandler-6718) | unauthorize looks the grant up under the next nonce, so a standing grant can never be revoked.<br>Caught by: [`rvShUnauthorizeIsNeverRefusedOnAGrantThatStands`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L398) · [`rvShUnauthorizeRefusesAnUntrustedCallerOrAGrantThatDoesNotStand`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L125) |
| [6719](#spokehandler-6719) | the share price freshness check admits only a stamp no newer than the one on record, so a fresher price is refused.<br>Caught by: [`rcShSharePriceMovingToALaterStampIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L163) · [`rcShSharePriceStampedAtTheLocalClockIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L301) |
| [6720](#spokehandler-6720) | a zero share valuation is dropped instead of stored, so a live mark can never be written down to zero.<br>Caught by: [`rcShSharePriceCanBeMarkedToZeroIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L181) |
| [6722](#spokehandler-6722) | the asset price gate admits only an id the registry never entered, so a registered asset can never be repriced.<br>Caught by: [`rcShAssetPriceMovingToALaterStampIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L200) |
| [6723](#spokehandler-6723) | the request manager appointment is announced but never stored, so a pool never gets its request manager.<br>Caught by: [`rcShRequestManagerAppointmentIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L219) |
| [6724](#spokehandler-6724) | a zero request manager is read as leave unchanged rather than as a removal, so an appointed manager can never be taken off the pool.<br>Caught by: [`rcShRequestManagerWithdrawalIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L234) |
| [6725](#spokehandler-6725) | requestCallback names the next pool id to the manager, so the fulfillment is misrouted and the highest pool id reverts.<br>Caught by: [`rvShRequestCallbackIsNeverRefusedOnAPoolThatHasARequestManager`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L417) |
| [6726](#spokehandler-6726) | the escrow factory admin name writes the registry pointer instead, so the handler can never be repointed at another escrow factory.<br>Caught by: [`rcShFileRepointsTheEscrowFactoryIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L252) |
| [6727](#spokehandler-6727) | the registry admin name writes the escrow factory pointer instead, so the handler can never be repointed at another registry.<br>Caught by: [`rcShFileRepointsTheSpokeRegistryIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L267) |
| [6728](#spokehandler-6728) | a withdrawal of authority in the shared Auth mixin leaves the seat standing, so a ward of the handler can never be removed.<br>Caught by: [`rcShWardRoundTripIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L282) |
| [6729](#spokehandler-6729) | the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.<br>Caught by: [`rvShRequestCallbackRefusesAnUntrustedCallerOrAPoolWithNoRequestManager`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L200) · [`rvShSetPolicyRefusesAnUntrustedCallerOrAPoolNeverOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L91) · [`rvShSetRequestManagerRefusesAnUntrustedCallerOrAPoolNeverOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L183) · [`rvShUpdateBridgerRefusesAnUntrustedCallerOrAPoolNeverOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L74) · [`rvShUpdateManagerRefusesAnUntrustedCallerOrAPoolNeverOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L57) · [`rvShUnauthorizeRefusesAnUntrustedCallerOrAGrantThatDoesNotStand`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L125) |
| [8020](#spokehandler-8020) | addShareClass no longer ties the salt to the pool id, so a forged registration can take another pool's token address.<br>Caught by: [`rvShAddShareClassRefusesASaltOutsideItsPool`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L435) |
| [8021](#spokehandler-8021) | addShareClass inverts the salt check, so every registration whose salt belongs to its own pool is refused.<br>Caught by: [`rvShAddShareClassAcceptsACleanRegistration`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L329) |
| [8022](#spokehandler-8022) | addShareClass hands the registrar a hash of the salt, so the token misses the pool branded address the message named.<br>Caught by: [`hlShAddShareClassDeploysUnderTheMessagesPoolBrandedSalt`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L208) |
| [8023](#spokehandler-8023) | A request callback reaches the manager under the null pool, so the fulfillment is applied to a pool the message never named.<br>Caught by: [`hlShRequestCallbackDeliversThePool`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L222) |
| [8024](#spokehandler-8024) | A request callback reaches the manager under the null share class, so the fulfillment lands on a class the message never named.<br>Caught by: [`hlShRequestCallbackDeliversTheShareClass`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L235) |
| [8025](#spokehandler-8025) | A request callback reaches the manager under the null asset, so the fulfillment is applied to an asset the message never named.<br>Caught by: [`hlShRequestCallbackDeliversTheAsset`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L248) |
| [8026](#spokehandler-8026) | requestCallback hands the manager an empty body instead of the message payload, so no fulfillment reaches the manager.<br>Caught by: [`hlShRequestCallbackDeliversThePayload`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L261) |
| [8027](#spokehandler-8027) | addPool deploys the escrow but never registers the pool, so the escrow belongs to a pool the spoke does not know.<br>Caught by: [`stShEscrowBrandComesWithThePoolRow`](../../specs/core/spoke/SpokeHandler_LinkedRegistryFactory/SpokeHandler_LinkedRegistryFactory_properties.spec#L21) |
| [8400](#spokehandler-8400) | setPolicy keeps the nonce when the same policy is reinstalled, so authorizations granted before the reinstall stay spendable.<br>Caught by: [`hlShSetPolicyAlwaysAdvancesTheNamespace`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L340) |
| [8401](#spokehandler-8401) | addShareClass records the caller instead of the named registrar, so the class is operated by a contract the hub never chose.<br>Caught by: [`hlShAddShareClassBindsTheRegistrarTheMessageNames`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L276) |
| [8402](#spokehandler-8402) | Repointing the registry also overwrites the escrow factory with the same address, so later pools get no working escrow factory.<br>Caught by: [`hlShFileMovesOnlyThePointerItNames`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L289) |
| [8403](#spokehandler-8403) | addPool deploys the pool's escrow but never registers the pool, so the pool stays unknown on this spoke.<br>Caught by: [`rcShAddPoolBrandsItsEscrowAndOpensTheRowIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedRegistryFactory/SpokeHandler_LinkedRegistryFactory_properties.spec#L55) |
| [8407](#spokehandler-8407) | updateRestriction aims the update at the registrar instead of the class token, so hub restriction updates never reach the token.<br>Caught by: [`hlShUpdateRestrictionReachesTheClassTokenWithItsPayload`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L307) |
| [8636](#spokehandler-8636) | updatePricePoolPerShare drops its future time check, so a share price dated ahead of the spoke's clock is stored.<br>Caught by: [`stShPriceStampsNeverRunAheadOfTheClock`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L193) |
| [8637](#spokehandler-8637) | updatePricePoolPerAsset drops its future time check, so an asset price dated ahead of the spoke's clock is stored.<br>Caught by: [`stShPriceStampsNeverRunAheadOfTheClock`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L193) |
| [8638](#spokehandler-8638) | updatePricePoolPerShare lets a share price run one second ahead of the spoke's clock, so a price from the future is stored.<br>Caught by: [`rvShSharePriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L449) |
| [8639](#spokehandler-8639) | updatePricePoolPerAsset lets an asset price run one second ahead of the spoke's clock, so a price from the future is stored.<br>Caught by: [`rvShAssetPriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L461) |
| [8640](#spokehandler-8640) | updatePricePoolPerShare refuses a price dated at the current time, so a share price computed in the block it arrives in never lands.<br>Caught by: [`rcShSharePriceStampedAtTheLocalClockIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L301) |
| [8641](#spokehandler-8641) | updatePricePoolPerAsset refuses a price dated at the current time, so an asset price computed in the block it arrives in never lands.<br>Caught by: [`rcShAssetPriceStampedAtTheLocalClockIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L317) |
| [8928](#spokehandler-8928) | updateVault refuses an unlink message that carries a payload, so the hub can no longer take a linked vault out of service with one.<br>Caught by: [`rvShUpdateVaultUnlinkIsNeverRefusedForALinkedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L473) |
| [8954](#spokehandler-8954) | registerVault no longer refuses an address that already has a vault row, so a deploy onto a registered vault overwrites its row.<br>Caught by: [`rvShUpdateVaultDeployAndLinkRefusesAnUnknownAssetADeadClassOrATakenAddress`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L306) |
| [9006](#spokehandler-9006) | updateShareMetadata sends the name as a restriction update, so the token is not renamed and receives a stray restriction update.<br>Caught by: [`hlShUpdateShareMetadataWritesNoHandlerOrRegistryField`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/SpokeHandler_LinkedSpokeRegistry_entry_gate_properties.spec#L6) |
| [9074](#spokehandler-9074) | Vault registration always records token id zero, so a vault for an ERC6909 asset points at the wrong token.<br>Caught by: [`hlShDeployAndLinkRegistersTheVaultRowTheMessageNames`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L72) |
| [9075](#spokehandler-9075) | Opening a pool no longer records when it was opened, so the pool never counts as active on this spoke.<br>Caught by: [`rcShAddPoolOpensThePoolIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L4) |
| [9240](#spokehandler-9240) | updateShareMetadata loses its ward gate, so any caller can rename and reticker a share token through the handler.<br>Caught by: [`acShUpdateShareMetadataRefusesANonWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/SpokeHandler_LinkedSpokeRegistry_entry_gate_properties.spec#L61) |
| [9260](#spokehandler-9260) | addPool registers the pool before deploying its escrow, so the pool is known on the spoke before its escrow exists.<br>Caught by: [`stShPoolRowOpensOnlyAfterItsEscrowIsBranded`](../../specs/core/spoke/SpokeHandler_LinkedRegistryFactory/SpokeHandler_LinkedRegistryFactory_properties.spec#L38) |

## SpokeHandler #3205

setPolicy installs a replacement without advancing the install counter, so outstanding authorizations survive the swap.

- **Mutant:** [`3205.sol`](3205.sol)
- **Caught by:** [`stShPolicySwapAdvancesTheAuthorizationNamespace`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L136)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 3205`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule stShPolicySwapAdvancesTheAuthorizationNamespace`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -158,7 +158,7 @@
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce); // MUTATION: the namespace stands still
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeHandler #3206

updatePricePoolPerShare drops the existence check, so a price is seeded onto a share class that was never created.

- **Mutant:** [`3206.sol`](3206.sol)
- **Caught by:** [`stShPricesNeedTheRowsTheyPriceTo`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L168)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 3206`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule stShPricesNeedTheRowsTheyPriceTo`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -351,7 +351,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
-        require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
+        // MUTATION: a price no longer needs the class it prices
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
```

## SpokeHandler #3207

addPool enters the pool in the registry without deploying its escrow, so a live pool can exist with no custody contract behind it.

- **Mutant:** [`3207.sol`](3207.sol)
- **Caught by:** [`stShPoolRowNeedsTheEscrowDeployBehindIt`](../../specs/core/spoke/SpokeHandler_LinkedRegistryFactory/SpokeHandler_LinkedRegistryFactory_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 3207`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedRegistryFactory/properties.conf --rule stShPoolRowNeedsTheEscrowDeployBehindIt`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -54,7 +54,7 @@
 
     /// @inheritdoc ISpokeGatewayHandler
     function addPool(PoolId poolId) external auth {
-        escrowFactory.newEscrow(poolId);
+        // MUTATION: the pool row no longer waits on the escrow deploy behind it
         spokeRegistry.addPool(poolId);
     }
 
```

## SpokeHandler #3208

linking a vault also moves the asset id it serves, so a link toggle changes the vault's identity.

- **Mutant:** [`3208.sol`](3208.sol)
- **Caught by:** [`stShVaultLinkNeverMovesItsIdentity`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L95)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 3208`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule stShVaultLinkNeverMovesItsIdentity`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -262,6 +262,7 @@
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
         vaultDetails_.isLinked = true;
+        vaultDetails_.assetId = AssetId.wrap(assetId.raw() + 1); /* MUTATION: linking also moves the vault's asset id */
 
         emit LinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeHandler #3209

filing an authorization also advances the policy nonce, so an authorization moves while the namespace it is filed under shifts.

- **Mutant:** [`3209.sol`](3209.sol)
- **Caught by:** [`stShAuthorizationsMoveOnlyWithinAStandingNamespace`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L151)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 3209`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule stShAuthorizationsMoveOnlyWithinAStandingNamespace`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -169,6 +169,7 @@
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
         authorizations[id]++;
+        _policy[poolId].nonce++; /* MUTATION: filing an authorization also advances the namespace */
         emit AuthorizationGranted(poolId, id, data);
     }
 
```

## SpokeHandler #3210

addShareClass files the token's reverse lookup under a neighbour pool, so the newly bound token no longer looks back to its own class.

- **Mutant:** [`3210.sol`](3210.sol)
- **Caught by:** [`stShShareClassBindsTheRegistrarsTokenAndItsLookupBack`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L117)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 3210`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule stShShareClassBindsTheRegistrarsTokenAndItsLookupBack`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -97,7 +97,7 @@
 
         shareClass_.shareToken = IERC20(shareToken_);
         shareClass_.registrar = registrar_;
-        tokenDetails[shareToken_] = TokenDetails(poolId, scId);
+        tokenDetails[shareToken_] = TokenDetails(PoolId.wrap(poolId.raw() + 1), scId); /* MUTATION: reverse lookup files the token under a neighbour pool */
         emit AddShareClass(poolId, scId, shareToken_, registrar_);
     }
 
```

## SpokeHandler #3219

addShareClass binds the registry itself instead of the registrar's new token, so the class points at the wrong contract.

- **Mutant:** [`3219.sol`](3219.sol)
- **Caught by:** [`stShShareClassBindsTheRegistrarsTokenAndItsLookupBack`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L117)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 3219`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule stShShareClassBindsTheRegistrarsTokenAndItsLookupBack`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -74,7 +74,7 @@
         require(PoolId.wrap(uint64(bytes8(salt))) == poolId, InvalidSalt());
 
         address shareToken_ = registrar.newToken(name, symbol, decimals, salt, payload);
-        spokeRegistry.addShareClass(poolId, scId, shareToken_, registrar);
+        spokeRegistry.addShareClass(poolId, scId, address(spokeRegistry), registrar); /* MUTATION: the registry bound as the token */
     }
 
     /// @inheritdoc ISpokeGatewayHandler
```

## SpokeHandler #4700

file loses its ward gate, so any caller repoints the handler at a registry and an escrow factory of its own.

- **Mutant:** [`4700.sol`](4700.sol)
- **Caught by:** [`acShRegistryPointerMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L20) · [`acShEscrowFactoryPointerMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4700`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShRegistryPointerMovesOnlyForAWard acShEscrowFactoryPointerMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -41,7 +41,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeHandler
-    function file(bytes32 what, address data) external auth {
+    function file(bytes32 what, address data) external { // MUTATION: the ward gate is gone
         if (what == "spokeRegistry") spokeRegistry = ISpokeRegistry(data);
         else if (what == "escrowFactory") escrowFactory = IEscrowFactory(data);
         else revert FileUnrecognizedParam();
```

## SpokeHandler #4701

addPool loses its ward gate, so any caller opens a pool on this spoke and stamps its registry row.

- **Mutant:** [`4701.sol`](4701.sol)
- **Caught by:** [`acShPoolRowMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L53)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4701`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShPoolRowMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -53,7 +53,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeGatewayHandler
-    function addPool(PoolId poolId) external auth {
+    function addPool(PoolId poolId) external { // MUTATION: the ward gate is gone
         escrowFactory.newEscrow(poolId);
         spokeRegistry.addPool(poolId);
     }
```

## SpokeHandler #4702

addShareClass loses its ward gate, so any caller binds a share class to a registrar and token of its own.

- **Mutant:** [`4702.sol`](4702.sol)
- **Caught by:** [`acShShareClassBindingMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L69) · [`acShTokenLookupMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L88)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4702`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShShareClassBindingMovesOnlyForAWard acShTokenLookupMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -68,7 +68,7 @@
         bytes32 salt,
         IRegistrar registrar,
         bytes memory payload
-    ) external auth {
+    ) external { // MUTATION: the ward gate is gone
         require(address(registrar) != address(0), InvalidRegistrar());
         // A registrar can serve multiple pools, so this prevents forged salts from taking another pool's token address.
         require(PoolId.wrap(uint64(bytes8(salt))) == poolId, InvalidSalt());
```

## SpokeHandler #4703

updateManager loses its ward gate, so any caller hands out or withdraws the manager seat that runs a pool's balance sheet.

- **Mutant:** [`4703.sol`](4703.sol)
- **Caught by:** [`acShManagerSeatMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L107)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4703`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShManagerSeatMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -143,7 +143,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeGatewayHandler
-    function updateManager(PoolId poolId, address who, bool canManage) external auth {
+    function updateManager(PoolId poolId, address who, bool canManage) external { // MUTATION: the ward gate is gone
         spokeRegistry.updateManager(poolId, who, canManage);
     }
 
```

## SpokeHandler #4704

updateBridger loses its ward gate, so any caller hands out or withdraws the right to burn a pool's shares for a cross chain transfer.

- **Mutant:** [`4704.sol`](4704.sol)
- **Caught by:** [`acShBridgerSeatMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L123)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4704`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShBridgerSeatMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -148,7 +148,7 @@
     }
 
     /// @inheritdoc ISpokeGatewayHandler
-    function updateBridger(PoolId poolId, address who, bool canBridge) external auth {
+    function updateBridger(PoolId poolId, address who, bool canBridge) external { // MUTATION: the ward gate is gone
         spokeRegistry.updateBridger(poolId, who, canBridge);
     }
 
```

## SpokeHandler #4705

setPolicy loses its ward gate, so any caller swaps a pool's policy and voids its pending authorizations.

- **Mutant:** [`4705.sol`](4705.sol)
- **Caught by:** [`acShPolicyRowMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L139)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4705`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShPolicyRowMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -157,7 +157,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeGatewayHandler
-    function setPolicy(PoolId poolId, IPolicy policy) external auth {
+    function setPolicy(PoolId poolId, IPolicy policy) external { // MUTATION: the ward gate is gone
         spokeRegistry.setPolicy(poolId, policy);
     }
 
```

## SpokeHandler #4706

authorize loses its ward gate, so any caller files a standing permission in the pool's consume only ledger.

- **Mutant:** [`4706.sol`](4706.sol)
- **Caught by:** [`acShAuthorizationLedgerMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L158)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4706`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShAuthorizationLedgerMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -162,7 +162,7 @@
     }
 
     /// @inheritdoc ISpokeGatewayHandler
-    function authorize(PoolId poolId, bytes calldata data) external auth {
+    function authorize(PoolId poolId, bytes calldata data) external { // MUTATION: the ward gate is gone
         spokeRegistry.authorize(poolId, data);
     }
 
```

## SpokeHandler #4707

updatePricePoolPerShare loses its ward gate, so any caller reprices a share class and every local vault settles against the number it invented.

- **Mutant:** [`4707.sol`](4707.sol)
- **Caught by:** [`acShSharePriceMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L174)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4707`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShSharePriceMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -176,7 +176,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeGatewayHandler
-    function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
+    function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external { // MUTATION: the ward gate is gone
         spokeRegistry.updatePricePoolPerShare(poolId, scId, price, computedAt);
     }
 
```

## SpokeHandler #4708

updatePricePoolPerAsset loses its ward gate, so any caller misprices the asset leg every deposit and withdrawal settles through.

- **Mutant:** [`4708.sol`](4708.sol)
- **Caught by:** [`acShAssetPriceMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L193)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4708`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShAssetPriceMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -183,7 +183,7 @@
     /// @inheritdoc ISpokeGatewayHandler
     function updatePricePoolPerAsset(PoolId poolId, ShareClassId scId, AssetId assetId, D18 price, uint64 computedAt)
         external
-        auth
+        // MUTATION: the ward gate is gone
     {
         spokeRegistry.updatePricePoolPerAsset(poolId, scId, assetId, price, computedAt);
     }
```

## SpokeHandler #4709

updateVault loses its ward gate, so any caller registers a vault of its own or switches an existing one into and out of the router.

- **Mutant:** [`4709.sol`](4709.sol)
- **Caught by:** [`acShVaultRowMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L212)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4709`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShVaultRowMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -117,7 +117,7 @@
         address vaultOrFactory,
         VaultUpdateKind kind,
         bytes calldata payload
-    ) external auth {
+    ) external { // MUTATION: the ward gate is gone
         if (kind == VaultUpdateKind.DeployAndLink) {
             (address asset, uint256 tokenId) = spokeRegistry.idToAsset(assetId, true);
             address shareToken = address(spokeRegistry.shareToken(poolId, scId));
```

## SpokeHandler #4710

setRequestManager loses its ward gate, so any caller makes itself the callee of every request the hub sends this pool.

- **Mutant:** [`4710.sol`](4710.sol)
- **Caught by:** [`acShRequestManagerPointerMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L241)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4710`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShRequestManagerPointerMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -193,7 +193,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc ISpokeGatewayHandler
-    function setRequestManager(PoolId poolId, ISpokeRequestManager manager) external auth {
+    function setRequestManager(PoolId poolId, ISpokeRequestManager manager) external { // MUTATION: the ward gate is gone
         spokeRegistry.setRequestManager(poolId, manager);
     }
 
```

## SpokeHandler #4711

executeTransferShares loses its ward gate, so any caller mints shares to any receiver with no transfer from the hub.

- **Mutant:** [`4711.sol`](4711.sol)
- **Caught by:** [`acShShareSupplyMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L257) · [`acShHolderBalanceMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L273)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4711`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShShareSupplyMovesOnlyForAWard acShHolderBalanceMovesOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -97,7 +97,7 @@
     /// @inheritdoc ISpokeGatewayHandler
     /// @dev The shares are minted to this contract and then transferred, so transfer hooks can
     ///      identify the flow as a crosschain transfer execution (this contract is the crosschain source).
-    function executeTransferShares(PoolId poolId, ShareClassId scId, bytes32 receiver, uint128 amount) external auth {
+    function executeTransferShares(PoolId poolId, ShareClassId scId, bytes32 receiver, uint128 amount) external { // MUTATION: the ward gate is gone
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
         registrar.mint(address(token), address(this), amount);
```

## SpokeHandler #4712

requestCallback loses its ward gate, so any caller drives the pool's request pipeline with traffic the hub never sent.

- **Mutant:** [`4712.sol`](4712.sol)
- **Caught by:** [`acShRequestCallbackGoesOutOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L289)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4712`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShRequestCallbackGoesOutOnlyForAWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -198,7 +198,7 @@
     }
 
     /// @inheritdoc ISpokeGatewayHandler
-    function requestCallback(PoolId poolId, ShareClassId scId, AssetId assetId, bytes memory payload) external auth {
+    function requestCallback(PoolId poolId, ShareClassId scId, AssetId assetId, bytes memory payload) external { // MUTATION: the ward gate is gone
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
 
```

## SpokeHandler #4713

The auth modifier's ward test is inverted, so only non-wards pass and any of them can make itself a ward.

- **Mutant:** [`4713.sol`](4713.sol)
- **Caught by:** [`acShWardRosterMovesOnlyForAWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4713`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/access_control.conf --rule acShWardRosterMovesOnlyForAWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -17,7 +17,7 @@
 
     /// @dev Check if the msg.sender has permissions
     modifier auth() {
-        require(wards[msg.sender] == 1, NotAuthorized());
+        require(wards[msg.sender] != 1, NotAuthorized()); // MUTATION: the ward test is inverted
         _;
     }
 
```

## SpokeHandler #4714

file no longer refuses a name it does not know, so a wiring message naming nothing is accepted in silence instead of rejected.

- **Mutant:** [`4714.sol`](4714.sol)
- **Caught by:** [`rvShFileRefusesANonWardOrAnUnknownName`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4714`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShFileRefusesANonWardOrAnUnknownName`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -44,7 +44,7 @@
     function file(bytes32 what, address data) external auth {
         if (what == "spokeRegistry") spokeRegistry = ISpokeRegistry(data);
         else if (what == "escrowFactory") escrowFactory = IEscrowFactory(data);
-        else revert FileUnrecognizedParam();
+        // MUTATION: an unrecognised name is accepted in silence
         emit File(what, data);
     }
 
```

## SpokeHandler #4715

addPool's existence check is inverted, so a new pool is refused and a pool already added is added again.

- **Mutant:** [`4715.sol`](4715.sol)
- **Caught by:** [`rvShAddPoolRefusesAnUntrustedCallerOrAPoolAlreadyOpen`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L19)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4715`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShAddPoolRefusesAnUntrustedCallerOrAPoolAlreadyOpen`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -62,7 +62,7 @@
     function addPool(PoolId poolId) external auth {
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
-        require(pool_.createdAt == 0, PoolAlreadyAdded());
+        require(pool_.createdAt != 0, PoolAlreadyAdded()); // MUTATION: the entry latch is inverted
         pool_.createdAt = uint64(block.timestamp);
 
         emit AddPool(poolId);
```

## SpokeHandler #4716

the share token uniqueness test is read inverted, so a token another class already claims is accepted and a token still free is refused.

- **Mutant:** [`4716.sol`](4716.sol)
- **Caught by:** [`rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L35) · [`rvShAddShareClassAcceptsACleanRegistration`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L329)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4716`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot rvShAddShareClassAcceptsACleanRegistration`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -93,7 +93,7 @@
         // relative to the check so the same-token case does not trip TokenAlreadyRegistered on itself.
         if (address(shareClass_.shareToken) != address(0)) delete tokenDetails[address(shareClass_.shareToken)];
 
-        require(tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered());
+        require(!tokenDetails[shareToken_].poolId.isNull(), TokenAlreadyRegistered()); // MUTATION: the uniqueness test is inverted
 
         shareClass_.shareToken = IERC20(shareToken_);
         shareClass_.registrar = registrar_;
```

## SpokeHandler #4717

isPoolActive requires a creation time in the future, so every pool the hub opened reads inactive and its updates fail.

- **Mutant:** [`4717.sol`](4717.sol)
- **Caught by:** [`rvShUpdateManagerIsNeverRefusedOnAPoolTheHubOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L380)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4717`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUpdateManagerIsNeverRefusedOnAPoolTheHubOpened`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -110,7 +110,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function isPoolActive(PoolId poolId) public view returns (bool) {
-        return pool[poolId].createdAt > 0;
+        return pool[poolId].createdAt > block.timestamp; // MUTATION: the pool reads live only ahead of the clock
     }
 
     /// @inheritdoc ISpokeRegistry
```

## SpokeHandler #4718

hasShareClass checks the registrar slot instead of the token slot, so a class with a registrar but no token reads as present.

- **Mutant:** [`4718.sol`](4718.sol)
- **Caught by:** [`rvShUpdatePricePoolPerShareRefusesAnUntrustedCallerAnAbsentClassOrAnOlderStamp`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L143) · [`rvShUpdatePricePoolPerAssetRefusesAnUntrustedCallerAnUnknownRowOrAnOlderStamp`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L162)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4718`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUpdatePricePoolPerShareRefusesAnUntrustedCallerAnAbsentClassOrAnOlderStamp rvShUpdatePricePoolPerAssetRefusesAnUntrustedCallerAnUnknownRowOrAnOlderStamp`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -115,7 +115,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function hasShareClass(PoolId poolId, ShareClassId scId) public view returns (bool) {
-        return address(shareClass[poolId][scId].shareToken) != address(0);
+        return address(shareClass[poolId][scId].registrar) != address(0); // MUTATION: the wrong slot answers for the class
     }
 
     /// @inheritdoc ISpokeRegistry
```

## SpokeHandler #4719

authorize drops the installed policy check, so a grant is filed on a pool with no policy instead of refused.

- **Mutant:** [`4719.sol`](4719.sol)
- **Caught by:** [`rvShAuthorizeRefusesAnUntrustedCallerOrAPoolWithNoRuleBook`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L108)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4719`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShAuthorizeRefusesAnUntrustedCallerOrAPoolWithNoRuleBook`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -165,7 +165,7 @@
     /// @inheritdoc ISpokeRegistry
     function authorize(PoolId poolId, bytes calldata data) external auth {
         PolicyInfo memory info = _policy[poolId];
-        require(address(info.policy) != address(0), PolicyNotInstalled());
+        // MUTATION: a grant no longer needs an installed rule book
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
         authorizations[id]++;
```

## SpokeHandler #4720

unauthorize demands two outstanding grants where one is enough, so the last grant a pool holds can no longer be revoked.

- **Mutant:** [`4720.sol`](4720.sol)
- **Caught by:** [`rvShUnauthorizeIsNeverRefusedOnAGrantThatStands`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L398)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4720`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUnauthorizeIsNeverRefusedOnAGrantThatStands`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -177,7 +177,7 @@
         PolicyInfo memory info = _policy[poolId];
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
         uint256 count = authorizations[id];
-        require(count != 0, NoOutstandingAuthorization());
+        require(count > 1, NoOutstandingAuthorization()); // MUTATION: the last outstanding grant can no longer be revoked
 
         authorizations[id] = count - 1;
         emit AuthorizationRevoked(poolId, id, data);
```

## SpokeHandler #4721

updateRestriction drops the share token check, so a restriction is pushed at a class this chain does not carry instead of being refused.

- **Mutant:** [`4721.sol`](4721.sol)
- **Caught by:** [`rvShUpdateRestrictionRefusesAnUntrustedCallerOrAClassTheSpokeDoesNotCarry`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L218)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4721`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUpdateRestrictionRefusesAnUntrustedCallerOrAClassTheSpokeDoesNotCarry`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -90,7 +90,7 @@
     /// @inheritdoc ISpokeGatewayHandler
     function updateRestriction(PoolId poolId, ShareClassId scId, bytes memory update) external auth {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
-        require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
+        // MUTATION: a restriction no longer needs the class it restricts
         registrar.updateRestriction(address(token), update);
     }
 
```

## SpokeHandler #4722

executeTransferShares casts the receiver word unchecked, so a word with nonzero trailing bytes is paid out instead of refused.

- **Mutant:** [`4722.sol`](4722.sol)
- **Caught by:** [`rvShExecuteTransferSharesRefusesAnAbsentClassOrAMalformedReceiver`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L236)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4722`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShExecuteTransferSharesRefusesAnAbsentClassOrAMalformedReceiver`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -101,8 +101,8 @@
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
         registrar.mint(address(token), address(this), amount);
-        SafeTransferLib.safeTransfer(address(token), receiver.toAddress(), amount);
-        emit ExecuteTransferShares(poolId, scId, receiver.toAddress(), amount);
+        SafeTransferLib.safeTransfer(address(token), address(bytes20(receiver)), amount); // MUTATION: the malformed receiver word guard is gone
+        emit ExecuteTransferShares(poolId, scId, address(bytes20(receiver)), amount);
     }
 
     //----------------------------------------------------------------------------------------------
```

## SpokeHandler #4723

linkVault drops the registered vault check, so a link message activates an address never registered as a vault.

- **Mutant:** [`4723.sol`](4723.sol)
- **Caught by:** [`rvShUpdateVaultLinkRefusesAnUnknownOrMismatchedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L257)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4723`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUpdateVaultLinkRefusesAnUnknownOrMismatchedVault`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -257,7 +257,7 @@
 
         VaultDetails storage vaultDetails_ = _vaultDetails[vault_];
         require(!vaultDetails_.isLinked, AlreadyLinkedVault());
-        require(vaultDetails_.asset != address(0), UnknownVault());
+        // MUTATION: routing no longer needs a registered vault behind it
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
```

## SpokeHandler #4724

requestCallback inverts its manager check, so a callback to a pool with a request manager is refused.

- **Mutant:** [`4724.sol`](4724.sol)
- **Caught by:** [`rvShRequestCallbackIsNeverRefusedOnAPoolThatHasARequestManager`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L417)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4724`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShRequestCallbackIsNeverRefusedOnAPoolThatHasARequestManager`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -200,7 +200,7 @@
     /// @inheritdoc ISpokeGatewayHandler
     function requestCallback(PoolId poolId, ShareClassId scId, AssetId assetId, bytes memory payload) external auth {
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
-        require(address(manager) != address(0), InvalidRequestManager());
+        require(address(manager) == address(0), InvalidRequestManager()); // MUTATION: the request manager test is inverted
 
         manager.callback(poolId, scId, assetId, payload);
     }
```

## SpokeHandler #4725

rely loses its ward gate in the shared Auth mixin, so authority over the handler is handed on by an account that never held it.

- **Mutant:** [`4725.sol`](4725.sol)
- **Caught by:** [`rvShRelyRefusesANonWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L354)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4725`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShRelyRefusesANonWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -22,7 +22,7 @@
     }
 
     /// @inheritdoc IAuth
-    function rely(address user) public auth {
+    function rely(address user) public { // MUTATION: the ward gate is gone
         wards[user] = 1;
         emit Rely(user);
     }
```

## SpokeHandler #4726

deny loses its ward gate in the shared Auth mixin, so authority over the handler is withdrawn by an account that never held it.

- **Mutant:** [`4726.sol`](4726.sol)
- **Caught by:** [`rvShDenyRefusesANonWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L367)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4726`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShDenyRefusesANonWard`

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

## SpokeHandler #4727

executeTransferShares mints one share more than it delivers, so every bridge arrival inflates supply by one.

- **Mutant:** [`4727.sol`](4727.sol)
- **Caught by:** [`hlShExecuteTransferSharesMintsExactlyTheBridgedAmount`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L5)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4727`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShExecuteTransferSharesMintsExactlyTheBridgedAmount`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -100,7 +100,7 @@
     function executeTransferShares(PoolId poolId, ShareClassId scId, bytes32 receiver, uint128 amount) external auth {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        registrar.mint(address(token), address(this), amount);
+        registrar.mint(address(token), address(this), uint256(amount) + 1); // MUTATION: one share more than the message names
         SafeTransferLib.safeTransfer(address(token), receiver.toAddress(), amount);
         emit ExecuteTransferShares(poolId, scId, receiver.toAddress(), amount);
     }
```

## SpokeHandler #4728

executeTransferShares sends the minted shares to the handler itself, so the named receiver gets nothing.

- **Mutant:** [`4728.sol`](4728.sol)
- **Caught by:** [`hlShExecuteTransferSharesPaysTheReceiverInFull`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L21) · [`hlShExecuteTransferSharesAddressedPastTheHandlerLeavesNoResidue`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L39)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4728`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShExecuteTransferSharesPaysTheReceiverInFull hlShExecuteTransferSharesAddressedPastTheHandlerLeavesNoResidue`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -101,7 +101,7 @@
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
         registrar.mint(address(token), address(this), amount);
-        SafeTransferLib.safeTransfer(address(token), receiver.toAddress(), amount);
+        SafeTransferLib.safeTransfer(address(token), address(this), amount); // MUTATION: the minted shares never leave the handler
         emit ExecuteTransferShares(poolId, scId, receiver.toAddress(), amount);
     }
 
```

## SpokeHandler #4729

updateRestriction also mints one share to the handler, so a restriction message inflates the share supply.

- **Mutant:** [`4729.sol`](4729.sol)
- **Caught by:** [`vtShShareSupplyMovesOnlyOnTheTransferExecutor`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4729`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule vtShShareSupplyMovesOnlyOnTheTransferExecutor`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -92,6 +92,7 @@
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
         registrar.updateRestriction(address(token), update);
+        registrar.mint(address(token), address(this), 1); // MUTATION: the restriction push also mints a share
     }
 
     /// @inheritdoc ISpokeGatewayHandler
```

## SpokeHandler #4730

deploy and link registers the new vault but never links it, so the vault is left unroutable.

- **Mutant:** [`4730.sol`](4730.sol)
- **Caught by:** [`hlShDeployAndLinkLeavesTheNewVaultLinked`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L57)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4730`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShDeployAndLinkLeavesTheNewVaultLinked`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -128,7 +128,7 @@
             spokeRegistry.registerVault(
                 poolId, scId, assetId, asset, tokenId, IVaultFactory(vaultOrFactory), vault_, payload
             );
-            spokeRegistry.linkVault(poolId, scId, assetId, vault_);
+            // MUTATION: the freshly deployed vault is left unrouted
         } else if (kind == VaultUpdateKind.Link) {
             spokeRegistry.linkVault(poolId, scId, assetId, vaultOrFactory);
         } else if (kind == VaultUpdateKind.Unlink) {
```

## SpokeHandler #4732

unlinkVault shifts the vault's asset id instead of clearing its link flag, so the vault stays linked under a wrong asset.

- **Mutant:** [`4732.sol`](4732.sol)
- **Caught by:** [`hlShLinkThenUnlinkRestoresTheRoutingFlag`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L95) · [`hlShLinkThenUnlinkLeavesTheVaultIdentityUntouched`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L111)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4732`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShLinkThenUnlinkRestoresTheRoutingFlag hlShLinkThenUnlinkLeavesTheVaultIdentityUntouched`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -276,7 +276,7 @@
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
-        vaultDetails_.isLinked = false;
+        vaultDetails_.assetId = AssetId.wrap(assetId.raw() + 1); // MUTATION: the unlink moves the asset id and leaves the routing flag on
 
         emit UnlinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeHandler #4733

the bridger role update also sets the manager role, so a bridging grant hands out balance sheet control.

- **Mutant:** [`4733.sol`](4733.sol)
- **Caught by:** [`vtShManagerSeatMovesOnlyOnItsRoleMessage`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L59)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4733`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule vtShManagerSeatMovesOnlyOnItsRoleMessage`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -148,6 +148,7 @@
     function updateBridger(PoolId poolId, address who, bool canBridge) external auth {
         require(isPoolActive(poolId), InvalidPool());
         bridger[poolId][who] = canBridge;
+        manager[poolId][who] = canBridge; // MUTATION: the bridger message also seats the manager
         emit UpdateBridger(poolId, who, canBridge);
     }
 
```

## SpokeHandler #4734

the manager role update also sets the bridger role, so a manager grant hands out share bridging rights.

- **Mutant:** [`4734.sol`](4734.sol)
- **Caught by:** [`vtShBridgerSeatMovesOnlyOnItsRoleMessage`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L76)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4734`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule vtShBridgerSeatMovesOnlyOnItsRoleMessage`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -141,6 +141,7 @@
     function updateManager(PoolId poolId, address who, bool canManage) external auth {
         require(isPoolActive(poolId), InvalidPool());
         manager[poolId][who] = canManage;
+        bridger[poolId][who] = canManage; // MUTATION: the manager message also seats the bridger
         emit UpdateManager(poolId, who, canManage);
     }
 
```

## SpokeHandler #4735

addPool only looks up the escrow address instead of deploying it, so the pool opens with no escrow deployed.

- **Mutant:** [`4735.sol`](4735.sol)
- **Caught by:** [`hlShAddPoolAsksTheEscrowFactoryExactlyOnce`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L137) · [`hlShAddPoolAsksTheEscrowFactoryForThatPool`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L151)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4735`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShAddPoolAsksTheEscrowFactoryExactlyOnce hlShAddPoolAsksTheEscrowFactoryForThatPool`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -54,7 +54,7 @@
 
     /// @inheritdoc ISpokeGatewayHandler
     function addPool(PoolId poolId) external auth {
-        escrowFactory.newEscrow(poolId);
+        escrowFactory.escrow(poolId); // MUTATION: the registration reads the address instead of deploying the escrow
         spokeRegistry.addPool(poolId);
     }
 
```

## SpokeHandler #4736

a fulfillment coming back from the hub is handed to the pool's request manager twice, so one inbound request is processed as two.

- **Mutant:** [`4736.sol`](4736.sol)
- **Caught by:** [`hlShRequestCallbackIsDeliveredExactlyOnce`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L163)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4736`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShRequestCallbackIsDeliveredExactlyOnce`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -203,5 +203,6 @@
         require(address(manager) != address(0), InvalidRequestManager());
 
         manager.callback(poolId, scId, assetId, payload);
+        manager.callback(poolId, scId, assetId, payload); // MUTATION: the same fulfillment goes out a second time
     }
 }
```

## SpokeHandler #4737

requestCallback calls the escrow factory instead of the pool's request manager, so the manager never gets the callback.

- **Mutant:** [`4737.sol`](4737.sol)
- **Caught by:** [`hlShRequestCallbackReachesTheRegisteredManager`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L178)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4737`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShRequestCallbackReachesTheRegisteredManager`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -199,7 +199,7 @@
 
     /// @inheritdoc ISpokeGatewayHandler
     function requestCallback(PoolId poolId, ShareClassId scId, AssetId assetId, bytes memory payload) external auth {
-        ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
+        ISpokeRequestManager manager = ISpokeRequestManager(address(escrowFactory)); // MUTATION: the callee is the wired factory, not the pool's manager
         require(address(manager) != address(0), InvalidRequestManager());
 
         manager.callback(poolId, scId, assetId, payload);
```

## SpokeHandler #4738

a revocation checks the row and then writes it back unchanged, so a grant survives the revocation that was meant to cancel it.

- **Mutant:** [`4738.sol`](4738.sol)
- **Caught by:** [`hlShGrantThenRevokeLeavesTheLedgerUntouched`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L193)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4738`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShGrantThenRevokeLeavesTheLedgerUntouched`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -179,7 +179,7 @@
         uint256 count = authorizations[id];
         require(count != 0, NoOutstandingAuthorization());
 
-        authorizations[id] = count - 1;
+        authorizations[id] = count; // MUTATION: the revocation leaves the row where it stood
         emit AuthorizationRevoked(poolId, id, data);
     }
 
```

## SpokeHandler #4739

addShareClass drops the already registered check, so a live class can be rebound to another token and registrar.

- **Mutant:** [`4739.sol`](4739.sol)
- **Caught by:** [`vtShLiveShareClassKeepsItsTokenAndRegistrar`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L7) · [`vtShShareTokenKeepsThePoolItBacks`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L25)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4739`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule vtShLiveShareClassKeepsItsTokenAndRegistrar vtShShareTokenKeepsThePoolItBacks`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -71,7 +71,7 @@
     /// @inheritdoc ISpokeRegistry
     function addShareClass(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        require(address(shareClass[poolId][scId].shareToken) == address(0), ShareClassAlreadyRegistered());
+        // MUTATION: a class that already runs on a token can be rebound
 
         _linkToken(poolId, scId, shareToken_, registrar_);
     }
```

## SpokeHandler #4740

unlinkVault drops the asset match check, so an unlink naming the wrong asset switches the vault off instead of reverting.

- **Mutant:** [`4740.sol`](4740.sol)
- **Caught by:** [`rvShUpdateVaultUnlinkRefusesAnUnroutedOrMismatchedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L282)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 4740`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUpdateVaultUnlinkRefusesAnUnroutedOrMismatchedVault`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -273,7 +273,7 @@
 
         VaultDetails storage vaultDetails_ = _vaultDetails[vault_];
         require(vaultDetails_.isLinked, AlreadyUnlinkedVault());
-        require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
+        // MUTATION: the unlink no longer needs to name the leg the vault serves
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
         vaultDetails_.isLinked = false;
```

## SpokeHandler #6701

addShareClass's taken slot check is inverted, so a new share class is refused and only an already bound one passes.

- **Mutant:** [`6701.sol`](6701.sol)
- **Caught by:** [`rvShAddShareClassAcceptsACleanRegistration`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L329) · [`rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L35)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6701`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShAddShareClassAcceptsACleanRegistration rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -71,7 +71,7 @@
     /// @inheritdoc ISpokeRegistry
     function addShareClass(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        require(address(shareClass[poolId][scId].shareToken) == address(0), ShareClassAlreadyRegistered());
+        require(address(shareClass[poolId][scId].shareToken) != address(0), ShareClassAlreadyRegistered()); // MUTATION: the registration latch is read inverted
 
         _linkToken(poolId, scId, shareToken_, registrar_);
     }
```

## SpokeHandler #6702

addShareClass now admits only a pool never opened, so an opened pool can never get a share class.

- **Mutant:** [`6702.sol`](6702.sol)
- **Caught by:** [`rvShAddShareClassAcceptsACleanRegistration`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L329) · [`rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L35)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6702`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShAddShareClassAcceptsACleanRegistration rvShAddShareClassRefusesAnUntrustedCallerANullRegistrarOrATakenSlot`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -70,7 +70,7 @@
 
     /// @inheritdoc ISpokeRegistry
     function addShareClass(PoolId poolId, ShareClassId scId, address shareToken_, IRegistrar registrar_) external auth {
-        require(isPoolActive(poolId), InvalidPool());
+        require(!isPoolActive(poolId), InvalidPool()); // MUTATION: the share class gate admits only a pool that was never opened
         require(address(shareClass[poolId][scId].shareToken) == address(0), ShareClassAlreadyRegistered());
 
         _linkToken(poolId, scId, shareToken_, registrar_);
```

## SpokeHandler #6704

the vault link check is inverted, so an unlinked vault can never be linked and a linked one is accepted again.

- **Mutant:** [`6704.sol`](6704.sol)
- **Caught by:** [`rvShUpdateVaultLinkRefusesAnUnknownOrMismatchedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L257)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6704`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUpdateVaultLinkRefusesAnUnknownOrMismatchedVault`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -256,7 +256,7 @@
         require(assetIdKey.asset != address(0), UnknownAsset());
 
         VaultDetails storage vaultDetails_ = _vaultDetails[vault_];
-        require(!vaultDetails_.isLinked, AlreadyLinkedVault());
+        require(vaultDetails_.isLinked, AlreadyLinkedVault()); // MUTATION: the link gate admits only a vault already in service
         require(vaultDetails_.asset != address(0), UnknownVault());
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
```

## SpokeHandler #6705

the unlink gate admits only a vault already out of service, so a vault in service can never be taken out of service.

- **Mutant:** [`6705.sol`](6705.sol)
- **Caught by:** [`rcShUnlinkSwitchesOffALinkedVaultIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6705`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShUnlinkSwitchesOffALinkedVaultIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -272,7 +272,7 @@
         require(assetIdKey.asset != address(0), UnknownAsset());
 
         VaultDetails storage vaultDetails_ = _vaultDetails[vault_];
-        require(vaultDetails_.isLinked, AlreadyUnlinkedVault());
+        require(!vaultDetails_.isLinked, AlreadyUnlinkedVault()); // MUTATION: the unlink gate admits only a vault already out of service
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
```

## SpokeHandler #6706

an unlink sets the routing flag instead of clearing it, so a linked vault can never be taken out of service.

- **Mutant:** [`6706.sol`](6706.sol)
- **Caught by:** [`rcShUnlinkSwitchesOffALinkedVaultIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6706`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShUnlinkSwitchesOffALinkedVaultIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -276,7 +276,7 @@
         require(vaultDetails_.assetId.raw() == assetId.raw(), UnknownAsset());
         require(vaultDetails_.poolId == poolId && vaultDetails_.scId == scId, InvalidVault());
 
-        vaultDetails_.isLinked = false;
+        vaultDetails_.isLinked = true; // MUTATION: the unlink leaves the routing flag standing
 
         emit UnlinkVault(poolId, scId, assetIdKey.asset, assetIdKey.tokenId, vault_);
     }
```

## SpokeHandler #6707

executeTransferShares pays the receiver one unit less than it mints, so the handler keeps a residue of every transfer.

- **Mutant:** [`6707.sol`](6707.sol)
- **Caught by:** [`hlShExecuteTransferSharesPaysTheReceiverInFull`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L21) · [`hlShExecuteTransferSharesAddressedPastTheHandlerLeavesNoResidue`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L39)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6707`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShExecuteTransferSharesPaysTheReceiverInFull hlShExecuteTransferSharesAddressedPastTheHandlerLeavesNoResidue`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -101,7 +101,7 @@
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
         registrar.mint(address(token), address(this), amount);
-        SafeTransferLib.safeTransfer(address(token), receiver.toAddress(), amount);
+        SafeTransferLib.safeTransfer(address(token), receiver.toAddress(), amount - 1); // MUTATION: the leg pays one share less than it minted
         emit ExecuteTransferShares(poolId, scId, receiver.toAddress(), amount);
     }
 
```

## SpokeHandler #6708

the bridge arrival leg burns where it should mint, so shares are destroyed rather than created on the destination side of a transfer.

- **Mutant:** [`6708.sol`](6708.sol)
- **Caught by:** [`hlShExecuteTransferSharesMintsExactlyTheBridgedAmount`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L5)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6708`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShExecuteTransferSharesMintsExactlyTheBridgedAmount`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -100,7 +100,7 @@
     function executeTransferShares(PoolId poolId, ShareClassId scId, bytes32 receiver, uint128 amount) external auth {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        registrar.mint(address(token), address(this), amount);
+        registrar.burn(address(token), address(this), amount); // MUTATION: the arrival leg burns where it should mint
         SafeTransferLib.safeTransfer(address(token), receiver.toAddress(), amount);
         emit ExecuteTransferShares(poolId, scId, receiver.toAddress(), amount);
     }
```

## SpokeHandler #6709

executeTransferShares mints the amount truncated to 64 bits, so a large transfer creates fewer shares than it carries.

- **Mutant:** [`6709.sol`](6709.sol)
- **Caught by:** [`hlShExecuteTransferSharesMintsExactlyTheBridgedAmount`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L5) · [`hlShExecuteTransferSharesPaysTheReceiverInFull`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6709`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShExecuteTransferSharesMintsExactlyTheBridgedAmount hlShExecuteTransferSharesPaysTheReceiverInFull`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -100,7 +100,7 @@
     function executeTransferShares(PoolId poolId, ShareClassId scId, bytes32 receiver, uint128 amount) external auth {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        registrar.mint(address(token), address(this), amount);
+        registrar.mint(address(token), address(this), uint64(amount)); // MUTATION: the minted amount is truncated to 64 bits
         SafeTransferLib.safeTransfer(address(token), receiver.toAddress(), amount);
         emit ExecuteTransferShares(poolId, scId, receiver.toAddress(), amount);
     }
```

## SpokeHandler #6710

executeTransferShares now refuses a zero amount, so an empty transfer message fails instead of passing through.

- **Mutant:** [`6710.sol`](6710.sol)
- **Caught by:** [`rcShTransferSharesForAnEmptyLegIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6710`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShTransferSharesForAnEmptyLegIsReachable`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -99,7 +99,7 @@
     ///      identify the flow as a crosschain transfer execution (this contract is the crosschain source).
     function executeTransferShares(PoolId poolId, ShareClassId scId, bytes32 receiver, uint128 amount) external auth {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
-        require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
+        require(address(token) != address(0) && amount != 0, ISpokeRegistry.ShareTokenDoesNotExist()); // MUTATION: an empty leg is screened out at the entry
         registrar.mint(address(token), address(this), amount);
         SafeTransferLib.safeTransfer(address(token), receiver.toAddress(), amount);
         emit ExecuteTransferShares(poolId, scId, receiver.toAddress(), amount);
```

## SpokeHandler #6711

executeTransferShares mints to the caller, not the handler, so the receiver is paid from the handler's own holdings.

- **Mutant:** [`6711.sol`](6711.sol)
- **Caught by:** [`rcShTransferSharesAddressedToTheHandlerIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L65)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6711`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShTransferSharesAddressedToTheHandlerIsReachable`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -100,7 +100,7 @@
     function executeTransferShares(PoolId poolId, ShareClassId scId, bytes32 receiver, uint128 amount) external auth {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        registrar.mint(address(token), address(this), amount);
+        registrar.mint(address(token), msg.sender, amount); // MUTATION: the new shares are minted to the caller instead of to the handler
         SafeTransferLib.safeTransfer(address(token), receiver.toAddress(), amount);
         emit ExecuteTransferShares(poolId, scId, receiver.toAddress(), amount);
     }
```

## SpokeHandler #6712

the manager seat message always seats whatever flag it carries, so the seat that runs a pool's balance sheet can never be withdrawn.

- **Mutant:** [`6712.sol`](6712.sol)
- **Caught by:** [`rcShManagerSeatRoundTripIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L87)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6712`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShManagerSeatRoundTripIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -140,7 +140,7 @@
     /// @inheritdoc ISpokeRegistry
     function updateManager(PoolId poolId, address who, bool canManage) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        manager[poolId][who] = canManage;
+        manager[poolId][who] = true; // MUTATION: the seat message always seats, whatever flag it carries
         emit UpdateManager(poolId, who, canManage);
     }
 
```

## SpokeHandler #6713

the bridge seat latches once granted, so the right to burn a pool's shares for a cross chain transfer can never be withdrawn.

- **Mutant:** [`6713.sol`](6713.sol)
- **Caught by:** [`rcShBridgerSeatRoundTripIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L105)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6713`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShBridgerSeatRoundTripIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -147,7 +147,7 @@
     /// @inheritdoc ISpokeRegistry
     function updateBridger(PoolId poolId, address who, bool canBridge) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        bridger[poolId][who] = canBridge;
+        bridger[poolId][who] = canBridge || bridger[poolId][who]; // MUTATION: the bridge seat latches once granted
         emit UpdateBridger(poolId, who, canBridge);
     }
 
```

## SpokeHandler #6714

setPolicy clears the pool's policy instead of installing the one named, so manager calls skip the policy check.

- **Mutant:** [`6714.sol`](6714.sol)
- **Caught by:** [`hlShSetPolicyAlwaysAdvancesTheNamespace`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L340)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6714`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShSetPolicyAlwaysAdvancesTheNamespace`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -158,7 +158,7 @@
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        _policy[poolId] = PolicyInfo(IPolicy(address(0)), _policy[poolId].nonce + 1); // MUTATION: the swap clears the rule book instead of installing the one named
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeHandler #6715

setPolicy ignores a zero policy, so a pool's policy can never be removed and its nonce does not advance.

- **Mutant:** [`6715.sol`](6715.sol)
- **Caught by:** [`rcShPolicyRemovalIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L123)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6715`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShPolicyRemovalIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -158,7 +158,7 @@
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        if (address(policy_) != address(0)) _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1); // MUTATION: a zero rule book is read as leave unchanged
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeHandler #6716

a grant is filed one namespace past the rule book in force, so the row a later consumption will look at never grows.

- **Mutant:** [`6716.sol`](6716.sol)
- **Caught by:** [`rcShGrantsStackOnOneRowIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L141)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6716`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShGrantsStackOnOneRowIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -167,7 +167,7 @@
         PolicyInfo memory info = _policy[poolId];
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
-        bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId, address(info.policy), info.nonce + 1, data); // MUTATION: the grant is filed one namespace past the one in force
         authorizations[id]++;
         emit AuthorizationGranted(poolId, id, data);
     }
```

## SpokeHandler #6717

the authorization ledger latches a flag instead of counting, so one call can never hold two outstanding grants at once.

- **Mutant:** [`6717.sol`](6717.sol)
- **Caught by:** [`rcShGrantsStackOnOneRowIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L141)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6717`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShGrantsStackOnOneRowIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -168,7 +168,7 @@
         require(address(info.policy) != address(0), PolicyNotInstalled());
 
         bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
-        authorizations[id]++;
+        authorizations[id] = 1; // MUTATION: the ledger latches a flag instead of counting
         emit AuthorizationGranted(poolId, id, data);
     }
 
```

## SpokeHandler #6718

unauthorize looks the grant up under the next nonce, so a standing grant can never be revoked.

- **Mutant:** [`6718.sol`](6718.sol)
- **Caught by:** [`rvShUnauthorizeIsNeverRefusedOnAGrantThatStands`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L398) · [`rvShUnauthorizeRefusesAnUntrustedCallerOrAGrantThatDoesNotStand`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L125)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6718`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUnauthorizeIsNeverRefusedOnAGrantThatStands rvShUnauthorizeRefusesAnUntrustedCallerOrAGrantThatDoesNotStand`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -175,7 +175,7 @@
     /// @inheritdoc ISpokeRegistry
     function unauthorize(PoolId poolId, bytes calldata data) external auth {
         PolicyInfo memory info = _policy[poolId];
-        bytes32 id = _authId(poolId, address(info.policy), info.nonce, data);
+        bytes32 id = _authId(poolId, address(info.policy), info.nonce + 1, data); // MUTATION: the revocation is filed one namespace past the grant
         uint256 count = authorizations[id];
         require(count != 0, NoOutstandingAuthorization());
 
```

## SpokeHandler #6719

the share price freshness check admits only a stamp no newer than the one on record, so a fresher price is refused.

- **Mutant:** [`6719.sol`](6719.sol)
- **Caught by:** [`rcShSharePriceMovingToALaterStampIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L163) · [`rcShSharePriceStampedAtTheLocalClockIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L301)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6719`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShSharePriceMovingToALaterStampIsReachable rcShSharePriceStampedAtTheLocalClockIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -354,7 +354,7 @@
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
-        require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
+        require(computedAt <= poolPerShare.computedAt, CannotSetOlderPrice()); // MUTATION: the freshness gate admits only a mark no newer than the one on record
 
         poolPerShare.price = price;
         poolPerShare.computedAt = computedAt;
```

## SpokeHandler #6720

a zero share valuation is dropped instead of stored, so a live mark can never be written down to zero.

- **Mutant:** [`6720.sol`](6720.sol)
- **Caught by:** [`rcShSharePriceCanBeMarkedToZeroIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L181)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6720`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShSharePriceCanBeMarkedToZeroIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -356,7 +356,7 @@
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
-        poolPerShare.price = price;
+        if (D18.unwrap(price) != 0) poolPerShare.price = price; // MUTATION: a zero mark is dropped instead of stored
         poolPerShare.computedAt = computedAt;
         emit UpdateSharePrice(poolId, scId, price, computedAt);
     }
```

## SpokeHandler #6722

the asset price gate admits only an id the registry never entered, so a registered asset can never be repriced.

- **Mutant:** [`6722.sol`](6722.sol)
- **Caught by:** [`rcShAssetPriceMovingToALaterStampIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L200)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6722`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShAssetPriceMovingToALaterStampIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -367,7 +367,7 @@
         auth
     {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
-        require(isRegistered(assetId), UnknownAsset());
+        require(!isRegistered(assetId), UnknownAsset()); // MUTATION: the asset gate admits only an id the registry never entered
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
         require(computedAt <= block.timestamp, CannotSetFuturePrice());
```

## SpokeHandler #6723

the request manager appointment is announced but never stored, so a pool never gets its request manager.

- **Mutant:** [`6723.sol`](6723.sol)
- **Caught by:** [`rcShRequestManagerAppointmentIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L219)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6723`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShRequestManagerAppointmentIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -104,7 +104,7 @@
     /// @inheritdoc ISpokeRegistry
     function setRequestManager(PoolId poolId, ISpokeRequestManager manager_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        requestManager[poolId] = manager_;
+        // MUTATION: the appointment is announced but never filed
         emit SetRequestManager(poolId, manager_);
     }
 
```

## SpokeHandler #6724

a zero request manager is read as leave unchanged rather than as a removal, so an appointed manager can never be taken off the pool.

- **Mutant:** [`6724.sol`](6724.sol)
- **Caught by:** [`rcShRequestManagerWithdrawalIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L234)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6724`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShRequestManagerWithdrawalIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -104,7 +104,7 @@
     /// @inheritdoc ISpokeRegistry
     function setRequestManager(PoolId poolId, ISpokeRequestManager manager_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        requestManager[poolId] = manager_;
+        if (address(manager_) != address(0)) requestManager[poolId] = manager_; // MUTATION: a zero appointment is read as leave unchanged
         emit SetRequestManager(poolId, manager_);
     }
 
```

## SpokeHandler #6725

requestCallback names the next pool id to the manager, so the fulfillment is misrouted and the highest pool id reverts.

- **Mutant:** [`6725.sol`](6725.sol)
- **Caught by:** [`rvShRequestCallbackIsNeverRefusedOnAPoolThatHasARequestManager`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L417)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6725`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShRequestCallbackIsNeverRefusedOnAPoolThatHasARequestManager`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -202,6 +202,6 @@
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
 
-        manager.callback(poolId, scId, assetId, payload);
+        manager.callback(PoolId.wrap(poolId.raw() + 1), scId, assetId, payload); // MUTATION: the fulfillment is announced under the neighbouring pool
     }
 }
```

## SpokeHandler #6726

the escrow factory admin name writes the registry pointer instead, so the handler can never be repointed at another escrow factory.

- **Mutant:** [`6726.sol`](6726.sol)
- **Caught by:** [`rcShFileRepointsTheEscrowFactoryIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L252)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6726`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShFileRepointsTheEscrowFactoryIsReachable`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -43,7 +43,7 @@
     /// @inheritdoc ISpokeHandler
     function file(bytes32 what, address data) external auth {
         if (what == "spokeRegistry") spokeRegistry = ISpokeRegistry(data);
-        else if (what == "escrowFactory") escrowFactory = IEscrowFactory(data);
+        else if (what == "escrowFactory") spokeRegistry = ISpokeRegistry(data); // MUTATION: the escrow factory name writes the registry pointer
         else revert FileUnrecognizedParam();
         emit File(what, data);
     }
```

## SpokeHandler #6727

the registry admin name writes the escrow factory pointer instead, so the handler can never be repointed at another registry.

- **Mutant:** [`6727.sol`](6727.sol)
- **Caught by:** [`rcShFileRepointsTheSpokeRegistryIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L267)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6727`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShFileRepointsTheSpokeRegistryIsReachable`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -42,7 +42,7 @@
 
     /// @inheritdoc ISpokeHandler
     function file(bytes32 what, address data) external auth {
-        if (what == "spokeRegistry") spokeRegistry = ISpokeRegistry(data);
+        if (what == "spokeRegistry") escrowFactory = IEscrowFactory(data); // MUTATION: the registry name writes the escrow factory pointer
         else if (what == "escrowFactory") escrowFactory = IEscrowFactory(data);
         else revert FileUnrecognizedParam();
         emit File(what, data);
```

## SpokeHandler #6728

a withdrawal of authority in the shared Auth mixin leaves the seat standing, so a ward of the handler can never be removed.

- **Mutant:** [`6728.sol`](6728.sol)
- **Caught by:** [`rcShWardRoundTripIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L282)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6728`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShWardRoundTripIsReachable`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        wards[user] = 1; // MUTATION: the withdrawal of authority leaves the seat standing
         emit Deny(user);
     }
 }
```

## SpokeHandler #6729

the shared ward gate no longer looks at the caller, so every guarded entry of this contract answers an outsider.

- **Mutant:** [`6729.sol`](6729.sol)
- **Caught by:** [`rvShRequestCallbackRefusesAnUntrustedCallerOrAPoolWithNoRequestManager`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L200) · [`rvShSetPolicyRefusesAnUntrustedCallerOrAPoolNeverOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L91) · [`rvShSetRequestManagerRefusesAnUntrustedCallerOrAPoolNeverOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L183) · [`rvShUpdateBridgerRefusesAnUntrustedCallerOrAPoolNeverOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L74) · [`rvShUpdateManagerRefusesAnUntrustedCallerOrAPoolNeverOpened`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L57) · [`rvShUnauthorizeRefusesAnUntrustedCallerOrAGrantThatDoesNotStand`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L125)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 6729`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShRequestCallbackRefusesAnUntrustedCallerOrAPoolWithNoRequestManager rvShSetPolicyRefusesAnUntrustedCallerOrAPoolNeverOpened rvShSetRequestManagerRefusesAnUntrustedCallerOrAPoolNeverOpened rvShUpdateBridgerRefusesAnUntrustedCallerOrAPoolNeverOpened rvShUpdateManagerRefusesAnUntrustedCallerOrAPoolNeverOpened rvShUnauthorizeRefusesAnUntrustedCallerOrAGrantThatDoesNotStand`

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

## SpokeHandler #8020

addShareClass no longer ties the salt to the pool id, so a forged registration can take another pool's token address.

- **Mutant:** [`8020.sol`](8020.sol)
- **Caught by:** [`rvShAddShareClassRefusesASaltOutsideItsPool`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L435)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8020`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShAddShareClassRefusesASaltOutsideItsPool`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -71,7 +71,7 @@
     ) external auth {
         require(address(registrar) != address(0), InvalidRegistrar());
         // A registrar can serve multiple pools, so this prevents forged salts from taking another pool's token address.
-        require(PoolId.wrap(uint64(bytes8(salt))) == poolId, InvalidSalt());
+        // MUTATION: the salt is no longer tied to the pool
 
         address shareToken_ = registrar.newToken(name, symbol, decimals, salt, payload);
         spokeRegistry.addShareClass(poolId, scId, shareToken_, registrar);
```

## SpokeHandler #8021

addShareClass inverts the salt check, so every registration whose salt belongs to its own pool is refused.

- **Mutant:** [`8021.sol`](8021.sol)
- **Caught by:** [`rvShAddShareClassAcceptsACleanRegistration`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L329)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8021`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShAddShareClassAcceptsACleanRegistration`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -71,7 +71,7 @@
     ) external auth {
         require(address(registrar) != address(0), InvalidRegistrar());
         // A registrar can serve multiple pools, so this prevents forged salts from taking another pool's token address.
-        require(PoolId.wrap(uint64(bytes8(salt))) == poolId, InvalidSalt());
+        require(!(PoolId.wrap(uint64(bytes8(salt))) == poolId), InvalidSalt()); // MUTATION: the check is inverted
 
         address shareToken_ = registrar.newToken(name, symbol, decimals, salt, payload);
         spokeRegistry.addShareClass(poolId, scId, shareToken_, registrar);
```

## SpokeHandler #8022

addShareClass hands the registrar a hash of the salt, so the token misses the pool branded address the message named.

- **Mutant:** [`8022.sol`](8022.sol)
- **Caught by:** [`hlShAddShareClassDeploysUnderTheMessagesPoolBrandedSalt`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L208)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8022`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShAddShareClassDeploysUnderTheMessagesPoolBrandedSalt`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -73,7 +73,7 @@
         // A registrar can serve multiple pools, so this prevents forged salts from taking another pool's token address.
         require(PoolId.wrap(uint64(bytes8(salt))) == poolId, InvalidSalt());
 
-        address shareToken_ = registrar.newToken(name, symbol, decimals, salt, payload);
+        address shareToken_ = registrar.newToken(name, symbol, decimals, keccak256(abi.encode(salt)), payload); // MUTATION: the deployment salt is hashed
         spokeRegistry.addShareClass(poolId, scId, shareToken_, registrar);
     }
 
```

## SpokeHandler #8023

A request callback reaches the manager under the null pool, so the fulfillment is applied to a pool the message never named.

- **Mutant:** [`8023.sol`](8023.sol)
- **Caught by:** [`hlShRequestCallbackDeliversThePool`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L222)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8023`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShRequestCallbackDeliversThePool`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -202,6 +202,6 @@
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
 
-        manager.callback(poolId, scId, assetId, payload);
+        manager.callback(PoolId.wrap(0), scId, assetId, payload); // MUTATION: the callback names the null pool
     }
 }
```

## SpokeHandler #8024

A request callback reaches the manager under the null share class, so the fulfillment lands on a class the message never named.

- **Mutant:** [`8024.sol`](8024.sol)
- **Caught by:** [`hlShRequestCallbackDeliversTheShareClass`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L235)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8024`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShRequestCallbackDeliversTheShareClass`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -202,6 +202,6 @@
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
 
-        manager.callback(poolId, scId, assetId, payload);
+        manager.callback(poolId, ShareClassId.wrap(bytes16(0)), assetId, payload); // MUTATION: the callback names the null share class
     }
 }
```

## SpokeHandler #8025

A request callback reaches the manager under the null asset, so the fulfillment is applied to an asset the message never named.

- **Mutant:** [`8025.sol`](8025.sol)
- **Caught by:** [`hlShRequestCallbackDeliversTheAsset`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L248)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8025`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShRequestCallbackDeliversTheAsset`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -202,6 +202,6 @@
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
 
-        manager.callback(poolId, scId, assetId, payload);
+        manager.callback(poolId, scId, AssetId.wrap(0), payload); // MUTATION: the callback names the null asset
     }
 }
```

## SpokeHandler #8026

requestCallback hands the manager an empty body instead of the message payload, so no fulfillment reaches the manager.

- **Mutant:** [`8026.sol`](8026.sol)
- **Caught by:** [`hlShRequestCallbackDeliversThePayload`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L261)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8026`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShRequestCallbackDeliversThePayload`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -202,6 +202,6 @@
         ISpokeRequestManager manager = spokeRegistry.requestManager(poolId);
         require(address(manager) != address(0), InvalidRequestManager());
 
-        manager.callback(poolId, scId, assetId, payload);
+        manager.callback(poolId, scId, assetId, new bytes(0)); // MUTATION: the callback carries an empty body
     }
 }
```

## SpokeHandler #8027

addPool deploys the escrow but never registers the pool, so the escrow belongs to a pool the spoke does not know.

- **Mutant:** [`8027.sol`](8027.sol)
- **Caught by:** [`stShEscrowBrandComesWithThePoolRow`](../../specs/core/spoke/SpokeHandler_LinkedRegistryFactory/SpokeHandler_LinkedRegistryFactory_properties.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8027`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedRegistryFactory/properties.conf --rule stShEscrowBrandComesWithThePoolRow`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -55,7 +55,7 @@
     /// @inheritdoc ISpokeGatewayHandler
     function addPool(PoolId poolId) external auth {
         escrowFactory.newEscrow(poolId);
-        spokeRegistry.addPool(poolId);
+        // MUTATION: the pool row is never opened on this spoke
     }
 
     /// @inheritdoc ISpokeGatewayHandler
```

## SpokeHandler #8400

setPolicy keeps the nonce when the same policy is reinstalled, so authorizations granted before the reinstall stay spendable.

- **Mutant:** [`8400.sol`](8400.sol)
- **Caught by:** [`hlShSetPolicyAlwaysAdvancesTheNamespace`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L340)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8400`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShSetPolicyAlwaysAdvancesTheNamespace`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -158,7 +158,7 @@
     /// @inheritdoc ISpokeRegistry
     function setPolicy(PoolId poolId, IPolicy policy_) external auth {
         require(isPoolActive(poolId), InvalidPool());
-        _policy[poolId] = PolicyInfo(policy_, _policy[poolId].nonce + 1);
+        _policy[poolId] = PolicyInfo(policy_, address(policy_) == address(_policy[poolId].policy) ? _policy[poolId].nonce : _policy[poolId].nonce + 1); // MUTATION: a same address reinstall keeps the old tenure
         emit SetPolicy(poolId, policy_);
     }
 
```

## SpokeHandler #8401

addShareClass records the caller instead of the named registrar, so the class is operated by a contract the hub never chose.

- **Mutant:** [`8401.sol`](8401.sol)
- **Caught by:** [`hlShAddShareClassBindsTheRegistrarTheMessageNames`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L276)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8401`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShAddShareClassBindsTheRegistrarTheMessageNames`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -74,7 +74,7 @@
         require(PoolId.wrap(uint64(bytes8(salt))) == poolId, InvalidSalt());
 
         address shareToken_ = registrar.newToken(name, symbol, decimals, salt, payload);
-        spokeRegistry.addShareClass(poolId, scId, shareToken_, registrar);
+        spokeRegistry.addShareClass(poolId, scId, shareToken_, IRegistrar(msg.sender)); // MUTATION: the class is bound to the caller, not the named registrar
     }
 
     /// @inheritdoc ISpokeGatewayHandler
```

## SpokeHandler #8402

Repointing the registry also overwrites the escrow factory with the same address, so later pools get no working escrow factory.

- **Mutant:** [`8402.sol`](8402.sol)
- **Caught by:** [`hlShFileMovesOnlyThePointerItNames`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L289)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8402`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShFileMovesOnlyThePointerItNames`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -42,7 +42,7 @@
 
     /// @inheritdoc ISpokeHandler
     function file(bytes32 what, address data) external auth {
-        if (what == "spokeRegistry") spokeRegistry = ISpokeRegistry(data);
+        if (what == "spokeRegistry") { spokeRegistry = ISpokeRegistry(data); escrowFactory = IEscrowFactory(data); } // MUTATION: the escrow factory is overwritten too
         else if (what == "escrowFactory") escrowFactory = IEscrowFactory(data);
         else revert FileUnrecognizedParam();
         emit File(what, data);
```

## SpokeHandler #8403

addPool deploys the pool's escrow but never registers the pool, so the pool stays unknown on this spoke.

- **Mutant:** [`8403.sol`](8403.sol)
- **Caught by:** [`rcShAddPoolBrandsItsEscrowAndOpensTheRowIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedRegistryFactory/SpokeHandler_LinkedRegistryFactory_properties.spec#L55)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8403`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedRegistryFactory/properties.conf --rule rcShAddPoolBrandsItsEscrowAndOpensTheRowIsReachable`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -55,7 +55,7 @@
     /// @inheritdoc ISpokeGatewayHandler
     function addPool(PoolId poolId) external auth {
         escrowFactory.newEscrow(poolId);
-        spokeRegistry.addPool(poolId);
+        // MUTATION: the pool row is never opened on this spoke
     }
 
     /// @inheritdoc ISpokeGatewayHandler
```

## SpokeHandler #8407

updateRestriction aims the update at the registrar instead of the class token, so hub restriction updates never reach the token.

- **Mutant:** [`8407.sol`](8407.sol)
- **Caught by:** [`hlShUpdateRestrictionReachesTheClassTokenWithItsPayload`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L307)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8407`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShUpdateRestrictionReachesTheClassTokenWithItsPayload`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -91,7 +91,7 @@
     function updateRestriction(PoolId poolId, ShareClassId scId, bytes memory update) external auth {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        registrar.updateRestriction(address(token), update);
+        registrar.updateRestriction(address(registrar), update); // MUTATION: the restriction is aimed at the registrar, not the class token
     }
 
     /// @inheritdoc ISpokeGatewayHandler
```

## SpokeHandler #8636

updatePricePoolPerShare drops its future time check, so a share price dated ahead of the spoke's clock is stored.

- **Mutant:** [`8636.sol`](8636.sol)
- **Caught by:** [`stShPriceStampsNeverRunAheadOfTheClock`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L193)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8636`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule stShPriceStampsNeverRunAheadOfTheClock`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -353,7 +353,7 @@
     function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard is removed from the share price update, so the handler lands a share price stamped ahead of the clock
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
```

## SpokeHandler #8637

updatePricePoolPerAsset drops its future time check, so an asset price dated ahead of the spoke's clock is stored.

- **Mutant:** [`8637.sol`](8637.sol)
- **Caught by:** [`stShPriceStampsNeverRunAheadOfTheClock`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_transitions.spec#L193)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8637`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/transitions.conf --rule stShPriceStampsNeverRunAheadOfTheClock`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -370,7 +370,7 @@
         require(isRegistered(assetId), UnknownAsset());
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the future stamp guard is removed from the asset price update, so the handler lands an asset price stamped ahead of the clock
         require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
 
         poolPerAsset.price = price;
```

## SpokeHandler #8638

updatePricePoolPerShare lets a share price run one second ahead of the spoke's clock, so a price from the future is stored.

- **Mutant:** [`8638.sol`](8638.sol)
- **Caught by:** [`rvShSharePriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L449)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8638`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShSharePriceStampedAheadOfTheClockIsRefused`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -353,7 +353,8 @@
     function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the share price clock bound admits one second of future
+        require(computedAt <= block.timestamp + 1, CannotSetFuturePrice());
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
```

## SpokeHandler #8639

updatePricePoolPerAsset lets an asset price run one second ahead of the spoke's clock, so a price from the future is stored.

- **Mutant:** [`8639.sol`](8639.sol)
- **Caught by:** [`rvShAssetPriceStampedAheadOfTheClockIsRefused`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L461)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8639`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShAssetPriceStampedAheadOfTheClockIsRefused`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -370,7 +370,8 @@
         require(isRegistered(assetId), UnknownAsset());
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the asset price clock bound admits one second of future
+        require(computedAt <= block.timestamp + 1, CannotSetFuturePrice());
         require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
 
         poolPerAsset.price = price;
```

## SpokeHandler #8640

updatePricePoolPerShare refuses a price dated at the current time, so a share price computed in the block it arrives in never lands.

- **Mutant:** [`8640.sol`](8640.sol)
- **Caught by:** [`rcShSharePriceStampedAtTheLocalClockIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L301)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8640`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShSharePriceStampedAtTheLocalClockIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -353,7 +353,8 @@
     function updatePricePoolPerShare(PoolId poolId, ShareClassId scId, D18 price, uint64 computedAt) external auth {
         require(hasShareClass(poolId, scId), ShareTokenDoesNotExist());
         Price storage poolPerShare = shareClass[poolId][scId].pricePoolPerShare;
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the share price clock bound turns strict and refuses a price stamped in the current block
+        require(computedAt < block.timestamp, CannotSetFuturePrice());
         require(computedAt >= poolPerShare.computedAt, CannotSetOlderPrice());
 
         poolPerShare.price = price;
```

## SpokeHandler #8641

updatePricePoolPerAsset refuses a price dated at the current time, so an asset price computed in the block it arrives in never lands.

- **Mutant:** [`8641.sol`](8641.sol)
- **Caught by:** [`rcShAssetPriceStampedAtTheLocalClockIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L317)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8641`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShAssetPriceStampedAtTheLocalClockIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -370,7 +370,8 @@
         require(isRegistered(assetId), UnknownAsset());
         AssetIdKey memory assetIdKey = _idToAsset[assetId];
         Price storage poolPerAsset = _pricePoolPerAsset[poolId][scId][assetId];
-        require(computedAt <= block.timestamp, CannotSetFuturePrice());
+        // MUTATION: the asset price clock bound turns strict and refuses a price stamped in the current block
+        require(computedAt < block.timestamp, CannotSetFuturePrice());
         require(computedAt >= poolPerAsset.computedAt, CannotSetOlderPrice());
 
         poolPerAsset.price = price;
```

## SpokeHandler #8928

updateVault refuses an unlink message that carries a payload, so the hub can no longer take a linked vault out of service with one.

- **Mutant:** [`8928.sol`](8928.sol)
- **Caught by:** [`rvShUpdateVaultUnlinkIsNeverRefusedForALinkedVault`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L473)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8928`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUpdateVaultUnlinkIsNeverRefusedForALinkedVault`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -132,6 +132,7 @@
         } else if (kind == VaultUpdateKind.Link) {
             spokeRegistry.linkVault(poolId, scId, assetId, vaultOrFactory);
         } else if (kind == VaultUpdateKind.Unlink) {
+            require(payload.length == 0, MalformedVaultUpdateMessage()); // MUTATION: an unlink carrying a payload is refused
             spokeRegistry.unlinkVault(poolId, scId, assetId, vaultOrFactory);
         } else {
             revert MalformedVaultUpdateMessage(); // Unreachable due to the enum check
```

## SpokeHandler #8954

registerVault no longer refuses an address that already has a vault row, so a deploy onto a registered vault overwrites its row.

- **Mutant:** [`8954.sol`](8954.sol)
- **Caught by:** [`rvShUpdateVaultDeployAndLinkRefusesAnUnknownAssetADeadClassOrATakenAddress`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reverts.spec#L306)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 8954`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reverts.conf --rule rvShUpdateVaultDeployAndLinkRefusesAnUnknownAssetADeadClassOrATakenAddress`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -243,7 +243,7 @@
         require(assetIdKey.asset != address(0), UnknownAsset());
         require(assetIdKey.asset == asset && assetIdKey.tokenId == tokenId, UnknownAsset());
 
-        require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
+        // MUTATION: a registered vault address is no longer refused
         require(vault_.code.length > 0, NotAContract());
 
         _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
```

## SpokeHandler #9006

updateShareMetadata sends the name as a restriction update, so the token is not renamed and receives a stray restriction update.

- **Mutant:** [`9006.sol`](9006.sol)
- **Caught by:** [`hlShUpdateShareMetadataWritesNoHandlerOrRegistryField`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/SpokeHandler_LinkedSpokeRegistry_entry_gate_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 9006`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/entry_gate_properties.conf --rule hlShUpdateShareMetadataWritesNoHandlerOrRegistryField`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -84,7 +84,7 @@
     {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
-        registrar.updateMetadata(address(token), name, symbol);
+        registrar.updateRestriction(address(token), bytes(name)); // MUTATION: the rename is sent as a restriction update
     }
 
     /// @inheritdoc ISpokeGatewayHandler
```

## SpokeHandler #9074

Vault registration always records token id zero, so a vault for an ERC6909 asset points at the wrong token.

- **Mutant:** [`9074.sol`](9074.sol)
- **Caught by:** [`hlShDeployAndLinkRegistersTheVaultRowTheMessageNames`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_high_level.spec#L72)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 9074`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/high_level.conf --rule hlShDeployAndLinkRegistersTheVaultRowTheMessageNames`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -246,7 +246,7 @@
         require(_vaultDetails[vault_].asset == address(0), AlreadyRegisteredVault());
         require(vault_.code.length > 0, NotAContract());
 
-        _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, tokenId, false);
+        _vaultDetails[vault_] = VaultDetails(poolId, scId, assetId, asset, 0, false); // MUTATION: the vault row records token id zero as if every asset were an ERC20
         emit DeployVault(poolId, scId, asset, tokenId, factory, vault_, payload);
     }
 
```

## SpokeHandler #9075

Opening a pool no longer records when it was opened, so the pool never counts as active on this spoke.

- **Mutant:** [`9075.sol`](9075.sol)
- **Caught by:** [`rcShAddPoolOpensThePoolIsReachable`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/single/SpokeHandler_LinkedSpokeRegistry_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 9075`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/reachability.conf --rule rcShAddPoolOpensThePoolIsReachable`

```diff
--- a/src/core/spoke/SpokeRegistry.sol
+++ b/src/core/spoke/SpokeRegistry.sol
@@ -63,7 +63,7 @@
         require(!poolId.isNull(), InvalidPool());
         Pool storage pool_ = pool[poolId];
         require(pool_.createdAt == 0, PoolAlreadyAdded());
-        pool_.createdAt = uint64(block.timestamp);
+        // MUTATION: the opening time is no longer written, so the pool is never stamped
 
         emit AddPool(poolId);
     }
```

## SpokeHandler #9240

updateShareMetadata loses its ward gate, so any caller can rename and reticker a share token through the handler.

- **Mutant:** [`9240.sol`](9240.sol)
- **Caught by:** [`acShUpdateShareMetadataRefusesANonWard`](../../specs/core/spoke/SpokeHandler_LinkedSpokeRegistry/SpokeHandler_LinkedSpokeRegistry_entry_gate_properties.spec#L61)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 9240`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedSpokeRegistry/entry_gate_properties.conf --rule acShUpdateShareMetadataRefusesANonWard`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -80,7 +80,7 @@
     /// @inheritdoc ISpokeGatewayHandler
     function updateShareMetadata(PoolId poolId, ShareClassId scId, string memory name, string memory symbol)
         external
-        auth
+        // MUTATION: the ward gate is removed
     {
         (IERC20 token, IRegistrar registrar) = spokeRegistry.shareTokenAndRegistrar(poolId, scId);
         require(address(token) != address(0), ISpokeRegistry.ShareTokenDoesNotExist());
```

## SpokeHandler #9260

addPool registers the pool before deploying its escrow, so the pool is known on the spoke before its escrow exists.

- **Mutant:** [`9260.sol`](9260.sol)
- **Caught by:** [`stShPoolRowOpensOnlyAfterItsEscrowIsBranded`](../../specs/core/spoke/SpokeHandler_LinkedRegistryFactory/SpokeHandler_LinkedRegistryFactory_properties.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh SpokeHandler 9260`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/SpokeHandler_LinkedRegistryFactory/properties.conf --rule stShPoolRowOpensOnlyAfterItsEscrowIsBranded`

```diff
--- a/src/core/spoke/SpokeHandler.sol
+++ b/src/core/spoke/SpokeHandler.sol
@@ -54,8 +54,7 @@
 
     /// @inheritdoc ISpokeGatewayHandler
     function addPool(PoolId poolId) external auth {
-        escrowFactory.newEscrow(poolId);
-        spokeRegistry.addPool(poolId);
+        spokeRegistry.addPool(poolId); escrowFactory.newEscrow(poolId); // MUTATION: the pool is registered before its escrow exists
     }
 
     /// @inheritdoc ISpokeGatewayHandler
```

