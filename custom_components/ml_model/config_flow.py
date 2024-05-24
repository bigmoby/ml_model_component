"""Config flow for the ML model Integration."""

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
import voluptuous as vol
import logging
from .const import DOMAIN


_LOGGER: logging.Logger = logging.getLogger(__package__)
DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME, default=""): str,
        vol.Required(CONF_PASSWORD, default=""): str,
    }
)


class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input: dict | None = None  # type: ignore[type-arg]
                              ) -> ConfigFlowResult:
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=DATA_SCHEMA)

        username = user_input[CONF_USERNAME]
        password=user_input[CONF_PASSWORD]
        unique_id = await self.async_set_unique_id(username)
        _LOGGER.debug("Creating unique ID %s", unique_id)
        self._abort_if_unique_id_configured({CONF_USERNAME: username})
        entry = self.async_create_entry(
            title=username,
            data={
                CONF_USERNAME: username,
                CONF_PASSWORD: password,
            },
        )
        return entry
