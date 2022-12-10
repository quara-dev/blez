from __future__ import annotations

import abc
from typing import Any, Callable, Generic, Mapping, TypeVar

from .events import DeviceEvent, DeviceEventType, StationEvent, StationEventType

DevicePropsT = TypeVar("DevicePropsT")
StationPropsT = TypeVar("StationPropsT")


class IoTDeviceBackend(Generic[DevicePropsT], metaclass=abc.ABCMeta):
    """Device backend interface."""

    @abc.abstractmethod
    def get_props(self) -> DevicePropsT:
        """Get device properties. Backend implementations are expected to update
        properties asynchonously, but expose them synchronously."""
        ...

    @abc.abstractmethod
    def get_characteristics(self) -> list[str]:
        """Get device characteristics. Backend implementations are expected to update
        characteristics asynchonously, but expose them synchronously."""
        ...

    @abc.abstractmethod
    async def disconnect(self) -> None:
        """Force disconnection of device to any station it might be connected to."""
        ...

    @abc.abstractmethod
    async def set_time(self) -> None:
        """Set time on device to current time.

        Implementation may vary between backends.
        """
        ...

    @abc.abstractmethod
    async def sync_time(self) -> None:
        """Sync time on device to current time.

        Implementation may vary between backends.
        """
        ...

    @abc.abstractmethod
    async def read_value(self, characteristic: str) -> bytearray:
        """Read a characteristic value as bytearray."""
        ...

    @abc.abstractmethod
    async def write_value(self, characteristic: str, value: bytearray) -> int:
        """Write a value and return number of bytes written under given characteristic."""
        ...

    @abc.abstractmethod
    async def enable_notifications(self, key: str) -> None:
        """Start notifications for given characteristic."""
        ...

    @abc.abstractmethod
    async def disable_notifications(self, key: str) -> None:
        """Stop notifications for given characteristic."""
        ...

    @abc.abstractmethod
    async def reset(self) -> None:
        ...


class IoTStationBackend(Generic[StationPropsT, DevicePropsT], metaclass=abc.ABCMeta):
    """Station backend interface."""

    @abc.abstractmethod
    def get_props(self) -> StationPropsT:
        """Get station properties. Backend implementations are expected to update
        properties asynchonously, but expose them synchronously."""
        ...

    @abc.abstractmethod
    def get_device(self, device: str) -> IoTDeviceBackend[DevicePropsT]:
        """Get a single device properties. Backend implementations are expected to update
        properties asynchonously, but expose them synchronously."""
        ...

    @abc.abstractmethod
    def list_discovered_devices(self) -> list[str]:
        """List devices discovered by station. Backend implementations are expected to update
        discovered devices asynchonously, but expose them synchronously."""
        ...

    @abc.abstractmethod
    def list_connected_devices(self) -> list[str]:
        """List devices connected to the station. Backend implementations are expected to update
        connected devices asynchonously, but expose them synchronously."""
        ...

    @abc.abstractmethod
    def get_discovered_devices(self) -> dict[str, IoTDeviceBackend[DevicePropsT]]:
        """Get devices discovered by the station. Backend implementations are expected to update
        discovered devices properties asynchonously, but expose them synchronously."""
        ...

    @abc.abstractmethod
    def get_connected_devices(self) -> dict[str, IoTDeviceBackend[DevicePropsT]]:
        """Get devices connected to the station. Backend implementations are expected to update
        connected devices properties asynchonously, but expose them synchronously."""
        ...

    @abc.abstractmethod
    async def start(self) -> None:
        """Start the station, I.E, enable communications between devices and the station."""
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stop the station, I.E, disable communications between devices and the station."""
        ...

    @abc.abstractmethod
    async def connect(self, device: str) -> None:
        """Connect the station, I.E, enable communications between station and gateway."""
        ...

    @abc.abstractmethod
    async def disconnect(self, device: str) -> None:
        """Disconnect the station, I.E, disable communications between station and gateway."""
        ...

    @abc.abstractmethod
    async def start_discovery(self) -> None:
        """Start discovering devices."""
        ...

    @abc.abstractmethod
    async def stop_discovery(self) -> None:
        """Stop discovering devices."""
        ...

    @abc.abstractmethod
    async def enable_discovery(self) -> None:
        """Enable passive devices discovery.

        Passing discovery is not impacted by imperative scanning
        performed through start_discovery and stop_discovery methods.
        """
        ...

    @abc.abstractmethod
    async def disable_discovery(self) -> None:
        """Disable passive devices discovery."""
        ...

    @abc.abstractmethod
    def set_workstation_event_sink(
        self,
        type: StationEventType | None,
        sink: Callable[[StationEvent], None] | None,
    ) -> None:
        """Define function to execute on each event emitted by the station."""
        ...

    @abc.abstractmethod
    def set_device_event_sink(
        self,
        type: DeviceEventType | None,
        sink: Callable[[DeviceEvent], None] | None,
    ) -> None:
        """Define function to execute on each device event received by the station."""
        ...


class IoTHubStorageBackend(Generic[StationPropsT, DevicePropsT], metaclass=abc.ABCMeta):
    """IoT Hub storage interface."""

    @abc.abstractmethod
    async def list_stations(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def list_devices(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def find_devices(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[DevicePropsT]:
        ...

    @abc.abstractmethod
    async def find_stations(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[StationPropsT]:
        ...

    @abc.abstractmethod
    async def update_device_props(
        self,
        device: str,
        changed_props: Mapping[str, Any] | None = None,
        invalidated_props: list[str] | None = None,
    ) -> None:
        ...

    @abc.abstractmethod
    async def update_station_props(
        self,
        station: str,
        changed_props: Mapping[str, Any] | None = None,
        invalidated_props: list[str] | None = None,
    ) -> None:
        ...
