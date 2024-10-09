from src.config import load_config
from crewai import LLM


def llama3_8b():
    config = load_config()
    return LLM(    model="groq/llama3-8b-8192",
    api_key=config['GROQ_API_KEY'],
    base_url="https://api.groq.com/openai/v1",
    temperature=0.2  # Optimized for focused, quick results)
    )