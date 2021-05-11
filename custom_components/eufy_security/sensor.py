"""Define support for Eufy sensors."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    PERCENTAGE,
    TEMP_CELSIUS,
)

from .device import ParamEntity
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
            ParamSensor(station, param_type, coordinator)
            for param_type, value in station.params.items()
            if param_type in PARAM_TYPES and type(value) == int
        )

    for device in api.devices.values():
        async_add_entities([
            ParamSensor(device, param_type, coordinator)
            for param_type, value in device.params.items()
            if param_type in PARAM_TYPES and type(value) == int
        ])


class ParamSensor(ParamEntity, SensorEntity):
    """Define a Eufy device parameter sensor."""

    def __init__(self, device, param_type, coordinator):
        super().__init__(device, param_type, coordinator)
        SensorEntity.__init__(self)

    @property
    def state(self):
        """Return the state of the device."""
        return self._device.params.get(self._param_type)

    @property
    def device_class(self):
        return PARAM_TYPE_DEVICE_CLASS.get(self._param_type)

    @property
    def unit_of_measurement(self):
        return PARAM_TYPE_UNIT_OF_MEASUREMENT.get(self._param_type)
