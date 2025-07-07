## Visão Geral

O chatbot do Recicla App utiliza as capacidades avançadas de **Function Calling** (também conhecido como Tool Use) do modelo Gemini. Isso permite que ele execute ações específicas do aplicativo e forneça respostas contextuais baseadas em dados em tempo real do nosso sistema, de forma inteligente e flexível.

## Como Funciona

O processo é orquestrado pela inteligência do próprio modelo de linguagem, seguindo um fluxo moderno e eficiente:

1.  **Análise da Intenção pelo Modelo**: O usuário envia uma mensagem (ex: "onde posso reciclar pilhas perto de casa?"). O prompt é enriquecido com a localização do usuário, se disponível.

2.  **Seleção de Ferramenta (Function Calling)**: O modelo Gemini analisa a mensagem e a compara com a lista de "ferramentas" (nossas funções) que ele conhece. Ele determina que a melhor ferramenta para responder é a `get_collection_points` e deduz os parâmetros necessários (`material="Pilhas"`, `lat=...`, `lng=...`).

3.  **Execução da Função no Backend**: Nosso backend recebe a solicitação do Gemini, executa a função `get_collection_points` com os parâmetros fornecidos e busca os dados reais no nosso `collection_points_service`.

4.  **Retorno dos Dados para o Modelo**: Os resultados da busca (a lista de pontos de coleta) são enviados de volta para o Gemini.

5.  **Resposta Final e Contextual**: Com os dados em mãos, o Gemini gera uma resposta final em linguagem natural, amigável e útil para o usuário, listando os pontos encontrados de forma organizada.

## Funções (Ferramentas) Disponíveis

O modelo Gemini tem acesso às seguintes ferramentas:

1.  **`get_collection_points`**

    - Busca e filtra pontos de coleta com base em vários critérios combinados.
    - Parâmetros: `material`, `neighborhood`, `city`, `lat`, `lng`, `radius_km`, `search`.

2.  **`get_collection_points_statistics`**

    - Obtém estatísticas sobre os pontos de coleta (contagem total, etc.).
    - Não possui parâmetros.

3.  **`get_available_materials`**
    - Lista todos os tipos de materiais aceitos na plataforma.
    - Não possui parâmetros.

## Exemplos de Uso

A inteligência do modelo permite uma conversa fluida.

### ✅ Exemplos que ATIVAM o Function Calling:

**Busca por Material Específico:**

- "Onde posso descartar pilhas usadas?"
- "Preciso reciclar vidro, onde posso levar?"
- "Gostaria de saber onde posso reciclar eletrônicos na Trindade" (Combina material e bairro)

**Busca por Proximidade:**

- "Pontos de coleta perto de mim"
- "Quero encontrar pontos de coleta próximos"

**Estatísticas:**

- "Quantos pontos de coleta vocês têm em Florianópolis?"
- "Me mostre as estatísticas dos pontos de coleta"

### ❌ Exemplos que NÃO ativam o Function Calling:

(O modelo responde como uma conversa normal)

- "Boa noite"
- "Obrigado pela ajuda"
- "Reciclagem é muito importante para o planeta"

## Implementação Técnica

### Backend (Python/FastAPI + Gemini)

A implementação é centrada em descrever as ferramentas para o modelo e deixar que ele decida quando usá-las.

```python

tools = {
    "get_collection_points": {
        "description": "Busca e filtra pontos de coleta com base em vários critérios...",
        "parameters": { "type": "object", "properties": { # ...parâmetros
        }}
    },
}

model = genai.GenerativeModel(MODEL_NAME, tools=tools)

chat = model.start_chat(enable_automatic_function_calling=True)
response = chat.send_message(user_prompt)

```
