from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Generic

from ..pubsub import PubSubProtocol, ServiceProtocol
from .backends import DevicePropsT, IoTStationBackend, StationPropsT
from .events import DeviceEvent, StationEvent
from .queries import StationQuery, StationQueryType
from .requests import (
    DeviceRequest,
    DeviceRequestType,
    StationRequest,
    StationRequestType,
)
from .subjects import SERVICE_SUBJECTS


@dataclass
class GatewayState:
    name: str
    request_service: ServiceProtocol[StationRequest, Any]
    query_service: ServiceProtocol[StationQuery, Any]
    device_services: dict[str, ServiceProtocol[DeviceRequest, Any]]


class IoTGateway(Generic[StationPropsT, DevicePropsT]):
    @abc.abstractmethod
    def get_pubsub(self) -> PubSubProtocol:
        """Get pubsub implementation."""
        ...

    @abc.abstractmethod
    def get_backend(self) -> IoTStationBackend[StationPropsT, DevicePropsT]:
        """Get station backend implementation."""
        ...

    @abc.abstractmethod
    def get_state(self) -> GatewayState:
        """Get gateway state."""
        ...

    def create_station_requests_handler(
        self,
    ) -> Callable[[StationRequest], Awaitable[None]]:
        """Create a function to handle station requests."""
        backend = self.get_backend()

        async def handler(request: StationRequest) -> None:
            """Handle a request directed to the station."""
            TYPE = StationRequestType(request.type)
            if TYPE == StationRequestType.CONNECT:
                device = request.options["device"]
                return await backend.connect(device=device)
            if TYPE == StationRequestType.DISCONNECT:
                device = request.options["device"]
                return await backend.disconnect(device=device)
            if TYPE == StationRequestType.START_DISCOVERY:
                return await backend.start_discovery()
            if TYPE == StationRequestType.STOP_DISCOVERY:
                return await backend.stop_discovery()
            if TYPE == StationRequestType.ENABLE_DISCOVERY:
                return await backend.enable_discovery()
            if TYPE == StationRequestType.DISABLE_DISCOVERY:
                return await backend.disable_discovery()
            if TYPE == StationRequestType.START:
                return await backend.start()
            if TYPE == StationRequestType.STOP:
                return await backend.stop()
            raise NotImplementedError(f"Request type not supported yet: {TYPE}")

        return handler

    def create_device_requests_handler(
        self, device: str
    ) -> Callable[[DeviceRequest], Awaitable[None]]:
        """Create a function to handle requests for a single device."""
        backend = self.get_backend()

        async def handler(request: DeviceRequest) -> None:
            """Handle a request directed to a device."""
            device_backend = backend.get_device(device)
            TYPE = request.type
            if TYPE == DeviceRequestType.DISCONNECT:
                return await device_backend.disconnect()
            if TYPE == DeviceRequestType.SET_TIME:
                return await device_backend.set_time()
            if TYPE == DeviceRequestType.SYNC_TIME:
                return await device_backend.sync_time()
            if TYPE == DeviceRequestType.START_NOTIFY:
                characteristic = request.options["characteristic"]
                return await device_backend.enable_notifications(characteristic)
            if TYPE == DeviceRequestType.STOP_NOTIFY:
                characteristic = request.options["characteristic"]
                return await device_backend.disable_notifications(characteristic)
            if TYPE == DeviceRequestType.READ_VALUE:
                target = request.options["characteristic"]
                return await device_backend.read_value(target)
            if TYPE == DeviceRequestType.WRITE_VALUE:
                target = request.options["characteristic"]
                value = request.options["value"]
                return await device_backend.write_value(target, value)
            if TYPE == DeviceRequestType.RESET:
                return await device_backend.reset()

        return handler

    def create_station_query_handler(self) -> Callable[[StationQuery], Awaitable[Any]]:
        """Create a function to a handle station queries."""
        backend = self.get_backend()

        async def handler(query: StationQuery) -> Any:
            TYPE = StationQueryType(query.type)
            if TYPE == StationQueryType.GET_CONNECTED_DEVICES:
                return await backend.get_connected_devices()
            if TYPE == StationQueryType.GET_DISCOVERED_DEVICES:
                return await backend.get_discovered_devices()
            if TYPE == StationQueryType.LIST_CONNECTED_DEVICES:
                return await backend.list_connected_devices()
            if TYPE == StationQueryType.LIST_DISCOVERED_DEVICES:
                return await backend.list_discovered_devices()
            if TYPE == StationQueryType.GET_PROPS:
                return await backend.get_props()
            if TYPE == StationQueryType.GET_DEVICE_PROPS:
                device = backend.get_device(query.options["device"])
                return device.get_props()
            if TYPE == StationQueryType.GET_DEVICE_CHARS:
                device = backend.get_device(query.options["device"])
                return device.get_characteristics()
            raise NotImplementedError(f"Query type is not supported yet: {TYPE}")

        return handler

    def create_device_event_handler(self) -> Callable[[DeviceEvent], Awaitable[Any]]:
        """Create a function to handle device events."""
        pubsub = self.get_pubsub()

        def handler(event: DeviceEvent) -> None:
            subject = SERVICE_SUBJECTS[event.type]
            pubsub.publish_no_wait(subject, event.data, tokens={"device": event.device})

        return handler

    def create_station_event_handler(self) -> Callable[[StationEvent], Awaitable[Any]]:
        """Create a function to handle station events."""
        pubsub = self.get_pubsub()

        def handler(event: StationEvent) -> None:
            subject = SERVICE_SUBJECTS[event.type]
            pubsub.publish_no_wait(
                subject, event.data, tokens={"station": event.station}
            )

        return handler

    async def start_services(self) -> None:
        state = self.get_state()
        if "request_handler" in state or "query_handler" in state:
            raise Exception(f"Station is already registered")
        pubsub = self.get_pubsub()
        backend = self.get_backend()
        # Create station request service
        request_handler = self.create_station_requests_handler()
        request_service = await pubsub.create_service(
            SERVICE_SUBJECTS[StationRequestType.ALL], request_handler
        )
        # Save request service
        state.request_service = request_service
        # Create station query service
        query_handler = self.create_station_query_handler()
        query_service = await pubsub.create_service(
            SERVICE_SUBJECTS[StationQueryType.ALL], query_handler
        )
        # Save query service
        state.query_service = query_service
        # Register connected devices request handlers
        for device in backend.list_connected_devices():
            await self.start_device_service(device)

    async def stop_services(self) -> None:
        state = self.get_state()
        backend = self.get_backend()
        # First stop device services
        for device in backend.list_connected_devices():
            await self.stop_device_service(device)
        # Then unregister request handler
        if state.request_service:
            await state.request_service.drain()
        # Finally unregister query handler
        if state.query_service:
            await state.query_service.drain()

    async def start_device_service(self, device: str) -> None:
        state = self.get_state()
        if device in state.device_services:
            raise Exception(f"A service is already registered for device")
        pubsub = self.get_pubsub()
        handler = self.create_device_requests_handler(device)
        device_service = await pubsub.create_service(
            SERVICE_SUBJECTS[DeviceRequestType.ALL], handler
        )
        state.device_services[device] = device_service

    async def stop_device_service(self, device: str) -> None:
        state = self.get_state()
        device_service = state.device_services.pop(device, None)
        if device_service is None:
            return
        await device_service.drain()

    async def start(self) -> None:
        pubsub = self.get_pubsub()
        backend = self.get_backend()
        await pubsub.connect()
        backend.set_device_event_sink(self.handle_device_event)
        backend.set_workstation_event_sink(self.handle_station_event)
        await self.start_services()

    async def stop(self) -> None:
        pubsub = self.get_pubsub()
        backend = self.get_backend()
        await self.stop_services()
        backend.set_device_event_sink(None)
        backend.set_workstation_event_sink(None)
        await backend.disconnect()
        await pubsub.disconnect()
