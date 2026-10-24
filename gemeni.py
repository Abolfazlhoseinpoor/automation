import httpx,asyncio,os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("gemni_api_key")
MODEL = "gemini-flash-latest"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
async def ask_gemini(payam: list):
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": key
    }
    body = {
        "contents": payam
    }
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response =await client.post(URL,headers=headers,json=body)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"error : {e}")

async def dastor():
    chat_history = [
        {"role": "user", "parts": [{"text": "Salam! Esm man Ali hast."}]},
        {"role": "model", "parts": [{"text": "Salam Ali! Khoshbakhtam. Chetori?"}]},
        {"role": "user", "parts": [{"text": "Esm man chie?"}]}
    ]
    javab = await ask_gemini(chat_history)
    print(f"gemini: {javab}")

asyncio.run(dastor())