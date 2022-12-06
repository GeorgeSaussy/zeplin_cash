from datetime import datetime, timedelta
from typing import Optional

from zeppelin_cash.accounting.account import Account
from zeppelin_cash.accounting.account_entry import AccountEntry
from zeppelin_cash.accounting.account_metadata import AccountMetadata
from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.money import Money


def test_account_metadata() -> None:
    """Check that account metadata can correctly be read."""
    def check_metadata(metadata: AccountMetadata,
                       balance: Optional[Money]) -> bool:
        assert metadata.name == "My Account"
        assert metadata.is_asset == True
        assert metadata.account_id == "1234"
        assert metadata.balance == balance
        return True

    account = Account("My Account", True, "1234")
    start = datetime.now()
    account.set_starting_balance(start, Money(0, usd()))
    metadata = account.metadata(start + timedelta(seconds=1))
    assert check_metadata(metadata, Money(0, usd()))

    metadata = account.metadata(start + timedelta(seconds=4))
    assert check_metadata(metadata, Money(0, usd()))

    entry = AccountEntry(start + timedelta(seconds=3), Money(100, usd()))
    assert account.add_entry(True, entry).is_ok()
    metadata = account.metadata(start + timedelta(seconds=4))
    assert check_metadata(metadata, Money(100, usd()))

    entry = AccountEntry(start + timedelta(seconds=6), Money(10, usd()))
    assert account.add_entry(True, entry).is_ok()
    metadata = account.metadata(start + timedelta(seconds=4))
    assert check_metadata(metadata, Money(100, usd()))
    metadata = account.metadata(start + timedelta(seconds=7))
    assert check_metadata(metadata, Money(110, usd()))
    assert metadata.balance == account.balance()

    metadata = account.metadata(start - timedelta(seconds=1))
    assert check_metadata(metadata, None)
