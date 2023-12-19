"""Config flow for ROMY integration."""
from __future__ import annotations

from typing import Any

import romy
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import zeroconf
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, LOGGER


def _schema_with_host() -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_HOST): cv.string,
        },
    )


def _schema_with_password() -> vol.Schema:
    return vol.Schema(
        {vol.Required(CONF_PASSWORD): vol.All(cv.string, vol.Length(8))},
    )


class RomyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for ROMY."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self) -> None:
        """Handle a config flow for ROMY."""
        self.host: str = ""
        self.password: str = ""
        self.robot_name_given_by_user: str = ""

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Handle the user step."""
        errors: dict[str, str] = {}

        if user_input:
            self.host = user_input[CONF_HOST]

            new_romy = await romy.create_romy(self.host, "")

            if not new_romy.is_initialized:
                errors[CONF_HOST] = "cannot_connect"
            else:
                await self.async_set_unique_id(new_romy.unique_id)
                self._abort_if_unique_id_configured()

                self.robot_name_given_by_user = new_romy.user_name

                if not new_romy.is_unlocked:
                    return await self.async_step_password()
                return await self._async_step_finish_config()

        return self.async_show_form(
            step_id="user", data_schema=_schema_with_host(), errors=errors
        )

    async def async_step_password(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Unlock the robots local http interface with password."""
        errors: dict[str, str] = {}

        if user_input:
            self.password = user_input[CONF_PASSWORD]
            new_romy = await romy.create_romy(self.host, self.password)

            if not new_romy.is_initialized:
                errors[CONF_HOST] = "cannot_connect"
                return self.async_show_form(
                    step_id="user", data_schema=_schema_with_host(), errors=errors
                )

            if not new_romy.is_unlocked:
                errors[CONF_PASSWORD] = "invalid_auth"

            if not errors:
                return await self._async_step_finish_config()

        return self.async_show_form(
            step_id="password", data_schema=_schema_with_password(), errors=errors
        )

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle zeroconf discovery."""

        LOGGER.debug("Zeroconf discovery_info: %s", discovery_info)

        # connect and gather information from your ROMY
        self.host = discovery_info.host
        LOGGER.debug("ZeroConf Host: %s", self.host)

        new_discovered_romy = await romy.create_romy(self.host, "")

        self.robot_name_given_by_user = new_discovered_romy.user_name
        LOGGER.debug("ZeroConf Name: %s", self.robot_name_given_by_user)

        # get unique id and stop discovery if robot is already added
        unique_id = new_discovered_romy.unique_id
        LOGGER.debug("ZeroConf Unique_id: %s", unique_id)
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured(updates={CONF_HOST: discovery_info.host})

        self.context.update(
            {
                "title_placeholders": {
                    "name": f"{self.robot_name_given_by_user} ({self.host} / {unique_id})"
                },
                "configuration_url": f"http://{self.host}:{new_discovered_romy.port}",
            }
        )

        # if robot got already unlocked with password add it directly
        if not new_discovered_romy.is_initialized:
            return self.async_abort(reason="cannot_connect")

        if new_discovered_romy.is_unlocked:
            return await self.async_step_zeroconf_confirm()

        return await self.async_step_password()

    async def async_step_zeroconf_confirm(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Handle a confirmation flow initiated by zeroconf."""
        if user_input is None:
            return self.async_show_form(
                step_id="zeroconf_confirm",
                description_placeholders={
                    "name": self.robot_name_given_by_user,
                    "host": self.host,
                },
            )
        return await self._async_step_finish_config()

    async def _async_step_finish_config(self) -> FlowResult:
        """Finish the configuration setup."""
        return self.async_create_entry(
            title=self.robot_name_given_by_user,
            data={
                CONF_HOST: self.host,
                CONF_PASSWORD: self.password,
            }
        )
