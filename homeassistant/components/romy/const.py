"""Constants for the ROMY integration."""

from datetime import timedelta
import logging

from homeassistant.const import Platform

# This is the internal name of the integration, it should also match the directory
# name for the integration.
DOMAIN = "romy"
PLATFORMS = [Platform.VACUUM]
UPDATE_INTERVAL = timedelta(seconds=5)
LOGGER = logging.getLogger(__package__)
