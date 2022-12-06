"""Test wallet.accounting.america implementation."""
from zeppelin_cash.accounting.america import ars, brl, cad, clp, cop, mxn, pen, pei, peh, ttd, usd, veb


def test_america():
    """Check that the American currencies are correct.

    For each currency, we check the ISO codes, the name, and the symbol.
    """
    # USD
    assert usd().name() == "US dollar"
    assert usd().code() == "USD"
    assert usd().numeric_code() == 840
    assert usd().symbol() == "$"
    assert usd().fraction_symbol() == "¢"
    # ARS
    assert ars().name() == "Argentinian peso"
    assert ars().code() == "ARS"
    assert ars().numeric_code() == 32
    assert ars().symbol() == ""
    # BRL
    assert brl().name() == "Brazilian real"
    assert brl().code() == "BRL"
    assert brl().numeric_code() == 986
    assert brl().symbol() == "R$"
    # CAD
    assert cad().name() == "Canadian dollar"
    assert cad().code() == "CAD"
    assert cad().numeric_code() == 124
    assert cad().symbol() == "Can$"
    # CLP
    assert clp().name() == "Chilean peso"
    assert clp().code() == "CLP"
    assert clp().numeric_code() == 152
    assert clp().symbol() == "Cs$"
    # COP
    assert cop().name() == "Columbian peso"
    assert cop().code() == "COP"
    assert cop().numeric_code() == 170
    assert cop().symbol() == "Col$"
    # MXN
    assert mxn().name() == "Mexican peso"
    assert mxn().code() == "MXN"
    assert mxn().numeric_code() == 484
    assert mxn().symbol() == "Mex$"
    # PEN
    assert pen().name() == "Peruvian nuevo sol"
    assert pen().code() == "PEN"
    assert pen().numeric_code() == 604
    assert pen().symbol() == "S/."
    # PEI
    assert pei().name() == "Peruvian inti"
    assert pei().code() == "PEI"
    assert pei().symbol() == "I/."
    # PEH
    assert peh().name() == "Peruvian sol"
    assert peh().code() == "PEH"
    assert peh().symbol() == "S./"
    # TTD
    assert ttd().name() == "Trinidad & Tobago dollar"
    assert ttd().code() == "TTD"
    assert ttd().numeric_code() == 840
    assert ttd().symbol() == "TT$"
    # VEB
    assert veb().name() == "Venezuelan bolivar"
    assert veb().code() == "VEB"
    assert veb().numeric_code() == 862
    assert veb().symbol() == "Bs"
