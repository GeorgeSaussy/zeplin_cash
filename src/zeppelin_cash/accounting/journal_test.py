"""The module wallet.accounting.test_journal tests the Journal implementation."""
from datetime import datetime, timedelta
from random import randint

from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.journal import Journal
from zeppelin_cash.accounting.journal_entry import JournalEntry
from zeppelin_cash.accounting.journal_transaction import JournalTransaction
from zeppelin_cash.accounting.money import Money


def test_journal() -> None:
    """Test that a journal works as expected."""
    journal = Journal()
    assert journal.is_valid()
    entries = [
        JournalEntry("cash-id", False, Money(3000, usd())),  # pay 30% up front
        # put 70% on credit
        JournalEntry("debt-id", False, Money(7000, usd())),
        # get $10k of 'equipment'
        JournalEntry("equipment-id", True, Money(10000, usd())),
    ]
    okay_transaction = JournalTransaction(
        datetime.now(), "Getting more equipment on credit", entries)
    assert okay_transaction.is_valid()
    journal.add_transaction(okay_transaction)
    assert journal.is_valid()
    entries = [JournalEntry("equipment-id", True, Money(10000, usd()))]
    fraudulent_transaction = JournalTransaction(
        datetime.now(), "Where is this equipment from?", entries)
    assert not fraudulent_transaction.is_valid()
    err = journal.add_transaction(fraudulent_transaction)
    assert not err.is_ok()
    assert journal.is_valid()
    # we can force a bad transaction onto the journal, but this can be
    # detected.
    journal.transactions.append(fraudulent_transaction)
    assert not journal.is_valid()


def test_add_transaction_wrong_order() -> None:
    """Test that adding a transaction fails if the times are in the wrong order."""
    journal = Journal()
    assert journal.is_valid()
    entries = [
        # pay 30% up front
        JournalEntry("cash-id", False, Money(3000, usd())),
        # put 70% on credit
        JournalEntry("debt-id", False, Money(7000, usd())),
        # get $10k of 'equipment'
        JournalEntry("equipment-id", True, Money(10000, usd())),
    ]
    first_time = datetime.now()
    second_time = first_time + timedelta(seconds=1)
    transaction1 = JournalTransaction(
        second_time, "Getting more equipment on credit", entries)
    assert transaction1.is_valid()
    journal.add_transaction(transaction1)
    assert journal.is_valid()
    entries = [
        JournalEntry("cash-id", False, Money(1000, usd())),
        JournalEntry("equipment-id", True, Money(1000, usd())),
    ]
    transaction2 = JournalTransaction(
        first_time, "Buy more equipment for cash", entries)
    assert transaction2.is_valid()
    err = journal.add_transaction(transaction2)
    assert not err.is_ok()
    assert journal.is_valid()


def test_transaction_publishing() -> None:
    """Test that a journal's transaction publishing works as expected."""
    num_transactions = 100
    num_entries_per_transaction = 100
    journal = Journal()
    assert journal.is_valid()
    ongoing_time = datetime.now()
    for i in range(num_transactions):
        num_debit = randint(1, num_entries_per_transaction - 1)
        entries = [
            JournalEntry(
                str(k),
                k >= num_debit,
                Money(
                    randint(
                        1,
                        1000),
                    usd())) for k in range(num_entries_per_transaction)]
        total = Money(0, usd())
        for entry in entries:
            total += entry.amount() if entry.is_debit() else entry.amount().scale(-1)
        entries.append(JournalEntry("final", True, total.scale(-1)))
        ongoing_time += timedelta(seconds=1)
        transaction = JournalTransaction(ongoing_time, str(i), entries)
        assert transaction.is_valid()
        err = journal.add_transaction(transaction)
        assert err.is_ok()
        assert journal.is_valid()
    unpublished = journal.un_pushed_transactions()
    assert len(unpublished) == num_transactions
    err = journal.have_pushed(10)
    assert err.is_ok()
    unpublished = journal.un_pushed_transactions()
    assert len(unpublished) == num_transactions - 10
    err = journal.have_pushed(num_transactions)
    assert not err.is_ok()
