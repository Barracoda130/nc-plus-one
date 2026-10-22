

from fastapi import HTTPException

CODE_TO_MESSAGE = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "INVALID_INPUT",
}

class NCPlusOneError(Exception):
    """Base class for exceptions in this module."""
    pass

class NCPlusOneHTTPException(HTTPException):
    """Custom HTTP exception for NC Plus One."""
    def __init__(self, 
                 status_code: int, 
                 detail: str,
                 *args, **kwargs):
        code_str = CODE_TO_MESSAGE.get(status_code, "UNKNOWN_ERROR")
        custom_detail = {
            "error": {
                "code": code_str if code_str else status_code,
                "message": detail
            }
        }
        super().__init__(status_code=status_code, 
                         detail=custom_detail,
                         *args, **kwargs)
                         
                         