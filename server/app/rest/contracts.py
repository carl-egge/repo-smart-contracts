# from typing import List, Union
from fastapi import (
    APIRouter, 
    Response,
    Depends,
    Query,
    # status
)
from app.db import (
    DatabaseManager,
    get_database
)
from app.db.models import (
    ContractDB,
    ContractsResponse,
    OID,
    ResponseModel,
    ErrorResponseModel
)

router = APIRouter()

# -------------------------------- /contracts --------------------------------

#
# GET :: Endpoint to get a list of filtered smart contracts
#
@router.get('/contracts', response_model=ContractsResponse, summary="All Contract Files",
            description="""
Returns a list of all smart contracts that match the specified filters. The _/contracts_ endpoint accesses the contracts collection which holds Solidity files
that may contain imports. The contracts collection is larger than the flatcontracts collection.
            """)
async def all_contracts(
                        response: Response,
                        name: str = Query(None, title="Contract name", description="The name of the contract."),
                        language: str = Query(None, title="Programming language", description="Specifiy the programming language."),
                        license: str = Query(None, title="License", description="Only contracts with this license (GitHub shortcode)."),
                        sha: str = Query(None, title="Git sha", description="Git sha for this contract or one of its versions."),
                        repo: str = Query(None, title="Source Repository", description="Show contracts from a specified source repository."),
                        owner: str = Query(None, title="Repository Owner", description="Filter for ID or name of repository owner."),
                        amountOfVersions: int = Query(None, ge=1, title="Amount of Versions", description="Only contracts that have this amount of versions."),
                        pragma: str = Query(None, title="Compiler Version", description="Filter for Solidity files that were compiled with this pragma version (format: 0.0.0)."),
                        size: str = Query(None, title="File size", description="Only contracts with this file size (Can be range in the format: 10..20)."),
                        searchAllVersions: bool = Query(False, title="Search in all versions", description="Search in all versions of a contract (default searches only in latest version)."),
                        limit: int = Query(default=50, ge=1, le=200, title="Limit for Objects", description="Paginate the amount of returned objects (limit)."),
                        skip: int = Query(default=0, ge=0, title="Offset for Objects", description="Paginate the amount of returned objects (offset)."),
                        db: DatabaseManager = Depends(get_database)
                    ):
    db_size = await db.count_database('contracts')
    response.headers["X-Total-DB-Size"] = str(db_size)
    contracts = await db.get_contracts(name, language, license, sha, repo, owner, amountOfVersions, pragma, size, searchAllVersions, limit, skip, 'contracts')
    if contracts:
        result_size = await db.count_contracts(name, language, license, sha, repo, owner, amountOfVersions, pragma, size, searchAllVersions, 'contracts')
        return ResponseModel(contracts, "Smart contracts retrieved successfully", result_size)
    return ResponseModel(contracts, "No smart contracts found", 0)

#
# GET :: Endpoint to get a one smart contract by id
#
@router.get('/contracts/{contract_id}', responses={
                                            200: {
                                                    "model": ContractDB, 
                                                    "description": "Returns the complete database model of a smart contract."
                                                },
                                            210: {
                                                    "model": str,
                                                    "description": "Returns only the code for the specified version."
                                                }
                                        }, summary="One Contract File")
async def one_contract(
                        contract_id: OID,
                        vers: int = Query(None, ge=0, title="Version ID", description="Query a specific version id to receive only the sourcecode of this version"),
                        db: DatabaseManager = Depends(get_database)
                    ):
    contract = await db.get_contract(contract_id, version_id=vers, collection='contracts')
    if contract == "version out of range":
        return ErrorResponseModel("NotFoundError", 404, "Version number is out of range.")
    elif not contract:
        return ErrorResponseModel("NotFoundError", 404, "Smart Contract was not found.")
    return ResponseModel(contract, "Contract data retrieved successfully", 1)


# -------------------------------- /flatcontracts --------------------------------

#
# GET :: Endpoint to get a list of filtered smart contracts
#
@router.get('/flatcontracts', response_model=ContractsResponse, summary="All flattened Smart Contracts",
            description="""
Returns a list of all smart contracts that match the specified filters. The _/flatcontracts_ endpoint accesses the flatcontracts collection which holds Solidity files
that are flattened and compilable. The flatcontracts collection is smaller than the contracts collection.
            """)
async def all_contracts(
                        response: Response,
                        name: str = Query(None, title="Contract name", description="The name of the contract."),
                        language: str = Query(None, title="Programming language", description="Specifiy the programming language."),
                        license: str = Query(None, title="License", description="Only contracts with this license (GitHub shortcode)."),
                        sha: str = Query(None, title="Git sha", description="Git sha for this contract or one of its versions."),
                        repo: str = Query(None, title="Source Repository", description="Show contracts from a specified source repository."),
                        owner: str = Query(None, title="Repository Owner", description="Filter for ID or name of repository owner."),
                        amountOfVersions: int = Query(None, ge=1, title="Amount of Versions", description="Only contracts that have this amount of versions."),
                        pragma: str = Query(None, title="Compiler Version", description="Filter for Solidity files that were compiled with this pragma version (format: 0.0.0)."),
                        size: str = Query(None, title="File size", description="Only contracts with this file size (Can be range in the format: 10..20)."),
                        searchAllVersions: bool = Query(False, title="Search in all versions", description="Search in all versions of a contract (default searches only in latest version)."),
                        limit: int = Query(default=50, ge=1, le=200, title="Limit for Objects", description="Paginate the amount of returned objects (limit)."),
                        skip: int = Query(default=0, ge=0, title="Offset for Objects", description="Paginate the amount of returned objects (offset)."),
                        db: DatabaseManager = Depends(get_database)
                    ):
    db_size = await db.count_database('flatcontracts')
    response.headers["X-Total-DB-Size"] = str(db_size)
    contracts = await db.get_contracts(name, language, license, sha, repo, owner, amountOfVersions, pragma, size, searchAllVersions, limit, skip, 'flatcontracts')
    if contracts:
        result_size = await db.count_contracts(name, language, license, sha, repo, owner, amountOfVersions, pragma, size, searchAllVersions, 'flatcontracts')
        return ResponseModel(contracts, "Flat Smart contracts retrieved successfully", result_size)
    return ResponseModel(contracts, "No smart contracts found", 0)

#
# GET :: Endpoint to get a one smart contract by id
#
@router.get('/flatcontracts/{contract_id}', responses={
                                            200: {
                                                    "model": ContractDB, 
                                                    "description": "Returns the complete database model of a smart contract."
                                                },
                                            210: {
                                                    "model": str,
                                                    "description": "Returns only the code for the specified version."
                                                }
                                        }, summary="One specific flattened Contract File")
async def one_contract(
                        contract_id: OID,
                        vers: int = Query(None, ge=0, title="Version ID", description="Query a specific version id to receive only the sourcecode of this version"),
                        db: DatabaseManager = Depends(get_database)
                    ):
    contract = await db.get_contract(contract_id, version_id=vers, collection='flatcontracts')
    if contract == "version out of range":
        return ErrorResponseModel("NotFoundError", 404, "Version number is out of range.")
    elif not contract:
        return ErrorResponseModel("NotFoundError", 404, "Smart Contract was not found.")
    return ResponseModel(contract, "Flat Contract data retrieved successfully", 1)
