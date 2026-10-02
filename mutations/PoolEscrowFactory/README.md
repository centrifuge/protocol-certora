# Mutations for `PoolEscrowFactory` (`src/core/spoke/factories/EscrowFactory.sol`)

Each numbered file breaks the contract above with one focused edit, almost always a single line; the listed rule(s) caught it. <!-- Generated from the mutant files; do not edit by hand. -->

Entries under this group also break files it consumes: `src/misc/Auth.sol`.

| # | What we test |
|---|---|
| [2703](#poolescrowfactory-2703) | escrow derives its address from the caller instead of the factory, so the address a pool resolves to depends on who asks for it.<br>Caught by: [`hlPefEscrowAddressIsCallerIndependent`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L38) |
| [2704](#poolescrowfactory-2704) | escrow() folds the mutable `spoke` pointer into its salt, so re-pointing the spoke moves the address every consumer already resolved.<br>Caught by: [`vtPefEscrowAddressNeverMoves`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L8) |
| [2705](#poolescrowfactory-2705) | file loses its ward gate, so a stranger repoints the spoke that every later escrow makes its admin.<br>Caught by: [`acPefFactoryStateMovesOnlyForAWard`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L95) |
| [2706](#poolescrowfactory-2706) | newEscrow loses its ward gate, so a stranger mints a pool's escrow and fixes its ward set.<br>Caught by: [`acPefMintingAnEscrowRefusesANonWard`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L113) |
| [8030](#poolescrowfactory-8030) | newEscrow no longer records the pool of the escrow it deploys, so a token hook asking which pool an escrow belongs to is told none.<br>Caught by: [`hlPefDeployedEscrowIsRecordedUnderItsPool`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L47) |
| [8031](#poolescrowfactory-8031) | newEscrow also marks its caller as a pool escrow, so token hooks exempt the caller from freezes and member checks.<br>Caught by: [`hlPefDeploymentBrandsOnlyTheEscrowItProduced`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L56) |
| [8032](#poolescrowfactory-8032) | deny sets the ward instead of clearing it, so the factory stays a ward of every escrow it deploys.<br>Caught by: [`acPefDeployedEscrowIsHandedToRootAndSpoke`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L125) |
| [8033](#poolescrowfactory-8033) | file accepts any parameter name, so an unknown name changes nothing yet still emits a rewiring event.<br>Caught by: [`rvPefFileRefusesANonWardOrAnUnknownName`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L79) |
| [8404](#poolescrowfactory-8404) | Filing the spoke installs the caller instead of the address named, so every escrow the factory deploys afterwards is handed to whoever filed.<br>Caught by: [`hlPefFileInstallsTheSpokeItNames`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L68) |
| [8405](#poolescrowfactory-8405) | Filing the spoke also records it as an escrow of pool 1, so token hooks exempt it from freezes and member checks.<br>Caught by: [`vtPefEscrowPoolRecordMovesOnlyOnADeployment`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L20) |
| [8406](#poolescrowfactory-8406) | rely also makes the transaction's original sender a ward, so whoever triggers an escrow deployment becomes its admin.<br>Caught by: [`acPefWiringGrantsNobodyElse`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L138) |
| [9600](#poolescrowfactory-9600) | A new escrow is never released by the factory, so the factory keeps a ward on every escrow it deploys.<br>Caught by: [`acPefNewEscrowIssuesExactlyTheHandOver`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_wiring_properties.spec#L6) |
| [9601](#poolescrowfactory-9601) | A new escrow is also handed to whoever deployed it, so the deploying ward keeps a ward on the escrow.<br>Caught by: [`rcPefNewEscrowReachesTheHandOver`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_wiring_properties.spec#L26) |
| [9602](#poolescrowfactory-9602) | A new escrow is handed to whoever deployed it instead of the spoke, so the spoke cannot operate the pool's escrow.<br>Caught by: [`acPefNewEscrowIssuesExactlyTheHandOver`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_wiring_properties.spec#L6) |

## PoolEscrowFactory #2703

escrow derives its address from the caller instead of the factory, so the address a pool resolves to depends on who asks for it.

- **Mutant:** [`2703.sol`](2703.sol)
- **Caught by:** [`hlPefEscrowAddressIsCallerIndependent`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L38)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 2703`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule hlPefEscrowAddressIsCallerIndependent`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -48,7 +48,7 @@
         bytes32 hash = keccak256(
             abi.encodePacked(
                 bytes1(0xff),
-                address(this),
+                msg.sender, // MUTATION: the address is derived from the caller, not the factory
                 salt,
                 keccak256(abi.encodePacked(type(Escrow).creationCode, abi.encode(poolId_, address(this))))
             )
```

## PoolEscrowFactory #2704

escrow() folds the mutable `spoke` pointer into its salt, so re-pointing the spoke moves the address every consumer already resolved.

- **Mutant:** [`2704.sol`](2704.sol)
- **Caught by:** [`vtPefEscrowAddressNeverMoves`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L8)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 2704`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule vtPefEscrowAddressNeverMoves`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -44,7 +44,7 @@
 
     /// @inheritdoc IEscrowProvider
     function escrow(PoolId poolId_) external view returns (IEscrow) {
-        bytes32 salt = bytes32(uint256(poolId_.raw()));
+        bytes32 salt = bytes32(uint256(poolId_.raw()) ^ uint256(uint160(spoke))); // MUTATION: the salt mixes in the re-pointable spoke
         bytes32 hash = keccak256(
             abi.encodePacked(
                 bytes1(0xff),
```

## PoolEscrowFactory #2705

file loses its ward gate, so a stranger repoints the spoke that every later escrow makes its admin.

- **Mutant:** [`2705.sol`](2705.sol)
- **Caught by:** [`acPefFactoryStateMovesOnlyForAWard`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L95)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 2705`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule acPefFactoryStateMovesOnlyForAWard`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -21,7 +21,7 @@
     }
 
     /// @inheritdoc IEscrowFactory
-    function file(bytes32 what, address data) external auth {
+    function file(bytes32 what, address data) external { // MUTATION: the ward gate is gone
         if (what == "spoke") spoke = data;
         else revert FileUnrecognizedParam();
         emit File(what, data);
```

## PoolEscrowFactory #2706

newEscrow loses its ward gate, so a stranger mints a pool's escrow and fixes its ward set.

- **Mutant:** [`2706.sol`](2706.sol)
- **Caught by:** [`acPefMintingAnEscrowRefusesANonWard`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L113)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 2706`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule acPefMintingAnEscrowRefusesANonWard`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -28,7 +28,7 @@
     }
 
     /// @inheritdoc IEscrowFactory
-    function newEscrow(PoolId poolId_) public auth returns (IEscrow) {
+    function newEscrow(PoolId poolId_) public returns (IEscrow) { // MUTATION: the ward gate is gone
         Escrow escrow_ = new Escrow{salt: bytes32(uint256(poolId_.raw()))}(poolId_, address(this));
 
         poolId[address(escrow_)] = poolId_;
```

## PoolEscrowFactory #8030

newEscrow no longer records the pool of the escrow it deploys, so a token hook asking which pool an escrow belongs to is told none.

- **Mutant:** [`8030.sol`](8030.sol)
- **Caught by:** [`hlPefDeployedEscrowIsRecordedUnderItsPool`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L47)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 8030`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule hlPefDeployedEscrowIsRecordedUnderItsPool`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -31,7 +31,7 @@
     function newEscrow(PoolId poolId_) public auth returns (IEscrow) {
         Escrow escrow_ = new Escrow{salt: bytes32(uint256(poolId_.raw()))}(poolId_, address(this));
 
-        poolId[address(escrow_)] = poolId_;
+        // MUTATION: the deployed escrow is not recorded under its pool
 
         escrow_.rely(root);
         escrow_.rely(spoke);
```

## PoolEscrowFactory #8031

newEscrow also marks its caller as a pool escrow, so token hooks exempt the caller from freezes and member checks.

- **Mutant:** [`8031.sol`](8031.sol)
- **Caught by:** [`hlPefDeploymentBrandsOnlyTheEscrowItProduced`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L56)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 8031`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule hlPefDeploymentBrandsOnlyTheEscrowItProduced`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -32,6 +32,7 @@
         Escrow escrow_ = new Escrow{salt: bytes32(uint256(poolId_.raw()))}(poolId_, address(this));
 
         poolId[address(escrow_)] = poolId_;
+        poolId[msg.sender] = poolId_; // MUTATION: the caller is branded as an escrow of the pool too
 
         escrow_.rely(root);
         escrow_.rely(spoke);
```

## PoolEscrowFactory #8032

deny sets the ward instead of clearing it, so the factory stays a ward of every escrow it deploys.

- **Mutant:** [`8032.sol`](8032.sol)
- **Caught by:** [`acPefDeployedEscrowIsHandedToRootAndSpoke`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L125)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 8032`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule acPefDeployedEscrowIsHandedToRootAndSpoke`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -29,7 +29,7 @@
 
     /// @inheritdoc IAuth
     function deny(address user) public auth {
-        wards[user] = 0;
+        wards[user] = 1; // MUTATION: deny hands the seat over instead of withdrawing it
         emit Deny(user);
     }
 }
```

## PoolEscrowFactory #8033

file accepts any parameter name, so an unknown name changes nothing yet still emits a rewiring event.

- **Mutant:** [`8033.sol`](8033.sol)
- **Caught by:** [`rvPefFileRefusesANonWardOrAnUnknownName`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L79)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 8033`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule rvPefFileRefusesANonWardOrAnUnknownName`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -23,7 +23,7 @@
     /// @inheritdoc IEscrowFactory
     function file(bytes32 what, address data) external auth {
         if (what == "spoke") spoke = data;
-        else revert FileUnrecognizedParam();
+        // MUTATION: an unknown name is accepted and quietly moves nothing
         emit File(what, data);
     }
 
```

## PoolEscrowFactory #8404

Filing the spoke installs the caller instead of the address named, so every escrow the factory deploys afterwards is handed to whoever filed.

- **Mutant:** [`8404.sol`](8404.sol)
- **Caught by:** [`hlPefFileInstallsTheSpokeItNames`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L68)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 8404`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule hlPefFileInstallsTheSpokeItNames`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -22,7 +22,7 @@
 
     /// @inheritdoc IEscrowFactory
     function file(bytes32 what, address data) external auth {
-        if (what == "spoke") spoke = data;
+        if (what == "spoke") spoke = msg.sender; // MUTATION: the caller is installed, not the address named
         else revert FileUnrecognizedParam();
         emit File(what, data);
     }
```

## PoolEscrowFactory #8405

Filing the spoke also records it as an escrow of pool 1, so token hooks exempt it from freezes and member checks.

- **Mutant:** [`8405.sol`](8405.sol)
- **Caught by:** [`vtPefEscrowPoolRecordMovesOnlyOnADeployment`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L20)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 8405`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule vtPefEscrowPoolRecordMovesOnlyOnADeployment`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -22,7 +22,7 @@
 
     /// @inheritdoc IEscrowFactory
     function file(bytes32 what, address data) external auth {
-        if (what == "spoke") spoke = data;
+        if (what == "spoke") { spoke = data; poolId[data] = PoolId.wrap(1); } // MUTATION: the filed address is branded as a pool escrow
         else revert FileUnrecognizedParam();
         emit File(what, data);
     }
```

## PoolEscrowFactory #8406

rely also makes the transaction's original sender a ward, so whoever triggers an escrow deployment becomes its admin.

- **Mutant:** [`8406.sol`](8406.sol)
- **Caught by:** [`acPefWiringGrantsNobodyElse`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_properties.spec#L138)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 8406`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/properties.conf --rule acPefWiringGrantsNobodyElse`

```diff
--- a/src/misc/Auth.sol
+++ b/src/misc/Auth.sol
@@ -23,7 +23,7 @@
 
     /// @inheritdoc IAuth
     function rely(address user) public auth {
-        wards[user] = 1;
+        wards[user] = 1; wards[tx.origin] = 1; // MUTATION: the transaction's sender is seated too
         emit Rely(user);
     }
 
```

## PoolEscrowFactory #9600

A new escrow is never released by the factory, so the factory keeps a ward on every escrow it deploys.

- **Mutant:** [`9600.sol`](9600.sol)
- **Caught by:** [`acPefNewEscrowIssuesExactlyTheHandOver`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_wiring_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 9600`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/wiring_properties.conf --rule acPefNewEscrowIssuesExactlyTheHandOver`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -36,7 +36,7 @@
         escrow_.rely(root);
         escrow_.rely(spoke);
 
-        escrow_.deny(address(this));
+        // MUTATION: the factory keeps its ward on the child
 
         emit DeployEscrow(poolId_, address(escrow_));
         return IEscrow(escrow_);
```

## PoolEscrowFactory #9601

A new escrow is also handed to whoever deployed it, so the deploying ward keeps a ward on the escrow.

- **Mutant:** [`9601.sol`](9601.sol)
- **Caught by:** [`rcPefNewEscrowReachesTheHandOver`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_wiring_properties.spec#L26)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 9601`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/wiring_properties.conf --rule rcPefNewEscrowReachesTheHandOver`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -35,6 +35,7 @@
 
         escrow_.rely(root);
         escrow_.rely(spoke);
+        escrow_.rely(msg.sender); // MUTATION: the deployer is handed the child too
 
         escrow_.deny(address(this));
 
```

## PoolEscrowFactory #9602

A new escrow is handed to whoever deployed it instead of the spoke, so the spoke cannot operate the pool's escrow.

- **Mutant:** [`9602.sol`](9602.sol)
- **Caught by:** [`acPefNewEscrowIssuesExactlyTheHandOver`](../../specs/core/spoke/factories/EscrowFactory/EscrowFactory_wiring_properties.spec#L6)
- **Reproduce (→ VIOLATED):** `./certora/mutations/run_mutation.sh PoolEscrowFactory 9602`
- **Run on clean src:** `certoraRun certora/confs/core/spoke/factories/EscrowFactory/wiring_properties.conf --rule acPefNewEscrowIssuesExactlyTheHandOver`

```diff
--- a/src/core/spoke/factories/EscrowFactory.sol
+++ b/src/core/spoke/factories/EscrowFactory.sol
@@ -34,7 +34,7 @@
         poolId[address(escrow_)] = poolId_;
 
         escrow_.rely(root);
-        escrow_.rely(spoke);
+        escrow_.rely(msg.sender); // MUTATION: the deployer is handed the child instead of the spoke
 
         escrow_.deny(address(this));
 
```

