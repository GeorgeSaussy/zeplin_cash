from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from zeppelin_cash.accounting.money import Money


@dataclass
class AccountMetadata:
    """An AccountMetadata instance contains a brief overview of an account."""
    account_id: str
    name: str
    # mey be empty if invalid timestamp for given account
    balance: Optional[Money]
    balance_timestamp: datetime
    is_asset: bool
