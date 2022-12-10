from __future__ import annotations

from enum import Enum
from typing import Any, Generic, TypeVar

from typing_extensions import Literal

SuccessT = TypeVar("SuccessT")
FailureT = TypeVar("FailureT")
ExceptionT = TypeVar("ExceptionT")


class ResultStatus(str, Enum):
    OK = "OK"
    FAILURE = "FAILURE"
    ERROR = "ERROR"


class Result:
    def is_success(self) -> bool:
        raise NotImplementedError

    def is_failure(self) -> bool:
        raise NotImplementedError

    def is_error(self) -> bool:
        raise NotImplementedError

    @classmethod
    def create_result(
        cls,
        code: int,
        success: SuccessT | None = None,
        failure: FailureT | None = None,
        error: ExceptionT | None = None,
    ) -> Success[None] | Success[SuccessT] | Failure[FailureT] | Error[ExceptionT]:
        """Create a result which may be a success, a failure or an error."""
        if error is not None:
            return cls.create_error(code, error)
        elif failure is not None:
            return cls.create_failure(code, failure)
        elif success:
            return cls.create_success(code, success)
        else:
            return Success(code=code, status=ResultStatus.OK, value=None)

    @classmethod
    def create_error(cls, code: int, exception: ExceptionT) -> Error[ExceptionT]:
        """Create an error."""
        return Error(code, ResultStatus.ERROR, exception)

    @classmethod
    def create_failure(cls, code: int, failure: FailureT) -> Failure[FailureT]:
        """Create a failure."""
        return Failure(code, ResultStatus.FAILURE, failure)

    @classmethod
    def create_success(cls, code: int, value: SuccessT) -> Success[SuccessT]:
        """Create a success."""
        return Success(code, ResultStatus.OK, value)


class Success(Result, Generic[SuccessT]):
    def __init__(
        self, code: int, status: Literal[ResultStatus.OK], value: SuccessT
    ) -> None:
        self.code = code
        self.status = status
        self.value = value

    def __bool__(self) -> Literal[True]:
        return True

    def is_success(self) -> Literal[True]:
        return True

    def is_failure(self) -> Literal[False]:
        return False

    def is_error(self) -> Literal[False]:
        return False

    def get_value(self) -> SuccessT:
        return self.value

    def get_failure(self) -> None:
        return None

    def get_error(self) -> None:
        return None


class Failure(Result, Generic[FailureT]):
    def __init__(
        self, code: int, status: Literal[ResultStatus.FAILURE], value: FailureT
    ) -> None:
        self.code = code
        self.status = status
        self.value = value

    def __bool__(self) -> Literal[False]:
        return False

    def is_success(self) -> Literal[False]:
        return False

    def is_failure(self) -> Literal[True]:
        return True

    def is_error(self) -> Literal[False]:
        return False

    def get_value(self) -> None:
        return None

    def get_failure(self) -> FailureT:
        return self.value

    def get_error(self) -> None:
        return None


class Error(Result, Generic[ExceptionT]):
    def __init__(
        self, code: int, status: Literal[ResultStatus.ERROR], value: ExceptionT
    ) -> None:
        self.code = code
        self.status = status
        self.value = value

    def __bool__(self) -> Literal[False]:
        return False

    def is_success(self) -> Literal[False]:
        return False

    def is_failure(self) -> Literal[False]:
        return False

    def is_error(self) -> Literal[True]:
        return True

    def get_value(self) -> None:
        return None

    def get_failure(self) -> None:
        return None

    def get_error(self) -> ExceptionT:
        return self.value
