import os
import pytest
from unittest.mock import patch
from app.agents.flights import flights_finder, FlightsInput
import json

#Mock environment variable for testing
os.environ['RAPIDAPI_KEY'] = 'f7b1890a2dmsh7fb453b01443606p18a048jsneecf1af0bcdf'

# Load the dummy response from the JSON file
with open('app/agents/sample_data/blr_sin_response.json') as f:
    dummy_response = json.load(f)

def mock_requests_post(*args, **kwargs):
    class MockResponse:
        def json(self):
            return dummy_response

    return MockResponse()

@patch('app.agents.utils.skyscanner_api.requests.post', side_effect=mock_requests_post)
def test_flights_finder_valid_input(mock_post):
    params = FlightsInput(
        departure_airport='BLR',
        arrival_airport='SIN',
        outbound_date='2024-11-20',
        return_date='2024-12-20',
        adults=1,
        children=0,
        infants_in_seat=0,
        infants_on_lap=0
    )

    result = flights_finder.invoke({'params': params})

    assert isinstance(result, dict)
    assert result.get('status') is True
    assert result.get('message') == "Successful"
    assert 'data' in result

# def test_flights_finder_invalid_input():
#     params = FlightsInput(
#         departure_airport='',
#         arrival_airport='',
#         outbound_date='',
#         return_date='',
#         adults=0,
#         children=0,
#         infants_in_seat=0,
#         infants_on_lap=0
#     )

#     result = flights_finder.invoke({'params': params})

#     assert isinstance(result, dict)
#     assert result.get('status') is False
#     assert result.get('message') == "Errors"
#     assert 'errors' in result

# def test_flights_finder_missing_api_key():
#     del os.environ['RAPIDAPI_KEY']

#     params = FlightsInput(
#         departure_airport='BLR',
#         arrival_airport='SIN',
#         outbound_date='2024-11-20',
#         return_date='2024-12-20',
#         adults=1,
#         children=0,
#         infants_in_seat=0,
#         infants_on_lap=0
#     )

#     result = flights_finder.invoke({'params': params})

#     assert isinstance(result, dict)
#     assert result.get('status') is False
#     assert 'errors' in result