from src.config import load_config
from langchain_groq import ChatGroq
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




    

