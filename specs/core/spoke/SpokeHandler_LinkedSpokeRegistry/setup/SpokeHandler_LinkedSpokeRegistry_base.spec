// SpokeHandler, registry linked. Setup: real registry, the escrow factory a model.

import "../../SpokeHandler/setup/SpokeHandler_base.spec";
import "../../SpokeRegistry/setup/SpokeRegistry_base.spec";
import "../../factories/EscrowFactory/setup/EscrowFactory_cvl.spec";

using ShareTokenStub as _ShareTokenStub;
using VaultStub as _VaultStub;

function setupSpokeHandlerLinkedSpokeRegistry(env e) {
    setupSpokeHandler(e);
    setupSpokeRegistry(e);
    require(ghostRegistrarNewToken == _ShareTokenStub, "SCOPE: a new share token is the modelled token contract");
    require(ghostHmNewVault == _VaultStub, "SCOPE: a new vault is the modelled vault contract");
}

// SAFE: the file key "spokeRegistry" as left-aligned ASCII.
definition FILE_KEY_SPOKE_REGISTRY_SH_CVL() returns bytes32 =
    to_bytes32(0x73706f6b65526567697374727900000000000000000000000000000000000000);

// SAFE: the file key "escrowFactory" as left-aligned ASCII.
definition FILE_KEY_ESCROW_FACTORY_SH_CVL() returns bytes32 =
    to_bytes32(0x657363726f77466163746f727900000000000000000000000000000000000000);

function setupSpokeHandlerLinkedSpokeRegistryValidState(env e) {
    setupSpokeHandlerLinkedSpokeRegistry(e);
    assumeLinkedVaultIsRegistered();
}
