import datetime
import operator
import os
from typing import Annotated, TypedDict
import logging
from logging.handlers import SysLogHandler

from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

from app.agents.flights import flights_finder

import uuid

# Configure the logger
logger = logging.getLogger('app_logger')
logger.setLevel(logging.ERROR)

# Create a handler for Logstash
logstash_handler = SysLogHandler(address=('logstash', 5044))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logstash_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(logstash_handler)

# Load environment variables
load_dotenv()

CURRENT_YEAR = datetime.datetime.now().year

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

TOOLS_SYSTEM_PROMPT = f"""You are a smart travel agency. Use the tools to look up information.
    You are allowed to make multiple calls (either together or in sequence).
    Only look up information when you are sure of what you want.
    The current year is {CURRENT_YEAR}.
    I want to have in your output links to flights websites (if possible).
    I want to have as well the logo of the airline company (if possible).
    In your output always include the price of the flight and the currency as well (if possible).
    """

TOOLS = [flights_finder]

DATABASE_URL = os.getenv('DATABASE_URL')


class Agent:

    def __init__(self):
        self._tools = {t.name: t for t in TOOLS}
        self._tools_llm = ChatOpenAI(model='gpt-4o-mini').bind_tools(TOOLS)
        
        self.memory_store = InMemoryStore()
        
        #checkpoint = checkpointer.get(config)

        self.builder = StateGraph(AgentState)
        self.builder.add_node('retrieve_memory', self.retrieve_memory)
        self.builder.add_node('update_memory', self.update_memory)
        self.builder.add_node('call_tools_llm', self.call_tools_llm)
        self.builder.add_node('invoke_tools', self.invoke_tools)
        
        self.builder.set_entry_point('retrieve_memory')
        #builder.add_node('flights_finder', flights_finder)
        self.builder.add_edge('retrieve_memory', 'call_tools_llm')
        self.builder.add_conditional_edges('call_tools_llm', self.exists_action, {'more_tools': 'invoke_tools', 
                                                                             'update_memory': 'update_memory'})
        self.builder.add_edge('invoke_tools', 'call_tools_llm')
        self.builder.add_edge('update_memory', END)
        
        #memory = MemorySaver()
    
    def get_builder(self):
        return self.builder

    @staticmethod
    def exists_action(state: AgentState):
        result = state['messages'][-1]
        
        if len(result.tool_calls) == 0:
            return 'update_memory'
        return 'more_tools'
    
    def retrieve_memory(self, state: AgentState, config):
        store = self.memory_store
        user_id = config["configurable"]["user_id"]
        namespace = (user_id, "memories")
        memories = store.search(namespace)
        print("Memories: ", memories)
        
        memory_messages = [memory['value']['messages'] for memory in memories]
        history = '\n'.join(memory_messages)
        print(f"Memory Retrieved:\n {history}")
        
        return {"messages": [SystemMessage(content=f"Memory:\n {history}")] + state["messages"]}
    
    def update_memory(self, state: AgentState, config):
        store = self.memory_store
        user_id = config["configurable"]["user_id"]
        namespace = (user_id, "memories")
        
        memory_id = str(uuid.uuid4())
        store.put(namespace, memory_id, {"messages": state["messages"]})
        print(f"Memory Updated:\n {state['messages']}")
        return state
    
    def call_tools_llm(self, state: AgentState):
        print("Calling tools LLM")
        messages = state['messages']
        messages = [SystemMessage(content=TOOLS_SYSTEM_PROMPT)] + messages
        message = self._tools_llm.invoke(messages)
        return {'messages': [message]}

    def invoke_tools(self, state: AgentState):
        print("Invoking tools")
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            if not t['name'] in self._tools:  # check for bad tool name from LLM
                result = 'bad tool name, retry'  # instruct LLM to retry if bad
            else:
                result = self._tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        return {'messages': results}


def call_agent(message: str, user_id: str, namespace: str, thread_id: str):
    try:
        agent = Agent()
        builder = agent.get_builder()
        
        with PostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
            checkpointer.setup()
            print("Compiling graph")
            graph = builder.compile(checkpointer=checkpointer, store=agent.memory_store)
            print("Graph compiled")
            initial_state = {'messages': [HumanMessage(content=message)]}
            print("Invoking graph")
        
            message = graph.invoke(initial_state, config={"configurable": {"user_id": user_id, "checkpoint_ns": namespace, "thread_id": thread_id}})
            return {"message": message["messages"][-1].content} 
    except Exception as e:
        logger.error("An error occurred in call_agent", exc_info=True)

if __name__ == "__main__":
    agent = Agent()
    # Example usage
    initial_state = {'messages': [HumanMessage(content="Find me flights from BLR to SIN on 2024-11-23, and return from SIN to BLR on 2024-12-20")]}
    #response = agent.graph.invoke(initial_state)
    #print(response)
