"""The module wallet.accounting.book contains the Book implementation."""
from typing import List, Tuple
from datetime import datetime

from zeppelin_cash.accounting.account import Account, AccountId
from zeppelin_cash.accounting.america import usd
from zeppelin_cash.accounting.account_entry import AccountEntry
from zeppelin_cash.accounting.account_metadata import AccountMetadata
from zeppelin_cash.accounting.balance_sheet import BalanceSheet
from zeppelin_cash.accounting.cash_flow_statement import CashFlowStatement
from zeppelin_cash.accounting.currency import Currency
from zeppelin_cash.accounting.financial_statement import FinancialStatement
from zeppelin_cash.accounting.income_statement import IncomeStatement
from zeppelin_cash.accounting.journal import Journal
from zeppelin_cash.accounting.journal_transaction import JournalTransaction
from zeppelin_cash.accounting.ledger import Ledger
from zeppelin_cash.accounting.money import Money
from zeppelin_cash.errors import Error, ok, Result


class Book:
    """A book contains the entire book for a firm."""

    def __init__(self, time: datetime, currency: Currency = usd()) -> None:
        """Create an empty book.

        Args:
            time: the start time of the book
            currency: the accounting currency of the book
        """
        self.ledger = Ledger([])
        self.journal = Journal()
        self.accounting_currency = currency
        self.__account_id_iter = 3
        self.start_time = time

        # Add the basic ledger accounts

        # Assets
        account = Account("Cash", True, default_cash_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._cash_account_ids = [default_cash_id()]
        account = Account("Accounts Recievable", True,
                          default_accounts_recievable_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._accounts_recievable_ids = [default_accounts_recievable_id()]
        account = Account("Inventory", True, default_inventory_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._inventory_ids = [default_inventory_id()]
        account = Account(
            "Prepaid Expenses",
            True,
            default_prepaid_expenses_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._prepaid_expenses_ids = [default_prepaid_expenses_id()]
        account = Account("Other Assets", True, default_other_assets_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._other_assets_ids = [default_other_assets_id()]
        account = Account("Fixed Assets at Cost", True,
                          default_fixed_assets_at_cost_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._fixed_assets_at_cost_ids = [default_fixed_assets_at_cost_id()]
        account = Account("Accumulated Depreciation", True,
                          default_accumulated_depreciation_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._accumulated_depreciation_ids = [
            default_accumulated_depreciation_id()]

        # Liabilities
        account = Account("Accounts Payable", False,
                          default_accounts_payable_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._accounts_payable_ids = [default_accounts_payable_id()]
        account = Account("Accrued Expenses", False,
                          default_accrued_expenses_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._accrued_expenses_ids = [default_accrued_expenses_id()]
        account = Account("Currenct Portion of Debt", False,
                          default_current_portion_of_debt_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._current_portion_of_debt_ids = [
            default_current_portion_of_debt_id()]
        account = Account("Income Taxes Payable", False,
                          default_income_taxes_payable_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._income_taxes_payable_ids = [default_income_taxes_payable_id()]
        account = Account("Long Term Debt", False, default_long_term_debt_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._long_term_debt_ids = [default_long_term_debt_id()]
        account = Account("Capital Stock", False, default_capital_stock_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._capital_stock_ids = [default_capital_stock_id()]
        account = Account("Retained Earnings", False,
                          default_retained_earnings_id())
        account.set_starting_balance(
            self.start_time, Money(0, self.accounting_currency))
        self.ledger.add_account(account)
        self._retained_earnings_ids = [default_retained_earnings_id()]

        # other account types
        self._sales_account_ids: List[str] = []
        self._cost_of_goods_sold_ids: List[str] = []
        self._sales_and_marketing_ids: List[str] = []
        self._research_and_development_ids: List[str] = []
        self._interest_income_ids: List[str] = []
        self._general_and_administrative_ids: List[str] = []

    def is_valid(self) -> bool:
        """Check If the book is valid.

        Returns:
            True iff the account is valid.
        """
        return self.journal.is_valid()

    def add_transaction(self, transaction: JournalTransaction) -> Error:
        """Add a transaction to the book.

        Valid transactions are automatically pushed from the journal
        to the ledger. This is an atomic operation.

        Returns:
            an error if an error occurs.
        """
        err = self.journal.add_transaction(transaction)
        if not err.is_ok():
            return err
        self.push()
        return ok()

    def push(self) -> None:
        """Push all transactions on the journal to the ledger.

        Returns:
            None
        """
        transactions = self.journal.unpushed_transactions()
        for transaction in transactions:
            for entry in transaction.entries():
                account_entry = AccountEntry(
                    transaction.time(), entry.amount())
                self.ledger.add_entry(entry.account_id(),
                                      entry.is_debit(), account_entry)
        self.journal.have_pushed(len(transactions))

    def __new_account_id(self) -> str:
        """Get a new account id.

        Returns:
            some unique id string
        """
        ret = str(self.__account_id_iter)
        self.__account_id_iter += 1
        return ret

    def balance_sheet(self, time: datetime) -> Result[BalanceSheet]:
        """Get a balance sheet for a given time.

        Args:
            time: the time of the statement

        Returns:
            a balance sheet or an error
        """
        sheet = BalanceSheet(time)
        still_ok = True
        # assets
        sheet.cash, err = self._sum_balances(time, self._cash_account_ids)
        still_ok = still_ok and err.is_ok()
        sheet.accounts_recievable, err = self._sum_balances(
            time, self._accounts_recievable_ids)
        still_ok = still_ok and err.is_ok()
        sheet.inventory, err = self._sum_balances(time, self._inventory_ids)
        still_ok = still_ok and err.is_ok()
        sheet.prepaid_expenses, err = self._sum_balances(
            time, self._prepaid_expenses_ids)
        still_ok = still_ok and err.is_ok()
        sheet.other_assets, err = self._sum_balances(
            time, self._other_assets_ids)
        still_ok = still_ok and err.is_ok()
        sheet.fixed_assets_at_cost, err = self._sum_balances(
            time, self._fixed_assets_at_cost_ids)
        still_ok = still_ok and err.is_ok()
        sheet.accumulated_depreciation, err = self._sum_balances(
            time, self._accumulated_depreciation_ids)
        still_ok = still_ok and err.is_ok()
        # liabilities
        sheet.accounts_payable, err = self._sum_balances(
            time, self._accounts_payable_ids)
        still_ok = still_ok and err.is_ok()
        sheet.accrued_expenses, err = self._sum_balances(
            time, self._accrued_expenses_ids)
        still_ok = still_ok and err.is_ok()
        sheet.current_portion_of_debt, err = self._sum_balances(
            time, self._current_portion_of_debt_ids)
        still_ok = still_ok and err.is_ok()
        sheet.income_taxes_payable, err = self._sum_balances(
            time, self._income_taxes_payable_ids)
        still_ok = still_ok and err.is_ok()
        sheet.long_term_debt, err = self._sum_balances(
            time, self._long_term_debt_ids)
        still_ok = still_ok and err.is_ok()
        sheet.capital_stock, err = self._sum_balances(
            time, self._capital_stock_ids)
        still_ok = still_ok and err.is_ok()
        sheet.retained_earnings, err = self._sum_balances(
            time, self._retained_earnings_ids)
        still_ok = still_ok and err.is_ok()
        return Result(ok=sheet) if still_ok else Result(
            err=Error("cannot calculate balance sheet"))

    def cash_flow_statement(self, start: datetime,
                            end: datetime) -> Result[CashFlowStatement]:
        """Get a cash flow statement for the book.

        Args:
            start: the starting time
            end: the ending time

        Returns:
            a cash flow statement or an error
        """
        statement = CashFlowStatement(start, end)
        still_ok = True

        statement.beginning_cash_balance, err = self._sum_balances(
            start, self._cash_account_ids)
        still_ok = still_ok and err.is_ok()

        first, err = self._sum_balances(end, self._fixed_assets_at_cost_ids)
        still_ok = still_ok and err.is_ok()
        second, err = self._sum_balances(start, self._fixed_assets_at_cost_ids)
        still_ok = still_ok and err.is_ok()
        statement.fixed_asset_purchases = first - second

        first, err = self._sum_balances(end, self._long_term_debt_ids)
        still_ok = still_ok and err.is_ok()
        second, err = self._sum_balances(
            end, self._current_portion_of_debt_ids)
        still_ok = still_ok and err.is_ok()
        third, err = self._sum_balances(start, self._long_term_debt_ids)
        still_ok = still_ok and err.is_ok()
        fourth, err = self._sum_balances(
            start, self._current_portion_of_debt_ids)
        still_ok = still_ok and err.is_ok()
        statement.net_borrowings = first + second - third - fourth

        first, err = self._sum_balances(end, self._capital_stock_ids)
        still_ok = still_ok and err.is_ok()
        second, err = self._sum_balances(start, self._capital_stock_ids)
        still_ok = still_ok and err.is_ok()
        statement.sale_of_stock = first - second

        statement.income_taxes_paid = self._income_taxes_paid(start, end)
        statement.cash_receipts = self._cash_receipts(start, end)
        statement.cash_disbursements = self._cash_disbursements(start, end)

        return Result(ok=statement) if still_ok else Result(
            err=Error("cannot calculate cash flow statement"))

    def income_statement(self, start: datetime,
                         end: datetime) -> Result[IncomeStatement]:
        """Get an income statement for the book.

        Args:
            start: the starting time
            end: the ending time

        Returns:
            an income statement or an error
        """
        statement = IncomeStatement(start, end)
        statement.start_time = start
        statement.end_time = end

        still_ok = True
        first, err = self._sum_balances(end, self._sales_account_ids)
        still_ok = still_ok and err.is_ok()
        second, err = self._sum_balances(start, self._sales_account_ids)
        still_ok = still_ok and err.is_ok()
        statement.net_sales = first - second

        first, err = self._sum_balances(end, self._cost_of_goods_sold_ids)
        still_ok = still_ok and err.is_ok()
        second, err = self._sum_balances(start, self._cost_of_goods_sold_ids)
        still_ok = still_ok and err.is_ok()
        statement.cost_of_goods_sold = first - second

        first, err = self._sum_balances(end, self._sales_and_marketing_ids)
        still_ok = still_ok and err.is_ok()
        second, err = self._sum_balances(start, self._sales_and_marketing_ids)
        still_ok = still_ok and err.is_ok()
        statement.sales_and_marketing = first - second

        first, err = self._sum_balances(
            end, self._research_and_development_ids)
        still_ok = still_ok and err.is_ok()
        second, err = self._sum_balances(
            start, self._research_and_development_ids)
        still_ok = still_ok and err.is_ok()
        statement.research_and_development = first - second

        first, err = self._sum_balances(
            end, self._general_and_administrative_ids)
        still_ok = still_ok and err.is_ok()
        second, err = self._sum_balances(
            start, self._general_and_administrative_ids)
        still_ok = still_ok and err.is_ok()
        statement.general_and_administrative = first - second

        first, err = self._sum_balances(end, self._interest_income_ids)
        still_ok = still_ok and err.is_ok()
        second, err = self._sum_balances(start, self._interest_income_ids)
        still_ok = still_ok and err.is_ok()
        statement.interest_income = first - second

        statement.income_taxes = self._income_taxes_paid(start, end)
        return Result(ok=statement) if still_ok else Result(
            err=Error("cannot calculate income statement"))

    def financial_statement(self, start: datetime,
                            end: datetime) -> Result[FinancialStatement]:
        """Get a financial statement for the book.

        This implementation returns a financial statement with all zero values.

        Returns:
            A financial statement.
        """
        self.push()
        bs_result = self.balance_sheet(end)
        if not bs_result.is_ok():
            return Result(err=bs_result.err())
        balance_sheet = bs_result.ok()
        cf_result = self.cash_flow_statement(start, end)
        if not cf_result.is_ok():
            return Result(err=cf_result.err())
        cash_flow = cf_result.ok()
        is_result = self.income_statement(start, end)
        if not is_result.is_ok():
            return Result(err=is_result.err())
        income = is_result.ok()
        return Result(ok=FinancialStatement(balance_sheet, cash_flow, income))

    def _sum_balances(self, time: datetime,
                      account_ids: List[str]) -> Tuple[Money, Error]:
        """Sum the balances at a given time of the accounts listed.

        Args:
            time: the time of the balance
            account_ids: the accounts to sum

        Returns:
            The sum.
        """
        total = Money(0, self.accounting_currency)
        for account_id in account_ids:
            result = self.ledger.balance_as_of_date(time, account_id)
            if not result.is_ok():
                return total, result.err()
            total += result.ok()
        return total, ok()

    def _income_taxes_paid(self, start: datetime, end: datetime) -> Money:
        """Calculate the income taxes paid.

        This looks for entries that reduce income taxes receivable.

        Args:
            start: the start time in which to look
            end: the end time in which to look

        Returns:
            The income taxes paid in the period.
        """
        ret = Money(0.0, self.accounting_currency)
        for transaction in self.journal.transactions:
            if transaction.time() < start or transaction.time() > end:
                continue
            for entry in transaction.entries():
                if entry.account_id() in self._income_taxes_payable_ids and entry.is_debit():
                    ret += entry.amount()
        return ret

    def _cash_receipts(self, start: datetime, end: datetime) -> Money:
        """Calculate the cash receipts for a period.

        Cash reciepts are anything that increases cash that is not
        from capital stock or borrowing. Usually this is from sales.

        Args:
            start: the start of the period
            end: the end of the period

        Returns:
            The cash receipts in the period.
        """
        ret = Money(0.0, self.accounting_currency)
        negs = self._capital_stock_ids + \
            self._long_term_debt_ids + \
            self._current_portion_of_debt_ids + \
            self._income_taxes_payable_ids + \
            self._fixed_assets_at_cost_ids
        for transaction in self.journal.transactions:
            if transaction.time() < start or transaction.time() > end:
                continue
            cash_diff = Money(0, self.accounting_currency)
            capital_and_borrowing_diff = Money(0, self.accounting_currency)
            for entry in transaction.entries():
                if entry.account_id() in self._cash_account_ids:
                    cash_diff += entry.amount().scale(1.0 if entry.is_debit() else -1.0)
                elif entry.account_id() in negs:
                    factor = 1.0 if entry.is_debit() else -1.0
                    capital_and_borrowing_diff += entry.amount().scale(factor)
            diff = cash_diff + capital_and_borrowing_diff
            if diff.quantity() > 0.0:
                ret += diff
        return ret

    def _cash_disbursements(self, start: datetime, end: datetime) -> Money:
        """Calculate the cash disbursements for a period.

        Cash disbursements are all cash payments other than paying off
        debt, buying back stock, or paying taxes.

        Args:
            start: the start of the period
            end: the end of the period

        Returns:
            The cash receipts in the period.
        """
        ret = Money(0.0, self.accounting_currency)
        negs = self._capital_stock_ids + \
            self._long_term_debt_ids + \
            self._current_portion_of_debt_ids + \
            self._income_taxes_payable_ids + \
            self._fixed_assets_at_cost_ids
        for transaction in self.journal.transactions:
            if transaction.time() < start or transaction.time() > end:
                continue
            cash_diff = Money(0, self.accounting_currency)
            capital_and_borrowing_diff = Money(0, self.accounting_currency)
            for entry in transaction.entries():
                if entry.account_id() in self._cash_account_ids:
                    cash_diff += entry.amount().scale(1.0 if entry.is_debit() else -1.0)
                elif entry.account_id() in negs:
                    capital_and_borrowing_diff += entry.amount().scale(
                        1.0 if entry.is_debit() else -1.0)
            diff = cash_diff + capital_and_borrowing_diff
            if diff.quantity() < 0.0:
                ret += diff.scale(-1.0)
        return ret

    def add_account(self, name: str, is_asset: bool) -> AccountId:
        """Add a new account to the book.

        Args:
            name: the human-readable name of the account
            is_asset: whether or not the account represents an asset.
                If the account represents an asset, then the balance of the
                account is added to the balance sheet. Otherwise, the account represents
                liabilities and the value is subtracted from the balance sheet.

        Returns:
            The id for the new account.
        """
        new_id = self.__new_account_id()
        assert self.ledger.add_account(Account(name, is_asset, new_id)).is_ok()
        self._cash_account_ids.append(new_id)
        return new_id

    def list_accounts(self, timestamp: datetime) -> List[AccountMetadata]:
        """List all of the accounts on the ledger.

        This will push all journalled transactions to the accounts
        in order to calculate updated balances.

        Args:
            timestamp: the timestamp at which the account balances should be calculated.

        Returns:
            The metadata for all existing accounts in the ledger."""
        self.push()
        return self.ledger.list_accounts(timestamp)

    def add_cash_account(self, name: str) -> str:
        """Add a cash account to the list of accounts.

        TODO(gs): Similar account adding methods should be made
        for other types of accounts.

        Args:
            name: name of the account

        Returns:
            The id of the new account.
        """
        new_id = self.__new_account_id()
        assert self.ledger.add_account(Account(name, True, new_id)).is_ok()
        self._cash_account_ids.append(new_id)
        return new_id

    def add_research_and_development_account(self, name: str) -> str:
        """Add a research and development account.

        Args:
            name: the name of the account

        Returns:
            The id of the new account.
        """
        new_id = self.__new_account_id()
        assert self.ledger.add_account(Account(name, True, new_id)).is_ok()
        self._research_and_development_ids.append(new_id)
        return new_id


# id getters


def default_cash_id() -> str:
    """Get the id of the cash account.

    Returns:
        "cash"
    """
    return "cash"


def default_accounts_recievable_id() -> str:
    """Get the id of the accounts recievable account.

    Returns:
        "accounts-recievable"
    """
    return "accounts-recievable"


def default_inventory_id() -> str:
    """Get the id of the inventory account.

    Returns:
        "inventory"
    """
    return "inventory"


def default_prepaid_expenses_id() -> str:
    """Get the id of the prepaid expenses account.

    Returns:
        "prepaid expenses"
    """
    return "prepaid-expenses"


def default_other_assets_id() -> str:
    """Get the id of the other assets account.

    Returns:
        "other-assets"
    """
    return "other-assets"


def default_fixed_assets_at_cost_id() -> str:
    """Get the id of the fixed assets at cost account.

    Returns:
        "fixed-assets-at-cost"
    """
    return "fixed-assets-at-cost"


def default_accumulated_depreciation_id() -> str:
    """Get the id of the accumulated depreciation account.

    Returns:
        "accumulated-depreciation"
    """
    return "accumulated-depreciation"


def default_accounts_payable_id() -> str:
    """Get the id of the accounts payable account.

    Returns:
        "accounts-payable"
    """
    return "accounts-payable"


def default_accrued_expenses_id() -> str:
    """Get the id of the accrued expnses account.

    Returns:
        "accrued-expenses"
    """
    return "accrued-expenses"


def default_current_portion_of_debt_id() -> str:
    """Get the id of the current portion of debt account.

    Returns:
        "current-portion-of-debt"
    """
    return "current-portion-of-debt"


def default_income_taxes_payable_id() -> str:
    """Get the id of the income taxes payable account.

    Returns:
        "income-taxes-payable-id"
    """
    return "income-taxed-payable-id"


def default_long_term_debt_id() -> str:
    """Get the id of the long term debt account.

    Returns:
        "long-term-debt"
    """
    return "long-term-debt"


def default_capital_stock_id() -> str:
    """Get the id of the capital stock account.

    Returns:
        "capital-stock"
    """
    return "capital-stock"


def default_retained_earnings_id() -> str:
    """Get the id of the retained earnings account.

    Returns:
        "retained-earnings"
    """
    return "retained-earnings"
