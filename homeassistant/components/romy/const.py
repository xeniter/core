"""Constants for the ROMY integration."""

from datetime import timedelta
import logging

from homeassistant.const import Platform

DOMAIN = "romy"
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.VACUUM]
UPDATE_INTERVAL = timedelta(seconds=5)
LOGGER = logging.getLogger(__package__)
