from __future__ import annotations

import abc
from typing import Any, Mapping

from typing_extensions import TypeAlias

from ..pubsub import PubSubProtocol, ReplyProtocol, SubscriptionProtocol
from .events import (
    DeviceEventFamily,
    DeviceEventType,
    StationEventFamily,
    StationEventType,
)
from .queries import HubQueryType, StationQuery, StationQueryType
from .requests import DeviceRequestType, StationRequest
from .subjects import CLIENT_SUBJECTS
from .twins import RemoteDevice, RemoteStation

DecodedType: TypeAlias = Mapping[str, Any]


@abc.abstractmethod
class IoTHubClient:
    """Should depend only on pub/sub + subjects used in Gateway + Hub"""

    @abc.abstractmethod
    def get_pubsub(self) -> PubSubProtocol[DecodedType]:
        """IoTHubClient uses JSON or BSON protocol."""
        ...

    async def send_hub_query(
        self,
        query_type: HubQueryType | str,
        options: Mapping[str, Any] | None = None,
        tokens: Mapping[str, Any] | None = None,
        timeout: float | None = None,
        deadline: float | None = None,
    ) -> ReplyProtocol[DecodedType]:
        pubsub = self.get_pubsub()
        subject = CLIENT_SUBJECTS[HubQueryType(query_type)]
        return await pubsub.request(
            subject, data=options, tokens=tokens, timeout=timeout, deadline=deadline
        )

    async def send_device_request(
        self,
        request_type: DeviceRequestType | str,
        device: str,
        options: Mapping[str, Any] | None = None,
        timeout: float | None = None,
        deadline: float | None = None,
    ) -> ReplyProtocol[DecodedType]:
        """Send a request to a device"""
        pubsub = self.get_pubsub()
        subject = CLIENT_SUBJECTS[HubQueryType(request_type)]
        tokens = {"device": device}
        return await pubsub.request(
            subject, data=options, tokens=tokens, timeout=timeout, deadline=deadline
        )

    async def send_station_query(
        self,
        query_type: StationQueryType | str,
        station: str,
        options: Mapping[str, Any] | None = None,
        timeout: float | None = None,
        deadline: float | None = None,
    ) -> ReplyProtocol[DecodedType]:
        """Send a query to a station"""
        pubsub = self.get_pubsub()
        subject = CLIENT_SUBJECTS[StationQuery(query_type)]
        tokens = {"station": station}
        return await pubsub.request(
            subject, data=options, tokens=tokens, timeout=timeout, deadline=deadline
        )

    async def station_request(
        self,
        request_type: StationQueryType | str,
        station: str,
        options: Mapping[str, Any] | None = None,
        timeout: float | None = None,
        deadline: float | None = None,
    ) -> ReplyProtocol[DecodedType]:
        """Send a request to a station"""
        pubsub = self.get_pubsub()
        subject = CLIENT_SUBJECTS[StationRequest(request_type)]
        tokens = {"station": station}
        return await pubsub.request(
            subject, data=options, tokens=tokens, timeout=timeout, deadline=deadline
        )

    def get_device(self, device: str) -> RemoteDevice[DecodedType]:
        return RemoteDevice(self, device)

    def get_station(self, station: str) -> RemoteStation[DecodedType]:
        return RemoteStation(self, station)

    async def list_devices(
        self, timeout: float | None = None, deadline: float | None = None
    ) -> list[str]:
        """List existing devices"""
        reply = await self.send_hub_query(
            HubQueryType.LIST_DEVICES, timeout=timeout, deadline=deadline
        )
        reply.raise_for_status(200)
        return reply.data.get("devices", [])

    async def list_stations(
        self, timeout: float | None = None, deadline: float | None = None
    ) -> list[str]:
        """List existing stations"""
        reply = await self.send_hub_query(
            HubQueryType.LIST_STATIONS, timeout=timeout, deadline=deadline
        )
        reply.raise_for_status(200)
        return reply.data.get("stations", [])

    async def find_devices(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        timeout: float | None = None,
        deadline: float | None = None,
    ) -> dict[str, Any]:
        options = {
            "filter": filter,
            "limit": limit,
            "offset": offset,
        }
        reply = await self.send_hub_query(
            HubQueryType.FIND_DEVICES,
            options=options,
            timeout=timeout,
            deadline=deadline,
        )
        reply.raise_for_status(200)
        return reply.data.get("devices", {})

    async def find_stations(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        timeout: float | None = None,
        deadline: float | None = None,
    ) -> dict[str, Any]:
        options = {
            "filter": filter,
            "limit": limit,
            "offset": offset,
        }
        reply = await self.send_hub_query(
            HubQueryType.FIND_STATIONS,
            options=options,
            timeout=timeout,
            deadline=deadline,
        )
        reply.raise_for_status(200)
        return reply.data.get("stations", {})

    async def subscribe_to_device_events(
        self,
        device: str | None = None,
        event_type: DeviceEventType | DeviceEventFamily | None = None,
        characteristic: str | None = None,
        queue: str | None = None,
    ) -> SubscriptionProtocol[DecodedType]:
        pubsub = self.get_pubsub()
        tokens = {"device": device or "*", "characteristic": characteristic or "*"}
        event_type = event_type or DeviceEventFamily.ALL
        return await pubsub.create_subscription(
            CLIENT_SUBJECTS[event_type], queue=queue, tokens=tokens
        )

    async def subscribe_to_station_events(
        self,
        station: str | None = None,
        event_type: StationEventType | StationEventFamily | None = None,
        queue: str | None = None,
    ) -> SubscriptionProtocol[DecodedType]:
        pubsub = self.get_pubsub()
        tokens = {
            "station": station or "*",
        }
        event_type = event_type or StationEventFamily.ALL
        return await pubsub.create_subscription(
            CLIENT_SUBJECTS[event_type], queue=queue, tokens=tokens
        )
