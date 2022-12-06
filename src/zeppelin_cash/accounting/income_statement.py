"""The module wallet.accounting.income_statement contains the
IncomeStatement implementation."""
from datetime import datetime

from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.currency import Currency
from zeppelin_cash.accounting.money import Money


class IncomeStatement:
    """IncomeStatement encapsulates the income statement component
    of a financial statement.
    """

    def __init__(self, start_time: datetime, end_time: datetime,
                 currency: Currency = usd()) -> None:
        """Create a new IncomeStatement instance.

        Args:
            start_time: the start time of the period covered by the statement
            end_time: the end time of the period covered by the statement
            currency: the currency used in the statement
        """
        self.start_time = start_time
        self.end_time = end_time
        self.currency = currency

        # Sales only add to net sales when the product is realized.
        # Until this point, a pending sale it called an "order". Say
        # WidgetTech gets an order for 100 widgets. That order becomes
        # a sale when the widgets are shipped. If the customer has not yet
        # paid, then the sale is also recorded as accounts receivable on the
        # balance sheet.
        self.net_sales = Money(0, self.currency)

        # When a good is sold, the inventory value associated with the
        # sale added here.
        self.cost_of_goods_sold = Money(0, self.currency)
        self.sales_and_marketing = Money(0, self.currency)

        self.research_and_development = Money(0, self.currency)
        self.general_and_administrative = Money(0, self.currency)

        # Interest income from a loan by the firm is recorded in this
        # component.
        self.interest_income = Money(0, self.currency)
        self.income_taxes = Money(0, self.currency)

    def gross_margin(self) -> Money:
        """Get the gross margin.

        Gross margin is the difference between net sales and the cost of
        goods sold.

        Returns:
            The gross margin.
        """
        return self.net_sales - self.cost_of_goods_sold

    def operating_expenses(self) -> Money:
        """Get the operating expenses.

        Operating expenses are the costs of the things a firm dies to allow
        it to make money. This includes sales and marketing; research and
        development; and general and administrative. This is also called
        SG&A expenses for "sales, general, and administrative expenses".

        Returns:
            The operating expenses.
        """
        return self.sales_and_marketing + \
            self.research_and_development + self.general_and_administrative

    def income_from_operations(self) -> Money:
        """Get the income from operations.

        Income from operations is the difference between gross margin
        and operating expenses.

        Returns:
            Income from operations.
        """
        return self.gross_margin() - self.operating_expenses()

    def net_income(self) -> Money:
        """Get the net income.

        Net income is the sum of income from operations and non-operating
        income and expenses.

        Returns:
            The net income.
        """
        return self.income_from_operations() + self.interest_income - self.income_taxes

    def __add__(self, other: 'IncomeStatement') -> 'IncomeStatement':
        """Add two income statements together.

        Args:
            other: the other income statement to sum

        Returns:
            The sum.
        """
        ins = IncomeStatement(
            self.start_time,
            self.end_time,
            currency=self.currency)

        ins.net_sales = self.net_sales + other.net_sales
        ins.cost_of_goods_sold = self.cost_of_goods_sold + other.cost_of_goods_sold
        ins.sales_and_marketing = self.sales_and_marketing + other.sales_and_marketing

        ins.research_and_development = self.research_and_development + \
            other.research_and_development
        ins.general_and_administrative = self.general_and_administrative + \
            other.general_and_administrative
        ins.interest_income = self.interest_income + other.interest_income
        ins.income_taxes = self.income_taxes + other.income_taxes

        return ins

    def __str__(self) -> str:
        """Get the income statement as a string.

        Returns:
            The IncomeStatement instance as a string.
        """
        return """
Income Statement for the period {} to {}
----------------------
Net sales: {}
Cost of goods sold: {}
----------------------
Gross margin: {}
Sales & marketing: {}
Research & development: {}
General & administrative: {}
----------------------
Operating expenses: {}
Income from operations: {}
Interest income: {}
Income taxes: {}
----------------------
Net income: {}
""".format(
            str(self.start_time),
            str(self.end_time),
            str(self.net_sales),
            str(self.cost_of_goods_sold),
            str(self.gross_margin()),
            str(self.sales_and_marketing),
            str(self.research_and_development),
            str(self.general_and_administrative),
            str(self.operating_expenses()),
            str(self.income_from_operations()),
            str(self.interest_income),
            str(self.income_taxes),
            str(self.net_income()))
