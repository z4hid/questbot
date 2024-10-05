import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'TELEGRAM_API_KEY': os.getenv('TELEGRAM_API_KEY'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
        'SERPER_API_KEY': os.getenv('SERPER_API_KEY')
    }
