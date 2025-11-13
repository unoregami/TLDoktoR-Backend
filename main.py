# FASTapi
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
# SYSTEM intialization libraries
import os
from openai import OpenAI
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel, AutoModelForSeq2SeqLM
import torch
from youtube_transcript_api import YouTubeTranscriptApi
from translation import nllb_token, translate_main
import spacy
from spacy.lang.tl import Tagalog
import gtts_t2s as t2s
import re
from gtts import gTTS
import io
# SYSTEM features methods
from abstractive_sum import openai_summarize
from extractive_sum import summarize
from gpt_textclassifier import classify
from ytvideo_transcript import getTranscript



# Initialization
# OpenAI API
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Extractive BERT model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
bert_model = AutoModel.from_pretrained("bert-base-uncased").to(device)

# YT-transcript-api
ytt_api = YouTubeTranscriptApi()

# Translation
nlp = spacy.load("en_core_web_sm")
nlp_tgl = Tagalog()
nlp_tgl.add_pipe('sentencizer')
gtts_token = t2s.langs
# Taglish model
taglish_model_name = "touno/english_to_taglish_8483_v2"
taglish_tokenizer = AutoTokenizer.from_pretrained(taglish_model_name)
taglish_model = AutoModelForSeq2SeqLM.from_pretrained(taglish_model_name).to(device)
# NLLB model
NLLB_model_name = "facebook/nllb-200-distilled-1.3B"
NLLB_tokenizer = AutoTokenizer.from_pretrained(NLLB_model_name)
NLLB_model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_model_name).to(device)


# Features
app = FastAPI()


# Allow CORS to frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "chrome-extension://hpnailkchddmloppdabobccclkdmfaad"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELS

# Text class
class Text(BaseModel):
    value: str

# Text - Summary length pair
class TextSumLen(BaseModel):
    text: str
    length: int

# YT link - Range pair
class YTLinkRange(BaseModel):
    data: dict
    start: int
    end : int

# Text - Language pair
class TextLanguage(BaseModel):
    text: str
    lang: str


# METHODS

# Sample
@app.post('/print')
async def print_to_console(text: Text):
    print(text.value)
    return {"message": "Data received successfull."}

# Summarization method
@app.post('/to-summarize')
async def to_summarize(data: TextSumLen):
    print("Summarizing text...")
    try:
        text = data.text
        length = data.length
        compression_ratio = 0.4
        text_domain = ""

        match length:
            case 1:
                compression_ratio = 0.2
            case 2:
                compression_ratio = 0.4
            case 3:
                compression_ratio = 0.65
            case _:
                compression_ratio = 0.4

        text_type = classify(text, client)
        summary = ""
        match text_type:
            case "1" | "4":
                if text_type == "1":
                    text_domain = "Science"
                else:
                    text_domain = "Mathematics"

                summary = await run_in_threadpool(
                    summarize,
                    text,
                    compression_ratio,
                    bert_tokenizer,
                    bert_model,
                    device
                )
                print(f"{text_domain} Extractive Summarization done.")
            case "2" | "3":
                if text_type == "2":
                    text_domain = "Programming"
                else:
                    text_domain = "English Literature"

                summary = await run_in_threadpool(
                    openai_summarize,
                    text,
                    length,
                    client
                )
                print(f"{text_domain} Abstractive Summarization done.")
        
        return {"summary": summary}
    except Exception as e:
        print(f"AN ERROR OCCURRED in /to-summarize: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"An internal error occurred: {str(e)}"
        )

# Validate YouTube link, returns YT transcript data and max timestamp
@app.post('/validate/YT')
async def validate_YT(link: Text):
    print("Validating Link...")
    link = link.value
    print("Link:", link)
    try:
        if "youtube" in link:   # URL Link
            print("URL link")
            id = link[link.index("=")+1:]
            data = ytt_api.fetch(id)
            maxTimestamp = round(data[-1].start)

            print("Success fetching.")
            return {
                "status": True,
                "data": data,
                "maxTime": maxTimestamp,
                "startTime": 0
                }
        elif "youtu.be" in link:    # Share link
            print("Share link")
            id = link[17:link.index("?")]
            data = ytt_api.fetch(id)
            startTime = 0
            maxTimestamp = round(data[-1].start)

            if "t=" in link:
                startTime = int(link[link.index("t=")+2:])

            print("Success fetching.")
            return {
                "status": True,
                "data": data,
                "maxTime": maxTimestamp,
                "startTime": startTime
                }
        return { "status": False }
    except Exception as e:
        print(f"AN ERROR OCCURRED in /validate/YT: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"An internal error occurred: {str(e)}"
        )

# Summarize YouTube Video
@app.post('/to-summarize/YT')
async def to_summarize_YT(yt: YTLinkRange):
    print("Summarizing YouTube video...")
    try:
        yt_data = yt.data
        timestamp = [yt.start, yt.end]
        print("YT Data Fetched.")
        print("Timestamp:", timestamp)
        transcript = await run_in_threadpool(
            getTranscript,
            yt_data,
            timestamp
        )
        
        summary = await run_in_threadpool(
                openai_summarize,
                transcript,
                2,
                client
            )
        print("Summarization sucess.")
        return {"summary": summary}
    except Exception as e:
        print(f"AN ERROR OCCURRED in /to-summarize/YT: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"An internal error occurred: {str(e)}"
        )

# Translation method
@app.post('/to-translate')
async def to_translate(data: TextLanguage):
    print("Starting translation...")
    
    try:
        text = data.text
        to = data.lang.lower()
        to = re.sub(" ", "_", to)
        print(f"To {to}")

        translated_text, gtts_target = await run_in_threadpool(
                translate_main,
                text,
                to,
                nlp,
                nlp_tgl,
                gtts_token,
                nllb_token,
                taglish_tokenizer,
                taglish_model,
                NLLB_tokenizer,
                NLLB_model
            )
        print("Translation successful.")
        print("GTTS target:", gtts_target)
        return {
            "text": translated_text,
            "gtts_target": gtts_target
            }
    except Exception as e:
        print(f"AN ERROR OCCURRED in /to-translate: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"An internal error occurred: {str(e)}"
        )

# Play speech
@app.post('/play-speech')
async def play_speech(text: str = Form(...), lang: str = Form('en')):
    mp3_fp = io.BytesIO()

    tts = gTTS(text, lang=lang)
    tts.write_to_fp(mp3_fp)

    mp3_fp.seek(0)

    return StreamingResponse(mp3_fp, media_type="audio/mpeg")
