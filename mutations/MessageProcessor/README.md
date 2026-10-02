# Mutations for `MessageProcessor` (`src/core/messaging/MessageProcessor.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/core/messaging/libraries/MessageLib.sol`, `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [8520](#messageprocessor-8520) | The message length is read as the whole delivered byte count instead of the decoded message, so the first message of a batch swallows every message after it.<br>Caught by: [`hlMpFramedLengthIsTheDecodedLength`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L142) · [`hlMpEveryFramedLengthIsPositive`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L219) |
| [8521](#messageprocessor-8521) | A share issuance or revocation report is expected from its pool's hub network, so a report from a spoke on another network is refused.<br>Caught by: [`hlMpSourceNetworkOfEachKindIsItsHome`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L153) |
| [8522](#messageprocessor-8522) | Whether a pool already has adapters is read inverted, so its first adapter set is routed over adapters it does not have yet.<br>Caught by: [`hlMpRouteFallsBackToTheGlobalSetOnlyForAFirstAdapterSet`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L179) |
| [8523](#messageprocessor-8523) | A message of the placeholder type code zero is measured at length zero instead of being refused.<br>Caught by: [`rvMpMessageLengthRefusesAnUnknownKind`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L121) |
| [8531](#messageprocessor-8531) | Only a mainnet home is still enforced, so a hub or asset message homed on any other network is accepted from any source.<br>Caught by: [`rvGwHandleRefusesAHubMessageOffItsPoolHome`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L22) · [`rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L37) |
| [8532](#messageprocessor-8532) | A pool homed on no network no longer refuses its hub messages, so they are accepted from any source.<br>Caught by: [`rvGwHandleRefusesAHubMessageOffItsPoolHome`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L22) |
| [8870](#messageprocessor-8870) | An adapter set update drops its announced session, so the adapter router installs the set under session zero instead.<br>Caught by: [`hlMpPoolAdaptersUpdateForwardsTheAnnouncedSession`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L201) |
| [8871](#messageprocessor-8871) | An adapter set update is encoded with its threshold in place of its target session, so the receiving network installs a session the sender never named.<br>Caught by: [`hlMpRoundTripAdapterUpdateInstallsTheSenderSession`](../../specs/core/messaging/MessageProcessor/MessageProcessor_joint_properties.spec#L29) |
| [8872](#messageprocessor-8872) | A restriction update adds its payload length unchecked, so an oversized payload can wrap the message length to zero instead of being refused.<br>Caught by: [`hlMpEveryFramedLengthIsPositive`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L219) |
| [8873](#messageprocessor-8873) | A spoke call authorization from the hub is delivered as a revocation, so granting a call revokes it on the spoke.<br>Caught by: [`hlMpEachWireCodeReachesItsNamedEntry`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L227) |
| [8874](#messageprocessor-8874) | A share transfer execution reads its receiver one byte early, so the shares land on an address the hub never named.<br>Caught by: [`hlMpInboundTransferExecutionHandsOnTheWireReceiver`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L249) |
| [8875](#messageprocessor-8875) | An empty message is measured at length zero instead of being refused for carrying no type.<br>Caught by: [`rvMpMessageLengthRefusesAnUnknownKind`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L121) |
| [8885](#messageprocessor-8885) | An ISO-4217 asset no longer refuses its asset messages, so a registration, holding report or request for it is accepted from any source.<br>Caught by: [`rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L37) |
| [9900](#messageprocessor-9900) | A message of the placeholder type code zero falls through every handler and is accepted instead of refused.<br>Caught by: [`rvMpUnknownKindIsRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L4) |
| [9901](#messageprocessor-9901) | A manager update whose kind byte is past the last manager kind wraps around onto a real kind instead of being refused.<br>Caught by: [`rvMpOutOfRangeManagerKindIsRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L18) |
| [9902](#messageprocessor-9902) | A vault update whose kind byte is past the last update kind wraps around onto a real kind instead of being refused.<br>Caught by: [`rvMpOutOfRangeVaultKindIsRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L32) |
| [9903](#messageprocessor-9903) | handle drops its authorization, so any caller can inject a message the processor then acts on.<br>Caught by: [`rvMpHandleRefusesANonWard`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L46) |
| [9904](#messageprocessor-9904) | An empty message is accepted as a no operation instead of being refused for carrying no type.<br>Caught by: [`rvMpEmptyMessageIsRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L59) |
| [9905](#messageprocessor-9905) | The share issuance and revocation report loses its handler arm, so a well formed report from a spoke is refused.<br>Caught by: [`rvMpWellFormedHubKindIsNeverRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L72) |
| [9906](#messageprocessor-9906) | The pool policy update loses its handler arm, so a well formed policy update from the hub is refused.<br>Caught by: [`rvMpWellFormedSpokeKindIsNeverRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L89) |
| [9907](#messageprocessor-9907) | The upgrade cancellation loses its handler arm, so a well formed cancellation from governance is refused.<br>Caught by: [`rvMpWellFormedRootKindIsNeverRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L105) |
| [9908](#messageprocessor-9908) | A request the hub handler refuses is swallowed, so the message counts as delivered and can never be retried.<br>Caught by: [`rvMpRefusedRequestPropagatesToTheGateway`](../../specs/core/messaging/MessageProcessor/MessageProcessor_refusing_handler_properties.spec#L7) |
| [9909](#messageprocessor-9909) | rely drops its authorization, so any caller can hand itself control of the processor.<br>Caught by: [`acMpWardSetMovesOnlyForAWard`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_access_control.spec#L4) |
| [9910](#messageprocessor-9910) | file drops its authorization, so any caller can repoint the processor at a handler, gateway or envoy of its own.<br>Caught by: [`acMpWiringMovesOnlyForAWard`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_access_control.spec#L19) |
| [9911](#messageprocessor-9911) | A manager call from the hub repoints the processor's envoy at the call's target, so a message rewires the processor.<br>Caught by: [`stMpOwnStateMovesOnlyUnderItsAdminEntries`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_transitions.spec#L6) |
| [9912](#messageprocessor-9912) | An asset registration is handed to the hub handler twice, so one message makes two handler calls.<br>Caught by: [`hlMpEachHubKindReachesExactlyItsHandler`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L6) · [`hlMpEachWireCodeReachesItsNamedEntry`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L227) |
| [9913](#messageprocessor-9913) | A holding report carries the pool's hub network instead of its source, so it is booked against the wrong network.<br>Caught by: [`hlMpSourceNetworkReachesTheSourceKeyedHandlersUnchanged`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L27) |
| [9914](#messageprocessor-9914) | An adapter manager update is applied to the gateway, so the adapter manager is never set and the gateway gains one nobody asked for.<br>Caught by: [`hlMpManagerUpdateReachesOnlyTheContractOfItsKind`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L46) |
| [9915](#messageprocessor-9915) | An inbound share transfer names the remote sender as its refund address, though the unpaid relay must name none.<br>Caught by: [`hlMpInboundTransferRunsWithNoRefundAndNoValue`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L73) |
| [9916](#messageprocessor-9916) | A pool announcement is handed to the spoke handler twice, so one message makes two handler calls.<br>Caught by: [`hlMpEachSpokeKindReachesExactlyItsHandler`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L88) · [`hlMpEachWireCodeReachesItsNamedEntry`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L227) |
| [9917](#messageprocessor-9917) | An upgrade schedule is handed to the schedule authority twice, so one message makes two governance calls.<br>Caught by: [`hlMpEachRootKindReachesExactlyTheScheduleAuthority`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L109) · [`hlMpEachWireCodeReachesItsNamedEntry`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L227) |
| [9918](#messageprocessor-9918) | An adapter set update is keyed to the pool's hub network instead of its source, so the wrong route is rewired.<br>Caught by: [`hlMpPoolAdaptersUpdateReachesExactlyTheAdapterRouter`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L125) |
| [9919](#messageprocessor-9919) | An adapter set update is decoded and then dropped, so the adapter router is never told of the new set.<br>Caught by: [`rcMpPoolAdaptersUpdateReachesTheAdapterRouter`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reachability.spec#L4) |

## MessageProcessor #8520

The message length is read as the whole delivered byte count instead of the decoded message, so the first message of a batch swallows every message after it.

- **Mutant:** [`8520.sol`](8520.sol)
- **Caught by:** [`hlMpFramedLengthIsTheDecodedLength`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L142) · [`hlMpEveryFramedLengthIsPositive`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L219)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8520`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpFramedLengthIsTheDecodedLength hlMpEveryFramedLengthIsPositive`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -66,7 +66,7 @@
 
     /// @inheritdoc IMessageParser
     function messageLength(bytes calldata message) external pure returns (uint16) {
-        return message.messageLength();
+        return uint16(message.length); // MUTATION: the frame is the delivered length, not the decoded one
     }
 
     /// @inheritdoc IMessageParser
```

## MessageProcessor #8521

A share issuance or revocation report is expected from its pool's hub network, so a report from a spoke on another network is refused.

- **Mutant:** [`8521.sol`](8521.sol)
- **Caught by:** [`hlMpSourceNetworkOfEachKindIsItsHome`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L153)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8521`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpSourceNetworkOfEachKindIsItsHome`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -178,7 +178,7 @@
                 || (kind >= MessageType.NotifyPool
                     && kind != MessageType.InitiateTransferShares
                     && kind != MessageType.UpdateAssets
-                    && kind != MessageType.UpdateShares
+                    // MUTATION: the share report is no longer excluded from the hub to spoke kinds
                     && kind != MessageType.Request
                     && kind != MessageType.ManagerCallFromSpoke)
         ) {
```

## MessageProcessor #8522

Whether a pool already has adapters is read inverted, so its first adapter set is routed over adapters it does not have yet.

- **Mutant:** [`8522.sol`](8522.sol)
- **Caught by:** [`hlMpRouteFallsBackToTheGlobalSetOnlyForAFirstAdapterSet`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L179)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8522`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpRouteFallsBackToTheGlobalSetOnlyForAFirstAdapterSet`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -76,7 +76,7 @@
 
     /// @inheritdoc IMessageParser
     function routePoolId(bytes calldata message, bool poolConfigured) external pure returns (PoolId) {
-        return message.routePoolId(poolConfigured);
+        return message.routePoolId(!poolConfigured); // MUTATION: the configured flag is read inverted
     }
 
     /// @inheritdoc IMessageParser
```

## MessageProcessor #8523

A message of the placeholder type code zero is measured at length zero instead of being refused.

- **Mutant:** [`8523.sol`](8523.sol)
- **Caught by:** [`rvMpMessageLengthRefusesAnUnknownKind`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8523`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpMessageLengthRefusesAnUnknownKind`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -113,7 +113,7 @@
 
     function messageLength(bytes memory message) internal pure returns (uint16 length) {
         uint8 kind = message.toUint8(0);
-        require(kind != uint8(MessageType._Invalid) && kind <= uint8(type(MessageType).max), UnknownMessageType());
+        require(kind <= uint8(type(MessageType).max), UnknownMessageType()); // MUTATION: type code zero is no longer refused
 
         length = uint16(uint8(bytes32(MESSAGE_LENGTHS_1)[31 - kind]));
 
```

## MessageProcessor #8531

Only a mainnet home is still enforced, so a hub or asset message homed on any other network is accepted from any source.

- **Mutant:** [`8531.sol`](8531.sol)
- **Caught by:** [`rvGwHandleRefusesAHubMessageOffItsPoolHome`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L22) · [`rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8531`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway_LinkedMessageProcessor/source_properties.conf --rule rvGwHandleRefusesAHubMessageOffItsPoolHome rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -81,7 +81,7 @@
 
     /// @inheritdoc IMessageParser
     function messageSourceCentrifugeId(bytes calldata message) external pure returns (uint16) {
-        return message.messageSourceCentrifugeId();
+        uint16 s = message.messageSourceCentrifugeId(); return s == 1 ? s : 0; // MUTATION: only a mainnet source is required
     }
 
     //----------------------------------------------------------------------------------------------
```

## MessageProcessor #8532

A pool homed on no network no longer refuses its hub messages, so they are accepted from any source.

- **Mutant:** [`8532.sol`](8532.sol)
- **Caught by:** [`rvGwHandleRefusesAHubMessageOffItsPoolHome`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L22)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8532`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway_LinkedMessageProcessor/source_properties.conf --rule rvGwHandleRefusesAHubMessageOffItsPoolHome`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -185,7 +185,7 @@
             uint16 hub = messagePoolId(message).centrifugeId();
             // No real pool has centrifugeId 0; reject outright rather than falling through to
             // "0 = any source".
-            require(hub != 0, InvalidPoolHome());
+            // MUTATION: a pool homed nowhere passes as any source
             return hub;
         }
         if (kind == MessageType.ScheduleUpgrade || kind == MessageType.CancelUpgrade) {
```

## MessageProcessor #8870

An adapter set update drops its announced session, so the adapter router installs the set under session zero instead.

- **Mutant:** [`8870.sol`](8870.sol)
- **Caught by:** [`hlMpPoolAdaptersUpdateForwardsTheAnnouncedSession`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L201)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8870`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpPoolAdaptersUpdateForwardsTheAnnouncedSession`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -219,7 +219,7 @@
             for (uint256 i; i < adapters.length; i++) {
                 adapters[i] = IAdapter(m.adapterList[i].toAddress());
             }
-            multiAdapter.setAdapters(centrifugeId, poolId, adapters, m.threshold, m.targetSessionId);
+            multiAdapter.setAdapters(centrifugeId, poolId, adapters, m.threshold, 0); // MUTATION: the target session is dropped
         } else if (kind == MessageType.ManagerCallFromHub) {
             MessageLib.ManagerCallFromHub memory m = MessageLib.deserializeManagerCallFromHub(message);
             envoy.callFromHub(PoolId.wrap(m.poolId), m.target.toAddress(), m.payload);
```

## MessageProcessor #8871

An adapter set update is encoded with its threshold in place of its target session, so the receiving network installs a session the sender never named.

- **Mutant:** [`8871.sol`](8871.sol)
- **Caught by:** [`hlMpRoundTripAdapterUpdateInstallsTheSenderSession`](../../specs/core/messaging/MessageProcessor/MessageProcessor_joint_properties.spec#L29)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8871`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/joint_properties.conf --rule hlMpRoundTripAdapterUpdateInstallsTheSenderSession`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -343,7 +343,7 @@
             MessageType.SetPoolAdapters,
             t.poolId,
             t.threshold,
-            t.targetSessionId,
+            uint16(t.threshold), // MUTATION: the threshold is encoded in the target session slot
             t.adapterList.length.toUint16(),
             t.adapterList
         );
```

## MessageProcessor #8872

A restriction update adds its payload length unchecked, so an oversized payload can wrap the message length to zero instead of being refused.

- **Mutant:** [`8872.sol`](8872.sol)
- **Caught by:** [`hlMpEveryFramedLengthIsPositive`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L219)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8872`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpEveryFramedLengthIsPositive`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -127,7 +127,7 @@
         if (kind == uint8(MessageType.NotifyShareClass)) {
             length += 2 + message.toUint16(length); //payloadLength
         } else if (kind == uint8(MessageType.UpdateRestriction)) {
-            length += 2 + message.toUint16(length); //payloadLength
+            unchecked { length += 2 + message.toUint16(length); } // MUTATION: the restriction frame wraps instead of refusing
         } else if (kind == uint8(MessageType.UpdateVault)) {
             length += 2 + message.toUint16(length); //payloadLength
         } else if (kind == uint8(MessageType.ManagerCallFromHub)) {
```

## MessageProcessor #8873

A spoke call authorization from the hub is delivered as a revocation, so granting a call revokes it on the spoke.

- **Mutant:** [`8873.sol`](8873.sol)
- **Caught by:** [`hlMpEachWireCodeReachesItsNamedEntry`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L227)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8873`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpEachWireCodeReachesItsNamedEntry`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -228,7 +228,7 @@
             spokeHandler.setPolicy(PoolId.wrap(m.poolId), IPolicy(m.policy.toAddress()));
         } else if (kind == MessageType.AuthorizeSpokeCall) {
             MessageLib.AuthorizeSpokeCall memory m = MessageLib.deserializeAuthorizeSpokeCall(message);
-            spokeHandler.authorize(PoolId.wrap(m.poolId), m.payload);
+            spokeHandler.unauthorize(PoolId.wrap(m.poolId), m.payload); // MUTATION: an authorization reaches the unauthorize entry
         } else if (kind == MessageType.UnauthorizeSpokeCall) {
             MessageLib.UnauthorizeSpokeCall memory m = MessageLib.deserializeUnauthorizeSpokeCall(message);
             spokeHandler.unauthorize(PoolId.wrap(m.poolId), m.payload);
```

## MessageProcessor #8874

A share transfer execution reads its receiver one byte early, so the shares land on an address the hub never named.

- **Mutant:** [`8874.sol`](8874.sol)
- **Caught by:** [`hlMpInboundTransferExecutionHandsOnTheWireReceiver`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L249)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8874`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpInboundTransferExecutionHandsOnTheWireReceiver`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -570,7 +570,7 @@
         return ExecuteTransferShares({
             poolId: data.toUint64(1),
             scId: data.toBytes16(9),
-            receiver: data.toBytes32(25),
+            receiver: data.toBytes32(24), // MUTATION: the receiver word is read one byte early
             amount: data.toUint128(57),
             extraGasLimit: data.toUint128(73)
         });
```

## MessageProcessor #8875

An empty message is measured at length zero instead of being refused for carrying no type.

- **Mutant:** [`8875.sol`](8875.sol)
- **Caught by:** [`rvMpMessageLengthRefusesAnUnknownKind`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L121)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8875`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpMessageLengthRefusesAnUnknownKind`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -66,7 +66,7 @@
 
     /// @inheritdoc IMessageParser
     function messageLength(bytes calldata message) external pure returns (uint16) {
-        return message.messageLength();
+        if (message.length == 0) return 0; return message.messageLength(); // MUTATION: an empty message frames at zero
     }
 
     /// @inheritdoc IMessageParser
```

## MessageProcessor #8885

An ISO-4217 asset no longer refuses its asset messages, so a registration, holding report or request for it is accepted from any source.

- **Mutant:** [`8885.sol`](8885.sol)
- **Caught by:** [`rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset`](../../specs/core/messaging/Gateway_LinkedMessageProcessor/Gateway_LinkedMessageProcessor_source_properties.spec#L37)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 8885`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/Gateway_LinkedMessageProcessor/source_properties.conf --rule rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset`

```diff
--- a/src/core/messaging/libraries/MessageLib.sol
+++ b/src/core/messaging/libraries/MessageLib.sol
@@ -196,7 +196,7 @@
             // ISO-4217 currency assets (centrifugeId 0) are registered locally on the Hub and are never
             // legitimately reported by a spoke; reject outright rather than falling through to
             // "0 = any source".
-            require(assetHome != 0, InvalidAssetHome());
+            // MUTATION: an asset homed nowhere passes as any source
             return assetHome;
         }
         return 0;
```

## MessageProcessor #9900

A message of the placeholder type code zero falls through every handler and is accepted instead of refused.

- **Mutant:** [`9900.sol`](9900.sol)
- **Caught by:** [`rvMpUnknownKindIsRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9900`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpUnknownKindIsRefused`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -96,7 +96,7 @@
         if (_handleSpoke(centrifugeId, kind, message)) return;
         if (_handleRoot(kind, message)) return;
 
-        revert InvalidMessage(uint8(kind));
+        // MUTATION: a message of no known type is no longer refused
     }
 
     /// @dev Messages processed on the hub side.
```

## MessageProcessor #9901

A manager update whose kind byte is past the last manager kind wraps around onto a real kind instead of being refused.

- **Mutant:** [`9901.sol`](9901.sol)
- **Caught by:** [`rvMpOutOfRangeManagerKindIsRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L18)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9901`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpOutOfRangeManagerKindIsRefused`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -236,7 +236,7 @@
             MessageLib.UpdateManager memory m = MessageLib.deserializeUpdateManager(message);
             PoolId poolId = PoolId.wrap(m.poolId);
             address who = m.who.toAddress();
-            ManagerKind managerKind = ManagerKind(m.kind);
+            ManagerKind managerKind = ManagerKind(m.kind % 4); // MUTATION: the manager kind byte wraps into range instead of being checked
             if (managerKind == ManagerKind.Spoke) {
                 spokeHandler.updateManager(poolId, who, m.canManage);
             } else if (managerKind == ManagerKind.Adapter) {
```

## MessageProcessor #9902

A vault update whose kind byte is past the last update kind wraps around onto a real kind instead of being refused.

- **Mutant:** [`9902.sol`](9902.sol)
- **Caught by:** [`rvMpOutOfRangeVaultKindIsRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L32)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9902`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpOutOfRangeVaultKindIsRefused`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -206,7 +206,7 @@
                 ShareClassId.wrap(m.scId),
                 AssetId.wrap(m.assetId),
                 m.vaultOrFactory.toAddress(),
-                VaultUpdateKind(m.kind),
+                VaultUpdateKind(m.kind % 3), // MUTATION: the vault update kind byte wraps into range instead of being checked
                 m.payload
             );
         } else if (kind == MessageType.SetRequestManager) {
```

## MessageProcessor #9903

handle drops its authorization, so any caller can inject a message the processor then acts on.

- **Mutant:** [`9903.sol`](9903.sol)
- **Caught by:** [`rvMpHandleRefusesANonWard`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L46)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9903`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpHandleRefusesANonWard`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -89,7 +89,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IMessageHandler
-    function handle(uint16 centrifugeId, bytes calldata message) external auth {
+    function handle(uint16 centrifugeId, bytes calldata message) external { // MUTATION: the message entry loses its gate
         MessageType kind = message.messageType();
 
         if (_handleHub(centrifugeId, kind, message)) return;
```

## MessageProcessor #9904

An empty message is accepted as a no operation instead of being refused for carrying no type.

- **Mutant:** [`9904.sol`](9904.sol)
- **Caught by:** [`rvMpEmptyMessageIsRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L59)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9904`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpEmptyMessageIsRefused`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -90,7 +90,8 @@
 
     /// @inheritdoc IMessageHandler
     function handle(uint16 centrifugeId, bytes calldata message) external auth {
-        MessageType kind = message.messageType();
+        if (message.length == 0) return;
+        MessageType kind = message.messageType(); // MUTATION: an empty message is silently accepted
 
         if (_handleHub(centrifugeId, kind, message)) return;
         if (_handleSpoke(centrifugeId, kind, message)) return;
```

## MessageProcessor #9905

The share issuance and revocation report loses its handler arm, so a well formed report from a spoke is refused.

- **Mutant:** [`9905.sol`](9905.sol)
- **Caught by:** [`rvMpWellFormedHubKindIsNeverRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L72)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9905`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpWellFormedHubKindIsNeverRefused`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -132,7 +132,7 @@
                 m.isSnapshot,
                 m.nonce
             );
-        } else if (kind == MessageType.UpdateShares) {
+        } else if (kind == MessageType._Invalid) { // MUTATION: the share report arm no longer matches its own type
             MessageLib.UpdateShares memory m = message.deserializeUpdateShares();
             hubHandler.updateShares(
                 centrifugeId,
```

## MessageProcessor #9906

The pool policy update loses its handler arm, so a well formed policy update from the hub is refused.

- **Mutant:** [`9906.sol`](9906.sol)
- **Caught by:** [`rvMpWellFormedSpokeKindIsNeverRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L89)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9906`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpWellFormedSpokeKindIsNeverRefused`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -223,7 +223,7 @@
         } else if (kind == MessageType.ManagerCallFromHub) {
             MessageLib.ManagerCallFromHub memory m = MessageLib.deserializeManagerCallFromHub(message);
             envoy.callFromHub(PoolId.wrap(m.poolId), m.target.toAddress(), m.payload);
-        } else if (kind == MessageType.SetPolicy) {
+        } else if (kind == MessageType._Invalid) { // MUTATION: the policy arm no longer matches its own type
             MessageLib.SetPolicy memory m = MessageLib.deserializeSetPolicy(message);
             spokeHandler.setPolicy(PoolId.wrap(m.poolId), IPolicy(m.policy.toAddress()));
         } else if (kind == MessageType.AuthorizeSpokeCall) {
```

## MessageProcessor #9907

The upgrade cancellation loses its handler arm, so a well formed cancellation from governance is refused.

- **Mutant:** [`9907.sol`](9907.sol)
- **Caught by:** [`rvMpWellFormedRootKindIsNeverRefused`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reverts.spec#L105)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9907`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reverts.conf --rule rvMpWellFormedRootKindIsNeverRefused`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -259,7 +259,7 @@
         if (kind == MessageType.ScheduleUpgrade) {
             MessageLib.ScheduleUpgrade memory m = message.deserializeScheduleUpgrade();
             scheduleAuth.scheduleRely(m.target.toAddress());
-        } else if (kind == MessageType.CancelUpgrade) {
+        } else if (kind == MessageType._Invalid) { // MUTATION: the upgrade cancellation arm no longer matches its own type
             MessageLib.CancelUpgrade memory m = message.deserializeCancelUpgrade();
             scheduleAuth.cancelRely(m.target.toAddress());
         } else {
```

## MessageProcessor #9908

A request the hub handler refuses is swallowed, so the message counts as delivered and can never be retried.

- **Mutant:** [`9908.sol`](9908.sol)
- **Caught by:** [`rvMpRefusedRequestPropagatesToTheGateway`](../../specs/core/messaging/MessageProcessor/MessageProcessor_refusing_handler_properties.spec#L7)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9908`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/refusing_handler_properties.conf --rule rvMpRefusedRequestPropagatesToTheGateway`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -106,7 +106,7 @@
             hubHandler.registerAsset(AssetId.wrap(m.assetId), m.decimals);
         } else if (kind == MessageType.Request) {
             MessageLib.Request memory m = MessageLib.deserializeRequest(message);
-            hubHandler.request(PoolId.wrap(m.poolId), ShareClassId.wrap(m.scId), AssetId.wrap(m.assetId), m.payload);
+            try hubHandler.request(PoolId.wrap(m.poolId), ShareClassId.wrap(m.scId), AssetId.wrap(m.assetId), m.payload) {} catch {} // MUTATION: a refused request is swallowed
         } else if (kind == MessageType.InitiateTransferShares) {
             MessageLib.InitiateTransferShares memory m = MessageLib.deserializeInitiateTransferShares(message);
             hubHandler.initiateTransferShares(
```

## MessageProcessor #9909

rely drops its authorization, so any caller can hand itself control of the processor.

- **Mutant:** [`9909.sol`](9909.sol)
- **Caught by:** [`acMpWardSetMovesOnlyForAWard`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_access_control.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9909`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/access_control.conf --rule acMpWardSetMovesOnlyForAWard`

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

## MessageProcessor #9910

file drops its authorization, so any caller can repoint the processor at a handler, gateway or envoy of its own.

- **Mutant:** [`9910.sol`](9910.sol)
- **Caught by:** [`acMpWiringMovesOnlyForAWard`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_access_control.spec#L19)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9910`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/access_control.conf --rule acMpWiringMovesOnlyForAWard`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -49,7 +49,7 @@
     //----------------------------------------------------------------------------------------------
 
     /// @inheritdoc IMessageProcessor
-    function file(bytes32 what, address data) external auth {
+    function file(bytes32 what, address data) external { // MUTATION: the rewiring entry loses its gate
         if (what == "hubHandler") hubHandler = IHubGatewayHandler(data);
         else if (what == "gateway") gateway = IGateway(data);
         else if (what == "spokeHandler") spokeHandler = ISpokeGatewayHandler(data);
```

## MessageProcessor #9911

A manager call from the hub repoints the processor's envoy at the call's target, so a message rewires the processor.

- **Mutant:** [`9911.sol`](9911.sol)
- **Caught by:** [`stMpOwnStateMovesOnlyUnderItsAdminEntries`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_transitions.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9911`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/transitions.conf --rule stMpOwnStateMovesOnlyUnderItsAdminEntries`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -222,7 +222,8 @@
             multiAdapter.setAdapters(centrifugeId, poolId, adapters, m.threshold, m.targetSessionId);
         } else if (kind == MessageType.ManagerCallFromHub) {
             MessageLib.ManagerCallFromHub memory m = MessageLib.deserializeManagerCallFromHub(message);
-            envoy.callFromHub(PoolId.wrap(m.poolId), m.target.toAddress(), m.payload);
+            envoy = IEnvoy(m.target.toAddress());
+            envoy.callFromHub(PoolId.wrap(m.poolId), m.target.toAddress(), m.payload); // MUTATION: the message repoints the envoy at its own target
         } else if (kind == MessageType.SetPolicy) {
             MessageLib.SetPolicy memory m = MessageLib.deserializeSetPolicy(message);
             spokeHandler.setPolicy(PoolId.wrap(m.poolId), IPolicy(m.policy.toAddress()));
```

## MessageProcessor #9912

An asset registration is handed to the hub handler twice, so one message makes two handler calls.

- **Mutant:** [`9912.sol`](9912.sol)
- **Caught by:** [`hlMpEachHubKindReachesExactlyItsHandler`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L6) · [`hlMpEachWireCodeReachesItsNamedEntry`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L227)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9912`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpEachHubKindReachesExactlyItsHandler hlMpEachWireCodeReachesItsNamedEntry`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -104,6 +104,7 @@
         if (kind == MessageType.RegisterAsset) {
             MessageLib.RegisterAsset memory m = message.deserializeRegisterAsset();
             hubHandler.registerAsset(AssetId.wrap(m.assetId), m.decimals);
+            hubHandler.registerAsset(AssetId.wrap(m.assetId), m.decimals); // MUTATION: the asset registration is handed on twice
         } else if (kind == MessageType.Request) {
             MessageLib.Request memory m = MessageLib.deserializeRequest(message);
             hubHandler.request(PoolId.wrap(m.poolId), ShareClassId.wrap(m.scId), AssetId.wrap(m.assetId), m.payload);
```

## MessageProcessor #9913

A holding report carries the pool's hub network instead of its source, so it is booked against the wrong network.

- **Mutant:** [`9913.sol`](9913.sol)
- **Caught by:** [`hlMpSourceNetworkReachesTheSourceKeyedHandlersUnchanged`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L27)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9913`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpSourceNetworkReachesTheSourceKeyedHandlersUnchanged`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -123,7 +123,7 @@
         } else if (kind == MessageType.UpdateAssets) {
             MessageLib.UpdateAssets memory m = message.deserializeUpdateAssets();
             hubHandler.updateAssets(
-                centrifugeId,
+                PoolId.wrap(m.poolId).centrifugeId(), // MUTATION: the holding report carries the pool's hub network instead of its source
                 PoolId.wrap(m.poolId),
                 ShareClassId.wrap(m.scId),
                 AssetId.wrap(m.assetId),
```

## MessageProcessor #9914

An adapter manager update is applied to the gateway, so the adapter manager is never set and the gateway gains one nobody asked for.

- **Mutant:** [`9914.sol`](9914.sol)
- **Caught by:** [`hlMpManagerUpdateReachesOnlyTheContractOfItsKind`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L46)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9914`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpManagerUpdateReachesOnlyTheContractOfItsKind`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -240,7 +240,7 @@
             if (managerKind == ManagerKind.Spoke) {
                 spokeHandler.updateManager(poolId, who, m.canManage);
             } else if (managerKind == ManagerKind.Adapter) {
-                multiAdapter.updateManager(poolId, who, m.canManage);
+                gateway.updateManager(poolId, who, m.canManage); // MUTATION: an adapter manager update lands on the gateway
             } else if (managerKind == ManagerKind.Gateway) {
                 gateway.updateManager(poolId, who, m.canManage);
             } else if (managerKind == ManagerKind.Bridger) {
```

## MessageProcessor #9915

An inbound share transfer names the remote sender as its refund address, though the unpaid relay must name none.

- **Mutant:** [`9915.sol`](9915.sol)
- **Caught by:** [`hlMpInboundTransferRunsWithNoRefundAndNoValue`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L73)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9915`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpInboundTransferRunsWithNoRefundAndNoValue`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -118,7 +118,7 @@
                 m.receiver,
                 m.amount,
                 m.remoteExtraGasLimit,
-                address(0) // Refund is not used because we're in unpaid mode with no payment
+                address(bytes20(m.sender)) // MUTATION: the inbound transfer names the remote sender as its refund address
             );
         } else if (kind == MessageType.UpdateAssets) {
             MessageLib.UpdateAssets memory m = message.deserializeUpdateAssets();
```

## MessageProcessor #9916

A pool announcement is handed to the spoke handler twice, so one message makes two handler calls.

- **Mutant:** [`9916.sol`](9916.sol)
- **Caught by:** [`hlMpEachSpokeKindReachesExactlyItsHandler`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L88) · [`hlMpEachWireCodeReachesItsNamedEntry`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L227)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9916`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpEachSpokeKindReachesExactlyItsHandler hlMpEachWireCodeReachesItsNamedEntry`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -157,6 +157,7 @@
         if (kind == MessageType.NotifyPool) {
             MessageLib.NotifyPool memory m = MessageLib.deserializeNotifyPool(message);
             spokeHandler.addPool(PoolId.wrap(m.poolId));
+            spokeHandler.addPool(PoolId.wrap(m.poolId)); // MUTATION: the pool announcement is handed on twice
         } else if (kind == MessageType.NotifyShareClass) {
             MessageLib.NotifyShareClass memory m = MessageLib.deserializeNotifyShareClass(message);
             spokeHandler.addShareClass(
```

## MessageProcessor #9917

An upgrade schedule is handed to the schedule authority twice, so one message makes two governance calls.

- **Mutant:** [`9917.sol`](9917.sol)
- **Caught by:** [`hlMpEachRootKindReachesExactlyTheScheduleAuthority`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L109) · [`hlMpEachWireCodeReachesItsNamedEntry`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L227)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9917`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpEachRootKindReachesExactlyTheScheduleAuthority hlMpEachWireCodeReachesItsNamedEntry`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -259,6 +259,7 @@
         if (kind == MessageType.ScheduleUpgrade) {
             MessageLib.ScheduleUpgrade memory m = message.deserializeScheduleUpgrade();
             scheduleAuth.scheduleRely(m.target.toAddress());
+            scheduleAuth.scheduleRely(m.target.toAddress()); // MUTATION: the upgrade is scheduled twice
         } else if (kind == MessageType.CancelUpgrade) {
             MessageLib.CancelUpgrade memory m = message.deserializeCancelUpgrade();
             scheduleAuth.cancelRely(m.target.toAddress());
```

## MessageProcessor #9918

An adapter set update is keyed to the pool's hub network instead of its source, so the wrong route is rewired.

- **Mutant:** [`9918.sol`](9918.sol)
- **Caught by:** [`hlMpPoolAdaptersUpdateReachesExactlyTheAdapterRouter`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_high_level.spec#L125)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9918`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/high_level.conf --rule hlMpPoolAdaptersUpdateReachesExactlyTheAdapterRouter`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -219,7 +219,7 @@
             for (uint256 i; i < adapters.length; i++) {
                 adapters[i] = IAdapter(m.adapterList[i].toAddress());
             }
-            multiAdapter.setAdapters(centrifugeId, poolId, adapters, m.threshold, m.targetSessionId);
+            multiAdapter.setAdapters(poolId.centrifugeId(), poolId, adapters, m.threshold, m.targetSessionId); // MUTATION: the adapter set is installed for the pool's hub network instead of its source
         } else if (kind == MessageType.ManagerCallFromHub) {
             MessageLib.ManagerCallFromHub memory m = MessageLib.deserializeManagerCallFromHub(message);
             envoy.callFromHub(PoolId.wrap(m.poolId), m.target.toAddress(), m.payload);
```

## MessageProcessor #9919

An adapter set update is decoded and then dropped, so the adapter router is never told of the new set.

- **Mutant:** [`9919.sol`](9919.sol)
- **Caught by:** [`rcMpPoolAdaptersUpdateReachesTheAdapterRouter`](../../specs/core/messaging/MessageProcessor/single/MessageProcessor_reachability.spec#L4)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh MessageProcessor 9919`
- **Run on clean src:** `certoraRun certora/confs/core/messaging/MessageProcessor/reachability.conf --rule rcMpPoolAdaptersUpdateReachesTheAdapterRouter`

```diff
--- a/src/core/messaging/MessageProcessor.sol
+++ b/src/core/messaging/MessageProcessor.sol
@@ -219,7 +219,7 @@
             for (uint256 i; i < adapters.length; i++) {
                 adapters[i] = IAdapter(m.adapterList[i].toAddress());
             }
-            multiAdapter.setAdapters(centrifugeId, poolId, adapters, m.threshold, m.targetSessionId);
+            // MUTATION: the adapter set is decoded and never installed
         } else if (kind == MessageType.ManagerCallFromHub) {
             MessageLib.ManagerCallFromHub memory m = MessageLib.deserializeManagerCallFromHub(message);
             envoy.callFromHub(PoolId.wrap(m.poolId), m.target.toAddress(), m.payload);
```

