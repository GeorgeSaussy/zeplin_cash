"""The module wallet.accounting.test_financial_statement tests
the FinancialStatement implementation."""
from datetime import datetime, timedelta

from zeppelin_cash.accounting.america import usd, ars
from zeppelin_cash.accounting.balance_sheet import BalanceSheet
from zeppelin_cash.accounting.cash_flow_statement import CashFlowStatement
from zeppelin_cash.accounting.financial_statement import FinancialStatement
from zeppelin_cash.accounting.income_statement import IncomeStatement
from zeppelin_cash.accounting.money import Money


def test_financial_statement_init() -> None:
    """Test that a FinancialStatement instance can be created."""
    start = datetime.now()
    end = start + timedelta(days=365)
    balance_sheet = BalanceSheet(end)
    balance_sheet.cash = Money(1000, usd())
    balance_sheet.capital_stock = Money(1000, usd())
    cash_flow_statement = CashFlowStatement(start, end)
    cash_flow_statement.beginning_cash_balance = Money(1000, usd())
    income_statement = IncomeStatement(start, end)
    financial_statement = FinancialStatement(
        balance_sheet, cash_flow_statement, income_statement)
    assert financial_statement.is_valid()
    # Now we are doing fraud, where did this cash come from if not investors?
    financial_statement.balance_sheet.capital_stock = Money(0, usd())
    assert not financial_statement.is_valid()


def test_statements_use_one_currency() -> None:
    """Check that financial statements use one currency."""
    start = datetime.now()
    end = start + timedelta(days=365)
    balance_sheet = BalanceSheet(end)
    cash_flow_statement = CashFlowStatement(start, end, currency=ars())
    income_statement = IncomeStatement(start, end)
    financial_statement = FinancialStatement(
        balance_sheet, cash_flow_statement, income_statement)
    assert not financial_statement.is_valid()


def test_blank_financial_statement() -> None:
    """Test the a blank financial statement can be created."""
    start = datetime.now()
    end = start + timedelta(days=365)
    financial_statement = FinancialStatement.blank(start, end)
    assert financial_statement.is_valid()
    assert financial_statement.balance_sheet.cash.quantity() == 0


def test_adding_financial_statements() -> None:
    """Test that financial statements can be added."""
    start = datetime.now()
    end = start + timedelta(days=365)

    balance_sheet_1 = BalanceSheet(end)
    balance_sheet_1.cash = Money(100, usd())
    balance_sheet_2 = BalanceSheet(end)
    balance_sheet_2.inventory = Money(500, usd())

    cash_flow_statement_1 = CashFlowStatement(datetime.now(), datetime.now())
    cash_flow_statement_1.cash_receipts = Money(100, usd())
    cash_flow_statement_2 = CashFlowStatement(datetime.now(), datetime.now())
    cash_flow_statement_2.cash_disbursements = Money(10, usd())

    income_statement_1 = IncomeStatement(datetime.now(), datetime.now())
    income_statement_1.net_sales = Money(100, usd())
    income_statement_2 = IncomeStatement(datetime.now(), datetime.now())
    income_statement_2.research_and_development = Money(15, usd())

    financial_statement_1 = FinancialStatement(
        balance_sheet_1, cash_flow_statement_1, income_statement_1)
    financial_statement_2 = FinancialStatement(
        balance_sheet_2, cash_flow_statement_2, income_statement_2)
    total = financial_statement_1 + financial_statement_2

    assert total.balance_sheet.total_assets().quantity() == 600
    assert total.cash_flow_statement.cash_from_operations().quantity() == 90
    assert total.income_statement.net_sales.quantity() == 100
    assert total.income_statement.research_and_development.quantity() == 15
    assert total.income_statement.net_income().quantity() == 85
