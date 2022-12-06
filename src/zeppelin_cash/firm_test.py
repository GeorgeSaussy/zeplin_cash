"""The module medici.test_firm tests the Firm implementation."""
from datetime import datetime, timedelta

from zeppelin_cash.firm import Firm


def test_firm() -> None:
    """Test the Firm implementation."""
    start = datetime.now()
    firm = Firm(start)
    result = firm.financial_statement(start, start + timedelta(seconds=1))
    assert result.is_ok()
    assert result.ok().cash_flow_statement.cash_disbursements.quantity() == 0
    result = firm.financial_statement(start - timedelta(seconds=1), start)
    assert not result.is_ok()
