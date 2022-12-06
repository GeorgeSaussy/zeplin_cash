from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from zeppelin_cash.accounting.account import Account, AccountId
from zeppelin_cash.accounting.account_metadata import AccountMetadata
from zeppelin_cash.accounting.financial_statement import FinancialStatement
from zeppelin_cash.accounting.journal_transaction import JournalTransaction
from zeppelin_cash.errors import Result
from zeppelin_cash.errors.error import Error

"""
TODO(OMEGA-411): The client is not feature complete.
    - It should be possible to revoke API keys.
    - User accounts should be organized into organizations.
    - Users should be able to belong to more than one organization.
    - It should be possible for a organization to own another organization.
    - It should be possible for users to have different
      read/write permissions for different accounts.
    - User permissions and membership should be able to be synced with LDAP.
"""


class Client(ABC):
    """A Client can read from the treasury service."""

    @abstractmethod
    def financial_statement(self, start: datetime,
                            end: datetime) -> Result[FinancialStatement]:
        pass

    @abstractmethod
    def list_accounts(
            self, timestamp: datetime) -> Result[List[AccountMetadata]]:
        pass

    @abstractmethod
    def add_account(self, account_name: str,
                    is_asset: bool) -> Result[AccountId]:
        pass

    @abstractmethod
    def get_account(self, account_id: AccountId) -> Result[Account]:
        pass

    @abstractmethod
    def add_transaction(self, txn: JournalTransaction) -> Error:
        pass
