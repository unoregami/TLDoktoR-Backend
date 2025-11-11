# FASTapi
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
# SYSTEM intialization libraries
import os
from openai import OpenAI
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
import torch
from youtube_transcript_api import YouTubeTranscriptApi
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
device = None or ("cuda" if torch.cuda.is_available() else "cpu")
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
bert_model = AutoModel.from_pretrained("bert-base-uncased").to(device)

# YT-transcript-api
ytt_api = YouTubeTranscriptApi()

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
    link: str
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
    try:
        text = data.text
        length = data.length

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
                summary = await run_in_threadpool(
                    summarize,
                    text,
                    compression_ratio,
                    bert_tokenizer,
                    bert_model,
                    device
                )
                print(f"{text_type} Extractive Summarization done.")
            case "2" | "3":
                summary = await run_in_threadpool(
                    openai_summarize,
                    text,
                    length,
                    client
                )
                print(f"{text_type} Abstractive Summarization done.")
        
        return {"summary": summary}
    except Exception as e:
        print(f"AN ERROR OCCURRED in /to-summarize: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"An internal error occurred: {str(e)}"
        )

# Validate YouTube link
@app.post('/validate/YT')
async def validate_YT(link: Text):
    print(link.value)

# Summarize YouTube Video
@app.post('/to-summarize/YT')
async def to_summarize_YT(data: YTLinkRange):
    link = data.link
    timestamp = [data.start, data.end]

    print(f"Link: {link}\nTimestamp: {timestamp}")

# Translation method
@app.post('/to-translate')
async def to_translate(data: TextLanguage):
    text = data.text
    to = data.lang.lower()
    print(f"Text: {text}\nLanguage: {to}")