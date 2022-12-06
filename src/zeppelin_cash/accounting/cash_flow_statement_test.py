"""The module wallet.accounting.test_cash_flow_statement test the
CashFlowStatement implementation."""
from datetime import datetime

from zeppelin_cash.accounting.cash_flow_statement import CashFlowStatement
from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.money import Money


def test_cash_flow_statement_init() -> None:
    """Test that a CashFlowStatement can be created."""
    stmt = CashFlowStatement(datetime.now(), datetime.now())
    assert stmt.beginning_cash_balance.quantity() == 0
    assert stmt.cash_disbursements.quantity() == 0


def test_cash_from_operations() -> None:
    """Test that cash from operations can be calculated."""
    stmt = CashFlowStatement(datetime.now(), datetime.now())
    stmt.cash_receipts = Money(100, usd())
    stmt.cash_disbursements = Money(10, usd())
    assert stmt.cash_from_operations().quantity() == 90


def test_ending_cash_balance() -> None:
    """Test that ending cash balance can be calculated."""
    stmt = CashFlowStatement(datetime.now(), datetime.now())
    stmt.beginning_cash_balance = Money(100, usd())
    stmt.cash_receipts = Money(100, usd())
    stmt.cash_disbursements = Money(10, usd())
    stmt.net_borrowings = Money(50, usd())
    stmt.income_taxes_paid = Money(10, usd())
    assert stmt.ending_cash_balance().quantity() == 230


def test_adding_cash_flow_statements() -> None:
    """Test that cash flow statements can be added."""
    stmt1 = CashFlowStatement(datetime.now(), datetime.now())
    stmt1.cash_receipts = Money(100, usd())
    stmt2 = CashFlowStatement(datetime.now(), datetime.now())
    stmt2.cash_disbursements = Money(10, usd())
    total = stmt1 + stmt2
    assert total.cash_from_operations().quantity() == 90


def test_string_cash_flow_statement() -> None:
    """Test that a cash flow statement can be converted to string."""
    stmt = CashFlowStatement(datetime.now(), datetime.now())
    stmt.cash_receipts = Money(100, usd())
    stmt.cash_disbursements = Money(10, usd())
    assert "Cash receipts: {}".format(stmt.cash_receipts) in str(stmt)
    assert "Cash disbursements: {}".format(
        stmt.cash_disbursements) in str(stmt)
    assert "Cash from operations: {}".format(
        stmt.cash_from_operations()) in str(stmt)
