from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable

from blez.interfaces.dbus import Codec, Message

DEFAULT_CLOCK = time.time


@dataclass
class BluezMessage:
    timestamp: int
    path: str

    @classmethod
    def parse(
        cls,
        message: Message,
        codec: Codec,
        timestamp: int | None = None,
        clock: Callable[[], float] = DEFAULT_CLOCK,
    ) -> PropertiesChanged | InterfacesAdded | InterfacesRemoved | None:
        # Get timestamp
        received_timestamp = timestamp or clock()
        # Get message member
        MEMBER = message.member
        # Process message according to Member field
        if MEMBER == "InterfacesAdded":
            object_path, packed_added_interfaces = message.body
            added_interfaces = codec.unpack(packed_added_interfaces)
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
            changed_properties = codec.unpack(packed_changed_properties)
            return PropertiesChanged(
                received_timestamp,
                message.path,
                changed_interface,
                changed_properties,
                invalidated_properties,
            )


@dataclass
class PropertiesChanged(BluezMessage):
    interface: str
    changed_props: dict[str, Any]
    invalidated_props: list[str]

    @classmethod
    def parse(
        cls,
        message: Message,
        codec: Codec,
        timestamp: int | None = None,
        clock: Callable[[], float] = DEFAULT_CLOCK,
    ) -> PropertiesChanged:
        msg = super().parse(message, codec, timestamp, clock)
        if not isinstance(msg, cls):
            raise TypeError(f"Invalid type: {type(msg).__name__}")
        return msg


@dataclass
class InterfacesRemoved(BluezMessage):
    removed_interfaces: list[str]

    @classmethod
    def parse(
        cls,
        message: Message,
        codec: Codec,
        timestamp: int | None = None,
        clock: Callable[[], float] = DEFAULT_CLOCK,
    ) -> InterfacesAdded:
        msg = super().parse(message, codec, timestamp, clock)
        if not isinstance(msg, cls):
            raise TypeError(f"Invalid type: {type(msg).__name__}")
        return msg


@dataclass
class InterfacesAdded(BluezMessage):
    added_interfaces: dict[str, dict[str, Any]]

    @classmethod
    def parse(
        cls,
        message: Message,
        codec: Codec,
        timestamp: int | None = None,
        clock: Callable[[], float] = DEFAULT_CLOCK,
    ) -> InterfacesRemoved:
        msg = super().parse(message, codec, timestamp, clock)
        if not isinstance(msg, cls):
            raise TypeError(f"Invalid type: {type(msg).__name__}")
        return msg
