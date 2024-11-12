from langchain_community.tools import BraveSearch

from dotenv import load_dotenv
import os
import json

from openai import OpenAI


import argparse

def chat_with_gpt4(prompt):

    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        # Initialize the OpenAI client
        chat_completion = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": "Given a string, form a search query using it in a question form if applicable, and only return it",
                                },
                                {
                                    "role": "user",
                                    "content": prompt,
                                }
                            ],
                            model="gpt-4o-mini",
                        )

        # Extract and return the response content
        message_content = chat_completion.choices[0].message.content
        return message_content
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def test(prompt):

    query = chat_with_gpt4(prompt=prompt)
    print(query)

    load_dotenv()
    brave_search_api = os.getenv('BRAVE_SEARCH_API')
    tool = BraveSearch.from_api_key(api_key=brave_search_api, search_kwargs={"count": 3})
    results = tool.run(query)
    print(results)

    parsed_list = json.loads(results)

    # Print the title of the first item to verify content
    print(parsed_list)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Search for a query using GPT-4 and Brave Search')
    parser.add_argument('--prompt', default='cheap flights to paris in august', type=str, help='Prompt to use for GPT-4')

    args = parser.parse_args()

    test(args.prompt)
