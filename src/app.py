

from fastapi import APIRouter, FastAPI
import uvicorn

from src.endpoints.events import router as events_router

app = FastAPI(title="NC+1 API")

default_router = APIRouter(prefix="/api") 
default_router.include_router(events_router)

app.include_router(default_router)

def run():
    uvicorn.run("src.app:app", reload=True)
