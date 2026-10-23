

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
import uvicorn

from src.endpoints.events import router as events_router
from src.endpoints.auth import router as auth_router
from src.exceptions import NCPlusOneHTTPException

app = FastAPI(title="NC+1 API")

default_router = APIRouter(prefix="/api") 
default_router.include_router(events_router)
default_router.include_router(auth_router)

app.include_router(default_router)

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, 
                                               exc: RequestValidationError):
    raise NCPlusOneHTTPException(status_code=422, detail="Invalid request data")

def run():
    uvicorn.run("src.app:app", reload=True)
