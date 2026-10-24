import httpx, asyncio, os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("gemni_api_key") 

MODEL = "gemini-flash-latest" 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

async def ask_gemini(prompt: str):
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": key
    }
    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(URL, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

async def dastor():
    javab = await ask_gemini("Salam! Khodet ro moarefi kon.")
    print(f"gemini: {javab}")

asyncio.run(dastor())