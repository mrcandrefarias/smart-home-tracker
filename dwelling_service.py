from typing import Dict, Optional, List
from uuid import uuid4


class Dwelling:

    def __init__(self):
        self._id = str(uuid4())
        self._occupied = False
        self._hub_id = None

    def get_id(self) -> str:
        return self._id

    def set_occupied(self, occupied: bool) -> None:
        self._occupied = occupied
        return True

    def install_hub(self, hub_id: str) -> bool:
        self._hub_id = hub_id
        return True


class DwellingRepo:

    def __init__(self):
        self._dwellings: Dict[str, Dwelling] = {}

    def create(self, dwelling: Dwelling):
        self._dwellings[dwelling.get_id()] = dwelling
        return dwelling

    def get_dwelling(self, id: str) -> Optional[Dwelling]:
        return self._dwellings.get(id)

    def list_dwellings(self) -> List[Dwelling]:
        return list(self._dwellings.values())


class DwellingService:

    def __init__(self, dwelling_repo: DwellingRepo):
        self._dwelling_repo = dwelling_repo

    def create_dwelling(self) -> Optional[Dwelling]:
        return self._dwelling_repo.create(Dwelling())

    def occupied(self, dwelling_id: str) -> bool:
        dwelling = self._dwelling_repo.get_dwelling(dwelling_id)
        return dwelling.set_occupied(True) if dwelling else False

    def vacant(self, dwelling_id: str) -> bool:
        dwelling = self._dwelling_repo.get_dwelling(dwelling_id)
        return dwelling.set_occupied(False) if dwelling else False

    def install_hub(self, dwelling_id: str, hub_id: str) -> bool:
        dwelling = self._dwelling_repo.get_dwelling(dwelling_id)
        return dwelling.install_hub(hub_id) if dwelling else False

    def list_dwellings(self) -> List[Dwelling]:
        return self._dwelling_repo.list_dwellings()
