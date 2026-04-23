"""Config flow placeholder for e-Tende Intelligenti."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class ETendeIntelligentiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for e-Tende Intelligenti."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user step."""
        if user_input is not None:
            return self.async_create_entry(title="e-Tende Intelligenti", data={})

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
