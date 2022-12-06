"""Test that the currency utility methods work."""
from zeppelin_cash.accounting.america import ars, brl, cad, clp, cop, mxn, pen, pei, peh, ttd, usd, veb
from zeppelin_cash.accounting.util import get_currency


def test_get_currency() -> None:
    """Check that we can get a currency based on its ISO code."""
    currencies = [
        ars(),
        brl(),
        cad(),
        clp(),
        cop(),
        mxn(),
        pen(),
        pei(),
        peh(),
        ttd(),
        usd(),
        veb()]
    for currency in currencies:
        found = get_currency(currency.code())
        assert found.code() == currency.code()
