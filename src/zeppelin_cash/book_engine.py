"""The module medici.book_engine contains a abstract book storage engine implementation."""
from abc import ABC, abstractmethod
from zeppelin_cash.accounting.book import Book
from zeppelin_cash.errors import Error, Result
from zeppelin_cash.user import UserId

"""
There are a few tables that are maintained:
    - users:
        - user_id: str
        - name: str
    - api_keys:
        - key: str
        - user_id: str, fk to users
    - ledgers:
        - user_id: str, fk to users
    - account_types:
        - account_type_id: str
        - name: str
    - accounts:
        - account_id: str
        - name: str
        - is_asset: bool
        - ledger_id: str, fk to ledgers
        - initial_balance: float, money
        - open_date: int, float, posix timestamp
    - transactions:
        - transaction_id: str
        - timestamp: int, posix timestamp
    - account_entries:
        - account_id: str, fk to accounts
        - transaction_id: str, fk to transactions
        - is_debit: bool
"""


class BookEngine(ABC):
    """BookEngine is an abstract book storage class.

    The expectation is that for each book backend, this class will be implemented.
    """

    @abstractmethod
    def book(self, user_id: UserId) -> Result[Book]:
        """Get a copy of the internal book object.

        Updates to this book will not be reflected in the stored book.
        """
        raise NotImplementedError()
