"""Define support for Eufy Security devices."""
from datetime import timedelta
import asyncio
import logging

from eufy_security import async_login
from eufy_security.errors import EufySecurityError, InvalidCredentialsError
import voluptuous as vol

from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client, config_validation as cv
from homeassistant.helpers.event import async_track_time_interval

from .config_flow import configured_instances
from .const import DATA_API, DATA_LISTENER, DOMAIN
from .station import Station
from .camera import EufySecurityCam
from .sensor import BinarySensor

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up the Eufy Security component."""
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][DATA_API] = {}
    hass.data[DOMAIN][DATA_LISTENER] = {}

    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]

    if conf[CONF_USERNAME] in configured_instances(hass):
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_IMPORT},
            data={
                CONF_USERNAME: conf[CONF_USERNAME],
                CONF_PASSWORD: conf[CONF_PASSWORD],
            },
        )
    )

    return True


async def async_setup_entry(hass, entry):
    """Set up Eufy Security as a config entry."""
    session = aiohttp_client.async_get_clientsession(hass)

    try:
        api = await async_login(
            entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD], session
        )
    except InvalidCredentialsError:
        _LOGGER.error("Invalid username and/or password")
        return False
    except EufySecurityError as err:
        _LOGGER.error("Config entry failed: %s", err)
        raise ConfigEntryNotReady

    async def refresh(event_time):
        """Refresh data from the API."""
        _LOGGER.debug("Refreshing API data")
        await api.async_update_device_info()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_API: api,
        DATA_LISTENER: async_track_time_interval(hass, refresh, DEFAULT_SCAN_INTERVAL),
    }

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass, entry):
    """Unload a Eufy Security config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unload_ok:
        entry_data = hass.data[DOMAIN].pop(entry.entry_id)
        entry_data[DATA_LISTENER]()

    return unload_ok
