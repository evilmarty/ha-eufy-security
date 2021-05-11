"""Define support for Eufy Security devices."""
from datetime import timedelta
import asyncio
import logging

from eufy_security import async_login
from eufy_security.errors import EufySecurityError, InvalidCredentialsError
import voluptuous as vol

from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_SCAN_INTERVAL
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client, config_validation as cv
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .config_flow import configured_instances
from .const import DATA_API, DATA_LISTENER, DATA_COORDINATOR, DOMAIN, PLATFORMS

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

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_API: api,
        DATA_COORDINATOR: DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=f"api_{entry.entry_id}",
            update_method=api.async_update_device_info,
            update_interval=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        ),
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
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
