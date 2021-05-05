"""Define support for Eufy base stations."""
import logging

from homeassistant.const import STATE_UNKNOWN

from .device import Device
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][DATA_API]
    async_add_entities(
        Station(hass, station)
        for station in api.stations.values()
    )


class Station(Device):
    """Define a Eufy Base Station."""

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:home-automation"

    @property
    def state(self):
        """Return the station state."""
        guard_mode = self._station.guard_mode
        if guard_mode is None:
            return STATE_UNKNOWN
        else:
            return guard_mode.name.lower()
