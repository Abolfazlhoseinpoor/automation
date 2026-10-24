import os,httpx
from fastapi import FastAPI,HTTPException,Depends,Request
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
from pydantic import BaseModel
import uuid


load_dotenv()
GEMINI_KEY = os.getenv("gemni_api_key")
MODEL = "gemini-flash-latest"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

app = FastAPI()

api_key = APIKeyHeader (name="Authorization",auto_error=False)
key = str(uuid.uuid4())

def token(token : str = Depends(api_key)):
    if not token or token != key:
        raise HTTPException(status_code=401,detail="shoma dastrasi nadarid!")
    return "khosh amadid!"

@app.middleware("http")
async def guard(request : Request , call_next):
    masir_omomi = ["/docs","/openapi.json","/redoc"]
    if request.url.path not in masir_omomi:
        token = request.headers.get("Authorization")
        if token != key:
            return JSONResponse(
                status_code=401,
                content={"payam":"shoma dastrasi nadarid! "}
            )
    response = await call_next(request)
    return response

history = {}

class chat(BaseModel):
    payam : str

class javab(BaseModel):
    payam : str

async def gemini(payam : list):
    headers = {"Content-Type":"application.json",
               "x-goog-api-key":GEMINI_KEY}
    body = {"contents":payam}
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(url=URL,headers=headers,json=body)
            response.raise_for_status()
            data = response.json()
            print(f"{data} \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            return data["condidates"][0]["content"]["parts"][0]["text"]
        except httpx.TimeoutException :
            raise HTTPException(status_code=504 ,detail="timeout")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.raise_for_status , detail=f"khata gemini : {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500 , detail=f"khataye systemi : {str(e)}")

@app.post("/chat", response_model= javab)
async def javab_gemini(request : chat , user : str = Depends(token)):
    if user not in history:
        history[user] = []
    history[user].append({"role":"user","part":[{"text":request.payam}]})
    try:
        response = await gemini(history[user])
        history[user].append({"role":"model","part":[{"text":response}]})
        return javab(payam=response)
    except Exception as e:
        history[user].pop()
        raise HTTPException(status_code=500,detail=f"{str(e)}")

@app.get("/history")
def history(user:str = Depends(token)):
    return {"user":user,
            "history":history.get(user,[])}

@app.post("/reset")
def clear(user : str = Depends(token)):
    if user in history:
        history[user].clear()
        return "tarikhche pak shod!"
    else:
        return " shoma hich sabeghe ie nadarid!"
    