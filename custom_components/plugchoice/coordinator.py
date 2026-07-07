"""Data update coordinator for Plugchoice."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import PlugchoiceApi
from .const import DOMAIN


SCAN_INTERVAL = timedelta(seconds=30)


class PlugchoiceCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Plugchoice data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: PlugchoiceApi,
    ) -> None:
        """Initialize coordinator."""

        self.api = api

        super().__init__(
            hass,
            logger=__import__("logging").getLogger(DOMAIN),
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from Plugchoice."""

        try:
            chargers = await self.api.get_chargers()

            return chargers

        except Exception as err:
            raise UpdateFailed(
                f"Error communicating with Plugchoice: {err}"
            ) from err