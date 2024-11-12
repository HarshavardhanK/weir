# agent.py
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent

from scripts.configuration import Configuration

model = ChatOpenAI(model="gpt-4o-mini")

tools = [TavilySearchResults(max_results=2)]

# compiled graph
graph = create_react_agent(model, tools)