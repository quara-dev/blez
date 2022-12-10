from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Generic, Mapping

from blez.entities.iot.subjects import SERVICE_SUBJECTS

from ..pubsub import PubSubProtocol, PushConsumerProtocol, ServiceProtocol
from .backends import DevicePropsT, IoTHubStorageBackend, StationPropsT
from .events import (
    DeviceEvent,
    DeviceEventFamily,
    DeviceEventType,
    StationEvent,
    StationEventFamily,
    StationEventType,
)
from .queries import HubQuery, HubQueryType


@dataclass
class HubState:
    query_service: ServiceProtocol[HubQuery, Any] | None = None
    event_consumer: PushConsumerProtocol[DeviceEvent | StationEvent] = None


class IoTHub(Generic[StationPropsT, DevicePropsT]):
    @abc.abstractmethod
    def get_pubsub(self) -> PubSubProtocol:
        ...

    @abc.abstractmethod
    def get_storage(self) -> IoTHubStorageBackend:
        ...

    @abc.abstractmethod
    def get_state(self) -> HubState:
        ...

    async def list_stations(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[str]:
        storage = self.get_storage()
        return await storage.list_stations(filter=filter, limit=limit, offset=offset)

    async def list_devices(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[str]:
        storage = self.get_storage()
        return await storage.list_devices(filter=filter, limit=limit, offset=offset)

    async def find_devices(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[DevicePropsT]:
        storage = self.get_storage()
        return await storage.find_devices(filter=filter, limit=limit, offset=offset)

    async def find_stations(
        self,
        filter: Mapping[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[StationPropsT]:
        storage = self.get_storage()
        return await storage.find_stations(filter=filter, limit=limit, offset=offset)

    async def get_device(self, device: str) -> DevicePropsT | None:
        storage = self.get_storage()
        devices = await storage.find_devices(filter={"device": device}, limit=1)
        return devices.get(device)

    async def get_station(self, station: str) -> StationPropsT:
        storage = self.get_storage()
        stations = await storage.find_devices(filter={"station": station}, limit=1)
        return stations.get(station)

    def create_event_handler(
        self,
    ) -> Callable[[StationEvent | DeviceEvent], Awaitable[None]]:
        storage = self.get_storage()

        async def process_event(event: StationEvent | DeviceEvent) -> None:
            if isinstance(event, DeviceEvent):
                if event.type == DeviceEventType.PROPS_CHANGED:
                    await storage.update_device_props(
                        device=event.device,
                        changed_props=event.data["changed_props"],
                        invalidated_props=event.data["invalidated_props"],
                    )
                return
            if isinstance(event, StationEvent):
                if event.type == StationEventType.PROPS_CHANGED:
                    await storage.update_station_props(
                        device=event.device,
                        changed_props=event.data["changed_props"],
                        invalidated_props=event.data["invalidated_props"],
                    )
                return

        return process_event

    def create_query_handler(self) -> Callable[[HubQuery], Awaitable[Any]]:
        hub = self

        async def handler(query: HubQuery) -> Any:
            TYPE = HubQueryType(query.type)
            if TYPE == HubQueryType.FIND_DEVICES:
                return await hub.find_devices(**query.options)
            if TYPE == HubQueryType.FIND_STATIONS:
                return await hub.find_stations(**query.options)
            if TYPE == HubQueryType.GET_DEVICE:
                return await hub.get_device(**query.options)
            if TYPE == HubQueryType.GET_STATION:
                return await hub.get_station(**query.options)
            if TYPE == HubQueryType.LIST_DEVICES:
                return await hub.list_devices(**query.options)
            if TYPE == HubQueryType.LIST_STATIONS:
                return await hub.list_stations(**query.options)

        return handler

    async def start(self) -> None:
        state = self.get_state()
        if state.query_service or state.event_consumer:
            raise Exception("Hub is already started")
        # Connect pubsub
        pubsub = self.get_pubsub()
        await pubsub.connect()
        # Start event consumer
        state.event_consumer = await pubsub.create_push_consumer(
            [
                SERVICE_SUBJECTS[StationEventFamily.PROPS],
                SERVICE_SUBJECTS[DeviceEventFamily.PROPS],
            ],
            self.create_event_handler(),
            tokens={"device": "*", "characteristic": "*", "station": "*"},
        )
        # Start query service
        state.query_service = await pubsub.create_service(
            SERVICE_SUBJECTS[HubQueryType.ALL],
            self.create_query_handler(),
            tokens={"device": "*"},
        )

    async def drain(self) -> None:
        pubsub = self.get_pubsub()
        state = self.get_state()
        did_timeout: TimeoutError | None = None
        if state.query_service:
            try:
                await state.query_service.drain()
            except TimeoutError as exc:
                did_timeout = exc
            state.query_service = None
        if state.event_consumer:
            try:
                await state.event_consumer.drain()
            except TimeoutError as exc:
                did_timeout = exc
            state.event_consumer = None
        await pubsub.disconnect()
        # Raise back timeout error
        if did_timeout:
            raise did_timeout

    async def stop(self) -> None:
        pubsub = self.get_pubsub()
        state = self.get_state()
        if state.query_service:
            await state.query_service.stop()
            state.query_service = None
        if state.event_consumer:
            await state.event_consumer.stop()
            state.event_consumer = None
        await pubsub.disconnect()
