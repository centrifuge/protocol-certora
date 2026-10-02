import "setup/Gateway_LinkedMessageProcessor_base.spec";
import "setup/Gateway_LinkedMessageProcessor_pool.spec";

// --- high_level ---

// GW-HL-19: every message an accepted batch forwards belongs to the pool the batch was authorized for.
rule hlGwHandleForwardsOnlyTheBatchPool(env e, uint16 c, bytes batch) {

    setupEnv(e);
    require(ghostGwBatchPool64 == _MessageProcessor.messagePoolId(batch),
        "SAFE: binds the check to the batch's authorizing pool");
    require(!ghostGwForeignPoolForwarded, "SAFE: no foreign-pool message forwarded yet");

    _Gateway.handle(e, c, batch);

    assert(!ghostGwForeignPoolForwarded, "every forwarded message carries the batch's own pool");
}
