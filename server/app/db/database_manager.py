from abc import abstractmethod
from typing import List, Union

from app.db.models import ContractDB, OID, ContractIn, ContractPatch


class DatabaseManager(object):
    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def connect_to_database(self, path: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def get_contracts(self, source_str) -> List[ContractDB]:
        pass

    @abstractmethod
    async def get_contract(self, contract_id: OID, version_id: Union[int, None]):
        pass

    @abstractmethod
    async def add_contract(self, contract: ContractIn) -> ContractDB:
        pass

    @abstractmethod
    async def update_contract(self, contract: ContractPatch, contract_id: OID) -> ContractDB:
        pass

    @abstractmethod
    async def delete_contract(contract_id: OID, version_id: Union[int, None]):
        pass
