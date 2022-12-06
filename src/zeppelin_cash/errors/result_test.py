"""Test the wallet.errors.result module."""
from zeppelin_cash.errors.error import Error
from zeppelin_cash.errors.result import Result, ResultException


def test_bad_init() -> None:
    """Check that a bad init function will throw an exception."""
    try:
        Result[str](ok="bonsoir", err=Error("elliot"))
        assert False
    except ResultException:
        pass
    try:
        Result[str](ok=None, err=None)
        assert False
    except ResultException:
        pass


def test_ok_init() -> None:
    """Check that a result can also be created correctly."""
    result = Result[str](ok="bonsoir")
    assert result.is_ok()
    assert result.ok() == "bonsoir"
    try:
        result.err()
        assert False
    except ResultException:
        pass
    result = Result[str](err=Error("elliot"))
    assert not result.is_ok()
    assert result.err().message() == "elliot"
    try:
        result.ok()
        assert False
    except ResultException:
        pass
