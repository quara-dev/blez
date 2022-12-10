from __future__ import annotations

import abc
from typing import Any, Awaitable, Callable, Generic, Mapping, TypeVar

from blez.entities.pubsub.consumers import PullConsumerProtocol, PushConsumerProtocol

from .codec import CodecProtocol
from .replies import ReplyProtocol
from .services import ReturnT, ServiceProtocol
from .subscriptions import SubscriptionProtocol

MsgT = TypeVar("MsgT")
StreamMsgT = TypeVar("StreamMsgT")


class PubSubProtocol(Generic[MsgT, StreamMsgT], metaclass=abc.ABCMeta):
    """Backend for publish/subscribe broker"""

    @abc.abstractmethod
    def get_codec(self) -> CodecProtocol[Any, MsgT]:
        ...

    @abc.abstractmethod
    async def connect(self) -> None:
        """Connect to message broker server.

        Broker is expected to be configured on initialization.
        As such connection can be performed without option.
        """
        ...

    @abc.abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from broker server."""
        ...

    @abc.abstractmethod
    async def drain(
        self, timeout: float | None = None, deadline: float | None = None
    ) -> None:
        """Drain subscriptions and services before disconnecting from broker server."""
        ...

    @abc.abstractmethod
    async def create_service(
        self,
        subject: str,
        cb: Callable[[MsgT], Awaitable[ReturnT]],
        queue: str | None = None,
        tokens: Mapping[str, Any] | None = None,
    ) -> ServiceProtocol[MsgT, ReturnT]:
        """Create a new service on given subject.

        Service is started as soon as it is created.
        """
        ...

    @abc.abstractmethod
    async def create_subscription(
        self,
        subject: str,
        queue: str | None = None,
        tokens: Mapping[str, Any] | None = None,
    ) -> SubscriptionProtocol[MsgT]:
        """Create a new subscription on given subject.

        Subscription is started as soon as it is created.
        """
        ...

    @abc.abstractmethod
    async def create_pull_consumer(
        self,
        name: str,
        subjects: list[str],
        tokens: Mapping[str, Any] | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> PullConsumerProtocol[StreamMsgT]:
        ...

    @abc.abstractmethod
    async def create_push_consumer(
        self,
        name: str,
        subjects: list[str],
        callback: Callable[[StreamMsgT], Awaitable[None]],
        tokens: Mapping[str, Any] | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> PushConsumerProtocol[StreamMsgT, None]:
        ...

    @abc.abstractmethod
    def publish_no_wait(
        self, subject: str, data: MsgT, tokens: Mapping[str, Any] | None = None
    ) -> None:
        """Append a new message to the publish buffer."""
        ...

    @abc.abstractmethod
    async def publish(
        self,
        subject: str,
        data: MsgT,
        tokens: Mapping[str, Any] | None = None,
        timeout: float | None = None,
        deadline: float | None = None,
    ) -> None:
        """Publish a message and wait until message is sent to underlying transport.

        Raises:
            TimeoutError: message was not flushed to transport before timeout.
        """
        ...

    @abc.abstractmethod
    async def request(
        self,
        subject: str,
        data: MsgT,
        tokens: Mapping[str, Any] | None = None,
        timeout: float | None = None,
        deadline: float | None = None,
    ) -> ReplyProtocol[MsgT]:
        """Send a request and wait for a reply.

        Raises:
            NotFoundError: no service listening on subject.
            TimeoutError: no reply before deadline.
        """
        ...

    @abc.abstractmethod
    async def flush(
        self, timeout: float | None = None, deadline: float | None = None
    ) -> None:
        """Force publish buffer to be flushed to underlying transport.

        Raises:
            TimeoutError: when publish buffer is not be flushed before deadline.
        """
        ...

    @abc.abstractmethod
    def get_tokens(self) -> dict[str, Any]:
        ...

    @abc.abstractmethod
    def update_tokens(self, values: Mapping[str, Any] | None) -> None:
        ...
