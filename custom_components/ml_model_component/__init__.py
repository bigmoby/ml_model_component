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
from homeassistant.core import HomeAssistant, callback

# from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import (
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


def proper_round(num, dec=0):
    """Round a number to a specified number of decimal using "round half up" rule.

    This function rounds a given number to the specified number of decimal places.
    It implements the "round half up" rule, where numbers exactly halfway between
    two values are rounded up.

    Args:
        num (float): The number to be rounded.
        dec (int): The number of decimal places to round to (default is 0).

    Returns:
        float: The rounded number.

    Example:
        >>> proper_round(2.675, 2)
        2.68
        >>> proper_round(2.674, 2)
        2.67

    """
    num_str = str(num)
    num_str = num_str[: num_str.index(".") + dec + 2]
    if num_str[-1] >= "5":
        return float(num_str[: -2 - (not dec)] + str(int(num_str[-2 - (not dec)]) + 1))
    return float(num_str[:-1])


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
    async def message_received(args: ReceiveMessage) -> None:
        """Receive a new MQTT message."""

        # topic = getattr(args, "topic")
        payload = getattr(args, "payload")
        # qos = getattr(args, "qos")

        params = string_to_int_list(payload)

        _LOGGER.debug("Applied ML model file %s", ml_model_file)
        LOADED_MODEL = joblib.load(ml_model_file)

        outcome = LOADED_MODEL.predict(X=[params])
        coefficients = LOADED_MODEL.coef_

        result = proper_round(outcome[0], 1)

        _LOGGER.debug("Outcome : %s - Coefficients : %s", result, coefficients)

        await mqtt.async_publish(hass, ml_output_topic, result, qos=0, retain=False)
        hass.states.async_set(entity_id, result)

    hass.states.async_set(entity_id, "No messages")
    _LOGGER.debug("Subscribe to mqtt input topic : %s", ml_input_topic)
    await mqtt.async_subscribe(hass, ml_input_topic, message_received)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
