"""The module wallet.accounting.income_statement tests the IncomeStatement implementation."""
from datetime import datetime

from zeppelin_cash.accounting.income_statement import IncomeStatement
from zeppelin_cash.accounting.money import Money


def test_income_statement_init() -> None:
    """Check that an IncomeStatement instance can be created."""
    stmt = IncomeStatement(datetime.now(), datetime.now())
    assert stmt.net_sales.quantity() == 0
    assert stmt.income_taxes.quantity() == 0


def test_gross_margin() -> None:
    """Check that the gross margin is correct."""
    stmt = IncomeStatement(datetime.now(), datetime.now())
    stmt.net_sales = Money(100, stmt.currency)
    stmt.cost_of_goods_sold = Money(10, stmt.currency)
    assert stmt.gross_margin().quantity() == 90


def test_operating_expenses() -> None:
    """Check that operating expenses are correct."""
    stmt = IncomeStatement(datetime.now(), datetime.now())
    stmt.sales_and_marketing = Money(100, stmt.currency)
    stmt.research_and_development = Money(15, stmt.currency)
    stmt.general_and_administrative = Money(12, stmt.currency)
    assert stmt.operating_expenses().quantity() == 127


def test_income_from_operations() -> None:
    """Check that income from operations can be calculated."""
    stmt = IncomeStatement(datetime.now(), datetime.now())
    stmt.sales_and_marketing = Money(100, stmt.currency)
    stmt.research_and_development = Money(15, stmt.currency)
    stmt.general_and_administrative = Money(12, stmt.currency)
    stmt.net_sales = Money(100, stmt.currency)
    stmt.cost_of_goods_sold = Money(10, stmt.currency)
    assert stmt.income_from_operations().quantity() == -37


def test_net_income() -> None:
    """Check that the net income can be calculated."""
    stmt = IncomeStatement(datetime.now(), datetime.now())
    stmt.sales_and_marketing = Money(100, stmt.currency)
    stmt.research_and_development = Money(15, stmt.currency)
    stmt.general_and_administrative = Money(12, stmt.currency)
    stmt.net_sales = Money(1000, stmt.currency)
    stmt.cost_of_goods_sold = Money(10, stmt.currency)
    stmt.income_taxes = Money(1, stmt.currency)
    stmt.interest_income = Money(5, stmt.currency)
    assert stmt.net_income().quantity() == 867


def test_add_income_statements() -> None:
    """Check that income statements can be added."""
    stmt1 = IncomeStatement(datetime.now(), datetime.now())
    stmt1.net_sales = Money(100, stmt1.currency)
    stmt2 = IncomeStatement(datetime.now(), datetime.now())
    stmt2.research_and_development = Money(15, stmt2.currency)
    total = stmt1 + stmt2
    assert total.net_sales.quantity() == 100
    assert total.research_and_development.quantity() == 15
    assert total.net_income().quantity() == 85


def test_printing_income_statement() -> None:
    """Test that the income statement can be printed."""
    stmt = IncomeStatement(datetime.now(), datetime.now())
    stmt.net_sales = Money(100, stmt.currency)
    stmt.research_and_development = Money(15, stmt.currency)
    assert "Net sales: {}".format(stmt.net_sales) in str(stmt)
    assert "Research & development: {}".format(
        stmt.research_and_development) in str(stmt)
    assert "Net income: {}".format(stmt.net_income()) in str(stmt)
