"""Switch platform for e-Tende Intelligenti."""
from homeassistant.components.switch import SwitchEntity
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
    """Set up the switch platform."""
    controller = hass.data[DOMAIN][entry.entry_id]["controller"]
    name = entry.data.get(CONF_PROFILE_NAME) or entry.title or "e-Tende"

    async_add_entities([ETendeSwitch(controller, name, entry.entry_id)])


class ETendeSwitch(SwitchEntity):
    """Switch to enable/disable the automatic control."""

    _attr_has_entity_name = True
    _attr_name = "Automazione"
    _attr_icon = "mdi:robot-window"

    def __init__(self, controller, profile_name, entry_id):
        """Initialize the switch."""
        self._controller = controller
        self._attr_unique_id = f"{entry_id}_switch_auto"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=profile_name,
            manufacturer="EA SAS",
            model="Gestione Tenda Intelligente",
        )

    @property
    def is_on(self) -> bool:
        """Return True if the automation is enabled."""
        return self._controller.cfg.enabled

    async def async_turn_on(self, **kwargs) -> None:
        """Enable the automatic control."""
        self._controller.cfg.enabled = True
        self.async_write_ha_state()
        await self._controller.async_apply_now()

    async def async_turn_off(self, **kwargs) -> None:
        """Disable the automatic control."""
        self._controller.cfg.enabled = False
        self.async_write_ha_state()

