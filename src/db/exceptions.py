

from src.exceptions import NCPlusOneError

class DatabaseError(NCPlusOneError):
    """Base class for database-related exceptions."""
    pass

class CreationFailedError(DatabaseError):
    """Raised when a database creation operation fails."""
    pass

class AlreadyExistsError(CreationFailedError):
    """Raised when attempting to create a record that already exists."""
    pass