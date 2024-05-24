"""Custom integration to integrate ML model Integration
with Home Assistant.
"""

import logging
from .const import DOMAIN, PLATFORMS, STARTUP_MESSAGE
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Establish connection with ML model."""

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    session = async_get_clientsession(hass)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True