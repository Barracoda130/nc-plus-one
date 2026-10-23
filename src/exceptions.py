

from fastapi import HTTPException



class NCPlusOneError(Exception):
    """Base class for exceptions in this module."""
    pass

class NCPlusOneHTTPException(HTTPException):
    """Custom HTTP exception for NC Plus One."""
    pass
                         
                         