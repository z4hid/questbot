from crewai_tools import SerperDevTool
from src.config import load_config

def create_search_tool():
    config = load_config()
    return SerperDevTool(api_key=config['SERPER_API_KEY'])