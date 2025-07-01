from pydantic import BaseModel

class GeminiRequest(BaseModel):
    prompt: str
    scope: str = "reciclagem"  # reciclagem, sustentabilidade, ecologia
    response_type: str = "resumida"  # resumida, detalhada, lista, curiosidade, passo-a-passo, infantil 