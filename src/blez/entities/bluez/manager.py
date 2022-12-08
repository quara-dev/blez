from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Callable

from blez.interfaces.dbus import MessageType

from ..dbus.errors import BluezDBusError
from ..dbus.match import MatchRules, MatchRulesDef
from ..dbus.tree import Tree
from .messages import MessageHandler

if TYPE_CHECKING:
    from blez.interfaces.dbus import Bus, Message


DEFAULT_CLOCK = time.time


class Manager:
    def __init__(
        self,
        bus: Bus,
        name: str,
        tree: Tree | None = None,
        clock: Callable[[], float] = DEFAULT_CLOCK,
    ) -> None:
        self.bus = bus
        self.codec = self.bus.codec
        self.clock = clock
        self.name = name
        self.tree = tree or Tree()
        self.handler = MessageHandler(self.tree, self.codec, self.clock)

    async def reset_tree(self) -> None:
        self.tree.objects.clear()
        self.tree.objects.update(await self.get_managed_objects())

    async def call(
        self,
        path: str,
        interface: str,
        member: str,
        signature: str = "",
        body: list[Any] = [],
    ) -> Message:
        reply = await self.bus.call(
            self.codec.message(
                destination=self.name,
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
        path: str,
        interface: str,
        key: str,
    ) -> Any:
        """Get a value from a specific object interface property on the bus"""
        reply = await self.call(
            path=path,
            interface="org.freedesktop.DBus.Properties",
            member="Get",
            signature="ss",
            body=[interface, key],
        )
        return self.codec.decode(reply.body[0])

    async def get_all_properties(
        self,
        path: str,
        interface: str,
    ) -> dict[str, Any]:
        """Get a value from a specific object interface property on the bus"""
        reply = await self.call(
            path=path,
            interface="org.freedesktop.DBus.Properties",
            member="GetAll",
            signature="s",
            body=[interface],
        )
        return self.codec.unpack(reply.body[0])

    async def set_property(
        self,
        path: str,
        interface: str,
        key: str,
        value: Any,
        signature: str,
    ) -> None:
        """Set value for a specific object interface property on the bus"""
        encoded = self.codec.encode(value, signature)
        await self.call(
            path=path,
            interface="org.freedesktop.DBus.Properties",
            member="Set",
            signature="ssv",
            body=[interface, key, encoded],
        )

    async def get_managed_objects(
        self, path: str = "/"
    ) -> dict[str, dict[str, dict[str, Any]]]:
        """Get managed objects for given DBus service."""
        # Send message and await reply
        reply = await self.call(
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

    async def add_match(self, rules: MatchRules | MatchRulesDef) -> Message:
        """Calls org.freedesktop.DBus.AddMatch using ``rules``."""
        if isinstance(rules, MatchRulesDef):
            rules = MatchRules.from_def(rules)
        return await self.bus.call(
            self.codec.message(
                destination="org.freedesktop.DBus",
                interface="org.freedesktop.DBus",
                path="/org/freedesktop/DBus",
                member="AddMatch",
                signature="s",
                body=[str(rules)],
            )
        )

    async def remove_match(self, rules: MatchRules | MatchRulesDef) -> Message:
        """Calls org.freedesktop.DBus.RemoveMatch using ``rules``."""
        if isinstance(rules, MatchRulesDef):
            rules = MatchRules.from_def(rules)
        return await self.bus.call(
            self.codec.message(
                destination="org.freedesktop.DBus",
                interface="org.freedesktop.DBus",
                path="/org/freedesktop/DBus",
                member="RemoveMatch",
                signature="s",
                body=[str(rules)],
            )
        )

    def get_default_match_rules(
        self, path: str
    ) -> tuple[MatchRulesDef, MatchRulesDef, MatchRulesDef]:
        interface_added = MatchRulesDef(
            interface="org.freedesktop.DBus.ObjectManager",
            member="InterfacesAdded",
            path_namespace=path,
        )
        interface_removed = MatchRulesDef(
            interface="org.freedesktop.DBus.ObjectManager",
            member="InterfacesRemoved",
            path_namespace=path,
        )
        properties_changed = MatchRulesDef(
            interface="org.freedesktop.DBus.Properties",
            member="PropertiesChanged",
            path_namespace=path,
        )
        return interface_added, interface_removed, properties_changed

    async def watch_from_path(self, path: str) -> None:
        for rules in self.get_default_match_rules(path):
            await self.add_match(rules)

    async def unwatch_from_path(self, path: str) -> None:
        for rules in self.get_default_match_rules(path):
            await self.remove_match(rules)
