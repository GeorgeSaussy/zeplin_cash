from copy import deepcopy

from zeppelin_cash.accounting.book import Book
from zeppelin_cash.book_engine import BookEngine
from zeppelin_cash.errors.result import Result
from zeppelin_cash.user import UserId


class MemoryBookEngine(BookEngine):
    def __init__(self, book: Book) -> None:
        self.__book = book

    def book(self, _user_id: UserId) -> Result[Book]:
        return Result.of_ok(deepcopy(self.__book))
