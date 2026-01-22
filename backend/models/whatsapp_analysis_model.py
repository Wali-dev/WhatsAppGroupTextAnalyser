from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
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


class DayWiseStats(BaseModel):
    """Model for daily statistics"""
    date: str
    new_users: int
    active_users: int


class WhatsAppAnalysisModel(BaseModel):
    """MongoDB model for WhatsApp analysis data"""
    id: Optional[PyObjectId] = None
    filename: str
    upload_date: datetime
    range_start: str
    range_end: str
    day_wise_graph_data: List[DayWiseStats]
    active_4_days_users: List[str]
    user_id: Optional[str] = None  # ID of the user who uploaded this analysis

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class WhatsAppAnalysisDocument(WhatsAppAnalysisModel):
    """Model for storing in MongoDB"""
    id: Optional[PyObjectId] = None
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }