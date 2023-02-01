from abc import abstractmethod

class AST(type):

    def __new__(cls, name, *subclasses, **dict):
        dict = { '_fields': { } }
        return super().__new__(cls, name, subclasses, dict)

    def __getattr__(self, __field):
        return self.__dict__['_fields'][__field]

    def __setattr__(self, __name: str, __value):
        self.__dict__['_fields'][__name] = __value
