

import asyncpg
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from src.db.exceptions import DatabaseError
from src.endpoints.events import router as events_router
from src.endpoints.auth import router as auth_router
from src.exception_handler import http_exception_handler, request_validation_exception_handler, database_exception_handler
from src.exceptions import NCPlusOneHTTPException

app = FastAPI(title="NC+1 API")

default_router = APIRouter(prefix="/api") 
default_router.include_router(events_router)
default_router.include_router(auth_router)

app.include_router(default_router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(DatabaseError, database_exception_handler)
app.add_exception_handler(asyncpg.exceptions.PostgresError, database_exception_handler)


def run():
    uvicorn.run("src.app:app", reload=True)
