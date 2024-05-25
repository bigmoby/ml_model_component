"""Config flow for the ML model Integration."""

from functools import cached_property
import logging
from pathlib import Path
import shutil

from homeassistant import config_entries
from homeassistant.components.file_upload import process_uploaded_file
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.selector import FileSelector, FileSelectorConfig
import voluptuous as vol

from .const import ACCEPTED_SUFFIX_FILE, DOMAIN, ML_MODEL_LOCAL_FILE

_LOGGER: logging.Logger = logging.getLogger(__package__)
DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME, default=""): str,
        vol.Required(CONF_PASSWORD, default=""): str,
        vol.Required(ML_MODEL_LOCAL_FILE): FileSelector(
            FileSelectorConfig(accept=ACCEPTED_SUFFIX_FILE)
        ),
    }
)


class MLModelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg] # noqa: E501
    """Handle a config flow for Example integration.

    This class manages the configuration flow for the Example integration,
    allowing users to configure the integration through the Home Assistant UI.
    """

    @cached_property
    def _local_dir(self) -> Path:
        """Return real path to "/www" directory."""
        return Path(self.hass.config.path("www"))

    @cached_property
    def _uploaded_dir(self) -> Path:
        """Return real path to "/www/ml_model_storage" directory."""
        return self._local_dir / "ml_model_storage"

    def _save_uploaded_file(self, uploaded_file_id: str) -> str:
        """Save uploaded file.

        Must be called in an executor.

        Returns name of file relative to "/www".
        """
        with process_uploaded_file(self.hass, uploaded_file_id) as uf_path:
            ud = self._uploaded_dir
            ud.mkdir(parents=True, exist_ok=True)
            suffix = "pkl"
            fn = ud / f"x.{suffix}"
            idx = 0
            while (uf := fn.with_stem(f"model_{idx:03d}")).exists():
                idx += 1
            shutil.move(uf_path, uf)
            return str(uf.absolute())

    async def async_step_user(
        self,
        user_input: dict | None = None,  # type: ignore[type-arg]
    ) -> ConfigFlowResult:
        """Handle the initial step initiated by the user.

        This method handles the first step in the configuration flow when initiated
        by the user through the Home Assistant UI. It prompts the user to input
        their username and password, validates the input, and creates a unique
        configuration entry.

        Args:
            user_input (Optional[Dict[str, Any]]): A dictionary containing user inputs.
                Defaults to None.

        Returns:
            config_entries.ConfigFlowResult: The result of the configuration flow.

        """

        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

        username = user_input[CONF_USERNAME]
        password = user_input[CONF_PASSWORD]
        unique_id = await self.async_set_unique_id(username)

        _LOGGER.debug("Creating unique ID %s", unique_id)
        self._abort_if_unique_id_configured({CONF_USERNAME: username})

        uploaded_file_id = user_input.get(ML_MODEL_LOCAL_FILE)

        local_file = await self.hass.async_add_executor_job(
            self._save_uploaded_file, uploaded_file_id
        )

        _LOGGER.debug("Stored ML model file %s", local_file)

        entry = self.async_create_entry(
            title=username,
            data={
                CONF_USERNAME: username,
                CONF_PASSWORD: password,
                ML_MODEL_LOCAL_FILE: local_file,
            },
        )
        return entry
