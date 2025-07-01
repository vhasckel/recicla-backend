import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY')
    GEMINI_API_URL: str = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'

settings = Settings() 