// HubHandler, linked hub core lane. Valid state: posted debits cover the holdings' value.

import "setup/HubHandler_LinkedHubCore_base.spec";

// HH-VS-01: any two holdings are together never worth more than the pool's posted debits.
invariant postedDebitsCoverCarriedValue(env e)
    ghostHoAssetAmountValue128[ghostHoAssetE1] + ghostHoAssetAmountValue128[ghostHoAssetE2]
        <= AC_TOTAL_DEBIT_SUM()
filtered { f -> !EXCLUDED_FUNCTION_HH(f) } { preserved with (env eFunc) { SETUP_HH(e, eFunc); } }
