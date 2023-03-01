#from email import message
#from email.policy import default
#from lib2to3.pgen2.token import OP
#from optparse import Option
#from typing import Union
from typing import Optional, List
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

class Repository(BaseModel):
    repo_id: int = Field(..., description="The GitHub ID of the source repository")
    full_name: Optional[str] = Field(description="The full name of the repository")
    description: Optional[str] = Field(description="The description of the GitHub repository")
    url: Optional[str] = Field(description="The url to the GitHub API responose for this repository")
    owner_id: Optional[int] = Field(description="The GitHub ID of the owner of the source repository")

class Version(BaseModel):
    version_id: int = Field(default=1, description="Vesion ID")
    sha: Optional[str] = Field(description="GitHub commit sha")
    message: Optional[str] = Field(description="Optional commit message")
    size: Optional[int] = Field(description="The byte size of the content")
    created: datetime = Field(description="ISOdate of the creation of this version")
    compiler_version: Optional[str] = Field(description="The pragma compiler verion of this commit")
    parents: Optional[str] = Field(description="To represent a tree a version can have multiple parents")
    content: str = Field(..., description="This field holds the utf-8 encoded source code of this version")

class ContractDB(BaseDBModel):
    id: Optional[OID]
    name: str = Field(..., description="The file name of the smart contract")
    path: str = Field(..., description="The path to this file within the source repository")
    sha: Optional[str] = Field(description="The git sha for this smart contract file")
    language: Optional[str] = Field(description="Name of the programming language of this smart contract")
    license: Optional[str] = Field(description="A short key indicating the license that the source is under")
    repo: Repository = Field(..., description="Further information on the source repository of this contract")
    versions: List[Version] = Field(..., description="A list of versions (git commits) of the source code")

    class Config:
        schema_extra = {
            "example": {
                "name": "TestContract",
                "path": "contracts/TestContract.sol",
                "sha": "915b5cdc2e295884d583fb148afe63dfaea6be40",
                "language": "Solidity",
                "license": "mit",
                "repo": {
                    "repo_id": 312330931,
                    "full_name": "john-doe/test-repo",
                    "description": "This is an example schema",
                    "url": "https://api.github.com/repos/john-doe/test-repo",
                    "owner_id": 764158
                },
                "versions": [
                    {
                        "version_id": 1,
                        "sha": "ace505dce9550c98eb0d2bd6992c22c24f1ce88f",
                        "message": "Created smart contract",
                        "size": 1232,
                        "created": "2018-11-07T13:52:12Z",
                        "compiler_version": "0.4.18",
                        "content": "pragma solidity ^0.4.18; ...",
                        "parents": "[cfed62ac04053e33e894fe0eddaf6b1446b3627b]"
                    }
                ]
            }
        }

class ContractsResponse(BaseDBModel):
    status: int
    message: str
    total_count: int
    data: List[ContractDB]


def ResponseModel(data, message, count):
    return {
        "status": 200,
        "message": message,
        "total_count": count,
        "data": data,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "status": code, "message": message}