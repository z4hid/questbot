from crewai import Agent, Task, Crew
from src.agents.travel import create_trip_agent, trip_agent
from pydantic import BaseModel
from typing import Dict, List

# Pydantic model for structured trip plan
class ComprehensiveTripPlan(BaseModel):
    transportation: Dict[str, str]
    accommodation: Dict[str, str]
    attractions: List[Dict[str, str]]
    fun_places: List[Dict[str, str]]
    budget_breakdown: Dict[str, float]
    recommendations: str


# Task description for efficient trip planning
trip_planning_task = Task(
    description="You need to plan a trip from {start_location} to {destination} for {travel_dates} . The user prioritizes speed and affordability. Create a detailed itinerary using easy language including transportation, accommodation, key attractions, and a budget breakdown.",
    agent=trip_agent,
    expected_output="A clear and concise easy actionable trip plan with all key details covered.",
    output_json=ComprehensiveTripPlan
)

    
# Crew setup for optimized trip planning
travel_planning_crew = Crew(
    agents=[trip_agent],
    tasks=[trip_planning_task],
    verbose=True # Reducing verbosity for performance optimization
)
    
def plan_optimized_trip(start_location: str, destination: str, travel_dates: str):
    trip_details = {
        'start_location': start_location,
        'destination': destination,
        # 'budget': budget,
        'travel_dates': travel_dates
    }
    result = travel_planning_crew.kickoff(inputs=trip_details)
    return result
