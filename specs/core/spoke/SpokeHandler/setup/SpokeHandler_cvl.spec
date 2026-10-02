// SpokeHandler. Model: records that a call arrived, for scenes not compiling it.

methods {
    // UNSAFE: the handler's own effects and refusals are dropped.
    function _.addPool(uint64 poolId) external
        => spokeHandlerEntryCVL(101) expect void UNRESOLVED;
    function _.addShareClass(uint64 poolId, bytes16 scId, string tokenName, string tokenSymbol,
        uint8 decimals, bytes32 salt, address registrar, bytes payload) external
        => spokeHandlerAddShareClassCVL(salt, registrar) expect void UNRESOLVED;
    function _.updateShareMetadata(uint64 poolId, bytes16 scId, string tokenName, string tokenSymbol) external
        => spokeHandlerEntryCVL(103) expect void UNRESOLVED;
    function _.updatePricePoolPerShare(uint64 poolId, bytes16 scId, uint128 price, uint64 computedAt) external
        => spokeHandlerEntryCVL(104) expect void UNRESOLVED;
    function _.updatePricePoolPerAsset(uint64 poolId, bytes16 scId, uint128 assetId, uint128 price,
        uint64 computedAt) external
        => spokeHandlerEntryCVL(105) expect void UNRESOLVED;
    function _.updateRestriction(uint64 poolId, bytes16 scId, bytes update) external
        => spokeHandlerEntryCVL(106) expect void UNRESOLVED;
    function _.updateVault(uint64 poolId, bytes16 scId, uint128 assetId, address vaultOrFactory,
        uint8 kind, bytes payload) external
        => spokeHandlerEntryCVL(107) expect void UNRESOLVED;
    function _.setRequestManager(uint64 poolId, address manager) external
        => spokeHandlerEntryCVL(108) expect void UNRESOLVED;
    function _.authorize(uint64 poolId, bytes data) external
        => spokeHandlerEntryCVL(109) expect void UNRESOLVED;
    function _.unauthorize(uint64 poolId, bytes data) external
        => spokeHandlerEntryCVL(110) expect void UNRESOLVED;
    function _.setPolicy(uint64 poolId, address policy) external
        => spokeHandlerEntryCVL(111) expect void UNRESOLVED;
    // UNSAFE: also answers MultiAdapter and Gateway, effects dropped.
    function _.updateManager(uint64 poolId, address who, bool canManage) external
        => spokeHandlerUpdateManagerCVL(calledContract) expect void UNRESOLVED;
    function _.updateBridger(uint64 poolId, address who, bool canBridge) external
        => spokeHandlerUpdateBridgerCVL(calledContract) expect void UNRESOLVED;
    function _.executeTransferShares(uint64 poolId, bytes16 scId, bytes32 receiver, uint128 amount) external
        => spokeHandlerExecuteTransferSharesCVL(receiver) expect void UNRESOLVED;
    function _.requestCallback(uint64 poolId, bytes16 scId, uint128 assetId, bytes payload) external
        => spokeHandlerEntryCVL(113) expect void UNRESOLVED;
}

persistent ghost mathint ghostShCallCount {
    init_state axiom ghostShCallCount == 0;
    axiom ghostShCallCount >= 0;
}
persistent ghost bytes32 ghostShLastSalt;
persistent ghost address ghostShLastRegistrar;
persistent ghost address ghostShLastCallee;
persistent ghost bool ghostShLastWasBridger;
// Tags the entry last reached, unique across the handler faces: 1xx spoke, 2xx hub, 3xx envoy, 4xx root.
persistent ghost mathint ghostShLastEntry;
persistent ghost bytes32 ghostShLastTransferReceiver;

function spokeHandlerRecordCVL() {
    ghostShCallCount = ghostShCallCount + 1;
}

function spokeHandlerEntryCVL(mathint tag) {
    spokeHandlerRecordCVL();
    ghostShLastEntry = tag;
}

function spokeHandlerExecuteTransferSharesCVL(bytes32 receiver) {
    spokeHandlerEntryCVL(112);
    ghostShLastTransferReceiver = receiver;
}

function spokeHandlerAddShareClassCVL(bytes32 salt, address registrar) {
    spokeHandlerEntryCVL(102);
    ghostShLastSalt = salt;
    ghostShLastRegistrar = registrar;
}

function spokeHandlerUpdateManagerCVL(address callee) {
    spokeHandlerRecordCVL();
    ghostShLastCallee = callee;
    ghostShLastWasBridger = false;
}

function spokeHandlerUpdateBridgerCVL(address callee) {
    spokeHandlerRecordCVL();
    ghostShLastCallee = callee;
    ghostShLastWasBridger = true;
}
