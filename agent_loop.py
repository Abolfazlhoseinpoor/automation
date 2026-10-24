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
            print(data)
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"error : {e}"


async def dastor():
    chat_history = []
    print("agent is ready talk to him and press exit to exit!")
    while True:
        prompt = input("matn khod ro vared konid: ta agent javab dahad ")
        if prompt == "":
            print("shoma prompt ro vare dnakardid!")
            continue
        if prompt.lower() == "exit":
            print("bye bye ")
            break
        chat_history.append({"role":"user","parts":[{"text":prompt}]})
        print("gemini is thinking ... ")
        javab = await ask_gemini(chat_history)
        print(f"gemini : {javab}")
        if javab and not javab.startswith("Error:"):
            chat_history.append({"role":"model","parts":[{"text":javab}]})
        else:
            chat_history.pop()

asyncio.run(dastor())

