from typing import Dict
from db import *
import asyncio
import requests
import json


async def main():
    # utterence_data = {
    #     "Starttime": "2022-01-01T00:00:00",
    #     "Endtime": "2022-01-01T00:05:00",
    #     "Original_voice": b"original voice",
    #     "Transcript_original": "This is the original transcript v2",
    #     "Transcript_english": "This is the English transcript",
    #     "Sentiment": "positive",
    #     "Source": "Call Center",
    #     "Link_to_CX_channel": "link to CX channel"
    # }
    # inserted_utterence = await insert_utterence_data(utterence_data)

    # cxchannel_data = {
    #     "Link_to_Calling_party": "link to calling party",
    #     "Link_Human_agent": "link to human agent",
    #     "Link_Virtual_agent": "link to virtual agent",
    #     "Start_time": "2022-01-01T09:00:00",
    #     "End_time": "2022-01-01T09:30:00",
    #     "FirstCallResolution": True,
    #     "Language": "en"
    # }
    # inserted_cxchannel = await insert_cxchannel_data(cxchannel_data)

    # virtualagent_data = {
    #     "Name": "Mark",
    #     "Version": "0.0.1",
    #     "ReleasedDate": "2022-01-01T09:30:00",
    # }
    # inserted_virtualagent = await insert_virtualagent_data(virtualagent_data)

    CP = {
            "Phone": "6462940064",
            "FirstName": "Mark",
            "SecondName": "Beech",
            "Profile": "Influence",
            "Proficiency": "Native",
        }
    HA = {
        "FirstName": "John",
        "SecondName": "Farigous",
        "Profile": "Steadiness",
        "Proficiency": "Native",
    }
    CX = {
        "Link_to_Calling_party": "651caf999b59fe2fa9fc1386",
        "Link_Human_agent": "651caf979b59fe2fa9fc1385",
        "Link_Virtual_agent": "",
        "Start_time": "2022-01-01T09:00:00",
        "End_time": "2022-01-01T09:03:00",
        "FirstCallResolution": True,
        "Language": ""
    }
    # await insert_humanagent_data(HA)
    # await insert_callingparty_data(CP)
    inserted = await insert_cxchannel_data(CX)

    # inserted = inserted.json()
    print(json.loads(inserted.body)["_id"])
    # inserted_humanagent = await insert_humanagent_data(humanagent_data)
    


if __name__ == "__main__":
    asyncio.run(main())