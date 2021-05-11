"""Define support for Eufy binary sensors."""
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from eufy_security.types import ParamType

from .device import DeviceEntity, ParamEntity
from .const import (
    DOMAIN,
    DATA_API,
    DATA_COORDINATOR,
    PARAM_TYPES,
    PARAM_TYPE_DEVICE_CLASS,
    PARAM_TYPE_UNIT_OF_MEASUREMENT,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id][DATA_API]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

    for station in api.stations.values():
        async_add_entities(
            ParamBinarySensor(station, param_type, coordinator)
            for param_type, value in station.params.items()
            if param_type in PARAM_TYPES and type(value) == bool
        )

    for device in api.devices.values():
        async_add_entities([
            ParamBinarySensor(device, param_type, coordinator)
            for param_type, value in device.params.items()
            if param_type in PARAM_TYPES and type(value) == bool
        ])

        if device.device_type.is_sensor:
            async_add_entities([DeviceBinarySensor(device, coordinator)])


class DeviceBinarySensor(DeviceEntity, BinarySensorEntity):
    """Define a Eufy device sensor."""

    def __init__(self, device, coordinator):
        super().__init__(device, coordinator)
        BinarySensorEntity.__init__(self)

    @property
    def is_on(self):
        """Return the status of the sensor."""
        return self._device.params.get(ParamType.SENSOR_STATUS)

    @property
    def device_class(self):
        return PARAM_TYPE_DEVICE_CLASS.get(ParamType.SENSOR_STATUS)


class ParamBinarySensor(ParamEntity, BinarySensorEntity):
    """Define a Eufy device parameter sensor."""

    def __init__(self, device, param_type, coordinator):
        super().__init__(device, param_type, coordinator)
        BinarySensorEntity.__init__(self)

    @property
    def is_on(self):
        """Return the status of the sensor."""
        return self._device.params.get(self._param_type)

    @property
    def device_class(self):
        return PARAM_TYPE_DEVICE_CLASS.get(self._param_type)
