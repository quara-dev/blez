from __future__ import annotations

import abc
from typing import Callable, Generic, TypeVar

DataT = TypeVar("DataT")
T = TypeVar("T")


class ReplyProtocol(Generic[DataT], metaclass=abc.ABCMeta):
    def __init__(
        self,
        code: int | None,
        subject: str,
        origin: str,
        data: DataT,
    ) -> None:
        self.code = code
        self.subject = subject
        self.origin = origin
        self.data = data

    @abc.abstractmethod
    def raise_for_status(self, code: int | None = None) -> None:
        ...

    @abc.abstractmethod
    def get_data(self, as_: Callable[[DataT], T] | type[T]) -> T:
        ...
