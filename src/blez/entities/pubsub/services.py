from __future__ import annotations

import abc
from typing import Awaitable, Callable, Generic, TypeVar

InputT = TypeVar("InputT")
ReturnT = TypeVar("ReturnT")


class ServiceProtocol(Generic[InputT, ReturnT], metaclass=abc.ABCMeta):
    """A service is active from the moment it is created.

    It is a subscription which execute a callback on each received item.
    """

    @abc.abstractproperty
    def callback(self) -> Callable[[InputT], Awaitable[ReturnT]]:
        """Service callback executed on each received items."""
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stopping a service should cancel the subscription callback
        regardless of pending messages."""
        ...

    @abc.abstractmethod
    async def drain(
        self, timeout: float | None = None, deadline: float | None = None
    ) -> None:
        """Draining a subscription should wait for all pending messages to be processed
        before cancelling the subscription callback.

        If not all pending messages are processed before deadline (or timeout),
        subscription is stopped, I.E, all pending subscribers are cancelled.

        Raises:
            TimeoutError: when subscription is stopped due to pending subscribers not completing before deadline.
        """
        ...
