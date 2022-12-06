from datetime import datetime
from enum import auto, Enum
from os import listdir, makedirs
from os.path import exists, isdir
from typing import List, Optional

from zeppelin_cash.accounting.account import Account
from zeppelin_cash.accounting.account_metadata import AccountMetadata
from zeppelin_cash.accounting.book import Book
from zeppelin_cash.accounting.financial_statement import FinancialStatement
from zeppelin_cash.accounting.journal_transaction import JournalTransaction
from zeppelin_cash.book_engine import BookEngine, UserId
from zeppelin_cash.memory_book_engine import MemoryBookEngine
from zeppelin_cash.fs_book_engine import FsBookEngine
from zeppelin_cash.client import AccountId
from zeppelin_cash.errors import Error, ok, Result


class LMCOpenType(Enum):
    OpenDirectory = auto()
    CreateDirectory = auto()
    OpenOrCreateDirectory = auto()
    UseMemory = auto()


class LocalMultiClient:

    def __init__(
            self, dir_name: Optional[str], open_type: LMCOpenType, start: Optional[datetime] = None) -> None:
        self.__dir_name = dir_name
        self.__open_type = open_type
        self.__start = start
        self.__book_engine: Optional[BookEngine] = None

    def init(self) -> Error:
        if self.__dir_name is None:
            assert self.__open_type == LMCOpenType.UseMemory
            assert self.__start is not None
            self.__book_engine = MemoryBookEngine(Book(self.__start))
            return ok()
        assert self.__dir_name is not None
        assert self.__open_type != LMCOpenType.UseMemory
        if self.__open_type == LMCOpenType.OpenDirectory or self.__open_type == LMCOpenType.OpenOrCreateDirectory:
            self.__book_engine = FsBookEngine(self.__dir_name)
            return ok()
        assert self.__open_type == LMCOpenType.OpenOrCreateDirectory or self.__open_type == LMCOpenType.CreateDirectory

        # make sure a book engine directory exists and is empty
        if exists(self.__dir_name):
            if not isdir(self.__dir_name) or len(
                    listdir(self.__dir_name)) != 0:
                return Error("directory name already in use")
        else:
            makedirs(self.__dir_name)

        self.__book_engine = FsBookEngine(self.__dir_name)
        return ok()

    @staticmethod
    def open_directory(cls, dir_name: str) -> Result["LocalMultiClient"]:
        client = LocalMultiClient(dir_name, LMCOpenType.OpenDirectory)
        err = client.init()
        return Result(ok=client) if err.is_ok() else Result(err=err)

    @staticmethod
    def create_directory(cls, dir_name: str) -> Result["LocalMultiClient"]:
        client = LocalMultiClient(dir_name, LMCOpenType.CreateDirectory)
        err = client.init()
        return Result(ok=client) if err.is_ok() else Result(err=err)

    @staticmethod
    def open_or_create_directory(
            cls, dir_name: str) -> Result["LocalMultiClient"]:
        client = LocalMultiClient(dir_name, LMCOpenType.OpenOrCreateDirectory)
        err = client.init()
        return Result(ok=client) if err.is_ok() else Result(err=err)

    @staticmethod
    def make_in_memory(cls, start: datetime) -> "LocalMultiClient":
        client = LocalMultiClient(None, LMCOpenType.UseMemory)
        assert client.init().is_ok()
        return client

    def financial_statement(self, user_id: UserId, start: datetime,
                            end: datetime) -> Result[FinancialStatement]:
        raise NotImplementedError()

    def list_accounts(self, user_id: UserId,
                      start: datetime) -> Result[List[AccountMetadata]]:
        raise NotImplementedError()

    def add_account(self, user_id: UserId, account_name: str,
                    is_asset: bool) -> Result[AccountId]:
        raise NotImplementedError()

    def get_account(self, user_id: UserId,
                    account_id: AccountId) -> Result[Account]:
        raise NotImplementedError()

    def add_transaction(self, user_id: UserId,
                        txn: JournalTransaction) -> Error:
        raise NotImplementedError()
