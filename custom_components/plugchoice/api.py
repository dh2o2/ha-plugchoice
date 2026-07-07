"""Plugchoice API client."""

from __future__ import annotations

import aiohttp

from .const import BASE_URL


class PlugchoiceApi:
    """Client for Plugchoice API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token: str,
    ) -> None:
        """Initialize the API client."""

        self._session = session
        self._token = token

        self._headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

    async def get_chargers(self) -> list[dict]:
        """Get chargers list."""

        url = f"{BASE_URL}/chargers"

        async with self._session.get(
            url,
            headers=self._headers,
        ) as response:

            response.raise_for_status()

            data = await response.json()

            return data["data"]