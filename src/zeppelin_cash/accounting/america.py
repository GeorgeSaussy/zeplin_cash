"""The module wallet.accounting.america contains helper functions for
creating currencies from the Americas."""
from zeppelin_cash.accounting.currency import Currency


def usd() -> Currency:
    """Create a US dollar.

    Returns:
        A new Currency instance.
    """
    return Currency("US dollar", "USD", numeric_code=840,
                    symbol="$", fraction_symbol="¢")


def ars() -> Currency:
    """Create an Argentinian peso.

    Returns:
        A new Currency instance.
    """
    return Currency("Argentinian peso", "ARS", numeric_code=32)


def brl() -> Currency:
    """Create a Brazilian real.

    Returns:
        A new Currency instance.
    """
    return Currency("Brazilian real", "BRL", numeric_code=986, symbol="R$")


def cad() -> Currency:
    """Create a Canadian dollar.

    Returns:
        A new Currency instance.
    """
    return Currency("Canadian dollar", "CAD", numeric_code=124, symbol="Can$")


def clp() -> Currency:
    """Create a Chilean peso.

    Returns:
        A new Currency instance.
    """
    return Currency("Chilean peso", "CLP", numeric_code=152, symbol="Cs$")


def cop() -> Currency:
    """Create a Columbian peso.

    Returns:
        A new Currency instance.
    """
    return Currency("Columbian peso", "COP", numeric_code=170, symbol="Col$")


def mxn() -> Currency:
    """Create a Mexican peso.

    Returns:
        A new Currency instance.
    """
    return Currency("Mexican peso", "MXN", numeric_code=484, symbol="Mex$")


def pen() -> Currency:
    """Create a Peruvian nuevo sol.

    Returns:
        A new Currency instance.
    """
    return Currency("Peruvian nuevo sol", "PEN",
                    numeric_code=604, symbol="S/.")


def pei() -> Currency:
    """Create a Peruvian inti.

    Returns:
        A new Currency instance.
    """
    return Currency("Peruvian inti", "PEI", numeric_code=0, symbol="I/.")


def peh() -> Currency:
    """Create a Peruvian sol.

    Returns:
        A new Currency instance.
    """
    return Currency("Peruvian sol", "PEH", numeric_code=0, symbol="S./")


def ttd() -> Currency:
    """Create a Trinidad & Tobago dollar.

    Returns:
        A new Currency instance.
    """
    return Currency("Trinidad & Tobago dollar", "TTD",
                    numeric_code=840, symbol="TT$")


def veb() -> Currency:
    """Create a Venezuelan bolivar.

    Returns:
        A new Currency instance.
    """
    return Currency("Venezuelan bolivar", "VEB", numeric_code=862, symbol="Bs")
