
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
    if not messages:
        return {"reply": "❌ Сообщение не получено."}

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — AI-финансовый помощник. Отвечай чётко и ясно. "
                        "На каждый вопрос сразу говори переплату и годовую эффективную ставку (ГЭСВ). "
                        "Добавляй немного эмоций: например, 'офигеть', 'это много', 'до добра не доведёт'. "
                        "Избегай расчётов и формул. Скажи вывод и рекомендацию: выгодно ли это, или нет, и как лучше закрыть кредит. "
                        "Если пользователь говорит 'как лучше', 'что делать' — дай конкретный совет. Будь дружелюбным и лаконичным."
                    )
                },
                *messages
            ],
            temperature=0.5,
            max_tokens=500
        )
        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"❌ Ошибка: {str(e)}"}
