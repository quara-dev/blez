from typing import TYPE_CHECKING

from .device import DEVICE_INTERFACE, Device1Property
from .messages import (
    BluezMessage,
    InterfacesAdded,
    InterfacesRemoved,
    PropertiesChanged,
)

if TYPE_CHECKING:
    Event = InterfacesAdded | InterfacesRemoved | PropertiesChanged
else:
    Event = BluezMessage


def device_discovered(message: Event) -> bool:
    """Return True if device has been discovered"""
    if isinstance(message, PropertiesChanged):
        if Device1Property.RSSI in message.changed_props:
            return True
        return False
    if isinstance(message, InterfacesAdded):
        if DEVICE_INTERFACE in message.added_interfaces:
            if Device1Property.RSSI in message.added_interfaces[DEVICE_INTERFACE]:
                return True
    return False


def device_connected(message: Event) -> bool:
    """Return True if device successfully connected"""
    if isinstance(message, PropertiesChanged):
        if message.interface.get(Device1Property.CONNECTED, False):
            return True
        return False
    if isinstance(message, InterfacesAdded):
        if message.added_interfaces.get(DEVICE_INTERFACE, {}).get(
            Device1Property.CONNECTED, False
        ):
            return True
        return False
    return False
