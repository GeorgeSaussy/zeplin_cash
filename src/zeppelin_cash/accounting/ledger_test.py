"""The module wallet.accounting.test_ledger tests the Ledger implementation."""
from datetime import datetime, timedelta

from zeppelin_cash.accounting.account import Account
from zeppelin_cash.accounting.account_entry import AccountEntry
from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.ledger import Ledger
from zeppelin_cash.accounting.money import Money


def basic_ledger(start: datetime) -> Ledger:
    """Get a simple ledger instance."""
    cash = Account("cash", True, "cash-id")
    cash.set_starting_balance(start, Money(1337, usd()))
    debt = Account("debt", False, "debt-id")
    debt.set_starting_balance(start, Money(42, usd()))
    return Ledger([cash, debt])


def test_ledger_init() -> None:
    """Test that a new Ledger instance can be created."""
    start = datetime.now()
    ledger = basic_ledger(start)
    result = ledger.balance_as_of_date(start + timedelta(seconds=1), "cash-id")
    assert result.is_ok()
    assert result.ok().quantity() == 1337
    assert not ledger.balance_as_of_date(
        start + timedelta(seconds=1), "nonce-id").is_ok()


def test_adding_account() -> None:
    """Test that an account can be added to the ledger."""
    start = datetime.now()
    ledger = basic_ledger(start)
    account = Account("equipment", True, "equip-id")
    account.set_starting_balance(
        start + timedelta(seconds=50), Money(1234, usd()))
    assert ledger.add_account(account).is_ok()
    result = ledger.balance_as_of_date(
        start + timedelta(seconds=51), "equip-id")
    assert result.is_ok()
    assert result.ok().quantity() == 1234
    account = Account("more equipment", True, "equip-id")
    assert not ledger.add_account(account).is_ok()


def test_add_entry() -> None:
    """Check that an entry can be added to the ledger."""
    start = datetime.now()
    increment = start + timedelta(seconds=1)
    ledger = basic_ledger(start)
    result = ledger.balance_as_of_date(increment, "cash-id")
    assert result.is_ok()
    start_balance = result.ok()
    entry = AccountEntry(increment, Money(15, usd()))
    assert ledger.add_entry("cash-id", True, entry).is_ok()
    increment += timedelta(seconds=1)
    result = ledger.balance_as_of_date(increment, "cash-id")
    assert result.is_ok()
    assert result.ok().quantity() == start_balance.quantity() + 15
    assert not ledger.add_entry("nonce-id", True, entry).is_ok()
    result = ledger.balance_as_of_date(increment, "cash-id")
    assert result.is_ok()
    assert result.ok().quantity() == start_balance.quantity() + 15


def test_list_accounts() -> None:
    """Check that all accounts can be listed."""
    start = datetime.now()
    ledger = basic_ledger(start)
    metadata = ledger.list_accounts(start + timedelta(seconds=1))
    assert len(metadata) == 2
    for my_metadata in metadata:
        if my_metadata.name == "cash":
            assert my_metadata.balance == Money(1337, usd())
            continue
        assert my_metadata.name == "debt"
        assert my_metadata.balance == Money(42, usd())
