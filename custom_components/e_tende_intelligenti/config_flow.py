"""Config flow for e-Tende Intelligenti."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_COVER_ENTITY,
    CONF_DEFAULT_POSITION,
    CONF_ENABLED,
    CONF_FOV_LEFT,
    CONF_FOV_RIGHT,
    CONF_INTERVAL_MINUTES,
    CONF_MAX_ELEVATION,
    CONF_MAX_POSITION,
    CONF_MIN_DELTA,
    CONF_MIN_ELEVATION,
    CONF_MIN_POSITION,
    CONF_SUNSET_POSITION,
    CONF_WINDOW_AZIMUTH,
    DOMAIN,
)


def _schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    d = defaults or {}
    return vol.Schema(
        {
            vol.Required(CONF_COVER_ENTITY, default=d.get(CONF_COVER_ENTITY, "cover.")): cv.entity_id,
            vol.Required(CONF_WINDOW_AZIMUTH, default=d.get(CONF_WINDOW_AZIMUTH, 180.0)): vol.Coerce(float),
            vol.Required(CONF_FOV_LEFT, default=d.get(CONF_FOV_LEFT, 70.0)): vol.Coerce(float),
            vol.Required(CONF_FOV_RIGHT, default=d.get(CONF_FOV_RIGHT, 70.0)): vol.Coerce(float),
            vol.Required(CONF_MIN_ELEVATION, default=d.get(CONF_MIN_ELEVATION, 8.0)): vol.Coerce(float),
            vol.Required(CONF_MAX_ELEVATION, default=d.get(CONF_MAX_ELEVATION, 65.0)): vol.Coerce(float),
            vol.Required(CONF_DEFAULT_POSITION, default=d.get(CONF_DEFAULT_POSITION, 100)): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            vol.Required(CONF_SUNSET_POSITION, default=d.get(CONF_SUNSET_POSITION, 0)): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            vol.Required(CONF_MIN_POSITION, default=d.get(CONF_MIN_POSITION, 0)): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            vol.Required(CONF_MAX_POSITION, default=d.get(CONF_MAX_POSITION, 100)): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            vol.Required(CONF_MIN_DELTA, default=d.get(CONF_MIN_DELTA, 3)): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            vol.Required(CONF_INTERVAL_MINUTES, default=d.get(CONF_INTERVAL_MINUTES, 5)): vol.All(vol.Coerce(int), vol.Range(min=1, max=120)),
            vol.Required(CONF_ENABLED, default=d.get(CONF_ENABLED, True)): bool,
        }
    )


class ETendeIntelligentiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for e-Tende Intelligenti."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        return ETendeIntelligentiOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle user step."""
        if user_input is not None:
            return self.async_create_entry(
                title=f"e-Tende {user_input[CONF_COVER_ENTITY]}",
                data=user_input,
            )

        return self.async_show_form(step_id="user", data_schema=_schema())


class ETendeIntelligentiOptionsFlow(config_entries.OptionsFlow):
    """Handle options for existing entry."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(step_id="init", data_schema=_schema(current))
