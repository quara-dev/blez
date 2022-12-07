from enum import Enum, IntEnum


class StandardCharacteristic(str, Enum):
    DEVICE_NAME = "00002a00-0000-1000-8000-00805f9b34fb"
    APPEARANCE = "00002a01-0000-1000-8000-00805f9b34fb"
    PERIPHERAL_PRIVACY_FLAG = "00002a02-0000-1000-8000-00805f9b34fb"
    RECONNECTION_ADDRESS = "00002a03-0000-1000-8000-00805f9b34fb"
    PERIPHERAL_PREFERRED_CONNECTION_PARAMETERS = "00002a04-0000-1000-8000-00805f9b34fb"
    SERVICE_CHANGED = "00002a05-0000-1000-8000-00805f9b34fb"
    ALERT_LEVEL = "00002a06-0000-1000-8000-00805f9b34fb"
    TX_POWER_LEVEL = "00002a07-0000-1000-8000-00805f9b34fb"
    DATE_TIME = "00002a08-0000-1000-8000-00805f9b34fb"
    DAY_OF_WEEK = "00002a09-0000-1000-8000-00805f9b34fb"
    DAY_DATE_TIME = "00002a0a-0000-1000-8000-00805f9b34fb"
    EXACT_TIME_100 = "00002a0b-0000-1000-8000-00805f9b34fb"
    EXACT_TIME_256 = "00002a0c-0000-1000-8000-00805f9b34fb"
    DST_OFFSET = "00002a0d-0000-1000-8000-00805f9b34fb"
    TIME_ZONE = "00002a0e-0000-1000-8000-00805f9b34fb"
    LOCAL_TIME_INFORMATION = "00002a0f-0000-1000-8000-00805f9b34fb"
    SECONDARY_TIME_ZONE = "00002a10-0000-1000-8000-00805f9b34fb"
    TIME_WITH_DST = "00002a11-0000-1000-8000-00805f9b34fb"
    TIME_ACCURACY = "00002a12-0000-1000-8000-00805f9b34fb"
    TIME_SOURCE = "00002a13-0000-1000-8000-00805f9b34fb"
    REFERENCE_TIME_INFORMATION = "00002a14-0000-1000-8000-00805f9b34fb"
    TIME_BROADCAST = "00002a15-0000-1000-8000-00805f9b34fb"
    TIME_UPDATE_CONTROL_POINT = "00002a16-0000-1000-8000-00805f9b34fb"
    TIME_UPDATE_STATE = "00002a17-0000-1000-8000-00805f9b34fb"
    GLUCOSE_MEASUREMENT = "00002a18-0000-1000-8000-00805f9b34fb"
    BATTERY_LEVEL = "00002a19-0000-1000-8000-00805f9b34fb"
    BATTERY_POWER_STATE = "00002a1a-0000-1000-8000-00805f9b34fb"
    BATTERY_LEVEL_STATE = "00002a1b-0000-1000-8000-00805f9b34fb"
    TEMPERATURE_MEASUREMENT = "00002a1c-0000-1000-8000-00805f9b34fb"
    TEMPERATURE_TYPE = "00002a1d-0000-1000-8000-00805f9b34fb"
    INTERMEDIATE_TEMPERATURE = "00002a1e-0000-1000-8000-00805f9b34fb"
    TEMPERATURE_CELSIUS = "00002a1f-0000-1000-8000-00805f9b34fb"
    TEMPERATURE_FAHRENHEIT = "00002a20-0000-1000-8000-00805f9b34fb"
    MEASUREMENT_INTERVAL = "00002a21-0000-1000-8000-00805f9b34fb"
    BOOT_KEYBOARD_INPUT_REPORT = "00002a22-0000-1000-8000-00805f9b34fb"
    SYSTEM_ID = "00002a23-0000-1000-8000-00805f9b34fb"
    MODEL_NUMBER_STRING = "00002a24-0000-1000-8000-00805f9b34fb"
    SERIAL_NUMBER_STRING = "00002a25-0000-1000-8000-00805f9b34fb"
    FIRMWARE_REVISION_STRING = "00002a26-0000-1000-8000-00805f9b34fb"
    HARDWARE_REVISION_STRING = "00002a27-0000-1000-8000-00805f9b34fb"
    SOFTWARE_REVISION_STRING = "00002a28-0000-1000-8000-00805f9b34fb"
    MANUFACTURER_NAME_STRING = "00002a29-0000-1000-8000-00805f9b34fb"
    IEEE_11073_20601_REGULATORY_CERTIFICATION_DATA_LIST = (
        "00002a2a-0000-1000-8000-00805f9b34fb"
    )
    CURRENT_TIME = "00002a2b-0000-1000-8000-00805f9b34fb"
    MAGNETIC_DECLINATION = "00002a2c-0000-1000-8000-00805f9b34fb"
    POSITION_2D = "00002a2f-0000-1000-8000-00805f9b34fb"
    POSITION_3D = "00002a30-0000-1000-8000-00805f9b34fb"
    SCAN_REFRESH = "00002a31-0000-1000-8000-00805f9b34fb"
    BOOT_KEYBOARD_OUTPUT_REPORT = "00002a32-0000-1000-8000-00805f9b34fb"
    BOOT_MOUSE_INPUT_REPORT = "00002a33-0000-1000-8000-00805f9b34fb"
    GLUCOSE_MEASUREMENT_CONTEXT = "00002a34-0000-1000-8000-00805f9b34fb"
    BLOOD_PRESSURE_MEASUREMENT = "00002a35-0000-1000-8000-00805f9b34fb"
    INTERMEDIATE_CUFF_PRESSURE = "00002a36-0000-1000-8000-00805f9b34fb"
    HEART_RATE_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"
    BODY_SENSOR_LOCATION = "00002a38-0000-1000-8000-00805f9b34fb"
    HEART_RATE_CONTROL_POINT = "00002a39-0000-1000-8000-00805f9b34fb"
    REMOVABLE = "00002a3a-0000-1000-8000-00805f9b34fb"
    SERVICE_REQUIRED = "00002a3b-0000-1000-8000-00805f9b34fb"
    SCIENTIFIC_TEMPERATURE_CELSIUS = "00002a3c-0000-1000-8000-00805f9b34fb"
    STRING = "00002a3d-0000-1000-8000-00805f9b34fb"
    NETWORK_AVAILABILITY = "00002a3e-0000-1000-8000-00805f9b34fb"
    ALERT_STATUS = "00002a3f-0000-1000-8000-00805f9b34fb"
    RINGER_CONTROL_POINT = "00002a40-0000-1000-8000-00805f9b34fb"
    RINGER_SETTING = "00002a41-0000-1000-8000-00805f9b34fb"
    ALERT_CATEGORY_ID_BIT_MASK = "00002a42-0000-1000-8000-00805f9b34fb"
    ALERT_CATEGORY_ID = "00002a43-0000-1000-8000-00805f9b34fb"
    ALERT_NOTIFICATION_CONTROL_POINT = "00002a44-0000-1000-8000-00805f9b34fb"
    UNREAD_ALERT_STATUS = "00002a45-0000-1000-8000-00805f9b34fb"
    NEW_ALERT = "00002a46-0000-1000-8000-00805f9b34fb"
    SUPPORTED_NEW_ALERT_CATEGORY = "00002a47-0000-1000-8000-00805f9b34fb"
    SUPPORTED_UNREAD_ALERT_CATEGORY = "00002a48-0000-1000-8000-00805f9b34fb"
    BLOOD_PRESSURE_FEATURE = "00002a49-0000-1000-8000-00805f9b34fb"
    HID_INFORMATION = "00002a4a-0000-1000-8000-00805f9b34fb"
    REPORT_MAP = "00002a4b-0000-1000-8000-00805f9b34fb"
    HID_CONTROL_POINT = "00002a4c-0000-1000-8000-00805f9b34fb"
    REPORT = "00002a4d-0000-1000-8000-00805f9b34fb"
    PROTOCOL_MODE = "00002a4e-0000-1000-8000-00805f9b34fb"
    SCAN_INTERVAL_WINDOW = "00002a4f-0000-1000-8000-00805f9b34fb"
    PNP_ID = "00002a50-0000-1000-8000-00805f9b34fb"
    GLUCOSE_FEATURE = "00002a51-0000-1000-8000-00805f9b34fb"
    RECORD_ACCESS_CONTROL_POINT = "00002a52-0000-1000-8000-00805f9b34fb"
    RSC_MEASUREMENT = "00002a53-0000-1000-8000-00805f9b34fb"
    RSC_FEATURE = "00002a54-0000-1000-8000-00805f9b34fb"
    SC_CONTROL_POINT = "00002a55-0000-1000-8000-00805f9b34fb"
    DIGITAL = "00002a56-0000-1000-8000-00805f9b34fb"
    DIGITAL_OUTPUT = "00002a57-0000-1000-8000-00805f9b34fb"
    ANALOG = "00002a58-0000-1000-8000-00805f9b34fb"
    ANALOG_OUTPUT = "00002a59-0000-1000-8000-00805f9b34fb"
    AGGREGATE = "00002a5a-0000-1000-8000-00805f9b34fb"
    CSC_MEASUREMENT = "00002a5b-0000-1000-8000-00805f9b34fb"
    CSC_FEATURE = "00002a5c-0000-1000-8000-00805f9b34fb"
    SENSOR_LOCATION = "00002a5d-0000-1000-8000-00805f9b34fb"
    PLX_SPOT_CHECK_MEASUREMENT = "00002a5e-0000-1000-8000-00805f9b34fb"
    PLX_CONTINUOUS_MEASUREMENT_CHARACTERISTIC = "00002a5f-0000-1000-8000-00805f9b34fb"
    PLX_FEATURES = "00002a60-0000-1000-8000-00805f9b34fb"
    PULSE_OXIMETRY_CONTROL_POINT = "00002a62-0000-1000-8000-00805f9b34fb"
    CYCLING_POWER_MEASUREMENT = "00002a63-0000-1000-8000-00805f9b34fb"
    CYCLING_POWER_VECTOR = "00002a64-0000-1000-8000-00805f9b34fb"
    CYCLING_POWER_FEATURE = "00002a65-0000-1000-8000-00805f9b34fb"
    CYCLING_POWER_CONTROL_POINT = "00002a66-0000-1000-8000-00805f9b34fb"
    LOCATION_AND_SPEED_CHARACTERISTIC = "00002a67-0000-1000-8000-00805f9b34fb"
    NAVIGATION = "00002a68-0000-1000-8000-00805f9b34fb"
    POSITION_QUALITY = "00002a69-0000-1000-8000-00805f9b34fb"
    LN_FEATURE = "00002a6a-0000-1000-8000-00805f9b34fb"
    LN_CONTROL_POINT = "00002a6b-0000-1000-8000-00805f9b34fb"
    ELEVATION = "00002a6c-0000-1000-8000-00805f9b34fb"
    PRESSURE = "00002a6d-0000-1000-8000-00805f9b34fb"
    TEMPERATURE = "00002a6e-0000-1000-8000-00805f9b34fb"
    HUMIDITY = "00002a6f-0000-1000-8000-00805f9b34fb"
    TRUE_WIND_SPEED = "00002a70-0000-1000-8000-00805f9b34fb"
    TRUE_WIND_DIRECTION = "00002a71-0000-1000-8000-00805f9b34fb"
    APPARENT_WIND_SPEED = "00002a72-0000-1000-8000-00805f9b34fb"
    APPARENT_WIND_DIRECTION = "00002a73-0000-1000-8000-00805f9b34fb"
    GUST_FACTOR = "00002a74-0000-1000-8000-00805f9b34fb"
    POLLEN_CONCENTRATION = "00002a75-0000-1000-8000-00805f9b34fb"
    UV_INDEX = "00002a76-0000-1000-8000-00805f9b34fb"
    IRRADIANCE = "00002a77-0000-1000-8000-00805f9b34fb"
    RAINFALL = "00002a78-0000-1000-8000-00805f9b34fb"
    WIND_CHILL = "00002a79-0000-1000-8000-00805f9b34fb"
    HEAT_INDEX = "00002a7a-0000-1000-8000-00805f9b34fb"
    DEW_POINT = "00002a7b-0000-1000-8000-00805f9b34fb"
    DESCRIPTOR_VALUE_CHANGED = "00002a7d-0000-1000-8000-00805f9b34fb"
    AEROBIC_HEART_RATE_LOWER_LIMIT = "00002a7e-0000-1000-8000-00805f9b34fb"
    AEROBIC_THRESHOLD = "00002a7f-0000-1000-8000-00805f9b34fb"
    AGE = "00002a80-0000-1000-8000-00805f9b34fb"
    ANAEROBIC_HEART_RATE_LOWER_LIMIT = "00002a81-0000-1000-8000-00805f9b34fb"
    ANAEROBIC_HEART_RATE_UPPER_LIMIT = "00002a82-0000-1000-8000-00805f9b34fb"
    ANAEROBIC_THRESHOLD = "00002a83-0000-1000-8000-00805f9b34fb"
    AEROBIC_HEART_RATE_UPPER_LIMIT = "00002a84-0000-1000-8000-00805f9b34fb"
    DATE_OF_BIRTH = "00002a85-0000-1000-8000-00805f9b34fb"
    DATE_OF_THRESHOLD_ASSESSMENT = "00002a86-0000-1000-8000-00805f9b34fb"
    EMAIL_ADDRESS = "00002a87-0000-1000-8000-00805f9b34fb"
    FAT_BURN_HEART_RATE_LOWER_LIMIT = "00002a88-0000-1000-8000-00805f9b34fb"
    FAT_BURN_HEART_RATE_UPPER_LIMIT = "00002a89-0000-1000-8000-00805f9b34fb"
    FIRST_NAME = "00002a8a-0000-1000-8000-00805f9b34fb"
    FIVE_ZONE_HEART_RATE_LIMITS = "00002a8b-0000-1000-8000-00805f9b34fb"
    GENDER = "00002a8c-0000-1000-8000-00805f9b34fb"
    HEART_RATE_MAX = "00002a8d-0000-1000-8000-00805f9b34fb"
    HEIGHT = "00002a8e-0000-1000-8000-00805f9b34fb"
    HIP_CIRCUMFERENCE = "00002a8f-0000-1000-8000-00805f9b34fb"
    LAST_NAME = "00002a90-0000-1000-8000-00805f9b34fb"
    MAXIMUM_RECOMMENDED_HEART_RATE = "00002a91-0000-1000-8000-00805f9b34fb"
    RESTING_HEART_RATE = "00002a92-0000-1000-8000-00805f9b34fb"
    SPORT_TYPE_FOR_AEROBIC_AND_ANAEROBIC_THRESHOLDS = (
        "00002a93-0000-1000-8000-00805f9b34fb"
    )
    THREE_ZONE_HEART_RATE_LIMITS = "00002a94-0000-1000-8000-00805f9b34fb"
    TWO_ZONE_HEART_RATE_LIMIT = "00002a95-0000-1000-8000-00805f9b34fb"
    VO2_MAX = "00002a96-0000-1000-8000-00805f9b34fb"
    WAIST_CIRCUMFERENCE = "00002a97-0000-1000-8000-00805f9b34fb"
    WEIGHT = "00002a98-0000-1000-8000-00805f9b34fb"
    DATABASE_CHANGE_INCREMENT = "00002a99-0000-1000-8000-00805f9b34fb"
    USER_INDEX = "00002a9a-0000-1000-8000-00805f9b34fb"
    BODY_COMPOSITION_FEATURE = "00002a9b-0000-1000-8000-00805f9b34fb"
    BODY_COMPOSITION_MEASUREMENT = "00002a9c-0000-1000-8000-00805f9b34fb"
    WEIGHT_MEASUREMENT = "00002a9d-0000-1000-8000-00805f9b34fb"
    WEIGHT_SCALE_FEATURE = "00002a9e-0000-1000-8000-00805f9b34fb"
    USER_CONTROL_POINT = "00002a9f-0000-1000-8000-00805f9b34fb"
    MAGNETIC_FLUX_DENSITY_2D = "00002aa0-0000-1000-8000-00805f9b34fb"
    MAGNETIC_FLUX_DENSITY_3D = "00002aa1-0000-1000-8000-00805f9b34fb"
    LANGUAGE = "00002aa2-0000-1000-8000-00805f9b34fb"
    BAROMETRIC_PRESSURE_TREND = "00002aa3-0000-1000-8000-00805f9b34fb"
    BOND_MANAGEMENT_CONTROL_POINT = "00002aa4-0000-1000-8000-00805f9b34fb"
    BOND_MANAGEMENT_FEATURES = "00002aa5-0000-1000-8000-00805f9b34fb"
    CENTRAL_ADDRESS_RESOLUTION = "00002aa6-0000-1000-8000-00805f9b34fb"
    CGM_MEASUREMENT = "00002aa7-0000-1000-8000-00805f9b34fb"
    CGM_FEATURE = "00002aa8-0000-1000-8000-00805f9b34fb"
    CGM_STATUS = "00002aa9-0000-1000-8000-00805f9b34fb"
    CGM_SESSION_START_TIME = "00002aaa-0000-1000-8000-00805f9b34fb"
    CGM_SESSION_RUN_TIME = "00002aab-0000-1000-8000-00805f9b34fb"
    CGM_SPECIFIC_OPS_CONTROL_POINT = "00002aac-0000-1000-8000-00805f9b34fb"
    INDOOR_POSITIONING_CONFIGURATION = "00002aad-0000-1000-8000-00805f9b34fb"
    LATITUDE = "00002aae-0000-1000-8000-00805f9b34fb"
    LONGITUDE = "00002aaf-0000-1000-8000-00805f9b34fb"
    LOCAL_NORTH_COORDINATE = "00002ab0-0000-1000-8000-00805f9b34fb"
    LOCAL_EAST_COORDINATE = "00002ab1-0000-1000-8000-00805f9b34fb"
    FLOOR_NUMBER = "00002ab2-0000-1000-8000-00805f9b34fb"
    ALTITUDE = "00002ab3-0000-1000-8000-00805f9b34fb"
    UNCERTAINTY = "00002ab4-0000-1000-8000-00805f9b34fb"
    LOCATION_NAME = "00002ab5-0000-1000-8000-00805f9b34fb"
    URI = "00002ab6-0000-1000-8000-00805f9b34fb"
    HTTP_HEADERS = "00002ab7-0000-1000-8000-00805f9b34fb"
    HTTP_STATUS_CODE = "00002ab8-0000-1000-8000-00805f9b34fb"
    HTTP_ENTITY_BODY = "00002ab9-0000-1000-8000-00805f9b34fb"
    HTTP_CONTROL_POINT = "00002aba-0000-1000-8000-00805f9b34fb"
    HTTPS_SECURITY = "00002abb-0000-1000-8000-00805f9b34fb"
    TDS_CONTROL_POINT = "00002abc-0000-1000-8000-00805f9b34fb"
    OTS_FEATURE = "00002abd-0000-1000-8000-00805f9b34fb"
    OBJECT_NAME = "00002abe-0000-1000-8000-00805f9b34fb"
    OBJECT_TYPE = "00002abf-0000-1000-8000-00805f9b34fb"
    OBJECT_SIZE = "00002ac0-0000-1000-8000-00805f9b34fb"
    OBJECT_FIRST_CREATED = "00002ac1-0000-1000-8000-00805f9b34fb"
    OBJECT_LAST_MODIFIED = "00002ac2-0000-1000-8000-00805f9b34fb"
    OBJECT_ID = "00002ac3-0000-1000-8000-00805f9b34fb"
    OBJECT_PROPERTIES = "00002ac4-0000-1000-8000-00805f9b34fb"
    OBJECT_ACTION_CONTROL_POINT = "00002ac5-0000-1000-8000-00805f9b34fb"
    OBJECT_LIST_CONTROL_POINT = "00002ac6-0000-1000-8000-00805f9b34fb"
    OBJECT_LIST_FILTER = "00002ac7-0000-1000-8000-00805f9b34fb"
    OBJECT_CHANGED = "00002ac8-0000-1000-8000-00805f9b34fb"
    RESOLVABLE_PRIVATE_ADDRESS_ONLY = "00002ac9-0000-1000-8000-00805f9b34fb"
    FITNESS_MACHINE_FEATURE = "00002acc-0000-1000-8000-00805f9b34fb"
    TREADMILL_DATA = "00002acd-0000-1000-8000-00805f9b34fb"
    CROSS_TRAINER_DATA = "00002ace-0000-1000-8000-00805f9b34fb"
    STEP_CLIMBER_DATA = "00002acf-0000-1000-8000-00805f9b34fb"
    STAIR_CLIMBER_DATA = "00002ad0-0000-1000-8000-00805f9b34fb"
    ROWER_DATA = "00002ad1-0000-1000-8000-00805f9b34fb"
    INDOOR_BIKE_DATA = "00002ad2-0000-1000-8000-00805f9b34fb"
    TRAINING_STATUS = "00002ad3-0000-1000-8000-00805f9b34fb"
    SUPPORTED_SPEED_RANGE = "00002ad4-0000-1000-8000-00805f9b34fb"
    SUPPORTED_INCLINATION_RANGE = "00002ad5-0000-1000-8000-00805f9b34fb"
    SUPPORTED_RESISTANCE_LEVEL_RANGE = "00002ad6-0000-1000-8000-00805f9b34fb"
    SUPPORTED_HEART_RATE_RANGE = "00002ad7-0000-1000-8000-00805f9b34fb"
    SUPPORTED_POWER_RANGE = "00002ad8-0000-1000-8000-00805f9b34fb"
    FITNESS_MACHINE_CONTROL_POINT = "00002ad9-0000-1000-8000-00805f9b34fb"
    FITNESS_MACHINE_STATUS = "00002ada-0000-1000-8000-00805f9b34fb"
    DATE_UTC = "00002aed-0000-1000-8000-00805f9b34fb"
    RC_FEATURE = "00002b1d-0000-1000-8000-00805f9b34fb"
    RC_SETTINGS = "00002b1e-0000-1000-8000-00805f9b34fb"
    RECONNECTION_CONFIGURATION_CONTROL_POINT = "00002b1f-0000-1000-8000-00805f9b34fb"


class AdvertisementDataType(IntEnum):
    """
    Generic Access Profile advertisement data types.
    `Source <https://btprodspecificationrefs.blob.core.windows.net/assigned-numbers/Assigned%20Number%20Types/Generic%20Access%20Profile.pdf>`.
    .. versionadded:: 0.15.0
    """

    FLAGS = 0x01
    INCOMPLETE_LIST_SERVICE_UUID16 = 0x02
    COMPLETE_LIST_SERVICE_UUID16 = 0x03
    INCOMPLETE_LIST_SERVICE_UUID32 = 0x04
    COMPLETE_LIST_SERVICE_UUID32 = 0x05
    INCOMPLETE_LIST_SERVICE_UUID128 = 0x06
    COMPLETE_LIST_SERVICE_UUID128 = 0x07
    SHORTENED_LOCAL_NAME = 0x08
    COMPLETE_LOCAL_NAME = 0x09
    TX_POWER_LEVEL = 0x0A
    CLASS_OF_DEVICE = 0x0D

    SERVICE_DATA_UUID16 = 0x16
    SERVICE_DATA_UUID32 = 0x20
    SERVICE_DATA_UUID128 = 0x21

    MANUFACTURER_SPECIFIC_DATA = 0xFF
