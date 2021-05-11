"""Define Eufy Security constants."""
from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    PERCENTAGE,
    TEMP_CELSIUS,
)
from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_LIGHT,
)

from eufy_security.types import ParamType

DOMAIN = "eufy_security"
PLATFORMS = ["sensor", "binary_sensor", "camera", "alarm_control_panel"]
MANUFACTURER = "Eufy Security"

DATA_API = "api"
DATA_LISTENER = "listener"
DATA_COORDINATOR = "coordinator"

ATTR_SERIAL = "serial_number"
ATTR_STATION_SERIAL = "station_serial"
ATTR_SOFTWARE_VERSION = "software_version"
ATTR_HARDWARE_VERSION = "hardware_version"

DEFAULT_ATTRIBUTION = "Data provided by Eufy Security"

PARAM_TYPES = [
    ParamType.BATTERY_LEVEL,
    ParamType.BATTERY_TEMP,
    ParamType.CAMERA_WIFI_RSSI,
    ParamType.SUB1G_RSSI,
    ParamType.REPEATER_RSSI,
    ParamType.CAMERA_SPEAKER_VOLUME,
    ParamType.FLOODLIGHT_MANUAL_BRIGHTNESS,
    ParamType.LIVEVIEW_LED_SWITCH,
    ParamType.DEV_LED_SWITCH,
    ParamType.SENSOR_CHIRP_VOLUME,
]

PARAM_TYPE_DEVICE_CLASS = {
    ParamType.BATTERY_LEVEL: DEVICE_CLASS_BATTERY,
    ParamType.BATTERY_TEMP: DEVICE_CLASS_TEMPERATURE,
    ParamType.CAMERA_WIFI_RSSI: DEVICE_CLASS_SIGNAL_STRENGTH,
    ParamType.SUB1G_RSSI: DEVICE_CLASS_SIGNAL_STRENGTH,
    ParamType.REPEATER_RSSI: DEVICE_CLASS_SIGNAL_STRENGTH,
    ParamType.LIVEVIEW_LED_SWITCH: DEVICE_CLASS_LIGHT,
    ParamType.DEV_LED_SWITCH: DEVICE_CLASS_LIGHT,
    ParamType.SENSOR_STATUS: DEVICE_CLASS_DOOR,
}

PARAM_TYPE_UNIT_OF_MEASUREMENT = {
    ParamType.BATTERY_LEVEL: PERCENTAGE,
    ParamType.BATTERY_TEMP: TEMP_CELSIUS,
    ParamType.CAMERA_WIFI_RSSI: SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    ParamType.SUB1G_RSSI: SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    ParamType.REPEATER_RSSI: SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    ParamType.CAMERA_SPEAKER_VOLUME: PERCENTAGE,
    ParamType.FLOODLIGHT_MANUAL_BRIGHTNESS: PERCENTAGE,
    ParamType.SENSOR_CHIRP_VOLUME: PERCENTAGE,
}

PARAM_TYPE_FRIENDLY_NAMES = {
    ParamType.BATTERY_LEVEL: "Battery",
    ParamType.BATTERY_TEMP: "Device Temperature",
    ParamType.CAMERA_WIFI_RSSI: "Wifi Signal Strength",
    ParamType.SUB1G_RSSI: "Sub1G Signal Strength",
    ParamType.REPEATER_RSSI: "Repeater Signal Strength",
    ParamType.CAMERA_SPEAKER_VOLUME : "Speaker Volume",
    ParamType.FLOODLIGHT_MANUAL_BRIGHTNESS: "Floodlight Brightness",
    ParamType.LIVEVIEW_LED_SWITCH: "Live view LED Light",
    ParamType.DEV_LED_SWITCH: "LED Light",
    ParamType.SENSOR_CHIRP_VOLUME: "Chirp Volume",
}
