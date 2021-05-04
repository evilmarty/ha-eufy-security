"""Define support for Eufy base stations."""
import logging

from eufy_security.types import ParamType, GuardMode

from homeassistant.helpers.entity import Entity
from homeassistant.const import STATE_UNKNOWN

from .const import DOMAIN, MANUFACTURER


_LOGGER = logging.getLogger(__name__)

class Station(Entity):
    """Define a Eufy Base Station."""

    def __init__(self, hass, station):
        """Initialize."""
        super().__init__()

        self._station = station

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "manufacturer": MANUFACTURER,
            "model": self._station.model,
            "sw_version": self._station.software_version,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            param.name.lower(): value for param, value in self._station.params.items()
        }

    @property
    def name(self):
        """Return the name of this station."""
        return self._station.name

    @property
    def should_poll(self):
        """Return False, updates are controlled via the hub."""
        return False

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._station.serial

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:home-automation"

    @property
    def state(self):
        """Return the station state."""
        try:
            guard_mode = GuardMode(self._station.params[ParamType.GUARD_MODE])
            return guard_mode.name.lower()
        except ValueError:
            return STATE_UNKNOWN
