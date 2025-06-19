from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from enum import Enum
from uuid import uuid4


class DeviceType(Enum):
    SWITCH = "switch"
    DIMMER = "dimmer"
    LOCK = "lock"
    THERMOSTAT = "thermostat"


class DeviceState(Enum):
    ON = "on"
    OFF = "off"
    LOCKED = "locked"
    UNLOCKED = "unlocked"


class BaseDevice(ABC):

    def __init__(self, device_type: DeviceType):
        self._id = str(uuid4())
        self._type = device_type

    def _info(self) -> Dict[str, Any]:
        return {
            "id": self._id,
            "type": self._type.value,
        }

    def get_id(self) -> str:
        return self._id

    @abstractmethod
    def get_info(self) -> bool:
        pass

    @abstractmethod
    def modify(self) -> bool:
        pass


class Switch(BaseDevice):

    def __init__(self):
        super().__init__(DeviceType.SWITCH)
        self._state = DeviceState.OFF.value

    def get_info(self) -> dict:
        info = super()._info()
        info["state"] = self._state
        return info

    def modify(self, **kwargs) -> bool:
        state = kwargs.get("state")
        if state in [DeviceState.OFF.value, DeviceState.ON.value]:
            self._state = state
            return True
        return False


class Dimmer(BaseDevice):

    def __init__(self):
        super().__init__(DeviceType.DIMMER)
        self._brightness = 0

    def get_info(self) -> Dict[str, Any]:
        info = super()._info()
        info["brightness"] = self._brightness
        return info

    def modify(self, **kwargs) -> bool:
        value = kwargs.get("brightness")
        if isinstance(value, int) and 0 <= value <= 100:
            self._brightness = value
            return True
        return False


class Lock(BaseDevice):

    def __init__(self):
        super().__init__(DeviceType.LOCK)
        self._state = DeviceState.LOCKED.value
        self._pin_code = None

    def get_info(self) -> Dict[str, Any]:
        info = super()._info()
        info.update({"state": self._state, "has_pin": self._pin_code is not None})
        return info

    def modify(self, **kwargs) -> bool:
        modified = False
        state = kwargs.get("state")
        if state in [DeviceState.LOCKED.value, DeviceState.UNLOCKED.value]:
            self._state = state
            modified = True

        pin_code = kwargs.get("pin_code")
        if pin_code:
            self._pin_code = pin_code
            modified = True

        return modified


class Thermostat(BaseDevice):

    def __init__(self):
        super().__init__(DeviceType.THERMOSTAT)
        self._temperature = 20

    def get_info(self) -> Dict[str, Any]:
        info = super()._info()
        info["temperature"] = self._temperature
        return info

    def modify(self, **kwargs) -> bool:
        temperature = kwargs.get("temperature")
        if isinstance(temperature, (int, float)) and 0 <= temperature <= 40:
            self._temperature = temperature
            return True
        return False


class DeviceFactory:

    @staticmethod
    def _create_device(device_type: DeviceType) -> Optional[BaseDevice]:
        device_map = {
            DeviceType.SWITCH: Switch,
            DeviceType.DIMMER: Dimmer,
            DeviceType.LOCK: Lock,
            DeviceType.THERMOSTAT: Thermostat,
        }
        device_class = device_map.get(device_type)
        if device_class:
            return device_class()
        return None

    @staticmethod
    def create_device_from_string(device_type_str: str) -> Optional[BaseDevice]:
        try:
            device_type = DeviceType(device_type_str.lower())
            return DeviceFactory._create_device(device_type)
        except ValueError:
            return None
