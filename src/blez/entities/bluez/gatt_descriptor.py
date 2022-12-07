from __future__ import annotations

from enum import Enum

from ..dbus.interface import Interface

GATT_DESCRIPTOR_INTERFACE = "org.bluez.GattDescriptor1"


class GattDescriptor1Property(str, Enum):
    UUID = "UUID"
    CHARACTERISTIC = "Characteristic"
    VALUE = "Value"
    FLAGS = "Flags"
    HANDLE = "Handle"


class GattDescriptor1Member(str, Enum):
    READ_VALUE = "ReadValue"
    WRITE_VALUE = "WriteValue"


class GattDescriptor1Signature(str, Enum):
    READ_VALUE = "a{sv}"
    WRITE_VALUE = "aya{sv}"


class GattDescriptor1MemberOption(str, Enum):
    OFFSET = "offset"
    PREPARE_AUTHORIZE = "prepare-authorize"


class BluezGattDescriptor(Interface, name=GATT_DESCRIPTOR_INTERFACE):
    @property
    def uuid(self) -> str:
        return self.cached_properties[GattDescriptor1Property.UUID]

    @property
    def characteristic(self) -> str:
        return self.cached_properties[GattDescriptor1Property.CHARACTERISTIC]

    @property
    def value(self) -> bytearray | None:
        return self.cached_properties.get(GattDescriptor1Property.VALUE, None)

    @property
    def flags(self) -> list[str]:
        return self.cached_properties[GattDescriptor1Property.FLAGS]

    @property
    def handle(self) -> int | None:
        return self.cached_properties.get(GattDescriptor1Property.HANDLE, None)

    async def read_value(self, offset: int | None = None) -> bytearray:
        """Issues a request to read the value of the
        characteristic and returns the value if the
        operation was successful.

        Possible Errors:
            - `org.bluez.Error.Failed`
            - `org.bluez.Error.InProgress`
            - `org.bluez.Error.NotPermitted`
            - `org.bluez.Error.NotAuthorized`
            - `org.bluez.Error.NotSupported`
        """
        # Fetch codec from client
        codec = self.service.client.codec
        # Build options
        options = {}
        if offset is not None:
            options[GattDescriptor1MemberOption.OFFSET] = codec.encode("n", offset)
        # Send message
        reply = await self.call(
            member=GattDescriptor1Member.READ_VALUE,
            signature=GattDescriptor1Signature.READ_VALUE,
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
        """Issues a request to write the value of the characteristic.

        Possible Errors:
            - `org.bluez.Error.Failed`
            - `org.bluez.Error.InProgress`
            - `org.bluez.Error.NotPermitted`
            - `org.bluez.Error.InvalidValueLength`
            - `org.bluez.Error.NotAuthorized`
            - `org.bluez.Error.NotSupported`
        """
        # Fetch codec from client
        codec = self.service.client.codec
        # Convert payload to bytes
        payload = bytes(value)
        # Initialize options
        options = {}
        # Include options
        if offset is not None:
            options[GattDescriptor1MemberOption.OFFSET] = codec.encode("n", offset)
        if prepare_authorize is not None:
            options[GattDescriptor1MemberOption.PREPARE_AUTHORIZE] = codec.encode(
                "b", prepare_authorize
            )
        # Send message
        await self.call(
            member=GattDescriptor1Member.WRITE_VALUE,
            signature=GattDescriptor1Signature.WRITE_VALUE,
            body=[payload, options],
        )
        # Return number of bytes written
        return len(payload)

    async def get_uuid(self) -> str:
        """128-bit service UUID."""
        return await self.get_property(GattDescriptor1Property.UUID)

    async def get_characteristic(self) -> str:
        """Object path of the GATT characteristic the descriptor belongs to."""
        return await self.get_property(GattDescriptor1Property.CHARACTERISTIC)

    async def get_value(self) -> bytearray:
        """The cached value of the descriptor.

        This property gets updated only after a successful
        read request, upon which a PropertiesChanged signal will be emitted.
        """
        return await self.get_property(GattDescriptor1Property.VALUE)

    async def get_flags(self) -> list[str]:
        """Defines how the descriptor value can be used.

        See Core spec:
            - "Table 3.5: Characteristic Properties bit field",
            - "Table 3.8: Characteristic Extended Properties bit field".

        Allowed values:
            - `read`
            - `write`
            - `encrypt-read`
            - `encrypt-write`
            - `encrypt-authenticated-read`
            - `encrypt-authenticated-write`
            - `authorize`
        """
        return await self.get_property(GattDescriptor1Property.FLAGS)

    async def get_handle(self) -> int:
        return await self.get_property(GattDescriptor1Property.HANDLE)
