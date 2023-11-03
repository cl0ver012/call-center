import os
import time

import librosa
import soundfile as sf
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from speechbrain.pretrained.interfaces import foreign_class
import whisperx
from speechbrain.pretrained import SepformerSeparation as separator
import torchaudio
import torch
from df.enhance import enhance, init_df, load_audio, save_audio
from df.utils import download_file
import openai
from easygoogletranslate import EasyGoogleTranslate
from db import insert_cxchannel_data, fs, insert_utterence_data
import json

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:2048"

# Load environment variables from .env file for sensitive data like Hugging Face tokens.
load_dotenv()

openai.api_key = os.getenv('OPENAI_KEY')
# Initialize FastAPI app instance.
app = FastAPI()


# Enable Cross Origin Resource Sharing for all origins, headers and methods.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)

# Class for handling speech to text conversion and emotion recognition.
class STT:
    # Initializer loads classifier, diarization, and alignment models.
    def __init__(self, device="cuda", batch_size=16, compute_type="float32"):
        self.device = device
        self.batch_size = batch_size
        self.compute_type = compute_type
        # Load the pre-trained model for Speech Recognition.
        self.model = whisperx.load_model("large", self.device, compute_type=compute_type)
        self.hf_token = os.getenv('HUGGINGFACE_TOKEN')
        self.diarize_model = whisperx.DiarizationPipeline(use_auth_token=self.hf_token,device=self.device)
        self.min_speakers = 2
        self.max_speakers = 2
        self.run_opts = {"device": self.device}

        # Load the pre-trained model for Emotion Recognition.
        self.classifier = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
                                        pymodule_file="custom_interface.py",
                                        classname="CustomEncoderWav2vec2Classifier",
                                        run_opts=self.run_opts)
        self.enhancement_model, self.df_state, _ = init_df()
        self.translator = EasyGoogleTranslate(target_language="en",timeout=10)
        self.CP = {
            "Phone": "6462940064",
            "FirstName": "Mark",
            "SecondName": "Beech",
            "Profile": "Influence",
            "Proficiency": "Native",
        }
        self.HA = {
            "FirstName": "John",
            "SecondName": "Farigous",
            "Profile": "Steadiness",
            "Proficiency": "Native",
        }
        self.CX = {
            "Link_to_Calling_party": "651caf999b59fe2fa9fc1386",
            "Link_Human_agent": "651caf979b59fe2fa9fc1385",
            "Link_Virtual_agent": "",
            "Start_time": "2022-01-01T09:00:00",
            "End_time": "2022-01-01T09:03:00",
            "Original_voice": "file id in grid fs",
            "FirstCallResolution": True,
            "Language": ""
        }

    # Main function for transcribing the audio file and return the results.
    async def transcribe(self, audio_file, speech_enhancement=True, correction=True):
        if speech_enhancement:
            self.enhancement(audio_file)
            audio_file = audio_file + ".enhanced.wav"
        audio = self.load_audio(audio_file)
        diarize_segments = self.diarize(audio)
        result = self.align(audio, diarize_segments)
        result = self.emotion_recognition(audio_file, result)
        if correction:
            result = self.result_correction(result)
        result = self.translate(result)
        with open(audio_file, "rb") as file:
            file_id = await fs.upload_from_stream(audio_file,
                                          file)
        self.CX["Original_voice"] = str(file_id)
        inserted = await insert_cxchannel_data(self.CX)
        inserted = json.loads(inserted.body)
        CX_id = inserted["_id"]
        for segment in result:
            temp = ""
            if  segment["speaker"] == "SPEAKER_01":
                temp = "CP" 
            else:
                temp = "HA"

            utterence = {
                "Starttime": segment["start"],
                "Endtime": segment["end"],
                "Transcript_original": segment["original_text"],
                "Transcript_english": segment["english_text"],
                "Sentiment": segment["emotion"],
                "Source" :temp,
                "Link_to_CX_channel": CX_id
            }

            await insert_utterence_data(utterence)

        return result

    # Function to load audio file.
    @staticmethod
    def load_audio(audio_file):
        return whisperx.load_audio(audio_file)

    # Function to translate text into english
    def translate(self, result):
        for i in range(len(result)):
            result[i]["english_text"] =self.translator.translate(result[i]["original_text"])
        return result

    # Function to perform speaker diarization.
    def diarize(self, audio):
        return self.diarize_model(audio, min_speakers=self.min_speakers, max_speakers=self.max_speakers)

    # Function to perform alignment, assign speakers to words and clean up segments.
    def align(self, audio, diarize_segments):
        result = self.model.transcribe(audio, batch_size=self.batch_size)
        self.CX["Language"] = result["language"]
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
        result = whisperx.align(result["segments"], model_a, metadata, audio,
                                self.device, return_char_alignments=False)
        result = whisperx.assign_word_speakers(diarize_segments, result)
        return STT.clean(result["segments"])

    # Function to perform speech enhancement
    def enhancement(self, audio_file):
        audio, _ = load_audio(audio_file, sr=self.df_state.sr())
        enhanced = enhance(self.enhancement_model, self.df_state, audio)
        save_path = audio_file + ".enhanced.wav"
        save_audio(save_path, enhanced, self.df_state.sr())

    # Consecutive segments spoken by the same speaker are merged.
    @staticmethod
    def clean(segments):
        cleaned = [{"speaker": segments[0]["speaker"], "original_text": segments[0]["text"],
                    "start": segments[0]["start"], "end": segments[0]["end"]}]
        for i in range(1, len(segments)):
            print(cleaned[-1],":", segments[i].keys())
            print("--------------------")
            if "speaker" in segments[i].keys():
                if cleaned[-1]["speaker"] == segments[i]["speaker"]:
                    cleaned[-1]["original_text"] += " " + segments[i]["text"]
                    cleaned[-1]["end"] = segments[i]["end"]
                else:
                    cleaned.append({"speaker": segments[i]["speaker"], "original_text": segments[i]["text"],
                                    "start": segments[i]["start"], "end": segments[i]["end"]})
            else:
                cleaned[-1]["original_text"] += " " + segments[i]["text"]
                cleaned[-1]["end"] = segments[i]["end"]
        return cleaned

    # Assigns emotion to segments and updates result.
    def emotion_recognition(self, audio_file, result):
        audio, sr = librosa.load(audio_file, sr=None)
        for i, seg in enumerate(result):
            start_samples = seg["start"] * sr
            end_samples = seg["end"] * sr
            clip = audio[int(start_samples):int(end_samples)]
            save_path = self.save_temp_clip(i, clip, sr)  
            out_prob, score, index, text_lab = self.classifier.classify_file(save_path)
            result[i]["emotion"] = text_lab[0]
        return result

    # Function to perform trascript correction
    def result_correction(self, result):
        dialogue = ""
        for sentence in result:
            dialogue += sentence["speaker"] + ":"+ sentence["original_text"] + "\n"
        system_msg = """You are TranscriptFixer 4.0, an AI who is skilled in compiling messy interview transcripts to improve their structure without losing the customer's voice.
Your task is to improve text transcript and rewrite it.
While you are rewriting, please silently do the following:
Rule: The original transcript may be incorrect. In this case, a word or words that don't make sense will be present. If, based on the context of the discussion, you can determine what words sound similar that should go there, replace the incorrect words with correct ones
"""
        user_msg = """
Please correct the following dialogue.
###
{}
###
""".format(dialogue)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[{"role": "system", "content": system_msg},
                                                {"role": "user", "content": user_msg}])
        corrected = response["choices"][0]["message"]["content"]
        corrected = corrected.split("\n")
        while "" in corrected:
            corrected.remove("")
        for i, sentence in enumerate(corrected):
            speaker = sentence.split(":")[0]
            res = sentence.split(":")[1]
            print(result)
            if result[i]["speaker"] in speaker:
                result[i]["original_text"] = res
        return result


    # Saves each clip into a temporary wav file.
    @staticmethod
    def save_temp_clip(index, clip, sr):
        save_path = os.path.join("Temp", f'output_{index}.wav')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        sf.write(save_path, clip, sr)
        return save_path

# Create an instance of the STT class for use in FastAPI routes.
stt = STT()

# Endpoint for transcribing the uploaded audio file.
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    global stt
    start_time = time.time()
    file_content = await file.read()
    file_path = os.path.join("Temp", file.filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    response = await stt.transcribe(file_path, speech_enhancement=False, correction=True)
    response_time = time.time() - start_time
    print("Total Response Time : ", response_time)
    return response

# Root endpoint for basic check if the app is running.
@app.get("/")
async def root():
    return {"message": "hello world"}
