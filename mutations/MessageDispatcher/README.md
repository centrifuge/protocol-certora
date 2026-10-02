# Mutations for `MessageDispatcher` (`src/core/messaging/MessageDispatcher.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/messaging/libraries/MessageLib.sol`, `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [1901](#messagedispatcher-1901) | The overload forwards through an external self-call, so its auth checks the dispatcher instead of the caller.<br>Caught by: [`acMdNoUnwardedCallerReachesANeighbour`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_access_control.spec#L42) |
| [1902](#messagedispatcher-1902) | The overload inlines the forwarded body without its auth, so any caller can report assets to the hub or the wire.<br>Caught by: [`acMdNoUnwardedCallerReachesANeighbour`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_access_control.spec#L42) |
| [1903](#messagedispatcher-1903) | file drops its authorization, so any caller can repoint the router at a gateway, handler or envoy of its own.<br>Caught by: [`acMdWiringMovesOnlyForAWard`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_access_control.spec#L19) |
| [1904](#messagedispatcher-1904) | rely drops its authorization, so any caller can hand itself control of the dispatcher.<br>Caught by: [`acMdWardSetMovesOnlyForAWard`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_access_control.spec#L4) |
| [8707](#messagedispatcher-8707) | A local pool announcement is also sent over the wire instead of refunding the fee, so the pool is announced twice.<br>Caught by: [`vtMdEachEntryReachesAtMostOneNeighbour`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_transitions.spec#L6) |
| [8708](#messagedispatcher-8708) | Local and remote routing of pool announcements is swapped, so no pool reaches the chain it was announced for.<br>Caught by: [`hlMdNotifyPoolRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L6) |
| [8709](#messagedispatcher-8709) | Local and remote routing of asset reports is swapped, so holdings are booked on a hub that does not own the pool.<br>Caught by: [`hlMdUpdateAssetsRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L26) |
| [8710](#messagedispatcher-8710) | Local and remote routing of share transfers is swapped, so the receiver is credited on the wrong network.<br>Caught by: [`hlMdExecuteTransferSharesRoutesByTheTargetChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L48) |
| [8711](#messagedispatcher-8711) | A local adapter manager grant goes to the gateway instead of the adapter router, so the wrong contract records it.<br>Caught by: [`hlMdLocalManagerUpdateReachesTheContractOfItsKind`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L71) |
| [8712](#messagedispatcher-8712) | Rewiring the gateway repoints the hub handler instead, so outbound traffic keeps the old gateway.<br>Caught by: [`hlMdFileRepointsOnlyTheNamedSlot`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L94) |
| [8713](#messagedispatcher-8713) | A rewiring under an unknown name is accepted silently, so a mistyped name looks applied while nothing changes.<br>Caught by: [`rvMdFileRefusesANonWardOrAnUnknownName`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reverts.spec#L6) |
| [8714](#messagedispatcher-8714) | A local adapter set announcement is dropped silently instead of refused, so the fee stays in the dispatcher.<br>Caught by: [`rvMdSetPoolAdaptersRefusesTheLocalNetwork`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reverts.spec#L22) |
| [8886](#messagedispatcher-8886) | The adapter set message packs the target session ahead of the threshold, so the receiving chain decodes a garbled threshold and session.<br>Caught by: [`hlMdSetPoolAdaptersWiresItsTargetSession`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L66) |
| [8887](#messagedispatcher-8887) | The asset and share report messages swap type codes, so a chain on the existing numbering books assets as shares and the reverse.<br>Caught by: [`hlMdEverySendCarriesItsFrozenTypeCode`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L81) |
| [8888](#messagedispatcher-8888) | The share transfer message packs the amount ahead of the receiver, so the destination decodes a garbled receiver and amount.<br>Caught by: [`hlMdTransferCarriesTheNamedReceiver`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L95) |
| [8889](#messagedispatcher-8889) | A local share transfer keeps only the leading 20 bytes of its receiver, so shares meant for an invalid receiver land on a truncated address.<br>Caught by: [`hlMdTransferCarriesTheNamedReceiver`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L95) |
| [9039](#messagedispatcher-9039) | Share transfer starts are routed on an inverted hub chain test, so local pools go to the gateway and remote ones never leave.<br>Caught by: [`rcMdInitiateTransferSharesLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L439) · [`rcMdInitiateTransferSharesRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L455) |
| [9040](#messagedispatcher-9040) | Hub manager calls are routed on an inverted destination test, so local calls go to the gateway and remote ones run here.<br>Caught by: [`rcMdManagerCallFromHubLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L185) · [`rcMdManagerCallFromHubRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L200) |
| [9740](#messagedispatcher-9740) | Local and remote legs of pool announcements are swapped, so a remote pool is handled here instead of sent.<br>Caught by: [`hlMdNotifyPoolSendsToTheNamedChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L699) |
| [9741](#messagedispatcher-9741) | Local and remote legs of share class announcements are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdNotifyShareClassRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L128) |
| [9742](#messagedispatcher-9742) | Local and remote legs of share metadata updates are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdNotifyShareMetadataRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L153) |
| [9743](#messagedispatcher-9743) | Local and remote legs of share price updates are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdNotifyPricePoolPerShareRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L176) |
| [9744](#messagedispatcher-9744) | Local and remote legs of asset price updates are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdNotifyPricePoolPerAssetRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L201) |
| [9745](#messagedispatcher-9745) | Local and remote legs of restriction updates are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdUpdateRestrictionRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L225) |
| [9746](#messagedispatcher-9746) | Local and remote legs of manager calls from the hub are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdManagerCallFromHubRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L248) |
| [9747](#messagedispatcher-9747) | Local and remote legs of vault updates are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdUpdateVaultRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L272) |
| [9748](#messagedispatcher-9748) | Local and remote legs of request manager assignments are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdSetRequestManagerRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L297) |
| [9749](#messagedispatcher-9749) | Local and remote legs of spoke call authorizations are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdAuthorizeSpokeCallRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L320) |
| [9750](#messagedispatcher-9750) | Local and remote legs of spoke call revocations are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdUnauthorizeSpokeCallRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L343) |
| [9751](#messagedispatcher-9751) | Local and remote legs of policy assignments are swapped, so each is routed to the wrong side.<br>Caught by: [`hlMdSetPolicyRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L366) |
| [9752](#messagedispatcher-9752) | Local manager updates are sent over the wire and remote ones handled here, so each lands on the wrong side.<br>Caught by: [`hlMdUpdateManagerRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L389) |
| [9753](#messagedispatcher-9753) | Local upgrade schedules are sent over the wire and remote ones handled here, so each lands on the wrong side.<br>Caught by: [`hlMdScheduleUpgradeRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L412) |
| [9754](#messagedispatcher-9754) | Local upgrade cancellations are sent over the wire and remote ones handled here, so each lands on the wrong side.<br>Caught by: [`hlMdCancelUpgradeRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L434) |
| [9755](#messagedispatcher-9755) | Share transfer initiations for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.<br>Caught by: [`hlMdInitiateTransferSharesRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L456) |
| [9756](#messagedispatcher-9756) | Share transfers to this chain are sent over the wire and remote ones handled here, so each lands on the wrong side.<br>Caught by: [`hlMdExecuteTransferSharesSendsToTheTargetChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L734) |
| [9757](#messagedispatcher-9757) | Asset reports for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.<br>Caught by: [`hlMdUpdateAssetsSendsToThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L716) · [`hlMdUpdateHoldingAmountRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L481) · [`hlMdLocalAssetReportCarriesTheFlushedNet`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L753) |
| [9758](#messagedispatcher-9758) | Share reports for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.<br>Caught by: [`hlMdUpdateSharesRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L505) |
| [9759](#messagedispatcher-9759) | Local asset registrations are sent over the wire and remote ones handled here, so each lands on the wrong side.<br>Caught by: [`hlMdRegisterAssetRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L529) |
| [9760](#messagedispatcher-9760) | Requests for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.<br>Caught by: [`hlMdRequestRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L552) |
| [9761](#messagedispatcher-9761) | Spoke manager calls for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.<br>Caught by: [`hlMdManagerCallFromSpokeRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L576) |
| [9762](#messagedispatcher-9762) | Request callbacks for a local asset are sent over the wire and remote ones handled here, so each goes astray.<br>Caught by: [`hlMdRequestCallbackRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L599) |
| [9763](#messagedispatcher-9763) | The adapter set announcement is sent in unpaid mode, so an underfunded one is queued instead of reverting.<br>Caught by: [`hlMdSetPoolAdaptersShipsPaidOverTheGatewayOnce`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L623) |
| [9764](#messagedispatcher-9764) | A local bridger grant or revocation is refunded as done but never reaches the spoke handler, so the bridger set silently keeps its old value.<br>Caught by: [`hlMdEachSendReachesExactlyOneNeighbour`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L115) · [`hlMdUpdateManagerRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L389) |
| [9765](#messagedispatcher-9765) | A local send paid exactly one wei keeps that wei instead of refunding it, so the dispatcher accumulates ETH nobody can reclaim.<br>Caught by: [`hlMdKeepsNoneOfTheValueItIsHanded`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_native_properties.spec#L6) |
| [9766](#messagedispatcher-9766) | The holding amount report refunds its caller instead of the given refund address, so refunds reach the wrong account.<br>Caught by: [`hlMdHoldingAmountShimActsAsUpdateAssetsForAnyPrice`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_native_properties.spec#L28) |
| [9767](#messagedispatcher-9767) | A pool announcement to another chain is sent in unpaid mode, so an underfunded one is queued instead of reverting.<br>Caught by: [`hlMdOnlyRequestsCallbacksAndForwardedTransfersTravelUnpaid`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L641) |
| [9768](#messagedispatcher-9768) | A remote request is always sent paid, ignoring the caller's mode, so an underfunded one reverts instead of being queued.<br>Caught by: [`hlMdRequestAndCallbackCarryTheCallersPaymentMode`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L660) |
| [9769](#messagedispatcher-9769) | A transfer leg's unpaid flag is inverted, so underfunded forwarded transfers revert while underfunded local ones are queued.<br>Caught by: [`hlMdForwardedTransferRunsUnpaidExactlyWhenItArrivedFromElsewhere`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L681) |
| [9770](#messagedispatcher-9770) | A local asset report hands the hub handler the opposite direction, so a deposit is booked on the hub as a withdrawal and the reverse.<br>Caught by: [`hlMdLocalAssetReportCarriesTheFlushedNet`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L753) |
| [9771](#messagedispatcher-9771) | A remote asset price is sent to the pool's hub chain instead of the asset's chain, so the holding spoke never learns it.<br>Caught by: [`hlMdNotifyPricePoolPerAssetRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L201) |
| [9772](#messagedispatcher-9772) | A remote vault update is sent to the pool's hub chain instead of the asset's chain, so the vault is never set up there.<br>Caught by: [`hlMdUpdateVaultRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L272) |
| [9773](#messagedispatcher-9773) | A share transfer started on a spoke is sent to the target chain instead of the pool's hub, so the hub never forwards it.<br>Caught by: [`hlMdInitiateTransferSharesRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L456) |
| [9774](#messagedispatcher-9774) | A remote asset report is sent to the asset's chain instead of the pool's hub chain, so the hub never sees the change.<br>Caught by: [`hlMdUpdateAssetsSendsToThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L716) |
| [9775](#messagedispatcher-9775) | A forwarded share transfer is sent back to its origin chain instead of its target, so the receiver is credited on the wrong chain.<br>Caught by: [`hlMdExecuteTransferSharesSendsToTheTargetChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L734) |
| [9776](#messagedispatcher-9776) | A pool announcement meant for another chain is addressed to this chain, so the chain it names never learns the pool exists.<br>Caught by: [`hlMdNotifyPoolSendsToTheNamedChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L699) |
| [9777](#messagedispatcher-9777) | The length table overstates a pool announcement by one byte, so a batch reader misreads every message after it.<br>Caught by: [`hlMdEveryWireMessageMeasuresItsOwnLength`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L6) |
| [9778](#messagedispatcher-9778) | The share price message swaps the pool and share class id fields, so readers decode a garbled share class.<br>Caught by: [`hlMdEveryPoolMessageCarriesItsPoolAtOffsetOne`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L21) |
| [9779](#messagedispatcher-9779) | The extra gas reader of a share transfer initiation returns its remote gas limit, so the hub leg gets the wrong gas budget.<br>Caught by: [`hlMdEveryWireMessageYieldsItsExtraGasLimit`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L43) |
| [9780](#messagedispatcher-9780) | Every send addressed to another chain reverts instead of reaching the gateway, so no message ever leaves the chain.<br>Caught by: [`rcMdNotifyPoolRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L20) · [`rcMdNotifyShareClassRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L50) · [`rcMdNotifyShareMetadataRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L80) · [`rcMdNotifyPricePoolPerShareRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L110) · [`rcMdNotifyPricePoolPerAssetRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L141) · [`rcMdUpdateRestrictionRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L171) · [`rcMdManagerCallFromHubRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L200) · [`rcMdUpdateVaultRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L231) · [`rcMdSetRequestManagerRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L261) · [`rcMdAuthorizeSpokeCallRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L289) · [`rcMdUnauthorizeSpokeCallRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L317) · [`rcMdSetPolicyRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L345) · [`rcMdUpdateManagerRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L373) · [`rcMdScheduleUpgradeRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L400) · [`rcMdCancelUpgradeRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L426) · [`rcMdInitiateTransferSharesRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L455) · [`rcMdExecuteTransferSharesRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L487) · [`rcMdUpdateAssetsRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L518) · [`rcMdUpdateHoldingAmountRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L548) · [`rcMdUpdateSharesRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L578) · [`rcMdRegisterAssetRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L607) · [`rcMdRequestRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L635) · [`rcMdManagerCallFromSpokeRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L663) · [`rcMdRequestCallbackRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L692) · [`rcMdSetPoolAdaptersRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L707) |
| [9781](#messagedispatcher-9781) | The local refund step always reverts, so most messages addressed to the local chain can no longer be applied.<br>Caught by: [`rcMdNotifyPoolLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L6) · [`rcMdNotifyShareClassLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L34) · [`rcMdNotifyShareMetadataLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L66) · [`rcMdNotifyPricePoolPerShareLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L94) · [`rcMdNotifyPricePoolPerAssetLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L126) · [`rcMdUpdateRestrictionLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L156) · [`rcMdUpdateVaultLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L215) · [`rcMdSetRequestManagerLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L247) · [`rcMdAuthorizeSpokeCallLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L275) · [`rcMdUnauthorizeSpokeCallLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L303) · [`rcMdSetPolicyLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L331) · [`rcMdUpdateManagerLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L359) · [`rcMdScheduleUpgradeLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L387) · [`rcMdCancelUpgradeLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L413) · [`rcMdExecuteTransferSharesLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L471) · [`rcMdUpdateAssetsLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L503) · [`rcMdUpdateHoldingAmountLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L533) · [`rcMdUpdateSharesLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L563) · [`rcMdRegisterAssetLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L593) · [`rcMdRequestLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L621) · [`rcMdManagerCallFromSpokeLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L649) · [`rcMdRequestCallbackLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L677) |
| [9920](#messagedispatcher-9920) | A local share transfer initiation passes the hub handler a zero refund address instead of the caller's, so leftover fees are lost.<br>Caught by: [`rcMpLocalAndRoundTripTransferInitiationHandDifferentRefunds`](../../specs/core/messaging/MessageProcessor/MessageProcessor_joint_properties.spec#L6) |

## MessageDispatcher #1901

The overload forwards through an external self-call, so its auth checks the dispatcher instead of the caller.

- **Mutant:** [`1901.sol`](1901.sol)
- **Caught by:** [`acMdNoUnwardedCallerReachesANeighbour`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_access_control.spec#L42)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 1901`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/access_control.conf --rule acMdNoUnwardedCallerReachesANeighbour`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -538,7 +538,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable {
-        sendUpdateAssets(poolId, scId, assetId, data, extraGasLimit, refund);
+        this.sendUpdateAssets(poolId, scId, assetId, data, extraGasLimit, refund); // MUTATION: external self-call, so auth reads the dispatcher and not the caller
     }
 
     /// @inheritdoc ISpokeMessageSender
```

## MessageDispatcher #1902

The overload inlines the forwarded body without its auth, so any caller can report assets to the hub or the wire.

- **Mutant:** [`1902.sol`](1902.sol)
- **Caught by:** [`acMdNoUnwardedCallerReachesANeighbour`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_access_control.spec#L42)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 1902`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/access_control.conf --rule acMdNoUnwardedCallerReachesANeighbour`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -538,7 +538,31 @@
         uint128 extraGasLimit,
         address refund
     ) external payable {
-        sendUpdateAssets(poolId, scId, assetId, data, extraGasLimit, refund);
+        // MUTATION: the forwarded call inlined, so the gate it was inheriting is gone
+        if (poolId.centrifugeId() == localCentrifugeId) {
+            hubHandler.updateAssets(
+                localCentrifugeId, poolId, scId, assetId, data.netAmount, data.isIncrease, data.isSnapshot, data.nonce
+            );
+            _refund(refund);
+        } else {
+            _send(
+                poolId.centrifugeId(),
+                MessageLib.UpdateAssets({
+                        poolId: poolId.raw(),
+                        scId: scId.raw(),
+                        assetId: assetId.raw(),
+                        amount: data.netAmount,
+                        timestamp: uint64(block.timestamp),
+                        isIncrease: data.isIncrease,
+                        isSnapshot: data.isSnapshot,
+                        nonce: data.nonce,
+                        extraGasLimit: extraGasLimit
+                    }).serialize(),
+                false,
+                refund
+            );
+        }
+    
     }
 
     /// @inheritdoc ISpokeMessageSender
```

## MessageDispatcher #1903

file drops its authorization, so any caller can repoint the router at a gateway, handler or envoy of its own.

- **Mutant:** [`1903.sol`](1903.sol)
- **Caught by:** [`acMdWiringMovesOnlyForAWard`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_access_control.spec#L19)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 1903`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/access_control.conf --rule acMdWiringMovesOnlyForAWard`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -60,7 +60,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IMessageDispatcher
-    function file(bytes32 what, address data) external auth {
+    function file(bytes32 what, address data) external { // MUTATION: the wiring entry loses its gate
         if (what == "envoy") envoy = IEnvoy(data);
         else if (what == "gateway") gateway = IGateway(data);
         else if (what == "multiAdapter") multiAdapter = IMultiAdapter(data);
```

## MessageDispatcher #1904

rely drops its authorization, so any caller can hand itself control of the dispatcher.

- **Mutant:** [`1904.sol`](1904.sol)
- **Caught by:** [`acMdWardSetMovesOnlyForAWard`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 1904`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/access_control.conf --rule acMdWardSetMovesOnlyForAWard`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -22,7 +22,7 @@
     }
 
     /// @inheritdoc IAuth
-    function rely(address user) public auth {
+    function rely(address user) public { // MUTATION: the ward entry loses its gate
         wards[user] = 1;
         emit Rely(user);
     }
```

## MessageDispatcher #8707

A local pool announcement is also sent over the wire instead of refunding the fee, so the pool is announced twice.

- **Mutant:** [`8707.sol`](8707.sol)
- **Caught by:** [`vtMdEachEntryReachesAtMostOneNeighbour`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8707`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/transitions.conf --rule vtMdEachEntryReachesAtMostOneNeighbour`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -79,7 +79,7 @@
     function sendNotifyPool(uint16 centrifugeId, PoolId poolId, address refund) external payable auth {
         if (centrifugeId == localCentrifugeId) {
             spokeHandler.addPool(poolId);
-            _refund(refund);
+            _send(centrifugeId, MessageLib.NotifyPool({poolId: poolId.raw()}).serialize(), false, refund); // MUTATION: the local announcement is also put on the wire
         } else {
             _send(centrifugeId, MessageLib.NotifyPool({poolId: poolId.raw()}).serialize(), false, refund);
         }
```

## MessageDispatcher #8708

Local and remote routing of pool announcements is swapped, so no pool reaches the chain it was announced for.

- **Mutant:** [`8708.sol`](8708.sol)
- **Caught by:** [`hlMdNotifyPoolRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8708`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdNotifyPoolRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -77,7 +77,7 @@
 
     /// @inheritdoc IHubMessageSender
     function sendNotifyPool(uint16 centrifugeId, PoolId poolId, address refund) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: local and remote arms swapped
             spokeHandler.addPool(poolId);
             _refund(refund);
         } else {
```

## MessageDispatcher #8709

Local and remote routing of asset reports is swapped, so holdings are booked on a hub that does not own the pool.

- **Mutant:** [`8709.sol`](8709.sol)
- **Caught by:** [`hlMdUpdateAssetsRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L26)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8709`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdUpdateAssetsRoutesByThePoolsHubChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -501,7 +501,7 @@
         uint128 extraGasLimit,
         address refund
     ) public payable auth {
-        if (poolId.centrifugeId() == localCentrifugeId) {
+        if (poolId.centrifugeId() != localCentrifugeId) { // MUTATION: local and remote arms swapped
             hubHandler.updateAssets(
                 localCentrifugeId, poolId, scId, assetId, data.netAmount, data.isIncrease, data.isSnapshot, data.nonce
             );
```

## MessageDispatcher #8710

Local and remote routing of share transfers is swapped, so the receiver is credited on the wrong network.

- **Mutant:** [`8710.sol`](8710.sol)
- **Caught by:** [`hlMdExecuteTransferSharesRoutesByTheTargetChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L48)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8710`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdExecuteTransferSharesRoutesByTheTargetChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -472,7 +472,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable auth {
-        if (targetCentrifugeId == localCentrifugeId) {
+        if (targetCentrifugeId != localCentrifugeId) { // MUTATION: local and remote arms swapped
             // Spoke chain X => Hub chain Y => Spoke chain Y
             spokeHandler.executeTransferShares(poolId, scId, receiver, amount);
             _refund(refund);
```

## MessageDispatcher #8711

A local adapter manager grant goes to the gateway instead of the adapter router, so the wrong contract records it.

- **Mutant:** [`8711.sol`](8711.sol)
- **Caught by:** [`hlMdLocalManagerUpdateReachesTheContractOfItsKind`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L71)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8711`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdLocalManagerUpdateReachesTheContractOfItsKind`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -378,7 +378,7 @@
             if (kind == ManagerKind.Spoke) {
                 spokeHandler.updateManager(poolId, whoAddr, canManage);
             } else if (kind == ManagerKind.Adapter) {
-                multiAdapter.updateManager(poolId, whoAddr, canManage);
+                gateway.updateManager(poolId, whoAddr, canManage); // MUTATION: the adapter manager grant goes to the gateway
             } else if (kind == ManagerKind.Gateway) {
                 gateway.updateManager(poolId, whoAddr, canManage);
             } else if (kind == ManagerKind.Bridger) {
```

## MessageDispatcher #8712

Rewiring the gateway repoints the hub handler instead, so outbound traffic keeps the old gateway.

- **Mutant:** [`8712.sol`](8712.sol)
- **Caught by:** [`hlMdFileRepointsOnlyTheNamedSlot`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L94)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8712`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdFileRepointsOnlyTheNamedSlot`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -62,7 +62,7 @@
     /// @inheritdoc IMessageDispatcher
     function file(bytes32 what, address data) external auth {
         if (what == "envoy") envoy = IEnvoy(data);
-        else if (what == "gateway") gateway = IGateway(data);
+        else if (what == "gateway") hubHandler = IHubGatewayHandler(data); // MUTATION: the gateway name repoints the hub handler
         else if (what == "multiAdapter") multiAdapter = IMultiAdapter(data);
         else if (what == "spokeHandler") spokeHandler = ISpokeGatewayHandler(data);
         else if (what == "hubHandler") hubHandler = IHubGatewayHandler(data);
```

## MessageDispatcher #8713

A rewiring under an unknown name is accepted silently, so a mistyped name looks applied while nothing changes.

- **Mutant:** [`8713.sol`](8713.sol)
- **Caught by:** [`rvMdFileRefusesANonWardOrAnUnknownName`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reverts.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8713`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/reverts.conf --rule rvMdFileRefusesANonWardOrAnUnknownName`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -66,7 +66,7 @@
         else if (what == "multiAdapter") multiAdapter = IMultiAdapter(data);
         else if (what == "spokeHandler") spokeHandler = ISpokeGatewayHandler(data);
         else if (what == "hubHandler") hubHandler = IHubGatewayHandler(data);
-        else revert FileUnrecognizedParam();
+        else {} // MUTATION: an unknown name is accepted
 
         emit File(what, data);
     }
```

## MessageDispatcher #8714

A local adapter set announcement is dropped silently instead of refused, so the fee stays in the dispatcher.

- **Mutant:** [`8714.sol`](8714.sol)
- **Caught by:** [`rvMdSetPoolAdaptersRefusesTheLocalNetwork`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reverts.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8714`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/reverts.conf --rule rvMdSetPoolAdaptersRefusesTheLocalNetwork`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -690,7 +690,7 @@
         address refund
     ) external payable auth {
         if (centrifugeId == localCentrifugeId) {
-            revert CannotBeSentLocally();
+            // MUTATION: the local refusal is dropped
         } else {
             _send(
                 centrifugeId,
```

## MessageDispatcher #8886

The adapter set message packs the target session ahead of the threshold, so the receiving chain decodes a garbled threshold and session.

- **Mutant:** [`8886.sol`](8886.sol)
- **Caught by:** [`hlMdSetPoolAdaptersWiresItsTargetSession`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L66)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8886`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/wire_properties.conf --rule hlMdSetPoolAdaptersWiresItsTargetSession`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -342,8 +342,7 @@
         return abi.encodePacked(
             MessageType.SetPoolAdapters,
             t.poolId,
-            t.threshold,
-            t.targetSessionId,
+            t.targetSessionId, t.threshold, // MUTATION: the session is packed ahead of the threshold
             t.adapterList.length.toUint16(),
             t.adapterList
         );
```

## MessageDispatcher #8887

The asset and share report messages swap type codes, so a chain on the existing numbering books assets as shares and the reverse.

- **Mutant:** [`8887.sol`](8887.sol)
- **Caught by:** [`hlMdEverySendCarriesItsFrozenTypeCode`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L81)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8887`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/wire_properties.conf --rule hlMdEverySendCarriesItsFrozenTypeCode`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -31,8 +31,7 @@
     UpdateRestriction,
     UpdateVault,
     // --- Balance sheet ---
-    UpdateAssets,
-    UpdateShares,
+    UpdateShares, UpdateAssets, // MUTATION: the two balance sheet codes are renumbered
     // --- Investment requests ---
     Request,
     RequestCallback,
```

## MessageDispatcher #8888

The share transfer message packs the amount ahead of the receiver, so the destination decodes a garbled receiver and amount.

- **Mutant:** [`8888.sol`](8888.sol)
- **Caught by:** [`hlMdTransferCarriesTheNamedReceiver`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L95)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8888`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/wire_properties.conf --rule hlMdTransferCarriesTheNamedReceiver`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -578,7 +578,7 @@
 
     function serialize(ExecuteTransferShares memory t) internal pure returns (bytes memory) {
         return
-            abi.encodePacked(MessageType.ExecuteTransferShares, t.poolId, t.scId, t.receiver, t.amount, t.extraGasLimit);
+            abi.encodePacked(MessageType.ExecuteTransferShares, t.poolId, t.scId, t.amount, t.receiver, t.extraGasLimit); // MUTATION: the amount is packed ahead of the receiver
     }
 
     //---------------------------------------
```

## MessageDispatcher #8889

A local share transfer keeps only the leading 20 bytes of its receiver, so shares meant for an invalid receiver land on a truncated address.

- **Mutant:** [`8889.sol`](8889.sol)
- **Caught by:** [`hlMdTransferCarriesTheNamedReceiver`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L95)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 8889`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/wire_properties.conf --rule hlMdTransferCarriesTheNamedReceiver`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -474,7 +474,7 @@
     ) external payable auth {
         if (targetCentrifugeId == localCentrifugeId) {
             // Spoke chain X => Hub chain Y => Spoke chain Y
-            spokeHandler.executeTransferShares(poolId, scId, receiver, amount);
+            spokeHandler.executeTransferShares(poolId, scId, bytes32(bytes20(receiver)), amount); // MUTATION: the local receiver keeps only its leading 20 bytes
             _refund(refund);
         } else {
             _send(
```

## MessageDispatcher #9039

Share transfer starts are routed on an inverted hub chain test, so local pools go to the gateway and remote ones never leave.

- **Mutant:** [`9039.sol`](9039.sol)
- **Caught by:** [`rcMdInitiateTransferSharesLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L439) · [`rcMdInitiateTransferSharesRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L455)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9039`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/reachability.conf --rule rcMdInitiateTransferSharesLocalLegIsReachable rcMdInitiateTransferSharesRemoteLegIsReachable`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -430,7 +430,7 @@
         uint128 remoteExtraGasLimit,
         address refund
     ) external payable auth {
-        if (poolId.centrifugeId() == localCentrifugeId) {
+        if (poolId.centrifugeId() != localCentrifugeId) { // MUTATION: sendInitiateTransferShares takes the remote leg for a local pool and the local leg for a remote one
             hubHandler.initiateTransferShares{value: msg.value}(
                 localCentrifugeId,
                 targetCentrifugeId,
```

## MessageDispatcher #9040

Hub manager calls are routed on an inverted destination test, so local calls go to the gateway and remote ones run here.

- **Mutant:** [`9040.sol`](9040.sol)
- **Caught by:** [`rcMdManagerCallFromHubLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L185) · [`rcMdManagerCallFromHubRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L200)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9040`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/reachability.conf --rule rcMdManagerCallFromHubLocalLegIsReachable rcMdManagerCallFromHubRemoteLegIsReachable`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -246,7 +246,7 @@
     ) external payable auth {
         // `target` is explicit: the `fromHub` manager being addressed. No origin args: already authorized
         // at the Hub.
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: sendManagerCallFromHub takes the remote leg for a local pool and the local leg for a remote one
             envoy.callFromHub{value: value}(poolId, target, payload);
             // Refund any value not forwarded rather than assume `value == msgValue()`: if that Hub
             // precondition ever changes, the remainder is returned instead of silently stranded here.
```

## MessageDispatcher #9740

Local and remote legs of pool announcements are swapped, so a remote pool is handled here instead of sent.

- **Mutant:** [`9740.sol`](9740.sol)
- **Caught by:** [`hlMdNotifyPoolSendsToTheNamedChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L699)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9740`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdNotifyPoolSendsToTheNamedChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -77,7 +77,7 @@
 
     /// @inheritdoc IHubMessageSender
     function sendNotifyPool(uint16 centrifugeId, PoolId poolId, address refund) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.addPool(poolId);
             _refund(refund);
         } else {
```

## MessageDispatcher #9741

Local and remote legs of share class announcements are swapped, so each is routed to the wrong side.

- **Mutant:** [`9741.sol`](9741.sol)
- **Caught by:** [`hlMdNotifyShareClassRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L128)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9741`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdNotifyShareClassRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -97,7 +97,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.addShareClass(
                 poolId,
                 scId,
```

## MessageDispatcher #9742

Local and remote legs of share metadata updates are swapped, so each is routed to the wrong side.

- **Mutant:** [`9742.sol`](9742.sol)
- **Caught by:** [`hlMdNotifyShareMetadataRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L153)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9742`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdNotifyShareMetadataRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -139,7 +139,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.updateShareMetadata(poolId, scId, name, symbol);
             _refund(refund);
         } else {
```

## MessageDispatcher #9743

Local and remote legs of share price updates are swapped, so each is routed to the wrong side.

- **Mutant:** [`9743.sol`](9743.sol)
- **Caught by:** [`hlMdNotifyPricePoolPerShareRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L176)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9743`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdNotifyPricePoolPerShareRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -167,7 +167,7 @@
         uint64 computedAt,
         address refund
     ) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.updatePricePoolPerShare(poolId, scId, pricePoolPerShare, computedAt);
             _refund(refund);
         } else {
```

## MessageDispatcher #9744

Local and remote legs of asset price updates are swapped, so each is routed to the wrong side.

- **Mutant:** [`9744.sol`](9744.sol)
- **Caught by:** [`hlMdNotifyPricePoolPerAssetRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L201)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9744`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdNotifyPricePoolPerAssetRoutesByTheAssetsChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -191,7 +191,7 @@
         address refund
     ) external payable auth {
         uint64 timestamp = block.timestamp.toUint64();
-        if (assetId.centrifugeId() == localCentrifugeId) {
+        if (assetId.centrifugeId() != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.updatePricePoolPerAsset(poolId, scId, assetId, pricePoolPerAsset, timestamp);
             _refund(refund);
         } else {
```

## MessageDispatcher #9745

Local and remote legs of restriction updates are swapped, so each is routed to the wrong side.

- **Mutant:** [`9745.sol`](9745.sol)
- **Caught by:** [`hlMdUpdateRestrictionRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L225)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9745`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdUpdateRestrictionRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -219,7 +219,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.updateRestriction(poolId, scId, payload);
             _refund(refund);
         } else {
```

## MessageDispatcher #9746

Local and remote legs of manager calls from the hub are swapped, so each is routed to the wrong side.

- **Mutant:** [`9746.sol`](9746.sol)
- **Caught by:** [`hlMdManagerCallFromHubRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L248)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9746`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdManagerCallFromHubRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -246,7 +246,7 @@
     ) external payable auth {
         // `target` is explicit: the `fromHub` manager being addressed. No origin args: already authorized
         // at the Hub.
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             envoy.callFromHub{value: value}(poolId, target, payload);
             // Refund any value not forwarded rather than assume `value == msgValue()`: if that Hub
             // precondition ever changes, the remainder is returned instead of silently stranded here.
```

## MessageDispatcher #9747

Local and remote legs of vault updates are swapped, so each is routed to the wrong side.

- **Mutant:** [`9747.sol`](9747.sol)
- **Caught by:** [`hlMdUpdateVaultRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L272)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9747`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdUpdateVaultRoutesByTheAssetsChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -276,7 +276,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable auth {
-        if (assetId.centrifugeId() == localCentrifugeId) {
+        if (assetId.centrifugeId() != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.updateVault(poolId, scId, assetId, vaultOrFactory.toAddress(), kind, payload);
             _refund(refund);
         } else {
```

## MessageDispatcher #9748

Local and remote legs of request manager assignments are swapped, so each is routed to the wrong side.

- **Mutant:** [`9748.sol`](9748.sol)
- **Caught by:** [`hlMdSetRequestManagerRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L297)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9748`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdSetRequestManagerRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -303,7 +303,7 @@
         payable
         auth
     {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.setRequestManager(poolId, ISpokeRequestManager(manager.toAddress()));
             _refund(refund);
         } else {
```

## MessageDispatcher #9749

Local and remote legs of spoke call authorizations are swapped, so each is routed to the wrong side.

- **Mutant:** [`9749.sol`](9749.sol)
- **Caught by:** [`hlMdAuthorizeSpokeCallRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L320)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9749`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdAuthorizeSpokeCallRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -322,7 +322,7 @@
         payable
         auth
     {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.authorize(poolId, data);
             _refund(refund);
         } else {
```

## MessageDispatcher #9750

Local and remote legs of spoke call revocations are swapped, so each is routed to the wrong side.

- **Mutant:** [`9750.sol`](9750.sol)
- **Caught by:** [`hlMdUnauthorizeSpokeCallRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L343)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9750`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdUnauthorizeSpokeCallRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -341,7 +341,7 @@
         payable
         auth
     {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.unauthorize(poolId, data);
             _refund(refund);
         } else {
```

## MessageDispatcher #9751

Local and remote legs of policy assignments are swapped, so each is routed to the wrong side.

- **Mutant:** [`9751.sol`](9751.sol)
- **Caught by:** [`hlMdSetPolicyRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L366)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9751`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdSetPolicyRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -356,7 +356,7 @@
 
     /// @inheritdoc IHubMessageSender
     function sendSetPolicy(uint16 centrifugeId, PoolId poolId, bytes32 policy, address refund) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.setPolicy(poolId, IPolicy(policy.toAddress()));
             _refund(refund);
         } else {
```

## MessageDispatcher #9752

Local manager updates are sent over the wire and remote ones handled here, so each lands on the wrong side.

- **Mutant:** [`9752.sol`](9752.sol)
- **Caught by:** [`hlMdUpdateManagerRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L389)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9752`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdUpdateManagerRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -373,7 +373,7 @@
         bool canManage,
         address refund
     ) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             address whoAddr = who.toAddress();
             if (kind == ManagerKind.Spoke) {
                 spokeHandler.updateManager(poolId, whoAddr, canManage);
```

## MessageDispatcher #9753

Local upgrade schedules are sent over the wire and remote ones handled here, so each lands on the wrong side.

- **Mutant:** [`9753.sol`](9753.sol)
- **Caught by:** [`hlMdScheduleUpgradeRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L412)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9753`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdScheduleUpgradeRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -400,7 +400,7 @@
 
     /// @inheritdoc IScheduleAuthMessageSender
     function sendScheduleUpgrade(uint16 centrifugeId, bytes32 target, address refund) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             scheduleAuth.scheduleRely(target.toAddress());
             _refund(refund);
         } else {
```

## MessageDispatcher #9754

Local upgrade cancellations are sent over the wire and remote ones handled here, so each lands on the wrong side.

- **Mutant:** [`9754.sol`](9754.sol)
- **Caught by:** [`hlMdCancelUpgradeRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L434)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9754`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdCancelUpgradeRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -410,7 +410,7 @@
 
     /// @inheritdoc IScheduleAuthMessageSender
     function sendCancelUpgrade(uint16 centrifugeId, bytes32 target, address refund) external payable auth {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             scheduleAuth.cancelRely(target.toAddress());
             _refund(refund);
         } else {
```

## MessageDispatcher #9755

Share transfer initiations for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.

- **Mutant:** [`9755.sol`](9755.sol)
- **Caught by:** [`hlMdInitiateTransferSharesRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L456)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9755`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdInitiateTransferSharesRoutesByThePoolsHubChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -430,7 +430,7 @@
         uint128 remoteExtraGasLimit,
         address refund
     ) external payable auth {
-        if (poolId.centrifugeId() == localCentrifugeId) {
+        if (poolId.centrifugeId() != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             hubHandler.initiateTransferShares{value: msg.value}(
                 localCentrifugeId,
                 targetCentrifugeId,
```

## MessageDispatcher #9756

Share transfers to this chain are sent over the wire and remote ones handled here, so each lands on the wrong side.

- **Mutant:** [`9756.sol`](9756.sol)
- **Caught by:** [`hlMdExecuteTransferSharesSendsToTheTargetChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L734)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9756`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdExecuteTransferSharesSendsToTheTargetChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -472,7 +472,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable auth {
-        if (targetCentrifugeId == localCentrifugeId) {
+        if (targetCentrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             // Spoke chain X => Hub chain Y => Spoke chain Y
             spokeHandler.executeTransferShares(poolId, scId, receiver, amount);
             _refund(refund);
```

## MessageDispatcher #9757

Asset reports for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.

- **Mutant:** [`9757.sol`](9757.sol)
- **Caught by:** [`hlMdUpdateAssetsSendsToThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L716) · [`hlMdUpdateHoldingAmountRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L481) · [`hlMdLocalAssetReportCarriesTheFlushedNet`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L753)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9757`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdUpdateAssetsSendsToThePoolsHubChain hlMdUpdateHoldingAmountRoutesByThePoolsHubChain hlMdLocalAssetReportCarriesTheFlushedNet`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -501,7 +501,7 @@
         uint128 extraGasLimit,
         address refund
     ) public payable auth {
-        if (poolId.centrifugeId() == localCentrifugeId) {
+        if (poolId.centrifugeId() != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             hubHandler.updateAssets(
                 localCentrifugeId, poolId, scId, assetId, data.netAmount, data.isIncrease, data.isSnapshot, data.nonce
             );
```

## MessageDispatcher #9758

Share reports for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.

- **Mutant:** [`9758.sol`](9758.sol)
- **Caught by:** [`hlMdUpdateSharesRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L505)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9758`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdUpdateSharesRoutesByThePoolsHubChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -549,7 +549,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable auth {
-        if (poolId.centrifugeId() == localCentrifugeId) {
+        if (poolId.centrifugeId() != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             hubHandler.updateShares(
                 localCentrifugeId, poolId, scId, data.netAmount, data.isIncrease, data.isSnapshot, data.nonce
             );
```

## MessageDispatcher #9759

Local asset registrations are sent over the wire and remote ones handled here, so each lands on the wrong side.

- **Mutant:** [`9759.sol`](9759.sol)
- **Caught by:** [`hlMdRegisterAssetRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L529)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9759`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdRegisterAssetRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -579,7 +579,7 @@
         payable
         auth
     {
-        if (centrifugeId == localCentrifugeId) {
+        if (centrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             hubHandler.registerAsset(assetId, decimals);
             _refund(refund);
         } else {
```

## MessageDispatcher #9760

Requests for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.

- **Mutant:** [`9760.sol`](9760.sol)
- **Caught by:** [`hlMdRequestRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L552)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9760`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdRequestRoutesByThePoolsHubChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -602,7 +602,7 @@
         bool unpaidMode,
         address refund
     ) external payable auth {
-        if (poolId.centrifugeId() == localCentrifugeId) {
+        if (poolId.centrifugeId() != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             hubHandler.request(poolId, scId, assetId, payload);
             _refund(refund);
         } else {
```

## MessageDispatcher #9761

Spoke manager calls for a locally hubbed pool are sent over the wire and remote ones handled here, so each goes astray.

- **Mutant:** [`9761.sol`](9761.sol)
- **Caught by:** [`hlMdManagerCallFromSpokeRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L576)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9761`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdManagerCallFromSpokeRoutesByThePoolsHubChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -632,7 +632,7 @@
     ) external payable auth {
         uint16 hubCentrifugeId = poolId.centrifugeId();
 
-        if (hubCentrifugeId == localCentrifugeId) {
+        if (hubCentrifugeId != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             envoy.callFromSpoke(poolId, target.toAddress(), payload, localCentrifugeId, sender);
             _refund(refund);
         } else {
```

## MessageDispatcher #9762

Request callbacks for a local asset are sent over the wire and remote ones handled here, so each goes astray.

- **Mutant:** [`9762.sol`](9762.sol)
- **Caught by:** [`hlMdRequestCallbackRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L599)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9762`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdRequestCallbackRoutesByTheAssetsChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -661,7 +661,7 @@
         bool unpaidMode,
         address refund
     ) external payable auth {
-        if (assetId.centrifugeId() == localCentrifugeId) {
+        if (assetId.centrifugeId() != localCentrifugeId) { // MUTATION: the local and the remote leg trade places
             spokeHandler.requestCallback(poolId, scId, assetId, payload);
             _refund(refund);
         } else {
```

## MessageDispatcher #9763

The adapter set announcement is sent in unpaid mode, so an underfunded one is queued instead of reverting.

- **Mutant:** [`9763.sol`](9763.sol)
- **Caught by:** [`hlMdSetPoolAdaptersShipsPaidOverTheGatewayOnce`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L623)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9763`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdSetPoolAdaptersShipsPaidOverTheGatewayOnce`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -700,7 +700,7 @@
                         targetSessionId: targetSessionId,
                         adapterList: adapters
                     }).serialize(),
-                false,
+                true, // MUTATION: the adapter set announcement is booked unpaid
                 refund
             );
         }
```

## MessageDispatcher #9764

A local bridger grant or revocation is refunded as done but never reaches the spoke handler, so the bridger set silently keeps its old value.

- **Mutant:** [`9764.sol`](9764.sol)
- **Caught by:** [`hlMdEachSendReachesExactlyOneNeighbour`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L115) · [`hlMdUpdateManagerRoutesByDestination`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L389)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9764`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdEachSendReachesExactlyOneNeighbour hlMdUpdateManagerRoutesByDestination`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -382,7 +382,7 @@
             } else if (kind == ManagerKind.Gateway) {
                 gateway.updateManager(poolId, whoAddr, canManage);
             } else if (kind == ManagerKind.Bridger) {
-                spokeHandler.updateBridger(poolId, whoAddr, canManage);
+                // MUTATION: the bridger grant never reaches the spoke handler
             } else {
                 revert InvalidManagerKind(); // Unreachable due the enum check
             }
```

## MessageDispatcher #9765

A local send paid exactly one wei keeps that wei instead of refunding it, so the dispatcher accumulates ETH nobody can reclaim.

- **Mutant:** [`9765.sol`](9765.sol)
- **Caught by:** [`hlMdKeepsNoneOfTheValueItIsHanded`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_native_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9765`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/native_properties.conf --rule hlMdKeepsNoneOfTheValueItIsHanded`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -711,7 +711,7 @@
     }
 
     function _refund(address refund) internal {
-        if (msg.value > 0) {
+        if (msg.value > 1) { // MUTATION: a single wei is kept rather than refunded
             SafeTransferLib.safeTransferETH(refund, msg.value);
         }
     }
```

## MessageDispatcher #9766

The holding amount report refunds its caller instead of the given refund address, so refunds reach the wrong account.

- **Mutant:** [`9766.sol`](9766.sol)
- **Caught by:** [`hlMdHoldingAmountShimActsAsUpdateAssetsForAnyPrice`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_native_properties.spec#L28)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9766`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/native_properties.conf --rule hlMdHoldingAmountShimActsAsUpdateAssetsForAnyPrice`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -538,7 +538,7 @@
         uint128 extraGasLimit,
         address refund
     ) external payable {
-        sendUpdateAssets(poolId, scId, assetId, data, extraGasLimit, refund);
+        sendUpdateAssets(poolId, scId, assetId, data, extraGasLimit, msg.sender); // MUTATION: the shim refunds its caller instead of the refund address
     }
 
     /// @inheritdoc ISpokeMessageSender
```

## MessageDispatcher #9767

A pool announcement to another chain is sent in unpaid mode, so an underfunded one is queued instead of reverting.

- **Mutant:** [`9767.sol`](9767.sol)
- **Caught by:** [`hlMdOnlyRequestsCallbacksAndForwardedTransfersTravelUnpaid`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L641)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9767`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdOnlyRequestsCallbacksAndForwardedTransfersTravelUnpaid`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -81,7 +81,7 @@
             spokeHandler.addPool(poolId);
             _refund(refund);
         } else {
-            _send(centrifugeId, MessageLib.NotifyPool({poolId: poolId.raw()}).serialize(), false, refund);
+            _send(centrifugeId, MessageLib.NotifyPool({poolId: poolId.raw()}).serialize(), true, refund); // MUTATION: the pool announcement travels unpaid
         }
     }
 
```

## MessageDispatcher #9768

A remote request is always sent paid, ignoring the caller's mode, so an underfunded one reverts instead of being queued.

- **Mutant:** [`9768.sol`](9768.sol)
- **Caught by:** [`hlMdRequestAndCallbackCarryTheCallersPaymentMode`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L660)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9768`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdRequestAndCallbackCarryTheCallersPaymentMode`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -615,7 +615,7 @@
                         extraGasLimit: extraGasLimit,
                         payload: payload
                     }).serialize(),
-                unpaidMode,
+                false, // MUTATION: the caller's payment mode is dropped
                 refund
             );
         }
```

## MessageDispatcher #9769

A transfer leg's unpaid flag is inverted, so underfunded forwarded transfers revert while underfunded local ones are queued.

- **Mutant:** [`9769.sol`](9769.sol)
- **Caught by:** [`hlMdForwardedTransferRunsUnpaidExactlyWhenItArrivedFromElsewhere`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L681)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9769`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdForwardedTransferRunsUnpaidExactlyWhenItArrivedFromElsewhere`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -486,7 +486,7 @@
                         amount: amount,
                         extraGasLimit: extraGasLimit
                     }).serialize(),
-                originCentrifugeId != localCentrifugeId,
+                originCentrifugeId == localCentrifugeId, // MUTATION: the unpaid flag of a transfer leg is inverted
                 refund
             );
         }
```

## MessageDispatcher #9770

A local asset report hands the hub handler the opposite direction, so a deposit is booked on the hub as a withdrawal and the reverse.

- **Mutant:** [`9770.sol`](9770.sol)
- **Caught by:** [`hlMdLocalAssetReportCarriesTheFlushedNet`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L753)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9770`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdLocalAssetReportCarriesTheFlushedNet`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -503,7 +503,7 @@
     ) public payable auth {
         if (poolId.centrifugeId() == localCentrifugeId) {
             hubHandler.updateAssets(
-                localCentrifugeId, poolId, scId, assetId, data.netAmount, data.isIncrease, data.isSnapshot, data.nonce
+                localCentrifugeId, poolId, scId, assetId, data.netAmount, !data.isIncrease, data.isSnapshot, data.nonce // MUTATION: the local report flips its direction
             );
             _refund(refund);
         } else {
```

## MessageDispatcher #9771

A remote asset price is sent to the pool's hub chain instead of the asset's chain, so the holding spoke never learns it.

- **Mutant:** [`9771.sol`](9771.sol)
- **Caught by:** [`hlMdNotifyPricePoolPerAssetRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L201)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9771`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdNotifyPricePoolPerAssetRoutesByTheAssetsChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -196,7 +196,7 @@
             _refund(refund);
         } else {
             _send(
-                assetId.centrifugeId(),
+                poolId.centrifugeId(), // MUTATION: the asset price goes to the pool's chain
                 MessageLib.NotifyPricePoolPerAsset({
                         poolId: poolId.raw(),
                         scId: scId.raw(),
```

## MessageDispatcher #9772

A remote vault update is sent to the pool's hub chain instead of the asset's chain, so the vault is never set up there.

- **Mutant:** [`9772.sol`](9772.sol)
- **Caught by:** [`hlMdUpdateVaultRoutesByTheAssetsChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L272)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9772`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdUpdateVaultRoutesByTheAssetsChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -281,7 +281,7 @@
             _refund(refund);
         } else {
             _send(
-                assetId.centrifugeId(),
+                poolId.centrifugeId(), // MUTATION: the vault update goes to the pool's chain
                 MessageLib.UpdateVault({
                         poolId: poolId.raw(),
                         scId: scId.raw(),
```

## MessageDispatcher #9773

A share transfer started on a spoke is sent to the target chain instead of the pool's hub, so the hub never forwards it.

- **Mutant:** [`9773.sol`](9773.sol)
- **Caught by:** [`hlMdInitiateTransferSharesRoutesByThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L456)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9773`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdInitiateTransferSharesRoutesByThePoolsHubChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -444,7 +444,7 @@
             );
         } else {
             _send(
-                poolId.centrifugeId(),
+                targetCentrifugeId, // MUTATION: the transfer initiation goes to the target chain
                 MessageLib.InitiateTransferShares({
                         centrifugeId: targetCentrifugeId,
                         poolId: poolId.raw(),
```

## MessageDispatcher #9774

A remote asset report is sent to the asset's chain instead of the pool's hub chain, so the hub never sees the change.

- **Mutant:** [`9774.sol`](9774.sol)
- **Caught by:** [`hlMdUpdateAssetsSendsToThePoolsHubChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L716)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9774`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdUpdateAssetsSendsToThePoolsHubChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -508,7 +508,7 @@
             _refund(refund);
         } else {
             _send(
-                poolId.centrifugeId(),
+                assetId.centrifugeId(), // MUTATION: the asset report goes to the asset's chain
                 MessageLib.UpdateAssets({
                         poolId: poolId.raw(),
                         scId: scId.raw(),
```

## MessageDispatcher #9775

A forwarded share transfer is sent back to its origin chain instead of its target, so the receiver is credited on the wrong chain.

- **Mutant:** [`9775.sol`](9775.sol)
- **Caught by:** [`hlMdExecuteTransferSharesSendsToTheTargetChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L734)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9775`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdExecuteTransferSharesSendsToTheTargetChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -478,7 +478,7 @@
             _refund(refund);
         } else {
             _send(
-                targetCentrifugeId,
+                originCentrifugeId, // MUTATION: the transfer goes back to its origin chain
                 MessageLib.ExecuteTransferShares({
                         poolId: poolId.raw(),
                         scId: scId.raw(),
```

## MessageDispatcher #9776

A pool announcement meant for another chain is addressed to this chain, so the chain it names never learns the pool exists.

- **Mutant:** [`9776.sol`](9776.sol)
- **Caught by:** [`hlMdNotifyPoolSendsToTheNamedChain`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_high_level.spec#L699)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9776`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/high_level.conf --rule hlMdNotifyPoolSendsToTheNamedChain`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -81,7 +81,7 @@
             spokeHandler.addPool(poolId);
             _refund(refund);
         } else {
-            _send(centrifugeId, MessageLib.NotifyPool({poolId: poolId.raw()}).serialize(), false, refund);
+            _send(localCentrifugeId, MessageLib.NotifyPool({poolId: poolId.raw()}).serialize(), false, refund); // MUTATION: the announcement is addressed to this chain
         }
     }
 
```

## MessageDispatcher #9777

The length table overstates a pool announcement by one byte, so a batch reader misreads every message after it.

- **Mutant:** [`9777.sol`](9777.sol)
- **Caught by:** [`hlMdEveryWireMessageMeasuresItsOwnLength`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9777`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/wire_properties.conf --rule hlMdEveryWireMessageMeasuresItsOwnLength`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -82,7 +82,7 @@
         (33  << uint8(MessageType.CancelUpgrade) * 8) +
         (18  << uint8(MessageType.RegisterAsset) * 8) +
         (14  << uint8(MessageType.SetPoolAdapters) * 8) +
-        (9   << uint8(MessageType.NotifyPool) * 8) +
+        (10  << uint8(MessageType.NotifyPool) * 8) + // MUTATION: the length table overstates a pool announcement by one byte
         (250 << uint8(MessageType.NotifyShareClass) * 8) +
         (49  << uint8(MessageType.NotifyPricePoolPerShare) * 8) +
         (65  << uint8(MessageType.NotifyPricePoolPerAsset) * 8) +
```

## MessageDispatcher #9778

The share price message swaps the pool and share class id fields, so readers decode a garbled share class.

- **Mutant:** [`9778.sol`](9778.sol)
- **Caught by:** [`hlMdEveryPoolMessageCarriesItsPoolAtOffsetOne`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L21)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9778`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/wire_properties.conf --rule hlMdEveryPoolMessageCarriesItsPoolAtOffsetOne`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -437,7 +437,7 @@
     }
 
     function serialize(NotifyPricePoolPerShare memory t) internal pure returns (bytes memory) {
-        return abi.encodePacked(MessageType.NotifyPricePoolPerShare, t.poolId, t.scId, t.price, t.timestamp);
+        return abi.encodePacked(MessageType.NotifyPricePoolPerShare, t.scId, t.poolId, t.price, t.timestamp); // MUTATION: the share price message puts the share class where the pool belongs
     }
 
     //---------------------------------------
```

## MessageDispatcher #9779

The extra gas reader of a share transfer initiation returns its remote gas limit, so the hub leg gets the wrong gas budget.

- **Mutant:** [`9779.sol`](9779.sol)
- **Caught by:** [`hlMdEveryWireMessageYieldsItsExtraGasLimit`](../../specs/core/messaging/MessageDispatcher/MessageDispatcher_wire_properties.spec#L43)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9779`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/wire_properties.conf --rule hlMdEveryWireMessageYieldsItsExtraGasLimit`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -234,7 +234,7 @@
         } else if (kind == uint8(MessageType.NotifyShareMetadata)) {
             return message.toUint128(185);
         } else if (kind == uint8(MessageType.InitiateTransferShares)) {
-            return message.toUint128(91);
+            return message.toUint128(75); // MUTATION: the gas reader reads the remote limit of a transfer initiation
         } else if (kind == uint8(MessageType.ExecuteTransferShares)) {
             return message.toUint128(73);
         } else if (kind == uint8(MessageType.UpdateRestriction)) {
```

## MessageDispatcher #9780

Every send addressed to another chain reverts instead of reaching the gateway, so no message ever leaves the chain.

- **Mutant:** [`9780.sol`](9780.sol)
- **Caught by:** [`rcMdNotifyPoolRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L20) · [`rcMdNotifyShareClassRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L50) · [`rcMdNotifyShareMetadataRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L80) · [`rcMdNotifyPricePoolPerShareRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L110) · [`rcMdNotifyPricePoolPerAssetRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L141) · [`rcMdUpdateRestrictionRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L171) · [`rcMdManagerCallFromHubRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L200) · [`rcMdUpdateVaultRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L231) · [`rcMdSetRequestManagerRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L261) · [`rcMdAuthorizeSpokeCallRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L289) · [`rcMdUnauthorizeSpokeCallRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L317) · [`rcMdSetPolicyRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L345) · [`rcMdUpdateManagerRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L373) · [`rcMdScheduleUpgradeRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L400) · [`rcMdCancelUpgradeRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L426) · [`rcMdInitiateTransferSharesRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L455) · [`rcMdExecuteTransferSharesRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L487) · [`rcMdUpdateAssetsRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L518) · [`rcMdUpdateHoldingAmountRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L548) · [`rcMdUpdateSharesRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L578) · [`rcMdRegisterAssetRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L607) · [`rcMdRequestRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L635) · [`rcMdManagerCallFromSpokeRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L663) · [`rcMdRequestCallbackRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L692) · [`rcMdSetPoolAdaptersRemoteLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L707)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9780`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/reachability.conf --rule rcMdNotifyPoolRemoteLegIsReachable rcMdNotifyShareClassRemoteLegIsReachable rcMdNotifyShareMetadataRemoteLegIsReachable rcMdNotifyPricePoolPerShareRemoteLegIsReachable rcMdNotifyPricePoolPerAssetRemoteLegIsReachable rcMdUpdateRestrictionRemoteLegIsReachable rcMdManagerCallFromHubRemoteLegIsReachable rcMdUpdateVaultRemoteLegIsReachable rcMdSetRequestManagerRemoteLegIsReachable rcMdAuthorizeSpokeCallRemoteLegIsReachable rcMdUnauthorizeSpokeCallRemoteLegIsReachable rcMdSetPolicyRemoteLegIsReachable rcMdUpdateManagerRemoteLegIsReachable rcMdScheduleUpgradeRemoteLegIsReachable rcMdCancelUpgradeRemoteLegIsReachable rcMdInitiateTransferSharesRemoteLegIsReachable rcMdExecuteTransferSharesRemoteLegIsReachable rcMdUpdateAssetsRemoteLegIsReachable rcMdUpdateHoldingAmountRemoteLegIsReachable rcMdUpdateSharesRemoteLegIsReachable rcMdRegisterAssetRemoteLegIsReachable rcMdRequestRemoteLegIsReachable rcMdManagerCallFromSpokeRemoteLegIsReachable rcMdRequestCallbackRemoteLegIsReachable rcMdSetPoolAdaptersRemoteLegIsReachable`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -707,7 +707,7 @@
     }
 
     function _send(uint16 centrifugeId, bytes memory message, bool unpaidMode, address refund) internal {
-        gateway.send{value: msg.value}(centrifugeId, message, unpaidMode, refund);
+        revert CannotBeSentLocally(); // MUTATION: nothing is ever handed to the gateway
     }
 
     function _refund(address refund) internal {
```

## MessageDispatcher #9781

The local refund step always reverts, so most messages addressed to the local chain can no longer be applied.

- **Mutant:** [`9781.sol`](9781.sol)
- **Caught by:** [`rcMdNotifyPoolLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L6) · [`rcMdNotifyShareClassLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L34) · [`rcMdNotifyShareMetadataLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L66) · [`rcMdNotifyPricePoolPerShareLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L94) · [`rcMdNotifyPricePoolPerAssetLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L126) · [`rcMdUpdateRestrictionLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L156) · [`rcMdUpdateVaultLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L215) · [`rcMdSetRequestManagerLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L247) · [`rcMdAuthorizeSpokeCallLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L275) · [`rcMdUnauthorizeSpokeCallLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L303) · [`rcMdSetPolicyLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L331) · [`rcMdUpdateManagerLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L359) · [`rcMdScheduleUpgradeLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L387) · [`rcMdCancelUpgradeLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L413) · [`rcMdExecuteTransferSharesLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L471) · [`rcMdUpdateAssetsLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L503) · [`rcMdUpdateHoldingAmountLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L533) · [`rcMdUpdateSharesLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L563) · [`rcMdRegisterAssetLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L593) · [`rcMdRequestLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L621) · [`rcMdManagerCallFromSpokeLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L649) · [`rcMdRequestCallbackLocalLegIsReachable`](../../specs/core/messaging/MessageDispatcher/single/MessageDispatcher_reachability.spec#L677)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9781`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageDispatcher/reachability.conf --rule rcMdNotifyPoolLocalLegIsReachable rcMdNotifyShareClassLocalLegIsReachable rcMdNotifyShareMetadataLocalLegIsReachable rcMdNotifyPricePoolPerShareLocalLegIsReachable rcMdNotifyPricePoolPerAssetLocalLegIsReachable rcMdUpdateRestrictionLocalLegIsReachable rcMdUpdateVaultLocalLegIsReachable rcMdSetRequestManagerLocalLegIsReachable rcMdAuthorizeSpokeCallLocalLegIsReachable rcMdUnauthorizeSpokeCallLocalLegIsReachable rcMdSetPolicyLocalLegIsReachable rcMdUpdateManagerLocalLegIsReachable rcMdScheduleUpgradeLocalLegIsReachable rcMdCancelUpgradeLocalLegIsReachable rcMdExecuteTransferSharesLocalLegIsReachable rcMdUpdateAssetsLocalLegIsReachable rcMdUpdateHoldingAmountLocalLegIsReachable rcMdUpdateSharesLocalLegIsReachable rcMdRegisterAssetLocalLegIsReachable rcMdRequestLocalLegIsReachable rcMdManagerCallFromSpokeLocalLegIsReachable rcMdRequestCallbackLocalLegIsReachable`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -711,7 +711,7 @@
     }
 
     function _refund(address refund) internal {
-        if (msg.value > 0) {
+        revert CannotBeSentLocally(); if (msg.value > 0) { // MUTATION: every refunding local leg reverts
             SafeTransferLib.safeTransferETH(refund, msg.value);
         }
     }
```

## MessageDispatcher #9920

A local share transfer initiation passes the hub handler a zero refund address instead of the caller's, so leftover fees are lost.

- **Mutant:** [`9920.sol`](9920.sol)
- **Caught by:** [`rcMpLocalAndRoundTripTransferInitiationHandDifferentRefunds`](../../specs/core/messaging/MessageProcessor/MessageProcessor_joint_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageDispatcher 9920`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/joint_properties.conf --rule rcMpLocalAndRoundTripTransferInitiationHandDifferentRefunds`

```diff
--- a/src/core/messaging/MessageDispatcher.sol
+++ b/src/core/messaging/MessageDispatcher.sol
@@ -440,7 +440,7 @@
                 receiver,
                 amount,
                 remoteExtraGasLimit,
-                refund
+                address(0) // MUTATION: the local transfer initiation drops the caller's refund address
             );
         } else {
             _send(
```

