from pydantic import BaseModel
from typing import Optional, Any
from bson import ObjectId
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(ObjectId):
    """Custom ObjectId field for Pydantic models"""
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: Any
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class UserModel(BaseModel):
    """Model for user data with hashed password"""
    id: Optional[PyObjectId] = None
    userid: str
    email: str
    password_hash: str  # Store the hashed password

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class UserCreateModel(BaseModel):
    """Model for creating a new user (with plain password for input validation)"""
    userid: str
    email: str
    password: str  # Plain password for input, will be hashed before storage

    class Config:
        arbitrary_types_allowed = True


class UserResponseModel(BaseModel):
    """Model for user response (without password fields)"""
    id: Optional[PyObjectId] = None
    userid: str
    email: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }