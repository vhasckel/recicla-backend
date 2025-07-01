from fastapi import APIRouter, Request
from app.services.gemini_service import call_gemini_with_memory

router = APIRouter()

@router.post("/gemini")
async def handle_chat(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt")
    session_id = data.get("session_id", "default_user")
    
    # Opcional: coordenadas do usuário para buscas por proximidade
    user_location = data.get("user_location", {})
    
    # Passar localização como parâmetro separado, não como parte do prompt
    response_text = call_gemini_with_memory(user_prompt, session_id, user_location)
    
    return {"response": response_text} 