import logging
from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.db import DatabaseManager
from app.db.models import ContractDB, OID


class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10)
        self.db = self.client.main_db
        logging.info("\n\n\n\n")
        logging.info(ContractDB.schema_json(indent=2))
        logging.info("\n\n\n\n")
        logging.info("Connected to MongoDB.")

    async def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")

    async def get_contracts(self) -> List[ContractDB]:
        contracts_list = []
        contracts_q = self.db.contracts.find()
        async for contract in contracts_q:
            contracts_list.append(ContractDB(**contract, id=contract['_id']))
        return contracts_list

    async def get_contract(self, contract_id: OID) -> ContractDB:
        contract_q = await self.db.contracts.find_one({'_id': ObjectId(contract_id)})
        if contract_q:
            return ContractDB(**contract_q, id=contract_q['_id'])

    async def delete_contract(self, contract_id: OID):
        await self.db.contracts.delete_one({'_id': ObjectId(contract_id)})

    async def update_contract(self, contract_id: OID, contract: ContractDB):
        await self.db.contracts.update_one({'_id': ObjectId(contract_id)},
                                       {'$set': contract.dict(exclude={'id'})})

    async def add_contract(self, contract: ContractDB):
        await self.db.contracts.insert_one(contract.dict(exclude={'id'}))
