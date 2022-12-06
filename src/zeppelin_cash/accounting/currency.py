"""The module wallet.accounting.currency contains the Currency class implementation."""


class Currency:
    """Currency encapsulates a *type* of physical cash.

    Examples could be US dollars or Kenyan shillings.
    """
    # pylint: disable=R0913

    def __init__(
            self,
            name: str,
            code: str,
            numeric_code: int = 0,
            symbol: str = "",
            fraction_symbol: str = "",
            fractions_per_unit: int = 100) -> None:
        """Create a new currency instance.

        Args:
            name: the name of the currency
            code: the three letter ISO 4217 code, e.g. USD
            numeric_code: the numeric ISO 4217 code
            symbol: the currency's symbol, e.g. "$" for USD
            fraction_symbol: the fractional symbol for the currency, e.g. "¢" for USD
            fractions_per_unit: the number of the fraction unit in the currency,
                e.g. 100 cents in a US dollar
        """
        self.__name = name
        self.__code = code
        self.__numeric_code = numeric_code
        self.__symbol = symbol
        self.__fraction_symbol = fraction_symbol
        self.__fractions_per_unit = fractions_per_unit

    def name(self) -> str:
        """Get the name of the currency.

        Returns:
            The name of the currency, e.g. "US dollar".
        """
        return self.__name

    def code(self) -> str:
        """Get the ISO 4217 three letter code for the currency.

        Returns:
            The ISO code for the currency, e.g. USD.
        """
        return self.__code

    def numeric_code(self) -> int:
        """Get the ISO 4217 numeric code.

        Returns:
            The ISO code for the currency, e.g. 840 for USD.
        """
        return self.__numeric_code

    def symbol(self) -> str:
        """Get the symbol for the currency, e.g. "$" for USD.

        Returns:
            The symbol for the currency.
        """
        return self.__symbol

    def fraction_symbol(self) -> str:
        """Get the symbol used for fractions of the currency, e.g. "¢" for USD.

        Returns:
            The fraction symbol for the currency.
        """
        return self.__fraction_symbol

    def fractions_per_unit(self) -> int:
        """Get the number of fractional parts are in the currency, e.g. 100 cents in 1 USD.

        Returns:
            The number in the fractional part of the currency.
        """
        return self.__fractions_per_unit
