from typing import Dict, Optional, List, Any

from devices import BaseDevice, DeviceFactory
from pairing_repository import PairingRepository


class DeviceRepository:

    def __init__(self):
        self._devices: Dict[str, BaseDevice] = {}

    def get_device(self, device_id: str) -> Optional[BaseDevice]:
        return self._devices.get(device_id)

    def create(self, device: BaseDevice) -> BaseDevice:
        self._devices[device.get_id()] = device
        return device

    def delete(self, device_id: str) -> bool:
        del self._devices[device_id]
        return True

    def list_devices(self) -> List[BaseDevice]:
        return list(self._devices.values())


class DeviceService:

    def __init__(
        self, device_repository: DeviceRepository, pairing_repo: PairingRepository
    ):
        self._device_repository = device_repository
        self._pairing_repo = pairing_repo

    def get_device(self, device_id: str) -> Optional[BaseDevice]:
        return self._device_repository.get_device(device_id)

    def create(self, device_type: str) -> Optional[BaseDevice]:
        device = DeviceFactory.create_device_from_string(device_type)
        if not device:
            return

        return self._device_repository.create(device)

    def delete(self, device_id: str) -> bool:
        device: BaseDevice = self.get_device(device_id)
        if not device:
            return False

        if self._pairing_repo.is_paired(device_id):  # TODO validate
            return False

        return self._device_repository.delete(device_id)

    def info(self, device_id: str) -> Optional[Dict[str, Any]]:
        device = self.get_device(device_id)
        return device.get_info() if device else None

    def modify(self, device_id: str, **kwargs) -> bool:
        device = self.get_device(device_id)
        return device.modify(**kwargs) if device else False

    def list_devices(self) -> List[BaseDevice]:
        return self._device_repository.list_devices()
