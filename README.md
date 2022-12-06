# README

This is the Zeppelin Cash accounting system. 
It is designed to generate and manipulate financial statements.

## Usage

The library implements a logical model of GAAP-compliant financial statements. 
The in-line documentation include an overview of how a financial statement works,
e.g. looking at `BalanceSheet` implementation in `./src/zeppelin_cash/accounting/balance_sheet.py`,
the definition of "prepaid expenses" is given:

```python
# Prepaid expenses are the vaud of goods or service that the firm has
# paid for, bug which have not yet been relised. For example, say
# WidgetTech orders 1,000 widget parts and pays for them. For the time
# between paying for the order and the parts arriving, the value of the
# parts is accounted for as a prepaid expense.
self.prepaid_expenses = Money(0, self.currency)
```

To generate a simple financial statement with the default set of accounts, import the library
and run something like

```python
from datetime import datetime, timedelta

from zeppelin_cash.accounting.book import Book, default_cash_id, default_capital_stock_id
from zeppelin_cash.fs_book_engine import FsBookEngine
from zeppelin_cash.accounting.journal_transaction import JournalTransaction
from zeppelin_cash.accounting.journal_entry import JournalEntry
from zeppelin_cash.accounting.money import Money
from zeppelin_cash.accounting.america import usd

# Create the general ledger for a firm started today.
founding_date = datetime.now()
book = Book(founding_date)

# Invest $1mm into the firm one second after it is created.
transaction = JournalTransaction(
                start + timedelta(seconds=1), # when the transaction occurred
                "Investing some cash", # a human readable note
                [
                    # debiting the default capital stock account
                    # (other capital stock accounts can be created through the BalanceSheet API)
                    JournalEntry( 
                        default_capital_stock_id(), # the ID of the account to debit 
                        False,                      # False => account debit
                        Money(1000000, usd())       # the amount to debit, $1mm
                    ),
                    # credit the cash account
                    JournalEntry(
                        default_cash_id(),   # the ID of the account to credit
                        True,                # True => account credit
                        Money(1000000, usd() # the amount to credit, $1mm
                    )),
                ]) 
err = book.add_transaction(transaction)

# Assert the transaction could be added to the general ledger.
# This would fail if the total credits and debits did not balance.
assert err.is_ok()

# Get the balance sheet from one second later.
balance_sheet_result = book.balance_sheet(founding_date + timedelta(seconds=2))
assert bs_result.is_ok() # this will fail if the book is invalid,
                         # e.g. a date before the founding is requested, or the
                         # credits and debits do not add up. 
balance_sheet = bs_result.ok()

# We expect the balance sheet to show 1M USD in cash.
assert balance_sheet.cash.quantity() == 1000000
# We also expect it to show 1M USD in shareholder equity.
assert balance_sheet.shareholders_equity().quantity() == 1000000

# Finally, we can print the full financial statement for the period spanning
# the firm's founding to two seconds later.
financial_stmt_result = book.financial_statement(founding_date, founding_date + timedelta(seconds=2))
assert financial_stmt_result.is_ok()
financial_stmt = financial_stmt_result.ok()
print(financial_stmt)
```

## Warnings

This repo comes from my notes from reading ["Accounting" by Peter Eisen](https://www.amazon.com/Accounting-Barrons-Business-Review-Peter/dp/143800138X).
Those notes were taken in the from of Python scripts that implemented the logical model of a financial statement.
Those scripts were then polished and combined into this repository.
While pre-1.0, majority of the public facing API is stable, if a implemented verbosely.
The main change is the storage engine, which simply pickles the Python object.
I would strongly recommend *not* using this feature.