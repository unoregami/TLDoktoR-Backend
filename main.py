from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

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
    text = data.text
    length = data.length

    match length:
        case 1:
            lengthText = "Short"
        case 2:
            lengthText = "Medium"
        case 3:
            lengthText = "Long"
        case _:
            lengthText = "Medium"
    print(f"Text: {text}\nLength ({length}): {lengthText}")

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