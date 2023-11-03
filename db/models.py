import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
from datetime import datetime
from typing import Dict
import asyncio
import requests
import json

load_dotenv()


MONGODB_URL = os.getenv('ATLAS_URI')

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client["call_record"]
fs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(db)

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UtteranceModel(BaseModel):
    ID: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Starttime: float = Field(...)
    Endtime: float = Field(...)
    Transcript_original: str = Field(...)
    Transcript_english: str = Field(...)
    Sentiment: str = Field(...)
    Source: str = Field(...)
    Link_to_CX_channel: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ID": "123",
                "Starttime": "0.0",
                "Endtime": "3.2",
                "Transcript_original": "This is the original transcript",
                "Transcript_english": "This is the English transcript",
                "Sentiment": "positive",
                "Source": "AI",
                "Link_to_CX_channel": "link to CX channel"
            }
        }


class UpdateUtteranceModel(BaseModel):
    Starttime: Optional[float]
    Endtime: Optional[float]
    Transcript_original: Optional[str]
    Transcript_english: Optional[str]
    Sentiment: Optional[str]
    Source: Optional[str]
    Link_to_CX_channel: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ID": "123",
                "Starttime": "0.0",
                "Endtime": "3.2",
                "Transcript_original": "This is the original transcript",
                "Transcript_english": "This is the English transcript",
                "Sentiment": "positive",
                "Source": "AI",
                "Link_to_CX_channel": "link to CX channel"
            }
        }


class CxChannelModel(BaseModel):
    ID: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Link_to_Calling_party: str = Field(...)
    Link_Human_agent: str = Field(...)
    Link_Virtual_agent: str = Field(...)
    Start_time: datetime = Field(...)
    End_time: datetime = Field(...)
    FirstCallResolution: bool = Field(...)
    Language: str = Field(...)
    Original_voice : str = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ID": "123",
                "Link_to_Calling_party": "link to calling party",
                "Link_Human_agent": "link to human agent",
                "Link_Virtual_agent": "link to virtual agent",
                "Start_time": "2022-01-01T09:00:00",
                "End_time": "2022-01-01T09:30:00",
                "Original_voice" : "sdfsdfsf",
                "FirstCallResolution": True,
                "Language": "en"
            }
        }

class UpdateCxChannelModel(BaseModel):
    Link_to_Calling_party: Optional[str]
    Link_Human_agent:  Optional[str]
    Link_Virtual_agent:  Optional[str]
    Start_time:  Optional[datetime]
    End_time:  Optional[datetime]
    FirstCallResolution:  Optional[bool]
    Language:  Optional[str]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Link_to_Calling_party": "link to calling party",
                "Link_Human_agent": "link to human agent",
                "Link_Virtual_agent": "link to virtual agent",
                "Start_time": "2022-01-01T09:00:00",
                "End_time": "2022-01-01T09:30:00",
                "FirstCallResolution": True,
                "Language": "en"
            }
        }


class VirtualAgentModel(BaseModel):
    ID: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Name: str = Field(...)
    Version: str = Field(...)
    ReleasedDate: datetime = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ID": "123",
                "Name": "Mark",
                "Version": "0.0.1",
                "ReleasedDate": "2022-01-01T09:30:00",
            }
        }

class UpdateVirtualAgentModel(BaseModel):
    Name: Optional[str]
    Version: Optional[str]
    ReleasedDate: Optional[datetime]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Name": "Mark",
                "Version": "0.0.1",
                "ReleasedDate": "2022-01-01T09:30:00",
            }
        }



class HumanAgentModel(BaseModel):
    ID: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    FirstName: str = Field(...)
    SecondName: str = Field(...)
    Profile: str = Field(...)
    Proficiency: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ID": "123",
                "FirstName": "Mark",
                "SecondName": "Beech",
                "Profile": "Steadiness",
                "Proficiency": "Native",
            }
        }


class UpdateHumanAgentModel(BaseModel):
    FirstName: Optional[str]
    SecondName: Optional[str]
    Profile: Optional[str]
    Proficiency: Optional[str]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "FirstName": "Mark",
                "SecondName": "Beech",
                "Profile": "Steadiness",
                "Proficiency": "Native",
            }
        }


class CallingPartyModel(BaseModel):
    ID: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Phone: str = Field(...)
    FirstName: str = Field(...)
    SecondName: str = Field(...)
    Profile: str = Field(...)
    Proficiency: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ID": "123",
                "Phone": "6462940054",
                "FirstName": "Mark",
                "SecondName": "Beech",
                "Profile": "Influence",
                "Proficiency": "Native",
            }
        }

class UpdateCallingPartyModel(BaseModel):
    Phone: Optional[str]
    FirstName: Optional[str]
    SecondName: Optional[str]
    Profile: Optional[str]
    Proficiency: Optional[str]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Phone": "6462940054",
                "FirstName": "Mark",
                "SecondName": "Beech",
                "Profile": "Influence",
                "Proficiency": "Native",
            }
        }

class KPIModel(BaseModel):
    ID: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Link_to_CX_channel: str = Field(...)
    CallLength: float = Field(...)
    USR: float = Field(...)
    Datetime: datetime = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ID": "123",
                "Link_to_CX_channel": "link to CX channel",
                "CallLength": 135.0,
                "USR": 4.0,
                "Datetime": "2022-01-01T09:30:00"
            }
        }

class UpdateKPIModel(BaseModel):
    Link_to_CX_channel: Optional[str]
    CallLength: Optional[float]
    USR: Optional[float]
    Datetime: Optional[datetime]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Link_to_CX_channel": "link to CX channel",
                "CallLength": 135.0,
                "USR": 4.0,
                "Datetime": "2022-01-01T09:30:00"
            }
        }
    
class SummaryModel(BaseModel):
    ID: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Link_to_CX_channel: str = Field(...)
    CallSummary: str = Field(...)
    Datetime: datetime = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ID": "123",
                "Link_to_CX_channel": "link to CX channel",
                "CallSummary": "Perfect Conversation!",
                "Datetime": "2022-01-01T09:30:00"
            }
        }
    
class UpdateSummaryModel(BaseModel):
    Link_to_CX_channel: Optional[str]
    CallSummary: Optional[str]
    Datetime: Optional[datetime]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Link_to_CX_channel": "link to CX channel",
                "CallSummary": "Perfect Conversation!",
                "Datetime": "2022-01-01T09:30:00"
            }
        }
