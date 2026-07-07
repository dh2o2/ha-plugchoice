"""The Plugchoice integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PlugchoiceApi
from .const import CONF_TOKEN, DOMAIN
from .coordinator import PlugchoiceCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Plugchoice from a config entry."""

    session = async_get_clientsession(hass)

    api = PlugchoiceApi(
        session,
        entry.data[CONF_TOKEN],
    )

    coordinator = PlugchoiceCoordinator(
        hass,
        api,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = coordinator

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Plugchoice entry."""

    hass.data[DOMAIN].pop(entry.entry_id)

    return True