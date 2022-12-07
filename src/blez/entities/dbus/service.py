from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .tree import Tree

if TYPE_CHECKING:
    from blez.interfaces.dbus import Message

    from .client import Client


class Service:
    def __init__(self, client: Client, name: str, tree: Tree | None = None) -> None:
        self.client = client
        self.name = name
        self.tree = tree or Tree()

    async def reset_tree(self) -> None:
        self.tree.objects.clear()
        self.tree.objects.update(await self.client.get_managed_objects(self.name))

    async def call(
        self,
        path: str,
        interface: str,
        member: str,
        signature: str = "",
        body: list[Any] = [],
    ) -> Message:
        return await self.client.call(
            service=self.name,
            path=path,
            interface=interface,
            member=member,
            signature=signature,
            body=body,
        )

    async def get_property(
        self,
        path: str,
        interface: str,
        key: str,
    ) -> Any:
        """Get a value from a specific object interface property on the bus"""
        return await self.client.get_property(
            service=self.name, path=path, interface=interface, key=key
        )

    async def get_all_properties(
        self,
        path: str,
        interface: str,
    ) -> dict[str, Any]:
        """Get a value from a specific object interface property on the bus"""
        return await self.client.get_all_properties(
            service=self.name,
            path=path,
            interface=interface,
        )

    async def set_property(
        self,
        path: str,
        interface: str,
        key: str,
        value: Any,
        signature: str,
    ) -> None:
        """Set value for a specific object interface property on the bus"""
        return await self.client.set_property(
            service=self.name,
            path=path,
            interface=interface,
            key=key,
            value=value,
            signature=signature,
        )
