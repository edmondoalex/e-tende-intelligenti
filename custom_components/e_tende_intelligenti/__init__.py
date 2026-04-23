"""e-Tende Intelligenti custom integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .const import ATTR_ENTRY_ID, DOMAIN, SERVICE_APPLY_NOW
from .coordinator import ETendeCoverController, build_config


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up integration from YAML (placeholder)."""
    hass.data.setdefault(DOMAIN, {})

    async def _handle_apply_now(call: ServiceCall) -> None:
        requested_entry = call.data.get(ATTR_ENTRY_ID)
        for entry_id, payload in hass.data.get(DOMAIN, {}).items():
            if requested_entry and requested_entry != entry_id:
                continue
            controller: ETendeCoverController | None = payload.get("controller")
            if controller is not None:
                await controller.async_apply_now()

    if not hass.services.has_service(DOMAIN, SERVICE_APPLY_NOW):
        hass.services.async_register(DOMAIN, SERVICE_APPLY_NOW, _handle_apply_now)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up e-Tende Intelligenti from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    merged: dict[str, Any] = {**entry.data, **entry.options}
    cfg = build_config(merged)

    controller = ETendeCoverController(hass, entry.entry_id, cfg)
    hass.data[DOMAIN][entry.entry_id] = {"controller": controller}

    await controller.async_start()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    payload = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if payload and payload.get("controller"):
        await payload["controller"].async_stop()

    if not hass.data.get(DOMAIN):
        if hass.services.has_service(DOMAIN, SERVICE_APPLY_NOW):
            hass.services.async_remove(DOMAIN, SERVICE_APPLY_NOW)

    return True
