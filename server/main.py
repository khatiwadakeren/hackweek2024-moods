from fastapi import FastAPI, Query # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from dotenv import load_dotenv # type: ignore
import httpx # type: ignore
import os
import random

load_dotenv()

search_term = "angry"
giphy_api_key = os.getenv("giphy_api_key")

app = FastAPI()

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



@app.get("/api/gif")
async def search_giphy(q: str = Query(default=search_term)):
    api_url = f"https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": giphy_api_key,
        "q": q,
        "limit": 10,  # You can adjust the limit as needed
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
                    return {"embed_url": embed_url}
                
                
