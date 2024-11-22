import os
import json
import pytest
from unittest.mock import patch
from langchain_core.messages import HumanMessage, ToolMessage
from app.agents.graph import Agent

# Mock environment variable for testing
os.environ['RAPIDAPI_KEY'] = 'f7b1890a2dmsh7fb453b01443606p18a048jsneecf1af0bcdf'

# Load the sample response from the JSON file
with open('app/agents/sample_data/blr_sin_response.json') as f:
    sample_response = json.load(f)

def mock_requests_post(*args, **kwargs):
    class MockResponse:
        def json(self):
            return sample_response

    return MockResponse()

@patch('app.agents.utils.skyscanner_api.requests.post', side_effect=mock_requests_post)
def test_graph_flights_finder(mock_post):
    agent = Agent()
    # Simulate a natural language input
    initial_state = {'messages': [HumanMessage(content="Find me flights from BLR to SIN on 2024-11-20 and return from SIN to BLR on 2024-12-20")]}
    result = agent.graph.invoke(initial_state)

    assert isinstance(result, dict)
    assert 'messages' in result
    assert len(result['messages']) > 0

    # Check the tool message
    tool_message = result['messages'][0]
    assert tool_message.name == "flights_finder"
    assert "IndiGo" in tool_message.content
    assert "BLR" in tool_message.content
    assert "SIN" in tool_message.content
    assert "$362" in tool_message.content
    assert "USD" in tool_message.content
    assert "Air India" in tool_message.content
    assert "Singapore Airlines" in tool_message.content

# Mock the search_flights function
def mock_search_flights(*args, **kwargs):
    return {
        "flights": [
            {
                "airline": "Mock Airline",
                "departure": "BLR",
                "arrival": "SIN",
                "price": 500,
                "currency": "USD"
            }
        ]
    }

@patch('app.agents.utils.skyscanner_api.search_flights', side_effect=mock_search_flights)
def test_graph_with_flights_tool(mock_search):
    agent = Agent()
    # Simulate a natural language input
    initial_state = {'messages': [HumanMessage(content="Find me flights from BLR to SIN on 2024-11-20 and return from SIN to BLR on 2024-12-20"
                                               )]}
    result = agent.graph.invoke(initial_state)

    assert isinstance(result, dict)
    assert 'messages' in result
    assert len(result['messages']) > 0
    tool_message = result['messages'][0]
    assert tool_message.name == "flights_finder"
    assert "Mock Airline" in tool_message.content
    assert "BLR" in tool_message.content
    assert "SIN" in tool_message.content
    assert "500" in tool_message.content
    assert "USD" in tool_message.content
