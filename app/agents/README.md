# Agents Directory

This directory contains the core logic for the Weir application, including the implementation of various agents responsible for handling different aspects of travel planning. The agents utilize tools and APIs to process user queries and provide recommendations.

## Key Components

- **graph.py**: Defines the main agent class and the logic for invoking tools and managing state transitions.
- **flights.py**: Contains tools for finding flights using external APIs or mock data.
- **memory.py**: Implements tools for storing and retrieving user memory data in PostgreSQL.
- **planner.py**: Manages the planning logic and integrates with various tools for travel recommendations.

The agents are designed to be extensible, allowing for the integration of additional tools and services.