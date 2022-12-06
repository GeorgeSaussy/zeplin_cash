"""The wallet.errors.error module contains the Error implementation."""
from typing import Optional


class Error:
    """Error represents an error in the program."""

    def __init__(self, message: Optional[str] = None) -> None:
        """Create a new error.

        Args:
            message: the error message
        """
        self.msg = message if not message is None else ""
        self.ok_err = message is None

    def message(self) -> str:
        """Get the error message.

        Returns:
            the error message
        """
        return self.msg

    def is_ok(self) -> bool:
        """Check if the error is okay.

        Returns:
            True iff the error is okay.
        """
        return self.ok_err
