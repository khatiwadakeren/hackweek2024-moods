from fastapi import FastAPI, Query, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from dotenv import load_dotenv # type: ignore
from transformers import pipeline
from pydantic import BaseModel
from nltk.corpus import wordnet as wn
import httpx # type: ignore
import os
import random
import nltk

nltk.download('wordnet')
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
    "http://localhost:5173",  # React app
    "http://127.0.0.1",
    "http://127.0.0.1:5173",  # React app
    "http://127.0.0.1:8000",  # API server
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmoteRequest(BaseModel):
    emote: str

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
        
def get_emotion(emote: str) -> str:
    # Define broader sets of synonyms for each emotion
    angry_synonyms = {"angry", "mad", "furious", "irate", "enraged", "annoyed", "outraged", "livid", "resentful", "indignant"}
    happy_synonyms = {"happy", "joyful", "cheerful", "content", "pleased", "delighted", "ecstatic", "glad", "satisfied", "joyous"}
    neutral_synonyms = {"neutral", "indifferent", "unemotional", "calm", "dispassionate", "impartial"}

    # Convert emote to lowercase and get its WordNet synsets
    emote_lower = emote.lower()

    # Direct check for known synonyms
    if emote_lower in angry_synonyms:
        return "angry"
    elif emote_lower in happy_synonyms:
        return "happy"
    elif emote_lower in neutral_synonyms:
        return "neutral"

    # Fallback to WordNet synonym check
    emote_synsets = wn.synsets(emote_lower)

    for synset in emote_synsets:
        for lemma in synset.lemmas():
            lemma_name = lemma.name().lower()
            if lemma_name in angry_synonyms:
                return "angry"
            elif lemma_name in happy_synonyms:
                return "happy"
            elif lemma_name in neutral_synonyms:
                return "neutral"

    # Default to neutral if no matches found
    return "neutral"

@app.post("/api/emotion-check/")
async def emotion_check(emote_request: EmoteRequest):
    emote = emote_request.emote
    if not emote:
        raise HTTPException(status_code=400, detail="Missing 'emote' parameter")

    detected_emotion = get_emotion(emote)
    return {"emotion": detected_emotion}