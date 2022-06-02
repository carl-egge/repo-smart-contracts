from abc import abstractmethod
from typing import List

from app.db.models import ContractDB, OID


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
    async def get_contracts(self) -> List[ContractDB]:
        pass

    @abstractmethod
    async def get_contract(self, contract_id: OID) -> ContractDB:
        pass

    @abstractmethod
    async def add_contract(self, contract: ContractDB):
        pass

    @abstractmethod
    async def update_contract(self, contract_id: OID, contract: ContractDB):
        pass

    @abstractmethod
    async def delete_contract(self, contract_id: OID):
        pass
