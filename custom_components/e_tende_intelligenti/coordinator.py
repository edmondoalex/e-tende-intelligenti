"""Core controller for e-Tende Intelligenti."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.storage import Store

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
)

_LOGGER = logging.getLogger(__name__)
_STORAGE_VERSION = 1


@dataclass
class ETendeConfig:
    """Runtime configuration for one managed cover."""

    cover_entity: str
    window_azimuth: float
    fov_left: float
    fov_right: float
    min_elevation: float
    max_elevation: float
    default_position: int
    sunset_position: int
    min_position: int
    max_position: int
    min_delta: int
    interval_minutes: int
    enabled: bool


class ETendeCoverController:
    """Manage a single cover with sun-aware logic."""

    def __init__(self, hass: HomeAssistant, entry_id: str, cfg: ETendeConfig) -> None:
        self.hass = hass
        self.entry_id = entry_id
        self.cfg = cfg
        self._unsub_interval = None
        self._store = Store(hass, _STORAGE_VERSION, f"e_tende_intelligenti.{entry_id}")
        self._runtime: dict[str, Any] = {
            "last_target_position": None,
            "last_apply_at": None,
        }

    async def async_start(self) -> None:
        """Start periodic execution."""
        saved = await self._store.async_load()
        if isinstance(saved, dict):
            self._runtime.update(saved)

        interval = timedelta(minutes=max(1, int(self.cfg.interval_minutes)))

        async def _tick(_now) -> None:
            await self.async_apply_now()

        self._unsub_interval = async_track_time_interval(self.hass, _tick, interval)
        await self.async_apply_now()

    async def async_stop(self) -> None:
        """Stop periodic execution."""
        if self._unsub_interval is not None:
            self._unsub_interval()
            self._unsub_interval = None
        await self._store.async_save(self._runtime)

    async def async_apply_now(self) -> None:
        """Compute and apply target position now."""
        if not self.cfg.enabled:
            return

        target = self._calculate_target_position()
        if target is None:
            return

        state = self.hass.states.get(self.cfg.cover_entity)
        if state is None:
            _LOGGER.warning("Cover entity not found: %s", self.cfg.cover_entity)
            return

        current = self._safe_int(state.attributes.get("current_position"))
        if current is not None and abs(current - target) < self.cfg.min_delta:
            self._runtime["last_target_position"] = target
            self._runtime["last_apply_at"] = datetime.utcnow().isoformat()
            await self._store.async_save(self._runtime)
            return

        await self.hass.services.async_call(
            "cover",
            "set_cover_position",
            {"entity_id": self.cfg.cover_entity, "position": target},
            blocking=False,
        )

        self._runtime["last_target_position"] = target
        self._runtime["last_apply_at"] = datetime.utcnow().isoformat()
        await self._store.async_save(self._runtime)

    def _calculate_target_position(self) -> int | None:
        """Compute target position based on current sun state and config."""
        sun = self.hass.states.get("sun.sun")
        if sun is None:
            return None

        if sun.state == "below_horizon":
            return self._clamp_position(self.cfg.sunset_position)

        azimuth = self._safe_float(sun.attributes.get("azimuth"))
        elevation = self._safe_float(sun.attributes.get("elevation"))

        if azimuth is None or elevation is None:
            return self._clamp_position(self.cfg.default_position)

        in_front = self._is_sun_in_front(azimuth)
        in_elevation = self.cfg.min_elevation <= elevation <= self.cfg.max_elevation

        if not in_front or not in_elevation:
            return self._clamp_position(self.cfg.default_position)

        # Se c'è il sole sulla finestra, la tapparella deve essere tutta chiusa
        return self._clamp_position(self.cfg.min_position)

    def _is_sun_in_front(self, sun_azimuth: float) -> bool:
        """Check if sun is inside the window field-of-view."""
        center = self.cfg.window_azimuth % 360
        diff = self._smallest_angle_diff(center, sun_azimuth % 360)
        return (-self.cfg.fov_left) <= diff <= self.cfg.fov_right

    @staticmethod
    def _smallest_angle_diff(a: float, b: float) -> float:
        """Return signed shortest angle difference b-a in degrees."""
        return ((b - a + 180) % 360) - 180

    def _clamp_position(self, value: int) -> int:
        """Clamp position between min and max bounds."""
        low = min(self.cfg.min_position, self.cfg.max_position)
        high = max(self.cfg.min_position, self.cfg.max_position)
        return max(low, min(high, int(value)))

    @staticmethod
    def _safe_float(value: Any) -> float | None:
        """Safely cast any value to float."""
        try:
            if value is None:
                return None
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _safe_int(value: Any) -> int | None:
        """Safely cast any value to int."""
        try:
            if value is None:
                return None
            return int(float(value))
        except (TypeError, ValueError):
            return None


def build_config(data: dict[str, Any]) -> ETendeConfig:
    """Build typed config from entry data/options."""
    return ETendeConfig(
        cover_entity=data[CONF_COVER_ENTITY],
        window_azimuth=float(data[CONF_WINDOW_AZIMUTH]),
        fov_left=float(data[CONF_FOV_LEFT]),
        fov_right=float(data[CONF_FOV_RIGHT]),
        min_elevation=float(data[CONF_MIN_ELEVATION]),
        max_elevation=float(data[CONF_MAX_ELEVATION]),
        default_position=int(data[CONF_DEFAULT_POSITION]),
        sunset_position=int(data[CONF_SUNSET_POSITION]),
        min_position=int(data[CONF_MIN_POSITION]),
        max_position=int(data[CONF_MAX_POSITION]),
        min_delta=int(data[CONF_MIN_DELTA]),
        interval_minutes=int(data[CONF_INTERVAL_MINUTES]),
        enabled=bool(data[CONF_ENABLED]),
    )
