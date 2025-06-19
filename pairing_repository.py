from typing import Dict


class PairingRepository:

    def __init__(self):
        self._device_to_hub: Dict[str, str] = {}
        self._hub_to_devices: Dict[str, set[str]] = {}

    def pair(self, device_id: str, hub_id: str) -> bool:
        if self.is_paired(device_id):
            return False

        self._device_to_hub[device_id] = hub_id

        if hub_id not in self._hub_to_devices:
            self._hub_to_devices[hub_id] = set()

        self._hub_to_devices[hub_id].add(device_id)
        return True

    def unpair(self, device_id: str) -> bool:
        hub_id = self._device_to_hub.pop(device_id, None)
        if not hub_id:
            return False

        self._hub_to_devices[hub_id].discard(device_id)
        return True

    def is_paired(self, device_id: str) -> bool:
        return device_id in self._device_to_hub

    def get_devices_for_hub(self, hub_id: str) -> list[str]:
        return list(self._hub_to_devices.get(hub_id, set()))
