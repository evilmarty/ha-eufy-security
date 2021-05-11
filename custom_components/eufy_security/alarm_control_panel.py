"""Define support for Eufy base stations."""
import logging

from homeassistant.const import (
    STATE_UNKNOWN,
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_DISARMED,
)
from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    SUPPORT_ALARM_ARM_AWAY,
    SUPPORT_ALARM_ARM_HOME,
)

from .const import DOMAIN, DATA_API, DATA_COORDINATOR
from .device import DeviceEntity


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id][DATA_API]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities(
        Station(station, coordinator)
        for station in api.stations.values()
    )


class Station(DeviceEntity, AlarmControlPanelEntity):
    """Define a Eufy Base Station."""

    def __init__(self, device, coordinator):
        super().__init__(device, coordinator)
        AlarmControlPanelEntity.__init__(self)

    @property
    def code_arm_required(self):
        """Whether the code is required for arm actions."""
        return False

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_ALARM_ARM_HOME | SUPPORT_ALARM_ARM_AWAY

    @property
    def state(self):
        """Return the station state."""
        if self._device.away_mode:
            return STATE_ALARM_ARMED_AWAY
        elif self._device.home_mode:
            return STATE_ALARM_ARMED_HOME
        elif self._device.disarmed_mode:
            return STATE_ALARM_DISARMED
        elif self._device.guard_mode is not None:
            return self._device.guard_mode.name.lower()
        else:
            return STATE_UNKNOWN

    async def async_alarm_disarm(self, code=None):
        """Set station to disarmed."""
        await self._device.set_disarmed_mode()

    async def async_alarm_arm_away(self, code=None):
        """Set station to away."""
        await self._device.set_away_mode()

    async def async_alarm_arm_home(self, code=None):
        """Set station to home."""
        await self._device.set_home_mode()
