// Environment floor: setupEnv() pins sender, timestamp and block for every scene.

definition MIN_BLOCK_TIMESTAMP() returns mathint = max_uint16;
definition MAX_BLOCK_TIMESTAMP() returns mathint = max_uint32;

function setupEnv(env e) {
    require(e.msg.sender != 0 && e.msg.sender != currentContract, "SAFE: an outside caller, not address zero");
    require(e.block.timestamp >= MIN_BLOCK_TIMESTAMP() && e.block.timestamp < MAX_BLOCK_TIMESTAMP(),
        "SAFE: a realistic timestamp, before 2106");
    require(e.block.number != 0, "SAFE: no transaction runs in the genesis block");
}

function requireSameEnv(env e1, env e2) {
    require(e1.block.number == e2.block.number, "SAFE: both calls in the same block");
    require(e1.block.timestamp == e2.block.timestamp, "SAFE: both calls at the same time");
    require(e1.msg.sender == e2.msg.sender, "SAFE: both calls from the same caller");
    require(e1.msg.value == e2.msg.value, "SAFE: both calls carry the same ether");
}
