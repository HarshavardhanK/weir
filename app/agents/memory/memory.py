import os
import json
from typing import Optional
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from app.agents.memory.utils.postgres_utils import store_memory_in_db, retrieve_memory_from_db

class MemoryInput(BaseModel):
    user_id: str = Field(description='User ID for storing memory')
    memory_data: dict = Field(description='Memory data to store')

class MemoryInputSchema(BaseModel):
    params: MemoryInput

@tool(args_schema=MemoryInputSchema)
def store_memory(params: MemoryInput):
    '''
    Store memory data in the PostgreSQL database.

    Returns:
        dict: Result of the storage operation.
    '''
    try:
        result = store_memory_in_db(params.user_id, params.memory_data)
    except Exception as e:
        result = {"error": str(e)}
        
    return result