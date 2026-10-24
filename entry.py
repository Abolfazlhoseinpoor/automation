# ino  az ai komak gereftam va zadam baraye inke bedonm aya cloud flare poshtibani mikone pyton ro va chejory deploy mikoonnd toye cloud flare


import os
import httpx
import datetime
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from workers import WorkerEntrypoint
import asgi

app = FastAPI()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
GEMINI_KEY = os.environ.get("GEMINI_KEY", "")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
MODEL = "gemini-1.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

# ==========================================
# ۱. ابزارها (Tools)
# ==========================================
def zaman():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def search_digikala(query: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    url = f"https://www.digikala.com/search/?q={query}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers, timeout=20, follow_redirects=True)
            soup = BeautifulSoup(resp.text, "html.parser")
            card = soup.find("div", attrs={"data-testid": "product-card"})
            if not card:
                return "محصولی در دیجی‌کالا پیدا نشد."
            
            title = card.find("h3").text.strip() if card.find("h3") else "نامشخص"
            full_text = card.get_text(separator=" ", strip=True)
            price = "نامشخص"
            if "تومان" in full_text:
                parts = full_text.split("تومان")
                price = parts[0].strip().split()[-1] + " تومان"
            return f"دیجی‌کالا: {title} - قیمت: {price}"
        except Exception as e:
            return f"خطا در دیجی‌کالا: {str(e)}"

async def search_torob(query: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    url = f"https://api.torob.com/v4/base-product/search/?page=0&size=1&query={query}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers, timeout=20)
            data = resp.json()
            results = data.get("results", [])
            if not results:
                return "محصولی در ترب پیدا نشد."
                
            item = results[0]
            title = item.get("name", "نامشخص")
            price_toman = int(item.get("price", 0)) // 10
            return f"ترب: {title} - قیمت: {price_toman:,} تومان"
        except Exception as e:
            return f"خطا در ترب: {str(e)}"

abzar = [{
    "function_declarations": [
        {"name": "zaman", "description": "Get the current date and time."},
        {
            "name": "search_digikala",
            "description": "Search for a product price on Digikala.",
            "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]}
        },
        {
            "name": "search_torob",
            "description": "Search for a product price on Torob.",
            "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]}
        }
    ]
}]

# ==========================================
# ۲. ارتباط با Gemini
# ==========================================
async def gemini(messages: list):
    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_KEY}
    body = {"contents": messages, "tools": abzar}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(GEMINI_URL, headers=headers, json=body, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

# ==========================================
# ۳. منطق اصلی پردازش پیام
# ==========================================
user_histories = {}

async def process_message(user_id: int, text: str):
    if user_id not in user_histories:
        user_histories[user_id] = []
    
    user_histories[user_id].append({"role": "user", "parts": [{"text": text}]})
    
    javab = await gemini(user_histories[user_id])
    
    if "error" in javab:
        return f"خطا: {javab['error']}"
    
    model = javab["candidates"][0]["content"]["parts"]
    
    # چک کردن اینکه آیا جمنای درخواست ابزار داده یا نه
    function_calls = [p["functionCall"] for p in model if "functionCall" in p]
    
    if function_calls:
        model_parts_to_append = []
        user_parts_to_append = []
        
        for fc in function_calls:
            func = fc["name"]
            args = fc.get("args", {})
            
            if func == "zaman":
                res = zaman()
            elif func == "search_digikala":
                res = await search_digikala(args.get("query", ""))
            elif func == "search_torob":
                res = await search_torob(args.get("query", ""))
            else:
                res = "ابزار ناشناخته"
            
            model_parts_to_append.append({"functionCall": fc})
            user_parts_to_append.append({"functionResponse": {"name": func, "response": {"result": res}}})
        
        user_histories[user_id].append({"role": "model", "parts": model_parts_to_append})
        user_histories[user_id].append({"role": "user", "parts": user_parts_to_append})
        
        final_result = await gemini(user_histories[user_id])
        
        if "error" in final_result:
            return f"خطای نهایی: {final_result['error']}"
            
        if "candidates" in final_result:
            final_answer = final_result["candidates"][0]["content"]["parts"][0]["text"]
            user_histories[user_id].append({"role": "model", "parts": [{"text": final_answer}]})
            return final_answer
        return "پاسخی دریافت نشد."
    else:
        answer = model[0]["text"]
        user_histories[user_id].append({"role": "model", "parts": [{"text": answer}]})
        return answer

# ==========================================
# ۴. Webhook تلگرام (با لاگ برای دیباگ)
# ==========================================
@app.post("/webhook")
async def telegram_webhook(request: Request):
    print("LOG 1: Webhook received!")
    try:
        update = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"detail": "Invalid JSON"})
    
    if "message" not in update or "text" not in update["message"]:
        return {"ok": True}
    
    message = update["message"]
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    text = message["text"]
    print(f"LOG 2: User text: {text}")
    
    print("LOG 3: Sending waiting message...")
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": "⏳ در حال پردازش..."})
        print(f"LOG 4: Telegram wait msg status: {resp.status_code}")
    
    print("LOG 5: Calling Gemini...")
    reply = await process_message(user_id, text)
    print(f"LOG 6: Gemini replied: {reply[:50]}...")
    
    print("LOG 7: Sending final message...")
    async with httpx.AsyncClient() as client:
        resp2 = await client.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": reply})
        print(f"LOG 8: Telegram final msg status: {resp2.status_code}")
    
    return {"ok": True}

# ==========================================
# ۵. پوسته کلادفلر
# ==========================================
class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)