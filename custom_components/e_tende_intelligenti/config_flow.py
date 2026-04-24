"""Config flow for e-Tende Intelligenti."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import selector

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
    CONF_PROFILE_NAME,
    CONF_SUNSET_POSITION,
    CONF_WINDOW_AZIMUTH,
    DOMAIN,
)

# HA moved to OptionsFlowWithConfigEntry in newer releases.
_BaseOptionsFlow = getattr(config_entries, "OptionsFlowWithConfigEntry", config_entries.OptionsFlow)


def _as_float(value: Any, default: float) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: int) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _as_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _cover_key(current: dict[str, Any]) -> vol.Required:
    c = current.get(CONF_COVER_ENTITY)
    if isinstance(c, str) and c:
        return vol.Required(CONF_COVER_ENTITY, default=c)
    return vol.Required(CONF_COVER_ENTITY)


def _full_schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    d = defaults or {}
    return vol.Schema(
        {
            _cover_key(d): selector({"entity": {"domain": "cover"}}),
            vol.Optional(CONF_PROFILE_NAME, default=str(d.get(CONF_PROFILE_NAME) or "")): selector({"text": {}}),
            vol.Required(CONF_WINDOW_AZIMUTH, default=_as_float(d.get(CONF_WINDOW_AZIMUTH), 180.0)): selector({"number": {"min": 0, "max": 360, "step": 1, "mode": "box"}}),
            vol.Required(CONF_FOV_LEFT, default=_as_float(d.get(CONF_FOV_LEFT), 70.0)): selector({"number": {"min": 0, "max": 180, "step": 1, "mode": "box"}}),
            vol.Required(CONF_FOV_RIGHT, default=_as_float(d.get(CONF_FOV_RIGHT), 70.0)): selector({"number": {"min": 0, "max": 180, "step": 1, "mode": "box"}}),
            vol.Required(CONF_MIN_ELEVATION, default=_as_float(d.get(CONF_MIN_ELEVATION), 8.0)): selector({"number": {"min": -10, "max": 90, "step": 1, "mode": "box"}}),
            vol.Required(CONF_MAX_ELEVATION, default=_as_float(d.get(CONF_MAX_ELEVATION), 65.0)): selector({"number": {"min": -10, "max": 90, "step": 1, "mode": "box"}}),
            vol.Required(CONF_DEFAULT_POSITION, default=_as_int(d.get(CONF_DEFAULT_POSITION), 100)): selector({"number": {"min": 0, "max": 100, "step": 1, "mode": "slider"}}),
            vol.Required(CONF_SUNSET_POSITION, default=_as_int(d.get(CONF_SUNSET_POSITION), 0)): selector({"number": {"min": 0, "max": 100, "step": 1, "mode": "slider"}}),
            vol.Required(CONF_MIN_POSITION, default=_as_int(d.get(CONF_MIN_POSITION), 0)): selector({"number": {"min": 0, "max": 100, "step": 1, "mode": "slider"}}),
            vol.Required(CONF_MAX_POSITION, default=_as_int(d.get(CONF_MAX_POSITION), 100)): selector({"number": {"min": 0, "max": 100, "step": 1, "mode": "slider"}}),
            vol.Required(CONF_MIN_DELTA, default=_as_int(d.get(CONF_MIN_DELTA), 3)): selector({"number": {"min": 0, "max": 100, "step": 1, "mode": "box"}}),
            vol.Required(CONF_INTERVAL_MINUTES, default=_as_int(d.get(CONF_INTERVAL_MINUTES), 5)): selector({"number": {"min": 1, "max": 120, "step": 1, "mode": "box"}}),
            vol.Required(CONF_ENABLED, default=_as_bool(d.get(CONF_ENABLED), True)): selector({"boolean": {}}),
        }
    )


class ETendeIntelligentiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        return ETendeIntelligentiOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            cover_id = user_input[CONF_COVER_ENTITY]
            profile_name = (user_input.get(CONF_PROFILE_NAME) or "").strip()
            if not profile_name:
                st = self.hass.states.get(cover_id)
                profile_name = st.attributes.get("friendly_name") if st else cover_id
            return self.async_create_entry(title=f"e-Tende {profile_name}", data=user_input)

        return self.async_show_form(step_id="user", data_schema=_full_schema())


class ETendeIntelligentiOptionsFlow(_BaseOptionsFlow):
    """Complete and stable options flow."""

    def __init__(self, config_entry) -> None:
        # Keep explicit reference for HA versions where OptionsFlow doesn't expose config_entry.
        self._config_entry = config_entry

    @property
    def _entry(self):
        return getattr(self, "config_entry", self._config_entry)

    async def async_step_init(self, user_input=None):
        current = {**self._entry.data, **self._entry.options}

        if user_input is not None:
            # Complete merge so old keys never disappear.
            merged = {**current, **user_input}
            return self.async_create_entry(title="", data=merged)

        return self.async_show_form(step_id="init", data_schema=_full_schema(current))
