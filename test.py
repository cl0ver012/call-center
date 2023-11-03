import requests
from db import insert_utterence_data, insert_cxchannel_data, insert_humanagent_data, insert_virtualagent_data

def send_file():
    file_path = './call_centax.wav'
    with open(file_path, 'rb') as file:
        response = requests.post('http://localhost:8080/transcribe/', files={'file': file})
    result = response.json()
    print(result)


send_file()