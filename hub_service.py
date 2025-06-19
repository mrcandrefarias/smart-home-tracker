from typing import Optional, Dict, List, Any
from uuid import uuid4

from pairing_repository import PairingRepository
from device_service import DeviceService
from devices import BaseDevice


class Hub:

    def __init__(self):
        self._id = str(uuid4())

    def get_id(self):
        return self._id


class HubRepository:

    def __init__(self):
        self._hubs: Dict[str, Hub] = {}

    def create(self, hub: Hub) -> Hub:
        self._hubs[hub.get_id()] = hub
        return hub

    def get_hub(self, hub_id: str) -> Optional[Hub]:
        return self._hubs.get(hub_id)


class HubService:

    def __init__(
        self,
        hub_repository: HubRepository,
        pairing_repository: PairingRepository,
        device_service: DeviceService,
    ):
        self._hub_repository = hub_repository
        self._device_service = device_service
        self._pairing_repository = pairing_repository

    def create(self) -> Hub:
        return self._hub_repository.create(Hub())

    def get_hub(self, id: str) -> Hub:
        return self._hub_repository.get_hub(id)

    def pair_device_to_hub(self, hub_id: str, device_id: str) -> bool:
        device = self._device_service.get_device(device_id)
        if not device:
            return False  # device not found

        hub = self.get_hub(hub_id)
        if not hub:
            return False  # hub not found

        return self._pairing_repository.pair(device_id, hub_id)

    def remove_device_from_hub(self, device_id: str) -> bool:
        return self._pairing_repository.unpair(device_id)

    def device_info(self, device_id: str) -> Optional[Dict[str, Any]]:
        if self._pairing_repository.is_paired(device_id):
            return False

        return self._device_service.info(device_id)

    def list_devices(self, hub_id: str) -> List[BaseDevice]:
        return [
            self._device_service.get_device(id)
            for id in self._pairing_repository.get_devices_for_hub(hub_id)
        ]
