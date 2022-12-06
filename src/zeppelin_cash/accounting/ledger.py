"""The module wallet.accounting.ledger contains the Ledger implementation."""
from typing import List
from datetime import datetime

from zeppelin_cash.accounting.account import Account
from zeppelin_cash.accounting.account_entry import AccountEntry
from zeppelin_cash.accounting.account_metadata import AccountMetadata
from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.currency import Currency
from zeppelin_cash.accounting.money import Money
from zeppelin_cash.errors import Error, ok, Result


class Ledger:
    """A Ledger contains logical accounts.

    Using a ledger, one should be able to replay the transaction history
    of a firm.
    """

    def __init__(self, accounts: List[Account],
                 currency: Currency = usd()) -> None:
        """Create a new Ledger instance.

        Args:
            accounts: the account pages that comprise the ledger
            currency: the currency used in the accounting
        """
        self.accounts = accounts
        self.accounting_currency = currency

    def add_account(self, account: Account) -> Error:
        """Add an account.

        Args:
            account: the account to add

        Returns:
            An error if the account cannot be added.
        """
        for each in self.accounts:
            if each.id() == account.id():
                return Error("account id already present")
        self.accounts.append(account)
        return ok()

    def add_entry(self, account_id: str, is_debit: bool,
                  entry: AccountEntry) -> Error:
        """Add an entry to an account.

        Args:
            account_id: the id of the account
            is_debit: True iff the update is a debit
            entry: the entry to append

        Returns:
            An error if an error occurs.
        """
        for k in range(len(self.accounts)):
            if self.accounts[k].id() != account_id:
                continue
            return self.accounts[k].add_entry(is_debit, entry)
        return Error("account not found")

    def balance_as_of_date(self, time: datetime,
                           account_id: str) -> Result[Money]:
        """Get the balance as of a given date.

        Args:
            time: the time at which to get the balance.
            account_id: the account for which to get the balance.

        Return:
            The balance of the account at that time, or an error
            if the parameters were invalid.
        """
        for account in self.accounts:
            if account.id() != account_id:
                continue
            return account.balance_as_of_date(time)
        return Result(err=Error("account not found"))

    def list_accounts(self, timestamp: datetime) -> List[AccountMetadata]:
        """List the metadata for all the accounts in the ledger.

        Args:
            timestamp: the timestamp at which the balance should be calculated

        Returns:
            A list of metadata about the accounts."""
        return [account.metadata(timestamp) for account in self.accounts]
