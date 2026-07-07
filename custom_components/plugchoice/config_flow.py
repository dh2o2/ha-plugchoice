"""Config flow for Plugchoice."""

from __future__ import annotations

from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PlugchoiceApi
from .const import CONF_TOKEN, DOMAIN, ERROR_AUTH, ERROR_CONNECTION


class PlugchoiceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Plugchoice."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ):
        """Handle the initial step."""

        errors = {}

        if user_input is not None:
            token = user_input[CONF_TOKEN]

            try:
                session = async_get_clientsession(self.hass)

                api = PlugchoiceApi(
                    session,
                    token,
                )

                await api.get_chargers()

            except aiohttp.ClientResponseError as err:

                if err.status in (401, 403):
                    errors["base"] = ERROR_AUTH
                else:
                    errors["base"] = ERROR_CONNECTION

            except aiohttp.ClientError:
                errors["base"] = ERROR_CONNECTION

            else:
                return self.async_create_entry(
                    title="Plugchoice",
                    data={
                        CONF_TOKEN: token,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TOKEN): str,
                }
            ),
            errors=errors,
        )