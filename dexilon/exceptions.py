class DexilonException(Exception):

    code: int = 0
    name: str = 'Error'
    message: str = ''

    def __str__(self) -> str:
        return '{}(code={}, message={})'.format(self.name, self.code, self.message)



class DexilonRequestException(DexilonException):

    code = -1
    name = 'RequestError'

    def __init__(self, message: str) -> None:
        self.message: str = message


class DexilonAPIException(DexilonException):

    code = 0
    name = 'APIError'

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class DexilonAuthException(Exception):

    code = 1
    name = 'AuthError'

    def __init__(self, message: str) -> None:
        self.message = message


class DexilonEventException(Exception):

    code = 2
    name = 'EventError'

    def __init__(self, message: str) -> None:
        self.message = message
