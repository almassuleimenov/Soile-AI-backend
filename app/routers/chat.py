import os
from fastapi import APIRouter, HTTPException
from groq import AsyncGroq
from app import schemas

router = APIRouter(prefix="/api/chat", tags=["Chat"])

api_key = os.getenv("GROQ_API_KEY")
client = AsyncGroq(api_key=api_key)

@router.post("/ask", response_model=schemas.ChatResponse)
async def ask_ai(request: schemas.ChatRequest):
    
    child_info_kz = ""
    child_info_ru = ""
    if request.child_age is not None:
        gender_kz = "ұл" if request.child_gender == "boy" else "қыз"
        gender_ru = "мальчик" if request.child_gender == "boy" else "девочка"
        
        child_info_kz = f"Бала туралы мәлімет: жасы - {request.child_age}, жынысы - {gender_kz}, ата-ананың мақсаты - '{request.parent_goal}'."
        child_info_ru = f"Информация о ребенке: возраст - {request.child_age} лет, пол - {gender_ru}, цель родителя - '{request.parent_goal}'."

    if request.language == 'kz':
        system_prompt = f"""Сен 'Soile AI' мобильді қосымшасының виртуалды логопедісің. 
        {child_info_kz}
        Сенің мақсатың - ата-аналардың сұрақтарына қысқа, нақты және мейірімді жауап беру. 
        Жауаптарыңды қазақ тілінде жаз. Тым ұзын жазба, ең көбі 3-4 сөйлем. Эмодзилерді міндетті түрде қолдан."""
    else:
        system_prompt = f"""Ты профессиональный логопед в мобильном приложении 'Soile AI'. 
        {child_info_ru}
        Твоя цель - давать короткие, четкие и дружелюбные советы родителям. 
        Отвечай на русском языке. Не пиши слишком длинно, максимум 3-4 предложения. Используй эмодзи."""

    # 1. Кладем системный промпт самым первым
    api_messages = [{"role": "system", "content": system_prompt}]
    
    # 2. Добавляем ВСЮ историю переписки, которую прислал телефон
    for msg in request.messages:
        api_messages.append({"role": msg.role, "content": msg.content})

    try:
        chat_completion = await client.chat.completions.create(
            messages=api_messages, # <--- Передаем всю историю
            model="llama-3.3-70b-versatile", 
            temperature=0.7, 
            max_tokens=300,
        )
        
        ai_reply = chat_completion.choices[0].message.content
        return schemas.ChatResponse(reply=ai_reply)

    except Exception as e:
        print(f"Groq API Error: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при обращении к ИИ")