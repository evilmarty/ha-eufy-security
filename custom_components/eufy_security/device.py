"""Define support for Eufy device."""
import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, MANUFACTURER, PARAM_TYPE_FRIENDLY_NAMES


_LOGGER = logging.getLogger(__name__)


class DeviceEntity(CoordinatorEntity):
    """Define a Eufy Device."""
    def __init__(self, device, coordinator):
        super().__init__(coordinator)
        self._device = device

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device.serial)},
            "name": self.name,
            "manufacturer": MANUFACTURER,
            "model": self._device.model,
            "sw_version": self._device.software_version,
        }

    @property
    def name(self):
        """Return the name of this station."""
        return self._device.name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device.serial

    @property
    def available(self):
        return bool(self._device.status)

    def _api_update_handler(self, _api):
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self._device._api.subscribe(self._api_update_handler)

    async def async_will_remove_from_hass(self):
        self._device._api.unsubscribe(self._api_update_handler)


class ParamEntity(DeviceEntity):
    """Define a Eufy Param."""
    def __init__(self, device, param_type, coordinator):
        super().__init__(device, coordinator)
        self._param_type = param_type

    @property
    def name(self):
        """Return the name of the param."""
        return PARAM_TYPE_FRIENDLY_NAMES.get(
            self._param_type,
            self._param_type.name
        )

    @property
    def unique_id(self):
        """Return a unique ID."""
        return "{}-{}".format(self._device.serial, self._param_type.value)
