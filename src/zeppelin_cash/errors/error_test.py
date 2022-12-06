"""Test the wallet.errors.error module."""
from zeppelin_cash.errors.error import Error


def test_error() -> None:
    """Test the Error implementation."""
    err = Error("bonsoir elliot")
    assert err.message() == "bonsoir elliot"
    assert not err.is_ok()
    err = Error()
    assert err.message() == ""
    assert err.is_ok()
