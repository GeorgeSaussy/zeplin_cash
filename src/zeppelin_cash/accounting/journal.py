"""The module wallet.accounting.journal contains the Journal class implementation."""
from typing import List

from zeppelin_cash.accounting.journal_transaction import JournalTransaction
from zeppelin_cash.errors import Error, ok


class Journal:
    """This is the general journal."""

    def __init__(self) -> None:
        """Create a new Journal instance."""
        self.transactions: List[JournalTransaction] = []
        self._pushed_index = 0

    def add_transaction(self, transaction: JournalTransaction) -> Error:
        """Add a transaction to the journal.

        This will fail if the transactions' associated times are not added in order.

        Args:
            transaction: the transaction to append.

        Returns:
            An error if an error occurs.
        """
        if not transaction.is_valid():
            return Error("invalid transaction")
        len_tran = len(self.transactions)
        if len_tran > 0:
            if self.transactions[len_tran - 1].time() > transaction.time():
                return Error("invalid transaction time")
        self.transactions.append(transaction)
        return ok()

    def is_valid(self) -> bool:
        """Check if a Journal is valid.

        Returns:
            True iff the transaction is valid.
        """
        for transaction in self.transactions:
            if not transaction.is_valid():
                return False
        return True

    def un_pushed_transactions(self) -> List[JournalTransaction]:
        """Get a list of all un-pushed transactions.

        Returns:
            A list of all un-pushed transactions.
        """
        return self.transactions[self._pushed_index:]

    def have_pushed(self, num_pushed: int) -> Error:
        """Set some number of transactions to have been pushed.

        Args:
            num_pushed the number pushed

        Returns:
            An error if the number pushed is greater than the number of un-pushed transactions.
        """
        if num_pushed > len(self.transactions) - self._pushed_index:
            return Error(
                "the number pushed is greater than the number of un-pushed transactions")
        self._pushed_index += num_pushed
        return ok()
