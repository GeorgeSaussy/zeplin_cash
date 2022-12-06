from datetime import datetime
from enum import auto, Enum
from typing import List, Optional, Tuple

from zeppelin_cash.accounting.account import Account, AccountId
from zeppelin_cash.accounting.account_metadata import AccountMetadata
from zeppelin_cash.accounting.book import Book
from zeppelin_cash.accounting.financial_statement import FinancialStatement
from zeppelin_cash.accounting.journal_transaction import JournalTransaction
from zeppelin_cash.book_engine import UserId
from zeppelin_cash.client import Client
from zeppelin_cash.errors import Error, Result
from zeppelin_cash.local_multi_client import LocalMultiClient


class LocalClient(Client):
    """A Client can read from the treasury service."""

    def __init__(self, start: Optional[datetime] = None,
                 multi_client: Optional[Tuple[UserId, LocalMultiClient]] = None) -> None:
        self.__in_memory_book: Optional[Book] = None
        self.__user_id: Optional[UserId] = None
        self.__local_multi_client: Optional[LocalMultiClient] = None

        if multi_client is None:
            assert start is not None
            self.__in_memory_book = Book(start)
            return

        assert start is None
        self.__user_id = multi_client[0]
        self.__local_multi_client = multi_client[1]

    def financial_statement(self, start: datetime,
                            end: datetime) -> Result[FinancialStatement]:
        if self.__in_memory_book is not None:
            return self.__in_memory_book.financial_statement(start, end)
        assert self.__user_id is not None
        assert self.__local_multi_client is not None
        return self.__local_multi_client.financial_statement(
            self.__user_id, start, end)

    def list_accounts(
            self, timestamp: datetime) -> Result[List[AccountMetadata]]:
        if self.__in_memory_book is not None:
            return Result(ok=self.__in_memory_book.list_accounts(timestamp))
        assert self.__user_id is not None
        assert self.__local_multi_client is not None
        return self.__local_multi_client.list_accounts(
            self.__user_id, timestamp)

    def add_account(self, account_name: str,
                    is_asset: bool) -> Result[AccountId]:
        if self.__in_memory_book is not None:
            account_id = self.__in_memory_book.add_account(
                account_name, is_asset)
            return Result(ok=account_id)
        assert self.__user_id is not None
        assert self.__local_multi_client is not None
        return self.__local_multi_client.add_account(
            self.__user_id, account_name, is_asset)

    def get_account(self, account_id: AccountId) -> Result[Account]:
        if self.__in_memory_book is not None:
            # TODO(OMEGA-411): Implement this.
            raise NotImplementedError()
        assert self.__user_id is not None
        assert self.__local_multi_client is not None
        return self.__local_multi_client.get_account(
            self.__user_id, account_id)

    def add_transaction(self, txn: JournalTransaction) -> Error:
        if self.__in_memory_book is not None:
            return self.__in_memory_book.add_transaction(txn)
        assert self.__user_id is not None
        assert self.__local_multi_client is not None
        return self.__local_multi_client.add_transaction(self.__user_id, txn)
