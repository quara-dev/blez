from __future__ import annotations

from logging import getLogger
from typing import Any

from blez.interfaces.dbus import Bus, Codec, Message, MessageType

from .errors import BluezDBusError

logger = getLogger(__name__)


class Client:
    def __init__(
        self,
        bus: Bus,
        codec: Codec,
    ) -> None:
        self.bus = bus
        self.codec = codec

    async def connect(self) -> None:
        await self.bus.connect()

    async def disconnect(self) -> None:
        await self.bus.disconnect()

    async def call(
        self,
        service: str,
        path: str,
        interface: str,
        member: str,
        signature: str = "",
        body: list[Any] = [],
    ) -> Message:
        reply = await self.bus.call(
            self.codec.message(
                destination=service,
                path=path,
                interface=interface,
                member=member,
                signature=signature,
                body=body,
            )
        )
        self.raise_for_status(reply)
        return reply

    async def get_property(
        self,
        service: str,
        path: str,
        interface: str,
        key: str,
    ) -> Any:
        """Get a value from a specific object interface property on the bus"""
        reply = await self.call(
            service=service,
            path=path,
            interface="org.freedesktop.DBus.Properties",
            member="Get",
            signature="ss",
            body=[interface, key],
        )
        return self.codec.decode(reply.body[0])

    async def get_all_properties(
        self,
        service: str,
        path: str,
        interface: str,
    ) -> dict[str, Any]:
        """Get a value from a specific object interface property on the bus"""
        reply = await self.call(
            service=service,
            path=path,
            interface="org.freedesktop.DBus.Properties",
            member="GetAll",
            signature="s",
            body=[interface],
        )
        return self.codec.unpack(reply.body[0])

    async def set_property(
        self,
        service: str,
        path: str,
        interface: str,
        key: str,
        value: Any,
        signature: str,
    ) -> None:
        """Set value for a specific object interface property on the bus"""
        encoded = self.codec.encode(value, signature)
        await self.call(
            service=service,
            path=path,
            interface="org.freedesktop.DBus.Properties",
            member="Set",
            signature="ssv",
            body=[interface, key, encoded],
        )

    async def get_managed_objects(
        self, service: str, path: str = "/"
    ) -> dict[str, dict[str, dict[str, Any]]]:
        """Get managed objects for given DBus service."""
        # Send message and await reply
        reply = await self.call(
            service=service,
            path=path,
            member="GetManagedObjects",
            interface="org.freedesktop.DBus.ObjectManager",
        )
        # Unpack interfaces
        return self.codec.unpack(reply.body[0])

    @staticmethod
    def raise_for_status(reply: Message) -> Message:
        """Checks that a D-Bus message is successfull

        Raises:
            BluezError: if the message type is ``MessageType.ERROR``
            AssentationError: if the message type is not ``MessageType.METHOD_RETURN``
        """
        if reply.message_type.value == MessageType.ERROR.value:
            raise BluezDBusError(reply.error_name, reply.body)
        assert reply.message_type.value == MessageType.METHOD_RETURN.value
        return reply
