"""Component to allow timer_programmer support for platforms."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, final

import voluptuous as vol
from homeassistant.backports.enum import StrEnum
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_MODE
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.config_validation import (  # noqa: F401
    PLATFORM_SCHEMA, PLATFORM_SCHEMA_BASE)
from homeassistant.helpers.entity import Entity, EntityDescription
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.typing import ConfigType

from .const import (ATTR_BIT, ATTR_VALUE, DOMAIN, SERVICE_SET_VALUE,
                    SERVICE_TOGGLE_BIT, SERVICE_TURN_OFF_BIT,
                    SERVICE_TURN_ON_BIT)

SCAN_INTERVAL = timedelta(seconds=30)

ENTITY_ID_FORMAT = DOMAIN + ".{}"

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Timer Programmer entities."""
    component = hass.data[DOMAIN] = EntityComponent(
        _LOGGER, DOMAIN, hass, SCAN_INTERVAL
    )
    await component.async_setup(config)

    component.async_register_entity_service(
        SERVICE_SET_VALUE,
        {vol.Required(ATTR_VALUE): vol.Coerce(int)},
        async_set_value,
    )

    component.async_register_entity_service(
        SERVICE_TOGGLE_BIT,
        {vol.Required(ATTR_BIT): vol.Coerce(int)},
        async_toggle,
    )

    component.async_register_entity_service(
        SERVICE_TURN_OFF_BIT,
        {vol.Required(ATTR_BIT): vol.Coerce(int)},
        async_turn_off,
    )

    component.async_register_entity_service(
        SERVICE_TURN_ON_BIT,
        {vol.Required(ATTR_BIT): vol.Coerce(int)},
        async_turn_on,
    )

    return True


async def async_set_value(entity: TimerProgrammerEntity, service_call: ServiceCall) -> None:
    """Service call wrapper to set a new value."""
    value = service_call.data["value"]
    await entity.async_set_value(value)

async def async_toggle(entity: TimerProgrammerEntity, service_call: ServiceCall) -> None:
    """Service call wrapper to set a new value."""
    bit = service_call.data["bit"]
    await entity.async_toggle(bit)

async def async_turn_off(entity: TimerProgrammerEntity, service_call: ServiceCall) -> None:
    """Service call wrapper to set a new value."""
    bit = service_call.data["bit"]
    await entity.async_turn_off(bit)

async def async_turn_on(entity: TimerProgrammerEntity, service_call: ServiceCall) -> None:
    """Service call wrapper to set a new value."""
    bit = service_call.data["bit"]
    await entity.async_turn_on(bit)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    component: EntityComponent = hass.data[DOMAIN]
    return await component.async_setup_entry(entry)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    component: EntityComponent = hass.data[DOMAIN]
    return await component.async_unload_entry(entry)


@dataclass
class TimerProgrammerEntityDescription(EntityDescription):
    """A class that describes TimerProgrammer entities."""


class TimerProgrammerEntity(Entity):
    """Representation of a TimerProgrammer entity."""

    entity_description: TimerProgrammerEntityDescription
    _attr_state: None = None
    _attr_value: int

    @property
    @final
    def state(self) -> int | None:
        """Return the entity state."""
        return self.value

    @property
    def value(self) -> int | None:
        """Return the entity value to represent the entity state."""
        return self._attr_value

    def set_value(self, value: int) -> None:
        """Set new value."""
        raise NotImplementedError()

    def is_on(self, bit: int) -> bool:
      """Returns True if the corresponding bit is on."""
      mask = 2**bit
      return (self.value & mask) == mask

    async def async_set_value(self, value: int) -> None:
        """Set new value."""
        await self.hass.async_add_executor_job(self.set_value, value)

    def toggle(self, bit: int) -> None:
      """Toggle a bit status."""
      if self.is_on(bit):
        self.turn_off(bit)
      else:
        self.turn_on(bit)

    async def async_toggle(self, bit: int) -> None:
        """Set new value."""
        # await self.hass.async_add_executor_job(self.toggle, bit)
        if self.is_on(bit):
            await self.async_turn_off(bit)
        else:
            await self.async_turn_on(bit)

    def turn_off(self, bit: int) -> None:
        """Set new value."""
        raise NotImplementedError()

    async def async_turn_off(self, bit: int) -> None:
        """Set new value."""
        await self.hass.async_add_executor_job(self.turn_off, bit)

    def turn_on(self, bit: int) -> None:
        """Set new value."""
        raise NotImplementedError()

    async def async_turn_on(self, bit: int) -> None:
        """Set new value."""
        await self.hass.async_add_executor_job(self.turn_on, bit)
