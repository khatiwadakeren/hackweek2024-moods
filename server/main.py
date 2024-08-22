from fastapi import FastAPI, Query, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from dotenv import load_dotenv # type: ignore
from transformers import pipeline
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import httpx # type: ignore
import os
import random
import glob
from nltk.corpus import wordnet as wn

import nltk

nltk.download('wordnet')
load_dotenv()

search_term = "angry"
giphy_api_key = os.getenv("giphy_api_key")

# Load the setiment detection model in case we want to use it later
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load the emotion detection model
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

# Map moods to sound directories
sound_effect_directories = {
    "anger": "sounds/anger/",
    "joy": "sounds/joy/",
    "neutral": "sounds/neutral/",
    "sadness": "sounds/sadness/",
    "surprise": "sounds/surprise/",
    "happy": "sounds/happy/"
}

app = FastAPI()

# Serve the sounds directory as static files
app.mount("/sounds", StaticFiles(directory=str(Path(__file__).parent / "sounds")), name="sounds")
print(str(Path(__file__).parent / "sounds"))

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

# Main endpoint: Detect mood and return both the GIF URL and sound URL
@app.post("/api/detect-mood")
async def get_gif_and_sound(request: TicketRequest):

    result = emotion_model(request.ticket_body)[0]
    emotion = result['label'].lower()

    # Get the sound effect based on the emotion
    sound_dir = Path(__file__).parent / sound_effect_directories.get(emotion, "server/sounds/default/")
    if sound_dir.exists():
        print(f"Directory exists: {sound_dir}")
        print(f"Files in directory: {os.listdir(sound_dir)}")
    else:
        print(f"Directory does not exist: {sound_dir}")

    sound_files = glob.glob(str(sound_dir / "*.mp3"))

    print(f"Sound files found: {sound_files}")

    sound_url = None  # Initialize sound_url as None
    default_sounds = []  # Initialize default_sounds as an empty list

    if sound_files:
        sound_url = f"/sounds/{emotion}/{os.path.basename(random.choice(sound_files))}"
        print(f"Sound file found: {sound_url}")
    else:
        # Fallback in case no sounds are found
        default_sounds = glob.glob(str(Path(__file__).parent / "sounds/default/*.mp3"))
    print(f"Default sound files: {default_sounds}")
    if default_sounds:
        sound_url = f"/sounds/default/{os.path.basename(random.choice(default_sounds))}"
        print(f"Using default sound: {sound_url}")
    else:
        print("No sound files found in either primary or default directories.")

    api_url = f"https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": giphy_api_key,
        "q": emotion,
        "limit": 50,  # Adjust the limit as needed
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
                    return {"emotion": emotion, "embed_url": embed_url,"sound_url": sound_url}
                else:
                    raise HTTPException(status_code=404, detail="No embed URL found for GIF")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch GIFs from Giphy")
        
def get_emotion(emote: str) -> str:
    # Define broader sets of synonyms for each emotion
    angry_synonyms = {"angry", "mad", "furious", "irate", "enraged", "annoyed", "outraged", "livid", "resentful", "indignant", "anger", "sadness"}
    happy_synonyms = {"happy", "joyful", "cheerful", "content", "pleased", "delighted", "ecstatic", "glad", "satisfied", "joyous", "joy"}
    neutral_synonyms = {"neutral", "indifferent", "unemotional", "calm", "dispassionate", "impartial", "surprise"}

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
