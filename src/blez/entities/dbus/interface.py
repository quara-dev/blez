from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from blez.entities.bluez.manager import Manager
    from blez.interfaces.dbus import Message


class Interface:
    def __init_subclass__(cls, name: str) -> None:
        """Create a new interface class."""
        cls.DBUS_INTERFACE = name

    def __init__(self, object_path: str, service: Manager) -> None:
        """Create a new interface."""
        self.path = object_path
        self.service = service

    @property
    def cached_properties(self) -> dict[str, Any]:
        """Access interface cached properties."""
        return self.service.tree.get_interface(self.path, self.DBUS_INTERFACE)

    async def call(
        self, member: str, signature: str = "", body: list[Any] | None = None
    ) -> Message:
        """Call interface member using provided signature and body."""
        return await self.service.call(
            path=self.path,
            member=member,
            interface=self.DBUS_INTERFACE,
            signature=signature,
            body=body or [],
        )

    async def get_property(
        self,
        key: str,
    ) -> Any:
        """Get a value from a specific object interface property on the bus"""
        return await self.service.get_property(
            path=self.path,
            interface=self.DBUS_INTERFACE,
            key=key,
        )

    async def get_all_properties(
        self,
    ) -> Any:
        """Get a value from a specific object interface property on the bus"""
        return await self.service.get_all_properties(
            path=self.path,
            interface=self.DBUS_INTERFACE,
        )

    async def set_property(
        self,
        key: str,
        value: Any,
        signature: str,
    ) -> None:
        """Set value for a specific object interface property on the bus"""
        await self.service.set_property(
            path=self.path,
            interface=self.DBUS_INTERFACE,
            key=key,
            value=value,
            signature=signature,
        )
