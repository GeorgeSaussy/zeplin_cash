"""The module wallet.accounting.test_book test the Book implementation."""
from datetime import datetime, timedelta

from zeppelin_cash.accounting.book import Book, default_cash_id, default_capital_stock_id
from zeppelin_cash.accounting.journal_transaction import JournalTransaction
from zeppelin_cash.accounting.journal_entry import JournalEntry
from zeppelin_cash.accounting.money import Money
from zeppelin_cash.accounting.america import usd


def test_book_init() -> None:
    """Test that a Book instance can be created."""
    start = datetime.now()
    book = Book(start)
    assert book.is_valid()
    result = book.financial_statement(start, start + timedelta(seconds=1))
    assert result.is_ok()
    financial_statement = result.ok()
    assert financial_statement.is_valid()


def test_balance_sheet() -> None:
    """Test that we can get a balance sheet from the book."""
    start = datetime.now()
    book = Book(start)
    err = book.add_transaction(
        JournalTransaction(
            start + timedelta(seconds=1),
            "Investing some cash",
            [JournalEntry(default_capital_stock_id(), False, Money(1000000, usd())),
             JournalEntry(default_cash_id(), True, Money(1000000, usd()))]))
    assert err.is_ok()
    result = book.balance_sheet(start + timedelta(seconds=2))
    assert result.is_ok()
    balance_sheet = result.ok()
    assert balance_sheet.cash.quantity() == 1000000
    assert balance_sheet.shareholders_equity().quantity() == 1000000


def test_add_bad_transaction() -> None:
    """Test that a bad transaction is rejected."""
    start = datetime.now()
    book = Book(start)
    err = book.add_transaction(
        JournalTransaction(
            start + timedelta(seconds=1),
            "Investing some cash",
            [JournalEntry(default_capital_stock_id(), True, Money(1000000, usd())),
             JournalEntry(default_cash_id(), True, Money(1000000, usd()))]))
    assert not err.is_ok()


def test_new_account_id() -> None:
    """Test that a new account can be created and used."""
    start = datetime.now()
    book = Book(start)
    # Invest some cash.
    err = book.add_transaction(
        JournalTransaction(
            start + timedelta(seconds=1),
            "Investing some cash",
            [JournalEntry(default_capital_stock_id(), False, Money(1000000, usd())),
             JournalEntry(default_cash_id(), True, Money(1000000, usd()))]))
    assert err.is_ok()
    # Open a new cash account.
    new_cash_id = book.add_cash_account("New Account")
    err = book.add_transaction(
        JournalTransaction(
            start + timedelta(seconds=2),
            "Transfer cash",
            [JournalEntry(default_cash_id(), False, Money(500000, usd())),
             JournalEntry(new_cash_id, True, Money(500000, usd()))]))
    assert err.is_ok()
    money_result = book.ledger.balance_as_of_date(
        start + timedelta(seconds=3), default_cash_id())
    assert money_result.is_ok()
    assert money_result.ok().quantity() == 500000
    money_result = book.ledger.balance_as_of_date(
        start + timedelta(seconds=3), new_cash_id)
    assert money_result.is_ok()
    assert money_result.ok().quantity() == 500000
    bs_result = book.balance_sheet(start + timedelta(seconds=3))
    assert bs_result.is_ok()
    balance_sheet = bs_result.ok()
    assert balance_sheet.cash.quantity() == 1000000


def test_cash_flow_statement() -> None:
    """Check that a cash flow statement can be calculated from the book."""
    start = datetime.now()
    book = Book(start)
    err = book.add_transaction(
        JournalTransaction(
            start + timedelta(seconds=1),
            "Investing some cash",
            [JournalEntry(default_capital_stock_id(), False, Money(1000000, usd())),
             JournalEntry(default_cash_id(), True, Money(1000000, usd()))]))
    assert err.is_ok()
    cf_result = book.cash_flow_statement(start, start + timedelta(seconds=2))
    assert cf_result.is_ok()
    cash_flow_statement = cf_result.ok()
    assert cash_flow_statement.sale_of_stock.quantity() == 1000000
    cf_result = book.cash_flow_statement(
        start +
        timedelta(
            seconds=365),
        start +
        timedelta(
            seconds=356))
    assert cf_result.is_ok()
    cash_flow_statement = cf_result.ok()
    assert cash_flow_statement.cash_disbursements.quantity() == 0


def test_income_statement() -> None:
    """Check that an income statement can be calculated from the book."""
    start = datetime.now()
    book = Book(start)
    err = book.add_transaction(
        JournalTransaction(
            start + timedelta(seconds=1),
            "Investing some cash",
            [JournalEntry(default_capital_stock_id(), False, Money(1000000, usd())),
             JournalEntry(default_cash_id(), True, Money(1000000, usd()))]))
    assert err.is_ok()
    rnd_id = book.add_research_and_development_account("Prototype shop")
    err = book.add_transaction(
        JournalTransaction(
            start + timedelta(seconds=2),
            "Paying for a prototype",
            [JournalEntry(default_cash_id(), False, Money(100000, usd())),
             JournalEntry(rnd_id, True, Money(100000, usd()))]))
    assert err.is_ok()
    is_result = book.income_statement(start, start + timedelta(seconds=3))
    assert is_result.is_ok()
    income_statement = is_result.ok()
    assert income_statement.research_and_development.quantity() == 100000
