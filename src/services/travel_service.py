from crewai import Agent, Task, Crew
from src.models.llm_models import get_groq_model
from pydantic import BaseModel
from typing import Dict, List
from src.agents import create_trip_agent

class ComprehensiveTripPlan(BaseModel):
    transportation: Dict[str, str]
    accommodation: Dict[str, str]
    attractions: List[Dict[str, str]]
    fun_places: List[Dict[str, str]]
    budget_breakdown: Dict[str, float]
    recommendations: str

class TravelPlannerService:
    def __init__(self):
        self.trip_agent = create_trip_agent()
        self.trip_planning_task = Task(
            description="You need to plan a trip from {start_location} to {destination} for {travel_dates}. "
                        "The user prioritizes speed and affordability. Create a detailed itinerary including "
                        "transportation, accommodation, key attractions, and a budget breakdown.",
            agent=self.trip_agent,
            expected_output="A clear and actionable trip plan with all key details covered.",
            output_json=ComprehensiveTripPlan
        )
        self.travel_planning_crew = Crew(
            agents=[self.trip_agent],
            tasks=[self.trip_planning_task],
            verbose=True
        )

    def plan_optimized_trip(self, start_location: str, destination: str, travel_dates: str):
        trip_details = {
            'start_location': start_location,
            'destination': destination,
            'travel_dates': travel_dates
        }
        try:
            result = self.travel_planning_crew.kickoff(inputs=trip_details)
            return result.parsed if result.parsed else result.raw
        except Exception as e:
            return f"An error occurred during trip planning: {str(e)}"
