"""Test the wallet.errors.util module."""
from zeppelin_cash.errors.util import ok


def test_ok() -> None:
    """Test the ok function."""
    err = ok()
    assert err.message() == ""
    assert err.is_ok()
