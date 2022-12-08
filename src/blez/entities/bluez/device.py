from __future__ import annotations

from datetime import datetime
from enum import Enum

from ..assigned import StandardCharacteristic
from ..dbus.interface import Interface
from .gatt_characteristic import BluezGattCharacteristic

DEVICE_INTERFACE = "org.bluez.Device1"
BATTERY_INTERFACE = "org.bluez.Battery1"


class Battery1Property(str, Enum):
    PERCENTAGE = "Percentage"


class Device1Property(str, Enum):
    ADDRESS = "Address"
    ADDRESS_TYPE = "AddressType"
    NAME = "Name"
    ICON = "Icon"
    CLASS = "Class"
    APPEARANCE = "Appearance"
    UUIDS = "UUIDs"
    PAIRED = "Paired"
    BONDED = "Bonded"
    CONNECTED = "Connected"
    TRUSTED = "Trusted"
    BLOCKED = "Blocked"
    WAKE_ALLOWED = "WakeAllowed"
    ALIAS = "Alias"
    ADAPTER = "Adapter"
    LEGACY_PAIRING = "LegacyPairing"
    MODALIAS = "Modalias"
    RSSI = "RSSI"
    TX_POWER = "TxPower"
    MANUFACTURER_DATA = "ManufacturerData"
    SERVICE_DATA = "ServiceData"
    SERVICES_RESOLVED = "ServicesResolved"
    ADVERTISING_FLAGS = "AdvertisingFlags"
    ADVERTISING_DATA = "AdvertisingData"


class Device1Member(str, Enum):
    CONNECT = "Connect"
    DISCONNECT = "Disconnect"
    CONNECT_PROFILE = "ConnectProfile"
    DISCONNECT_PROFILE = "DisconnectProfile"
    PAIR = "Pair"
    CANCEL_PAIRING = "CancelPairing"


class BluezDevice(Interface, name=DEVICE_INTERFACE):
    """This implementation depends solely on the abstract class Interface."""

    @property
    def adapter(self) -> str:
        return self.cached_properties[Device1Property.ADAPTER]

    @property
    def address(self) -> str:
        return self.cached_properties[Device1Property.ADDRESS]

    @property
    def address_type(self) -> str | None:
        return self.cached_properties.get(Device1Property.ADDRESS_TYPE, None)

    @property
    def name(self) -> str | None:
        return self.cached_properties.get(Device1Property.NAME, None)

    @property
    def alias(self) -> str | None:
        return self.cached_properties.get(Device1Property.ALIAS, None)

    @property
    def icon(self) -> str | None:
        return self.cached_properties.get(Device1Property.ICON, None)

    @property
    def class_(self) -> int | None:
        return self.cached_properties.get(Device1Property.CLASS, None)

    @property
    def appearance(self) -> int | None:
        return self.cached_properties.get(Device1Property.APPEARANCE, None)

    @property
    def uuids(self) -> list[str]:
        return self.cached_properties.get(Device1Property.UUIDS, [])

    @property
    def paired(self) -> bool:
        return self.cached_properties[Device1Property.PAIRED]

    @property
    def connected(self) -> bool:
        return self.cached_properties[Device1Property.CONNECTED]

    @property
    def trusted(self) -> bool:
        return self.cached_properties[Device1Property.TRUSTED]

    @property
    def wake_allowed(self) -> bool:
        return self.cached_properties[Device1Property.WAKE_ALLOWED]

    @property
    def blocked(self) -> bool:
        return self.cached_properties[Device1Property.BLOCKED]

    @property
    def legacy_pairing(self) -> bool:
        return self.cached_properties[Device1Property.LEGACY_PAIRING]

    @property
    def modalias(self) -> str | None:
        return self.cached_properties.get(Device1Property.MODALIAS, None)

    @property
    def tx_power(self) -> int | None:
        return self.cached_properties.get(Device1Property.TX_POWER, None)

    @property
    def rssi(self) -> int | None:
        return self.cached_properties.get(Device1Property.RSSI, None)

    @property
    def manufacturer_data(self) -> dict[str, bytearray]:
        return self.cached_properties.get(Device1Property.MANUFACTURER_DATA, {})

    @property
    def service_data(self) -> dict[str, bytearray]:
        return self.cached_properties.get(Device1Property.SERVICE_DATA, {})

    @property
    def services_resolved(self) -> bool:
        return self.cached_properties.get(Device1Property.SERVICES_RESOLVED, False)

    @property
    def advertising_flags(self) -> bytearray | None:
        return self.cached_properties.get(Device1Property.ADVERTISING_FLAGS, None)

    @property
    def advertising_data(self) -> dict[str, bytearray]:
        return self.cached_properties.get(Device1Property.ADVERTISING_DATA, {})

    @property
    def battery_level(self) -> int | None:
        """Access battery through a different interfact."""
        return self.service.tree.get_interface(self.path, BATTERY_INTERFACE).get(
            Battery1Property.PERCENTAGE, None
        )

    @property
    def last_update(self) -> datetime | None:
        return self.cached_properties.get("last_update", None)

    @property
    def last_discovery(self) -> datetime | None:
        return self.cached_properties.get("last_discovery", None)

    async def connect(self) -> None:
        """This is a generic method to connect any profiles
        the remote device supports that can be connected
        to and have been flagged as auto-connectable on
        our side. If only subset of profiles is already
        connected it will try to connect currently disconnected
        ones.

        If at least one profile was connected successfully this
        method will indicate success.

        For dual-mode devices only one bearer is connected at
        time, the conditions are in the following order:

            1. Connect the disconnected bearer if already
            connected.

            2. Connect first the bonded bearer. If no
            bearers are bonded or both are skip and check
            latest seen bearer.

            3. Connect last seen bearer, in case the
            timestamps are the same BR/EDR takes
            precedence.

        Possible errors:
            - `org.bluez.Error.NotReady`
            - `org.bluez.Error.Failed`
            - `org.bluez.Error.InProgress`
            - `org.bluez.Error.AlreadyConnected`
        """
        await self.call(member=Device1Member.CONNECT)

    async def disconnect(self) -> None:
        """This method gracefully disconnects all connected
        profiles and then terminates low-level ACL connection.

        ACL connection will be terminated even if some profiles
        were not disconnected properly e.g. due to misbehaving
        device.

        This method can be also used to cancel a preceding
        Connect call before a reply to it has been received.

        For non-trusted devices connected over LE bearer calling
        this method will disable incoming connections until
        Connect method is called again.

        Possible errors:
            - `org.bluez.Error.NotConnected`
        """
        await self.call(member=Device1Member.DISCONNECT)

    async def connect_profile(self, uuid: str) -> None:
        """This method connects a specific profile of this
        device. The UUID provided is the remote service
        UUID for the profile.

        Possible errors:
            - `org.bluez.Error.Failed`
            - `org.bluez.Error.InProgress`
            - `org.bluez.Error.InvalidArguments`
            - `org.bluez.Error.NotAvailable`
            - `org.bluez.Error.NotReady`
        """
        await self.call(
            member=Device1Member.CONNECT_PROFILE, signature="s", body=[uuid]
        )

    async def disconnect_profile(self, uuid: str) -> None:
        """This method disconnects a specific profile of
        this device. The profile needs to be registered
        client profile.

        There is no connection tracking for a profile, so
        as long as the profile is registered this will always
        succeed.

        Possible errors:
            - `org.bluez.Error.Failed`
            - `org.bluez.Error.InProgress`
            - `org.bluez.Error.InvalidArguments`
            - `org.bluez.Error.NotSupported`
        """
        await self.call(
            member=Device1Member.DISCONNECT_PROFILE, signature="s", body=[uuid]
        )

    async def pair(self) -> None:
        """This method will connect to the remote device,
        initiate pairing and then retrieve all SDP records
        (or GATT primary services).

        If the application has registered its own agent,
        then that specific agent will be used. Otherwise
        it will use the default agent.

        Only for applications like a pairing wizard it
        would make sense to have its own agent. In almost
        all other cases the default agent will handle
        this just fine.

        In case there is no application agent and also
        no default agent present, this method will fail.

        Possible errors:
            - `org.bluez.Error.InvalidArguments`
            `org.bluez.Error.Failed`
            `org.bluez.Error.AlreadyExists`
            `org.bluez.Error.AuthenticationCanceled`
            `org.bluez.Error.AuthenticationFailed`
            `org.bluez.Error.AuthenticationRejected`
            `org.bluez.Error.AuthenticationTimeout`
            `org.bluez.Error.ConnectionAttemptFailed`
        """
        await self.call(member=Device1Member.PAIR)

    async def cancel_pairing(self) -> None:
        """This method can be used to cancel a pairing
        operation initiated by the Pair method.

        Possible errors:
            - `org.bluez.Error.DoesNotExist`
            - `org.bluez.Error.Failed`
        """
        await self.call(member=Device1Member.CANCEL_PAIRING)

    async def set_trusted(self, trusted: bool) -> None:
        """Indicates if the remote is seen as trusted."""
        await self.set_property(Device1Property.TRUSTED, trusted, "b")

    async def set_blocked(self, blocked: bool) -> None:
        """If set to true any incoming connections from the
        device will be immediately rejected.

        t.Any device drivers will also be removed and no new ones will
        be probed as long as the device is blocked.
        """
        await self.set_property(Device1Property.BLOCKED, blocked, "b")

    async def set_alias(self, alias: str) -> None:
        """The name alias for the remote device. The alias can
        be used to have a different friendly name for the
        remote device.

        When resetting the alias with an empty string, the
                property will default back to the remote name.
        """
        await self.set_property(Device1Property.ALIAS, alias, "s")

    async def get_address(self) -> str:
        """The Bluetooth device address of the remote device."""
        return await self.get_property(Device1Property.ADDRESS)

    async def get_address_type(self) -> str:
        """The Bluetooth device Address Type.

        For dual-mode and BR/EDR only devices this defaults to "public".
        Single mode LE devices may have either value.
        If remote device uses privacy than before pairing this
        represents address type used for connection and
        Identity Address after pairing.
        """
        return await self.get_property(Device1Property.ADDRESS_TYPE)

    async def get_name(self) -> str:
        """The Bluetooth remote name. This value can not be
        changed. Use the Alias property instead.

        This value is only present for completeness. It is
        better to always use the Alias property when
        displaying the devices name.

        If the Alias property is unset, it will reflect
        this value which makes it more convenient.
        """
        return await self.get_property(Device1Property.NAME)

    async def get_icon(self) -> str:
        """Proposed icon name according to the freedesktop.org
        icon naming specification."""
        return await self.get_property(Device1Property.ICON)

    async def get_class(self) -> int:
        """The Bluetooth class of device of the remote device."""
        return await self.get_property(Device1Property.CLASS)

    async def get_appearance(self) -> int:
        """External appearance of device, as found on GAP service."""
        return await self.get_property(Device1Property.APPEARANCE)

    async def get_uuids(self) -> list[str]:
        """t.List of 128-bit UUIDs that represents the available
        remote services."""
        return await self.get_property(Device1Property.UUIDS)

    async def get_paired(self) -> bool:
        """Indicates if the remote device is paired."""
        return await self.get_property(Device1Property.PAIRED)

    async def get_connected(self) -> bool:
        """Indicates if the remote device is currently connected.

        A PropertiesChanged signal indicate changes to this
        status.
        """
        return await self.get_property(Device1Property.CONNECTED)

    async def get_trusted(self) -> bool:
        """Indicates if the remote is seen as trusted."""
        return await self.get_property(Device1Property.TRUSTED)

    async def get_blocked(self) -> bool:
        """If set to true any incoming connections from the
        device will be immediately rejected.

        t.Any device drivers will also be removed and no new ones will
        be probed as long as the device is blocked.
        """
        return await self.get_property(Device1Property.BLOCKED)

    async def get_alias(self) -> str:
        """The name alias for the remote device."""
        return await self.get_property(Device1Property.ALIAS)

    async def get_adapter(self) -> str:
        """The object path of the adapter the device belongs to."""
        return await self.get_property(Device1Property.ADAPTER)

    async def get_legacy_pairing(self) -> bool:
        """Set to true if the device only supports the pre-2.1
        pairing mechanism. This property is useful during
        device discovery to anticipate whether legacy or
        simple pairing will occur if pairing is initiated."""
        return await self.get_property(Device1Property.LEGACY_PAIRING)

    async def get_modalias(self) -> int:
        """Remote Device ID information in modalias format
        used by the kernel and udev."""
        return await self.get_property(Device1Property.MODALIAS)

    async def get_rssi(self) -> int:
        """Received Signal Strength Indicator of the remote
        device (inquiry or advertising)."""
        return await self.get_property(Device1Property.RSSI)

    async def get_txpower(self) -> int:
        """Advertised transmitted power level (inquiry or advertising)."""
        return await self.get_property(Device1Property.TX_POWER)

    async def get_manufacturer_data(self) -> dict[int, bytearray]:
        """Manufacturer specific advertisement data.

        Keys are 16 bits Manufacturer ID followed by
        its byte array value.
        """
        return await self.get_property(Device1Property.MANUFACTURER_DATA)

    async def get_service_data(self) -> dict[str, bytearray]:
        """Service advertisement data.

        Keys are the UUIDs in string format followed by its byte array value.
        """
        return await self.get_property(Device1Property.SERVICE_DATA)

    async def get_services_resolved(self) -> bool:
        """Indicate whether or not service discovery has been
        resolved."""
        return await self.get_property(Device1Property.SERVICES_RESOLVED)

    async def get_advertising_flags(self) -> bytearray:
        """The Advertising Data Flags of the remote device."""
        return await self.get_property(Device1Property.ADVERTISING_FLAGS)

    async def get_advertising_data(self) -> dict[int, bytearray]:
        """The Advertising Data of the remote device. Keys are
        are 8 bits AD Type followed by data as byte array.

        Note: Only types considered safe to be handled by
        application are exposed.
        """
        return await self.get_property(Device1Property.ADVERTISING_DATA)

    async def read_battery(self) -> int:
        """Read battery level"""
        return await self.service.get_property(
            path=self.path, interface=BATTERY_INTERFACE, key=Battery1Property.PERCENTAGE
        )

    # Wrappers
    def get_characteristic(
        self, char_or_uuid: str | BluezGattCharacteristic
    ) -> BluezGattCharacteristic:
        """Get a characteristic from device."""
        if isinstance(char_or_uuid, BluezGattCharacteristic):
            char_or_uuid = char_or_uuid.uuid
        elif isinstance(char_or_uuid, StandardCharacteristic):
            char_or_uuid = char_or_uuid.value
        for characteristic in self.service.tree.get_all_interfaces(
            BluezGattCharacteristic.DBUS_INTERFACE, prefix=self.path
        ).values():
            if characteristic["uuid"] == char_or_uuid:
                return characteristic
        raise KeyError(char_or_uuid)

    async def read(
        self, characteristic: str | BluezGattCharacteristic, offset: int | None = None
    ) -> bytearray:
        """Read a characteristic value."""
        # Mock battery read
        if characteristic == StandardCharacteristic.BATTERY_LEVEL:
            value = await self.read_battery()
            return bytearray([value])
        # Get GATT characteristic
        gatt_char = self.get_characteristic(char_or_uuid=characteristic)
        # Fetch characteristic and call read method
        return await gatt_char.read_value(offset=offset)

    async def write(
        self,
        characteristic: str | BluezGattCharacteristic,
        value: bytearray,
        offset: int | None = None,
        prepare_authorize: bool | None = None,
    ) -> int:
        """Write a characteristic value"""
        # Get GATT characteristic
        gatt_char = self.get_characteristic(char_or_uuid=characteristic)
        return await gatt_char.write_value(
            value, offset=offset, prepare_authorize=prepare_authorize
        )

    async def start_notify(
        self, characteristic: str | BluezGattCharacteristic, always: bool = False
    ) -> None:
        # Mock battery noify
        if characteristic == StandardCharacteristic.BATTERY_LEVEL:
            return None
        gatt_char = self.get_characteristic(char_or_uuid=characteristic)
        # Look into cache if characteristic is already notifying
        if always or not gatt_char.notifying:
            return await gatt_char.start_notify()

    async def stop_notify(
        self, characteristic: str | BluezGattCharacteristic, always: bool = False
    ) -> None:
        # Mock battery noify
        if characteristic == StandardCharacteristic.BATTERY_LEVEL:
            return None
        gatt_char = self.get_characteristic(char_or_uuid=characteristic)
        # Look into cache if characteristic is already notifying
        if always or gatt_char.notifying:
            return await gatt_char.stop_notify()
