"""Platform for ML model sensor integration."""
from __future__ import annotations

try:
    import joblib
except ImportError:
    from sklearn.externals import joblib
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
import logging
from homeassistant.const import UnitOfTemperature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)
from .const import NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,async_add_entities: AddEntitiesCallback,
) -> None:
    """Setups the ML model Platform based on a config entry."""
    _LOGGER.debug("ML model async_setup_entry called")

    username: str = entry.data[CONF_USERNAME]
    password: str = entry.data[CONF_PASSWORD]

    new_entities = []

    new_entities.append(MLModelSensor())

    async_add_entities(new_entities, update_before_add=True)


class MLModelSensor(SensorEntity):
    """Representation of a ML model Sensor."""

    _attr_name = NAME
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        loaded_model = joblib.load('predictor.pkl')

        X_TEST = [[1, 2, 5]]
        outcome = loaded_model.predict(X=X_TEST)
        coefficients = loaded_model.coef_

        print('Outcome : {}\nCoefficients : {}'.format(outcome, coefficients))
        self._attr_native_value = outcome