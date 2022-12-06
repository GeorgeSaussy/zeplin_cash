"""The module wallet.accounting.journal_entry contains the JournalEntry implementation."""
from zeppelin_cash.accounting.money import Money


class JournalEntry:
    """A JournalEntry instance encapsulates a single entry in the general journal."""

    def __init__(self, my_id: str, is_debit: bool, amount: Money) -> None:
        """Create a new JournalEntry instance.

        Args:
            my_id: the ID of the account
            is_debit: True iff the entry is a debit
            amount: the size of the entry
        """
        self._account_id = my_id
        self._amount = amount
        self._is_debit = is_debit

    def account_id(self) -> str:
        """Get the account id of the entry.

        Returns:
            The id.
        """
        return self._account_id

    def amount(self) -> Money:
        """Get the amount of money for the entry.

        Returns:
            The amount of money for the entry.
        """
        return self._amount

    def is_debit(self) -> bool:
        """Check if the entry is a debit.

        Returns:
            True iff the entry is a debit.
        """
        return self._is_debit
