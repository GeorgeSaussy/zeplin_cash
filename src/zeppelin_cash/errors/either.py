"""The wallet.errors.either module contains the Either implementation."""
from typing import Generic, Optional, Type, TypeVar

T = TypeVar("T")  # pylint: disable=C0103
U = TypeVar("U")  # pylint: disable=C0103


class EitherException(Exception):
    """An EitherException is thrown by an Either implementation.

    It is thrown when an Either instance is misconfigured."""


class Either(Generic[T, U]):
    """Either can be be used instead of a union type."""

    def __init__(self, first: Optional[T] = None,
                 second: Optional[U] = None) -> None:
        """Create a new Either instance.

        Exactly one of `first` or `second` must be non-None.

        Args:
            first: the possible first value
            second: the possible second value
        """
        if first is None and second is None:
            raise EitherException("either must contain a value")
        if (not first is None) and (not second is None):
            raise EitherException("either must not contain both values")
        self._first: Optional[T] = first
        self._second: Optional[U] = second

    @classmethod
    def of_first(cls: Type["Either"], first: T) -> "Either":
        """Create an instance of first type.

        Args:
            first: the value of the Either instance.

        Returns:
            A new either instance.
        """
        return cls(first=first)

    @classmethod
    def of_second(cls: Type["Either"], second: U) -> "Either":
        """Create an instance of the second type.

        Args:
            second: the value of the Either instance.

        Returns:
            A new either instance.
        """
        return cls(second=second)

    def is_first(self) -> bool:
        """Check if the Either instance is the first type.

        Returns:
            True iff the instance is the first type.
        """
        return self._first is not None

    def first(self) -> T:
        """Get the first value.

        Returns:
            The value, or an exception if it is not the first type.
        """
        if self._first is None:
            raise EitherException(
                "cannot get first value from Either instance")
        return self._first

    def second(self) -> U:
        """Get the second value.

        Returns:
            The value, or an exception if it is not the second type.
        """
        if self._second is None:
            raise EitherException(
                "cannot get the second value from Either instance")
        return self._second
