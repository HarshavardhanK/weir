from fastapi import APIRouter
from app.router import router


app = APIRouter()
app.include_router(router.router)