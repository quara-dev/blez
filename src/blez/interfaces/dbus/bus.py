from __future__ import annotations

from enum import Enum
from typing import Protocol

from .encoder import Message


class BusType(Enum):
    """An enum that indicates a type of bus. On most systems, there are
    normally two different kinds of buses running.
    """

    SESSION = 1  #: A bus for the current graphical user session.
    SYSTEM = 2  #: A persistent bus for the whole machine.


class Bus(Protocol):
    """A bus is used to send and receive messages between D-Bus clients or services."""

    def __init__(
        self,
        bus_address: str | None = None,
        bus_type: BusType = BusType.SYSTEM,
        negociate_unix_fd: bool = True,
    ) -> None:
        raise NotImplementedError

    async def connect(self) -> None:
        raise NotImplementedError

    def disconnect(self):
        """Disconnect the message bus by closing the underlying connection asynchronously.

        All pending  and future calls will error with a connection error.
        """
        raise NotImplementedError

    async def call(self, msg: Message) -> Message:
        raise NotImplementedError
