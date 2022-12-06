"""This module contains some utility functions for wallet.errors."""
from zeppelin_cash.errors.error import Error


def ok() -> Error:  # pylint: disable=C0103
    """Get an ok Error instance.

    Returns:
        an okay error."""
    return Error()
