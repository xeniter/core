"""Binary Sensors from your ROMY."""

from typing import Any

from romy import RomyRobot

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RomyVacuumCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ROMY binary sensor with config entry."""

    coordinator: RomyVacuumCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    romy: RomyRobot = coordinator.romy

    device_info = {
        "manufacturer": "ROMY",
        "model": romy.model,
        "sw_version": romy.firmware,
        "identifiers": {"serial": romy.unique_id},
    }

    romy_binary_sensor_entitiy_docked = RomyBinarySensor(
        coordinator, romy, device_info, None, "Dustbin present", "dustbin"
    )
    romy_binary_sensor_entitiy_dustbin_present = RomyBinarySensor(
        coordinator,
        romy,
        device_info,
        BinarySensorDeviceClass.PRESENCE,
        "Robot docked",
        "dock",
    )
    romy_binary_sensor_entitiy_watertank_present = RomyBinarySensor(
        coordinator,
        romy,
        device_info,
        BinarySensorDeviceClass.MOISTURE,
        "Watertank present",
        "water_tank",
    )
    romy_binary_sensor_entitiy_watertank_empty = RomyBinarySensor(
        coordinator,
        romy,
        device_info,
        BinarySensorDeviceClass.PROBLEM,
        "Watertank empty",
        "water_tank_empty",
    )

    # complete binary sensor list
    all_binary_sensor_entities = [
        romy_binary_sensor_entitiy_docked,
        romy_binary_sensor_entitiy_dustbin_present,
        romy_binary_sensor_entitiy_watertank_present,
        romy_binary_sensor_entitiy_watertank_empty,
    ]

    # add only supported / available sensors:
    supported_binary_sensor_entities = []
    for binary_sensor_entity in all_binary_sensor_entities:
        if binary_sensor_entity.device_descriptor in romy.binary_sensors:
            supported_binary_sensor_entities.append(binary_sensor_entity)

    async_add_entities(supported_binary_sensor_entities, True)


class RomyBinarySensor(CoordinatorEntity[RomyVacuumCoordinator], BinarySensorEntity):
    """RomyBinarySensor Class."""

    def __init__(
        self,
        coordinator: RomyVacuumCoordinator,
        romy: RomyRobot,
        device_info: dict[str, Any],
        device_class: BinarySensorDeviceClass | None,
        sensor_name: str,
        device_descriptor: str,
    ) -> None:
        """Initialize ROMYs BinarySensor."""
        super().__init__(coordinator)
        self.romy = romy
        self._attr_unique_id = romy.unique_id
        self._attr_device_class = device_class
        self._sensor_value = False
        self._sensor_name = sensor_name
        self._device_descriptor = device_descriptor

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{self.romy.name} {self._sensor_name}"

    @property
    def device_descriptor(self) -> str:
        """Return the device_descriptor of this sensor."""
        return self._device_descriptor

    @property
    def unique_id(self) -> str:
        """Return the ID of this sensor."""
        return f"{self._device_descriptor}_{self._attr_unique_id}"

    @property
    def is_on(self) -> bool | None:
        """Return the state of the sensor."""
        return self.romy.binary_sensors[self._device_descriptor]
