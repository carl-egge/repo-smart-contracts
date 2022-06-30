from datetime import datetime
import logging
import re
from turtle import title
from typing import List, Union
from xmlrpc.client import DateTime

from fastapi import HTTPException
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.db import DatabaseManager
from app.db.models import ContractDB, OID, ContractIn, ContractPatch


class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    #
    # DB: database connection is opened
    #
    async def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10)
        self.db = self.client.main_db
        logging.info("Connected to MongoDB.")

    #
    # DB : database connection is closed
    #
    async def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")

    #
    # READS : all contracts from the database are returned in an array
    #
    async def get_contracts(self) -> List[ContractDB]:
        contracts_list = []
        contracts_q = self.db.contracts.find()
        async for contract in contracts_q:
            contracts_list.append(ContractDB(**contract, id=contract['_id']))
        return contracts_list

    #
    # READ : a single contract or one version of its code is returned
    #
    async def get_contract(self, contract_id: OID, version_id: Union[int, None]):
        contract_q = await self.db.contracts.find_one({'_id': ObjectId(contract_id)})
        if contract_q:
            if version_id == None:
                return ContractDB(**contract_q, id=contract_q['_id'])
            if version_id <= 0 or version_id > contract_q["latest_version"]:
                raise HTTPException(status_code=404, detail="Version number is out of range")
            else:
                return contract_q["versions"][version_id-1]["content"]
               

    #
    # DELETE : a contract is deleted from the database
    #
    async def delete_contract(self, contract_id: OID, version_id: Union[int, None]):
        contract_q = await self.db.contracts.find_one({'_id': ObjectId(contract_id)})
        # check if contract exists
        if contract_q == None:
            raise HTTPException(status_code=404, detail="Contract Id not found")
        else:
            # check if version id is given and valid
            if version_id != None and (version_id <= 0 or version_id > contract_q["latest_version"]):
                raise HTTPException(status_code=404, detail="Version number is out of range")
            elif version_id == None or contract_q["latest_version"] == 1:
                await self.db.contracts.delete_one({'_id': ObjectId(contract_id)})
                return
            else:
                # decrement latest_version and remove version from array
                await self.db.contracts.update_one( {'_id': ObjectId(contract_id)},
                                                    {
                                                        "$inc": {
                                                            "latest_version": -1
                                                        },
                                                        "$pull": {
                                                            "versions": { "vid": version_id } 
                                                        },
                                                    }
                                                )
                # update all version ids in the array
                await self.db.contracts.update_one( {'_id': ObjectId(contract_id)},
                                                    {
                                                        "$inc": { 
                                                            "versions.$[elem].vid" : -1 
                                                        }
                                                    },
                                                    array_filters=[ 
                                                        { "elem.vid": { "$gte": version_id } }
                                                    ]
                                                )


    #
    # UPDATE : title and description is updated, new version of code is added
    #
    async def update_contract(self, contract_id: OID, contract: ContractPatch):
        contract_q = await self.db.contracts.find_one({'_id': ObjectId(contract_id)})
        new_vid = contract_q["latest_version"] + 1
        # if some fields are not send in the body we want to keep the values from the last version
        new_title = contract.title if contract.title else contract_q["title"]
        new_description = contract.description if contract.description else contract_q["description"]
        new_created = contract.created if contract.created else datetime.utcnow()
        new_parents = contract.parents if contract.parents else [contract_q["latest_version"]]
        new_sourcecode = contract.sourcecode if contract.sourcecode else contract_q["versions"][new_vid-2]["content"]["sourcecode"]
        new_bytecode = contract.bytecode if contract.bytecode else contract_q["versions"][new_vid-2]["content"]["bytecode"]
        new_abi = contract.abi if contract.abi else contract_q["versions"][new_vid-2]["content"]["abi"]
        new_pragma = self.get_compiler_version(contract.sourcecode) if contract.sourcecode else contract_q["versions"][new_vid-2]["content"]["compilerversion"]
        await self.db.contracts.update_one( {'_id': ObjectId(contract_id)},
                                            {
                                               "$set": {
                                                    "title": new_title,
                                                    "description": new_description
                                                },
                                                "$inc": {
                                                    "latest_version": 1
                                                },
                                                "$push": {
                                                    "versions": { 
                                                        "vid": new_vid,
                                                        "message": contract.message,
                                                        "created": new_created,
                                                        "parents": new_parents,
                                                        "content": {
                                                            "compilerversion": new_pragma,
                                                            "sourcecode": new_sourcecode,
                                                            "bytecode": new_bytecode,
                                                            "abi": new_abi
                                                        }
                                                    }
                                                }
                                            })
        res = await self.db.contracts.find_one({'_id': ObjectId(contract_id)})
        return ContractDB(**res, id=contract_q['_id'])

    #
    # INSERT : insert a new contract in the database
    #
    async def add_contract(self, contract: ContractIn):
        pragma = self.get_compiler_version(contract.sourcecode) if contract.sourcecode else None
        created = contract.created if contract.created else datetime.utcnow()
        new =   await self.db.contracts.insert_one(
                    { 
                        "title": contract.title,
                        "description": contract.description,
                        "source": contract.source,
                        "source_file_path": contract.source_file_path,
                        "latest_version": 1,
                        "versions": [
                            { 
                                "vid": 1,
                                "message": "Initial commit",
                                "created": created,
                                "parents": [],
                                "content": {
                                    "compilerversion": pragma,
                                    "sourcecode": contract.sourcecode,
                                    "bytecode": contract.bytecode,
                                    "abi": contract.abi
                                }
                            }
                        ]
                    }
                )
        res = await self.db.contracts.find_one({'_id': ObjectId(new.inserted_id)})
        return ContractDB(**res, id=res['_id'])

    #
    # Helperfunctions
    #
    def get_compiler_version(self, code):
        check_version = re.search(r'pragma solidity [<>^]?=?\s*([\d.]+)', code)
        if (check_version):
            return check_version.group(1)
        else:
            return None