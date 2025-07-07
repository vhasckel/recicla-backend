"""
Teste do chatbot com function calling
Demonstra como o chatbot pode executar ações específicas do app
"""

from app.services.gemini_service import call_gemini_with_memory, execute_function
from app.services.collection_points_service import collection_points_service


def test_function_calling():
    """Testa as funcionalidades do chatbot com function calling"""

    print("=== Teste do Chatbot com Function Calling ===\n")

    # Teste 1: Busca por pontos de coleta de pilhas
    print("1. Usuário pergunta: 'Onde posso descartar pilhas usadas?'")
    response1 = call_gemini_with_memory(
        "Onde posso descartar pilhas usadas?", "test_user_1"
    )
    print(f"Resposta: {response1}\n")

    # Teste 2: Busca por pontos próximos (com coordenadas)
    print(
        "2. Usuário pergunta: 'Quais pontos de coleta ficam perto de mim?' (com localização)"
    )
    response2 = call_gemini_with_memory(
        "Quais pontos de coleta ficam perto de mim? Localização do usuário: Latitude -27.5969, Longitude -48.5495",
        "test_user_2",
    )
    print(f"Resposta: {response2}\n")

    # Teste 3: Busca por estatísticas
    print("3. Usuário pergunta: 'Quantos pontos de coleta vocês têm?'")
    response3 = call_gemini_with_memory(
        "Quantos pontos de coleta vocês têm?", "test_user_3"
    )
    print(f"Resposta: {response3}\n")

    # Teste 4: Busca por materiais aceitos
    print("4. Usuário pergunta: 'Que tipos de materiais vocês aceitam?'")
    response4 = call_gemini_with_memory(
        "Que tipos de materiais vocês aceitam?", "test_user_4"
    )
    print(f"Resposta: {response4}\n")

    # Teste 5: Pergunta fora do escopo
    print("5. Usuário pergunta: 'Qual é o melhor time de futebol?'")
    response5 = call_gemini_with_memory(
        "Qual é o melhor time de futebol?", "test_user_5"
    )
    print(f"Resposta: {response5}\n")


def test_direct_functions():
    """Testa as funções diretamente"""

    print("=== Teste Direto das Funções ===\n")

    # Teste da função de busca por material
    print("1. Buscando pontos que aceitam 'Pilhas':")
    result1 = execute_function("search_collection_points", {"material": "Pilhas"})
    print(f"Resultado: {result1}\n")

    # Teste da função de busca por coordenadas
    print("2. Buscando pontos próximos ao centro de Florianópolis:")
    result2 = execute_function(
        "search_collection_points", {"lat": -27.5969, "lng": -48.5495, "radius_km": 2.0}
    )
    print(f"Resultado: {result2}\n")

    # Teste da função de estatísticas
    print("3. Obtendo estatísticas:")
    result3 = execute_function("get_collection_points_statistics", {})
    print(f"Resultado: {result3}\n")


if __name__ == "__main__":
    test_direct_functions()
    print("\n" + "=" * 50 + "\n")
    test_function_calling()
