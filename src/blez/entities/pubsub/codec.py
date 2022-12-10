from __future__ import annotations

import abc
from typing import Generic, TypeVar

EncodedT = TypeVar("EncodedT")
DecodedT = TypeVar("DecodedT")


class CodecProtocol(Generic[EncodedT, DecodedT], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encode(self, data: DecodedT) -> EncodedT:
        ...

    @abc.abstractmethod
    def decode(self, value: EncodedT) -> DecodedT:
        ...
