from __future__ import annotations

import re

from .entities.bluez.adapter import BluezAdapter
from .entities.bluez.device import BluezDevice
from .entities.bluez.manager import Manager
from .interfaces.dbus import Bus

ADDRESS_PATTERN = re.compile("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")


def default_bus_backend() -> type[Bus]:
    from .ports.dbus_fast import DBusFastBus

    return DBusFastBus


def is_address(value: str) -> bool:
    return ADDRESS_PATTERN.match(value) is not None


class BlezClient:
    def __init__(
        self,
        bus_address: str | None = None,
        bus_backend: type[Bus] | None = None,
    ) -> None:
        self.bus_address = bus_address
        self.bus_backend = bus_backend or default_bus_backend()
        self.bluez = Manager(self.bus_backend(self.bus_address), name="org.bluez")

    async def connect(self) -> None:
        await self.bluez.bus.connect()
        await self.bluez.reset_tree()
        self.bluez.bus.add_message_handler(self.bluez.handler.process_message)
        await self.bluez.watch_from_path("/org/bluez")

    async def disconnect(self) -> None:
        await self.bluez.unwatch_from_path("/org/bluez")
        self.bluez.bus.remove_message_handler(self.bluez.handler.process_message)
        await self.bluez.bus.disconnect()

    def get_adapter(self, name: str | None) -> BluezAdapter | None:
        """Get a single adapter"""
        if name is None:
            for adapter_path in self.bluez.tree.get_all_interfaces(
                "org.bluez.Adapter1"
            ):
                return BluezAdapter(adapter_path)
            return None
        return BluezAdapter(f"/org/bluez/{name}", service=self.bluez)

    def get_device(
        self, name_or_address: str, adapter: str | None = None
    ) -> BluezDevice | None:
        """Get a single device"""
        prefix: str | None = None
        if adapter:
            bluez_adapter = self.get_adapter(adapter)
            prefix = bluez_adapter.path
        if is_address(name_or_address):
            for path in self.bluez.tree.get_all_interfaces(
                "org.bluez.Device1", prefix=prefix
            ):
                device = BluezDevice(path, service=self.bluez)
                if device.address == name_or_address:
                    return device
        else:
            for path in self.bluez.tree.get_all_interfaces(
                "org.bluez.Device1", prefix=prefix
            ):
                device = BluezDevice(path, service=self.bluez)
                if device.name == name_or_address:
                    return device
                elif device.alias == name_or_address:
                    return device
        return None
