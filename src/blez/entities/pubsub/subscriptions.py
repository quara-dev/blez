from __future__ import annotations

import abc
from typing import AsyncIterator, Generic, TypeVar

T = TypeVar("T")


class SubscriptionProtocol(Generic[T], metaclass=abc.ABCMeta):
    """A subscription is active from the moment it is created.

    As such, it does not have a start() method, but it provides two methods
    to stop receiving data:
        - stop() method can be used to immediatly stop the subscription, regardless of pending messages.
        - drain() method can be used to stop receiving data immedialty, but wait until pending messages are processed.
    """

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stopping a subscription does not wait until pending messages are processed."""
        ...

    @abc.abstractmethod
    async def drain(
        self, timeout: float | None = None, deadline: float | None = None
    ) -> None:
        """Draining a subscription should wait for all pending messages to be processed.

        If not all pending messages are processed before deadline (or timeout),
        subscription is stopped, I.E, all pending subscribers are lost.

        Warning: Draining a subscription with unprocessed messages can cause a deadlock when
        both timeout argument and deadline argument are None.

        Raises:
            TimeoutError: when subscription is stopped due to pending subscribers not completing before deadline.
        """
        ...

    @abc.abstractmethod
    async def get_next(
        self, timeout: float | None = None, deadline: float | None = None
    ) -> T:
        """Get next item to process.

        Raises:
            TimeoutError: when no message was received before deadline.
        """
        ...

    @abc.abstractmethod
    async def get_batch(
        self, max_size: int, timeout: float | None = None, deadline: float | None = None
    ) -> list[T]:
        """Get a batch of items to process.

        Wait until either max_size items are received or deadline is reached.

        Raises:
            TimeoutError: when no message was received before deadline
        """
        ...

    @abc.abstractmethod
    async def iterate(self, max_size: int | None = None) -> AsyncIterator[T]:
        """Iterate over items to process.

        Subscription is not stopped automatically when iterator exits.
        It is up to developers to always stop subscriptions when they are
        no longer useful.
        """
        ...
