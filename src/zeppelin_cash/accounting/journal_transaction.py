"""The module wallet.accounting.journal_transaction contains the
JournalTransaction implementation."""
from typing import List
from datetime import datetime

from zeppelin_cash.accounting.journal_entry import JournalEntry


class JournalTransaction:
    """A JournalTransaction instance represents a set of journal transactions.

    The transactions are part of a single change to the general ledger, such that
    the sum of credits and debits is zero.
    """

    def __init__(self, time: datetime, description: str,
                 entries: List[JournalEntry]) -> None:
        """Create a new JournalTransaction instance.

        Args:
            time: the time of the transaction
            description: a plain text description of the transaction
            entries: the entries in the transaction
        """
        self._time = time
        self.description = description
        self._entries = entries

    def is_valid(self) -> bool:
        """Check if a transaction is valid.

        Returns:
            True iff the transaction is valid
        """
        if len(self._entries) == 0:
            # XXX: Is this the correct policy?
            return True
        code = self._entries[0].amount().currency().code()
        for entry in self._entries:
            if entry.amount().currency().code() != code:
                return False
        my_credits = []  # there is already a built-in 'credits'
        debits = []
        for entry in self._entries:
            if entry.is_debit():
                debits.append(entry)
            else:
                my_credits.append(entry)
        if len(my_credits) == 0 or len(debits) == 0:
            return False
        credit = my_credits[0].amount()
        for k in range(1, len(my_credits)):
            credit += my_credits[k].amount()
        debit = debits[0].amount()
        for k in range(1, len(debits)):
            debit += debits[k].amount()
        assert credit.currency().code() == debit.currency().code()
        return credit.quantity() == debit.quantity()

    def time(self) -> datetime:
        """Get the time of the transaction.

        Returns:
            The time.
        """
        return self._time

    def entries(self) -> List[JournalEntry]:
        """Get the journal entries.

        Returns:
            A list of entries.
        """
        return self._entries
