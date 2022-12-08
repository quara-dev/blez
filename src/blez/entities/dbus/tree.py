from __future__ import annotations

from typing import Any, TypeVar

TreeT = TypeVar("TreeT", bound="Tree")


class Tree:
    def __init__(
        self,
        initial_state: dict[str, dict[str, dict[str, Any]]] | None = None,
    ) -> None:
        """Create a new instance of DBusTreeState."""
        self.objects: dict[str, dict[str, dict[str, Any]]] = initial_state or {}

    def copy(
        self: TreeT, update: dict[str, dict[str, dict[str, Any]]] | None = None
    ) -> TreeT:
        """Copy a DBusTreeState"""
        new_state = self.__class__(self.objects.copy())
        if update:
            for object_path, interfaces in update.items():
                new_state.update_object(object_path, interfaces)
        return new_state

    def list_objects(self) -> list[str]:
        """List all object paths in state"""
        return list(self.objects)

    def list_interfaces(self, object_path: str) -> list[str]:
        """List all interfaces of a single object"""
        return list(self.get_object(object_path))

    def list_properties(self, object_path: str, interface: str) -> list[str]:
        """List all properties of a single object interface"""
        return list(self.get_interface(object_path, interface))

    def get_all_objects(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Get all interfaces properties for all objects.

        Example:
        >>> get_all_objects()
        {
            "/org/bluez/hci0": {
                "org.bluez.Adapter1": {
                    "Address": "XX:XX:XX:XX",
                    ...
                },
                ...
            },
            ...
        }
        """
        return self.objects.copy()

    def get_all_interfaces(
        self, interface: str, prefix: str | None = None
    ) -> dict[str, dict[str, Any]]:
        """Get all interface properties for a single type of interface.

        Example:
        >>> get_all_interfaces("org.bluez.Adapter1")
        {
            "/org/bluez/hci0": {
                "Address": ...,
                ...
            },
            "org/bluez/hci1": {
                "Address": ...,
                ...
            },
            ...
        }
        """
        instances: dict[str, dict[str, Any]] = {}
        for path, interfaces in self.objects.items():
            if prefix:
                if not path.startswith(prefix):
                    continue
            if interface in interfaces:
                instances[path] = interfaces[interface]
        return instances

    def get_object(self, object_path: str) -> dict[str, dict[str, Any]]:
        """Get all interfaces properties for object.

        Returns:
            A dict of interfaces names and interfaces properties.
            Interface properties are dict of property names and property values.

        Example:
        >>> get_object("/org/bluez/hci0")
        {
            "org.bluez.Adapter1": {
                "Address": "XX:XX:XX:XX",
                ...
            },
            ...
        }

        Raises:
            - `KeyError`: When path is not known
        """
        return self.objects[object_path]

    def get_interface(self, object_path: str, interface: str) -> dict[str, Any]:
        """Get all properties for a single object interface.

        Returns:
            A dict of property names and property values

        Example:
        >>> get_interface("/org/bluez/hci0", "org.bluez.Adapter1")
        {
            "Address": "XX:XX:XX:XX",
            ...
        }

        Raises:
            - `KeyError`: When path is not known or interface is not known
        """
        return self.objects[object_path][interface]

    def get_property(self, object_path: str, interface: str, key: str) -> Any:
        """Get a single property value on an object interface

        Returns:
            Value of property

        Example:
        >>> get_property("/org/bluez/hci0", "org.bluez.Adapter1", "Address")
        Any("s", "XX:XX:XX:XX")

        Raises:
            - `KeyError`: When path, interface or key is not known
        """
        return self.objects[object_path][interface][key]

    def remove_object(self, object_path: str) -> None:
        """Remove all interfaces from an object in the state"""
        self.objects.pop(object_path, None)

    def remove_interface(self, object_path: str, interface: str) -> None:
        """Remove an interface from an object"""
        obj = self.objects.get(object_path, {})
        obj.pop(interface, None)
        if not obj:
            self.objects.pop(object_path, None)

    def remove_property(self, object_path: str, interface: str, key: str) -> None:
        props = self.objects.get(object_path, {}).get(interface, {})
        if key in props:
            props.pop(key)

    def set_object(
        self, object_path: str, interfaces_properties: dict[str, dict[str, Any]]
    ) -> None:
        """Set multiple interfaces properties on an object"""
        self.objects[object_path] = interfaces_properties

    def set_interface(
        self, object_path: str, interface: str, properties: dict[str, Any]
    ) -> None:
        """Set single interface properties on an object"""
        if object_path in self.objects:
            self.objects[object_path][interface] = properties
        else:
            self.objects[object_path] = {interface: properties}

    def set_property(
        self, object_path: str, interface: str, key: str, value: Any
    ) -> None:
        """Set a single property value on an object interface"""
        # If interface is not known or object is not known
        if interface not in self.objects.get(object_path, {}):
            return self.set_interface(object_path, interface, {key: value})
        # If both object and interface are known
        self.objects[object_path][interface][key] = value

    def update(self, state: dict[str, dict[str, dict[str, Any]]]) -> None:
        """Update state"""
        for object_path, interface_props in state.items():
            self.update_object(object_path, interface_props)

    def update_object(
        self, path: str, interfaces_changed_props: dict[str, dict[str, Any]]
    ) -> None:
        """Update a single object in state"""
        for interface, changed_props in interfaces_changed_props.items():
            self.update_interface(path, interface, changed_props)

    def update_interface(
        self,
        path: str,
        interface: str,
        changed_props: dict[str, Any],
        invalidated_props: list[str] | None = None,
    ) -> None:
        """Update a single interface in state"""
        if invalidated_props:
            for prop in invalidated_props:
                self.remove_property(path, interface, prop)
        for key, value in changed_props.items():
            self.set_property(path, interface, key, value)
