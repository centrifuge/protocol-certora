import "setup/EscrowFactory_wiring.spec";

// --- access_control ---

// PEF-AC-05: a deployment adds Root, then the spoke, as escrow admins, then drops the factory, nothing more.
rule acPefNewEscrowIssuesExactlyTheHandOver(env e, uint64 poolId) {

    setupPoolEscrowFactoryWiring(e);

    address rootAddr = _PoolEscrowFactory.root();
    address spokeAddr = _PoolEscrowFactory.spoke();

    address deployed = _PoolEscrowFactory.newEscrow(e, poolId);

    assert(ghostPefN == 3
        && ghostPefTarget[0] == deployed && ghostPefTarget[1] == deployed && ghostPefTarget[2] == deployed
        && ghostPefIsRely[0] && ghostPefWho[0] == rootAddr
        && ghostPefIsRely[1] && ghostPefWho[1] == spokeAddr
        && !ghostPefIsRely[2] && ghostPefWho[2] == _PoolEscrowFactory,
        "on the new escrow only root and spoke added, then the factory removed");
}

// --- reachability ---

// PEF-RC-01: an admin can deploy a pool escrow in three admin changes, the first and last made on it.
rule rcPefNewEscrowReachesTheHandOver(env e, uint64 poolId) {

    setupPoolEscrowFactoryWiring(e);

    address deployed = _PoolEscrowFactory.newEscrow(e, poolId);

    satisfy(ghostPefN == 3 && ghostPefTarget[0] == deployed && ghostPefTarget[2] == deployed,
        "a deployment can make three admin calls, first and last on the escrow");
}
