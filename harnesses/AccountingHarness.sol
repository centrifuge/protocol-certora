// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.28;

import {PoolId} from "../../src/core/types/PoolId.sol";
import {AccountId} from "../../src/core/types/AccountId.sol";
import {Accounting} from "../../src/core/hub/Accounting.sol";
import {IAccounting, JournalEntry} from "../../src/core/hub/interfaces/IAccounting.sol";

// Carries the scene's name, which the conf links and the specs resolve against.
contract AccountingHarness is Accounting {
    constructor(address deployer) Accounting(deployer) {}
}

// Stands in for the Hub, which opens and closes a session inside one call.
contract AccountingCaller {
    IAccounting public accounting;

    // Hub._journal; the two legs carry independent values, so an unbalanced session is reachable.
    function journalPair(
        PoolId poolId,
        AccountId debitAccount,
        uint128 debitValue,
        AccountId creditAccount,
        uint128 creditValue
    ) external {
        accounting.unlock(poolId);
        accounting.addDebit(debitAccount, debitValue);
        accounting.addCredit(creditAccount, creditValue);
        accounting.lock();
    }

    // Hub.updateJournal.
    function journalBatch(PoolId poolId, JournalEntry[] memory debits, JournalEntry[] memory credits) external {
        accounting.unlock(poolId);
        accounting.addJournal(debits, credits);
        accounting.lock();
    }
}
