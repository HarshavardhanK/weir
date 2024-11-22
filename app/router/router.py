from fastapi import APIRouter, HTTPException
from app.agents.image import ImageAgent
from pydantic import BaseModel
from app.agents.expander import expand_question
from app.agents.graph import call_agent
from langchain_core.messages import HumanMessage, ToolMessage

class ImageRequest(BaseModel):
    url: str

class QueryRequest(BaseModel):
    query: str

class ExpandRequest(BaseModel):
    question: str

class ExpandResponse(BaseModel):
    sub_questions: list[str]

class GraphRequest(BaseModel):
    message: str

class GraphResponse(BaseModel):
    result: dict

router = APIRouter()


#DEV SAMPLE ENDPOINTS

@router.get("/")
def read_root():
    return {"message": "Hello, World!"}

@router.post("/image")
async def image_url_endpoint(request: ImageRequest):
    print(request)
    image_agent = ImageAgent()
    
    #TODO: Think about persisting this to a database
    return {"message": image_agent(request.url)}

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    print(request)
    return {"message": "Query received"}


@router.post("/expand", response_model=ExpandResponse)
async def expand_question_endpoint(request: ExpandRequest):
    try:
        sub_questions = expand_question(request.question)
        return ExpandResponse(sub_questions=sub_questions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/graph", response_model=GraphResponse)
async def graph_endpoint(request: GraphRequest):
    try:
    
        print("Calling agent")
        result = call_agent(request.message, user_id="123", namespace="memories", thread_id="123")
        
        # Return the full result without extraction
        return GraphResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))