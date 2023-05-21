"""Support for Wi-Fi enabled ROMY vacuum cleaner robots.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/vacuum.romy/.
"""


from collections.abc import Mapping
from typing import Any

from romy import RomyRobot

from homeassistant.components.vacuum import VacuumEntity, VacuumEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ICON, LOGGER
from .coordinator import RomyVacuumCoordinator

FAN_SPEED_NONE = "Default"
FAN_SPEED_NORMAL = "Normal"
FAN_SPEED_SILENT = "Silent"
FAN_SPEED_INTENSIVE = "Intensive"
FAN_SPEED_SUPER_SILENT = "Super_Silent"
FAN_SPEED_HIGH = "High"
FAN_SPEED_AUTO = "Auto"

FAN_SPEEDS: list[str] = [
    FAN_SPEED_NONE,
    FAN_SPEED_NORMAL,
    FAN_SPEED_SILENT,
    FAN_SPEED_INTENSIVE,
    FAN_SPEED_SUPER_SILENT,
    FAN_SPEED_HIGH,
    FAN_SPEED_AUTO,
]

# Commonly supported features
SUPPORT_ROMY_ROBOT = (
    VacuumEntityFeature.BATTERY
    | VacuumEntityFeature.PAUSE
    | VacuumEntityFeature.RETURN_HOME
    | VacuumEntityFeature.SEND_COMMAND
    | VacuumEntityFeature.STATUS
    | VacuumEntityFeature.STOP
    | VacuumEntityFeature.TURN_OFF
    | VacuumEntityFeature.TURN_ON
    | VacuumEntityFeature.FAN_SPEED
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ROMY vacuum cleaner."""

    coordinator: RomyVacuumCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    romy: RomyRobot = coordinator.romy

    device_info = {
        "manufacturer": "ROMY",
        "model": romy.model,
        "sw_version": romy.firmware,
        "identifiers": {"serial": romy.unique_id},
    }

    romy_vacuum_entity = RomyVacuumEntity(coordinator, romy, device_info)
    entities = [romy_vacuum_entity]
    async_add_entities(entities, True)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ROMY vacuum cleaner."""

    coordinator: RomyVacuumCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    romy: RomyRobot = coordinator.romy

    device_info = {
        "manufacturer": "ROMY",
        "model": romy.model,
        "sw_version": romy.firmware,
        "identifiers": {"serial": romy.unique_id},
    }

    romy_vacuum_entity = RomyVacuumEntity(coordinator, romy, device_info)
    entities = [romy_vacuum_entity]
    async_add_entities(entities, True)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ROMY vacuum cleaner."""

    coordinator: RomyVacuumCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    romy: RomyRobot = coordinator.romy

    device_info = {
        "manufacturer": "ROMY",
        "model": romy.model,
        "sw_version": romy.firmware,
        "identifiers": {"serial": romy.unique_id},
    }

    romy_vacuum_entity = RomyVacuumEntity(coordinator, romy, device_info)
    entities = [romy_vacuum_entity]
    async_add_entities(entities, True)


class RomyVacuumEntity(VacuumEntity):
    """Representation of a ROMY vacuum cleaner robot."""

    def __init__(
        self,
        coordinator: RomyVacuumCoordinator,
        romy: RomyRobot,
        device_info: dict[str, Any],
    ) -> None:
        """Initialize the ROMY Robot."""
        self.coordinator = coordinator
        self.romy = romy
        self._device_info = device_info
        self._attr_unique_id = self.romy.unique_id

        self._battery_level = None
        self._fan_speed = FAN_SPEEDS.index(FAN_SPEED_NONE)
        self._fan_speed_update = False
        self._is_on = False
        self._state_attrs: dict[str, Any] = {}
        self._status = None

    @property
    def supported_features(self) -> VacuumEntityFeature:
        """Flag vacuum cleaner robot features that are supported."""
        return SUPPORT_ROMY_ROBOT

    @property
    def fan_speed(self) -> str:
        """Return the current fan speed of the vacuum cleaner."""
        return FAN_SPEEDS[self._fan_speed]

    @property
    def fan_speed_list(self) -> list[str]:
        """Get the list of available fan speed steps of the vacuum cleaner."""
        return FAN_SPEEDS

    @property
    def battery_level(self) -> None | int:
        """Return the battery level of the vacuum cleaner."""
        return self._battery_level

    @property
    def status(self) -> None | str:
        """Return the status of the vacuum cleaner."""
        return self._status

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        return self._is_on

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return "hack"
        # return self.romy.name

    @property
    def icon(self) -> str:
        """Return the icon to use for device."""
        return ICON

    @property
    def device_state_attributes(self) -> Mapping[str, Any] | None:
        """Return the state attributes of the device."""
        return self._state_attrs

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the vacuum on."""
        LOGGER.debug("async_turn_on")
        # is_on, _ = await self.romy_async_query(
        #    f"set/clean_start_or_continue?cleaning_parameter_set={self._fan_speed}"
        # )
        # if is_on:
        #    self._is_on = True

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the vacuum off and return to home."""
        LOGGER.debug("async_turn_off")
        # await self.async_return_to_base()

    async def async_stop(self, **kwargs: Any) -> None:
        """Stop the vacuum cleaner."""
        LOGGER.debug("async_stop")
        # is_off, _ = await self.romy_async_query("set/stop")
        # if is_off:
        #    self._is_on = False

    async def async_pause(self, **kwargs: Any) -> None:
        """Pause the cleaning cycle."""
        LOGGER.debug("async_pause")
        # is_off, _ = await self.romy_async_query("set/stop")
        # if is_off:
        #    self._is_on = False

    async def async_start_pause(self, **kwargs: Any) -> None:
        """Pause the cleaning task or resume it."""
        LOGGER.debug("async_start_pause")
        # if self.is_on:
        #    await self.async_stop()
        # else:
        #    await self.async_turn_on()

    # return_to_base -> run go_home
    async def async_return_to_base(self, **kwargs: Any) -> None:
        """Set the vacuum cleaner to return to the dock."""
        LOGGER.debug("async_return_to_base")
        # is_on, _ = await self.romy_async_query("set/go_home")
        # if is_on:
        #    self._is_on = False

    async def async_set_fan_speed(self, fan_speed: str, **kwargs: Any) -> None:
        """Set fan speed."""
        LOGGER.debug("async_set_fan_speed to %s", fan_speed)
        # if fan_speed in FAN_SPEEDS:
        #    self._fan_speed_update = True
        #    self._fan_speed = FAN_SPEEDS.index(fan_speed)
        #    ret, response = await self.romy_async_query(
        #        f"set/switch_cleaning_parameter_set?cleaning_parameter_set={self._fan_speed}"
        #    )
        #    self._fan_speed_update = False
        #    if not ret:
        #        LOGGER.error(
        #            " async_set_fan_speed -> async_query response: %s", response
        #        )
        # else:
        #    LOGGER.error("No such fan speed available: %d", fan_speed)

    async def async_update(self) -> None:
        """Fetch state from the device."""
        LOGGER.debug("async_update")

        # ret, response = await self.romy_async_query("get/status")
        # if ret:
        #    status = json.loads(response)
        #    self._status = status["mode"]
        #    self._battery_level = status["battery_level"]
        # else:
        #    LOGGER.error(
        #        "ROMY function async_update -> async_query response: %s", response
        #    )

        # ret, response = await self.romy_async_query("get/cleaning_parameter_set")
        # if ret:
        #    status = json.loads(response)
        #    # dont update if we set fan speed currently:
        #    if not self._fan_speed_update:
        #        self._fan_speed = status["cleaning_parameter_set"]
        # else:
        #    LOGGER.error(
        #        "FOMY function async_update -> async_query response: %s", response
        #   )
