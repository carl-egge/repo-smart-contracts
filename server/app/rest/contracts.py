from fastapi import APIRouter, Depends

from app.db import DatabaseManager, get_database
from app.db.models import ContractDB, OID

router = APIRouter()


@router.get('/')
async def all_contracts(db: DatabaseManager = Depends(get_database)):
    print("\n\n\n\n")
    print(ContractDB.schema_json(indent=2))
    print("\n\n\n\n")
    contracts = await db.get_contracts()
    return contracts


@router.get('/{contract_id}')
async def one_contract(contract_id: OID, db: DatabaseManager = Depends(get_database)):
    contract = await db.get_contract(contract_id=contract_id)
    return contract


@router.put('/{contract_id}')
async def update_contract(contract_id: OID, contract: ContractDB, db: DatabaseManager = Depends(get_database)):
    contract = await db.update_contract(contract=contract, contract_id=contract_id)
    return contract


@router.post('/', status_code=201)
async def add_contract(contract_response: ContractDB, db: DatabaseManager = Depends(get_database)):
    contract = await db.add_contract(contract_response)
    return contract


@router.delete('/{contract_id}')
async def delete_contract(contract_id: OID, db: DatabaseManager = Depends(get_database)):
    await db.delete_contract(contract_id=contract_id)
