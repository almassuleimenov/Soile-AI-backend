import os
from fastapi import APIRouter, HTTPException
from groq import AsyncGroq
from app import schemas

router = APIRouter(prefix="/api/chat", tags=["Chat"])

api_key = os.getenv("GROQ_API_KEY")

client = AsyncGroq(api_key=api_key)

@router.post("/ask", response_model=schemas.ChatResponse)
async def ask_ai(request: schemas.ChatRequest):
    if request.language == 'kz':
        system_prompt = """Сен 'Soile AI' мобильді қосымшасының виртуалды логопедісің. 
        Сенің мақсатың - балалардың сөйлеу қабілетін дамытуға қатысты ата-аналардың сұрақтарына қысқа, нақты және мейірімді жауап беру. 
        Жауаптарыңды қазақ тілінде жаз. Тым ұзын жазба, ең көбі 3-4 сөйлем. Эмодзилерді қолдан."""
    else:
        system_prompt = """Ты виртуальный логопед в мобильном приложении 'Soile AI'. 
        Твоя цель - давать короткие, четкие и дружелюбные советы родителям по развитию речи их детей. 
        Отвечай на русском языке. Не пиши слишком длинно, максимум 3-4 предложения. Используй эмодзи."""

    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.7, 
            max_tokens=300,
        )
        
        ai_reply = chat_completion.choices[0].message.content
        return schemas.ChatResponse(reply=ai_reply)

    except Exception as e:
        print(f"Groq API Error: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при обращении к ИИ")