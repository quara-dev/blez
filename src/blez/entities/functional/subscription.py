from __future__ import annotations

import abc
from typing import Any, AsyncIterator, Awaitable, Callable, Generic, TypeVar

T = TypeVar("T")


class PubSub:
    """Backend for publish/subscribe"""

    @abc.abstractmethod
    async def connect(self) -> None:
        ...

    @abc.abstractmethod
    async def disconnect(self) -> None:
        ...

    @abc.abstractmethod
    async def create_service(
        self, subject: str, cb: Callable[..., Awaitable[Any]]
    ) -> ServiceProtocol:
        ...

    @abc.abstractmethod
    async def subscribe(self, subjec: str) -> SubscriptionProtocol:
        ...

    @abc.abstractmethod
    def publish_no_wait(self, subject: str, data: bytes) -> None:
        ...


class SubscriptionProtocol(Generic[T]):
    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...

    async def drain(self) -> None:
        ...

    async def next(self) -> T:
        ...

    async def iterate(self) -> AsyncIterator[T]:
        ...


class ServiceProtocol:
    async def drain(self) -> None:
        ...

    async def stop(self) -> None:
        ...
