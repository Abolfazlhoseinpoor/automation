import httpx, asyncio

async def test():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://www.google.com")
            print("Connection to Google: OK", r.status_code)
    except Exception as e:
        print("Failed:", e)

asyncio.run(test())