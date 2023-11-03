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



MONGODB_URL = "mongodb+srv://andrewnakamura147:igbP1nfIR7r9TKco@cluster0.4ynrtjd.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"

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


#################

@app.post("/callingparty/", response_description="Add new callingparty", response_model=CallingPartyModel)
async def create_callingparty(callingparty: CallingPartyModel = Body(...)):
    callingparty = jsonable_encoder(callingparty)
    new_callingparty = await db["CallingParty"].insert_one(callingparty)
    created_callingparty = await db["CallingParty"].find_one({"_id": new_callingparty.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_callingparty)


@app.get(
    "/callingparty/", response_description="List all callingpartys", response_model=List[CallingPartyModel]
)
async def list_callingpartys():
    callingpartys = await db["CallingParty"].find().to_list(1000)
    return callingpartys


@app.get(
    "/callingparty/{id}", response_description="Get a single callingparty", response_model=CallingPartyModel
)
async def show_callingparty(id: str):
    if (callingparty := await db["CallingParty"].find_one({"_id": id})) is not None:
        return callingparty

    raise HTTPException(status_code=404, detail=f"callingparty {id} not found")


@app.put("/callingparty/{id}", response_description="Update a callingparty", response_model=CallingPartyModel)
async def update_callingparty(id: str, callingparty: UpdateCallingPartyModel = Body(...)):
    callingparty = {k: v for k, v in callingparty.dict().items() if v is not None}

    if len(callingparty) >= 1:
        update_result = await db["CallingParty"].update_one({"_id": id}, {"$set": callingparty})

        if update_result.modified_count == 1:
            if (
                updated_callingparty := await db["CallingParty"].find_one({"_id": id})
            ) is not None:
                return updated_callingparty

    if (existing_callingparty := await db["CallingParty"].find_one({"_id": id})) is not None:
        return existing_callingparty

    raise HTTPException(status_code=404, detail=f"callingparty {id} not found")


@app.delete("/callingparty/{id}", response_description="Delete a callingparty")
async def delete_callingparty(id: str):
    delete_result = await db["CallingParty"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"callingparty {id} not found")


##################


@app.post("/virtualagent/", response_description="Add new virtualagent", response_model=VirtualAgentModel)
async def create_virtualagent(virtualagent: VirtualAgentModel = Body(...)):
    virtualagent = jsonable_encoder(virtualagent)
    new_virtualagent = await db["VirtualAgent"].insert_one(virtualagent)
    created_virtualagent = await db["VirtualAgent"].find_one({"_id": new_virtualagent.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_virtualagent)


@app.get(
    "/virtualagent/", response_description="List all virtualagents", response_model=List[VirtualAgentModel]
)
async def list_virtualagents():
    virtualagents = await db["VirtualAgent"].find().to_list(1000)
    return virtualagents


@app.get(
    "/virtualagent/{id}", response_description="Get a single virtualagent", response_model=VirtualAgentModel
)
async def show_virtualagent(id: str):
    if (virtualagent := await db["VirtualAgent"].find_one({"_id": id})) is not None:
        return virtualagent

    raise HTTPException(status_code=404, detail=f"Virtual Agent {id} not found")


@app.put("/virtualagent/{id}", response_description="Update a virtualagent", response_model=VirtualAgentModel)
async def update_virtualagent(id: str, virtualagent: UpdateVirtualAgentModel = Body(...)):
    virtualagent = {k: v for k, v in virtualagent.dict().items() if v is not None}

    if len(virtualagent) >= 1:
        update_result = await db["VirtualAgent"].update_one({"_id": id}, {"$set": virtualagent})

        if update_result.modified_count == 1:
            if (
                updated_virtualagent := await db["VirtualAgent"].find_one({"_id": id})
            ) is not None:
                return updated_virtualagent

    if (existing_virtualagent := await db["VirtualAgent"].find_one({"_id": id})) is not None:
        return existing_virtualagent

    raise HTTPException(status_code=404, detail=f"Virtual Agent {id} not found")


@app.delete("/virtualagent/{id}", response_description="Delete a virtualagent")
async def delete_virtualagent(id: str):
    delete_result = await db["VirtualAgent"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Virtual Agent {id} not found")


#####################################


@app.post("/humanagent/", response_description="Add new humanagent", response_model=HumanAgentModel)
async def create_humanagent(humanagent: HumanAgentModel = Body(...)):
    humanagent = jsonable_encoder(humanagent)
    new_humanagent = await db["HumanAgent"].insert_one(humanagent)
    created_humanagent = await db["HumanAgent"].find_one({"_id": new_humanagent.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_humanagent)


@app.get(
    "/humanagent/", response_description="List all humanagents", response_model=List[HumanAgentModel]
)
async def list_humanagents():
    humanagents = await db["HumanAgent"].find().to_list(1000)
    return humanagents


@app.get(
    "/humanagent/{id}", response_description="Get a single humanagent", response_model=HumanAgentModel
)
async def show_humanagent(id: str):
    if (humanagent := await db["HumanAgent"].find_one({"_id": id})) is not None:
        return humanagent

    raise HTTPException(status_code=404, detail=f"Human Agent {id} not found")


@app.put("/humanagent/{id}", response_description="Update a humanagent", response_model=HumanAgentModel)
async def update_humanagent(id: str, humanagent: UpdateHumanAgentModel = Body(...)):
    humanagent = {k: v for k, v in humanagent.dict().items() if v is not None}

    if len(humanagent) >= 1:
        update_result = await db["HumanAgent"].update_one({"_id": id}, {"$set": humanagent})

        if update_result.modified_count == 1:
            if (
                updated_humanagent := await db["HumanAgent"].find_one({"_id": id})
            ) is not None:
                return updated_humanagent

    if (existing_humanagent := await db["HumanAgent"].find_one({"_id": id})) is not None:
        return existing_humanagent

    raise HTTPException(status_code=404, detail=f"Human Agent {id} not found")


@app.delete("/humanagent/{id}", response_description="Delete a humanagent")
async def delete_humanagent(id: str):
    delete_result = await db["HumanAgent"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Human Agent {id} not found")


###################
@app.post("/cxchannel/", response_description="Add new cxchannel", response_model=CxChannelModel)
async def create_cxchannel(cxchannel: CxChannelModel = Body(...)):
    cxchannel = jsonable_encoder(cxchannel)
    new_cxchannel = await db["CxChannel"].insert_one(cxchannel)
    created_cxchannel = await db["CxChannel"].find_one({"_id": new_cxchannel.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_cxchannel)


@app.get(
    "/cxchannel/", response_description="List all cxchannels", response_model=List[CxChannelModel]
)
async def list_cxchannels():
    cxchannels = await db["CxChannel"].find().to_list(1000)
    return cxchannels


@app.get(
    "/cxchannel/{id}", response_description="Get a single cxchannel", response_model=CxChannelModel
)
async def show_cxchannel(id: str):
    if (cxchannel := await db["CxChannel"].find_one({"_id": id})) is not None:
        return cxchannel

    raise HTTPException(status_code=404, detail=f"CxChannel {id} not found")


@app.put("/cxchannel/{id}", response_description="Update a cxchannel", response_model=CxChannelModel)
async def update_cxchannel(id: str, cxchannel: UpdateCxChannelModel = Body(...)):
    cxchannel = {k: v for k, v in cxchannel.dict().items() if v is not None}

    if len(cxchannel) >= 1:
        update_result = await db["CxChannel"].update_one({"_id": id}, {"$set": cxchannel})

        if update_result.modified_count == 1:
            if (
                updated_cxchannel := await db["CxChannel"].find_one({"_id": id})
            ) is not None:
                return updated_cxchannel

    if (existing_cxchannel := await db["CxChannel"].find_one({"_id": id})) is not None:
        return existing_cxchannel

    raise HTTPException(status_code=404, detail=f"CxChannel {id} not found")


@app.delete("/cxchannel/{id}", response_description="Delete a CxChannel")
async def delete_cxchannel(id: str):
    delete_result = await db["CxChannel"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"CxChannel {id} not found")

##################

@app.post("/utterence/", response_description="Add new utterence", response_model=UtteranceModel)
async def create_utterence(utterence: UtteranceModel = Body(...)):
    utterence = jsonable_encoder(utterence)
    new_utterence = await db["Utterance"].insert_one(utterence)
    created_utterence = await db["Utterance"].find_one({"_id": new_utterence.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_utterence)


@app.get(
    "/utterence/", response_description="List all utterences", response_model=List[UtteranceModel]
)
async def list_utterences():
    utterences = await db["Utterance"].find().to_list(1000)
    return utterences


@app.get(
    "/utterence/{id}", response_description="Get a single utterence", response_model=UtteranceModel
)
async def show_utterence(id: str):
    if (utterence := await db["Utterance"].find_one({"_id": id})) is not None:
        return utterence

    raise HTTPException(status_code=404, detail=f"Utterence {id} not found")


@app.put("/utterence/{id}", response_description="Update a utterence", response_model=UtteranceModel)
async def update_utterence(id: str, utterence: UpdateUtteranceModel = Body(...)):
    utterence = {k: v for k, v in utterence.dict().items() if v is not None}

    if len(utterence) >= 1:
        update_result = await db["Utterance"].update_one({"_id": id}, {"$set": utterence})

        if update_result.modified_count == 1:
            if (
                updated_utterence := await db["Utterance"].find_one({"_id": id})
            ) is not None:
                return updated_utterence

    if (existing_utterence := await db["Utterance"].find_one({"_id": id})) is not None:
        return existing_utterence

    raise HTTPException(status_code=404, detail=f"Utterence {id} not found")


@app.delete("/utterence/{id}", response_description="Delete a utterence")
async def delete_utterence(id: str):
    delete_result = await db["Utterance"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Utterence {id} not found")

async def insert_callingparty_data(callingparty_data: Dict[str, str]):
    callingparty_model = CallingPartyModel(**callingparty_data)
    new_callingparty = await create_callingparty(callingparty_model)
    return new_callingparty

async def insert_utterence_data(utterence_data: Dict[str, str]):
    utterence_model = UtteranceModel(**utterence_data)
    new_utterence = await create_utterence(utterence_model)
    return new_utterence

async def insert_cxchannel_data(cxchannel_data: Dict[str, str]):
    cxchannel_model = CxChannelModel(**cxchannel_data)
    new_cxchannel = await create_cxchannel(cxchannel_model)
    return new_cxchannel

async def insert_humanagent_data(humanagent_data: Dict[str, str]):
    humanagent_model = HumanAgentModel(**humanagent_data)
    new_humanagent = await create_humanagent(humanagent_model)
    return new_humanagent

async def insert_virtualagent_data(virtualagent_data: Dict[str, str]):
    virtualagent_model = VirtualAgentModel(**virtualagent_data)
    new_virtualagent = await create_virtualagent(virtualagent_model)
    return new_virtualagent


# import uvicorn

# if __name__ == '__main__':
#     uvicorn.run("app", host="0.0.0.0", port=8001, reload=True)
    