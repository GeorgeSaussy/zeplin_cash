"""The module wallet.accounting.test_account tests the Account implementation."""
from datetime import datetime, timedelta

from zeppelin_cash.accounting.account import Account
from zeppelin_cash.accounting.account_entry import AccountEntry
from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.money import Money


def test_account_init() -> None:
    """Test that an Account instance can be created."""
    account = Account("My Account", True, "1234")
    assert account.id() == "1234"
    assert account.balance().quantity() == 0


def test_computing_balance() -> None:
    """Check that the balance can be computed."""
    account = Account("My Account", True, "1234")
    start = datetime.now()
    account.set_starting_balance(start, Money(0, usd()))
    assert account.balance().quantity() == 0
    entry = AccountEntry(start + timedelta(seconds=1), Money(100, usd()))
    assert account.add_entry(True, entry).is_ok()
    entry = AccountEntry(start + timedelta(seconds=2), Money(10, usd()))
    assert account.add_entry(False, entry).is_ok()
    assert account.balance().quantity() == 90
    result = account.balance_as_of_date(
        start + timedelta(seconds=3))
    assert result.is_ok()
    assert result.ok().quantity() == 90


def test_set_starting_balance() -> None:
    """Test that we can set the starting balance of an account."""
    account = Account("My Account", True, "1234")
    some_time = datetime.now()
    money = Money(1000.00, usd())
    account.set_starting_balance(some_time, money)
    assert account.balance().quantity() == money.quantity()
    result = account.balance_as_of_date(some_time + timedelta(seconds=1))
    assert result.is_ok()
    assert result.ok().quantity() == money.quantity()
    result = account.balance_as_of_date(some_time - timedelta(seconds=1))
    assert not result.is_ok()


def test_bad_additions() -> None:
    """Check that entries can only be added in order."""
    account = Account("My Account", True, "1234")
    start = datetime.now()
    account.set_starting_balance(start, Money(0, usd()))
    assert account.balance().quantity() == 0
    entry = AccountEntry(start + timedelta(seconds=3), Money(100, usd()))
    assert account.add_entry(True, entry).is_ok()
    entry = AccountEntry(start + timedelta(seconds=2), Money(10, usd()))
    assert not account.add_entry(False, entry).is_ok()
    assert account.balance().quantity() == 100
    entry = AccountEntry(start + timedelta(seconds=6), Money(10, usd()))
    assert account.add_entry(False, entry).is_ok()
    entry = AccountEntry(start + timedelta(seconds=5), Money(50, usd()))
    assert not account.add_entry(False, entry).is_ok()
    assert account.balance().quantity() == 90
