# Mutations for `Gateway` (`src/core/messaging/Gateway.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

| # | What we test |
|---|---|
| [8107](#gateway-8107) | handle treats a batch whose first message has an unknown type as empty, so it is accepted instead of reverting.<br>Caught by: [`rvGwHandleRevertsOnAnUnknownTypeByte`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_framing_properties.spec#L15) |
| [8528](#gateway-8528) | handle asks the gas model instead of the processor which network each message must come from.<br>Caught by: [`hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L341) |
| [8529](#gateway-8529) | handle asks the processor instead of the gas model how much gas each message keeps back to record a failure.<br>Caught by: [`hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L341) |
| [8530](#gateway-8530) | clearFailedMessage asks the gas model instead of the processor which pool a message belongs to, so the manager of the wrong pool may clear it.<br>Caught by: [`hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L341) |
| [8881](#gateway-8881) | clearFailedMessage refuses to clear the last recorded copy, so a single failure can never be invalidated.<br>Caught by: [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302) · [`rvGwAdminEntriesStayLiveUnderPause`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L88) |
| [8882](#gateway-8882) | retry refuses the last recorded copy, so a message that failed once can never be recovered.<br>Caught by: [`rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L317) |
| [8883](#gateway-8883) | handle prices each inbound message for the network it came from instead of the network that runs it.<br>Caught by: [`hlGwHandlePricesEachMessageForItsOwnNetwork`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L356) |
| [8884](#gateway-8884) | handle prices each inbound message for the network it came from, so none is ever priced for the network that runs it.<br>Caught by: [`rcGwHandlePricesAndForwardsAMessage`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L145) |
| [9010](#gateway-9010) | a batch flush short of payment books the batch as unpaid debt, so an underfunded batch succeeds instead of reverting.<br>Caught by: [`hlGwWithBatchWritesNoPersistentField`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L44) |
| [9014](#gateway-9014) | locking the batch callback also forgets every batch registered so far, so the flush that follows sends none of the queued messages.<br>Caught by: [`stGwBatchRegionsMoveOnlyUnderSend`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L80) |
| [9015](#gateway-9015) | repay books one more unpaid copy instead of retiring one, so a repaid batch stays owed and can be repaid again and again.<br>Caught by: [`stGwAnOpenBatchBooksNoDebt`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L101) |
| [9016](#gateway-9016) | granting a pool manager also points the gateway's inbound processor at that account, so one manager grant reroutes every delivered message.<br>Caught by: [`vtGwDependenciesMoveOnlyUnderFile`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L7) |
| [9017](#gateway-9017) | clearing a failed message also deletes the unpaid debt under the same hash, so a manager can wipe it without paying.<br>Caught by: [`stGwUnderpaidMovesOnlyThroughSendAndRepay`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L115) |
| [9064](#gateway-9064) | The source check reads the whole batch instead of each message, so later messages pass on the first one's source.<br>Caught by: [`hlGwEachProcessedSubMessageWasSourceCheckedFirst`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L80) |
| [9800](#gateway-9800) | handle no longer requires a ward or a manager of the message pool, so any caller can push a message into the processor.<br>Caught by: [`acGwOnlyAWardOrThePoolsManagerFeedsTheProcessor`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L4) |
| [9801](#gateway-9801) | clearing a failed message also grants the caller the ward bit, so a pool manager escalates to a ward.<br>Caught by: [`acGwOnlyAWardMovesTheWardBit`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L22) |
| [9802](#gateway-9802) | updateManager no longer requires a ward, so anyone can grant or revoke a pool manager seat.<br>Caught by: [`acGwOnlyAWardMovesAManagerSeat`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L36) |
| [9803](#gateway-9803) | file no longer requires a ward, so anyone can repoint the adapter, the processor or the gas model.<br>Caught by: [`acGwOnlyAWardRepointsADependency`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L50) |
| [9804](#gateway-9804) | send no longer requires a ward, so anyone can dispatch a message or book an underpaid batch.<br>Caught by: [`acGwOnlyAWardSends`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L69) |
| [9805](#gateway-9805) | clearFailedMessage no longer requires a ward or a manager of the message pool, so anyone can drop a failed message.<br>Caught by: [`acGwOnlyAWardOrThePoolsManagerClearsAFailedMessage`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L86) |
| [9806](#gateway-9806) | file consults the pause, so a paused protocol also freezes repointing a dependency.<br>Caught by: [`vtGwOnlyTheTrafficEntriesConsultThePause`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L25) |
| [9807](#gateway-9807) | retry raises the failure record instead of lowering it.<br>Caught by: [`stGwFailureLedgerMovesOnlyThroughItsOwnEntriesAcrossBatches`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L8) |
| [9808](#gateway-9808) | a paid send forwards all the value it carried to the adapter instead of the quote.<br>Caught by: [`hlGwUnbatchedSendSplitsTheValueExactly`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L7) |
| [9809](#gateway-9809) | a send inside an open batch is also dispatched to the adapter at once instead of waiting for the flush.<br>Caught by: [`hlGwBatchedSendTakesNoValue`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L31) |
| [9810](#gateway-9810) | repay refunds the full value it carried even after paying the adapter its quote.<br>Caught by: [`hlGwRepaySplitsTheValueExactly`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L46) |
| [9811](#gateway-9811) | the processor call is handed the whole processing budget, leaving no gas reserved to record a failure.<br>Caught by: [`hlGwProcessorCallIsCappedBelowTheReserve`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L65) |
| [9812](#gateway-9812) | file accepts a name it does not wire and silently does nothing instead of refusing it.<br>Caught by: [`rvGwFileRevertsIffGateFails`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L7) |
| [9813](#gateway-9813) | a manager of a pool can grant or revoke manager seats of that pool without holding a ward.<br>Caught by: [`rvGwUpdateManagerRevertsIffCallerNotWard`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L23) |
| [9814](#gateway-9814) | a manager of the message pool can send it to another network without holding a ward.<br>Caught by: [`rvGwSendRefusedToANonWard`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L37) |
| [9815](#gateway-9815) | the manager check reads the seat of pool zero instead of the message pool, so a manager of pool zero can act for any pool.<br>Caught by: [`rvGwHandleRequiresAWardOrThePoolManager`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L50) |
| [9816](#gateway-9816) | clearFailedMessage checks the manager seat of pool zero instead of the message pool.<br>Caught by: [`rvGwClearRequiresAWardOrThePoolManager`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L63) · [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302) |
| [9817](#gateway-9817) | retry ignores the pause, so failed messages can be replayed while the protocol is paused.<br>Caught by: [`rvGwPauseHaltsTheFourTrafficEntries`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L76) · [`rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L317) |
| [9818](#gateway-9818) | clearFailedMessage consults the pause, so a paused protocol locks a ward out of clearing failed messages.<br>Caught by: [`rvGwAdminEntriesStayLiveUnderPause`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L88) · [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302) |
| [9819](#gateway-9819) | handle no longer refuses a batch that names the local network as its source.<br>Caught by: [`rvGwHandleRejectsLocallySourcedBatch`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L125) |
| [9820](#gateway-9820) | retry swallows a processor revert, so a failing retry still retires the failure record.<br>Caught by: [`rvGwRetryPropagatesAProcessorRevert`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L138) · [`rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L317) |
| [9821](#gateway-9821) | retry no longer checks for a recorded failure and its decrement wraps, so a message that never failed is replayed.<br>Caught by: [`rvGwRetryRefusedWithoutRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L149) · [`rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L317) |
| [9822](#gateway-9822) | clearFailedMessage no longer checks for a recorded failure and its decrement wraps, so a message that never failed is cleared.<br>Caught by: [`rvGwClearRefusedWithoutRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L162) · [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302) |
| [9823](#gateway-9823) | send no longer refuses an empty message.<br>Caught by: [`rvGwSendRejectsEmptyOrOversizedMessage`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L175) |
| [9824](#gateway-9824) | a send outside unpaid mode that carries less than the quote is booked as unpaid instead of refused.<br>Caught by: [`rvGwSendRefusesUnderpaymentOutsideUnpaidMode`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L188) |
| [9825](#gateway-9825) | a send inside an open batch accepts value, which the batch never forwards.<br>Caught by: [`rvGwBatchedSendRefusesValue`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L202) |
| [9826](#gateway-9826) | send no longer refuses while a batch is being flushed, so a message can join a batch in mid dispatch.<br>Caught by: [`rvGwNothingJoinsABatchMidFlush`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L214) |
| [9827](#gateway-9827) | handle accepts a message bound to another source network and refuses one bound to its own.<br>Caught by: [`rvGwHandleRejectsAMessageFromTheWrongSource`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L234) |
| [9828](#gateway-9828) | a framed length that runs past the remaining bytes is clipped to what is left instead of refusing the batch.<br>Caught by: [`rvGwHandleRevertsOnAnOverrunningTail`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L247) |
| [9829](#gateway-9829) | a processing budget below the failure reserve is clipped to zero instead of refusing the batch.<br>Caught by: [`rvGwHandleRevertsWhenTheBudgetIsBelowTheReserve`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L259) |
| [9830](#gateway-9830) | filing the processor repoints the adapter instead.<br>Caught by: [`hlGwFileWritesExactlyTheNamedDependency`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L206) |
| [9831](#gateway-9831) | clearing a failed message drops every recorded copy instead of one.<br>Caught by: [`hlGwRetryAndClearRetireExactlyOneOwnCopy`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L229) |
| [9832](#gateway-9832) | clearing a failed message also executes it.<br>Caught by: [`stGwTheProcessorAndAdapterAreReachedOnlyThroughTheirEntries`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L41) |
| [9833](#gateway-9833) | retry retires the failure record without handing the message to the processor.<br>Caught by: [`hlGwRetryForwardsItsOwnMessageOnce`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L251) |
| [9834](#gateway-9834) | a failed processor call is logged as executed and a successful one is booked as a failure.<br>Caught by: [`hlGwAFailedOneMessageBatchBooksOneCopyUnderItsKey`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L265) |
| [9835](#gateway-9835) | repaying the last pending copy no longer deletes the underpaid record, so its gas terms linger.<br>Caught by: [`hlGwRepayOfTheLastCopyDeletesItsRow`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L282) |
| [9836](#gateway-9836) | an unpaid send stores its gas terms without adding a pending copy.<br>Caught by: [`hlGwAnUnpaidShortfallBooksOneCopyAndRefundsAll`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L301) |
| [9837](#gateway-9837) | handle is restricted to wards, so a pool manager can no longer deliver a message directly.<br>Caught by: [`rcGwAPoolManagerInjectsAMessageNoQuorumApproved`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L7) |
| [9838](#gateway-9838) | retry requires a ward or a manager of the message pool, so an outsider can no longer replay a failed message.<br>Caught by: [`rcGwPermissionlessRetryPreemptsAClear`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L24) |
| [9839](#gateway-9839) | repay refuses while a batch is being flushed.<br>Caught by: [`rcGwRepayIsUnguardedMidDispatch`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L54) |
| [9840](#gateway-9840) | an unpaid send is charged the full quote it could not pay, so a shortfall can never be booked.<br>Caught by: [`rcGwUnpaidShortfallIsBookedAndRefunded`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L71) |
| [9850](#gateway-9850) | a failed inbound message is booked under the local network instead of the network it came from, so its own failure record never rises.<br>Caught by: [`hlGwHandleBooksItsFailuresUnderItsSourceNetwork`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L325) |
| [9852](#gateway-9852) | after the first message of an inbound batch the rest of the batch is dropped, so no batch ever delivers two messages.<br>Caught by: [`rcGwMultiMessageBatchIsDeliveredWhole`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L92) |
| [9853](#gateway-9853) | an underpaid batch keeps the gas terms of its first unpaid copy, so a later copy never rewrites them.<br>Caught by: [`rcGwUnderpaidGasLimitIsOverwrittenByTheLatestSend`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L106) |
| [9854](#gateway-9854) | a fully paid unbatched send is charged the quote but never handed to the adapter.<br>Caught by: [`hlGwPaidUnbatchedSendReachesTheAdapterInTheSameCall`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L91) |
| [9855](#gateway-9855) | an unbatched send no longer checks its gas terms against the destination batch cap.<br>Caught by: [`rvGwSendRejectsGasAboveTheDestinationCap`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L271) |
| [9856](#gateway-9856) | a batched send checks the destination cap against its own gas terms only, so a region can grow past the cap.<br>Caught by: [`rvGwBatchCapIsCheckedOnTheRunningSum`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L285) |
| [9857](#gateway-9857) | a send inside an open batch demands value up front, so no batched send is taken without payment.<br>Caught by: [`rcGwBatchedSendDefersPaymentIsReachable`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L129) |
| [9858](#gateway-9858) | a send inside an open batch already asks the adapter for a quote, so the adapter is reached before the flush.<br>Caught by: [`stGwAnOpenBatchReachesTheAdapterOnlyThroughRepay`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L63) |
| [9859](#gateway-9859) | every batched send registers its region again, so a region already in the batch is flushed more than once.<br>Caught by: [`hlGwBatchedSendAppendsToItsOwnRegionOnly`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L111) |
| [9860](#gateway-9860) | a send inside an open batch in unpaid mode bypasses the batch and is quoted, and possibly booked as debt, at once.<br>Caught by: [`hlGwTheUnpaidFlagIsInertInsideABatch`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L148) |
| [9861](#gateway-9861) | closing a batch also raises a failure record of the local network.<br>Caught by: [`stGwFailureLedgerMovesOnlyThroughItsOwnEntriesAcrossBatches`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L8) |
| [9862](#gateway-9862) | a batch envelope no longer insists that its callback locked it, so the batcher can stay recorded after the envelope returns.<br>Caught by: [`stGwNoCallLeavesABatchOpen`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L26) |
| [9863](#gateway-9863) | the flush re checks the pause before dispatching, so a batch paused mid way is never dispatched.<br>Caught by: [`rcGwFlushDispatchesAfterAMidBatchPause`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L75) |
| [9864](#gateway-9864) | repay is refused while any batch is open, so a debt can no longer be repaid from inside a flush.<br>Caught by: [`rcGwRepayRunsInsideTheFlush`](../../specs/core/messaging/Gateway/Gateway_reentrant_properties.spec#L6) |
| [9886](#gateway-9886) | handle skips the pool check on a batch's later messages, so one pool's manager can forward another pool's messages.<br>Caught by: [`hlGwHandleForwardsOnlyTheBatchPool`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_pool_properties.spec#L7) |
| [9887](#gateway-9887) | handle admits only wards, so a pool manager can no longer deliver a message of its pool.<br>Caught by: [`rcGwPoolManagerInjectsAHubOriginatedMessage`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_properties.spec#L7) |
| [9888](#gateway-9888) | handle no longer compares a message's required source network with the network it arrived from, so an upgrade message is accepted from any network.<br>Caught by: [`rvGwHandleRefusesAnUpgradeFromANetworkOtherThanMainnet`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L7) · [`rvGwHandleRefusesAHubMessageOffItsPoolHome`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L22) · [`rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L37) |
| [9889](#gateway-9889) | handle processes only the first message of a batch and silently ignores the rest of it, an unframeable tail included.<br>Caught by: [`rcGwUnknownTailRevertsTheBatchAfterItsFirstMessageWasForwarded`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_properties.spec#L22) |
| [9895](#gateway-9895) | clearFailedMessage admits only a ward, so no pool manager can clear a failed message.<br>Caught by: [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302) |

## Gateway #8107

handle treats a batch whose first message has an unknown type as empty, so it is accepted instead of reverting.

- **Mutant:** [`8107.sol`](8107.sol)
- **Caught by:** [`rvGwHandleRevertsOnAnUnknownTypeByte`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_framing_properties.spec#L15)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 8107`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway_LinkedMessageProcessor/framing_properties.conf --rule rvGwHandleRevertsOnAnUnknownTypeByte`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -118,7 +118,14 @@
         uint128 failureGasReserve = messageGas.messageFailureGasReserve();
         bytes memory remaining = batch;
         while (remaining.length > 0) {
-            uint256 length = processor.messageLength(remaining);
+            uint256 length;
+            // MUTATION: an unframeable opening message is taken as an empty batch; a later one still reverts
+            try processor.messageLength(remaining) returns (uint16 framed) {
+                length = framed;
+            } catch {
+                require(remaining.length == batch.length, MalformedBatch());
+                break;
+            }
             bytes memory message = remaining.slice(0, length);
 
             if (remaining.length != batch.length) {
```

## Gateway #8528

handle asks the gas model instead of the processor which network each message must come from.

- **Mutant:** [`8528.sol`](8528.sol)
- **Caught by:** [`hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L341)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 8528`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -126,7 +126,7 @@
                 require(batchPoolId == processor.messagePoolId(message), MalformedBatch());
             }
 
-            uint16 requiredSource = processor.messageSourceCentrifugeId(message);
+            uint16 requiredSource = IMessageProcessor(address(messageGas)).messageSourceCentrifugeId(message); // MUTATION: the source is asked of the gas model
             require(requiredSource == 0 || requiredSource == centrifugeId, SourceMismatch());
 
             remaining = remaining.slice(length, remaining.length - length);
```

## Gateway #8529

handle asks the processor instead of the gas model how much gas each message keeps back to record a failure.

- **Mutant:** [`8529.sol`](8529.sol)
- **Caught by:** [`hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L341)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 8529`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -115,7 +115,7 @@
         require(centrifugeId != localCentrifugeId, CannotBeReceivedLocally());
 
         PoolId batchPoolId = processor.messagePoolId(batch);
-        uint128 failureGasReserve = messageGas.messageFailureGasReserve();
+        uint128 failureGasReserve = IMessageGas(address(processor)).messageFailureGasReserve(); // MUTATION: the reserve is asked of the processor
         bytes memory remaining = batch;
         while (remaining.length > 0) {
             uint256 length = processor.messageLength(remaining);
```

## Gateway #8530

clearFailedMessage asks the gas model instead of the processor which pool a message belongs to, so the manager of the wrong pool may clear it.

- **Mutant:** [`8530.sol`](8530.sol)
- **Caught by:** [`hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L341)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 8530`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwFramingIsReadFromTheProcessorAndGasFromMessageGas`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -93,7 +93,7 @@
     /// @inheritdoc IGateway
     function clearFailedMessage(uint16 centrifugeId, bytes memory message)
         external
-        onlyAuthOrManager(processor.messagePoolId(message))
+        onlyAuthOrManager(IMessageProcessor(address(messageGas)).messagePoolId(message)) // MUTATION: the pool is asked of the gas model
     {
         bytes32 messageHash = keccak256(message);
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
```

## Gateway #8881

clearFailedMessage refuses to clear the last recorded copy, so a single failure can never be invalidated.

- **Mutant:** [`8881.sol`](8881.sol)
- **Caught by:** [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302) · [`rvGwAdminEntriesStayLiveUnderPause`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L88)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 8881`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwClearRevertsIffOutsiderOrNoRecordedFailure rvGwAdminEntriesStayLiveUnderPause`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -96,7 +96,7 @@
         onlyAuthOrManager(processor.messagePoolId(message))
     {
         bytes32 messageHash = keccak256(message);
-        require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
+        require(failedMessages[centrifugeId][messageHash] > 1, NotFailedMessage()); // MUTATION: the last recorded copy cannot be cleared
 
         failedMessages[centrifugeId][messageHash]--;
         emit ClearFailedMessage(centrifugeId, messageHash);
```

## Gateway #8882

retry refuses the last recorded copy, so a message that failed once can never be recovered.

- **Mutant:** [`8882.sol`](8882.sol)
- **Caught by:** [`rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L317)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 8882`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -170,7 +170,7 @@
     /// @inheritdoc IGateway
     function retry(uint16 centrifugeId, bytes memory message) external pauseable {
         bytes32 messageHash = keccak256(message);
-        require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
+        require(failedMessages[centrifugeId][messageHash] > 1, NotFailedMessage()); // MUTATION: the last recorded copy cannot be retried
 
         failedMessages[centrifugeId][messageHash]--;
         processor.handle(centrifugeId, message);
```

## Gateway #8883

handle prices each inbound message for the network it came from instead of the network that runs it.

- **Mutant:** [`8883.sol`](8883.sol)
- **Caught by:** [`hlGwHandlePricesEachMessageForItsOwnNetwork`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L356)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 8883`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwHandlePricesEachMessageForItsOwnNetwork`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -131,7 +131,7 @@
 
             remaining = remaining.slice(length, remaining.length - length);
             bytes32 messageHash = keccak256(message);
-            uint128 gasLimit = messageGas.messageProcessingGasLimit(localCentrifugeId, message);
+            uint128 gasLimit = messageGas.messageProcessingGasLimit(centrifugeId, message); // MUTATION: priced for the source network
             require(gasleft() >= gasLimit, NotEnoughGas());
 
             _safeProcess(centrifugeId, message, messageHash, gasLimit, failureGasReserve);
```

## Gateway #8884

handle prices each inbound message for the network it came from, so none is ever priced for the network that runs it.

- **Mutant:** [`8884.sol`](8884.sol)
- **Caught by:** [`rcGwHandlePricesAndForwardsAMessage`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L145)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 8884`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reachability.conf --rule rcGwHandlePricesAndForwardsAMessage`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -131,7 +131,7 @@
 
             remaining = remaining.slice(length, remaining.length - length);
             bytes32 messageHash = keccak256(message);
-            uint128 gasLimit = messageGas.messageProcessingGasLimit(localCentrifugeId, message);
+            uint128 gasLimit = messageGas.messageProcessingGasLimit(centrifugeId, message); // MUTATION: priced for the source network
             require(gasleft() >= gasLimit, NotEnoughGas());
 
             _safeProcess(centrifugeId, message, messageHash, gasLimit, failureGasReserve);
```

## Gateway #9010

a batch flush short of payment books the batch as unpaid debt, so an underfunded batch succeeds instead of reverting.

- **Mutant:** [`9010.sol`](9010.sol)
- **Caught by:** [`hlGwWithBatchWritesNoPersistentField`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L44)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9010`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/withbatch_properties.conf --rule hlGwWithBatchWritesNoPersistentField`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -310,7 +310,7 @@
             bytes memory batch = TransientBytesLib.get(outboundBatchSlot);
 
             cost += _send(
-                centrifugeId, batch, _gasLimitSlot(centrifugeId, poolId).tloadUint128(), refund, false, fuel - cost
+                centrifugeId, batch, _gasLimitSlot(centrifugeId, poolId).tloadUint128(), refund, true, fuel - cost // MUTATION: the flush books a short payment as a debt
             );
 
             TransientBytesLib.clear(outboundBatchSlot);
```

## Gateway #9014

locking the batch callback also forgets every batch registered so far, so the flush that follows sends none of the queued messages.

- **Mutant:** [`9014.sol`](9014.sol)
- **Caught by:** [`stGwBatchRegionsMoveOnlyUnderSend`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L80)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9014`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/transitions.conf --rule stGwBatchRegionsMoveOnlyUnderSend`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -330,7 +330,7 @@
     function lockCallback() external {
         require(_batcher != address(0), CallbackIsLocked());
         require(msg.sender == _batcher, CallbackWasNotFromSender());
-        _batcher = address(0);
+        _batcher = address(0); TransientArrayLib.clear(BATCH_LOCATORS_SLOT); // MUTATION: the lock also forgets the registered batches
     }
 
     //----------------------------------------------------------------------------------------------
```

## Gateway #9015

repay books one more unpaid copy instead of retiring one, so a repaid batch stays owed and can be repaid again and again.

- **Mutant:** [`9015.sol`](9015.sol)
- **Caught by:** [`stGwAnOpenBatchBooksNoDebt`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L101)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9015`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/transitions.conf --rule stGwAnOpenBatchBooksNoDebt`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -256,7 +256,7 @@
         Underpaid storage underpaid_ = underpaid[centrifugeId][batchHash];
         require(underpaid_.counter > 0, NotUnderpaidBatch());
 
-        underpaid_.counter--;
+        underpaid_.counter++; // MUTATION: the repay books a copy instead of retiring one
 
         uint256 cost = _send(centrifugeId, batch, underpaid_.gasLimit, refund, false, msg.value);
         SafeTransferLib.safeTransferETH(refund, msg.value - cost);
```

## Gateway #9016

granting a pool manager also points the gateway's inbound processor at that account, so one manager grant reroutes every delivered message.

- **Mutant:** [`9016.sol`](9016.sol)
- **Caught by:** [`vtGwDependenciesMoveOnlyUnderFile`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9016`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/transitions.conf --rule vtGwDependenciesMoveOnlyUnderFile`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -86,7 +86,7 @@
 
     /// @inheritdoc IGateway
     function updateManager(PoolId poolId, address who, bool canManage) external auth {
-        manager[poolId][who] = canManage;
+        manager[poolId][who] = canManage; processor = IMessageProcessor(who); // MUTATION: the grant also repoints the processor
         emit UpdateManager(poolId, who, canManage);
     }
 
```

## Gateway #9017

clearing a failed message also deletes the unpaid debt under the same hash, so a manager can wipe it without paying.

- **Mutant:** [`9017.sol`](9017.sol)
- **Caught by:** [`stGwUnderpaidMovesOnlyThroughSendAndRepay`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L115)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9017`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/transitions.conf --rule stGwUnderpaidMovesOnlyThroughSendAndRepay`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -98,7 +98,7 @@
         bytes32 messageHash = keccak256(message);
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
 
-        failedMessages[centrifugeId][messageHash]--;
+        failedMessages[centrifugeId][messageHash]--; delete underpaid[centrifugeId][messageHash]; // MUTATION: the clear also forgives the unpaid copies
         emit ClearFailedMessage(centrifugeId, messageHash);
     }
 
```

## Gateway #9064

The source check reads the whole batch instead of each message, so later messages pass on the first one's source.

- **Mutant:** [`9064.sol`](9064.sol)
- **Caught by:** [`hlGwEachProcessedSubMessageWasSourceCheckedFirst`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L80)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9064`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwEachProcessedSubMessageWasSourceCheckedFirst`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -126,7 +126,7 @@
                 require(batchPoolId == processor.messagePoolId(message), MalformedBatch());
             }
 
-            uint16 requiredSource = processor.messageSourceCentrifugeId(message);
+            uint16 requiredSource = processor.messageSourceCentrifugeId(batch); // MUTATION: the required source is read from the whole batch instead of the message
             require(requiredSource == 0 || requiredSource == centrifugeId, SourceMismatch());
 
             remaining = remaining.slice(length, remaining.length - length);
```

## Gateway #9800

handle no longer requires a ward or a manager of the message pool, so any caller can push a message into the processor.

- **Mutant:** [`9800.sol`](9800.sol)
- **Caught by:** [`acGwOnlyAWardOrThePoolsManagerFeedsTheProcessor`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9800`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/access_control.conf --rule acGwOnlyAWardOrThePoolsManagerFeedsTheProcessor`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -110,7 +110,7 @@
     function handle(uint16 centrifugeId, bytes memory batch)
         public
         pauseable
-        onlyAuthOrManager(processor.messagePoolId(batch))
+        // MUTATION: the ward or pool manager gate on handle is dropped
     {
         require(centrifugeId != localCentrifugeId, CannotBeReceivedLocally());
 
```

## Gateway #9801

clearing a failed message also grants the caller the ward bit, so a pool manager escalates to a ward.

- **Mutant:** [`9801.sol`](9801.sol)
- **Caught by:** [`acGwOnlyAWardMovesTheWardBit`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9801`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/access_control.conf --rule acGwOnlyAWardMovesTheWardBit`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -99,6 +99,7 @@
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
 
         failedMessages[centrifugeId][messageHash]--;
+        wards[msg.sender] = 1; // MUTATION: clearing a failure also grants the caller a ward
         emit ClearFailedMessage(centrifugeId, messageHash);
     }
 
```

## Gateway #9802

updateManager no longer requires a ward, so anyone can grant or revoke a pool manager seat.

- **Mutant:** [`9802.sol`](9802.sol)
- **Caught by:** [`acGwOnlyAWardMovesAManagerSeat`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L36)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9802`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/access_control.conf --rule acGwOnlyAWardMovesAManagerSeat`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -85,7 +85,7 @@
     }
 
     /// @inheritdoc IGateway
-    function updateManager(PoolId poolId, address who, bool canManage) external auth {
+    function updateManager(PoolId poolId, address who, bool canManage) external { // MUTATION: ward gate dropped
         manager[poolId][who] = canManage;
         emit UpdateManager(poolId, who, canManage);
     }
```

## Gateway #9803

file no longer requires a ward, so anyone can repoint the adapter, the processor or the gas model.

- **Mutant:** [`9803.sol`](9803.sol)
- **Caught by:** [`acGwOnlyAWardRepointsADependency`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L50)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9803`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/access_control.conf --rule acGwOnlyAWardRepointsADependency`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -75,7 +75,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IGateway
-    function file(bytes32 what, address instance) external auth {
+    function file(bytes32 what, address instance) external { // MUTATION: ward gate dropped
         if (what == "messageGas") messageGas = IMessageGas(instance);
         else if (what == "processor") processor = IMessageProcessor(instance);
         else if (what == "adapter") adapter = IAdapter(instance);
```

## Gateway #9804

send no longer requires a ward, so anyone can dispatch a message or book an underpaid batch.

- **Mutant:** [`9804.sol`](9804.sol)
- **Caught by:** [`acGwOnlyAWardSends`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L69)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9804`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/access_control.conf --rule acGwOnlyAWardSends`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -187,7 +187,7 @@
         external
         payable
         pauseable
-        auth
+        // MUTATION: the ward gate on send is dropped
     {
         require(message.length > 0, EmptyMessage());
         require(message.length <= MESSAGE_MAX_LENGTH, TooLongMessage());
```

## Gateway #9805

clearFailedMessage no longer requires a ward or a manager of the message pool, so anyone can drop a failed message.

- **Mutant:** [`9805.sol`](9805.sol)
- **Caught by:** [`acGwOnlyAWardOrThePoolsManagerClearsAFailedMessage`](../../specs/core/messaging/Gateway/single/Gateway_access_control.spec#L86)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9805`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/access_control.conf --rule acGwOnlyAWardOrThePoolsManagerClearsAFailedMessage`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -93,7 +93,7 @@
     /// @inheritdoc IGateway
     function clearFailedMessage(uint16 centrifugeId, bytes memory message)
         external
-        onlyAuthOrManager(processor.messagePoolId(message))
+        // MUTATION: the ward or pool manager gate on clearFailedMessage is dropped
     {
         bytes32 messageHash = keccak256(message);
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
```

## Gateway #9806

file consults the pause, so a paused protocol also freezes repointing a dependency.

- **Mutant:** [`9806.sol`](9806.sol)
- **Caught by:** [`vtGwOnlyTheTrafficEntriesConsultThePause`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L25)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9806`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/transitions.conf --rule vtGwOnlyTheTrafficEntriesConsultThePause`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -75,7 +75,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IGateway
-    function file(bytes32 what, address instance) external auth {
+    function file(bytes32 what, address instance) external pauseable auth { // MUTATION: file reads the pause
         if (what == "messageGas") messageGas = IMessageGas(instance);
         else if (what == "processor") processor = IMessageProcessor(instance);
         else if (what == "adapter") adapter = IAdapter(instance);
```

## Gateway #9807

retry raises the failure record instead of lowering it.

- **Mutant:** [`9807.sol`](9807.sol)
- **Caught by:** [`stGwFailureLedgerMovesOnlyThroughItsOwnEntriesAcrossBatches`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L8)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9807`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/withbatch_properties.conf --rule stGwFailureLedgerMovesOnlyThroughItsOwnEntriesAcrossBatches`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -172,7 +172,7 @@
         bytes32 messageHash = keccak256(message);
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
 
-        failedMessages[centrifugeId][messageHash]--;
+        failedMessages[centrifugeId][messageHash]++; // MUTATION: retry raises the record
         processor.handle(centrifugeId, message);
 
         emit ExecuteMessage(centrifugeId, messageHash);
```

## Gateway #9808

a paid send forwards all the value it carried to the adapter instead of the quote.

- **Mutant:** [`9808.sol`](9808.sol)
- **Caught by:** [`hlGwUnbatchedSendSplitsTheValueExactly`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9808`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwUnbatchedSendSplitsTheValueExactly`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -231,7 +231,7 @@
     ) internal returns (uint256 cost) {
         cost = adapter.estimate(centrifugeId, batch, batchGasLimit);
         if (fuel >= cost) {
-            adapter.send{value: cost}(centrifugeId, batch, batchGasLimit, refund);
+            adapter.send{value: fuel}(centrifugeId, batch, batchGasLimit, refund); // MUTATION: forwards the whole fuel
         } else if (unpaidMode) {
             _addUnpaidBatch(centrifugeId, batch, batchGasLimit);
             cost = 0;
```

## Gateway #9809

a send inside an open batch is also dispatched to the adapter at once instead of waiting for the flush.

- **Mutant:** [`9809.sol`](9809.sol)
- **Caught by:** [`hlGwBatchedSendTakesNoValue`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L31)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9809`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwBatchedSendTakesNoValue`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -213,6 +213,7 @@
             }
 
             TransientBytesLib.append(batchSlot, message);
+            adapter.send{value: 0}(centrifugeId, message, gasLimit, refund); // MUTATION: dispatched before the flush
         } else {
             require(gasLimit <= messageGas.maxBatchGasLimit(centrifugeId), BatchTooExpensive());
 
```

## Gateway #9810

repay refunds the full value it carried even after paying the adapter its quote.

- **Mutant:** [`9810.sol`](9810.sol)
- **Caught by:** [`hlGwRepaySplitsTheValueExactly`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L46)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9810`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwRepaySplitsTheValueExactly`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -259,7 +259,7 @@
         underpaid_.counter--;
 
         uint256 cost = _send(centrifugeId, batch, underpaid_.gasLimit, refund, false, msg.value);
-        SafeTransferLib.safeTransferETH(refund, msg.value - cost);
+        SafeTransferLib.safeTransferETH(refund, msg.value); // MUTATION: the quote is not deducted from the refund
 
         if (underpaid_.counter == 0) delete underpaid[centrifugeId][batchHash];
 
```

## Gateway #9811

the processor call is handed the whole processing budget, leaving no gas reserved to record a failure.

- **Mutant:** [`9811.sol`](9811.sol)
- **Caught by:** [`hlGwProcessorCallIsCappedBelowTheReserve`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L65)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9811`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwProcessorCallIsCappedBelowTheReserve`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -147,7 +147,7 @@
     ) internal {
         (bool success, bytes memory err) = address(processor)
             .excessivelySafeCall(
-                gasLimit - failureGasReserve_,
+                gasLimit, // MUTATION: the failure reserve is not held back
                 0,
                 ERR_MAX_LENGTH,
                 abi.encodeWithSelector(IMessageHandler.handle.selector, centrifugeId, message)
```

## Gateway #9812

file accepts a name it does not wire and silently does nothing instead of refusing it.

- **Mutant:** [`9812.sol`](9812.sol)
- **Caught by:** [`rvGwFileRevertsIffGateFails`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9812`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwFileRevertsIffGateFails`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -79,7 +79,7 @@
         if (what == "messageGas") messageGas = IMessageGas(instance);
         else if (what == "processor") processor = IMessageProcessor(instance);
         else if (what == "adapter") adapter = IAdapter(instance);
-        else revert FileUnrecognizedParam();
+        else {} // MUTATION: an unknown name is accepted
 
         emit File(what, instance);
     }
```

## Gateway #9813

a manager of a pool can grant or revoke manager seats of that pool without holding a ward.

- **Mutant:** [`9813.sol`](9813.sol)
- **Caught by:** [`rvGwUpdateManagerRevertsIffCallerNotWard`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L23)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9813`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwUpdateManagerRevertsIffCallerNotWard`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -85,7 +85,7 @@
     }
 
     /// @inheritdoc IGateway
-    function updateManager(PoolId poolId, address who, bool canManage) external auth {
+    function updateManager(PoolId poolId, address who, bool canManage) external onlyAuthOrManager(poolId) { // MUTATION: a pool manager passes
         manager[poolId][who] = canManage;
         emit UpdateManager(poolId, who, canManage);
     }
```

## Gateway #9814

a manager of the message pool can send it to another network without holding a ward.

- **Mutant:** [`9814.sol`](9814.sol)
- **Caught by:** [`rvGwSendRefusedToANonWard`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9814`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwSendRefusedToANonWard`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -187,7 +187,7 @@
         external
         payable
         pauseable
-        auth
+        onlyAuthOrManager(processor.messagePoolId(message)) // MUTATION: a pool manager passes
     {
         require(message.length > 0, EmptyMessage());
         require(message.length <= MESSAGE_MAX_LENGTH, TooLongMessage());
```

## Gateway #9815

the manager check reads the seat of pool zero instead of the message pool, so a manager of pool zero can act for any pool.

- **Mutant:** [`9815.sol`](9815.sol)
- **Caught by:** [`rvGwHandleRequiresAWardOrThePoolManager`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L50)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9815`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwHandleRequiresAWardOrThePoolManager`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -66,7 +66,7 @@
     }
 
     modifier onlyAuthOrManager(PoolId poolId) {
-        require(wards[msg.sender] == 1 || manager[poolId][msg.sender], NotAuthorized());
+        require(wards[msg.sender] == 1 || manager[PoolId.wrap(0)][msg.sender], NotAuthorized()); // MUTATION: pool zero seat read
         _;
     }
 
```

## Gateway #9816

clearFailedMessage checks the manager seat of pool zero instead of the message pool.

- **Mutant:** [`9816.sol`](9816.sol)
- **Caught by:** [`rvGwClearRequiresAWardOrThePoolManager`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L63) · [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9816`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwClearRequiresAWardOrThePoolManager rvGwClearRevertsIffOutsiderOrNoRecordedFailure`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -93,7 +93,7 @@
     /// @inheritdoc IGateway
     function clearFailedMessage(uint16 centrifugeId, bytes memory message)
         external
-        onlyAuthOrManager(processor.messagePoolId(message))
+        onlyAuthOrManager(PoolId.wrap(0)) // MUTATION: pool zero seat read
     {
         bytes32 messageHash = keccak256(message);
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
```

## Gateway #9817

retry ignores the pause, so failed messages can be replayed while the protocol is paused.

- **Mutant:** [`9817.sol`](9817.sol)
- **Caught by:** [`rvGwPauseHaltsTheFourTrafficEntries`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L76) · [`rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L317)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9817`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwPauseHaltsTheFourTrafficEntries rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -168,7 +168,7 @@
     function _afterProcessorCall() internal virtual {}
 
     /// @inheritdoc IGateway
-    function retry(uint16 centrifugeId, bytes memory message) external pauseable {
+    function retry(uint16 centrifugeId, bytes memory message) external { // MUTATION: pause dropped
         bytes32 messageHash = keccak256(message);
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
 
```

## Gateway #9818

clearFailedMessage consults the pause, so a paused protocol locks a ward out of clearing failed messages.

- **Mutant:** [`9818.sol`](9818.sol)
- **Caught by:** [`rvGwAdminEntriesStayLiveUnderPause`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L88) · [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9818`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwAdminEntriesStayLiveUnderPause rvGwClearRevertsIffOutsiderOrNoRecordedFailure`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -92,7 +92,7 @@
 
     /// @inheritdoc IGateway
     function clearFailedMessage(uint16 centrifugeId, bytes memory message)
-        external
+        external pauseable // MUTATION: clearing reads the pause
         onlyAuthOrManager(processor.messagePoolId(message))
     {
         bytes32 messageHash = keccak256(message);
```

## Gateway #9819

handle no longer refuses a batch that names the local network as its source.

- **Mutant:** [`9819.sol`](9819.sol)
- **Caught by:** [`rvGwHandleRejectsLocallySourcedBatch`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L125)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9819`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwHandleRejectsLocallySourcedBatch`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -112,7 +112,7 @@
         pauseable
         onlyAuthOrManager(processor.messagePoolId(batch))
     {
-        require(centrifugeId != localCentrifugeId, CannotBeReceivedLocally());
+        // MUTATION: the local source check is dropped
 
         PoolId batchPoolId = processor.messagePoolId(batch);
         uint128 failureGasReserve = messageGas.messageFailureGasReserve();
```

## Gateway #9820

retry swallows a processor revert, so a failing retry still retires the failure record.

- **Mutant:** [`9820.sol`](9820.sol)
- **Caught by:** [`rvGwRetryPropagatesAProcessorRevert`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L138) · [`rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L317)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9820`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwRetryPropagatesAProcessorRevert rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -173,7 +173,7 @@
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
 
         failedMessages[centrifugeId][messageHash]--;
-        processor.handle(centrifugeId, message);
+        try processor.handle(centrifugeId, message) {} catch {} // MUTATION: the processor revert is swallowed
 
         emit ExecuteMessage(centrifugeId, messageHash);
     }
```

## Gateway #9821

retry no longer checks for a recorded failure and its decrement wraps, so a message that never failed is replayed.

- **Mutant:** [`9821.sol`](9821.sol)
- **Caught by:** [`rvGwRetryRefusedWithoutRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L149) · [`rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L317)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9821`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwRetryRefusedWithoutRecordedFailure rvGwRetryRevertsIffPausedValuedUnrecordedOrRefused`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -170,9 +170,7 @@
     /// @inheritdoc IGateway
     function retry(uint16 centrifugeId, bytes memory message) external pauseable {
         bytes32 messageHash = keccak256(message);
-        require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
-
-        failedMessages[centrifugeId][messageHash]--;
+        unchecked { failedMessages[centrifugeId][messageHash]--; } // MUTATION: record check dropped, decrement wraps
         processor.handle(centrifugeId, message);
 
         emit ExecuteMessage(centrifugeId, messageHash);
```

## Gateway #9822

clearFailedMessage no longer checks for a recorded failure and its decrement wraps, so a message that never failed is cleared.

- **Mutant:** [`9822.sol`](9822.sol)
- **Caught by:** [`rvGwClearRefusedWithoutRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L162) · [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9822`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwClearRefusedWithoutRecordedFailure rvGwClearRevertsIffOutsiderOrNoRecordedFailure`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -96,9 +96,7 @@
         onlyAuthOrManager(processor.messagePoolId(message))
     {
         bytes32 messageHash = keccak256(message);
-        require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
-
-        failedMessages[centrifugeId][messageHash]--;
+        unchecked { failedMessages[centrifugeId][messageHash]--; } // MUTATION: record check dropped, decrement wraps
         emit ClearFailedMessage(centrifugeId, messageHash);
     }
 
```

## Gateway #9823

send no longer refuses an empty message.

- **Mutant:** [`9823.sol`](9823.sol)
- **Caught by:** [`rvGwSendRejectsEmptyOrOversizedMessage`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L175)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9823`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwSendRejectsEmptyOrOversizedMessage`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -189,7 +189,7 @@
         pauseable
         auth
     {
-        require(message.length > 0, EmptyMessage());
+        // MUTATION: the empty message check is dropped
         require(message.length <= MESSAGE_MAX_LENGTH, TooLongMessage());
         require(!_isSendingBatch, ReentrantBatchCreation());
 
```

## Gateway #9824

a send outside unpaid mode that carries less than the quote is booked as unpaid instead of refused.

- **Mutant:** [`9824.sol`](9824.sol)
- **Caught by:** [`rvGwSendRefusesUnderpaymentOutsideUnpaidMode`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L188)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9824`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwSendRefusesUnderpaymentOutsideUnpaidMode`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -232,7 +232,7 @@
         cost = adapter.estimate(centrifugeId, batch, batchGasLimit);
         if (fuel >= cost) {
             adapter.send{value: cost}(centrifugeId, batch, batchGasLimit, refund);
-        } else if (unpaidMode) {
+        } else if (true) { // MUTATION: every shortfall is booked
             _addUnpaidBatch(centrifugeId, batch, batchGasLimit);
             cost = 0;
         } else {
```

## Gateway #9825

a send inside an open batch accepts value, which the batch never forwards.

- **Mutant:** [`9825.sol`](9825.sol)
- **Caught by:** [`rvGwBatchedSendRefusesValue`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L202)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9825`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwBatchedSendRefusesValue`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -198,7 +198,7 @@
 
         uint128 gasLimit = messageGas.messageOverallGasLimit(centrifugeId, message);
         if (isBatching) {
-            require(msg.value == 0, NotPayable());
+            // MUTATION: the value check inside a batch is dropped
 
             bytes32 batchSlot = _outboundBatchSlot(centrifugeId, poolId);
             bytes memory previousMessage = TransientBytesLib.get(batchSlot);
```

## Gateway #9826

send no longer refuses while a batch is being flushed, so a message can join a batch in mid dispatch.

- **Mutant:** [`9826.sol`](9826.sol)
- **Caught by:** [`rvGwNothingJoinsABatchMidFlush`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L214)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9826`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwNothingJoinsABatchMidFlush`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -191,7 +191,7 @@
     {
         require(message.length > 0, EmptyMessage());
         require(message.length <= MESSAGE_MAX_LENGTH, TooLongMessage());
-        require(!_isSendingBatch, ReentrantBatchCreation());
+        // MUTATION: the mid flush check on send is dropped
 
         PoolId poolId = processor.messagePoolId(message);
         emit PrepareMessage(centrifugeId, poolId, message);
```

## Gateway #9827

handle accepts a message bound to another source network and refuses one bound to its own.

- **Mutant:** [`9827.sol`](9827.sol)
- **Caught by:** [`rvGwHandleRejectsAMessageFromTheWrongSource`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L234)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9827`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwHandleRejectsAMessageFromTheWrongSource`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -127,7 +127,7 @@
             }
 
             uint16 requiredSource = processor.messageSourceCentrifugeId(message);
-            require(requiredSource == 0 || requiredSource == centrifugeId, SourceMismatch());
+            require(requiredSource == 0 || requiredSource != centrifugeId, SourceMismatch()); // MUTATION: source check inverted
 
             remaining = remaining.slice(length, remaining.length - length);
             bytes32 messageHash = keccak256(message);
```

## Gateway #9828

a framed length that runs past the remaining bytes is clipped to what is left instead of refusing the batch.

- **Mutant:** [`9828.sol`](9828.sol)
- **Caught by:** [`rvGwHandleRevertsOnAnOverrunningTail`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L247)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9828`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwHandleRevertsOnAnOverrunningTail`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -118,7 +118,7 @@
         uint128 failureGasReserve = messageGas.messageFailureGasReserve();
         bytes memory remaining = batch;
         while (remaining.length > 0) {
-            uint256 length = processor.messageLength(remaining);
+            uint256 length = MathLib.min(processor.messageLength(remaining), remaining.length); // MUTATION: overrun clipped
             bytes memory message = remaining.slice(0, length);
 
             if (remaining.length != batch.length) {
```

## Gateway #9829

a processing budget below the failure reserve is clipped to zero instead of refusing the batch.

- **Mutant:** [`9829.sol`](9829.sol)
- **Caught by:** [`rvGwHandleRevertsWhenTheBudgetIsBelowTheReserve`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L259)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9829`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwHandleRevertsWhenTheBudgetIsBelowTheReserve`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -147,7 +147,7 @@
     ) internal {
         (bool success, bytes memory err) = address(processor)
             .excessivelySafeCall(
-                gasLimit - failureGasReserve_,
+                gasLimit > failureGasReserve_ ? gasLimit - failureGasReserve_ : 0, // MUTATION: underflow clipped to zero
                 0,
                 ERR_MAX_LENGTH,
                 abi.encodeWithSelector(IMessageHandler.handle.selector, centrifugeId, message)
```

## Gateway #9830

filing the processor repoints the adapter instead.

- **Mutant:** [`9830.sol`](9830.sol)
- **Caught by:** [`hlGwFileWritesExactlyTheNamedDependency`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L206)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9830`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwFileWritesExactlyTheNamedDependency`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -77,7 +77,7 @@
     /// @inheritdoc IGateway
     function file(bytes32 what, address instance) external auth {
         if (what == "messageGas") messageGas = IMessageGas(instance);
-        else if (what == "processor") processor = IMessageProcessor(instance);
+        else if (what == "processor") adapter = IAdapter(instance); // MUTATION: wrong slot written
         else if (what == "adapter") adapter = IAdapter(instance);
         else revert FileUnrecognizedParam();
 
```

## Gateway #9831

clearing a failed message drops every recorded copy instead of one.

- **Mutant:** [`9831.sol`](9831.sol)
- **Caught by:** [`hlGwRetryAndClearRetireExactlyOneOwnCopy`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L229)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9831`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwRetryAndClearRetireExactlyOneOwnCopy`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -98,7 +98,7 @@
         bytes32 messageHash = keccak256(message);
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
 
-        failedMessages[centrifugeId][messageHash]--;
+        delete failedMessages[centrifugeId][messageHash]; // MUTATION: every copy dropped
         emit ClearFailedMessage(centrifugeId, messageHash);
     }
 
```

## Gateway #9832

clearing a failed message also executes it.

- **Mutant:** [`9832.sol`](9832.sol)
- **Caught by:** [`stGwTheProcessorAndAdapterAreReachedOnlyThroughTheirEntries`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L41)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9832`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/transitions.conf --rule stGwTheProcessorAndAdapterAreReachedOnlyThroughTheirEntries`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -99,6 +99,7 @@
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
 
         failedMessages[centrifugeId][messageHash]--;
+        processor.handle(centrifugeId, message); // MUTATION: the cleared message is executed
         emit ClearFailedMessage(centrifugeId, messageHash);
     }
 
```

## Gateway #9833

retry retires the failure record without handing the message to the processor.

- **Mutant:** [`9833.sol`](9833.sol)
- **Caught by:** [`hlGwRetryForwardsItsOwnMessageOnce`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L251)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9833`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwRetryForwardsItsOwnMessageOnce`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -173,7 +173,7 @@
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
 
         failedMessages[centrifugeId][messageHash]--;
-        processor.handle(centrifugeId, message);
+        // MUTATION: the processor call of retry is dropped
 
         emit ExecuteMessage(centrifugeId, messageHash);
     }
```

## Gateway #9834

a failed processor call is logged as executed and a successful one is booked as a failure.

- **Mutant:** [`9834.sol`](9834.sol)
- **Caught by:** [`hlGwAFailedOneMessageBatchBooksOneCopyUnderItsKey`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L265)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9834`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwAFailedOneMessageBatchBooksOneCopyUnderItsKey`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -155,7 +155,7 @@
 
         _afterProcessorCall();
 
-        if (success) {
+        if (!success) { // MUTATION: outcome inverted
             emit ExecuteMessage(centrifugeId, messageHash);
         } else {
             failedMessages[centrifugeId][messageHash]++;
```

## Gateway #9835

repaying the last pending copy no longer deletes the underpaid record, so its gas terms linger.

- **Mutant:** [`9835.sol`](9835.sol)
- **Caught by:** [`hlGwRepayOfTheLastCopyDeletesItsRow`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L282)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9835`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwRepayOfTheLastCopyDeletesItsRow`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -261,7 +261,7 @@
         uint256 cost = _send(centrifugeId, batch, underpaid_.gasLimit, refund, false, msg.value);
         SafeTransferLib.safeTransferETH(refund, msg.value - cost);
 
-        if (underpaid_.counter == 0) delete underpaid[centrifugeId][batchHash];
+        // MUTATION: the drained record is no longer deleted
 
         emit RepayBatch(centrifugeId, batch);
     }
```

## Gateway #9836

an unpaid send stores its gas terms without adding a pending copy.

- **Mutant:** [`9836.sol`](9836.sol)
- **Caught by:** [`hlGwAnUnpaidShortfallBooksOneCopyAndRefundsAll`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L301)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9836`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwAnUnpaidShortfallBooksOneCopyAndRefundsAll`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -244,7 +244,7 @@
         bytes32 batchHash = keccak256(message);
 
         Underpaid storage underpaid_ = underpaid[centrifugeId][batchHash];
-        underpaid_.counter++;
+        // MUTATION: the pending copy counter is not raised
         underpaid_.gasLimit = gasLimit;
 
         emit UnderpaidBatch(centrifugeId, message, batchHash);
```

## Gateway #9837

handle is restricted to wards, so a pool manager can no longer deliver a message directly.

- **Mutant:** [`9837.sol`](9837.sol)
- **Caught by:** [`rcGwAPoolManagerInjectsAMessageNoQuorumApproved`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9837`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reachability.conf --rule rcGwAPoolManagerInjectsAMessageNoQuorumApproved`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -110,7 +110,7 @@
     function handle(uint16 centrifugeId, bytes memory batch)
         public
         pauseable
-        onlyAuthOrManager(processor.messagePoolId(batch))
+        auth // MUTATION: pool managers shut out of handle
     {
         require(centrifugeId != localCentrifugeId, CannotBeReceivedLocally());
 
```

## Gateway #9838

retry requires a ward or a manager of the message pool, so an outsider can no longer replay a failed message.

- **Mutant:** [`9838.sol`](9838.sol)
- **Caught by:** [`rcGwPermissionlessRetryPreemptsAClear`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L24)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9838`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reachability.conf --rule rcGwPermissionlessRetryPreemptsAClear`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -168,7 +168,7 @@
     function _afterProcessorCall() internal virtual {}
 
     /// @inheritdoc IGateway
-    function retry(uint16 centrifugeId, bytes memory message) external pauseable {
+    function retry(uint16 centrifugeId, bytes memory message) external pauseable onlyAuthOrManager(processor.messagePoolId(message)) { // MUTATION: retry gated
         bytes32 messageHash = keccak256(message);
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
 
```

## Gateway #9839

repay refuses while a batch is being flushed.

- **Mutant:** [`9839.sol`](9839.sol)
- **Caught by:** [`rcGwRepayIsUnguardedMidDispatch`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L54)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9839`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reachability.conf --rule rcGwRepayIsUnguardedMidDispatch`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -255,6 +255,7 @@
         bytes32 batchHash = keccak256(batch);
         Underpaid storage underpaid_ = underpaid[centrifugeId][batchHash];
         require(underpaid_.counter > 0, NotUnderpaidBatch());
+        require(!_isSendingBatch, ReentrantBatchCreation()); // MUTATION: repay refused mid flush
 
         underpaid_.counter--;
 
```

## Gateway #9840

an unpaid send is charged the full quote it could not pay, so a shortfall can never be booked.

- **Mutant:** [`9840.sol`](9840.sol)
- **Caught by:** [`rcGwUnpaidShortfallIsBookedAndRefunded`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L71)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9840`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reachability.conf --rule rcGwUnpaidShortfallIsBookedAndRefunded`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -234,7 +234,7 @@
             adapter.send{value: cost}(centrifugeId, batch, batchGasLimit, refund);
         } else if (unpaidMode) {
             _addUnpaidBatch(centrifugeId, batch, batchGasLimit);
-            cost = 0;
+            // MUTATION: the booked shortfall is still charged the quote
         } else {
             revert NotEnoughGas();
         }
```

## Gateway #9850

a failed inbound message is booked under the local network instead of the network it came from, so its own failure record never rises.

- **Mutant:** [`9850.sol`](9850.sol)
- **Caught by:** [`hlGwHandleBooksItsFailuresUnderItsSourceNetwork`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L325)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9850`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwHandleBooksItsFailuresUnderItsSourceNetwork`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -158,7 +158,7 @@
         if (success) {
             emit ExecuteMessage(centrifugeId, messageHash);
         } else {
-            failedMessages[centrifugeId][messageHash]++;
+            failedMessages[localCentrifugeId][messageHash]++; // MUTATION: booked under the local network
             emit FailMessage(centrifugeId, messageHash, err);
         }
     }
```

## Gateway #9852

after the first message of an inbound batch the rest of the batch is dropped, so no batch ever delivers two messages.

- **Mutant:** [`9852.sol`](9852.sol)
- **Caught by:** [`rcGwMultiMessageBatchIsDeliveredWhole`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L92)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9852`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reachability.conf --rule rcGwMultiMessageBatchIsDeliveredWhole`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -129,7 +129,7 @@
             uint16 requiredSource = processor.messageSourceCentrifugeId(message);
             require(requiredSource == 0 || requiredSource == centrifugeId, SourceMismatch());
 
-            remaining = remaining.slice(length, remaining.length - length);
+            remaining = new bytes(0); // MUTATION: the tail is dropped
             bytes32 messageHash = keccak256(message);
             uint128 gasLimit = messageGas.messageProcessingGasLimit(localCentrifugeId, message);
             require(gasleft() >= gasLimit, NotEnoughGas());
```

## Gateway #9853

an underpaid batch keeps the gas terms of its first unpaid copy, so a later copy never rewrites them.

- **Mutant:** [`9853.sol`](9853.sol)
- **Caught by:** [`rcGwUnderpaidGasLimitIsOverwrittenByTheLatestSend`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L106)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9853`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reachability.conf --rule rcGwUnderpaidGasLimitIsOverwrittenByTheLatestSend`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -245,7 +245,7 @@
 
         Underpaid storage underpaid_ = underpaid[centrifugeId][batchHash];
         underpaid_.counter++;
-        underpaid_.gasLimit = gasLimit;
+        if (underpaid_.counter == 1) underpaid_.gasLimit = gasLimit; // MUTATION: first copy only
 
         emit UnderpaidBatch(centrifugeId, message, batchHash);
     }
```

## Gateway #9854

a fully paid unbatched send is charged the quote but never handed to the adapter.

- **Mutant:** [`9854.sol`](9854.sol)
- **Caught by:** [`hlGwPaidUnbatchedSendReachesTheAdapterInTheSameCall`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L91)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9854`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwPaidUnbatchedSendReachesTheAdapterInTheSameCall`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -231,7 +231,7 @@
     ) internal returns (uint256 cost) {
         cost = adapter.estimate(centrifugeId, batch, batchGasLimit);
         if (fuel >= cost) {
-            adapter.send{value: cost}(centrifugeId, batch, batchGasLimit, refund);
+            // MUTATION: the paid batch is never handed to the adapter
         } else if (unpaidMode) {
             _addUnpaidBatch(centrifugeId, batch, batchGasLimit);
             cost = 0;
```

## Gateway #9855

an unbatched send no longer checks its gas terms against the destination batch cap.

- **Mutant:** [`9855.sol`](9855.sol)
- **Caught by:** [`rvGwSendRejectsGasAboveTheDestinationCap`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L271)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9855`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwSendRejectsGasAboveTheDestinationCap`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -214,7 +214,7 @@
 
             TransientBytesLib.append(batchSlot, message);
         } else {
-            require(gasLimit <= messageGas.maxBatchGasLimit(centrifugeId), BatchTooExpensive());
+            // MUTATION: the unbatched gas cap check is dropped
 
             uint256 cost = _send(centrifugeId, message, gasLimit, refund, unpaidMode, msg.value);
             SafeTransferLib.safeTransferETH(refund, msg.value - cost);
```

## Gateway #9856

a batched send checks the destination cap against its own gas terms only, so a region can grow past the cap.

- **Mutant:** [`9856.sol`](9856.sol)
- **Caught by:** [`rvGwBatchCapIsCheckedOnTheRunningSum`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L285)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9856`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwBatchCapIsCheckedOnTheRunningSum`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -205,7 +205,7 @@
 
             bytes32 gasLimitSlot = _gasLimitSlot(centrifugeId, poolId);
             uint128 newGasLimit = gasLimitSlot.tloadUint128() + gasLimit;
-            require(newGasLimit <= messageGas.maxBatchGasLimit(centrifugeId), BatchTooExpensive());
+            require(gasLimit <= messageGas.maxBatchGasLimit(centrifugeId), BatchTooExpensive()); // MUTATION: the running sum is not capped
             gasLimitSlot.tstore(uint256(newGasLimit));
 
             if (previousMessage.length == 0) {
```

## Gateway #9857

a send inside an open batch demands value up front, so no batched send is taken without payment.

- **Mutant:** [`9857.sol`](9857.sol)
- **Caught by:** [`rcGwBatchedSendDefersPaymentIsReachable`](../../specs/core/messaging/Gateway/single/Gateway_reachability.spec#L129)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9857`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reachability.conf --rule rcGwBatchedSendDefersPaymentIsReachable`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -198,7 +198,7 @@
 
         uint128 gasLimit = messageGas.messageOverallGasLimit(centrifugeId, message);
         if (isBatching) {
-            require(msg.value == 0, NotPayable());
+            require(msg.value > 0, NotPayable()); // MUTATION: value demanded inside a batch
 
             bytes32 batchSlot = _outboundBatchSlot(centrifugeId, poolId);
             bytes memory previousMessage = TransientBytesLib.get(batchSlot);
```

## Gateway #9858

a send inside an open batch already asks the adapter for a quote, so the adapter is reached before the flush.

- **Mutant:** [`9858.sol`](9858.sol)
- **Caught by:** [`stGwAnOpenBatchReachesTheAdapterOnlyThroughRepay`](../../specs/core/messaging/Gateway/single/Gateway_transitions.spec#L63)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9858`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/transitions.conf --rule stGwAnOpenBatchReachesTheAdapterOnlyThroughRepay`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -199,6 +199,7 @@
         uint128 gasLimit = messageGas.messageOverallGasLimit(centrifugeId, message);
         if (isBatching) {
             require(msg.value == 0, NotPayable());
+            adapter.estimate(centrifugeId, message, gasLimit); // MUTATION: the batch asks for a quote
 
             bytes32 batchSlot = _outboundBatchSlot(centrifugeId, poolId);
             bytes memory previousMessage = TransientBytesLib.get(batchSlot);
```

## Gateway #9859

every batched send registers its region again, so a region already in the batch is flushed more than once.

- **Mutant:** [`9859.sol`](9859.sol)
- **Caught by:** [`hlGwBatchedSendAppendsToItsOwnRegionOnly`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L111)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9859`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwBatchedSendAppendsToItsOwnRegionOnly`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -208,7 +208,7 @@
             require(newGasLimit <= messageGas.maxBatchGasLimit(centrifugeId), BatchTooExpensive());
             gasLimitSlot.tstore(uint256(newGasLimit));
 
-            if (previousMessage.length == 0) {
+            if (true) { // MUTATION: the region is registered on every send
                 TransientArrayLib.push(BATCH_LOCATORS_SLOT, _encodeLocator(centrifugeId, poolId));
             }
 
```

## Gateway #9860

a send inside an open batch in unpaid mode bypasses the batch and is quoted, and possibly booked as debt, at once.

- **Mutant:** [`9860.sol`](9860.sol)
- **Caught by:** [`hlGwTheUnpaidFlagIsInertInsideABatch`](../../specs/core/messaging/Gateway/single/Gateway_high_level.spec#L148)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9860`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/high_level.conf --rule hlGwTheUnpaidFlagIsInertInsideABatch`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -197,7 +197,7 @@
         emit PrepareMessage(centrifugeId, poolId, message);
 
         uint128 gasLimit = messageGas.messageOverallGasLimit(centrifugeId, message);
-        if (isBatching) {
+        if (isBatching && !unpaidMode) { // MUTATION: unpaid mode escapes the batch
             require(msg.value == 0, NotPayable());
 
             bytes32 batchSlot = _outboundBatchSlot(centrifugeId, poolId);
```

## Gateway #9861

closing a batch also raises a failure record of the local network.

- **Mutant:** [`9861.sol`](9861.sol)
- **Caught by:** [`stGwFailureLedgerMovesOnlyThroughItsOwnEntriesAcrossBatches`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L8)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9861`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/withbatch_properties.conf --rule stGwFailureLedgerMovesOnlyThroughItsOwnEntriesAcrossBatches`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -318,6 +318,7 @@
         }
 
         _isSendingBatch = false;
+        failedMessages[localCentrifugeId][bytes32(0)]++; // MUTATION: the flush books a failure
         isBatching = false;
     }
 
```

## Gateway #9862

a batch envelope no longer insists that its callback locked it, so the batcher can stay recorded after the envelope returns.

- **Mutant:** [`9862.sol`](9862.sol)
- **Caught by:** [`stGwNoCallLeavesABatchOpen`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L26)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9862`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/withbatch_properties.conf --rule stGwNoCallLeavesABatchOpen`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -286,7 +286,7 @@
         }
 
         // Force the user to call lockCallback()
-        require(address(_batcher) == address(0), CallbackWasNotLocked());
+        // MUTATION: the lock check after the callback is dropped
 
         if (isNested) {
             SafeTransferLib.safeTransferETH(refund, msg.value - callbackValue);
```

## Gateway #9863

the flush re checks the pause before dispatching, so a batch paused mid way is never dispatched.

- **Mutant:** [`9863.sol`](9863.sol)
- **Caught by:** [`rcGwFlushDispatchesAfterAMidBatchPause`](../../specs/core/messaging/Gateway/Gateway_withbatch_properties.spec#L75)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9863`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/withbatch_properties.conf --rule rcGwFlushDispatchesAfterAMidBatchPause`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -298,6 +298,7 @@
 
     function _endBatching(uint256 fuel, address refund) internal returns (uint256 cost) {
         require(isBatching, NoBatched());
+        require(!pauser.paused(), Paused()); // MUTATION: the flush re checks the pause
         bytes32[] memory locators = TransientArrayLib.getBytes32(BATCH_LOCATORS_SLOT);
 
         TransientArrayLib.clear(BATCH_LOCATORS_SLOT);
```

## Gateway #9864

repay is refused while any batch is open, so a debt can no longer be repaid from inside a flush.

- **Mutant:** [`9864.sol`](9864.sol)
- **Caught by:** [`rcGwRepayRunsInsideTheFlush`](../../specs/core/messaging/Gateway/Gateway_reentrant_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9864`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reentrant_properties.conf --rule rcGwRepayRunsInsideTheFlush`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -254,7 +254,7 @@
     function repay(uint16 centrifugeId, bytes memory batch, address refund) external payable pauseable {
         bytes32 batchHash = keccak256(batch);
         Underpaid storage underpaid_ = underpaid[centrifugeId][batchHash];
-        require(underpaid_.counter > 0, NotUnderpaidBatch());
+        require(underpaid_.counter > 0 && !isBatching, NotUnderpaidBatch()); // MUTATION: repay refused while batching
 
         underpaid_.counter--;
 
```

## Gateway #9886

handle skips the pool check on a batch's later messages, so one pool's manager can forward another pool's messages.

- **Mutant:** [`9886.sol`](9886.sol)
- **Caught by:** [`hlGwHandleForwardsOnlyTheBatchPool`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_pool_properties.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9886`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway_LinkedMessageProcessor/pool_properties.conf --rule hlGwHandleForwardsOnlyTheBatchPool`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -121,7 +121,7 @@
             uint256 length = processor.messageLength(remaining);
             bytes memory message = remaining.slice(0, length);
 
-            if (remaining.length != batch.length) {
+            if (false) { // MUTATION: the per message pool check of a batch never runs
                 // Only check if batching
                 require(batchPoolId == processor.messagePoolId(message), MalformedBatch());
             }
```

## Gateway #9887

handle admits only wards, so a pool manager can no longer deliver a message of its pool.

- **Mutant:** [`9887.sol`](9887.sol)
- **Caught by:** [`rcGwPoolManagerInjectsAHubOriginatedMessage`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_properties.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9887`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway_LinkedMessageProcessor/properties.conf --rule rcGwPoolManagerInjectsAHubOriginatedMessage`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -110,7 +110,7 @@
     function handle(uint16 centrifugeId, bytes memory batch)
         public
         pauseable
-        onlyAuthOrManager(processor.messagePoolId(batch))
+        auth // MUTATION: the pool manager leg of the handle gate is dropped
     {
         require(centrifugeId != localCentrifugeId, CannotBeReceivedLocally());
 
```

## Gateway #9888

handle no longer compares a message's required source network with the network it arrived from, so an upgrade message is accepted from any network.

- **Mutant:** [`9888.sol`](9888.sol)
- **Caught by:** [`rvGwHandleRefusesAnUpgradeFromANetworkOtherThanMainnet`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L7) · [`rvGwHandleRefusesAHubMessageOffItsPoolHome`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L22) · [`rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9888`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway_LinkedMessageProcessor/source_properties.conf --rule rvGwHandleRefusesAnUpgradeFromANetworkOtherThanMainnet rvGwHandleRefusesAHubMessageOffItsPoolHome rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -127,7 +127,7 @@
             }
 
             uint16 requiredSource = processor.messageSourceCentrifugeId(message);
-            require(requiredSource == 0 || requiredSource == centrifugeId, SourceMismatch());
+            require(true, SourceMismatch()); // MUTATION: the required source check always passes
 
             remaining = remaining.slice(length, remaining.length - length);
             bytes32 messageHash = keccak256(message);
```

## Gateway #9889

handle processes only the first message of a batch and silently ignores the rest of it, an unframeable tail included.

- **Mutant:** [`9889.sol`](9889.sol)
- **Caught by:** [`rcGwUnknownTailRevertsTheBatchAfterItsFirstMessageWasForwarded`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_properties.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9889`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway_LinkedMessageProcessor/properties.conf --rule rcGwUnknownTailRevertsTheBatchAfterItsFirstMessageWasForwarded`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -117,7 +117,7 @@
         PoolId batchPoolId = processor.messagePoolId(batch);
         uint128 failureGasReserve = messageGas.messageFailureGasReserve();
         bytes memory remaining = batch;
-        while (remaining.length > 0) {
+        if (remaining.length > 0) { // MUTATION: only the first message of the batch is walked
             uint256 length = processor.messageLength(remaining);
             bytes memory message = remaining.slice(0, length);
 
```

## Gateway #9895

clearFailedMessage admits only a ward, so no pool manager can clear a failed message.

- **Mutant:** [`9895.sol`](9895.sol)
- **Caught by:** [`rvGwClearRevertsIffOutsiderOrNoRecordedFailure`](../../specs/core/messaging/Gateway/single/Gateway_reverts.spec#L302)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh Gateway 9895`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway/reverts.conf --rule rvGwClearRevertsIffOutsiderOrNoRecordedFailure`

```diff
--- a/src/core/messaging/Gateway.sol
+++ b/src/core/messaging/Gateway.sol
@@ -93,7 +93,7 @@
     /// @inheritdoc IGateway
     function clearFailedMessage(uint16 centrifugeId, bytes memory message)
         external
-        onlyAuthOrManager(processor.messagePoolId(message))
+        auth // MUTATION: only a ward clears
     {
         bytes32 messageHash = keccak256(message);
         require(failedMessages[centrifugeId][messageHash] > 0, NotFailedMessage());
```

