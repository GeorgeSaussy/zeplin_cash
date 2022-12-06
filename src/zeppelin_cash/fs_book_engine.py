"""The medici.fs_book_engine allows a book to sync to the file system."""
from typing import Optional
import pickle

from zeppelin_cash.book_engine import BookEngine
from zeppelin_cash.accounting.book import Book
from zeppelin_cash.errors import Error, ok, Result
from zeppelin_cash.user import UserId


class FsBookEngine(BookEngine):
    """The FsBookEngine allow a book to be synced to a file system."""

    def __init__(self, fname: str) -> None:
        """Create a new FsBookEngine instance.

        Args:
            fname: the name of the file with which to sync
        """
        self.fname = fname

    def load_book(self) -> Result[Book]:
        """Load a book from the file system.

        Returns:
            A Book instance or an error.
        """
        with open(self.fname, "rb") as my_file:
            book = pickle.load(my_file)
        return Result(ok=book)

    def write_book(self, book: Book) -> Error:
        """Write a book to the file system.

        Returns:
            An error if the write fails.
        """
        with open(self.fname, "wb") as my_file:
            pickle.dump(book, my_file)
        return ok()

    def book(self, _user_id: UserId) -> Result[Book]:
        return self.load_book()
