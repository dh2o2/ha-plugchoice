"""Sensor platform for Plugchoice."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import PlugchoiceCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Plugchoice sensors."""

    coordinator: PlugchoiceCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for charger in coordinator.data:
        entities.append(
            PlugchoiceSensor(
                coordinator,
                charger,
                "connection_status",
                "Connection",
            )
        )

        entities.append(
            PlugchoiceSensor(
                coordinator,
                charger,
                "firmware_version",
                "Firmware",
            )
        )

        entities.append(
            PlugchoiceSensor(
                coordinator,
                charger,
                "max_current",
                "Max Current",
            )
        )

    async_add_entities(entities)


class PlugchoiceSensor(SensorEntity):
    """Representation of a Plugchoice sensor."""

    def __init__(
        self,
        coordinator,
        charger,
        key,
        name,
    ):
        """Initialize sensor."""

        self.coordinator = coordinator
        self.charger = charger
        self.key = key

        self._attr_name = (
            f"{charger['reference']} {name}"
        )

        self._attr_unique_id = (
            f"{charger['uuid']}_{key}"
        )

    @property
    def native_value(self):
        """Return sensor value."""

        return self.charger.get(self.key)

    async def async_update(self):
        """Update sensor."""

        await self.coordinator.async_request_refresh()