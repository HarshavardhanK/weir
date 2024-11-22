import requests
import json
import os

from dotenv import load_dotenv

def search_flights(departure_airport, arrival_airport, outbound_date, return_date, adults=1, children=0, infants=0):
    
    load_dotenv()
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-multi-city"

    payload = {
        "market": "US",
        "locale": "en-US",
        "currency": "USD",
        "adults": adults,
        "children": children,
        "infants": infants,
		"cabinClass": "economy",
		"stops": ["direct", "1stop", "2stops"],
		"sort": "cheapest_first",
		"flights": [
			{
				"fromEntityId": departure_airport,
				"toEntityId": arrival_airport,
				"departDate": outbound_date
			},
			{
				"fromEntityId": arrival_airport,
				"toEntityId": departure_airport,
				"departDate": return_date
			}
		]
	}
    
    headers = {
		"x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
		"x-rapidapi-host": "sky-scanner3.p.rapidapi.com",
		"Content-Type": "application/json"
	}

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
