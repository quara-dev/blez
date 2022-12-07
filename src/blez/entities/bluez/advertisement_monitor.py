from __future__ import annotations

from enum import Enum
from typing import NamedTuple

from ..assigned import AdvertisementDataType
from ..dbus.interface import Interface


class OrPattern(NamedTuple):
    """
    BlueZ advertisement monitor or-pattern.
    https://github.com/bluez/bluez/blob/master/doc/advertisement-monitor-api.txt
    """

    start_position: int
    ad_data_type: AdvertisementDataType
    content_of_pattern: bytes


ADVERTISEMENT_MONITOR_INTERFACE = "org.bluez.AdvertisementMonitor1"
ADVERTISEMENT_MONITOR_MANAGER_INTERFACE = "org.bluez.AdvertisementMonitorManager1"


class AdvertisementMonitor1Property(str, Enum):
    TYPE = "Type"
    RSSI_LOW_THRESHOLD = "RSSILowThreshold"
    RSSI_HIGH_THRESHOLD = "RSSIHighThreshold"
    RSSI_LOW_TIMEOUT = "RSSILowTimeout"
    RSSI_HIGH_TIMEOUT = "RSSIHighTimeout"
    RSSI_SAMPLING_PERIOD = "RSSISamplingPeriod"
    PATTERNS = "Patterns"


class AdvertisementMonitorManager1Property(str, Enum):
    SUPPORTED_MONITOR_TYPES = "SupportedMonitorTypes"
    SUPPORTED_FEATURES = "SupportedFeatures"


class AdvertisementMonitorManager1Member(str, Enum):
    REGISTER_MONITOR = "RegisterMonitor"
    UNREGISTER_MONITOR = "UnregisterMonitor"


class BluezAdvertisementMonitor(Interface, name=ADVERTISEMENT_MONITOR_INTERFACE):
    @property
    def type(self) -> str:
        """The type of the monitor.

        See SupportedMonitorTypes in org.bluez.AdvertisementMonitorManager1
        for the available options.
        """
        return self.cached_properties[AdvertisementMonitor1Property.TYPE]

    @property
    def rssi_low_threshold(self) -> int | None:
        """Used in conjunction with RSSILowTimeout to determine
        whether a device becomes out-of-range.

        Valid range is -127 to 20 (dBm), while 127 indicates unset."""
        return self.cached_properties.get(
            AdvertisementMonitor1Property.RSSI_LOW_THRESHOLD, None
        )

    @property
    def rssi_high_threshold(self) -> int | None:
        """Used in conjunction with RSSIHighTimeout to determine
                whether a device becomes in-range.

        Valid range is -127 to 20 (dBm), while 127 indicates unset."""
        return self.cached_properties.get(
            AdvertisementMonitor1Property.RSSI_HIGH_THRESHOLD, None
        )

    @property
    def rssi_low_timeout(self) -> int | None:
        """The time it takes to consider a device as out-of-range.

                If this many seconds elapses without receiving any signal
        at least as strong as RSSILowThreshold, a currently in-range
        device will be considered as out-of-range (lost).

        Valid range is 1 to 300 (seconds), while 0 indicates unset."""
        return self.cached_properties.get(
            AdvertisementMonitor1Property.RSSI_LOW_TIMEOUT, None
        )

    @property
    def rssi_high_timeout(self) -> int | None:
        """The time it takes to consider a device as in-range.

        If this many seconds elapses while we continuously receive signals
        at least as strong as RSSIHighThreshold, a currently out-of-range
        device will be considered as in-range (found).

        Valid range is 1 to 300 (seconds), while 0 indicates unset.
        """
        return self.cached_properties.get(
            AdvertisementMonitor1Property.RSSI_HIGH_TIMEOUT, None
        )

    @property
    def rssi_sampling_period(self) -> int | None:
        """Grouping rules on how to propagate the received
        advertisement packets to the client.

        Valid range is 0 to 255 while 256 indicates unset.

        The meaning of this property is as follows:

        - 0:
            All advertisement packets from in-range devices
            would be propagated.
        - 255:
            Only the first advertisement packet of in-range
            devices would be propagated. If the device
            becomes lost, then the first packet when it is
            found again will also be propagated.
        - 1 to 254:
            Advertisement packets would be grouped into
            100ms * N time period. Packets in the same group
            will only be reported once, with the RSSI value
            being averaged out.

        Currently this is unimplemented in user space, so the
        value is only used to be forwarded to the kernel.
        """
        return self.cached_properties.get(
            AdvertisementMonitor1Property.RSSI_SAMPLING_PERIOD, None
        )

    @property
    def patterns(self) -> tuple[int, int, bytes] | None:
        """If the Type property is set to "or_patterns", then this
        property must exist and have at least one entry in the
        array.

        The structure of a pattern contains the following:

        uint8 start_position
            The index in an AD data field where the search
            should start. The beginning of an AD data field
            is index 0.

        uint8 AD_data_type
            See https://www.bluetooth.com/specifications/
            assigned-numbers/generic-access-profile/ for
            the possible allowed value.

        array{byte} content_of_pattern
            This is the value of the pattern. The maximum
            length of the bytes is 31.
        """
        patterns = self.cached_properties.get(
            AdvertisementMonitor1Property.PATTERNS, None
        )
        if patterns is None:
            return None
        return OrPattern(*patterns)

    async def get_type(self) -> str:
        return await self.get_property(AdvertisementMonitor1Property.TYPE)

    async def get_rssi_low_threshold(self) -> int | None:
        return await self.get_property(AdvertisementMonitor1Property.RSSI_LOW_THRESHOLD)

    async def get_rssi_high_threshold(self) -> int | None:
        return await self.get_property(
            AdvertisementMonitor1Property.RSSI_HIGH_THRESHOLD
        )

    async def get_rssi_low_timeout(self) -> int | None:
        return await self.get_property(AdvertisementMonitor1Property.RSSI_LOW_TIMEOUT)

    async def get_rssi_high_timeout(self) -> int | None:
        return await self.get_property(AdvertisementMonitor1Property.RSSI_HIGH_TIMEOUT)

    async def get_rssi_sampling_period(self) -> int | None:
        return await self.get_property(
            AdvertisementMonitor1Property.RSSI_SAMPLING_PERIOD
        )

    async def get_patterns(self) -> OrPattern:
        patterns = await self.get_property(AdvertisementMonitor1Property.PATTERNS)
        if patterns is None:
            return None
        return OrPattern(*patterns)


class BluezAdvertisementMonitorManager(
    Interface, name=ADVERTISEMENT_MONITOR_MANAGER_INTERFACE
):
    @property
    def supported_monitor_types(self) -> list[str]:
        """This lists the supported types of advertisement monitors.

        An application should check this before instantiate and expose an object of
        org.bluez.AdvertisementMonitor1.
        """
        return self.cached_properties[
            AdvertisementMonitorManager1Property.SUPPORTED_MONITOR_TYPES
        ]

    @property
    def supported_features(self) -> list[str]:
        """This lists the fetures of advertisement monitoring supported by Bluez

        Possible values for features:
            "controller-patterns"
                If the controller is capable of performing
                advertisement monitoring by patterns, BlueZ
                would offload the patterns to the controller to
                reduce power consumption.
        """
        return self.cached_properties[
            AdvertisementMonitorManager1Property.SUPPORTED_FEATURES
        ]

    async def register_monitor(self, object_path: str) -> None:
        """This registers the root path of a hierarchy of advertisement monitors.

        The application object path together with the D-Bus
        system bus connection ID define the identification of
        the application registering advertisement monitors.

        Once a root path is registered by a client via this
        method, the client can freely expose/unexpose
        advertisement monitors without re-registering the root
        path again.

        After use, the client should call UnregisterMonitor() method
        to invalidate the advertisement monitors.

        Possible errors:
            org.bluez.Error.InvalidArguments
            org.bluez.Error.AlreadyExists
            org.bluez.Error.Failed
        """
        await self.call("RegisterMonitor", "o", [object_path])

    async def unregister_monitor(self, object_path: str) -> None:
        """This unregisters a hierarchy of advertisement monitors
        that has been previously registered.

        The object path parameter must match the same value that
        has been used on registration.
        Upon unregistration, the advertisement monitor(s) should
        expect to receive Release() method as the signal that
        the advertisement monitor(s) has been deactivated.

        Possible errors:
            org.bluez.Error.InvalidArguments
            org.bluez.Error.DoesNotExist
        """
        await self.call(
            AdvertisementMonitorManager1Member.UNREGISTER_MONITOR, "o", [object_path]
        )

    async def get_supported_monitor_types(self) -> list[str]:
        return await self.get_property(
            AdvertisementMonitorManager1Property.SUPPORTED_MONITOR_TYPES
        )

    async def get_supported_features(self) -> list[str]:
        return await self.get_property(
            AdvertisementMonitorManager1Property.SUPPORTED_FEATURES
        )
