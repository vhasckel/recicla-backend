"""
Debug do chatbot - Testa diferentes cenários para identificar problemas
"""

import requests
import json

def test_chatbot_scenarios():
    """Testa diferentes cenários do chatbot"""
    
    url = 'http://localhost:5000/api/gemini'
    
    test_cases = [
        {
            'name': 'Saudação simples',
            'data': {
                'prompt': 'boa noite',
                'session_id': 'test_user_1',
                'user_location': None
            }
        },
        {
            'name': 'Saudação com localização',
            'data': {
                'prompt': 'boa noite',
                'session_id': 'test_user_2',
                'user_location': {
                    'lat': -27.5969,
                    'lng': -48.5495
                }
            }
        },
        {
            'name': 'Busca por pilhas',
            'data': {
                'prompt': 'Onde posso descartar pilhas usadas?',
                'session_id': 'test_user_3',
                'user_location': None
            }
        },
        {
            'name': 'Busca por pilhas com localização',
            'data': {
                'prompt': 'Onde posso descartar pilhas usadas?',
                'session_id': 'test_user_4',
                'user_location': {
                    'lat': -27.5969,
                    'lng': -48.5495
                }
            }
        },
        {
            'name': 'Olá simples',
            'data': {
                'prompt': 'olá',
                'session_id': 'test_user_5',
                'user_location': None
            }
        },
        {
            'name': 'Oi simples',
            'data': {
                'prompt': 'oi',
                'session_id': 'test_user_6',
                'user_location': None
            }
        },
        {
            'name': 'Processo de reciclagem',
            'data': {
                'prompt': 'Qual o processo de reciclagem de garrafas de plástico?',
                'session_id': 'test_user_7',
                'user_location': None
            }
        }
    ]
    
    print("=== Debug do Chatbot ===\n")
    
    for test in test_cases:
        print(f"🧪 Teste: {test['name']}")
        print(f"📤 Enviando: {test['data']['prompt']}")
        
        # Remove user_location se for None para não enviar campo nulo no JSON
        data = {k: v for k, v in test['data'].items() if v is not None}
        
        try:
            response = requests.post(url, json=data)
            result = response.json()
            
            response_text = result.get('response', 'Erro')
            print(f"📥 Resposta (raw): {repr(response_text)}")
            print(f"📥 Resposta (formatada): {response_text}")
            
            # Verificar se a resposta contém pontos de coleta (não deveria para saudações)
            if 'boa noite' in test['data']['prompt'].lower() or 'olá' in test['data']['prompt'].lower() or 'oi' in test['data']['prompt'].lower():
                if any(word in response_text for word in ['ponto', 'coleta', 'descarte', 'rua', 'endereço']):
                    print("❌ PROBLEMA: Saudação retornou pontos de coleta!")
                else:
                    print("✅ OK: Saudação retornou resposta adequada")
            else:
                if any(word in response_text for word in ['ponto', 'coleta', 'descarte']):
                    print("✅ OK: Busca retornou pontos de coleta")
                else:
                    print("❓ Inesperado: Busca não retornou pontos de coleta")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_chatbot_scenarios() 