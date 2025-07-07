import os
import json
from fastapi import HTTPException
from app.core.config import settings
from app.services.collection_points_service import collection_points_service
from app.models.collection_point import CollectionPointFilters
import google.generativeai as genai

SYSTEM_PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "docs",
    "chatbot-system-prompt.txt",
)
with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

genai.configure(api_key=settings.GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-flash-latest"
chat_sessions = {}

tools = [
    {
        "name": "get_collection_points",
        "description": "Busca e filtra pontos de coleta com base em vários critérios combinados, como material, bairro, cidade, proximidade geográfica (latitude/longitude) ou um termo de busca geral.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "material": {
                    "type": "STRING",
                    "description": "Filtra por um material específico (ex: 'Vidro', 'Pilhas').",
                },
                "neighborhood": {
                    "type": "STRING",
                    "description": "Filtra por um bairro específico.",
                },
                "city": {
                    "type": "STRING",
                    "description": "Filtra por uma cidade específica.",
                },
                "search": {
                    "type": "STRING",
                    "description": "Termo de busca geral para nome, rua ou descrição do ponto.",
                },
                "lat": {
                    "type": "NUMBER",
                    "description": "Latitude do usuário para busca por proximidade.",
                },
                "lng": {
                    "type": "NUMBER",
                    "description": "Longitude do usuário para busca por proximidade.",
                },
                "radius_km": {
                    "type": "NUMBER",
                    "description": "Raio em quilômetros para a busca por proximidade (padrão: 5.0).",
                },
            },
        },
    },
    {
        "name": "get_collection_points_statistics",
        "description": "Obtém estatísticas sobre os pontos de coleta, como contagem total, distribuição por bairro e por material.",
        "parameters": {"type": "OBJECT", "properties": {}},
    },
    {
        "name": "get_available_materials",
        "description": "Lista todos os materiais que podem ser reciclados nos pontos de coleta.",
        "parameters": {"type": "OBJECT", "properties": {}},
    },
]

# Instancia o modelo
model = genai.GenerativeModel(
    MODEL_NAME,
    system_instruction=SYSTEM_PROMPT,
    tools=tools,
    tool_config={"function_calling_config": "ANY"},
)

SAUDACOES = [
    "olá",
    "oi",
    "boa noite",
    "bom dia",
    "boa tarde",
    "tudo bem",
    "obrigado",
    "valeu",
]


def is_saudacao(prompt):
    return any(s in prompt.lower() for s in SAUDACOES)


def execute_function(function_call: dict) -> dict:
    function_name = function_call.name
    params = function_call.args
    print(
        f"[Executor] Gemini solicitou a função: {function_name} com parâmetros: {params}"
    )
    try:
        if function_name == "get_collection_points":
            filters = CollectionPointFilters(**params)
            results = collection_points_service.get_all_collection_points(
                filters=filters
            )
            data_to_return = [p.model_dump() for p in results]
            return {"data": data_to_return, "count": len(data_to_return)}
        elif function_name == "get_collection_points_statistics":
            stats = collection_points_service.get_collection_points_statistics()
            return {"data": stats}
        elif function_name == "get_available_materials":
            from app.data.mock_collection_points import AVAILABLE_MATERIALS

            return {"data": AVAILABLE_MATERIALS}
        else:
            return {"error": f"Função desconhecida: {function_name}"}
    except Exception as e:
        print(f"[Executor] Erro ao executar a função '{function_name}': {e}")
        return {"error": f"Ocorreu um erro interno ao tentar executar a ação: {str(e)}"}


def get_or_create_chat_session(session_id: str):
    if session_id not in chat_sessions:
        print(f"Criando nova sessão de chat para: {session_id}")
        chat_sessions[session_id] = model.start_chat(history=[])
    return chat_sessions[session_id]


def call_gemini_with_memory(
    user_prompt: str, session_id: str, user_location: dict = None
) -> str:
    try:
        chat = get_or_create_chat_session(session_id)

        full_prompt = user_prompt
        if user_location and user_location.get("lat") and user_location.get("lng"):
            loc = user_location
            full_prompt += f" (Minha localização atual para referência é latitude {loc['lat']} e longitude {loc['lng']})."

        print(
            f"[GeminiService] Enviando prompt para a sessão {session_id}: '{full_prompt}'"
        )

        # 1. Envia a mensagem inicial
        response = chat.send_message(full_prompt)

        # Extrai a primeira (e geralmente única) parte da resposta para análise
        response_part = response.parts[0] if response.parts else None

        # 2. Verifica se o Gemini solicitou uma chamada de função
        if response_part and hasattr(response_part, "function_call"):
            function_call = response_part.function_call
            if is_saudacao(user_prompt):
                return "Olá! Como posso ajudar você com reciclagem, ecologia ou sustentabilidade hoje?"
            function_response_data = execute_function(function_call)
            if function_call.name == "get_collection_points":
                return format_collection_points_response(function_response_data)
            elif function_call.name == "get_collection_points_statistics":
                return format_statistics_response(function_response_data)
            else:
                return json.dumps(function_response_data, ensure_ascii=False, indent=2)

        # Se não for function_call, retorna o texto normalmente
        final_text = "".join(part.text for part in response.parts)
        if final_text:
            print(f"[DEBUG] Texto final recebido: {final_text}")
            return final_text

        return "Não foi possível gerar uma resposta em texto."

    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


def format_collection_points_response(function_response_data):
    pontos = function_response_data.get("data", [])
    if not isinstance(pontos, list):
        return "Não foi possível encontrar pontos de coleta para sua busca."
    if not pontos:
        return "Nenhum ponto de coleta encontrado para sua busca."
    resposta = f"Encontrei {len(pontos)} pontos de coleta próximos a você! Aqui estão os mais relevantes:\n\n"
    for ponto in pontos[:5]:
        resposta += (
            f"• {ponto['name']} - {ponto['street']}, {ponto['number']}, {ponto['neighborhood']}\n"
            f"  Materiais aceitos: {', '.join(ponto['materials'])}\n"
            f"  Horário: {ponto['operating_hours']}\n"
            f"  Distância: {ponto.get('distance_km', '?')} km\n\n"
        )
    resposta += "Que tal visitar um desses pontos? Cada atitude conta para um mundo mais verde! 🌱"
    return resposta


def format_statistics_response(function_response_data):
    stats = function_response_data.get("data", {})
    if not isinstance(stats, dict):
        return "Não foi possível obter as estatísticas."
    resposta = "Aqui estão algumas estatísticas dos pontos de coleta:\n"
    resposta += f"- Total de pontos: {stats.get('total_points', '?')}\n"
    materiais = stats.get("materials_distribution", {})
    if materiais:
        resposta += "- Distribuição de materiais:\n"
        for mat, qtd in materiais.items():
            resposta += f"  • {mat}: {qtd}\n"
    bairros = stats.get("neighborhoods_distribution", {})
    if bairros:
        resposta += "- Distribuição por bairro:\n"
        for bairro, qtd in bairros.items():
            resposta += f"  • {bairro}: {qtd}\n"
    resposta += f"- Pontos que aceitam todos os materiais: {stats.get('points_accepting_all_materials', '?')}\n"
    return resposta
