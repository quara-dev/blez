from __future__ import annotations

from typing import Any, Mapping

from dbus_next import Message, Variant
from dbus_next.aio.message_bus import MessageBus

from blez.interfaces.dbus import (
    Bus,
    Codec,
    MessageFlag,
    MessageType,
    SignatureTree,
    SignatureType,
)


class DBusNextCodec(Codec):
    def decode(self, value: Variant) -> Any:
        return value.value

    def encode(
        self, value: Any, signature: str | SignatureType | SignatureTree
    ) -> Variant:
        return Variant(signature, value, verify=True)

    def unpack(self, values: Mapping[str, Variant]) -> Mapping[str, Any]:
        # Initialize empty dict with string keys and unknown value types
        unpacked: dict[str, Any] = {}
        # Iterate over dictionary items
        for key, item in values.items():
            # Use .value attribute if item is a Variant instance
            value = item.value if isinstance(item, Variant) else item
            # Check if value is a dictionary
            if isinstance(value, dict):
                # In this case recursively call the function
                value = self.unpack(value)
            # Check if value is a list
            elif isinstance(value, list):
                # In this case recursively call the function on each item of the list
                # NOTE: We can assume each item of the list is a dictionary due to D-Bus messages format
                value = [x.value if isinstance(x, Variant) else x for x in value]
            # Finally save the unpacked value
            unpacked[key] = value
        # Return unpacked dict
        return unpacked

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
        return Message(
            destination=destination,
            path=path,
            interface=interface,
            member=member,
            message_type=message_type,
            flags=flags,
            error_name=error_name,
            reply_serial=reply_serial,
            sender=sender,
            unix_fds=unix_fds,
            signature=signature,
            body=body,
            serial=serial,
            validate=validate,
        )


class DBusNextBus(Bus):
    def __init__(self) -> None:
        self._bus: MessageBus | None = None

    async def connect(self) -> None:
        if not self._bus:
            self._bus = MessageBus()
            await self._bus.connect()

    async def disconnect(self):
        if self._bus:
            await self._bus.disconnect()
            self._bus = None
