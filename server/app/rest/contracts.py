from typing import List, Union
from fastapi import APIRouter, Depends, status, Response, Query

from app.db import DatabaseManager, get_database
from app.db.models import Content, ContractDB, OID, ContractIn, ContractPatch

router = APIRouter()


@router.get('/', response_model=List[ContractDB])
async def all_contracts(response: Response,
                        src: Union[str, None] = Query(default=None, title="Contract source", description="Only contracts from a specified source repository (must be URIencoded)."),
                        title: Union[str,None] = Query(default=None, title="Contract title", description="Get contracts with a specified title."),
                        limit: int = Query(default=50, ge=1, le=200, title="Limit for Objects", description="Paginate the amount of returned objects (limit)."),
                        skip: int = Query(default=0, ge=0, title="Offset for Objects", description="Paginate the amount of returned objects (offset)."),
                        db: DatabaseManager = Depends(get_database)):
    db_size = await db.count_contracts()
    response.headers["X-Total-DB-Size"] = str(db_size)
    contracts = await db.get_contracts(source_str=src,title_str=title,limit=limit,skip=skip)
    return contracts


@router.get('/{contract_id}', responses={200: {"model": ContractDB, "description": "Returns the complete database model of a smart contract."}, 210: {"model": Content, "description": "Returns only the code for the specified version."}})
async def one_contract(contract_id: OID, vers: Union[int, None] = None, db: DatabaseManager = Depends(get_database)):
    contract = await db.get_contract(contract_id=contract_id, version_id=vers)
    return contract


@router.put('/{contract_id}', response_model=ContractDB)
async def update_contract(contract_id: OID, contract: ContractPatch, db: DatabaseManager = Depends(get_database)):
    contract = await db.update_contract(contract=contract, contract_id=contract_id)
    return contract


@router.post('/', status_code=201, response_model=ContractDB)
async def add_contract(contract_response: ContractIn, db: DatabaseManager = Depends(get_database)):
    contract = await db.add_contract(contract_response)
    return contract


@router.delete('/{contract_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_contract(contract_id: OID, vers: Union[int, None] = None, db: DatabaseManager = Depends(get_database)):
    await db.delete_contract(contract_id=contract_id, version_id=vers)
    return None


# dev help: Print database scheme
    #print("\n\n\n\n")
    #print(ContractDB.schema_json(indent=2))
    #print("\n\n\n\n")