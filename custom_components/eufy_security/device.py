"""Define support for Eufy device."""
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.const import STATE_UNKNOWN

from .const import DOMAIN, MANUFACTURER


_LOGGER = logging.getLogger(__name__)


class Device(Entity):
    """Define a Eufy Device."""

    def __init__(self, hass, device):
        """Initialize."""
        super().__init__()
        self._device = device

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "manufacturer": MANUFACTURER,
            "model": self._device.model,
            "sw_version": self._device.software_version,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            param.name.lower(): value for param, value in self._device.params.items()
        }

    @property
    def name(self):
        """Return the name of this station."""
        return self._device.name

    @property
    def should_poll(self):
        """Return False, updates are controlled via the hub."""
        return False

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device.serial
