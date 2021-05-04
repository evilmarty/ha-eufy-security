"""Define support for Eufy sensors."""
import logging

from eufy_security.types import ParamType, DeviceType

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_MOTION,
)

from .const import DOMAIN, MANUFACTURER


_LOGGER = logging.getLogger(__name__)

class BinarySensor(BinarySensorEntity):
    """Define a Eufy sensor."""

    def __init__(self, hass, sensor):
        """Initialize."""
        super().__init__()

        self._sensor = sensor

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "manufacturer": MANUFACTURER,
            "model": self._sensor.model,
            "sw_version": self._sensor.software_version,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            param.name.lower(): value for param, value in self._sensor.params.items() if param != ParamType.SENSOR_OPEN
        }

    @property
    def name(self):
        """Return the name of this sensor."""
        return self._sensor.name

    @property
    def should_poll(self):
        """Return False, updates are controlled via the hub."""
        return False

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._sensor.serial

    @property
    def is_on(self):
        """Return the status of the sensor."""
        return self._sensor.params[Param.SENSOR_OPEN] == 1

    @property
    def device_class(self):
        if self._sensor.device_type == DeviceType.MOTION_SENSOR:
            DEVICE_CLASS_MOTION
        else:
            DEVICE_CLASS_DOOR
