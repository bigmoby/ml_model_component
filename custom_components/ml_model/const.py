from homeassistant.const import Platform

# Base component constants
NAME = "ML model controller integration"
DOMAIN = "ml_model"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ISSUE_URL = "https://github.com/bigmoby/ml_model_component/issues"

# Platforms
PLATFORMS = [Platform.SENSOR]

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""