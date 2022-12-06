"""The module wallet.accounting.test_account_entry test the AccountEntry implementation."""
from datetime import datetime

from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.money import Money
from zeppelin_cash.accounting.account_entry import AccountEntry


def test_account_entry() -> None:
    """Test that an AccountEntry instance can be created."""
    some_time = datetime.now()
    money = Money(100, usd())
    entry = AccountEntry(some_time, money)
    assert entry.time() == some_time
    assert entry.amount().quantity() == 100
    assert entry.amount().currency().code() == usd().code()
