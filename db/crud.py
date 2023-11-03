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
from models import db, app, fs, client


async def create_callingparty(callingparty: CallingPartyModel = Body(...)):
    callingparty = jsonable_encoder(callingparty)
    new_callingparty = await db["CallingParty"].insert_one(callingparty)
    created_callingparty = await db["CallingParty"].find_one({"_id": new_callingparty.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_callingparty)


async def list_callingpartys():
    callingpartys = await db["CallingParty"].find().to_list(1000)
    return callingpartys


async def show_callingparty(id: str):
    if (callingparty := await db["CallingParty"].find_one({"_id": id})) is not None:
        return callingparty

    raise HTTPException(status_code=404, detail=f"callingparty {id} not found")


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


async def delete_callingparty(id: str):
    delete_result = await db["CallingParty"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"callingparty {id} not found")


async def create_virtualagent(virtualagent: VirtualAgentModel = Body(...)):
    virtualagent = jsonable_encoder(virtualagent)
    new_virtualagent = await db["VirtualAgent"].insert_one(virtualagent)
    created_virtualagent = await db["VirtualAgent"].find_one({"_id": new_virtualagent.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_virtualagent)


async def list_virtualagents():
    virtualagents = await db["VirtualAgent"].find().to_list(1000)
    return virtualagents


async def show_virtualagent(id: str):
    if (virtualagent := await db["VirtualAgent"].find_one({"_id": id})) is not None:
        return virtualagent

    raise HTTPException(status_code=404, detail=f"Virtual Agent {id} not found")


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


async def delete_virtualagent(id: str):
    delete_result = await db["VirtualAgent"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Virtual Agent {id} not found")


async def create_humanagent(humanagent: HumanAgentModel = Body(...)):
    humanagent = jsonable_encoder(humanagent)
    new_humanagent = await db["HumanAgent"].insert_one(humanagent)
    created_humanagent = await db["HumanAgent"].find_one({"_id": new_humanagent.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_humanagent)


async def list_humanagents():
    humanagents = await db["HumanAgent"].find().to_list(1000)
    return humanagents


async def show_humanagent(id: str):
    if (humanagent := await db["HumanAgent"].find_one({"_id": id})) is not None:
        return humanagent

    raise HTTPException(status_code=404, detail=f"Human Agent {id} not found")


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


async def delete_humanagent(id: str):
    delete_result = await db["HumanAgent"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Human Agent {id} not found")


async def create_cxchannel(cxchannel: CxChannelModel = Body(...)):
    cxchannel = jsonable_encoder(cxchannel)
    new_cxchannel = await db["CxChannel"].insert_one(cxchannel)
    created_cxchannel = await db["CxChannel"].find_one({"_id": new_cxchannel.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_cxchannel)


async def list_cxchannels():
    cxchannels = await db["CxChannel"].find().to_list(1000)
    return cxchannels


async def show_cxchannel(id: str):
    if (cxchannel := await db["CxChannel"].find_one({"_id": id})) is not None:
        return cxchannel

    raise HTTPException(status_code=404, detail=f"CxChannel {id} not found")


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


async def delete_cxchannel(id: str):
    delete_result = await db["CxChannel"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"CxChannel {id} not found")

async def create_utterence(utterence: UtteranceModel = Body(...)):
    utterence = jsonable_encoder(utterence)
    new_utterence = await db["Utterance"].insert_one(utterence)
    created_utterence = await db["Utterance"].find_one({"_id": new_utterence.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_utterence)


async def list_utterences():
    utterences = await db["Utterance"].find().to_list(1000)
    return utterences


async def show_utterence(id: str):
    if (utterence := await db["Utterance"].find_one({"_id": id})) is not None:
        return utterence

    raise HTTPException(status_code=404, detail=f"Utterence {id} not found")


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

