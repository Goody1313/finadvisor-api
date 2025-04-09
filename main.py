
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    messages = data.get("messages", [])
    temperature = data.get("temperature", 0.5)
    max_tokens = data.get("max_tokens", 300)

    # Гарантируем наличие system prompt
    system_message = {
        "role": "system",
        "content": (
            "Ты — AI-ассистент по финансовой грамотности. "
            "Объясняй просто и коротко, желательно в пределах Казахстана. "
            "Всегда стремись помочь пользователю сократить переплату, понять ставку и принять выгодное решение. "
            "Если вопрос не по теме — вежливо уточни."
        )
    }

    # Объединяем system + последние 3 сообщения
    history = [system_message] + messages[-6:]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history,
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"❌ Ошибка: {str(e)}"}
