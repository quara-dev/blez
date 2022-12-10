from .events import (
    DeviceEventFamily,
    DeviceEventType,
    StationEventFamily,
    StationEventType,
)
from .queries import HubQueryType, StationQueryType
from .requests import DeviceRequestType, StationRequestType

DEFAULT_PREFIX = "{IOT_PREFIX}"


SERVICE_SUBJECTS = {
    # Device requests
    DeviceRequestType.RESET: "{IOT_PREFIX}.{account}.{user}.DEVICE.{device}.RESET",
    DeviceRequestType.DISCONNECT: "{IOT_PREFIX}.{account}.{user}.DEVICE.{device}.DISCONNECT",
    DeviceRequestType.READ_VALUE: "{IOT_PREFIX}.{account}.{user}.DEVICE.{device}.READ_VALUE",
    DeviceRequestType.WRITE_VALUE: "{IOT_PREFIX}.{account}.{user}.DEVICE.{device}.WRITE_VALUE",
    DeviceRequestType.SET_TIME: "{IOT_PREFIX}.{account}.{user}.DEVICE.{device}.SET_TIME",
    DeviceRequestType.SYNC_TIME: "{IOT_PREFIX}.{account}.{user}.DEVICE.{device}.SYNC_TIME",
    DeviceRequestType.START_NOTIFY: "{IOT_PREFIX}.{account}.{user}.DEVICE.{device}.START_NOTIFY",
    DeviceRequestType.STOP_NOTIFY: "{IOT_PREFIX}.{account}.{user}.DEVICE.{device}.STOP_NOTIFY",
    # Station requests
    StationRequestType.START: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.START",
    StationRequestType.STOP: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.STOP",
    StationRequestType.START_DISCOVERY: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.START_DISCOVERY",
    StationRequestType.STOP_DISCOVERY: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.STOP_DISCOVERY",
    StationRequestType.ENABLE_DISCOVERY: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.ENABLE_DISCOVERY",
    StationRequestType.DISABLE_DISCOVERY: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.DISABLE_DISCOVERY",
    StationRequestType.CONNECT: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.CONNECT",
    StationRequestType.DISCONNECT: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.DISCONNECT",
    # Hub queries
    HubQueryType.FIND_DEVICES: "{IOT_PREFIX}.{account}.{user}.DEVICES.FIND",
    HubQueryType.FIND_STATIONS: "{IOT_PREFIX}.{account}.{user}.STATIONS.FIND",
    HubQueryType.GET_DEVICE: "{IOT_PREFIX}.{account}.{user}.DEVICES.GET.{device}",
    HubQueryType.GET_STATION: "{IOT_PREFIX}.{account}.{user}.STATIONS.GET.{station}",
    HubQueryType.LIST_DEVICES: "{IOT_PREFIX}.{account}.{user}.DEVICES.LIST",
    HubQueryType.LIST_STATIONS: "{IOT_PREFIX}.{account}.{user}.STATIONS.LIST",
    # Station queries
    StationQueryType.GET_CONNECTED_DEVICES: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.GET_CONNECTED",
    StationQueryType.GET_DISCOVERED_DEVICES: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.GET_DISCOVERED",
    StationQueryType.LIST_CONNECTED_DEVICES: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.LIST_CONNECTED",
    StationQueryType.LIST_DISCOVERED_DEVICES: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.LIST_DISCOVERED",
    StationQueryType.GET_DEVICE_CHARS: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.GET_DEVICE_CHARS",
    StationQueryType.GET_DEVICE_PROPS: "{IOT_PREFIX}.{account}.{user}.STATION.{station}.GET_DEVICE_PROPS",
    # Device Event Families
    DeviceEventFamily.ALL: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.>",
    DeviceEventFamily.CONNECTION: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.*",
    DeviceEventFamily.TIME_SYNCHRONISATION: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.TIME.*",
    DeviceEventFamily.NOTIFICATION: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.NOTIFY.{characteristic}.*",
    # Device events
    DeviceEventType.DISCONNECTED: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.DISCONNECTED",
    DeviceEventType.CONNECTED: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.CONNECTED",
    DeviceEventType.NOTIFIED: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.NOTIFY.{characteristic}.NOTIFIED",
    DeviceEventType.NOTIFY_STARTED: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.NOTIFY.{characteristic}.STARTED",
    DeviceEventType.NOTIFY_STOPPED: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.NOTIFY.{characteristic}.STOPPED",
    DeviceEventType.TIME_SET: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.TIME.SET",
    DeviceEventType.TIME_SYNCED: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.TIME.SYNCED",
    DeviceEventType.PROPS_CHANGED: "{IOT_PREFIX}.{account}.{user}.EVENTS.DEVICE.{device}.PROPS.CHANGED",
    # Station Event families
    StationEventFamily.ALL: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.>",
    StationEventFamily.DEVICE: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.DEVICE.*",
    StationEventFamily.DISCOVERY: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.DISCOVERY.*",
    StationEventFamily.PROPS: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.PROPS.*",
    StationEventFamily.LIFECYCLE: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.LIFECYCLE.*",
    # Station Events
    StationEventType.DEVICE_CONNECTED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.DEVICE.CONNECTED",
    StationEventType.DEVICE_DISCONNECTED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.DEVICE.DISCONNECTED",
    StationEventType.DEVICE_DISCOVERED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.DEVICE.DISCOVERED",
    StationEventType.DISCOVERY_STARTED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.DISCOVERY.STARTED",
    StationEventType.DISCOVERY_STOPPED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.DISCOVERY.STOPPED",
    StationEventType.DISCOVERY_ENABLED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.DISCOVERY.ENABLED",
    StationEventType.DISCOVERY_DISABLED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.DISCOVERY.DISABLED",
    StationEventType.PROPS_CHANGED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.PROPS.CHANGED",
    StationEventType.STARTED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.LIFECYCLE.STARTED",
    StationEventType.STOPPED: "{IOT_PREFIX}.{account}.{user}.EVENTS.STATION.{station}.LIFECYCLE.STOPPED",
}


CLIENT_SUBJECTS = {
    # Device requests
    DeviceRequestType.RESET: "{IOT_PREFIX}.DEVICE.{device}.RESET",
    DeviceRequestType.DISCONNECT: "{IOT_PREFIX}.DEVICE.{device}.DISCONNECT",
    DeviceRequestType.READ_VALUE: "{IOT_PREFIX}.DEVICE.{device}.READ_VALUE",
    DeviceRequestType.WRITE_VALUE: "{IOT_PREFIX}.DEVICE.{device}.WRITE_VALUE",
    DeviceRequestType.SET_TIME: "{IOT_PREFIX}.DEVICE.{device}.SET_TIME",
    DeviceRequestType.SYNC_TIME: "{IOT_PREFIX}.DEVICE.{device}.SYNC_TIME",
    DeviceRequestType.START_NOTIFY: "{IOT_PREFIX}.DEVICE.{device}.START_NOTIFY",
    DeviceRequestType.STOP_NOTIFY: "{IOT_PREFIX}.DEVICE.{device}.STOP_NOTIFY",
    # Station requests
    StationRequestType.START: "{IOT_PREFIX}.STATION.{station}.START",
    StationRequestType.STOP: "{IOT_PREFIX}.STATION.{station}.STOP",
    StationRequestType.START_DISCOVERY: "{IOT_PREFIX}.STATION.{station}.START_DISCOVERY",
    StationRequestType.STOP_DISCOVERY: "{IOT_PREFIX}.STATION.{station}.STOP_DISCOVERY",
    StationRequestType.ENABLE_DISCOVERY: "{IOT_PREFIX}.STATION.{station}.ENABLE_DISCOVERY",
    StationRequestType.DISABLE_DISCOVERY: "{IOT_PREFIX}.STATION.{station}.DISABLE_DISCOVERY",
    StationRequestType.CONNECT: "{IOT_PREFIX}.STATION.{station}.CONNECT",
    StationRequestType.DISCONNECT: "{IOT_PREFIX}.STATION.{station}.DISCONNECT",
    # Hub queries
    HubQueryType.FIND_DEVICES: "{IOT_PREFIX}.DEVICES.FIND",
    HubQueryType.FIND_STATIONS: "{IOT_PREFIX}.STATIONS.FIND",
    HubQueryType.GET_DEVICE: "{IOT_PREFIX}.DEVICES.GET.{device}",
    HubQueryType.GET_STATION: "{IOT_PREFIX}.STATIONS.GET.{station}",
    HubQueryType.LIST_DEVICES: "{IOT_PREFIX}.DEVICES.LIST",
    HubQueryType.LIST_STATIONS: "{IOT_PREFIX}.STATIONS.LIST",
    # Station queries
    StationQueryType.GET_CONNECTED_DEVICES: "{IOT_PREFIX}.STATION.{station}.GET_CONNECTED",
    StationQueryType.GET_DISCOVERED_DEVICES: "{IOT_PREFIX}.STATION.{station}.GET_DISCOVERED",
    StationQueryType.LIST_CONNECTED_DEVICES: "{IOT_PREFIX}.STATION.{station}.LIST_CONNECTED",
    StationQueryType.LIST_DISCOVERED_DEVICES: "{IOT_PREFIX}.STATION.{station}.LIST_DISCOVERED",
    StationQueryType.GET_DEVICE_CHARS: "{IOT_PREFIX}.STATION.{station}.GET_DEVICE_CHARS",
    StationQueryType.GET_DEVICE_PROPS: "{IOT_PREFIX}.STATION.{station}.GET_DEVICE_PROPS",
    # Device Event Families
    DeviceEventFamily.ALL: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.>",
    DeviceEventFamily.CONNECTION: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.*",
    DeviceEventFamily.TIME_SYNCHRONISATION: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.TIME.*",
    DeviceEventFamily.NOTIFICATION: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.NOTIFY.{characteristic}.*",
    # Device events
    DeviceEventType.DISCONNECTED: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.DISCONNECTED",
    DeviceEventType.CONNECTED: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.CONNECTED",
    DeviceEventType.NOTIFIED: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.NOTIFY.{characteristic}.NOTIFIED",
    DeviceEventType.NOTIFY_STARTED: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.NOTIFY.{characteristic}.STARTED",
    DeviceEventType.NOTIFY_STOPPED: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.NOTIFY.{characteristic}.STOPPED",
    DeviceEventType.TIME_SET: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.TIME.SET",
    DeviceEventType.TIME_SYNCED: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.TIME.SYNCED",
    DeviceEventType.PROPS_CHANGED: "{IOT_PREFIX}.EVENTS.DEVICE.{device}.PROPS.CHANGED",
    # Station Event families
    StationEventFamily.ALL: "{IOT_PREFIX}.EVENTS.STATION.{station}.>",
    StationEventFamily.DEVICE: "{IOT_PREFIX}.EVENTS.STATION.{station}.DEVICE.*",
    StationEventFamily.DISCOVERY: "{IOT_PREFIX}.EVENTS.STATION.{station}.DISCOVERY.*",
    StationEventFamily.PROPS: "{IOT_PREFIX}.EVENTS.STATION.{station}.PROPS.*",
    StationEventFamily.LIFECYCLE: "{IOT_PREFIX}.EVENTS.STATION.{station}.LIFECYCLE.*",
    # Station Events
    StationEventType.DEVICE_CONNECTED: "{IOT_PREFIX}.EVENTS.STATION.{station}.DEVICE.CONNECTED",
    StationEventType.DEVICE_DISCONNECTED: "{IOT_PREFIX}.EVENTS.STATION.{station}.DEVICE.DISCONNECTED",
    StationEventType.DEVICE_DISCOVERED: "{IOT_PREFIX}.EVENTS.STATION.{station}.DEVICE.DISCOVERED",
    StationEventType.DISCOVERY_STARTED: "{IOT_PREFIX}.EVENTS.STATION.{station}.DISCOVERY.STARTED",
    StationEventType.DISCOVERY_STOPPED: "{IOT_PREFIX}.EVENTS.STATION.{station}.DISCOVERY.STOPPED",
    StationEventType.DISCOVERY_ENABLED: "{IOT_PREFIX}.EVENTS.STATION.{station}.DISCOVERY.ENABLED",
    StationEventType.DISCOVERY_DISABLED: "{IOT_PREFIX}.EVENTS.STATION.{station}.DISCOVERY.DISABLED",
    StationEventType.PROPS_CHANGED: "{IOT_PREFIX}.EVENTS.STATION.{station}.PROPS.CHANGED",
    StationEventType.STARTED: "{IOT_PREFIX}.EVENTS.STATION.{station}.LIFECYCLE.STARTED",
    StationEventType.STOPPED: "{IOT_PREFIX}.EVENTS.STATION.{station}.LIFECYCLE.STOPPED",
}
