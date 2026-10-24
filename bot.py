import asyncio
import os
import httpx
import datetime
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("telegram_key")
GEMINI_KEY = os.getenv("gemni_api_key")

bot = Bot(token=TOKEN)
dp = Dispatcher()

MODEL = "gemini-flash-latest"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def zaman():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

abzar = [{
    "function_declarations": [{
        "name": "zaman",
        "description": "Get the current date and time of the system."
    }]
}]


async def gemini(payam: list):
    headers = {
        "Content-type": "application/json",
        "x-goog-api-key": GEMINI_KEY
    }
    body = {
        "contents": payam,
        "tools": abzar
    }
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(URL, headers=headers, json=body)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

user_histories = {}

@dp.message()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "parts": [{"text": message.text}]})

    wait_message = await message.answer("dar hal fekr kardan ...")
    
    javab = await gemini(user_histories[user_id])
    
    if "error" in javab:
        await wait_message.delete()
        await message.answer(f"خطا: {javab['error']}")
        user_histories[user_id].pop() 
        return

    model = javab["candidates"][0]["content"]["parts"]
    tool = model[0]
    
    if "functionCall" in tool:
        func = tool["functionCall"]["name"]
        
        if func == "zaman":
            func_result = zaman()
            
            user_histories[user_id].append({"role": "model", "parts": [{"functionCall": {"name": func, "args": {}}}]})
            user_histories[user_id].append({
                "role": "user", 
                "parts": [{
                    "functionResponse": {
                        "name": func,
                        "response": {"result": func_result}
                    }
                }]
            })
            
            final_result = await gemini(user_histories[user_id])
            
            if "candidates" in final_result:
                final_answer = final_result["candidates"][0]["content"]["parts"][0]["text"]
                user_histories[user_id].append({"role": "model", "parts": [{"text": final_answer}]})
                
                await wait_message.delete()
                await message.answer(f" {final_answer}")
            else:
                await wait_message.delete()
                await message.answer("khatiy rokh dad.")
    else:
        answer = tool["text"]
        user_histories[user_id].append({"role": "model", "parts": [{"text": answer}]})
        
        await wait_message.delete()
        await message.answer(f"gemini:  {answer}")

async def main():
    print("agent rah andazi shod!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())