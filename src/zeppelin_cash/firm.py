"""The module medici.firm contains a simple firm implementation."""
from datetime import datetime

from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.book import Book
from zeppelin_cash.accounting.currency import Currency
from zeppelin_cash.accounting.financial_statement import FinancialStatement
from zeppelin_cash.errors import Result


class Firm:
    """Firm encapsulates a firm.

    The expectation is that this class will be subclassed for each particular
    firm.
    """

    def __init__(self, founding: datetime, currency: Currency = usd()) -> None:
        """Create a new Firm instance.

        Args:
            founding: the date the firm was founded
        """
        self.founding = founding
        self.book = Book(founding, currency)

    def financial_statement(self, start: datetime,
                            end: datetime) -> Result[FinancialStatement]:
        """Get a financial statement for the firm.

        This implementation returns a financial statement with all zero values.

        Returns:
            A financial statement.
        """
        return self.book.financial_statement(start, end)
