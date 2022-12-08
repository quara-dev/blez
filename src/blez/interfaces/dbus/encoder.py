from __future__ import annotations

from enum import IntEnum, IntFlag
from typing import Any, Mapping, Protocol


class MessageFlag(IntFlag):
    """Flags that affect the behavior of sent and received messages"""

    NONE = 0
    NO_REPLY_EXPECTED = 1  #: The method call does not expect a method return.
    NO_AUTOSTART = 2
    ALLOW_INTERACTIVE_AUTHORIZATION = 4


class MessageType(IntEnum):
    """An enum that indicates a type of message."""

    METHOD_CALL = 1  #: An outgoing method call.
    METHOD_RETURN = 2  #: A return to a previously sent method call
    ERROR = 3  #: A return to a method call that has failed
    SIGNAL = 4  #: A broadcast signal to subscribed connections


class SignatureType(Protocol):
    token: str
    children: list[SignatureType]

    def verify(self, body: Any) -> bool:
        ...


class SignatureTree(Protocol):
    signature: str
    types: list[SignatureType]

    def verify(self, body: list[Any]) -> bool:
        ...


class Variant(Protocol):
    signature: str
    type: SignatureType
    value: Any


class Message(Protocol):
    """Message protocol"""

    destination: str | None
    path: str | None
    interface: str | None
    member: str | None
    message_type: int | MessageType
    flags: int | MessageFlag
    error_name: str | None
    reply_serial: int
    sender: str | None
    unix_fds: list[int]
    signature: str
    signature_tree: SignatureTree
    body: list[Any]
    serial: int


class Codec(Protocol):
    def decode(self, value: Variant) -> Any:
        raise NotImplementedError

    def encode(
        self, value: Any, signature: str | SignatureType | SignatureTree
    ) -> Variant:
        raise NotImplementedError

    def unpack(self, values: Mapping[str, Variant]) -> Mapping[str, Any]:
        raise NotImplementedError

    def message(
        self,
        destination: str | None = None,
        path: str | None = None,
        interface: str | None = None,
        member: str | None = None,
        message_type: int | MessageType = MessageType.METHOD_CALL,
        flags: int | MessageFlag = MessageFlag.NONE,
        error_name: str | None = None,
        reply_serial: int = 0,
        sender: str | None = None,
        unix_fds: list[int] = [],
        signature: str | SignatureTree | None = None,
        body: list[Any] = [],
        serial: int = 0,
        validate: bool = True,
    ) -> Message:
        raise NotImplementedError
