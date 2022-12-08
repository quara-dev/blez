from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable

from blez.interfaces.dbus import Codec, Message, MessageType

from ..dbus.tree import Tree

DEFAULT_CLOCK = time.time


@dataclass
class BluezMessage:
    timestamp: int
    path: str


@dataclass
class PropertiesChanged(BluezMessage):
    interface: str
    changed_props: dict[str, Any]
    invalidated_props: list[str]


@dataclass
class InterfacesRemoved(BluezMessage):
    removed_interfaces: list[str]


@dataclass
class InterfacesAdded(BluezMessage):
    added_interfaces: dict[str, dict[str, Any]]


class MessageHandler:
    def __init__(
        self, tree: Tree, codec: Codec, clock: Callable[[], float] = DEFAULT_CLOCK
    ) -> None:
        self.tree = tree
        self.codec = codec
        self.clock = clock

    def parse_message(
        self,
        message: Message,
        timestamp: int | None = None,
    ) -> PropertiesChanged | InterfacesAdded | InterfacesRemoved | None:
        if message.message_type.value != MessageType.SIGNAL.value:
            return
        # Get timestamp
        received_timestamp = timestamp or self.clock()
        # Get message member
        MEMBER = message.member
        # Process message according to Member field
        if MEMBER == "InterfacesAdded":
            object_path, packed_added_interfaces = message.body
            added_interfaces = self.codec.unpack(packed_added_interfaces)
            return InterfacesAdded(received_timestamp, object_path, added_interfaces)
        if MEMBER == "InterfacesRemoved":
            object_path, removed_interfaces = message.body
            return InterfacesRemoved(
                received_timestamp, object_path, removed_interfaces
            )
        if MEMBER == "PropertiesChanged":
            (
                changed_interface,
                packed_changed_properties,
                invalidated_properties,
            ) = message.body
            changed_properties = self.codec.unpack(packed_changed_properties)
            return PropertiesChanged(
                received_timestamp,
                message.path,
                changed_interface,
                changed_properties,
                invalidated_properties,
            )

    def process_message(
        self, message: Message
    ) -> PropertiesChanged | InterfacesAdded | InterfacesRemoved | None:
        event = self.parse_message(message)
        if event is None:
            return None
        if isinstance(event, PropertiesChanged):
            self.tree.update_interface(
                path=event.path,
                interface=event.interface,
                changed_props=event.changed_props,
                invalidated_props=event.invalidated_props,
            )
            return event
        if isinstance(event, InterfacesAdded):
            for interface, props in event.added_interfaces.items():
                self.tree.set_interface(
                    object_path=event.path,
                    interface=interface,
                    properties=props,
                )
            return event
        if isinstance(event, InterfacesRemoved):
            for interface in event.removed_interfaces:
                self.tree.remove_interface(event.path, interface)
            return event
        return None
