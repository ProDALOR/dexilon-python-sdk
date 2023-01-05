from typing import List, Optional

from pydantic import parse_obj_as
from .responses import ErrorBody
from .chain_responses import ChainErrorBody


class DexilonException(Exception):

    code: int = 0
    message: str = ''
    details: Optional[List[str]] = None

    def __str__(self) -> str:
        return f'Error(code={self.code}): {self.message}{f" {self.details}" if self.details else ""}'


class DexilonAPIException(DexilonException):

    def __init__(self, code: int, message: str, details: str = None):
        self.code = code
        self.message = message
        self.details = details

    @classmethod
    def from_dict(cls, data: dict) -> 'DexilonAPIException':
        error = parse_obj_as(ErrorBody, data)
        return cls(
            code=error.code,
            message=error.name,
            details=error.details
        )


class DexilonChainException(DexilonException):

    def __init__(self, code: int, message: str, details: str = None):
        self.code = code
        self.message = message
        self.details = details

    @classmethod
    def from_dict(cls, data: dict) -> 'DexilonChainException':
        error = parse_obj_as(ChainErrorBody, data)
        return cls(
            code=error.code,
            message=error.message,
            details=error.details
        )


class DexilonRequestException(DexilonException):

    def __init__(self, message: str):
        self.message = message


class DexilonApiAuthException(DexilonAPIException):

    pass


class DexilonChainAuthException(DexilonChainException):

    pass
