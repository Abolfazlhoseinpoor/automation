import os ,httpx
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("gemni_api_key")
MODEL = "gemini-1-5-latest"
URL =  f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

app = FastAPI()

history = []
class Chat(BaseModel):
    payam : str

class javab(BaseModel):
    payam : str

async def gemini(payam : list):
    headers = {
        "Content-Type":"application/json",
        "x-goog-api-key":GEMINI_KEY
    }
    body = {"contents":payam}
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(url=URL,headers=headers,json=body)
            response.raise_for_status()
            data = response.json()
            print(f"{data} \n\n\n\n\n\n\n\n\n\n\n\n\n")
            return data["condidates"][0]["content"]["parts"][0]["text"]
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Zaman pasokhdehi be payan resid (Timeout).")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Khata az tarafe Gemini: {e.response.text}")           
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Khata dar communication: {str(e)}")


@app.post("/chat",response_model=javab)
async def chat(darkhast : Chat):
    history.append({"role":"user","parts":[{"text":darkhast}]})
    try:
        javab_gemini = await gemini(history)
        history.append({"role":"model","parts":[{"text":javab_gemini}]})
        return javab(payam=javab_gemini)
    except HTTPException:
        history.pop()
    except Exception as e:
        history.pop()
        raise HTTPException(status_code=500, detail=f"Khata dar endpoint: {str(e)}")

@app.get("/history")
def get_history():
    return {"history":history}

@app.post("/reset")
def reset_chat():
    history.clear()
    return {"message": "History pak shod!"}