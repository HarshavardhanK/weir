from fastapi import APIRouter
from app.agents.image import ImageAgent
from pydantic import BaseModel

class ImageRequest(BaseModel):
    url: str

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello, World!"}

@router.post("/image")
async def image_url_endpoint(request: ImageRequest):
    print(request)
    image_agent = ImageAgent()
    return {"message": image_agent(request.url)}