from crewai import Agent, Task, Crew, LLM
from src.config import load_config
from src.models.llm_models import llama3_8b
config = load_config()

    
def create_trip_agent():
    """
    Creates an Agent that is an efficient travel planner. The agent is
    responsible for creating an optimized travel plan with a focus on speed
    and budget. The agent is also very verbose and will explain each step it
    takes to create the plan.

    Returns:
        Agent: The created agent.
    """
    llm = llama3_8b()
    
    trip_agent = Agent(
        role="Efficient Travel Planner",
        goal="Create an optimized travel plan with a focus on speed and budget.",
        backstory="You are a highly efficient and budget-conscious travel planner known for finding the best deals without compromising on quality.",
        verbose=False,
        llm=llm
    )
    return trip_agent