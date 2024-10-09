from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from src.config import load_config
from src.models.llm_models import llama3_8b
config = load_config()


llm = llama3_8b()


    
# Trip planning agent
trip_agent = Agent(
    role="Efficient Travel Planner",
    goal="Create an optimized travel plan with a focus on speed and budget.",
    backstory="You are a highly efficient and budget-conscious travel planner known for finding the best deals without compromising on quality. You have access to a suite of tools to search for flights, accommodation, and attractions, compare prices, and generate itineraries quickly.",
    
    verbose=False,  # Reducing verbosity for performance
    llm=llm
)