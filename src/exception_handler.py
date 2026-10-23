

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.exceptions import NCPlusOneHTTPException
from src.db.exceptions import *
from asyncpg.exceptions import PostgresError

CODE_TO_MESSAGE = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "INVALID_INPUT",
}

DATABASE_EXCEPTION_TO_MESSAGE = {
    CreationFailedError: NCPlusOneHTTPException(status_code=400, detail="Creation failed"),
    AlreadyExistsError: NCPlusOneHTTPException(status_code=409, detail="Resource already exists"),
    DatabaseError: NCPlusOneHTTPException(status_code=400, detail="Database error"),
    PostgresError: NCPlusOneHTTPException(status_code=400, detail="Database error"),
}


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, HTTPException):
        exc = NCPlusOneHTTPException(status_code=500, detail="Internal server error")
        
    return custom_error_formatter(exc)

async def request_validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    exception = NCPlusOneHTTPException(status_code=422, detail="Invalid request data")
    return custom_error_formatter(exception)

async def database_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    exception = DATABASE_EXCEPTION_TO_MESSAGE.get(type(exc), None)
    if exception is None:
        exception = NCPlusOneHTTPException(status_code=500, detail="Internal server error")
    return custom_error_formatter(exception)



def custom_error_formatter(exc: HTTPException) -> JSONResponse:
    code_str = CODE_TO_MESSAGE.get(exc.status_code)
    
    return JSONResponse(
        status_code=exc.status_code,
        headers=getattr(exc, "headers", None),
        content={"detail": {"error": {"message": exc.detail, 
                                      "code": code_str if code_str else exc.status_code}}}
    )