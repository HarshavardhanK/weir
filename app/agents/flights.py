import os
import json

from typing import Optional
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from app.agents.utils.skyscanner_api import search_flights

class FlightsInput(BaseModel):
    departure_airport: Optional[str] = Field(description='Departure airport code (IATA)')
    arrival_airport: Optional[str] = Field(description='Arrival airport code (IATA)')
    outbound_date: Optional[str] = Field(description='Parameter defines the outbound date. The format is YYYY-MM-DD. e.g. 2024-06-22')
    return_date: Optional[str] = Field(description='Parameter defines the return date. The format is YYYY-MM-DD. e.g. 2024-06-28')
    adults: Optional[int] = Field(1, description='Parameter defines the number of adults. Default to 1.')
    children: Optional[int] = Field(0, description='Parameter defines the number of children. Default to 0.')
    infants_in_seat: Optional[int] = Field(0, description='Parameter defines the number of infants in seat. Default to 0.')
    infants_on_lap: Optional[int] = Field(0, description='Parameter defines the number of infants on lap. Default to 0.')

class FlightsInputSchema(BaseModel):
    params: FlightsInput

@tool(args_schema=FlightsInputSchema)
def flights_finder_real(params: FlightsInput):
    '''
    Find flights using the Skyscanner API.

    Returns:
        dict: Flight search results.
    '''
    try:
        results = search_flights(
            departure_airport=params.departure_airport,
            arrival_airport=params.arrival_airport,
            outbound_date=params.outbound_date,
            return_date=params.return_date,
            adults=params.adults,
            children=params.children,
            infants=params.infants_in_seat + params.infants_on_lap
        )
    except Exception as e:
        results = {"error": str(e)}
        
    #print("Tool response: ", results)
    return results

@tool(args_schema=FlightsInputSchema)
def flights_finder(params: FlightsInput):
    '''
    Find flights using a mock response from a JSON file.

    Returns:
        dict: Flight search results.
    '''
    try:
        # Load the sample response from the JSON file
        with open('app/agents/sample_data/blr_sin_response.json') as f:
            results = json.load(f)
    except Exception as e:
        results = {"error": str(e)}
        
    #print("Tool response: ", results)
    print("what the fyck")
    return results