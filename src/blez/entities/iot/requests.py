from __future__ import annotations

from enum import Enum
from typing import Any, Mapping


class DeviceRequestType(str, Enum):
    """Enumeration of requests types available for IoT devices."""

    ALL = "ALL"
    RESET = "RESET"
    DISCONNECT = "DISCONNECT"
    START_NOTIFY = "START_NOTIFY"
    STOP_NOTIFY = "STOP_NOTIFY"
    SET_TIME = "SET_TIME"
    SYNC_TIME = "SYNC_TIME"
    READ_VALUE = "READ_VALUE"
    WRITE_VALUE = "WRITE_VALUE"


class StationRequestType(str, Enum):
    """Enumeration of requests types available for stations."""

    ALL = "ALL"
    START = "START"
    STOP = "STOP"
    CONNECT = "CONNECT"
    DISCONNECT = "DISCONNECT"
    START_DISCOVERY = "START_DISCOVERY"
    STOP_DISCOVERY = "STOP_DISCOVERY"
    ENABLE_DISCOVERY = "ENABLE_DISCOVERY"
    DISABLE_DISCOVERY = "DISABLE_DISCOVERY"


class DeviceRequest:
    """A request to send to an IoT device."""

    def __init__(
        self,
        type: DeviceRequestType | str,
        options: Mapping[str, Any] | None = None,
        deadline: float | None = None,
    ) -> None:
        self.type = DeviceRequestType(type)
        self.options = options
        self.deadline = deadline


class StationRequest:
    """A request to send to an IoT station."""

    def __init__(
        self,
        type: StationRequestType | str,
        options: Mapping[str, Any] | None = None,
        deadline: float | None = None,
    ) -> None:
        self.type = StationRequestType(type)
        self.options = options
        self.deadline = deadline
