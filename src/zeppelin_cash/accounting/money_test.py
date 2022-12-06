"""Test the money implementation."""
from zeppelin_cash.accounting.america import ars, usd
from zeppelin_cash.accounting.money import Money


def test_money_init() -> None:
    """Test that the Money implementation works as expected."""
    money = Money(0.42, usd())
    assert str(money) == "0.42 USD"
    money = Money(1234567, usd())
    assert str(money) == "1,234,567.00 USD"
    # rounding is undefined
    money = Money(0.1337, usd())
    assert str(money) in ["0.13 USD", "0.14 USD"]
    money1 = Money(10.0, usd())
    money2 = Money(1.0, usd())
    assert str(money1 + money2) == "11.00 USD"


def test_adding_money() -> None:
    """Test that adding money types works as expected."""
    money1 = Money(100, usd())
    money2 = Money(1000, usd())
    total = money1 + money2
    assert total.quantity() == 1100
    money2 = Money(1000, ars())
    try:
        print("This should throw an exception", money1 + money2)
        assert False
    except NotImplementedError:
        pass


def test_subtracting_money() -> None:
    """Test that subtracting money types works as expected."""
    money1 = Money(1000, usd())
    money2 = Money(100, usd())
    diff = money1 - money2
    assert diff.quantity() == 900
    money2 = Money(100, ars())
    try:
        print("This should throw an exception", money1 - money2)
        assert False
    except NotImplementedError:
        pass


def test_scale_money() -> None:
    """Check that Money instances can be scaled."""
    start = Money(10, usd())
    finish = start.scale(10)
    assert finish.quantity() == 100
