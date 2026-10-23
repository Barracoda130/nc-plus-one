

class BaseQuery:
    def __new__(cls):
        raise NotImplementedError("This class should not be instantiated")   
