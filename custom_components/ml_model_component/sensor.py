"""Platform for ML model sensor integration."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setups the ML model Platform based on a config entry."""
    _LOGGER.debug("ML model async_setup_entry called")

    # username: str = entry.data[CONF_USERNAME]
    # password: str = entry.data[CONF_PASSWORD]

    """
    ml_model_file: str = entry.data[ML_MODEL_LOCAL_FILE]
    LAST_UPLOADED_ML_MODEL_FILE = ml_model_file
    joblib.load(LAST_UPLOADED_ML_MODEL_FILE)
    _LOGGER.debug("ml_model_file : %s", LAST_UPLOADED_ML_MODEL_FILE)
    """

    new_entities = []

    new_entities.append(MLModelSensor())

    async_add_entities(new_entities, update_before_add=True)


class MLModelSensor(SensorEntity):
    """Representation of a ML model Sensor."""


'''
    _attr_name = NAME
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        X_TEST = [[1, 2, 5]]
        outcome = LOADED_MODEL.predict(X=X_TEST)
        coefficients = LOADED_MODEL.coef_

        _LOGGER.debug("Outcome : %s\nCoefficients : %s", outcome, coefficients)
        self._attr_native_value = outcome
'''
