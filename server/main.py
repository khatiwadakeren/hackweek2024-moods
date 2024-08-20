from fastapi import FastAPI, Query, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from dotenv import load_dotenv # type: ignore
from transformers import pipeline
from pydantic import BaseModel
import httpx # type: ignore
import os
import random

load_dotenv()

search_term = "angry"
giphy_api_key = os.getenv("giphy_api_key")

# Load the setiment detection model in case we want to use it later
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load the emotion detection model
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)


app = FastAPI()

# Defines a model for the request body
class TicketRequest(BaseModel):
    ticket_body: str


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# This is the endpoint to test the model
@app.post("/api/test-model")  
async def analyze_emotion(request: TicketRequest):
    # Analyze emotion
    result = emotion_model(request.ticket_body)[0]
    emotion = result['label'].lower() 

    return {"emotion": emotion}

# This was just me playing around with the API
@app.post("/api/sentiment")
async def analyze_sentiment(request: TicketRequest):
    # Analyze sentiment
    result = sentiment_model(request.ticket_body)[0]
    sentiment = result['label'].lower()

    return {"sentiment": sentiment}

#this is the endpoint to test the model, this returns the mood as well as a gif url
@app.post("/api/detect-mood")
async def get_gif(request: TicketRequest):
    result = await analyze_emotion(request)
    print(TicketRequest)
    emotion = result["emotion"]

    api_url = f"https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": giphy_api_key,
        "q": emotion,
        "limit": 10,  # Adjust the limit as needed
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)
        response_data = response.json()

        if response.status_code == 200 and "data" in response_data:
            gifs = response_data["data"]
            if gifs:
                random.shuffle(gifs)
                embed_url = gifs[0].get("embed_url")
                if embed_url:
                    return {"emotion": emotion, "embed_url": embed_url}
                else:
                    raise HTTPException(status_code=404, detail="No embed URL found for GIF")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch GIFs from Giphy")