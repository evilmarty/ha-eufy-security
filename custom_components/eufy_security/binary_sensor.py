"""Define support for Eufy sensors."""
import logging

from eufy_security.types import DeviceType

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_MOTION,
)

from .device import Device
from .const import DOMAIN, DATA_API


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][DATA_API]
    async_add_entities(
        BinarySensor(hass, sensor)
        for sensor in api.sensors.values()
    )


class BinarySensor(Device, BinarySensorEntity):
    """Define a Eufy sensor."""

    def __init__(self, hass, device):
        """Initialize."""
        super().__init__(hass, device)
        BinarySensorEntity.__init__()

    @property
    def is_on(self):
        """Return the status of the sensor."""
        return self._sensor.is_on

    @property
    def device_class(self):
        if self._sensor.device_type == DeviceType.MOTION_SENSOR:
            DEVICE_CLASS_MOTION
        else:
            DEVICE_CLASS_DOOR
