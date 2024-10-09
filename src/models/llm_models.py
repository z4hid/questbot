from langchain_groq import ChatGroq
from crewai import LLM
from src.config import load_config

def get_groq_model(model_name: str):
    """
    Returns an instance of the specified Large Language Model (LLM) from the Groq Models Hub.
    
    Parameters
    ----------
    model_name : str
        The name of the LLM model to be retrieved.
    
    Returns
    -------
    ChatGroq
        An instance of the specified LLM.
    """
    config = load_config()
    return ChatGroq(
        model=model_name,
        temperature=0.4,
        max_tokens=4096,
        timeout=None,
        max_retries=2,
        groq_api_key=config['GROQ_API_KEY']
    )
    
    

def llama3_8b ():
    config = load_config()
    return LLM(
        model="groq/llama3-8b-8192",
        api_key=config['GROQ_API_KEY'],
        base_url="https://api.groq.com/openai/v1",
        temperature=0.2  # Optimized for focused, quick results
    )

