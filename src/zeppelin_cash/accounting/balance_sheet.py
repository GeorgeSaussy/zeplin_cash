"""The module wallet.accounting.balance_sheet contains the
BalanceSheet implementation."""
from datetime import datetime

from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.currency import Currency
from zeppelin_cash.accounting.money import Money


class BalanceSheet:
    """BalanceSheet is a class that encapsulates a balance sheet for a financial statement."""

    def __init__(self, time: datetime, currency: Currency = usd()) -> None:
        """Create a new BlananceSheet instance

        Args:
            time: the timestap for the encapsulated balance sheet
            currency: the currency for the balance sheet
        """
        self.time = time
        self.currency = currency

        # Assets

        # This is cash availible in a bank account or physical cash that
        # the firm owns. Cash should be reported in the currency of the
        # home country of the firm. If the firm has forign currency, say
        # from over seas operations, then that value should
        # be converted to the local currency for reporting.
        self.cash = Money(0, self.currency)

        # Accounts recievable is the sum of the value of good or services
        # sold, but that have not been paid for. For example, say WidgitTech
        # shiped a regular client 100 widgets but the customer has not yet
        # paid, this would be considered accounts recievable.
        # This is different from cash from goods sold, because *it is not cash*.
        # Accounts recievable also entails a legal right to collect a debt.
        self.accounts_recievable = Money(0, self.currency)

        # Inventory is the value of both finished goods ready to be sold,
        # and the row materials and itermediate products used to
        # manufacture final goods.
        # TODO(gs): Figure out how to value inventory.
        self.inventory = Money(0, self.currency)

        # Prepaid expenses are the vaud of goods or service that the firm has
        # paid for, bug which have not yet been relised. For example, say
        # WidgetTech orders 1,000 widget parts and pays for them. For the time
        # between paying for the order and the parts arriving, the value of the
        # parts is accounted for as a prepaid expense.
        self.prepaid_expenses = Money(0, self.currency)

        # Other assets include all other assets not included in other
        # categoies. This includes things like patents, source code,
        # copyrights, and brand value.
        self.other_assets = Money(0, self.currency)

        # Fixed assets are assets that are useful for production, but
        # that are not intended for sale. A farm's tractors are fixed
        # assets, and the office building that WidgetTech uses is also a
        # fixed asset. These are reported at the *purchasing price*, not
        # their resale value if they were to be sold used as of the
        # timestamp of the balance sheet.
        self.fixed_assets_at_cost = Money(0, self.currency)

        # This this the value that adjusts the fixed assets for depreciation.
        # Wear and tear on fixed assets is accounted for in this component.
        self.accumulated_depreciation = Money(0, self.currency)

        # Liabilities

        # These are liabilities for materials purchased that have not yet
        # been paid for. For example, say WidgetTech hires a contractor who
        # performs some service. For the time between when the service is
        # rendered, and the contractor is paid, the liability for the
        # transaction is recorded as accounts payable.
        self.accounts_payable = Money(0, self.currency)

        # Accrues expenses are a type of liability that mostly differs from
        # accounts payable in the whom the liability is owed. Accrued
        # expenses are things like as-of-yet unpaid salaries, layers fees,
        # or interest payments to banks.
        self.accrued_expenses = Money(0, self.currency)

        # Current portion of debt is made of notes payable and the current
        # portion of long-term debt. Notes payable are payments that are due
        # to a bank within the next 12 months according to the terms of the
        # loan. Further, for a debt that must be paid over a longer term,
        # then the portion of that debt must be paid within the next 12 months
        # is called the "current portion of long-term debt".
        self.current_portion_of_debt = Money(0, self.currency)

        # Income taxes payable are income taxes owed to the government that
        # have not yet been paid.
        self.income_taxes_payable = Money(0, self.currency)

        self.long_term_debt = Money(0, self.currency)

        # Capital stock is the money originally contributed to start a
        # business. If WidgetTech's founder, Mr. Widget, started the
        # company with by putting in 100 USD of his own money, then that
        # 100 USD would be included in this line as capital stock.
        # TODO(gs): This is also the line in which the sale of stock should
        # be accounted.
        self.capital_stock = Money(0, self.currency)

        # Retained earnings are the difference between profits and dividends.
        # If a company takes a loss, this number could be negative.
        self.retained_earnings = Money(0, self.currency)

    def current_assets(self) -> Money:
        """Get the value of current assets.

        Returns:
            The value of current assets.
        """
        return self.cash + self.accounts_recievable + \
            self.inventory + self.prepaid_expenses

    def net_fixed_assets(self) -> Money:
        """Get the value of net fixed assets.

        This is the value of fixed assets taking into account depreciation.
        Since depreciation can only be a positive value accounting for TKTK

        Returns:
            The value of net fixed assets.
        """
        return self.fixed_assets_at_cost - self.accumulated_depreciation

    def total_assets(self) -> Money:
        """Get the value of total assets.

        Returns:
            The value of total assets.
        """
        return self.current_assets() + self.other_assets + self.net_fixed_assets()

    def current_liabilities(self) -> Money:
        """Get the value of current liabilities.

        Liabilities are oblications of the firm. This includes shareholder equity,
        although this liability is not expected to be repaid in the normal course
        of business. Current liabilities are liabilities that must be paid within
        one year of the date of the balance sheet. Current liabilities are the
        inverse of current assets.

        Returns:
            The value of current liabilities.
        """
        return self.accounts_payable + self.accrued_expenses + \
            self.current_portion_of_debt + self.income_taxes_payable

    def shareholders_equity(self) -> Money:
        """Get the value of shareholder's equity.

        Shareholder equity is the sum of retained earning and capital stock.

        Returns:
            The value of shareholders equity.
        """
        return self.capital_stock + self.retained_earnings

    def total_liabilities_and_equity(self) -> Money:
        """Get the value of total liabilities and equity.

        Returns:
            The value of total liabilities and equity.
        """
        return self.current_liabilities() + self.long_term_debt + \
            self.shareholders_equity()

    def capital_employed(self) -> Money:
        """Get the value of the capital employed.

        This is defined as total assets - current liabilities,
        It is needed to calculate ROCE to find the value of a firm.

        Returns:
            The total capital employed.
        """
        return self.current_assets() - self.current_liabilities()

    def __add__(self, sheet: 'BalanceSheet') -> 'BalanceSheet':
        """Add two balance sheets together.

        Args:
            x: the other balance sheet

        Returns:
            A new balance sheet.
        """
        ret = BalanceSheet(self.time, currency=self.currency)
        ret.time = self.time
        # Assets
        ret.cash = self.cash + sheet.cash
        ret.accounts_recievable = self.accounts_recievable + sheet.accounts_recievable
        ret.inventory = self.inventory + sheet.inventory
        ret.prepaid_expenses = self.prepaid_expenses + sheet.prepaid_expenses

        ret.other_assets = self.other_assets + sheet.other_assets

        ret.fixed_assets_at_cost = self.fixed_assets_at_cost + sheet.fixed_assets_at_cost
        ret.accumulated_depreciation = self.accumulated_depreciation + \
            sheet.accumulated_depreciation

        # Liabilities
        ret.accounts_payable = self.accounts_payable + sheet.accounts_payable
        ret.accrued_expenses = self.accrued_expenses + sheet.accrued_expenses
        ret.current_portion_of_debt = self.current_portion_of_debt + \
            ret.current_portion_of_debt
        ret.income_taxes_payable = self.income_taxes_payable + sheet.income_taxes_payable

        ret.long_term_debt = self.long_term_debt + sheet.long_term_debt

        ret.capital_stock = self.capital_stock + sheet.capital_stock
        ret.retained_earnings = self.retained_earnings + self.retained_earnings
        return ret

    def __str__(self) -> str:
        """Convert the BalanceSheet instance to a string.

        Returns:
            The balance sheet as a string.
        """
        return """
Balance Sheet as of {}
----------------------
Assets
----------------------
Cash: {}
Accounts Receivable: {}
Inventory: {}
Prepaid expenses: {}
----------------------
Current assets: {}
Other assets: {}
Fixed assets at cost: {}
Accumulated depreciation: {}
----------------------
Net fixed assets: {}
----------------------
Total assets: {}
----------------------
Liabilities
----------------------
Accounts Payable: {}
Accrued expenses: {}
Current portion of debt: {}
Income taxes payable: {}
----------------------
Current liabilities: {}
Long-term debt: {}
Capital stock: {}
Retained earnings: {}
----------------------
Shareholders equity: {}
Total liabilities & equity: {}`,
""".format(
            str(self.time),
            str(self.cash),
            str(self.accounts_recievable),
            str(self.inventory),
            str(self.prepaid_expenses),
            str(self.current_assets()),
            str(self.other_assets),
            str(self.fixed_assets_at_cost),
            str(self.accumulated_depreciation),
            str(self.net_fixed_assets()),
            str(self.total_assets()),
            str(self.accounts_payable),
            str(self.accrued_expenses),
            str(self.current_portion_of_debt),
            str(self.income_taxes_payable),
            str(self.current_liabilities()),
            str(self.long_term_debt),
            str(self.capital_stock),
            str(self.retained_earnings),
            str(self.shareholders_equity()),
            str(self.total_liabilities_and_equity()))
