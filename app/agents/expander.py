from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from app.agents.state import State
import os

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

"""
1. Design this expander agent to consider train and flight. 
2. If train takes 2x longer than flight, then suggest flight option.
3. If the budget does not allow for flight, then suggest train, but check for the duration of the trip.



"""

def decompose_query(state: State) -> State:
    question = state["input"]
    
    prompt = f"""
    You are an expert at breaking down complex questions into smaller, more manageable parts.
    Question: {question}
    """
    
    response = llm.invoke(prompt)
    sub_questions = response.content.split("\n")
    
    state["output"] = sub_questions
    state["messages"] = sub_questions
    return state

graph = StateGraph(State)
graph.add_node("decompose_question", decompose_query)
graph.add_edge(START, "decompose_question")
graph.add_edge("decompose_question", END)

expander = graph.compile()

def expand_question(question: str):
    return expander.invoke({"input": question})["output"]

if __name__ == "__main__":
    print(expand_question("What is the capital of France?"))