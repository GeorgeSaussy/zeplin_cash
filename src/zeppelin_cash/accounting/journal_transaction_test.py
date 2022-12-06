"""The module wallet.accounting.test_journal_transaction tests the
JournalTransaction implementation."""
from datetime import datetime

from zeppelin_cash.accounting.america import usd, ars
from zeppelin_cash.accounting.money import Money
from zeppelin_cash.accounting.journal_entry import JournalEntry
from zeppelin_cash.accounting.journal_transaction import JournalTransaction


def test_journal_transaction() -> None:
    """Test that a journal transaction works as expected."""
    entries = [
        # pay 20% up front
        JournalEntry("cash-id", False, Money(2000, usd())),
        # put 80% on credit
        JournalEntry("debt-id", False, Money(8000, usd())),
        # get $10k of 'equipment'
        JournalEntry("equipment-id", True, Money(10000, usd())),
    ]
    okay_transaction = JournalTransaction(
        datetime.now(), "Buying equipment", entries)
    assert okay_transaction.is_valid()
    entries = [JournalEntry("equipment-id", True, Money(10000, usd()))]
    fraudulent_transaction = JournalTransaction(
        datetime.now(), "Where is this equipment from?", entries)
    assert not fraudulent_transaction.is_valid()


def test_empty_transaction_is_valid() -> None:
    """Check that an empty transaction is *technically* valid."""
    transaction = JournalTransaction(datetime.now(), "No Op", [])
    assert transaction.is_valid()


def test_multiple_debits() -> None:
    """Check that the a JournalTransaction works even if there are multiple debits."""
    entries = [
        # pay $10K
        JournalEntry("cash-id", False, Money(10000, usd())),
        # receive $8K in equipment
        JournalEntry("equipment-id", True, Money(8000, usd())),
        # receive $2K in raw materials
        JournalEntry("raw-material-id", True, Money(2000, usd())),
    ]
    deal = JournalTransaction(datetime.now(), "Deal on equipment", entries)
    assert deal.is_valid()


def test_same_currency_used() -> None:
    """Check that a transaction is not valid if the entries are not in the same currency."""
    entries = [
        JournalEntry("foo", False, Money(1, usd())),
        JournalEntry("bar", True, Money(1, ars())),
    ]
    bad_transaction = JournalTransaction(
        datetime.now(), "Foo for Bar", entries)
    assert not bad_transaction.is_valid()


def test_transaction_time() -> None:
    """Test the transaction datetime getter."""
    some_time = datetime.now()
    transaction = JournalTransaction(some_time, "Foo", [])
    assert some_time == transaction.time()


def test_transaction_entries() -> None:
    """Test the transaction entries getter."""
    entries = [
        JournalEntry("foo", False, Money(1, usd())),
        JournalEntry("bar", True, Money(1, usd())),
    ]
    transaction = JournalTransaction(datetime.now(), "Foo for Bar", entries)
    found = transaction.entries()
    assert len(found) == 2
    found0 = found[0].account_id()
    found1 = found[1].account_id()
    assert (found0 == "foo" and found1 == "bar") or (
        found0 == "bar" and found1 == "foo")
