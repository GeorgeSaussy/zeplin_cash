"""The module wallet.accounting.financial_statement contains the
FinancialStatement implementation."""
from datetime import datetime

from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.balance_sheet import BalanceSheet
from zeppelin_cash.accounting.cash_flow_statement import CashFlowStatement
from zeppelin_cash.accounting.currency import Currency
from zeppelin_cash.accounting.income_statement import IncomeStatement


class FinancialStatement:
    """FinancialStatement is designed to encapsulate GAAP financial statements."""

    def __init__(self, balance_sheet: BalanceSheet,
                 cash_flow_statement: CashFlowStatement,
                 income_statement: IncomeStatement) -> None:
        """Create a new FinancialStatement instance.

        Args:
            balance_sheet: the statement's balance sheet
            cash_flow_statement: the statement's cash flow statement
            income_statement: the statement's income statement

        Returns:
            A new FiancialStatement instance.
        """
        self.balance_sheet = balance_sheet
        self.cash_flow_statement = cash_flow_statement
        self.income_statement = income_statement

    @classmethod
    def blank(cls, start_time: datetime, end_time: datetime,
              currency: Currency = usd()) -> 'FinancialStatement':
        """Get a blank financial statement.

        Args:
            start_time: the starting time of the period covered by the statement
            end_time: the ending time of the period covered by the statement
            currency: the accounting currency for the statement

        Returns:
            A blank financial statement.
        """
        return FinancialStatement(
            BalanceSheet(end_time, currency=currency),
            CashFlowStatement(start_time, end_time, currency=currency),
            IncomeStatement(start_time, end_time, currency=currency),
        )

    def is_valid(self) -> bool:
        """Check that a financial statement is legal.

        Returns:
            True iff the statement adds up.
        """
        balance_sheet = self.balance_sheet
        cash_flow = self.cash_flow_statement
        income = self.income_statement
        if balance_sheet.currency.code() != cash_flow.currency.code() or cash_flow.currency.code(
        ) != income.currency.code() or income.currency.code() != balance_sheet.currency.code():
            return False
        return cash_flow.ending_cash_balance() == balance_sheet.cash \
            and balance_sheet.total_assets() == balance_sheet.total_liabilities_and_equity()

    def __add__(self, other: 'FinancialStatement') -> 'FinancialStatement':
        """Add two financial statements together.

        Args:
            other: the other financial statement

        Returns:
            The sum of the financial statements.
        """
        balance_sheet = self.balance_sheet + other.balance_sheet
        cash_flow_statement = self.cash_flow_statement + other.cash_flow_statement
        income_statement = self.income_statement + other.income_statement
        return FinancialStatement(
            balance_sheet, cash_flow_statement, income_statement)

    def __str__(self) -> str:
        return '\n'.join([str(stmt) for stmt in
                          [self.balance_sheet, self.cash_flow_statement, self.income_statement]])
