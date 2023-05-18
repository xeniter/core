from romy import RomyRobot

from homeassistant.core import HomeAssistant

# from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER, UPDATE_INTERVAL


class RomyVacuumCoordinator(DataUpdateCoordinator[bool]):
    def __init__(self, hass: HomeAssistant, romy: RomyRobot) -> None:
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)
        self.hass = hass
        self.romy = romy

    # async def async_setup(self):
    #    # Check if the robot is online
    #    if not await self.romy_api.is_robot_online():
    #        raise Exception("Robot is not online.")

    #    # Create the vacuum entity
    #    self.romy_vacuum = RomyVacuumEntity(self)

    async def async_update_data(self):
        # Perform update tasks if needed
        pass

    # async def async_refresh(self):
    #    await self.coordinator.async_request_refresh()
