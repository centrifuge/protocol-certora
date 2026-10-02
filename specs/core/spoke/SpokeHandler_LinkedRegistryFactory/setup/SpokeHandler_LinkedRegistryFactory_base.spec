// SpokeHandler_LinkedRegistryFactory. Setup: the real registry, factory and escrow.

import "../../SpokeHandler/setup/SpokeHandler_base.spec";
import "../../SpokeRegistry/setup/SpokeRegistry_base.spec";
import "../../factories/EscrowFactory/setup/EscrowFactory_base.spec";

// A hook resolves an alias only from a file processed before it, so the poolId hooks carry their own.
using EscrowFactoryHarness as _ShPoolEscrowFactory;
using ShareTokenStub as _ShareTokenStub;
using VaultStub as _VaultStub;

persistent ghost mapping(address => mathint) ghostPefEscrowPool64 {
    init_state axiom forall address a. ghostPefEscrowPool64[a] == 0;
    axiom forall address a. ghostPefEscrowPool64[a] >= 0 && ghostPefEscrowPool64[a] <= max_uint64;
}

hook Sload EscrowFactoryHarness.PoolId val _ShPoolEscrowFactory.poolId[KEY address a] {
    require(ghostPefEscrowPool64[a] == val, "SAFE: mirror tracks storage");
}

// Persistent so a havocked rely or deny on a fresh escrow leaves it intact.
persistent ghost bool ghostShBrandedBeforeRow;

hook Sstore _ShPoolEscrowFactory.poolId[KEY address a] EscrowFactoryHarness.PoolId val {
    ghostPefEscrowPool64[a] = val;
    ghostShBrandedBeforeRow = val == ghostPoolA64 ? ghostSrCreatedAt64 == 0 : ghostShBrandedBeforeRow;
}

function setupSpokeHandlerLinkedRegistryFactory(env e) {
    setupSpokeHandler(e);
    setupSpokeRegistry(e);
    setupPoolEscrowFactory(e);
    require(ghostRegistrarNewToken == _ShareTokenStub, "SCOPE: a new share token is the modelled token contract");
    require(ghostHmNewVault == _VaultStub, "SCOPE: a new vault is the modelled vault contract");
}

function setupSpokeHandlerLinkedRegistryFactoryValidState(env e) {
    setupSpokeHandlerLinkedRegistryFactory(e);
}
