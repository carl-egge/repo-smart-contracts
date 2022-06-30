"""
    I preferred using DB postfix for db models.
    It will not be confused with response objects - if you will need anything other than a simple CRUD.
"""
from email import message
from email.policy import default
from lib2to3.pgen2.token import OP
from optparse import Option
from typing import Optional, List, Union
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


class Content(BaseModel):
    compilerversion: Optional[str]
    sourcecode: Optional[str]
    bytecode: Optional[str]
    abi: Optional[str]


class Version(BaseModel):
    vid: int = Field(default=1, description="Vesion ID")
    message: Optional[str] = Field(description="Optional commit message")
    created: datetime = Field(description="ISOdate of the creation of this version")
    parents: List[int] = Field(description="To represent a tree a version can have multiple parents")
    content: Content = Field(description="This embedded document holds the code")


class ContractIn(BaseModel):
    title: str = Field(description="Give the smart contract a title")
    description: Optional[str] = Field(description="Optionally give it a description")
    source: Optional[str] = Field(default="Manually Uploaded", description="What is the source of this smart contract")
    source_file_path: Optional[str] = Field(description="What is the file path in the source location?")
    created: Optional[datetime] = Field(description="When was this smart contract created")
    sourcecode: Optional[str] = Field(description="Enter the source code")
    bytecode: Optional[str] = Field(description="Optionally enter the byte code")
    abi: Optional[str] = Field(description="Optionally enter the application binary interface")


class ContractPatch(BaseModel):
    title: Optional[str] = Field(description="Change the title of this smart contract")
    description: Optional[str] = Field(description="Change the description of this smart contract")
    message: Optional[str] = Field(description="Give the new version a commit message")
    created: Optional[datetime] = Field(description="When was the new version created")
    parents: Optional[List[int]] = Field(exclude=True, description="After merging, a new version can have multiple parents")
    sourcecode: Optional[str] = Field(description="Update the source code")
    bytecode: Optional[str] = Field(description="Update the byte code")
    abi: Optional[str] = Field(description="Update the application binary interface")


class ContractDB(BaseDBModel):
    id: Optional[OID]
    title: str = Field(description="The title")
    description: Optional[str] = Field(description="The description")
    source: Optional[str] = Field(description="URL or name of the source of the contract.")
    source_file_path: Optional[str] = Field(description="Path of name of the file in the source repository")
    latest_version: Optional[int] = Field(default=1, description="Just internal helper to find last version element")
    versions: List[Version] = Field(description="A list of version elements of the source code")

