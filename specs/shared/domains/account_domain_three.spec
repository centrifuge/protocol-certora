// Three-account sizing of the chart of accounts: the three pinned rows are distinct.

// UNSAFE: only the three pinned accounts are analysed.
persistent ghost uint256 ghostAcAccountE1;

persistent ghost uint256 ghostAcAccountE2;

persistent ghost uint256 ghostAcAccountE3;

definition VALID_ACCOUNT(mathint a) returns bool =
    a == ghostAcAccountE1 || a == ghostAcAccountE2 || a == ghostAcAccountE3;

function setupAccountDomain() {
    require(ghostAcAccountE1 != ghostAcAccountE2 && ghostAcAccountE1 != ghostAcAccountE3
        && ghostAcAccountE2 != ghostAcAccountE3, "SCOPE: three distinct modelled ledger accounts");
}
