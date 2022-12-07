from __future__ import annotations

from typing import Any, Mapping

from dbus_fast import BusType as FastDBusBusType
from dbus_fast import Message
from dbus_fast import MessageFlag as FastDBusMessageFlag
from dbus_fast import MessageType as FastDBusMessageType
from dbus_fast import Variant, unpack_variants
from dbus_fast.aio.message_bus import MessageBus

from blez.interfaces.dbus import (
    Bus,
    BusType,
    Codec,
    MessageFlag,
    MessageType,
    SignatureTree,
    SignatureType,
)


class DBusFastCodec(Codec):
    def decode(self, value: Variant) -> Any:
        return value.value

    def encode(
        self, value: Any, signature: str | SignatureType | SignatureTree
    ) -> Variant:
        return Variant(signature, value, verify=True)

    def unpack(self, values: Mapping[str, Variant]) -> Mapping[str, Any]:
        return unpack_variants(values)

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
            message_type=FastDBusMessageType(MessageType(message_type).value),
            flags=FastDBusMessageFlag(MessageFlag(flags).value),
            error_name=error_name,
            reply_serial=reply_serial,
            sender=sender,
            unix_fds=unix_fds,
            signature=signature,
            body=body,
            serial=serial,
            validate=validate,
        )


class DBusFastBus(Bus):
    def __init__(
        self,
        bus_address: str | None = None,
        bus_type: BusType = BusType.SYSTEM,
        negociate_unix_fd: bool = True,
    ) -> None:
        self.bus_address = bus_address
        self.bus_type = bus_type
        self.negociate_unix_fd = negociate_unix_fd
        self._bus: MessageBus | None = None

    async def connect(self) -> None:
        if not self._bus:
            self._bus = MessageBus(
                bus_address=self.bus_address,
                bus_type=FastDBusBusType(BusType(self.bus_type).value),
                negotiate_unix_fd=self.negociate_unix_fd,
            )
            await self._bus.connect()

    async def disconnect(self):
        if self._bus:
            await self._bus.disconnect()
            self._bus = None

    async def call(self, msg: Message) -> Message:
        return await self._bus.call(msg)
