from __future__ import annotations

from enum import Enum

from ..dbus.interface import Interface
from .gatt_characteristic import BluezGattCharacteristic

GATT_SERVICE_INTERFACE = "org.bluez.GattService1"


class GattService1Property(str, Enum):
    UUID = "UUID"
    PRIMARY = "Primary"
    DEVICE = "Device"
    INCLUDES = "Includes"
    HANDLE = "Handle"


class BluezGattService(Interface, name=GATT_SERVICE_INTERFACE):
    def get_characteristics(self) -> dict[str, BluezGattCharacteristic]:
        """Get all characteristics discovered under service."""
        return {
            key: BluezGattCharacteristic(key, service=self.service)
            for key in self.service.tree.get_all_interfaces(
                BluezGattCharacteristic.DBUS_INTERFACE, prefix=self.path
            )
        }

    @property
    def uuid(self) -> str:
        """128-bit service UUID as a string."""
        return self.cached_properties[GattService1Property.UUID]

    @property
    def primary(self) -> bool:
        """Indicates whether or not this GATT service is a
        primary service. If false, the service is secondary.
        """
        return self.cached_properties[GattService1Property.PRIMARY]

    @property
    def includes(self) -> list[str]:
        """Array of object paths representing the included
        services of this service."""
        return self.cached_properties.get(GattService1Property.INCLUDES, [])

    @property
    def handle(self) -> int | None:
        return self.cached_properties.get(GattService1Property.HANDLE, None)

    async def get_uuid(self) -> str:
        """128-bit service UUID."""
        return await self.get_property(GattService1Property.UUID)

    async def get_primary(self) -> str:
        """Indicates whether or not this GATT service is a
        primary service. If false, the service is secondary."""
        return await self.get_property(GattService1Property.PRIMARY)

    async def get_device(self) -> str:
        """Object path of the Bluetooth device the service
        belongs to."""
        return await self.get_property(GattService1Property.DEVICE)

    async def get_include(self) -> list[str]:
        """Array of object paths representing the included
        services of this service."""
        return await self.get_property(GattService1Property.INCLUDES)
