from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


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

# Text class
class Text(BaseModel):
    value: str


@app.post('/print')
async def print_to_console(text: Text):
    print(text.value)
    return {"message": "Data received successfull."}