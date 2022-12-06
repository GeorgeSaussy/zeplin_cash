"""Test the wallet.errors.either module."""
from zeppelin_cash.errors.either import Either, EitherException


def test_first() -> None:
    """Check that the first type can be used."""
    either = Either[int, str](first=42)
    assert either.first() == 42
    assert either.is_first()
    either = Either[int, str].of_first(42)
    assert either.first() == 42
    try:
        either.second()
        assert False
    except EitherException:
        pass


def test_second() -> None:
    """Check that the second type can be used."""
    either = Either[int, str](second="bonsoir elliot")
    assert either.second() == "bonsoir elliot"
    assert not either.is_first()
    either = Either[int, str].of_second("bonsoir elliot")
    assert either.second() == "bonsoir elliot"
    try:
        either.first()
        assert False
    except EitherException:
        pass


def test_either_init() -> None:
    """Test that the implementation throws an exception for bad parameters."""
    try:
        Either[int, str](first=42, second="bonsoir elliot")
        assert False
    except EitherException:
        pass
    try:
        Either[int, str]()
        assert False
    except EitherException:
        pass
