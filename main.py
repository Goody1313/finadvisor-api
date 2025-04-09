
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
    temperature = data.get("temperature", 0.4)
    max_tokens = data.get("max_tokens", 300)

    system_prompt = {
        "role": "system",
        "content": (
            "Ты — AI-ассистент по финансовой грамотности и микрокредитам в Казахстане. "
            "Говори кратко, по делу, как опытный консультант. "
            "1. Всегда сначала оценивай процент, переплату, а затем рассчитывай ГЭСВ (годовую эффективную ставку). "
            "2. Если данных не хватает (сумма, срок, ставка) — запроси их. "
            "3. Обязательно предложи, как выгодно погасить кредит: досрочно, ежемесячно, или рефинансировать. "
            "4. Если условия слишком дорогие — удивляйся! Используй эмоции (например: «офигеть», «это тревожно», «до добра не доведёт»), но не переигрывай. "
            "Добавляй emoji при необходимости."
        )
    }

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[system_prompt] + messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"❌ Ошибка: {str(e)}"}
