// Accounting, metadata lane. Setup: setAccountMetadata kept, its bytes copied for real.

// Own setup: base cuts setAccountMetadata; kept there, its bytes copy (loop_iter 16) would weigh on every rule.

import "../../../../shared/env.spec";

// UNSAFE: loop and hash bounds leave metadata past 512 bytes unseen.
using AccountingHarness as _Accounting;

persistent ghost mathint ghostAcSessionStores {
    init_state axiom ghostAcSessionStores == 0;
}

hook Tstore _Accounting.debited uint128 val {
    ghostAcSessionStores = ghostAcSessionStores + 1;
}

hook Tstore _Accounting.credited uint128 val {
    ghostAcSessionStores = ghostAcSessionStores + 1;
}

hook Tstore _Accounting._currentPoolId AccountingHarness.PoolId val {
    ghostAcSessionStores = ghostAcSessionStores + 1;
}
