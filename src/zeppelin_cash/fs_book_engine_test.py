"""The module medici.test_fs_book_engine test the FsBookEngine
implementation."""
from datetime import datetime, timedelta

from zeppelin_cash.accounting.book import Book, default_cash_id, default_capital_stock_id
from zeppelin_cash.fs_book_engine import FsBookEngine
from zeppelin_cash.accounting.journal_transaction import JournalTransaction
from zeppelin_cash.accounting.journal_entry import JournalEntry
from zeppelin_cash.accounting.money import Money
from zeppelin_cash.accounting.america import usd


def test_fs_book_engine() -> None:
    """Test the FsBookEngine implementation."""
    start = datetime.now()
    book = Book(start)
    err = book.add_transaction(
        JournalTransaction(
            start + timedelta(seconds=1),
            "Investing some cash",
            [JournalEntry(default_capital_stock_id(), False, Money(1000000, usd())),
             JournalEntry(default_cash_id(), True, Money(1000000, usd()))]))
    assert err.is_ok()
    bs_result = book.balance_sheet(start + timedelta(seconds=2))
    assert bs_result.is_ok()
    balance_sheet = bs_result.ok()
    assert balance_sheet.cash.quantity() == 1000000
    assert balance_sheet.shareholders_equity().quantity() == 1000000
    engine = FsBookEngine("/tmp/book.p")
    engine.write_book(book)
    book_result = engine.load_book()
    assert book_result.is_ok()
    book = book_result.ok()
    bs_result = book.balance_sheet(start + timedelta(seconds=2))
    assert bs_result.is_ok()
    balance_sheet = bs_result.ok()
    assert balance_sheet.cash.quantity() == 1000000
    assert balance_sheet.shareholders_equity().quantity() == 1000000
