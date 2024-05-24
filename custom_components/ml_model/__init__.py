"""Custom integration to integrate ML model Integration
with Home Assistant.
"""

import logging

from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.config_entries import ConfigEntry

# from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant, ServiceCall, callback

# from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DEFAULT_TOPIC, DOMAIN, LOADED_MODEL, PLATFORMS, STARTUP_MESSAGE

_LOGGER: logging.Logger = logging.getLogger(__package__)


def string_to_int_list(s: str) -> list[int]:
    """Convert a string of comma-separated numbers into a list of integers.

    Args:
        s (str): A string containing numbers separated by commas.

    Returns:
        List[int]: A list of integers derived from the input string.

    Example:
        >>> string_to_int_list("1,4,5")
        [1, 4, 5]

    """
    str_list = s.split(",")
    int_list = [int(num) for num in str_list]
    return int_list


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Establish connection with ML model."""

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    # username = entry.data.get(CONF_USERNAME)
    # password = entry.data.get(CONF_PASSWORD)

    # session = async_get_clientsession(hass)

    entity_id = DOMAIN + ".model_outcome"

    # Listen to a message on MQTT.
    @callback
    def message_received(args: ReceiveMessage) -> None:
        """Receive a new MQTT message."""

        # logging.warning(args)  #just log the object to see how it looks

        # topic = getattr(args, "topic")
        payload = getattr(args, "payload")
        # qos = getattr(args, "qos")

        params = string_to_int_list(payload)

        outcome = LOADED_MODEL.predict(X=[params])
        coefficients = LOADED_MODEL.coef_

        _LOGGER.debug("Outcome : %s\nCoefficients : %s", outcome, coefficients)

        hass.states.async_set(entity_id, outcome)

    hass.states.async_set(entity_id, "No messages")

    # Service to publish a message on MQTT.
    @callback
    def set_state_service(call: ServiceCall) -> None:
        """Service to send a message."""
        hass.components.mqtt.async_publish(DEFAULT_TOPIC, call.data.get("new_state"))

    # Register our service with Home Assistant.
    hass.services.async_register(DOMAIN, "set_state", set_state_service)

    await hass.components.mqtt.async_subscribe(DEFAULT_TOPIC, message_received)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
