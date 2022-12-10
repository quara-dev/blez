from __future__ import annotations

from enum import Enum
from typing import Any, Mapping


class StationEventFamily(str, Enum):
    ALL = "ALL"
    LIFECYCLE = "LIFECYCLE"
    DEVICE = "DEVICE"
    DISCOVERY = "DISCOVERY"
    PROPS = "PROPS"


class StationEventType(str, Enum):
    """All events which can be emitted by an IoT station."""

    STARTED = "STARTED"
    STOPPED = "STOPPED"
    DISCOVERY_ENABLED = "DISCOVERY_ENABLED"
    DISCOVERY_DISABLED = "DISCOVERY_DISABLED"
    DISCOVERY_STARTED = "DISCOVERY_STARTED"
    DISCOVERY_STOPPED = "DISCOVERY_STOPPED"
    DEVICE_DISCOVERED = "DEVICE_DISCOVERED"
    DEVICE_CONNECTED = "DEVICE_CONNECTED"
    DEVICE_DISCONNECTED = "DEVICE_DISCONNECTED"
    PROPS_CHANGED = "PROPS_CHANGED"


class DeviceEventFamily(str, Enum):
    ALL = "ALL"
    CONNECTION = "CONNECTION"
    NOTIFICATION = "NOTIFICATION"
    TIME_SYNCHRONISATION = "TIME_SYNCHRONISATION"
    PROPS = "PROPS"


class DeviceEventType(str, Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    TIME_SET = "TIME_SET"
    TIME_SYNCED = "SYNCED"
    NOTIFIED = "NOTIFIED"
    NOTIFY_STARTED = "NOTIFY_STARTED"
    NOTIFY_STOPPED = "NOTIFY_STOPPED"
    PROPS_CHANGED = "PROPS_CHANGED"


class StationEvent:
    """An event emitted by an IoT station"""

    def __init__(
        self,
        type: StationEventType | str,
        station: str,
        data: Mapping[str, Any],
    ) -> None:
        self.type = StationEventType(type)
        self.station = station
        self.data = data


class DeviceEvent:
    """An event emitted by an IoT device."""

    def __init__(
        self, type: DeviceEventType, device: str, data: Mapping[str, Any]
    ) -> None:
        self.type = DeviceEventType(type)
        self.device = device
        self.data = data
