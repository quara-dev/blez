from __future__ import annotations

from enum import Enum

from ..dbus.interface import Interface

GATT_CHARACTERISTIC_INTERFACE = "org.bluez.GattCharacteristic1"


class GattCharacteristic1Property(str, Enum):
    UUID = "UUID"
    Service = "Service"
    Value = "Value"
    WriteAcquired = "WriteAcquired"
    NotifyAcquired = "NotifyAcquired"
    Notifying = "Notifying"
    Flags = "Flags"
    Handle = "Handle"
    MTU = "MTU"


class GattCharacteristic1Member(str, Enum):
    READ_VALUE = "ReadValue"
    WRITE_VALUE = "WriteValue"
    ACQUIRE_WRITE = "AcquireWrite"
    ACQUIRE_NOTIFY = "AcquireNotify"
    START_NOTIFY = "StartNotify"
    STOP_NOTIFY = "StopNotify"


class GattCharacteristic1Signature(str, Enum):
    READ_VALUE = "a{sv}"
    WRITE_VALUE = "aya{sv}"
    ACQUIRE_WRITE = "a{sv}"
    ACQUIRE_NOTIFY = "a{sv}"


class GattCharacteristic1MemberOption(str, Enum):
    OFFSET = "offset"
    PREPARE_AUTHORIZE = "prepare-authorize"


class BluezGattCharacteristic(Interface, name=GATT_CHARACTERISTIC_INTERFACE):
    @property
    def uuid(self) -> str:
        """Get characteristic UUID"""
        return self.cached_properties[GattCharacteristic1Property.UUID]

    @property
    def value(self) -> bytearray | None:
        return self.cached_properties.get(GattCharacteristic1Property.Value, None)

    @property
    def write_acquired(self) -> bool | None:
        return self.cached_properties.get(
            GattCharacteristic1Property.WriteAcquired, None
        )

    @property
    def notify_acquired(self) -> bool | None:
        return self.cached_properties.get(
            GattCharacteristic1Property.NotifyAcquired, None
        )

    @property
    def notifying(self) -> bool | None:
        return self.cached_properties.get(GattCharacteristic1Property.Notifying, None)

    @property
    def flags(self) -> list[str]:
        return self.cached_properties.get(GattCharacteristic1Property.Flags, [])

    @property
    def handle(self) -> int | None:
        return self.cached_properties.get(GattCharacteristic1Property.Handle, None)

    @property
    def mtu(self) -> int | None:
        return self.cached_properties.get(GattCharacteristic1Property.MTU, None)

    async def read_value(self, offset: int | None = None) -> bytearray:
        """Issues a request to read the value of the
        characteristic and returns the value if the
        operation was successful.

        Possible Errors: org.bluez.Error.Failed
            - `org.bluez.Error.InProgress`
            - `org.bluez.Error.NotPermitted`
            - `org.bluez.Error.NotAuthorized`
            - `org.bluez.Error.InvalidOffset`
            - `org.bluez.Error.NotSupported`
        """
        # Fetch codec from client
        codec = self.service.client.codec
        # Build options
        options = {}
        if offset is not None:
            options[GattCharacteristic1MemberOption.OFFSET] = codec.encode(offset, "n")
        # Send message
        reply = await self.call(
            member=GattCharacteristic1Member.READ_VALUE,
            signature=GattCharacteristic1Signature.READ_VALUE,
            body=[options],
        )
        # Return value as bytearray
        return bytearray(reply.body[0])

    async def write_value(
        self,
        value: bytes | bytearray,
        offset: int | None = None,
        prepare_authorize: bool | None = None,
    ) -> int:
        # Fetch codec from client
        codec = self.service.client.codec
        # Convert payload to bytes
        payload = bytes(value)
        # Initialize options
        options = {}
        # Include options
        if offset is not None:
            options[GattCharacteristic1MemberOption.OFFSET] = codec.encode(offset, "n")
        if prepare_authorize is not None:
            options[GattCharacteristic1MemberOption.PREPARE_AUTHORIZE] = codec.encode(
                prepare_authorize, "b"
            )
        # Send message
        await self.call(
            member=GattCharacteristic1Member.WRITE_VALUE,
            signature=GattCharacteristic1Signature.WRITE_VALUE,
            body=[payload, options],
        )
        # Return number of bytes written
        return len(payload)

    async def acquire_write(self) -> tuple[int, int]:
        """Acquire file descriptor and MTU for writing.

        Only sockets are supported. Usage of `WriteValue` will be
        locked causing it to return NotPermitted error.

        For client it only works with characteristic that has
        WriteAcquired property which relies on `write-without-response` Flag.

        To release the lock the client shall close the file
        descriptor, a HUP is generated in case the device
        is disconnected.

        Possible errors:
            - `org.bluez.Error.Failed`
            - `org.bluez.Error.NotSupported`

        Returns:
            A tuple of two elements: (unix file descriptor, MTU).
            The file descriptor can be closed using `os.close`.

        Example:
        ```python
        # Acquire file descriptor
        fd, mtu = await char.acquire_write()
        # Close descriptor later
        os.close(fd)
        ```
        """
        reply = await self.call(
            member=GattCharacteristic1Member.ACQUIRE_WRITE,
            signature=GattCharacteristic1Signature.ACQUIRE_WRITE,
            body=[{}],
        )
        return reply.unix_fds[0], reply.body[1]

    async def acquire_notify(self) -> tuple[int, int]:
        """Acquire file descriptor and MTU for notify. Only
        sockets are support. Usage of StartNotify will be locked
        causing it to return NotPermitted error.

        Only works with characteristic that has NotifyAcquired
        which relies on notify Flag and no other client have
        called `StartNotify`.

        Notification are enabled during this procedure so
        StartNotify shall not be called, any notification
        will be dispatched via file descriptor therefore the
        Value property is not affected during the time where
        notify has been acquired.

        To release the lock the client shall close the file
        descriptor, a HUP is generated in case the device
        is disconnected.

        Note: the MTU can only be negotiated once and is
        symmetric therefore this method may be delayed in
        order to have the exchange MTU completed, because of
        that the file descriptor is closed during
        reconnections as the MTU has to be renegotiated.

        Possible Errors:
            - `org.bluez.Error.Failed`
            - `org.bluez.Error.NotSupported`

        Returns:
            A tuple of two elements: (unix file descriptor, MTU).
            The file descriptor can be closed using `os.close`.

        Example:
        ```python
        # Acquire file descriptor
        fd, mtu = await char.acquire_notify()
        # Close descriptor later
        os.close(fd)
        ```
        """
        reply = await self.call(
            member=GattCharacteristic1Member.ACQUIRE_NOTIFY,
            signature=GattCharacteristic1Signature.ACQUIRE_NOTIFY,
            body=[{}],
        )
        return reply.unix_fds[0], reply.body[1]

    async def start_notify(self) -> None:
        """Starts a notification session from this characteristic
        if it supports value notifications or indications.

        Possible Errors:
            - `org.bluez.Error.Failed`
            - `org.bluez.Error.NotPermitted`
            - `org.bluez.Error.InProgress`
            - `org.bluez.Error.NotConnected`
            - `org.bluez.Error.NotSupported`
        """
        await self.call(member=GattCharacteristic1Member.START_NOTIFY)

    async def stop_notify(self) -> None:
        """This method will cancel any previous StartNotify transaction.

        Note that notifications from a characteristic are shared between
        sessions thus calling StopNotify will release a single session.

        Possible Errors:
            - `org.bluez.Error.Failed`
        """
        await self.call(member=GattCharacteristic1Member.STOP_NOTIFY)

    async def get_uuid(self) -> str:
        """128-bit characteristic UUID."""
        return await self.get_property(GattCharacteristic1Property.UUID)

    async def get_service(self) -> str:
        """Object path of the GATT service the characteristic
        belongs to."""
        return await self.get_property(GattCharacteristic1Property.Service)

    async def get_value(self) -> bytearray:
        """The cached value of the characteristic. This property
        gets updated only after a successful read request and
        when a notification or indication is received, upon
        which a PropertiesChanged signal will be emitted.
        """
        return await self.get_property(GattCharacteristic1Property.Value)

    async def get_write_acquired(self) -> bool:
        """True, if this characteristic has been acquired by any
        client using AcquireWrite.

        Property is ommited in case `write-without-response` flag
        is not set.
        """
        return await self.get_property(GattCharacteristic1Property.WriteAcquired)

    async def get_notify_acquired(self) -> bool:
        """True, if this characteristic has been acquired by any
        client using AcquireNotify.

        Property is ommited in case `notify` flag is not set.
        """
        return await self.get_property(GattCharacteristic1Property.NotifyAcquired)

    async def get_notifying(self) -> bool:
        """True, if notifications or indications on this
        characteristic are currently enabled.
        """
        return await self.get_property(GattCharacteristic1Property.Notifying)

    async def get_flags(self) -> list[str]:
        """Defines how the characteristic value can be used.

        See Core spec:
            - "Table 3.5: Characteristic Properties bit field",
            - "Table 3.8: Characteristic Extended Properties bit field".

        Allowed values:
            - `broadcast`
            - `read`
            - `write-without-response`
            - `write`
            - `notify`
            - `indicate`
            - `authenticated-signed-writes`
            - `reliable-write`
            - `writable-auxiliaries`
            - `encrypt-read`
            - `encrypt-write`
            - `encrypt-authenticated-read`
            - `encrypt-authenticated-write`
            - `authorize`
        """
        return await self.get_property(
            GattCharacteristic1Property.Flags,
        )

    async def get_handle(self) -> int:
        """Characteristic handle. When available in the server it
        would attempt to use to allocate into the database
        which may fail, to auto allocate the value 0x0000
        shall be used which will cause the allocated handle to
        be set once registered."""
        return await self.get_property(GattCharacteristic1Property.Handle)

    async def get_mtu(self) -> int | None:
        """Characteristic MTU, this is valid both for ReadValue and WriteValue but either method can use long
        procedures when supported."""
        return await self.get_property(GattCharacteristic1Property.MTU)
