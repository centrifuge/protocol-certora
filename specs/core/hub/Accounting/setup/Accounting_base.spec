// Accounting. Setup: harness link, session transients and the rules' call surface.

import "../../../../shared/env.spec";
import "../../../../shared/domains/account_domain_three.spec";

using AccountingHarness as _Accounting;
using AccountingCaller as _AccountingCaller;

methods {
    // SCOPE: setAccountMetadata is cut here, its footprint proved in the metadata lane.
    function _Accounting.setAccountMetadata(AccountingHarness.PoolId, AccountingHarness.AccountId, bytes) external
        => NONDET DELETE;
}

definition EXCLUDED_FUNCTION_AC(method f) returns bool =
    f.isView || f.isPure || f.isFallback
    // SCOPE: postings cut alone, journalPair runs them inside a session.
    || f.selector == sig:_Accounting.addDebit(AccountingHarness.AccountId,uint128).selector
    || f.selector == sig:_Accounting.addCredit(AccountingHarness.AccountId,uint128).selector
    || f.selector == sig:_Accounting.lock().selector
    ;

persistent ghost mathint ghostAcDebitedT {
    init_state axiom ghostAcDebitedT == 0;
}
persistent ghost mathint ghostAcCreditedT {
    init_state axiom ghostAcCreditedT == 0;
}
persistent ghost mathint ghostAcCurrentPoolT {
    init_state axiom ghostAcCurrentPoolT == 0;
}

hook Tload uint128 val _Accounting.debited {
    require(val == ghostAcDebitedT, "SAFE: mirror tracks storage");
}
hook Tstore _Accounting.debited uint128 val {
    ghostAcDebitedT = val;
}
hook Tload uint128 val _Accounting.credited {
    require(val == ghostAcCreditedT, "SAFE: mirror tracks storage");
}
hook Tstore _Accounting.credited uint128 val {
    ghostAcCreditedT = val;
}
hook Tload AccountingHarness.PoolId val _Accounting._currentPoolId {
    require(val == ghostAcCurrentPoolT, "SAFE: mirror tracks storage");
}
hook Tstore _Accounting._currentPoolId AccountingHarness.PoolId val {
    ghostAcCurrentPoolT = assert_uint64(val);
}

function setupAccounting(env e) {
    setupEnv(e);
    setupPoolMode();
    setupAccountDomain();
    setupJournalRegion();
    require(e.msg.sender != _Accounting, "SAFE: the ledger never calls itself");
    require(ghostAcCurrentPoolT == 0 && ghostAcDebitedT == 0 && ghostAcCreditedT == 0,
        "SAFE: transient storage starts empty");
}
