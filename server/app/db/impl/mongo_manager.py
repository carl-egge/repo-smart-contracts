# from datetime import datetime
# from turtle import title
# from xmlrpc.client import DateTime
# from fastapi import HTTPException

import logging
import re
from typing import List, Union
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.db import DatabaseManager
from app.db.models import (
    ContractDB,
    OID,
    ErrorResponseModel
)


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
    # READ-Functions -----------------------------------------------------------------------
    #

    # READS : all contracts from the database are returned in an array
    async def get_contracts(
            self,
            name: Union[str, None],
            language: Union[str, None],
            license: Union[str, None],
            sha: Union[str, None],
            repo: Union[str, None],
            owner: Union[str, None],
            amountOfVersions: Union[int, None],
            pragma: Union[str, None],
            size: Union[str, None],
            searchAllVersions: bool,
            limit: int,
            skip: int,
            collection: str = 'contracts') -> List[ContractDB]:
        contracts_q = []
        # Create and run query
        query = self.construct_query_obj(name, language, license, sha, repo, owner, amountOfVersions, pragma, size, searchAllVersions)
        if query == 0:
            return []
        else:
            contracts_q = self.db[collection].find(query)
        # Pagination -----------> TODO: Add next link to response if result is paginated
        contracts_q.skip(skip).limit(limit)
        # Fix format and return contracts
        contracts_list = []
        async for contract in contracts_q:
            contracts_list.append(ContractDB(**contract, id=contract['_id']))
        return contracts_list

    # READ : a single contract or one version of its code is returned
    async def get_contract(self, contract_id: OID, version_id: Union[int, None], collection: str = 'contracts'):
        contract_q = await self.db[collection].find_one({'_id': ObjectId(contract_id)})
        if contract_q:
            if version_id == None:
                return ContractDB(**contract_q, id=contract_q['_id'])
            if version_id < 0 or version_id >= len(contract_q['versions']):
                return "version out of range"
            else:
                return contract_q["versions"][version_id]["content"]
            
    # Count all documents in database (estimation)
    async def count_database(self, collection: str = 'contacts') -> int:
        # using estimated_document_count instead of count_documents because its faster
        return await self.db[collection].estimated_document_count()
    
    # Count the documents in the result set of the given query parameters if any are not None
    async def count_contracts(
            self,
            name: Union[str, None],
            language: Union[str, None],
            license: Union[str, None],
            sha: Union[str, None],
            repo: Union[str, None],
            owner: Union[str, None],
            amountOfVersions: Union[int, None],
            pragma: Union[str, None],
            size: Union[str, None],
            searchAllVersions: bool,
            collection: str = 'contracts') -> int:
        query = self.construct_query_obj(name, language, license, sha, repo, owner, amountOfVersions, pragma, size, searchAllVersions)
        if query:
            return await self.db[collection].count_documents(query)
        return await self.db[collection].estimated_document_count()
               
    #
    # Helperfunctions -----------------------------------------------------------------------
    #

    # Construct query object from query parameters
    def construct_query_obj(
            self,
            name: Union[str, None],
            language: Union[str, None],
            license: Union[str, None],
            sha: Union[str, None],
            repo: Union[str, None],
            owner: Union[str, None],
            amountOfVersions: Union[int, None],
            pragma: Union[str, None],
            size: Union[str, None],
            searchAllVersions: bool = False
    ):
        # Collect filters from query parameters
        filters = []
        if name:
            filters.append({'name': {'$regex': f'.*{name}.*'}})
        if language:
            filters.append({'language': language})
        if license:
            # Check if this is a valid license short code from github
            if license in ['apache-2.0','agpl-3.0','bsd-2-clause','bsd-3-clause','bsl-1.0','mit',
                'cc0-1.0','epl-2.0','gpl-2.0','gpl-3.0','lgpl-2.1','mpl-2.0','unlicense']:
                filters.append({'license': license})
            else:
                return 0
        if sha:
            # using or to check for the contract sha and its commit shas
            filters.append({ '$or': [ { 'sha': sha }, { 'versions.sha': sha } ] })
        if repo:
            # the repo can be specified through a repo_id or a name
            if repo.isdigit():
                filters.append({ 'repo.repo_id': int(repo) })
            else:
                filters.append({'repo.full_name': {'$regex': f'.*{repo}.*'}})
        if owner:
            # the owner can be specified through a owner_id or a name
            if owner.isdigit():
                filters.append({ 'repo.owner_id': int(owner) })
            else:
                filters.append({'repo.full_name': {'$regex': f'.*{owner}.*'}})
        if amountOfVersions:
            filters.append({"versions": {"$size": amountOfVersions}})
        if pragma:
            # using regex to precheck if pragma is in the valid format of 0.0.0
            check_pragma = re.search(r'^(\d*)\.(\d*)\.(\d*)$', pragma)
            if check_pragma and searchAllVersions:
                filters.append({'versions.compiler_version': {'$regex': f'.*{pragma}.*'}})
            elif check_pragma:
                # using arrayElemAt to get the last element of the array
                filters.append({
                    "$expr": {
                        "$regexMatch": {
                            'input': { "$arrayElemAt": [ "$versions.compiler_version", -1 ] },
                            'regex': f'.*{pragma}.*'
                        }
                    }
                })
            else:
                return 0
        if size:
            # using regex to check if size is a digit, range of digits or non valid
            check_range = re.search(r'^(.*)\.[\.+](.*)$', size)
            if size.isdigit():
                if searchAllVersions:
                    filters.append({'versions.size': int(size)})
                else:
                    filters.append({ "$expr": { "$eq": [{ "$arrayElemAt": [ "$versions.size", -1 ] }, int(size)] }})
            elif check_range and check_range.group(1).isdigit() and check_range.group(2).isdigit() and check_range.group(1) < check_range.group(2):
                if searchAllVersions:
                    # The first approach will filter the entire array at the same time and therefore have wrong results
                    # filters.append({'versions.size': { '$gte': int(check_range.group(1)), '$lte': int(check_range.group(2))}})
                    # This approach will exclude all contracts that have a size that is out of range
                    filters.append({'versions': {'$not': {'$elemMatch': {'$or': [
                        {'size': {'$lt': int(check_range.group(1))}},
                        {'size': {'$gt': int(check_range.group(2))}}
                    ]}}}})
                else:
                    filters.append({ "$expr": { "$gte": [{ "$arrayElemAt": [ "$versions.size", -1 ] }, int(check_range.group(1))]} })
                    filters.append({ "$expr": { "$lte": [{ "$arrayElemAt": [ "$versions.size", -1 ] }, int(check_range.group(2))]} })
            else:
                return 0
        # Check if filter exist
        if filters:
            return {'$and': filters}
        else:
            return {}

    # Extract compiler version for source code
    # def get_compiler_version(self, code):
    #     check_version = re.search(r'pragma solidity [<>^]?=?\s*([\d.]+)', code)
    #     if (check_version):
    #         return check_version.group(1)
    #     else:
    #         return None
