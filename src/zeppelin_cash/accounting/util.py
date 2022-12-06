"""The module wallet.accounting.util contains some generic test code."""
# pylint: disable=R0801
# pylint: disable=R0911
from zeppelin_cash.accounting.currency import Currency
from zeppelin_cash.accounting import america


def get_currency(code: str) -> Currency:
    """Get the currency for a given currency code.

    Returns:
        A currency instance.
    """
    if code == "USD":
        return america.usd()
    if code == "ARS":
        return america.ars()
    if code == "BRL":
        return america.brl()
    if code == "CAD":
        return america.cad()
    if code == "CLP":
        return america.clp()
    if code == "COP":
        return america.cop()
    if code == "MXN":
        return america.mxn()
    if code == "PEN":
        return america.pen()
    if code == "PEI":
        return america.pei()
    if code == "PEH":
        return america.peh()
    if code == "TTD":
        return america.ttd()
    if code == "VEB":
        return america.veb()
    # Create a new, default currency
    return Currency("", code)
