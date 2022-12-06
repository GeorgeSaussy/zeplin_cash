"""The module wallet.accounting.test_journal_entry tests the
JournalEntry implementation."""
from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.journal_entry import JournalEntry
from zeppelin_cash.accounting.money import Money


def test_journal_entry() -> None:
    """Test that a journal entry works as expected."""
    entry = JournalEntry("some-id", True, Money(1337.00, usd()))
    amount = entry.amount()
    assert amount.currency().code() == "USD"
    assert amount.quantity() == 1337.00
    assert entry.is_debit()
    entry = JournalEntry("another-id", False, Money(42.42, usd()))
    amount = entry.amount()
    assert amount.currency().code() == "USD"
    assert amount.quantity() == 42.42
    assert not entry.is_debit()
