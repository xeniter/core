"""ROMY coordinator."""

from romy import RomyRobot

from homeassistant.core import HomeAssistant

# from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER, UPDATE_INTERVAL


class RomyVacuumCoordinator(DataUpdateCoordinator[bool]):
    """ROMY Vacuum Coordinator."""
    def __init__(self, hass: HomeAssistant, romy: RomyRobot) -> None:
        """Setuping ROMY Vacuum Coordinator class."""
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)
        self.hass = hass
        self.romy = romy

    async def async_update_data(self) -> None:
        """Update ROMY Vacuum Cleaner data."""
