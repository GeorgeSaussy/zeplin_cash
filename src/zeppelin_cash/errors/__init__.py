"""The wallet.errors.module contains some error handling code.

The goal is to avoid exceptions where possible.
"""
from zeppelin_cash.errors.either import Either
from zeppelin_cash.errors.error import Error
from zeppelin_cash.errors.result import Result
from zeppelin_cash.errors.util import ok
