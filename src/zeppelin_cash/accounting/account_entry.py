"""The module wallet.accounting.account_entry contains the AccountEntry implementation."""
from datetime import datetime

from zeppelin_cash.accounting.money import Money


class AccountEntry:
    """Encapsulate a single entry in a ledger account."""

    def __init__(self, time: datetime, amount: Money) -> None:
        """Create a new AccountEntry instance.

        Args:
            time: the time of the entry
            amount: the size of the entry
        """
        self._time = time
        self._amount = amount

    def time(self) -> datetime:
        """Get the time of the entry.

        Returns:
            The time of the entry.
        """
        return self._time

    def amount(self) -> Money:
        """Get the amount of the entry.

        Returns:
            The amount of the entry.
        """
        return self._amount
