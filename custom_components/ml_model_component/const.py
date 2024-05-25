"""ML Model Controller Integration.

This module handles the integration of a machine learning model with Home Assistant.
It loads the model, defines the necessary constants, and sets up the platforms.

Attributes:
    NAME (str): The name of the integration.
    DOMAIN (str): The domain of the integration used for unique identification.
    DOMAIN_DATA (str): The domain data string for storing integration-specific data.
    VERSION (str): The current version of the integration.
    LOADED_MODEL (object): The ML model loaded from the file 'predictor.pkl'.
    ISSUE_URL (str): The URL for reporting issues related to this integration.
    PLATFORMS (list): The list of platforms that this integration supports.
    STARTUP_MESSAGE (str): The startup message displayed when the integration is loaded.
    DEFAULT_TOPIC (str): The default MQTT topic used by the integration.

"""

from homeassistant.const import Platform

# Base component constants

NAME = "ML model controller integration"
"""
str: The name of the integration.
"""

DOMAIN = "ml_model_component"
"""
str: The domain of the integration used for unique identification.
"""

DOMAIN_DATA = f"{DOMAIN}_data"
"""
str: The domain data string for storing integration-specific data.
"""

VERSION = "0.0.1"
"""
str: The current version of the integration.
"""

ISSUE_URL = "https://github.com/bigmoby/ml_model_component/issues"
"""
str: The URL for reporting issues related to this integration.
"""

# Platforms
PLATFORMS = [Platform.SENSOR]
"""
list: The list of platforms that this integration supports.
"""

STARTUP_MESSAGE = (
    "-------------------------------------------------------------------\n"
    f"{NAME}\n"
    f"Version: {VERSION}\n"
    "This is a custom integration!\n"
    "If you have any issues with this you need to open an issue here:\n"
    f"{ISSUE_URL}\n"
    "-------------------------------------------------------------------\n"
)
"""
str: The startup message displayed when the integration is loaded.
"""

DEFAULT_TOPIC = "home-assistant/ml_model_component"
"""
str: The default MQTT topic used by the integration.
"""

ML_MODEL_SUFFIXES = ("pkl", "pyc")
"""
list: The list of ml model file type that this integration supports.
"""

ACCEPTED_SUFFIX_FILE = ", ".join(f".{ext}" for ext in ML_MODEL_SUFFIXES)
"""
str: The joined stringed version of ml model file type that this integration supports.
"""

ML_MODEL_LOCAL_FILE = "ml_model_local_file"
"""
str: The uploaded ML model local file.
"""
