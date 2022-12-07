from __future__ import annotations

from typing import Any

from blez.tree import DBusTree


def test_dbus_tree(bluez_data: dict[str, dict[str, dict[str, Any]]]) -> None:
    state = DBusTree(bluez_data)
    assert state.get_object("/org/bluez") == {
        "org.bluez.AgentManager1": {},
        "org.bluez.ProfileManager1": {},
        "org.freedesktop.DBus.Introspectable": {},
    }
    assert state.get_interface("/org/bluez", "org.bluez.AgentManager1") == {}
    assert state.get_all_interfaces("org.bluez.AgentManager1") == {"/org/bluez": {}}
