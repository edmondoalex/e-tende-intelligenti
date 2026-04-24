"""Sensor platform for e-Tende Intelligenti."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, CONF_PROFILE_NAME

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    controller = hass.data[DOMAIN][entry.entry_id]["controller"]
    name = entry.data.get(CONF_PROFILE_NAME) or entry.title or "e-Tende"

    async_add_entities([ETendeStatusSensor(controller, name, entry.entry_id)])


class ETendeStatusSensor(SensorEntity):
    """Sensor to display the calculated position."""

    _attr_has_entity_name = True
    _attr_name = "Posizione Calcolata"
    _attr_icon = "mdi:sun-compass"
    _attr_native_unit_of_measurement = "%"

    def __init__(self, controller, profile_name, entry_id):
        """Initialize the sensor."""
        self._controller = controller
        self._attr_unique_id = f"{entry_id}_sensor_target_pos"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=profile_name,
            manufacturer="EA SAS",
            model="Gestione Tenda Intelligente",
        )

    @property
    def native_value(self) -> int | None:
        """Return the last calculated target position."""
        return self._controller._runtime.get("last_target_position")

    async def async_update(self):
        """Update sensor from the controller runtime state."""
        # Il coordinator salva il calcolo nel dizionario runtime e poi potremmo forzare l'aggiornamento
        pass
