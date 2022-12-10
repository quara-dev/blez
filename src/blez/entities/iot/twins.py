from __future__ import annotations

from typing import TYPE_CHECKING, Generic

from ..pubsub import SubscriptionProtocol
from .backends import DevicePropsT, IoTDeviceBackend, StationPropsT
from .events import DeviceEvent, DeviceEventType, StationEventType
from .queries import StationQuery, StationQueryType
from .requests import (
    DeviceRequest,
    DeviceRequestType,
    StationRequest,
    StationRequestType,
)

if TYPE_CHECKING:
    from .client import IoTHubClient


class RemoteStation(Generic[StationPropsT]):
    def __init__(self, client: IoTHubClient, station: str) -> None:
        self.client = client
        self.station = station

    async def subscribe_to_events(
        self,
        type: StationEventType | None = None,
    ) -> SubscriptionProtocol[StationEventType]:
        """Return an event subscription which can be used to iterate over station events."""
        return await self.client.subscribe_to_station_events(
            station=self.station, type=type
        )

    async def list_discovered_devices(self) -> list[str]:
        return await self.client.station_query(
            StationQuery(StationQueryType.LIST_DISCOVERED_DEVICES)
        )

    async def list_connected_devices(self) -> list[str]:
        return await self.client.station_query(
            StationQuery(StationQueryType.LIST_CONNECTED_DEVICES)
        )

    async def get_discovered_devices(self) -> dict[str, IoTDeviceBackend[DevicePropsT]]:
        """Discovered devices, excluding connected devices."""
        return await self.client.station_query(
            StationQuery(StationQueryType.GET_DISCOVERED_DEVICES)
        )

    async def get_connected_devices(self) -> dict[str, IoTDeviceBackend[DevicePropsT]]:
        """Connected devices, excluding discovered devices."""
        return await self.client.station_query(
            StationQuery(StationQueryType.GET_CONNECTED_DEVICES)
        )

    async def get_device_props(self, device: str) -> DevicePropsT:
        return await self.client.station_query(
            StationQuery(StationQueryType.GET_DEVICE_PROPS, {"device": device})
        )

    async def get_device_keys(self, device: str) -> list[str]:
        return await self.client.station_query(
            StationQuery(StationQueryType.GET_DEVICE_CHARS, {"device": device})
        )

    async def start(self) -> None:
        return await self.client.station_request(
            StationRequest(StationRequestType.START)
        )

    async def stop(self) -> None:
        return await self.client.station_request(
            StationRequest(StationRequestType.STOP)
        )

    async def connect_device(self, device: str) -> None:
        return await self.client.station_request(
            StationRequest(StationRequestType.CONNECT, {"device": device})
        )

    async def disconnect_device(self, device: str) -> None:
        return await self.client.station_request(
            StationRequest(StationRequestType.DISCONNECT, {"device": device})
        )

    async def start_discovery(self) -> None:
        return await self.client.station_request(
            StationRequest(StationRequestType.START_DISCOVERY)
        )

    async def stop_discovery(self) -> None:
        return await self.client.station_request(
            StationRequest(StationRequestType.STOP_DISCOVERY)
        )

    async def enable_discovery(self) -> None:
        return await self.client.station_request(
            StationRequest(StationRequestType.ENABLE_DISCOVERY)
        )

    async def disable_discovery(self) -> None:
        return await self.client.station_request(
            StationRequest(StationRequestType.DISABLE_DISCOVERY)
        )


class RemoteDevice(Generic[DevicePropsT]):
    def __init__(self, client: IoTHubClient, device: str) -> None:
        self.client = client
        self.device = device

    async def connect(self, station: str) -> None:
        """Connect a station to the device"""
        await self.client.station_request(
            station, StationRequest(StationRequestType.CONNECT, {"device": self.device})
        )

    async def disconnect(self) -> None:
        """Force disconnection of device to any station it might be connected to."""
        await self.client.send_device_request(
            self.device, DeviceRequest(DeviceRequestType.DISCONNECT)
        )

    async def set_time(self) -> None:
        """Set time on device to current time.

        Implementation may vary between backends.
        """
        await self.client.send_device_request(
            self.device, DeviceRequest(DeviceRequestType.SET_TIME)
        )

    async def sync_time(self) -> None:
        """Sync time on device to current time.

        Implementation may vary between backends.
        """
        await self.client.send_device_request(
            self.device, DeviceRequest(DeviceRequestType.SYNC_TIME)
        )

    async def read_value(self, key: str) -> bytearray:
        """Read a value as bytearray under given key."""
        await self.client.send_device_request(
            self.device, DeviceRequest(DeviceRequestType.READ_VALUE, {"key": key})
        )

    async def write_value(self, key: str, value: bytearray) -> int:
        """Write a value and return number of bytes written under given key."""
        await self.client.send_device_request(
            self.device,
            DeviceRequest(DeviceRequestType.WRITE_VALUE, {"key": key, "value": value}),
        )

    async def enable_notifications(self, key: str) -> None:
        """Start notifications for given key."""
        await self.client.send_device_request(
            self.device, DeviceRequest(DeviceRequestType.START_NOTIFY, {"key": key})
        )

    async def disable_notifications(self, key: str) -> None:
        """Stop notifications for given key."""
        await self.client.send_device_request(
            self.device, DeviceRequest(DeviceRequestType.STOP_NOTIFY, {"key": key})
        )

    async def reset(self) -> None:
        await self.client.send_device_request(
            self.device, DeviceRequest(DeviceRequestType.RESET)
        )

    async def subscribe_to_events(
        self,
        type: DeviceEventType | None = None,
    ) -> SubscriptionProtocol[DeviceEvent]:
        """Return an event subscription which can be used to iterate over device events."""
        return await self.client.subscribe_to_device_events(
            device=self.device, type=type
        )

    async def subscribe_to_notifications(
        self,
        key: str,
    ) -> SubscriptionProtocol[bytearray]:
        """Return a notification subscription which can be used to iterate over received messages."""
        return await self.client.subscribe_to_device_events(
            device=self.device, type=DeviceEventType.NOTIFIED, key=key
        )
