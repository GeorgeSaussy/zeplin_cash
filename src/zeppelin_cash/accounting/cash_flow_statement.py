"""The module wallet.accounting.cash_flow_statement contains the
CashFlowStatement implementation."""
from datetime import datetime

from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.currency import Currency
from zeppelin_cash.accounting.money import Money


class CashFlowStatement:
    """A CashFlowStatement encapulates the CashFlowStatement
    component of a financial statement.
    """

    def __init__(self, start_time: datetime, end_time: datetime,
                 currency: Currency = usd()) -> None:
        """Initialize a new cash flow statement.

        Args:
            start_time: the start time of the period covered by the statement
            end_time: the end time of the period covered by the statement
            currency: the currency used in the statement
        """
        self.start_time = start_time
        self.end_time = end_time
        self.currency = currency

        self.beginning_cash_balance = Money(0, self.currency)

        # Cash receipts are inflows of money from the operating of the
        # business. This is also called "collections" or "receipts".
        # Increases in the cash receipts decreases the amount due to the
        # firm on the accounts receivable.
        self.cash_receipts = Money(0, self.currency)

        # Cash disbursements are the outflows of money used in operating
        # the business. This includes paying for inventory or paying
        # salaries. These are also called "payments" or "disbusements".
        # Payments accounted here decreases accounts payable on the balance
        # sheet.
        self.cash_disbursements = Money(0, self.currency)

        # This is money used to buy fixed assets. This includes
        # PP&E, or property, plant, and equipment.
        self.fixed_asset_purchases = Money(0, self.currency)

        # Net borrowing increased the amount of cash a firm has. Net
        # borrowings is the difference between new getting new loans,
        # and paying back old loans.
        self.net_borrowings = Money(0, self.currency)

        # Income taxes only have a cash effect on a firm when paid.
        self.income_taxes_paid = Money(0, self.currency)

        # Selling stock increases cash.
        self.sale_of_stock = Money(0, self.currency)

    def cash_from_operations(self) -> Money:
        """Get the cash from operations.

        Cash from operations is defined as the difference between cash
        receipts and cash disbusements.

        Returns:
            The cash from operations.
        """
        return self.cash_receipts - self.cash_disbursements

    def ending_cash_balance(self) -> Money:
        """Get the ending cash balance.

        Returns:
            The ending cash balance.
        """
        return self.beginning_cash_balance + \
            self.cash_from_operations() - \
            self.fixed_asset_purchases + \
            self.net_borrowings - \
            self.income_taxes_paid + \
            self.sale_of_stock

    def __add__(self, other: 'CashFlowStatement') -> 'CashFlowStatement':
        """Add two cash flow statements together.

        Args:
            other: the other term in the sum

        Returns:
            The sum.
        """
        cfs = CashFlowStatement(
            self.start_time,
            self.end_time,
            currency=self.currency)

        cfs.beginning_cash_balance = self.beginning_cash_balance + \
            other.beginning_cash_balance
        cfs.cash_receipts = self.cash_receipts + other.cash_receipts
        cfs.cash_disbursements = self.cash_disbursements + other.cash_disbursements

        cfs.fixed_asset_purchases = self.fixed_asset_purchases + other.fixed_asset_purchases
        cfs.net_borrowings = self.net_borrowings + other.net_borrowings
        cfs.income_taxes_paid = self.income_taxes_paid + other.income_taxes_paid
        cfs.sale_of_stock = self.sale_of_stock + other.sale_of_stock

        return cfs

    def __str__(self) -> str:
        """Get a string representation of the cash flow statement.

        Returns:
            The CashFlowStatement instance as a string.
        """
        return """
Cash Flow Statement for the period {} to {}
----------------------
Beginning cash balance: {}
Cash receipts: {}
Cash disbursements: {}
----------------------
Cash from operations: {}
Fixed asset purchases: {}
Net borrowings: {}
Income taxes paid: {}
Sale of stock: {}
Ending cash balance: {}
""".format(
            str(self.start_time),
            str(self.end_time),
            str(self.beginning_cash_balance),
            str(self.cash_receipts),
            str(self.cash_disbursements),
            str(self.cash_from_operations()),
            str(self.fixed_asset_purchases),
            str(self.net_borrowings),
            str(self.income_taxes_paid),
            str(self.sale_of_stock),
            str(self.ending_cash_balance()))
