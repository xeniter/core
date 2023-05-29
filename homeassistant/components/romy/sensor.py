"""Sensor checking adc and status values from your ROMY."""

from typing import Any

from romy import RomyRobot

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
)
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
    """Set up ROMY sensor with config entry."""

    coordinator: RomyVacuumCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    romy: RomyRobot = coordinator.romy

    device_info = {
        "manufacturer": "ROMY",
        "model": romy.model,
        "sw_version": romy.firmware,
        "identifiers": {"serial": romy.unique_id},
    }

    # sensors

    romy_sensor_entitiy_battery = RomySensor(
        coordinator,
        romy,
        device_info,
        SensorDeviceClass.BATTERY,
        "Battery Level",
        "battery_level",
        PERCENTAGE,
    )
    romy_sensor_entitiy_rssi = RomySensor(
        coordinator,
        romy,
        device_info,
        SensorDeviceClass.SIGNAL_STRENGTH,
        "RSSI Level",
        "rssi",
        SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    )

    romy_sensor_entities = [
        romy_sensor_entitiy_battery,
        romy_sensor_entitiy_rssi,
    ]
    async_add_entities(romy_sensor_entities, True)

    # adc sensors
    romy_adc_sensor_entitiy_dustbin_full = RomyAdcSensor(
        coordinator, romy, device_info, "Dustbin Full Level", "dustbin_sensor"
    )

    all_adc_sensor_entities = [
        romy_adc_sensor_entitiy_dustbin_full,
    ]

    supported_adc_sensor_entities = []
    for adc_sensor_entity in all_adc_sensor_entities:
        if adc_sensor_entity.sensor_descriptor in romy.adc_sensors:
            supported_adc_sensor_entities.append(adc_sensor_entity)

    async_add_entities(supported_adc_sensor_entities, True)


class RomySensor(CoordinatorEntity[RomyVacuumCoordinator], SensorEntity):
    """RomyStatusSensor Class."""

    def __init__(
        self,
        coordinator: RomyVacuumCoordinator,
        romy: RomyRobot,
        device_info: dict[str, Any],
        device_class: SensorDeviceClass,
        sensor_name: str,
        sensor_descriptor: str,
        measurement_unit: str,
    ) -> None:
        """Initialize ROMYs BatterySensor."""
        super().__init__(coordinator)
        self.romy = romy
        self._sensor_value = None
        self._attr_unique_id = romy.unique_id
        self._device_info = device_info
        self._device_class = device_class
        self._sensor_name = sensor_name
        self._sensor_descriptor = sensor_descriptor
        self._measurement_unit = measurement_unit

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{self.romy.name} {self._sensor_name}"

    @property
    def unique_id(self) -> str:
        """Return the ID of this sensor."""
        return f"{self._sensor_descriptor}_{self._attr_unique_id}"

    @property
    def device_class(self) -> SensorDeviceClass:
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def entity_category(self) -> EntityCategory:
        """Device entity category."""
        return EntityCategory.DIAGNOSTIC

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit_of_measurement of the device."""
        return self._measurement_unit

    @property
    def native_value(self) -> int | None:
        """Return the value of the sensor."""
        return self.romy.sensors[self._sensor_descriptor]


class RomyAdcSensor(CoordinatorEntity[RomyVacuumCoordinator], SensorEntity):
    """RomyAdcSensor Class."""

    def __init__(
        self,
        coordinator: RomyVacuumCoordinator,
        romy: RomyRobot,
        device_info: dict[str, Any],
        sensor_name: str,
        sensor_descriptor: str,
    ) -> None:
        """Initialize ROMYs AdcSensor."""
        super().__init__(coordinator)
        self.romy = romy
        self._sensor_value = None
        self._attr_unique_id = romy.unique_id
        self._device_info = device_info
        self._sensor_name = sensor_name
        self._sensor_descriptor = sensor_descriptor

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{self.romy.name} {self._sensor_name}"

    @property
    def sensor_descriptor(self) -> str:
        """Return the sesnor_descriptor of this sensor."""
        return self._sensor_descriptor

    @property
    def unique_id(self) -> str:
        """Return the ID of this sensor."""
        return f"{self._sensor_descriptor}_{self._attr_unique_id}"

    @property
    def entity_category(self) -> EntityCategory:
        """Device entity category."""
        return EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> int | None:
        """Return the adc value of the sensor."""
        return self.romy.adc_sensors[self._sensor_descriptor]
