"""Custom integration to integrate ML model Integration
with Home Assistant.
"""

import logging

try:
    import joblib
except ImportError:
    from sklearn.externals import joblib

from homeassistant.components import mqtt
from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.config_entries import ConfigEntry

# from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant, ServiceCall, callback

# from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import (
    DEFAULT_INPUT_TOPIC,
    DOMAIN,
    ML_MODEL_INPUT_TOPIC,
    ML_MODEL_LOCAL_FILE,
    ML_MODEL_OUTPUT_TOPIC,
    PLATFORMS,
    STARTUP_MESSAGE,
)

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

    ml_input_topic = entry.data.get(ML_MODEL_INPUT_TOPIC)
    ml_output_topic = entry.data.get(ML_MODEL_OUTPUT_TOPIC)
    ml_model_file = entry.data.get(ML_MODEL_LOCAL_FILE)

    # session = async_get_clientsession(hass)
    entity_id = DOMAIN + ".outcome"

    # Listen to a message on MQTT.
    @callback
    def message_received(args: ReceiveMessage) -> None:
        """Receive a new MQTT message."""

        # logging.warning(args)  #just log the object to see how it looks

        # topic = getattr(args, "topic")
        payload = getattr(args, "payload")
        # qos = getattr(args, "qos")

        params = string_to_int_list(payload)

        _LOGGER.debug("Applied ML model file %s", ml_model_file)
        LOADED_MODEL = joblib.load(ml_model_file)

        outcome = LOADED_MODEL.predict(X=[params])
        coefficients = LOADED_MODEL.coef_

        _LOGGER.debug("Outcome : %s\nCoefficients : %s", outcome, coefficients)

        hass.states.async_set(entity_id, outcome)

    hass.states.async_set(entity_id, "No messages")

    # Service to publish a message on MQTT.
    @callback
    def set_state_service(call: ServiceCall) -> None:
        """Service to send a message."""
        mqtt.async_publish(hass, ml_input_topic, call.data.get("new_state"))

    await mqtt.async_subscribe(hass, ml_output_topic, message_received)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
