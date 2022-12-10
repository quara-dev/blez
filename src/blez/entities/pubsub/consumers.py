from __future__ import annotations

import abc
from typing import AsyncIterator, Awaitable, Callable, Generic, TypeVar

T = TypeVar("T")
InputT = TypeVar("InputT")
ReturnT = TypeVar("ReturnT")


class PullConsumerProtocol(Generic[T], metaclass=abc.ABCMeta):
    """A consumer is active from the moment it is created.

    It is a subscription which acknowledge received item upon callback completion.
    """

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

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stopping a consumer should cancel all pending iterators
        and stop the subscription regardless of pending messages."""
        ...

    @abc.abstractmethod
    async def drain(
        self, timeout: float | None = None, deadline: float | None = None
    ) -> None:
        """Draining a consumer should wait for all pending messages to be processed
        before cancelling the subscription.

        If not all pending messages are processed before deadline (or timeout),
        subscription is stopped, I.E, all pending messages are dropped without
        being acknowledged and iterators are cancelled.

        Raises:
            TimeoutError: when subscription is stopped due to pending subscribers not completing before deadline.
        """
        ...


class PushConsumerProtocol(Generic[InputT], metaclass=abc.ABCMeta):
    """A worker is active from the moment it is created.

    It is a subscription which acknowledge received item upon callback completion.
    """

    @abc.abstractproperty
    def callback(self) -> Callable[[InputT], Awaitable[None]]:
        """Function executed on each received item."""
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stopping a push consumer should cancel the callback regardless of pending messages."""
        ...

    @abc.abstractmethod
    async def drain(
        self, timeout: float | None = None, deadline: float | None = None
    ) -> None:
        """Draining a push consumer should wait for all pending messages to be processed
        before cancelling the subscription

        If not all pending messages are processed before deadline (or timeout),
        consumer is stopped, I.E, all pending messages are dropped without
        being acknowledged.

        Raises:
            TimeoutError: when worker is stopped due to pending subscribers not completing before deadline.
        """
        ...
