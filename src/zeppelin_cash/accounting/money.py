"""The wallet.accounting.money contains the Money implementation."""
from zeppelin_cash.accounting.currency import Currency


class Money:
    """Money encapsulates some amount of a given currency."""

    def __init__(self, quantity: float, currency: Currency) -> None:
        """Create a new Money instance.

        Args:
            quantity: the amount of the currency
            currency: the currency of the money
        """
        self.__quantity = quantity
        self.__currency = currency

    def currency(self) -> Currency:
        """Get the money's currency.

        Returns:
            The money's currency.
        """
        return self.__currency

    def quantity(self) -> float:
        """Get the quantity of the money.

        Returns:
            The quantity of the money.
        """
        return self.__quantity

    def scale(self, factor: float) -> 'Money':
        """Scale the money by a float.

        Args:
            f: the float to by which to scale

        Returns:
            A scaled Money instance.
        """
        return Money(factor * self.quantity(), self.currency())

    def __add__(self, other: 'Money') -> 'Money':
        """Add some money together.

        Args:
            other: the other Money instance

        Returns:
            The sum of self and other.
        """
        if self.currency().code() != other.currency().code():
            raise NotImplementedError()
        return Money(self.quantity() + other.quantity(), self.currency())

    def __sub__(self, other: 'Money') -> 'Money':
        """Subtract some money.

        Args:
            other: the money to subtract

        Returns:
            the difference
        """
        if self.currency().code() != other.currency().code():
            raise NotImplementedError()
        return Money(self.quantity() - other.quantity(), self.currency())

    def __eq__(self, other: object) -> bool:
        """Check if the object is equivalent to another.

        Args:
            other: the other object

        Returns:
            True iff they are the same, False otherwise.
        """
        if isinstance(other, Money):
            return self.currency().code() == other.currency(
            ).code() and self.quantity() == other.quantity()
        return False

    def __str__(self) -> str:
        """Get a string representation of Currency.

        Returns:
            The Currency instance as a string.
        """
        str_quant = str(int(self.quantity() * 100.0))
        if len(str_quant) <= 2:
            return "0." + str_quant + " " + self.currency().code()
        cents = str_quant[-2:]
        dollars = str_quant[:-2]
        chars = dollars
        ret = "." + cents + " " + self.currency().code()
        for k in range(len(chars)):
            char = chars[len(chars) - k - 1]
            ret = char + ret
            if k % 3 == 2 and k != len(chars) - 1:
                ret = ',' + ret
        return ret
