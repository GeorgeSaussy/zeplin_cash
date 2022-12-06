"""The module wallet.accounting.account includes the Account implementation."""
from typing import List
from datetime import datetime

from zeppelin_cash.errors import Error, ok, Result
from zeppelin_cash.accounting.account_metadata import AccountMetadata
from zeppelin_cash.accounting.money import Money
from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.account_entry import AccountEntry


AccountId = str


class Account:
    """Account encapsulates a single account page in a logical ledger."""

    def __init__(self, title: str, is_asset: bool, my_id: AccountId) -> None:
        """Create a new Account.

        Args:
            title: the name of the account, does not need to be unique
            is_assert: set to true if the balance is an assert,  otherwise it is a liability.
            my_id: some unique account ID
        """
        self.credits: List[AccountEntry] = []
        self.debits: List[AccountEntry] = []
        self.title = title
        self.is_asset = is_asset
        self._id = my_id
        self.init_balance = Money(0, usd())
        self.init_datetime = datetime(2019, 1, 1, 0, 0)

    def set_starting_balance(self, start_time: datetime,
                             balance: Money) -> None:
        """Set the starting value for account.

        Args:
            start_time: the starting time
            balance: the starting balance
        """
        self.init_balance = balance
        self.init_datetime = start_time

    def balance(self) -> Money:
        """Get the balance for a given account.

        Returns:
            The balance of the account.
        """
        money = Money(0, usd())  # assuming USD here
        debit_sign = 1.0 if self.is_asset else -1.0
        for transaction in self.debits:
            money += transaction.amount().scale(debit_sign)
        for transaction in self.credits:
            money += transaction.amount().scale(-1.0 * debit_sign)
        money += self.init_balance
        return money

    def balance_as_of_date(self, time: datetime) -> Result[Money]:
        """Get the balance as of a specific date.

        If the date is before the first entry of the account,
        the function will return 0 USD.

        Returns:
            The balance if the time is valid.
        """
        if self.init_datetime > time:
            return Result(
                err=Error("cannot compute balance at time before account was created"))
        money = Money(0, usd())
        debit_sign = 1.0 if self.is_asset else -1.0
        for transaction in self.debits:
            if transaction.time() < time:
                money += transaction.amount().scale(debit_sign)
        for transaction in self.credits:
            if transaction.time() < time:
                money += transaction.amount().scale(-1.0 * debit_sign)
        money += self.init_balance
        return Result(ok=money)

    def id(self) -> str:  # pylint: disable=C0103
        """Get the account id.

        Returns:
            The account id.
        """
        return self._id

    def add_entry(self, is_debit: bool, entry: AccountEntry) -> Error:
        """Add an entry to the account.

        Args:
            is_debit: True iff the entry is a debit
            entry: the entry to append

        Returns:
            An error if an error occurs.
        """

        # check dates
        if len(self.credits) > 0:
            if entry.time() < self.credits[len(self.credits) - 1].time():
                return Error("new entry is earlier than last entry")
        if len(self.debits) > 0:
            if entry.time() < self.debits[len(self.debits) - 1].time():
                return Error("new entry is earlier than last entry")
        # append
        if is_debit:
            self.debits.append(entry)
        else:
            self.credits.append(entry)
        return ok()

    def metadata(self, timestamp: datetime) -> AccountMetadata:
        """Get the metadata for an account as of a given timestamp.

        Args:
            timestamp: the timestamp from which to read the account values

        Returns:
            The metadata for the account or an error if the balance cannot be read.
        """
        result = self.balance_as_of_date(timestamp)
        balance = result.ok() if result.is_ok() else None
        return AccountMetadata(self.id(), self.title,
                               balance, timestamp, self.is_asset)
