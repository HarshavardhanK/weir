
import os

from typing import Annotated, Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

from langchain_community.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv
load_dotenv()

class QuestionDecomposer:
    """A node that decomposes a prompt into smaller questions using LangChain."""

    def __init__(self, llm) -> None:
        self.llm = llm
        self.prompt_template = """Break down the following complex task into 2-3 specific, answerable questions. 
        Format the output as a JSON array of strings.
        
        Task: {input_prompt}
        """

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
            prompt = message.content
        else:
            raise ValueError("No messages in inputs")

        # Create prompt from template
        formatted_prompt = self.prompt_template.format(input_prompt=prompt)
        
        # Get decomposed questions from LLM
        response = self.llm.invoke(formatted_prompt)
        
        try:
            questions = json.loads(response)
            if not isinstance(questions, list):
                raise ValueError("LLM response not in expected list format")
        except json.JSONDecodeError:
            # Fallback in case response isn't valid JSON
            questions = [prompt]

        # Return as messages for the graph
        return {
            "messages": [
                Message(content=question, role="assistant")
                for question in questions
            ]
        }


if __name__ == "__main__":

    llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", 
                    api_key=os.getenv("OPENAI_API_KEY"),
                    max_tokens=500)

    decomposer = QuestionDecomposer(llm)
    
    print(decomposer("I need to travel to Spain from LA on Nov 15th. What are my options?"))