from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Mapping

from ..dbus.interface import Interface

ADAPTER_INTERFACE = "org.bluez.Adapter1"


class Adapter1Property(str, Enum):
    ADDRESS = "Address"
    ADDRESS_TYPE = "AddressType"
    NAME = "Name"
    ALIAS = "Alias"
    CLASS = "Class"
    POWERED = "Powered"
    POWER_STATE = "PowerState"
    DISCOVERABLE = "Discoverable"
    PAIRABLE = "Pairable"
    PAIRABLE_TIMEOUT = "PairableTimeout"
    DISCOVERABLE_TIMEOUT = "DiscoverableTimeout"
    DISCOVERING = "Discovering"
    UUIDS = "UUIDs"
    MODALIAS = "Modalias"
    ROLES = "Roles"
    EXPERIMENAL_FEATURES = "ExperimentalFeatures"


class Adapter1Member(str, Enum):
    START_DISCOVERY = "StartDiscovery"
    STOP_DISCOVERY = "StopDiscovery"
    REMOVE_DEVICE = "RemoveDevice"
    SET_DISCOVERY_FILTER = "SetDiscoveryFilter"
    GET_DISCOVERY_FILTERS = "GetDiscoveryFilters"
    CONNECT_DEVICE = "ConnectDevice"


class BluezAdapter(Interface, name=ADAPTER_INTERFACE):
    @property
    def short_name(self) -> str:
        return self.path.split("/")[-1]

    @property
    def address(self) -> str:
        """Return address of adapter"""
        return self.cached_properties[Adapter1Property.ADDRESS]

    @property
    def address_type(self) -> str:
        """Return address type of adapter. Can be either 'public' or 'random'.

        For dual-mode and BR/EDR only adapter this defaults to "public".
        Single mode LE adapters may have either value.
        With privacy enabled this contains type of Identity Address and not type of
        address used for connection.
        """
        return self.cached_properties[Adapter1Property.ADDRESS_TYPE]

    @property
    def name(self) -> str:
        """Return name of adapter.

        This property is either a static system default
        or controlled by an external daemon providing
        access to the pretty hostname configuration
        """
        return self.cached_properties[Adapter1Property.NAME]

    @property
    def alias(self) -> str | None:
        """The Bluetooth friendly name. This value can be changed.

        In case no alias is set, it will return the system
        provided name. Setting an empty string as alias will
        convert it back to the system provided name (hostname).
        """
        return self.cached_properties.get(Adapter1Property.ALIAS, None)

    @property
    def class_(self) -> int | None:
        """Return class of adapter.

        This property represents the value that is either
        automatically configured by DMI/ACPI information
        or provided as static configuration
        """
        return self.cached_properties.get(Adapter1Property.CLASS, None)

    @property
    def powered(self) -> bool:
        """Adapter state can be on or off"""
        return self.cached_properties[Adapter1Property.POWERED]

    @property
    def power_state(self) -> str:
        """The power state of an adapter.

        The power state will show whether the adapter is
        turning off, or turning on, as well as being on
        or off.

        Possible values:
            "on" - powered on
            "off" - powered off
            "off-enabling" - transitioning from "off" to "on"
            "on-disabling" - transitioning from "on" to "off"
            "off-blocked" - blocked by rfkill"""
        return self.cached_properties[Adapter1Property.POWER_STATE]

    @property
    def discoverable(self) -> bool:
        """An adapter can be discoverable or non-discoverable to either make it visible or hide it"""
        return self.cached_properties[Adapter1Property.DISCOVERABLE]

    @property
    def pairable(self) -> bool:
        """An adapter can be pairable or non-pairable.

        Note that this property only affects incoming pairing requests.
        """
        return self.cached_properties[Adapter1Property.PAIRABLE]

    @property
    def pairable_timeout(self) -> int:
        """The pairable timeout in seconds.

        A value of zero means that the timeout is disabled and it will stay in
        pairable mode forever."""
        return self.cached_properties[Adapter1Property.PAIRABLE_TIMEOUT]

    @property
    def discoverable_timeout(self) -> int:
        """The discoverable timeout in seconds. A value of zero
        means that the timeout is disabled and it will stay in
        discoverable/limited mode forever.
        """
        return self.cached_properties[Adapter1Property.DISCOVERABLE_TIMEOUT]

    @property
    def discovering(self) -> bool:
        """Indicates that a device discovery procedure is active"""
        return self.cached_properties[Adapter1Property.DISCOVERING]

    @property
    def modalias(self) -> str | None:
        """Local device ID information in modalias format used by the kernel and udev"""
        return self.cached_properties.get(Adapter1Property.MODALIAS, None)

    @property
    def UUIDs(self) -> list[str]:
        """List of 128-bit UUIDs that represents the available local services."""
        return self.cached_properties.get(Adapter1Property.UUIDS, [])

    @property
    def roles(self) -> list[str]:
        """List of supported roles. Possible values:
        - "central": Supports the central role.
        - "peripheral": Supports the peripheral role.
        - "central-peripheral": Supports both roles concurrently.
        """
        return self.cached_properties.get(Adapter1Property.ROLES, [])

    @property
    def experimental_features(self) -> list[str]:
        """List of 128-bit UUIDs that represents the experimental features currently enabled.

        Available from Bluez 5.62 only
        """
        return self.cached_properties.get(Adapter1Property.EXPERIMENAL_FEATURES, [])

    @property
    def last_update(self) -> datetime | None:
        return self.cached_properties.get("last_update", None)

    # Methods

    async def start_discovery(self) -> None:
        """This method starts the device discovery session. This
        includes an inquiry procedure and remote device name
        resolving. Use StopDiscovery to release the sessions
        acquired.

        This process will start creating Device objects as
        new devices are discovered.

        During discovery RSSI delta-threshold is imposed.

        Possible errors:
            - `org.bluez.Error.NotReady`
            - `org.bluez.Error.Failed`
        """
        await self.call(member=Adapter1Member.START_DISCOVERY)

    async def stop_discovery(self) -> None:
        """This method will cancel any previous StartDiscovery transaction.

        Note that a discovery procedure is shared between all
        discovery sessions thus calling StopDiscovery will only
        release a single session.

        Possible errors:
            - `org.bluez.Error.NotReady`
            - `org.bluez.Error.Failed`
            - `org.bluez.Error.NotAuthorized`
        """
        await self.call(member=Adapter1Member.STOP_DISCOVERY)

    async def remove_device(self, path: str) -> None:
        """This removes the remote device object at the given
        path. It will remove also the pairing information.

        Possible errors:
            - `org.bluez.Error.InvalidArguments`
            - `org.bluez.Error.Failed`
        """
        await self.call(member=Adapter1Member.REMOVE_DEVICE, signature="o", body=[path])

    async def set_discovery_filters(self, filters: Mapping[str, Any]) -> None:
        """Set discovery filters.

        When discovery filter is set, Device objects will be
        created as new devices with matching criteria are
        discovered regardless of they are connectable or
        discoverable which enables listening to
        non-connectable and non-discoverable devices.

        When multiple clients call SetDiscoveryFilter, their
        filters are internally merged, and notifications about
        new devices are sent to all clients. Therefore, each
        client must check that device updates actually match
        its filter.

        When SetDiscoveryFilter is called multiple times by the
        same client, last filter passed will be active for
        given client.

        SetDiscoveryFilter can be called before StartDiscovery.
        It is useful when client will create first discovery
        session, to ensure that proper scan will be started
        right after call to StartDiscovery.

        Possible errors:
            - `org.bluez.Error.NotReady`
            - `org.bluez.Error.NotSupported`
            - `org.bluez.Error.Failed`
        """
        v_filters: dict[str, Any] = {}
        # Always set "Transport" to "le"
        v_filters["Transport"] = self.service.codec.encode("le", "s")
        for key, value in filters.items():
            if key == "UUIDs":
                v_filters[key] = self.service.codec.encode(value, "as")
            elif key == "RSSI":
                v_filters[key] = self.service.codec.encode(value, "n")
            elif key == "DuplicateData":
                v_filters[key] = self.service.codec.encode(value, "b")
            elif key == "Pathloss":
                v_filters[key] = self.service.codec.encode(value, "n")
            elif key == "Transport":
                v_filters[key] = self.service.codec.encode(value, "s")
            else:
                # logger.warning("Filter '%s' is not currently supported." % key)
                continue
        await self.call(
            member=Adapter1Member.SET_DISCOVERY_FILTER,
            signature="a{sv}",
            body=[v_filters],
        )

    async def reset_discovery_filters(self) -> None:
        """Reset discovery filters.

        Note: This method is calls `SetDiscoveryFilters` without argument.

        Possible errors:
            - `org.bluez.Error.NotReady`
            - `org.bluez.Error.Failed`
        """
        await self.call(member=Adapter1Member.SET_DISCOVERY_FILTER)

    async def get_discovery_filters(self) -> list[str]:
        """Return available filters that can be given to SetDiscoveryFilter.

        Possible errors: None
        """
        reply = await self.call(member=Adapter1Member.GET_DISCOVERY_FILTERS)
        return reply.body[0]  # type: ignore[no-any-return]

    async def connect_device(self, address: str, address_type: str) -> None:
        """This method connects to device without need of performing General Discovery.

        Connection mechanism is smilar to Connect method from Device1
        interface with exception that this method returns success
        when physical connection is established.
        After this method returns, services discovery will continue
        and any supported profile will be connected.
        There is no need for calling Connect on Device1 after this call.
        If connection was successful this method returns object path to
        created device object.
        """
        await self.call(
            member=Adapter1Member.CONNECT_DEVICE,
            signature="a{sv}",
            body=[
                {
                    "Address": self.service.codec.encode(address, "s"),
                    "AddressType": self.service.codec.encode(address_type, "s"),
                }
            ],
        )

    #  Properties setters

    async def set_powered(self, powered: bool) -> None:
        """Power on adapter"""
        return await self.set_property(Adapter1Property.POWERED, powered, "b")

    async def set_alias(self, value: str) -> None:
        """Set the Bluetooth friendly name.

        Setting an empty string as alias will convert it back
        to the system provided name.
        """
        return await self.set_property(Adapter1Property.ALIAS, value, "s")

    async def set_discoverable(self, value: bool) -> None:
        """Switch an adapter to discoverable or non-discoverable
        to either make it visible or hide it.

        In case the adapter is switched off, setting this
        value will fail.
        """
        return await self.set_property(Adapter1Property.DISCOVERABLE, value, "b")

    async def set_pairable(self, value: bool) -> None:
        """Switch an adapter to pairable or non-pairable.

        Note that this property only affects incoming pairing
        requests.
        """
        return await self.set_property(Adapter1Property.PAIRABLE, value, "b")

    async def set_pairable_timeout(self, value: int) -> None:
        """The pairable timeout in seconds.

        A value of zero means that the timeout is disabled
        and it will stay in pairable mode forever.
        """
        await self.set_property(Adapter1Property.PAIRABLE_TIMEOUT, value, "i")

    async def set_discoverable_timeout(self, value: int) -> None:
        """The discoverable timeout in seconds.

        A value of zero means that the timeout is disabled
        and it will stay in discoverable/limited mode forever.
        """
        await self.set_property(Adapter1Property.DISCOVERABLE_TIMEOUT, value, "i")

    async def get_address(self) -> str:
        """The Bluetooth device address."""
        return await self.get_property(Adapter1Property.ADDRESS)

    async def get_address_type(self) -> str:
        """The Bluetooth  Address Type.
        For dual-mode and BR/EDR only adapter this defaults to "public".
        Single mode LE adapters may have either value. With privacy enabled
        this contains type of Identity Address and not type of
        address used for connection.

        Possible values:
            - `public`: Public address
            - `random`: Random address
        """
        return await self.get_property(Adapter1Property.ADDRESS_TYPE)

    async def get_name(self) -> str:
        """The Bluetooth system name (pretty hostname).

        This property is either a static system default
        or controlled by an external daemon providing
        access to the pretty hostname configuration.
        """
        return await self.get_property(Adapter1Property.NAME)

    async def get_alias(self) -> str:
        """The Bluetooth friendly name. This value can be changed.

        In case no alias is set, it will return the system provided name.
        Only if the local name needs to be different from the pretty
                hostname, this property should be used as last resort.
        """
        return await self.get_property(Adapter1Property.ALIAS)

    async def get_class(self) -> int:
        """Return class of adapter.

        This property represents the value that is either
        automatically configured by DMI/ACPI information
        or provided as static configuration
        """
        return await self.get_property(Adapter1Property.CLASS)

    async def get_powered(self) -> bool:
        """The value of this property is not persistent.

        After restart or unplugging of the adapter it will reset
                back to false.
        """
        return await self.get_property(Adapter1Property.POWERED)

    async def get_power_state(self) -> bool:
        """The value of this property is not persistent."""
        return await self.get_property(Adapter1Property.POWER_STATE)

    async def get_discoverable(self) -> bool:
        """Adapter is visible when True or hidden when False."""
        return await self.get_property(Adapter1Property.DISCOVERABLE)

    async def get_pairable(self) -> bool:
        """Whether the adapter accepts or reject incoming pairing requests."""
        return await self.get_property(Adapter1Property.PAIRABLE)

    async def get_pairable_timeout(self) -> int:
        """The pairable timeout in seconds"""
        return await self.get_property(Adapter1Property.PAIRABLE_TIMEOUT)

    async def get_discoverable_timeout(self) -> int:
        """The discoverable timeout in seconds."""
        return await self.get_property(Adapter1Property.DISCOVERABLE_TIMEOUT)

    async def get_discovering(self) -> bool:
        """Indicates that a device discovery procedure is active"""
        return await self.get_property(Adapter1Property.DISCOVERING)

    async def get_uuids(self) -> list[str]:
        """List of 128-bit UUIDs that represents the available local services."""
        return await self.get_property(Adapter1Property.UUIDS)

    async def get_modalias(self) -> str:
        """Local Device ID information in modalias format
        used by the kernel and udev.
        """
        return await self.get_property(Adapter1Property.MODALIAS)
