from dotenv import load_dotenv
import asyncio , httpx , os , datetime

load_dotenv()

key = os.getenv("gemni_api_key")
MODEL = "gemini-flash-latest"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def zaman():
    now = datetime.datetime.now().strftime("%Y - %m - %d %H - %M - %S")
    return now

abzar = [{
    "function_declarations": [{
        "name": "zaman",
        "description": "Get the current date and time of the system."
    }]
}]


async def gemini(payam:list):
    headers = {
        "Content-type":"application/json",
        "x-goog-api-key":key
    }
    body ={
        "contents":payam,
        "tools":abzar
    }
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(URL,headers=headers,json=body)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            return {f"error":str(e)}
async def dastor():
    chat_history = []
    print("agent is ready for response type for quiet enter the exit")
    while True:
        prompt = input("lotfan prompt khod ro vared konid : ")
        if prompt == "":
            print("shoma prompty vared nakardid!")
            continue
        if prompt.lower() == "exit":
            print("bye bye")
            break
        chat_history.append({"role":"user","parts":[{"text":prompt}]})
        print("gemini is thinking ... ")
        javab = await gemini(chat_history)
        if "error" in javab:
            print(F"error : {javab['error']}")
            chat_history.pop()
            continue
        print(f"{javab} \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        model = javab["candidates"][0]["content"]["parts"]
        tool = model[0]
        if "functionCall" in tool:
            func = tool["functionCall"]["name"]
            print(f" [Agent decided to use tool: {func}]")
            if func == "zaman":
                func_result = zaman()
                print(f" [Tool Output: {func_result}]")

                chat_history.append({"role": "model", "parts": [{"functionCall": {"name": func, "args": {}}}]})

                chat_history.append({
                    "role": "user", 
                    "parts": [{
                        "functionResponse": {
                            "name": func,
                            "response": {"result": func_result}
                        }
                    }]
                })
                final_result = await gemini(chat_history) 
                print(f"{final_result} \n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                if "candidates" in final_result:
                    final_answer = final_result["candidates"][0]["content"]["parts"][0]["text"]
                    print(f" Agent: {final_answer}")
                    chat_history.append({"role": "model", "parts": [{"text": final_answer}]})
                else:
                    print("Error getting final answer.")
        else:
            answer = tool["text"]
            print(f" Agent: {answer}")
            chat_history.append({"role": "model", "parts": [{"text": answer}]})

                

asyncio.run(dastor())