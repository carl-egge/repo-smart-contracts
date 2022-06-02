"""
    I preferred using DB postfix for db models.
    It will not be confused with response objects - if you will need anything other than a simple CRUD.
"""
from email.policy import default
from typing import Optional
from datetime import datetime

from bson import ObjectId
from pydantic.main import BaseModel, Field


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v == '':
            raise TypeError('ObjectId is empty')
        if ObjectId.is_valid(v) is False:
            raise TypeError('ObjectId invalid')
        return str(v)


class BaseDBModel(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            """ Camel case generator """
            temp = string.split('_')
            return temp[0] + ''.join(ele.title() for ele in temp[1:])


class ContractDB(BaseDBModel):
    id: Optional[OID]
    title: str
    sourcecode: Optional[str]
    abi: Optional[str]
    bytecode: Optional[str]
    version: int = Field(default=1)
    created: datetime = Field(default_factory=datetime.utcnow)
