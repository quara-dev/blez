from __future__ import annotations

from enum import Enum
from typing import Any, Mapping


class StationQueryType(str, Enum):
    """Enumeration of query types available for stations."""

    ALL = "ALL"
    GET_PROPS = "GET_PROPS"
    GET_KNOWN_DEVICES = "GET_KNOWN_DEVICES"
    GET_CONNECTED_DEVICES = "GET_CONNECTED_DEVICES"
    GET_DISCOVERED_DEVICES = "GET_DISCOVERED_DEVICES"
    LIST_CONNECTED_DEVICES = "LIST_CONNECTED_DEVICES"
    LIST_DISCOVERED_DEVICES = "LIST_DISCOVERED_DEVICES"
    GET_DEVICE_PROPS = "GET_DEVICE_PROPS"
    GET_DEVICE_CHARS = "GET_DEVICE_CHARS"


class HubQueryType(str, Enum):
    """Enumeration of allowed queries for hub"""

    ALL = "ALL"
    LIST_DEVICES = "LIST_DEVICES"
    LIST_STATIONS = "LIST_STATIONS"
    FIND_DEVICES = "FIND_DEVICES"
    FIND_STATIONS = "FIND_STATIONS"
    GET_DEVICE = "GET_DEVICE"
    GET_STATION = "GET_STATION"


class StationQuery:
    """A query to send to a station."""

    def __init__(
        self,
        type: StationQueryType,
        options: Mapping[str, Any] | None = None,
        deadline: float | None = None,
    ) -> None:
        self.type = type
        self.options = options
        self.deadline = deadline


class HubQuery:
    def __init__(
        self,
        type: HubQueryType,
        options: Mapping[str, Any] | None = None,
        deadline: float | None = None,
    ) -> None:
        self.type = type
        self.options = options
        self.deadline = deadline
