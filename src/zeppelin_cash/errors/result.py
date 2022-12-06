"""Result contains the Result class implementation."""
from typing import Generic, Optional, TypeVar
from zeppelin_cash.errors.error import Error

# pylint: disable=C0103
T = TypeVar("T")


class ResultException(Exception):
    """An exception thrown by the Result implementation."""


class Result(Generic[T]):
    """A Result class for encapsulating return types that can fail."""

    def __init__(self, ok: Optional[T] = None,
                 err: Optional[Error] = None) -> None:
        """Create a result instance from a value."""
        if ok is None and err is None:
            raise ResultException(
                "ok value and error value cannot both be None")
        if (not ok is None) and (not err is None):
            raise ResultException(
                "one of ok value and error cannot both be present")
        self._ok: Optional[T] = ok
        self._err: Optional[Error] = err

    @classmethod
    def of_ok(cls, ok_value: T) -> "Result":
        """Create a new okay Result instance.

        Args:
            ok_value: the ok value

        Returns:
            A new Result instance.
        """
        return Result(ok=ok_value)

    @classmethod
    def of_err(cls, error_value: Error) -> "Result":
        """Create a new error instance.

        Args:
            error_value: the error value

        Returns:
            A new Result instance.
        """
        return Result(err=error_value)

    def is_ok(self) -> bool:
        """Check if the result is okay.

        Returns:
            True iff the result is okay
        """
        return self._ok is not None

    def ok(self) -> T:
        """Get the okay value.

        This will throw an exception if the result is not ok.

        Returns:
            The ok value.
        """
        if self._ok is None:
            raise ResultException(
                "cannot get the ok value for an error result")
        return self._ok

    def err(self) -> Error:
        """Get the error value.

        This will throw an exception if the result is not an error.

        Returns:
            The error value.
        """
        if self._err is None:
            raise ResultException(
                "cannot get the error value for an ok result")
        return self._err
