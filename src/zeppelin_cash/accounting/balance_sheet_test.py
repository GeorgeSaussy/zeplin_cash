"""The module wallet.accounting.balance_sheet test the BalanceSheet implementation."""
from datetime import datetime

from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.balance_sheet import BalanceSheet
from zeppelin_cash.accounting.money import Money


def test_balance_sheet_init() -> None:
    """Test a BalanceSheet instance can be created."""
    sheet = BalanceSheet(datetime.now())
    assert sheet.cash.quantity() == 0
    assert sheet.current_assets().quantity() == 0


def test_current_assets() -> None:
    """Test that current assets can be calculated."""
    sheet = BalanceSheet(datetime.now())
    sheet.cash = Money(100, usd())
    sheet.accounts_recievable = Money(15, usd())
    sheet.inventory = Money(10, usd())
    sheet.prepaid_expenses = Money(11, usd())
    assert sheet.current_assets().quantity() == 136


def test_net_fixed_assets() -> None:
    """Test that net fixed assets can be calculated."""
    sheet = BalanceSheet(datetime.now())
    sheet.fixed_assets_at_cost = Money(100, usd())
    sheet.accumulated_depreciation = Money(10, usd())
    assert sheet.net_fixed_assets().quantity() == 90


def test_total_assets() -> None:
    """Test that total assets can be calculated."""
    sheet = BalanceSheet(datetime.now())
    # current assets
    sheet.cash = Money(100, usd())
    sheet.accounts_recievable = Money(15, usd())
    sheet.inventory = Money(10, usd())
    sheet.prepaid_expenses = Money(11, usd())
    # net fixed assets
    sheet.fixed_assets_at_cost = Money(100, usd())
    sheet.accumulated_depreciation = Money(10, usd())
    # other assets
    sheet.other_assets = Money(12, usd())
    assert sheet.total_assets().quantity() == 238


def test_current_liabilities() -> None:
    """Test that the current liabilities can be calculated."""
    sheet = BalanceSheet(datetime.now())
    sheet.accounts_payable = Money(100, usd())
    sheet.accrued_expenses = Money(50, usd())
    sheet.current_portion_of_debt = Money(25, usd())
    sheet.income_taxes_payable = Money(10, usd())
    assert sheet.current_liabilities().quantity() == 185


def test_shareholders_equity() -> None:
    """Test that shareholders equity can be calculated."""
    sheet = BalanceSheet(datetime.now())
    sheet.capital_stock = Money(10, usd())
    sheet.retained_earnings = Money(15, usd())
    assert sheet.shareholders_equity().quantity() == 25


def test_total_liabilities_and_equity() -> None:
    """Test that total liabilities and equity can be calculated."""
    sheet = BalanceSheet(datetime.now())
    # current liabilities
    sheet.accounts_payable = Money(100, usd())
    sheet.accrued_expenses = Money(50, usd())
    sheet.current_portion_of_debt = Money(25, usd())
    sheet.income_taxes_payable = Money(10, usd())
    # long term debt
    sheet.long_term_debt = Money(22, usd())
    # shareholder's equity
    sheet.capital_stock = Money(10, usd())
    sheet.retained_earnings = Money(15, usd())
    assert sheet.total_liabilities_and_equity().quantity() == 232


def test_capital_employed() -> None:
    """Test that capital employed can be calculated."""
    sheet = BalanceSheet(datetime.now())
    # current assets
    sheet.cash = Money(100, usd())
    sheet.accounts_recievable = Money(15, usd())
    sheet.inventory = Money(10, usd())
    sheet.prepaid_expenses = Money(11, usd())
    # current liabilities
    sheet.accounts_payable = Money(100, usd())
    sheet.accrued_expenses = Money(50, usd())
    sheet.current_portion_of_debt = Money(25, usd())
    sheet.income_taxes_payable = Money(10, usd())
    assert sheet.capital_employed().quantity() == -49


def test_adding_balance_sheet() -> None:
    """Test that balance sheet instances can be added."""
    now = datetime.now()
    sheet1 = BalanceSheet(now)
    sheet1.cash = Money(100, usd())
    sheet2 = BalanceSheet(now)
    sheet2.inventory = Money(500, usd())
    total = sheet1 + sheet2
    assert total.total_assets().quantity() == 600


def test_balance_sheet_as_string() -> None:
    """Test that balance sheet can be represented as a string."""
    sheet = BalanceSheet(datetime.now())
    sheet.cash = Money(100, usd())
    sheet.inventory = Money(150, usd())
    assert "Cash: {}".format(sheet.cash) in str(sheet)
    assert "Inventory: {}".format(sheet.inventory) in str(sheet)
