"""
Teste de detecção de intenções do chatbot
Verifica se o sistema detecta corretamente quando deve executar funções
"""

import re

def has_search_intention(text):
    """Verifica se há intenção clara de busca por pontos de coleta"""
    search_patterns = [
        # Padrões específicos de busca
        r'\b(onde|onde posso|onde eu posso|onde encontrar|onde achar)\b.*\b(descarta?r?|joga?r?|leva?r?|entregar|reciclar)\b',
        r'\b(pontos? de coleta|pontos? de descarte|pontos? de reciclagem)\b',
        r'\b(próximo|perto|próximos?|pertos?)\b.*\b(mim|aqui|de mim|de casa)\b',
        r'\b(buscar|encontrar|achar|localizar)\b.*\b(pontos?|coleta|descarte)\b',
        r'\b(quero|preciso|gostaria de)\b.*\b(descarta?r?|reciclar|encontrar pontos?)\b',
        # Busca por materiais específicos
        r'\b(onde|onde posso|onde eu posso)\b.*\b(pilhas?|baterias?|vidro|plástico|papel|metal|alumínio|eletrônicos?)\b',
        r'\b(descarta?r?|joga?r?|leva?r?)\b.*\b(pilhas?|baterias?|vidro|plástico|papel|metal|alumínio|eletrônicos?)\b',
    ]
    
    for pattern in search_patterns:
        if re.search(pattern, text):
            return True
    return False

def has_stats_intention(text):
    """Verifica se há intenção de obter estatísticas"""
    stats_patterns = [
        r'\b(quantos?|quantas?)\b.*\b(pontos? de coleta|pontos? de descarte)\b',
        r'\b(total|estatísticas|estatisticas|números?|números?)\b.*\b(pontos?|coleta|descarte)\b',
        r'\b(quantos?|quantas?)\b.*\b(tem|existem|há|disponíveis?)\b',
        r'\b(estatísticas|estatisticas|informações?|dados)\b.*\b(pontos?|coleta|descarte)\b',
    ]
    
    for pattern in stats_patterns:
        if re.search(pattern, text):
            return True
    return False

def has_materials_intention(text):
    """Verifica se há intenção de saber sobre materiais aceitos"""
    materials_patterns = [
        r'\b(que|quais|quais são|que tipos? de)\b.*\b(materiais?|materiais? aceitos?|materiais? recicláveis?)\b',
        r'\b(aceitam|aceita|aceito)\b.*\b(que|quais|quais tipos? de)\b',
        r'\b(materiais?|materiais? aceitos?|materiais? recicláveis?)\b.*\b(disponíveis?|aceitos?|que)\b',
        r'\b(reciclar|reciclagem)\b.*\b(que|quais|quais tipos? de)\b.*\b(materiais?)\b',
    ]
    
    for pattern in materials_patterns:
        if re.search(pattern, text):
            return True
    return False

def test_intention_detection():
    """Testa a detecção de intenções"""
    
    print("=== Teste de Detecção de Intenções ===\n")
    
    # Testes que DEVEM ativar function calling
    positive_tests = [
        "Onde posso descartar pilhas usadas?",
        "Quero encontrar pontos de coleta próximos",
        "Preciso reciclar vidro, onde posso levar?",
        "Pontos de coleta perto de mim",
        "Quantos pontos de coleta vocês têm?",
        "Que materiais vocês aceitam?",
        "Onde encontrar pontos de descarte de eletrônicos?",
        "Gostaria de saber onde posso reciclar plástico",
        "Buscar pontos de coleta de papel",
        "Estatísticas dos pontos de coleta",
        "Quais tipos de materiais são aceitos?",
    ]
    
    # Testes que NÃO devem ativar function calling
    negative_tests = [
        "Boa noite",
        "Olá, como vai?",
        "Obrigado pela ajuda",
        "Que dia lindo hoje",
        "Vou reciclar em casa",
        "Reciclagem é importante",
        "O planeta precisa de ajuda",
        "Vamos cuidar do meio ambiente",
        "Bom dia!",
        "Tchau, até logo",
        "Que horas são?",
        "Como está o tempo?",
    ]
    
    print("🔍 TESTES POSITIVOS (devem ativar function calling):")
    print("-" * 50)
    for test in positive_tests:
        search = has_search_intention(test.lower())
        stats = has_stats_intention(test.lower())
        materials = has_materials_intention(test.lower())
        
        intention = "Nenhuma"
        if search:
            intention = "Busca"
        elif stats:
            intention = "Estatísticas"
        elif materials:
            intention = "Materiais"
        
        status = "✅" if (search or stats or materials) else "❌"
        print(f"{status} '{test}' -> {intention}")
    
    print("\n🚫 TESTES NEGATIVOS (NÃO devem ativar function calling):")
    print("-" * 50)
    for test in negative_tests:
        search = has_search_intention(test.lower())
        stats = has_stats_intention(test.lower())
        materials = has_materials_intention(test.lower())
        
        intention = "Nenhuma"
        if search:
            intention = "Busca"
        elif stats:
            intention = "Estatísticas"
        elif materials:
            intention = "Materiais"
        
        status = "❌" if (search or stats or materials) else "✅"
        print(f"{status} '{test}' -> {intention}")
    
    print("\n📊 RESUMO:")
    print("-" * 50)
    
    positive_correct = sum(1 for test in positive_tests 
                          if has_search_intention(test.lower()) or 
                             has_stats_intention(test.lower()) or 
                             has_materials_intention(test.lower()))
    
    negative_correct = sum(1 for test in negative_tests 
                          if not (has_search_intention(test.lower()) or 
                                 has_stats_intention(test.lower()) or 
                                 has_materials_intention(test.lower())))
    
    total_tests = len(positive_tests) + len(negative_tests)
    accuracy = (positive_correct + negative_correct) / total_tests * 100
    
    print(f"Testes positivos corretos: {positive_correct}/{len(positive_tests)}")
    print(f"Testes negativos corretos: {negative_correct}/{len(negative_tests)}")
    print(f"Precisão geral: {accuracy:.1f}%")

if __name__ == "__main__":
    test_intention_detection() 