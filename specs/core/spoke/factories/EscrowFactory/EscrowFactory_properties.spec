import "setup/EscrowFactory_base.spec";

using Escrow as _PoolEscrow;

// --- variable_transitions ---

// PEF-VT-01: a pool's escrow address never changes, whatever call the factory receives.
rule vtPefEscrowAddressNeverMoves(env e, env e2, method f, calldataarg args, uint64 p)
    filtered { f -> !EXCLUDED_FUNCTION_PEF(f) } {

    setupPoolEscrowFactory(e);
    address before = _PoolEscrowFactory.escrow(e, p);

    f(e2, args);

    assert(_PoolEscrowFactory.escrow(e, p) == before, "no entry moves a pool's escrow address");
}

// PEF-VT-02: an address's pool registration changes only when an escrow is deployed.
rule vtPefEscrowPoolRecordMovesOnlyOnADeployment(env e, env eView, method f, calldataarg args, address a)
    filtered { f -> !EXCLUDED_FUNCTION_PEF(f) } {

    setupPoolEscrowFactory(e);

    uint64 poolBefore = _PoolEscrowFactory.poolId(eView, a);

    f(e, args);

    assert(_PoolEscrowFactory.poolId(eView, a) != poolBefore
        => (f.selector == sig:_PoolEscrowFactory.newEscrow(EscrowFactoryHarness.PoolId).selector
            || f.selector == sig:_PoolEscrowFactory.newEscrowLinked(EscrowFactoryHarness.PoolId).selector),
        "only an escrow deployment changes an address's pool record");
}

// --- high_level ---

// PEF-HL-01: a pool's escrow address does not depend on who asks.
rule hlPefEscrowAddressIsCallerIndependent(env e1, env e2, uint64 p) {
    setupPoolEscrowFactory(e1);
    setupPoolEscrowFactory(e2);

    assert(_PoolEscrowFactory.escrow(e1, p) == _PoolEscrowFactory.escrow(e2, p),
        "a pool's escrow address is the same for every caller");
}

// PEF-HL-02: a newly deployed escrow is registered to the pool it was deployed for.
rule hlPefDeployedEscrowIsRecordedUnderItsPool(env e, env eView, uint64 p) {
    setupPoolEscrowFactory(e);

    address deployed = _PoolEscrowFactory.newEscrow(e, p);

    assert(_PoolEscrowFactory.poolId(eView, deployed) == p, "a fresh escrow's pool lookup returns the pool asked for");
}

// PEF-HL-03: deploying an escrow changes the pool registration of no other address.
rule hlPefDeploymentBrandsOnlyTheEscrowItProduced(env e, env eView, uint64 p, address other) {
    setupPoolEscrowFactory(e);

    uint64 otherBefore = _PoolEscrowFactory.poolId(eView, other);

    address deployed = _PoolEscrowFactory.newEscrow(e, p);

    assert(other != deployed => _PoolEscrowFactory.poolId(eView, other) == otherBefore,
        "a deployment changes no pool record but the new escrow's");
}

// PEF-HL-04: setting the spoke stores the address that later escrows get as admin.
rule hlPefFileInstallsTheSpokeItNames(env e, bytes32 what, address data) {
    setupPoolEscrowFactory(e);

    _PoolEscrowFactory.file(e, what, data);

    assert(_PoolEscrowFactory.spoke() == data, "a successful rewiring installs the given spoke");
}

// --- reverts ---

// PEF-RV-01: updating the factory's configuration fails for a non-admin or an unknown parameter.
rule rvPefFileRefusesANonWardOrAnUnknownName(env e, bytes32 what, address data) {

    setupPoolEscrowFactory(e);

    mathint senderWardBefore = _PoolEscrowFactory.wards(e.msg.sender);

    _PoolEscrowFactory.file@withrevert(e, what, data);
    bool reverted = lastReverted;

    assert((senderWardBefore != 1 || what != FILE_KEY_SPOKE_PEF_CVL()) => reverted,
        "rewiring fails for a non-ward or any name but spoke");
}

// --- access_control ---

// PEF-AC-01: only an admin can change the factory's spoke or its admin rights.
rule acPefFactoryStateMovesOnlyForAWard(env e, method f, calldataarg args, address who)
    filtered { f -> !EXCLUDED_FUNCTION_PEF(f) } {

    setupPoolEscrowFactory(e);

    mathint senderWardBefore = _PoolEscrowFactory.wards(e.msg.sender);
    address spokeBefore = _PoolEscrowFactory.spoke();
    mathint wardBefore = _PoolEscrowFactory.wards(who);

    f(e, args);

    assert((_PoolEscrowFactory.spoke() != spokeBefore || _PoolEscrowFactory.wards(who) != wardBefore)
        => senderWardBefore == 1,
        "the spoke pointer and the ward set change only for a ward");
}

// PEF-AC-02: only an admin can deploy a pool's escrow.
// SCOPE: refusal only, a deployment is invisible to a storage frame.
rule acPefMintingAnEscrowRefusesANonWard(env e, EscrowFactoryHarness.PoolId poolId) {

    setupPoolEscrowFactory(e);
    require(_PoolEscrowFactory.wards(e.msg.sender) != 1, "SCOPE: the caller is not a ward");

    _PoolEscrowFactory.newEscrow@withrevert(e, poolId);

    assert(lastReverted, "a non-ward cannot deploy a pool escrow");
}

// PEF-AC-03: a new escrow has Root and the spoke as admins, but not the factory.
// SCOPE: linked escrow stands in, a fresh deployment is unresolvable.
rule acPefDeployedEscrowIsHandedToRootAndSpoke(env e, EscrowFactoryHarness.PoolId poolId) {

    setupPoolEscrowFactory(e);

    _PoolEscrowFactory.newEscrowLinked(e, poolId);

    assert(_PoolEscrow.wards[_PoolEscrowFactory.root()] == 1
        && _PoolEscrow.wards[_PoolEscrowFactory.spoke()] == 1
        && _PoolEscrow.wards[_PoolEscrowFactory] == 0,
        "a new escrow is warded by root and spoke, not the factory");
}

// PEF-AC-04: deploying an escrow grants no admin rights beyond Root and the spoke.
rule acPefWiringGrantsNobodyElse(env e, EscrowFactoryHarness.PoolId poolId, address who) {

    setupPoolEscrowFactory(e);

    require(who != _PoolEscrowFactory.root() && who != _PoolEscrowFactory.spoke() && who != _PoolEscrowFactory,
        "SCOPE: anyone but root, spoke and factory (PEF-AC-03)");
    mathint wardBefore = _PoolEscrow.wards[who];

    _PoolEscrowFactory.newEscrowLinked(e, poolId);

    assert(_PoolEscrow.wards[who] == wardBefore, "deploying an escrow grants or revokes no one else");
}
