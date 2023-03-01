from abc import abstractmethod
from typing import List, Union

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
    async def get_contracts(self, name, language, license, sha, repo, owner, versionsAmount, pragma, size, limit, skip) -> List[ContractDB]:
        pass

    @abstractmethod
    async def count_database(self) -> int:
        pass

    @abstractmethod
    async def count_contracts(self, name, language, license, sha, repo, owner, versionsAmount, pragma, size) -> int:
        pass

    @abstractmethod
    async def get_contract(self, contract_id: OID, version_id: Union[int, None]):
        pass
