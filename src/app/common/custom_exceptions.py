class OperatorAlreadyExistsException(Exception):
    def __init__(self,email:str):
        self.email=email
        self.message=f"Operator with email '{email}' already exists."
        super().__init__(self.message)


class InvalidCredentialsException(Exception):
    def __init__(self,message:str):
        self.message=message
        super().__init__(self.message)

class OperatorNotFoundException(Exception):
   def __init__(self, message: str):
       self.message = message
       super().__init__(self.message)

class BusAlreadyExistsException(Exception):
    def __init__(self,number:str):
        self.number=number
        self.message=f"Bus with number '{number}' already exists."
        super().__init__(self.message)


class BusNotFoundException(Exception):
   def __init__(self, message: str):
       self.message = message
       super().__init__(self.message)


class SeatNotFoundException(Exception):
   def __init__(self, message: str):
       self.message = message
       super().__init__(self.message)

class RouteNotFoundException(Exception):
    def __init__(self, message: str):
       self.message = message
       super().__init__(self.message)